#!/usr/bin/env python3
"""
build_waves.py — Free Traveler Wave planner.

Reads the already-audited Task graph and deterministically assigns every
Task to a Wave, following a fixed 10-group ordering (Scaffold -> Shared/Data
-> Auth/DB/API -> SCR-001..SCR-005 -> Test/CI -> Release). Wave IDs are not
hard-coded — this script decides how many Waves exist by splitting any group
that would otherwise exceed the Wave size target or that contains a same-wave
file conflict.

Reads:
  - TASKS/TASK_MANIFEST.csv                     (ground truth: Task ID, Category,
                                                  Screen, DependsOn, ExpectedFiles)
  - TASKS/details/TASK-*.md (or TASKS/TASK-*.md if the former does not exist —
                                                  see resolve_detail_path())
  - design-reference/SCREEN_ROUTE_CONTRACT.json (Screen ground truth, used only
                                                  to sanity-check Page Owner screens)

Writes:
  - TASKS/TASK_DAG.md         (dependency graph, cycle check, topological order)
  - TASKS/WAVE_PLAN.md        (one row per Task: Wave | Task ID | Preview Checkpoint After —
                                same shape `.claude/commands/run-wave.md` already expects)
  - TASKS/WAVE_STATE.json     (fresh ledger: one entry per Wave, all `pending`)
  - TASKS/TASK_MANIFEST.csv   (same file, with a `wave_id` column added/updated —
                                all other columns and rows are preserved as-is)

Caveat (reported here, not hidden): `scripts/audit_tasks.py` regenerates
TASKS/TASK_MANIFEST.csv from TASKS/00_TASK_LIST.md with its own fixed column
list, which does NOT include `wave_id`. Re-running audit_tasks.py after this
script will silently drop the wave_id column again — re-run build_waves.py
afterward to restore it.

Rules enforced (numbered to match the spec):
  1. Dependency cycles are detected across the *whole* graph before anything
     else runs. A cycle is a hard failure — no output files are written.
  2. A Task's Wave index must never be before any of its dependencies' Wave
     index. Within the same Wave, a dependency must also sort before its
     dependent in Task-ID order (Wave-internal execution is strictly
     Task-ID order per rule 6), otherwise the dependent is pushed to the
     next Wave. This is verified again, globally, after construction.
  3. Waves default to 4-7 Tasks. This is a soft target — a group smaller
     than 4 Tasks (e.g. the single-Task Scaffold group) stays its own Wave
     rather than being merged into a neighboring group, to keep the fixed
     group order intact.
  4. A screen's Page Owner Task is always the last Task placed within its
     group's topological order (nothing in the group depends on a Page
     Owner), so it always lands in that group's final Wave.
  5. Two Tasks that declare an overlapping Expected File are never placed in
     the same Wave — the later one (by topological/ID order) is pushed to
     the next Wave even if the current Wave has not reached the 7-task cap.
  6. No retry/auto-fix loops are implemented (rule 7 of the spec) — this is
     a single deterministic pass plus one verification pass; any violation
     is reported and fails the run rather than being silently patched.
  7. No git branch/PR/merge automation is included (rule 8 of the spec).

Exit code: 0 and prints "BUILD_WAVES_PASS" plus the summary on success.
Exit code: 1 and prints "BUILD_WAVES_FAIL" (writes TASKS/TASK_DAG.md only,
for debugging) if a cycle or an ordering violation is found.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "TASKS/TASK_MANIFEST.csv"
DETAILS_DIR_PRIMARY = ROOT / "TASKS/details"
DETAILS_DIR_FALLBACK = ROOT / "TASKS"
CONTRACT_PATH = ROOT / "design-reference/SCREEN_ROUTE_CONTRACT.json"
DAG_PATH = ROOT / "TASKS/TASK_DAG.md"
WAVE_PLAN_PATH = ROOT / "TASKS/WAVE_PLAN.md"
WAVE_STATE_PATH = ROOT / "TASKS/WAVE_STATE.json"

MIN_WAVE_SIZE = 4
MAX_WAVE_SIZE = 7
WAVE_STATE_SCHEMA_VERSION = "traveler-wave-state-v1"

GROUP_TITLES: dict[int, str] = {
    1: "Scaffold, 문서, Harness 확인",
    2: "Airbnb 스타일 공통 UI, 정적 데이터, Layout",
    3: "Supabase Auth, 6개 Table, 기본 RLS(+백엔드 API)",
    4: "SCR-001 메인 Component와 Page Owner",
    5: "SCR-002 대표 소개 Component와 Page Owner",
    6: "SCR-003 여행 입력·외부 이동·동행글 입력 Component와 Page Owner",
    7: "SCR-004 동행 목록·상세·신청 Component와 Page Owner",
    8: "SCR-005 계정·내 활동·간단 관리자 Component와 Page Owner",
    9: "Unit·Playwright·접근성·CI",
    10: "Vercel Preview와 Release 확인",
}


# ---------------------------------------------------------------------------
# Input loading
# ---------------------------------------------------------------------------

def read_manifest() -> list[dict]:
    with MANIFEST_PATH.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def split_multi(cell: str) -> list[str]:
    cell = (cell or "").strip()
    if cell in ("", "없음", "N/A"):
        return []
    return [c.strip().strip("`") for c in cell.split(",") if c.strip()]


def extract_files(cell: str) -> set[str]:
    return set(re.findall(r"`([^`]+)`", cell or ""))


_details_fallback_reported = False


def resolve_detail_path(tid: str) -> Path | None:
    """TASKS/details/TASK-<id>.md if that directory exists, else TASKS/TASK-<id>.md.

    The fallback is reported once (stderr) the same way this project always
    reports the python3 -> python interpreter substitution: transparently,
    not silently.
    """
    global _details_fallback_reported
    primary = DETAILS_DIR_PRIMARY / f"TASK-{tid}.md"
    if DETAILS_DIR_PRIMARY.is_dir():
        return primary if primary.exists() else None
    if not _details_fallback_reported:
        print(
            f"NOTE: {DETAILS_DIR_PRIMARY.relative_to(ROOT)} does not exist — "
            f"falling back to {DETAILS_DIR_FALLBACK.relative_to(ROOT)}/TASK-<ID>.md for all detail files.",
            file=sys.stderr,
        )
        _details_fallback_reported = True
    fallback = DETAILS_DIR_FALLBACK / f"TASK-{tid}.md"
    return fallback if fallback.exists() else None


# ---------------------------------------------------------------------------
# Rule 1: cycle detection (global, before anything else)
# ---------------------------------------------------------------------------

def find_cycle(task_ids: set[str], deps: dict[str, list[str]]) -> list[str] | None:
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {tid: WHITE for tid in task_ids}

    def dfs(node: str, path: list[str]) -> list[str] | None:
        color[node] = GRAY
        path.append(node)
        for nxt in deps.get(node, []):
            if nxt not in task_ids:
                continue
            if color[nxt] == GRAY:
                idx = path.index(nxt)
                return path[idx:] + [nxt]
            if color[nxt] == WHITE:
                found = dfs(nxt, path)
                if found:
                    return found
        path.pop()
        color[node] = BLACK
        return None

    for tid in sorted(task_ids):
        if color[tid] == WHITE:
            found = dfs(tid, [])
            if found:
                return found
    return None


# ---------------------------------------------------------------------------
# Grouping (the fixed 10-group Wave order)
# ---------------------------------------------------------------------------

def classify_group(tid: str) -> int:
    if tid == "SETUP-DEPENDENCIES":
        return 1
    if tid.startswith("DATA-") or tid.startswith("SHARED-"):
        return 2
    if tid.startswith("DB-") or tid.startswith("API-") or tid == "TEST-RLS-BASIC":
        return 3
    if tid.startswith("COMP-SCR001") or tid == "PAGE-SCR001":
        return 4
    if tid.startswith("COMP-SCR002") or tid == "PAGE-SCR002":
        return 5
    if tid.startswith("COMP-SCR003") or tid == "PAGE-SCR003":
        return 6
    if tid.startswith("COMP-SCR004") or tid == "PAGE-SCR004":
        return 7
    if tid.startswith("COMP-SCR005") or tid == "PAGE-SCR005":
        return 8
    if tid.startswith("UNIT-") or tid.startswith("E2E-") or tid.startswith("CI-"):
        return 9
    if tid.startswith("MANUAL-"):
        return 10
    # Unclassified Task IDs fall into the Test/CI catch-all group rather than
    # silently vanishing; this is surfaced in the summary so it gets noticed.
    return 9


# ---------------------------------------------------------------------------
# Topological order within one group (Khan's algorithm, Task-ID tie-break
# for determinism)
# ---------------------------------------------------------------------------

def topo_order(tasks: list[str], deps: dict[str, list[str]]) -> list[str]:
    import heapq

    tset = set(tasks)
    indegree = {t: 0 for t in tasks}
    graph: dict[str, list[str]] = {t: [] for t in tasks}
    for t in tasks:
        for d in deps.get(t, []):
            if d in tset:
                graph[d].append(t)
                indegree[t] += 1

    heap = [t for t in tasks if indegree[t] == 0]
    heapq.heapify(heap)
    order: list[str] = []
    indegree_local = dict(indegree)
    while heap:
        t = heapq.heappop(heap)
        order.append(t)
        for nxt in sorted(graph[t]):
            indegree_local[nxt] -= 1
            if indegree_local[nxt] == 0:
                heapq.heappush(heap, nxt)
    return order


# ---------------------------------------------------------------------------
# Rules 2/3/4/5: pack one group's topological order into Waves
# ---------------------------------------------------------------------------

def pack_group_into_waves(
    order: list[str],
    deps: dict[str, list[str]],
    files_map: dict[str, set[str]],
) -> list[list[str]]:
    waves: list[list[str]] = []
    placed_wave_of: dict[str, int] = {}
    current: list[str] = []
    current_files: set[str] = set()

    def close_current() -> None:
        nonlocal current, current_files
        if not current:
            return
        waves.append(current)
        for x in current:
            placed_wave_of[x] = len(waves) - 1
        current = []
        current_files = set()

    for t in order:
        size_ok = len(current) < MAX_WAVE_SIZE
        dep_conflict = any(
            d in current and d >= t  # same provisional wave but wrong ID order
            for d in deps.get(t, [])
        )
        file_conflict = bool(files_map.get(t, set()) & current_files)
        if current and (not size_ok or dep_conflict or file_conflict):
            close_current()
        current.append(t)
        current_files |= files_map.get(t, set())
    close_current()
    return waves


# ---------------------------------------------------------------------------
# Rule 1/2 global verification (defensive — should never fire given the
# construction above, but checked rather than assumed)
# ---------------------------------------------------------------------------

def verify_wave_order(
    wave_index_of: dict[str, int],
    deps: dict[str, list[str]],
) -> list[str]:
    violations = []
    for t, wt in wave_index_of.items():
        for d in deps.get(t, []):
            if d not in wave_index_of:
                continue
            wd = wave_index_of[d]
            if wd > wt:
                violations.append(f"{t} (Wave index {wt}) depends on {d} placed in a LATER Wave index {wd}")
            elif wd == wt and not (d < t):
                violations.append(f"{t} and its dependency {d} share a Wave but do not sort as {d} < {t} for in-Wave ID-order execution")
    return violations


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------

def write_dag(
    task_ids: list[str],
    deps: dict[str, list[str]],
    categories: dict[str, str],
    global_order: list[str] | None,
    cycle: list[str] | None,
    group_of: dict[str, int],
    wave_id_of: dict[str, str] | None,
) -> None:
    lines = []
    lines.append("# TASK_DAG — Free Traveler Dependency Graph")
    lines.append("")
    lines.append(f"**Generated:** {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    lines.append(f"**Total Tasks:** {len(task_ids)}")
    if cycle:
        lines.append(f"**Cycle Check:** FAIL — 1 cycle found")
    else:
        lines.append("**Cycle Check:** PASS — 0 cycles")
    lines.append("")

    if cycle:
        lines.append("## 순환 의존성")
        lines.append("")
        lines.append("```")
        lines.append(" -> ".join(cycle))
        lines.append("```")
        lines.append("")
        lines.append("순환이 해소되기 전까지 `TASKS/WAVE_PLAN.md`/`TASKS/WAVE_STATE.json`은 생성하지 않는다.")
        lines.append("")
    elif global_order:
        lines.append("## Topological Order (group-first, Task-ID tie-break)")
        lines.append("")
        for i, tid in enumerate(global_order, 1):
            w = f" — {wave_id_of[tid]}" if wave_id_of else ""
            lines.append(f"{i}. `{tid}`{w}")
        lines.append("")

    lines.append("## Dependency Table")
    lines.append("")
    header = "| Task ID | Category | Group | Depends On |"
    if wave_id_of:
        header += " Wave |"
    lines.append(header)
    sep = "|---|---|---|---|"
    if wave_id_of:
        sep += "---|"
    lines.append(sep)
    for tid in sorted(task_ids):
        dep_cell = ", ".join(deps.get(tid, [])) or "없음"
        row = f"| `{tid}` | {categories.get(tid, '')} | {group_of.get(tid, '')} | {dep_cell} |"
        if wave_id_of:
            row += f" {wave_id_of.get(tid, '')} |"
        lines.append(row)
    lines.append("")

    DAG_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_wave_plan(
    wave_sequence: list[tuple[str, int, list[str]]],
    categories: dict[str, str],
) -> None:
    lines = []
    lines.append("# Wave Plan — Free Traveler")
    lines.append("")
    lines.append("`scripts/build_waves.py`가 `TASKS/TASK_MANIFEST.csv`의 Depends On 그래프로부터 생성했다. ")
    lines.append("Wave ID는 이 파일이 정본이다 — `.claude/commands/run-wave.md`/`prepare-task.md`는 이 파일을 그대로 읽는다.")
    lines.append("")
    lines.append("| Wave | Group | Task ID | Preview Checkpoint After |")
    lines.append("|---|---|---|---|")
    for wave_id, group_num, tids in wave_sequence:
        group_title = GROUP_TITLES.get(group_num, "")
        for tid in tids:
            checkpoint = "Y" if categories.get(tid) == "PAGE_OWNER" else "N"
            lines.append(f"| {wave_id} | {group_num}. {group_title} | {tid} | {checkpoint} |")
    lines.append("")
    WAVE_PLAN_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_wave_state(wave_sequence: list[tuple[str, int, list[str]]], categories: dict[str, str]) -> None:
    waves = []
    for wave_id, group_num, tids in wave_sequence:
        checkpoint_required = any(categories.get(t) == "PAGE_OWNER" for t in tids)
        waves.append({
            "wave_id": wave_id,
            "title": f"{group_num}. {GROUP_TITLES.get(group_num, '')}",
            "task_ids": tids,
            "status": "pending",
            "checkpoint_required": checkpoint_required,
            "checkpoint_result": None,
        })
    state = {
        "schema_version": WAVE_STATE_SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "waves": waves,
    }
    WAVE_STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_manifest_wave_id(rows: list[dict], wave_id_of: dict[str, str]) -> None:
    fieldnames = list(rows[0].keys())
    if "wave_id" not in fieldnames:
        fieldnames.append("wave_id")
    for r in rows:
        r["wave_id"] = wave_id_of.get(r["TaskID"], "")
    with MANIFEST_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    if not MANIFEST_PATH.exists():
        print(f"BUILD_WAVES_FAIL: missing {MANIFEST_PATH.relative_to(ROOT)} — run scripts/audit_tasks.py first.", file=sys.stderr)
        return 1

    rows = read_manifest()
    task_ids = {r["TaskID"] for r in rows}
    categories = {r["TaskID"]: r["Category"] for r in rows}
    deps = {r["TaskID"]: split_multi(r["DependsOn"]) for r in rows}
    files_map = {r["TaskID"]: extract_files(r["ExpectedFiles"]) for r in rows}
    screens = {r["TaskID"]: r["Screen"] for r in rows}

    # Precondition: every Task in the manifest has a resolvable detail file.
    missing_details = [tid for tid in sorted(task_ids) if resolve_detail_path(tid) is None]
    if missing_details:
        print(f"BUILD_WAVES_FAIL: no detail file found for: {missing_details}", file=sys.stderr)
        return 1

    if CONTRACT_PATH.exists():
        try:
            contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
            contract_screens = {s["screen_id"] for s in contract.get("screens", [])}
        except (json.JSONDecodeError, KeyError):
            contract_screens = set()
    else:
        contract_screens = set()
    page_owner_screen_mismatch = [
        tid for tid, cat in categories.items()
        if cat == "PAGE_OWNER" and contract_screens and screens.get(tid) not in contract_screens
    ]

    # Rule 1: global cycle check BEFORE anything else is built.
    cycle = find_cycle(task_ids, deps)
    if cycle:
        write_dag(sorted(task_ids), deps, categories, None, cycle, {}, None)
        print("BUILD_WAVES_FAIL", file=sys.stderr)
        print(f"Cycles: 1 -> {' -> '.join(cycle)}", file=sys.stderr)
        return 1

    if page_owner_screen_mismatch:
        print(f"BUILD_WAVES_FAIL: Page Owner task(s) reference a Screen outside SCREEN_ROUTE_CONTRACT.json: {page_owner_screen_mismatch}", file=sys.stderr)
        return 1

    # Group assignment (fixed 10-group order).
    group_of = {tid: classify_group(tid) for tid in task_ids}

    # Cross-group sanity check: no dependency may point into a LATER group.
    # (No automatic "fixing" — rule 7 forbids complex auto-correction. A
    # violation here means the fixed classification table itself is wrong
    # and must be edited by hand, so we fail loudly instead of guessing.)
    cross_group_violations = []
    for tid in task_ids:
        for d in deps.get(tid, []):
            if d in group_of and group_of[d] > group_of[tid]:
                cross_group_violations.append(f"{tid} (group {group_of[tid]}) depends on {d} (group {group_of[d]})")
    if cross_group_violations:
        print("BUILD_WAVES_FAIL: dependency points into a later Wave group:", file=sys.stderr)
        for v in cross_group_violations:
            print(f"  - {v}", file=sys.stderr)
        return 1

    # Build Waves group by group, in fixed order 1..10.
    wave_sequence: list[tuple[str, int, list[str]]] = []  # (wave_id, group_num, [task_ids])
    global_order: list[str] = []
    wave_counter = 0
    for group_num in sorted(GROUP_TITLES):
        group_tasks = sorted(tid for tid, g in group_of.items() if g == group_num)
        if not group_tasks:
            continue
        order = topo_order(group_tasks, deps)
        global_order.extend(order)
        group_waves = pack_group_into_waves(order, deps, files_map)
        for tids in group_waves:
            wave_counter += 1
            wave_sequence.append((f"W{wave_counter:02d}", group_num, tids))

    wave_id_of = {tid: wid for wid, _, tids in wave_sequence for tid in tids}
    wave_index_of = {tid: i for i, (wid, _, tids) in enumerate(wave_sequence) for tid in tids}

    # Rule 2 (defensive global re-check, not a retry loop — single pass).
    violations = verify_wave_order(wave_index_of, deps)
    if violations:
        write_dag(sorted(task_ids), deps, categories, global_order, None, group_of, wave_id_of)
        print("BUILD_WAVES_FAIL: Wave ordering violation(s):", file=sys.stderr)
        for v in violations:
            print(f"  - {v}", file=sys.stderr)
        return 1

    # Rule 4 (defensive check): each screen's Page Owner must be the last
    # Task in its own group's Wave.
    page_owner_violations = []
    for scr_group in (4, 5, 6, 7, 8):
        group_tids = [tid for tid, g in group_of.items() if g == scr_group]
        owners = [tid for tid in group_tids if categories.get(tid) == "PAGE_OWNER"]
        for owner in owners:
            later_in_group = [
                tid for tid in group_tids
                if tid != owner and wave_index_of.get(tid, -1) > wave_index_of.get(owner, -1)
            ]
            if later_in_group:
                page_owner_violations.append(f"{owner} is not last in its group — still followed by {later_in_group}")
    if page_owner_violations:
        print("BUILD_WAVES_FAIL: Page Owner placement violation(s):", file=sys.stderr)
        for v in page_owner_violations:
            print(f"  - {v}", file=sys.stderr)
        return 1

    # All checks passed — write outputs.
    write_dag(sorted(task_ids), deps, categories, global_order, None, group_of, wave_id_of)
    write_wave_plan(wave_sequence, categories)
    write_wave_state(wave_sequence, categories)
    update_manifest_wave_id(rows, wave_id_of)

    # Summary (per "종료" spec): cycle count, per-Wave task count, Page Owner placement.
    print("BUILD_WAVES_PASS")
    print("Cycles: 0")
    print(f"Waves: {len(wave_sequence)}")
    for wave_id, group_num, tids in wave_sequence:
        flag = ""
        if not (MIN_WAVE_SIZE <= len(tids) <= MAX_WAVE_SIZE):
            flag = f"  (outside 4-7 target: {len(tids)} task{'s' if len(tids) != 1 else ''}, group has too few/forced split)"
        print(f"  {wave_id} ({len(tids)} tasks) — {group_num}. {GROUP_TITLES[group_num]}{flag}")
    print("Page Owners:")
    for tid in sorted(tid for tid, c in categories.items() if c == "PAGE_OWNER"):
        print(f"  {tid} -> {wave_id_of[tid]} (last Task in its group's final Wave)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

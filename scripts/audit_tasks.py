#!/usr/bin/env python3
"""
audit_tasks.py — Free Traveler Task Pipeline final audit.

Reads:
  - TASKS/00_TASK_LIST.md                       (Task List table + NON_IMPLEMENTATION table)
  - TASKS/TASK-*.md                             (one detail file per Task)
  - docs/PROJECT_SCOPE.md                       (referenced for the 6-table DB rule)
  - design-reference/SCREEN_ROUTE_CONTRACT.json (Screen/Route/Page Entry ground truth)

Writes:
  - TASKS/TASK_MANIFEST.csv       (one row per Task List entry)
  - TASKS/TASK_AUDIT_REPORT.md    (human-readable report of all 18 checks)

Read-only with respect to TASKS/00_TASK_LIST.md and TASKS/TASK-*.md — never
mutates them. Only the two output files above are written/overwritten.

Checks (numbered to match the audit spec):
   1. Task List implementation IDs and TASK-*.md detail files are 1:1.
   2. Zero duplicate Task IDs.
   3. Zero missing Depends On (every reference resolves to a real Task ID).
   4. Zero dependency cycles.
   5. All 5 Screens have exactly one Page Owner Task each.
   6. Route / Page Entry / Expected Files are consistent with
      design-reference/SCREEN_ROUTE_CONTRACT.json.
   7. Zero "Component-only" Screens (a Screen with Component tasks but no
      Page Owner, or a Component task on a Screen outside the approved 5).
   8. SCR-001 has a starter-template-removal Acceptance Criterion.
   9. SCR-003 has an AC that assembles all three tabs (flight/hotel/mate).
  10. SCR-005 has an AC that assembles per-role (Guest/Member/Admin) state.
  11. DB Schema / RLS / Access / Seed tasks all exist.
  12. DB table count does not greatly exceed the 6-table baseline.
  13. External input (flight/hotel) non-persistence AC exists.
  14. Auth / adult-verification / baseline RLS AC exists.
  15. Exactly one Playwright Chromium Smoke task set (3 named E2E tasks) exists.
  16. Zero AWS / EC2 / auto-merge-runner implementation tasks.
  17. All REQ-FUNC (80) and REQ-NF (34) requirements exist in the Task List or
      the EXCLUDED (NON_IMPLEMENTATION) table.
  18. No detail implementation file exists for an EXCLUDED requirement.

Exit code: 0 and prints "AUDIT_PASS" + check count if every check passes.
Exit code: 1 if any check fails (also prints AUDIT_FAIL + which checks failed).
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASK_LIST_PATH = ROOT / "TASKS/00_TASK_LIST.md"
TASKS_DIR = ROOT / "TASKS"
CONTRACT_PATH = ROOT / "design-reference/SCREEN_ROUTE_CONTRACT.json"
PROJECT_SCOPE_PATH = ROOT / "docs/PROJECT_SCOPE.md"
MANIFEST_PATH = ROOT / "TASKS/TASK_MANIFEST.csv"
REPORT_PATH = ROOT / "TASKS/TASK_AUDIT_REPORT.md"

REQUIRED_TABLE_COLS = 11
DB_TABLE_BASELINE = 6
DB_TABLE_TOLERANCE = 2  # "크게 넘지 않음" — fail only once it clearly overshoots the baseline
REQUIRED_DB_TASK_IDS = ["DB-SCHEMA-BASE", "DB-RLS-BASE", "DB-ACCESS", "DB-SEED-BASE"]
REQUIRED_E2E_TASK_IDS = ["E2E-MATE-AUTH", "E2E-PUBLIC-SMOKE", "E2E-TRAVEL-TOOLS"]
FORBIDDEN_KEYWORDS = [
    "EC2", "AWS", "자동 병합", "자동병합",
    "Auto Merge", "Auto-Merge", "AutoMerge", "merge runner", "Merge Runner",
]


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

def parse_task_rows(text: str) -> list[list[str]]:
    rows = []
    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        if "Seq" in stripped or set(stripped) <= set("|- "):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) != REQUIRED_TABLE_COLS or not cells[0].isdigit():
            continue
        rows.append(cells)
    return rows


def rows_to_dict(rows: list[list[str]]) -> dict[str, dict]:
    by_id = {}
    for r in rows:
        seq, tid, title, cat, impl, reqref, screen, route, page_entry, deps, files = r
        by_id[tid] = dict(
            seq=seq, title=title, category=cat, impl=impl, reqref=reqref,
            screen=screen, route=route, page_entry=page_entry, depends=deps, files=files,
        )
    return by_id


def expand_req_ids(cell_text: str) -> set[str]:
    ids: set[str] = set()
    pattern = re.compile(r"REQ-(FUNC|NF)-(\d{3})((?:[,~]\s*\d{3}(?:\([^)]*\))?)*)")
    for m in pattern.finditer(cell_text):
        kind, first, rest = m.group(1), m.group(2), m.group(3)
        tokens = re.findall(r"([,~])\s*(\d{3})", rest)
        seq = [(None, int(first))] + [(s, int(n)) for s, n in tokens]
        for idx in range(len(seq)):
            sep, n = seq[idx]
            if sep == "~":
                start = seq[idx - 1][1]
                for x in range(start, n + 1):
                    ids.add(f"REQ-{kind}-{x:03d}")
            else:
                ids.add(f"REQ-{kind}-{n:03d}")
    return ids


def parse_non_implementation(text: str) -> set[str]:
    marker = "## NON_IMPLEMENTATION"
    if marker not in text:
        return set()
    segment = text.split(marker, 1)[1]
    segment = segment.split("## Release Check")[0]
    ids: set[str] = set()
    for line in segment.split("\n"):
        if line.strip().startswith("|"):
            ids |= expand_req_ids(line)
    return ids


def detail_text(task_id: str) -> str:
    path = TASKS_DIR / f"TASK-{task_id}.md"
    return path.read_text(encoding="utf-8") if path.exists() else ""


def detail_text_excluding_forbidden(task_id: str) -> str:
    """detail_text minus the '## Forbidden' section.

    The Forbidden section deliberately *names* things like EC2/AWS/Firefox as
    things NOT to do, so "is this being planned" scans must not look inside
    it, or every task false-positives on its own prohibition list.
    """
    return detail_text(task_id).split("## Forbidden")[0]


def detail_priority(task_id: str) -> str:
    t = detail_text(task_id)
    m = re.search(r"\*\*Priority:\*\*\s*(\S+)", t)
    return m.group(1) if m else ""


def split_multi(cell: str) -> list[str]:
    return [c.strip().strip("`") for c in cell.split(",") if c.strip()]


# ---------------------------------------------------------------------------
# Check result bookkeeping
# ---------------------------------------------------------------------------

class Check:
    def __init__(self, num: int, name: str, description: str):
        self.num = num
        self.name = name
        self.description = description
        self.status = "PASS"
        self.violations: list[str] = []

    def fail(self, msg: str) -> None:
        self.status = "FAIL"
        self.violations.append(msg)

    def as_dict(self) -> dict:
        return {
            "num": self.num, "name": self.name, "description": self.description,
            "status": self.status, "violations": self.violations,
        }


def main() -> int:
    checks: list[Check] = []
    extra_data: dict = {}

    if not TASK_LIST_PATH.exists():
        c = Check(0, "PRECONDITION", "TASKS/00_TASK_LIST.md must exist")
        c.fail(f"file not found: {TASK_LIST_PATH.relative_to(ROOT)}")
        checks.append(c)
        write_outputs(checks, {}, {}, extra_data)
        print("AUDIT_FAIL", file=sys.stderr)
        return 1

    text = TASK_LIST_PATH.read_text(encoding="utf-8")
    rows = parse_task_rows(text)
    by_id = rows_to_dict(rows)

    contract = {}
    if CONTRACT_PATH.exists():
        try:
            contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            contract = {}
    contract_screens = {s.get("screen_id"): s for s in contract.get("screens", [])}

    detail_files = {p.name[len("TASK-"):-len(".md")] for p in TASKS_DIR.glob("TASK-*.md")}
    task_ids = set(by_id.keys())

    # 1. Task List <-> detail files 1:1
    c1 = Check(1, "TASK_LIST_DETAIL_1TO1", "Task List implementation IDs and TASK-*.md files are 1:1")
    missing_details = sorted(task_ids - detail_files)
    orphan_details = sorted(detail_files - task_ids)
    if missing_details:
        c1.fail(f"tasks with no detail file: {missing_details}")
    if orphan_details:
        c1.fail(f"detail files with no matching task: {orphan_details}")
    checks.append(c1)

    # 2. No duplicate Task IDs
    c2 = Check(2, "NO_DUPLICATE_TASK_IDS", "Zero duplicate Task IDs")
    ids_list = [r[1] for r in rows]
    dupes = sorted({i for i in ids_list if ids_list.count(i) > 1})
    if dupes:
        c2.fail(f"duplicate task ids: {dupes}")
    checks.append(c2)

    # 3. Depends On resolves
    c3 = Check(3, "DEPENDS_ON_RESOLVES", "Zero missing Depends On references")
    for tid, row in by_id.items():
        deps_raw = row["depends"]
        if deps_raw in ("없음", "N/A"):
            continue
        for d in [d.strip() for d in deps_raw.split(",")]:
            if d and d not in task_ids:
                c3.fail(f"{tid} depends on unknown task '{d}'")
    checks.append(c3)

    # 4. No dependency cycles
    c4 = Check(4, "NO_DEPENDENCY_CYCLE", "Zero dependency cycles")
    graph: dict[str, list[str]] = {}
    for tid, row in by_id.items():
        deps_raw = row["depends"]
        deps = [] if deps_raw in ("없음", "N/A") else [d.strip() for d in deps_raw.split(",") if d.strip() in task_ids]
        graph[tid] = deps

    WHITE, GRAY, BLACK = 0, 1, 2
    color = {tid: WHITE for tid in graph}
    cycle_found: list[str] = []

    def dfs(node: str, path: list[str]) -> bool:
        color[node] = GRAY
        path.append(node)
        for nxt in graph.get(node, []):
            if color.get(nxt, WHITE) == GRAY:
                idx = path.index(nxt)
                cycle_found.append(" -> ".join(path[idx:] + [nxt]))
                return True
            if color.get(nxt, WHITE) == WHITE:
                if dfs(nxt, path):
                    return True
        path.pop()
        color[node] = BLACK
        return False

    for tid in graph:
        if color[tid] == WHITE:
            if dfs(tid, []):
                break
    if cycle_found:
        c4.fail(f"dependency cycle detected: {cycle_found[0]}")
    checks.append(c4)

    # 5. Exactly one Page Owner per Screen (5 screens)
    c5 = Check(5, "SCREEN_PAGE_OWNER_COUNT", "All 5 Screens have exactly one Page Owner Task each")
    expected_screens = [f"SCR-{i:03d}" for i in range(1, 6)]
    page_owners = {tid: row for tid, row in by_id.items() if row["category"] == "PAGE_OWNER"}
    owners_by_screen: dict[str, list[str]] = {}
    for tid, row in page_owners.items():
        owners_by_screen.setdefault(row["screen"], []).append(tid)
    for scr in expected_screens:
        got = owners_by_screen.get(scr, [])
        if len(got) != 1:
            c5.fail(f"{scr} has {len(got)} Page Owner task(s): {got}")
    extra_owner_screens = set(owners_by_screen) - set(expected_screens)
    if extra_owner_screens:
        c5.fail(f"Page Owner tasks for unexpected screens: {sorted(extra_owner_screens)}")
    checks.append(c5)

    # 6. Route / Page Entry / Expected Files match SCREEN_ROUTE_CONTRACT.json
    c6 = Check(6, "ROUTE_PAGE_ENTRY_EXPECTED_FILES_MATCH", "Route/Page Entry/Expected Files consistent with SCREEN_ROUTE_CONTRACT.json")
    if not contract_screens:
        c6.fail(f"could not load {CONTRACT_PATH.relative_to(ROOT)}")
    else:
        for tid, row in by_id.items():
            screens = split_multi(row["screen"]) if row["screen"] not in ("N/A", "전역") else []
            routes = split_multi(row["route"]) if row["route"] not in ("N/A", "전역", "전체(5개 Route 공통)") else []
            valid_screens = [s for s in screens if s in contract_screens]
            if not valid_screens:
                continue
            allowed_routes = {contract_screens[s]["route"] for s in valid_screens}
            for r_ in routes:
                if r_ not in allowed_routes and not r_.endswith(".ts"):
                    c6.fail(f"{tid}: route '{r_}' not in contract routes {sorted(allowed_routes)} for screen(s) {valid_screens}")
        for tid, row in page_owners.items():
            scr = row["screen"]
            contract_entry = contract_screens.get(scr, {})
            expected_entry = contract_entry.get("page_entry", "")
            actual_entry = row["page_entry"].strip("`")
            if expected_entry and actual_entry != expected_entry:
                c6.fail(f"{tid}: page_entry '{actual_entry}' != contract page_entry '{expected_entry}' for {scr}")
            if expected_entry and expected_entry not in row["files"]:
                c6.fail(f"{tid}: Expected Files does not reference page_entry '{expected_entry}'")
    checks.append(c6)

    # 7. No Component-only Screen
    c7 = Check(7, "NO_COMPONENT_ONLY_SCREEN", "Zero Screens with Component tasks but no Page Owner (or outside the approved 5)")
    component_screens: set[str] = set()
    for tid, row in by_id.items():
        if row["category"] == "COMPONENT":
            for s in split_multi(row["screen"]):
                component_screens.add(s)
    for s in sorted(component_screens):
        if s not in expected_screens:
            c7.fail(f"Component task references screen '{s}' outside the approved 5 screens")
        elif s not in owners_by_screen:
            c7.fail(f"Screen '{s}' has Component task(s) but no Page Owner task")
    checks.append(c7)

    # 8. SCR-001 starter removal AC
    c8 = Check(8, "SCR001_STARTER_REMOVAL_AC", "SCR-001 has a starter-template-removal Acceptance Criterion")
    t = detail_text("PAGE-SCR001")
    if not t:
        c8.fail("TASK-PAGE-SCR001.md not found")
    elif not re.search(r"스타터|starter", t, re.IGNORECASE):
        c8.fail("no mention of starter-template removal in TASK-PAGE-SCR001.md")
    checks.append(c8)

    # 9. SCR-003 three-tab assembly AC
    c9 = Check(9, "SCR003_THREE_TAB_ASSEMBLY_AC", "SCR-003 has an AC assembling all three tabs")
    t = detail_text("PAGE-SCR003")
    if not t:
        c9.fail("TASK-PAGE-SCR003.md not found")
    else:
        for kw in ["항공", "숙소", "동행"]:
            if kw not in t:
                c9.fail(f"TASK-PAGE-SCR003.md missing mention of '{kw}'")
    checks.append(c9)

    # 10. SCR-005 role-based assembly AC
    c10 = Check(10, "SCR005_ROLE_STATE_ASSEMBLY_AC", "SCR-005 has an AC assembling per-role (Guest/Member/Admin) state")
    t = detail_text("PAGE-SCR005")
    if not t:
        c10.fail("TASK-PAGE-SCR005.md not found")
    else:
        for en, ko in [("Guest", "게스트"), ("Member", "회원"), ("Admin", "관리자")]:
            if en not in t and ko not in t:
                c10.fail(f"TASK-PAGE-SCR005.md mentions neither '{en}' nor '{ko}'")
    checks.append(c10)

    # 11. DB Schema/RLS/Access/Seed tasks exist
    c11 = Check(11, "DB_SCHEMA_RLS_ACCESS_SEED_EXIST", "DB Schema / RLS / Access / Seed Tasks all exist")
    for rid in REQUIRED_DB_TASK_IDS:
        if rid not in by_id:
            c11.fail(f"required DB task '{rid}' not found in Task List")
        elif by_id[rid]["category"] != "DB":
            c11.fail(f"'{rid}' exists but category is '{by_id[rid]['category']}', expected 'DB'")
    checks.append(c11)

    # 12. DB table count does not greatly exceed 6
    c12 = Check(12, "DB_TABLE_COUNT_NEAR_BASELINE", f"DB table count does not greatly exceed the {DB_TABLE_BASELINE}-table baseline")
    t = detail_text("DB-SCHEMA-BASE")
    table_names: list[str] = []
    if not t:
        c12.fail("TASK-DB-SCHEMA-BASE.md not found")
    else:
        m = re.search(r"정확히\s*6개로?\s*제한\s*—?\s*(.+)", t)
        table_names = re.findall(r"`([a-z_]+)`", m.group(1)) if m else re.findall(r"`([a-z_]+)`", t)
        table_names = list(dict.fromkeys(table_names))
        if len(table_names) == 0:
            c12.fail("could not find any declared table names in TASK-DB-SCHEMA-BASE.md")
        elif len(table_names) > DB_TABLE_BASELINE + DB_TABLE_TOLERANCE:
            c12.fail(
                f"{len(table_names)} tables declared, more than {DB_TABLE_BASELINE + DB_TABLE_TOLERANCE} "
                f"(baseline {DB_TABLE_BASELINE} + tolerance {DB_TABLE_TOLERANCE}): {table_names}"
            )
    extra_data["db_tables"] = table_names
    checks.append(c12)

    # 13. External input non-persistence AC
    c13 = Check(13, "EXTERNAL_INPUT_NO_PERSIST_AC", "External input (flight/hotel) non-persistence AC exists")
    no_transmit_patterns = [
        r"서버.{0,25}(전송|전달|저장).{0,15}(하지 않|안 함|없음|금지)",
        r"(미전송|미전달)",
        r"전송하지 않는다",
        r"네트워크 요청 없음",
    ]
    candidates = [tid for tid, row in by_id.items()
                  if (row["screen"] == "SCR-003" and re.search(r"항공|숙소", tid + row["title"]))
                  or tid == "SHARED-EXTERNAL-LINKOUT"]
    if not candidates:
        c13.fail("no flight/hotel/SHARED-EXTERNAL-LINKOUT task found to check")
    for tid in candidates:
        t = detail_text(tid)
        if not any(re.search(p, t) for p in no_transmit_patterns):
            c13.fail(f"{tid} does not clearly state inputs are not sent to a server")
    checks.append(c13)

    # 14. Auth / adult-verification / baseline RLS AC
    c14 = Check(14, "AUTH_ADULT_RLS_AC", "Auth / adult-verification / baseline RLS AC exists")
    t_auth = detail_text("API-AUTH")
    if not t_auth:
        c14.fail("TASK-API-AUTH.md not found")
    else:
        if not re.search(r"인증|로그인", t_auth):
            c14.fail("TASK-API-AUTH.md does not mention 인증/로그인")
        if "성인" not in t_auth:
            c14.fail("TASK-API-AUTH.md does not mention 성인 확인")
    t_rls = detail_text("DB-RLS-BASE")
    if not t_rls:
        c14.fail("TASK-DB-RLS-BASE.md not found")
    elif not re.search(r"RLS|Row Level Security", t_rls, re.IGNORECASE):
        c14.fail("TASK-DB-RLS-BASE.md does not mention RLS")
    checks.append(c14)

    # 15. Playwright Chromium Smoke tasks
    c15 = Check(15, "PLAYWRIGHT_CHROMIUM_SMOKE_EXISTS", "Playwright Chromium Smoke Task(s) exist, no other browser")
    e2e_ids = sorted(tid for tid, row in by_id.items() if row["category"] == "E2E_TEST")
    if e2e_ids != REQUIRED_E2E_TASK_IDS:
        c15.fail(f"expected E2E tasks {REQUIRED_E2E_TASK_IDS}, found {e2e_ids}")
    browser_re = re.compile(r"firefox|webkit|safari|다중 브라우저|multi-browser", re.IGNORECASE)
    negation_re = re.compile(r"하지 않|포함하지|추가하지|제외|없다|않는다")
    for tid in e2e_ids:
        t = detail_text_excluding_forbidden(tid)
        for m in browser_re.finditer(t):
            window = t[m.end():m.end() + 80]
            if not negation_re.search(window):
                c15.fail(f"{tid} mentions a non-Chromium browser without negation: '{t[max(0, m.start()-20):m.end()+20]}'")
        if not re.search(r"chromium", t, re.IGNORECASE):
            c15.fail(f"{tid} does not mention Chromium")
    checks.append(c15)

    # 16. No AWS/EC2/auto-merge implementation tasks
    c16 = Check(16, "NO_AWS_EC2_AUTOMERGE_TASKS", "Zero AWS / EC2 / auto-merge-runner implementation tasks")
    haystacks = [("00_TASK_LIST.md", text)] + [
        (f"TASK-{tid}.md", detail_text_excluding_forbidden(tid)) for tid in by_id
    ]
    for name, content in haystacks:
        for kw in FORBIDDEN_KEYWORDS:
            if kw.lower() in content.lower():
                c16.fail(f"{name} references forbidden keyword '{kw}' outside a prohibition list")
    checks.append(c16)

    # 17. REQ-FUNC(80) + REQ-NF(34) all present in Task List or EXCLUDED table
    c17 = Check(17, "REQ_COVERAGE_80_34", "All 80 REQ-FUNC and 34 REQ-NF requirements exist in Task List or EXCLUDED table")
    main_table_text = text.split("## NON_IMPLEMENTATION")[0]
    covered: set[str] = set()
    for line in main_table_text.split("\n"):
        if line.strip().startswith("|"):
            covered |= expand_req_ids(line)
    excluded = parse_non_implementation(text)
    expected_func = {f"REQ-FUNC-{i:03d}" for i in range(1, 81)}
    expected_nf = {f"REQ-NF-{i:03d}" for i in range(1, 35)}
    expected_all = expected_func | expected_nf
    union = covered | excluded
    overlap = covered & excluded
    if overlap:
        c17.fail(f"requirements both covered and excluded: {sorted(overlap)}")
    missing = sorted(expected_all - union)
    if missing:
        c17.fail(f"requirements missing from both Task List and EXCLUDED table: {missing}")
    unexpected = sorted(union - expected_all)
    if unexpected:
        c17.fail(f"unknown requirement ids referenced: {unexpected}")
    checks.append(c17)
    extra_data["requirement_counts"] = {
        "func_total": len(expected_func), "nf_total": len(expected_nf),
        "implement": len(covered), "excluded": len(excluded), "total": len(union),
    }

    # 18. No detail implementation file for an EXCLUDED requirement
    c18 = Check(18, "EXCLUDED_NO_DETAIL_IMPLEMENTATION", "No detail implementation file exists for an EXCLUDED requirement")
    for tid in by_id:
        t = detail_text(tid)
        m = re.search(r"## Requirement Ref\s*\n+(.+?)\n", t)
        req_line = m.group(1) if m else ""
        ids_in_detail = expand_req_ids(req_line)
        bad = ids_in_detail & excluded
        if bad:
            c18.fail(f"TASK-{tid}.md's Requirement Ref includes EXCLUDED requirement(s): {sorted(bad)}")
    checks.append(c18)

    write_outputs(checks, by_id, contract_screens, extra_data)

    ok = all(c.status == "PASS" for c in checks)
    if ok:
        print(f"AUDIT_PASS ({len(checks)} checks)")
        return 0

    failed = [f"{c.num}:{c.name}" for c in checks if c.status == "FAIL"]
    print(f"AUDIT_FAIL ({len(checks)} checks, failed: {', '.join(failed)})", file=sys.stderr)
    return 1


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------

def write_outputs(checks: list[Check], by_id: dict, contract_screens: dict, extra_data: dict) -> None:
    write_manifest(by_id)
    write_report(checks, by_id, extra_data)


def write_manifest(by_id: dict) -> None:
    fieldnames = [
        "Seq", "TaskID", "Title", "Category", "ImplementationStatus", "Priority",
        "RequirementRef", "Screen", "Route", "PageEntry", "DependsOn", "ExpectedFiles",
        "DetailFileExists", "DetailFilePath",
    ]
    with MANIFEST_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for tid, row in sorted(by_id.items(), key=lambda kv: int(kv[1]["seq"])):
            detail_path = TASKS_DIR / f"TASK-{tid}.md"
            writer.writerow({
                "Seq": row["seq"],
                "TaskID": tid,
                "Title": row["title"],
                "Category": row["category"],
                "ImplementationStatus": row["impl"],
                "Priority": detail_priority(tid),
                "RequirementRef": row["reqref"],
                "Screen": row["screen"],
                "Route": row["route"],
                "PageEntry": row["page_entry"],
                "DependsOn": row["depends"],
                "ExpectedFiles": row["files"],
                "DetailFileExists": "Y" if detail_path.exists() else "N",
                "DetailFilePath": f"TASKS/TASK-{tid}.md",
            })


def write_report(checks: list[Check], by_id: dict, extra_data: dict) -> None:
    ok = all(c.status == "PASS" for c in checks)
    verdict = "AUDIT_PASS" if ok else "AUDIT_FAIL"
    passed = sum(1 for c in checks if c.status == "PASS")

    lines = []
    lines.append("# Task Audit Report — Free Traveler")
    lines.append("")
    lines.append(f"**Verdict:** {verdict}")
    lines.append(f"**Checks:** {passed}/{len(checks)} passed")
    lines.append(f"**Task List:** `TASKS/00_TASK_LIST.md` ({len(by_id)} tasks)")
    lines.append(f"**Manifest:** `TASKS/TASK_MANIFEST.csv`")
    lines.append("")
    lines.append("입력: `TASKS/00_TASK_LIST.md`, `TASKS/TASK-*.md`, `docs/PROJECT_SCOPE.md`, `design-reference/SCREEN_ROUTE_CONTRACT.json`")
    lines.append("")
    lines.append("## 검사 결과")
    lines.append("")
    lines.append("| # | 검사 | 상태 | 위반 |")
    lines.append("|---|---|---|---|")
    for c in checks:
        viol = "—" if not c.violations else "; ".join(c.violations[:3]) + (f" 외 {len(c.violations)-3}건" if len(c.violations) > 3 else "")
        viol = viol.replace("|", "\\|")
        lines.append(f"| {c.num} | {c.name} — {c.description} | {c.status} | {viol} |")
    lines.append("")

    if any(c.violations for c in checks):
        lines.append("## 위반 상세")
        lines.append("")
        for c in checks:
            if not c.violations:
                continue
            lines.append(f"### {c.num}. {c.name}")
            lines.append("")
            for v in c.violations:
                lines.append(f"- {v}")
            lines.append("")

    rc = extra_data.get("requirement_counts")
    if rc:
        lines.append("## Requirement 커버리지")
        lines.append("")
        lines.append("| 항목 | 값 |")
        lines.append("|---|---:|")
        lines.append(f"| REQ-FUNC 총수 | {rc['func_total']} |")
        lines.append(f"| REQ-NF 총수 | {rc['nf_total']} |")
        lines.append(f"| IMPLEMENT 계열(Task List) | {rc['implement']} |")
        lines.append(f"| EXCLUDED(NON_IMPLEMENTATION) | {rc['excluded']} |")
        lines.append(f"| 합계 | {rc['total']} |")
        lines.append("")

    if "db_tables" in extra_data:
        lines.append("## DB 테이블")
        lines.append("")
        lines.append(f"- 선언된 테이블 수: {len(extra_data['db_tables'])} (기본 {DB_TABLE_BASELINE}개 + 허용 오차 {DB_TABLE_TOLERANCE}개)")
        for t in extra_data["db_tables"]:
            lines.append(f"  - `{t}`")
        lines.append("")

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())

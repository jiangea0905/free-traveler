#!/usr/bin/env python3
"""
validate_inputs.py — Traveler Task Pipeline pre-flight check.

Run BEFORE /gen-tasklist and again before /gen-task-details.

What it checks (stdlib only, no third-party dependencies):
  1. All required input documents exist.
  2. design-reference/SCREEN_ROUTE_CONTRACT.json:
     - schema_version == "traveler-screen-route-v1"
     - framework == "nextjs-app-router"
     - exactly 5 screens
     - unique routes, unique page_entry values
     - category_summary reports 4 core / 1 auxiliary
     - SCR-001 has starter_template_forbidden == true
  3. docs/UIUX_TRACEABILITY.md:
     - contains exactly 114 unique REQ-FUNC-*/REQ-NF-* ids
     - REQ-FUNC-001..080 and REQ-NF-001..034 are all present (no gaps)
     - every occurrence has a recognizable Implementation Status token
  4. Snapshots the current src/app file tree to docs/tasks/_src_app_tree.json
     so later steps can tell "already exists" apart from "must be created"
     (Rule 4 of the traveler-project-pipeline skill).

Exit code: 0 if all checks pass, 1 otherwise. Always prints a JSON report
to stdout (in addition to a short human-readable summary) so it can be
parsed by other tooling.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_DOCS = [
    "docs/06_SRS_UIUX_REVISED.md",
    "docs/PROJECT_SCOPE.md",
    "docs/UIUX_TRACEABILITY.md",
    "design-reference/D-001/DESIGN.md",
    "design-reference/UI_CONTRACT.md",
    "design-reference/SCREEN_ROUTE_CONTRACT.json",
    "package.json",
]

EXPECTED_SCHEMA_VERSION = "traveler-screen-route-v1"
EXPECTED_FRAMEWORK = "nextjs-app-router"
EXPECTED_SCREEN_COUNT = 5

VALID_IMPL_STATUS_PATTERN = re.compile(
    r"IMPLEMENT(?:\(축소\)|\(대체\))?|EXCLUDED"
)


def fail(report: dict, message: str) -> None:
    report["ok"] = False
    report["errors"].append(message)


def check_required_docs(report: dict) -> None:
    for rel in REQUIRED_DOCS:
        path = ROOT / rel
        if not path.exists():
            fail(report, f"missing required input: {rel}")
    report["checked_documents"] = REQUIRED_DOCS


def check_screen_route_contract(report: dict) -> dict | None:
    path = ROOT / "design-reference/SCREEN_ROUTE_CONTRACT.json"
    if not path.exists():
        fail(report, "design-reference/SCREEN_ROUTE_CONTRACT.json not found")
        return None

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(report, f"SCREEN_ROUTE_CONTRACT.json is not valid JSON: {exc}")
        return None

    if data.get("schema_version") != EXPECTED_SCHEMA_VERSION:
        fail(
            report,
            "schema_version mismatch: expected "
            f"'{EXPECTED_SCHEMA_VERSION}', got '{data.get('schema_version')}'",
        )
    if data.get("framework") != EXPECTED_FRAMEWORK:
        fail(
            report,
            "framework mismatch: expected "
            f"'{EXPECTED_FRAMEWORK}', got '{data.get('framework')}'",
        )

    screens = data.get("screens", [])
    if len(screens) != EXPECTED_SCREEN_COUNT:
        fail(
            report,
            f"expected exactly {EXPECTED_SCREEN_COUNT} screens, "
            f"found {len(screens)}",
        )

    routes = [s.get("route") for s in screens]
    entries = [s.get("page_entry") for s in screens]
    if len(set(routes)) != len(routes):
        fail(report, f"duplicate routes in screens: {routes}")
    if len(set(entries)) != len(entries):
        fail(report, f"duplicate page_entry values in screens: {entries}")

    cat = data.get("category_summary", {})
    if cat.get("core_count") != 4 or cat.get("auxiliary_count") != 1:
        fail(
            report,
            "category_summary must report core_count=4 and "
            f"auxiliary_count=1, got {cat}",
        )

    scr001 = next((s for s in screens if s.get("screen_id") == "SCR-001"), None)
    if scr001 is None:
        fail(report, "SCR-001 not found in screens")
    elif scr001.get("starter_template_forbidden") is not True:
        fail(report, "SCR-001 must declare starter_template_forbidden=true")

    report["screen_route_contract"] = {
        "schema_version": data.get("schema_version"),
        "framework": data.get("framework"),
        "screen_count": len(screens),
        "routes": routes,
        "page_entries": entries,
    }
    return data


def check_traceability(report: dict) -> None:
    path = ROOT / "docs/UIUX_TRACEABILITY.md"
    if not path.exists():
        fail(report, "docs/UIUX_TRACEABILITY.md not found")
        return

    text = path.read_text(encoding="utf-8")

    # Pull every markdown table row that starts with a requirement id.
    row_pattern = re.compile(
        r"^\|\s*(REQ-(?:FUNC|NF)-\d{3})\s*\|\s*([^|]+?)\s*\|", re.MULTILINE
    )
    rows = row_pattern.findall(text)

    ids_seen: dict[str, str] = {}
    for req_id, status_cell in rows:
        ids_seen[req_id] = status_cell.strip()

    expected_func = {f"REQ-FUNC-{i:03d}" for i in range(1, 81)}
    expected_nf = {f"REQ-NF-{i:03d}" for i in range(1, 35)}
    expected_all = expected_func | expected_nf

    missing = sorted(expected_all - ids_seen.keys())
    unexpected = sorted(ids_seen.keys() - expected_all)

    if missing:
        fail(report, f"UIUX_TRACEABILITY.md is missing requirement rows: {missing}")
    if unexpected:
        fail(
            report,
            f"UIUX_TRACEABILITY.md has unexpected requirement ids: {unexpected}",
        )
    if len(ids_seen) != 114:
        fail(
            report,
            f"expected exactly 114 unique requirement rows, found {len(ids_seen)}",
        )

    bad_status = {
        req_id: status
        for req_id, status in ids_seen.items()
        if not VALID_IMPL_STATUS_PATTERN.fullmatch(status)
    }
    if bad_status:
        fail(
            report,
            "rows with an unrecognized Implementation Status token "
            f"(expected IMPLEMENT / IMPLEMENT(축소) / IMPLEMENT(대체) / EXCLUDED): "
            f"{bad_status}",
        )

    excluded = sorted(
        req_id for req_id, status in ids_seen.items() if status == "EXCLUDED"
    )
    implement = sorted(set(ids_seen.keys()) - set(excluded))

    report["traceability"] = {
        "total_requirements": len(ids_seen),
        "excluded_count": len(excluded),
        "implement_count": len(implement),
        "excluded_requirements": excluded,
    }


def snapshot_src_app_tree(report: dict) -> None:
    src_app = ROOT / "src" / "app"
    files: list[str] = []
    if src_app.exists():
        for p in sorted(src_app.rglob("*")):
            if p.is_file():
                files.append(str(p.relative_to(ROOT)).replace("\\", "/"))

    out_dir = ROOT / "docs" / "tasks"
    out_dir.mkdir(parents=True, exist_ok=True)
    snapshot_path = out_dir / "_src_app_tree.json"
    snapshot = {
        "generated_by": "scripts/validate_inputs.py",
        "root": "src/app",
        "existing_files": files,
    }
    snapshot_path.write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    report["src_app_snapshot"] = {
        "path": str(snapshot_path.relative_to(ROOT)).replace("\\", "/"),
        "existing_file_count": len(files),
        "existing_files": files,
    }


def main() -> int:
    report: dict = {"ok": True, "errors": []}

    check_required_docs(report)
    check_screen_route_contract(report)
    check_traceability(report)
    snapshot_src_app_tree(report)

    print(json.dumps(report, ensure_ascii=False, indent=2))

    if report["ok"]:
        print("\nvalidate_inputs: PASS", file=sys.stderr)
        return 0

    print("\nvalidate_inputs: FAIL", file=sys.stderr)
    for err in report["errors"]:
        print(f"  - {err}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())

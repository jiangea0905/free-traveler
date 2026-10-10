#!/usr/bin/env python3
"""
validate_harness.py — Free Traveler harness (.claude/* + CLAUDE.md) validator.

Checks that the agent harness itself (not the Task/Wave content) is intact:
CLAUDE.md exists, the traveler-project-pipeline Skill exists, exactly the 7
expected Commands exist, and the required Harness Marker values / core rule
sentences are actually present in CLAUDE.md (and, for the content rules,
optionally in the Skill as a fallback location).

Read-only. Never mutates any file.

Checks (numbered to match the validation spec):
   1. CLAUDE.md exists at the project root.
   2. The traveler-project-pipeline Skill file exists.
   3. Exactly the 7 expected Command files exist under .claude/commands/.
   4. The `HARNESS_SCHEMA=traveler-screen-route-v1` marker is present.
   5. `DESIGN_PATH=design-reference/D-001/DESIGN.md` marker is present AND
      that file actually exists (path match, not just text).
   6. `SCREEN_CONTRACT=design-reference/SCREEN_ROUTE_CONTRACT.json` marker is
      present AND that file exists AND its schema_version equals
      traveler-screen-route-v1 (cross-checked against check 4).
   7. A rule requiring exactly one Page Owner Task per Screen (5 Screens) exists.
   8. A rule stating the 6 baseline DB tables exists.
   9. A rule stating external (flight/hotel) input is never persisted exists.
  10. A rule scoping Playwright to Chromium Smoke exists.
  11. `AUTO_MERGE=false` marker is present.
  12. `AWS_ENABLED=false` marker is present.
  13. A rule protecting EXCLUDED requirements from being implemented exists.

Exit code 0 and prints "VALIDATE_HARNESS_PASS" if every check passes.
Exit code 1 otherwise; prints which files/rules are missing.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLAUDE_MD = ROOT / "CLAUDE.md"
SKILL_MD = ROOT / ".claude/skills/traveler-project-pipeline/SKILL.md"
COMMANDS_DIR = ROOT / ".claude/commands"
DESIGN_PATH = ROOT / "design-reference/D-001/DESIGN.md"
SCREEN_CONTRACT_PATH = ROOT / "design-reference/SCREEN_ROUTE_CONTRACT.json"

EXPECTED_COMMANDS = {
    "gen-tasklist.md",
    "gen-task-details.md",
    "audit-tasks.md",
    "prepare-task.md",
    "implement-task.md",
    "run-wave.md",
    "release-check.md",
}

DB_TABLES = ["user_profile", "mate_post", "mate_application", "user_block", "report", "admin_setting"]


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


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def main() -> int:
    checks: list[Check] = []

    claude_text = read(CLAUDE_MD)
    skill_text = read(SKILL_MD)
    combined = claude_text + "\n" + skill_text

    # 1. CLAUDE.md exists
    c1 = Check(1, "CLAUDE_MD_EXISTS", "CLAUDE.md exists at the project root")
    if not CLAUDE_MD.exists():
        c1.fail(f"missing file: {CLAUDE_MD.relative_to(ROOT)}")
    checks.append(c1)

    # 2. Skill file exists
    c2 = Check(2, "SKILL_FILE_EXISTS", "traveler-project-pipeline Skill file exists")
    if not SKILL_MD.exists():
        c2.fail(f"missing file: {SKILL_MD.relative_to(ROOT)}")
    checks.append(c2)

    # 3. Exactly 7 expected Commands exist
    c3 = Check(3, "SEVEN_COMMANDS_EXIST", "Exactly the 7 expected Command files exist under .claude/commands/")
    if not COMMANDS_DIR.exists():
        c3.fail(f"missing directory: {COMMANDS_DIR.relative_to(ROOT)}")
    else:
        actual = {p.name for p in COMMANDS_DIR.glob("*.md")}
        missing = sorted(EXPECTED_COMMANDS - actual)
        extra = sorted(actual - EXPECTED_COMMANDS)
        if missing:
            c3.fail(f"missing command file(s): {missing}")
        if extra:
            c3.fail(f"unexpected extra command file(s) (expected exactly 7): {extra}")
        if len(actual) != 7 and not missing and not extra:
            # defensive: should not happen given set equality above, but keep an explicit count check
            c3.fail(f"expected exactly 7 command files, found {len(actual)}")
    checks.append(c3)

    # 4. HARNESS_SCHEMA marker
    c4 = Check(4, "HARNESS_SCHEMA_MARKER", "HARNESS_SCHEMA=traveler-screen-route-v1 marker present in CLAUDE.md")
    if "HARNESS_SCHEMA=traveler-screen-route-v1" not in claude_text:
        c4.fail("CLAUDE.md does not contain 'HARNESS_SCHEMA=traveler-screen-route-v1'")
    checks.append(c4)

    # 5. DESIGN_PATH marker + path match
    c5 = Check(5, "DESIGN_PATH_MATCH", "DESIGN_PATH marker present and design-reference/D-001/DESIGN.md exists")
    if "DESIGN_PATH=design-reference/D-001/DESIGN.md" not in claude_text:
        c5.fail("CLAUDE.md does not contain 'DESIGN_PATH=design-reference/D-001/DESIGN.md'")
    if not DESIGN_PATH.exists():
        c5.fail(f"missing file: {DESIGN_PATH.relative_to(ROOT)}")
    checks.append(c5)

    # 6. SCREEN_CONTRACT marker + path match + schema_version consistency
    c6 = Check(6, "SCREEN_CONTRACT_MATCH", "SCREEN_CONTRACT marker present, file exists, schema_version matches")
    if "SCREEN_CONTRACT=design-reference/SCREEN_ROUTE_CONTRACT.json" not in claude_text:
        c6.fail("CLAUDE.md does not contain 'SCREEN_CONTRACT=design-reference/SCREEN_ROUTE_CONTRACT.json'")
    if not SCREEN_CONTRACT_PATH.exists():
        c6.fail(f"missing file: {SCREEN_CONTRACT_PATH.relative_to(ROOT)}")
    else:
        try:
            contract = json.loads(SCREEN_CONTRACT_PATH.read_text(encoding="utf-8"))
            if contract.get("schema_version") != "traveler-screen-route-v1":
                c6.fail(
                    "SCREEN_ROUTE_CONTRACT.json schema_version "
                    f"'{contract.get('schema_version')}' != 'traveler-screen-route-v1'"
                )
        except json.JSONDecodeError as exc:
            c6.fail(f"SCREEN_ROUTE_CONTRACT.json is not valid JSON: {exc}")
    checks.append(c6)

    # 7. Page Owner x5 rule
    c7 = Check(7, "PAGE_OWNER_FIVE_RULE", "A rule requiring exactly one Page Owner Task per Screen (5 Screens) exists")
    page_owner_patterns = [
        r"Page Owner Task를?\s*정확히\s*1개",
        r"5개\s*Screen.{0,30}Page Owner.{0,10}정확히\s*1개",
        r"PAGE-SCR001.{0,80}PAGE-SCR005",
    ]
    if not any(re.search(p, combined, re.DOTALL) for p in page_owner_patterns):
        c7.fail("no rule found requiring exactly one Page Owner per Screen (checked CLAUDE.md + SKILL.md)")
    checks.append(c7)

    # 8. DB 6-table baseline rule
    c8 = Check(8, "DB_SIX_TABLE_RULE", "A rule stating the 6 baseline DB tables exists")
    missing_tables = [t for t in DB_TABLES if t not in combined]
    if missing_tables:
        c8.fail(f"DB table name(s) not found in CLAUDE.md/SKILL.md: {missing_tables}")
    if not re.search(r"6개", combined):
        c8.fail("no '6개' (six-table) mention found alongside the table names")
    checks.append(c8)

    # 9. External input non-persistence rule
    c9 = Check(9, "EXTERNAL_INPUT_NO_PERSIST_RULE", "A rule stating external (flight/hotel) input is never persisted exists")
    if not re.search(r"항공", combined) or not re.search(r"숙소", combined):
        c9.fail("no 항공/숙소 input rule context found")
    if not re.search(r"(서버|DB|URL).{0,30}(보내지 않|전송하지 않|전달하지 않)", combined):
        c9.fail("no explicit 'not sent to server/DB/URL' phrasing found")
    checks.append(c9)

    # 10. Playwright Chromium Smoke rule
    c10 = Check(10, "PLAYWRIGHT_CHROMIUM_SMOKE_RULE", "A rule scoping Playwright to Chromium Smoke exists")
    if not re.search(r"chromium", combined, re.IGNORECASE):
        c10.fail("no mention of Chromium")
    if not re.search(r"smoke", combined, re.IGNORECASE):
        c10.fail("no mention of Smoke")
    checks.append(c10)

    # 11. AUTO_MERGE=false marker
    c11 = Check(11, "AUTO_MERGE_FALSE_MARKER", "AUTO_MERGE=false marker present")
    if "AUTO_MERGE=false" not in claude_text:
        c11.fail("CLAUDE.md does not contain 'AUTO_MERGE=false'")
    checks.append(c11)

    # 12. AWS_ENABLED=false marker
    c12 = Check(12, "AWS_ENABLED_FALSE_MARKER", "AWS_ENABLED=false marker present")
    if "AWS_ENABLED=false" not in claude_text:
        c12.fail("CLAUDE.md does not contain 'AWS_ENABLED=false'")
    checks.append(c12)

    # 13. EXCLUDED protection rule
    c13 = Check(13, "EXCLUDED_PROTECTION_RULE", "A rule protecting EXCLUDED requirements from being implemented exists")
    if not re.search(r"EXCLUDED.{0,40}(임의로 구현하지 않는다|구현하지 않는다|보호)", combined, re.DOTALL):
        c13.fail("no rule found protecting EXCLUDED requirements from arbitrary implementation")
    checks.append(c13)

    ok = all(c.status == "PASS" for c in checks)

    if ok:
        print("VALIDATE_HARNESS_PASS")
        print(f"({len(checks)} checks passed)", file=sys.stderr)
        return 0

    print("VALIDATE_HARNESS_FAIL", file=sys.stderr)
    for c in checks:
        if c.status == "FAIL":
            print(f"  [{c.num}] {c.name} — {c.description}", file=sys.stderr)
            for v in c.violations:
                print(f"      - {v}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())

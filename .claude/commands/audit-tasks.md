---
description: TASKS/00_TASK_LIST.md와 TASKS/TASK-*.md가 traveler-project-pipeline 규칙을 지키는지 감사한다(scripts/audit_tasks.py). Skill의 3단계.
---

# /audit-tasks

`traveler-project-pipeline` Skill §1~§12를 기준으로 이미 생성된 Task 목록과 상세 파일을 검사한다. 이 커맨드는 Task를 새로 만들지 않는다 — 검사와 리포트 생성만 한다.

## 공통 규칙 (반드시 지킨다)

- **traveler-project-pipeline Skill을 사용한다** — `scripts/audit_tasks.py`가 구현한 18개 검사는 Skill §1~§12에 대응한다는 전제로 결과를 해석한다.
- **실제 파일을 읽는다** — `scripts/audit_tasks.py`의 출력과 그것이 갱신한 `TASKS/TASK_AUDIT_REPORT.md`를 실제로 Read해서 보고한다. 실행하지 않고 이전 결과를 기억에 의존해 보고하지 않는다.
- **구현 코드를 만들지 않는다** — 이 커맨드는 `TASKS/TASK_MANIFEST.csv`, `TASKS/TASK_AUDIT_REPORT.md` 외에 어떤 파일도 만들거나 수정하지 않는다. 위반을 발견해도 이 커맨드 안에서 `src/**` 코드나 Task 파일을 직접 고치지 않는다.
- **Task Audit 실패를 무시하지 않는다** — `AUDIT_FAIL`이면 반드시 그 사실과 실패한 검사 번호·사유를 사용자에게 보고한다. 일부만 통과했다고 "대체로 통과"라고 말하지 않는다. `AUDIT_PASS`가 아니면 완료로 보고하지 않는다.

## 실행 절차

1. `scripts/audit_tasks.py`를 실행한다. 이 환경의 `python3`가 실패하면(예: 깨진 Windows Store 스텁) `python`으로 대체 실행하고 그 사실을 그대로 보고한다.
2. 스크립트는 `TASKS/TASK_MANIFEST.csv`(Task 목록 요약 CSV)와 `TASKS/TASK_AUDIT_REPORT.md`(18개 검사 결과 리포트)를 생성/갱신한다 — 실행 후 이 두 파일이 실제로 갱신되었는지 확인한다.
3. 종료 코드와 stdout/stderr(`AUDIT_PASS (N checks)` 또는 `AUDIT_FAIL (...)`)을 확인한다.
4. `AUDIT_PASS`면 "감사 통과(N/N)"라고 명확히 말하고 `TASKS/TASK_AUDIT_REPORT.md`의 Requirement 커버리지·DB 테이블 요약을 함께 보고한다.
5. `AUDIT_FAIL`이면 다음을 보고한다: 실패한 검사 번호와 이름, 관련 Task ID, `TASKS/TASK_AUDIT_REPORT.md`의 "위반 상세" 절 내용, 무엇을 고쳐야 하는지. **스스로 판단해 자동으로 목록/상세 파일을 고치지 않는다** — 사용자에게 `/gen-tasklist` 또는 `/gen-task-details`를 다시 실행할지, 특정 파일만 수동으로 고칠지 확인한다.
6. 통과했다고 거짓으로 보고하지 않는다. 스크립트를 실행하지 않고 통과를 추정하지 않는다.

## 참고

`scripts/audit_tasks.py`는 다음 18개를 검사한다(전체 로직은 스크립트 상단 docstring 참고): (1) Task List↔상세 파일 1:1, (2) 중복 Task ID 0, (3) Depends On 누락 0, (4) Dependency Cycle 0, (5) Screen 5개 모두 Page Owner 정확히 1개, (6) Route·Page Entry·Expected Files가 `SCREEN_ROUTE_CONTRACT.json`과 일치, (7) Component-only Screen 0, (8) SCR-001 Starter 제거 AC, (9) SCR-003 세 탭 조립 AC, (10) SCR-005 역할별 상태 조립 AC, (11) DB Schema·RLS·Access·Seed Task 존재, (12) DB Table 수가 6개 기준을 크게 넘지 않음, (13) 외부 입력 비저장 AC, (14) Auth·성인·기본 RLS AC, (15) Playwright Chromium Smoke Task 존재, (16) AWS·EC2·자동 Merge 구현 Task 0, (17) REQ-FUNC 80개·REQ-NF 34개가 Task 또는 EXCLUDED 표에 존재, (18) EXCLUDED 상세 구현 파일 미생성.

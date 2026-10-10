---
description: TASKS/00_TASK_LIST.md의 각 항목마다 상세 Task 파일(TASKS/TASK-<ID>.md)을 1:1로 생성한다. traveler-project-pipeline Skill의 2단계.
---

# /gen-task-details

`traveler-project-pipeline` Skill을 로드하고, `TASKS/00_TASK_LIST.md`에 있는 **모든** Task에 대해 `TASKS/TASK-<TASK_ID>.md`를 하나씩 생성한다.

## 공통 규칙 (반드시 지킨다)

- **traveler-project-pipeline Skill을 사용한다** — Skill §4(Task List·상세 Task 형식)의 14개 절 형식과 §5~§12(Page Owner·Component 분리, DB 경계, 외부 입력 비저장, Auth/RLS, Playwright, Wave, EXCLUDED 보호, AWS·EC2·자동 Merge 금지)를 그대로 따른다.
- **실제 파일을 읽는다** — `TASKS/00_TASK_LIST.md`와 아래 §실행 절차의 모든 문서를 실제로 Read한다. Task 제목·Requirement Ref·Depends On을 추측하지 않고 표에서 그대로 옮긴다.
- **구현 코드를 만들지 않는다** — 이 커맨드는 `TASKS/TASK-*.md` 상세 파일만 만든다. Expected Files에 적을 경로는 "앞으로 만들 파일" 목록일 뿐이며, 이 단계에서 그 경로에 실제 `src/**` 코드를 작성하지 않는다.
- **Task Audit 실패를 무시하지 않는다** — 마지막 8~9단계에서 감사를 실행하고 실패하면 그대로 보고한다. 감사를 생략하거나, 결과를 확인하지 않고 완료로 보고하지 않는다.

## 실행 절차

1. `TASKS/00_TASK_LIST.md`가 없으면 중단하고 먼저 `/gen-tasklist`를 실행하라고 안내한다.
2. `scripts/validate_inputs.py`를 다시 실행해(`python3` 실패 시 `python`으로 대체) `src/app` 파일 트리 스냅샷을 최신 상태로 갱신한다 — Task 상세를 쓰기 전 실제 트리를 반드시 확인한다.
3. `TASKS/00_TASK_LIST.md`의 각 Task 행과 그 아래 AC 블록을 Read해서, Skill의 "Task 상세 파일 형식"(Context / Project Scope / Requirement Ref / Screen · Route · Page Entry / Design Ref / Depends On / Expected Files / Functional AC / Visual AC / Security/Privacy AC / Test Cases / Verify / Definition of Done / Forbidden)에 맞춰 `TASKS/TASK-<TASK_ID>.md`를 작성한다.
4. **Page Owner Task 상세**는 다음을 반드시 포함한다.
   - `design-reference/UI_CONTRACT.md`의 해당 Screen 영역 순서 전체와 최소 콘텐츠 수 — 숫자·순서를 그대로 옮긴다.
   - `PAGE-SCR001`: Next.js 기본 스타터 템플릿 제거 확인 AC.
   - `PAGE-SCR003`: 항공편·숙소·동행 구하기 탭이 실제로 조립·전환되는지 확인하는 AC.
   - `PAGE-SCR005`: Guest·Member·Admin 상태가 실제로 조립되고 역할에 없는 영역은 렌더링되지 않는지 확인하는 AC.
   - 큰 빈 영역·Placeholder 문구 금지 및 완성형 Empty State 요구 AC.
   - Depends On에 적힌 Component Task 전부가 완료되어야 시작 가능하다는 문장.
5. Expected Files는 2단계에서 확인한 실제 파일 트리를 기준으로, 새로 만들 파일과 이미 존재하는 파일을 구분해서 적는다(이미 있는 파일을 "생성"으로 적지 않는다). Expected Files 절 바로 아래에 "이 Task는 위 Expected Files 목록에 있는 파일만 생성·수정한다"를 명시한다.
6. 항공·숙소 관련 Component/Page Owner/Shared Task 상세에는 "입력값을 서버·DB·외부 URL·로그·분석으로 전송하지 않는다"를 Forbidden 항목에 명시한다.
7. EXCLUDED Requirement는 어떤 상세 파일의 Requirement Ref에도 넣지 않는다 — `TASKS/00_TASK_LIST.md`의 NON_IMPLEMENTATION 표에만 남아 있으면 된다.
8. 모든 상세 파일 생성이 끝나면 **반드시** `scripts/audit_tasks.py`를 실행한다(`python3` 실패 시 `python`으로 대체하고 그 사실을 보고한다).
9. `audit_tasks.py`의 출력(`AUDIT_PASS`/`AUDIT_FAIL`, 실패한 검사 번호, `TASKS/TASK_AUDIT_REPORT.md` 내용)을 그대로 사용자에게 보고한다. `AUDIT_FAIL`이면 해당 Task 목록/상세를 수정하고 다시 감사를 돌린다 — 위반을 숨기거나 통과한 것처럼 보고하지 않는다.

## 완료 조건

- `TASKS/TASK-*.md` 파일 수 == `TASKS/00_TASK_LIST.md`의 Task 수(1:1).
- `scripts/audit_tasks.py`가 실제로 실행되었고 `AUDIT_PASS`이며, `TASKS/TASK_MANIFEST.csv`·`TASKS/TASK_AUDIT_REPORT.md`가 갱신되었음이 보고됨. `AUDIT_FAIL` 상태로는 완료로 보고하지 않는다.

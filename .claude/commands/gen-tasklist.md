---
description: Free Traveler 구현 Task 목록(TASKS/00_TASK_LIST.md)을 생성한다. traveler-project-pipeline Skill의 1단계.
---

# /gen-tasklist

`traveler-project-pipeline` Skill을 로드하고 그 §1~§12(입력 문서, Screen/Page Entry, IMPLEMENT·EXCLUDED 처리, Task List 형식, Page Owner·Component 분리, DB·정적 Data 경계 등)에 따라 `TASKS/00_TASK_LIST.md`를 생성(또는 갱신)한다.

## 공통 규칙 (반드시 지킨다)

- **traveler-project-pipeline Skill을 사용한다** — 이 커맨드만 단독으로 실행하지 않고 Skill의 정본 우선순위·ID 규칙·형식을 그대로 따른다.
- **실제 파일을 읽는다** — 아래 §실행 절차의 모든 파일을 실제로 Read한다. 이전에 읽었던 기억이나 추정으로 내용을 재구성하지 않는다(문서가 바뀌었을 수 있다).
- **구현 코드를 만들지 않는다** — 이 커맨드는 `TASKS/00_TASK_LIST.md` 외에 어떤 파일도 만들거나 수정하지 않는다. `src/**`, `supabase/**` 등 애플리케이션 코드를 작성하지 않는다.
- **Task Audit 실패를 무시하지 않는다** — 이 단계에서는 아직 감사를 실행하지 않지만, 이전에 실행된 `TASKS/TASK_AUDIT_REPORT.md`가 `AUDIT_FAIL`이었다면 그 사실을 먼저 보고하고, 실패 원인을 해결하는 방향으로 Task 목록을 갱신한다 — 실패를 못 본 척 새 목록을 덮어쓰지 않는다.

## 실행 절차

1. `scripts/validate_inputs.py`를 실행한다(`python3`이 실패하면 `python`으로 대체 실행하고 그 사실을 보고한다). 실패하면 오류 내용을 그대로 보고하고 중단한다.
2. 다음 파일을 실제로 Read한다: `docs/06_SRS_UIUX_REVISED.md`, `docs/PROJECT_SCOPE.md`, `docs/UIUX_TRACEABILITY.md`, `design-reference/D-001/DESIGN.md`, `design-reference/UI_CONTRACT.md`, `design-reference/SCREEN_ROUTE_CONTRACT.json`, `package.json`, 그리고 `scripts/validate_inputs.py`가 출력한 `src/app` 파일 트리 스냅샷.
3. `SCREEN_ROUTE_CONTRACT.json.screens`(정확히 5개)를 기준으로 Screen당 Page Owner Task 1개(`PAGE-SCR00N`)를 만든다.
4. 각 Screen의 `design-reference/UI_CONTRACT.md` "영역 순서"를 기준으로 Component Task(`COMP-SCR00N-<slug>`)를 만들고, Page Owner의 Depends On에 같은 Screen의 모든 Component Task ID를 넣는다.
5. 여행지·안전정보·대표 프로필은 `DATA-*` Task로, DB가 필요한 기능(동행/신고/차단/관리자 설정)은 `DB-*`/`API-*`/`SHARED-*` Task로 나눈다. DB 테이블은 6개 기본 테이블을 크게 넘지 않는다.
6. Header/Footer, 접근성, SEO, 오류 화면, 연락처 탐지, 외부 이동 유틸 등은 `SHARED-*` Task로 한 번만 만든다.
7. `docs/UIUX_TRACEABILITY.md`의 114개 Requirement를 전부 순회하며, IMPLEMENT 계열은 어떤 Task의 Requirement Ref에 최소 1번 들어가야 하고, EXCLUDED는 어떤 Task에도 넣지 않는 대신 `## NON_IMPLEMENTATION` 표에 근거·후속 방향과 함께 추가한다.
8. Playwright Task는 `E2E-PUBLIC-SMOKE`/`E2E-TRAVEL-TOOLS`/`E2E-MATE-AUTH` 3개만 만든다(Chromium 전용). 자동 Merge/EC2/AWS Task는 만들지 않는다.
9. 완성된 목록을 `TASKS/00_TASK_LIST.md`에 Skill이 정의한 형식(상단 요약 → Category별 표+AC 블록 → NON_IMPLEMENTATION 표 → 커버리지 검증)으로 저장한다. 이미 파일이 있으면 갱신하되, 기존에 승인된 Task ID를 이유 없이 바꾸지 않는다.
10. 생성/갱신된 Task 개수, EXCLUDED Requirement 개수, Screen당 Page Owner/Component 개수를 요약해 보고한다. 개수를 완료 조건처럼 말하지 않는다(45~65개는 참고치일 뿐이다).

## 금지

- `SCREEN_ROUTE_CONTRACT.json`에 없는 Screen을 추가하지 않는다.
- 이 단계에서 상세 파일(`TASKS/TASK-*.md`)을 만들지 않는다 — 그것은 `/gen-task-details`의 역할이다.
- 이 단계에서 `scripts/audit_tasks.py`를 실행하지 않는다(상세 파일이 아직 없으므로 통과할 수 없다) — 감사는 `/audit-tasks` 또는 `/gen-task-details`의 마지막 단계에서 실행한다.

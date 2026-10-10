---
description: prepare-task가 READY_TO_IMPLEMENT로 판정한 Task 하나를 실제로 구현한다. 기본적으로 Commit·Push·PR을 자동 수행하지 않는다.
---

# /implement-task

`TASKS/TASK-<TASK_ID>.md` 하나를 실제 코드로 구현한다. `CLAUDE.md`의 "Task 완료 순서" 3~7단계(구현 → 관련 포맷·Unit Test → 필요 시 Playwright → Diff 확인 → 완료 보고)에 해당하며, `/prepare-task`가 끝낸 1~2단계(Task 읽기, 입력 확인) 뒤에 실행한다.

## 선행 조건

- 같은 `WAVE_ID`·`TASK_ID`로 `/prepare-task`를 실행해 **`READY_TO_IMPLEMENT`**를 받은 뒤에만 이 Command를 실행한다.
- `/prepare-task`를 실행하지 않았거나 `READY_TO_IMPLEMENT`가 아니었다면, 이 Command를 실행하지 말고 먼저 `/prepare-task WAVE_ID TASK_ID`를 실행하라고 안내한다. `BLOCKED_*` 상태를 무시하고 구현을 진행하지 않는다.

## 규칙

1. **한 번에 Task 하나만 구현한다.** `/prepare-task`가 `READY_TO_IMPLEMENT`로 판정한 그 Task 하나만 다룬다. 같은 실행 안에서 다른 Task로 넘어가지 않는다(`CLAUDE.md` 규칙 7).
2. **Expected Files 안에서만 작업한다.** `TASKS/TASK-<TASK_ID>.md`의 `Expected Files` 절에 나열된 파일만 생성·수정한다. 목록 밖 파일은 건드리지 않는다(`CLAUDE.md` 규칙 8).
3. **Functional AC·Visual AC·Security/Privacy AC를 따른다.** `Design Ref`가 가리키는 `design-reference/D-001/DESIGN.md` 토큰(색상·타이포·spacing·radius 등)을 실제로 적용한다. AC에 없는 기능을 임의로 추가하지 않는다.
4. **Page Owner는 실제 Page Entry를 조립한다.** Category가 `PAGE_OWNER`인 Task는 새 Component를 만들지 않고, 이미 완료된 Component/Data/API 산출물을 `Page Entry`(`page.tsx`)에서 실제로 import·배치한다(`CLAUDE.md` 규칙 9). `PAGE-SCR001`은 Next.js 기본 스타터 콘텐츠를 완전히 제거하고, `PAGE-SCR003`은 항공·숙소·동행 세 탭을 실제로 조립하며, `PAGE-SCR005`는 Guest·Member·Admin 상태를 실제로 조립한다.
5. **관련 Unit Test를 실행한다.** Task 상세의 `Verify` 절에 `UNIT-*` 또는 Vitest 실행 명령이 적혀 있으면 그 테스트를 실제로 실행하고 결과(통과/실패)를 확인한다. 테스트가 없던 로직을 새로 만들었다면 이 Task 범위 안에서 대응하는 Unit Test도 함께 작성한다.
6. **Playwright Smoke는 Page Owner 또는 E2E Task일 때만 실행한다.** Category가 `PAGE_OWNER` 또는 `E2E_TEST`가 아닌 Task(Component/Data/DB/API/Shared 등)에서는 Playwright를 실행하지 않는다. 실행할 때도 `Verify`에 적힌 특정 스펙만, Chromium 프로젝트로만 돌린다(`npx playwright test <spec> --project=chromium`). 다른 브라우저나 관련 없는 스펙 전체를 돌리지 않는다.
7. **AWS·EC2·ORM·자동 Merge 기능을 추가하지 않는다.** Prisma 등 ORM 도입, AWS/EC2 연동 코드, 자동 Merge/자동 PR 워크플로를 이 Task의 일부로 만들지 않는다(`CLAUDE.md` 규칙 17·21).
8. **완료 후 변경 파일·검증·제약을 보고한다.** 다음을 빠짐없이 보고한다: 실제로 생성·수정한 파일 목록(Expected Files와 정확히 일치하는지 포함), 실행한 Unit Test/Playwright와 그 결과, Definition of Done 각 항목의 충족 여부, 아직 해결되지 않은 제약(Forbidden 위반 없음 확인, 수동 확인 필요 항목, 후속 Task에 넘길 사항).

## Commit·Push·PR 정책

- **기본값: Commit·Push·PR을 자동으로 수행하지 않는다.** 구현이 끝나면 작업 트리에 변경분만 남긴 채 보고를 마친다.
- **사용자가 명시적으로 요청한 경우에만** 이 Task의 변경분을 **Task 단위로 Commit**할 수 있다. 커밋 메시지에는 `TASK_ID`를 포함한다(예: `TASK-DB-SCHEMA-BASE: 핵심 6개 테이블 스키마 정의`).
- 사용자가 Commit을 요청했더라도 **Push와 PR 생성은 이 Command에서 하지 않는다.** Push·PR·Merge는 `docs/DECISION_LOG.md` DEC-012에 따라 사람이 별도로 수행한다.
- 여러 Task를 하나의 Commit으로 묶지 않는다 — Commit은 항상 이번에 구현한 Task 하나에 대응한다.

## 실행 절차

1. `/prepare-task`의 `READY_TO_IMPLEMENT` 판정을 확인한다(선행 조건).
2. `TASKS/TASK-<TASK_ID>.md` 전체를 다시 Read한다(Context, Project Scope, Requirement Ref, Design Ref, Depends On, Expected Files, Functional/Visual/Security AC, Test Cases, Definition of Done, Forbidden).
3. Expected Files 안에서 Functional·Visual·Security AC를 만족하도록 구현한다. Category가 `PAGE_OWNER`면 규칙 4에 따라 조립만 한다.
4. 규칙 5에 따라 관련 Unit Test를 실행한다. 실패하면 코드를 고치고 다시 실행한다 — 실패한 채로 다음 단계로 넘어가지 않는다.
5. 규칙 6에 따라 필요할 때만 Playwright Chromium Smoke를 실행한다.
6. 변경분을 Diff로 확인한다 — Expected Files와 정확히 일치하는지, Forbidden 절에 적힌 사항을 어기지 않았는지 확인한다.
7. 규칙 8에 따라 완료를 보고한다.
8. 사용자가 Commit을 요청하면 §Commit·Push·PR 정책에 따라 Task 단위로만 Commit한다. 요청이 없으면 Commit하지 않는다.

## 금지

- `READY_TO_IMPLEMENT`가 아닌 Task를 구현하지 않는다.
- Expected Files 밖의 파일을 생성·수정하지 않는다.
- `docs/PROJECT_SCOPE.md`/`docs/UIUX_TRACEABILITY.md`에서 EXCLUDED로 분류된 기능을 구현하지 않는다.
- Prisma 등 ORM, AWS, EC2, 자동 Merge/자동 PR 기능을 추가하지 않는다.
- 사용자 요청 없이 Commit하지 않는다. 요청이 있어도 Push나 PR 생성을 하지 않는다.
- `git reset --hard`, `git push --force`, `git clean -f` 등 destructive Git 명령을 사용하지 않는다.
- 검증(Unit Test/필요 시 Playwright)을 생략하고 완료로 보고하지 않는다.

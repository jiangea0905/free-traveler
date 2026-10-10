---
description: 특정 Wave의 특정 Task를 구현하기 전에 준비 상태를 점검하는 Read-only 게이트. 코드를 수정하지 않는다.
---

# /prepare-task

`WAVE_ID`와 `TASK_ID`를 받아, 그 Task를 지금 구현해도 되는지 8가지를 점검하고 `READY_TO_IMPLEMENT` 또는 4가지 `BLOCKED_*` 상태 중 하나를 출력한다. `CLAUDE.md`의 "Task 완료 순서" 1단계(Task 읽기)·2단계(입력 확인)를 형식화한 게이트이며, `traveler-project-pipeline` Skill이 정의한 Task List/상세 파일 형식을 기준으로 점검한다.

**이 Command는 코드를 수정하지 않는다.** 파일을 새로 만들거나, 고치거나, git 상태를 바꾸는 어떤 명령(`git add`, `git commit`, `git stash` 등)도 실행하지 않는다. 오직 읽고 판정만 한다.

## 입력

| 입력 | 설명 |
|---|---|
| `WAVE_ID` | 예: `W01`. 사용자가 `/prepare-task W01 DB-SCHEMA-BASE` 형태로 함께 전달한다. |
| `TASK_ID` | `TASKS/00_TASK_LIST.md`에 존재하는 Task ID(예: `DB-SCHEMA-BASE`, `PAGE-SCR001`). |
| 선택된 상세 Task 파일 | `TASKS/TASK-<TASK_ID>.md`. 이 파일이 실제 판정의 근거다. |

`WAVE_ID` 또는 `TASK_ID`가 없으면 다른 검사를 진행하지 않고 즉시 `BLOCKED_INPUT`을 출력한다.

## 검사 절차

이 순서대로 실제 파일을 Read하며 진행한다. 하나라도 실패하면 해당 검사의 출력 상태를 즉시 확정하고, 남은 검사는 "확인 안 함"으로 표시한 채 결과를 보고한다(이미 실패가 확정된 뒤에도 계속 점검해 여러 문제를 한 번에 알려주고 싶으면 그래도 되지만, 최종 출력은 아래 §우선순위에 따라 하나만 낸다).

1. **Working Tree 상태** — `git status --porcelain`을 실행한다.
   - 이 디렉터리가 git 저장소가 아니면 "해당 없음"으로 기록하고 통과 처리한다.
   - 추적되지 않은 변경(수정·추가·삭제)이 하나라도 있으면 **실패** → `BLOCKED_DIRTY_TREE`. 이전 Task의 변경이 커밋/스태시되지 않은 채 남아 있을 가능성이 크다.

2. **Task가 현재 Wave에 포함되는지** — Wave 구성은 고정 파일로 관리하지 않는다(`docs/DECISION_LOG.md` DEC-010). 다음 순서로 확인한다.
   - `TASKS/WAVE_<WAVE_ID>.md` 또는 `TASKS/WAVES.md`처럼 이번 대화 이전에 사용자가 만든 Wave 구성 파일이 있으면 그 안에서 `TASK_ID`를 찾는다.
   - 그런 파일이 없으면, 이번 대화에서 사용자가 `WAVE_ID`에 포함된다고 명시적으로 말한 Task 목록에 `TASK_ID`가 있는지 확인한다.
   - 위 두 경우 모두 확인할 방법이 없으면(Wave 범위가 아예 정의된 적이 없음) **실패** → `BLOCKED_INPUT`(Wave 범위를 먼저 알려달라고 안내).
   - Wave 범위는 확인됐는데 그 목록에 `TASK_ID`가 없으면 **실패** → `BLOCKED_INPUT`(다른 Wave 소속 Task를 잘못 지정).

3. **Depends On 완료 여부** — `TASKS/TASK-<TASK_ID>.md`의 `Depends On` 절을 읽는다. "없음"이면 통과.
   - 각 의존 Task ID에 대해 `TASKS/TASK-<DEP_ID>.md`의 `Expected Files`를 읽고, "(신규)"로 표시된 파일이 실제로 저장소에 존재하는지 확인한다.
   - 완료 여부를 더 정확히 아는 방법(커밋 로그, 사용자가 알려준 완료 목록 등)이 있으면 그것을 우선한다. 파일 존재만으로 판단할 때는 "(수정)" 대상은 원래 존재하던 파일이라 존재 자체가 완료를 증명하지 않는다는 점을 결과에 함께 적는다.
   - 하나라도 완료되지 않은 것으로 보이면 **실패** → `BLOCKED_DEPENDENCY`(어떤 Depends On이 어떤 이유로 미완료로 보이는지 나열).

4. **Expected Files** — `TASKS/TASK-<TASK_ID>.md`의 `Expected Files` 절을 읽는다.
   - 절 자체가 없거나 비어 있으면 **실패** → `BLOCKED_INPUT`(Task 정의 자체가 불완전).
   - "(신규)" 파일이 이미 존재하면(예상과 다름) 경고로 기록한다 — 이유(다른 Task가 먼저 만들었을 수 있음)를 함께 적되, 내용 확인 전에는 실패로 단정하지 않는다.
   - "(수정)" 파일이 아직 존재하지 않으면 **실패** → `BLOCKED_DEPENDENCY`(선행 Task가 그 파일을 아직 만들지 않았다).

5. **SRS·Scope·Design·Screen Ref** — `TASKS/TASK-<TASK_ID>.md`의 `Requirement Ref`, `Screen / Route / Page Entry`, `Design Ref` 절을 읽고 다음을 실제로 Read해 대조한다.
   - `Requirement Ref`의 각 ID가 `docs/06_SRS_UIUX_REVISED.md`/`docs/UIUX_TRACEABILITY.md`에 실제로 존재하는지.
   - `Screen`이 `N/A`/`전역`이 아니면, `Route`·`Page Entry`가 `design-reference/SCREEN_ROUTE_CONTRACT.json`의 해당 Screen 값과 일치하는지.
   - `Design Ref`가 가리키는 문서(`design-reference/D-001/DESIGN.md` 등)가 실제로 존재하는지.
   - 참조가 깨져 있거나(문서에 없는 ID, 계약과 다른 Route) 찾을 수 없으면 **실패** → `BLOCKED_INPUT`.

6. **필요한 환경변수 이름** — Task 성격(Supabase Auth/DB 관련인지)을 보고 필요한 환경변수 이름을 나열한다(예: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`). 정적 데이터(`DATA-*`)나 순수 UI Component처럼 환경변수가 필요 없는 Task는 "필요 없음"으로 기록하고 통과.
   - 필요한데 `.env.local`(로컬 실행 시) 또는 배포 환경 설정에 해당 이름이 없으면 **실패** → `BLOCKED_INPUT`(`docs/ARCHITECTURE.md` §16 착수 차단과 동일한 성격).

7. **Secret 하드코딩 위험** — Task의 `Expected Files`·`Functional AC`·`Forbidden` 내용에서 `service_role`/Service Role Key, API Secret 등이 Client Component(파일 상단에 `"use client"`가 있거나 `src/app/**/page.tsx` 등 브라우저에 번들되는 파일)에 들어갈 계획이 있는지 확인한다.
   - 그런 계획이 보이면 **실패** → `BLOCKED_SCOPE`(`CLAUDE.md` 규칙 15 위반 소지).
   - 특별한 계획이 없으면 통과하되, "Server 전용 모듈에만 Secret을 두라"는 주의를 결과에 한 줄 남긴다.

8. **EXCLUDED 범위 침범 여부** — `docs/PROJECT_SCOPE.md`, `docs/UIUX_TRACEABILITY.md`, `TASKS/00_TASK_LIST.md`의 `## NON_IMPLEMENTATION` 표를 Read한다.
   - Task의 `Requirement Ref`에 있는 어떤 ID도 EXCLUDED로 분류되어 있으면 안 된다.
   - Task의 `Functional AC`가 CMS·외부 Email 발송·Monitoring·감사 로그·실시간 채팅 등 명시적으로 제외된 기능(`docs/ARCHITECTURE.md` §17)을 구현하라고 요구하고 있지 않은지 확인한다.
   - 위반이 보이면 **실패** → `BLOCKED_SCOPE`.

## 출력

정확히 다음 5개 값 중 **하나만** 최종 결과로 낸다(예: `RESULT: READY_TO_IMPLEMENT`). 그 아래에 각 검사의 통과/실패와 근거를 짧게 나열한다.

| 출력 | 의미 | 발생 조건 |
|---|---|---|
| `READY_TO_IMPLEMENT` | 8개 검사 전부 통과 | — |
| `BLOCKED_INPUT` | 입력·정의 자체가 불완전하거나 참조가 깨짐 | 검사 1(git 없음은 제외)·2·4(절 없음)·5·6 실패 |
| `BLOCKED_DEPENDENCY` | 선행 Task가 아직 끝나지 않음 | 검사 3·4("(수정)" 대상 미존재) 실패 |
| `BLOCKED_DIRTY_TREE` | 이전 작업의 변경분이 커밋/스태시되지 않고 남아 있음 | 검사 1 실패 |
| `BLOCKED_SCOPE` | EXCLUDED 기능 구현 요구 또는 Secret 노출 위험 | 검사 7·8 실패(또는 검사 5에서 EXCLUDED Requirement 발견) |

한 Task에서 여러 검사가 동시에 실패할 수 있다. 이때는 다음 우선순위로 최종 출력을 하나만 정한다: `BLOCKED_DIRTY_TREE` > `BLOCKED_INPUT` > `BLOCKED_DEPENDENCY` > `BLOCKED_SCOPE`. 우선순위가 높은 것부터 해결해야 나머지 검사도 의미가 있기 때문이다(예: Working Tree가 더러우면 Depends On 완료 여부를 정확히 판단할 수 없다). 나머지 실패 사유도 보고에는 전부 남긴다 — 하나만 고치면 끝인 것처럼 숨기지 않는다.

## 실행 절차

1. `WAVE_ID`, `TASK_ID`가 모두 주어졌는지 확인한다. 없으면 즉시 `BLOCKED_INPUT`.
2. `TASKS/TASK-<TASK_ID>.md`를 Read한다. 없으면 즉시 `BLOCKED_INPUT`(Task ID 오타이거나 아직 `/gen-task-details`가 실행되지 않음).
3. 위 8개 검사를 순서대로 실행하며 실제 파일을 Read한다(추정하지 않는다).
4. §출력의 우선순위에 따라 최종 상태 하나를 정하고, 각 검사 결과(통과/실패/근거)를 함께 보고한다.
5. `READY_TO_IMPLEMENT`이더라도 이 Command는 구현을 시작하지 않는다 — 판정만 내리고 끝난다. 실제 구현은 사용자가 별도로 지시할 때 진행한다.

## 금지

- 코드·설정 파일을 생성·수정하지 않는다.
- git 상태를 바꾸는 명령을 실행하지 않는다(조회 명령만 허용: `git status` 등).
- 검사를 건너뛰고 `READY_TO_IMPLEMENT`로 단정하지 않는다.
- 여러 실패 사유 중 일부만 보고하고 나머지를 숨기지 않는다.

---
description: Wave 단위로 Task를 순차 실행한다(선택 → prepare-task 검사 → implement-task 구현 → 검증 → 상태 갱신 → 다음 Task). Branch·PR·Merge는 자동으로 만들지 않는다.
---

# /run-wave

`CLAUDE.md` 규칙 6·7(`/run-wave WXX`가 표준 개발 명령, Wave 내부 Task를 Depends On 순서로 한 번에 하나만 구현)을 실제로 수행하는 Command다. `/prepare-task`로 각 Task를 검사하고 `/implement-task`로 구현하는 것을 Wave 전체에 대해 자동으로 반복한다.

## 지원 명령

| 명령 | 동작 |
|---|---|
| `/run-wave W03` | Wave `W03`의 READY Task를 순서대로 하나씩 검사·구현한다(§본동작). |
| `/run-wave status` | 아무것도 구현하지 않고, 모든 Wave의 현재 상태를 읽어서 보고한다. |
| `/run-wave resume` | 가장 최근에 `WAITING_FOR_PREVIEW` 또는 `IN_PROGRESS`로 멈춘 Wave를 찾아 그 지점부터 이어서 실행한다. |
| `/run-wave dry-run W03` | Wave `W03`을 실제로 구현하지 않고, 어떤 순서로 어떤 Task를 처리할지와 각 Task의 `/prepare-task` 판정만 보고한다. |

## WAVE_PLAN과 WAVE_STATE

Wave 구성 자체는 `docs/DECISION_LOG.md` DEC-010에 따라 이 Command가 임의로 정의하지 않는다 — 사람이 미리 정해서 아래 두 파일에 반영해 둔 것을 읽기만 한다.

### WAVE_PLAN — `TASKS/WAVE_PLAN.md`

Wave별로 어떤 Task가 포함되는지, Task 뒤에 사람 Preview Checkpoint가 있는지를 정의하는 표.

```markdown
| Wave | Task ID | Preview Checkpoint After |
|---|---|---|
| W01 | SETUP-DEPENDENCIES | N |
| W01 | DB-SCHEMA-BASE | N |
| ... | ... | ... |
| W03 | PAGE-SCR001 | Y |
```

`Preview Checkpoint After = Y`는 그 Task가 `DONE`이 된 직후 사람이 화면을 확인해야 한다는 뜻이다(주로 `PAGE_OWNER` Task 뒤).

### WAVE_STATE — `TASKS/WAVE_STATE.md`

이 Command가 직접 갱신하는 실행 상태 로그. Task별로 최신 상태 한 줄만 유지한다.

```markdown
| Wave | Task ID | Status | Updated At | Note |
|---|---|---|---|---|
| W01 | SETUP-DEPENDENCIES | DONE | 2026-09-19T10:00:00 | Unit Test 없음, npm install 성공 |
| W03 | PAGE-SCR001 | WAITING_FOR_PREVIEW | 2026-09-20T09:00:00 | Preview Checkpoint |
```

`Status` ∈ `DONE` / `IN_PROGRESS` / `BLOCKED` / `WAITING_FOR_PREVIEW`. **표에 없는 Task는 아직 시작하지 않은 것**이다 — READY 여부는 저장하지 않고, 그때그때 `TASKS/00_TASK_LIST.md`의 `Depends On`과 `WAVE_STATE`의 `DONE` 목록을 대조해 실행 시점에 계산한다(READY = 아직 `DONE`이 아니고, 모든 Depends On이 `DONE`).

두 파일이 없으면 `/run-wave`는 구현을 시작하지 않고, 사람에게 먼저 `TASKS/WAVE_PLAN.md`를 만들어 달라고 요청한다(`WAVE_STATE.md`는 없으면 빈 상태로 새로 만들어도 된다 — 이건 순수 진행 기록이라 없어도 "아직 아무것도 안 함"으로 해석 가능).

## `/run-wave W03` 본동작

1. **WAVE_PLAN과 WAVE_STATE를 읽는다.** `TASKS/WAVE_PLAN.md`에서 `W03`에 속한 Task ID 목록(순서 포함)을 읽고, `TASKS/WAVE_STATE.md`에서 그 Task들의 현재 상태를 읽는다. `W03`이 `WAVE_PLAN.md`에 없으면 즉시 중단하고 그 사실을 보고한다.
2. **현재 Wave의 READY Task를 Depends On 순서로 하나 선택한다.** `TASKS/00_TASK_LIST.md`의 `Depends On`을 기준으로, 아직 `DONE`이 아니고 모든 Depends On이 `DONE`인 Task 중 `WAVE_PLAN.md`에 적힌 순서상 가장 앞선 것 하나를 고른다. 그런 Task가 없으면 7번 또는 §예외로 넘어간다.
3. **`/prepare-task` 규칙으로 검사한다.** 선택한 Task에 대해 `/prepare-task`의 8개 검사를 그대로 수행한다.
   - `READY_TO_IMPLEMENT`가 아니면: `WAVE_STATE.md`에 그 Task를 `BLOCKED`로 기록(사유 포함)하고, 그 Task는 건너뛴 채 같은 Wave의 다음 READY 후보가 있는지 다시 2번부터 시도한다. 더 시도할 Task가 없으면 실행을 멈추고 어떤 Task가 왜 막혔는지 보고한다.
4. **`/implement-task` 규칙으로 Task 하나를 구현한다.** `READY_TO_IMPLEMENT`로 확인된 Task에 대해 `/implement-task`의 8개 규칙(Expected Files 범위, AC 준수, Page Owner 조립, Unit Test, 필요 시 Playwright, 완료 보고 등)을 그대로 따라 구현한다. 구현 시작 시 `WAVE_STATE.md`에 `IN_PROGRESS`로 기록한다.
5. **관련 검증이 PASS하면 Task 상태를 DONE으로 갱신한다.** Unit Test(있다면)와 필요 시 Playwright Chromium Smoke가 모두 통과해야 `DONE`으로 기록한다. 하나라도 실패하면 `BLOCKED`로 기록하고 실패 내용을 보고한 뒤 실행을 멈춘다(다음 Task로 임의로 넘어가지 않는다).
6. **같은 Wave의 다음 READY Task를 계속 처리한다.** 이번 Task가 `DONE`이고 그 Task에 Preview Checkpoint가 없으면(`Preview Checkpoint After = N`), 2번으로 돌아가 같은 Wave 안에서 다음 READY Task를 찾아 반복한다.
7. **Wave Task가 모두 DONE이면 종료한다.** `WAVE_PLAN.md`에서 `W03`에 속한 모든 Task가 `WAVE_STATE.md`에 `DONE`으로 기록되어 있으면 "Wave W03 완료"를 보고하고 종료한다.
8. **사람 Preview Checkpoint가 있으면 WAITING_FOR_PREVIEW로 종료한다.** 방금 `DONE`이 된 Task의 `Preview Checkpoint After`가 `Y`이면, 남은 READY Task가 있어도 더 진행하지 않고 그 Task를 `WAITING_FOR_PREVIEW`로 기록한 뒤 종료한다(`CLAUDE.md` 규칙 22). 사람이 확인한 뒤 `/run-wave resume` 또는 `/run-wave W03`을 다시 실행해야 이어진다.

## `/run-wave status`

- 어떤 Task도 구현하지 않는다. `TASKS/WAVE_PLAN.md`와 `TASKS/WAVE_STATE.md`만 읽는다.
- Wave별로 전체 Task 수 대비 `DONE` 개수, 현재 `IN_PROGRESS`/`BLOCKED`/`WAITING_FOR_PREVIEW` Task가 있는지, 다음에 실행하면 어떤 Task가 선택될지를 요약해 보고한다.

## `/run-wave resume`

- `TASKS/WAVE_STATE.md`를 읽어 `WAITING_FOR_PREVIEW` 또는 `IN_PROGRESS` 상태인 Task가 속한 Wave를 찾는다. 여러 개면 가장 최근(`Updated At` 기준)인 Wave 하나를 고른다.
- `WAITING_FOR_PREVIEW`였다면, 사람이 실제로 Preview를 확인했다고 이번 요청에서 확인한 뒤에만 계속한다 — 확인 없이 자동으로 다음 Task로 넘어가지 않는다.
- `IN_PROGRESS`로 멈춰 있었다면(이전 실행이 중간에 끊겼다는 뜻), 그 Task부터 `/prepare-task`를 다시 실행해 여전히 유효한지 확인한 뒤 이어서 진행한다.
- 그 뒤로는 §본동작의 2~8번을 그대로 반복한다.
- 이어갈 `WAITING_FOR_PREVIEW`/`IN_PROGRESS` Task가 하나도 없으면 "이어갈 Wave 없음"을 보고하고 종료한다.

## `/run-wave dry-run W03`

- §본동작의 1~3번만 반복 수행한다(선택 → `/prepare-task` 검사) — **4번(구현)은 절대 실행하지 않는다.**
- Wave `W03`의 모든 Task를 Depends On 순서로 나열하면서, 각 Task가 지금 시점에 `READY_TO_IMPLEMENT`인지 `BLOCKED_*`인지, Preview Checkpoint가 어디에 걸리는지 표로 보고한다.
- `WAVE_STATE.md`를 갱신하지 않는다(읽기 전용 시뮬레이션).

## 자동 Branch·PR·Merge 미포함

- 이 Command는 git branch를 만들지 않는다. 항상 현재 checkout된 브랜치 위에서 파일을 바꾼다.
- PR을 생성하지 않는다. Merge를 실행하지 않는다(`docs/DECISION_LOG.md` DEC-012·DEC-013, `CLAUDE.md` 규칙 21).
- Commit도 기본적으로 하지 않는다 — `/implement-task`의 Commit 정책(사용자가 명시적으로 요청한 경우에만 Task 단위 Commit)을 그대로 물려받는다. `/run-wave` 실행 자체를 요청했다고 해서 각 Task를 자동으로 Commit하지 않는다. 사용자가 "Task마다 커밋해줘"처럼 명시했을 때만 Task 하나가 `DONE`이 될 때마다 그 Task 단위로 Commit한다.

## 예외 처리

- `TASKS/WAVE_PLAN.md`가 없으면: 구현을 시작하지 않고, 먼저 Wave 구성을 정의해 달라고 요청한다.
- 지정한 `WAVE_ID`가 `WAVE_PLAN.md`에 없으면: 존재하는 Wave 목록을 보여주고 중단한다.
- 같은 Wave 안에서 모든 남은 Task가 `BLOCKED`면(READY 후보가 없음): 실행을 멈추고 각 Task가 왜 막혔는지 `/prepare-task` 판정 사유를 그대로 보고한다 — 사용자가 해결할 때까지 기다린다.
- 이미 전부 `DONE`인 Wave를 다시 실행하면: 아무 것도 하지 않고 "이미 완료됨"을 보고한다.

## 금지

- Task를 Depends On 순서 없이 임의로 골라 처리하지 않는다.
- `/prepare-task`가 `BLOCKED_*`를 낸 Task를 억지로 구현하지 않는다.
- Unit Test/필요 시 Playwright가 실패했는데 `DONE`으로 기록하지 않는다.
- Preview Checkpoint가 있는 Task를 지나쳐 다음 Task로 자동 진행하지 않는다.
- git branch 생성, PR 생성, Merge를 실행하지 않는다.
- 사용자가 요청하지 않은 Commit을 하지 않는다.

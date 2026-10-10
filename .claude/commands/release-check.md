---
description: 릴리스 가능 여부를 7가지 근거로 확인하고 RELEASE_READY 또는 RELEASE_BLOCKED만 판정한다. 릴리스·배포·Merge를 직접 실행하지 않는다.
---

# /release-check

`docs/06_SRS_UIUX_REVISED.md` §3 Release Acceptance Criteria와 `docs/05_UIUX_APPROVED.md` §6을 실제 상태와 대조해, 지금 릴리스해도 되는지 **`RELEASE_READY`** 또는 **`RELEASE_BLOCKED`** 둘 중 하나로만 판정한다. 이 Command는 릴리스·배포·Merge를 직접 실행하지 않는다 — 판정과 근거 보고만 한다.

## 검사

아래 7가지를 전부 실제로 확인한다. 확인할 방법이 없거나 근거가 기록되어 있지 않으면 "통과"로 추정하지 않고 **미확인**으로 표시하며, 미확인은 실패와 동일하게 `RELEASE_BLOCKED` 사유가 된다.

### 1. Task·Wave 상태

- `TASKS/WAVE_PLAN.md`와 `TASKS/WAVE_STATE.md`를 Read한다.
- `WAVE_PLAN.md`에 정의된 모든 Wave의 모든 Task가 `WAVE_STATE.md`에서 `DONE`인지 확인한다.
- `BLOCKED` / `IN_PROGRESS` / `WAITING_FOR_PREVIEW` 상태로 남아 있는 Task가 하나라도 있으면 실패.
- 두 파일 중 하나라도 없으면 미확인(실패로 취급).

### 2. 5개 Page Owner DONE

- `PAGE-SCR001`, `PAGE-SCR002`, `PAGE-SCR003`, `PAGE-SCR004`, `PAGE-SCR005` 5개 전부가 `TASKS/WAVE_STATE.md`에서 `DONE`인지 확인한다(검사 1과 별개로 명시적으로 다시 확인한다 — Page Owner는 릴리스의 최소 조건이므로).
- 하나라도 `DONE`이 아니면 실패.

### 3. CI PASS

- `gh run list --branch <현재 브랜치> --limit 5` (또는 저장소에 맞는 동등 명령)로 최신 CI 실행 결과를 조회한다.
- `gh` 명령을 쓸 수 없거나 인증이 안 되어 있으면, 사람에게 최신 CI(GitHub Actions `CI-LINT-BUILD-TEST` 워크플로) 실행 결과 링크나 상태를 직접 알려달라고 요청한다 — 추측하지 않는다.
- 최신 실행이 실패했거나 확인할 수 없으면 실패.

### 4. Playwright Smoke PASS

- `E2E-PUBLIC-SMOKE`, `E2E-TRAVEL-TOOLS`, `E2E-MATE-AUTH` 3개 스펙을 `--project=chromium`으로 다시 실행할 수 있는 환경이면 실제로 실행해 결과를 확인한다.
- 지금 실행할 수 없는 환경이면(예: Supabase 연결 필요) `TASKS/WAVE_STATE.md`의 해당 Task Note에 기록된 마지막 통과 근거(실행 시각, 결과)를 확인한다. 기록이 없거나 오래돼 보이면 미확인으로 표시한다.
- 셋 중 하나라도 실패/미확인이면 실패.

### 5. Supabase 6개 Table·기본 RLS 확인 기록

- `DB-SCHEMA-BASE`, `DB-RLS-BASE` Task가 `DONE`인지, 그리고 `TASKS/WAVE_STATE.md`의 Note에 "테이블 6개 확인", "RLS 정책 적용 확인" 같은 실제 확인 기록이 있는지 본다.
- `MANUAL-SUPABASE-CONFIG` Task가 `DONE`이고 Supabase 프로젝트 연결·정책 확인 기록이 있는지도 함께 본다.
- 이 Command는 Supabase 콘솔에 직접 접속할 수 없으므로, 사람이 남긴 확인 기록이 없으면 미확인 → 실패. 기록이 있다면 테이블 수가 `docs/ARCHITECTURE.md` §8의 6개(`user_profile`, `mate_post`, `mate_application`, `user_block`, `report`, `admin_setting`)와 일치하는지 이름까지 대조한다.

### 6. Vercel Preview Checkpoint

- `MANUAL-VERCEL-DEPLOY` Task가 `DONE`인지, Note에 Preview/Production URL과 HTTPS 확인 기록이 있는지 본다.
- `TASKS/WAVE_PLAN.md`에서 `Preview Checkpoint After = Y`로 표시된 모든 Task(주로 5개 Page Owner)가 `WAVE_STATE.md`에서 `WAITING_FOR_PREVIEW`를 거쳐 실제로 `DONE`으로 넘어갔는지 확인한다 — `WAITING_FOR_PREVIEW`에 멈춘 채 남아 있는 것이 있으면 사람이 아직 그 화면을 확인하지 않은 것이므로 실패.
- 기록이 없으면 미확인 → 실패.

### 7. EXCLUDED 목록

- `python scripts/audit_tasks.py`를 실행한다(`python3`이 실패하면 `python`으로 대체하고 그 사실을 보고한다).
- `AUDIT_PASS`가 아니면 실패.
- `TASKS/TASK_AUDIT_REPORT.md`의 Requirement 커버리지에서 `EXCLUDED(NON_IMPLEMENTATION)` 개수가 `docs/PROJECT_SCOPE.md`/`docs/UIUX_TRACEABILITY.md` 기준 EXCLUDED 총수와 일치하는지 확인한다(현재 기준 25개) — 줄어들었다면 EXCLUDED 항목이 임의로 삭제되었거나 몰래 구현된 것이므로 실패, 늘어났다면 범위 정의 없이 새로 제외한 것이므로 이 역시 실패(별도 승인 없이 EXCLUDED를 추가하지 않는다).

## 판정

| 판정 | 조건 |
|---|---|
| `RELEASE_READY` | 검사 1~7 전부 통과(미확인 0건) |
| `RELEASE_BLOCKED` | 검사 1~7 중 하나라도 실패 또는 미확인 |

최종 결과는 `RELEASE_READY` 또는 `RELEASE_BLOCKED` 중 하나만 명확히 출력한다. `RELEASE_BLOCKED`면 실패/미확인한 검사 번호와 이유를 전부 나열한다(하나만 고치면 되는 것처럼 일부만 보고하지 않는다).

## 실행 절차

1. `TASKS/WAVE_PLAN.md`, `TASKS/WAVE_STATE.md`, `TASKS/00_TASK_LIST.md`, `TASKS/TASK_AUDIT_REPORT.md`, `docs/PROJECT_SCOPE.md`, `docs/UIUX_TRACEABILITY.md`, `docs/ARCHITECTURE.md`를 실제로 Read한다.
2. §검사 1~7을 순서대로 확인한다.
3. `python scripts/audit_tasks.py`를 실행해 검사 7의 근거를 확보한다.
4. 가능하면 Playwright Chromium Smoke를 실제로 재실행해 검사 4의 근거를 새로 확보한다.
5. §판정에 따라 `RELEASE_READY`/`RELEASE_BLOCKED`를 확정하고, 7개 검사 각각의 통과/실패/미확인 상태와 근거를 표로 보고한다.

## 금지

- 이 Command 안에서 실제 배포, Merge, Tag 생성, Vercel Production 승격 등 릴리스 행위를 직접 수행하지 않는다 — 판정만 한다.
- 근거를 확인할 수 없는 항목을 통과로 추정하지 않는다.
- 일부 검사만 보고 전체를 `RELEASE_READY`로 단정하지 않는다 — 7개 전부를 항상 확인한다.
- `TASKS/WAVE_STATE.md`, `TASKS/WAVE_PLAN.md`, `TASKS/00_TASK_LIST.md` 등 어떤 파일도 이 Command에서 수정하지 않는다(읽기 전용).

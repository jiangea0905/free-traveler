# Project State — Free Traveler

**Document ID:** PROJECT-STATE-001
**최종 갱신:** 2026-09-20 (초기 스냅샷 — 아직 구현 착수 전)
**갱신 주체:** 이 문서는 사람이 손으로 고치는 문서가 아니라 `/run-wave`, `/prepare-task`, `/release-check` 실행 결과로 갱신되는 살아있는 상태 기록이다. 각 필드는 실제로 확인한 값만 적는다 — 확인되지 않은 값을 "정상"으로 추정해 적지 않는다.

---

## 필드 요약

| 필드 | 값 |
|---|---|
| Harness Schema | `traveler-screen-route-v1` |
| Design Version | D-001 (Status: LOCKED) |
| Scope Mode | `docs/PROJECT_SCOPE.md` 기준 — IMPLEMENT 89 / EXCLUDED 25 (합계 114) |
| Current Wave | 없음 — `TASKS/WAVE_PLAN.md`가 아직 생성되지 않음 |
| Current Task | 없음 |
| Completed Tasks | 0 / 59 |
| Blocked Tasks | 0(진행 시도 자체가 없어 `BLOCKED` 판정 이력 없음) — 단, §Deferred Items 아래 환경 블로커 참고 |
| Latest CI | 실행 이력 없음 |
| Supabase State | 미확인(프로젝트 존재 여부 확인 안 됨) |
| Vercel Preview URL | 없음 |
| Screen Checkpoints | SCR-001~005, FINAL 전부 `PENDING`(아래 §Screen Checkpoints 참고) |
| Playwright State | 미설치·미실행 |
| Deferred Items | EXCLUDED 25개(`docs/UIUX_TRACEABILITY.md`, `TASKS/00_TASK_LIST.md` §NON_IMPLEMENTATION) |
| Next Action | `TASKS/WAVE_PLAN.md` 작성 → `SETUP-DEPENDENCIES`부터 `/prepare-task` 실행 |

---

## Harness Schema

`traveler-screen-route-v1` — `design-reference/SCREEN_ROUTE_CONTRACT.json`의 `schema_version`, `CLAUDE.md`의 `HARNESS_SCHEMA` 값과 일치. 변경 이력 없음.

## Design Version

**D-001**, Status: `LOCKED`(`design-reference/DESIGN_MANIFEST.md`). 정본 파일은 `design-reference/D-001/DESIGN.md`. LOCKED 동안 이 파일을 직접 수정하지 않는다.

## Scope Mode

`docs/PROJECT_SCOPE.md`의 4단계 분류(`IMPLEMENT` / `IMPLEMENT(축소)` / `IMPLEMENT(대체)` / `EXCLUDED`)를 그대로 따른다. `docs/UIUX_TRACEABILITY.md` 기준 REQ-FUNC 80개 + REQ-NF 34개 = 114개 중 IMPLEMENT 계열 89개, EXCLUDED 25개. `python scripts/audit_tasks.py`가 이 숫자를 매번 재확인한다(마지막 실행: `AUDIT_PASS`, 18개 검사 전부 통과 — `TASKS/TASK_AUDIT_REPORT.md` 참고).

## Current Wave / Current Task

- **Current Wave:** 없음. `TASKS/WAVE_PLAN.md`가 아직 만들어지지 않아 `/run-wave`가 실행된 적이 없다.
- **Current Task:** 없음. Wave가 없으므로 진행 중인 Task도 없다.
- 다음 단계는 §Next Action 참고.

## Completed Tasks

**0 / 59.** `TASKS/00_TASK_LIST.md`에 정의된 59개 Task 중 실제로 구현이 완료된 것은 없다. `TASKS/WAVE_STATE.md` 자체가 아직 존재하지 않는다(어떤 Task도 `DONE` 기록이 없음).

## Blocked Tasks

현재 `/prepare-task`로 검사를 시도해 `BLOCKED_*`를 받은 이력 자체가 없다(아직 아무 Task도 시도하지 않았기 때문). 다만 시도하면 즉시 막힐 것으로 확인되는 환경 문제가 있다 — 아래 §Deferred Items의 환경 블로커 참고. 이 블로커는 `docs/ARCHITECTURE.md` §16과 같은 근거이며, 여기에 하나 더 추가한다.

| # | 블로커 | 확인 방법 | 영향 |
|---|---|---|---|
| 1 | `package.json`에 Supabase/zod/Vitest/Playwright 미포함 | `cat package.json` | `SETUP-DEPENDENCIES` 전까지 관련 코드 작성 불가 |
| 2 | `.env.local`/`.env.example` 없음 | 저장소 루트에 `.env*` 없음 | Supabase 연동 Task 전부 |
| 3 | Supabase 프로젝트 존재 여부 미확인 | 로컬에서 확인 불가 | §Supabase State |
| 4 | `.github/workflows/` 없음 | 디렉터리 없음 | §Latest CI |
| 5 | `supabase/` 마이그레이션 없음 | 디렉터리 없음 | §Supabase State, DB 관련 Task 전부 |
| 6 | **git 저장소 자체가 초기화되지 않음**(`git rev-parse --is-inside-work-tree` → `fatal: not a git repository`) | 위 명령 실행 결과 | Commit(`/implement-task` Commit 정책), CI(GitHub Actions는 원격 저장소 필요), Vercel Git 연동 전부 불가능 — 착수 전 가장 먼저 해결해야 하는 항목 |

## Latest CI

실행 이력 없음. `.github/workflows/`가 없고(§Blocked Tasks #4) 이 저장소는 아직 git 저장소가 아니다(#6). `CI-LINT-BUILD-TEST` Task가 완료되고 GitHub 원격 저장소에 연결된 뒤에야 이 필드가 채워진다.

## Supabase State

**미확인.** `supabase/` 디렉터리, `.env*` 파일이 없어 프로젝트 연결 여부·6개 Table 존재 여부·RLS 정책 적용 여부를 로컬에서 확인할 수 없다. `DB-SCHEMA-BASE` → `DB-RLS-BASE` → `MANUAL-SUPABASE-CONFIG` Task가 끝나야 이 필드에 실제 값(프로젝트 리전, 테이블 6개 확인 시각, RLS 확인 시각)을 적을 수 있다.

## Vercel Preview URL

없음. 아직 어떤 Wave도 실행되지 않아 배포할 코드가 준비되지 않았다. `MANUAL-VERCEL-DEPLOY` Task 완료 후 이 필드에 실제 Preview/Production URL을 적는다.

## Screen Checkpoints

`docs/06_SRS_UIUX_REVISED.md`/`design-reference/SCREEN_ROUTE_CONTRACT.json`의 5개 Screen과 최종 릴리스 체크포인트. 초기값은 전부 `PENDING`이며, 각 Screen의 Page Owner Task가 `DONE`이 되고 사람이 Preview를 확인하면 `CONFIRMED`(또는 재확인 필요 시 `NEEDS_REVISION`)로 갱신한다. `FINAL`은 `/release-check`가 `RELEASE_READY`를 낸 시점에만 `CONFIRMED`로 바뀐다.

| Screen | Route | 상태 |
|---|---|---|
| SCR-001 | `/` | `PENDING` |
| SCR-002 | `/about` | `PENDING` |
| SCR-003 | `/travel-tools` | `PENDING` |
| SCR-004 | `/mates` | `PENDING` |
| SCR-005 | `/account` | `PENDING` |
| FINAL | — | `PENDING` |

## Playwright State

**미설치·미실행.** `package.json`에 `@playwright/test`가 없고 `e2e/` 디렉터리도 없다. `SETUP-DEPENDENCIES` → `E2E-PUBLIC-SMOKE`/`E2E-TRAVEL-TOOLS`/`E2E-MATE-AUTH` Task가 끝나야 Chromium Smoke 실행 결과(마지막 실행 시각, PASS/FAIL)를 이 필드에 기록한다.

## Deferred Items

- **EXCLUDED Requirement 25개** — `docs/UIUX_TRACEABILITY.md`와 `TASKS/00_TASK_LIST.md`의 `## NON_IMPLEMENTATION` 표에 근거·후속 방향과 함께 보존되어 있다. 이번 릴리스 범위에서 구현하지 않는다(`docs/DECISION_LOG.md` DEC-014).
- **명시적 범위 제외**(`docs/ARCHITECTURE.md` §17): 콘텐츠 CMS, 외부 Email 공급자 연동, Monitoring/관측 인프라. 착수 차단이 아니라 애초에 만들 계획이 없는 항목이다.
- **환경 블로커 6개**(§Blocked Tasks) — 착수 자체를 막는 항목이며, EXCLUDED와 달리 반드시 해소해야 한다.

## Next Action

1. **git 저장소 초기화**(§Blocked Tasks #6) — 이후 모든 Commit·CI·Vercel 연동의 전제 조건.
2. `TASKS/WAVE_PLAN.md` 작성 — `TASKS/00_TASK_LIST.md`의 Depends On 그래프를 근거로 Wave 구성을 정의한다(`.claude/commands/run-wave.md` §WAVE_PLAN 형식 참고).
3. 첫 Wave의 첫 Task는 Depends On이 없는 `SETUP-DEPENDENCIES`다 — `/prepare-task W01 SETUP-DEPENDENCIES`부터 시작한다.

이 문서는 위 세 가지가 진행되는 대로, 그리고 이후 각 Wave 실행마다 갱신되어야 한다. 갱신하지 않고 오래된 값을 그대로 두면 이 문서 자체가 §커버리지 검증 대상이 될 수 있다.

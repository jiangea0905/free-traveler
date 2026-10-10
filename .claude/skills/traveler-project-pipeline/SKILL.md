---
name: traveler-project-pipeline
description: Traveler PRD/SRS에서 Task를 생성·상세화·감사하고 5개 Screen과 Wave 개발을 지원하는 프로젝트 Skill
---

# Traveler Project Pipeline

이 Skill은 Free Traveler PRD/SRS를 실제 구현 Task로 변환하는 3단계 파이프라인(`/gen-tasklist` → `/gen-task-details` → `/audit-tasks`)의 규칙을 담는다. 이 파이프라인이 만든 `TASKS/00_TASK_LIST.md`와 `TASKS/TASK-<ID>.md`는 이후 `/run-wave WXX`(Wave 단위 개발, `CLAUDE.md` 규칙 6·7)가 그대로 소비하는 입력이다.

**이 Skill은 `CLAUDE.md`의 전역 규칙을 대체하지 않는다.** 이 문서와 `CLAUDE.md`가 같은 주제를 다룰 때는 항상 `CLAUDE.md`가 우선하며, 아래 각 절에서 해당하는 `CLAUDE.md` 규칙 번호를 명시했다. 이 Skill은 `CLAUDE.md`가 다루지 않는 **파이프라인 생성 절차**(입력 읽기, 형식, ID 규칙, 감사 스크립트)를 보충한다.

## 1. 입력 문서 목록

Task를 생성·상세화하기 전에 반드시 아래 문서를 실제로 Read한다(추정·기억으로 대체하지 않는다).

| 문서 | 역할 |
|---|---|
| `docs/06_SRS_UIUX_REVISED.md` | Requirement 정본(`CLAUDE.md` 규칙 2) |
| `docs/PROJECT_SCOPE.md` | IMPLEMENT/EXCLUDED 분류 정본(`CLAUDE.md` 규칙 3) |
| `docs/UIUX_TRACEABILITY.md` | 114개 Requirement 전수 목록 |
| `design-reference/D-001/DESIGN.md` | 디자인 정본, Status: LOCKED(`CLAUDE.md` 규칙 4) |
| `design-reference/UI_CONTRACT.md` | 화면별 Section 순서·최소 콘텐츠 수 |
| `design-reference/SCREEN_ROUTE_CONTRACT.json` | Screen 정본(`CLAUDE.md` 규칙 5) |
| `package.json` | 현재 의존성 상태(`CLAUDE.md` 규칙 1) |
| `scripts/validate_inputs.py`의 출력(`src/app` 파일 트리 스냅샷) | 이미 존재하는 파일과 신규 파일 구분 |

각 단계 시작 전 `scripts/validate_inputs.py`를 실행해 위 입력이 정상인지 확인한다. 이 환경의 `python3`가 실패하면(깨진 인터프리터) `python`으로 대체 실행하고 그 사실을 보고한다.

## 2. 5개 Screen과 Page Entry

Screen 목록·Route·Page Entry의 정본은 `design-reference/SCREEN_ROUTE_CONTRACT.json`이다(`CLAUDE.md` 규칙 5). 다른 문서의 서술이 이 JSON과 다르면 JSON을 따른다.

| Screen ID | 구분 | Route | Page Entry |
|---|---|---|---|
| SCR-001 | 핵심 | `/` | `src/app/page.tsx` |
| SCR-002 | 보조 | `/about` | `src/app/about/page.tsx` |
| SCR-003 | 핵심 | `/travel-tools` | `src/app/travel-tools/page.tsx` |
| SCR-004 | 핵심 | `/mates` | `src/app/mates/page.tsx` |
| SCR-005 | 핵심 | `/account` | `src/app/account/page.tsx` |

이 5개 외의 새 최상위 Page Entry를 추가하지 않는다. 각 Screen에는 Page Owner Task를 정확히 1개씩 만든다(`PAGE-SCR001`~`PAGE-SCR005`).

## 3. IMPLEMENT·EXCLUDED 상태 처리 규칙

- `docs/PROJECT_SCOPE.md`의 분류는 `IMPLEMENT` / `IMPLEMENT(축소)` / `IMPLEMENT(대체)` / `EXCLUDED` 네 가지다.
- `docs/UIUX_TRACEABILITY.md`의 **114개 Requirement 전부**가 `TASKS/00_TASK_LIST.md`에서 다음 둘 중 정확히 하나에 존재해야 한다: (a) `IMPLEMENT` 계열 → 어떤 Task의 Requirement Ref, (b) `EXCLUDED` → `## NON_IMPLEMENTATION` 표.
- 같은 Requirement가 Task Requirement Ref와 NON_IMPLEMENTATION 표 양쪽에 동시에 나타나지 않는다.
- `IMPLEMENT(축소)`/`IMPLEMENT(대체)`는 Task의 `Implementation Status` 열에 그대로 옮기고, 축소·대체 사유는 해당 Task 상세의 `Project Scope` 절에 원문 그대로 적는다.

## 4. Task List·상세 Task 형식

**Task List** (`TASKS/00_TASK_LIST.md`): 상단 요약(총 Task 수, Category별 개수) → Category별 표(열: `Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files`) + 표 각 행 아래 `**<TASK_ID>**` AC 블록(`Functional AC` / `Visual AC` / `Security/Privacy AC` / `Verify` / `Priority`) → `## NON_IMPLEMENTATION` 표(`Requirement | 근거(PROJECT_SCOPE.md) | 후속 방향`) → `## 커버리지 검증`.

**상세 Task 파일** (`TASKS/TASK-<TASK_ID>.md`): 다음 14개 절을 이 순서로 포함한다 — `Context`, `Project Scope`, `Requirement Ref`, `Screen / Route / Page Entry`, `Design Ref`, `Depends On`, `Expected Files`, `Functional AC`, `Visual AC`, `Security/Privacy AC`, `Test Cases`, `Verify`, `Definition of Done`, `Forbidden`. `Expected Files` 절 바로 아래에 "이 목록 밖의 파일은 생성·수정하지 않는다"를 명시한다(`CLAUDE.md` 규칙 8과 연결).

Task List의 Task 수와 상세 파일 수는 항상 1:1이어야 한다.

## 5. Page Owner·Component 분리 규칙

- **Page Owner Task**(`PAGE-SCR00N`): 화면 1개를 최종 조립한다. 그 자체로 새 UI를 그리지 않고, 이미 완료된 Component/Data/API 산출물을 Page Entry에서 **실제로 조립**한다(`CLAUDE.md` 규칙 9).
- **Component Task**(`COMP-SCR00N-<slug>`): 화면 안의 Section 또는 기능 1개를 구현한다.
- Page Owner는 같은 Screen에 속한 모든 Component Task를 Depends On에 넣는다.
- `PAGE-SCR001`은 Next.js 기본 스타터 콘텐츠 완전 제거 AC를 가진다(`CLAUDE.md` 규칙 10).
- `PAGE-SCR003`은 항공편·숙소·동행 구하기 세 탭을 실제로 조립하는 AC를 가진다(`CLAUDE.md` 규칙 11).
- `PAGE-SCR005`는 Guest·Member·Admin 상태를 실제로 조립하고, 역할에 없는 영역은 DOM에 렌더링하지 않는 AC를 가진다.

## 6. DB 6개 Table과 정적 Data 경계

- Supabase 테이블은 `user_profile`, `mate_post`, `mate_application`, `user_block`, `report`, `admin_setting` 6개를 기본으로 하며, 이를 크게 넘지 않는다.
- 여행지·국가 안전정보·`free_traveler` 대표 프로필은 **DB 테이블이 아니라 `src/data`의 정적 TypeScript Data**로 만든다(`CLAUDE.md` 규칙 16). 이 콘텐츠를 위한 CRUD API나 DB 테이블을 Task로 만들지 않는다.
- DB Schema(`DB-SCHEMA-BASE`) · RLS(`DB-RLS-BASE`) · Access(`DB-ACCESS`) · Seed(`DB-SEED-BASE`) Task는 항상 함께 존재해야 한다.

## 7. 외부 입력 비저장 불변조건

항공·숙소 입력값(국가·지역·날짜)은 서버·DB·URL 쿼리·로그·분석 이벤트 **어디로도 전송하지 않는다**(`CLAUDE.md` 규칙 12). 이 값을 다루는 모든 Task(Component/Page Owner/Shared)의 상세 파일에는 "Client Component의 일시 상태로만 유지하며 네트워크 요청이 없다"는 문장을 `Security/Privacy AC` 또는 `Forbidden` 절에 명시한다. 이 값을 위한 API Route나 DB 테이블을 만들지 않는다.

## 8. 기본 Auth·성인·RLS 규칙

- Supabase 쓰기는 Auth · 동행(모집글/참가요청/차단) · 신고 · 관리자 설정 범위로 제한한다(`CLAUDE.md` 규칙 13).
- 성인 확인은 정확한 생년월일이 아니라 `is_adult`/`adult_verified_at` 상태만 저장한다.
- RLS를 우회하는 Client 코드를 작성하지 않는다(`CLAUDE.md` 규칙 14). Service Role Key는 Server 전용 모듈 밖으로 절대 내보내지 않는다(`CLAUDE.md` 규칙 15).
- RLS 정책은 테이블당 최소 개수로 유지한다(기본값: 본인 행만 읽기/쓰기, 공개 열람이 필요한 테이블만 최소한으로 넓힘).

## 9. Playwright Chromium Smoke 범위

Playwright 테스트 Task는 Chromium 대상 Smoke Test 3개만 만든다: `E2E-PUBLIC-SMOKE`, `E2E-TRAVEL-TOOLS`, `E2E-MATE-AUTH`(`CLAUDE.md` 규칙 18). 다중 브라우저 매트릭스, 시각적 회귀, 부하 테스트 Task를 만들지 않는다.

## 10. Wave 내부 순차 실행

- 이 파이프라인이 만든 Task는 `/run-wave WXX`(`CLAUDE.md` 규칙 6)로 실행된다. Wave 안의 Task는 `TASKS/00_TASK_LIST.md`의 Depends On 순서에 따라 **한 번에 하나씩 순차로** 구현한다(`CLAUDE.md` 규칙 7).
- 이 Skill 자체(Task 생성·상세화·감사)도 같은 원칙을 따른다: `/gen-tasklist` → `/gen-task-details` → `/audit-tasks` 순서를 건너뛰거나 병렬로 실행하지 않는다.
- Wave 경계는 이 문서가 고정하지 않는다. 실행 시점에 Depends On 그래프를 기준으로 정한다(`docs/DECISION_LOG.md` DEC-010·DEC-011).

## 11. EXCLUDED 보호

- `EXCLUDED` Requirement는 상세 구현 Task를 만들지 않는다. `## NON_IMPLEMENTATION` 표에 근거와 후속 방향을 남기고, 어떤 문서를 새로 만들어도 이 표에서 삭제하지 않는다(`docs/DECISION_LOG.md` DEC-014).
- `docs/PROJECT_SCOPE.md`/`docs/UIUX_TRACEABILITY.md`에서 EXCLUDED로 분류된 기능을 임의로 구현하지 않는다(`CLAUDE.md` 규칙 19).
- 어떤 Task 상세 파일의 `Requirement Ref`에도 EXCLUDED Requirement ID를 넣지 않는다 — `scripts/audit_tasks.py`의 검사 18번이 이를 확인한다.

## 12. AWS·EC2·자동 Merge 금지

- Prisma·다른 ORM·AWS·EC2 관련 Task를 만들지 않는다(`CLAUDE.md` 규칙 17, Harness Marker `AWS_ENABLED=false`).
- 자동 Merge Runner, 자동 PR 병합 Task나 워크플로를 만들지 않는다(`CLAUDE.md` 규칙 21, Harness Marker `AUTO_MERGE=false`). PR·Merge는 사람이 수동으로 수행한다(`docs/DECISION_LOG.md` DEC-012·DEC-013).

---

## 감사(`/audit-tasks`)

`/gen-task-details` 마지막 단계와 `/audit-tasks`는 `scripts/audit_tasks.py`를 실행해 위 규칙(1~12절에 대응하는 18개 검사)을 확인하고, `TASKS/TASK_MANIFEST.csv`·`TASKS/TASK_AUDIT_REPORT.md`를 갱신한다. `AUDIT_FAIL`이면 그 사실과 실패 검사 번호를 그대로 보고한다 — 감사를 생략하거나 결과를 숨기고 완료로 보고하지 않는다.

## 예상 Task 개수

45~65개 내외를 예상하지만 개수 자체는 완료 조건이 아니다. 완료 조건은 위 12개 규칙 준수와 `scripts/audit_tasks.py`의 `AUDIT_PASS`다.

# Decision Log — Free Traveler

**Document ID:** DECISIONLOG-001
**작성일:** 2026-09-19
**상태 표기:** 모든 항목 `Accepted`(이미 다른 승인된 문서에서 확정되었고, 이 문서는 그 결정을 한곳에 모아 번호를 붙인 기록이다). 결정을 뒤집을 때는 새 행을 추가하지 않고 해당 DEC 항목의 `Status`를 `Superseded`로 바꾸고 사유·후속 DEC ID를 적는다.

---

## DEC-001 — 실제 개발 루트는 `traveler/app`

- **Status:** Accepted
- **결정:** 이 저장소에서 실제 코드가 작성되는 루트는 `traveler/app`이다(`package.json`, `src/app`, `TASKS/`, `docs/`, `design-reference/`가 모두 이 아래에 위치).
- **배경:** 상위 `traveler/` 디렉터리는 프로젝트 문서·산출물의 컨테이너일 뿐이며, Next.js 애플리케이션 자체(`next.config.ts`, `tsconfig.json`, `src/app`)는 `app` 하위에 스캐폴딩되어 있다.
- **영향:** 앞으로의 모든 Task, CI 워크플로, 배포 설정의 작업 디렉터리(working directory)는 `traveler/app`을 기준으로 삼는다. 상위 경로에 별도 애플리케이션 코드를 두지 않는다.
- **관련 문서:** `docs/ARCHITECTURE.md` §1, `package.json`

## DEC-002 — 디자인 Screen은 핵심 4개·보조 1개

- **Status:** Accepted
- **결정:** 승인된 디자인 Screen은 정확히 5개이며, 핵심(Core) 4개(SCR-001, SCR-003, SCR-004, SCR-005)와 보조(Auxiliary) 1개(SCR-002)로 구분한다.
- **배경:** SRS Baseline의 다중 Route를 5개 화면의 탭·Drawer·패널로 통합하는 과정에서, 대표 소개(SCR-002)는 서비스의 핵심 과업(탐색·여행 준비·동행·계정)과 달리 신뢰 구축용 보조 콘텐츠로 분류되었다.
- **영향:** 6번째 핵심/보조 Screen을 추가하지 않는다. 새 기능은 기존 5개 화면 안의 탭·Section으로 편입한다.
- **관련 문서:** `design-reference/SCREEN_ROUTE_CONTRACT.json`(`category_summary`), `docs/PROJECT_SCOPE.md` §1, `docs/ARCHITECTURE.md` §2

## DEC-003 — `/travel-tools`에 항공·숙소·동행 작성을 통합

- **Status:** Accepted
- **결정:** 항공편 찾기, 숙소 찾기, 동행 모집글 작성을 별도 Route가 아니라 `/travel-tools` 한 화면의 3개 탭으로 통합한다.
- **배경:** 세 기능 모두 "여행 조건을 먼저 정리한 뒤 다음 행동(외부 이동 또는 게시)으로 넘어간다"는 동일한 사용자 흐름을 공유한다. 별도 Route로 분리하면 화면 수가 늘고 내비게이션이 복잡해진다.
- **영향:** `src/app/travel-tools/page.tsx` 하나가 세 흐름의 Page Owner다. 세 탭은 각자 독립된 입력·검증·완료 상태를 가지며, 탭 전환이 다른 탭의 상태를 지우지 않는다.
- **관련 문서:** `docs/06_SRS_UIUX_REVISED.md` §1, `design-reference/UI_CONTRACT.md`(SCR-003), `design-reference/D-001/DESIGN.md` §Form · Tabs

## DEC-004 — 여행지·안전·대표는 정적 TypeScript Data

- **Status:** Accepted
- **결정:** 여행지, 국가 안전정보, `free_traveler` 대표 프로필 콘텐츠는 데이터베이스 테이블이 아니라 `src/data`의 정적 TypeScript 모듈로 관리한다.
- **배경:** 콘텐츠 CMS·편집자 워크플로를 이번 범위에서 만들지 않기로 했고(DEC-014 참고), 콘텐츠 변경 빈도가 낮아 코드 변경(PR)으로 충분하다.
- **영향:** 이 콘텐츠를 위한 CRUD API, 관리자 편집 화면, DB 테이블(DEC-006의 6개에 포함되지 않음)을 만들지 않는다.
- **관련 문서:** `docs/PROJECT_SCOPE.md`(정적 데이터 지정), `docs/ARCHITECTURE.md` §6, `TASKS/TASK-DATA-DESTINATIONS.md`/`TASK-DATA-SAFETY.md`/`TASK-DATA-REPRESENTATIVE.md`

## DEC-005 — Supabase는 Auth와 동행 기능 중심

- **Status:** Accepted
- **결정:** Supabase는 이메일 인증(성인 확인 포함)과 동행(Mate) 관련 기능(모집글·참가 요청·차단·신고·관리자 설정)을 위해서만 사용한다.
- **배경:** 콘텐츠는 DEC-004에 따라 정적 데이터로 분리되므로, Supabase의 역할을 "회원·상호작용 데이터" 저장소로 한정하는 것이 책임 경계가 명확하다.
- **영향:** Supabase를 콘텐츠 관리 백엔드로 확장하지 않는다.
- **관련 문서:** `docs/ARCHITECTURE.md` §7

## DEC-006 — DB는 6개 Table로 제한

- **Status:** Accepted
- **결정:** Supabase PostgreSQL 테이블은 정확히 `user_profile`, `mate_post`, `mate_application`, `user_block`, `report`, `admin_setting` 6개로 제한한다.
- **배경:** 동행 기능(DEC-005)의 최소 데이터 모델이 6개 테이블로 충분하며, 감사 로그·분석 이벤트·콘텐츠 테이블은 다른 결정(DEC-004, DEC-014)에 의해 이미 범위 밖이다.
- **영향:** 새 기능 추가 시 이 6개 테이블의 컬럼 확장을 우선 검토하고, 신규 테이블은 원칙적으로 만들지 않는다.
- **관련 문서:** `docs/PROJECT_SCOPE.md`, `docs/ARCHITECTURE.md` §8, `TASKS/TASK-DB-SCHEMA-BASE.md`

## DEC-007 — 항공·숙소 입력은 Browser Memory에만 유지

- **Status:** Accepted
- **결정:** 항공·숙소 입력 폼(국가·지역·날짜)은 Client Component의 일시 상태(Browser Memory)로만 유지하고, API·DB·URL 쿼리·서버 로그 어디에도 전송·저장하지 않는다.
- **배경:** 이 기능은 실제 예약·검색이 아니라 외부 사이트로의 안내이며, 사용자가 입력한 여행 조건을 서버가 보유할 이유가 없다. 개인정보 최소 수집 원칙과도 일치한다.
- **영향:** 이 입력값을 위한 API Route, DB 테이블, 분석 이벤트 속성을 만들지 않는다. 새로고침 시 값이 사라지는 것은 의도된 동작이다.
- **관련 문서:** `docs/06_SRS_UIUX_REVISED.md`(CON-01 계열), `docs/ARCHITECTURE.md` §4·§5, `TASKS/TASK-SHARED-EXTERNAL-LINKOUT.md`

## DEC-008 — Airbnb `DESIGN.md`는 vendor 참고본, D-001이 실제 정본

- **Status:** Accepted
- **결정:** `design-reference/vendor/airbnb/DESIGN-airbnb.md`는 구조적 영감을 얻기 위한 참고 자료일 뿐이며, 실제 구현이 따라야 할 디자인 정본은 `design-reference/D-001/DESIGN.md`(Status: LOCKED)다.
- **배경:** Airbnb 참고본의 색상·서체·상표 요소를 그대로 재현하면 상표권·브랜드 혼동 문제가 생긴다. 구조(백색 캔버스, 단일 포인트 컬러, 얕은 그림자 1단계 등)만 참고하고 토큰은 Free Traveler 고유 값으로 새로 정의했다.
- **영향:** 구현 중 색상·서체·컴포넌트 값이 필요하면 항상 D-001을 먼저 참조한다. Airbnb 참고본에서 값을 직접 복사하지 않는다.
- **관련 문서:** `design-reference/DESIGN_MANIFEST.md`, `design-reference/D-001/DESIGN.md`

## DEC-009 — Playwright는 Chromium Smoke만 필수

- **Status:** Accepted
- **결정:** Playwright E2E 테스트는 Chromium 대상 Smoke Test 3개(`E2E-PUBLIC-SMOKE`, `E2E-TRAVEL-TOOLS`, `E2E-MATE-AUTH`)만 필수로 유지한다.
- **배경:** 다중 브라우저 매트릭스, 시각적 회귀, 부하 테스트는 이 프로젝트 규모 대비 유지 비용이 과도하다.
- **영향:** Firefox/WebKit 프로젝트 설정이나 별도 시각적 회귀 도구를 추가하지 않는다. 새 E2E 필요 시 기존 3개 스펙 중 하나로 흐름을 편입하는 것을 우선 검토한다.
- **관련 문서:** `docs/PROJECT_SCOPE.md`, `docs/ARCHITECTURE.md` §12, `TASKS/TASK-E2E-*.md`

## DEC-010 — 사용자의 개발 실행 단위는 Wave

- **Status:** Accepted
- **결정:** 사람이 구현 작업을 승인·실행하는 단위를 **Wave**라고 부른다. Wave는 `TASKS/00_TASK_LIST.md`에서 서로 의존관계가 없거나 이미 완료된 Task에 의존하는 Task들의 묶음이며, 사용자가 한 번에 "이 Wave를 진행하라"고 지시하면 그 안의 Task들이 실행된다.
- **배경:** 59개 Task를 한 번에 지시하는 대신, Depends On 그래프(`TASK_MANIFEST.csv`)를 기준으로 실행 가능한 묶음 단위로 나누면 중간 검토·승인이 쉬워진다.
- **영향:** Wave 경계와 포함 Task 목록은 이 문서가 아니라 실행 시점에 `TASKS/00_TASK_LIST.md`의 Depends On을 기준으로 정한다. Wave ID·구성을 별도로 고정 문서화하지 않는 한, Wave는 실행 단위 개념으로만 존재한다.
- **관련 문서:** `TASKS/00_TASK_LIST.md`, `TASKS/TASK_MANIFEST.csv`

## DEC-011 — Single Agent가 Wave 내부 Task를 순차 수행

- **Status:** Accepted
- **결정:** 하나의 Wave 안에 있는 Task들은 여러 Agent에게 병렬로 나누지 않고, **단일 Agent가 Depends On 순서에 따라 순차적으로** 수행한다.
- **배경:** Task 수(59개)와 상호 의존관계(Page Owner → Component/Data/API → DB/Setup) 규모에서 다중 Agent 병렬화는 조율 비용이 이득보다 크고, 코드 일관성(같은 컴포넌트 규칙, 같은 명명 규칙)을 지키기 어렵게 만든다.
- **영향:** Wave 실행 지시 시 별도로 "병렬로 처리해줘"라고 요청하지 않는 한, 기본값은 순차 처리다.
- **관련 문서:** `TASKS/00_TASK_LIST.md`(Depends On 열)

## DEC-012 — PR·Merge는 사용자가 수동 수행

- **Status:** Accepted
- **결정:** Pull Request 생성 이후의 검토와 Merge는 Agent가 아니라 **사용자가 직접** 수행한다.
- **배경:** DEC-015(자동 Merge 미사용)와 같은 맥락으로, 코드 변경이 실제 브랜치에 반영되는 시점은 사람의 판단을 거쳐야 한다.
- **영향:** Agent는 Wave 실행 결과를 커밋/브랜치로 준비할 수는 있지만, PR을 최종 승인·Merge하는 행위는 하지 않는다.
- **관련 문서:** `docs/ARCHITECTURE.md` §15

## DEC-013 — EC2·AWS는 사용하지 않음

- **Status:** Accepted
- **결정:** 컴퓨팅·스토리지·데이터베이스 어떤 용도로도 AWS(EC2, S3, RDS, Lambda 등)를 사용하지 않는다.
- **배경:** 호스팅(Vercel)과 데이터베이스/인증(Supabase)만으로 이번 범위의 요구사항을 충족할 수 있어, 별도 클라우드 인프라 운영 비용·복잡도를 지지 않는다.
- **영향:** IaC(Terraform 등), AWS SDK, VPC/보안그룹 설정을 이 프로젝트에 추가하지 않는다.
- **관련 문서:** `docs/PROJECT_SCOPE.md`, `docs/ARCHITECTURE.md` §14

## DEC-014 — 제외 기능은 EXCLUDED로 관리

- **Status:** Accepted
- **결정:** 범위에서 제외한 모든 Requirement는 삭제하지 않고 **EXCLUDED** 상태로 추적표에 남긴다. 새 문서가 만들어지더라도 EXCLUDED 항목은 그 문서에서도 그대로 EXCLUDED로 옮겨 적는다.
- **배경:** 요구사항을 삭제하면 왜 안 만들었는지 근거가 사라지고, 나중에 같은 논의를 반복하게 된다. EXCLUDED로 남기면 재검토 시점과 근거를 바로 확인할 수 있다.
- **영향:** `docs/UIUX_TRACEABILITY.md`와 `TASKS/00_TASK_LIST.md`의 `NON_IMPLEMENTATION` 표가 이 원칙의 실제 구현체다. 어떤 문서를 새로 써도 EXCLUDED Requirement 목록(114개 중 25개)은 그대로 유지한다.
- **관련 문서:** `docs/PROJECT_SCOPE.md`, `docs/UIUX_TRACEABILITY.md`, `TASKS/00_TASK_LIST.md`(§NON_IMPLEMENTATION)

---

## 요약표

| ID | 결정 | 상태 |
|---|---|---|
| DEC-001 | 실제 개발 루트는 `traveler/app` | Accepted |
| DEC-002 | 디자인 Screen은 핵심 4개·보조 1개 | Accepted |
| DEC-003 | `/travel-tools`에 항공·숙소·동행 작성을 통합 | Accepted |
| DEC-004 | 여행지·안전·대표는 정적 TypeScript Data | Accepted |
| DEC-005 | Supabase는 Auth와 동행 기능 중심 | Accepted |
| DEC-006 | DB는 6개 Table로 제한 | Accepted |
| DEC-007 | 항공·숙소 입력은 Browser Memory에만 유지 | Accepted |
| DEC-008 | Airbnb DESIGN.md는 vendor 참고본, D-001이 실제 정본 | Accepted |
| DEC-009 | Playwright는 Chromium Smoke만 필수 | Accepted |
| DEC-010 | 사용자의 개발 실행 단위는 Wave | Accepted |
| DEC-011 | Single Agent가 Wave 내부 Task를 순차 수행 | Accepted |
| DEC-012 | PR·Merge는 사용자가 수동 수행 | Accepted |
| DEC-013 | EC2·AWS는 사용하지 않음 | Accepted |
| DEC-014 | 제외 기능은 EXCLUDED로 관리 | Accepted |

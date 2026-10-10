# Free Traveler — Task List

**Document ID:** TASKLIST-001
**작성일:** 2026-09-15
**기반 문서:** `docs/06_SRS_UIUX_REVISED.md`, `docs/PROJECT_SCOPE.md`, `docs/UIUX_TRACEABILITY.md`, `design-reference/D-001/DESIGN.md`, `design-reference/UI_CONTRACT.md`, `design-reference/SCREEN_ROUTE_CONTRACT.json`, 실제 `src/app` 파일 트리

## 선행 검사 결과

`python scripts/validate_inputs.py` 실행 결과 **PASS**. (이 환경의 `python3`는 깨진 Windows Store 스텁으로 연결되어 있어 즉시 실패하므로, 대신 Anaconda `python` 인터프리터로 동일 스크립트를 실행해 통과를 확인했다 — 두 실행 모두 같은 스크립트, 같은 판정.)

- Screen 5개, Route/Page Entry 중복 없음, `SCR-001.starter_template_forbidden=true` 확인.
- `docs/UIUX_TRACEABILITY.md`: Requirement 114개(REQ-FUNC-001~080, REQ-NF-001~034) 전수 확인, IMPLEMENT 계열 89개 / EXCLUDED 25개.
- `src/app` 실제 파일: `layout.tsx`, `page.tsx`(Next.js 기본 스타터 상태), `globals.css`, `favicon.ico` — 그 외 라우트 파일은 전부 신규 생성 대상.

검사가 실패했다면 이 Task List를 작성하지 않았을 것이다. 검사를 통과했으므로 아래 내용을 작성한다.

## 요약

| 구분 | 값 |
|---|---:|
| 총 Task 수(본 목록) | 59 |
| Page Owner Task | 5 |
| Component Task | 20 |
| Data Task | 3 |
| DB Task | 4 |
| API Task | 5 |
| Shared(공통) Task | 10 |
| CI/Ops Task | 2 |
| Manual Check Task | 2 |
| Unit/RLS/E2E Test Task | 7 |
| Setup Task | 1 |
| IMPLEMENT 계열 Requirement(본 목록에서 다룸) | 89 / 89 |
| EXCLUDED Requirement(NON_IMPLEMENTATION 표) | 25 / 25 |
| Requirement 합계(삭제 0건) | 114 |

Category별 개수: SETUP 1 · DB 4 · DATA 3 · API 5 · SHARED 10 · COMPONENT 20(SCR-001 4, SCR-002 3, SCR-003 3, SCR-004 6, SCR-005 4) · PAGE_OWNER 5 · CI_OPS 2 · MANUAL_CHECK 2 · UNIT_TEST 3 · RLS_TEST 1 · E2E_TEST 3.

45~65개 예상 범위 안이며, 이는 완료 조건이 아니라 참고치다. 개수보다 §"커버리지 검증" 절의 114개 전수 일치가 완료 판단 기준이다.

---

## Task List

Implementation Status 표기: `IMPLEMENT` / `IMPLEMENT(축소)` / `IMPLEMENT(대체)`. Requirement Ref의 괄호는 `docs/PROJECT_SCOPE.md` 원 분류가 축소/대체인 개별 항목을 표시한 것이다(행 전체의 Implementation Status와 다를 수 있음).

### 0. Setup

| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | SETUP-DEPENDENCIES | 의존성 추가(Supabase, zod, Playwright) | SETUP | IMPLEMENT | NF-031 | N/A | N/A | N/A | 없음 | `package.json`(수정 — `@supabase/supabase-js`, `@supabase/ssr`, `zod`, `@playwright/test` 추가) |

**Functional AC:** `package.json`에 Supabase 클라이언트, 입력 검증(zod), Playwright(Chromium만)가 devDependencies/dependencies로 추가되고 `npm install`이 성공한다.
**Visual AC:** 해당 없음.
**Security/Privacy AC:** 추가되는 패키지 버전은 고정(caret 범위) 표기, 알려진 취약점이 있는 버전을 고정하지 않는다.
**Verify:** `npm install` 성공, `npm run build` 성공(코드 없이도 스캐폴드 빌드가 깨지지 않음).
**Priority:** P0

---

### 1. DB

| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files |
|---|---|---|---|---|---|---|---|---|---|---|
| 2 | DB-SCHEMA-BASE | 핵심 6개 테이블 스키마 정의 | DB | IMPLEMENT | REQ-FUNC-044(기반) | N/A | N/A | N/A | SETUP-DEPENDENCIES | `supabase/migrations/0001_core_schema.sql`(신규) |
| 3 | DB-RLS-BASE | Row Level Security 정책 | DB | IMPLEMENT | REQ-FUNC-044, REQ-NF-013 | N/A | N/A | N/A | DB-SCHEMA-BASE | `supabase/migrations/0002_rls_policies.sql`(신규) |
| 4 | DB-ACCESS | 타입 안전 DB 접근 계층 | DB | IMPLEMENT | REQ-NF-014, REQ-NF-015 | N/A | N/A | N/A | DB-SCHEMA-BASE | `src/lib/supabase/client.ts`(신규), `src/lib/supabase/server.ts`(신규), `src/lib/db/queries.ts`(신규) |
| 5 | DB-SEED-BASE | 로컬 개발용 시드 스크립트 | DB | IMPLEMENT | (없음 — 개발 편의) | N/A | N/A | N/A | DB-SCHEMA-BASE | `supabase/seed.sql`(신규) |

**DB-SCHEMA-BASE**
- Functional AC: 테이블은 정확히 6개로 제한 — `user_profile`, `mate_post`, `mate_application`, `user_block`, `report`, `admin_setting`. 여행지·안전정보·대표 프로필은 테이블을 만들지 않는다(정적 데이터 Task로 처리, §DATA 참고).
- Visual AC: 해당 없음.
- Security/Privacy AC: `user_profile`에 정확한 생년월일 컬럼을 두지 않는다(`is_adult boolean`, `adult_verified_at timestamptz`만).
- Verify: 마이그레이션 적용 후 `information_schema.tables`에서 테이블 6개 확인.
- Priority: P0

**DB-RLS-BASE**
- Functional AC: 본인 글/요청, 글 작성자, Moderator/Admin만 비공개 행을 읽도록 정책 작성. `admin_setting`은 Admin만 쓰기 가능.
- Visual AC: 해당 없음.
- Security/Privacy AC: 익명 사용자는 `mate_application`, `report`, `user_block`을 읽을 수 없다.
- Verify: TEST-RLS-BASIC 통과.
- Priority: P0

**DB-ACCESS**
- Functional AC: 모든 쓰기 경로(API Route)가 이 계층을 통해서만 DB에 접근한다. zod 스키마로 입력을 검증한 뒤 쿼리한다.
- Visual AC: 해당 없음.
- Security/Privacy AC: 입력값 이스케이프/검증(저장 XSS 방지), 쿠키는 `SameSite`/`HttpOnly` 기본값 사용, 서버 전용 키는 클라이언트 번들에 포함하지 않는다.
- Verify: 단위 테스트로 악성 입력(script 태그 등) 케이스 검증.
- Priority: P0

**DB-SEED-BASE**
- Functional AC: 테스트용 회원 2~3명, 모집글 3~4건을 시드한다.
- Visual AC: 해당 없음.
- Security/Privacy AC: 시드 데이터에 실제 개인정보를 사용하지 않는다.
- Verify: `psql`/Supabase Studio에서 시드 행 존재 확인.
- Priority: P2

---

### 2. Static Data

| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files |
|---|---|---|---|---|---|---|---|---|---|---|
| 6 | DATA-DESTINATIONS | 여행지 정적 데이터(국내10·해외15개국30도시) | DATA | IMPLEMENT | REQ-FUNC-004, 006, 007, 008 | N/A | N/A | N/A | 없음 | `src/data/destinations.ts`(신규), `src/data/destinations.schema.ts`(신규) |
| 7 | DATA-SAFETY | 국가 안전정보 정적 데이터(15개국) | DATA | IMPLEMENT | REQ-FUNC-046, 047, 048, 052, 053 | N/A | N/A | N/A | 없음 | `src/data/safety.ts`(신규), `src/data/safety.schema.ts`(신규) |
| 8 | DATA-REPRESENTATIVE | free_traveler 대표 프로필 정적 데이터 | DATA | IMPLEMENT | REQ-FUNC-057, 058, 059, 060, 061 | N/A | N/A | N/A | 없음 | `src/data/representative.ts`(신규) |

**DATA-DESTINATIONS**
- Functional AC: **구현 방법(지정): 정적 데이터(src/data), DB 테이블 아님.** 각 여행지는 소개(300자+)·명소 5개+·추천 시기·1일/3일 일정·예산·교통·음식 3개+·에티켓 3개+·출처·수정일·`country_code`를 갖는다. 국내 10곳, 해외 15개국 30개 도시 이상.
- Visual AC: 대표 이미지 1장 이상의 `alt`·`source`·`author`·`license` 필드가 스키마에 존재.
- Security/Privacy AC: 해당 없음(공개 콘텐츠).
- Verify: CI-DATA-VALIDATION 스크립트로 수량·필수필드 검증.
- Priority: P0

**DATA-SAFETY**
- Functional AC: **구현 방법(지정): 정적 데이터.** 8개 카테고리(치안·사기·법규·교통·재난·보건·문화·긴급연락처), `advisory_level`, `scope_type`/`scope_text`, `source_url`, `verified_at`을 갖는다. 소개된 모든 해외 국가 커버.
- Visual AC: 해당 없음(데이터 레이어).
- Security/Privacy AC: 해당 없음.
- Verify: CI-DATA-VALIDATION.
- Priority: P0

**DATA-REPRESENTATIVE**
- Functional AC: **구현 방법(지정): 정적 데이터.** `50+ Trips`/`30+ Countries` 라벨, 소개문, 철학, `visited_countries`(30개 이상, 권역 라벨 포함), `timeline`(6개 이상, 연도/장소/요약), `hero_media` alt/출처, 문의·SNS 링크(선택).
- Visual AC: 해당 없음(데이터 레이어, 렌더링은 §SCR-002 Component).
- Security/Privacy AC: 해당 없음.
- Verify: CI-DATA-VALIDATION.
- Priority: P0

---

### 3. API Route

| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files |
|---|---|---|---|---|---|---|---|---|---|---|
| 9 | API-AUTH | Supabase 이메일 인증·성인 확인 | API | IMPLEMENT | REQ-FUNC-027, 028, 066 | N/A | `/auth/callback`(기술 Route) | `src/app/auth/callback/route.ts`(신규) | SETUP-DEPENDENCIES, DB-SCHEMA-BASE, DB-RLS-BASE | `src/app/auth/callback/route.ts`(신규), `src/lib/auth/actions.ts`(신규) |
| 10 | API-MATES | 동행글 목록·상세·작성·수정·마감 | API | IMPLEMENT | REQ-FUNC-030, 033, 037, REQ-NF-005(축소) | N/A | N/A | `src/app/api/mates/route.ts` | DB-SCHEMA-BASE, DB-RLS-BASE, DB-ACCESS | `src/app/api/mates/route.ts`(신규), `src/app/api/mates/[id]/route.ts`(신규) |
| 11 | API-APPLICATIONS | 참가 요청 생성·승인·거절 | API | IMPLEMENT | REQ-FUNC-035, REQ-NF-005(축소) | N/A | N/A | `src/app/api/applications/route.ts` | DB-SCHEMA-BASE, DB-RLS-BASE, DB-ACCESS | `src/app/api/applications/route.ts`(신규), `src/app/api/applications/[id]/route.ts`(신규) |
| 12 | API-BLOCKS-REPORTS | 차단·신고 접수 | API | IMPLEMENT | REQ-FUNC-039(연계), 040, REQ-NF-019(축소) | N/A | N/A | `src/app/api/blocks/route.ts`, `src/app/api/reports/route.ts` | DB-SCHEMA-BASE, DB-RLS-BASE, DB-ACCESS | `src/app/api/blocks/route.ts`(신규), `src/app/api/reports/route.ts`(신규) |
| 13 | API-ADMIN | 신고 상태 변경·외부 URL 설정 | API | IMPLEMENT(축소) | REQ-FUNC-077 | N/A | N/A | `src/app/api/admin/reports/route.ts`, `src/app/api/admin/settings/route.ts` | DB-SCHEMA-BASE, DB-RLS-BASE, DB-ACCESS | `src/app/api/admin/reports/route.ts`(신규), `src/app/api/admin/settings/route.ts`(신규) |

**API-AUTH**
- Functional AC: 이메일 가입·로그인·로그아웃·비밀번호 재설정, 성인 확인 체크박스 동의 시 `is_adult`/`adult_verified_at`만 저장. 미인증 사용자의 쓰기 요청은 401/리다이렉트.
- Visual AC: 해당 없음(API).
- Security/Privacy AC: 정확한 생년월일 저장 안 함. 세션 쿠키 `HttpOnly`/`SameSite`.
- Verify: E2E-MATE-AUTH.
- Priority: P0

**API-MATES**
- Functional AC: 목록 응답에 연락처 필드 없음(REQ-FUNC-033). 조회 시점에 `end_date` 경과분을 CLOSED로 계산해 반환(배치 작업 없음, REQ-FUNC-037). 국가·지역·기간·상태 필터 지원.
- Visual AC: 해당 없음.
- Security/Privacy AC: RLS로 비공개 필드 차단.
- Verify: UNIT-MATE-STATE, E2E-MATE-AUTH.
- Priority: P0

**API-APPLICATIONS**
- Functional AC: 동일 사용자·동일 글 중복 PENDING/ACCEPTED 요청을 DB 유니크 제약+API 검증으로 차단. 작성자만 승인/거절 가능(403 아니면 거부).
- Visual AC: 해당 없음.
- Security/Privacy AC: 요청 메시지는 작성자·요청자만 조회.
- Verify: UNIT-MATE-STATE.
- Priority: P0

**API-BLOCKS-REPORTS**
- Functional AC: 신고 접수 시 접수 ID 즉시 반환. 차단 성립 시 상호 글/프로필/요청 비노출(쿼리 단에서 필터).
- Visual AC: 해당 없음.
- Security/Privacy AC: 신고자/피신고자 상세는 Moderator/Admin만 조회.
- Verify: E2E-MATE-AUTH.
- Priority: P0

**API-ADMIN**
- Functional AC: **범위(축소, PROJECT_SCOPE 근거): 신고 상태 변경(OPEN/RESOLVED/DISMISSED)과 외부 URL 설정만 처리 — 콘텐츠 CRUD·감사로그·통계는 만들지 않는다.** URL은 HTTPS만 허용, `javascript:`/HTTP 저장 차단.
- Visual AC: 해당 없음.
- Security/Privacy AC: Admin 역할만 접근(RLS+서버 검증 이중).
- Verify: E2E-MATE-AUTH(관리자 경로 일부).
- Priority: P0

---

### 4. Shared (5개 Screen 공통)

| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files |
|---|---|---|---|---|---|---|---|---|---|---|
| 14 | SHARED-HEADER-FOOTER | 공통 Header/Footer 레이아웃 | SHARED | IMPLEMENT | REQ-FUNC-064, 065 | 전역 | 전체(5개 Route 공통) | `src/app/layout.tsx` | SETUP-DEPENDENCIES | `src/app/layout.tsx`(수정 — 기존 기본 레이아웃 교체), `src/components/layout/Header.tsx`(신규), `src/components/layout/Footer.tsx`(신규) |
| 15 | SHARED-A11Y-FOCUS | 접근성 공통 규칙(포커스·ARIA) | SHARED | IMPLEMENT | REQ-FUNC-079, REQ-NF-023 | 전역 | 전체(5개 Route 공통) | `src/app/layout.tsx` | SHARED-HEADER-FOOTER | `src/app/globals.css`(수정 — focus-visible 규칙), `src/components/ui/` 공통 컴포넌트(신규) |
| 16 | SHARED-SEO-PERFORMANCE | 메타데이터·이미지 최적화 | SHARED | IMPLEMENT | REQ-FUNC-070, REQ-NF-006, REQ-NF-030 | 전역 | 전체(5개 Route 공통) | 각 `page.tsx` | SETUP-DEPENDENCIES | 각 Screen `page.tsx`의 `generateMetadata`(수정), `next.config.ts`(수정 — 이미지 도메인 허용) |
| 17 | SHARED-ERROR-PAGES | 404/500/오류 화면 | SHARED | IMPLEMENT | REQ-FUNC-078 | 전역 | 전체(5개 Route 공통) | `src/app/not-found.tsx`, `src/app/error.tsx` | SHARED-HEADER-FOOTER | `src/app/not-found.tsx`(신규), `src/app/error.tsx`(신규) |
| 18 | SHARED-FAVORITES-LOCALSTORAGE | 즐겨찾기(localStorage) 유틸 | SHARED | IMPLEMENT | REQ-FUNC-068 | 전역 | N/A | N/A | 없음 | `src/lib/favorites.ts`(신규) |
| 19 | SHARED-SHARE-LINK | URL 공유 유틸 | SHARED | IMPLEMENT | REQ-FUNC-069 | 전역 | N/A | N/A | 없음 | `src/lib/share.ts`(신규) |
| 20 | SHARED-NOTIFICATION-TOAST | 상태 변경 Toast 알림 | SHARED | IMPLEMENT | REQ-FUNC-043 | 전역 | N/A | N/A | 없음 | `src/components/ui/Toast.tsx`(신규) |
| 21 | SHARED-CONTACT-FILTER | 공개 연락처 패턴 탐지 유틸 | SHARED | IMPLEMENT | REQ-FUNC-032 | N/A | N/A | N/A | 없음 | `src/lib/contact-filter.ts`(신규) |
| 22 | SHARED-EXTERNAL-LINKOUT | 외부 이동(새 탭, 비전달) 유틸 | SHARED | IMPLEMENT | REQ-NF-017 | N/A | N/A | N/A | 없음 | `src/lib/external-linkout.ts`(신규) |
| 23 | SHARED-POLICY-CONSENT | 정책 페이지+안전수칙 동의 기록 | SHARED | IMPLEMENT | REQ-FUNC-080 | 전역 | `/terms`, `/privacy`, `/safety-guideline`(기술 Route, 정책 콘텐츠) | `src/app/terms/page.tsx` 등 | 없음 | `src/app/terms/page.tsx`(신규), `src/app/privacy/page.tsx`(신규), `src/app/safety-guideline/page.tsx`(신규), `src/lib/consent.ts`(신규) |

**SHARED-HEADER-FOOTER**
- Functional AC: 5개 Screen 모두 같은 Header/Footer 컴포넌트를 import. 핵심 4개+보조 1개 화면으로 2회 이내 이동 가능한 내비게이션.
- Visual AC: `design-reference/D-001/DESIGN.md` Header/Footer 토큰(Desktop 72px/Mobile 56px, hairline border, 코랄 액센트만 CTA) 그대로 적용.
- Security/Privacy AC: 해당 없음.
- Verify: E2E-PUBLIC-SMOKE.
- Priority: P0

**SHARED-A11Y-FOCUS**
- Functional AC: 폼·모달·탭·Toast에 올바른 ARIA role/상태.
- Visual AC: `:focus-visible` 2px 코랄 아웃라인 공통 적용, 터치 영역 44×44px 이상.
- Security/Privacy AC: 해당 없음.
- Verify: E2E-PUBLIC-SMOKE(키보드 포커스 기본 확인).
- Priority: P1

**SHARED-SEO-PERFORMANCE**
- Functional AC: 각 페이지 고유 title/description/canonical/OG. 이미지 `next/image` 사용, LCP 이미지 `priority`.
- Visual AC: 해당 없음.
- Security/Privacy AC: 해당 없음.
- Verify: 단위 테스트(메타데이터 존재), CI-DATA-VALIDATION.
- Priority: P2

**SHARED-ERROR-PAGES**
- Functional AC: 404/500 화면에 홈·이전·재시도 중 최소 1개 복구 행동.
- Visual AC: Empty/Error 상태 토큰(`D-001/DESIGN.md`) 사용, Lorem ipsum/준비 중 문구 금지.
- Security/Privacy AC: 스택 트레이스 등 민감 정보 노출 금지.
- Verify: E2E-PUBLIC-SMOKE.
- Priority: P2

**SHARED-FAVORITES-LOCALSTORAGE**
- Functional AC: **구현 방법(지정): localStorage.** 여행지 ID 배열 저장, 중복 추가 방지, 서버 동기화 없음.
- Visual AC: 해당 없음(유틸).
- Security/Privacy AC: 개인 식별 정보 저장하지 않음(여행지 ID만).
- Verify: 단위 테스트(중복 추가 방지).
- Priority: P1

**SHARED-SHARE-LINK**
- Functional AC: Web Share API 우선 시도, 실패 시 클립보드 복사 폴백.
- Visual AC: 해당 없음.
- Security/Privacy AC: 해당 없음.
- Verify: 단위 테스트.
- Priority: P2

**SHARED-NOTIFICATION-TOAST**
- Functional AC: **구현 방법(지정): 화면 상태 기반 Toast, 실제 이메일 발송 없음.** 참가 요청 접수/승인/거절/신고 접수 시 노출, 약 4초 자동 닫힘.
- Visual AC: `D-001/DESIGN.md` Toast 토큰(ink 배경, 하단 위치) 적용.
- Security/Privacy AC: 해당 없음.
- Verify: E2E-MATE-AUTH.
- Priority: P1

**SHARED-CONTACT-FILTER**
- Functional AC: 전화번호·이메일·메신저 ID 패턴 탐지 함수, 탐지 시 제출 차단 + 수정 안내 메시지 반환.
- Visual AC: 해당 없음(유틸, UI는 COMP-SCR003-MATE-COMPOSER).
- Security/Privacy AC: 해당 없음.
- Verify: UNIT-CONTACT-DETECTION.
- Priority: P0

**SHARED-EXTERNAL-LINKOUT**
- Functional AC: **입력값을 서버·DB·외부 URL에 전달하지 않는다(금지).** `window.open`으로 `noopener,noreferrer` 새 탭, 목적지·날짜 쿼리 파라미터 미부착. 허용목록 밖/미설정 URL은 이동 차단.
- Visual AC: 해당 없음.
- Security/Privacy AC: 클라이언트 상태로만 유지, 네트워크 요청 없음.
- Verify: E2E-TRAVEL-TOOLS(네트워크 탭 확인).
- Priority: P0

**SHARED-POLICY-CONSENT**
- Functional AC: 이용약관/개인정보처리방침/동행 안전수칙/콘텐츠 면책 페이지 제공, 동행글 작성 시 정책 버전+동의 시각 저장.
- Visual AC: 해당 없음(정적 텍스트 페이지).
- Security/Privacy AC: 동의 기록은 DB `mate_post`의 감사 필드가 아닌 최소 컬럼(정책 버전, 시각)만 저장.
- Verify: E2E-MATE-AUTH(동의 없이 제출 차단 확인).
- Priority: P1

---

### 5. SCR-001 `/` 메인

| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files |
|---|---|---|---|---|---|---|---|---|---|---|
| 24 | COMP-SCR001-SEARCH-DESTINATIONS | 검색 Hero+국내/해외 Grid+테마 Chip | COMPONENT | IMPLEMENT | REQ-FUNC-001,002,003,005,009,010,067, REQ-NF-004(축소) | SCR-001 | `/` | N/A | DATA-DESTINATIONS | `src/components/home/SearchHero.tsx`(신규), `src/components/home/DestinationGrid.tsx`(신규), `src/components/home/ThemeChips.tsx`(신규) |
| 25 | COMP-SCR001-SAFETY | 국가별 주의사항 Grid+Drawer | COMPONENT | IMPLEMENT | REQ-FUNC-006,049,050,051,054, REQ-NF-028(축소) | SCR-001 | `/` | N/A | DATA-SAFETY | `src/components/home/SafetyGrid.tsx`(신규), `src/components/home/SafetyDrawer.tsx`(신규) |
| 26 | COMP-SCR001-DESTINATION-DRAWER | 여행지 상세 Drawer | COMPONENT | IMPLEMENT | REQ-FUNC-004 | SCR-001 | `/` | N/A | DATA-DESTINATIONS, SHARED-SHARE-LINK, SHARED-FAVORITES-LOCALSTORAGE | `src/components/home/DestinationDrawer.tsx`(신규) |
| 27 | COMP-SCR001-MATES-PROFILE-TEASER | 최근 동행글+free_traveler 요약 | COMPONENT | IMPLEMENT | (표시 전용 — API-MATES/DATA-REPRESENTATIVE 재사용) | SCR-001 | `/` | N/A | API-MATES, DATA-REPRESENTATIVE | `src/components/home/RecentMates.tsx`(신규), `src/components/home/ProfileSummary.tsx`(신규) |
| 28 | PAGE-SCR001 | SCR-001 메인 Page Owner | PAGE_OWNER | IMPLEMENT | REQ-FUNC-001~010, 046~054, 064~070(공통, 조립) | SCR-001 | `/` | `src/app/page.tsx` | COMP-SCR001-SEARCH-DESTINATIONS, COMP-SCR001-SAFETY, COMP-SCR001-DESTINATION-DRAWER, COMP-SCR001-MATES-PROFILE-TEASER, SHARED-HEADER-FOOTER, DATA-DESTINATIONS, DATA-SAFETY | `src/app/page.tsx`(**수정** — 기존 Next.js 스타터 콘텐츠 전면 교체, 신규 생성 아님) |

**COMP-SCR001-SEARCH-DESTINATIONS**
- Functional AC: 국내/해외 탭 구분(오분류 0건), 국가·도시·계절·테마·기간 AND 필터, 키워드 부분 일치 검색, 필터 결과 0건 시 조건 완화 안내+초기화 버튼, 허용 필터만 URL query 반영.
- Visual AC: Card 3열×2행(Desktop)/1열(Mobile), Hero는 480~560px로 제한해 1440px에서 다음 Section 제목이 보임.
- Security/Privacy AC: 해당 없음.
- Verify: 단위 테스트(필터 조합), E2E-PUBLIC-SMOKE.
- Priority: P0

**COMP-SCR001-SAFETY**
- Functional AC: 8개 카테고리 표시, 외교부 링크 새 탭, `verified_at` 7일 초과 시 stale 경고를 **렌더링 시점 계산**(배치 없음), 중대 경보 텍스트 라벨 상단 노출.
- Visual AC: 경보 단계는 코랄이 아닌 semantic 색상(`caution`/`warning`/`danger`)+텍스트 라벨.
- Security/Privacy AC: 해당 없음.
- Verify: 단위 테스트(날짜 경계값), E2E-PUBLIC-SMOKE.
- Priority: P0

**COMP-SCR001-DESTINATION-DRAWER**
- Functional AC: 같은 화면에서 오픈(페이지 이동 없음), 소개·명소 5개+·일정·예산·교통·음식·에티켓·출처 전부 표시, 해외는 안전정보 Drawer로 전환 링크.
- Visual AC: `rounded.lg`, 우측 패널(Desktop)/하단 시트(Mobile), 1단계 그림자.
- Security/Privacy AC: 해당 없음.
- Verify: E2E-PUBLIC-SMOKE.
- Priority: P1

**COMP-SCR001-MATES-PROFILE-TEASER**
- Functional AC: 최근 모집중 글 3개 또는 완성형 Empty State(설명 문장+이용 방법+작성 CTA), free_traveler `50+`/`30+` 수치는 `DATA-REPRESENTATIVE`와 100% 일치.
- Visual AC: 큰 빈 영역·Placeholder 문구 금지, Empty State에도 시각적으로 완성된 카드 형태 유지.
- Security/Privacy AC: 동행글 카드에 연락처 미노출(API-MATES 응답 신뢰).
- Verify: E2E-PUBLIC-SMOKE.
- Priority: P1

**PAGE-SCR001**
- Functional AC(Section 순서, 최소 콘텐츠 수 — `UI_CONTRACT.md`/계약 그대로): Header → ①검색 Hero → ②국내 여행지 **6개** → ③해외 여행지 **6개** → ④여행 동기 **6개** Chip → ⑤국가별 주의사항 **6개** → ⑥최근 동행글 **3개** 또는 완성형 Empty State → ⑦free_traveler 소개 → Footer. 각 Section 데이터 출처: ②③은 `DATA-DESTINATIONS`, ⑤는 `DATA-SAFETY`, ⑥은 `API-MATES`, ⑦은 `DATA-REPRESENTATIVE`.
- Functional AC(스타터 제거): `src/app/page.tsx`에 create-next-app 기본 템플릿(Next.js 로고, "Get started by editing" 문구, 기본 카드 링크)이 **하나도 남아있지 않아야 한다** — Page Owner 완료 조건.
- Functional AC(의존): 위 4개 Component Task가 모두 완료되어야 조립을 시작한다(임의 Placeholder로 먼저 조립하지 않는다).
- Functional AC(상태 — `UI_CONTRACT.md` SCR-001 §상태): Loading(Card Grid 스켈레톤), Empty(필터 결과 0건 → 조건 완화 안내+초기화 버튼; 최근 동행글 0건 → 완성형 Empty State), Error(Section별 로드 실패 배너+다시 시도)를 실제로 조립한다.
- Visual AC: Desktop 콘텐츠 최대 폭 1200~1280px, Section 상하 여백 64~96px(Mobile 40~64px), Card 1열(Mobile)/3~4열(Desktop) 반응형 밀도 준수.
- Security/Privacy AC: 없음(조립 계층).
- Verify: E2E-PUBLIC-SMOKE, 수동 브라우저 확인(§Release Check).
- Priority: P0

---

### 6. SCR-002 `/about` 대표 소개

| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files |
|---|---|---|---|---|---|---|---|---|---|---|
| 29 | COMP-SCR002-PROFILE-HERO | Hero+여행 지표+소개·철학+문의링크 | COMPONENT | IMPLEMENT | REQ-FUNC-057,058,062 | SCR-002 | `/about` | N/A | DATA-REPRESENTATIVE | `src/components/about/ProfileHero.tsx`(신규), `src/components/about/Stats.tsx`(신규), `src/components/about/Philosophy.tsx`(신규) |
| 30 | COMP-SCR002-TIMELINE-COUNTRIES | 여행 Timeline+방문 국가 | COMPONENT | IMPLEMENT | REQ-FUNC-059,060 | SCR-002 | `/about` | N/A | DATA-REPRESENTATIVE | `src/components/about/Timeline.tsx`(신규), `src/components/about/VisitedCountries.tsx`(신규) |
| 31 | COMP-SCR002-GALLERY-RECOMMENDED | Gallery+추천 여행지+CTA | COMPONENT | IMPLEMENT | REQ-FUNC-061,063 | SCR-002 | `/about` | N/A | DATA-REPRESENTATIVE | `src/components/about/Gallery.tsx`(신규), `src/components/about/RecommendedDestinations.tsx`(신규) |
| 32 | PAGE-SCR002 | SCR-002 대표 소개 Page Owner | PAGE_OWNER | IMPLEMENT | REQ-FUNC-057~063(조립) | SCR-002 | `/about` | `src/app/about/page.tsx` | COMP-SCR002-PROFILE-HERO, COMP-SCR002-TIMELINE-COUNTRIES, COMP-SCR002-GALLERY-RECOMMENDED, SHARED-HEADER-FOOTER, DATA-REPRESENTATIVE | `src/app/about/page.tsx`(신규) |

**COMP-SCR002-PROFILE-HERO**
- Functional AC: 대표명·`50+ Trips`·`30+ Countries`가 홈(`ProfileSummary`)과 완전히 동일한 데이터 소스(`DATA-REPRESENTATIVE`) 참조. 소개문 2~4문단.
- Visual AC: Hero는 뷰포트를 채우지 않음(다음 Section 제목이 1440px에서 보임).
- Security/Privacy AC: 해당 없음.
- Verify: 단위 테스트(값 일치).
- Priority: P1

**COMP-SCR002-TIMELINE-COUNTRIES**
- Functional AC: Timeline **6개 이상** 시점(연도·장소·요약), 방문 국가 **30개**를 권역별(아시아/유럽/북미/오세아니아 등) Chip으로 그룹.
- Visual AC: 세로형 Timeline, 권역별 Chip 목록 — 같은 카드 패턴 반복 금지(교차 배치).
- Security/Privacy AC: 해당 없음.
- Verify: 데이터 수량 검증 테스트(CI-DATA-VALIDATION).
- Priority: P1

**COMP-SCR002-GALLERY-RECOMMENDED**
- Functional AC: Gallery **8장 이상**(서로 다른 장소, 실제 alt 텍스트), 기억에 남는 여행지 **4개**+CTA(`/travel-tools`, `/mates`).
- Visual AC: 4열(Desktop)/1열(Mobile) 반응형 Photo Grid.
- Security/Privacy AC: 해당 없음.
- Verify: 데이터 수량 검증 테스트.
- Priority: P1

**PAGE-SCR002**
- Functional AC(Section 순서·최소 수): Header → ①Profile Hero → ②여행 지표 → ③소개·철학 → ④Timeline **6개+** → ⑤방문 국가 **30개** → ⑥Gallery **8장+** → ⑦기억에 남는 여행지 **4개**+CTA → Footer. 전 Section 데이터 출처는 `DATA-REPRESENTATIVE` 단일 소스.
- Functional AC(상태 — `UI_CONTRACT.md` SCR-002 §상태): Loading(사진·Timeline 스켈레톤), Error(이미지 로드 실패 시 alt 텍스트 노출 대체 박스)를 실제로 조립한다(정적 콘텐츠이므로 Empty/Unauthorized 해당 없음).
- Visual AC: Desktop 최대 폭 1200~1280px, Section 여백 64~96px(Mobile 40~64px). Hero/통계/좌우분할/Timeline/Chip목록/Gallery/CTA Banner를 교차 배치해 동일 패턴 반복 금지.
- Security/Privacy AC: 없음.
- Verify: E2E-PUBLIC-SMOKE, 수동 브라우저 확인.
- Priority: P1

---

### 7. SCR-003 `/travel-tools` 통합 여행 준비

| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files |
|---|---|---|---|---|---|---|---|---|---|---|
| 33 | COMP-SCR003-FLIGHT-FORM | 항공편 입력·검증·요약·외부이동 | COMPONENT | IMPLEMENT | REQ-FUNC-011~018(UNIT-TRAVEL-DATES 연계), REQ-NF-004(축소) | SCR-003 | `/travel-tools` | N/A | SHARED-EXTERNAL-LINKOUT | `src/components/travel-tools/FlightForm.tsx`(신규), `src/components/travel-tools/FlightSummary.tsx`(신규) |
| 34 | COMP-SCR003-HOTEL-FORM | 숙소 입력·검증·요약·외부이동 | COMPONENT | IMPLEMENT | REQ-FUNC-019~026, REQ-NF-017 | SCR-003 | `/travel-tools` | N/A | SHARED-EXTERNAL-LINKOUT | `src/components/travel-tools/HotelForm.tsx`(신규), `src/components/travel-tools/HotelSummary.tsx`(신규) |
| 35 | COMP-SCR003-MATE-COMPOSER | 동행 작성 Form/로그인 유도/안전 안내 | COMPONENT | IMPLEMENT | REQ-FUNC-031, 032, 080 | SCR-003 | `/travel-tools` | N/A | SHARED-CONTACT-FILTER, SHARED-POLICY-CONSENT, API-AUTH, API-MATES | `src/components/travel-tools/MateComposer.tsx`(신규), `src/components/travel-tools/GuestBanner.tsx`(신규) |
| 36 | PAGE-SCR003 | SCR-003 통합 여행 준비 Page Owner | PAGE_OWNER | IMPLEMENT | REQ-FUNC-011~026, 031, 032, 080(조립) | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | COMP-SCR003-FLIGHT-FORM, COMP-SCR003-HOTEL-FORM, COMP-SCR003-MATE-COMPOSER, SHARED-HEADER-FOOTER, API-AUTH | `src/app/travel-tools/page.tsx`(신규) |

**COMP-SCR003-FLIGHT-FORM**
- Functional AC: 국가·지역·출발일·귀국일 필수, 과거/역전 날짜 차단(UNIT-TRAVEL-DATES), 요약 후 `noopener,noreferrer` 새 탭. **입력값을 서버·DB·URL에 전달하지 않는다.**
- Visual AC: `text-input` 48px, 오류는 필드 하단 danger 색상.
- Security/Privacy AC: 네트워크 요청 없음(클라이언트 상태만).
- Verify: UNIT-TRAVEL-DATES, E2E-TRAVEL-TOOLS.
- Priority: P0

**COMP-SCR003-HOTEL-FORM**
- Functional AC: 국가·지역·체크인·체크아웃 필수, 체크인≥체크아웃 차단(UNIT-TRAVEL-DATES), 비전달 고지 표시. **입력값을 서버·DB·URL에 전달하지 않는다.**
- Visual AC: FLIGHT-FORM과 동일 패턴(일관성), 요약 Action Card.
- Security/Privacy AC: 네트워크 요청 없음.
- Verify: UNIT-TRAVEL-DATES, E2E-TRAVEL-TOOLS.
- Priority: P0

**COMP-SCR003-MATE-COMPOSER**
- Functional AC: 비로그인/미성년 → 로그인 유도 배너(CTA `/account`). 로그인+성인확인 완료 → 작성 Form, 연락처 패턴 탐지(SHARED-CONTACT-FILTER) 시 제출 차단, 안전수칙 동의 체크 필수.
- Visual AC: 탭 전환 시 다른 탭 입력 상태를 지우지 않음(독립 상태).
- Security/Privacy AC: 연락처 미노출, 동의 시각 저장.
- Verify: UNIT-CONTACT-DETECTION, E2E-MATE-AUTH.
- Priority: P0

**PAGE-SCR003**
- Functional AC(Section 순서): Header → ①Intro(목적+3단계 요약) → ②탭(항공편/숙소/동행 구하기, **실제 조립·전환 동작**) → ③여행정보 Form(탭별) → ④입력 요약·외부 이동 → ⑤찾기 Tip 3개+비전달 고지 → ⑥동행 작성 또는 로그인 안내·안전 안내 → Footer. 세 탭은 각자 독립된 입력/검증/완료 상태를 가진다(탭 전환이 다른 탭 데이터를 지우지 않음).
- Functional AC(상태 — `UI_CONTRACT.md` SCR-003 §상태, 탭별 독립): 항공편/숙소 탭은 Loading(외부 이동 처리 중)·Success·Error(날짜 검증 오류, 외부 URL 미설정 오류)를 조립한다. 동행 구하기 탭은 Loading(제출 처리 중)·Success·Error(연락처 패턴 감지·필수값 오류)·Unauthorized(비로그인/미성년 → 로그인 유도 배너)를 조립한다.
- Visual AC: Desktop 최대 폭 1200~1280px, Mobile은 탭을 풀폭 세그먼트로.
- Security/Privacy AC: 항공·숙소 입력값이 어떤 경로로도 서버/DB/외부 URL에 전달되지 않음(SHARED-EXTERNAL-LINKOUT 재사용으로 이중 보장).
- Verify: E2E-TRAVEL-TOOLS.
- Priority: P0

---

### 8. SCR-004 `/mates` 동행 조회

| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files |
|---|---|---|---|---|---|---|---|---|---|---|
| 37 | COMP-SCR004-FILTER | 검색 Filter+결과 요약 | COMPONENT | IMPLEMENT | REQ-FUNC-030, REQ-NF-004(축소) | SCR-004 | `/mates` | N/A | API-MATES | `src/components/mates/FilterBar.tsx`(신규) |
| 38 | COMP-SCR004-LIST | 동행글 목록(최대 8, Empty State) | COMPONENT | IMPLEMENT | REQ-FUNC-033, 037 | SCR-004 | `/mates` | N/A | API-MATES, COMP-SCR004-FILTER | `src/components/mates/MateList.tsx`(신규), `src/components/mates/MateListEmptyState.tsx`(신규) |
| 39 | COMP-SCR004-DETAIL | 상세 패널(Desktop 분할/Mobile Drawer) | COMPONENT | IMPLEMENT | REQ-FUNC-033 | SCR-004 | `/mates` | N/A | API-MATES | `src/components/mates/MateDetailPanel.tsx`(신규) |
| 40 | COMP-SCR004-APPLY | 참가 요청 Form+신청 방법 3단계 | COMPONENT | IMPLEMENT | REQ-FUNC-034, 035, 036 | SCR-004 | `/mates` | N/A | API-APPLICATIONS, API-AUTH | `src/components/mates/ApplyForm.tsx`(신규), `src/components/mates/ApplyGuide.tsx`(신규) |
| 41 | COMP-SCR004-REPORT | 신고 Modal | COMPONENT | IMPLEMENT | REQ-FUNC-039, REQ-NF-019(축소) | SCR-004 | `/mates` | N/A | API-BLOCKS-REPORTS | `src/components/mates/ReportModal.tsx`(신규) |
| 42 | COMP-SCR004-BLOCK | 차단 Modal+안전 안내 CTA | COMPONENT | IMPLEMENT | REQ-FUNC-040 | SCR-004 | `/mates` | N/A | API-BLOCKS-REPORTS | `src/components/mates/BlockModal.tsx`(신규), `src/components/mates/SafetyBanner.tsx`(신규) |
| 43 | PAGE-SCR004 | SCR-004 동행 조회 Page Owner | PAGE_OWNER | IMPLEMENT | REQ-FUNC-030, 033~040(조립) | SCR-004 | `/mates` | `src/app/mates/page.tsx` | COMP-SCR004-FILTER, COMP-SCR004-LIST, COMP-SCR004-DETAIL, COMP-SCR004-APPLY, COMP-SCR004-REPORT, COMP-SCR004-BLOCK, SHARED-HEADER-FOOTER, SHARED-NOTIFICATION-TOAST | `src/app/mates/page.tsx`(신규) |

**COMP-SCR004-FILTER**
- Functional AC: 국가·지역·기간·모집 상태 필터, "조건에 맞는 동행글 N개" 요약 문장.
- Visual AC: 필터 초기화 아이콘 버튼 44px+.
- Security/Privacy AC: 해당 없음.
- Verify: 단위 테스트(필터 조합).
- Priority: P0

**COMP-SCR004-LIST**
- Functional AC: 데이터 있으면 최대 **8개** 카드, 없으면 **완성형 Empty State**(안내 문장+필터 초기화+작성 CTA+이용 방법) — Lorem ipsum/준비 중/빈 Card 금지. 연락처 미노출.
- Visual AC: 상태 배지는 텍스트 라벨 동반(코랄=모집중, 회색=마감).
- Security/Privacy AC: API-MATES 응답 신뢰(연락처 없음).
- Verify: E2E-MATE-AUTH.
- Priority: P0

**COMP-SCR004-DETAIL**
- Functional AC: Desktop 목록 40%(`lg:col-span-5`)+상세 60%(`lg:col-span-7`) 분할, Mobile은 Card 선택 시 하단 Drawer.
- Visual AC: `rounded.lg`, 1단계 그림자.
- Security/Privacy AC: 비공개 필드는 RLS로 서버단 차단.
- Verify: E2E-MATE-AUTH.
- Priority: P0

**COMP-SCR004-APPLY**
- Functional AC: 500자 이하 비공개 메시지, 중복 PENDING/ACCEPTED 요청 차단, 비로그인/미성년 시도 시 로그인 유도. 신청 방법 3단계 안내 텍스트.
- Visual AC: 폼 오류는 danger 색상 인라인.
- Security/Privacy AC: 메시지는 작성자·요청자만 조회.
- Verify: UNIT-MATE-STATE, E2E-MATE-AUTH.
- Priority: P0

**COMP-SCR004-REPORT**
- Functional AC: 신고 접수 3초 이내 접수 ID 표시(Toast).
- Visual AC: Modal 스크림 50%, `Esc`/스크림 클릭으로 닫힘.
- Security/Privacy AC: 신고 사유·설명은 Moderator/Admin만 조회.
- Verify: E2E-MATE-AUTH.
- Priority: P1

**COMP-SCR004-BLOCK**
- Functional AC: 차단 성립 후 상호 글/프로필/요청 비노출, 안전 안내+`/travel-tools` CTA.
- Visual AC: Modal 패턴 REPORT와 동일.
- Security/Privacy AC: 해당 없음.
- Verify: E2E-MATE-AUTH.
- Priority: P1

**PAGE-SCR004**
- Functional AC(Section 순서·데이터 출처): Header → ①Intro+작성 CTA → ②Filter+결과 요약(`API-MATES`) → ③동행글 목록(`API-MATES`, 최대 8) → ④목록+상세 분할(Desktop)/Drawer(Mobile) → ⑤신청 방법 3단계 → ⑥안전·신고·차단 안내+CTA → Footer.
- Functional AC(상태 — `UI_CONTRACT.md` SCR-004 §상태): Loading(목록/상세 스켈레톤), Empty(조건에 맞는 글 없음 → 완성형 Empty State), Error(신청 실패·중복 요청·네트워크 오류), Unauthorized(신청/작성 시도 시 로그인·성인 확인 유도)를 실제로 조립한다.
- Visual AC: Desktop 최대 폭 1200~1280px, 목록·필터·상세·참가·신고·차단이 각각 별도 컴포넌트로 명확히 분리되어 있음(§Component 참고).
- Security/Privacy AC: 연락처 비노출·차단 관계 비노출이 조립 이후에도 유지되는지 재확인.
- Verify: E2E-MATE-AUTH.
- Priority: P0

---

### 9. SCR-005 `/account` 계정·관리

| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files |
|---|---|---|---|---|---|---|---|---|---|---|
| 44 | COMP-SCR005-AUTH | Guest 인증 영역 | COMPONENT | IMPLEMENT | REQ-FUNC-027(게이트 UI) | SCR-005 | `/account` | N/A | API-AUTH | `src/components/account/AuthPanel.tsx`(신규) |
| 45 | COMP-SCR005-PROFILE | Member 프로필 요약·수정 | COMPONENT | IMPLEMENT | REQ-FUNC-029 | SCR-005 | `/account` | N/A | API-AUTH, DB-ACCESS | `src/components/account/ProfilePanel.tsx`(신규) |
| 46 | COMP-SCR005-MY-ACTIVITY | 내 활동(내 글·요청·즐겨찾기·차단) | COMPONENT | IMPLEMENT | REQ-FUNC-036, 038 | SCR-005 | `/account` | N/A | API-MATES, API-APPLICATIONS, API-BLOCKS-REPORTS, SHARED-FAVORITES-LOCALSTORAGE | `src/components/account/MyActivity.tsx`(신규) |
| 47 | COMP-SCR005-ADMIN | 관리자(신고 상태·외부 URL) | COMPONENT | IMPLEMENT(축소) | REQ-FUNC-041, 042, 077 | SCR-005 | `/account` | N/A | API-ADMIN, API-BLOCKS-REPORTS | `src/components/account/AdminPanel.tsx`(신규) |
| 48 | PAGE-SCR005 | SCR-005 계정·관리 Page Owner | PAGE_OWNER | IMPLEMENT | REQ-FUNC-027~029, 036, 038, 041, 042, 077(조립) | SCR-005 | `/account` | `src/app/account/page.tsx` | COMP-SCR005-AUTH, COMP-SCR005-PROFILE, COMP-SCR005-MY-ACTIVITY, COMP-SCR005-ADMIN, SHARED-HEADER-FOOTER, API-AUTH | `src/app/account/page.tsx`(신규) |

**COMP-SCR005-AUTH**
- Functional AC: 로그인/가입/비밀번호 재설정 Card, 로그인 후 가능한 기능 안내, 보안 안내(성인 확인·최소 개인정보 수집).
- Visual AC: 탭 없이 단일 뷰.
- Security/Privacy AC: 이메일 외 개인정보 요구하지 않음.
- Verify: E2E-MATE-AUTH.
- Priority: P0

**COMP-SCR005-PROFILE**
- Functional AC: 닉네임·연령대·성별(선택)·여행 스타일·성인 확인 상태 표시·수정.
- Visual AC: Form 패턴 `D-001/DESIGN.md` `text-input` 재사용.
- Security/Privacy AC: 생년월일 미수집.
- Verify: E2E-MATE-AUTH.
- Priority: P1

**COMP-SCR005-MY-ACTIVITY**
- Functional AC: "새 동행글 작성" CTA(`/travel-tools`), 내가 쓴 글(수정/마감), 받은 참가 요청(승인/거절), 즐겨찾기(localStorage 기반, → SCR-001 딥링크), 차단 목록(해제). 4블록 모두 데이터 없을 때 **완성형 Empty State**(설명+이용 방법+CTA).
- Visual AC: 2×2 그리드(Desktop)/세로 스택(Mobile), 큰 빈 영역 금지.
- Security/Privacy AC: 본인 데이터만 조회(RLS).
- Verify: E2E-MATE-AUTH.
- Priority: P0

**COMP-SCR005-ADMIN**
- Functional AC: **범위(축소, PROJECT_SCOPE 근거): 신고 목록+상태 변경, 외부 URL(HTTPS만) 설정만. 차트·KPI·Dashboard 금지.**
- Visual AC: 목록+Select+저장 버튼 형태, 통계 위젯 없음.
- Security/Privacy AC: Admin 역할만 렌더링(역할 없으면 탭 자체 미노출).
- Verify: E2E-MATE-AUTH(관리자 경로).
- Priority: P0

**PAGE-SCR005**
- Functional AC(역할별 Section, 데이터 출처): Guest → Intro/로그인·가입·재설정(`API-AUTH`)/기능 안내/보안 안내. Member → 탭[프로필(`API-AUTH`), 내 활동(`API-MATES`/`API-APPLICATIONS`/`API-BLOCKS-REPORTS`/localStorage)]. Admin → +탭[관리자(`API-ADMIN`)]. **역할에 없는 관리 영역은 렌더링하지 않는다**(DOM에 존재하지 않아야 함, CSS로 숨기기만 하는 방식 금지).
- Functional AC(상태 — `UI_CONTRACT.md` SCR-005 §상태, 역할별 독립): Guest는 Loading·Success·Error(로그인 실패·이메일 중복)를 조립한다. Member 프로필은 Loading·Success·Error(수정 실패)를 조립한다. Member 내 활동은 Loading·Success·Empty(블록별 완성형 Empty State+CTA)·Error(로드/처리 실패)·Unauthorized(비회원 직접 접근 → Guest 뷰로 대체)를 조립한다. Admin은 Loading·Success·Empty(처리할 신고 없음)·Error(상태 변경 실패, 잘못된 URL 저장 차단)·Unauthorized(권한 없음 → 관리자 탭 미노출)를 조립한다.
- Visual AC: 큰 빈 영역·Placeholder 문구 금지, 4블록 각각 완성형 Empty State.
- Security/Privacy AC: 비로그인 상태에서 Member/Admin 영역 접근 시 Guest 뷰로 대체(서버 검증 포함).
- Verify: E2E-MATE-AUTH.
- Priority: P0

---

### 10. CI / Ops

| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files |
|---|---|---|---|---|---|---|---|---|---|---|
| 49 | CI-LINT-BUILD-TEST | CI: lint·build·단위테스트 게이트 | CI_OPS | IMPLEMENT | REQ-NF-031 | N/A | N/A | N/A | SETUP-DEPENDENCIES | `.github/workflows/ci.yml`(신규) 또는 동등 CI 설정 |
| 50 | CI-DATA-VALIDATION | 정적 데이터 완전성 검증 스크립트 | CI_OPS | IMPLEMENT(대체) | REQ-FUNC-074, REQ-NF-026, REQ-NF-027, REQ-NF-028(축소) | N/A | N/A | N/A | DATA-DESTINATIONS, DATA-SAFETY, DATA-REPRESENTATIVE | `scripts/validate_content.py`(신규) |

**CI-LINT-BUILD-TEST**
- Functional AC: PR/병합 전 `next lint`, `next build`, 단위 테스트 실행, 실패 시 병합 차단.
- Visual AC: 해당 없음.
- Security/Privacy AC: 시크릿을 CI 로그에 출력하지 않음.
- Verify: 실제 PR에서 게이트 동작 확인(MANUAL-VERCEL-DEPLOY와 연계).
- Priority: P1

**CI-DATA-VALIDATION**
- Functional AC: **런타임 게시 게이트 대신 빌드/CI 단계 정적 데이터 검증으로 대체(PROJECT_SCOPE 근거).** 여행지 수량(국내10/해외15개국30도시), 안전정보 8카테고리, 대표 프로필 30국/6타임라인/8갤러리, 필수 필드 누락을 검사하고 실패 시 CI 실패.
- Visual AC: 해당 없음.
- Security/Privacy AC: 해당 없음.
- Verify: `python scripts/validate_content.py` 성공 종료.
- Priority: P1

---

### 11. Manual Check

| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files |
|---|---|---|---|---|---|---|---|---|---|---|
| 51 | MANUAL-VERCEL-DEPLOY | Vercel 배포·HTTPS·비용 확인 | MANUAL_CHECK | IMPLEMENT | REQ-NF-012, REQ-NF-034 | N/A | N/A | N/A | PAGE-SCR001, PAGE-SCR002, PAGE-SCR003, PAGE-SCR004, PAGE-SCR005, CI-LINT-BUILD-TEST | 없음(배포 콘솔 확인) |
| 52 | MANUAL-SUPABASE-CONFIG | Supabase 환경변수·연결 확인 | MANUAL_CHECK | IMPLEMENT | REQ-NF-016 | N/A | N/A | N/A | DB-SCHEMA-BASE, DB-RLS-BASE, API-AUTH | `.env.example`(신규) |

**MANUAL-VERCEL-DEPLOY**
- Functional AC: 배포 URL이 HTTPS로 서비스되는지, 무료/저비용 티어로 월 비용 목표(콘텐츠 인건비 제외 10만원 이하) 충족하는지 사람이 콘솔에서 확인.
- Visual AC: 해당 없음.
- Security/Privacy AC: 비밀키가 클라이언트 번들에 노출되지 않았는지 빌드 산출물 검색으로 확인.
- Verify: 사람이 Vercel 대시보드에서 확인 후 결과 기록.
- Priority: P0

**MANUAL-SUPABASE-CONFIG**
- Functional AC: `.env` 값이 실제 Supabase 프로젝트를 가리키는지, Auth/DB 연결이 되는지 사람이 확인.
- Visual AC: 해당 없음.
- Security/Privacy AC: `.env` 파일이 git에 커밋되지 않았는지 확인.
- Verify: 사람이 로컬/배포 환경에서 로그인 흐름 1회 수동 테스트.
- Priority: P0

---

### 12. Test (Unit / RLS / E2E)

| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files |
|---|---|---|---|---|---|---|---|---|---|---|
| 53 | UNIT-TRAVEL-DATES | 날짜 검증 단위 테스트 | UNIT_TEST | IMPLEMENT | REQ-FUNC-013, 021 | N/A | N/A | N/A | COMP-SCR003-FLIGHT-FORM, COMP-SCR003-HOTEL-FORM | `src/lib/__tests__/travel-dates.test.ts`(신규) |
| 54 | UNIT-CONTACT-DETECTION | 연락처 탐지 단위 테스트 | UNIT_TEST | IMPLEMENT | REQ-FUNC-032 | N/A | N/A | N/A | SHARED-CONTACT-FILTER | `src/lib/__tests__/contact-filter.test.ts`(신규) |
| 55 | UNIT-MATE-STATE | 동행글·요청 상태 전이 단위 테스트 | UNIT_TEST | IMPLEMENT | REQ-FUNC-035, 036, 037 | N/A | N/A | N/A | API-MATES, API-APPLICATIONS | `src/lib/__tests__/mate-state.test.ts`(신규) |
| 56 | TEST-RLS-BASIC | Supabase RLS 정책 테스트 | RLS_TEST | IMPLEMENT | REQ-FUNC-044, REQ-NF-013 | N/A | N/A | N/A | DB-RLS-BASE | `supabase/tests/rls_basic.sql`(신규) 또는 동등 테스트 |
| 57 | E2E-PUBLIC-SMOKE | 공개 화면 Smoke(홈·안전정보·대표소개·내비게이션) | E2E_TEST | IMPLEMENT | REQ-FUNC-001~010, 046~054, 057~065(경로 확인 수준) | 전역 | `/`, `/about` | `playwright.config.ts` | PAGE-SCR001, PAGE-SCR002 | `e2e/public-smoke.spec.ts`(신규) |
| 58 | E2E-TRAVEL-TOOLS | 항공·숙소 흐름 Smoke | E2E_TEST | IMPLEMENT | REQ-FUNC-011~026 | SCR-003 | `/travel-tools` | `playwright.config.ts` | PAGE-SCR003 | `e2e/travel-tools.spec.ts`(신규) |
| 59 | E2E-MATE-AUTH | 동행·인증·관리자 흐름 Smoke | E2E_TEST | IMPLEMENT | REQ-FUNC-027~044(경로 확인 수준 — 045는 NON_IMPLEMENTATION 표에서 별도 관리) | SCR-004, SCR-005 | `/mates`, `/account` | `playwright.config.ts` | PAGE-SCR004, PAGE-SCR005 | `e2e/mate-auth.spec.ts`(신규) |

**UNIT-TRAVEL-DATES**
- Functional AC: 과거 출발일/체크인, 역전 날짜(귀국일<출발일, 체크아웃≤체크인) 경계값 케이스 전수 통과.
- Visual AC: 해당 없음. **Security/Privacy AC:** 해당 없음.
- Verify: `npm test` 통과. **Priority:** P0

**UNIT-CONTACT-DETECTION**
- Functional AC: 전화번호/이메일/메신저 ID 패턴 탐지율 95% 이상, 오탐 5% 이하 기준 케이스셋 통과.
- Visual AC: 해당 없음. **Security/Privacy AC:** 해당 없음.
- Verify: `npm test` 통과. **Priority:** P0

**UNIT-MATE-STATE**
- Functional AC: 중복 요청 차단, 비작성자 승인/거절 거부, 종료일 경과 후 CLOSED 전환 계산이 모두 검증됨.
- Visual AC: 해당 없음. **Security/Privacy AC:** 해당 없음.
- Verify: `npm test` 통과. **Priority:** P0

**TEST-RLS-BASIC**
- Functional AC: 비회원/타인 계정으로 비공개 행(신청 메시지, 신고, 차단) 조회·수정 시도가 전부 거부됨.
- Visual AC: 해당 없음. **Security/Privacy AC:** 부정 접근 테스트 100% 실패(차단) 확인.
- Verify: Supabase 테스트 러너 또는 SQL 어서션 스크립트 실행. **Priority:** P0

**E2E-PUBLIC-SMOKE**
- Functional AC: **Playwright는 Chromium 대상 Smoke Test만** — Firefox/WebKit 매트릭스, 시각적 회귀, 부하 테스트를 포함하지 않는다. `/` 진입→필터→상세 Drawer→안전정보 Drawer→`/about` 이동까지 5~7개 핵심 흐름 중 앞부분을 커버.
- Visual AC: 390px/1440px 두 뷰포트에서 레이아웃 깨짐 없음(§Release Check 연계).
- Security/Privacy AC: 해당 없음.
- Verify: `npx playwright test e2e/public-smoke.spec.ts --project=chromium`.
- Priority: P0

**E2E-TRAVEL-TOOLS**
- Functional AC: Chromium 전용. 항공/숙소 입력→검증→요약→외부 새 탭 오픈까지 확인, 네트워크 탭에서 입력값이 요청 본문/쿼리에 없음을 확인.
- Visual AC: 해당 없음. **Security/Privacy AC:** 입력값 서버 미전송 재확인(SHARED-EXTERNAL-LINKOUT 계약 검증).
- Verify: `npx playwright test e2e/travel-tools.spec.ts --project=chromium`.
- Priority: P0

**E2E-MATE-AUTH**
- Functional AC: Chromium 전용. 로그인→동행글 작성(연락처 차단 포함)→참가 요청→승인/거절→신고/차단→관리자 신고 상태 변경까지 남은 핵심 흐름 커버.
- Visual AC: 해당 없음. **Security/Privacy AC:** 비인증 접근 차단 재확인.
- Verify: `npx playwright test e2e/mate-auth.spec.ts --project=chromium`.
- Priority: P0

---

## NON_IMPLEMENTATION (EXCLUDED Requirement, 상세 Task 없음 — 25개)

이 표의 Requirement는 위 Task List 어디에도 구현 대상으로 포함하지 않는다. 추적표(`docs/UIUX_TRACEABILITY.md`)에서도 삭제하지 않으며, 여기서 근거와 후속 방향만 기록한다.

| Requirement | 근거(PROJECT_SCOPE.md) | 후속 방향 |
|---|---|---|
| REQ-FUNC-045 | 탈퇴 시 30일 내 삭제·법적 보존 예외 판단은 감사 로그·운영 프로세스가 필요해 제외. 계정 삭제 자체는 Supabase Auth 기본 기능으로 대체 | 운영 인력이 배정되는 단계에서 별도 프로젝트로 재검토 |
| REQ-FUNC-055 | 안전 콘텐츠 작성·검수·게시 워크플로(CMS)는 제외, 콘텐츠는 개발자가 `src/data` 직접 수정 | 콘텐츠 편집자 인력 확보 시 관리자 CRUD 재검토 |
| REQ-FUNC-056 | 안전정보 변경 이력 보존은 감사 로그 제외에 따라 미구현, 이력은 git 커밋으로 대체 | 감사 로그 인프라 도입 시 재검토 |
| REQ-FUNC-071 | 행동 분석 이벤트 스키마·수집 파이프라인은 분석 인프라 부재로 제외 | 분석 플랫폼(GA4 등) 도입 시 재검토 |
| REQ-FUNC-072 | 여행지 콘텐츠 CRUD 관리자 화면은 CMS 제외에 따라 미구현 | 콘텐츠 CMS 도입 시 재검토 |
| REQ-FUNC-073 | 미디어 업로드·라이선스 입력 워크플로 제외, 이미지는 URL+alt만 관리 | 미디어 파이프라인 도입 시 재검토 |
| REQ-FUNC-075 | 안전정보 stale 현황·담당자 대시보드는 "간단한 관리자 탭" 범위(신고 상태·외부 URL만) 밖 | 운영 대시보드 필요성 재확인 후 별도 계획 |
| REQ-FUNC-076 | 관리자 변경·신고 처리 감사 로그는 범용 감사 로그 제외에 따라 미구현 | 감사 로그 인프라 도입 시 재검토 |
| REQ-NF-001 | LCP RUM 측정은 분석 인프라 부재로 제외 | RUM 도입 시 재검토 |
| REQ-NF-002 | INP RUM 측정은 분석 인프라 부재로 제외 | RUM 도입 시 재검토 |
| REQ-NF-003 | CLS RUM 측정은 분석 인프라 부재로 제외 | RUM 도입 시 재검토 |
| REQ-NF-007 | Lighthouse CI 성능 게이트는 CI 파이프라인 확장 범위 밖 | CI 고도화 시 재검토 |
| REQ-NF-008 | 월간 가용성 SLA 측정은 업타임 모니터링 인프라 부재로 제외 | 모니터링 도입 시 재검토 |
| REQ-NF-009 | 내부 API 5xx 비율 모니터링은 모니터링 인프라 부재로 제외 | 모니터링 도입 시 재검토 |
| REQ-NF-010 | DB 백업 RPO/RTO 목표는 "자동 백업" 제외에 따라 다루지 않음, Supabase 기본 백업 사용 | 백업 정책 강화 필요 시 재검토 |
| REQ-NF-011 | 외부 링크 주 1회 자동 검사는 "장애 알림" 인프라 제외 | 스케줄러 도입 시 재검토 |
| REQ-NF-018 | 개인정보 내보내기·탈퇴·삭제 요청 전체 흐름은 감사 로그·운영 프로세스 필요로 제외 | REQ-FUNC-045와 함께 재검토 |
| REQ-NF-020 | 신고 1차 검토 24h 90% SLA는 운영 인력·모니터링 체계 부재로 제외 | 운영 인력 확보 시 재검토 |
| REQ-NF-021 | 글·요청·신고 rate limit 미들웨어는 "간단한 차단·신고" 범위 밖 | 남용 사례 발생 시 재검토 |
| REQ-NF-022 | Moderator 조치 감사 로그 추적성은 범용 감사 로그 제외 | 감사 로그 인프라 도입 시 재검토 |
| REQ-NF-024 | axe 자동 접근성 검사 CI 게이트는 별도 파이프라인 구축 필요로 제외 | 접근성 전담 리소스 확보 시 재검토 |
| REQ-NF-025 | 정식 키보드·스크린리더 수동 검사 프로세스 미도입, E2E에서 기본 포커스만 확인 | 접근성 감사 예산 확보 시 재검토 |
| REQ-NF-029 | 미디어 라이선스 메타데이터(작가·라이선스URL·다운로드일) 100% 관리는 미디어 워크플로 제외, 이미지는 URL+alt만 | 미디어 파이프라인 도입 시 재검토 |
| REQ-NF-032 | 구조화 로그 시스템은 별도 로깅 인프라 필요로 제외, 콘솔 로그로 대체 | 로깅 플랫폼 도입 시 재검토 |
| REQ-NF-033 | 5xx 비율·외부 링크 실패 자동 알림은 "장애 알림" 제외 | 모니터링/알림 도입 시 재검토 |

---

## Release Check (Task List에 포함하지 않는 릴리스 전 수동 확인 항목)

다음은 별도 Task로 만들지 않고, 관련 Task의 Verify 단계 또는 릴리스 직전 사람이 한 번에 확인한다.

- 390px/1440px 실제 기기·브라우저에서 5개 Screen 레이아웃 확인(E2E-PUBLIC-SMOKE/E2E-TRAVEL-TOOLS/E2E-MATE-AUTH의 뷰포트 커버로 상당 부분 대체).
- 항공·호텔·외교부 외부 링크가 실제로 열리는지 배포 직전 1회 수동 클릭 점검.
- `docs/STITCH_VALIDATION_REPORT.md`의 `STITCH_VALIDATION_NEEDS_HUMAN`(SCR-001/SCR-004 `/travel-tools` CTA 경로) 재확인.

---

## 커버리지 검증

| 항목 | 값 |
|---|---:|
| Task List(위 표) 행 수 | 59 |
| Requirement Ref에 등장한 IMPLEMENT 계열 Requirement 수(중복 제외) | 89 |
| NON_IMPLEMENTATION 표 Requirement 수 | 25 |
| **Task List + NON_IMPLEMENTATION 합계** | **114** |
| 빠진 Requirement ID | 없음 |

REQ-FUNC-001~080, REQ-NF-001~034 114개 전부가 위 두 표 중 정확히 하나에만 등장한다(중복·누락 없음). 빠진 항목이 있었다면 이 문서를 완료로 보고하지 않았을 것이다.

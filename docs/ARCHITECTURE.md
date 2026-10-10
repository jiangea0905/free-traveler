# Architecture — Free Traveler

**Document ID:** ARCH-TRAVEL-001
**작성일:** 2026-09-19
**기반 문서:** `package.json`, `docs/06_SRS_UIUX_REVISED.md`, `docs/PROJECT_SCOPE.md`, `design-reference/D-001/DESIGN.md`, `design-reference/UI_CONTRACT.md`, `design-reference/SCREEN_ROUTE_CONTRACT.json`, `TASKS/TASK_MANIFEST.csv`

이 문서는 Free Traveler가 **무엇으로 만들어지고 무엇으로 만들어지지 않는지**를 정의한다. 새로운 기술 스택이나 인프라를 여기서 결정하지 않는다 — 이미 승인된 문서(SRS, PROJECT_SCOPE, DESIGN, Task List)에 있는 결정을 하나의 경계선으로 정리한다.

---

## 1. 기술 스택

| 계층 | 선택 | 근거 |
|---|---|---|
| 프레임워크 | **Next.js App Router** (`package.json`: `next@16.3.4`) | `docs/06_SRS_UIUX_REVISED.md` §2 UI Route Contract, `design-reference/SCREEN_ROUTE_CONTRACT.json`의 `framework: "nextjs-app-router"` |
| 언어 | **TypeScript** (`typescript@^5`) | 전 프로젝트 정적 타입 검사, `tsconfig.json` 기준 |
| UI 라이브러리 | React 19 (`react@19.2.8`, `react-dom@19.2.8`) | Next.js 16 기본 |
| 스타일 | Tailwind CSS 4 (`@tailwindcss/postcss@^4`, `tailwindcss@^4`) | `design-reference/D-001/DESIGN.md`의 Color/Spacing/Radius 토큰을 유틸리티 클래스로 매핑 |
| 데이터베이스/인증 | Supabase (PostgreSQL + Auth) | §7, §8 참고 |
| ORM | **사용하지 않음** | §11 참고 |
| 정적 콘텐츠 | `src/data`의 TypeScript 모듈 | §6 참고 |
| 테스트 | Vitest(단위) + Playwright(Chromium Smoke) | §12 참고 |
| CI/배포 | GitHub Actions + Vercel Preview | §13 참고 |

Next.js App Router를 쓰므로 라우팅은 파일 시스템 기반(`src/app/**/page.tsx`)이며, 별도 라우터 라이브러리를 추가하지 않는다.

## 2. 화면 구성 — 핵심 4개·보조 1개

`design-reference/SCREEN_ROUTE_CONTRACT.json`의 `category_summary`(core 4 / auxiliary 1)를 그대로 따른다.

| Screen ID | 구분 | Route | Page Entry |
|---|---|---|---|
| SCR-001 | 핵심(Core) | `/` | `src/app/page.tsx` |
| SCR-002 | 보조(Auxiliary) | `/about` | `src/app/about/page.tsx` |
| SCR-003 | 핵심(Core) | `/travel-tools` | `src/app/travel-tools/page.tsx` |
| SCR-004 | 핵심(Core) | `/mates` | `src/app/mates/page.tsx` |
| SCR-005 | 핵심(Core) | `/account` | `src/app/account/page.tsx` |

이 5개 Page Entry 외의 새 최상위 Route(`src/app/<name>/page.tsx`)를 추가하지 않는다. `/auth/callback`, `/api/*`, `not-found.tsx`, `error.tsx`는 기술 Route이며 이 5개 Screen 목록에 포함되지 않는다(`TASKS/TASK_MANIFEST.csv`의 `PAGE-SCR00N` 5개 행과 대응).

## 3. Server Component와 Client Component 구분

| 구분 | 사용처 | 규칙 |
|---|---|---|
| **Server Component**(기본값) | 각 Page Entry(`page.tsx`) 자체, `src/data` 정적 콘텐츠를 읽어 렌더링하는 목록/상세 Section, SEO 메타데이터(`generateMetadata`) | 데이터 조회(정적 데이터 import, Supabase 서버 클라이언트 조회)는 가능한 한 Server Component에서 수행한다. 브라우저 API·이벤트 핸들러·상태(`useState`)를 사용하지 않는다. |
| **Client Component**(`"use client"`) | 항공·숙소 입력 Form, 검색·필터 상호작용, Drawer/Modal 열고 닫기, 탭 전환, Toast, 즐겨찾기(localStorage), 참가 요청/신고/차단 폼, 관리자 상태 변경 UI | 사용자 입력·브라우저 전용 API(`localStorage`, `window.open`)·일시 상태가 필요한 곳에만 최소 범위로 `"use client"`를 선언한다. |

Page Owner(`PAGE-SCR00N`)는 Server Component로 시작해, 상호작용이 필요한 하위 Component만 Client Component로 조립한다. 페이지 전체를 Client Component로 만들지 않는다.

## 4. 항공·숙소 입력 폼 — Client Component 일시 상태만 사용

- 항공(`/travel-tools` 항공편 탭)·숙소(숙소 탭) 입력 Form은 **Client Component의 컴포넌트 상태(`useState`/`useReducer`)로만** 국가·지역·출발일(체크인)·귀국일(체크아웃)을 보관한다.
- 이 상태는 페이지를 벗어나거나 새로고침하면 사라지는 **일시 상태**다. `localStorage`, `sessionStorage`, 쿠키, 전역 상태 관리 라이브러리에 저장하지 않는다.
- 요약 확인 후 외부 이동 버튼을 누르면 `noopener,noreferrer` 새 탭으로 설정된 외부 URL을 열 뿐, 폼 상태를 어디에도 전달하지 않는다.

## 5. 항공·숙소 입력값 비전송 원칙

항공·숙소 입력값(국가, 지역, 출발일/체크인, 귀국일/체크아웃)은 다음 어디로도 전송하지 않는다.

- **API**: 이 값들을 위한 Route Handler(`src/app/api/**`)를 만들지 않는다.
- **DB**: Supabase 테이블에 저장하지 않는다(§8의 6개 테이블 중 이 값을 위한 테이블은 없다).
- **URL**: 외부 이동 시 목적지 URL에 쿼리 파라미터로 붙이지 않는다.
- **로그**: 서버 로그, 분석 이벤트, 에러 리포팅 어디에도 원문 값을 기록하지 않는다.

`SHARED-EXTERNAL-LINKOUT` 유틸(`src/lib/external-linkout.ts`, `TASKS/TASK-SHARED-EXTERNAL-LINKOUT.md`)이 이 규칙을 코드 레벨에서 강제하는 유일한 통로다.

## 6. 정적 콘텐츠 — `src/data`

여행지, 국가 안전정보, `free_traveler` 대표 프로필은 데이터베이스 테이블이 아니라 **`src/data`의 TypeScript 정적 데이터**로 관리한다.

| 콘텐츠 | 파일(예정) | Task |
|---|---|---|
| 여행지(국내 10 · 해외 15개국 30도시) | `src/data/destinations.ts` | `DATA-DESTINATIONS` |
| 국가 안전정보 | `src/data/safety.ts` | `DATA-SAFETY` |
| 대표 프로필 | `src/data/representative.ts` | `DATA-REPRESENTATIVE` |

이 콘텐츠를 위한 CRUD API, 관리자 편집 화면, 별도 DB 테이블을 만들지 않는다. 콘텐츠 변경은 코드 변경(PR)으로 이루어진다.

## 7. Supabase — Auth와 동행 기능 중심

Supabase는 **이메일 인증(성인 확인 포함)과 동행(Mate) 기능**을 위해서만 사용한다.

- 인증: 이메일 가입·로그인·로그아웃·비밀번호 재설정, 성인 확인 상태(`is_adult`, `adult_verified_at`)만 저장 — 정확한 생년월일은 저장하지 않는다.
- 동행 기능: 동행 모집글, 참가 요청, 차단, 신고, 관리자 설정(§8 6개 테이블).
- 여행지·안전정보·대표 프로필은 Supabase에 저장하지 않는다(§6).
- 콘텐츠 관리 백엔드(CMS)로 쓰지 않는다.

## 8. 데이터베이스 — 정확히 6개 Table

| Table | 역할 |
|---|---|
| `user_profile` | 닉네임, 연령대, 여행 스타일, 성인 확인 상태 |
| `mate_post` | 동행 모집글 |
| `mate_application` | 참가 요청 |
| `user_block` | 차단 관계 |
| `report` | 신고 |
| `admin_setting` | 항공·숙소 외부 URL 등 관리자 설정 |

이 6개를 넘는 새 테이블을 추가하지 않는다(`docs/PROJECT_SCOPE.md`의 DB 6개 제한, `TASKS/TASK-DB-SCHEMA-BASE.md` 근거). 여행지/안전정보/대표 프로필용 테이블, 감사 로그 테이블, 분석 이벤트 테이블은 만들지 않는다.

## 9. Browser Client와 Server Client 분리

| 클라이언트 | 위치(예정) | 사용처 |
|---|---|---|
| Browser Supabase Client | `src/lib/supabase/client.ts` | Client Component에서의 세션 확인, 로그인/로그아웃 호출 |
| Server Supabase Client | `src/lib/supabase/server.ts` | Server Component·Route Handler에서의 데이터 조회/쓰기, 쿠키 기반 세션 검증 |

두 클라이언트는 별도 모듈로 분리하고, Server 전용 키(있다면)는 Server Client 모듈 밖으로 내보내지 않는다.

## 10. 간단한 RLS 원칙

- 기본값은 **본인 행만 읽기/쓰기 가능**(`user_id = auth.uid()`)이다.
- `mate_post`, `report` 등 공개 열람이 필요한 테이블은 "공개 여부가 명시된 행만 익명 SELECT 허용" 형태로 최소한만 넓힌다.
- `admin_setting`과 신고 상태 변경은 `user_profile.role = 'admin'`(또는 동등 컬럼)인 사용자만 쓰기 허용.
- 복잡한 계층적 정책, 커스텀 함수 기반 정책 엔진을 만들지 않는다 — 정책은 테이블당 최소 개수로 유지한다.
- RLS는 `TASKS/TASK-DB-RLS-BASE.md`에서 관리하며, 애플리케이션 코드가 아니라 DB 정책이 최종 방어선이다.

## 11. Prisma·ORM 미사용

Supabase JS 클라이언트(`@supabase/supabase-js`, `@supabase/ssr`)로 직접 쿼리한다. Prisma, Drizzle 등 별도 ORM을 추가하지 않는다. 타입 안전성은 Supabase가 생성하는 타입(또는 수기 작성한 타입)과 zod 입력 검증으로 확보한다.

## 12. 테스트 전략

| 종류 | 도구 | 범위 |
|---|---|---|
| 단위 테스트 | **Vitest** | 날짜 검증, 연락처 탐지, 동행 상태 전이 등 순수 로직(`TASKS/TASK-UNIT-*.md`) |
| E2E 테스트 | **Playwright — Chromium Smoke만** | 공개 화면, 항공·숙소 흐름, 동행·인증·관리자 흐름 3개 스펙(`TASKS/TASK-E2E-*.md`) |

Firefox/WebKit 매트릭스, 시각적 회귀 테스트, 부하 테스트, Jest 등 다른 테스트 러너를 추가하지 않는다.

## 13. CI/CD — GitHub Actions와 Vercel Preview

- **GitHub Actions**: PR마다 lint(`next lint`) · build(`next build`) · Vitest 단위 테스트를 실행하는 게이트(`TASKS/TASK-CI-LINT-BUILD-TEST.md`). 정적 데이터 완전성 검증 스크립트(`TASKS/TASK-CI-DATA-VALIDATION.md`)도 같은 파이프라인에서 실행한다.
- **Vercel Preview**: GitHub 저장소와 Vercel 프로젝트를 연결해 PR마다 Preview 배포를 받는다. 별도 배포 스크립트나 컨테이너 빌드를 만들지 않는다.
- Playwright E2E는 이 CI 파이프라인 또는 Preview 배포 URL을 대상으로 수동/정기 실행하며, 매 PR마다 강제하지는 않는다(§12 범위 유지).

## 14. AWS·EC2 미사용

컴퓨팅·스토리지·데이터베이스 어떤 용도로도 AWS(EC2, S3, RDS, Lambda 등)를 사용하지 않는다. 호스팅은 Vercel, 데이터베이스/인증은 Supabase로 충분하다.

## 15. 자동 Merge 미사용

CI가 통과했다고 자동으로 PR을 병합하는 워크플로(auto-merge, merge bot, merge queue 자동화)를 구성하지 않는다. 병합은 사람이 검토 후 수동으로 수행한다.

---

## 16. 착수 차단 (Blockers)

아래 항목은 실제로 로컬 저장소에 없는 것을 확인한 파일·환경변수만 기록한다. "아직 구현하지 않은 기능"은 여기 포함하지 않는다 — 그런 항목은 `TASKS/00_TASK_LIST.md`와 `TASKS/TASK_MANIFEST.csv`가 이미 추적하고 있다.

| # | 차단 항목 | 확인 방법 | 해소 방법 |
|---|---|---|---|
| 1 | `package.json`에 `@supabase/supabase-js`, `@supabase/ssr`, `zod`, `vitest`, `@playwright/test`가 없음 | `cat package.json` — 현재 `dependencies`/`devDependencies`에 4개 패키지 미포함 확인 | `TASKS/TASK-SETUP-DEPENDENCIES.md` 수행 |
| 2 | `.env.local`/`.env.example` 파일이 저장소에 없음 | 저장소 루트에 `.env*` 파일 없음 확인 | `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY` 값을 담은 `.env.local`(로컬)과 `.env.example`(커밋용, 값 없이 키만) 생성 — `TASKS/TASK-MANUAL-SUPABASE-CONFIG.md` |
| 3 | Supabase 프로젝트 자체의 존재 여부를 로컬에서 확인할 수 없음 | 코드/설정에 프로젝트 URL·키 참조가 없어 실제 프로비저닝 여부 미확인 | 사람이 Supabase 콘솔에서 프로젝트를 생성하고 URL/anon key를 발급해 항목 2에 반영 |
| 4 | `.github/workflows/` 디렉터리가 없음 | 저장소에 GitHub Actions 워크플로 파일 없음 확인 | `TASKS/TASK-CI-LINT-BUILD-TEST.md` 수행(§13) |
| 5 | `supabase/` 디렉터리(마이그레이션)가 없음 | 저장소에 `supabase/migrations/*.sql` 없음 확인 | `TASKS/TASK-DB-SCHEMA-BASE.md` 수행(§8) |

이 5가지가 해소되기 전에는 Supabase 연동 코드나 CI 파이프라인을 실제로 동작시킬 수 없다. 반대로 `src/data` 정적 데이터 작성, UI Component 작업(§2~§4)은 이 블로커와 무관하게 바로 시작할 수 있다.

## 17. 명시적 범위 제외

다음은 이번 프로젝트 범위에서 **제외**한다(`docs/PROJECT_SCOPE.md` 근거). 착수 차단 항목이 아니며, 앞으로도 만들 계획이 없다.

- **콘텐츠 CMS**: 여행지·안전정보·대표 프로필 편집을 위한 관리자 CRUD 화면·백엔드를 만들지 않는다(§6).
- **외부 Email 공급자 연동**: 실제 이메일 발송(SendGrid, SES 등)을 연동하지 않는다. 알림은 화면 내 Toast/상태로 대체한다.
- **Monitoring/관측 인프라**: APM, 구조화 로그 수집, 업타임 모니터링, 에러 리포팅 서비스(Sentry 등)를 도입하지 않는다.

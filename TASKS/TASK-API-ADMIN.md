# API-ADMIN — 신고 상태 변경·외부 URL 설정

**Category:** API | **Implementation Status:** IMPLEMENT(축소) | **Priority:** P0 | **Seq:** 13

## Context

신고 상태 변경·외부 URL 설정. Next.js Route Handler로 구현하는 내부 API이며, DB Task 완료 후 Component/Page Owner가 호출한다.

## Project Scope

Implementation Status: **IMPLEMENT(축소)** (`docs/PROJECT_SCOPE.md` 기준). 범위(축소, PROJECT_SCOPE 근거): 신고 상태 변경(OPEN/RESOLVED/DISMISSED)과 외부 URL 설정만 처리 — 콘텐츠 CRUD·감사로그·통계는 만들지 않는다. Requirement Ref: REQ-FUNC-077.

## Requirement Ref

REQ-FUNC-077

## Screen / Route / Page Entry

- Screen: N/A
- Route: N/A
- Page Entry: `src/app/api/admin/reports/route.ts`, `src/app/api/admin/settings/route.ts`

## Design Ref

해당 없음(비-UI Task)

## Depends On

DB-SCHEMA-BASE, DB-RLS-BASE, DB-ACCESS

## Expected Files

`src/app/api/admin/reports/route.ts`(신규), `src/app/api/admin/settings/route.ts`(신규)

이 Task는 위 Expected Files 목록에 있는 파일만 생성 · 수정한다. 목록 밖의 파일을 건드리지 않는다.

## Functional AC

**범위(축소, PROJECT_SCOPE 근거): 신고 상태 변경(OPEN/RESOLVED/DISMISSED)과 외부 URL 설정만 처리 — 콘텐츠 CRUD·감사로그·통계는 만들지 않는다.** URL은 HTTPS만 허용, `javascript:`/HTTP 저장 차단

## Visual AC

해당 없음

## Security/Privacy AC

Admin 역할만 접근(RLS+서버 검증 이중)

## Test Cases

- 범위(축소, PROJECT_SCOPE 근거): 신고 상태 변경(OPEN/RESOLVED/DISMISSED)과 외부 URL 설정만 처리 — 콘텐츠 CRUD·감사로그·통계는 만들지 않는다
- URL은 HTTPS만 허용, `javascript:`/HTTP 저장 차단

## Verify

E2E-MATE-AUTH(관리자 경로 일부)

## Definition of Done

- Functional AC, Visual AC, Security/Privacy AC 항목이 모두 충족된다.
- Expected Files에 명시된 파일만 생성 · 수정되었고 그 외 파일은 변경하지 않았다.
- Verify에 명시된 테스트/확인이 실제로 통과한다.
- Depends On에 있는 모든 선행 Task가 완료된 상태에서 시작했다.

## Forbidden

- Expected Files 목록 밖의 파일을 생성·수정하지 않는다.
- Airbnb 등 참고 디자인의 상표 요소(로고 · 워드마크 · 브랜드 컬러)를 재현하지 않는다.
- 구매 · 예약 · 결제 UI, 실시간 항공권 · 호텔 가격, 별점 · 리뷰, 광고 배너를 추가하지 않는다.
- EC2 · AWS 인프라, 자동 Merge Runner를 구성하지 않는다.
- `docs/PROJECT_SCOPE.md`에서 EXCLUDED로 분류된 기능(콘텐츠 CMS, 미디어 업로드 워크플로, 감사 로그, 실시간 채팅 · 위치공유, rate limit 미들웨어 등)을 이 Task 범위에서 구현하지 않는다.
- 신고 상태 변경과 외부 URL 설정 외의 관리자 기능(콘텐츠 CRUD, 감사 로그, 통계)을 추가하지 않는다.

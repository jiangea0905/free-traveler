# API-BLOCKS-REPORTS — 차단·신고 접수

**Category:** API | **Implementation Status:** IMPLEMENT | **Priority:** P0 | **Seq:** 12

## Context

차단·신고 접수. Next.js Route Handler로 구현하는 내부 API이며, DB Task 완료 후 Component/Page Owner가 호출한다.

## Project Scope

Implementation Status: **IMPLEMENT** (`docs/PROJECT_SCOPE.md` 기준). 축소나 대체 없이 전체 범위를 구현한다. Requirement Ref: REQ-FUNC-039(연계), 040, REQ-NF-019(축소).

## Requirement Ref

REQ-FUNC-039(연계), 040, REQ-NF-019(축소)

## Screen / Route / Page Entry

- Screen: N/A
- Route: N/A
- Page Entry: `src/app/api/blocks/route.ts`, `src/app/api/reports/route.ts`

## Design Ref

해당 없음(비-UI Task)

## Depends On

DB-SCHEMA-BASE, DB-RLS-BASE, DB-ACCESS

## Expected Files

`src/app/api/blocks/route.ts`(신규), `src/app/api/reports/route.ts`(신규)

이 Task는 위 Expected Files 목록에 있는 파일만 생성 · 수정한다. 목록 밖의 파일을 건드리지 않는다.

## Functional AC

신고 접수 시 접수 ID 즉시 반환. 차단 성립 시 상호 글/프로필/요청 비노출(쿼리 단에서 필터)

## Visual AC

해당 없음

## Security/Privacy AC

신고자/피신고자 상세는 Moderator/Admin만 조회

## Test Cases

- 신고 접수 시 접수 ID 즉시 반환
- 차단 성립 시 상호 글/프로필/요청 비노출(쿼리 단에서 필터)

## Verify

E2E-MATE-AUTH

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

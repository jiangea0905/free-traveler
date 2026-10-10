# DB-SCHEMA-BASE — 핵심 6개 테이블 스키마 정의

**Category:** DB | **Implementation Status:** IMPLEMENT | **Priority:** P0 | **Seq:** 2

## Context

핵심 6개 테이블 스키마 정의. Supabase PostgreSQL 계층의 기반 작업이며, 이후 모든 API Task가 이 위에서 동작한다.

## Project Scope

Implementation Status: **IMPLEMENT** (`docs/PROJECT_SCOPE.md` 기준). 축소나 대체 없이 전체 범위를 구현한다. Requirement Ref: REQ-FUNC-044(기반).

## Requirement Ref

REQ-FUNC-044(기반)

## Screen / Route / Page Entry

- Screen: N/A
- Route: N/A
- Page Entry: N/A

## Design Ref

해당 없음(비-UI Task)

## Depends On

SETUP-DEPENDENCIES

## Expected Files

`supabase/migrations/0001_core_schema.sql`(신규)

이 Task는 위 Expected Files 목록에 있는 파일만 생성 · 수정한다. 목록 밖의 파일을 건드리지 않는다.

## Functional AC

테이블은 정확히 6개로 제한 — `user_profile`, `mate_post`, `mate_application`, `user_block`, `report`, `admin_setting`. 여행지·안전정보·대표 프로필은 테이블을 만들지 않는다(정적 데이터 Task로 처리, §DATA 참고)

## Visual AC

해당 없음

## Security/Privacy AC

`user_profile`에 정확한 생년월일 컬럼을 두지 않는다(`is_adult boolean`, `adult_verified_at timestamptz`만)

## Test Cases

- 테이블은 정확히 6개로 제한 — `user_profile`, `mate_post`, `mate_application`, `user_block`, `report`, `admin_setting`
- 여행지·안전정보·대표 프로필은 테이블을 만들지 않는다(정적 데이터 Task로 처리, §DATA 참고)

## Verify

마이그레이션 적용 후 `information_schema.tables`에서 테이블 6개 확인

## Definition of Done

- Functional AC, Visual AC, Security/Privacy AC 항목이 모두 충족된다.
- Expected Files에 명시된 파일만 생성 · 수정되었고 그 외 파일은 변경하지 않았다.
- Verify에 명시된 테스트/확인이 실제로 통과한다.
- Depends On에 있는 모든 선행 Task가 완료된 상태에서 시작했다.
- 정의된 6개 테이블 외 테이블을 추가하지 않았다.

## Forbidden

- Expected Files 목록 밖의 파일을 생성·수정하지 않는다.
- Airbnb 등 참고 디자인의 상표 요소(로고 · 워드마크 · 브랜드 컬러)를 재현하지 않는다.
- 구매 · 예약 · 결제 UI, 실시간 항공권 · 호텔 가격, 별점 · 리뷰, 광고 배너를 추가하지 않는다.
- EC2 · AWS 인프라, 자동 Merge Runner를 구성하지 않는다.
- `docs/PROJECT_SCOPE.md`에서 EXCLUDED로 분류된 기능(콘텐츠 CMS, 미디어 업로드 워크플로, 감사 로그, 실시간 채팅 · 위치공유, rate limit 미들웨어 등)을 이 Task 범위에서 구현하지 않는다.
- 정의된 6개 테이블(user_profile/mate_post/mate_application/user_block/report/admin_setting) 외 신규 테이블을 추가하지 않는다.

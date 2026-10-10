# DB-RLS-BASE — Row Level Security 정책

**Category:** DB | **Implementation Status:** IMPLEMENT | **Priority:** P0 | **Seq:** 3

## Context

Row Level Security 정책. Supabase PostgreSQL 계층의 기반 작업이며, 이후 모든 API Task가 이 위에서 동작한다.

## Project Scope

Implementation Status: **IMPLEMENT** (`docs/PROJECT_SCOPE.md` 기준). 축소나 대체 없이 전체 범위를 구현한다. Requirement Ref: REQ-FUNC-044, REQ-NF-013.

## Requirement Ref

REQ-FUNC-044, REQ-NF-013

## Screen / Route / Page Entry

- Screen: N/A
- Route: N/A
- Page Entry: N/A

## Design Ref

해당 없음(비-UI Task)

## Depends On

DB-SCHEMA-BASE

## Expected Files

`supabase/migrations/0002_rls_policies.sql`(신규)

이 Task는 위 Expected Files 목록에 있는 파일만 생성 · 수정한다. 목록 밖의 파일을 건드리지 않는다.

## Functional AC

본인 글/요청, 글 작성자, Moderator/Admin만 비공개 행을 읽도록 정책 작성. `admin_setting`은 Admin만 쓰기 가능

## Visual AC

해당 없음

## Security/Privacy AC

익명 사용자는 `mate_application`, `report`, `user_block`을 읽을 수 없다

## Test Cases

- 본인 글/요청, 글 작성자, Moderator/Admin만 비공개 행을 읽도록 정책 작성
- `admin_setting`은 Admin만 쓰기 가능

## Verify

TEST-RLS-BASIC 통과

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
- DB-SCHEMA-BASE가 정의한 6개 테이블 스키마를 벗어나는 새 테이블을 추가하지 않는다.

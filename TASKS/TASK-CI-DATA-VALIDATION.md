# CI-DATA-VALIDATION — 정적 데이터 완전성 검증 스크립트

**Category:** CI_OPS | **Implementation Status:** IMPLEMENT(대체) | **Priority:** P1 | **Seq:** 50

## Context

정적 데이터 완전성 검증 스크립트. 코드 품질 또는 콘텐츠 완전성을 자동으로 검증하는 파이프라인 작업이다.

## Project Scope

Implementation Status: **IMPLEMENT(대체)** (`docs/PROJECT_SCOPE.md` 기준). 런타임 게시 게이트 대신 빌드/CI 단계 정적 데이터 검증으로 대체(PROJECT_SCOPE 근거). Requirement Ref: REQ-FUNC-074, REQ-NF-026, REQ-NF-027, REQ-NF-028(축소).

## Requirement Ref

REQ-FUNC-074, REQ-NF-026, REQ-NF-027, REQ-NF-028(축소)

## Screen / Route / Page Entry

- Screen: N/A
- Route: N/A
- Page Entry: N/A

## Design Ref

해당 없음(비-UI Task)

## Depends On

DATA-DESTINATIONS, DATA-SAFETY, DATA-REPRESENTATIVE

## Expected Files

`scripts/validate_content.py`(신규)

이 Task는 위 Expected Files 목록에 있는 파일만 생성 · 수정한다. 목록 밖의 파일을 건드리지 않는다.

## Functional AC

**런타임 게시 게이트 대신 빌드/CI 단계 정적 데이터 검증으로 대체(PROJECT_SCOPE 근거).** 여행지 수량(국내10/해외15개국30도시), 안전정보 8카테고리, 대표 프로필 30국/6타임라인/8갤러리, 필수 필드 누락을 검사하고 실패 시 CI 실패

## Visual AC

해당 없음

## Security/Privacy AC

해당 없음

## Test Cases

- 런타임 게시 게이트 대신 빌드/CI 단계 정적 데이터 검증으로 대체(PROJECT_SCOPE 근거)
- 여행지 수량(국내10/해외15개국30도시), 안전정보 8카테고리, 대표 프로필 30국/6타임라인/8갤러리, 필수 필드 누락을 검사하고 실패 시 CI 실패

## Verify

`python scripts/validate_content.py` 성공 종료

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

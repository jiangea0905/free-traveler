# UNIT-CONTACT-DETECTION — 연락처 탐지 단위 테스트

**Category:** UNIT_TEST | **Implementation Status:** IMPLEMENT | **Priority:** P0 | **Seq:** 54

## Context

연락처 탐지 단위 테스트. 관련 구현 Task가 완료된 뒤 실행하는 검증 Task다.

## Project Scope

Implementation Status: **IMPLEMENT** (`docs/PROJECT_SCOPE.md` 기준). 축소나 대체 없이 전체 범위를 구현한다. Requirement Ref: REQ-FUNC-032.

## Requirement Ref

REQ-FUNC-032

## Screen / Route / Page Entry

- Screen: N/A
- Route: N/A
- Page Entry: N/A

## Design Ref

해당 없음(비-UI Task)

## Depends On

SHARED-CONTACT-FILTER

## Expected Files

`src/lib/__tests__/contact-filter.test.ts`(신규)

이 Task는 위 Expected Files 목록에 있는 파일만 생성 · 수정한다. 목록 밖의 파일을 건드리지 않는다.

## Functional AC

전화번호/이메일/메신저 ID 패턴 탐지율 95% 이상, 오탐 5% 이하 기준 케이스셋 통과

## Visual AC

해당 없음

## Security/Privacy AC

해당 없음

## Test Cases

- 전화번호/이메일/메신저 ID 패턴 탐지율 95% 이상, 오탐 5% 이하 기준 케이스셋 통과

## Verify

`npm test` 통과

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

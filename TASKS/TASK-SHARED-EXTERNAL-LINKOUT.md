# SHARED-EXTERNAL-LINKOUT — 외부 이동(새 탭, 비전달) 유틸

**Category:** SHARED | **Implementation Status:** IMPLEMENT | **Priority:** P0 | **Seq:** 22

## Context

외부 이동(새 탭, 비전달) 유틸. 여러 Screen이 공통으로 재사용하는 유틸 또는 컴포넌트다.

## Project Scope

Implementation Status: **IMPLEMENT** (`docs/PROJECT_SCOPE.md` 기준). 입력값을 서버·DB·외부 URL에 전달하지 않는다(금지). Requirement Ref: REQ-NF-017.

## Requirement Ref

REQ-NF-017

## Screen / Route / Page Entry

- Screen: N/A
- Route: N/A
- Page Entry: N/A

## Design Ref

해당 없음(로직 유틸, UI는 COMP-SCR003-FLIGHT-FORM/HOTEL-FORM)

## Depends On

없음

## Expected Files

`src/lib/external-linkout.ts`(신규)

이 Task는 위 Expected Files 목록에 있는 파일만 생성 · 수정한다. 목록 밖의 파일을 건드리지 않는다.

## Functional AC

**입력값을 서버·DB·외부 URL에 전달하지 않는다(금지).** `window.open`으로 `noopener,noreferrer` 새 탭, 목적지·날짜 쿼리 파라미터 미부착. 허용목록 밖/미설정 URL은 이동 차단

## Visual AC

해당 없음

## Security/Privacy AC

클라이언트 상태로만 유지, 네트워크 요청 없음

## Test Cases

- 입력값을 서버·DB·외부 URL에 전달하지 않는다(금지)
- `window.open`으로 `noopener,noreferrer` 새 탭, 목적지·날짜 쿼리 파라미터 미부착
- 허용목록 밖/미설정 URL은 이동 차단

## Verify

E2E-TRAVEL-TOOLS(네트워크 탭 확인)

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
- 입력값(국가 · 지역 · 날짜)을 서버, DB, 외부 URL 쿼리 파라미터로 전송하지 않는다.

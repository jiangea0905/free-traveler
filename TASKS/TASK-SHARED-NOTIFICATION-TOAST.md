# SHARED-NOTIFICATION-TOAST — 상태 변경 Toast 알림

**Category:** SHARED | **Implementation Status:** IMPLEMENT | **Priority:** P1 | **Seq:** 20

## Context

상태 변경 Toast 알림. 여러 Screen이 공통으로 재사용하는 유틸 또는 컴포넌트다.

## Project Scope

Implementation Status: **IMPLEMENT** (`docs/PROJECT_SCOPE.md` 기준). 구현 방법(지정): 화면 상태 기반 Toast, 실제 이메일 발송 없음. Requirement Ref: REQ-FUNC-043.

## Requirement Ref

REQ-FUNC-043

## Screen / Route / Page Entry

- Screen: 전역
- Route: N/A
- Page Entry: N/A

## Design Ref

`design-reference/D-001/DESIGN.md` §Alert · Toast

## Depends On

없음

## Expected Files

`src/components/ui/Toast.tsx`(신규)

이 Task는 위 Expected Files 목록에 있는 파일만 생성 · 수정한다. 목록 밖의 파일을 건드리지 않는다.

## Functional AC

**구현 방법(지정): 화면 상태 기반 Toast, 실제 이메일 발송 없음.** 참가 요청 접수/승인/거절/신고 접수 시 노출, 약 4초 자동 닫힘

## Visual AC

`D-001/DESIGN.md` Toast 토큰(ink 배경, 하단 위치) 적용

## Security/Privacy AC

해당 없음

## Test Cases

- 구현 방법(지정): 화면 상태 기반 Toast, 실제 이메일 발송 없음
- 참가 요청 접수/승인/거절/신고 접수 시 노출, 약 4초 자동 닫힘

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

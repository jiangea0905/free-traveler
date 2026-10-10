# SHARED-HEADER-FOOTER — 공통 Header/Footer 레이아웃

**Category:** SHARED | **Implementation Status:** IMPLEMENT | **Priority:** P0 | **Seq:** 14

## Context

공통 Header/Footer 레이아웃. 여러 Screen이 공통으로 재사용하는 유틸 또는 컴포넌트다.

## Project Scope

Implementation Status: **IMPLEMENT** (`docs/PROJECT_SCOPE.md` 기준). 축소나 대체 없이 전체 범위를 구현한다. Requirement Ref: REQ-FUNC-064, 065.

## Requirement Ref

REQ-FUNC-064, 065

## Screen / Route / Page Entry

- Screen: 전역
- Route: 전체(5개 Route 공통)
- Page Entry: `src/app/layout.tsx`

## Design Ref

`design-reference/D-001/DESIGN.md` §Header · Footer

## Depends On

SETUP-DEPENDENCIES

## Expected Files

`src/app/layout.tsx`(수정 — 기존 기본 레이아웃 교체), `src/components/layout/Header.tsx`(신규), `src/components/layout/Footer.tsx`(신규)

이 Task는 위 Expected Files 목록에 있는 파일만 생성 · 수정한다. 목록 밖의 파일을 건드리지 않는다.

## Functional AC

5개 Screen 모두 같은 Header/Footer 컴포넌트를 import. 핵심 4개+보조 1개 화면으로 2회 이내 이동 가능한 내비게이션

## Visual AC

`design-reference/D-001/DESIGN.md` Header/Footer 토큰(Desktop 72px/Mobile 56px, hairline border, 코랄 액센트만 CTA) 그대로 적용

## Security/Privacy AC

해당 없음

## Test Cases

- 5개 Screen 모두 같은 Header/Footer 컴포넌트를 import
- 핵심 4개+보조 1개 화면으로 2회 이내 이동 가능한 내비게이션

## Verify

E2E-PUBLIC-SMOKE

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

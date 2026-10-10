# PAGE-SCR002 — SCR-002 대표 소개 Page Owner

**Category:** PAGE_OWNER | **Implementation Status:** IMPLEMENT | **Priority:** P1 | **Seq:** 32

## Context

SCR-002 대표 소개 Page Owner. SCR-002(`/about`)의 최종 Route Page를 조립하는 Page Owner Task이며, Depends On에 명시된 Component/Data/API/Shared Task의 산출물을 가져와 `src/app/about/page.tsx`에 배치한다.

## Project Scope

Implementation Status: **IMPLEMENT** (`docs/PROJECT_SCOPE.md` 기준). 축소나 대체 없이 전체 범위를 구현한다. Requirement Ref: REQ-FUNC-057~063(조립).

## Requirement Ref

REQ-FUNC-057~063(조립)

## Screen / Route / Page Entry

- Screen: SCR-002
- Route: `/about`
- Page Entry: `src/app/about/page.tsx`

## Design Ref

`design-reference/D-001/DESIGN.md` §Page Section 최대 폭과 상하 여백, §화면별 Section 순서와 최소 콘텐츠 수

## Depends On

COMP-SCR002-PROFILE-HERO, COMP-SCR002-TIMELINE-COUNTRIES, COMP-SCR002-GALLERY-RECOMMENDED, SHARED-HEADER-FOOTER, DATA-REPRESENTATIVE

## Expected Files

`src/app/about/page.tsx`(신규)

이 Task는 위 Expected Files 목록에 있는 파일만 생성 · 수정한다. 목록 밖의 파일을 건드리지 않는다.

## Functional AC

Header → ①Profile Hero → ②여행 지표 → ③소개·철학 → ④Timeline **6개+** → ⑤방문 국가 **30개** → ⑥Gallery **8장+** → ⑦기억에 남는 여행지 **4개**+CTA → Footer. 전 Section 데이터 출처는 `DATA-REPRESENTATIVE` 단일 소스

Functional AC(상태 — `design-reference/UI_CONTRACT.md` SCR-002 §상태 그대로 조립): **Loading**은 사진·Timeline 스켈레톤으로 표시한다(정적 콘텐츠이므로 Empty/Unauthorized는 해당 없음). **Error**는 이미지 로드 실패 시 alt 텍스트가 보이는 대체 박스로 표시한다.

## Visual AC

Desktop 최대 폭 1200~1280px, Section 여백 64~96px(Mobile 40~64px). Hero/통계/좌우분할/Timeline/Chip목록/Gallery/CTA Banner를 교차 배치해 동일 패턴 반복 금지

## Security/Privacy AC

없음

## Test Cases

- Header → ①Profile Hero → ②여행 지표 → ③소개·철학 → ④Timeline 6개+ → ⑤방문 국가 30개 → ⑥Gallery 8장+ → ⑦기억에 남는 여행지 4개+CTA → Footer
- 전 Section 데이터 출처는 `DATA-REPRESENTATIVE` 단일 소스

## Verify

E2E-PUBLIC-SMOKE, 수동 브라우저 확인

## Definition of Done

- Functional AC, Visual AC, Security/Privacy AC 항목이 모두 충족된다.
- Expected Files에 명시된 파일만 생성 · 수정되었고 그 외 파일은 변경하지 않았다.
- Verify에 명시된 테스트/확인이 실제로 통과한다.
- Depends On에 있는 모든 선행 Task가 완료된 상태에서 시작했다.
- 새로운 Component/Data/API를 직접 만들지 않고 기존 산출물만 조립했다.
- Loading(사진·Timeline 스켈레톤)·Error(이미지 로드 실패 대체 박스) 상태가 실제로 조립되어 있다.

## Forbidden

- Expected Files 목록 밖의 파일을 생성·수정하지 않는다.
- Airbnb 등 참고 디자인의 상표 요소(로고 · 워드마크 · 브랜드 컬러)를 재현하지 않는다.
- 구매 · 예약 · 결제 UI, 실시간 항공권 · 호텔 가격, 별점 · 리뷰, 광고 배너를 추가하지 않는다.
- EC2 · AWS 인프라, 자동 Merge Runner를 구성하지 않는다.
- `docs/PROJECT_SCOPE.md`에서 EXCLUDED로 분류된 기능(콘텐츠 CMS, 미디어 업로드 워크플로, 감사 로그, 실시간 채팅 · 위치공유, rate limit 미들웨어 등)을 이 Task 범위에서 구현하지 않는다.
- 이 Task 안에서 새로운 Component/Data/API를 직접 구현하지 않는다 — 이미 완료된 하위 Task 결과물만 조립한다.

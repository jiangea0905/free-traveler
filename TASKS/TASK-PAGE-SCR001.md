# PAGE-SCR001 — SCR-001 메인 Page Owner

**Category:** PAGE_OWNER | **Implementation Status:** IMPLEMENT | **Priority:** P0 | **Seq:** 28

## Context

SCR-001 메인 Page Owner. SCR-001(`/`)의 최종 Route Page를 조립하는 Page Owner Task이며, Depends On에 명시된 Component/Data/API/Shared Task의 산출물을 가져와 `src/app/page.tsx`에 배치한다.

## Project Scope

Implementation Status: **IMPLEMENT** (`docs/PROJECT_SCOPE.md` 기준). 축소나 대체 없이 전체 범위를 구현한다. Requirement Ref: REQ-FUNC-001~010, 046~054, 064~070(공통, 조립).

## Requirement Ref

REQ-FUNC-001~010, 046~054, 064~070(공통, 조립)

## Screen / Route / Page Entry

- Screen: SCR-001
- Route: `/`
- Page Entry: `src/app/page.tsx`

## Design Ref

`design-reference/D-001/DESIGN.md` §Page Section 최대 폭과 상하 여백, §Hero 높이와 다음 Section 노출 규칙, §화면별 Section 순서와 최소 콘텐츠 수

## Depends On

COMP-SCR001-SEARCH-DESTINATIONS, COMP-SCR001-SAFETY, COMP-SCR001-DESTINATION-DRAWER, COMP-SCR001-MATES-PROFILE-TEASER, SHARED-HEADER-FOOTER, DATA-DESTINATIONS, DATA-SAFETY

## Expected Files

`src/app/page.tsx`(**수정** — 기존 Next.js 스타터 콘텐츠 전면 교체, 신규 생성 아님)

이 Task는 위 Expected Files 목록에 있는 파일만 생성 · 수정한다. 목록 밖의 파일을 건드리지 않는다.

## Functional AC

Header → ①검색 Hero → ②국내 여행지 **6개** → ③해외 여행지 **6개** → ④여행 동기 **6개** Chip → ⑤국가별 주의사항 **6개** → ⑥최근 동행글 **3개** 또는 완성형 Empty State → ⑦free_traveler 소개 → Footer. 각 Section 데이터 출처: ②③은 `DATA-DESTINATIONS`, ⑤는 `DATA-SAFETY`, ⑥은 `API-MATES`, ⑦은 `DATA-REPRESENTATIVE`

Functional AC(상태 — `design-reference/UI_CONTRACT.md` SCR-001 §상태 그대로 조립): **Loading**은 Card Grid 스켈레톤(최종 Card/Grid와 동일한 radius·열 수)으로 표시하고 전체 페이지 스피너로 대체하지 않는다. **Empty**는 필터 결과 0건 시 조건 완화 안내+초기화 버튼, 최근 동행글 0건 시 완성형 Empty State로 표시한다. **Error**는 Section별 로드 실패 배너+다시 시도 액션으로 표시한다(Unauthorized는 전체 공개이므로 해당 없음). / `src/app/page.tsx`에 create-next-app 기본 템플릿(Next.js 로고, "Get started by editing" 문구, 기본 카드 링크)이 **하나도 남아있지 않아야 한다** — Page Owner 완료 조건 / 위 4개 Component Task가 모두 완료되어야 조립을 시작한다(임의 Placeholder로 먼저 조립하지 않는다)

## Visual AC

Desktop 콘텐츠 최대 폭 1200~1280px, Section 상하 여백 64~96px(Mobile 40~64px), Card 1열(Mobile)/3~4열(Desktop) 반응형 밀도 준수

## Security/Privacy AC

없음(조립 계층)

## Test Cases

- Header → ①검색 Hero → ②국내 여행지 6개 → ③해외 여행지 6개 → ④여행 동기 6개 Chip → ⑤국가별 주의사항 6개 → ⑥최근 동행글 3개 또는 완성형 Empty State → ⑦free_traveler 소개 → Footer
- 각 Section 데이터 출처: ②③은 `DATA-DESTINATIONS`, ⑤는 `DATA-SAFETY`, ⑥은 `API-MATES`, ⑦은 `DATA-REPRESENTATIVE`
- `src/app/page.tsx`에 create-next-app 기본 템플릿(Next.js 로고, "Get started by editing" 문구, 기본 카드 링크)이 하나도 남아있지 않아야 한다 — Page Owner 완료 조건
- 위 4개 Component Task가 모두 완료되어야 조립을 시작한다(임의 Placeholder로 먼저 조립하지 않는다)

## Verify

E2E-PUBLIC-SMOKE, 수동 브라우저 확인(§Release Check)

## Definition of Done

- Functional AC, Visual AC, Security/Privacy AC 항목이 모두 충족된다.
- Expected Files에 명시된 파일만 생성 · 수정되었고 그 외 파일은 변경하지 않았다.
- Verify에 명시된 테스트/확인이 실제로 통과한다.
- Depends On에 있는 모든 선행 Task가 완료된 상태에서 시작했다.
- 새로운 Component/Data/API를 직접 만들지 않고 기존 산출물만 조립했다.
- `src/app/page.tsx`에 Next.js 기본 스타터 콘텐츠(로고, "Get started by editing" 등)가 전혀 남아있지 않다.
- Loading(Card Grid 스켈레톤)·Empty(조건 완화 안내+초기화 버튼, 완성형 Empty State)·Error(Section별 다시 시도 배너) 상태가 실제로 조립되어 있다.

## Forbidden

- Expected Files 목록 밖의 파일을 생성·수정하지 않는다.
- Airbnb 등 참고 디자인의 상표 요소(로고 · 워드마크 · 브랜드 컬러)를 재현하지 않는다.
- 구매 · 예약 · 결제 UI, 실시간 항공권 · 호텔 가격, 별점 · 리뷰, 광고 배너를 추가하지 않는다.
- EC2 · AWS 인프라, 자동 Merge Runner를 구성하지 않는다.
- `docs/PROJECT_SCOPE.md`에서 EXCLUDED로 분류된 기능(콘텐츠 CMS, 미디어 업로드 워크플로, 감사 로그, 실시간 채팅 · 위치공유, rate limit 미들웨어 등)을 이 Task 범위에서 구현하지 않는다.
- 이 Task 안에서 새로운 Component/Data/API를 직접 구현하지 않는다 — 이미 완료된 하위 Task 결과물만 조립한다.

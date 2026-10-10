# PAGE-SCR004 — SCR-004 동행 조회 Page Owner

**Category:** PAGE_OWNER | **Implementation Status:** IMPLEMENT | **Priority:** P0 | **Seq:** 43

## Context

SCR-004 동행 조회 Page Owner. SCR-004(`/mates`)의 최종 Route Page를 조립하는 Page Owner Task이며, Depends On에 명시된 Component/Data/API/Shared Task의 산출물을 가져와 `src/app/mates/page.tsx`에 배치한다.

## Project Scope

Implementation Status: **IMPLEMENT** (`docs/PROJECT_SCOPE.md` 기준). 축소나 대체 없이 전체 범위를 구현한다. Requirement Ref: REQ-FUNC-030, 033~040(조립).

## Requirement Ref

REQ-FUNC-030, 033~040(조립)

## Screen / Route / Page Entry

- Screen: SCR-004
- Route: `/mates`
- Page Entry: `src/app/mates/page.tsx`

## Design Ref

`design-reference/D-001/DESIGN.md` §Mate Post Card, §Page Section 최대 폭과 상하 여백

## Depends On

COMP-SCR004-FILTER, COMP-SCR004-LIST, COMP-SCR004-DETAIL, COMP-SCR004-APPLY, COMP-SCR004-REPORT, COMP-SCR004-BLOCK, SHARED-HEADER-FOOTER, SHARED-NOTIFICATION-TOAST

## Expected Files

`src/app/mates/page.tsx`(신규)

이 Task는 위 Expected Files 목록에 있는 파일만 생성 · 수정한다. 목록 밖의 파일을 건드리지 않는다.

## Functional AC

Header → ①Intro+작성 CTA → ②Filter+결과 요약(`API-MATES`) → ③동행글 목록(`API-MATES`, 최대 8) → ④목록+상세 분할(Desktop)/Drawer(Mobile) → ⑤신청 방법 3단계 → ⑥안전·신고·차단 안내+CTA → Footer

Functional AC(상태 — `design-reference/UI_CONTRACT.md` SCR-004 §상태 그대로 조립): **Loading**은 목록/상세 스켈레톤으로 표시한다. **Empty**는 조건에 맞는 글이 없을 때 완성형 Empty State(안내 문장+필터 초기화+작성 CTA+이용 방법)로 표시한다. **Error**는 신청 실패·중복 요청·네트워크 오류를 인라인 오류로 표시한다. **Unauthorized**는 참가 요청/작성 시도 시 로그인·성인 확인 유도로 처리한다.

## Visual AC

Desktop 최대 폭 1200~1280px, 목록·필터·상세·참가·신고·차단이 각각 별도 컴포넌트로 명확히 분리되어 있음(§Component 참고)

## Security/Privacy AC

연락처 비노출·차단 관계 비노출이 조립 이후에도 유지되는지 재확인

## Test Cases

- Header → ①Intro+작성 CTA → ②Filter+결과 요약(`API-MATES`) → ③동행글 목록(`API-MATES`, 최대 8) → ④목록+상세 분할(Desktop)/Drawer(Mobile) → ⑤신청 방법 3단계 → ⑥안전·신고·차단 안내+CTA → Footer

## Verify

E2E-MATE-AUTH

## Definition of Done

- Functional AC, Visual AC, Security/Privacy AC 항목이 모두 충족된다.
- Expected Files에 명시된 파일만 생성 · 수정되었고 그 외 파일은 변경하지 않았다.
- Verify에 명시된 테스트/확인이 실제로 통과한다.
- Depends On에 있는 모든 선행 Task가 완료된 상태에서 시작했다.
- 새로운 Component/Data/API를 직접 만들지 않고 기존 산출물만 조립했다.
- Loading(목록/상세 스켈레톤)·Empty(완성형 Empty State)·Error(신청 실패/중복/네트워크 오류)·Unauthorized(로그인·성인 확인 유도) 상태가 실제로 조립되어 있다.

## Forbidden

- Expected Files 목록 밖의 파일을 생성·수정하지 않는다.
- Airbnb 등 참고 디자인의 상표 요소(로고 · 워드마크 · 브랜드 컬러)를 재현하지 않는다.
- 구매 · 예약 · 결제 UI, 실시간 항공권 · 호텔 가격, 별점 · 리뷰, 광고 배너를 추가하지 않는다.
- EC2 · AWS 인프라, 자동 Merge Runner를 구성하지 않는다.
- `docs/PROJECT_SCOPE.md`에서 EXCLUDED로 분류된 기능(콘텐츠 CMS, 미디어 업로드 워크플로, 감사 로그, 실시간 채팅 · 위치공유, rate limit 미들웨어 등)을 이 Task 범위에서 구현하지 않는다.
- 이 Task 안에서 새로운 Component/Data/API를 직접 구현하지 않는다 — 이미 완료된 하위 Task 결과물만 조립한다.

# PAGE-SCR003 — SCR-003 통합 여행 준비 Page Owner

**Category:** PAGE_OWNER | **Implementation Status:** IMPLEMENT | **Priority:** P0 | **Seq:** 36

## Context

SCR-003 통합 여행 준비 Page Owner. SCR-003(`/travel-tools`)의 최종 Route Page를 조립하는 Page Owner Task이며, Depends On에 명시된 Component/Data/API/Shared Task의 산출물을 가져와 `src/app/travel-tools/page.tsx`에 배치한다.

## Project Scope

Implementation Status: **IMPLEMENT** (`docs/PROJECT_SCOPE.md` 기준). 축소나 대체 없이 전체 범위를 구현한다. Requirement Ref: REQ-FUNC-011~026, 031, 032, 080(조립).

## Requirement Ref

REQ-FUNC-011~026, 031, 032, 080(조립)

## Screen / Route / Page Entry

- Screen: SCR-003
- Route: `/travel-tools`
- Page Entry: `src/app/travel-tools/page.tsx`

## Design Ref

`design-reference/D-001/DESIGN.md` §Form · Tabs, §Page Section 최대 폭과 상하 여백

## Depends On

COMP-SCR003-FLIGHT-FORM, COMP-SCR003-HOTEL-FORM, COMP-SCR003-MATE-COMPOSER, SHARED-HEADER-FOOTER, API-AUTH

## Expected Files

`src/app/travel-tools/page.tsx`(신규)

이 Task는 위 Expected Files 목록에 있는 파일만 생성 · 수정한다. 목록 밖의 파일을 건드리지 않는다.

## Functional AC

Header → ①Intro(목적+3단계 요약) → ②탭(항공편/숙소/동행 구하기, **실제 조립·전환 동작**) → ③여행정보 Form(탭별) → ④입력 요약·외부 이동 → ⑤찾기 Tip 3개+비전달 고지 → ⑥동행 작성 또는 로그인 안내·안전 안내 → Footer. 세 탭은 각자 독립된 입력/검증/완료 상태를 가진다(탭 전환이 다른 탭 데이터를 지우지 않음)

Functional AC(상태 — `design-reference/UI_CONTRACT.md` SCR-003 §상태 그대로 조립, 탭별 독립): 항공편/숙소 탭은 **Loading**(외부 이동 처리 중)·**Success**(요약+새 탭 오픈)·**Error**(날짜 검증 오류, 외부 URL 미설정 오류)를 조립한다(Empty/Unauthorized 해당 없음). 동행 구하기 탭은 **Loading**(제출 처리 중)·**Success**(작성 완료 후 이동)·**Error**(연락처 패턴 감지·필수값 오류)·**Unauthorized**(비로그인/미성년 → 로그인 유도 배너)를 조립한다.

## Visual AC

Desktop 최대 폭 1200~1280px, Mobile은 탭을 풀폭 세그먼트로

## Security/Privacy AC

항공·숙소 입력값이 어떤 경로로도 서버/DB/외부 URL에 전달되지 않음(SHARED-EXTERNAL-LINKOUT 재사용으로 이중 보장)

## Test Cases

- Header → ①Intro(목적+3단계 요약) → ②탭(항공편/숙소/동행 구하기, 실제 조립·전환 동작) → ③여행정보 Form(탭별) → ④입력 요약·외부 이동 → ⑤찾기 Tip 3개+비전달 고지 → ⑥동행 작성 또는 로그인 안내·안전 안내 → Footer
- 세 탭은 각자 독립된 입력/검증/완료 상태를 가진다(탭 전환이 다른 탭 데이터를 지우지 않음)

## Verify

E2E-TRAVEL-TOOLS

## Definition of Done

- Functional AC, Visual AC, Security/Privacy AC 항목이 모두 충족된다.
- Expected Files에 명시된 파일만 생성 · 수정되었고 그 외 파일은 변경하지 않았다.
- Verify에 명시된 테스트/확인이 실제로 통과한다.
- Depends On에 있는 모든 선행 Task가 완료된 상태에서 시작했다.
- 새로운 Component/Data/API를 직접 만들지 않고 기존 산출물만 조립했다.
- 항공편 · 숙소 · 동행 구하기 세 탭이 실제로 조립되어 서로 독립된 상태로 전환 동작한다.
- 탭별 Loading·Error(항공편/숙소) 및 Loading·Error·Unauthorized(동행 구하기) 상태가 실제로 조립되어 있다.

## Forbidden

- Expected Files 목록 밖의 파일을 생성·수정하지 않는다.
- Airbnb 등 참고 디자인의 상표 요소(로고 · 워드마크 · 브랜드 컬러)를 재현하지 않는다.
- 구매 · 예약 · 결제 UI, 실시간 항공권 · 호텔 가격, 별점 · 리뷰, 광고 배너를 추가하지 않는다.
- EC2 · AWS 인프라, 자동 Merge Runner를 구성하지 않는다.
- `docs/PROJECT_SCOPE.md`에서 EXCLUDED로 분류된 기능(콘텐츠 CMS, 미디어 업로드 워크플로, 감사 로그, 실시간 채팅 · 위치공유, rate limit 미들웨어 등)을 이 Task 범위에서 구현하지 않는다.
- 입력값(국가 · 지역 · 날짜)을 서버, DB, 외부 URL 쿼리 파라미터로 전송하지 않는다.
- 이 Task 안에서 새로운 Component/Data/API를 직접 구현하지 않는다 — 이미 완료된 하위 Task 결과물만 조립한다.

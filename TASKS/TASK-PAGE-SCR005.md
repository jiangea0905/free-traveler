# PAGE-SCR005 — SCR-005 계정·관리 Page Owner

**Category:** PAGE_OWNER | **Implementation Status:** IMPLEMENT | **Priority:** P0 | **Seq:** 48

## Context

SCR-005 계정·관리 Page Owner. SCR-005(`/account`)의 최종 Route Page를 조립하는 Page Owner Task이며, Depends On에 명시된 Component/Data/API/Shared Task의 산출물을 가져와 `src/app/account/page.tsx`에 배치한다.

## Project Scope

Implementation Status: **IMPLEMENT** (`docs/PROJECT_SCOPE.md` 기준). 축소나 대체 없이 전체 범위를 구현한다. Requirement Ref: REQ-FUNC-027~029, 036, 038, 041, 042, 077(조립).

## Requirement Ref

REQ-FUNC-027~029, 036, 038, 041, 042, 077(조립)

## Screen / Route / Page Entry

- Screen: SCR-005
- Route: `/account`
- Page Entry: `src/app/account/page.tsx`

## Design Ref

`design-reference/D-001/DESIGN.md` §Do / Do Not(관리자 Dashboard 금지), §완성형 Empty State와 Placeholder 문구 금지 규칙

## Depends On

COMP-SCR005-AUTH, COMP-SCR005-PROFILE, COMP-SCR005-MY-ACTIVITY, COMP-SCR005-ADMIN, SHARED-HEADER-FOOTER, API-AUTH

## Expected Files

`src/app/account/page.tsx`(신규)

이 Task는 위 Expected Files 목록에 있는 파일만 생성 · 수정한다. 목록 밖의 파일을 건드리지 않는다.

## Functional AC

Guest → Intro/로그인·가입·재설정(`API-AUTH`)/기능 안내/보안 안내. Member → 탭[프로필(`API-AUTH`), 내 활동(`API-MATES`/`API-APPLICATIONS`/`API-BLOCKS-REPORTS`/localStorage)]. Admin → +탭[관리자(`API-ADMIN`)]. **역할에 없는 관리 영역은 렌더링하지 않는다**(DOM에 존재하지 않아야 함, CSS로 숨기기만 하는 방식 금지)

Functional AC(상태 — `design-reference/UI_CONTRACT.md` SCR-005 §상태 그대로 조립, 역할별 독립): Guest는 **Loading**(로그인 처리 중)·**Success**(로그인 성공 전환)·**Error**(로그인 실패·이메일 중복)를 조립한다. Member 프로필은 **Loading**·**Success**·**Error**(수정 실패)를 조립한다. Member 내 활동은 **Loading**·**Success**·**Empty**(블록별 완성형 Empty State+CTA)·**Error**(로드/처리 실패)·**Unauthorized**(비회원 직접 접근 → Guest 뷰로 대체)를 조립한다. Admin은 **Loading**·**Success**·**Empty**(처리할 신고 없음)·**Error**(상태 변경 실패, 잘못된 URL 저장 차단)·**Unauthorized**(권한 없음 → 관리자 탭 미노출, 직접 접근 시 권한 없음 안내)를 조립한다.

## Visual AC

큰 빈 영역·Placeholder 문구 금지, 4블록 각각 완성형 Empty State

## Security/Privacy AC

비로그인 상태에서 Member/Admin 영역 접근 시 Guest 뷰로 대체(서버 검증 포함)

## Test Cases

- Guest → Intro/로그인·가입·재설정(`API-AUTH`)/기능 안내/보안 안내
- Member → 탭[프로필(`API-AUTH`), 내 활동(`API-MATES`/`API-APPLICATIONS`/`API-BLOCKS-REPORTS`/localStorage)]
- Admin → +탭[관리자(`API-ADMIN`)]
- 역할에 없는 관리 영역은 렌더링하지 않는다(DOM에 존재하지 않아야 함, CSS로 숨기기만 하는 방식 금지)

## Verify

E2E-MATE-AUTH

## Definition of Done

- Functional AC, Visual AC, Security/Privacy AC 항목이 모두 충족된다.
- Expected Files에 명시된 파일만 생성 · 수정되었고 그 외 파일은 변경하지 않았다.
- Verify에 명시된 테스트/확인이 실제로 통과한다.
- Depends On에 있는 모든 선행 Task가 완료된 상태에서 시작했다.
- 새로운 Component/Data/API를 직접 만들지 않고 기존 산출물만 조립했다.
- Guest/Member/Admin 역할별 영역이 실제로 조립되며, 역할에 없는 영역은 DOM에 렌더링되지 않는다.
- 역할별 Loading·Empty·Error·Unauthorized 상태(Guest/Member 프로필/Member 내 활동/Admin 각각)가 실제로 조립되어 있다.

## Forbidden

- Expected Files 목록 밖의 파일을 생성·수정하지 않는다.
- Airbnb 등 참고 디자인의 상표 요소(로고 · 워드마크 · 브랜드 컬러)를 재현하지 않는다.
- 구매 · 예약 · 결제 UI, 실시간 항공권 · 호텔 가격, 별점 · 리뷰, 광고 배너를 추가하지 않는다.
- EC2 · AWS 인프라, 자동 Merge Runner를 구성하지 않는다.
- `docs/PROJECT_SCOPE.md`에서 EXCLUDED로 분류된 기능(콘텐츠 CMS, 미디어 업로드 워크플로, 감사 로그, 실시간 채팅 · 위치공유, rate limit 미들웨어 등)을 이 Task 범위에서 구현하지 않는다.
- 관리자 영역에 차트 · KPI · 통계 Dashboard를 추가하지 않는다.
- 이 Task 안에서 새로운 Component/Data/API를 직접 구현하지 않는다 — 이미 완료된 하위 Task 결과물만 조립한다.

# COMP-SCR005-ADMIN — 관리자(신고 상태·외부 URL)

**Category:** COMPONENT | **Implementation Status:** IMPLEMENT(축소) | **Priority:** P0 | **Seq:** 47

## Context

관리자(신고 상태·외부 URL). SCR-005 화면의 한 Section 또는 기능을 담당하는 재사용 가능한 UI Component이며, 관련 Data/API Task의 데이터를 소비해 렌더링한다.

## Project Scope

Implementation Status: **IMPLEMENT(축소)** (`docs/PROJECT_SCOPE.md` 기준). 범위(축소, PROJECT_SCOPE 근거): 신고 목록+상태 변경, 외부 URL(HTTPS만) 설정만. 차트·KPI·Dashboard 금지. Requirement Ref: REQ-FUNC-041, 042, 077.

## Requirement Ref

REQ-FUNC-041, 042, 077

## Screen / Route / Page Entry

- Screen: SCR-005
- Route: `/account`
- Page Entry: N/A

## Design Ref

`design-reference/D-001/DESIGN.md` §Do / Do Not(관리자 Dashboard 금지)

## Depends On

API-ADMIN, API-BLOCKS-REPORTS

## Expected Files

`src/components/account/AdminPanel.tsx`(신규)

이 Task는 위 Expected Files 목록에 있는 파일만 생성 · 수정한다. 목록 밖의 파일을 건드리지 않는다.

## Functional AC

**범위(축소, PROJECT_SCOPE 근거): 신고 목록+상태 변경, 외부 URL(HTTPS만) 설정만. 차트·KPI·Dashboard 금지.**

## Visual AC

목록+Select+저장 버튼 형태, 통계 위젯 없음

## Security/Privacy AC

Admin 역할만 렌더링(역할 없으면 탭 자체 미노출)

## Test Cases

- 범위(축소, PROJECT_SCOPE 근거): 신고 목록+상태 변경, 외부 URL(HTTPS만) 설정만
- 차트·KPI·Dashboard 금지

## Verify

E2E-MATE-AUTH(관리자 경로)

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
- 차트 · KPI · 통계 Dashboard를 추가하지 않는다. 신고 상태 변경과 외부 URL 설정 외 기능을 추가하지 않는다.

# COMP-SCR002-TIMELINE-COUNTRIES — 여행 Timeline+방문 국가

**Category:** COMPONENT | **Implementation Status:** IMPLEMENT | **Priority:** P1 | **Seq:** 30

## Context

여행 Timeline+방문 국가. SCR-002 화면의 한 Section 또는 기능을 담당하는 재사용 가능한 UI Component이며, 관련 Data/API Task의 데이터를 소비해 렌더링한다.

## Project Scope

Implementation Status: **IMPLEMENT** (`docs/PROJECT_SCOPE.md` 기준). 축소나 대체 없이 전체 범위를 구현한다. Requirement Ref: REQ-FUNC-059,060.

## Requirement Ref

REQ-FUNC-059,060

## Screen / Route / Page Entry

- Screen: SCR-002
- Route: `/about`
- Page Entry: N/A

## Design Ref

`design-reference/D-001/DESIGN.md` §Section별 제목 · 설명 · 본문 · CTA 계층과 시각적 리듬

## Depends On

DATA-REPRESENTATIVE

## Expected Files

`src/components/about/Timeline.tsx`(신규), `src/components/about/VisitedCountries.tsx`(신규)

이 Task는 위 Expected Files 목록에 있는 파일만 생성 · 수정한다. 목록 밖의 파일을 건드리지 않는다.

## Functional AC

Timeline **6개 이상** 시점(연도·장소·요약), 방문 국가 **30개**를 권역별(아시아/유럽/북미/오세아니아 등) Chip으로 그룹

## Visual AC

세로형 Timeline, 권역별 Chip 목록 — 같은 카드 패턴 반복 금지(교차 배치)

## Security/Privacy AC

해당 없음

## Test Cases

- Timeline 6개 이상 시점(연도·장소·요약), 방문 국가 30개를 권역별(아시아/유럽/북미/오세아니아 등) Chip으로 그룹

## Verify

데이터 수량 검증 테스트(CI-DATA-VALIDATION)

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

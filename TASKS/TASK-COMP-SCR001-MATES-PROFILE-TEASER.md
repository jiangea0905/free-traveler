# COMP-SCR001-MATES-PROFILE-TEASER — 최근 동행글+free_traveler 요약

**Category:** COMPONENT | **Implementation Status:** IMPLEMENT | **Priority:** P1 | **Seq:** 27

## Context

최근 동행글+free_traveler 요약. SCR-001 화면의 한 Section 또는 기능을 담당하는 재사용 가능한 UI Component이며, 관련 Data/API Task의 데이터를 소비해 렌더링한다.

## Project Scope

Implementation Status: **IMPLEMENT** (`docs/PROJECT_SCOPE.md` 기준). 축소나 대체 없이 전체 범위를 구현한다. Requirement Ref: (표시 전용 — API-MATES/DATA-REPRESENTATIVE 재사용).

## Requirement Ref

(표시 전용 — API-MATES/DATA-REPRESENTATIVE 재사용)

## Screen / Route / Page Entry

- Screen: SCR-001
- Route: `/`
- Page Entry: N/A

## Design Ref

`design-reference/D-001/DESIGN.md` §Mate Post Card, §완성형 Empty State와 Placeholder 문구 금지 규칙

## Depends On

API-MATES, DATA-REPRESENTATIVE

## Expected Files

`src/components/home/RecentMates.tsx`(신규), `src/components/home/ProfileSummary.tsx`(신규)

이 Task는 위 Expected Files 목록에 있는 파일만 생성 · 수정한다. 목록 밖의 파일을 건드리지 않는다.

## Functional AC

최근 모집중 글 3개 또는 완성형 Empty State(설명 문장+이용 방법+작성 CTA), free_traveler `50+`/`30+` 수치는 `DATA-REPRESENTATIVE`와 100% 일치

## Visual AC

큰 빈 영역·Placeholder 문구 금지, Empty State에도 시각적으로 완성된 카드 형태 유지

## Security/Privacy AC

동행글 카드에 연락처 미노출(API-MATES 응답 신뢰)

## Test Cases

- 최근 모집중 글 3개 또는 완성형 Empty State(설명 문장+이용 방법+작성 CTA), free_traveler `50+`/`30+` 수치는 `DATA-REPRESENTATIVE`와 100% 일치

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

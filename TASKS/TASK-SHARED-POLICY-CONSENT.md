# SHARED-POLICY-CONSENT — 정책 페이지+안전수칙 동의 기록

**Category:** SHARED | **Implementation Status:** IMPLEMENT | **Priority:** P1 | **Seq:** 23

## Context

정책 페이지+안전수칙 동의 기록. 여러 Screen이 공통으로 재사용하는 유틸 또는 컴포넌트다.

## Project Scope

Implementation Status: **IMPLEMENT** (`docs/PROJECT_SCOPE.md` 기준). 축소나 대체 없이 전체 범위를 구현한다. Requirement Ref: REQ-FUNC-080.

## Requirement Ref

REQ-FUNC-080

## Screen / Route / Page Entry

- Screen: 전역
- Route: `/terms`, `/privacy`, `/safety-guideline`(기술 Route, 정책 콘텐츠)
- Page Entry: `src/app/terms/page.tsx` 등

## Design Ref

`design-reference/D-001/DESIGN.md` §Header · Footer(정책 링크 위치)

## Depends On

없음

## Expected Files

`src/app/terms/page.tsx`(신규), `src/app/privacy/page.tsx`(신규), `src/app/safety-guideline/page.tsx`(신규), `src/lib/consent.ts`(신규)

이 Task는 위 Expected Files 목록에 있는 파일만 생성 · 수정한다. 목록 밖의 파일을 건드리지 않는다.

## Functional AC

이용약관/개인정보처리방침/동행 안전수칙/콘텐츠 면책 페이지 제공, 동행글 작성 시 정책 버전+동의 시각 저장

## Visual AC

해당 없음(정적 텍스트 페이지)

## Security/Privacy AC

동의 기록은 DB `mate_post`의 감사 필드가 아닌 최소 컬럼(정책 버전, 시각)만 저장

## Test Cases

- 이용약관/개인정보처리방침/동행 안전수칙/콘텐츠 면책 페이지 제공, 동행글 작성 시 정책 버전+동의 시각 저장

## Verify

E2E-MATE-AUTH(동의 없이 제출 차단 확인)

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

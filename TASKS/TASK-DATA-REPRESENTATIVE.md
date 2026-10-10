# DATA-REPRESENTATIVE — free_traveler 대표 프로필 정적 데이터

**Category:** DATA | **Implementation Status:** IMPLEMENT | **Priority:** P0 | **Seq:** 8

## Context

free_traveler 대표 프로필 정적 데이터. `docs/PROJECT_SCOPE.md`가 지정한 대로 DB 테이블이 아닌 `src/data` 정적 데이터로 콘텐츠를 관리한다.

## Project Scope

Implementation Status: **IMPLEMENT** (`docs/PROJECT_SCOPE.md` 기준). 구현 방법(지정): 정적 데이터. Requirement Ref: REQ-FUNC-057, 058, 059, 060, 061.

## Requirement Ref

REQ-FUNC-057, 058, 059, 060, 061

## Screen / Route / Page Entry

- Screen: N/A
- Route: N/A
- Page Entry: N/A

## Design Ref

해당 없음(비-UI Task)

## Depends On

없음

## Expected Files

`src/data/representative.ts`(신규)

이 Task는 위 Expected Files 목록에 있는 파일만 생성 · 수정한다. 목록 밖의 파일을 건드리지 않는다.

## Functional AC

**구현 방법(지정): 정적 데이터.** `50+ Trips`/`30+ Countries` 라벨, 소개문, 철학, `visited_countries`(30개 이상, 권역 라벨 포함), `timeline`(6개 이상, 연도/장소/요약), `hero_media` alt/출처, 문의·SNS 링크(선택)

## Visual AC

해당 없음(데이터 레이어, 렌더링은 §SCR-002 Component)

## Security/Privacy AC

해당 없음

## Test Cases

- 구현 방법(지정): 정적 데이터
- `50+ Trips`/`30+ Countries` 라벨, 소개문, 철학, `visited_countries`(30개 이상, 권역 라벨 포함), `timeline`(6개 이상, 연도/장소/요약), `hero_media` alt/출처, 문의·SNS 링크(선택)

## Verify

CI-DATA-VALIDATION

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

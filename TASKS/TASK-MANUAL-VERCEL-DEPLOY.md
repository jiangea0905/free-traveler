# MANUAL-VERCEL-DEPLOY — Vercel 배포·HTTPS·비용 확인

**Category:** MANUAL_CHECK | **Implementation Status:** IMPLEMENT | **Priority:** P0 | **Seq:** 51

## Context

Vercel 배포·HTTPS·비용 확인. 자동화할 수 없어 사람이 직접 확인해야 하는 배포·설정 점검이다.

## Project Scope

Implementation Status: **IMPLEMENT** (`docs/PROJECT_SCOPE.md` 기준). 축소나 대체 없이 전체 범위를 구현한다. Requirement Ref: REQ-NF-012, REQ-NF-034.

## Requirement Ref

REQ-NF-012, REQ-NF-034

## Screen / Route / Page Entry

- Screen: N/A
- Route: N/A
- Page Entry: N/A

## Design Ref

해당 없음(비-UI Task)

## Depends On

PAGE-SCR001, PAGE-SCR002, PAGE-SCR003, PAGE-SCR004, PAGE-SCR005, CI-LINT-BUILD-TEST

## Expected Files

없음(배포 콘솔 확인)

이 Task는 위 Expected Files 목록에 있는 파일만 생성 · 수정한다. 목록 밖의 파일을 건드리지 않는다.

## Functional AC

배포 URL이 HTTPS로 서비스되는지, 무료/저비용 티어로 월 비용 목표(콘텐츠 인건비 제외 10만원 이하) 충족하는지 사람이 콘솔에서 확인

## Visual AC

해당 없음

## Security/Privacy AC

비밀키가 클라이언트 번들에 노출되지 않았는지 빌드 산출물 검색으로 확인

## Test Cases

- 배포 URL이 HTTPS로 서비스되는지, 무료/저비용 티어로 월 비용 목표(콘텐츠 인건비 제외 10만원 이하) 충족하는지 사람이 콘솔에서 확인

## Verify

사람이 Vercel 대시보드에서 확인 후 결과 기록

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

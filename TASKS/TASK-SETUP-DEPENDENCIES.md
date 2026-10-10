# SETUP-DEPENDENCIES — 의존성 추가(Supabase, zod, Playwright)

**Category:** SETUP | **Implementation Status:** IMPLEMENT | **Priority:** P0 | **Seq:** 1

## Context

의존성 추가(Supabase, zod, Playwright). 이후 모든 Task가 의존하는 프로젝트 초기 설정 작업이다.

## Project Scope

Implementation Status: **IMPLEMENT** (`docs/PROJECT_SCOPE.md` 기준). 축소나 대체 없이 전체 범위를 구현한다. Requirement Ref: NF-031.

## Requirement Ref

NF-031

## Screen / Route / Page Entry

- Screen: N/A
- Route: N/A
- Page Entry: N/A

## Design Ref

해당 없음(비-UI Task)

## Depends On

없음

## Expected Files

`package.json`(수정 — `@supabase/supabase-js`, `@supabase/ssr`, `zod`, `@playwright/test` 추가)

이 Task는 위 Expected Files 목록에 있는 파일만 생성 · 수정한다. 목록 밖의 파일을 건드리지 않는다.

## Functional AC

package.json에 Supabase 클라이언트, 입력 검증(zod), Playwright(Chromium만)가 devDependencies/dependencies로 추가되고 npm install이 성공한다

## Visual AC

해당 없음

## Security/Privacy AC

추가되는 패키지 버전은 고정(caret 범위) 표기, 알려진 취약점이 있는 버전을 고정하지 않는다

## Test Cases

- package.json에 Supabase 클라이언트, 입력 검증(zod), Playwright(Chromium만)가 devDependencies/dependencies로 추가되고 npm install이 성공한다

## Verify

npm install 성공, npm run build 성공(코드 없이도 스캐폴드 빌드가 깨지지 않음)

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

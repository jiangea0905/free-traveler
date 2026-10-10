# CLAUDE.md — Free Traveler

이 파일은 `traveler/app`(실제 개발 루트, `docs/DECISION_LOG.md` DEC-001)에서 작업하는 모든 Agent가 지켜야 할 규칙을 담은 단일 정본이다. 다른 Agent 규칙 파일을 참조하지 않는다 — 필요한 규칙은 전부 이 문서 안에 직접 적혀 있다.

## Harness Marker

```
HARNESS_SCHEMA=traveler-screen-route-v1
DESIGN_PATH=design-reference/D-001/DESIGN.md
SCREEN_CONTRACT=design-reference/SCREEN_ROUTE_CONTRACT.json
PROJECT_SCOPE=docs/PROJECT_SCOPE.md
PLAYWRIGHT_ENABLED=true
PLAYWRIGHT_SCOPE=chromium-smoke
AUTO_MERGE=false
AWS_ENABLED=false
```

## 필수 규칙

1. 작업 전 `package.json`과 현재 Next.js 공식 문서를 확인한다 — 버전에 맞지 않는 API나 폐기된 패턴을 가정하지 않는다.
2. SRS 정본은 `docs/06_SRS_UIUX_REVISED.md`다. Requirement 내용이 궁금하면 이 문서를 먼저 본다.
3. Scope 분류(IMPLEMENT / IMPLEMENT(축소) / IMPLEMENT(대체) / EXCLUDED) 정본은 `docs/PROJECT_SCOPE.md`다.
4. 디자인 정본은 `design-reference/D-001/DESIGN.md`(Status: LOCKED)다. `design-reference/vendor/airbnb/DESIGN-airbnb.md`는 구조적 참고본일 뿐 정본이 아니다.
5. Screen 정본은 `design-reference/SCREEN_ROUTE_CONTRACT.json`이다. Screen ID, Route, Page Entry가 다른 문서와 어긋나면 이 JSON을 따른다.
6. `/run-wave WXX`를 표준 개발 명령으로 사용한다. 임의의 다른 방식으로 Wave 실행을 시작하지 않는다.
7. Wave 내부 Task는 `TASKS/00_TASK_LIST.md`의 Depends On 순서에 따라 **한 번에 하나만** 구현한다. 여러 Task를 동시에 건드리지 않는다.
8. 현재 진행 중인 Task의 `Expected Files` 목록 밖에 있는 파일은 수정하지 않는다.
9. Page Owner Task는 새 Component를 만들지 않고, 이미 완료된 Component/Data/API 산출물을 Page Entry(`page.tsx`)에서 **실제로 조립**한다.
10. SCR-001(`src/app/page.tsx`) 완료 시 Next.js 기본 스타터 콘텐츠(로고, "Get started by editing" 등)를 완전히 제거한다.
11. SCR-003(`/travel-tools`)은 항공·숙소·동행 세 탭을 모두 조립하고, 각 탭이 독립된 입력·검증·완료 상태를 갖도록 한다.
12. 항공·숙소 입력값(국가·지역·날짜)은 서버·DB·URL 쿼리·로그·분석 이벤트 어디로도 보내지 않는다. Client Component의 일시 상태로만 유지한다.
13. Supabase 쓰기는 Auth · 동행(모집글/참가요청/차단) · 신고 · 관리자 설정 범위로 제한한다. 여행지·안전정보·대표 프로필용 쓰기 경로를 만들지 않는다.
14. RLS를 우회하는 Client 코드(예: `service_role` 키를 브라우저로 내려보내거나, RLS 정책을 무시하는 우회 쿼리)를 작성하지 않는다.
15. Service Role Key는 Server 전용 모듈 밖으로 절대 내보내지 않는다 — Client Component, 클라이언트 번들, `NEXT_PUBLIC_*` 환경변수에 넣지 않는다.
16. 여행지 · 안전정보 · 대표 프로필은 `src/data`의 정적 TypeScript Data를 사용한다. 이 콘텐츠를 위한 DB 테이블이나 CRUD API를 만들지 않는다.
17. Prisma · 다른 ORM · AWS · EC2를 프로젝트에 추가하지 않는다.
18. Playwright는 핵심 Chromium Smoke Test만 작성한다(`E2E-PUBLIC-SMOKE`, `E2E-TRAVEL-TOOLS`, `E2E-MATE-AUTH`). 다중 브라우저 매트릭스, 시각적 회귀, 부하 테스트를 추가하지 않는다.
19. `docs/PROJECT_SCOPE.md`/`docs/UIUX_TRACEABILITY.md`에서 EXCLUDED로 분류된 기능을 임의로 구현하지 않는다.
20. `git reset --hard`, `git push --force`, `git clean -f`, 브랜치 삭제 등 destructive Git 명령을 사용자 명시적 요청 없이 임의로 사용하지 않는다.
21. 자동 PR 생성이나 자동 Merge를 실행하지 않는다(`AUTO_MERGE=false`). PR·Merge는 사람이 수동으로 수행한다.
22. 화면 단위 작업이 끝나면 사람이 Preview를 확인할 때까지 기다리고, 확인 후에만 다음 화면 Wave로 진행한다.
23. 작업 완료 시 변경한 파일 목록, 검증 결과(Unit Test/Playwright 실행 여부와 결과), 남은 제한사항(미해결 항목·수동 확인 필요 항목)을 보고한다.

## Task 완료 순서

1. **Task 읽기** — `TASKS/TASK-<ID>.md` 전체를 읽는다(Context, Project Scope, Requirement Ref, Design Ref, Depends On, Expected Files, AC, Forbidden 전부).
2. **입력 확인** — Depends On에 있는 선행 Task가 실제로 완료되었는지, 참조할 정본 문서(SRS/PROJECT_SCOPE/DESIGN/SCREEN_CONTRACT)가 최신인지 확인한다.
3. **구현** — Expected Files 안에서만 코드를 작성·수정한다.
4. **관련 포맷·Unit Test** — 해당 Task에 정의된 포맷팅/린트와 Unit Test(있다면 `UNIT-*`)를 실행한다.
5. **필요 시 Playwright** — 해당 Task가 E2E 검증 대상이면(`Verify`에 `E2E-*` 명시) Chromium Smoke 테스트를 실행한다.
6. **Diff 확인** — 변경분이 Expected Files와 정확히 일치하는지, 의도치 않은 파일 변경이 없는지 확인한다.
7. **완료 보고** — 규칙 23에 따라 변경 파일·검증 결과·남은 제한사항을 보고한다.

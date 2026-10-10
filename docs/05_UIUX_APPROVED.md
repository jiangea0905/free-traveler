# UI/UX Approved Baseline — Free Traveler

**Document ID:** UIUX-APPROVED-001
**작성일:** 2026-09-15
**기반 문서:** `docs/02_SRS_BASELINE.md`, `docs/PROJECT_SCOPE.md`, `docs/03_UI_COVERAGE_ANALYSIS.md`, `design-reference/UI_CONTRACT.md`, `design-reference/SCREEN_ROUTE_CONTRACT.json`, `design-reference/D-001/DESIGN.md`, `docs/STITCH_VALIDATION_REPORT.md`

이 문서는 승인된 5개 디자인 Screen(SCR-001~005)과 `docs/02_SRS_BASELINE.md`의 Route/Requirement 구조를 연결한 승인 기록이다. SRS의 REQ-FUNC-001~080, REQ-NF-001~034는 이 문서에서도 하나도 삭제하지 않는다(전체 배치는 `docs/UIUX_TRACEABILITY.md` 참고).

---

## 1. 승인 상태 요약

| 항목 | 값 |
|---|---|
| 승인된 Screen 수 | 5개(SCR-001~005) |
| Mobile 변형 | SCR-001, SCR-003 |
| Design 정본 | `design-reference/D-001/DESIGN.md` (Status: LOCKED) |
| Stitch 검증 결과 | `STITCH_VALIDATION_PASS` 대상 12개 검사 통과, 잔여 1건 `STITCH_VALIDATION_NEEDS_HUMAN`(§4 참고) |
| 핵심/보조 구분 | 핵심 4개(SCR-001, SCR-003, SCR-004, SCR-005) · 보조 1개(SCR-002) |

## 2. 기존 Route → 승인된 5개 Screen 통합 매핑

`02_SRS_BASELINE.md` §3.5 Page and Route Inventory에 정의된 다중 공개 Route를 5개 디자인 Screen의 탭·패널·Drawer·Modal로 통합한다. 개별 URL Route는 사라지지 않고, 화면 안의 상태(필터, 탭, 상세 패널)로 표현된다.

| SRS 원본 Route | 성격 | 통합된 Screen | 통합 방식 |
|---|---|---|---|
| `/` | 홈 | SCR-001 `/` | Hero + Card Grid |
| `/destinations` | 전체 여행지 | SCR-001 `/` | 국내/해외 탭 + 필터 |
| `/destinations/domestic` | 국내 여행지 | SCR-001 `/` | 국내 탭 상태 |
| `/destinations/overseas` | 해외 여행지 | SCR-001 `/` | 해외 탭 상태 |
| `/destinations/[slug]` | 여행지 상세 | SCR-001 `/` | 상세 Drawer(같은 화면에서 오픈) |
| `/flights` | 비행기 찾기 | SCR-003 `/travel-tools` | 항공편 탭 |
| `/hotels` | 호텔 찾기 | SCR-003 `/travel-tools` | 숙소 탭 |
| `/mates` | 동행 모집글 목록 | SCR-004 `/mates` | 목록 영역 |
| `/mates/[id]` | 동행 모집글 상세 | SCR-004 `/mates` | 목록+상세 분할(Desktop) / 상세 Drawer(Mobile) |
| `/mates/new` | 동행 모집글 작성 | SCR-003 `/travel-tools` | 동행 구하기 탭 |
| `/safety` | 국가별 주의사항 목록 | SCR-001 `/` | 국가별 주의사항 Card Grid |
| `/safety/[countryCode]` | 국가별 주의사항 상세 | SCR-001 `/` | 안전정보 Drawer(같은 화면에서 오픈) |
| `/about` | 대표 소개 | SCR-002 `/about` | 그대로 유지(보조 화면) |
| `/auth/*` | 가입·로그인·성인 확인 | SCR-005 `/account` | Guest 상태(탭 없음) |
| `/my/*` | 내 글·참가 요청·차단 | SCR-005 `/account` | Member "내 활동" 탭 |
| `/admin/*` | 콘텐츠·신고·설정 | SCR-005 `/account` | Admin "관리자" 탭(신고 상태 변경 + 외부 URL 설정만, 콘텐츠 CRUD는 EXCLUDED) |

`/travel-tools`는 요구대로 항공·숙소·동행 작성 세 탭을 모두 포함하며, `/account`는 인증(Guest)·프로필(Member)·내 활동(Member)·간단 관리자(Admin)를 역할에 따라 렌더링한다.

## 3. Screen ↔ Requirement 연결 원칙

- 화면 배치는 `docs/03_UI_COVERAGE_ANALYSIS.md`의 UI_DIRECT/UI_STATE/NON_UI/OPERATIONS 분류와 `docs/PROJECT_SCOPE.md`의 IMPLEMENT/EXCLUDED 분류를 그대로 계승한다. 이 문서는 새로운 분류를 만들지 않는다.
- Screen에 배치됐다고 해서 EXCLUDED 요구사항이 구현 범위로 복귀하지 않는다 — Screen 배치는 "화면에 나타날 자리가 있다"는 뜻이며, EXCLUDED 항목은 여전히 만들지 않는다.
- 전체 목록과 8개 열(Requirement/Implementation Status/Screen/Route/Page Entry/Task/Test/Status)의 상세 대응은 `docs/UIUX_TRACEABILITY.md`에 있다.

## 4. 알려진 미해결 사항 (거짓 기록 금지 원칙에 따른 명시)

- `STITCH_VALIDATION_REPORT.md` 기준, SCR-001과 SCR-004의 "여행 준비" 관련 CTA/내비게이션 링크가 `/travel-tools`가 아닌 `#prep`/`/prep`을 가리키는 결함이 아직 사람 확인 대기 중이다(`STITCH_VALIDATION_NEEDS_HUMAN`). 이 문서를 포함한 어떤 산출물도 두 화면을 "완전히 검증 완료(PASS)"로 기록하지 않는다.
- 2026-09-15 기준 `src/app`에는 Next.js 기본 스캐폴드(`layout.tsx`, `page.tsx`)만 존재하며, 5개 Screen 중 실제 구현이 완료된 것은 없다. 아래 §5 UI Route Contract와 `docs/UIUX_TRACEABILITY.md`의 모든 요구사항은 승인된 **디자인 계약**이지 구현 완료 기록이 아니다.

## 5. UI Route Contract (요약)

전체 계약은 `design-reference/SCREEN_ROUTE_CONTRACT.json`(schema `traveler-screen-route-v1`)이 정본이며, 이 문서는 요약만 제공한다.

| Screen ID | Route | Page Entry | 구분 | Mobile 변형 |
|---|---|---|---|---|
| SCR-001 | `/` | `src/app/page.tsx` | 핵심 | 있음 |
| SCR-002 | `/about` | `src/app/about/page.tsx` | 보조 | 없음 |
| SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | 핵심 | 있음 |
| SCR-004 | `/mates` | `src/app/mates/page.tsx` | 핵심 | 없음 |
| SCR-005 | `/account` | `src/app/account/page.tsx` | 핵심 | 없음 |

기술 Route(`/auth/callback`, `/api/*`, `not-found`, `error boundary`)는 Screen 수에 포함하지 않는다.

## 6. Release Acceptance Criteria

다음 조건을 모두 만족해야 이 UI/UX 승인 범위를 "릴리스 가능"으로 판정한다. 하나라도 미충족이면 릴리스하지 않는다.

| # | 조건 | 현재 상태 |
|---|---|---|
| 1 | SCR-001~005가 `SCREEN_ROUTE_CONTRACT.json`의 Route/Page Entry와 정확히 일치하게 구현됨(Route 중복 없음, Page Entry 중복 없음) | 미착수(계약만 존재) |
| 2 | SCR-001의 `src/app/page.tsx`가 Next.js 기본 스타터 템플릿이 아님(`starter_template_forbidden=true`) | 미착수(현재 기본 스캐폴드 상태) |
| 3 | `docs/UIUX_TRACEABILITY.md`에서 Implementation Status가 IMPLEMENT/IMPLEMENT(축소)/IMPLEMENT(대체)인 모든 REQ-FUNC/REQ-NF 항목이 실제 코드로 반영되고 Test 열에 기술된 방법으로 검증됨 | 미착수 |
| 4 | EXCLUDED로 분류된 요구사항이 화면·코드 어디에도 임의로 복원되지 않음 | 해당 없음(아직 구현 시작 전이므로 위반 없음) |
| 5 | SCR-001, SCR-004의 "여행 준비" CTA/내비게이션이 `/travel-tools`로 정확히 연결됨(`STITCH_VALIDATION_NEEDS_HUMAN` 해소) | 미해결 — 사람 확인 필요 |
| 6 | Playwright 핵심 Smoke Test(5개 화면 진입 + 항공·호텔 외부 이동 + 동행글 작성~참가 요청)가 통과함 | 미착수 |
| 7 | Header/Footer가 5개 Screen에서 동일 컴포넌트로 공유됨 | 미착수 |
| 8 | 관리자 화면(SCR-005 관리자 탭)에 차트·KPI·Dashboard가 없고 목록+상태 변경 UI로만 구성됨 | 계약상 명시됨(구현 전) |

이 표의 "현재 상태"는 문서 작성 시점 기준이며, 실제 구현이 진행되는 대로 갱신해야 한다. 구현되지 않은 항목을 "완료"로 표기하지 않는다.

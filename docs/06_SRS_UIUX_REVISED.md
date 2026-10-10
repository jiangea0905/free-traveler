# SRS UI/UX Revision — Free Traveler

**Document ID:** SRS-TRAVEL-001-UIUX-REV1
**작성일:** 2026-09-15
**기반 문서:** `docs/02_SRS_BASELINE.md`(Baseline, 변경 없음 유지), `docs/PROJECT_SCOPE.md`, `docs/03_UI_COVERAGE_ANALYSIS.md`, `design-reference/UI_CONTRACT.md`, `design-reference/SCREEN_ROUTE_CONTRACT.json`

## 0. 개정 성격

이 문서는 `docs/02_SRS_BASELINE.md`를 **대체하지 않는다**. Baseline의 REQ-FUNC-001~080, REQ-NF-001~034는 그대로 유효하며 이 문서에서도 하나도 삭제하지 않는다(§4 전체 목록 참고). 이 문서가 개정하는 부분은 오직 다음 두 가지다.

1. Baseline §3.5 Page and Route Inventory — 다중 공개 Route를 승인된 5개 디자인 Screen(SCR-001~005)의 탭·패널·Drawer·Modal로 통합한다.
2. Baseline에는 없던 **UI Route Contract**와 **Release Acceptance Criteria**를 신설한다.

Baseline의 다른 장(§1 Introduction, §2 Stakeholders, §4 Specific Requirements 본문, §6 Appendix 데이터 모델 등)은 변경 없이 유지된다.

---

## 1. 개정 §3.5 — Page and Route Inventory (승인된 5개 Screen 기준)

| Screen ID | Route | Page Entry | Access | Baseline 원본 Route(통합됨) |
|---|---|---|---|---|
| SCR-001 | `/` | `src/app/page.tsx` | Public | `/`, `/destinations`, `/destinations/domestic`, `/destinations/overseas`, `/destinations/[slug]`, `/safety`, `/safety/[countryCode]` |
| SCR-002 | `/about` | `src/app/about/page.tsx` | Public | `/about` |
| SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | Public(동행 탭 작성은 Adult Member) | `/flights`, `/hotels`, `/mates/new` |
| SCR-004 | `/mates` | `src/app/mates/page.tsx` | Public(참가 요청은 Adult Member) | `/mates`, `/mates/[id]` |
| SCR-005 | `/account` | `src/app/account/page.tsx` | Public/Member/Role Restricted(역할별 탭) | `/auth/*`, `/my/*`, `/admin/*` |

여행지 상세와 국가 안전정보 상세는 별도 페이지가 아니라 SCR-001 안의 Drawer/Modal 상태로 존재한다. 동행 모집글 상세는 Desktop에서 SCR-004의 상세 패널, Mobile에서 상세 Drawer로 존재한다. 이 변경은 REQ-FUNC-001~080, REQ-NF-001~034의 내용 자체를 바꾸지 않으며, 각 요구사항이 어느 화면·Route·파일에서 검증되는지만 재배치한다.

## 2. UI Route Contract

정본은 `design-reference/SCREEN_ROUTE_CONTRACT.json`(`schema_version: traveler-screen-route-v1`, `framework: nextjs-app-router`)이다. 핵심 규칙:

- `screens` 배열은 SCR-001~005 정확히 5개, Route 중복 없음, Page Entry 중복 없음.
- 핵심(Core) 4개: SCR-001, SCR-003, SCR-004, SCR-005 / 보조(Auxiliary) 1개: SCR-002.
- 모든 Screen에 `page_owner_task_required=true`, `preview_required=true`.
- SCR-001에만 `starter_template_forbidden=true` — 현재 `src/app/page.tsx`의 Next.js 기본 스캐폴드는 그대로 두면 안 된다.
- `technical_routes`(인증 콜백 `/auth/callback`, API Route `/api/*`, `not-found`, `error boundary`)는 Screen 수에 포함하지 않는다.
- `required_navigation` 14건이 화면 간 실제 이동 관계를 정의한다(`docs/05_UIUX_APPROVED.md` §2, `design-reference/UI_CONTRACT.md` 각 Screen 표 참고).

## 3. Release Acceptance Criteria

Baseline §6.8 Validation Plan에 더해, 이 UI/UX 개정판을 릴리스하기 위한 추가 조건은 다음과 같다(전체는 `docs/05_UIUX_APPROVED.md` §6과 동일하며 여기서는 SRS 관점으로 재기술한다).

1. `SCREEN_ROUTE_CONTRACT.json`과 실제 `src/app` 라우팅 구조가 Route·Page Entry 기준으로 100% 일치해야 한다.
2. §4의 Implementation Status가 `IMPLEMENT` 계열(IMPLEMENT / IMPLEMENT(축소) / IMPLEMENT(대체))인 모든 요구사항이 코드로 반영되고, `docs/UIUX_TRACEABILITY.md`의 Test 열에 기술된 방법으로 검증되어야 한다.
3. Implementation Status가 `EXCLUDED`인 요구사항은 어떤 화면에도 임의로 복원하지 않는다.
4. `STITCH_VALIDATION_REPORT.md`의 `STITCH_VALIDATION_NEEDS_HUMAN` 항목(SCR-001·SCR-004 CTA 경로)이 해소되어야 한다.
5. Playwright 핵심 Smoke Test(REQ-FUNC-011의 UC-01~UC-09 대응)가 5개 Screen 전부에서 통과해야 한다.
6. 이 문서, `docs/UIUX_TRACEABILITY.md`, `docs/05_UIUX_APPROVED.md` 중 어디에도 미구현 항목을 "구현 완료"로 기록하지 않는다 — 위반 발견 시 해당 문서를 즉시 정정한다.

이 조건이 모두 충족되기 전까지 §4의 모든 IMPLEMENT 계열 요구사항은 Implementation Status와 무관하게 **미구현 상태**로 취급한다.

## 4. Requirement Disposition — 전체 목록 (REQ-FUNC-001~080, REQ-NF-001~034)

`Implementation Status`는 `docs/PROJECT_SCOPE.md`의 분류를 그대로 옮긴 것이며, 실제 코드 구현 여부를 뜻하지 않는다(구현 여부는 `docs/UIUX_TRACEABILITY.md`의 `Status` 열 참고 — 2026-09-15 기준 전부 `NOT_STARTED`). `Route`가 "N/A"인 항목은 화면에 직접 나타나지 않는 데이터/보안/운영 요구사항이다.

### 4.1 F1 Destination Guide

| Requirement | Implementation Status | Screen | Route |
|---|---|---|---|
| REQ-FUNC-001 | IMPLEMENT | SCR-001 | `/` |
| REQ-FUNC-002 | IMPLEMENT | SCR-001 | `/` |
| REQ-FUNC-003 | IMPLEMENT | SCR-001 | `/` |
| REQ-FUNC-004 | IMPLEMENT | SCR-001 | `/` |
| REQ-FUNC-005 | IMPLEMENT | SCR-001 | `/` |
| REQ-FUNC-006 | IMPLEMENT | SCR-001 | `/` |
| REQ-FUNC-007 | IMPLEMENT | SCR-001 | `/` |
| REQ-FUNC-008 | IMPLEMENT | N/A | N/A |
| REQ-FUNC-009 | IMPLEMENT | SCR-001 | `/` |
| REQ-FUNC-010 | IMPLEMENT | SCR-001 | `/` |

### 4.2 F2 Flight Link-out

| Requirement | Implementation Status | Screen | Route |
|---|---|---|---|
| REQ-FUNC-011 | IMPLEMENT | SCR-003 | `/travel-tools` |
| REQ-FUNC-012 | IMPLEMENT | SCR-003 | `/travel-tools` |
| REQ-FUNC-013 | IMPLEMENT | SCR-003 | `/travel-tools` |
| REQ-FUNC-014 | IMPLEMENT | SCR-003 | `/travel-tools` |
| REQ-FUNC-015 | IMPLEMENT | SCR-003 | `/travel-tools` |
| REQ-FUNC-016 | IMPLEMENT | SCR-003 | `/travel-tools` |
| REQ-FUNC-017 | IMPLEMENT | N/A | N/A |
| REQ-FUNC-018 | IMPLEMENT | SCR-003 | `/travel-tools` |

### 4.3 F3 Hotel Link-out

| Requirement | Implementation Status | Screen | Route |
|---|---|---|---|
| REQ-FUNC-019 | IMPLEMENT | SCR-003 | `/travel-tools` |
| REQ-FUNC-020 | IMPLEMENT | SCR-003 | `/travel-tools` |
| REQ-FUNC-021 | IMPLEMENT | SCR-003 | `/travel-tools` |
| REQ-FUNC-022 | IMPLEMENT | SCR-003 | `/travel-tools` |
| REQ-FUNC-023 | IMPLEMENT | SCR-003 | `/travel-tools` |
| REQ-FUNC-024 | IMPLEMENT | SCR-003 | `/travel-tools` |
| REQ-FUNC-025 | IMPLEMENT | N/A | N/A |
| REQ-FUNC-026 | IMPLEMENT | SCR-003 | `/travel-tools` |

### 4.4 F4 Travel Mate

| Requirement | Implementation Status | Screen | Route |
|---|---|---|---|
| REQ-FUNC-027 | IMPLEMENT | SCR-003 | `/travel-tools` |
| REQ-FUNC-028 | IMPLEMENT | SCR-005 | `/account` |
| REQ-FUNC-029 | IMPLEMENT | SCR-005 | `/account` |
| REQ-FUNC-030 | IMPLEMENT | SCR-004 | `/mates` |
| REQ-FUNC-031 | IMPLEMENT | SCR-003 | `/travel-tools` |
| REQ-FUNC-032 | IMPLEMENT | SCR-003 | `/travel-tools` |
| REQ-FUNC-033 | IMPLEMENT | SCR-004 | `/mates` |
| REQ-FUNC-034 | IMPLEMENT | SCR-004 | `/mates` |
| REQ-FUNC-035 | IMPLEMENT | SCR-004 | `/mates` |
| REQ-FUNC-036 | IMPLEMENT | SCR-005 | `/account` |
| REQ-FUNC-037 | IMPLEMENT | SCR-004 | `/mates` |
| REQ-FUNC-038 | IMPLEMENT | SCR-005 | `/account` |
| REQ-FUNC-039 | IMPLEMENT | SCR-004 | `/mates` |
| REQ-FUNC-040 | IMPLEMENT | SCR-004 | `/mates` |
| REQ-FUNC-041 | IMPLEMENT(축소) | SCR-005 | `/account` |
| REQ-FUNC-042 | IMPLEMENT(축소) | SCR-005 | `/account` |
| REQ-FUNC-043 | IMPLEMENT | 전역 | 전체(5개 Route 공통) |
| REQ-FUNC-044 | IMPLEMENT | N/A | N/A |
| REQ-FUNC-045 | EXCLUDED | N/A | N/A |

### 4.5 F5 Country Safety

| Requirement | Implementation Status | Screen | Route |
|---|---|---|---|
| REQ-FUNC-046 | IMPLEMENT | N/A | N/A |
| REQ-FUNC-047 | IMPLEMENT | SCR-001 | `/` |
| REQ-FUNC-048 | IMPLEMENT | SCR-001 | `/` |
| REQ-FUNC-049 | IMPLEMENT | SCR-001 | `/` |
| REQ-FUNC-050 | IMPLEMENT | SCR-001 | `/` |
| REQ-FUNC-051 | IMPLEMENT | SCR-001 | `/` |
| REQ-FUNC-052 | IMPLEMENT | SCR-001 | `/` |
| REQ-FUNC-053 | IMPLEMENT | SCR-001 | `/` |
| REQ-FUNC-054 | IMPLEMENT | SCR-001 | `/` |
| REQ-FUNC-055 | EXCLUDED | N/A | N/A |
| REQ-FUNC-056 | EXCLUDED | N/A | N/A |

### 4.6 F6 About free_traveler

| Requirement | Implementation Status | Screen | Route |
|---|---|---|---|
| REQ-FUNC-057 | IMPLEMENT | SCR-002 | `/about` |
| REQ-FUNC-058 | IMPLEMENT | SCR-002 | `/about` |
| REQ-FUNC-059 | IMPLEMENT | SCR-002 | `/about` |
| REQ-FUNC-060 | IMPLEMENT | SCR-002 | `/about` |
| REQ-FUNC-061 | IMPLEMENT | SCR-002 | `/about` |
| REQ-FUNC-062 | IMPLEMENT | SCR-002 | `/about` |
| REQ-FUNC-063 | IMPLEMENT | SCR-002 | `/about` |

### 4.7 F7 Common, Admin, Governance

| Requirement | Implementation Status | Screen | Route |
|---|---|---|---|
| REQ-FUNC-064 | IMPLEMENT | 전역 | 전체(5개 Route 공통) |
| REQ-FUNC-065 | IMPLEMENT | 전역 | 전체(5개 Route 공통) |
| REQ-FUNC-066 | IMPLEMENT | SCR-005 | `/account` |
| REQ-FUNC-067 | IMPLEMENT | SCR-001 | `/` |
| REQ-FUNC-068 | IMPLEMENT | SCR-001 | `/` |
| REQ-FUNC-069 | IMPLEMENT | SCR-001 | `/` |
| REQ-FUNC-070 | IMPLEMENT | 전역 | 전체(5개 Route 공통) |
| REQ-FUNC-071 | EXCLUDED | N/A | N/A |
| REQ-FUNC-072 | EXCLUDED | N/A | N/A |
| REQ-FUNC-073 | EXCLUDED | N/A | N/A |
| REQ-FUNC-074 | IMPLEMENT(대체) | N/A | N/A |
| REQ-FUNC-075 | EXCLUDED | N/A | N/A |
| REQ-FUNC-076 | EXCLUDED | N/A | N/A |
| REQ-FUNC-077 | IMPLEMENT | SCR-005 | `/account` |
| REQ-FUNC-078 | IMPLEMENT | 전역 | 전체(5개 Route 공통) |
| REQ-FUNC-079 | IMPLEMENT | 전역 | 전체(5개 Route 공통) |
| REQ-FUNC-080 | IMPLEMENT | SCR-003 | `/travel-tools` |

### 4.8 NF Performance

| Requirement | Implementation Status | Screen | Route |
|---|---|---|---|
| REQ-NF-001 | EXCLUDED | N/A | N/A |
| REQ-NF-002 | EXCLUDED | N/A | N/A |
| REQ-NF-003 | EXCLUDED | N/A | N/A |
| REQ-NF-004 | IMPLEMENT(축소) | SCR-001 | `/` |
| REQ-NF-005 | IMPLEMENT(축소) | N/A | N/A |
| REQ-NF-006 | IMPLEMENT | 전역 | 전체(5개 Route 공통) |
| REQ-NF-007 | EXCLUDED | N/A | N/A |

### 4.9 NF Reliability

| Requirement | Implementation Status | Screen | Route |
|---|---|---|---|
| REQ-NF-008 | EXCLUDED | N/A | N/A |
| REQ-NF-009 | EXCLUDED | N/A | N/A |
| REQ-NF-010 | EXCLUDED | N/A | N/A |
| REQ-NF-011 | EXCLUDED | N/A | N/A |

### 4.10 NF Security and Privacy

| Requirement | Implementation Status | Screen | Route |
|---|---|---|---|
| REQ-NF-012 | IMPLEMENT | N/A | N/A |
| REQ-NF-013 | IMPLEMENT | N/A | N/A |
| REQ-NF-014 | IMPLEMENT | N/A | N/A |
| REQ-NF-015 | IMPLEMENT | N/A | N/A |
| REQ-NF-016 | IMPLEMENT | N/A | N/A |
| REQ-NF-017 | IMPLEMENT | N/A | N/A |
| REQ-NF-018 | EXCLUDED | N/A | N/A |

### 4.11 NF Safety and Moderation

| Requirement | Implementation Status | Screen | Route |
|---|---|---|---|
| REQ-NF-019 | IMPLEMENT(축소) | SCR-004 | `/mates` |
| REQ-NF-020 | EXCLUDED | N/A | N/A |
| REQ-NF-021 | EXCLUDED | N/A | N/A |
| REQ-NF-022 | EXCLUDED | N/A | N/A |

### 4.12 NF Accessibility

| Requirement | Implementation Status | Screen | Route |
|---|---|---|---|
| REQ-NF-023 | IMPLEMENT | 전역 | 전체(5개 Route 공통) |
| REQ-NF-024 | EXCLUDED | N/A | N/A |
| REQ-NF-025 | EXCLUDED | N/A | N/A |

### 4.13 NF Content, Freshness, SEO, Copyright

| Requirement | Implementation Status | Screen | Route |
|---|---|---|---|
| REQ-NF-026 | IMPLEMENT | N/A | N/A |
| REQ-NF-027 | IMPLEMENT | N/A | N/A |
| REQ-NF-028 | IMPLEMENT(축소) | N/A | N/A |
| REQ-NF-029 | EXCLUDED | N/A | N/A |
| REQ-NF-030 | IMPLEMENT | 전역 | 전체(5개 Route 공통) |

### 4.14 NF Maintainability, Monitoring, Cost

| Requirement | Implementation Status | Screen | Route |
|---|---|---|---|
| REQ-NF-031 | IMPLEMENT | N/A | N/A |
| REQ-NF-032 | EXCLUDED | N/A | N/A |
| REQ-NF-033 | EXCLUDED | N/A | N/A |
| REQ-NF-034 | IMPLEMENT | N/A | N/A |

## 5. 총계 검증

REQ-FUNC-001~080(80개) + REQ-NF-001~034(34개) = **114개**, 이 문서 §4에 전부 기록됨(삭제 0건). 세부 열(Page Entry/Task/Test/Status)은 `docs/UIUX_TRACEABILITY.md`에서 관리한다.

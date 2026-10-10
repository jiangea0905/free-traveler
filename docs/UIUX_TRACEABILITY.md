# UI/UX Traceability Matrix — Free Traveler

**Document ID:** UIUX-TRACE-001
**작성일:** 2026-09-15
**기반 문서:** `docs/02_SRS_BASELINE.md`, `docs/PROJECT_SCOPE.md`, `docs/03_UI_COVERAGE_ANALYSIS.md`, `design-reference/UI_CONTRACT.md`, `design-reference/SCREEN_ROUTE_CONTRACT.json`, `docs/06_SRS_UIUX_REVISED.md`

REQ-FUNC-001~080, REQ-NF-001~034 총 114개를 하나도 삭제하지 않고 전부 기록한다. 열 정의는 다음과 같다.

| 열 | 의미 |
|---|---|
| **Requirement** | SRS Baseline 요구사항 ID |
| **Implementation Status** | `docs/PROJECT_SCOPE.md`의 범위 결정 — `IMPLEMENT` / `IMPLEMENT(축소)` / `IMPLEMENT(대체)` / `EXCLUDED`. 실제 코드 구현 여부가 아니라 "무엇을 만들기로 했는가"를 뜻한다. |
| **Screen** | 승인된 5개 Screen(SCR-001~005) 중 배치 위치, 5개 화면 공통이면 `전역`, 화면에 나타나지 않으면 `N/A` |
| **Route** | 해당 Screen의 Route, 공통이면 `전체(5개 Route 공통)`, 없으면 `N/A` |
| **Page Entry** | `SCREEN_ROUTE_CONTRACT.json` 기준 실제 구현 파일 경로, 없으면 `N/A` |
| **Task** | 이 요구사항을 구현할 작업 항목 ID. 작업이 아직 생성되지 않았으므로 전 항목 `PENDING_TASK_GENERATION` |
| **Test** | 검증 방법(요약) |
| **Status** | 2026-09-15 기준 실제 진행 상태 — `NOT_STARTED`(범위 내, 미착수) 또는 `EXCLUDED`(범위 밖, 계획 없음). 구현이 완료된 항목은 없다. |

`src/app`에는 현재 Next.js 기본 스캐폴드만 존재하므로(§`docs/05_UIUX_APPROVED.md` §4), 이 문서의 어떤 행도 `Status`를 `DONE`/`IMPLEMENTED`로 기록하지 않는다.

---

## F1. Destination Guide (REQ-FUNC-001~010)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-FUNC-001 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | Playwright: 탭 전환 후 구분값 검증 | NOT_STARTED |
| REQ-FUNC-002 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | 단위 테스트: 필터 조합 결과 검증 | NOT_STARTED |
| REQ-FUNC-003 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | 단위 테스트: 한글 부분 일치·결과 없음 | NOT_STARTED |
| REQ-FUNC-004 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | 데이터 스키마 검증 테스트 | NOT_STARTED |
| REQ-FUNC-005 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | Playwright: 빈 결과 유도 후 확인 | NOT_STARTED |
| REQ-FUNC-006 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | 단위 테스트: 여행지-국가 코드 일치 | NOT_STARTED |
| REQ-FUNC-007 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | 데이터 스키마 검증 테스트 | NOT_STARTED |
| REQ-FUNC-008 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | 데이터 수량 검증 테스트 | NOT_STARTED |
| REQ-FUNC-009 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | 단위 테스트: 추천 목록 개수·중복 제외 | NOT_STARTED |
| REQ-FUNC-010 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | Playwright: URL 공유 후 필터 복원 | NOT_STARTED |

## F2. Flight Link-out (REQ-FUNC-011~018)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-FUNC-011 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | Playwright: 미입력 시 오류 표시 | NOT_STARTED |
| REQ-FUNC-012 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | 단위 테스트 | NOT_STARTED |
| REQ-FUNC-013 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | 단위 테스트: 경계값 | NOT_STARTED |
| REQ-FUNC-014 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | Playwright: 수정 후 재확인 | NOT_STARTED |
| REQ-FUNC-015 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | Playwright: 문구 노출 확인 | NOT_STARTED |
| REQ-FUNC-016 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | Playwright: 새 탭 URL 검증 | NOT_STARTED |
| REQ-FUNC-017 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | 네트워크 탭/코드 리뷰 | NOT_STARTED |
| REQ-FUNC-018 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | Playwright: URL 미설정 오류 노출 | NOT_STARTED |

## F3. Hotel Link-out (REQ-FUNC-019~026)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-FUNC-019 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | Playwright: 미입력 오류 표시 | NOT_STARTED |
| REQ-FUNC-020 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | 단위 테스트 | NOT_STARTED |
| REQ-FUNC-021 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | 단위 테스트: 경계값 | NOT_STARTED |
| REQ-FUNC-022 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | Playwright: 값 대조 | NOT_STARTED |
| REQ-FUNC-023 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | Playwright: 문구 노출 확인 | NOT_STARTED |
| REQ-FUNC-024 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | Playwright: 새 탭 URL 검증 | NOT_STARTED |
| REQ-FUNC-025 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | 코드 리뷰·네트워크 탭 | NOT_STARTED |
| REQ-FUNC-026 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | Playwright: 오류 상태 입력값 보존 확인 | NOT_STARTED |

## F4. Travel Mate (REQ-FUNC-027~045)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-FUNC-027 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | Playwright: 비로그인 작성 시도 차단 확인 | NOT_STARTED |
| REQ-FUNC-028 | IMPLEMENT | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | DB 스키마 확인, 단위 테스트 | NOT_STARTED |
| REQ-FUNC-029 | IMPLEMENT | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | Playwright: 필수값 검증 | NOT_STARTED |
| REQ-FUNC-030 | IMPLEMENT | SCR-004 | `/mates` | `src/app/mates/page.tsx` | PENDING_TASK_GENERATION | 단위 테스트: 필터 조합, 차단 제외 | NOT_STARTED |
| REQ-FUNC-031 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | Playwright: 필수값·날짜 역전 차단 | NOT_STARTED |
| REQ-FUNC-032 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | 단위 테스트: 탐지 케이스셋 | NOT_STARTED |
| REQ-FUNC-033 | IMPLEMENT | SCR-004 | `/mates` | `src/app/mates/page.tsx` | PENDING_TASK_GENERATION | 단위 테스트: 응답 스키마 검사 | NOT_STARTED |
| REQ-FUNC-034 | IMPLEMENT | SCR-004 | `/mates` | `src/app/mates/page.tsx` | PENDING_TASK_GENERATION | Playwright: 요청 제출·PENDING 확인 | NOT_STARTED |
| REQ-FUNC-035 | IMPLEMENT | SCR-004 | `/mates` | `src/app/mates/page.tsx` | PENDING_TASK_GENERATION | 단위 테스트: 중복 요청 시도 | NOT_STARTED |
| REQ-FUNC-036 | IMPLEMENT | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | Playwright: 비작성자 변경 차단 확인 | NOT_STARTED |
| REQ-FUNC-037 | IMPLEMENT | SCR-004 | `/mates` | `src/app/mates/page.tsx` | PENDING_TASK_GENERATION | 단위 테스트: 종료일 경과 케이스 | NOT_STARTED |
| REQ-FUNC-038 | IMPLEMENT | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | Playwright: 수정·마감 흐름 | NOT_STARTED |
| REQ-FUNC-039 | IMPLEMENT | SCR-004 | `/mates` | `src/app/mates/page.tsx` | PENDING_TASK_GENERATION | Playwright: 신고 접수 후 ID 노출 확인 | NOT_STARTED |
| REQ-FUNC-040 | IMPLEMENT | SCR-004 | `/mates` | `src/app/mates/page.tsx` | PENDING_TASK_GENERATION | 단위 테스트: 차단 관계 필터링 | NOT_STARTED |
| REQ-FUNC-041 | IMPLEMENT(축소) | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | Playwright: 관리자 탭 신고 목록·상태 변경 확인 | NOT_STARTED |
| REQ-FUNC-042 | IMPLEMENT(축소) | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | Playwright: 신고 처리 후 글 숨김 확인 | NOT_STARTED |
| REQ-FUNC-043 | IMPLEMENT | 전역 | 전체(5개 Route 공통) | `src/app/layout.tsx` | PENDING_TASK_GENERATION | Playwright: 상태 변경 후 알림 표시 확인 | NOT_STARTED |
| REQ-FUNC-044 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | Supabase RLS 정책 테스트 | NOT_STARTED |
| REQ-FUNC-045 | EXCLUDED | N/A | N/A | N/A | PENDING_TASK_GENERATION | 해당 없음 | EXCLUDED |

## F5. Country Safety (REQ-FUNC-046~056)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-FUNC-046 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | 데이터 수량 검증 테스트 | NOT_STARTED |
| REQ-FUNC-047 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | 데이터 스키마 검증 테스트 | NOT_STARTED |
| REQ-FUNC-048 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | 데이터 스키마 검증 테스트 | NOT_STARTED |
| REQ-FUNC-049 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | Playwright: 링크 클릭 시 새 탭 확인 | NOT_STARTED |
| REQ-FUNC-050 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | 단위 테스트: 날짜 경계값 | NOT_STARTED |
| REQ-FUNC-051 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | Playwright: 경보 라벨 상단 노출 확인 | NOT_STARTED |
| REQ-FUNC-052 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | 데이터 스키마 검증 테스트 | NOT_STARTED |
| REQ-FUNC-053 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | 데이터 스키마 검증 테스트 | NOT_STARTED |
| REQ-FUNC-054 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | Playwright: 문구 노출 확인 | NOT_STARTED |
| REQ-FUNC-055 | EXCLUDED | N/A | N/A | N/A | PENDING_TASK_GENERATION | 해당 없음 | EXCLUDED |
| REQ-FUNC-056 | EXCLUDED | N/A | N/A | N/A | PENDING_TASK_GENERATION | 해당 없음 | EXCLUDED |

## F6. About free_traveler (REQ-FUNC-057~063)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-FUNC-057 | IMPLEMENT | SCR-002 | `/about` | `src/app/about/page.tsx` | PENDING_TASK_GENERATION | 단위 테스트: 값 일치 | NOT_STARTED |
| REQ-FUNC-058 | IMPLEMENT | SCR-002 | `/about` | `src/app/about/page.tsx` | PENDING_TASK_GENERATION | Playwright: 텍스트 노출 확인 | NOT_STARTED |
| REQ-FUNC-059 | IMPLEMENT | SCR-002 | `/about` | `src/app/about/page.tsx` | PENDING_TASK_GENERATION | 데이터 수량 검증 테스트 | NOT_STARTED |
| REQ-FUNC-060 | IMPLEMENT | SCR-002 | `/about` | `src/app/about/page.tsx` | PENDING_TASK_GENERATION | 데이터 스키마 검증 테스트 | NOT_STARTED |
| REQ-FUNC-061 | IMPLEMENT | SCR-002 | `/about` | `src/app/about/page.tsx` | PENDING_TASK_GENERATION | 데이터 스키마 검증 테스트 | NOT_STARTED |
| REQ-FUNC-062 | IMPLEMENT | SCR-002 | `/about` | `src/app/about/page.tsx` | PENDING_TASK_GENERATION | 단위 테스트: 빈 링크 미노출 | NOT_STARTED |
| REQ-FUNC-063 | IMPLEMENT | SCR-002 | `/about` | `src/app/about/page.tsx` | PENDING_TASK_GENERATION | 단위 테스트: 링크 유효성 | NOT_STARTED |

## F7. Common, Admin, Governance (REQ-FUNC-064~080)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-FUNC-064 | IMPLEMENT | 전역 | 전체(5개 Route 공통) | `src/app/layout.tsx` | PENDING_TASK_GENERATION | Playwright: 내비게이션 클릭 경로 확인 | NOT_STARTED |
| REQ-FUNC-065 | IMPLEMENT | 전역 | 전체(5개 Route 공통) | `src/app/layout.tsx` | PENDING_TASK_GENERATION | Playwright: 모바일 뷰포트 렌더 확인 | NOT_STARTED |
| REQ-FUNC-066 | IMPLEMENT | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | Playwright: 가입~로그인 흐름 | NOT_STARTED |
| REQ-FUNC-067 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | 단위 테스트: 검색 결과 라벨 | NOT_STARTED |
| REQ-FUNC-068 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | 단위 테스트: 중복 추가 방지 | NOT_STARTED |
| REQ-FUNC-069 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | Playwright: 공유 버튼 동작 확인 | NOT_STARTED |
| REQ-FUNC-070 | IMPLEMENT | 전역 | 전체(5개 Route 공통) | `src/app/layout.tsx` | PENDING_TASK_GENERATION | 단위 테스트: 메타데이터 존재 확인 | NOT_STARTED |
| REQ-FUNC-071 | EXCLUDED | N/A | N/A | N/A | PENDING_TASK_GENERATION | 해당 없음 | EXCLUDED |
| REQ-FUNC-072 | EXCLUDED | N/A | N/A | N/A | PENDING_TASK_GENERATION | 해당 없음 | EXCLUDED |
| REQ-FUNC-073 | EXCLUDED | N/A | N/A | N/A | PENDING_TASK_GENERATION | 해당 없음 | EXCLUDED |
| REQ-FUNC-074 | IMPLEMENT(대체) | N/A | N/A | N/A | PENDING_TASK_GENERATION | 빌드/CI 데이터 검증 테스트 | NOT_STARTED |
| REQ-FUNC-075 | EXCLUDED | N/A | N/A | N/A | PENDING_TASK_GENERATION | 해당 없음 | EXCLUDED |
| REQ-FUNC-076 | EXCLUDED | N/A | N/A | N/A | PENDING_TASK_GENERATION | 해당 없음 | EXCLUDED |
| REQ-FUNC-077 | IMPLEMENT | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | Playwright: 잘못된 URL 저장 차단 확인 | NOT_STARTED |
| REQ-FUNC-078 | IMPLEMENT | 전역 | 전체(5개 Route 공통) | `src/app/layout.tsx` | PENDING_TASK_GENERATION | Playwright: 오류 화면 복구 버튼 확인 | NOT_STARTED |
| REQ-FUNC-079 | IMPLEMENT | 전역 | 전체(5개 Route 공통) | `src/app/layout.tsx` | PENDING_TASK_GENERATION | Playwright: 키보드 포커스 기본 확인 | NOT_STARTED |
| REQ-FUNC-080 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | Playwright: 동의 없이 제출 차단 확인 | NOT_STARTED |

## NF Performance (REQ-NF-001~007)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-NF-001 | EXCLUDED | N/A | N/A | N/A | PENDING_TASK_GENERATION | 해당 없음 | EXCLUDED |
| REQ-NF-002 | EXCLUDED | N/A | N/A | N/A | PENDING_TASK_GENERATION | 해당 없음 | EXCLUDED |
| REQ-NF-003 | EXCLUDED | N/A | N/A | N/A | PENDING_TASK_GENERATION | 해당 없음 | EXCLUDED |
| REQ-NF-004 | IMPLEMENT(축소) | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | Playwright: 필터 클릭 후 렌더링 수동 확인 | NOT_STARTED |
| REQ-NF-005 | IMPLEMENT(축소) | N/A | N/A | N/A | PENDING_TASK_GENERATION | Playwright: 제출 응답 시간 수동 확인 | NOT_STARTED |
| REQ-NF-006 | IMPLEMENT | 전역 | 전체(5개 Route 공통) | `src/app/layout.tsx` | PENDING_TASK_GENERATION | 코드 리뷰: `Image` 컴포넌트 사용 확인 | NOT_STARTED |
| REQ-NF-007 | EXCLUDED | N/A | N/A | N/A | PENDING_TASK_GENERATION | 해당 없음 | EXCLUDED |

## NF Reliability and Recovery (REQ-NF-008~011)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-NF-008 | EXCLUDED | N/A | N/A | N/A | PENDING_TASK_GENERATION | 해당 없음 | EXCLUDED |
| REQ-NF-009 | EXCLUDED | N/A | N/A | N/A | PENDING_TASK_GENERATION | 해당 없음 | EXCLUDED |
| REQ-NF-010 | EXCLUDED | N/A | N/A | N/A | PENDING_TASK_GENERATION | 해당 없음 | EXCLUDED |
| REQ-NF-011 | EXCLUDED | N/A | N/A | N/A | PENDING_TASK_GENERATION | 해당 없음 | EXCLUDED |

## NF Security and Privacy (REQ-NF-012~018)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-NF-012 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | 배포 URL HTTPS 확인 | NOT_STARTED |
| REQ-NF-013 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | Supabase RLS 정책 테스트 | NOT_STARTED |
| REQ-NF-014 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | 코드 리뷰: 쿠키 설정 확인 | NOT_STARTED |
| REQ-NF-015 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | 단위 테스트: 스크립트 입력 케이스 | NOT_STARTED |
| REQ-NF-016 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | 빌드 산출물에서 키 문자열 검색 | NOT_STARTED |
| REQ-NF-017 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | 네트워크 탭/코드 리뷰 확인 | NOT_STARTED |
| REQ-NF-018 | EXCLUDED | N/A | N/A | N/A | PENDING_TASK_GENERATION | 해당 없음 | EXCLUDED |

## NF Safety and Moderation (REQ-NF-019~022)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-NF-019 | IMPLEMENT(축소) | SCR-004 | `/mates` | `src/app/mates/page.tsx` | PENDING_TASK_GENERATION | Playwright: 신고 제출 응답 수동 확인 | NOT_STARTED |
| REQ-NF-020 | EXCLUDED | N/A | N/A | N/A | PENDING_TASK_GENERATION | 해당 없음 | EXCLUDED |
| REQ-NF-021 | EXCLUDED | N/A | N/A | N/A | PENDING_TASK_GENERATION | 해당 없음 | EXCLUDED |
| REQ-NF-022 | EXCLUDED | N/A | N/A | N/A | PENDING_TASK_GENERATION | 해당 없음 | EXCLUDED |

## NF Accessibility (REQ-NF-023~025)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-NF-023 | IMPLEMENT | 전역 | 전체(5개 Route 공통) | `src/app/layout.tsx` | PENDING_TASK_GENERATION | 코드 리뷰: 시맨틱 마크업 확인 | NOT_STARTED |
| REQ-NF-024 | EXCLUDED | N/A | N/A | N/A | PENDING_TASK_GENERATION | 해당 없음 | EXCLUDED |
| REQ-NF-025 | EXCLUDED | N/A | N/A | N/A | PENDING_TASK_GENERATION | 해당 없음 | EXCLUDED |

## NF Content, Freshness, SEO, Copyright (REQ-NF-026~030)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-NF-026 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | 데이터 검증 테스트 | NOT_STARTED |
| REQ-NF-027 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | 데이터 검증 테스트 | NOT_STARTED |
| REQ-NF-028 | IMPLEMENT(축소) | N/A | N/A | N/A | PENDING_TASK_GENERATION | 단위 테스트: stale 경계값 | NOT_STARTED |
| REQ-NF-029 | EXCLUDED | N/A | N/A | N/A | PENDING_TASK_GENERATION | 해당 없음 | EXCLUDED |
| REQ-NF-030 | IMPLEMENT | 전역 | 전체(5개 Route 공통) | `src/app/layout.tsx` | PENDING_TASK_GENERATION | 단위 테스트: 메타데이터 누락 확인 | NOT_STARTED |

## NF Maintainability, Monitoring, Cost (REQ-NF-031~034)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-NF-031 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | CI: lint·build·단위 테스트 실행 | NOT_STARTED |
| REQ-NF-032 | EXCLUDED | N/A | N/A | N/A | PENDING_TASK_GENERATION | 해당 없음 | EXCLUDED |
| REQ-NF-033 | EXCLUDED | N/A | N/A | N/A | PENDING_TASK_GENERATION | 해당 없음 | EXCLUDED |
| REQ-NF-034 | IMPLEMENT | N/A | N/A | N/A | PENDING_TASK_GENERATION | 사용 중인 요금제 확인 | NOT_STARTED |

---

## 총계 검증

| 구분 | 개수 |
|---|---:|
| REQ-FUNC-001~080 | 80 |
| REQ-NF-001~034 | 34 |
| **합계(삭제 0건)** | **114** |
| Implementation Status = EXCLUDED | 25 |
| Implementation Status = IMPLEMENT 계열(IMPLEMENT/축소/대체) | 89 |
| Task = PENDING_TASK_GENERATION (전체) | 114 |
| Status = NOT_STARTED | 89 |
| Status = EXCLUDED | 25 |

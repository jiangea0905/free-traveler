# UI Coverage Analysis — Free Traveler 5-Screen 배치

**Document ID:** UICOV-TRAVEL-001
**Revision:** 1.0
**작성일:** 2026-09-11
**기반 문서:** `docs/02_SRS_BASELINE.md`, `docs/PROJECT_SCOPE.md`

이 문서는 SRS의 REQ-FUNC-001~080, REQ-NF-001~034 전체를 5개 디자인 Screen에 배치하고, 각 요구사항이 화면에서 어떤 성격으로 나타나는지 분류한다. 요구사항은 하나도 삭제하지 않으며, `PROJECT_SCOPE.md`에서 EXCLUDED로 정한 항목은 화면에 배치하더라도 구현 범위로 되돌리지 않는다.

---

## 1. Screen 인벤토리 (정확히 5개)

| Screen ID | 라우트 | 화면 이름 |
|---|---|---|
| SCR-001 | `/` | 메인(여행지 탐색 + 안전정보 Drawer) |
| SCR-002 | `/about` | 대표 소개 |
| SCR-003 | `/travel-tools` | 통합 여행 준비(항공/호텔/동행작성 탭) |
| SCR-004 | `/mates` | 동행 조회 |
| SCR-005 | `/account` | 계정·관리 |

API Route, 인증 콜백(`/auth/callback` 등), 오류 처리 라우트는 화면이 아니라 기술 Route로 취급하며 6번째 Screen으로 세지 않는다.

### 1.1 SCR-001 `/` 메인

| 항목 | 내용 |
|---|---|
| 사용자 목표 | 국내·해외 여행지를 탐색해 후보를 좁히고, 상세 콘텐츠와 해당 국가 안전정보를 확인한다. |
| 주요 영역 | 통합 검색바, 국내/해외 탭, 필터 바(국가·도시·계절·테마·기간), 여행지 카드 그리드, 여행지 상세 Drawer/Modal, 국가 안전정보 Drawer/Modal, 즐겨찾기·공유 버튼 |
| 상태 | 목록 로딩/빈 결과, 필터 적용 상태(URL query 동기화), 상세 Drawer open/close, 안전정보 Drawer open/close, stale 경고 표시, 즐겨찾기 토글 |
| 이동 목적지 | 여행지 Drawer 내에서 국가 안전정보 Drawer로 전환 · 항공/호텔 준비 CTA → SCR-003 · 동행 찾기 CTA → SCR-004 · 로그인/즐겨찾기 확인 → SCR-005 |

### 1.2 SCR-002 `/about` 대표 소개

| 항목 | 내용 |
|---|---|
| 사용자 목표 | `free_traveler`의 여행 경험과 콘텐츠 편집 기준을 확인한다. |
| 주요 영역 | 히어로 소개, `50+ Trips`/`30+ Countries` 수치 카드, 여행 철학·편집 원칙, 방문 권역 지도/국가 목록, 여행 타임라인, 추천 여행지 6곳, 문의·SNS 링크 |
| 상태 | 이미지 로딩, 지도/목록 표시 전환(선택) |
| 이동 목적지 | 추천 여행지 클릭 → SCR-001 여행지 상세 Drawer(딥링크) · 문의·SNS 링크 → 외부 새 탭 |

### 1.3 SCR-003 `/travel-tools` 통합 여행 준비

| 항목 | 내용 |
|---|---|
| 사용자 목표 | 항공·숙소 조건을 정리해 외부 사이트로 이동하거나, 동행 모집글을 작성한다. |
| 주요 영역 | 3개 탭(항공 / 호텔 / 동행 작성), 항공 입력 폼·요약, 호텔 입력 폼·요약, 동행 작성 폼(안전수칙 동의 포함) |
| 상태 | 탭 선택 상태, 입력값 검증 오류, 입력→요약 단계 전환, 로그인·성인 확인 가드 통과 여부, 외부 이동 성공/실패 상태 |
| 이동 목적지 | 항공/호텔 외부 사이트 새 탭 · 동행 작성 완료 → SCR-004 목록 · 로그인·성인 확인 미충족 → SCR-005 |

### 1.4 SCR-004 `/mates` 동행 조회

| 항목 | 내용 |
|---|---|
| 사용자 목표 | 조건에 맞는 동행 모집글을 찾아 참가를 요청하거나, 문제가 있는 글·사용자를 신고·차단한다. |
| 주요 영역 | 필터 바, 모집글 리스트, 동행 상세 패널(참가 요청 폼, 신고·차단 버튼 포함) |
| 상태 | 목록/상세 패널 open, 자동 마감 계산 결과 표시, 중복 요청 차단 오류, 신고 접수 완료, 차단 완료 |
| 이동 목적지 | 새 글 작성 → SCR-003 동행 작성 탭 · 요청·글 관리 → SCR-005 내 활동 · 차단 목록 관리 → SCR-005 · 비로그인 상태 → SCR-005 로그인 |

### 1.5 SCR-005 `/account` 계정·관리

| 항목 | 내용 |
|---|---|
| 사용자 목표 | 로그인·가입하고 프로필과 내 활동(글·요청·즐겨찾기·차단)을 관리하며, 필요 시 신고 처리와 외부 URL을 설정한다. |
| 주요 영역 | 4개 탭 — 로그인/가입, 프로필(성인 확인 포함), 내 활동(내 글·요청·즐겨찾기·차단 목록), 간단 관리자(신고 상태, 외부 URL 설정) |
| 상태 | 탭 전환, 인증 상태, 역할에 따른 관리자 탭 노출 여부, 요청 승인/거절 처리 상태 |
| 이동 목적지 | 내 활동의 글/요청 항목 → SCR-004 상세 패널 · 즐겨찾기 항목 → SCR-001 상세 Drawer |

---

## 2. Requirement 분류 기준

| 분류 | 의미 |
|---|---|
| **UI_DIRECT** | 화면에 그려지는 구체적인 요소(버튼, 목록, 카드, 문구, 패널)로 나타나는 요구사항 |
| **UI_STATE** | 화면의 동작·검증·표시 여부를 결정하는 로직/상태 요구사항(별도 시각 요소가 아니라 기존 요소의 동작 규칙) |
| **NON_UI** | 사용자에게 직접 보이지 않는 데이터·보안·성능·SEO 메타 요구사항 |
| **OPERATIONS** | 운영·거버넌스·모니터링·비용·CI 프로세스에 관한 요구사항(화면과 직접 연결되지 않음) |

`PROJECT_SCOPE` 열은 `docs/PROJECT_SCOPE.md`의 분류(IMPLEMENT / IMPLEMENT(축소) / IMPLEMENT(대체) / EXCLUDED)를 그대로 옮긴 값이다.

---

## 3. REQ-FUNC 매핑 (80개)

### 3.1 F1. Destination Guide — REQ-FUNC-001~010

| ID | UI 분류 | Screen | PROJECT_SCOPE | 비고 |
|---|---|---|---|---|
| REQ-FUNC-001 | UI_DIRECT | SCR-001 | IMPLEMENT | 국내/해외 탭 |
| REQ-FUNC-002 | UI_DIRECT | SCR-001 | IMPLEMENT | 필터 바 |
| REQ-FUNC-003 | UI_DIRECT | SCR-001 | IMPLEMENT | 통합 검색바 |
| REQ-FUNC-004 | UI_DIRECT | SCR-001 | IMPLEMENT | 여행지 상세 Drawer/Modal 콘텐츠 |
| REQ-FUNC-005 | UI_DIRECT | SCR-001 | IMPLEMENT | 빈 결과 안내·초기화 버튼 |
| REQ-FUNC-006 | UI_DIRECT | SCR-001 | IMPLEMENT | 상세 Drawer → 안전정보 Drawer 전환 링크 |
| REQ-FUNC-007 | UI_STATE | SCR-001 | IMPLEMENT | 이미지 alt/출처 속성(비시각 메타데이터) |
| REQ-FUNC-008 | NON_UI | N/A | IMPLEMENT | 콘텐츠 수량 데이터 검증 |
| REQ-FUNC-009 | UI_DIRECT | SCR-001 | IMPLEMENT | 관련 여행지 추천 목록 |
| REQ-FUNC-010 | UI_STATE | SCR-001 | IMPLEMENT | 필터 상태의 URL query 동기화 |

### 3.2 F2. Flight Link-out — REQ-FUNC-011~018

| ID | UI 분류 | Screen | PROJECT_SCOPE | 비고 |
|---|---|---|---|---|
| REQ-FUNC-011 | UI_DIRECT | SCR-003 | IMPLEMENT | 항공 탭 입력 폼 |
| REQ-FUNC-012 | UI_STATE | SCR-003 | IMPLEMENT | 국가별 지역 옵션 제한 로직 |
| REQ-FUNC-013 | UI_STATE | SCR-003 | IMPLEMENT | 날짜 검증 로직 |
| REQ-FUNC-014 | UI_DIRECT | SCR-003 | IMPLEMENT | 요약 단계 표시 |
| REQ-FUNC-015 | UI_DIRECT | SCR-003 | IMPLEMENT | 비전달 고지 문구 |
| REQ-FUNC-016 | UI_DIRECT | SCR-003 | IMPLEMENT | `항공편 보러 가기` 외부 이동 버튼 |
| REQ-FUNC-017 | NON_UI | N/A | IMPLEMENT | 서버 미저장 제약 |
| REQ-FUNC-018 | UI_DIRECT | SCR-003 | IMPLEMENT | 외부 이동 오류·재시도 상태 |

### 3.3 F3. Hotel Link-out — REQ-FUNC-019~026

| ID | UI 분류 | Screen | PROJECT_SCOPE | 비고 |
|---|---|---|---|---|
| REQ-FUNC-019 | UI_DIRECT | SCR-003 | IMPLEMENT | 호텔 탭 입력 폼 |
| REQ-FUNC-020 | UI_STATE | SCR-003 | IMPLEMENT | 국가별 지역 옵션 제한 로직 |
| REQ-FUNC-021 | UI_STATE | SCR-003 | IMPLEMENT | 날짜 검증 로직 |
| REQ-FUNC-022 | UI_DIRECT | SCR-003 | IMPLEMENT | 요약 표시 |
| REQ-FUNC-023 | UI_DIRECT | SCR-003 | IMPLEMENT | 비전달 고지 문구 |
| REQ-FUNC-024 | UI_DIRECT | SCR-003 | IMPLEMENT | `호텔 보러 가기` 외부 이동 버튼 |
| REQ-FUNC-025 | NON_UI | N/A | IMPLEMENT | 서버 미저장 제약 |
| REQ-FUNC-026 | UI_DIRECT | SCR-003 | IMPLEMENT | 외부 이동 오류·입력값 보존 상태 |

### 3.4 F4. Travel Mate — REQ-FUNC-027~045

| ID | UI 분류 | Screen | PROJECT_SCOPE | 비고 |
|---|---|---|---|---|
| REQ-FUNC-027 | UI_STATE | SCR-003 | IMPLEMENT | 쓰기 진입 가드, 미충족 시 SCR-005 로그인으로 이동 |
| REQ-FUNC-028 | UI_STATE | SCR-005 | IMPLEMENT | 성인 확인 상태 저장, 동행 작성 진입 시 SCR-003에서 게이트 체크(027) |
| REQ-FUNC-029 | UI_DIRECT | SCR-005 | IMPLEMENT | 프로필 탭 입력 필드 |
| REQ-FUNC-030 | UI_DIRECT | SCR-004 | IMPLEMENT | 동행 필터 바 |
| REQ-FUNC-031 | UI_DIRECT | SCR-003 | IMPLEMENT | 동행 작성 폼 |
| REQ-FUNC-032 | UI_STATE | SCR-003 | IMPLEMENT | 연락처 패턴 탐지 로직 |
| REQ-FUNC-033 | UI_STATE | SCR-004 | IMPLEMENT | 응답 데이터에서 연락처 제외(리스트/상세 공통) |
| REQ-FUNC-034 | UI_DIRECT | SCR-004 | IMPLEMENT | 동행 상세 패널의 참가 요청 폼 |
| REQ-FUNC-035 | UI_STATE | SCR-004 | IMPLEMENT | 중복 요청 차단 로직 |
| REQ-FUNC-036 | UI_DIRECT | SCR-005 | IMPLEMENT | 내 활동 탭의 승인/거절 버튼 |
| REQ-FUNC-037 | UI_STATE | SCR-004 | IMPLEMENT | 조회 시 종료일 기준 자동 마감 계산(내 활동 목록에도 반영) |
| REQ-FUNC-038 | UI_DIRECT | SCR-005 | IMPLEMENT | 내 활동 탭에서 진입, 편집 폼은 SCR-003 동행 작성 폼 재사용 |
| REQ-FUNC-039 | UI_DIRECT | SCR-004 | IMPLEMENT | 신고 버튼·모달 |
| REQ-FUNC-040 | UI_DIRECT | SCR-004 | IMPLEMENT | 차단 버튼, 차단 목록 관리는 SCR-005 내 활동 |
| REQ-FUNC-041 | UI_DIRECT | SCR-005 | IMPLEMENT(축소) | 간단 관리자 탭 신고 목록 |
| REQ-FUNC-042 | UI_DIRECT | SCR-005 | IMPLEMENT(축소) | 간단 관리자 탭 신고 처리 버튼 |
| REQ-FUNC-043 | UI_DIRECT | 전역(Toast) | IMPLEMENT | 상태 변경 알림은 화면에 관계없이 Toast로 노출 |
| REQ-FUNC-044 | NON_UI | N/A | IMPLEMENT | Supabase RLS 서버측 검증 |
| REQ-FUNC-045 | OPERATIONS | N/A | EXCLUDED | 탈퇴 시 30일 삭제·법적 보존 예외 프로세스 |

### 3.5 F5. Country Safety — REQ-FUNC-046~056

| ID | UI 분류 | Screen | PROJECT_SCOPE | 비고 |
|---|---|---|---|---|
| REQ-FUNC-046 | NON_UI | N/A | IMPLEMENT | 해외 국가 안전정보 커버리지 데이터 검증 |
| REQ-FUNC-047 | UI_DIRECT | SCR-001 | IMPLEMENT | 안전정보 Drawer 8개 카테고리 섹션 |
| REQ-FUNC-048 | UI_DIRECT | SCR-001 | IMPLEMENT | 출처·최종 확인일 표시 |
| REQ-FUNC-049 | UI_DIRECT | SCR-001 | IMPLEMENT | 외교부 원문 링크 버튼 |
| REQ-FUNC-050 | UI_STATE | SCR-001 | IMPLEMENT | 렌더링 시 stale 계산 및 경고 표시 로직 |
| REQ-FUNC-051 | UI_DIRECT | SCR-001 | IMPLEMENT | 중대 경보 상단 라벨 |
| REQ-FUNC-052 | UI_DIRECT | SCR-001 | IMPLEMENT | 국가/지역 범위 표시 |
| REQ-FUNC-053 | UI_DIRECT | SCR-001 | IMPLEMENT | 긴급연락처 표시 |
| REQ-FUNC-054 | UI_DIRECT | SCR-001 | IMPLEMENT | 안전정보 고지 문구(SCR-003 항공 요약에도 동일 고지 노출) |
| REQ-FUNC-055 | OPERATIONS | N/A | EXCLUDED | Editor/Admin 안전 콘텐츠 작성·검수·게시 워크플로 |
| REQ-FUNC-056 | OPERATIONS | N/A | EXCLUDED | 안전정보 변경 이력 보존 |

### 3.6 F6. About free_traveler — REQ-FUNC-057~063

| ID | UI 분류 | Screen | PROJECT_SCOPE | 비고 |
|---|---|---|---|---|
| REQ-FUNC-057 | UI_DIRECT | SCR-002 | IMPLEMENT | 대표명·수치 카드 |
| REQ-FUNC-058 | UI_DIRECT | SCR-002 | IMPLEMENT | 소개문·철학·편집 원칙 |
| REQ-FUNC-059 | UI_DIRECT | SCR-002 | IMPLEMENT | 방문 권역 지도/국가 목록 |
| REQ-FUNC-060 | UI_DIRECT | SCR-002 | IMPLEMENT | 여행 타임라인 |
| REQ-FUNC-061 | UI_STATE | SCR-002 | IMPLEMENT | 대표 이미지 alt/출처 속성 |
| REQ-FUNC-062 | UI_DIRECT | SCR-002 | IMPLEMENT | 문의·SNS 링크(빈 값 미노출) |
| REQ-FUNC-063 | UI_DIRECT | SCR-002 | IMPLEMENT | 추천 여행지 6곳 → SCR-001 상세 Drawer 연결 |

### 3.7 F7. Common, Admin, Governance — REQ-FUNC-064~080

| ID | UI 분류 | Screen | PROJECT_SCOPE | 비고 |
|---|---|---|---|---|
| REQ-FUNC-064 | UI_DIRECT | 전역(내비게이션/푸터) | IMPLEMENT | 5개 Screen 공통 내비게이션 |
| REQ-FUNC-065 | UI_STATE | 전역 | IMPLEMENT | 반응형 레이아웃 규칙(320px~데스크톱) |
| REQ-FUNC-066 | UI_DIRECT | SCR-005 | IMPLEMENT | 로그인/가입 탭 |
| REQ-FUNC-067 | UI_DIRECT | SCR-001 | IMPLEMENT | 통합 검색(여행지·안전정보) |
| REQ-FUNC-068 | UI_DIRECT | SCR-001 | IMPLEMENT | 즐겨찾기 버튼(목록은 SCR-005 내 활동에도 노출) |
| REQ-FUNC-069 | UI_DIRECT | SCR-001 | IMPLEMENT | 공유 버튼(SCR-004 동행 상세에도 동일 적용) |
| REQ-FUNC-070 | NON_UI | 전역 | IMPLEMENT | 페이지별 SEO 메타데이터(비시각) |
| REQ-FUNC-071 | NON_UI | N/A | EXCLUDED | 행동 분석 이벤트 스키마 |
| REQ-FUNC-072 | OPERATIONS | N/A | EXCLUDED | Editor/Admin 여행지 콘텐츠 CRUD |
| REQ-FUNC-073 | OPERATIONS | N/A | EXCLUDED | 미디어 업로드·라이선스 입력 워크플로 |
| REQ-FUNC-074 | NON_UI | N/A | IMPLEMENT(대체) | 정적 데이터 완전성 검증 스크립트/테스트 |
| REQ-FUNC-075 | OPERATIONS | N/A | EXCLUDED | 안전정보 stale 대시보드 |
| REQ-FUNC-076 | OPERATIONS | N/A | EXCLUDED | 관리자 변경·신고 처리 감사 로그 |
| REQ-FUNC-077 | UI_DIRECT | SCR-005 | IMPLEMENT | 간단 관리자 탭 외부 URL 설정 |
| REQ-FUNC-078 | UI_DIRECT | 전역(오류 화면) | IMPLEMENT | 404/500/권한없음/외부연결실패 복구 버튼 |
| REQ-FUNC-079 | UI_STATE | 전역 | IMPLEMENT | 시맨틱 HTML/ARIA 규칙 |
| REQ-FUNC-080 | UI_DIRECT | SCR-003 | IMPLEMENT | 동행 작성 시 안전수칙 동의(정책 페이지는 전역 푸터에서 접근) |

---

## 4. REQ-NF 매핑 (34개)

### 4.1 Performance — REQ-NF-001~007

| ID | UI 분류 | Screen | PROJECT_SCOPE | 비고 |
|---|---|---|---|---|
| REQ-NF-001 | NON_UI | N/A | EXCLUDED | LCP RUM 측정 |
| REQ-NF-002 | NON_UI | N/A | EXCLUDED | INP RUM 측정 |
| REQ-NF-003 | NON_UI | N/A | EXCLUDED | CLS RUM 측정 |
| REQ-NF-004 | UI_STATE | SCR-001 | IMPLEMENT(축소) | 필터 응답 속도(SCR-004 동행 필터에도 동일 적용) |
| REQ-NF-005 | NON_UI | N/A | IMPLEMENT(축소) | 쓰기 API 응답 속도 |
| REQ-NF-006 | UI_STATE | 전역 | IMPLEMENT | 이미지 반응형·지연 로딩 |
| REQ-NF-007 | OPERATIONS | N/A | EXCLUDED | Lighthouse CI 성능 게이트 |

### 4.2 Reliability and Recovery — REQ-NF-008~011

| ID | UI 분류 | Screen | PROJECT_SCOPE | 비고 |
|---|---|---|---|---|
| REQ-NF-008 | OPERATIONS | N/A | EXCLUDED | 월간 가용성 SLA |
| REQ-NF-009 | OPERATIONS | N/A | EXCLUDED | 내부 API 5xx 비율 모니터링 |
| REQ-NF-010 | OPERATIONS | N/A | EXCLUDED | DB 백업 RPO/RTO |
| REQ-NF-011 | OPERATIONS | N/A | EXCLUDED | 외부 링크 주 1회 자동 검사 |

### 4.3 Security and Privacy — REQ-NF-012~018

| ID | UI 분류 | Screen | PROJECT_SCOPE | 비고 |
|---|---|---|---|---|
| REQ-NF-012 | NON_UI | N/A | IMPLEMENT | TLS 1.2+ |
| REQ-NF-013 | NON_UI | N/A | IMPLEMENT | 인증·역할·RLS 서버 검증 |
| REQ-NF-014 | NON_UI | N/A | IMPLEMENT | CSRF 방어·SameSite 쿠키 |
| REQ-NF-015 | NON_UI | N/A | IMPLEMENT | 입력 검증·저장 XSS 방지 |
| REQ-NF-016 | NON_UI | N/A | IMPLEMENT | 비밀키 환경변수 관리 |
| REQ-NF-017 | NON_UI | N/A | IMPLEMENT | 항공·호텔 원시 입력값 서버 미보존 |
| REQ-NF-018 | OPERATIONS | N/A | EXCLUDED | 개인정보 내보내기·탈퇴·삭제 요청 흐름 |

### 4.4 Safety and Moderation — REQ-NF-019~022

| ID | UI 분류 | Screen | PROJECT_SCOPE | 비고 |
|---|---|---|---|---|
| REQ-NF-019 | UI_STATE | SCR-004 | IMPLEMENT(축소) | 신고 접수 응답 속도 |
| REQ-NF-020 | OPERATIONS | N/A | EXCLUDED | 신고 1차 검토 24h SLA |
| REQ-NF-021 | NON_UI | N/A | EXCLUDED | 글·요청·신고 속도 제한(rate limit) |
| REQ-NF-022 | OPERATIONS | N/A | EXCLUDED | Moderator 조치 감사 로그 추적성 |

### 4.5 Accessibility — REQ-NF-023~025

| ID | UI 분류 | Screen | PROJECT_SCOPE | 비고 |
|---|---|---|---|---|
| REQ-NF-023 | UI_STATE | 전역 | IMPLEMENT | WCAG 2.2 AA 목표 마크업 규칙 |
| REQ-NF-024 | OPERATIONS | N/A | EXCLUDED | axe 자동 접근성 검사 CI 게이트 |
| REQ-NF-025 | OPERATIONS | N/A | EXCLUDED | 키보드·스크린리더 정식 수동 검사 프로세스 |

### 4.6 Content, Freshness, SEO, Copyright — REQ-NF-026~030

| ID | UI 분류 | Screen | PROJECT_SCOPE | 비고 |
|---|---|---|---|---|
| REQ-NF-026 | NON_UI | N/A | IMPLEMENT | 여행지 콘텐츠 완전성 검증 |
| REQ-NF-027 | NON_UI | N/A | IMPLEMENT | 안전정보 커버리지 검증 |
| REQ-NF-028 | OPERATIONS | N/A | IMPLEMENT(축소) | 안전정보 최신성 95% 목표(계산 로직은 FUNC-050) |
| REQ-NF-029 | OPERATIONS | N/A | EXCLUDED | 미디어 라이선스 메타데이터 100% |
| REQ-NF-030 | NON_UI | 전역 | IMPLEMENT | 공개 페이지 SEO 메타데이터 |

### 4.7 Maintainability, Monitoring, Cost — REQ-NF-031~034

| ID | UI 분류 | Screen | PROJECT_SCOPE | 비고 |
|---|---|---|---|---|
| REQ-NF-031 | OPERATIONS | N/A | IMPLEMENT | TypeScript strict/lint/단위테스트 CI 게이트 |
| REQ-NF-032 | OPERATIONS | N/A | EXCLUDED | 구조화 로그 |
| REQ-NF-033 | OPERATIONS | N/A | EXCLUDED | 핵심 오류 알림 |
| REQ-NF-034 | OPERATIONS | N/A | IMPLEMENT | MVP 월 인프라 비용 목표 |

---

## 5. 총계 검증

| 구분 | 개수 |
|---|---:|
| REQ-FUNC-001~080 | 80 |
| REQ-NF-001~034 | 34 |
| **합계** | **114** |

### 5.1 UI 분류별 개수

| 분류 | 개수 |
|---|---:|
| UI_DIRECT | 49 |
| UI_STATE | 20 |
| NON_UI | 22 |
| OPERATIONS | 23 |
| **합계** | **114** |

### 5.2 Screen별 배치 개수 (전역·N/A 포함 전체 114개 기준)

| Screen | 배치된 Requirement 수 |
|---|---:|
| SCR-001 `/` | 21 |
| SCR-002 `/about` | 7 |
| SCR-003 `/travel-tools` | 18 |
| SCR-004 `/mates` | 8 |
| SCR-005 `/account` | 8 |
| 전역(내비게이션/Toast/레이아웃/오류화면/ARIA 등 공통 규칙) | 9 |
| NON_UI / OPERATIONS(화면 없음, N/A) | 43 |

> Screen 수는 5개로 고정되어 있으며, "전역"은 5개 Screen 모두에 적용되는 공통 규칙을 표시하는 용도일 뿐 별도 Screen이 아니다. EXCLUDED로 표시된 요구사항은 화면 배치 여부와 무관하게 이번 구현 범위에 포함하지 않는다.

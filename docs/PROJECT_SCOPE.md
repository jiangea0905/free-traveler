# Project Scope — Free Traveler MVP 구현 범위

**Document ID:** SCOPE-TRAVEL-001
**Revision:** 1.0
**작성일:** 2026-09-11
**기반 문서:** `docs/01_PRD.md`, `docs/02_SRS_BASELINE.md`
**적용 대상:** 현재 `app/` (Next.js App Router, `src/app`, `src/data`)

이 문서는 `02_SRS_BASELINE.md`의 REQ-FUNC-001~080, REQ-NF-001~034를 이번 구현 주기에서 어떻게 처리할지 정의한다. 두 가지 상태만 사용한다.

- **IMPLEMENT** — 직접 구현하고 테스트로 확인한다.
- **EXCLUDED** — 이번 구현 범위에서 만들지 않는다. 제외 이유를 함께 기록한다.

SRS의 요구사항 ID는 삭제하지 않는다. 범위를 줄이는 요구사항도 표에 남기고 EXCLUDED로 분류한다.

---

## 1. 반드시 직접 구현하는 범위

| # | 항목 | 구현 내용 |
|---|---|---|
| 1 | 핵심 화면 4개 + 보조 화면 1개 | 핵심: 여행지(검색·필터·상세), 항공·호텔 입력, 동행 찾기, 국가 안전정보. 보조: `free_traveler` 대표 소개. 이 외 인증·마이페이지·관리자 화면은 위 5개 화면을 지원하는 부속 화면으로 함께 구현한다. |
| 2 | 여행지 검색·필터와 상세 패널 | `src/data` 정적 데이터 기반 목록·필터·검색·상세 콘텐츠 |
| 3 | 국가 안전정보 패널 | `src/data` 정적 데이터, 렌더링 시 stale(7일 초과) 계산 |
| 4 | free_traveler 대표 소개 | `src/data` 정적 프로필 데이터 |
| 5 | 항공·숙소 입력·검증·요약·외부 이동 | 클라이언트 상태만 사용, 서버 미저장, 새 탭 `noopener,noreferrer` |
| 6 | Supabase 이메일 인증과 성인 확인 | 이메일 가입·로그인·로그아웃, `is_adult`/`adult_verified_at`만 저장 |
| 7 | 동행글 작성·조회·수정·마감 | 작성·수정·수동 마감, 조회 시 종료일 기준 자동 마감 판정 |
| 8 | 참가 요청·승인·거절 | PENDING/ACCEPTED/REJECTED 상태 전이 |
| 9 | 간단한 차단·신고 | 사용자 차단·해제, 신고 접수(사유 코드) |
| 10 | 내 활동과 간단한 관리자 탭 | 내 글/요청/차단 목록, 관리자는 신고 상태 변경과 외부 URL 설정만 처리 |
| 11 | Playwright 핵심 Smoke Test | 5개 화면 진입, 항공·호텔 외부 이동, 동행글 작성~참가 요청 흐름 |
| 12 | Vercel 배포 | 환경변수로 외부 URL·Supabase 키 관리 |

---

## 2. 구현 방식

| 영역 | 방식 |
|---|---|
| 여행지·안전·대표 콘텐츠 | `src/data`의 정적 TypeScript/JSON 데이터로 관리한다. 별도 CMS나 관리자 CRUD 화면을 만들지 않는다. |
| 즐겨찾기 | `localStorage`에 여행지 ID 목록으로 저장한다. 서버 동기화·다중 기기 동기화는 하지 않는다. |
| 알림 | 실제 이메일 발송 없이 Toast 또는 화면 내 상태(배지, 목록 갱신)로 대체한다. |
| 동행글 자동 마감 | 배치/크론 작업 없이, 목록·상세 조회 시점에 `end_date`를 오늘과 비교해 계산한다. |
| 안전정보 최신성(stale) | 배치 작업 없이, 렌더링 시점에 `verified_at`과 오늘 날짜의 차이를 계산해 7일 초과 여부를 표시한다. |
| 이미지 | 일반 인터넷 URL과 `alt` 텍스트만 사용한다. 라이선스 승인·다운로드 메타데이터 관리 기능은 만들지 않는다. |
| 관리자 기능 | 신고 상태 변경(RESOLVED/DISMISSED, 글 숨김)과 항공·호텔 외부 URL 설정만 다룬다. 그 외 관리자 기능은 만들지 않는다. |

---

## 3. 제외 기능과 이유

| 제외 기능 | 이유 |
|---|---|
| 전체 콘텐츠 CMS | 콘텐츠는 `src/data` 정적 데이터로 충분히 관리 가능하며, 편집자용 CRUD·워크플로 UI는 이번 범위에서 불필요한 복잡도다. |
| 미디어 업로드·라이선스 승인 워크플로 | 이미지는 일반 URL·alt 텍스트만 사용하므로 업로드·라이선스 심사 파이프라인이 필요하지 않다. |
| 범용 감사 로그 | 별도 로깅 인프라 없이도 신고 상태·글 상태는 DB 값으로 확인 가능하며, 변경 이력 보존은 운영 인력이 배정된 이후 단계의 과제다. |
| 자동 백업·장애 알림·부하 테스트 | 운영 모니터링·인프라 조직이 없는 현재 단계에서 구축·유지 비용이 기대 효과보다 크다. |
| 외부 이메일 사업자 연동 | 알림은 Toast/화면 상태로 대체 가능하며, 이메일 발송 사업자 연동은 별도 계약·비용이 필요하다. |
| EC2·AWS 인프라 | Vercel + Supabase 조합으로 배포·운영이 가능하므로 별도 서버 인프라를 두지 않는다. |
| 무인 자동 Merge Runner | 변경 검토와 병합은 사람이 직접 수행한다. |

---

## 4. 기능 요구사항(REQ-FUNC) 커버리지

### 4.1 F1. Destination Guide (REQ-FUNC-001~010)

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-FUNC-001 | IMPLEMENT | 국내/해외 탭으로 `src/data` 목록을 분리 표시 | Playwright: 탭 전환 후 구분값 검증 |
| REQ-FUNC-002 | IMPLEMENT | 국가·도시·계절·테마·기간 필터를 AND 조건 클라이언트 필터로 구현 | 단위 테스트로 필터 조합 결과 검증 |
| REQ-FUNC-003 | IMPLEMENT | 여행지명·국가명·테마 키워드 부분 일치 검색 | 단위 테스트: 한글 부분 일치, 결과 없음 케이스 |
| REQ-FUNC-004 | IMPLEMENT | 상세 페이지 필수 필드(소개·명소·시기·일정·예산·교통·음식·에티켓·출처·수정일)를 정적 데이터 스키마로 강제 | 데이터 스키마 검증 테스트(필수 필드 누락 시 실패) |
| REQ-FUNC-005 | IMPLEMENT | 필터 결과 0건 시 안내 문구와 초기화 버튼 표시 | Playwright: 조건 조합으로 빈 결과 유도 후 확인 |
| REQ-FUNC-006 | IMPLEMENT | 해외 상세의 `countryCode`로 안전정보 페이지 링크 연결 | 단위 테스트: 여행지-국가 코드 일치 검증 |
| REQ-FUNC-007 | IMPLEMENT | 정적 데이터에 `alt`, `source`, `author` 텍스트 필드로 관리(라이선스 승인 절차 없음) | 데이터 스키마 검증 테스트 |
| REQ-FUNC-008 | IMPLEMENT | 국내 10곳 이상, 해외 15개국 30개 도시 이상을 데이터 시드로 충족 | 데이터 수량 검증 테스트 |
| REQ-FUNC-009 | IMPLEMENT | 상세 하단 같은 국가·테마 관련 여행지 최대 6개 표시 | 단위 테스트: 추천 목록 개수·중복 제외 |
| REQ-FUNC-010 | IMPLEMENT | 허용된 필터 값만 URL query에 반영, 새로고침 시 복원 | Playwright: URL 공유 후 필터 복원 확인 |

### 4.2 F2. Flight Link-out (REQ-FUNC-011~018)

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-FUNC-011 | IMPLEMENT | 국가·지역·출발일·귀국일 필수 입력 필드 구현 | Playwright: 미입력 시 오류 표시 |
| REQ-FUNC-012 | IMPLEMENT | 국가 변경 시 지역 옵션 필터링 및 기존 선택값 초기화 | 단위 테스트 |
| REQ-FUNC-013 | IMPLEMENT | 과거 출발일·역전 날짜 클라이언트 검증 후 진행 차단 | 단위 테스트: 경계값 |
| REQ-FUNC-014 | IMPLEMENT | 유효 입력 후 요약 단계에 값 유지(세션 상태) | Playwright: 수정 후 재확인 |
| REQ-FUNC-015 | IMPLEMENT | 폼·요약에 입력값 비전달 고지 문구 표시 | Playwright: 문구 노출 확인 |
| REQ-FUNC-016 | IMPLEMENT | 설정된 외부 URL을 `noopener,noreferrer` 새 탭으로 열기, query 미부착 | Playwright: 새 탭 URL 검증 |
| REQ-FUNC-017 | IMPLEMENT | 입력값을 클라이언트 상태로만 보관, 서버 요청·저장 없음 | 네트워크 탭/코드 리뷰로 서버 전송 부재 확인 |
| REQ-FUNC-018 | IMPLEMENT | 외부 URL 미설정 시 이동 차단, 오류 메시지와 재시도 버튼 표시(운영 로그는 콘솔 수준) | Playwright: URL 미설정 상태 오류 노출 |

### 4.3 F3. Hotel Link-out (REQ-FUNC-019~026)

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-FUNC-019 | IMPLEMENT | 국가·지역·체크인·체크아웃 필수 입력 구현 | Playwright: 미입력 오류 표시 |
| REQ-FUNC-020 | IMPLEMENT | 국가 변경 시 지역 옵션 재계산 | 단위 테스트 |
| REQ-FUNC-021 | IMPLEMENT | 과거 체크인·체크인≥체크아웃 검증 후 차단 | 단위 테스트: 경계값 |
| REQ-FUNC-022 | IMPLEMENT | 요약 값이 입력값과 정확히 일치하도록 표시 | Playwright: 값 대조 |
| REQ-FUNC-023 | IMPLEMENT | 폼·요약에 비전달 고지 표시 | Playwright: 문구 노출 확인 |
| REQ-FUNC-024 | IMPLEMENT | 설정된 호텔 외부 URL을 새 탭 `noopener,noreferrer`로 열기 | Playwright: 새 탭 URL 검증 |
| REQ-FUNC-025 | IMPLEMENT | 입력값 서버 미저장(클라이언트 상태만) | 코드 리뷰·네트워크 탭 확인 |
| REQ-FUNC-026 | IMPLEMENT | URL 오류 시 이동 차단, 입력값 유지, 오류 표시 | Playwright: 오류 상태에서 입력값 보존 확인 |

### 4.4 F4. Travel Mate (REQ-FUNC-027~045)

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-FUNC-027 | IMPLEMENT | Supabase Auth 세션 필요, 비회원 쓰기 요청 차단 | Playwright: 비로그인 상태에서 작성 시도 차단 확인 |
| REQ-FUNC-028 | IMPLEMENT | 성인 확인 체크박스 동의 시 `is_adult`, `adult_verified_at`만 저장(생년월일 미저장) | DB 스키마 확인, 단위 테스트 |
| REQ-FUNC-029 | IMPLEMENT | 닉네임·연령대·여행 스타일 필수, 성별 선택 항목 폼 구현 | Playwright: 필수값 검증 |
| REQ-FUNC-030 | IMPLEMENT | 국가·지역·기간 겹침·연령대·성별·스타일·모집 상태 필터, 차단 사용자 글 제외 | 단위 테스트: 필터 조합, 차단 제외 |
| REQ-FUNC-031 | IMPLEMENT | 제목·국가·지역·기간·인원·선호조건·스타일·설명·안전수칙 동의 입력 폼 | Playwright: 필수값·날짜 역전 차단 |
| REQ-FUNC-032 | IMPLEMENT | 정규식 기반 전화번호·이메일·메신저 ID 패턴 탐지 후 제출 차단 | 단위 테스트: 탐지 케이스셋 |
| REQ-FUNC-033 | IMPLEMENT | 응답 데이터에 이메일·전화번호 등 연락처 필드 미포함 | 단위 테스트: 응답 스키마 검사 |
| REQ-FUNC-034 | IMPLEMENT | 모집중 글에 최대 500자 비공개 메시지로 참가 요청 제출 | Playwright: 요청 제출·PENDING 저장 확인 |
| REQ-FUNC-035 | IMPLEMENT | 동일 사용자·동일 글의 중복 PENDING/ACCEPTED 요청을 DB 유니크 제약과 UI 오류로 차단 | 단위 테스트: 중복 요청 시도 |
| REQ-FUNC-036 | IMPLEMENT | 글 작성자만 요청을 ACCEPTED/REJECTED로 변경 가능 | Playwright: 비작성자 변경 시도 차단 확인 |
| REQ-FUNC-037 | IMPLEMENT | 배치 작업 없이 조회 시점에 `end_date` 경과 여부를 계산해 CLOSED로 표시 | 단위 테스트: 종료일 경과 케이스 |
| REQ-FUNC-038 | IMPLEMENT | 작성자의 수동 마감·수정·삭제 기능 구현(승인 요청자 존재 시 경고 문구만 표시, 별도 알림 발송 없음) | Playwright: 수정·마감 흐름 |
| REQ-FUNC-039 | IMPLEMENT | 사유 코드·설명으로 글/사용자/요청 신고 접수, 접수 ID 즉시 표시 | Playwright: 신고 접수 후 ID 노출 확인 |
| REQ-FUNC-040 | IMPLEMENT | 사용자 차단·해제, 차단 후 상호 글·프로필·요청 미노출 | 단위 테스트: 차단 관계 필터링 |
| REQ-FUNC-041 | IMPLEMENT(축소) | 관리자 탭에 신고 목록과 상태(OPEN/RESOLVED/DISMISSED)만 표시. 우선순위·증거 첨부·담당자 배정 큐는 만들지 않는다 | Playwright: 관리자 탭에서 신고 목록·상태 변경 확인 |
| REQ-FUNC-042 | IMPLEMENT(축소) | 관리자가 신고를 RESOLVED/DISMISSED로 전환하고 해당 글을 숨김 처리하는 기능만 구현. 경고·계정 일시 제한 조치는 만들지 않는다 | Playwright: 신고 처리 후 글 숨김 확인 |
| REQ-FUNC-043 | IMPLEMENT | 요청 접수·승인·거절·신고 처리 결과를 Toast/화면 상태 배지로 표시(이메일 발송 없음) | Playwright: 상태 변경 후 알림 표시 확인 |
| REQ-FUNC-044 | IMPLEMENT | Supabase RLS로 본인 글·요청, 작성자, Admin만 비공개 데이터 접근 허용 | Supabase RLS 정책 테스트 |
| REQ-FUNC-045 | EXCLUDED | 회원 탈퇴 시 30일 내 개인정보 삭제와 법적 보존 예외 판단 절차는 감사 로그·운영 프로세스가 필요해 이번 범위에서 제외한다. 계정 삭제 자체는 Supabase Auth 기본 기능으로 대체한다 | 해당 없음 |

### 4.5 F5. Country Safety (REQ-FUNC-046~056)

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-FUNC-046 | IMPLEMENT | 소개되는 해외 국가 전체에 안전정보 정적 데이터 1건 이상 시드 | 데이터 수량 검증 테스트 |
| REQ-FUNC-047 | IMPLEMENT | 치안·사기·법규·교통·재난·보건·문화·긴급연락처 8개 카테고리를 데이터 스키마로 강제 | 데이터 스키마 검증 테스트 |
| REQ-FUNC-048 | IMPLEMENT | 각 안전정보에 출처명·URL·최종 확인일 필드 포함 | 데이터 스키마 검증 테스트 |
| REQ-FUNC-049 | IMPLEMENT | 외교부 해외안전여행 원문 링크를 새 탭 `noopener,noreferrer`로 제공 | Playwright: 링크 클릭 시 새 탭 확인 |
| REQ-FUNC-050 | IMPLEMENT | 렌더링 시점에 `verified_at` 기준 7일 초과 여부 계산해 재확인 경고 표시 | 단위 테스트: 날짜 경계값 |
| REQ-FUNC-051 | IMPLEMENT | 중대 경보 단계를 본문 상단에 텍스트 라벨로 표시(색상 단독 사용 금지) | Playwright: 경보 라벨 상단 노출 확인 |
| REQ-FUNC-052 | IMPLEMENT | 국가 전체/지역 범위를 `scope_type`, `scope_text` 데이터 필드로 구분 표시 | 데이터 스키마 검증 테스트 |
| REQ-FUNC-053 | IMPLEMENT | 현지 긴급전화·영사콜센터 정보를 데이터 필드로 표시 | 데이터 스키마 검증 테스트 |
| REQ-FUNC-054 | IMPLEMENT | 안전 페이지·항공 요약에 공식 판단 대체 불가 고지 문구 표시 | Playwright: 문구 노출 확인 |
| REQ-FUNC-055 | EXCLUDED | Editor/Admin의 안전 콘텐츠 작성·검수·게시 워크플로는 CMS 제외에 따라 만들지 않는다. 콘텐츠는 개발자가 `src/data`를 직접 수정한다 | 해당 없음 |
| REQ-FUNC-056 | EXCLUDED | 변경 이력(이전/새 값·사유·담당자) 보존은 감사 로그 제외에 따라 구현하지 않는다. 이력은 git 커밋 기록으로 대체한다 | 해당 없음 |

### 4.6 F6. About free_traveler (REQ-FUNC-057~063)

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-FUNC-057 | IMPLEMENT | 대표명·`50+ Trips`·`30+ Countries`를 단일 정적 데이터 소스에서 참조 | 단위 테스트: 홈/About 값 일치 |
| REQ-FUNC-058 | IMPLEMENT | 확정 소개문·철학·편집 원칙을 정적 데이터로 표시 | Playwright: 텍스트 노출 확인 |
| REQ-FUNC-059 | IMPLEMENT | 30개국 이상 방문 국가 목록/지도를 정적 데이터로 표시 | 데이터 수량 검증 테스트 |
| REQ-FUNC-060 | IMPLEMENT | 여행 타임라인(연도·장소·요약)을 정적 데이터로 표시 | 데이터 스키마 검증 테스트 |
| REQ-FUNC-061 | IMPLEMENT | 대표 이미지에 `alt`·출처 텍스트 필드 포함(라이선스 승인 절차 없음) | 데이터 스키마 검증 테스트 |
| REQ-FUNC-062 | IMPLEMENT | 문의·SNS 링크를 정적 데이터로 관리(관리자 UI 없음), 빈 값은 미노출 | 단위 테스트: 빈 링크 미노출 |
| REQ-FUNC-063 | IMPLEMENT | 추천 여행지 6곳을 공개 여행지 상세로 연결 | 단위 테스트: 링크 유효성 |

### 4.7 F7. Common, Admin, Governance (REQ-FUNC-064~080)

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-FUNC-064 | IMPLEMENT | 전역 내비게이션·푸터로 5개 화면 2회 이내 이동 보장 | Playwright: 내비게이션 클릭 경로 확인 |
| REQ-FUNC-065 | IMPLEMENT | Tailwind 반응형 레이아웃(320px~데스크톱) | Playwright: 모바일 뷰포트 렌더 확인 |
| REQ-FUNC-066 | IMPLEMENT | Supabase Auth 이메일 가입·인증·로그인·로그아웃·재설정 | Playwright: 가입~로그인 흐름 |
| REQ-FUNC-067 | IMPLEMENT | 정적 데이터 기반 여행지·안전정보 통합 키워드 검색 | 단위 테스트: 검색 결과 라벨 |
| REQ-FUNC-068 | IMPLEMENT | 즐겨찾기 추가/해제/조회를 `localStorage`로 구현, 중복 방지 | 단위 테스트: 중복 추가 방지 |
| REQ-FUNC-069 | IMPLEMENT | Web Share API 시도 후 실패 시 URL 클립보드 복사 폴백 | Playwright: 공유 버튼 동작 확인 |
| REQ-FUNC-070 | IMPLEMENT | Next.js Metadata API로 title/description/canonical/OG 제공 | 단위 테스트: 메타데이터 존재 확인 |
| REQ-FUNC-071 | EXCLUDED | 행동 분석 이벤트 스키마·수집 파이프라인은 분석 인프라가 없어 이번 범위에서 제외한다 | 해당 없음 |
| REQ-FUNC-072 | EXCLUDED | Editor/Admin의 여행지 콘텐츠 CRUD·미리보기 화면은 CMS 제외에 따라 만들지 않는다 | 해당 없음 |
| REQ-FUNC-073 | EXCLUDED | 미디어 업로드 시 출처·라이선스 필수 입력 워크플로는 미디어 업로드 제외에 따라 만들지 않는다. 이미지는 URL과 alt 텍스트만 정적 데이터에 기록한다 | 해당 없음 |
| REQ-FUNC-074 | IMPLEMENT(대체) | 런타임 게시 게이트 대신, 정적 데이터 필수 필드 검증 스크립트/테스트로 완전성을 확인한다 | 빌드/CI 단계 데이터 검증 테스트 |
| REQ-FUNC-075 | EXCLUDED | 안전정보 stale 현황·검토 담당자 대시보드는 "간단한 관리자 탭"(신고 상태·외부 URL만) 범위 밖이라 만들지 않는다 | 해당 없음 |
| REQ-FUNC-076 | EXCLUDED | 관리자 변경·신고 처리·권한 변경 감사 로그는 범용 감사 로그 제외에 따라 만들지 않는다 | 해당 없음 |
| REQ-FUNC-077 | IMPLEMENT | Admin이 항공·호텔 외부 URL을 HTTPS 허용값으로만 설정하는 간단한 설정 화면/환경변수 구현 | Playwright: 잘못된 URL(HTTP/javascript) 저장 차단 확인 |
| REQ-FUNC-078 | IMPLEMENT | 404/500/권한없음/외부연결실패 화면에 홈·이전·재시도 중 최소 1개 동작 제공 | Playwright: 각 오류 화면 진입 후 복구 버튼 확인 |
| REQ-FUNC-079 | IMPLEMENT | 폼·모달·탭·알림에 시맨틱 HTML과 기본 ARIA 속성 적용 | Playwright: 키보드 포커스 이동 기본 확인 |
| REQ-FUNC-080 | IMPLEMENT | 이용약관·개인정보 처리방침·동행 안전수칙·콘텐츠 면책 페이지 제공, 동행글 작성 시 안전수칙 동의 시각 저장 | Playwright: 동의 없이 제출 차단 확인 |

---

## 5. 비기능 요구사항(REQ-NF) 커버리지

### 5.1 Performance (REQ-NF-001~007)

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-NF-001 | EXCLUDED | LCP p75 실사용자 측정(RUM)은 별도 분석 인프라가 필요해 제외한다. 정적 데이터·경량 이미지로 체감 성능만 확보한다 | 해당 없음 |
| REQ-NF-002 | EXCLUDED | INP 실사용자 측정(RUM)은 분석 인프라 제외에 따라 만들지 않는다 | 해당 없음 |
| REQ-NF-003 | EXCLUDED | CLS 실사용자 측정(RUM)은 분석 인프라 제외에 따라 만들지 않는다 | 해당 없음 |
| REQ-NF-004 | IMPLEMENT(축소) | 정적 데이터 기반 클라이언트 필터로 즉시 응답을 구현한다. 동시 사용자 50명 부하 테스트를 통한 수치 검증은 제외한다 | Playwright: 필터 클릭 후 결과 렌더링 수동 확인 |
| REQ-NF-005 | IMPLEMENT(축소) | Supabase 쓰기 호출의 일반적인 응답 속도로 대응한다. 별도 부하 테스트는 제외한다 | Playwright: 글/요청/신고 제출 응답 시간 수동 확인 |
| REQ-NF-006 | IMPLEMENT | Next.js `Image` 컴포넌트로 반응형·지연 로딩 적용 | 코드 리뷰: `Image` 사용 여부 |
| REQ-NF-007 | EXCLUDED | 배포 전 Lighthouse CI 성능 게이트는 CI 파이프라인 구축 범위 밖이라 제외한다 | 해당 없음 |

### 5.2 Reliability and Recovery (REQ-NF-008~011)

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-NF-008 | EXCLUDED | 월간 가용성 99.5% 측정은 업타임 모니터링 인프라가 필요해 제외한다 | 해당 없음 |
| REQ-NF-009 | EXCLUDED | 내부 API 5xx 비율 측정은 모니터링·알림 인프라 제외에 따라 만들지 않는다 | 해당 없음 |
| REQ-NF-010 | EXCLUDED | DB 백업 RPO/RTO 목표는 "자동 백업" 제외에 따라 다루지 않는다. Supabase 기본 백업 정책을 그대로 사용한다 | 해당 없음 |
| REQ-NF-011 | EXCLUDED | 외부 링크 주 1회 자동 검사는 "장애 알림" 인프라 제외에 따라 만들지 않는다. Playwright 스모크 테스트 실행 시점에만 링크 유효성을 확인한다 | Playwright 실행 로그 |

### 5.3 Security and Privacy (REQ-NF-012~018)

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-NF-012 | IMPLEMENT | Vercel 기본 HTTPS/TLS 1.2+ 사용 | 배포 URL의 HTTPS 확인 |
| REQ-NF-013 | IMPLEMENT | Supabase RLS 정책과 서버측 역할 검증 적용 | RLS 정책 테스트 |
| REQ-NF-014 | IMPLEMENT | Supabase Auth 기본 SameSite 쿠키, Next.js Server Action 기본 CSRF 방어 사용 | 코드 리뷰: 쿠키 설정 확인 |
| REQ-NF-015 | IMPLEMENT | React 자동 이스케이프 + 입력 검증(zod 등)으로 저장 XSS 차단 | 단위 테스트: 스크립트 입력 케이스 |
| REQ-NF-016 | IMPLEMENT | 비밀키는 환경변수로만 관리, 클라이언트 번들 미포함 | 빌드 산출물에서 키 문자열 검색 |
| REQ-NF-017 | IMPLEMENT | 항공·호텔 입력값은 클라이언트 상태로만 유지, 서버·분석 미전송 | 네트워크 탭/코드 리뷰 확인 |
| REQ-NF-018 | EXCLUDED | 개인정보 내보내기·탈퇴·삭제 요청 전체 흐름은 감사 로그·운영 프로세스가 필요해 제외한다(REQ-FUNC-045 참고) | 해당 없음 |

### 5.4 Safety and Moderation (REQ-NF-019~022)

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-NF-019 | IMPLEMENT(축소) | Supabase insert 호출의 일반적인 응답 속도로 대응, 별도 부하 테스트는 제외 | Playwright: 신고 제출 응답 수동 확인 |
| REQ-NF-020 | EXCLUDED | 신고 1차 검토 24시간 90% SLA는 운영 인력·모니터링 체계가 필요해 제외한다. 관리자 탭은 상태 변경 기능만 제공한다 | 해당 없음 |
| REQ-NF-021 | EXCLUDED | 글·요청·신고 속도 제한(rate limit) 미들웨어는 "간단한 차단·신고" 범위 밖이라 만들지 않는다 | 해당 없음 |
| REQ-NF-022 | EXCLUDED | Moderator 조치의 감사 로그 추적성은 범용 감사 로그 제외에 따라 만들지 않는다 | 해당 없음 |

### 5.5 Accessibility (REQ-NF-023~025)

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-NF-023 | IMPLEMENT | WCAG 2.2 AA를 설계 목표로 시맨틱 HTML·ARIA 기본 적용(공식 인증 절차는 없음) | 코드 리뷰: 시맨틱 마크업 확인 |
| REQ-NF-024 | EXCLUDED | axe 자동 접근성 검사 CI 게이트는 별도 파이프라인 구축이 필요해 제외한다 | 해당 없음 |
| REQ-NF-025 | EXCLUDED | 정식 키보드·스크린리더 수동 검사 프로세스는 도입하지 않는다. Playwright 스모크 테스트에서 핵심 흐름의 키보드 포커스만 기본 확인한다 | 해당 없음 |

### 5.6 Content, Freshness, SEO, Copyright (REQ-NF-026~030)

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-NF-026 | IMPLEMENT | 여행지 정적 데이터 필수 필드 검증 스크립트/테스트로 완전성 확인 | 데이터 검증 테스트 |
| REQ-NF-027 | IMPLEMENT | 소개된 해외 국가 전체에 안전정보 데이터 존재를 검증 테스트로 확인 | 데이터 검증 테스트 |
| REQ-NF-028 | IMPLEMENT(축소) | stale 계산·경고 로직을 구현·테스트한다. 실제 7일 이내 95% 최신성 유지는 콘텐츠 운영 책임이며 코드 범위 밖이다 | 단위 테스트: stale 경계값 |
| REQ-NF-029 | EXCLUDED | 미디어 라이선스 메타데이터(작가·라이선스 유형·URL·다운로드일) 100% 관리는 미디어 업로드·라이선스 워크플로 제외에 따라 제외한다. 이미지는 URL·alt 텍스트만 관리한다 | 해당 없음 |
| REQ-NF-030 | IMPLEMENT | Next.js Metadata API로 공개 페이지 SEO 메타데이터 제공 | 단위 테스트: 메타데이터 누락 확인 |

### 5.7 Maintainability, Monitoring, Cost (REQ-NF-031~034)

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-NF-031 | IMPLEMENT | TypeScript strict, ESLint, 핵심 로직 단위 테스트를 병합 전 통과 조건으로 운영 | CI: `lint`, `build`, 단위 테스트 실행 |
| REQ-NF-032 | EXCLUDED | 구조화 로그(request_id 등) 시스템은 별도 로깅 인프라가 필요해 제외한다. 콘솔 로그 수준으로 대체한다 | 해당 없음 |
| REQ-NF-033 | EXCLUDED | 5xx 비율·외부 링크 실패 자동 알림은 "장애 알림" 제외에 따라 만들지 않는다 | 해당 없음 |
| REQ-NF-034 | IMPLEMENT | Vercel·Supabase 무료/저비용 티어 사용으로 월 인프라 비용 목표(콘텐츠 인건비 제외 10만원 이하) 충족 | 사용 중인 요금제 확인 |

---

## 6. 요약

- REQ-FUNC-001~080: IMPLEMENT 65건(일부 축소·대체 포함), EXCLUDED 15건(REQ-FUNC-045, 055, 056, 071, 072, 073, 075, 076 등).
- REQ-NF-001~034: IMPLEMENT 17건(일부 축소 포함), EXCLUDED 17건.
- EXCLUDED로 분류된 요구사항은 모두 1절의 12개 구현 범위와 3절의 제외 기능 목록에서 근거를 찾을 수 있다.

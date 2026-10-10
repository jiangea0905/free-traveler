# UI Contract — Free Traveler (Next.js App Router)

**기반 문서:** `docs/03_UI_COVERAGE_ANALYSIS.md`, `docs/04_UIUX_PLAN.md`, `docs/STITCH_VALIDATION_REPORT.md`, `design-reference/D-001/DESIGN.md`
**대응 파일:** `design-reference/SCREEN_ROUTE_CONTRACT.json` (기계 판독용 동일 계약)

이 문서는 승인된 5개 Screen(SCR-001~005)을 `src/app` App Router 구현이 지켜야 할 계약으로 옮긴다. 여기 적힌 순서·상태·이동·금지 사항은 `D-001/DESIGN.md`가 LOCKED 상태인 동안 임의로 바꾸지 않는다.

---

## SCR-001 — 메인

| 항목 | 내용 |
|---|---|
| **Screen ID** | SCR-001 |
| **Route** | `/` |
| **Page Entry** | `src/app/page.tsx` |
| **구분** | 핵심(Core) |
| **영역 순서** | Header → ① 검색 Hero(검색창 + `/travel-tools` CTA) → ② 국내 인기 여행지 Card Grid(6) → ③ 해외 인기 여행지 Card Grid(6) → ④ 여행 동기 Chip(6) → ⑤ 국가별 주의사항 Card Grid(6) → ⑥ 최근 동행글(3) 또는 완성형 Empty State → ⑦ free_traveler 요약 → Footer |
| **주요 Component** | `search-bar`, `destination-card`(국내/해외), `chip`/`chip-active`, `advisory-badge`, `mate-post-card`(소형), 여행지 상세 Drawer, 국가 안전정보 Drawer, `button-primary`(Hero CTA), Empty State 블록 |
| **상태** | Loading(Card Grid 스켈레톤), Success, Empty(필터 결과 0건 → 조건 완화 안내+초기화 버튼; 최근 동행글 0건 → 완성형 Empty State), Error(섹션별 로드 실패 배너+다시 시도) — Unauthorized 해당 없음(전체 공개) |
| **사용자 행동** | 통합 검색·필터 적용, 테마 Chip 선택, 여행지 Card 클릭(같은 화면에서 상세 Drawer 오픈), 안전정보 Drawer로 전환, 즐겨찾기 토글, 동행글 카드 클릭 |
| **다른 화면으로의 이동** | Hero CTA → SCR-003 `/travel-tools` · 최근 동행글 "모두 보기"/작성 CTA → SCR-004 `/mates` · free_traveler 요약 CTA → SCR-002 `/about` · 로그인/즐겨찾기 확인 → SCR-005 `/account` |
| **Desktop·Mobile 규칙** | Desktop 1440px: Card Grid 3열×2행, Hero 480~560px(다음 섹션 제목이 첫 화면에 보여야 함). Mobile 390px 변형 존재 — Card 1열, Header는 로고+햄버거, 터치 영역 44px 이상 |
| **금지 기능** | Airbnb 상표 요소, 여행지 예약·결제 UI, 별점/리뷰 점수, 실시간 항공권·호텔 가격 표시, 광고 배너, Lorem ipsum/"준비 중"/"정보 확인 필요" 문구, 빈 Card |

## SCR-002 — 대표 소개

| 항목 | 내용 |
|---|---|
| **Screen ID** | SCR-002 |
| **Route** | `/about` |
| **Page Entry** | `src/app/about/page.tsx` |
| **구분** | 보조(Auxiliary) |
| **영역 순서** | Header → ① Hero(대표 사진+소개 문장) → ② 여행 지표(50+ Trips/30+ Countries) → ③ 소개·철학(2~4문단, 좌우 분할) → ④ 여행 Timeline(6개 이상) → ⑤ 방문 국가(30개, 권역별 Chip) → ⑥ 여행 Gallery(8장 이상) → ⑦ 기억에 남는 여행지(4) + CTA Banner → Footer |
| **주요 Component** | Hero(사진+텍스트 split), 통계 Card, Timeline(세로형), 권역별 `chip` 그룹, Gallery Card Grid, 추천 여행지 `destination-card`(4), CTA Banner(2버튼) |
| **상태** | Loading(사진·Timeline 스켈레톤), Success — Empty/Unauthorized 해당 없음(정적 콘텐츠는 항상 채워져 있음), Error(이미지 로드 실패 시 alt 텍스트 노출 대체 박스) |
| **사용자 행동** | Timeline/Gallery 스크롤 열람, 추천 여행지 Card 클릭, 하단 CTA 클릭, 문의·SNS 링크 클릭(외부 새 탭) |
| **다른 화면으로의 이동** | 추천 여행지 Card → SCR-001 `/` 상세 Drawer 딥링크 · CTA Banner "여행 조건 정리하기" → SCR-003 `/travel-tools` · "동행 찾아보기" → SCR-004 `/mates` |
| **Desktop·Mobile 규칙** | Desktop 1440px만 승인 대상(이번 Mobile 변형 범위 밖). Section 콘텐츠 최대 폭 1200~1280px, 상하 여백 64~96px |
| **금지 기능** | Airbnb 상표 요소, 예약·결제 UI, 별점/리뷰, 실시간 가격, 광고, Lorem ipsum류 placeholder, 빈 Card, 방문 국가 30개 미만·Timeline 6개 미만·Gallery 8장 미만으로 축소 |

## SCR-003 — 통합 여행 준비

| 항목 | 내용 |
|---|---|
| **Screen ID** | SCR-003 |
| **Route** | `/travel-tools` |
| **Page Entry** | `src/app/travel-tools/page.tsx` |
| **구분** | 핵심(Core) |
| **영역 순서** | Header → ① Intro(목적+이용 3단계) → ② 탭 내비게이션(항공편/숙소/동행 구하기) → ③ 입력 Form(탭별 국가·지역·날짜) → ④ 요약+외부이동 Action Card → ⑤ 비전달 고지+Tip 3개 → ⑥ 동행 탭 콘텐츠(로그인 유도 배너 또는 작성 Form+안전 안내) → Footer |
| **주요 Component** | `tab-bar`/`tab-active`, `text-input`, 요약 Action Card, `button-primary`(외부 이동), Inline Alert(비전달 고지, 게스트 안내), 3단계 안내 리스트, 동행 작성 Form |
| **상태(탭별 독립)** | 항공편/숙소: Loading(외부 이동 처리 중), Success(요약+새 탭 오픈), Error(날짜 검증 오류, 외부 URL 미설정 오류) — Empty/Unauthorized 해당 없음. 동행 구하기: Loading(제출 처리 중), Success(작성 완료 후 이동), Error(연락처 패턴 감지·필수값 오류), Unauthorized(비로그인/미성년 → 로그인 유도 배너) |
| **사용자 행동** | 탭 전환, 국가·지역·날짜 입력, 요약 확인 후 외부 사이트 이동(새 탭), 동행글 작성 제출, 로그인 유도 배너의 로그인 버튼 클릭 |
| **다른 화면으로의 이동** | 항공/호텔 CTA → 외부 사이트(새 탭, `noopener,noreferrer`) · 동행 작성 완료 → SCR-004 `/mates` · 미인증 액션 → SCR-005 `/account` |
| **Desktop·Mobile 규칙** | Desktop 1440px, Mobile 390px 변형 모두 승인 대상. 세 탭은 각각 독립된 입력·검증·완료 상태를 가지며 탭 전환 시 다른 탭 상태를 지우지 않는다. Mobile은 탭을 풀폭 세그먼트 컨트롤로, Form 필드는 세로 1열로 배치 |
| **금지 기능** | 항공·호텔 실시간 검색 결과·가격 비교·예약·결제 UI, 입력값의 외부 URL 쿼리·서버 전송, Airbnb 상표 요소, Lorem ipsum류 placeholder |

## SCR-004 — 동행 조회

| 항목 | 내용 |
|---|---|
| **Screen ID** | SCR-004 |
| **Route** | `/mates` |
| **Page Entry** | `src/app/mates/page.tsx` |
| **구분** | 핵심(Core) |
| **영역 순서** | Header → ① Intro+작성 CTA → ② 검색 Filter+결과 요약 → ③ 동행글 Card 목록(최대 8, 데이터 있을 때) → ④ Desktop 목록+상세 분할 / Mobile 목록→상세 Drawer → ⑤ 동행 신청 방법 3단계 → ⑥ 안전·신고·차단 안내+CTA → Footer |
| **주요 Component** | Filter Bar, `mate-post-card`, `status-badge-open`/`status-badge-closed`, 상세 패널(참가 요청 Form), 3단계 안내, Inline Alert(안전 안내), Modal(신고/차단 확인) |
| **상태** | Loading(목록/상세 스켈레톤), Success, Empty(조건에 맞는 글 없음 → 완성형 Empty State: 안내 문장+필터 초기화+작성 CTA+이용 방법), Error(신청 실패·중복 요청·네트워크 오류), Unauthorized(신청/작성 시도 시 로그인·성인 확인 유도) |
| **사용자 행동** | 필터 적용, Card 클릭(상세 오픈: Desktop 분할/Mobile Drawer), 참가 요청 메시지 제출, 신고·차단 실행 |
| **다른 화면으로의 이동** | 작성 CTA → SCR-003 `/travel-tools` 동행 탭 · 안전 안내 "항공·숙소 준비하기" → SCR-003 `/travel-tools` · 요청/글 관리·차단 목록 관리 → SCR-005 `/account` 내 활동 · 미인증 액션 → SCR-005 `/account` 로그인 |
| **Desktop·Mobile 규칙** | Desktop 1440px: 목록 40%(`lg:col-span-5`)+상세 60%(`lg:col-span-7`) 좌우 분할. Mobile 390px: 목록 1열 → Card 선택 시 하단 Drawer로 상세 오픈(이번 잠금 범위는 Desktop만 승인, Mobile은 이 규칙을 그대로 적용해 후속 구현) |
| **금지 기능** | 동행글/카드에 전화번호·이메일·메신저 ID 등 공개 연락처 노출, 실시간 위치 공유·실시간 채팅·영상통화, 미성년자 동행, Airbnb 상표 요소, 별점/리뷰, Lorem ipsum류 placeholder |

## SCR-005 — 계정·관리

| 항목 | 내용 |
|---|---|
| **Screen ID** | SCR-005 |
| **Route** | `/account` |
| **Page Entry** | `src/app/account/page.tsx` |
| **구분** | 핵심(Core) |
| **영역 순서(역할별, 고정 Section 수 없음)** | Guest: Intro → 로그인/가입/재설정 Card → 로그인 후 가능한 기능 → 보안 안내. Member: 탭[프로필, 내 활동] → 프로필 요약+수정 Form / 내 활동(새 글 작성 CTA + 내 글·받은 요청·즐겨찾기·차단 4블록). Admin: 탭[프로필, 내 활동, 관리자] → 관리자 Intro + 신고 상태 변경 목록 + 외부 URL 설정 Form |
| **주요 Component** | `tab-bar`(역할에 없는 탭은 렌더링하지 않음), 로그인/가입/재설정 Card, 프로필 Form, 내 활동 4블록 리스트(Empty State 포함), Toast(상태 변경 알림), 관리자 신고 목록+상태 Select, 외부 URL 설정 Form |
| **상태** | Guest: Loading(로그인 처리 중), Success(로그인 성공 전환), Error(로그인 실패·이메일 중복). Member 프로필: Loading, Success, Error(수정 실패). Member 내 활동: Loading, Success, Empty(블록별 완성형 Empty State+CTA), Error(로드/처리 실패), Unauthorized(비회원 직접 접근 → Guest 뷰로 대체). Admin: Loading, Success, Empty(처리할 신고 없음), Error(상태 변경 실패, 잘못된 URL 저장 차단), Unauthorized(권한 없음 → 관리자 탭 미노출, 직접 접근 시 권한 없음 안내) |
| **사용자 행동** | 로그인/가입/비밀번호 재설정, 프로필 수정, 성인 확인, 내 글 수정/마감, 참가 요청 승인/거절, 즐겨찾기 항목 이동, 차단 해제, 신고 상태 변경, 외부 URL 저장 |
| **다른 화면으로의 이동** | 즐겨찾기 항목 클릭 → SCR-001 `/` 상세 Drawer · 내 글/요청 항목 클릭 → SCR-004 `/mates` 상세 · 새 동행글 작성 CTA → SCR-003 `/travel-tools` 동행 탭 |
| **Desktop·Mobile 규칙** | Desktop 1440px만 승인 대상. 관리자 탭에는 차트·KPI·복잡한 Dashboard를 만들지 않고 목록+상태 변경 UI로 한정 |
| **금지 기능** | 관리자 Dashboard/통계 차트, 회원 개인정보 노출 범위 확대, 감사 로그 UI, 콘텐츠 CMS(여행지/안전정보 CRUD), 미디어 업로드·라이선스 워크플로, Airbnb 상표 요소, Lorem ipsum류 placeholder |

---

## 공통 규칙 (5개 Screen 전체)

- Header/Footer는 5개 Screen 모두 동일 컴포넌트를 공유한다(`D-001/DESIGN.md` §Header·Footer).
- "여행 준비" 관련 CTA/내비게이션은 예외 없이 `/travel-tools`로 연결한다(내부 앵커 `#prep`, 오타 경로 `/prep` 금지 — `STITCH_VALIDATION_REPORT.md`에서 발견된 실결함).
- 화면 간 이동은 전체 페이지 새로고침이 아닌 Next.js App Router 네비게이션(`<Link>`/`useRouter`)으로 처리한다.
- API Route, 인증 콜백, 404/500 처리 등 기술 Route는 Screen 수에 포함하지 않는다(`SCREEN_ROUTE_CONTRACT.json`의 `technical_routes` 참고).

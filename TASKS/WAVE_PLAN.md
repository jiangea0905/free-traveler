# Wave Plan — Free Traveler

`scripts/build_waves.py`가 `TASKS/TASK_MANIFEST.csv`의 Depends On 그래프로부터 생성했다. 
Wave ID는 이 파일이 정본이다 — `.claude/commands/run-wave.md`/`prepare-task.md`는 이 파일을 그대로 읽는다.

| Wave | Group | Task ID | Preview Checkpoint After |
|---|---|---|---|
| W01 | 1. Scaffold, 문서, Harness 확인 | SETUP-DEPENDENCIES | N |
| W02 | 2. Airbnb 스타일 공통 UI, 정적 데이터, Layout | DATA-DESTINATIONS | N |
| W02 | 2. Airbnb 스타일 공통 UI, 정적 데이터, Layout | DATA-REPRESENTATIVE | N |
| W02 | 2. Airbnb 스타일 공통 UI, 정적 데이터, Layout | DATA-SAFETY | N |
| W02 | 2. Airbnb 스타일 공통 UI, 정적 데이터, Layout | SHARED-CONTACT-FILTER | N |
| W02 | 2. Airbnb 스타일 공통 UI, 정적 데이터, Layout | SHARED-EXTERNAL-LINKOUT | N |
| W02 | 2. Airbnb 스타일 공통 UI, 정적 데이터, Layout | SHARED-FAVORITES-LOCALSTORAGE | N |
| W02 | 2. Airbnb 스타일 공통 UI, 정적 데이터, Layout | SHARED-HEADER-FOOTER | N |
| W03 | 2. Airbnb 스타일 공통 UI, 정적 데이터, Layout | SHARED-A11Y-FOCUS | N |
| W03 | 2. Airbnb 스타일 공통 UI, 정적 데이터, Layout | SHARED-ERROR-PAGES | N |
| W03 | 2. Airbnb 스타일 공통 UI, 정적 데이터, Layout | SHARED-NOTIFICATION-TOAST | N |
| W03 | 2. Airbnb 스타일 공통 UI, 정적 데이터, Layout | SHARED-POLICY-CONSENT | N |
| W03 | 2. Airbnb 스타일 공통 UI, 정적 데이터, Layout | SHARED-SEO-PERFORMANCE | N |
| W03 | 2. Airbnb 스타일 공통 UI, 정적 데이터, Layout | SHARED-SHARE-LINK | N |
| W04 | 3. Supabase Auth, 6개 Table, 기본 RLS(+백엔드 API) | DB-SCHEMA-BASE | N |
| W05 | 3. Supabase Auth, 6개 Table, 기본 RLS(+백엔드 API) | DB-ACCESS | N |
| W05 | 3. Supabase Auth, 6개 Table, 기본 RLS(+백엔드 API) | DB-RLS-BASE | N |
| W06 | 3. Supabase Auth, 6개 Table, 기본 RLS(+백엔드 API) | API-ADMIN | N |
| W06 | 3. Supabase Auth, 6개 Table, 기본 RLS(+백엔드 API) | API-APPLICATIONS | N |
| W06 | 3. Supabase Auth, 6개 Table, 기본 RLS(+백엔드 API) | API-AUTH | N |
| W06 | 3. Supabase Auth, 6개 Table, 기본 RLS(+백엔드 API) | API-BLOCKS-REPORTS | N |
| W06 | 3. Supabase Auth, 6개 Table, 기본 RLS(+백엔드 API) | API-MATES | N |
| W06 | 3. Supabase Auth, 6개 Table, 기본 RLS(+백엔드 API) | DB-SEED-BASE | N |
| W06 | 3. Supabase Auth, 6개 Table, 기본 RLS(+백엔드 API) | TEST-RLS-BASIC | N |
| W07 | 4. SCR-001 메인 Component와 Page Owner | COMP-SCR001-DESTINATION-DRAWER | N |
| W07 | 4. SCR-001 메인 Component와 Page Owner | COMP-SCR001-MATES-PROFILE-TEASER | N |
| W07 | 4. SCR-001 메인 Component와 Page Owner | COMP-SCR001-SAFETY | N |
| W07 | 4. SCR-001 메인 Component와 Page Owner | COMP-SCR001-SEARCH-DESTINATIONS | N |
| W07 | 4. SCR-001 메인 Component와 Page Owner | PAGE-SCR001 | Y |
| W08 | 5. SCR-002 대표 소개 Component와 Page Owner | COMP-SCR002-GALLERY-RECOMMENDED | N |
| W08 | 5. SCR-002 대표 소개 Component와 Page Owner | COMP-SCR002-PROFILE-HERO | N |
| W08 | 5. SCR-002 대표 소개 Component와 Page Owner | COMP-SCR002-TIMELINE-COUNTRIES | N |
| W08 | 5. SCR-002 대표 소개 Component와 Page Owner | PAGE-SCR002 | Y |
| W09 | 6. SCR-003 여행 입력·외부 이동·동행글 입력 Component와 Page Owner | COMP-SCR003-FLIGHT-FORM | N |
| W09 | 6. SCR-003 여행 입력·외부 이동·동행글 입력 Component와 Page Owner | COMP-SCR003-HOTEL-FORM | N |
| W09 | 6. SCR-003 여행 입력·외부 이동·동행글 입력 Component와 Page Owner | COMP-SCR003-MATE-COMPOSER | N |
| W09 | 6. SCR-003 여행 입력·외부 이동·동행글 입력 Component와 Page Owner | PAGE-SCR003 | Y |
| W10 | 7. SCR-004 동행 목록·상세·신청 Component와 Page Owner | COMP-SCR004-APPLY | N |
| W10 | 7. SCR-004 동행 목록·상세·신청 Component와 Page Owner | COMP-SCR004-BLOCK | N |
| W10 | 7. SCR-004 동행 목록·상세·신청 Component와 Page Owner | COMP-SCR004-DETAIL | N |
| W10 | 7. SCR-004 동행 목록·상세·신청 Component와 Page Owner | COMP-SCR004-FILTER | N |
| W10 | 7. SCR-004 동행 목록·상세·신청 Component와 Page Owner | COMP-SCR004-LIST | N |
| W10 | 7. SCR-004 동행 목록·상세·신청 Component와 Page Owner | COMP-SCR004-REPORT | N |
| W10 | 7. SCR-004 동행 목록·상세·신청 Component와 Page Owner | PAGE-SCR004 | Y |
| W11 | 8. SCR-005 계정·내 활동·간단 관리자 Component와 Page Owner | COMP-SCR005-ADMIN | N |
| W11 | 8. SCR-005 계정·내 활동·간단 관리자 Component와 Page Owner | COMP-SCR005-AUTH | N |
| W11 | 8. SCR-005 계정·내 활동·간단 관리자 Component와 Page Owner | COMP-SCR005-MY-ACTIVITY | N |
| W11 | 8. SCR-005 계정·내 활동·간단 관리자 Component와 Page Owner | COMP-SCR005-PROFILE | N |
| W11 | 8. SCR-005 계정·내 활동·간단 관리자 Component와 Page Owner | PAGE-SCR005 | Y |
| W12 | 9. Unit·Playwright·접근성·CI | CI-DATA-VALIDATION | N |
| W12 | 9. Unit·Playwright·접근성·CI | CI-LINT-BUILD-TEST | N |
| W12 | 9. Unit·Playwright·접근성·CI | E2E-MATE-AUTH | N |
| W12 | 9. Unit·Playwright·접근성·CI | E2E-PUBLIC-SMOKE | N |
| W12 | 9. Unit·Playwright·접근성·CI | E2E-TRAVEL-TOOLS | N |
| W12 | 9. Unit·Playwright·접근성·CI | UNIT-CONTACT-DETECTION | N |
| W12 | 9. Unit·Playwright·접근성·CI | UNIT-MATE-STATE | N |
| W13 | 9. Unit·Playwright·접근성·CI | UNIT-TRAVEL-DATES | N |
| W14 | 10. Vercel Preview와 Release 확인 | MANUAL-SUPABASE-CONFIG | N |
| W14 | 10. Vercel Preview와 Release 확인 | MANUAL-VERCEL-DEPLOY | N |


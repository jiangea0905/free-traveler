---
version: "1.0"
name: Free-Traveler-Design-D-001
description: A white-canvas, photography-led travel-prep hub design system for Free Traveler. Structurally inspired by a generous consumer-marketplace layout (single accent color used sparingly, one shallow shadow tier, soft rounded cards, dense photo grids under a restrained hero), but with its own coral accent, its own type scale on Inter, and none of the source's brand colors, wordmarks, or booking/payment UI. This document is the locked visual and structural reference for the 5 approved screens (SCR-001~SCR-005, with SCR-001/SCR-003 Mobile variants) built in Stitch project `7876118700864225182`.

colors:
  canvas: "#ffffff"
  surface-soft: "#f7f7f8"
  surface-strong: "#f1f2f4"
  ink: "#22262b"
  body: "#4b5159"
  muted: "#6b7280"
  hairline: "#e4e6e9"
  border-strong: "#c7cbd1"
  coral: "#ff6f5e"
  coral-active: "#e85742"
  coral-disabled: "#ffd9d2"
  coral-tint: "#fff1ee"
  info: "#2563eb"
  success: "#187f4e"
  caution: "#b45309"
  caution-bg: "#fff6e9"
  warning: "#c2410c"
  warning-bg: "#fff0e6"
  danger: "#b3261e"
  danger-bg: "#fdedec"
  scrim: "#111318"

typography:
  display-xl:
    fontFamily: "Inter, 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', system-ui, sans-serif"
    fontSize: 32px
    fontWeight: 700
    lineHeight: 1.25
  display-lg:
    fontFamily: "Inter, 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', system-ui, sans-serif"
    fontSize: 26px
    fontWeight: 700
    lineHeight: 1.3
  title-lg:
    fontFamily: "Inter, 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', system-ui, sans-serif"
    fontSize: 20px
    fontWeight: 600
    lineHeight: 1.4
  title-md:
    fontFamily: "Inter, 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', system-ui, sans-serif"
    fontSize: 17px
    fontWeight: 600
    lineHeight: 1.45
  body-md:
    fontFamily: "Inter, 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', system-ui, sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
  body-sm:
    fontFamily: "Inter, 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', system-ui, sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.45
  caption:
    fontFamily: "Inter, 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', system-ui, sans-serif"
    fontSize: 13px
    fontWeight: 500
    lineHeight: 1.4
  button:
    fontFamily: "Inter, 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', system-ui, sans-serif"
    fontSize: 16px
    fontWeight: 600
    lineHeight: 1.25

rounded:
  sm: 8px
  md: 12px
  lg: 16px
  xl: 20px
  full: 9999px

spacing:
  xxs: 2px
  xs: 4px
  sm: 8px
  md: 12px
  base: 16px
  lg: 24px
  xl: 32px
  xxl: 48px
  section-desktop-min: 64px
  section-desktop-max: 96px
  section-mobile-min: 40px
  section-mobile-max: 64px

components:
  button-primary:
    backgroundColor: "{colors.coral}"
    textColor: "#ffffff"
    typography: "{typography.button}"
    rounded: "{rounded.sm}"
    height: 48px
    padding: 12px 24px
  button-primary-active:
    backgroundColor: "{colors.coral-active}"
    textColor: "#ffffff"
    rounded: "{rounded.sm}"
  button-primary-disabled:
    backgroundColor: "{colors.coral-disabled}"
    textColor: "#ffffff"
    rounded: "{rounded.sm}"
  button-secondary:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    border: "1px solid {colors.hairline}"
    typography: "{typography.button}"
    rounded: "{rounded.sm}"
    height: 48px
  search-bar:
    backgroundColor: "{colors.canvas}"
    border: "1px solid {colors.hairline}"
    rounded: "{rounded.full}"
    height: 56px
    padding: 12px 20px
  text-input:
    backgroundColor: "{colors.canvas}"
    border: "1px solid {colors.hairline}"
    rounded: "{rounded.sm}"
    height: 48px
    padding: 12px 14px
  text-input-focus:
    border: "2px solid {colors.ink}"
  chip:
    backgroundColor: "{colors.surface-strong}"
    textColor: "{colors.body}"
    rounded: "{rounded.full}"
    padding: 8px 16px
    height: 36px
  chip-active:
    backgroundColor: "{colors.coral-tint}"
    textColor: "{colors.coral}"
    border: "1px solid {colors.coral}"
  tab-bar:
    backgroundColor: "{colors.canvas}"
    border-bottom: "1px solid {colors.hairline}"
  tab-active:
    textColor: "{colors.coral}"
    border-bottom: "2px solid {colors.coral}"
    typography: "{typography.title-md}"
  tab-inactive:
    textColor: "{colors.muted}"
    typography: "{typography.title-md}"
  destination-card:
    backgroundColor: "{colors.canvas}"
    border: "1px solid {colors.hairline}"
    rounded: "{rounded.lg}"
    imageAspectRatio: "4:3"
  mate-post-card:
    backgroundColor: "{colors.canvas}"
    border: "1px solid {colors.hairline}"
    rounded: "{rounded.md}"
    padding: 20px
  status-badge-open:
    backgroundColor: "{colors.coral-tint}"
    textColor: "{colors.coral}"
    rounded: "{rounded.full}"
  status-badge-closed:
    backgroundColor: "{colors.surface-strong}"
    textColor: "{colors.muted}"
    rounded: "{rounded.full}"
  advisory-badge:
    textColor: "{colors.caution}"
    backgroundColor: "{colors.caution-bg}"
    rounded: "{rounded.full}"
  drawer:
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.lg} (top corners on mobile bottom-sheet)"
    shadow: "{elevation.panel}"
  modal:
    backgroundColor: "{colors.canvas}"
    rounded: "{rounded.lg}"
    shadow: "{elevation.panel}"
    scrim: "{colors.scrim} at 50%"
  toast:
    backgroundColor: "{colors.ink}"
    textColor: "#ffffff"
    rounded: "{rounded.sm}"
    padding: 12px 16px
  header:
    backgroundColor: "{colors.canvas}"
    height-desktop: 72px
    height-mobile: 56px
    border-bottom: "1px solid {colors.hairline}"
  footer:
    backgroundColor: "{colors.canvas}"
    border-top: "1px solid {colors.hairline}"
    padding-desktop: 64px 80px
    padding-mobile: 40px 20px
---

## Overview

Free Traveler is a **travel-prep hub**, not a booking or payment product: destination discovery, an outbound flight/hotel condition-planner, a travel-companion board, country safety information, and a curator profile. The canvas is **pure white** (`{colors.canvas}`), the dominant text is a **dark gray ink** (`{colors.ink}` — #22262B, never pure black), and a single **coral** accent (`{colors.coral}` — #FF6F5E) carries every primary CTA, active tab, active chip, and the favorite/save icon. Coral appears on 5–10% of any given screen — most of the page stays white + ink + muted gray, exactly as validated across the 7 approved Stitch screens.

This system is **structurally** inspired by a generous, photography-led marketplace reference (`design-reference/vendor/airbnb/DESIGN.md`): a restrained hero that doesn't fill the viewport, a single shallow shadow tier, soft rounded corners, and a rhythm that alternates open editorial bands with dense photo-card grids. None of that reference's brand color, typeface, wordmark, or booking/reservation UI is reused. Every token in this document is Free Traveler's own.

**Key characteristics (locked, matches the 7 approved Stitch screens):**
- Single accent: coral `#FF6F5E`, used only for primary buttons, active tab/chip state, and save icons.
- One typeface family: **Inter**, paired with a system Korean sans-serif fallback stack (`'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', system-ui, sans-serif`) for localized copy. No second display face, no proprietary/licensed font files — Inter loads from Google Fonts or a self-hosted open-license copy only.
- One shallow shadow tier, used only on hover-floated cards, dropdowns, Drawers, and Modals.
- Soft rounding: `{rounded.sm}` (8px) on buttons/inputs, `{rounded.md}` (12px) on tabs and compact cards, `{rounded.lg}` (16px) on destination/photo cards and Drawer/Modal panels, `{rounded.full}` on search bars, chips, and status badges.
- No hard corners anywhere except the outer page grid.
- Photography-led: every screen carries real-feeling travel photography with place-specific alt text; no stock office/business imagery, no gray placeholder boxes.

## Colors

### Brand & Accent
- **Coral** (`{colors.coral}` — #FF6F5E): the one brand color. Primary CTA fill, active tab underline/label, active chip fill+border, save/favorite icon fill.
- **Coral Active** (`{colors.coral-active}` — #E85742): press/pointer-down state of `button-primary`.
- **Coral Disabled** (`{colors.coral-disabled}` — #FFD9D2): pale tint for disabled primary CTAs.
- **Coral Tint** (`{colors.coral-tint}` — #FFF1EE): background for active chip, `status-badge-open` background.

### Surface
- **Canvas** (`{colors.canvas}` — #FFFFFF): the only page background. No dark mode on the public product.
- **Surface Soft** (`{colors.surface-soft}` — #F7F7F8): Empty State backgrounds, alternating section backgrounds where separation is needed without a hard border.
- **Surface Strong** (`{colors.surface-strong}` — #F1F2F4): inactive chip fill, `status-badge-closed` fill, icon-button backgrounds.

### Hairline & Border
- **Hairline** (`{colors.hairline}` — #E4E6E9): default 1px border — card borders, Header/Footer dividers, input outlines at rest.
- **Border Strong** (`{colors.border-strong}` — #C7CBD1): disabled input outline, secondary-button outline on hover.

### Text
- **Ink** (`{colors.ink}` — #22262B): headlines, primary body text, primary nav labels.
- **Body** (`{colors.body}` — #4B5159): secondary running text inside long-form destination/curator copy.
- **Muted** (`{colors.muted}` — #6B7280): captions, meta rows (dates, counts), inactive tab labels, footer sub-labels.

### Semantic (never the same hue as coral)
- **Info** (`{colors.info}` — #2563EB): inline links, "이 나라 안전정보 보기" style cross-links.
- **Success** (`{colors.success}` — #187F4E): submission confirmations, ACCEPTED status.
- **Caution** (`{colors.caution}` / `{colors.caution-bg}` — #B45309 on #FFF6E9): safety "여행유의" level, stale-data warning.
- **Warning** (`{colors.warning}` / `{colors.warning-bg}` — #C2410C on #FFF0E6): safety "여행자제"/stronger advisory level.
- **Danger** (`{colors.danger}` / `{colors.danger-bg}` — #B3261E on #FDEDEC): form validation errors, "여행금지" advisory level.
- Every semantic color is always paired with a text label (e.g. "여행유의", "최신 정보 재확인 필요") — color is never the only signal.

### Scrim
- **Scrim** (`{colors.scrim}` — #111318 at 50% opacity): Drawer and Modal backdrop.

## Typography

Every text role runs on **Inter**, with the Korean fallback stack loaded for localized copy: `Inter, 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', system-ui, sans-serif`. There is no second display family and no proprietary font file — Inter is pulled from Google Fonts (`fonts.googleapis.com`) or bundled from its open OFL license only.

| Token | Size / Line-height | Weight | Use |
|---|---|---|---|
| `{typography.display-xl}` | 32px / 1.25 | 700 | SCR-001 / SCR-002 Hero headline |
| `{typography.display-lg}` | 26px / 1.3 | 700 | Section `<h2>` titles |
| `{typography.title-lg}` | 20px / 1.4 | 600 | Card titles, Modal/Drawer titles |
| `{typography.title-md}` | 17px / 1.45 | 600 | Tab labels, sub-section `<h3>` |
| `{typography.body-md}` | 16px / 1.5 | 400 | Section description sentences, form labels |
| `{typography.body-sm}` | 14px / 1.45 | 400 | Card meta (dates, counts), Empty State body |
| `{typography.caption}` | 13px / 1.4 | 500 | Badges, timestamps, uppercase eyebrow labels |
| `{typography.button}` | 16px / 1.25 | 600 | Button labels |

Headline weights stay at 600–700 — never a heavier display cut. Photography and real content carry visual weight; type does not shout.

## Spacing

Base unit: **4px**. Tokens: `xxs`2 · `xs`4 · `sm`8 · `md`12 · `base`16 · `lg`24 · `xl`32 · `xxl`48, plus the section-band range below.

- **Section vertical padding — Desktop:** 64–96px (`section-desktop-min/max`). Hero uses 96px; dense Card Grid sections use the tighter 64px end so photo density per scroll stays high.
- **Section vertical padding — Mobile:** 40–64px (`section-mobile-min/max`).
- **Card gutter:** `{spacing.base}` (16px) between Cards in a grid on both Desktop and Mobile.
- **Card internal padding:** `{spacing.lg}` (24px) for `mate-post-card`/Drawer body content; `{spacing.base}` (16px) for `destination-card` meta block.

## Radius

`sm`8px (buttons, inputs) · `md`12px (tabs, compact/status cards) · `lg`16px (destination cards, photo cards, Drawer/Modal panels) · `xl`20px (large feature cards, e.g. SCR-002 recommended-destination cards) · `full`9999px (search bar, chips, status badges, icon buttons). No unrounded (0px) corner appears anywhere except the outer page/section grid.

## Shadow

One shallow elevation tier only, defined once as `{elevation.panel}`:

```
box-shadow: 0 1px 2px rgba(17,19,24,0.06), 0 8px 20px rgba(17,19,24,0.08);
```

Applied only to: Card hover state, dropdown menus, Drawer panels, Modal panels. Every other surface (Header, Footer, section bands, flat cards at rest) is shadow-free. There are no progressive elevation tiers — depth comes from photography, white-on-white separation via `{colors.hairline}` borders, and rounded clipping, not from stacked shadows.

## Header · Footer

Shared verbatim across all 5 Screens (SCR-001~005).

**Header**
- Desktop: 72px height, white, 1px `{colors.hairline}` bottom border. Left: "Free Traveler" text wordmark (no logo mark, no icon lockup). Center: primary nav — 여행지(`/`), 여행 준비(`/travel-tools`), 동행 찾기(`/mates`), 대표 소개(`/about`). Right: signed-out shows a "로그인" `button-secondary`; signed-in shows nickname + avatar linking to `/account`.
- Mobile: 56px height. Left wordmark, right a 44×44px hamburger icon opening a full-screen sheet with the same 4 nav items + auth entry.
- Every "여행 준비" nav link and every CTA that opens the travel-prep tool **must** point to `/travel-tools` — never an in-page anchor (`#prep`) or a stub path (`/prep`). (See Do/Do Not.)

**Footer**
- White background (matches canvas — no contrast band), 1px `{colors.hairline}` top border.
- Desktop padding `64px 80px`, 3 columns: 서비스 (여행지 탐색·항공편 찾기·숙소 찾기·동행 찾기) / 안내 (이용약관·개인정보 처리방침·동행 안전수칙·콘텐츠 이용 안내) / Free Traveler (대표 소개·문의·SNS).
- Mobile padding `40px 20px`, columns collapse to a single stacked list.
- Legal band: one muted `{typography.caption}` line — copyright + a one-sentence outbound/safety disclaimer. No dark footer variant exists.

## Search · Filter

- **Search bar** (`component.search-bar`): full pill shape (`{rounded.full}`), 56px height, white fill, 1px hairline border, placeholder in `{typography.body-md}` muted. Used in the SCR-001 Hero and the SCR-001 통합 검색 feature.
- **Filter bar**: a row of `text-input`/select controls (country, region, period, status) plus a result-count sentence in `{typography.body-sm}` muted (e.g. "조건에 맞는 동행글 12개"). Used on SCR-001 (destination filter) and SCR-004 (mate filter).
- A dedicated **필터 초기화** icon-button (44×44px) always sits beside the filter row; it is the required recovery action for the Empty State (see below).
- Applying a filter never triggers full-page navigation; results update in place under the same Header.

## Destination Card

- `{rounded.lg}` (16px) corner clip, 4:3 photo, `{elevation.panel}` on hover only.
- Beneath the photo: title (`{typography.title-lg}`), one-line hook (`{typography.body-sm}` muted), and a small season/region badge.
- Grid: 3 columns × 2 rows on Desktop (6 cards), 1 column on Mobile — never 2 columns as an intermediate stack; columns reduce, rows never grow to compensate.
- Clicking a card opens the destination Drawer in place — it never navigates to a new page.
- Every photo carries alt text naming the real place shown (e.g. "교토 후시미 이나리 신사의 붉은 도리이 행렬"); decorative icons use `alt=""`.

## Form · Tabs

- **Tab bar** (`component.tab-bar`): white background, 1px bottom hairline. Active tab: coral label + 2px coral underline (`title-md`, 600 weight). Inactive tab: muted label, no underline. Exactly 3 tabs on SCR-003 (항공편 / 숙소 / 동행 구하기) and up to 3 role-based tabs on SCR-005 (프로필 / 내 활동 / 관리자 — 관리자 renders only for the Admin role).
- Each tab owns its **own** input/validation/completion state — switching tabs never clears or merges another tab's in-progress data.
- **Text input** (`component.text-input`): 48px height, `{rounded.sm}`, 1px hairline border, label stacked above in `{typography.caption}` muted. On focus, the border thickens to 2px solid `{colors.ink}` — no glow, no colored ring.
- Inline validation renders directly under the field in `{typography.body-sm}`, using `{colors.danger}` for errors and `{colors.success}` for a passed-check confirmation — never a floating toast for field-level validation.
- Primary submit/CTA buttons inside a form are full-width on Mobile, intrinsic-width on Desktop, and disabled (`button-primary-disabled`) until required fields are valid.

## Mate Post Card

- `{rounded.md}` (12px), 1px hairline border, `{spacing.lg}` (24px) internal padding, no photo required.
- Header row: title (`{typography.title-lg}`) + status badge (`status-badge-open` "모집중" in coral tint, or `status-badge-closed` "마감" in muted gray — text label always present, never a color-only dot).
- Meta row: country + date range + travel-style chips, all `{typography.body-sm}` muted.
- Card never renders a phone number, email, or messenger ID — contact happens only through the private application form inside the Drawer/detail panel.
- List shows up to **8** cards before requiring further filtering; Desktop pairs the list with a live detail panel (`lg:col-span-5` list / `lg:col-span-7` detail split, confirmed in SCR-004); Mobile collapses the detail into a bottom Drawer opened by tapping a card.

## Drawer · Modal

- **Drawer**: used for destination detail, country-safety detail (both from SCR-001), and mate-post detail (from SCR-004 on Mobile). Slides in from the right on Desktop as a fixed-width panel; slides up as a bottom sheet on Mobile. `{rounded.lg}` on the leading corners, `{elevation.panel}` shadow, `{colors.scrim}` backdrop at 50%.
- **Modal**: used for confirmation moments (e.g. report submission, block confirmation). Centered, `{rounded.lg}`, max-width ~480px, same scrim.
- Both are dismissible via an explicit close control, the scrim click, and the `Esc` key; focus is trapped inside while open and returns to the trigger element on close.

## Alert · Toast

- **Inline Alert** (banner form): used for the "입력값은 외부 사이트로 전달되지 않습니다" disclosure, safety advisory-level banners, and the "동행글 작성은 로그인과 성인 인증이 필요합니다" guest banner. Background uses the matching semantic `-bg` token (never coral), `{rounded.sm}`, an icon + text label, optional inline CTA.
- **Toast**: dark `{colors.ink}` fill, white text, `{rounded.sm}`, bottom-center on Mobile / bottom-right on Desktop, auto-dismiss ~4s. Used for transient confirmations only (신청 접수 완료, 승인/거절 처리 완료, 신고 접수 완료) — never for content a user must be able to re-read later (that goes in the relevant list instead).

## Loading · Empty · Error 상태

| 상태 | 규칙 |
|---|---|
| **Loading** | Skeleton blocks matching the final Card/list shape (same radius, same grid) — never a full-page spinner replacing the layout. |
| **Empty** | See the dedicated rule below — every Empty State is a fully designed, finished composition, never a bare blank area. |
| **Error** | An inline message in `{colors.danger}` + `{colors.danger-bg}` with a plain-language cause and a retry/return action (버튼 or link) — never a raw error code alone. |

## Desktop · Mobile 규칙

| 기준 | Desktop | Mobile |
|---|---|---|
| 기준 폭 | 1440px | 390px |
| Section 콘텐츠 최대 폭 | 1200–1280px, 중앙 정렬 | 100% 폭 − 좌우 거터 |
| Section 상하 여백 | 64–96px | 40–64px |
| Card 그리드 열 수 | 3~4열 (콘텐츠에 맞춰 축소, 절대 2열 중간단계로 어중간하게 늘어지지 않음) | 1열 |
| Header 높이 | 72px, 가운데 정렬 내비게이션 노출 | 56px, 로고+햄버거로 축약 |
| Footer 레이아웃 | 3열 | 1열 스택 |
| Drawer 방향 | 우측 고정폭 패널 | 하단 Bottom Sheet |
| 터치 영역 | — | 모든 버튼·탭·Chip·아이콘 버튼 최소 44×44px |
| 포커스 표시 | `:focus-visible`에 2px solid 코랄 아웃라인 + 2px offset (Desktop·Mobile 공통) | 동일 |

## Page Section 최대 폭과 상하 여백

- Desktop 콘텐츠 최대 폭: **1200–1280px**, 뷰포트가 1440px보다 넓어지면 좌우 여백이 남는 여분을 흡수한다.
- Desktop Section 상하 여백: **64~96px** — Hero와 편집형 섹션은 상단 범위(96px)를, 카드 그리드처럼 밀도가 필요한 섹션은 하단 범위(64px)를 사용한다.
- Mobile Section 상하 여백: **40~64px**로 축소하고, Card는 항상 1열로 배치한다.

## Hero 높이와 다음 Section 노출 규칙

- Hero는 1440px Desktop 뷰포트 전체 높이를 차지하지 않는다. 권장 높이는 **480~560px**이며, `100vh`/`h-screen` 클래스를 Hero 자체에 적용하지 않는다(페이지 최상위 `<body>`/래퍼에 대한 `min-h-screen`은 짧은 페이지의 Footer 고정용으로만 허용된다).
- Hero 바로 아래 Section의 제목 일부가 스크롤 없이 뷰포트 안에 보여야 한다 — SCR-001과 SCR-002 모두 이 규칙으로 검증됨(Stitch Validation Report §3-9 참고).
- Hero는 제목 1개, 1~2문장 설명, 그리고 검색창 또는 주요 CTA 중 최소 하나를 포함한다.

## Section별 제목·설명·본문·CTA 계층과 시각적 리듬

모든 Section은 다음 4단 계층을 갖는다: **① 제목**(`{typography.display-lg}`, 필요 시 상단에 `{typography.caption}` uppercase eyebrow 라벨) → **② 설명 1~3문장**(`{typography.body-md}` 또는 `body-sm`, muted) → **③ 실제 본문**(Card Grid / 좌우 분할 / Chip 목록 / Timeline / 3단계 안내 중 하나) → **④ 명확한 CTA 또는 다음 행동**(버튼, 링크, 또는 그 Section 자체가 CTA인 배너).

시각적 리듬은 같은 패턴을 연달아 반복하지 않는다. 한 페이지 안에서 Hero, Card Grid, 좌우 분할(텍스트+이미지), Chip 목록, 번호 매긴 3단계 안내, CTA Banner를 교차 배치해 스크롤할 때마다 구성이 달라지도록 한다.

## 화면별 Section 순서와 최소 콘텐츠 수 (승인된 Stitch 화면 기준, 고정값)

| Screen | Section 순서 | 최소 콘텐츠 수 |
|---|---|---|
| **SCR-001** `/` | Hero(검색+CTA) → 국내 인기 여행지 → 해외 인기 여행지 → 여행 동기 Chip → 국가별 주의사항 → 최근 동행글(또는 완성형 Empty State) → free_traveler 요약 | 국내 여행지 **6**, 해외 여행지 **6**, 테마 Chip **6**, 안전 국가 **6**, 최근 동행글 **3**(또는 Empty State) |
| **SCR-002** `/about` | Hero → 여행 지표 → 소개·철학 → Timeline → 방문 국가 → Gallery → 추천 여행지+CTA | Timeline **6개 이상** 시점, 방문 국가 **30개**(권역별 그룹), Gallery **8장 이상**, 추천 여행지 **4개** |
| **SCR-003** `/travel-tools` | Intro(3단계) → 3개 탭 → 입력 Form → 요약+외부이동 Action Card → 비전달 고지+팁 → 동행 탭(로그인 유도 또는 작성 Form) | 탭 **3개**(항공편/숙소/동행 구하기), Tip **3개**, 3단계 안내 **3단계** |
| **SCR-004** `/mates` | Intro+작성 CTA → 필터+결과 요약 → 동행글 목록 → 목록+상세 분할 → 신청 방법 3단계 → 안전·신고·차단 안내+CTA | 목록 카드 최대 **8개**, 신청 방법 **3단계** |
| **SCR-005** `/account` | (역할별) Guest: Intro+로그인/가입/재설정+기능 안내+보안 안내 · Member: 프로필+내 활동 · Admin: +관리자 | 내 활동 **4블록**(내 글/받은 요청/즐겨찾기/차단), 관리자 **2파트**(신고 상태 변경/외부 URL 설정) |

이 표의 순서와 최소 수는 승인된 Stitch 화면(§Manifest 참고)에서 실측 확인된 값이며, 향후 수정 시에도 이 값 아래로 내려가지 않아야 한다.

## 완성형 Empty State와 Placeholder 문구 금지

- 데이터가 없는 모든 목록/섹션은 다음 3요소를 반드시 포함한 **완성된 구성**으로 렌더링한다: (1) 상황을 설명하는 한 문장, (2) 이용 방법 한 줄, (3) 명확한 다음 행동 CTA. 예: "아직 즐겨찾기한 여행지가 없어요 — 마음에 드는 여행지에서 하트를 눌러보세요 [여행지 둘러보기]".
- 금지 문구: `Lorem ipsum`, `준비 중`, `정보 확인 필요`, 그 외 의미 없는 자리표시 텍스트. 빈 카드(텍스트·이미지 없이 테두리만 있는 Card)도 금지.
- 필터 결과 0건인 경우 목록 Empty State에는 **필터 초기화** 버튼이 항상 함께 있어야 한다(SCR-001, SCR-004 공통 규칙).

## Do / Do Not

**Do**
- 코랄은 주요 CTA·활성 탭/Chip·저장 아이콘에만 좁게 사용한다.
- 안전정보·오류·경고는 코랄과 다른 계열의 semantic 색상 + 텍스트 라벨을 함께 표시한다.
- 모든 이미지에 실제 장소·행동을 설명하는 alt 텍스트를 붙인다.
- 여행 준비 도구로 이동하는 모든 CTA/내비게이션은 `/travel-tools` 실제 경로로 연결한다.
- 데이터 없는 상태는 안내 문장 + 이용 방법 + CTA를 갖춘 완성형 Empty State로 그린다.
- Google Fonts 등 오픈 라이선스 경로로 Inter를 로드하거나, OFL 라이선스 사본을 직접 번들한다.

**Do Not**
- Airbnb의 로고, 워드마크, 브랜드 컬러(Rausch `#ff385c` 등), "Guest favorite" 류 상표적 배지 문구를 재현하지 않는다.
- 예약·결제·장바구니·가격 비교·"Reserve"/"Book now" 같은 구매 UI를 어떤 화면에도 추가하지 않는다.
- 라이선스가 확인되지 않은 Proprietary Font 파일을 프로젝트에 포함하지 않는다.
- 이 문서(§Color Token)에 정의되지 않은 임의의 색상 값을 화면에 추가하지 않는다 — 새 의미가 필요하면 새 semantic 토큰을 이 문서에 먼저 추가한다.
- Hero를 `100vh`/`h-screen`으로 만들어 다음 Section을 뷰포트 밖으로 밀어내지 않는다.
- 여행 준비 CTA에 내부 앵커(`#prep`)나 오타 경로(`/prep`)를 사용하지 않는다 — 반드시 `/travel-tools`.
- 관리자 화면에 차트·KPI 위젯·복잡한 대시보드를 추가하지 않는다 — 목록 + 상태 변경 UI로 제한한다.
- 별점·리뷰 점수, 광고 배너, 실시간 항공권·호텔 가격을 어떤 Card에도 추가하지 않는다.

## Known Gaps

- **Dark mode:** 공개 제품에는 다크 모드가 없다(Airbnb 참고본과 동일한 전제).
- **Map/위치 시각화:** 방문 국가·권역 지도의 세부 스타일(타일 컬러, 마커 모양)은 아직 확정하지 않았다.
- **애니메이션/모션:** 카드 hover 이외의 전환 모션(예: Drawer 슬라이드 easing curve)은 이 문서에서 값으로 고정하지 않았다.
- **다국어 타이포그래피:** 현재는 한국어 우선 스택만 고정했으며, 추가 언어 폰트 대체는 이후 리비전에서 다룬다.

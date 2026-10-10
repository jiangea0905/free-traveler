# Design Manifest — Free Traveler

이 문서는 Free Traveler 프로젝트에서 현재 유효한 디자인 정본(source of truth)이 무엇인지 선언한다. 코드·콘텐츠·추가 디자인 작업은 아래 `Active File`을 기준으로 삼아야 하며, `Status: LOCKED`인 동안 `Active File`의 토큰·규칙을 임의로 바꾸지 않는다.

| 항목 | 값 |
|---|---|
| **Active Design Version** | D-001 |
| **Status** | LOCKED |
| **Active File** | `design-reference/D-001/DESIGN.md` |
| **Vendor Reference** | `design-reference/vendor/airbnb/DESIGN.md` (구조적 참고 전용 — 색상·서체·상표 요소는 채택하지 않음) |
| **기반 문서** | `docs/04_UIUX_PLAN.md`, `docs/STITCH_VALIDATION_REPORT.md` |
| **Stitch Project** | `projects/7876118700864225182` (title: Free Traveler) |
| **Design System Asset** | `assets/13918331161660316385` |
| **잠금 일자** | 2026-09-15 |

## Approved Screens (SCR-001 ~ SCR-005)

| Screen | Route | Screen ID | Device | 상태 |
|---|---|---|---|---|
| SCR-001 | `/` | `18119f6a2c6a4d948f638f8a2c74c3fb` | Desktop 1440px | 승인(경미한 CTA 경로 수정 필요 — STITCH_VALIDATION_REPORT §4 참고) |
| SCR-002 | `/about` | `a61c8204ab2b41cebf76d00803ed36ff` | Desktop 1440px | 승인(PASS) |
| SCR-003 | `/travel-tools` | `372a5cee3f0f46408db798118bf71358` | Desktop 1440px | 승인(PASS) |
| SCR-004 | `/mates` | `334768bc49364517b81be074b66ee450` | Desktop 1440px | 승인(경미한 CTA 경로 수정 필요 — STITCH_VALIDATION_REPORT §4 참고) |
| SCR-005 | `/account` | `7e368d521d174027875228410c9a889f` | Desktop 1440px | 승인(PASS) |

## Mobile Variants

| Screen | Route | Screen ID | Device |
|---|---|---|---|
| SCR-001 Mobile | `/` | `6af5d7abb15b4d61b44c4a80523f5ca5` | Mobile 390px |
| SCR-003 Mobile | `/travel-tools` | `57f6f025529942428e684cafd91cd854` | Mobile 390px |

SCR-002, SCR-004, SCR-005는 Mobile 변형을 이번 잠금 범위에 포함하지 않는다.

## 제외/보류 항목

- 위 7개 승인 화면 외에 프로젝트 캔버스에 남아 있는 과거 중복본(`hidden: true` 상태의 스크린 인스턴스)은 정본에서 제외한다.
- SCR-001, SCR-004의 "여행 준비" 관련 CTA/내비게이션 링크가 `/travel-tools`가 아닌 `#prep`/`/prep`을 가리키는 경미한 결함이 `STITCH_VALIDATION_REPORT.md` 기준 아직 사람 확인 대기 중이다(`STITCH_VALIDATION_NEEDS_HUMAN`). 정본 잠금은 콘텐츠·구조 기준으로 이루어지며, 이 결함은 `design-reference/D-001/DESIGN.md`의 "여행 준비 CTA는 반드시 `/travel-tools`로 연결한다" 규칙(Do 항목)으로 이미 명문화했다.

## 금지 사항 (D-001 전 범위에 적용)

- Airbnb 상표 요소(로고, 워드마크, 브랜드 컬러, "Guest favorite" 류 상표적 배지 문구) 사용 금지.
- 구매·예약·결제 UI(가격 비교, "Reserve"/"Book now", 장바구니, 결제 폼) 추가 금지.
- Proprietary Font 파일 포함 금지 — Inter는 오픈 라이선스(OFL) 경로로만 로드한다.
- `design-reference/D-001/DESIGN.md`의 Color Token에 없는 임의 색상 추가 금지 — 새 의미가 필요하면 토큰을 먼저 추가하고 문서를 갱신한 뒤 사용한다.

## 갱신 절차

새 리비전이 필요하면 `design-reference/D-002/DESIGN.md`를 새로 만들고, 검증(Stitch Validation)을 통과한 뒤에만 이 매니페스트의 `Active Design Version`/`Active File`을 D-002로 교체한다. `Status`가 `LOCKED`인 동안 D-001 파일 자체를 직접 수정하지 않는다.

# P40 — Program value designation from College Scorecard: campus counts, family-level outcomes and "PrivacySuppressed"

| Field | Value |
|---|---|
| Domain | Higher-education accountability / state workforce funding / consumer information |
| Objective family | Descriptive & Distribution Analysis (scorecard) with grain conformance |
| Task shape | 10 · Scorecard against thresholds (program × test, completer-weighted pass share) |
| Core technique | Mixed-grain join: campus-level (UNITID) completer counts with family-level (OPEID6) outcomes; suppression semantics; unit conversion (monthly payment → annual); external threshold join by state |
| Trap family (honest data) | De-duplicating OPEID6 rows and losing campus completers; summing completers per OPEID6 row multiplied by campuses; suppressed values as zero/fail; monthly payment used as annual |
| Primary sources | U.S. Department of Education College Scorecard (Field of Study and Institution files), ED-published earnings thresholds, IPEDS completions |

## 1. The real-world project

A state workforce board grants a **"Return on Investment" designation** to institutions whose programs deliver value:
at least 75% of an institution's completers must be in programs that pass an earnings-premium test, a debt-to-earnings test
and a minimum-size rule. A multi-campus community-college system applied. The analyst's first pass gave the system 52%; the
system's IR office computed 81%.

## 2. The business decision (one deterministic recommendation)

**Go / no-go: does the applicant system earn the designation?**

Rules (designation standard):

* Programs: rows of the Field of Study file for the applicant's OPEID6 (all UNITIDs/campuses), CIP 4-digit × credential
  level, undergraduate credentials only.
* Outcomes (debt and earnings) in the file are reported at the **OPEID6 family** level and repeat on each campus row; completer
  counts (`IPEDSCOUNT1`/`IPEDSCOUNT2`, as specified) are **campus-level**. A program's completers = Σ over campus rows.
* T1 earnings premium: median earnings (field named in the standard) > the state's earnings threshold published by ED.
* T2 debt-to-earnings: 12 × median 10-year monthly payment (field named in the standard) ÷ median earnings ≤ 8%.
* T3 size: earnings cohort count ≥ 30.
* `PrivacySuppressed` or null in any required field → program **not evaluated** (excluded from numerator and denominator).
* Pass share = completers in programs passing T1–T3 ÷ completers in evaluated programs. Go if ≥ 75%.

## 3. Why this gets overlooked in real projects

* Identical outcome values on every campus row look like duplicate records; de-duplicating by OPEID6 × CIP × credential
  keeps one campus's completer count and throws away the rest.
* Conversely, summing family-level counts across campus rows multiplies them.
* `PrivacySuppressed` is a string in numeric columns; coercion produces NaN → 0 → fail.
* Scorecard reports monthly payments; D/E tests use annual payments.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1 | `Most-Recent-Cohorts-Field-of-Study.csv` | CSV | ~230k | College Scorecard (collegescorecard.ed.gov/data) | U.S. Gov public domain | Program outcomes, counts |
| 2 | `Most-Recent-Cohorts-Institution.csv` | CSV | ~6.5k | College Scorecard | Public domain | UNITID ↔ OPEID6, main/branch |
| 3 | `FieldOfStudyData_dictionary.xlsx` (CollegeScorecardDataDictionary) | XLSX | — | College Scorecard | Public domain | Field definitions and levels |
| 4 | `scorecard_technical_documentation_fos.pdf` | PDF | — | ED | Public domain | OPEID6 reporting, suppression |
| 5 | `ed_earnings_thresholds_by_state.xlsx` | XLSX | ~55 | U.S. Department of Education (FVT/GE threshold publication) | Public domain | T1 thresholds |
| 6 | `C2022_A.csv` | CSV | ~300k | NCES IPEDS Completions | Public domain | Cross-check of campus completers |
| 7 | `HD2022.csv` | CSV | ~6.3k | NCES IPEDS | Public domain | Campus names, states |
| 8 | `designation_standard.pdf` | PDF | — | Task author | — | Rules in §2 |
| 9 | `applicant.json` | JSON | 1 | Task author | — | OPEID6, state |
| 10 | `scorecard_api_sample.json` | JSON | ~50 | College Scorecard API | Public domain | Field naming cross-check |

## 5. Deterministic solution path

1. Filter FoS rows by OPEID6 and undergraduate credential levels; parse suppressed values as missing.
2. Build program keys (CIP4 × credential); take outcomes from any campus row (verify identical); sum campus completers.
3. Apply T1–T3; classify evaluated/not evaluated; compute pass share; decide.
4. Contrast: de-dup by program; family counts summed across rows; suppressed-as-fail; monthly payment.

## 6. The traps

**Trap A — de-duplication.** Large programs taught on several campuses lose completers; pass share swings.

**Trap B — monthly payment as annual.** D/E 12× too small → everything passes (or the reverse if the solver annualizes earnings
wrongly).

**Trap C — suppressed as fail.** Denominator includes non-evaluated programs; share drops below 75%.

**Trap D — wrong threshold state / national threshold.** T1 outcomes change for mid-earning programs.

## 7. Why the data is honest

Scorecard publishes outcomes exactly as ED computes them, with documented aggregation levels and suppression. The grain
mismatch is a documented design choice, not an error.

## 8. Draft task prompt (prose)

> The applicant system earns our Return on Investment designation only if at least 75% of its evaluated completers are in
> programs passing all three tests in the designation standard. Using the College Scorecard and supporting files in the
> folder, evaluate every undergraduate program in the system and give me the decision. Produce
> `program_value_scorecard.csv` with one row per program (campuses, completers, earnings, threshold, annual payment, D/E,
> cohort size, each test, evaluated flag) and `program_value_chart.png`, a scatter of D/E against earnings relative to the
> threshold with point size by completers and the pass region shaded. Add a one-page `designation_memo.pdf` with the
> decision, the pass share, and the program whose result most affects the outcome.

## 9. Deliverables

* `program_value_scorecard.csv`, `program_value_chart.png`, `designation_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* ~10–15 programs × 3 tests (+ evaluated flag); completers per program; pass share; decision; pivotal program.

## 11. Golden-output checklist

* Campus completers summed; family outcomes once; suppression excluded; annual payment; state threshold; decision stated.

## 12. Build notes (scope tuning)

* Choose a multi-campus OPEID6 system with programs offered on several campuses and a pass share near 75%; confirm Trap A
  and C flip the decision.
* Confirm the exact earnings and payment field names and the count fields' grain in the current data dictionary.

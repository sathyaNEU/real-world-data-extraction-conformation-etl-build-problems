# AD02 — Benford screening of council payments: a publication threshold that makes every ledger look suspicious

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Digit- and distribution-based fraud screens on truncated data (expense audits with reporting thresholds, payments above approval limits) |
| Domain | Public-sector internal audit / forensic accounting |
| Task shape | 10 · Scorecard against thresholds (department × digit test → refer / clear) |
| Core method | Digit-frequency tests (first, second, first-two digits) with mean-absolute-deviation conformity bands; restricting to the amount range where the expected distribution holds |
| Analytical stump | Payments are published only above £500, so digit frequencies over [£500, ∞) cannot follow Benford's law even for clean books; and with tens of thousands of payments chi-square rejects everything. The test must be restricted to complete decades and judged by effect size |
| Primary sources | Local authority "spending over £500" monthly transparency files (Local Government Transparency Code), Nigrini's Benford conformity thresholds |

## 1. The real-world situation

A council's internal audit team piloted Benford analysis on two years of published payments to choose departments for a
forensic review. Every department failed the first-two-digit chi-square test at p < 0.001, and the 50–99 prefixes were
heavily over-represented everywhere. The audit committee asked whether the whole council was fraudulent or the test was
wrong.

## 2. The decision (one deterministic recommendation)

**Which departments are referred for forensic review?** (Go/no-go per department; the council-level decision is whether any
referral is made.)

Rules (audit committee standard):

* Payments: positive amounts in the council's monthly transparency files for the two financial years in the folder,
  de-duplicated on transaction reference.
* The expected digit distribution must be one the council's payments could follow **given that only amounts of £500 or
  more are published**; amounts outside the range used for testing are excluded from all tests.
* Tests per department (service area as published): first digit, second digit, first-two digits; conformity judged by the
  mean absolute deviation (MAD) against Nigrini's bands (stated in the standard). Departments with fewer than 1,000 payments
  in the test range are not tested.
* Refer a department if its first-two-digit MAD is in the nonconformity band **and** at least one other test is at least
  "marginally acceptable" or worse.

## 3. Why capable analysts get it wrong

* Benford's law describes data spread over several complete orders of magnitude; a £500 floor removes £100–£499, so
  prefixes 10–49 are under-represented relative to 50–99 for every department.
* Chi-square p-values shrink with sample size; with 20,000 payments, trivial deviations are "significant".
* The fix (test only complete decades, e.g. £1,000–£999,999) is a methodological choice the standard implies but does not
  spell out.
* Small departments produce noisy MADs; the minimum-sample rule matters.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–24 | `spend_over_500_YYYY_MM.csv` (24 monthly files) | CSV | 3k–10k each | The chosen council's transparency page | OGL v3.0 | Payments |
| 25 | `spend_over_500_combined.parquet` | Parquet | ~100–200k | Derived | OGL v3.0 | Combined, de-duplicated |
| 26 | `transparency_code_2015_extract.pdf` | PDF | — | DLUHC Local Government Transparency Code | OGL v3.0 | £500 threshold, fields |
| 27 | `nigrini_conformity_bands.json` | JSON | — | Nigrini (2012), Benford's Law (cite) | Cite | MAD thresholds |
| 28 | `benford_expected_frequencies.xlsx` | XLSX | ~100 | Computed reference | — | First/second/first-two expectations |
| 29 | `audit_committee_standard.pdf` | PDF | — | Task author | — | Rules in §2 |
| 30 | `pilot_chisquare_results.xlsx` | XLSX | ~10 | Task author | — | The failed pilot |
| 31 | `council_service_areas.csv` | CSV | ~15 | Council | OGL v3.0 | Department names |

## 5. Deterministic solution path

1. Combine and de-duplicate payments; keep positive amounts; assign departments.
2. Choose the test range: complete decades within the published range (£1,000 – £999,999.99); show why [£500, ∞) fails by
   computing MADs on a clean-looking department.
3. For each department with ≥ 1,000 in range: MAD for the three tests; classify bands.
4. Apply the referral rule; produce the department × test scorecard.
5. Contrast with chi-square on the full published range.

## 6. Wrong paths (method errors, not misreadings)

**A — full published range.** Every department nonconforming; referral of all.

**B — chi-square decisions.** Same over-flagging; ignores effect size.

**C — no minimum sample.** Small departments referred on noise.

**D — negative amounts included as absolute values.** Credit notes distort digits.

## 7. Why the stump is analytical, not semantic

The data and threshold are explicit; the standard defines the referral rule and the MAD bands. The failure is statistical
— applying a distributional law outside the conditions under which it holds, and using a significance test whose power
grows with n.

## 8. Draft task prompt (prose)

> Audit committee wants to know which departments, if any, to send for forensic review based on our two years of published
> payments and the standard in the folder. Run the digit tests so that they are fair to a council that only publishes
> payments over £500, and give me the referrals. Produce `benford_scorecard.csv` (department × test: n, MAD, band, referral
> flag), `first_two_digits.png` showing the observed versus expected first-two-digit frequencies for the council overall and
> for any referred department, and a one-page `referral_memo.pdf` explaining the referral decision and why the pilot flagged
> everyone.

## 9. Deliverables

* `benford_scorecard.csv`, `first_two_digits.png`, `referral_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* ~10 departments × 3 tests (MAD + band) = 30 cells; referral flags; test range; pilot explanation.

## 11. Golden-output checklist

* Complete-decade range; MAD bands; minimum n; positives only; referral rule applied.

## 12. Build notes (scope tuning)

* Choose a council with ≥ 8 departments above 1,000 payments in range and confirm that at most 1–2 are referred under the
  correct method while all fail on the full range.
* Verify Nigrini's band values for each test from the cited source before freezing the standard.

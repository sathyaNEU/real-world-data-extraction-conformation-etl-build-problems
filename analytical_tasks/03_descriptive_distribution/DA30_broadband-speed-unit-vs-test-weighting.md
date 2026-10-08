# DA30 — Do households get the speed they pay for? Count households, not tests

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Per-user versus per-session metrics in product analytics (heavy users dominate session-level distributions); ISP and CDN quality reporting |
| Domain | Telecommunications / consumer protection |
| Task shape | 10 · Scorecard against thresholds (ISP × speed tier → share of households receiving ≥ 80% of advertised download speed at peak; pass/fail per ISP against the regulator's 90% standard) |
| Core method | Per-unit (household whitebox) peak-hour median of test results ÷ advertised tier; household-level pass if ≥ 0.8; ISP score = share of households passing (weighted per memo); comparison with pooled test-level shares |
| Analytical stump | Test-level distributions overweight households that run more tests (units with longer panel participation or more frequent schedules) and treat each test as independent. The standard concerns households; aggregating within household first and then across households changes which ISPs pass |
| Primary sources | FCC Measuring Broadband America (MBA) fixed raw data — whitebox panel test results and unit profiles |

## 1. The real-world situation

A consumer-protection agency publishes whether each ISP delivers at least 80% of advertised download speed at peak to at least 90% of
households. The draft computed the share of all peak-hour tests at or above 80% of tier, by ISP, and passed seven ISPs. ISPs with smaller,
newer panels objected that a few always-on units with frequent tests dominated their figures.

## 2. The decision (one deterministic recommendation)

**The list of ISPs passing the 90% household standard for the reporting month, with household-level and test-level shares for each ISP.**

Rules (agency memo):

* Data: MBA raw download test results (`curr_httpgetmt` or the memo's test type) for the reporting month; unit profile file for ISP and
  advertised tier.
* Peak hours: 19:00–23:00 local time, weekdays.
* Validity: units with ≥ 5 valid peak tests in the month; tests flagged invalid per the data dictionary excluded.
* Household metric: median of peak-test throughput ÷ advertised download speed; pass if ≥ 0.8.
* ISP score: share of passing households, each household weighted equally within the ISP (memo).
* Standard: score ≥ 90% → pass.
* Test-level contrast: share of all valid peak tests with throughput ≥ 0.8 × tier.

## 3. Why capable analysts get it wrong

* Test records are the rows; pooling them is the default.
* Units differ in the number of tests; pooling weights them unequally.
* A household's typical experience is a within-unit summary, not a pool of tests.
* Advertised tiers vary within an ISP; ratios must be computed per unit.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `curr_httpgetmt_<yyyy>_<mm>.csv` | CSV | ~5–8M | FCC MBA raw data | U.S. Gov public domain | Download throughput tests |
| 2 | `unit_profile_<yyyy>.xlsx` | XLSX | ~3–5k | FCC MBA | Public domain | Unit → ISP, tier, technology |
| 3 | `mba_raw_data_dictionary.pdf` | PDF | — | FCC | Public domain | Fields, validity flags |
| 4 | `unit_timezone_map.csv` | CSV | ~4k | FCC MBA unit metadata | Public domain | Local time |
| 5 | `agency_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `draft_test_level_scorecard.xlsx` | XLSX | ~12 | Task author | — | Draft results |
| 7 | `mba_technical_appendix_citation.pdf` | PDF | — | FCC MBA report (cite) | Public domain | Methodology context |
| 8 | `unit_test_counts.parquet` | Parquet | ~4k | Derived | Public domain | Tests per unit |

## 5. Deterministic solution path

1. Filter tests to peak hours (local), validity, month.
2. Join unit profiles; compute per-test ratios.
3. Household medians; pass flags; ISP scores; validity floor.
4. Test-level contrast; pass list.

## 6. Wrong paths (method errors, not misreadings)

**A — test-level pooling.** Heavy testers dominate.

**B — mean ratio per household.** Sensitive to outlier tests; memo uses the median.

**C — UTC instead of local time.** Wrong peak window.

**D — no minimum tests per unit.** Noisy households.

## 7. Why the stump is analytical, not semantic

Units, metrics and the standard are specified. The trap is the unit of analysis when observations are clustered.

## 8. Draft task prompt (prose)

> Which ISPs meet our 90% household speed standard this month? Compute household-level peak performance from the MBA panel as the agency memo
> specifies and compare with the draft's test-level figures. Provide `isp_scorecard.csv` (ISP: households, household share passing, test-level
> share, pass), `tests_per_unit.png` (distribution of tests per household by ISP), and a one-page `speed_standard_results.pdf`.

## 9. Deliverables

* `isp_scorecard.csv`, `tests_per_unit.png`, `speed_standard_results.pdf`.

## 10. Where 25+ rubric criteria come from

* ~12 ISPs × (household share, test-level share, pass) = 36; validity exclusions; local-time handling.

## 11. Golden-output checklist

* Peak window in local time; validity; per-unit medians; equal household weights; standard.

## 12. Build notes (scope tuning)

* Confirm at least one ISP passes on test-level pooling and fails on household shares.

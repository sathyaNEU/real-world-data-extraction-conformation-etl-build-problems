# P20 — PM2.5 attainment from AQS: quarterly means, collocated monitors, event flags and the 98th-percentile rank table

| Field | Value |
|---|---|
| Domain | Air quality permitting / environmental consulting / site selection |
| Objective family | Descriptive & Distribution Analysis (regulatory scorecard) |
| Task shape | 10 · Scorecard against thresholds (with 14 · cuts of a distribution for the 98th percentile) |
| Core technique | Regulatory-algorithm replication (40 CFR Part 50 Appendix N): site-level record combination, completeness tests, quarter→year→3-year averaging, rank-table percentiles, rounding conventions; de-duplication by pollutant standard/event type |
| Trap family (honest data) | Simple annual average of all daily values; averaging collocated monitors; counting duplicated standard rows; including concurred exceptional events; wrong parameter code |
| Primary sources | EPA AQS pre-generated daily files (parameter 88101), AQS monitor/site listings, 40 CFR Part 50 Appendix N |

## 1. The real-world project

A manufacturer is choosing a county for a new plant. If the county violates a PM2.5 NAAQS, the project faces
nonattainment New Source Review (offsets, LAER) — months of delay and real money. The consultant computed "annual
average PM2.5" for 2021–2023 by averaging every daily value at every monitor in the county and declared attainment
with the 9.0 µg/m³ annual standard (revised in 2024). The state agency's own design value said otherwise.

## 2. The business decision (one deterministic recommendation)

**Go / no-go for the candidate county: does it meet both the 2024 annual PM2.5 standard (9.0 µg/m³) and the 24-hour
standard (35 µg/m³) on 2021–2023 design values?**

Rules (Appendix N as summarized in the folder; the regulation text governs):

* Parameter 88101 only (FRM/FEM); one value per site-day after combining collocated monitors per Appendix N's site-level
  rules (primary monitor first, substitution from other qualifying monitors when missing).
* Exclude days flagged for exceptional events **with EPA concurrence**; keep other flagged days.
* Quarterly mean = mean of creditable daily values in the quarter; a quarter is complete at ≥ 75% capture of scheduled
  samples (substitution tests per Appendix N where a quarter is incomplete).
* Annual mean = mean of 4 quarterly means; annual DV = mean of 3 annual means, rounded to 0.1 µg/m³.
* 98th percentile per year from the Appendix N rank table (rank depends on number of creditable samples); 24-hour DV =
  mean of three yearly 98th percentiles, rounded to the nearest 1 µg/m³.
* County DV = the **maximum** valid site DV in the county; go only if both county DVs are at or below the standards.

## 3. Why this gets overlooked in real projects

* "Annual average" sounds like a mean of days. Appendix N averages quarters first, so a heavily sampled smoky summer
  quarter weighs no more than a sparsely sampled winter quarter.
* Collocated monitors (POCs) are common at core sites; averaging them is intuitive and wrong; so is summing their counts.
* AQS daily files can repeat a monitor-day under different pollutant-standard or event-handling labels; a naive load
  double counts.
* Exceptional-event logic is three-valued (no event / flagged / concurred); dropping all flagged days or none both err.
* The 98th percentile is not `numpy.percentile(…, 98)`; it is a rank lookup that depends on sample count.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1–3 | `daily_88101_2021.csv`, `daily_88101_2022.csv`, `daily_88101_2023.csv` | CSV | ~0.6–0.8M each | EPA AQS pre-generated data files | U.S. Gov public domain | Daily PM2.5 |
| 4 | `daily_88502_2023.csv` | CSV | ~0.5M | EPA AQS | Public domain | Non-regulatory PM2.5 (decoy-free context; must not be used) |
| 5 | `aqs_monitors.csv` | CSV | ~350k | EPA AQS | Public domain | Monitor attributes, NAAQS-primary flags |
| 6 | `aqs_sites.csv` | CSV | ~20k | EPA AQS | Public domain | Site → county |
| 7 | `annual_conc_by_monitor_2023.csv` | CSV | ~70k | EPA AQS | Public domain | Cross-check of means |
| 8 | `pm25_designvalues_2021_2023.xlsx` | XLSX | ~1k sites | EPA design value reports | Public domain | Reconciliation target |
| 9 | `40cfr50_appendixN.pdf` | PDF | — | eCFR | Public domain | Algorithm |
| 10 | `exceptional_events_concurrence.json` | JSON | small | EPA exceptional-events tracking (public) | Public domain | Concurred flags (if not in daily file) |
| 11 | `aqs_codes_qualifiers.csv` | CSV | ~500 | EPA AQS code tables | Public domain | Qualifier/event code meanings |
| 12 | `candidate_county.json` | JSON | 1 | Task author | — | County FIPS |

## 5. Deterministic solution path

1. Load 88101 daily rows for the county's sites; de-duplicate monitor-days across standard/event labels using the
   documented columns.
2. Build site-day records by Appendix N combination rules; drop concurred exceptional-event days.
3. Compute quarterly completeness and means; apply substitution tests where needed; annual means; 3-year annual DV.
4. Compute yearly 98th percentiles via the rank table; 24-hour DV.
5. Take county maxima; compare to 9.0 and 35; decide; reconcile to EPA's published DVs.

## 6. The traps

**Trap A — mean of all days.** Biased toward heavily sampled quarters; flips the annual decision near 9.0.

**Trap B — averaging collocated POCs.** Dilutes the high monitor.

**Trap C — duplicated standard/event rows.** Double weights some days.

**Trap D — event handling.** Dropping all flagged days or keeping concurred ones moves 98th percentiles in fire years.

**Trap E — percentile function / rounding.** Library percentiles and unrounded comparisons change borderline outcomes.

**Trap F — mean of site DVs.** County DV must be the maximum.

## 7. Why the data is honest

AQS data are the regulatory record; the computation is fully specified in federal regulation and EPA publishes the
resulting design values for reconciliation.

## 8. Draft task prompt (prose)

> Before we commit to the candidate county, I need a go or no-go on whether it meets both PM2.5 standards on 2021–2023
> design values, computed exactly the way Appendix N in the folder prescribes. Using the AQS files, compute every site's
> annual and 24-hour design values and the county values, and give me the call. Deliver `pm25_dv_scorecard.xlsx` with
> one row per site-year (quarterly capture, quarterly means, annual mean, 98th percentile and its rank) plus a site summary
> with both design values and pass/fail, and `pm25_dv_chart.png` showing each site's annual design value against the 9.0
> line and its 24-hour design value against the 35 line. On the summary sheet, give the decision, the controlling site,
> its margin to the standard, and whether EPA's published design values agree.

## 9. Deliverables

* `pm25_dv_scorecard.xlsx`, `pm25_dv_chart.png`.

## 10. Where 25+ rubric criteria come from

* Per site × year: completeness and means (≥ 3 sites × 3 years × 2 metrics), site DVs (2 per site), county DVs, decision,
  controlling site and margin, reconciliation result.

## 11. Golden-output checklist

* 88101 only; de-duplicated; site combination; concurred events excluded; quarterly averaging; rank-table 98th; rounding;
  county maximum; decision stated.

## 12. Build notes (scope tuning)

* Choose a county with collocated monitors and a design value within ±0.4 µg/m³ of 9.0 so Traps A/B flip the decision;
  wildfire-affected western counties often have concurred events relevant to the 24-hour DV.
* Verify the exact columns that encode pollutant standard and event status in the downloaded files before writing rules.

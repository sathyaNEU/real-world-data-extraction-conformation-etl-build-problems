# DA09 — Salary bands from a self-selected survey: rake to the workforce before you cut percentiles

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Compensation and people-analytics teams at technology companies benchmarking pay from public surveys; any product analytics on opt-in samples |
| Domain | Labour market / compensation |
| Task shape | 14 · Cuts of a distribution (P25, P50, P75 of US developer pay for 4 role families; the band published to recruiters) |
| Core method | Raking (iterative proportional fitting) of survey respondents to population margins (occupation × state group from BLS OEWS employment; experience band from the memo's external split); weighted percentiles; trimming of extreme weights per memo |
| Analytical stump | Respondents to an online developer survey over-represent some states, younger developers and certain roles. Unweighted percentiles describe the respondents, not the workforce. Raking to known employment margins changes the pay bands, especially at P75 |
| Primary sources | Stack Overflow Annual Developer Survey (public results); BLS Occupational Employment and Wage Statistics (OEWS) state data |

## 1. The real-world situation

A technology company publishes salary bands to recruiters for four developer role families in the United States. The comp analyst took
the latest Stack Overflow survey and reported unweighted percentiles of annual compensation. A people-analytics reviewer noted that the
respondents are heavily concentrated in a few states and early-career levels, while the company hires nationally across experience levels.

## 2. The decision (one deterministic recommendation)

**The P25–P75 band and median (USD, rounded to the nearest $1,000) for each of the four role families, computed on raked weights.**

Rules (compensation memo):

* Respondents: US, employed full-time, annual compensation in USD between $10,000 and $1,000,000 (converted per survey fields), role
  family per the mapping file.
* Margins: (a) OEWS employment by role family's SOC codes × state group (6 groups in the memo); (b) experience bands (0–4, 5–9, 10–19, 20+
  years) with shares from the memo's reference split.
* Raking: IPF over margins (a) and (b) until all margins match within 0.1%; cap weights at 5× the median weight, then re-rake (one
  iteration of trimming).
* Weighted percentiles: the memo's definition (weighted empirical CDF, smallest value with cumulative weight ≥ p).
* Report unweighted values for contrast.

## 3. Why capable analysts get it wrong

* Survey percentiles look authoritative because of large sample sizes.
* Large n does not fix selection bias; weighting to known margins does (partially).
* Raking without trimming can let a few respondents dominate; untrimmed and trimmed answers differ.
* Weighted percentile definitions vary; the memo fixes one.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `survey_results_public.csv` | CSV | ~65–90k | Stack Overflow Developer Survey | Open Database License (ODbL) | Responses |
| 2 | `survey_results_schema.csv` | CSV | ~80 | Stack Overflow | ODbL | Question text |
| 3 | `oesm<yy>st.xlsx` (state OEWS) | XLSX | ~40k | BLS OEWS | U.S. Gov public domain | Employment by state × occupation |
| 4 | `role_family_mapping.csv` | CSV | ~40 | Task author | — | Survey roles ↔ SOC codes |
| 5 | `state_groups.json` | JSON | 6 | Task author | — | State grouping |
| 6 | `experience_reference_split.json` | JSON | 4 | Task author (from public workforce statistics) | — | Experience margins |
| 7 | `compensation_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 8 | `analyst_unweighted_bands.xlsx` | XLSX | 4 | Task author | — | Naive bands |
| 9 | `raking_check.json` | JSON | ~10 | Task author | — | Small IPF test case |
| 10 | `deming_stephan_ipf_citation.pdf` | PDF | — | Cite | Cite | Raking |

## 5. Deterministic solution path

1. Filter respondents; map roles, states, experience.
2. Build OEWS margins; rake; trim; re-rake.
3. Weighted percentiles per role family; rounding.
4. Contrast with unweighted bands.

## 6. Wrong paths (method errors, not misreadings)

**A — unweighted percentiles.** Respondent mix, not workforce.

**B — post-stratification on one margin only.** Residual imbalance.

**C — no trimming.** Unstable bands.

**D — weighted mean ± SD instead of percentiles.** Skewed pay misdescribed.

## 7. Why the stump is analytical, not semantic

Margins, raking and percentile definitions are specified. The trap is treating a self-selected sample as representative.

## 8. Draft task prompt (prose)

> Give recruiters the pay bands for our four developer role families using the raked survey weights in the compensation memo. Provide
> `pay_bands.csv` (role family: n, P25, P50, P75 weighted and unweighted), `weight_diagnostics.png` (weight distribution and margin fit), and a
> one-page `pay_band_memo.pdf`.

## 9. Deliverables

* `pay_bands.csv`, `weight_diagnostics.png`, `pay_band_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 families × (P25, P50, P75) weighted = 12 and unweighted = 12; margin fit; trimming count; recommendation.

## 11. Golden-output checklist

* Filters; mapping; margins; IPF convergence; trimming; percentile definition; rounding.

## 12. Build notes (scope tuning)

* Pick the survey year whose respondent mix differs most from OEWS margins; confirm at least two P75 values shift by ≥ $5,000.

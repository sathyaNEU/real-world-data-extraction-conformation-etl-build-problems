# RC13 — Which aircraft components go on the reliability alert list: worse parts, more flying, or a few airlines reporting more?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Field-reliability alerting where reporters differ in propensity (Cisco TAC cases dominated by a few large customers, app crash reports skewed by one OEM, warranty claims by dealer) |
| Domain | Aviation maintenance and reliability |
| Task shape | 01 · Ranked list under a cap (the five JASC component codes placed on the reliability alert list, ranked by within-operator rate change) |
| Core method | SDR counts by JASC code × operator × aircraft type × year; exposure = airborne hours from BTS T2 for the same operator × type × year; Poisson GLM per JASC code with operator × type fixed effects and a year effect (within-reporter rate ratio, current vs reference year); Pearson overdispersion check and quasi-Poisson standard errors; rank by the lower 90% bound of the rate ratio among codes with ≥ 20 reports |
| Analytical stump | Year-over-year growth in raw report counts mixes three things: more flying, a shift of flying toward operators who report far more often, and genuine change in part behaviour. Reporting propensity differs by an order of magnitude between operators, so a fleet expansion at one high-reporting airline inflates counts for every component it flies. Only a within-operator comparison isolates the part |
| Primary sources | FAA Service Difficulty Reporting System (SDRS) data; U.S. DOT BTS Air Carrier Summary (T2: traffic and capacity statistics by aircraft type, airborne hours) |

## 1. The real-world situation

An airline industry reliability working group publishes an annual alert list of five component categories whose service difficulty reports grew
fastest. The draft list ranked JASC codes by percentage growth in report counts. Two of the five belonged to systems on a narrow-body type that one
carrier had expanded sharply, and that carrier files SDRs at several times the industry rate. The group asked for a list that reflects the
components, not the reporters.

## 2. The decision (one deterministic recommendation)

**The five JASC codes on the alert list, in rank order, each with its within-operator rate ratio, 90% interval and report counts.**

Rules (reliability memo):

* Data: SDRs for U.S. Part 121 operators in the reference and current calendar years; keep reports with an aircraft make/model mapped to a BTS
  aircraft type (memo crosswalk) and an operator mapped to a BTS carrier (memo crosswalk); JASC code at 4 digits.
* Exposure: BTS T2 airborne hours by carrier × aircraft type × year.
* Eligible codes: ≥ 20 reports across both years.
* Model per code: log E[count] = log(hours) + α(operator × type) + γ·I(current year); quasi-Poisson; rate ratio = exp(γ).
* Cells with zero reports in both years contribute nothing and are kept for exposure consistency.
* Ranking: lower 90% confidence bound of exp(γ), descending; ties by more reports. Alert list = top 5 with lower bound > 1.

## 3. Why capable analysts get it wrong

* Percentage growth in counts is the familiar metric and is easy to compute.
* Normalising by total fleet hours still lets reporter mix leak in.
* Small cells produce huge apparent ratios.
* Overdispersion is common in maintenance reports; Poisson intervals are too narrow.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `sdrs_<ref_year>.csv` | CSV | ~40k | FAA SDRS public query/download | U.S. Government work (public domain) | Reference-year reports |
| 2 | `sdrs_<cur_year>.csv` | CSV | ~40k | FAA SDRS | Public domain | Current-year reports |
| 3 | `bts_t2_<years>.csv` | CSV | ~6k | BTS TranStats, Air Carrier Summary T2 | Public domain | Airborne hours by carrier × type |
| 4 | `jasc_codes.xlsx` | XLSX | ~1,500 | FAA JASC code table | Public domain | Code hierarchy |
| 5 | `operator_crosswalk.csv` | CSV | ~80 | Task author (from FAA operator designators and BTS carrier codes) | — | Reporter → carrier |
| 6 | `aircraft_type_crosswalk.csv` | CSV | ~150 | Task author (SDR make/model → BTS aircraft type) | — | Model → type |
| 7 | `reliability_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 8 | `draft_alert_list.xlsx` | XLSX | 5 | Task author (count-growth ranking) | — | Draft list |

## 5. Deterministic solution path

1. Load and filter SDRs; map operators and aircraft types; aggregate counts by code × operator × type × year.
2. Join exposures; drop codes below 20 reports.
3. Fit the fixed-effects quasi-Poisson per code; extract rate ratio and 90% bounds.
4. Rank; take the top 5 with lower bound > 1.
5. Decompose the draft list's top codes: exposure growth, reporter mix, within-operator change.

## 6. Wrong paths (method errors, not misreadings)

**A — growth in raw counts.** Ranks by flying and reporter mix.

**B — rate per total fleet hours without operator effects.** The high-reporting carrier's growth still inflates rates.

**C — separate operator-level rates ranked individually.** Small cells (0 → 3 reports) dominate the list.

**D — Poisson standard errors.** Intervals too narrow; codes with noisy counts pass the lower-bound rule.

## 7. Why the stump is analytical, not semantic

The crosswalks, eligibility rule, model and ranking metric are given. The trap is comparing across reporters with different propensities and
exposure, instead of within them.

## 8. Draft task prompt (prose)

> Our working group's draft alert list ranks component codes by growth in service difficulty reports. Rebuild the list with the reliability memo's
> within-operator method so it reflects the parts rather than who flew and reported more. Provide `alert_ranking.csv` (code: rate ratio, 90% bounds,
> counts, rank), `rate_ratio_forest.png`, and a one-page `alert_list_rationale.pdf`.

## 9. Deliverables

* `alert_ranking.csv` — all eligible codes with rate ratios and bounds; top 5 flagged.
* `rate_ratio_forest.png` — forest plot of rate ratios for the top 20 codes, draft-list codes highlighted.
* `alert_list_rationale.pdf` — final list and the decomposition of the draft list's entries.

## 10. Where 25+ rubric criteria come from

* Mapping coverage (reports mapped/unmapped by crosswalk): 3.
* Eligible code count: 1.
* Rate ratio and bounds for each of the top 5: 15.
* Dispersion parameter reported and used: 2.
* Rank order and the > 1 rule: 2.
* Draft-list decomposition (exposure, mix, within): 3+.

## 11. Golden-output checklist

* Part 121 filter; 4-digit JASC; both crosswalks applied.
* Exposure from T2 airborne hours as offset.
* Operator × type fixed effects; quasi-Poisson.
* Lower 90% bound ranking; ≥ 20 reports eligibility.

## 12. Build notes (scope tuning)

* Pick years in which one high-reporting carrier grew its hours on one aircraft type by ≥ 25% while others were flat; confirm that at least two
  draft-list codes drop out under the within-operator model.

# RC05 — Subway delays doubled: more incidents, longer incidents, or more service to be delayed?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | SRE incident analysis (incident minutes rising because of a few long outages versus more frequent incidents, normalised by traffic) |
| Domain | Urban transit operations |
| Task shape | 18 · Hypotheses versus evidence (causes: more frequent incidents, longer incidents, one or two extreme events, more service exposure; evidence lines × causes; the cause acted on) |
| Core method | Decompose total delay minutes = incidents × mean minutes per incident; incident rate per 1,000 train-hours (exposure); median and trimmed mean of minutes (heavy tail); contributions of the top 1% incidents; compare years by line and incident code group |
| Analytical stump | Total delay minutes are dominated by a handful of extreme events (fires, police investigations, track failures); year-over-year comparisons of totals or means swing with them. Without separating frequency and severity, and normalising frequency by service hours, analysts chase the wrong cause |
| Primary sources | Toronto Transit Commission (TTC) subway delay data (City of Toronto Open Data) |

## 1. The real-world situation

A transit agency reported that subway delay minutes rose 90% year over year and launched a programme to reduce passenger-related incidents, the
most frequent code. Operations staff noted two multi-hour track incidents and an expansion of service hours.

## 2. The decision (one deterministic recommendation)

**The hypothesis acted on (from the memo's four) — the one whose evidence lines are all consistent — with the frequency and severity contributions to
the change.**

Rules (operations memo):

* Data: TTC subway delay records for two consecutive years (date, time, station, code, min delay, line).
* Code groups from `delay_code_groups.csv`.
* Exposure: train-hours by line and year (`service_hours.csv`, from the agency's service summaries).
* Decomposition: Δ minutes = Δ(rate × hours × mean minutes) split into exposure, frequency (rate), severity (mean minutes) via log-mean Divisia
  (LMDI) per memo.
* Heavy tail: share of minutes from the top 1% of incidents each year; trimmed mean (excluding top 1%).
* Hypotheses: H1 more frequent incidents (rate up ≥ 15%); H2 longer typical incidents (trimmed mean up ≥ 15%); H3 extreme events (top 1% share up
  ≥ 10 points and explains ≥ 50% of Δ minutes); H4 exposure (hours up ≥ 10% and explains ≥ 50% of Δ).
* Act on the hypothesis with all its evidence lines consistent; if several, the one explaining the largest share.

## 3. Why capable analysts get it wrong

* Total minutes and counts by code are the standard reports.
* Delay durations are extremely skewed; means are unstable.
* Service expansion raises exposure.
* Frequency and severity have different remedies.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `ttc-subway-delay-data-<year1>.xlsx` | XLSX | ~20k | City of Toronto Open Data | Open Government Licence – Toronto | Delay records |
| 2 | `ttc-subway-delay-data-<year2>.xlsx` | XLSX | ~20k | Same | OGL – Toronto | Delay records |
| 3 | `ttc-subway-delay-codes.xlsx` | XLSX | ~200 | Same | OGL – Toronto | Code descriptions |
| 4 | `delay_code_groups.csv` | CSV | ~200 | Task author | — | Groups |
| 5 | `service_hours.csv` | CSV | 8 | Task author (from TTC service summaries; cite) | Public | Exposure |
| 6 | `operations_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `agency_report_totals.xlsx` | XLSX | — | Task author | — | Original claim |

## 5. Deterministic solution path

1. Clean records; group codes; join exposure.
2. Rates, mean and trimmed mean minutes; top-1% shares.
3. LMDI decomposition; evaluate hypotheses; act.

## 6. Wrong paths (method errors, not misreadings)

**A — totals by code.** Frequency-heavy codes blamed.

**B — means without trimming.** Extreme events dominate.

**C — no exposure.** Service growth misread as deterioration.

**D — additive decomposition with arbitrary order.** Non-unique attribution (memo uses LMDI).

## 7. Why the stump is analytical, not semantic

Definitions, thresholds and decomposition are specified. The trap is heavy tails and exposure in incident metrics.

## 8. Draft task prompt (prose)

> Why did subway delay minutes jump? Test the four hypotheses in the operations memo with frequency, severity, tail and exposure evidence. Provide
> `hypothesis_grid.csv` (hypothesis × evidence: value, consistent?), `delay_decomposition.png`, and a one-page `delay_rca.pdf`.

## 9. Deliverables

* `hypothesis_grid.csv`, `delay_decomposition.png`, `delay_rca.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 hypotheses × 3 evidence lines = 12 cells; LMDI components; top incidents; chosen hypothesis; line-level breakdown (4 lines).

## 11. Golden-output checklist

* Cleaning; groups; exposure; LMDI; tail metrics; rule.

## 12. Build notes (scope tuning)

* Choose years where two extreme incidents drive the increase.

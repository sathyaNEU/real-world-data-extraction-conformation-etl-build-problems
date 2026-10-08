# RC18 — The emergency department's four-hour performance jumped 6 points: better flow, or more minor cases in the denominator?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | SLA metrics that improve because easy cases enter the denominator (support tickets routed from a self-serve channel, on-time rates after adding short routes, "resolved within a day" after counting password resets) |
| Domain | Hospital emergency care |
| Task shape | 03 · Bridge between two totals (all-types four-hour performance, same months a year apart → after a co-located urgent treatment centre opened; bridged into denominator inflation, streaming of minors out of the major ED, and genuine flow change) |
| Core method | Provider-level monthly attendances and > 4-hour waits by department type; like-for-like counterfactual: the pre-period site population at pre-period performance plus the additional attendances at the urgent treatment centre's performance; denominator effect = counterfactual − pre; genuine flow effect = post − counterfactual; seasonal control by comparing the same calendar months; check whether the extra attendances were transferred from another provider |
| Analytical stump | The all-types percentage rises when a high-performing, low-acuity stream is added to the denominator, even if no patient is seen faster. Looking at the major-ED (type 1) series alone is also wrong: streaming minors away makes type 1 performance fall even with unchanged flow. Only a like-for-like construction separates mix from flow |
| Primary sources | NHS England — A&E Attendances and Emergency Admissions monthly statistics (provider-level, by department type); NHS Organisation Data Service (provider and site codes) |

## 1. The real-world situation

A hospital trust's all-types four-hour performance rose from 71% to 77% between the same quarters a year apart. The board credited its new
patient-flow programme and proposed rolling it out to two sister sites. A regional analyst noticed that the trust had opened a co-located urgent
treatment centre (type 3) during the year, while the major ED's own (type 1) performance had fallen. The region asked for a bridge before
endorsing the roll-out.

## 2. The decision (one deterministic recommendation)

**Whether the flow programme is credited and rolled out (credit only if the genuine flow effect ≥ +2.0 percentage points), with the bridge in
percentage points.**

Rules (regional memo):

* Data: monthly provider-level A&E statistics for the trust and for every other provider in the same integrated care board (ICB); attendances and
  attendances > 4 hours by type (1, 2, 3).
* Pre period: the 3 months a year before the post period; post period: the memo's 3 months.
* Pre: attendances A0 and performance P0 = 1 − (> 4 h ÷ attendances), all types (the trust had no type 3 then).
* Post: type 1 (A1, P1), type 3 (A3, P3), all types P_post.
* Extra attendances X = A1 + A3 − A0 (if X ≤ 0, the denominator effect is computed with X = 0).
* Counterfactual CF = (A0 × P0 + X × P3) ÷ (A0 + X).
* Denominator effect = CF − P0; genuine flow effect = P_post − CF.
* Transfer check: change in type 3 attendances at other ICB providers between the same periods; report the share of X matched by declines elsewhere.
* Credit the programme only if the genuine flow effect ≥ +2.0 points.

## 3. Why capable analysts get it wrong

* The headline metric moved in the hoped-for direction.
* Department types look like separate services, but they share one patient population.
* The type 1 series moves the "wrong" way for compositional reasons, inviting the opposite error.
* New services also attract new and transferred activity.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `ae_monthly_provider_<months>.csv` (24 files) | CSV | ~12k provider-months | NHS England A&E Attendances and Emergency Admissions | Open Government Licence v3.0 | Attendances and > 4 h by type |
| 2 | `ods_trusts_sites.csv` | CSV | ~3k | NHS ODS | OGL v3.0 | Provider names, sites, ICB membership |
| 3 | `ae_definitions_guidance.pdf` | PDF | — | NHS England | OGL v3.0 | Department type definitions |
| 4 | `regional_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `board_flow_programme_paper.pdf` | PDF | — | Task author | — | The board's claim |
| 6 | `utc_opening_dates.json` | JSON | ~10 | Task author (from trust public announcements; cite) | Cite | Context only |

## 5. Deterministic solution path

1. Stack the monthly files; filter the trust and ICB providers; compute per-type and all-types performance.
2. Compute A0, P0, A1, P1, A3, P3, P_post and X.
3. Counterfactual; denominator and flow effects; transfer check.
4. Decision; contrast with the board paper and with a type 1–only reading.

## 6. Wrong paths (method errors, not misreadings)

**A — headline all-types change.** +6 points credited to the programme.

**B — type 1 only.** Shows a fall and blames the programme, ignoring that minors left the type 1 denominator.

**C — sequential months instead of the same months a year earlier.** Winter–spring seasonality dominates.

**D — ignoring extra attendances.** Treats the UTC as serving only patients diverted from the ED, overstating flow gains.

## 7. Why the stump is analytical, not semantic

The counterfactual is defined algebraically from published counts. The trap is a ratio metric whose denominator composition changed.

## 8. Draft task prompt (prose)

> The board wants to roll out its flow programme because four-hour performance jumped 6 points. Bridge the change using the regional memo's
> like-for-like method and tell me whether the programme deserves the credit. Provide `four_hour_bridge.csv` (component: points), `four_hour_bridge.png`,
> and a one-page `rollout_recommendation.pdf`.

## 9. Deliverables

* `four_hour_bridge.csv` — P0, denominator effect, genuine flow effect, P_post; plus A0, A1, A3, X and the transfer share.
* `four_hour_bridge.png` — waterfall from P0 to P_post with the 2-point credit threshold marked.
* `rollout_recommendation.pdf` — decision, bridge, and why the headline and type 1 readings mislead.

## 10. Where 25+ rubric criteria come from

* Monthly extraction for 6 months × types: 6.
* A0, P0, A1, P1, A3, P3, P_post, X: 8.
* CF, denominator effect, flow effect: 3.
* Transfer check: 2.
* Decision: 1.
* Contrasts (headline, type 1): 3.
* Chart elements: 2+.

## 11. Golden-output checklist

* Same calendar months a year apart.
* Performance = 1 − breaches ÷ attendances by type and all types.
* Counterfactual formula with X floored at 0.
* Credit threshold of +2.0 points.

## 12. Build notes (scope tuning)

* Choose a trust that opened a co-located UTC reported under its own provider code during the year; confirm that the genuine flow effect is below
  +2.0 points while the headline gain exceeds +4.

# DS19 — Acting on probability forecasts: a "70% chance" is only worth what it verifies at

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Acting on model probabilities with a cost–loss trade-off (pre-positioning inventory before demand spikes, scaling capacity on predicted load, hedging on risk forecasts) |
| Domain | Energy trading / weather risk |
| Task shape | 10 · Scorecard against thresholds (regions × probability bins → observed frequency; the action rule adopted for buying cold-weather gas hedges) |
| Core method | Reliability analysis of 8–14 day temperature outlooks (forecast probability of "below normal" versus observed frequency) by region from archived outlooks and verifying observations; recalibration mapping; cost–loss decision rule: hedge if calibrated P(below) ≥ C/L; replay over the archive to compare realised costs with acting on raw probabilities and never/always hedging |
| Analytical stump | Applying the cost–loss threshold to issued probabilities assumes they are reliable. Outlook probabilities are often under-confident or over-confident by region and season; acting on raw probabilities hedges too rarely or too often. The decision needs reliability-corrected probabilities, evaluated by realised cost, not accuracy |
| Primary sources | NOAA Climate Prediction Center 8–14 day outlook archives (probabilities by region) and verification observations |

## 1. The real-world situation

A gas utility buys short-term cold-weather hedges when the 8–14 day outlook gives a high chance of below-normal temperatures. The hedge costs
C; an unhedged cold spell costs L (C/L = 0.40). The desk hedges whenever the issued probability of below-normal exceeds 40%. The risk team noted
that verification shows the issued probabilities are not reliable in all regions.

## 2. The decision (one deterministic recommendation)

**The action threshold on issued probability (per region) equivalent to calibrated P(below) ≥ 0.40, and the realised annual cost of the rule versus
the current raw-probability rule over the verification period.**

Rules (risk memo):

* Data: CPC 8–14 day outlook probabilities (below/near/above) for the utility's 4 climate regions (grid points in memo), 2015–2023 winters (Nov–Mar).
* Verification: observed week-2 mean temperature category at the same points (CPC verification data).
* Calibration: for each region, bin issued P(below) in 10-point bins; observed frequency per bin; isotonic mapping (memo) fitted on 2015–2019 and
  applied to 2020–2023.
* Decision: hedge if calibrated P ≥ 0.40; costs: hedge C per event; unhedged cold event L.
* Replay 2020–2023: realised cost for calibrated rule, raw rule, always-hedge and never-hedge.
* Report the issued-probability threshold equivalent to calibrated 0.40 per region.

## 3. Why capable analysts get it wrong

* Forecast probabilities are taken at face value.
* Reliability varies by region and lead time; biases change optimal actions.
* Accuracy metrics (hit rate) don't map to costs; cost–loss replay does.
* Calibration must be fitted out of sample.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `cpc_814day_outlooks_2015_2023.csv` (extracted grid points) | CSV | ~6k issuances × points | NOAA CPC archives | U.S. Gov public domain | Probabilities |
| 2 | `cpc_814day_verification_2015_2023.csv` | CSV | ~6k | NOAA CPC | Public domain | Observed categories |
| 3 | `cpc_outlook_archive_readme.txt` | Text | — | NOAA CPC | Public domain | Archive formats |
| 4 | `region_grid_points.json` | JSON | 4 regions | Task author | — | Regions |
| 5 | `risk_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `desk_raw_threshold_log.xlsx` | XLSX | ~300 | Task author | — | Current decisions |
| 7 | `cost_loss_reference.pdf` | PDF | — | Cite (Murphy 1977; Richardson 2000) | Cite | Cost–loss model |

## 5. Deterministic solution path

1. Align outlooks and verification by issuance and region.
2. Reliability tables; isotonic calibration on 2015–2019.
3. Apply rules to 2020–2023; realised costs; thresholds on issued probability.
4. Contrast with raw rule and trivial strategies.

## 6. Wrong paths (method errors, not misreadings)

**A — raw probability threshold.** Miscalibrated actions.

**B — calibrating on the replay period.** Optimistic.

**C — choosing by hit rate.** Not cost-relevant.

**D — pooling regions.** Region-specific biases lost.

## 7. Why the stump is analytical, not semantic

The calibration and decision rules are specified. The trap is trusting stated probabilities in a cost–loss decision.

## 8. Draft task prompt (prose)

> When should we buy cold-weather hedges based on the 8–14 day outlook? Calibrate the outlook probabilities by region and replay the cost–loss rule
> as the risk memo specifies. Provide `reliability_and_costs.csv` (region × bin: issued, observed frequency; rule costs), `reliability_diagrams.png`, and
> a one-page `hedging_rule.pdf`.

## 9. Deliverables

* `reliability_and_costs.csv`, `reliability_diagrams.png`, `hedging_rule.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 regions × 5 bins observed frequencies = 20; thresholds per region; realised costs for 4 strategies.

## 11. Golden-output checklist

* Alignment; binning; out-of-sample calibration; decision rule; replay costs.

## 12. Build notes (scope tuning)

* Confirm at least two regions have materially miscalibrated probabilities around 40%.

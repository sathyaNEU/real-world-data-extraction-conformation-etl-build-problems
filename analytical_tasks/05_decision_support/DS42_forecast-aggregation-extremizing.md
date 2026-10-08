# DS42 — Combining analysts' probability forecasts: the simple average is systematically timid

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Aggregating expert or analyst forecasts for go/no-go calls (deal-closing probabilities in sales forecasts, risk committees, prediction-market-style internal forecasting at tech companies) |
| Domain | Forecasting / judgement aggregation |
| Task shape | 10 · Scorecard against thresholds (aggregation methods × evaluation metrics → Brier score and decision cost; the aggregation rule adopted for the risk committee) |
| Core method | Aggregate individual probability forecasts per question: unweighted mean, median, mean of log-odds, and extremized log-odds mean (multiply by a = optimum fitted on a training set of questions); weighting by forecasters' past Brier scores; evaluate on held-out questions by Brier score and by decision cost at the committee's action threshold |
| Analytical stump | Averaging probabilities from forecasters with partially independent information regresses the aggregate toward 0.5; decisions made at thresholds (e.g., act if p ≥ 0.7) are then delayed or missed. Extremizing the log-odds mean (fitted out of sample) corrects under-confidence; fitting the extremizing factor on the evaluation questions overstates benefits |
| Primary sources | Good Judgment Project (IARPA ACE) forecasting tournament data (individual forecasts and question resolutions) |

## 1. The real-world situation

A company's risk committee asks 30 internal analysts for probabilities on geopolitical and market events and acts when the aggregate exceeds 0.70.
It averages analysts' latest forecasts. Post-mortems show that it acted late on events that happened and that the average rarely exceeded 0.70.

## 2. The decision (one deterministic recommendation)

**The aggregation rule adopted (lowest decision cost on held-out questions among the memo's four rules), its Brier score, and the extremizing
factor used.**

Rules (committee memo):

* Data: GJP individual forecasts (years 2–3 per memo), binary questions only; each forecaster's latest forecast per question as of 7 days before
  resolution (or close).
* Questions split by resolution date: first 60% train, last 40% test.
* Rules: (1) mean probability; (2) median; (3) mean of log-odds; (4) extremized log-odds mean with a chosen on training questions to minimise Brier
  (grid 1.0–3.0 step 0.1); forecasts clipped to [0.01, 0.99] before log-odds.
* Decision cost: act if aggregate ≥ 0.70; cost 1 for acting when the event does not occur, 3 for not acting when it occurs (memo).
* Adopt the rule with lowest test decision cost; ties → lower Brier.

## 3. Why capable analysts get it wrong

* Averages feel neutral and robust.
* Forecasters share some information and have private information; aggregation should be more extreme than the average.
* Extremizing must be fitted out of sample.
* Threshold decisions magnify under-confidence costs.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `gjp_individual_forecasts_y<n>.csv` | CSV | ~500k forecasts per year | Good Judgment Project data (Harvard Dataverse) | Dataverse licence (CC0 per deposit; verify) | Forecasts |
| 2 | `gjp_questions.csv` | CSV | ~600 | Same | Same | Question metadata, resolutions |
| 3 | `gjp_data_readme.pdf` | PDF | — | Same | Same | Fields |
| 4 | `committee_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `current_average_decisions.xlsx` | XLSX | — | Task author | — | Current rule results |
| 6 | `baron_2014_extremizing_citation.pdf` | PDF | — | Baron et al., Decision Analysis 2014 (cite) | Cite | Method |

## 5. Deterministic solution path

1. Filter binary questions; latest forecasts at the cutoff; split.
2. Fit extremizing factor on train.
3. Aggregate test forecasts by four rules; Brier and decision cost; choose.

## 6. Wrong paths (method errors, not misreadings)

**A — simple average.** Under-confident.

**B — extremizing fitted on test.** Optimistic.

**C — using all forecasts (not latest).** Stale forecasts.

**D — no clipping before log-odds.** Infinite values.

## 7. Why the stump is analytical, not semantic

Rules, cutoffs and costs are specified. The trap is naive aggregation of correlated expert probabilities.

## 8. Draft task prompt (prose)

> Which aggregation rule should the risk committee use? Compare the four rules on held-out questions as the committee memo specifies. Provide
> `aggregation_scorecard.csv` (rule: Brier, decision cost, acts, misses), `calibration_curves.png`, and a one-page `aggregation_policy.pdf`.

## 9. Deliverables

* `aggregation_scorecard.csv`, `calibration_curves.png`, `aggregation_policy.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 rules × (Brier, cost, acts, misses) = 16; extremizing factor; question counts; decision.

## 11. Golden-output checklist

* Question filter; cutoff; split; clipping; training fit; costs.

## 12. Build notes (scope tuning)

* Confirm the simple average has the highest decision cost.

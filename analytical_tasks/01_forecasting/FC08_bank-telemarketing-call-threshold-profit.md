# FC08 — How many clients should the call centre phone? Setting the score cut-off by money, not accuracy

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Score cut-offs set by expected value (sales outreach lists, fraud review queues, retention offers) rather than by accuracy metrics |
| Domain | Retail banking / direct marketing / propensity modelling |
| Task shape | 04 · Setting one dial (score threshold → number of calls) |
| Core method | Time-ordered train/validation/test split, admissible-feature propensity model (logistic regression, MLE), expected-profit threshold chosen on validation, reported on test |
| Analytical stump | The profit-maximizing cut-off comes from the cost/benefit ratio and calibrated probabilities, not from accuracy, F1 or 0.5; class imbalance and a time-shifted base rate make accuracy-based thresholds call far too few clients. A post-call feature (call duration) makes any threshold look perfect |
| Primary sources | UCI Bank Marketing dataset (Portuguese bank telemarketing campaigns, 2008–2010) |

## 1. The real-world situation

A bank's call centre runs term-deposit campaigns and wants a **score cut-off** for the next list: call every client whose
predicted subscription probability is above it. The analytics team trained a classifier with a random split, chose the
threshold that maximized accuracy, and recommended calling 4% of the list. The campaign manager pointed out that each call
costs a few euros and each subscription earns far more — so why call so few?

## 2. The decision (one deterministic recommendation)

**The probability cut-off (to 0.001) for the next campaign list, and the number of calls and expected profit it implies on
the held-out period.**

Rules (campaign analytics memo):

* Data: `bank-additional-full.csv`, which is ordered by contact date. Train = first 70% of rows, validation = next 10%,
  test = last 20% (no shuffling).
* Admissible features are those known before a call is placed: client attributes, previous-campaign attributes
  (`pdays`, `previous`, `poutcome`), contact channel, month, day of week, and the economic indicators. `duration` and
  `campaign` (contacts during this campaign, including the last) are not admissible.
* Model: unpenalized logistic regression (MLE), categorical variables one-hot with the first level dropped, `pdays = 999`
  encoded as a separate indicator with `pdays` set to 0.
* Economics: cost per call €6; margin per subscription €70.
* Choose the cut-off maximizing realized profit on the **validation** rows (candidate cut-offs = every distinct predicted
  probability); report calls, subscriptions and profit on the **test** rows at that cut-off.

## 3. Why capable analysts get it wrong

* Accuracy is maximized by predicting the majority class almost everywhere when only ~11% subscribe; F1 and 0.5 cut-offs
  also ignore the economics.
* The decision-theoretic cut-off is roughly cost ÷ margin (≈ 0.086) only if probabilities are calibrated for the period;
  the subscription rate shifts over time, so the cut-off must be tuned on a later, time-ordered validation slice.
* `duration` is measured after the call ends; including it inflates performance and is unusable in production.
* Random splits mix 2008 and 2010 contacts and overstate how well probabilities transfer.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `bank-additional-full.csv` | CSV (semicolon) | 41,188 | UCI ML Repository (id 222) | CC BY 4.0 | Main data, date-ordered |
| 2 | `bank-additional.csv` | CSV | 4,119 | UCI | CC BY 4.0 | 10% sample |
| 3 | `bank-full.csv`, `bank.csv` | CSV | 45,211 / 4,521 | UCI (older version) | CC BY 4.0 | Context only |
| 4 | `bank-additional-names.txt` | Text | — | UCI | CC BY 4.0 | Attribute notes (incl. duration warning) |
| 5 | `moro_cortez_rita_2014.pdf` | PDF | — | Decision Support Systems paper (cite) | Cite | Background |
| 6 | `ecb_euribor3m_monthly_2008_2010.csv` | CSV | ~36 | ECB | Re-use with attribution | Economic indicator cross-check |
| 7 | `ine_portugal_cpi_cci_2008_2010.xlsx` | XLSX | ~36 | Statistics Portugal (INE) | Re-use with attribution | Indicator cross-check |
| 8 | `campaign_economics.json` | JSON | — | Task author | — | Costs and margins |
| 9 | `campaign_analytics_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 10 | `team_random_split_results.xlsx` | XLSX | ~10 | Task author | — | Accuracy-based recommendation |

## 5. Deterministic solution path

1. Split by row order; build admissible features with the specified encoding.
2. Fit the logistic model on train; score validation and test.
3. Sweep cut-offs on validation; pick the profit maximizer (ties → higher cut-off).
4. Apply to test; report calls, subscriptions, profit, and the profit at 0.5, at the accuracy-maximizing cut-off and at
   cost ÷ margin.

## 6. Wrong paths (method errors, not misreadings)

**A — accuracy/F1/0.5 cut-off.** Calls a tiny fraction; profit far below optimum.

**B — random split.** Different cut-off and inflated expected profit.

**C — duration/campaign included.** Near-perfect validation scores; cut-off meaningless in production.

**D — cut-off tuned on test.** Optimistic reported profit.

## 7. Why the stump is analytical, not semantic

The memo defines admissible features, economics, split and model. The wrong answers come from optimizing the wrong
objective, ignoring class imbalance and temporal shift, or validating on the evaluation set — all methodological.

## 8. Draft task prompt (prose)

> Set the call cut-off for the next term-deposit campaign so that it maximizes profit, using the bank marketing data and
> the analytics memo in the folder. Train the specified model on the earliest contacts, pick the cut-off on the validation
> slice and report what it delivers on the latest contacts. Give me `cutoff_sweep.csv` (for each candidate cut-off on
> validation: calls, subscriptions, profit), `profit_curve.png` showing validation and test profit against the number of
> clients called with the chosen cut-off, the 0.5 cut-off and the accuracy-optimal cut-off marked, and a one-page
> `call_plan.pdf` with the cut-off, test-period calls, subscriptions and profit, and the profit lost under the team's
> accuracy-based recommendation.

## 9. Deliverables

* `cutoff_sweep.csv`, `profit_curve.png`, `call_plan.pdf`.

## 10. Where 25+ rubric criteria come from

* Cut-off; validation and test calls/subscriptions/profit; three comparator cut-offs × (calls, profit); model coefficient
  spot-checks; leakage exclusion.

## 11. Golden-output checklist

* Time-ordered split; admissible features; specified encoding; validation-tuned cut-off; test reporting; comparators.

## 12. Build notes (scope tuning)

* Verify the row ordering by date in the file (documented by UCI) and that the accuracy-optimal cut-off calls < 25% of the
  calls made at the profit-optimal cut-off.
* Publish the reference coefficients (rounded) so graders can verify model fitting.

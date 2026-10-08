# OS22 — Fraud model ROI: catching many small frauds is not catching the money

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Payment-risk teams sizing the value of a new fraud model (card issuers, payment processors, marketplaces), where review costs and fraud amounts drive economics |
| Domain | Payments risk |
| Task shape | 04 · Setting one dial (the review threshold on the model score that maximises net savings; the annualised savings at that threshold) |
| Core method | Time-ordered train/test split; model scores on the test period; for each threshold: blocked fraud amount (sum of amounts of true frauds above threshold), review cost (alerts × cost per review), customer friction cost (false positives × amount-based cost per memo); net savings curve; choose the maximum |
| Analytical stump | Sizing with count-based metrics (recall, F1, AUC) treats a $2 test charge like a $2,000 fraud and ignores the cost of reviewing alerts. Random splits leak time patterns. The threshold maximising F1 is not the one maximising money saved, and the sized savings differ by multiples |
| Primary sources | ULB Machine Learning Group credit card fraud dataset (European cardholders, September 2013) |

## 1. The real-world situation

A card issuer's risk team proposes replacing its rules with a model. The proposal reported "recall 85% at F1-optimal threshold" and sized
savings as recall × total fraud losses. Finance asked for the threshold that maximises net savings, including the cost of reviews and false
declines, and the resulting annual value.

## 2. The decision (one deterministic recommendation)

**The review threshold (score to two decimals) maximising net savings on the test period, and the annualised net savings at that threshold.**

Rules (risk memo):

* Data: ULB credit card dataset; split by `Time`: first 70% of transactions for training, last 30% for testing.
* Model: logistic regression on V1–V28 and scaled Amount with class weights per memo (fixed solver and regularisation), trained on the training
  part only.
* For thresholds 0.01–0.99 step 0.01 on test scores:
  * blocked fraud = Σ Amount of frauds with score ≥ t;
  * review cost = €3 × alerts;
  * false-decline cost = 5% × Σ Amount of legitimate transactions with score ≥ t (memo convention).
* Net savings = blocked − review cost − false-decline cost; choose maximum (ties → higher t).
* Annualise: test period covers ~0.6 days of the two-day dataset; scale by the memo's annualisation factor based on the issuer's volume.

## 3. Why capable analysts get it wrong

* ML evaluation reflexes optimise count-based metrics.
* Fraud amounts are skewed; a few large frauds dominate losses.
* Each alert costs money; low thresholds create many alerts.
* Time leakage inflates performance.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `creditcard.csv` | CSV | 284,807 | ULB MLG (Kaggle / OpenML mirror) | Open Database License (DbCL v1.0) | Transactions (PCA features, amount, class) |
| 2 | `dataset_description.pdf` | PDF | — | Dal Pozzolo et al. (cite) | Cite | Description |
| 3 | `risk_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 4 | `proposal_f1_sizing.xlsx` | XLSX | — | Task author | — | Naive sizing |
| 5 | `model_spec.json` | JSON | — | Task author | — | Solver, regularisation, seed |
| 6 | `cost_assumptions.json` | JSON | — | Task author | — | Costs and annualisation |
| 7 | `threshold_check_values.json` | JSON | ~5 | Task author | — | Checks |

## 5. Deterministic solution path

1. Time split; train the model per spec; score the test set.
2. Sweep thresholds; compute net savings components.
3. Choose threshold; annualise; contrast with F1-based sizing.

## 6. Wrong paths (method errors, not misreadings)

**A — F1-optimal threshold.** Wrong economics.

**B — recall × total losses.** Ignores amounts and costs.

**C — random split.** Optimistic.

**D — ignoring false-decline costs.** Threshold too low.

## 7. Why the stump is analytical, not semantic

Model, split and costs are specified. The trap is optimising the wrong objective for sizing.

## 8. Draft task prompt (prose)

> What threshold should the new fraud model run at, and what is it worth per year? Follow the risk memo: time-ordered evaluation and net
> savings in money. Provide `threshold_sweep.csv` (threshold: alerts, blocked fraud, costs, net), `net_savings_curve.png`, and a one-page
> `model_value.pdf`.

## 9. Deliverables

* `threshold_sweep.csv`, `net_savings_curve.png`, `model_value.pdf`.

## 10. Where 25+ rubric criteria come from

* Threshold; sweep values at 10 thresholds; components at the optimum; annualised value; F1 contrast.

## 11. Golden-output checklist

* Time split; model spec; cost components; sweep; tie rule; annualisation.

## 12. Build notes (scope tuning)

* Confirm the F1-optimal threshold differs from the net-savings optimum by ≥ 0.1.

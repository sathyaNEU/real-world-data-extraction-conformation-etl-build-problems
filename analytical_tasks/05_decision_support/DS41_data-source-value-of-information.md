# DS41 — Is the extra data source worth buying? Measure it in decisions changed, not in AUC

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Buying third-party data or building expensive features (credit bureau attributes, enrichment vendors, telemetry) where the value lies in better decisions |
| Domain | Consumer credit / risk management |
| Task shape | 13 · Scenarios and the flip point (data cost per applicant × loss-given-default scenarios → net value of the data source; buy or not, and the data price at which the decision flips) |
| Core method | Two models — base (credit limit and education, protected attributes excluded) and enhanced (+ repayment history features as the "purchased" source); calibrated PDs; approval decision per applicant maximising expected profit (margin × balance × (1 − PD) − LGD × balance × PD > 0); value of information = profit(enhanced decisions) − profit(base decisions) on a held-out set, per applicant, minus data cost |
| Analytical stump | An AUC gain of a few points says little about money; value comes only from applicants whose decision changes and depends on margins, balances and LGD. The data can have large AUC lift and small decision value (or the reverse); the buy decision requires expected-profit comparison |
| Primary sources | UCI "Default of Credit Card Clients" dataset (Taiwan, 2005) |

## 1. The real-world situation

A card issuer is offered a data feed with applicants' recent repayment history at $1.80 per application. The data-science team showed that adding
the features raises AUC from 0.71 to 0.78 and recommended buying. Finance asked what the feed is worth in approval-decision profit per applicant.

## 2. The decision (one deterministic recommendation)

**Buy or not at $1.80 per application, the net value per 1,000 applicants, and the price at which the decision flips.**

Rules (risk memo):

* Data: UCI Taiwan credit dataset; target = default next month; split 60/20/20 (train/calibration/test, seed 11, stratified).
* Base features: LIMIT_BAL and EDUCATION (memo excludes sex, marital status and age as protected attributes); enhanced = base + PAY_0…PAY_6
  and BILL_AMT/PAY_AMT features.
* Models: gradient boosting (fixed hyperparameters), isotonic calibration on the calibration split.
* Economics per applicant: exposure = LIMIT_BAL × 0.3 (memo's expected balance), annual margin 12%, LGD 0.6.
* Decision: approve if 0.12 × exposure × (1 − PD) − 0.6 × exposure × PD > 0.
* Realised profit on test using actual outcomes: approved non-defaulters earn margin; approved defaulters lose LGD × exposure; declined = 0.
* VOI per applicant = (profit_enhanced − profit_base) ÷ applicants − data cost.
* Scenarios: LGD 0.4/0.6/0.8 × price $1.00/$1.80/$3.00; flip price at LGD 0.6.

## 3. Why capable analysts get it wrong

* AUC is the standard model metric.
* Decision value depends on threshold region and economics.
* Calibration matters for threshold decisions.
* Data cost is per applicant, value only for changed decisions.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `default_of_credit_card_clients.xls` | XLS | 30,000 | UCI ML Repository (id 350) | CC BY 4.0 | Clients, features, default |
| 2 | `uci_credit_description.html` | HTML | — | UCI | CC BY 4.0 | Variables |
| 3 | `yeh_lien_2009_citation.pdf` | PDF | — | Yeh & Lien 2009 (cite) | Cite | Dataset paper |
| 4 | `risk_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `ds_team_auc_case.xlsx` | XLSX | — | Task author | — | AUC-based case |
| 6 | `model_spec.json` | JSON | — | Task author | — | Hyperparameters, seeds |
| 7 | `economics.json` | JSON | — | Task author | — | Margin, LGD, exposure |

## 5. Deterministic solution path

1. Split; train base and enhanced models; calibrate.
2. Decisions on test; realised profits; VOI per applicant.
3. Scenario grid; flip price; decision.

## 6. Wrong paths (method errors, not misreadings)

**A — buy on AUC lift.** Ignores economics.

**B — uncalibrated PDs.** Wrong approvals.

**C — evaluating on training data.** Optimistic VOI.

**D — counting value for unchanged decisions.** Inflated.

## 7. Why the stump is analytical, not semantic

The models, economics and evaluation are specified. The trap is measuring information value with a ranking metric.

## 8. Draft task prompt (prose)

> Should we buy the repayment-history data feed at $1.80 per application? Compare decisions with and without it in expected-profit terms as the risk
> memo specifies. Provide `voi_scenarios.csv` (LGD × price: VOI per 1,000 applicants), `decision_changes.png`, and a one-page `data_purchase.pdf` with the
> flip price.

## 9. Deliverables

* `voi_scenarios.csv`, `decision_changes.png`, `data_purchase.pdf`.

## 10. Where 25+ rubric criteria come from

* 9 scenario cells; AUCs; approval rates; changed decisions; profits; flip price; decision.

## 11. Golden-output checklist

* Split and seeds; feature sets; calibration; decision rule; realised profit; VOI.

## 12. Build notes (scope tuning)

* Choose economics so that VOI is near the price (decision sensitive) while AUC lift looks large.

# FC46 — Which customers will buy again? A great past rate means little if the customer has quietly left

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | E-commerce and subscription CRM forecasting customer lifetime activity (non-contractual churn) |
| Domain | Retail / CRM analytics |
| Task shape | 01 · Ranked list under a cap (500 customers for a loyalty programme) |
| Core method | BG/NBD model (Pareto/NBD-type) fitted by maximum likelihood on a calibration window; conditional expected transactions and P(alive) given each customer's frequency and recency |
| Analytical stump | In non-contractual settings you never see churn. Ranking by historical purchase rate (or frequency × 52) assumes every customer is still active; a frequent buyer who has been silent for months is probably gone. Recency must enter through a probabilistic model, not a heuristic score |
| Primary sources | CDNOW customer transaction dataset (Fader & Hardie) |

## 1. The real-world situation

An online music retailer invites **500 customers** into a loyalty programme designed to retain its most valuable *future* buyers.
Marketing ranked customers by purchases per week since their first order and projected 39 more weeks. Many invitees never bought
again; several customers who were buying steadily were left out.

## 2. The decision (one deterministic recommendation)

**The 500 customers with the highest expected number of repeat transactions in the next 39 weeks, and customer #501.**

Rules (CRM memo):

* Data: the CDNOW master dataset (cohort of first purchases in Q1 1997). Calibration period: first 39 weeks from each customer's
  first purchase window start (1997-01-01 to 1997-09-30); holdout: next 39 weeks (to 1998-06-30).
* Per customer: x = repeat transactions in calibration (same-day purchases count once), t_x = time of last repeat purchase (weeks
  since first purchase), T = weeks from first purchase to end of calibration.
* Fit BG/NBD parameters (r, α, a, b) by maximum likelihood on all customers (Fader, Hardie & Lee 2005).
* Score = conditional expected transactions in the next 39 weeks given (x, t_x, T). Rank; ties by higher P(alive), then lower ID.
* Validation: compare predicted vs actual holdout transactions for the selected 500 and for marketing's 500.

## 3. Why capable analysts get it wrong

* Rate-based projections are intuitive and treat every customer as permanently active.
* Recency is the signal of dropout; a probabilistic model turns long silence into a low probability of being alive.
* Same-day multiple transactions inflate frequency unless collapsed.
* Calibration and holdout must not overlap.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `CDNOW_master.txt` | Text | ~69.7k transactions | Bruce Hardie's teaching datasets (CDNOW) | Distributed for research/teaching (verify terms) | Transactions (ID, date, units, value) |
| 2 | `CDNOW_sample.txt` | Text | ~6.9k | Same | Same | 10% sample (for checking estimates) |
| 3 | `cdnow_customer_summary.csv` | CSV | 23,570 | Derived | Same | x, t_x, T |
| 4 | `fader_hardie_lee_2005_bgnbd.pdf` (citation) | PDF | — | Marketing Science 2005 (cite) | Cite | Model and formulas |
| 5 | `bgnbd_implementation_note.pdf` (citation) | PDF | — | Fader & Hardie note (cite) | Cite | Likelihood details |
| 6 | `crm_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `marketing_rate_ranking.xlsx` | XLSX | 500 | Task author | — | Rate-based list |
| 8 | `weekly_repeat_transactions.csv` | CSV | 78 | Derived | Same | Aggregate tracking plot data |
| 9 | `parameter_check_sample.json` | JSON | — | Task author (published sample estimates for verification) | — | Sanity check |
| 10 | `holdout_actuals.csv` | CSV | 23,570 | Derived | Same | Validation only |

## 5. Deterministic solution path

1. Collapse same-day transactions; compute x, t_x, T per customer in calibration.
2. Fit BG/NBD by MLE; report parameters (check against published values for the sample).
3. Compute conditional expectations and P(alive); rank; select 500.
4. Validate on the holdout; contrast with the rate-based list.

## 6. Wrong paths (method errors, not misreadings)

**A — rate × 39 weeks.** Selects lapsed heavy buyers.

**B — RFM score without a model.** Arbitrary weights; different list.

**C — same-day duplicates kept.** Inflated frequency.

**D — fitting on calibration + holdout.** Look-ahead.

## 7. Why the stump is analytical, not semantic

All quantities are defined; the trap is the modelling assumption that customers never churn unobservably.

## 8. Draft task prompt (prose)

> Choose the 500 customers for the loyalty programme as the CRM memo specifies: fit the BG/NBD model on the first 39 weeks and rank
> customers by expected repeat purchases in the next 39. Provide `customer_scores.csv` (customer: x, t_x, T, P(alive), expected
> transactions, rank), `frequency_recency_heatmap.png` (expected transactions by frequency and recency), and a one-page
> `loyalty_selection.pdf` with the list summary, customer #501, parameter estimates and the holdout comparison with marketing's list.

## 9. Deliverables

* `customer_scores.csv`, `frequency_recency_heatmap.png`, `loyalty_selection.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 parameters; scores for 10 named customers; #500 and #501; holdout totals for both lists; overlap count.

## 11. Golden-output checklist

* Same-day collapse; correct x/t_x/T; MLE; conditional expectation; tie rule; holdout validation.

## 12. Build notes (scope tuning)

* Verify licence terms for redistribution of CDNOW; if restricted, link to the source instead of shipping the file.
* Confirm the overlap between the two 500-lists is below 70%.

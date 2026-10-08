# DS44 — Who gets the fundraising mailing? Likely donors give small amounts; big givers respond rarely

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Value-based targeting (marketing to maximise revenue rather than conversions, sales prioritisation by expected deal value) |
| Domain | Nonprofit fundraising / direct marketing |
| Task shape | 01 · Ranked list under a cap (households mailed in the next campaign: all with expected net gift > mailing cost, ranked by expected net value) |
| Core method | Two-part model: P(response) from a classifier and E[gift | response] from a regression on responders only (log-gift with smearing per memo); expected value = P × E[gift | response]; mail if expected value > $0.68; evaluate realised net donations on the validation file; compare with mailing the top-probability households |
| Analytical stump | Targeting by response probability (or by a single model of donation amount including zeros) ignores that gift size and response probability are negatively related across donors; maximising responses does not maximise net donations. The decision rule must combine both parts and compare with the mailing cost |
| Primary sources | KDD Cup 1998 donor dataset (Paralyzed Veterans of America mailing; UCI KDD Archive) |

## 1. The real-world situation

A charity mails appeals at $0.68 per piece. The marketing vendor targets households with the highest predicted probability of responding. The
development director notes that a few large donors respond rarely but give far more than typical respondents.

## 2. The decision (one deterministic recommendation)

**The mailing rule (expected value > $0.68), the number of households mailed in the validation file, and realised net donations versus the
probability-ranked rule mailing the same number.**

Rules (fundraising memo):

* Data: KDD Cup 1998 learning file (95,412 records; TARGET_B response, TARGET_D amount) and validation file with outcomes (per the archive).
* Features: the memo's set (RFA codes, past giving summaries, demographics excluding protected attributes per memo).
* Response model: logistic regression (fixed spec) on learning file.
* Amount model: OLS on log(TARGET_D) for responders; smearing correction for the mean.
* EV = P × E[gift | response]; mail if EV > 0.68.
* Realised net on validation = Σ actual gifts of mailed − 0.68 × mailed.
* Contrast: mail the same number of households ranked by P.

## 3. Why capable analysts get it wrong

* Response models are standard in direct marketing.
* Value = probability × amount; the two are negatively correlated.
* Log-amount models need back-transformation bias correction.
* Comparing rules at equal mailing volume isolates targeting quality.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `cup98LRN.txt` | Text (CSV) | 95,412 | UCI KDD Archive (KDD Cup 1998) | Archive terms (public research use; cite) | Learning data |
| 2 | `cup98VAL.txt` | Text | 96,367 | Same | Same | Validation data |
| 3 | `valtargt.txt` | Text | 96,367 | Same | Same | Validation outcomes |
| 4 | `cup98DOC.txt`, `cup98DIC.txt` | Text | — | Same | Same | Documentation, dictionary |
| 5 | `fundraising_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `vendor_probability_targeting.xlsx` | XLSX | — | Task author | — | Current rule |
| 7 | `feature_spec.json` | JSON | — | Task author | — | Features |

## 5. Deterministic solution path

1. Prepare features; fit response and amount models on learning data.
2. Score validation; EV; mail decision.
3. Realised net; probability-ranked contrast at equal volume.

## 6. Wrong paths (method errors, not misreadings)

**A — rank by probability.** Misses high-value donors.

**B — single regression of TARGET_D with zeros.** Poor fit; wrong EV.

**C — no smearing.** Underestimates expected gifts.

**D — evaluating on learning file.** Optimistic.

## 7. Why the stump is analytical, not semantic

The models and decision rule are specified. The trap is optimising a proxy (response) for the objective (net revenue).

## 8. Draft task prompt (prose)

> Who should receive the next appeal? Combine response probability and expected gift as the fundraising memo specifies and compare with
> probability-based targeting on the validation file. Provide `mailing_results.csv` (rule: mailed, responders, gifts, net), `value_vs_probability.png`,
> and a one-page `mailing_policy.pdf`.

## 9. Deliverables

* `mailing_results.csv`, `value_vs_probability.png`, `mailing_policy.pdf`.

## 10. Where 25+ rubric criteria come from

* Mailed counts; net donations (2 rules); responders; model coefficients; smearing factor; deciles of EV (10).

## 11. Golden-output checklist

* Feature prep; two-part models; smearing; threshold; equal-volume contrast.

## 12. Build notes (scope tuning)

* Confirm the EV rule yields higher net donations than probability ranking at equal volume.

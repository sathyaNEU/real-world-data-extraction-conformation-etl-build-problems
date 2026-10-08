# DS30 — Setting a catch limit: the point estimate of the overfishing limit is not the limit

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Setting limits under estimation uncertainty with a tolerated breach probability (rate limits, credit limits, quotas, emission caps) |
| Domain | Fisheries management |
| Task shape | 04 · Setting one dial (the acceptable biological catch for each of 6 stocks, given the overfishing limit's uncertainty and the council's tolerance P* = 0.40) |
| Core method | Overfishing limit (OFL) from the latest assessment as a lognormal distribution with σ from the assessment's CV (minimum σ per memo); ABC = OFL_median × exp(z_{P*} × σ) (P* approach); compare with setting catch at the OFL point estimate or a fixed 25% buffer; projected probability of overfishing for each rule |
| Analytical stump | Setting catch equal to the estimated OFL gives a ~50% chance of overfishing; a fixed percentage buffer ignores that uncertainty differs by stock. The P* approach links the buffer to each stock's estimation uncertainty and the tolerated risk |
| Primary sources | NOAA Fisheries Stock Assessment and Fishery Evaluation (Stock SMART) assessment summaries |

## 1. The real-world situation

A regional fishery council sets annual catch limits for 6 stocks. A proposal set each limit at the latest OFL point estimate minus a uniform 10%.
Scientific advisers pointed out that two stocks have highly uncertain assessments and one is well estimated; the council's policy tolerates a 40%
probability of exceeding OFL.

## 2. The decision (one deterministic recommendation)

**The ABC for each stock (tonnes, rounded to the nearest 10 t) under P* = 0.40, and each rule's probability of overfishing.**

Rules (council memo):

* Data: Stock SMART latest assessment per stock: OFL (or F_MSY-based catch), biomass and F estimates with uncertainty (CV) where reported.
* σ = max(reported CV of OFL proxy converted to lognormal σ, 0.36) (memo's minimum uncertainty for data-moderate stocks).
* ABC = OFL × exp(Φ⁻¹(0.40) × σ).
* Probability of overfishing for a catch C: P(OFL < C) = Φ((ln C − ln OFL) ÷ σ).
* Rules compared: ABC (P*), OFL × 0.9 (proposal), OFL (no buffer).

## 3. Why capable analysts get it wrong

* Point estimates are presented prominently.
* Uncertainty differs among stocks; uniform buffers misallocate risk.
* Lognormal uncertainty makes the median the natural centre; z-scores apply on the log scale.
* Minimum uncertainty prevents overconfident assessments from driving tiny buffers.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `stock_smart_assessment_summary.xlsx` | XLSX | ~1k assessments | NOAA Fisheries Stock SMART | U.S. Gov public domain | Assessment results |
| 2 | `stock_smart_time_series.csv` | CSV | ~100k | NOAA Fisheries | Public domain | Biomass, F, catch series |
| 3 | `stocks_in_scope.json` | JSON | 6 | Task author | — | Stocks and OFL fields |
| 4 | `council_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `proposal_uniform_buffer.xlsx` | XLSX | 6 | Task author | — | Proposal |
| 6 | `pstar_approach_citation.pdf` | PDF | — | Prager & Shertzer 2010; NOAA guidance (cite) | Public | Method |

## 5. Deterministic solution path

1. Extract OFL and uncertainty per stock; σ with minimum.
2. ABC by P*; probabilities of overfishing for each rule.
3. Compare; recommendation table.

## 6. Wrong paths (method errors, not misreadings)

**A — OFL as the limit.** ~50% overfishing risk.

**B — uniform buffer.** Ignores stock-specific uncertainty.

**C — normal (not lognormal) uncertainty.** Wrong buffer.

**D — ignoring σ minimum.** Overconfident buffers.

## 7. Why the stump is analytical, not semantic

The distributions and P* rule are specified. The trap is treating an uncertain estimate as a known limit.

## 8. Draft task prompt (prose)

> What catch limits should the council set for the six stocks? Apply the P* buffer to each stock's OFL uncertainty as the council memo specifies and
> compare with the uniform-buffer proposal. Provide `abc_table.csv` (stock: OFL, σ, ABC, P(overfishing) by rule), `risk_by_rule.png`, and a one-page
> `catch_limits.pdf`.

## 9. Deliverables

* `abc_table.csv`, `risk_by_rule.png`, `catch_limits.pdf`.

## 10. Where 25+ rubric criteria come from

* 6 stocks × (σ, ABC, 3 risks) = 30; recommendation.

## 11. Golden-output checklist

* OFL extraction; σ conversion; minimum; formula; probabilities; rounding.

## 12. Build notes (scope tuning)

* Choose stocks with CVs spanning 0.1–0.8 so the uniform buffer is too tight for some and too loose for others.

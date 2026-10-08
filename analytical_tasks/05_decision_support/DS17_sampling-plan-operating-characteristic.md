# DS17 — How many samples per window? A plan that rarely fails good plants also rarely catches bad ones

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Acceptance-sampling and audit-frequency decisions (supplier lot inspection, data-quality audits, compliance sampling) |
| Domain | Food safety / meat and poultry processing |
| Task shape | 10 · Scorecard against thresholds (candidate sampling plans × true-prevalence scenarios → probability of flagging; the plan adopted for the next year) |
| Core method | Operating characteristic (OC) curves: for a plan with n samples per 52-week window and acceptance number c, P(flag) = 1 − Binomial CDF(c; n, p) across true prevalence p; estimate the distribution of true establishment prevalence from historical results (beta-binomial fit); choose the smallest n meeting both a producer-risk limit (flag ≤ 5% of plants at p = the standard) and a consumer-risk target (flag ≥ 80% at p = 2× standard) |
| Analytical stump | Judging plans by the observed share of establishments flagged in past data confounds plan performance with the prevalence mix. Small n with a fixed acceptance number has weak power; raising c to protect good plants silently lets bad ones pass. Decisions require OC curves at the policy-relevant prevalences |
| Primary sources | USDA FSIS Salmonella verification sampling results (establishment-level sample results for raw poultry) |

## 1. The real-world situation

A regulator reviews its sampling plan for a raw-poultry product: samples per establishment per 52-week window and the maximum allowable positives
before an establishment is flagged. A proposal to cut samples from 52 to 26 per window cited the fact that the share of establishments flagged
barely changed when the previous plan was relaxed.

## 2. The decision (one deterministic recommendation)

**The plan adopted (n, c) from the memo's candidate list, its producer and consumer risks, and whether the proposed 26-sample plan meets the
targets.**

Rules (sampling memo):

* Data: FSIS Salmonella verification results for the product class in memo, 2019–2023: establishment, sample date, result.
* Standard: maximum acceptable prevalence p0 (memo, e.g., 9.8%); "bad" prevalence p1 = 2 × p0.
* Candidate plans: (n, c) pairs in `candidate_plans.json` (e.g., (52, 5), (39, 4), (26, 3), (26, 2)).
* OC: P(flag | p) = 1 − Σ_{k≤c} C(n,k) p^k (1−p)^{n−k}.
* Producer risk: P(flag | p0) ≤ 5%; consumer risk: P(flag | p1) ≥ 80%.
* Choose the plan with the smallest n meeting both; ties → larger c.
* Context: beta-binomial fit to establishment-level positives to show how many establishments sit near p0 and p1 (reported, not used in the rule).

## 3. Why capable analysts get it wrong

* Historical flag rates seem to measure plan effectiveness.
* Flag rates depend on how many plants are near the standard.
* Power falls quickly with fewer samples.
* Producer and consumer risks must both be checked.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `fsis_salmonella_verification_<product>_2019_2023.csv` | CSV | ~100k samples | USDA FSIS sampling datasets | U.S. Gov public domain | Sample results |
| 2 | `fsis_sampling_program_documentation.pdf` | PDF | — | USDA FSIS | Public domain | Programme description |
| 3 | `candidate_plans.json` | JSON | ~6 | Task author | — | Plans |
| 4 | `performance_standard.json` | JSON | — | Task author (from FSIS standards) | Public domain | p0 |
| 5 | `sampling_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `proposal_flag_rate_argument.xlsx` | XLSX | — | Task author | — | Proposal evidence |
| 7 | `acceptance_sampling_reference.pdf` | PDF | — | Cite (Montgomery, SQC) | Cite | OC curves |

## 5. Deterministic solution path

1. Compute OC values for each plan at p0 and p1; full OC curves.
2. Apply the risk targets; choose the plan.
3. Fit beta-binomial to establishment data for context; contrast with the proposal's evidence.

## 6. Wrong paths (method errors, not misreadings)

**A — historical flag-rate comparison.** Confounded by prevalence mix.

**B — producer risk only.** Weak plans pass.

**C — normal approximation at small n.** Misstated risks.

**D — choosing by average prevalence.** Not the policy-relevant points.

## 7. Why the stump is analytical, not semantic

Plans, standards and targets are specified. The trap is evaluating a test by outcomes rather than by its error rates.

## 8. Draft task prompt (prose)

> Which sampling plan should we adopt, and does the 26-sample proposal meet our risk targets? Compute OC curves for the candidate plans as the sampling
> memo specifies. Provide `plan_scorecard.csv` (plan: n, c, P(flag) at p0 and p1, meets targets), `oc_curves.png`, and a one-page
> `sampling_plan_decision.pdf`.

## 9. Deliverables

* `plan_scorecard.csv`, `oc_curves.png`, `sampling_plan_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 6 plans × (P at p0, P at p1, pass) = 18; chosen plan; proposal verdict; beta-binomial parameters; contrast.

## 11. Golden-output checklist

* Exact binomial; targets; tie rule; context fit; verdict.

## 12. Build notes (scope tuning)

* Confirm the 26-sample proposal fails the consumer-risk target.

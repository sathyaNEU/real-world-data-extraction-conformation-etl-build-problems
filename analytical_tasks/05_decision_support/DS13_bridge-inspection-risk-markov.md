# DS13 — Which bridges get more frequent inspection? Risk is probability of decline times consequence

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Risk-based inspection and monitoring frequency decisions (security audits, equipment inspections, data-quality checks) where current state alone misguides priorities |
| Domain | Infrastructure safety |
| Task shape | 10 · Scorecard against thresholds (bridges × risk components → inspection interval tier: 12, 24 or 48 months; the bridges moved to 12-month inspection) |
| Core method | Markov transition probabilities of deck/superstructure/substructure condition ratings by material, age band and ADT band estimated from consecutive NBI years; probability of reaching rating ≤ 4 within 24 months; consequence score from ADT × detour length; risk = probability × consequence; tier thresholds per memo |
| Analytical stump | Assigning frequent inspection to bridges with the lowest current rating ignores that some fair-rated bridges deteriorate quickly (material, age, traffic) and that consequences differ by orders of magnitude (detour length, traffic). Probability-weighted consequence ranks differ sharply from condition-only ranking |
| Primary sources | FHWA National Bridge Inventory (NBI) delimited files (multiple years) |

## 1. The real-world situation

A state DOT may reduce routine inspection intervals for low-risk bridges to 48 months and must move high-risk bridges to 12 months. The draft
policy put all bridges with any component rated 5 or lower on 12 months. Engineers argued for a risk-based approach under the federal
risk-based inspection framework.

## 2. The decision (one deterministic recommendation)

**The list of bridges assigned to 12-month inspection (risk ≥ the memo's upper threshold), the counts per tier, and bridges whose tier differs from
the draft policy.**

Rules (inspection memo):

* Data: NBI files for the state for 2013–2023; items 58 (deck), 59 (superstructure), 60 (substructure), 43 (structure type/material), 27 (year
  built), 29 (ADT), 19 (detour length).
* Transitions: for each component, empirical one-year transition matrices by material × age band (0–24, 25–49, 50+) × ADT band (< 5k, 5–25k,
  > 25k); two-step product for 24 months.
* P(fail) = probability that the minimum of the three components reaches ≤ 4 within 24 months (memo: treat components independently).
* Consequence = ADT × detour length (km) normalised to 0–1 by the state's 99th percentile.
* Risk = P(fail) × consequence. Tiers: 12 months if risk ≥ 0.02; 48 months if risk < 0.002 and all ratings ≥ 7; otherwise 24.
* Report draft-policy tiers for contrast.

## 3. Why capable analysts get it wrong

* Current condition ratings are the most familiar indicators.
* Deterioration speed varies with material, age and traffic.
* Consequence matters as much as probability for inspection priorities.
* Multi-year matrices need consistent bridge identifiers across files.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–11 | `<ST><yy>.txt` (2013–2023) | Comma-delimited text | ~10–50k bridges per year | FHWA NBI | U.S. Gov public domain | Bridge records |
| 12 | `nbi_recording_coding_guide.pdf` | PDF | — | FHWA | Public domain | Item definitions |
| 13 | `inspection_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 14 | `draft_policy_tiers.xlsx` | XLSX | ~bridges | Task author | — | Draft tiers |
| 15 | `transition_matrix_check.json` | JSON | — | Task author | — | Check values for one stratum |
| 16 | `fhwa_rbi_framework_citation.pdf` | PDF | — | FHWA risk-based inspection guidance (cite) | Public domain | Context |

## 5. Deterministic solution path

1. Link bridges across years; build transition counts by stratum and component.
2. Transition matrices; two-step probabilities; P(fail).
3. Consequence; risk; tiers.
4. Contrast with the draft policy.

## 6. Wrong paths (method errors, not misreadings)

**A — condition-only tiers.** Ignores dynamics and consequence.

**B — pooled transitions across materials.** Misestimated deterioration.

**C — one-step probability for 24 months.** Underestimates.

**D — consequence ignored.** Rural low-traffic bridges overprioritised.

## 7. Why the stump is analytical, not semantic

Items, strata and formulas are specified. The trap is static condition versus dynamic risk.

## 8. Draft task prompt (prose)

> Which bridges should move to 12-month inspections under the risk-based approach in the inspection memo? Estimate deterioration probabilities from
> NBI histories and combine them with consequences. Provide `bridge_risk_scorecard.csv` (bridge: ratings, P(fail), consequence, risk, tier, draft
> tier), `risk_matrix.png`, and a one-page `inspection_intervals.pdf`.

## 9. Deliverables

* `bridge_risk_scorecard.csv`, `risk_matrix.png`, `inspection_intervals.pdf`.

## 10. Where 25+ rubric criteria come from

* 12-month list; tier counts; values for 10 bridges; transition check; contrast counts.

## 11. Golden-output checklist

* Linking; strata; matrices; two-step; P(fail); consequence normalisation; thresholds.

## 12. Build notes (scope tuning)

* Choose a state with diverse materials; confirm at least 30% of draft 12-month bridges move to 24 months.

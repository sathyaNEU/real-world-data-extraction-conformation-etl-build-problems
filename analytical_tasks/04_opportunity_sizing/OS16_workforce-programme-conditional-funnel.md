# OS16 — Where does a training dollar buy the most jobs? Stage rates must be conditional on reaching the stage

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Product and sales funnels (visit → sign-up → activation → paid), hiring funnels, onboarding flows — choosing the stage to invest in |
| Domain | Workforce development |
| Task shape | 09 · Funnel or chain of stages (registered → enrolled in training → completed training → credential attained → employed in 2nd quarter after exit; the stage where $2M buys the most additional employed completers) |
| Core method | Conditional pass-through rates computed on the cohort reaching each stage (same exit cohort), unit cost per additional pass-through at each stage from the memo's cost table; marginal employed outcomes from raising one stage's rate, propagated through downstream conditional rates |
| Analytical stump | Reported performance tables give each outcome as a share of all exiters (unconditional) or with different denominators and cohorts. Multiplying unconditional rates double-applies earlier stages; mixing cohorts misstates conversion. The best stage to fund depends on conditional rates and costs |
| Primary sources | U.S. DOL ETA Workforce Innovation and Opportunity Act (WIOA) Participant Individual Record Layout (PIRL) public use data |

## 1. The real-world situation

A state workforce board has $2M to improve outcomes in its adult programme. Staff ranked stages by the published performance indicators
("credential rate 58%", "employment rate Q2 70%") and recommended funding credential exam vouchers. Analysts noted the indicators use
different denominators and exit cohorts.

## 2. The decision (one deterministic recommendation)

**The funnel stage funded with $2M and the additional participants employed in the second quarter after exit it is expected to produce.**

Rules (board memo):

* Data: PIRL public use file for the state and programme year in memo; adult programme participants who exited in the cohort window.
* Stages: S1 enrolled in training (training service received), S2 completed training, S3 credential attained, S4 employed Q2 after exit.
* Conditional rates: r_k = count(S_k) ÷ count(S_{k−1}) within the same exit cohort (S0 = all exiters in the window).
* Intervention: $2M at stage k raises r_k by Δ_k per the memo's cost table (cost per percentage point per 1,000 at-risk participants).
* Additional employed = recomputed S4 − current S4, holding other conditional rates fixed.
* Choose the stage with the largest additional employed.

## 3. Why capable analysts get it wrong

* Published indicators look like stage conversion rates but are not.
* Conditional rates must be on the population reaching the prior stage.
* Raising an early stage's rate yields more downstream only through later rates.
* Costs per point differ by stage and by the number at risk.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `wioa_pirl_puf_py<yyyy>.csv` | CSV | ~1–2M participant records (national) | DOL ETA WIOA performance data | U.S. Gov public domain | Participant records |
| 2 | `pirl_puf_data_dictionary.xlsx` | XLSX | ~400 | DOL ETA | Public domain | Elements and codes |
| 3 | `wioa_performance_indicators_guidance.pdf` | PDF | — | DOL ETA (TEGL) | Public domain | Indicator definitions |
| 4 | `state_programme_scope.json` | JSON | — | Task author | — | State, programme, cohort |
| 5 | `stage_cost_table.json` | JSON | 4 | Task author | — | Cost per point |
| 6 | `board_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `staff_indicator_ranking.xlsx` | XLSX | 4 | Task author | — | Naive ranking |
| 8 | `published_state_performance.xlsx` | XLSX | — | DOL ETA | Public domain | Validation |

## 5. Deterministic solution path

1. Filter state, programme, exit cohort; define stage flags.
2. Conditional rates; current S4.
3. For each stage, apply Δ_k; recompute S4; additional employed.
4. Choose; contrast with the staff ranking.

## 6. Wrong paths (method errors, not misreadings)

**A — unconditional indicator rates.** Double-applied earlier stages.

**B — mixing exit cohorts across indicators.** Mismatched denominators.

**C — ignoring costs per at-risk participant.** Wrong marginal comparison.

**D — counting credential among all exiters, not training completers.** Different stage definition.

## 7. Why the stump is analytical, not semantic

Stages and costs are specified. The trap is the funnel's conditional structure and denominators.

## 8. Draft task prompt (prose)

> Which stage of our adult programme should the $2M fund? Build the conditional funnel from PIRL data as the board memo specifies and size each
> option in additional employed exiters. Provide `programme_funnel.csv` (stage: count, conditional rate, Δ, additional employed), `funnel_chart.png`,
> and a one-page `funding_decision.pdf`.

## 9. Deliverables

* `programme_funnel.csv`, `funnel_chart.png`, `funding_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 5 stage counts; 4 conditional rates; 4 options' additional employed; choice; validation; contrast.

## 11. Golden-output checklist

* Cohort filter; stage flags; conditional rates; propagation; choice.

## 12. Build notes (scope tuning)

* Confirm the staff's recommended stage is not optimal under conditional rates and costs.

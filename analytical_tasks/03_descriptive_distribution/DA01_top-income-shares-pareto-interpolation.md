# DA01 — How concentrated is a state's income? Top shares from binned tax data need the right tail model

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Domain | Public finance / state revenue volatility / credit analysis |
| Task shape | 14 · Cuts of a distribution (top 10% / 5% / 1% thresholds and shares across six states) |
| Core method | Pareto interpolation within income classes and in the open-ended top class (alpha from the class mean), cumulative shares from grouped data |
| Analytical stump | Grouped data hide the within-class distribution. Linear (uniform) interpolation or class midpoints understate the upper tail; the open top class must be modelled from its mean. The top 1% usually lies entirely inside the open-ended class |
| Primary sources | IRS Statistics of Income state data (Historic Table 2), SOI documentation |

## 1. The real-world situation

A credit analyst's **fiscal-volatility screen** flags states whose revenue depends heavily on top earners (capital-gains
swings): a state is flagged if its top-1% share of adjusted gross income (AGI) exceeds 20%. The analyst only had IRS state
tables by AGI class and estimated the top 1% by spreading returns evenly within classes and assuming everyone in the
"$200,000 or more" class earned the class average. Several states known for concentrated incomes came in under 20%.

## 2. The decision (one deterministic recommendation)

**Which of the six states are flagged (top-1% AGI share > 20%), and what are their top 10%, 5% and 1% thresholds and shares?**

Rules (screen methodology):

* Data: SOI Historic Table 2, tax year 2021, the six states in the folder: number of returns and AGI by AGI class (negative
  and zero AGI included in totals; the population is all returns).
* Within a closed class [a, b), assume a Pareto distribution through the class boundaries: the number of returns above y is
  N(y) = N_a·(a/y)^α with α = ln(N_a/N_b) ÷ ln(b/a), where N_a, N_b are returns with AGI ≥ a and ≥ b.
* In the open top class [a, ∞): α = ȳ ÷ (ȳ − a), with ȳ = the class mean AGI.
* Income above y within a Pareto segment follows from the same α (formula in the memo); thresholds solve N(y) = p × total
  returns for p = 10%, 5%, 1%; shares = income above the threshold ÷ total AGI.
* Flag if top-1% share > 20%.

## 3. Why capable analysts get it wrong

* Linear interpolation is the default for grouped data and is reasonable in the middle of the distribution, but income tails
  are Pareto-like; uniform spreading makes the tail too thin.
* The open-ended class has no upper bound; treating it as concentrated at its mean (or truncating it) understates the top.
* Shares require income above the threshold, not just counts — the second Pareto formula is easy to skip.
* Using the number of individuals or households instead of returns changes p × N.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `21in55cmcsv.csv` (Historic Table 2, all states) | CSV | ~5k (state × class × ~150 items) | IRS SOI | U.S. Gov public domain | Returns and AGI by class |
| 2 | `21in55cm.xlsx` | XLSX | same | IRS SOI | Public domain | Same, workbook |
| 3 | `20in55cmcsv.csv`, `19in55cmcsv.csv` | CSV | ~5k each | IRS SOI | Public domain | Prior years (stability) |
| 4 | `21zpallagi.csv` | CSV | ~160k | IRS SOI ZIP data | Public domain | Cross-check of class totals |
| 5 | `soi_historic_table2_documentation.pdf` | PDF | — | IRS SOI | Public domain | Definitions |
| 6 | `feenberg_poterba_1993_reference.pdf` (citation) | PDF | — | NBER (cite) | Cite | Pareto interpolation method |
| 7 | `states_in_scope.json` | JSON | 6 | Task author | — | Scope |
| 8 | `screen_methodology.pdf` | PDF | — | Task author | — | Rules and formulas |
| 9 | `analyst_linear_estimates.xlsx` | XLSX | ~18 | Task author | — | Linear/midpoint estimates |
| 10 | `bea_state_personal_income_2021.csv` | CSV | ~60 | BEA | Public domain | Context only |

## 5. Deterministic solution path

1. Extract returns and AGI by class for each state; compute cumulative counts N_a above each boundary.
2. Locate the class containing each threshold; compute α for that class (boundary formula or open-class mean formula).
3. Solve thresholds; compute income above threshold (within-class Pareto plus all higher classes).
4. Shares; flags; compare with linear/midpoint estimates.

## 6. Wrong paths (method errors, not misreadings)

**A — uniform within classes.** Top shares too low; fewer flags.

**B — open class at its mean.** The top 1% share collapses toward the class average share.

**C — threshold from counts only, share from class totals.** Inconsistent; double counts or omits part of a class.

**D — wrong population.** p × households instead of returns.

## 7. Why the stump is analytical, not semantic

All quantities and formulas' inputs are defined; the difficulty is recognizing that the within-class distribution
matters and using a tail model consistent with income distributions — a statistical modelling choice.

## 8. Draft task prompt (prose)

> Run our fiscal-volatility screen for the six states in the folder: estimate each state's top 10%, 5% and 1% AGI
> thresholds and shares from the IRS state tables using the screen methodology, and tell me which states are flagged.
> Provide `top_shares.csv` (state × cut: threshold, share, class used, alpha), `lorenz_tails.png` comparing the six states'
> top-share curves with the 20% line, and a one-page `volatility_screen.pdf` naming the flagged states and showing what the
> linear-interpolation estimates would have said.

## 9. Deliverables

* `top_shares.csv`, `lorenz_tails.png`, `volatility_screen.pdf`.

## 10. Where 25+ rubric criteria come from

* 6 states × 3 cuts × (threshold, share) = 36; flags; linear contrast.

## 11. Golden-output checklist

* Correct α per class; open-class formula; income-above-threshold formula; consistent population; flags.

## 12. Build notes (scope tuning)

* Choose states near the 20% line under the Pareto method so the linear method changes at least two flags.
* Write the income-above-threshold formula for both segment types in the memo to make results reproducible.

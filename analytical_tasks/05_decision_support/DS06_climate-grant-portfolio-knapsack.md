# DS06 — Funding emission-cutting projects under a budget: the best ratio first is not the best portfolio

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Portfolio selection under a budget with indivisible projects (roadmap planning, capital allocation, marketing bets, R&D portfolios) |
| Domain | Climate finance / public grants |
| Task shape | 01 · Ranked list under a cap (projects funded within a $250M budget to maximise GHG reductions, chosen by integer optimisation) |
| Core method | 0–1 knapsack: maximise Σ GHG reductions subject to Σ costs ≤ budget and programme constraints (minimum 25% of funds to disadvantaged-community projects); solve exactly (dynamic programming or MILP); compare with greedy selection by tCO₂e per dollar |
| Analytical stump | Ranking by cost-effectiveness and funding down the list stops when the next project doesn't fit, leaving budget unused or skipping a large project that would add more reductions; with a set-aside constraint, greedy selection can violate or mishandle it. Exact optimisation picks a different set |
| Primary sources | California Climate Investments (CCI) project-level data (California Air Resources Board annual report data) |

## 1. The real-world situation

A state agency selects projects for a new $250M round from past-programme-like proposals. The draft list funded proposals in order of tCO₂e per
dollar until the budget ran out and left $38M unallocated because the next project was too large. Programme staff also had to meet a 25%
disadvantaged-community set-aside.

## 2. The decision (one deterministic recommendation)

**The funded project set maximising estimated GHG reductions within $250M and the set-aside, its total reductions, and the gap versus the greedy
list.**

Rules (programme memo):

* Candidates: projects in `candidate_projects.csv` drawn from CCI project data (cost = GGRF funds, benefit = estimated GHG reductions in MTCO₂e,
  DAC benefit flag).
* Constraint 1: Σ cost ≤ $250,000,000.
* Constraint 2: Σ cost of DAC-benefiting projects ≥ 25% of Σ cost funded.
* Objective: maximise Σ GHG reductions.
* Solve exactly (MILP); tie-break by lower total cost, then lower project IDs.
* Greedy contrast: sort by reductions ÷ cost; add if it fits; report its set and whether it meets the set-aside.

## 3. Why capable analysts get it wrong

* Ratio ranking is intuitive and usually near-optimal for divisible items.
* Indivisible projects create gaps that a ratio list cannot fill optimally.
* Side constraints interact with selection.
* Exact solvers handle hundreds of items easily.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `cci_project_list_<year>.xlsx` | XLSX | ~200k project records (all years) | CARB California Climate Investments data | California public records (public) | Project costs, GHG reductions, DAC flags |
| 2 | `cci_data_dictionary.pdf` | PDF | — | CARB | Public | Fields |
| 3 | `candidate_projects.csv` | CSV | ~400 | Task author (filtered, frozen subset of CCI records) | Public source | Candidates |
| 4 | `programme_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `draft_greedy_list.xlsx` | XLSX | ~120 | Task author | — | Greedy list |
| 6 | `cci_quantification_methodology_citation.pdf` | PDF | — | CARB (cite) | Public | GHG quantification |

## 5. Deterministic solution path

1. Load candidates; verify costs and reductions.
2. Solve the MILP with constraints; tie-breaks.
3. Compute totals; greedy contrast; gap.

## 6. Wrong paths (method errors, not misreadings)

**A — greedy by ratio.** Unused budget; fewer reductions.

**B — set-aside applied after greedy (swapping by hand).** Suboptimal.

**C — fractional relaxation reported as a plan.** Infeasible fractional projects.

**D — maximising number of projects.** Wrong objective.

## 7. Why the stump is analytical, not semantic

The objective, constraints and data are specified. The trap is using a heuristic for an integer problem.

## 8. Draft task prompt (prose)

> Which proposals should the $250M round fund? Solve the selection exactly with the set-aside as the programme memo specifies and compare with the
> cost-effectiveness list. Provide `funded_projects.csv` (project: cost, reductions, DAC, funded), `portfolio_comparison.png`, and a one-page
> `funding_round.pdf`.

## 9. Deliverables

* `funded_projects.csv`, `portfolio_comparison.png`, `funding_round.pdf`.

## 10. Where 25+ rubric criteria come from

* Funded set (each project a criterion, ~60); totals; set-aside check; greedy totals; differences.

## 11. Golden-output checklist

* Constraints; exact solution; tie-breaks; totals; contrast.

## 12. Build notes (scope tuning)

* Choose candidates with a few very large high-reduction projects so greedy and exact solutions differ by ≥ 5% in reductions.

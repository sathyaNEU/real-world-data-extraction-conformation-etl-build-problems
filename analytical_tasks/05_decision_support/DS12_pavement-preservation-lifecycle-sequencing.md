# DS12 — Fix the worst roads first? Preserving fair roads is cheaper than rebuilding them later

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Maintenance prioritisation under budget (technical debt, preventive maintenance, infrastructure upkeep) where cheap early interventions avoid expensive late ones |
| Domain | Transportation asset management |
| Task shape | 06 · Sequenced schedule under capacity (5-year treatment plan for 300 road sections under an annual budget, with a blackout year for one corridor and one dependency) |
| Core method | Condition deterioration model (IRI growth by functional class and pavement type, fitted from section histories); treatment options with costs and condition resets (preservation, rehabilitation, reconstruction); dynamic programming / MILP minimising lifecycle cost to keep network condition above the target; compare with worst-first scheduling |
| Analytical stump | Treating the worst sections first spends the budget on reconstruction while fair sections deteriorate into the expensive category; network condition declines. Lifecycle-optimal schedules prioritise timely preservation on sections near the deterioration "knee". Ranking by current condition alone is the trap |
| Primary sources | FHWA Highway Performance Monitoring System (HPMS) section data (IRI, pavement type, AADT) |

## 1. The real-world situation

A state DOT district schedules five years of pavement treatments on 300 sections with an annual budget of $40M. The draft plan ranks sections by
current roughness (IRI) and treats the worst first. The asset manager argued that preserving fair sections would keep more of the network in good
condition for the same money.

## 2. The decision (one deterministic recommendation)

**The 5-year schedule (section × year × treatment) minimising lifecycle cost while keeping ≥ 80% of lane-miles at IRI ≤ 170 in each year, and the
network condition trajectory versus worst-first.**

Rules (asset memo):

* Sections: HPMS sections in the district (300, list in memo) with IRI history 2014–2023, pavement type, functional class, AADT, lane-miles.
* Deterioration: IRI_{t+1} = IRI_t × e^{g}, g by class × type from history (median annual growth).
* Treatments (cost per lane-mile, effect): preservation ($60k; IRI − 15%, only if IRI ≤ 140), rehabilitation ($350k; IRI → 80, if IRI ≤ 220),
  reconstruction ($1.2M; IRI → 60).
* Budget $40M per year; blackout: corridor X sections cannot be treated in year 2 (event); dependency: section S12 must be treated before S13
  (shared detour).
* Objective: minimise 5-year cost plus terminal penalty (cost to bring sections back to IRI ≤ 95 at year 5) subject to the condition target.
* Solve by MILP (memo formulation). Worst-first contrast: each year treat highest IRI with the cheapest feasible treatment until budget runs out.

## 3. Why capable analysts get it wrong

* Worst-first is intuitive and politically visible.
* Deterioration accelerates; delaying cheap treatments increases future costs.
* Terminal conditions matter; otherwise optimisers defer work beyond the horizon.
* Constraints (blackout, dependency) affect sequencing.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `hpms_<state>_<yyyy>.csv` (2014–2023) | CSV | ~100k sections per year (state) | FHWA HPMS public release | U.S. Gov public domain | IRI, type, class, AADT |
| 2 | `hpms_field_manual.pdf` | PDF | — | FHWA | Public domain | Field definitions |
| 3 | `district_sections.json` | JSON | 300 | Task author | — | Scope |
| 4 | `treatment_catalogue.json` | JSON | 3 | Task author (from state DOT published unit costs; cite) | — | Costs and effects |
| 5 | `asset_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `worst_first_plan.xlsx` | XLSX | ~300 | Task author | — | Draft plan |
| 7 | `deterioration_rates.csv` | CSV | ~12 | Derived | Public domain | Growth rates |

## 5. Deterministic solution path

1. Assemble section histories; fit growth rates.
2. Build the MILP with treatments, budget, condition target, blackout, dependency, terminal penalty.
3. Solve; schedule; condition trajectory; costs.
4. Simulate worst-first; contrast.

## 6. Wrong paths (method errors, not misreadings)

**A — worst-first.** Higher lifecycle cost, worse network condition.

**B — no terminal penalty.** Defers work beyond horizon.

**C — linear deterioration.** Misses acceleration.

**D — ignoring constraints.** Infeasible schedule.

## 7. Why the stump is analytical, not semantic

Models, costs and constraints are specified. The trap is myopic prioritisation versus lifecycle optimisation.

## 8. Draft task prompt (prose)

> Build our five-year pavement treatment schedule. Optimise lifecycle cost under the budget and condition target in the asset memo and compare with
> worst-first. Provide `treatment_schedule.csv` (section × year: treatment, cost, IRI), `network_condition.png`, and a one-page
> `pavement_programme.pdf`.

## 9. Deliverables

* `treatment_schedule.csv`, `network_condition.png`, `pavement_programme.pdf`.

## 10. Where 25+ rubric criteria come from

* Annual spend and share in good condition (5 years × 2 plans = 20); total costs; constraint checks; sample section decisions.

## 11. Golden-output checklist

* Growth fit; treatment rules; budget; target; blackout; dependency; terminal penalty.

## 12. Build notes (scope tuning)

* Confirm worst-first fails the 80% target by year 3 while the optimised plan meets it.

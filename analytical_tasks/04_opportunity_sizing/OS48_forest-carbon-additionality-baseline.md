# OS48 — Forest carbon credits: growth that would happen anyway is not a credit

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Incremental versus organic outcomes (revenue from a campaign versus baseline growth, impact of a feature versus trend) in any programme that claims credit for change |
| Domain | Forestry / carbon markets |
| Task shape | 03 · Bridge between two totals (gross carbon accumulation on enrolled forest land → additional sequestration over the business-as-usual baseline net of leakage and buffer; the credit volume underwritten) |
| Core method | Plot-level carbon stocks from forest inventory remeasurements with expansion factors (acres represented per plot); baseline = growth net of harvest on comparable non-enrolled plots (same forest type, ownership and site class); additionality = project growth with harvest deferral − baseline growth; leakage and buffer deductions per memo |
| Analytical stump | Counting all carbon accumulation on enrolled land credits growth that would occur without the project. Unweighted plot averages misrepresent area; baselines must come from comparable land with typical harvest behaviour. Credits sized on gross accumulation overstate several-fold |
| Primary sources | USDA Forest Service Forest Inventory and Analysis (FIA) DataMart (plot, condition, tree tables with remeasurements and expansion factors) |

## 1. The real-world situation

A carbon developer plans an improved-forest-management project on private family forests in one state and asks an investor to underwrite the
expected credits. The prospectus used the average annual carbon gain per acre on all FIA plots in the state's family-owned forests. The investor
asked for additional sequestration over a business-as-usual baseline.

## 2. The decision (one deterministic recommendation)

**The annual credit volume (tCO₂e per year) underwritten for 100,000 enrolled acres, with the bridge from gross accumulation.**

Rules (underwriting memo):

* Data: FIA DataMart for the state; plots measured twice (remeasurement interval in memo); family forest ownership; forest types in scope.
* Plot carbon: above- and below-ground live tree carbon (FIA variables), per acre, expanded with the plot's expansion factor.
* Baseline: area-weighted mean annual net change in carbon per acre on comparable plots *including* harvest removals (business as usual).
* Project scenario: same plots with harvest removals deferred (memo: add back removals' carbon for harvested plots).
* Additional per acre = project − baseline.
* Deductions: leakage 20%, buffer 15%.
* Credits = additional per acre × 100,000 × (1 − 0.20) × (1 − 0.15) × 44/12 (C to CO₂e).
* Bridge: gross accumulation (prospectus) → minus baseline growth → leakage → buffer → credits.

## 3. Why capable analysts get it wrong

* Gross carbon gain is the visible quantity.
* Additionality requires a counterfactual baseline.
* Plots represent different areas; expansion factors are required.
* Leakage and buffer are standard deductions in crediting.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `<ST>_PLOT.csv` | CSV | ~50k | USDA FS FIA DataMart | U.S. Gov public domain | Plots, measurement years |
| 2 | `<ST>_COND.csv` | CSV | ~60k | FIA | Public domain | Conditions, ownership, forest type |
| 3 | `<ST>_TREE.csv` | CSV | ~1–2M | FIA | Public domain | Trees, carbon variables |
| 4 | `<ST>_POP_STRATUM.csv`, `<ST>_POP_PLOT_STRATUM_ASSGN.csv` | CSV | ~10k | FIA | Public domain | Expansion factors |
| 5 | `fiadb_user_guide.pdf` | PDF | — | USDA FS | Public domain | Database documentation |
| 6 | `underwriting_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `prospectus_gross_estimate.xlsx` | XLSX | — | Task author | — | Naive sizing |
| 8 | `forest_types_in_scope.json` | JSON | — | Task author | — | Scope |

## 5. Deterministic solution path

1. Select remeasured family-forest plots in scope; compute plot carbon per acre at both visits.
2. Annual net change with expansion-factor weights (baseline); project scenario with removals added back.
3. Additional per acre; deductions; credits; bridge.
4. Contrast with the prospectus.

## 6. Wrong paths (method errors, not misreadings)

**A — gross accumulation.** Not additional.

**B — unweighted plot means.** Area misrepresented.

**C — excluding harvested plots from baseline.** Baseline too high growth.

**D — no leakage/buffer.** Overstated credits.

## 7. Why the stump is analytical, not semantic

Variables, weights and deductions are specified. The trap is counterfactual baselines in incremental sizing.

## 8. Draft task prompt (prose)

> How many credits per year should we underwrite for the 100,000-acre project? Compute additional sequestration over the FIA business-as-usual
> baseline as the underwriting memo specifies. Provide `carbon_bridge.csv` (step: tCO₂e per year), `baseline_vs_project.png`, and a one-page
> `credit_underwriting.pdf`.

## 9. Deliverables

* `carbon_bridge.csv`, `baseline_vs_project.png`, `credit_underwriting.pdf`.

## 10. Where 25+ rubric criteria come from

* Bridge steps; per-acre values by forest type (6); plot counts; credits; contrast.

## 11. Golden-output checklist

* Plot selection; carbon variables; expansion factors; baseline with harvest; scenario; deductions; conversion.

## 12. Build notes (scope tuning)

* Confirm prospectus credits are ≥ 3× the underwritten volume.

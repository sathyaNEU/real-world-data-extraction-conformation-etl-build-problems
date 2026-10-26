# Determinism verdict, task308 (pass 4, run 18312, on 8851863d)

**Verdict:** NOT_DETERMINISTIC (also SOLUTION_WRONG on Ask A, which does not reproduce exactly).

**Disposition:** SEND_BACK. The main call turns on a repair-panel capacity cost adjustment that no shipped file or the prompt asks for. A literal reader files Severn Vale. The fix changes what solvers see (the prompt or the valuation basis), so a rerun is required.

**Why:** The governing text, catastrophe_layer_valuation_basis.pdf s.2 to s.3, values claims "at what repairing them would cost in the cover year". It gives the way to do that: the business plan's 2027 rebuild cost index (146.4, business_plan_2027.xlsx Assumptions). Nothing in the bundle mentions a capacity or demand-surge effect, a hinge, or a 2027 repair panel. Executed word for word (index-only), the layer's value is Severn Vale -0.1, Pennine -0.4, Coastal North -0.5, Fenland -0.8. The golden's Pennine +0.1 exists only after a fitted, unfiled hinge model of cost per claim on claims per panel firm, with the 2025 panel assumed for 2027. Gates C and E fail on the main recommendation, and on supplementary 3 (Pennine and Severn Vale values). Label: underspecified_objective.

## Evidence

| Item | Recomputed | Reproduced? |
|---|---|---|
| Quoted premiums (cat_xl_quotations_2027.pdf): 14.37%, 19.53%, 29.47% and 27.80% of GBP 15m | 2.155, 2.930, 4.420, 4.170 | yes |
| Occurrences from home_claims_2010_2025.parquet (72h wind, 168h flood and freeze, from the first spike day); 2027 scale from business_plan_2027.xlsx and the mid-2025 district mix; index factor 146.4/index of the month of loss; layer with 30m annual cap; reinstatement premium pro rata on min(R,15)/15 | index-only: Fenland -0.83, Pennine -0.44, Severn Vale -0.09, Coastal North -0.51 | Fenland, Severn Vale and Coastal North match the golden. Pennine does not (-0.4 against +0.1). |
| Pennine's four freezes (Dec 2010, Jan 2013, Dec 2017, Feb 2018) at 2027 scale, index-only | 20.5, 22.6, 24.7 and 21.8m | They do not exhaust the layer. Critical component 1 holds only after the unfiled surge. |
| Repair panel (distinct repair_contractor per year) | Pennine 30 to 34 firms, Fenland 104 to 137, Coastal North 118 to 148, Severn Vale 330 to 390 | yes |
| Cost per claim against claims per firm over 64 occurrences of 150 claims or more | Real step above about 16 claims per firm. Pennine freezes sit at 22.6 to 25.1 (2027: 44 to 50). | The effect is in the data. The step is a data-derived model, not a filed rule. |
| Golden fit (hinge at 16.5, 2.8% a claim per firm), run with the 2025 panel held to 2027 | Fenland -0.775, Pennine +0.087, Severn Vale -0.088, Coastal North -0.491. All four Pennine freezes exhaust, giving 3.75 recoveries, 0.73 reinstatement premium, 2.93 premium. | yes, as the golden |

Sensitivity of the golden: Pennine stays at +0.087 for hinge knots from 10 to 20, a linear fit, and a panel that grows with policies. The four freezes saturate the layer, so the cap makes the number robust once any surge model is accepted. A log-form fit gives Pennine -0.05, which rounds differently. The two readings are:

- Index-only (the literal text): Severn Vale -0.1, Pennine -0.4. Region: Severn Vale.
- With a fitted capacity surge on the 2025 panel: Pennine +0.1. Region: Pennine.

The prompt gives no cue that cost depends on capacity. The only hints are the claims_operations_report_2025.pdf s.2 sentence that repairs "go through our approved repair panel", and a record field. The business plan and the valuation basis both point to the index as the cost basis.

**Supplementary B (sums insured 31 Dec 2025)** reproduces exactly: 59,442.2 / 73,441.1 / 131,316.2 / 71,630.8. The method is direct_policies_in_force_2025-12-31.csv plus Lowther and Pike terms covering the date. A cancellation counts unless a non-Cancelled row is listed for a later month (reinstatement). The first listed sum insured is moved by endorsements effective by the date. It is rule application inferred from the bordereau structure, which the claims report describes only in part. It is acceptable as an ask.

**Supplementary A (incurred per policy, five perils, 2023 to 2025)** does not reproduce exactly. My best literal reconstruction:

- MLU cases are joined by policy, peril and date of loss.
- Cases are summed per claim at their last figure.
- The platform figure is kept where a case left the reports open.
- Unmatched MLU cases are added in the year of loss.
- The denominator is mid-year policies.

This gives Fenland 118.84 / 118.52 / 122.81, Pennine 135.41 / 134.86 / 132.46, Severn Vale 113.69 / 120.85 / 127.05, Coastal North 122.55 / 116.61 / 136.44. The golden is Fenland 117.89 / 117.26 / 121.28, Pennine 135.36 / 134.52 / 130.95, Severn Vale 113.58 / 120.57 / 125.88, Coastal North 122.17 / 116.35 / 135.16. The gaps run from 0.05 to 1.5 pounds per policy, largest in 2025 and 2024. The 2025 gaps are about the size of the unmatched MLU additions. The MLU handling is not stated in the prompt or in any file, and the rules the golden steps name do not reproduce the figures. Treat the twelve figures as unreproduced and the rules as an open fork (platform against MLU figure for left-open cases, treatment of unmatched cases). Recorded as solution_incorrect for Ask A, and also a Gate E finding because the pounds-and-pence answers hinge on unfiled MLU conventions.

Other forks checked and found immaterial for the main call: date-only losses against the hours clause (windows from the first loss day match the golden in three regions), and the premium and reinstatement arithmetic.

## Files/Hygiene
**PASS, with notes.** 13 files; formats are parquet, xlsx (3), csv (4) and pdf (5). Large inputs are 483,625 claims and 79,894 bordereau rows. Distractors are present: group_catastrophe_programme_2026.pdf, flood_resilience_survey_2024.csv, claims_operations_report_2025.pdf. The files read as real operational artifacts, with a monthly MLU workbook of 46 sheets, a bordereau with mixed rows, and a firm index with a provisional-months note. No authoring or synthetic disclosures and no temporal conflicts found (the quotations are dated 18 November 2026, after the 31 October extract; that is consistent with the fiction). No license or provenance documents are visible inside the bundle (not checkable here). Nothing is exclusion-level.

## Stump power
The trap that would work is the capacity surge on Pennine. A strong solver who follows the valuation basis and indexes costs lands on Severn Vale, so the stump would be real. But the stump is not a valid one while the text does not license the surge: the divergence is a reading of "what repairing them would cost", which is a fork rather than an analytical error. Once the estimand is pinned, the trap would be hard, since the panel field is only in the claims table and the effect needs a fitted out-of-sample-style check.

## Stumping type
`mechanism: method_or_model_selection (a cost-surge model on repair-panel capacity)`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The stated figures are fine and the method is the difficulty, so it would pass Gate G. It fails on determinism, since the method is not filed.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical (but unfiled)`. The field's own analysis is layer pricing from occurrence-based experience rating with demand-surge and capacity effects, which the swap test does not make generic. Layer 1 is the Lowther and Pike bordereau, MLU against platform claims, the fiscal-style index and the district mix. Layer 2 is the capacity-driven cost escalation inside the occurrences. The easy route (index-only) gives Severn Vale at -0.1, and a strong analyst who read every rule correctly would take it. That is why the decisive step depends on an estimand the text does not state, rather than on analysis alone.

## Fix
**prompt** (or the valuation basis in input_files). File the WHAT of the estimand without the HOW: say in the basis or the prompt that the cover year's repair cost includes the cost effect of the same claims being repaired through the region's repair panel as it stands at the cover year. Also file the 2027 panel (for example, the 2025 panel held). Keep the method of estimating the effect open and pinned by the data. Then rebuild or re-key Ask A, and file the MLU treatment (which figure governs for cases that left the reports open, and what happens to unmatched cases), then re-key the twelve figures to a version that reproduces exactly. Rerun is required.

# determinism-check report, task194, 2026-11-03

## Verdict
NOT_DETERMINISTIC (supplementary answers 4 and 5 only; the main recommendation, supplementary 1 to 3, 6 and the chart reproduce and are forced)
**Disposition:** SEND_BACK
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no (borderline)

## Why
The main call is forced: from the bundle Thrushgate rises 0.610 l/s, Ashworth Fold 0.306, and Kestle Hill and Moorend Low net to 0.0 once the BV-0412 crossing is removed. Two committed answer sets are not uniquely forced by shipped text.
- Supplementary 5 (occupied household properties) reproduces only if a CONV event makes the class permanent. Read literally (latest event's property_class), 87 properties have an OCC row with class HH after a CONV to NHH, and every area is 4 to 7 higher (Ashworth Fold 2,139 vs 2,135; Kestle Hill 2,251 vs 2,244; Barrowfold 3,040 vs 3,034; Gorsey Bank 1,649 vs 1,647). Label: competing_defensible_answer.
- Supplementary 4 (logged large users' October consumption) excludes Kalder Print Finishing (19A385556), the Stanecroft bottling hall sub-meter (10A186278) and Barrowfold Rail Maintenance (22A128742). No shipped sentence calls them check or tenant meters; they are accounts in large_user_accounts.xlsx "Logged since 2019-03". Only the register's Revenue meter column supports the exclusion. Literal "logged large users" gives Thrushgate about 1,103, not 823 (Thrushgate, Stanecroft and Barrowfold affected).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Kestle Hill own-leakage change before netting (l/s) | 0.9 | 0.943 | yes |
| Moorend Low before netting | -0.9 | -0.947 | yes |
| BV-0412 crossing (mean of both) | 0.9 | 0.945 | yes |
| Kestle Hill and Moorend Low after netting | 0.0 | -0.002 each | yes |
| Thrushgate | 0.6 | 0.610 | yes |
| Ashworth Fold | 0.3 | 0.306 | yes |
| Gap | 0.3 | 0.304 | yes |
| Supp 3, all 18 areas | as filed | match to one decimal | yes |
| Calvert Rise (PRV-C1 38.0 to 47.0 m on 2026-09-29) | 0.0 | 0.010 | yes |
| Pellow Bridge (depot meter 24A488028 from 1 Oct) | 0.0 | 0.003 | yes |
| Supp 4, all 18 areas (revenue-meter reading) | as filed | match | yes under golden reading only |
| Supp 5 (Ashworth Fold / Kestle Hill / Barrowfold) | 2,135 / 2,244 / 3,034 | 2,135 / 2,244 / 3,034 sticky-CONV; 2,139 / 2,251 / 3,040 last-event | only under sticky-CONV |
| Supp 6, all 18 areas | as filed | match (TC jobs resolved via Asset job number) | yes |
| Hourly KH01_FT vs MLW_INLET_FT1 | equal and opposite | +3.40 and -3.41 m3/h at 03:00, every hour | yes |

## Competing answers that survived
1. Large-user meter scope (supp 4): revenue meters only (golden) vs every listed meter (Thrushgate about 1,103 vs 823; Stanecroft and Barrowfold also differ). No shipped rule closes it; LP04 4.3 says only "logged large users". The design note's SF10 closes the area attribution, not the meter scope.
2. Property class after CONV then a later OCC row (supp 5): CONV sticky (golden) vs latest event's class; 87 properties, every area moves 4 to 7. Not in the fork table (SF4 covers only register vs billing).
Closed forks, for the record: no netting rule in LP04 (decides the main call, see Gate H); large-user area by supply point vs account (LP04 section 7 cites the register issue); Pellow Bridge zero-fill for nights before the meter exists; bar to metres (cancels).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | 5 (PDF, CSV, XLSX, GeoJSON, plus PDF deliverables) | yes |
| Large file | 25,000 rows or more | historian 180,405 rows; billing 46,006 | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | raingauge_hv03, customer_contacts, find_and_fix_outcomes (3); file names do not label them. prv_setpoint_log is used by the solution | yes |
| Distractor behaviour | unused, relevant, ruled out by a shipped fact | not verified to be arithmetic answers to a graded quantity; judge found none that answers one | yes (not stress-tested beyond the judge) |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pdf), both in golden/ | yes |
| Asks multi-dimensional with unit and rounding | yes | 18-area cuts; units and rounding in the prompt | yes |
| Prompt shape, 25 or more criteria | identifiable | per-area cuts (5 x 18 plus call, runner-up, gap, chart) clear 25 | yes |
| No LLM-generated feel | yes | judge found no authoring leakage or tool banners | yes |
| Fork-free supplementary answers | implied by determinism | supp 4 and 5 fork | NO |

## Gate G reconciliation
Judge: decomposition_attribution, analytical_non_defect, surface_read_dependency no, sole_data_defect no (borderline). Design note: stump class analytical, R2 (the procedure's full method) names Kestle Hill and R3 (boundary tested) names Thrushgate. These agree on mechanism and on the surface read. The declared distractors (rain gauge, contacts, find-and-fix outcomes) are not named by the judge as carrying the task, so none is too load-bearing. The surface read is the default path (Kestle Hill), not a metadata distractor. No banned_stumping_type raised. Class: not banned. Borderline flag: the judge notes that on data with no valve passing the task has no stump, and that the GIS lists BV-0412 as CLOSED, contradicting the flows.

## Gate H reconciliation
Judge: `domain: pass`, `layers: pass`, `decisive_step: analytical`. Explicit ruling: option (a), an analytical method of the field (inter-DMA transfer reconciliation, an area water balance across neighbouring meters). Not a planted defect: nothing is announced, no memo or decoy, and the crossing is a conservation-of-water balance a leakage engineer runs; physical corroboration is Moorend Low's impossible negative un-netted comparison leakage (-0.28 m3/h). Not rule application: LP04 6.1 defines own leakage and states no netting rule, so no stated rule is executed. Not data semantics: no field, code or unit read differently moves the call. Easy route: rank pressure-normalised net night flow, giving Kestle Hill 0.9 l/s, runner-up Thrushgate 0.6, gap 0.3, the wrong call. Swap test passes. This matches the design note's `## Three rules` (domain, no decoy, not semantics, not rule application).
Residual risk, recorded for the main thread: the discovery is by noticing a data anomaly (a CLOSED valve the flows contradict, an equal-and-opposite pair), which a reviewer could read as a planted slip. The design note itself says "the valve's true state is in no column" and calls it an "ordinary operational slip". The mitigation is that the analysis, not the catch, is what the field does (the water balance), but this is the line the real reviewer may draw differently.

## Stump power (Gate F)
The easy route lands on Kestle Hill and a model following LP04 sections 3 to 5 faithfully takes it; Calvert Rise and Pellow Bridge are cleared by LP04 itself. Only the boundary netting separates the committed answer, and it needs a neighbour-pair test. Likely to stump a model that stops once the procedure's steps are done; a model that checks the negative Moorend Low leakage will catch it. Water balance across boundaries is a textbook leakage-engineer route a strong solver can reach, so the main thread should weigh that against the ladder (stumping 1.3). Ladder on paper: Thrushgate is 2nd on the default path, 1.55x behind.

## Findings, ranked
1. Supp 5: the CONV-then-later-OCC class rule is open (87 properties, all 18 areas shift 4 to 7). competing_defensible_answer. Blocks determinism.
2. Supp 4: scope of "logged large users" is open (three excluded accounts listed as logged in large_user_accounts.xlsx; Thrushgate 823 vs about 1,103). Blocks determinism.
3. Borderline Gate H risk: the decisive discovery rests on spotting a data anomaly (GIS says CLOSED); ruled analytical by the judge but close to a planted-defect shape. Not a failure of the gate.
4. Design-note fork table gap: neither fork above has a row; SF4 and SF10 do not cover them, so the claim of "no open fork" is incomplete.
5. Stump power: netting across a boundary is a standard water-balance route; weigh on the ladder.
Main call, Gate A to E on the main recommendation: pass.

## Next action for the author
Pin both readings with the main call, stump and figures 1 to 3, 6 frozen: file which meters count as logged large users (a register column or a prompt clause naming revenue and replacement meters, not tenants' check meters on bulk supplies), and file which class governs a property with a CONV followed by a later OCC row, then add both as fork-table rows asserted in checks.py and run /fix-determinism. File the WHAT (population and class), not the netting method.

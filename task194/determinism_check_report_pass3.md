# determinism-check report (pass 3), task194, 2026-11-03

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no (borderline), sole_data_defect: no

## Why
Executing LP04 word for word on the shipped files reproduces every golden figure. The crew goes to Thrushgate (0.610 l/s, reported 0.6) with Ashworth Fold (0.307, reported 0.3) as runner-up; gap 0.303 reports as 0.3. LP04 6.1 defines own leakage as water lost "from the area's own mains and service pipes", which excludes the 0.9 l/s BV-0412 passes from Moorend Low's supply through Kestle Hill's inlet. Without netting Kestle Hill (0.898) leads; with it Kestle Hill and Moorend Low are both 0.0. Calvert Rise (PRV raised 38 to 47 m on 29 Sep; normalised 0.01) and Pellow Bridge (depot meter 24A488028; 0.003) fall under stated rules. Pass-2's ask-4 tie is no longer reported as a fork. No repair, no rerun.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Thrushgate own-leakage change (l/s) | 0.6 | 0.610 (THR01_FT) | yes |
| Ashworth Fold | 0.3 | 0.307 (AF01_FT) | yes |
| Gap | 0.3 | 0.303 | yes |
| Kestle Hill before / after netting | 0.9 / 0.0 | 0.898 / ~0.0 | yes |
| Moorend Low before / after netting | -0.9 / 0.0 | -0.902 / ~0.0 | yes |
| Barrowfold, Gorsey Bank, Lidden, Hennick, Oakshaw, Tollbar, Whinlow, Ravensclough | 0.2, 0.1, 0.1, -0.2, -0.1, -0.1, -0.1, -0.2 | 0.186, 0.103, 0.100, -0.201, -0.106, -0.096, -0.096, -0.198 | yes |
| Calvert Rise, Crake Bank, Netherby, Pellow Bridge, Stanecroft, Upper Sowden | 0.0 | all within 0.03 of zero | yes |
| Ask 3, all 18 areas | as filed | round to the golden | yes |
| Ask 4 (e.g. Pellow Bridge 6,346; Thrushgate 823), all 18 | as filed | all reproduce (Revenue-role meters, supply-point area, local October, rollover added back, Pennock swap handled) | yes |
| Ask 5, all 18 | as filed | all reproduce (effective date to 31 Oct, account-level last OCC/VAC, latest class HH, D3305 to D3341) | yes |
| Ask 6, all 18 (77 jobs) | as filed | all reproduce (asset key normalisation, 6 TC jobs via Asset) | yes |
| BV-0412 mirror | equal and opposite | step 3.2 m3/h on 7 Oct, hourly correlation -1.00, largest residual 0.5 m3/h against swings to 26; works order WM-004571 valve replacement (D4123) completed 6 Oct | yes |

## Competing answers that survived
None on the main call or any golden cell. Low-severity residual forks, recorded by the judge:
1. Meter role (ask 4): including the three Check meters (19A385556, 10A186278, 22A128742) adds 280.2, 1,097.5 and 492.4 m3 to Thrushgate, Stanecroft and Barrowfold. No shipped sentence defines Check vs Revenue; the register's Supply points sheet names one Revenue meter per supply point, so exclusion is supported, not stated. Main call unchanged (Thrushgate 0.611).
2. Area of a large user (ask 4): "Area (account)" column instead of the register's supply-point area changes 15 of 18 totals. The register is the stated source for areas.
3. Late-posted events (ask 5): excluding 9 events posted after 31 Oct moves Barrowfold and Pellow Bridge by one each; effective dating is the natural reading.
4. Netting criterion: LP04 states no detection test. Smaller opposite pairs exist (BV-0447 Barrowfold +0.19 / Hennick -0.20; BV-0489 Lidden +0.10 / Oakshaw -0.11; BV-0575 Gorsey Bank +0.10 / Tollbar -0.10). A solver who nets them would turn up to six ask-3 cells to 0.0. They are small, gradual, not hour-for-hour mirrors and have no valve-operation record; the call is unaffected. Low probability.
5. Hour convention for the 03:00 consumption: moves no ask-3 value (Thrushgate 0.610 or 0.601); ask 4 differs only for Pellow Bridge (5.8 m3), whose meter begins mid-month.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | 4 (PDF 1, CSV 8, XLSX 4, GeoJSON 1) | yes |
| Large file | 25,000 rows or more | historian about 180k, billing about 46k | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | raingauge_hv03, customer_contacts, find_and_fix_outcomes (3) | yes |
| Distractor behaviour | unused, relevant, ruled out | judge found none answering a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2, both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 18-area cuts, units and rounding in the prompt | yes |
| Prompt shape, 25 or more criteria | identifiable | clears 25 by count of per-area cuts; no generated rubric seen | yes (by count) |
| Not LLM-generated feel | yes | no authoring or solver language found | yes |
Prompt is the same single paragraph as before (no count the data hold).

## Gate G reconciliation
Judge: decomposition_attribution, analytical_non_defect, surface_read_dependency no (borderline), sole_data_defect no. Design note: analytical stump; default path names Kestle Hill, decisive step names Thrushgate. Agreement. The named metadata distractors do not carry the task. Not banned.

## Gate H reconciliation
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Explicit ruling (a), an analytical method of the field (inter-DMA water balance and transfer reconciliation), with a borderline note on (b). LP04 6.1 and LP04 2 (an area is "supplied through the inlet meters listed for it") together exclude water passing to a neighbour; LP04 states no netting rule, so executing the text word for word does not net: not rule application. Not data semantics. The crossing is found by the mirror in a neighbour and by the demand-shaped profile (3.2 m3/h at night against 13.4 m3/h whole-day mean), which a leak does not produce. Borderline element: GIS still says BV-0412 CLOSED (last operated 2024-02-03), a stale field set against the right answer; the judge does not rate it a decoy because no document argues for the wrong answer or certifies the wrong method. Easy route: rank normalised net night flow and file Kestle Hill 0.898 l/s, runner-up Thrushgate 0.610, gap 0.3, with Moorend Low at -0.9 in ask 3. Swap test passes. Matches the design note's Three rules.

## Stump power (Gate F)
Moderate. Pellow Bridge and Calvert Rise are stated-rule eliminations a careful solver clears. The weight rests on BV-0412. Moorend Low's mirrored -0.9 sits beside Kestle Hill in any all-areas table, so a thorough solver is likely to notice it; stump risk remains because GIS says CLOSED, no sentence authorises netting, and the call needs an inference beyond the stated corrections. The ask layer carries separate ETL difficulty. Water balance across boundaries is a textbook route a strong solver can reach (stumping 1.3); the main thread weighs this against the design note's ladder.

## Findings, ranked
1. No blocking finding. DETERMINISTIC, APPROVE.
2. Consistency flag for the main thread, not raised by the judge: pass 3 recomputes slightly different values from pass 2 (Kestle Hill 0.898 vs 0.943, Ashworth Fold 0.307 vs 0.306, step on 7 Oct vs 6 Oct) and cites a works order, WM-004571 valve replacement completed 6 Oct, that pass 2 reported as absent ("no work order... mentions it"). The bundle appears to have been rebuilt between passes. Confirm target.zip is the intended final cut, that the golden still agrees to the rounded figures (it does per the judge), and that the new works-order corroboration is intended: it is a data trace toward the answer, which is realistic mess and does not argue for the wrong method, but it eases the stump a little and contradicts the design note's earlier line that the valve's only trace is the flows.
3. Residual fork: the netting criterion (smaller opposite pairs) could turn up to six ask-3 cells to 0.0 for a solver who nets them; judged low probability.
4. Residual forks on ask 4 (Check meter role not stated in words; account vs supply-point area) and ask 5 (late-posted events); the golden readings are the better supported.
5. Borderline Gate H (b) counter-case: stale GIS CLOSED status; held analytical. Residual portal risk.

## Next action for the author
None required for determinism. Before shipping, re-run the final-cut gates on the same target.zip that this judge unzipped, and confirm finding 2 (the rebuild and the new works order) is intended and recorded in the design note.

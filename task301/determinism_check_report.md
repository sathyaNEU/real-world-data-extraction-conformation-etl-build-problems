# determinism-check report, task301, 2026-10-25

## Verdict
DETERMINISTIC, plus SOLUTION_WRONG (one supplementary figure: ask 4, Wexcombe)
**Disposition:** FIX_NOW (the judge's disposition stands; see Stump power for the scored readers' result)
**Stumping type:** mechanism: forecasting (transfer of a fitted physical effect to a different climate) / method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The main call is forced by the shipped files. Kingsley Fields at 9,700 MWh reproduces (11.0 MWp, Knowle Park PR 0.830, ten-year satellite irradiation, 0.15 per cent a year degradation). Hallam Down's 4.1 per cent irradiation lead is eaten by broiler dust on every well-fitting rain-driven fit the judge ran (4.7 to 5.6 per cent; the golden's own fit is 7.4). One graded figure is wrong: Wexcombe's alarm-to-arrival average recomputes to 19.654 h (25 alarms), so 19.7, not the filed 19.6. No licensed variant gives 19.6 (day taken from alarm, work order or attended day; strict inequality; visit in progress all give 19.654). Reading UTC against UK time gives 20.4, so the timezone step matters but does not produce the filed figure. A solution defect, not a task defect.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Knowle Park PR (fleet_daily_export / site_weather_daily, outage days kept, 716 days) | 0.83 | 0.8303 (0.833 with 8 O&M event days dropped, same exports) | yes |
| Degradation, four bifacial farms | 0.15 %/yr | 0.15 (se 0.11); 0 or 0.45 moves no 100 MWh line | yes |
| Kingsley Fields / Larkhill / Marston Vale / Hallam Down (pre-dust) | 9,700 / 9,500 / 9,300 / 10,100 | 9,680 / 9,480 / 9,276 / 10,080 | yes |
| Hallam Down irradiation lead over Kingsley Fields | 4.1 % | 1103.2 vs 1059.6, 4.11 % | yes |
| Block distances, Wexcombe nearest three / Hallam Down ten | 87 to 141 m / 76 to 269 m | 87, 102, 141 / 76 to 269 | yes |
| Wexcombe near-block deficit vs far-block median | 1.5 to 4.2 % | 4.2, 3.2, 1.5 (mean of daily ratios); 5.3, 4.5, 2.2 (ratio of sums) | yes, only for mean of daily ratios |
| Hallam Down dust loss / export after dust | 7.4 % (golden fit), min 4.7 %; no more than 9,600 | judge fits 4.7 to 5.6 %, export 9,530 or less | yes (bound) |
| Ask 3, 14 pyranometer ratios | 0.971 to 1.007 | all 14 identical to 3 dp, stable to boundary conventions | yes |
| Ask 4, 13 of 14 farms | 9.5 to 31.3 h | identical | yes |
| Ask 4, Wexcombe | 19.6 | 19.654 = 19.7 | NO |

## Competing answers that survived
- Wash threshold and cap on the deposit (1 to 2 mm threshold or 8 per cent cap gives 3.4 to 4.1 per cent, Hallam Down level or ahead). Those fits are clearly worse (rmse 0.0170 to 0.0195 against 0.0155 to 0.0157), so selection by fit closes it; the judge would not file it. Weak but closed.
- CRITICAL_COMPONENTS 3 holds only for the mean-of-daily-ratios form; the ratio-of-sums form gives 2.2 to 5.3 per cent. Wording fix, same call.
- Ask 6 Hallam Down bar has no single forced value (fits about 9,300 to 9,600); it is filed as a bound ("no more than 9,600"), gradable as such, not as a point.
- Ask 3 depends on the sensor-by-date reading (logger serial stale after swap); the files support it by internal consistency, and the alternatives give different values (data semantics, in an ask, which is permitted).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 17 | yes |
| Formats | 3 or more | 5 (csv, parquet, xlsx, docx, pdf) | yes |
| Large file | 25,000 rows or large DB | weather csv 65,754 rows; inverter parquet 282,544 rows | yes |
| Distractors in metadata.json | 2 or more, none named by file name | candidate_site_terms_2027.xlsx, module_datasheets.pdf; names do not label them | yes |
| Distractors unused yet weighable | relevant, ruled out by a shipped fact | lease/grid terms and warranty degradation; judge confirms present and unused (the datasheet degradation moves no call per SF3 in the design note) | yes |
| Deliverables | 1 to 3, each in golden | 2 (xlsx, docx); asks 1 to 6 all present | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 14-farm ratio and 14-farm hours asks; prompt states 100 MWh, 3 dp, 1 dp | yes |
| Prompt shape identifiable; rubric 25 or more criteria | yes | shape "other" (metadata); about 32 gradable figures (2 + 14 + 14 + chart/case); rubric itself not generated yet, not verified | yes, provisional |
| Reads human, not LLM | yes | judge found no README, benchmark language or authoring disclosure; one trivial date oddity (docx saved 29 Oct 2026) | yes |

## Gate G reconciliation
Thread: mechanism forecasting / method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card/design: gate_g forecasting, stump_class analytical, layer2 field_method (deposit by block distance carried through the candidate's own rain), no decoy, no planted defect. Match. The declared distractors (terms workbook, datasheets) are not named by the thread as the surface read carrying the task; the surface route the thread names is irradiation times the Knowle Park PR (Hallam Down 10,100), which is the declared default path, not a distractor. No finding on distractor load. Minor note: the judge flags the dust mechanism as hidden in the block data (borderline discovery), consistent with the note's "nothing names a deposit" rung 4; no figure is misreported.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical. Design note's Three rules and card (stump_class analytical, analyst_test, domain_test) agree: decisive step is a rain-conditioned deposit fit on Wexcombe's near blocks carried to Hallam Down's drier climate; asks 3 and 4 (sensor swap, UTC vs UK time, CMMS sync stamps) are Layer 1 / data-semantics and decoupled from the call.

## Stump power (Gate F)
Judge: good. Easy routes (irradiation times PR; the Wexcombe fiscal meter, which sits only 1.1 per cent off its peers; an unconditioned distance loss of 2 to 3 per cent, Hallam Down about 9,800) all file Hallam Down. Only a rain-conditioned deposit fit flips it. The judge reached the golden by running the fit itself, with judgment the data had to settle (threshold and cap selection by fit), so this is not a bare textbook-method call. Scored-readers input (from the coordinator, not from the judge): the two stage-4 readers were scored separately and one landed the call, so the architecture is spent at stage 4 regardless of the judge's findings; the main thread weighs this against the judge's "good". I record it here, not as a change to the determinism verdict or disposition.

## Findings, ranked
1. Ask 4 Wexcombe: filed 19.6, recomputes 19.654, so 19.7. Fix in submission.md (and golden xlsx, generator figures).
2. CRITICAL_COMPONENTS 3: say the 1.5 to 4.2 per cent is the mean of daily ratios against the far-block median (ratio of sums gives 2.2 to 5.3).
3. Ask 6 Hallam Down bar: keep as a bound; do not turn it into a point figure.
4. Wash-threshold fork: closed by fit quality, no filing needed (do not file the method).
5. Process: scored readers show the call is landable (see Stump power).

## Next action for the author
Correct the Wexcombe ask 4 value to 19.7 wherever it is written (generator figures, golden workbook, submission.md), reword CRITICAL_COMPONENTS 3 to name the mean-of-daily-ratios form, rebuild, and re-judge once only if the main thread keeps this architecture after weighing the scored readers' result.

# determinism-check report, task478 (architecture 6), 2026-10-23

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW (cosmetic: unfilled "%s's" placeholder in tbapcd_emission_inventory_guidance_2026.pdf section 7, line "%s's commercial billing extract as the utility delivered it"; confirmed by pdftotext; should read Tamsett Valley Gas). No figure, prompt or solution change. Re-judge once per stage 4 rule after the rebuild.
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread: one sonnet/medium judge on a fresh unzip (target.zip md5 946c750665ba00b7e3d40fa1c749f81f) at /tmp/determinism-check-task478-run1/target/. Its verdict: /tmp/determinism-check-task478-run1/verdict.md; brief: judge_brief.md in the same folder.

## Why
Every committed figure (main five, asks 1 to 6) recomputes from the bundle. Guidance section 3 files the estimand (annual heat input times the rate operated at over the year) and leaves the estimator open; the data force the one-climb catalyst-hours log-linear model (tests carried across a catalyst change miss by 48 to 77 per cent rms; model 6 to 7 per cent, leave-one-out). The top five is stable across every model form that fits; the sixth-place margin (Lindqvist 6.61 vs Sedge Hollow 8.29) is 25 per cent.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Rule 4306 devices / with CEMS | 35 / 9 | 35 / 9 | Yes |
| CEMS tons | 74 | 74 | Yes |
| Source tests | 172 | 172 (77 + 95) | Yes |
| Climb per 10,000 h (log) | 0.48 | 0.479 (about 4.9 per cent per 1,000 h) | Yes |
| Facility tons (14) | 24, 21, 22, 8, 6, 8, 7, 4, 3, 3, 2, 1, 1, 1 | same, all 14 | Yes |
| Gas total / 14 facilities | 18,290,110 MMBtu | same, every facility | Yes |
| Engines total / 14 facilities | 10,523 lb | same, every facility | Yes |

## Competing answers that survived
- Estimator forks: latest test per unit, time interpolation, mean of all tests each give Haskett and Lindqvist in and St. Aldric and Sedge Hollow out. The thread rejected them as invalid on the shipped data (rates predate the catalyst replacement). Guidance section 3 never names the catalyst link, so this is a method fork the data close, not a filed rule: the intended design (method open, data separates candidates).
- Linear (non-log) rate fit ties on the selection but misses 32 per cent in sample, 37 per cent out of sample; not a competent candidate.
- Residual whole-ton sensitivity: under worse-fitting forms (sqrt, log(h+1000)) Sedge Hollow's whole-ton figure would read 10 rather than 8 (selection unchanged). Ask 2 is graded on the best-fit model; note as a minor risk.
- Gas cutover: classifying by read date or bill date from 1 July gives 108 or 128 lines (18,327,593 / 18,289,683) against 126 stated; the text files "the 126 lines the utility's new billing system issued", and a clean cutover by bill date closes it. Literal "CCF times BTU for all" gives 18,648,178 (wrong read of a stated file).
- Engines: all-decimal logs give 10,087 lb; Feb 2027 permit list for replaced engines gives 7,545 lb. Wrong reads of stated files, not forks.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | Yes |
| Formats | 3 or more | CSV, PDF, XLSX | Yes |
| Large file | 25,000 rows or more | 60,257 (CEMS) | Yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | NO2 hourly csv and on-road NOx xlsx named in metadata; neither file name says distractor | Yes |
| Distractors unused yet weighing | yes | NO2 monitors (breathed concentrations) and on-road NOx (traffic) do not answer the graded quantity; plan scope rules them out | Yes |
| Deliverables | 1 to 3, all in golden | 3 (xlsx, csv, svg), all present in golden/ | Yes |
| Asks multi-dimensional, unit and rounding stated | yes | 14-facility cuts of tons, MMBtu, lb; each states unit and rounding (prompt names whole tons, MMBtu, pounds) | Yes |
| Prompt shape and 25 or more criteria | identifiable, 25+ | Shape 01 (ranked slate); 14 x 3 figures plus 5 picks plus CSV/SVG items comfortably exceed 25; rubric not generated here, not verified | Yes (by construction) |
| Reads as real, not LLM generated | yes | No finding from the thread; unfilled "%s's" template placeholder is the one tell and must be fixed | Pending the fix |

## Gate G reconciliation
Thread: method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card (task478.json): gate_g method_or_model_selection, stump_class analytical, stump_strategy other, decisive_rule_filed false, official_decoy false. Match. Declared distractors (NO2 hourly, on-road NOx) are not the surface read carrying the task: the thread's easy route is the latest source test, not either distractor. Gate G: PASS.

Gate H: domain pass (point-source inventory: CEMS, source-test rates, SCR catalyst deactivation; swap test fails), layers pass (Layer 1: two test databases in different layouts, renumbered facility, month-first dates, therms/MMscf/MMBtu, billing-system cutover, h.mm logs, replaced engines; Layer 2: catalyst-hours rate model), decisive_step analytical (easy route files Haskett and Lindqvist in, St. Aldric and Sedge Hollow out). Matches the card's analyst_test and domain_test and the design note's Three rules domain test. Gate H: PASS.

## Stump power (Gate F)
Strong on paper: the latest-test route files a wrong five, and the climb must be found and quantified from test histories against catalyst hours; the asks (gas cutover, h.mm logs, replaced-engine tiers) each need separate care. One caution for the main thread to weigh with the blind readers: the golden's method is the field's standard approach (rate degradation against operating age), and the thread class the step analytical because the data must settle the model form, not because it is a textbook method; reach by a strong solver who looks at test histories against catalyst age is plausible (stumping 1.3 note), so the scored readers' result governs.

## Findings, ranked
1. FIX_NOW cosmetic: unfilled "%s's" in guidance PDF section 7 (generator template; the format string is not filled in). Fix in the generator, rebuild twice byte-identical, rezip.
2. Minor: model form (one log-linear climb for all units) is unfiled; Sedge Hollow ton figure is model-form sensitive (8 vs 10 under poorer forms) though the five are stable. Consider whether the guidance should file "one climb for all units" as a selection criterion (file the WHAT, not the HOW), or accept as the best-fit-forced choice.
3. Thread could not check cross-batch duplication (no corpus in scope); leave to clone-check.

## Next action for the author
Fix the "%s's" placeholder in the guidance PDF generator (replace with Tamsett Valley Gas), rebuild twice for byte identity, rezip, and re-judge once.

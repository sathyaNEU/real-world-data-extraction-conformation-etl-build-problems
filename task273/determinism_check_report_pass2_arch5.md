# determinism-check report, task273, 2026-10-23 (pass 2)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE on determinism (the one re-judge after the pass 1 FIX_NOW). See the post-judgement note below: the final cut differs from the pack this thread read.
**Stumping type:** mechanism: method_or_model_selection (exposure-adjusted rates), stumping_family: method_or_model_selection, surface_read_dependency: no, sole_data_defect: no

## Post-judgement change to the pack (a record, not a new verdict)
The pass 2 thread judged target.zip with md5 fdf661989d11dbf2de9d31595c854472. The final cut is 73efe12945f11373da611367702e51a9, and no graded figure moved (checks 0 failed, verify PASS, figures_check 44 of 44, as reported by the coordinator).
- After pass 2, an isolated reader on fdf66198 found the persons file's later listings through the dictionary's new PERSON_NO sentence ("a later report on the crash numbers on from the earlier ones") and landed every ask figure. That sentence was withdrawn, and the persons line now reads "the people involved in crashes with an injury recorded".
- The population pin in the prompt ("not only those between moving vehicles") and seat code 00 for non-motorists stay.
- Pass 1 had read the pack in its earlier form (the "one row a person" line) and reproduced the golden only by keeping each person's later listing. Pass 2 read the pack with the PERSON_NO sentence, which the thread cited as stating the duplicate rule. Neither thread read the final dictionary wording. I did not re-run a judge on 73efe129 (one re-judge only), so the person-dedupe determinism on the final cut rests on this thread's finding that the seat-duplicate and later-record rules reproduce, plus the coordinator's check results.

## Why
Every committed answer reproduces from the shipped files. The coverage set holds under every exposure variant that stratifies by road class and hour, and the 1.5 line sits clear of the nearest values (parcel 1.74; uncovered uses 1.21 to 1.22). The soft spot is that rule 3.2 asks for "miles their vehicles drove" while no file gives miles by use. The pack supplies one route (not-at-fault struck vehicles as exposure, spread over class-by-hour VMT built from Table 1 and the hourly counts), and the answer is stable to the day-type definition.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Crashes with 2+ vehicles in transport | 124,753 | 124,753 | yes |
| Crashes caused: taxi / ride-hail / limo / shuttle / paratransit / parcel / app | 1,564 / 6,762 / 558 / 648 / 865 / 3,317 / 3,282 | identical | yes |
| Private drivers' crashes | 91,211 | 91,211 (92,142 if motorcycles kept; rule 4.4 excludes them) | yes |
| Miles; strata | 60,420 M; 288 | 60,420.0 M; 288 | yes |
| Struck vehicles, one-at-fault crashes | 134,224 | 134,224 | yes |
| Ratios to private | 1.9 / 2.1 / 1.7 / 2.0; others under 1.3 | 1.92 / 2.08 / 1.74 / 2.00; 1.21 / 1.22 / 1.22 | yes |
| Ask 2 KSI | 74/402/45/63/55/109/136 | identical (seat/unit dedupe, later record, register upgrades, 2,038 of 2,038 matched one-to-one) | yes |
| Ask 3 cost USD M | 505.9/1,979.6/242.4/299.5/279.5/641.9/699.9 | identical | yes |

## Competing answers that survived
- Exposure stratification (main call). Class x hour, with or without day type, gives the golden set. Class x day type only gives 1.55/1.40/0.85/1.30/1.40/1.82/1.72, a different set; hour only and no strata also flip the set; per-vehicle counts cover all seven. The call is forced only for a solver who stratifies by both class and hour, which the pack's counts and VMT table support. The method is not filed. This is an analytical step, but a literal reader could call the estimator unfiled. Optional closure: file the WHAT (miles estimated by road class and hour of day), never the HOW.
- No other fork survives: the exposure pool, 239 unnamed 2016 units (117 at fault, effect under 0.01), and 402 crashes with no time move nothing near the line.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 17 including README | yes |
| Formats | 3+ | csv, xlsx, pdf | yes |
| Large file | 25,000+ rows | crashes 176,063; units 339,100 | yes |
| Distractors | 2+ named in metadata.json, none in a file name | weather and work_zone_log named; the thread also treats DMV registrations, platform reports and fleet returns as plausible wrong-basis reads | yes (declare them or confirm a shipped fact rules them out, as in pass 1) |
| Deliverables | 1 to 3, all in golden | xlsx and pptx present | yes |
| Asks | multi-dimensional, unit and rounding stated | 7 uses x 3 asks | yes |
| Rubric 25+ | 25+ | no rubric in the folder | unverified |
| Reads as real | yes | no exclusion-level finding | yes |

## Gate G reconciliation
Thread: method_or_model_selection, no surface-read dependency, no sole data defect. This matches the design note's induced-exposure mechanism. No declared distractor is named as carrying the task. Gate G: pass. Gate H: domain pass, layers pass, decisive_step analytical (road safety's exposure-adjusted crash rate; easy routes per-vehicle rate or unstratified induced exposure).

## Stump power (Gate F)
The thread rates it good: per-vehicle rates cover all seven, and unstratified or hour-only induced exposure flips shuttles and paratransit in and parcel out. The decisive step is the field's standard method, so the main thread weighs it against the scored readers' result (stumping 1.3). The post-pass-2 isolated reader found the persons' later listings from the PERSON_NO sentence and landed every ask figure; that sentence has been withdrawn.

## Findings, ranked
1. The pack changed after this verdict (73efe129 against fdf66198). The final persons wording was not judged by a thread.
2. The miles estimator is not filed; the thread treats the main call as forced by the data.
3. Wrong-basis reads not declared in metadata.json.
4. Rubric criteria count not verifiable here.

## Next action for the author
Ship 73efe12945f11373da611367702e51a9 (determinism APPROVE on the earlier cut, figures_check 44 of 44 on the final one), and decide whether to file the estimand wording for miles (by road class and hour of day) or to declare the DMV, platform and fleet files as distractors.

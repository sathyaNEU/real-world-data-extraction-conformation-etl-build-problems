# determinism-check report, task247, 2026-10-18

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The judge thread recomputed every load-bearing value from the fresh unzip and reproduced all of them. The main call is the nine-site list: PB06, PB07, PB09, PB10, PB11, PB12, PB13, PB14, PB15.

The prompt does not name the estimator of the unreleased 2027 reprocessed record. That is the one open point, and the shipped 2018-2026 overlap closes it:
- Interpolating the anomaly between observed days gives RMS 0.0648 on 11,857 unobserved days. The flag-mean correction gives 0.1426.
- On hot days (anomaly above 0.6) interpolation is biased -0.0009. NRT is biased -0.270 and the flag-mean correction -0.263.
- Replaying the season maximum over 144 site-years, interpolation misclassifies the alert level 0 times and the NRT-based routes 4 times.

Candidate lists:
- NRT as issued: 4 sites.
- Flag-mean correction: 3 sites.
- Interpolation: 9 sites.

The estimand (population, window, unit, comparison) is pinned by methods note sections 3 to 6. The method is a stump, not a fork. Every rigorous interpolation variant keeps the same nine sites, and the thread ran SST interpolation, bias 0.06, forward-fill, keep-warmer and no bias correction.

Margins are clean but thin. PB06 is 8.85 against the line at 8, and PB08 is 6.96 below it. The replayed season-maximum error has SD 0.33 and a maximum of about 2.0 (PB08, 2023).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Observed-day NRT less reprocessed bias | 0.06 | +0.0595 (n=40,735) | yes |
| Unobserved-day bias | -0.007 | -0.0066 | yes |
| Fill RMS and hot-day bias, interpolation | 0.065 / -0.001 | 0.0648 / -0.0009 | yes |
| Fill RMS and hot-day bias, flag-mean | 0.142 / -0.263 | 0.1426 / -0.263 | yes |
| 16 season-maximum DHW values (whole numbers) | 3,5,2,6,5,9,11,7,10,12,13,10,12,9,11,6 | all 16 match (PB06 8.85, PB13 12.26 as the closest to .5) | yes |
| Alert levels and 16 verdicts (8 confirm, 8 raise, 0 lower) | as golden | match | yes |
| Declared levels from the bulletins (critical component 3) | as listed | match | yes |
| 2023 survey prevalence and colonies, 16 sites | e.g. PB01 78.4 on 148, PB12 9.3 on 161 | all 32 match | yes |
| Logger hours, 16 sites | e.g. PB01 3584, PB02 2783 | all 16 match (UTC correction on the Cozumel II trips) | yes |
| "Six sites" regression alternative | 6 | not reproduced (specification not defined in the shipped text) | no, rejected alternative only |

## Competing answers that survived
None on the main call.

Ask-level notes, neither of which changes the golden:
- Duplicate colonies: a literal line-counter keeps 153 more colonies (PB01 79.1 on 153). The protocol's "recorded once" and the observer pattern (only DW and KT repeat) pin the golden. This is an ask-level semantic fork and acceptable for an ask.
- Logger clock: ignoring UTC on the Cozumel II trips gives +5 hours at every site. The logger's temperature step at the true retrieval hour pins the reading in the files.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 17 | yes |
| Formats | 3 or more | 5 (csv, pdf, xlsx, md, eml) | yes |
| Large file | 25,000 rows or more | 425,836 rows (logger readings); 57,824 rows (NRT extract) | yes |
| Distractors named in metadata.json, none labelled by file name | 2 or more | 2 (kd490 monthly, port tide gauge); neither file name labels it a distractor | yes |
| Distractors unused yet weighable, none answers a graded quantity | yes | unused by the solution; water clarity and tide are plausible stressors; neither carries a heat-stress figure. The thread did not independently test whether a shipped fact is needed to rule them out. | yes, weak relevance (finding 2) |
| Deliverables | 1 to 3, all present in golden | 2 (xlsx, pdf), both present in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 16 sites by level, verdict, prevalence, colonies and hours; rounding stated in the prompt | yes |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | shape 01 (ranked list under a line); 16 sites by about 6 figures plus the list and count, well over 25 by construction. The rubric is generated downstream and not counted here. | yes |
| Prompt form | one paragraph, question first, under 1,000 characters | 848 characters, question first, no persona or bullets | yes |
| Not LLM-reading, goldens business-realistic | yes | thread found no authoring disclosure, README in-fiction, dates coherent; golden realism not re-judged in this pass | yes, as far as checked |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no.

Card and design note: gate_g method_or_model_selection, stump_class analytical, layer2_family estimation_fit, no official decoy, no validated decoy.

They match on every key. The bulletins (rung 0, four sites) are the declared levels the call checks, not a distractor, and the thread did not treat them as carrying the task. Neither declared distractor (kd490, tide gauge) was named as the surface read. No mismatch.

## Gate H
domain: pass, layers: pass, decisive_step: analytical.

This matches the card's `analyst_test` and `domain_test` and the design note's `## Three rules`:
- Layer 1: reissues, flag recoding by version, kelvin, a missing day, UTC against local.
- Layer 2: estimation_fit, refilling the cloud gaps from both sides, chosen by a back-test on the overlap.
- Easy route: the mean correction, which gives 3 sites.

## Stump power (Gate F)
Moderate to good. The easy routes (NRT as issued, flag-mean correction, regression) give 4, 3 and 6 sites, and none reaches the nine. A strong solver must find the filled-day fade through the hot-day overlap error. A flat bias correction is the natural plausible-but-wrong route, so a real stump rate is expected. The design note's pair ceiling is 34.6.

## Findings, ranked
1. Residual risk, no action: the estimator is not named in the prompt, and only the overlap back-test forces it. This is the intended stump, not a fork, because every convention row closes to the same nine and all interpolation variants agree.
2. Minor: PB06 at 8.85 is the least-margin site (0.85 above the line). All variants keep it above 8.
3. Minor: the two distractors are weak in relevance (water clarity and tide). They are acceptable, and no change is needed.

No exclusion-level finding.

## Next action for the author
None required. Proceed to ship task247 with the leak reader's result. No re-judge is needed, since the disposition is APPROVE.

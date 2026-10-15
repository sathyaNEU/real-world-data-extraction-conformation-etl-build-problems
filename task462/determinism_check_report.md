# determinism-check report, task462, 2026-10-15

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor (detection-limited sampling, inverse-probability weighting), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Read literally, the standard and the prompt fix the estimand: methane the sites emitted at rates of 5 kg/h or more, averaged over the campaigns flown in each operator's part of the rating year, as a share of methane produced, rated at 0.20 per cent or less. The shipped release study and methods note supply the detection correction. The judge reproduced every figure and found a wide gap to the line on both sides: rated Calbrent 0.104, Ostrel 0.108, Corrandale 0.119 and Brushy Mesa 0.134; nearest unrated Ashmund 0.232. The set survived all reasonable variants (coordinate vs named-facility attribution, no or either-way operator time split, linear-rate logistic, floor 0). It changes only at a 10 kg/h floor (outside the filed 5) or with no detection correction (the golden's named wrong route, eight rated). Isolated sonnet thread, single pass, scratch /tmp/determinism-check-task462-1792083160/.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Detection curve (182 releases, 96 detections) | 8.0 / 23.9 kg/h | 7.96 / 23.86 | Yes |
| Plume file rows / attributed / none | 2,348 / 2,241 / 107 | same | Yes |
| Methane emitted, 12 producers (t) | 7,961 ... 19,935 per submission | identical, all 12 | Yes |
| Intensity, 12 producers (%) | 0.104 ... 0.420 | identical to 3 dp, all 12 | Yes |
| Gas delivered, 12 producers (MMcf) | 189,884 ... 88,158 | identical, all 12 | Yes |
| Gas flared, 12 producers (MMcf) | 2,180 ... 625 | identical, all 12 | Yes |

## Competing answers that survived
Advisory only, none flips the main call:
1. Detection correction is never stated as a method; a word-for-word executor summing reported plume rates files eight producers. The estimand ("emitted") plus the shipped study and note 2.1/4.2 force the correction. The judge treats it as analytical estimand choice, not a semantic fork. A hostile reader could call it open; optional pin: state that "emitted" covers plumes the pass did not detect.
2. Ask 3: treatment of the plant's prior-period-adjustment lines is not in the data dictionary. Statement-month basis gives different values (Anchell 189,774 vs 189,884). Production month in the reference is the natural reading. Risk is to exact-figure grading of ask 3 only.
3. Ask 4: code FR (from January 2026) is absent from the dictionary. The basin summary "flared" column equals FL + FR in every month, which resolves it from the files. FL alone gives Anchell 1,195 vs 2,180.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 19 | Yes |
| Formats | 3 or more | 4 (csv, pdf, xlsx, json) | Yes |
| Large file | 25,000 rows or more | 38,150 rows (ogc_well_production) | Yes |
| Distractors | 2 or more named in metadata.json, none in a file name | ghgrp_subpart_w ..., tollaver_basin_satellite_methane ... (file names do not label them); unused by the solution (judge) | Yes |
| Distractor weighing | relevant, ruled out by a shipped fact | Subpart W filings and satellite estimates are other measures of intensity; the standard's measured basis rules them out (design note) | Yes |
| Deliverables | 1 to 3, all in golden | 2, both in golden/ | Yes |
| Asks | multi-dimensional, unit and rounding stated | 12-producer slates x 4 figures plus a 2,348-row file; units and rounding in the prompt | Yes |
| Prompt shape / rubric | identifiable, 25 or more criteria | shape 01; design note records 26 ask criteria plus the main block (generated rubric rerun at ship) | Yes (rubric generated at ship, not re-verified here) |
| Reads as real | no LLM tells, goldens realistic | judge saw no authoring leakage; workbook has ratings, chart, detection curve and sources sheets | Yes (golden-realism upstream) |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The card has stump_class: analytical and an analyst_test that matches the thread's easy route exactly (blank counted as zero, eight rated, four over the line). The design note's decisive step (weight each plume by 1/detection probability fitted to the blind releases) is the thread's mechanism. No mismatch. The declared distractors (Subpart W, satellite) were not named by the thread as the surface read, so they are not too load-bearing. The only wrong-answer artifact route (carrying detections through the year, none rated) is the design's own named alternative, not a shipped ranking.
Gate G line: PASS, analytical_non_defect, no surface read, no sole data defect.

## Stump power (Gate F)
Moderate on the main call, high on the asks. A strong model that fits the logistic from the release workbook will pass the main call. Likely losses are the second-order work: shared facility numbers (one-to-many lookup), pad vs tank-battery attribution, cloud-lost campaigns, the operator-change time split, and the ask 3 and ask 4 mess. The judge cannot estimate the empirical stump count.
Gate H line: domain: pass, layers: pass, decisive_step: analytical (detection-probability-weighted inverse estimation calibrated on controlled releases; not decoy, not semantics, not rule application). Matches the design note's `## Three rules` and the card's domain_test.

## Findings, ranked
1. Advisory: ask 3 prior-period-adjustment basis is unpinned in the dictionary (exact-figure grading risk).
2. Advisory: code FR not in the dictionary, resolved only via the basin summary.
3. Advisory: the detection correction is forced by estimand and shipped study, not stated as a method. Per CLAUDE.md the WHAT may be filed; filing "emitted includes undetected plumes" is estimand, not method, and is optional.
4. Stump-power note: the controlled-release workbook is a strong cue to the correction; thinning it would raise main-call difficulty without touching the estimand.

## Next action for the author
Ship as is. Optionally pin the prior-period-adjustment treatment and code FR in tarvane_rating_folder_data_dictionary.xlsx if you want asks 3 and 4 closed by a file; this leaves the main call untouched but needs a rebuild and re-zip.

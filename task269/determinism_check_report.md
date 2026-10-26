# determinism-check report, task269, 2026-10-26 (stage 4 round 2; supersedes round 1)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Bundle judged: target.zip md5 a4d6a8c43523ade49fd4523d3d787a37, fresh unzip at /tmp/determinism-check-task269-035102/target/. Judge verdict: /tmp/determinism-check-task269-035102/verdict.md. The judge thread was run by the main session (this runtime has no Agent tool); one thread, one pass.

## Why
Grant terms 2.1 to 2.4 file the estimand literally (compliance over the moments on every AM and PM shift of 2025-26, shifts weighted by required care hours, funded below 80 per cent, at most six). The gold audits avoid short-staffed shifts (5.3 per cent of audited moments on shifts over 10 per cent short, against 18.8 per cent of care hours; compliance 58.9 against 87.1). Every staffing-adjusted estimator tried funds AMU, ESSU, 4A, 7A, 9B (74 to 78.4 per cent); the sixth ward is at 80.9 or above (golden model 84.2), so the cap never binds. Asks A and B reproduce for all 14 wards.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Raw audit compliance, AM/PM | 9B 77.0, others 82.8+ | 9B 77.0, ESSU 82.8, AMU 83.2 ... ICU 88.4 | yes |
| Share of audited moments on >10% short shifts | 5.3 | 5.27 | yes |
| Share of care hours on those shifts | 18.8 | 18.75 | yes |
| Compliance short vs rest | 58.9 / 87.1 | 58.87 / 87.13 | yes |
| Funded set (ward + ratio bands, logistic, care-hour weighted) | AMU, ESSU, 4A, 7A, 9B | 9B 74.4, 4A 75.1, ESSU 75.3, AMU 76.1, 7A 76.2; next 8A 84.2 | yes |
| HOBSI per ward (Ask A) | 14 pairs, total 304 | all 14 | yes |
| Hand rub L and per 1,000 OBD (Ask B) | 14 pairs | all 14 | yes |

## Competing answers that survived
None on the main call. Alternatives returning 9B alone (raw audit rate, audit share weighted by care hours, per-audited-shift weighted by care hours) ignore the measured selection of audited shifts and do not estimate the filed estimand. A model with no ward term drops 9B but discards the ward-level target. Ask-level residuals, all closed by the shipped text: chained admissions (304 episodes vs 285 per admission; golden is the literal reading), one isolate matching two patients on DOB and sex (only one has an admission covering collection), resent dispenser records (184 under any look-back of 20 days or more).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 18 | yes |
| Formats | 3+ | 4 (csv, txt, pdf, xlsx) | yes |
| Large file | 25,000+ rows | acuity 224,319 | yes |
| Distractors | 2+ in metadata.json, none labelled by file name | patient_experience_survey, staff_influenza_vaccination | yes |
| Distractor weighs but unused | yes | survey hand hygiene question (~93 per cent every ward) ranks nothing; terms 2.3 make the gold audits the record | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both present in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 14-ward HOBSI and rub tables, rates per stated denominator, one decimal | yes |
| Prompt shape and 25+ criteria | yes | per-ward and per-cell grading (about 60 figures) | yes |
| Not LLM generated, goldens realistic | yes | judge found no benchmark or synthetic language; PDF Producer field minor | yes (minor note) |

## Gate G reconciliation
Judge: mechanism statistical_rigor, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: no planted memo, no shipped figure ranks wards, the only declared distractor (patient experience survey) ranks nothing at about 93 per cent. The thread did not name the declared distractor as the surface read. No mismatch.

Gate H: domain pass, layers pass, decisive_step analytical. Matches the note's `## Three rules` (No decoy, Not semantics, Not rule application) and its analyst test (care-hour weighting of the audits files 9B alone).

## Stump power (Gate F)
Strong per the judge: the easy route (weight audited compliance by care hours) files 9B alone; only a shift-grain join of audits to roster and acuity reveals the selection. The method is a standard post-stratification route, which the blind readers' result should weigh (stumping 1.3). Asks add separate devices (chained admissions, DOB/sex link, transfer-rebuilt attribution, handheld resends).

## Findings, ranked
1. None blocking.
2. Optional wording: SOLUTION_STEPS 6 could say the one isolate matching two patients on DOB and sex is linked to the patient whose admission covers the collection. No rerun.
3. Minor: PDF Producer metadata names a person or the organisation rather than software.

## Next action for the author
Proceed to ship; optionally add the one-sentence step 6 wording note to submission.md.

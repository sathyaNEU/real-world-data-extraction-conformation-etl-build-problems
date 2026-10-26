# determinism-check report, task269, 2026-10-26 (pass 3, target.zip md5 dfc0f006c43b02bff253cc2430452302)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated thread (verdict at /tmp/determinism-check-task269-050951/verdict.md) recomputed the call and all three ask tables from a fresh unzip. The funded set AMU, ESSU, 4A, 7A, 9B holds under nine model variants (nearest unfunded ward 83.9, funded wards 74.0 to 78.6). The audits as they stand give 9B alone. The rounds and store changes since pass 2 (repeat-minute dispenser records outside a re-sent record, contractor 8810 issues removed, no terminal-clean job in a re-sent batch) reproduce: Asks B and C 28 of 28 each, Ask A 14 of 14 counts and rates.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Audits as they stand | 9B 77.0, others 82.8 or above | 9B 76.95, ESSU 82.82, others 83.2 to 88.4 | Yes |
| Audited moments on shifts over 10 per cent short | 5.3 | 5.27 | Yes |
| Care hours on such shifts | 18.8 | 18.75 | Yes |
| Compliance on short / other audited shifts | 58.9 / 87.1 | 58.87 / 87.13 | Yes |
| Funded five below 80 | AMU, ESSU, 4A, 7A, 9B | same; 9 variants identical | Yes |
| HOBSI counts and rates, 14 wards (Ask A) | total 351 | 351, all 14 and rates | Yes |
| Hand rub litres and per 1,000, 14 wards | Ask B | 28 of 28 | Yes |
| Soap litres and per 1,000, 14 wards | Ask C | 28 of 28 | Yes |

## Competing answers that survived
- "9B alone" (audits as filed, or weighted by shift or AM/PM share). Closed by the terms' estimand (every moment on every AM and PM shift) and the shipped contrast 58.9 against 87.1. Low residual, not an open fork.
- Ask A only: a zero-gap admission (next begins at the minute the previous ended) read as a separate stay gives 332 instead of 351 and moves 4A, ESSU, AMU. Golden chains them. The solution steps and the definitions' stay wording are meant to close it; the judge treats it as forced but it is the one place a reasonable alternative reading exists. Optional pin, a data-dictionary line, no rerun. The design note records readers split on this device (round 2); it is an ask-level device, not the main call.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 18 | Yes |
| Formats | 3 or more | csv, pdf, xlsx, txt | Yes |
| Large file | 25,000 rows or more | 224,319 (acuity), 72,749 (roster), 26,265 (audits) | Yes |
| Distractors in metadata.json | 2 or more, none labelled by file name | patient_experience_survey, staff_influenza_vaccination; unused, names neutral | Yes |
| Distractor relevance | weighable, ruled out by a shipped fact | hospital-ward datasets by ward, no graded quantity answered | Yes (judge: present and unused) |
| Deliverables | 1 to 3, each in golden | xlsx and png, both in golden | Yes |
| Asks | multi-dimensional, unit and rounding stated | 84 figures over 14 wards, litres and per 1,000, one decimal; counts whole | Yes |
| Prompt shape and rubric | identifiable, 25 or more criteria | every ward and figure graded (more than 25) | Yes |
| Not LLM-generated, realistic goldens | | judge found no disclosure or synthetic tell; real-world irregularities present | Yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor, family analytical_non_defect, surface read no, sole defect no. Design note: Layer 2 estimation_fit (audit sample selected on a covariate that drives the outcome, post-stratified on the shift's required-over-worked ratio), no decoy. Match. The declared distractors are not the surface read; the surface read (audit rate as filed) is the task's own R0/R1, not a shipped ranking. No shipped artifact ranks wards on compliance.

## Gate H reconciliation
Thread: domain pass, layers pass, decisive_step analytical. Design note Three rules: same (domain test: compliance carried to the ward's workload mix; Layer 1 mess named and separate). Match. The decisive step is a modelled extrapolation with a 9-variant robust outcome, not a filed method, so it is not rule application. The judge notes a borderline: a reviewer could read "set aside the audit rate" as rejecting a correct number; the terms define the population as all shifts, which supports the estimation reading.

## Stump power (Gate F)
Judge: good. The easy route files 9B alone (four wards short); the correct route needs the acuity and roster join that no file narrates. The model fit is a standard estimator, but the judgment (that audits are selected on staffing) is settled by the data. Weigh with the scored readers' result (design note: both stage 4 round 4 readers filed 9B alone). Chart bar heights vary 1 to 4 points across valid methods; grade with a tolerance.

## Findings, ranked
1. Ask A stay-chaining residual (optional pin, no rerun).
2. Chart bar heights method-dependent (grading tolerance).
3. Minor Layer 1 label mismatch (audit "Assistant in nursing" against program "Personal care staff"), benign.

## Next action for the author
Proceed to ship from this target.zip; optionally add one data-dictionary line that admissions meeting at the same minute form one stay (this would change the zip, so only if re-cutting anyway).

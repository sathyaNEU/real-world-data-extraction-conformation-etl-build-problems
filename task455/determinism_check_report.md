# determinism-check report, task455, 2026-10-15

## Verdict
NOT_DETERMINISTIC (underspecified_objective on the xlsx supplementary asks only; the main call and the PDF figures reproduce and are forced). SOLUTION_WRONG does not apply.
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection (misclassification-corrected estimand), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The main recommendation (release, 190 against a baseline of 253, 24.9 per cent below) reproduces exactly from the files. Schedule B1 to B5 plus the 2025 review force it, and the competing methods are analytical errors that the data separates.

The xlsx ask 1, "how many it has added since", has two licensed readings that differ in six of seven years.
- The golden uses gross additions: 8/3/4/3/10/5/6.
- Net change (current file minus file at close) gives 6/2/2/1/9/3/6.
- Dropped deaths are amendments that moved a death to another county of residence or to a non-drug cause (10 cases over 2019 to 2024). Neither the prompt, the agreement nor the dictionary says whether those subtract.

Gates C and E fail on that ask (xlsx ask 1, years 2019 to 2024). A minor second fork sits on xlsx ask 2 (EMS residents with a blank home county).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Opioid certified deaths 2021/22/23/26 (wendmoor_death_records_2019_2026.csv) | 245/264/262/241 | 245/264/262/241 | yes |
| 2025 review join (ome_drug_death_review_2025.xlsx) | 216 opioid, 128 stimulant w/o opioid, 64 other (408 of 408 matched) | 216/128/64 | yes |
| Certificate rates from the review | opioid named 189/216 (.875); 64/128 stimulant deaths (.5); 0/64 other | same 3x3 confusion matrix | yes |
| Solved opioid deaths per year | 248/262/249/190 | 248.0/262.1/249.1/190.1 | yes |
| Baseline (Schedule B2) and change | 253; 24.9% | 253.1 (253 from rounded years); 24.89% | yes |
| Bridge lines | 245+31-28; 264+33-35; 262+31-44; 241+24-75 | 31.0/28.0; 32.8/34.7; 31.1/44.0; 23.8/74.7, round to golden | yes |
| Deaths on file at close, 2019 to 2025 | 334/377/385/410/404/406/408 | identical (receipt date for out-of-state versions; closed_date from vital_records_data_year_status.csv) | yes |
| "Added since" (xlsx ask 1) | 8/3/4/3/10/5/6 | gross reproduces; net is 6/2/2/1/9/3/6 | yes, as gross only; fork open |
| EMS non-fatal opioid encounters, 24 quarters (ems_patient_care_reports_2021_2026.csv) | listed | all 24 reproduce under (incident, sex, age) grouping, naloxone or T40.0-4/T40.6 on any report, Wendmoor home county on any report, no Dead disposition, quarter of psap_call_datetime | yes, under that reading; fork open |

A four-class inversion gives the identical 248.0/262.1/249.1/190.1. Bootstrapping the 408 review cases gives the change a median of 24.9 per cent (95 per cent interval 18.6 to 36.1), with 92 per cent of draws clearing 20 per cent: thin but clean on the filed point-estimate rule.

## Competing answers that survived
1. **xlsx ask 1, "added since" (open fork).**
   - Gross: deaths on today's file not on the close file (golden 8/3/4/3/10/5/6, the more literal reading of "added").
   - Net: today's count minus the close count (6/2/2/1/9/3/6).
   - Shipped rule meant to close it: none. A rigorous solver can reasonably give either answer, and the split is interpretation, not analysis.
2. **xlsx ask 2, EMS residents (minor open fork).**
   - 6,284 of 20,413 reports have a blank home county ("blank when not obtained"). The golden counts an encounter only if some report records Wendmoor (339/344/364/350/...).
   - Treating blank county and blank state as local gives 358/371/388/374/..., about 6 per cent higher every quarter.
   - By incident (327/337/359...) or by report (363/355/392...) are clearly weaker readings.
   - "Residents" favours the golden reading, and B6 says "county residents", but no file states how unknowns are treated.

Not forks (closed by the files):
- Main call method. Raw counts or a single scaling factor give 241 against 257.0, 6.2% below, so "first year only". A binary constant-FPR correction gives 198.8 against 226.0, 12.1% below, also "first year only". The review shows the false positives come only from stimulant deaths (64 of 128 against 0 of 64 other drug deaths), and the stimulant share of certificates rises from 21 to 56 over 2021 to 2026, so the three-class solution is the only one that uses the measured error consistently. The review's "same laboratory since 2018" sentence supports carrying the 2025 rates across years.
- Out-of-state effective date. registered_date gives 336/378/386/411/406/407/410 at close. The receipts file and its dictionary entry make received_date intended, so this is Layer 1 mess recoverable from the files.
- 2026 file taken as it stands at the extract (B4); 31 pending (R99) records are not a fork.

Gate B: every decisive fact is in a shipped file (B1 to B6 in ori_grant_agreement_2024.pdf, review workbook rates, close dates, exchange log). No external knowledge needed. The 17 June 2027 date appears only in the prompt and does not matter.

## Spec gates
Taken from the judge's Files/Hygiene section. Items the judge could not see are marked not checked here; I did not re-judge.

| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 10 | yes |
| Formats | 3 or more | 3 (csv x6, xlsx x2, pdf x1) | yes |
| Large file | 25,000 rows or more | death file 55,523 version rows; EMS file 20,413 | yes |
| Distractors | 2 or more in metadata.json, none named by file | population estimates and naloxone kit distribution present and unused; metadata.json naming not checked here | yes on presence; naming not checked |
| Distractor relevance | weighable, ruled out by a shipped fact | not checked here | not checked |
| Deliverables | 1 to 3, all in golden | xlsx and pdf-derived figures seen by the judge; count not checked here | not checked |
| Asks | multi-dimensional, unit and rounding stated | ask 1 wording ambiguous ("added since"); other asks not checked here | no (ask 1) |
| Prompt shape and rubric | 25 or more criteria | not checked here | not checked |
| Not LLM generated; realistic goldens | yes | judge: data evidently synthetic but reads as operational extracts; one About-sheet sentence ("same laboratory, contract and panel since 2018") reads slightly like a justification; license and provenance records not visible to the judge | yes with note |

## Gate G reconciliation
Thread: `mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. Gate G passes: no shipped artifact ranks candidates wrongly on the decision question, and the difficulty would survive deleting every wrong number. The declared distractors (population estimates, naloxone kits) were not named as the surface read carrying the task.

Gate H line: `domain: pass`, `layers: pass`, `decisive_step: analytical`. Layer 1 is version chains, legacy codes, interstate receipts, delayed close dates and multi-report EMS encounters. Layer 2 is a composition-aware misclassification-corrected annual burden validated on the 2025 medical examiner review. The swap test fails to carry over to "visits" or "megawatt-hours". The filed rule states only "correct by the error the review measures", not the steps, so it is not rule application.

Not done: comparison against the design note and the card (`stump_class`, `analyst_test`, `domain_test`). The caller asked for a report from the verdict only, so I did not open either. The author or caller should run that comparison before treating Gate G as reconciled.

## Stump power (Gate F)
Moderate on the main call. The easy routes (raw count, single factor, binary constant-FPR correction) land on 6.2% or 12.1% below the baseline and the call "first year only" instead of release. A strong model that notices the stimulant-driven false positives and stratifies reaches the golden. The xlsx asks add interpretation traps (received date, gross versus net, unknown county) that would stump for the wrong reason if left unpinned, which is a defect rather than difficulty.

## Findings, ranked
1. xlsx ask 1 "added since" is a two-way fork (gross versus net), different in 2019 to 2024. Fails Gates C and E.
2. xlsx ask 2 EMS residency with blank home county is a minor fork (about 6 per cent level shift every quarter).
3. Observation: the review's About-sheet "Toxicology" row reads slightly like a justification for transporting the rates.
4. Observation: the 95 per cent interval on the change (18.6 to 36.1) sits close to the 20 per cent threshold; this is a thin margin on the filed point-estimate rule, not a defect.

## Next action for the author
Run `/fix-determinism task455`. In `prompt.txt`, replace "how many it has added since" with a pinned phrase such as "how many deaths on the file today were not on it at its close" (the golden 8/3/4/3/10/5/6 stays), and preferably pin EMS residency as "residents (a Wendmoor home county recorded on at least one report of the encounter)". Add no wording that describes the three-class correction or the stimulant mechanism, since that would turn the decisive step into rule application. The golden figures, stump and data stay byte-identical, so the main-call ladder needs no rerun.

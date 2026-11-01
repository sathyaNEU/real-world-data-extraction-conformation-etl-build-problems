# determinism-check report, task501, 2026-11-01 (pass 3)

Judge thread verdict: /tmp/determinism-check-task501-58603/verdict.md (one thread, sonnet, medium, scratch folder only). Bundle: target.zip md5 81564f489c1ab10c04582ad74fecb818, 18 files (csv, pdf, xlsx), no docx or txt.

## Verdict
DETERMINISTIC. No SOLUTION_WRONG.
**Disposition:** FIX_NOW, optional and narrow: one wording change to the Ask 3 unit (see Next action). The main call and every graded figure are unchanged by it, so no rerun.
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Fund B is forced. Term-time (2 to 26 May 2023) diaries, scaled so a wholly susceptible region gives R0 15 (PS-07 3.2), give 1.299 with no catch-up. Each option's made-immune people come off its birth years' susceptibles (PS-07 3.5): A 1.288, B 0.892, C 1.292, D 1.292, E 1.289. PS-07 3.6 picks B, the only option below one. The thread reproduced all five people cells, all five dose pairs and all five case pairs. I re-ran the case column myself (below). The residual forks sit on asks, none moves the call.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| R, none / A / B / C / D / E | 1.3 / 1.3 / 0.9 / 1.3 / 1.3 / 1.3 | 1.2992 / 1.288 / 0.892 / 1.292 / 1.292 / 1.289 | yes |
| 15-19 susceptible share / region | 11.2% / 4.8% | 11.22% / 4.83% | yes |
| Residents A to E | 35,346 / 33,217 / 29,398 / 30,625 / 57,865 | same | yes |
| No dose / one dose A to E | 3,545/4,720; 4,286/6,091; 2,857/3,960; 4,971/7,302; 8,526/11,793 | same | yes |
| Cases / imported A to E | 9/2, 10/2, 11/3, 10/3, 16/5 | same (and mine, from nds_measles_cases_oriel_2019-2027.csv) | yes |

My own check of the case file: 119 rows, 96 Confirmed with onset 1 Jan 2019 to 30 Jun 2027 (25 Imported, 71 Import-related). Joining the 28 back-entered 2019 records to their migrated records by legacy number leaves 68. Six GP-and-hospital double notifications (same date of birth, sex, onset and county, different case_id) leave 62. A key of date of birth and sex alone also gives 62, and date of birth, sex and onset gives 62.

## Competing answers that survived
Rulings on the thread's six residual forks. "C1" is closure by convergence in the data or by a shipped document read literally.

1. **Diary set (term-time against pooled).** Ruling: this is the stump, not a fork, and it is closed by the filed text, so no pin. Pooled diaries give none 0.88 and "no catch-up needed", the easy route. Four things converge on term time. (a) PS-07 3.1 requires the figure to stay below one "throughout" the winter. A reader who does not know the calendar must satisfy every regime the diaries show, so the binding figure is the term-time 1.3 (holiday diaries alone give 0.83). Only an average of the two regimes gives 0.88, and an average is not "throughout". (b) The survey's at_school field separates the regimes (design note SF25: 17.5% of contacts at school in May against 2.2% in July and August). (c) The options paper has the school team in schools from 15 September to 20 November. (d) B stays under one at every holiday weight (0.96 at weight 0.5). The residual is that the 1-dp figures for none, A, C, D and E move to 1.2 only for a solver who invents a Christmas-holiday share, which no file supplies. Filing "term time" would file the decisive step, so it is barred and I do not recommend it.
2. **One person per child across registrations.** Ruling: designed device (Ask 1's second device, SF29), closed by the data, not by a document. It is the weakest closure of the people asks, and I record it as such. The data: 201 unmerged pairs, each sharing one GP return line and agreeing on date of birth, sex and area, none on three, no other line on two. A line is one dose to one child, so the other reading has one dose given to two children. No shipped sentence says so; the thread's own count under the other reading is 35,440 / 33,270 / 29,427 / 30,640 / 57,890. It is not a genuine second figure by the pack's own logic, but it is an inference from the data, not from text. Filing it would hand over the device, so leave it.
3. **Blank LHO code as not in the region.** Ruling: closed by convergence (C1). All 1,091 blank-code registrations, and only they, carry BT postcodes (I confirmed 1,091 and 0 BT postcodes with a code). The code route and the address route both exclude them. The alternative needs a blank code to mean "in the region", which neither route supports and the thread itself calls an outside-fact reading. Not a genuine second figure. Not a stump or a device in the main sense (SF23 retired).
4. **LH27 scheme in force at lho_recorded against the 2024-07 list.** Ruling: closed by a shipped document read literally. The circular (lho_revision_circular_2024-04.pdf) says LH27 Monaghan West was merged and the code went to a new Portlaoise area from 1 July 2024; lho_recorded dates every row. The 2024-07 list holds LH27 as Portlaoise, Midlands, from 2024-07-01 only. Applying it to earlier recordings contradicts the circular. This is the designed first device of Ask 1 (D7). Not a genuine second figure.
5. **"Imported" against "Import-related".** Ruling: closed by the literal reading of the column's own two labels, but weaker than before. The prompt says "imported", the column carries the distinct value Imported, and Import-related is a different named value. Counting both makes 71 of 96 rows imported and every confirmed case imported (9, 10, 11, 10, 16), so "whether any" would be trivial. One flag: the pass 2 closure rested on the register or case field notes, and this bundle ships no notes (the design note's "the field notes define both" is stale, the notes are gone from the 18 files). So the row now stands on the label alone. I rule it not a genuine second figure, since "imported" matches one value word for word, but it is a hazard (design note: hazard, not a device). No pin recommended.
6. **Case de-duplication (legacy number only against the golden).** Ruling: a genuine second figure on Ask 3 in the strict sense, because the bundle shipped no sentence that a case is an illness and not a record. Reconciliation with pass 2: pass 2 reproduced the same golden at 113 rows reduced to 81 by legacy number, so legacy-only pairing was then enough. This cut has 119 rows. The six extra rows are the GP-and-hospital double notifications the ask rework added (Ask 3 second device). They share date of birth, sex, onset and county, carry no legacy number and no epi-link, and are only joined by the person's own attributes. Pairing by legacy number alone now gives 68 persons and 10/3, 12/3, 13/4, 11/4, 17/6 (my recomputation matches the thread; the thread's 96 rows and 62 persons match mine). The pass 2 closure does not carry over to this cut. Is the legacy-only figure a competing defensible answer? I judge it a near miss, not a coherent literal reading: a reader who collapses back-entries because they are the same illness cannot also count two same-day, same-person, same-county notices as two cases (the thread itself accepts the legacy collapse with no filed rule). The comments name them as notifications by a GP and a hospital. Still, "cases" is not defined in the pack, so the reviewer can open it. Smallest closure that does not file the device: change the unit of the count from records to people, "how many people born in its years had a confirmed measles case with rash onset from 1 January 2019 to 30 June 2027, and whether any and if so how many of them were imported". This is a WHAT (the unit), not a HOW: which records are one person stays for the solver to find. It reproduces the golden under every person key I tried (date of birth and sex 62, with onset 62, via legacy number 62), and the 2024 twins (a boy and a girl) stay two people. The prompt is 904 characters; the swap is about length-neutral, so check voice-check.py and the cap.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 18 | yes |
| Formats | 3 or more | csv, pdf, xlsx | yes |
| Large file | 25,000 rows or more | register_mmr_events 280,221 rows (people register 165k) | yes |
| Distractors | 2 or more in metadata.json, none named in a file name | national_mmr_uptake_report_2027q1.pdf, mmr_stock_return_2027-06-30.csv (also nmrl results, unnamed, inert) | yes |
| Distractor weight | unused, weighable, ruled out by a shipped fact | uptake report covers 2022-25 births only (SF3); stock return unrelated to any graded quantity; the thread found both inert | yes |
| Deliverables | 1 to 3, all in the golden, no format family | xlsx and pptx, both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | grids by option; prompt states one decimal and whole numbers | yes |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | shape 07 (grid), about 37 criteria per the design note; the rubric itself is not in the folder, not verified by me | yes (design note) |
| Reads as real work | no LLM tell | thread: operational artefacts, real mess, no authoring language | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection (contact matrix for the season at risk), family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: mechanism R = rho(q diag(s) C) on term-time diaries, Gate G method_or_model_selection; card stump_class analytical, with an analyst_test naming the same easy routes (herd-immunity threshold, susceptibles weighted by contacts, every diary pooled) and a domain_test on the next-generation eigenvalue. They match. The thread names pooling all diaries as the easy route, which is the stump; it does not name either declared distractor (uptake report, stock return) as the surface read carrying the task. No distractor finding.

## Gate H
Thread: domain pass, layers pass, decisive_step analytical, with the caveat that term versus holiday rests on calendar knowledge and could be read as data semantics. The design note's Three rules agree (domain test on the next-generation eigenvalue, Layer 1 the register, case and survey mess, Layer 2 the season's matrix). I side with analytical: the choice of which regime the estimand covers is estimand choice, and a strong analyst who has cleaned the data and read every rule still files 0.9 by pooling.

## Stump power (Gate F)
Moderate. Not a landable-by-standard-method case: the golden needs the solver to see two diary regimes and bind "throughout", which a textbook next-generation-matrix build does not do by itself (it pools). The asks add heavy failure weight (LH27, merges, query log, unmerged duplicates, legacy and double notices). The main thread should weigh this against the design note's ladder.

## Findings, ranked
1. Case unit is undefined (fork 6): the only fork I would close. Legacy-only figures differ by 1 to 3 on every cell.
2. Fork 2 (one child) stands on data inference alone; accept, the reship brief bars filing it.
3. Fork 5 now has no shipped definition; accept, the literal label closes it.
4. Design note line about "the field notes define both" is stale; this bundle ships no notes.
5. Forks 1, 3, 4: closed as ruled; fork 1 is the stump and must not be filed.

## Next action for the author
Optional, one step: reword the Ask 3 clause of prompt.txt so the unit is people, as in fork 6, and re-run voice-check.py and the 1,000-character cap; leave Asks 1 and 2 and the stump unfiled. No data, golden or figure moves.

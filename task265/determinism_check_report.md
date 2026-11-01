# determinism-check report, task265, 2026-11-01

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judged: the current shipped cut (13-file target.zip: no data dictionary, no export manifest; policy VA-07 clause 4.3 with the follow-up sentence; prompt without counts). One thread, one pass. Thread output: /tmp/determinism-check-task265-1793567956/verdict.md.

## Why
Every committed figure reproduced from the shipped files alone: the six ten-year cumulative percent revisions, the 18 construct-by-hospital counts (1,009 hips), the 28 hips missing from the registry (by construct and by hospital) and the keep/off split. Policy VA-07 4.2 to 4.4 files the estimand (Kaplan-Meier, first revision only, deaths and moves out of Wisconsin censored, extract of 31 Dec 2026, 5.0 bar). The decisive step, risk sets that start at each legacy hip's "Enrolled on" visit, is read from the legacy workbook and the data-management log. The nearest alternatives (clock from operation, clock from 1 Jan 2018, crude share) each give a different, weaker answer. Removing the dictionary and manifest did not open a fork the thread could land on: every call outcome survives the ten-year day count (3,650 / 3,652.5 / 3,653), the month-only death day (1st / 15th / 28th) and ignoring moves or deaths.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Edvalt/Kelvarne 10-yr CPR | 7.0 | 7.02 | yes |
| Edvalt/Pellvoro | 5.7 | 5.68 | yes |
| Askvane/Quarvel | 3.7 | 3.70 | yes |
| Holbrin/Pellvoro | 4.1 | 4.10 | yes |
| Askvane/Pellvoro | 3.5 | 3.50 | yes |
| Kalvoran/Morvenne | 7.6 | 7.62 | yes |
| 2026 primary total hips (periop log net of explants, case-list side) | 1,009; 18 construct x hospital cells | 998 cases, 11 bilateral = 1,009; cells match | yes |
| Missing from registry (merge-resolved MRN, side, date) | 28 (1/2/7/4/8/6; 12/5/11) | 28, same splits | yes |
| Missing without him_mrn_merges | not claimed | 40 | n/a (merge file needed and shipped) |
Wrong routes (thread): from operation 3.08/3.16/2.15/3.24/3.02/6.25; from 1 Jan 2018 gives Edvalt/Pellvoro 4.55; crude share keeps all six.

## Competing answers that survived
None that change a graded figure. Two wording gaps the thread flagged as clarity points, not forks, because the data settle them: (1) no shipped text says implant rows on the non-operated side of a one-sided case are not that day's operation (the case-list Side column and registry data settle it, 48 cases); (2) no shipped text states that the registry holds a legacy hip only if unrevised at its visit, so the left-truncated entry rests on the "Enrolled on" column and the log's legacy-enrolment entries. Under a strict literal reading of 4.3, "Kaplan-Meier ... for every primary total hip" does not file the time origin; the thread judged the enrolment-visit entry the expert default and the only reading the files support, with the alternatives weaker. This is the intended Layer 2 and not a semantic fork, but it is the residual risk of the dictionary removal.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 13 | yes |
| Formats | 3+ | CSV 7, XLSX 4, PDF 2 | yes |
| Large file | 25,000+ rows | periop_implant_log_2026.csv, 32,416 | yes |
| Distractors | 2+ named in metadata.json, none labelled in a file name | price schedule PDF, clinic visits CSV; neither named as a distractor in file names | yes |
| Distractors unused, relevant, ruled out | yes | price schedule lists prices only; clinic visits unused (its enrolment dates equal the workbook's, so it supports the truth, not a wrong answer) | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, docx), both present in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | per-construct, per-hospital, per-cell asks; one decimal for percentages, whole hips, stated in the prompt | yes |
| Prompt | one paragraph, under 1,000 chars, no data counts | 790 chars, no counts | yes |
| Rubric 25+ criteria | 25+ | generated at build; the answer set (6 + 18 + 6 + 3 + chart/memo elements) supports well over 25; not counted here | yes (by construction) |
| No LLM tells, goldens read as work products | yes | thread found no authoring or benchmark language, no temporal incoherence; goldens not separately realism-read here | yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and metadata.json (read after the thread returned): declared distractors are Schedule B of the price schedule and the clinic visits file; the declared stump is the left-truncated risk set. No match problem: the thread named no distractor as the surface read carrying the task. Gate G line: analytical_non_defect, no surface read, no sole data defect (matches the prior pass).
Gate H line: domain pass, layers pass, decisive_step analytical. Matches the card's analytical stump_class and the note's Three rules (No decoy, Not semantics, Not rule application all present).
Note: the design note's build record still describes a 15-file pack with a dictionary; it is stale against the shipped 13-file cut and should be updated at the next note edit.

## Stump power (Gate F)
Moderate to strong. The easy route (Kaplan-Meier clocked from the operation) keeps both Edvalt constructs at 3.1 and 3.2 and removes only Kalvoran/Morvenne, a confident wrong call; cleaning alone does not catch it. The entry-time insight must come from the legacy workbook's structure. The decisive step is a method choice a strong registry analyst would know, so a strong solver can land it (stumping 1.3), which the main thread weighs against the ladder. The supplementary counts (explant netting, one-sided case opposite-side rows, merge-resolved matching) add grain-level work.

## Findings, ranked
1. Low: with the dictionary gone, the time origin for left-truncated legacy hips is inferred from the "Enrolled on" column and the log, not filed. Thread reads it as settled by the data.
2. Low: the non-operated-side rule is unfiled but settled by the case-list Side column.
3. Housekeeping: design note build record still lists the dictionary and 15 files.

## Next action for the author
None required to ship. Optionally refresh the design note's pack description to the 13-file cut.

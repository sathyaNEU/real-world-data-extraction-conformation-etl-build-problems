# determinism-check report, task122, 2026-10-13

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judge thread: one general-purpose sonnet agent at medium effort, reading only /tmp/determinism-check-task122-1791905812/target/ (fresh unzip) and the inlined brief. Verdict file: /tmp/determinism-check-task122-1791905812/verdict.md.

## Why
Every graded figure reproduces from the shipped files. Every filed-rule reading tried gives the same call: first-sample rule, post-stop samples set aside, baseline as mean of screening and day 1, central eGFR, dosing records over the disposition form, AE group identifier, potassium from all laboratories. The one unfiled choice is the start of the chronic-phase line (the prompt names no window). The data fix it: the 40 mg and 20 mg difference series are linear from week 24 (SSE of the 40 mg line 0.014 from week 24, 0.013 from week 32, 0.073 from week 20, 0.593 from week 12). Every start from week 24 to week 32 gives the same call and the same four integers (20 mg 3, 40 mg 2, 10 mg 1, 5 mg 0). Gates A to E pass.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| eGFR diff at month 36, 5 / 10 / 20 / 40 mg | 0 / 1 / 3 / 2 | -0.01 / 1.05 / 3.04 / 2.04 (patient-level OLS from wk 24: 3.03 / 2.05 / 1.05 / -0.01) | yes (lb, dm, ex, sv) |
| 40 mg wk12 to wk24 rise | 1.8 | 1.8 (-6.08 to -4.31) | yes |
| Week-52 best dose alone | 10 mg | 10 mg (-0.34) | yes |
| Loop diuretic reduced, 40 / 20 / pbo | 50/55, 35/61, 1/50 (weeks 12, 16, 20) | 49/55, 36/61, 2/50 (changed between wk 12 and wk 24 visits) | not exactly, same pattern (cm.csv, C03CA) |
| Potassium > 5.5 on treatment, pbo/5/10/20/40 | 2/4/10/29/68 | 2/4/10/29/68 | yes (lb, all labs) |
| Hyperkalaemia AEs on treatment | 1/2/8/28/80 | 1/2/8/28/80 | yes (ae, by group id) |
| Stopped for good before wk 52 | 5/6/7/9/10 | 5/6/7/9/10 | yes (ex, sv) |
| Years on drug before wk 52 | 147.1/148.4/145.7/146.1/144.7 | same | yes (ex, sv) |

## Competing answers that survived
None on the call or on any ask. Forks tested and closed by a shipped rule or the data:
- Chronic-line start: weeks 12 or 16 give 40 mg (4.8 / 3.6), closed by linearity of the series from week 24 (data-identified, not filed). Start 20 gives 20 mg 3.24 / 40 mg 2.83, call same but 40 mg rounds to 3.
- Post-stop samples kept: 40 mg also rounds to 3 (tie), closed by the synopsis estimand.
- Disposition-form stops (46 total) against dosing records (37), closed by SAP interruption rule.
- Central-lab-only potassium (0/2/8/24/60) against all labs: the prompt and SAP say serum potassium on treatment with no central restriction. Judge treated this as closed; it is the thinnest closure among the asks.
- AE records against groups (2/3/9/30/96), closed by the dictionary. Visit day in or out of exposure, closed by "before" and the protocol.
Sensitivity risk: haemolysed samples excluded puts 5 mg on the 0/1 rounding edge (0.50); a week-20 start puts 40 mg at the 2/3 edge.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | csv, pdf, xlsx | yes |
| Large file | 25,000 rows or more | lb.csv 69,405 rows | yes |
| Distractors in metadata.json | 2 or more, none named in a file name | vs.csv, pc.csv (file names neutral) | yes |
| Distractors unused, relevant, ruled out | each | judge confirms unused by any graded figure; design note says neither ranks the doses; I did not test that each is relevant enough to weigh | partial, not independently verified |
| Deliverables | 1 to 3, all in golden | 2 (pdf, xlsx), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 5 arms by 4 measures plus 4 doses by month; units and rounding in the prompt | yes |
| Prompt shape and 25 or more criteria | identifiable, 25 or more | shape 11 (before and after with a control) per design note; rubric is generated later, count not checkable here | not verifiable here |
| Not LLM generated, goldens real | yes | judge: reads as a CRO SDTM extract; golden realism not re-read by me | yes on the bundle |

## Gate G reconciliation
Gate G: PASS. No shipped artifact ranks the doses on the 36-month question. The protocol's week-52 primary end point is the only surface ranking (it favours 10 mg), is stated as the trial's own question, and is not a declared distractor (the declared ones are vs.csv and pc.csv). The thread named no distractor as carrying the task. Mechanism label "forecasting" is the thread's own taxonomy; the card's objective is Experiment & Causal Analysis, so the label differs but the stump (series structure, one-off recovery inside a projected window) matches the note. Thread's stumping_family analytical_non_defect, surface_read_dependency no and sole_data_defect no all agree with the card (stump_class analytical) and the note's stump sentence (chronic phase from week 24 after the diuretic recovery, month-3 convention and week-52 reflex as the wrong routes).

## Gate H
Gate H: domain pass, layers pass, decisive_step analytical. Matches the card's analyst_test and domain_test and the note's Three rules: easy route (chronic phase from month 3 or week 12 files 40 mg; week-52 difference files 10 mg) yields a wrong answer after correct cleaning.

## Stump power (Gate F)
Good. Three easy routes each land on a wrong or tied answer (week-52 difference gives 10 mg; slope from week 12, 16 or all visits gives 40 mg; keeping post-stop samples ties 40 mg at 3). Stump needs seeing the diuretic-driven recovery in cm.csv and the linear tail.

## Findings, ranked
1. Low-medium: the chronic-line window is not filed in the prompt. It is data-identified (judge), and by CLAUDE.md the method may stay open when the data separate the candidates; the judge accepted it. A week-20 start leaves 40 mg at 2.83 (rounds to 3, tying the printed 20 mg figure), so the ask-2 integers for 40 mg are the most window-sensitive figure.
2. Low: submission step 4 counts loop-diuretic reductions at weeks 12, 16 or 20 as 50/55, 35/61, 1/50; the judge's closest definition gave 49/36/2. Not a graded figure, but a reviewer who recomputes it may not match. Align the wording or the definition.
3. Low: potassium is not restricted to the central laboratory in the prompt; the all-laboratory reading gives the golden, the central-only reading differs on every dose. Closed by SAP section 5 and the dictionary per the judge.
4. Low: 5 mg sits near the 0/1 rounding edge if haemolysed samples are excluded (0.50).
5. Judge optional note: asking only for the dose and the 20 mg figure would protect the 40 mg rounding; not required.

## Next action for the author
No send-back. Proceed to ship; optionally reword step 4's loop-diuretic counts in submission.md so they recompute exactly from cm.csv.

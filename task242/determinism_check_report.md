# determinism-check report, task242, 2026-10-17

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated sonnet thread (medium) saw only a fresh unzip of target.zip and the extracted blocks. It recomputed every load-bearing figure. The register (SERO-D1) fixes the estimand as infection from 1 January 2027 to the specimen's collection, and SOP-EPI-07 fixes the M rule (more than 1.5x or less than 2/3 of the published value). Run literally, the panel's sensitivity by days since onset, averaged over each zone's own 2027 onsets up to each collection, flags six zones. The six unflagged zones top out at 1.29x and the flagged zones start at 1.85x. Confirmed-only, de-duplicated notifications and 15-day step bins flag the same six. The asks (Breteau index, household response rate) reproduce, and the protocol and SOP wording close their forks.
Note: the thread's verdict.md was produced by a thread spawned by the main session, because my runtime has no Agent tool. The brief is /tmp/determinism-check-task242-1792279951/judge_brief.md.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Tested / reactive (results csv, bulletin Table 1) | 4,952 / 440, 12 zone values | same | yes |
| Panel sera / patients / controls | 557 / 216 / 300 (4 reactive, Sp 0.9867) | same | yes |
| Visit sensitivities | 0.133 ... 0.000 (11 visits) | same | yes |
| Line list 2027 resident cases | 35,166 (1,476 non-resident, 7,554 pre-2027 out) | same | yes |
| Effective Se by zone | e.g. 0.268, 0.232, 0.760, 0.457 | same | yes |
| Estimated shares and multiples (12 zones) | e.g. 17.0 (3.00x), 18.7 (2.02x), 15.9 (1.29x) | same | yes |
| Flag set | six zones | six zones | yes |
| Breteau index (12) | 15,544 forms, 123 repeats, 813 LOCKED, 13,250 houses; BI 10.6 to 24.8 | same | yes |
| Response rate (12) | 2,037 households, 1,564 responded; 73.8 to 80.4 | same | yes |

## Competing answers that survived
None that flips a committed answer. Closed or residual forks:
- Ignoring specificity (Sp=1) adds Kottaivayal at 1.68x. The SOP says "allowance for the test's misclassification" and the panel measures specificity, so the wording closes it.
- Response-rate numerator, specimen received versus result tested (74.0 to 79.2%). The protocol's "gave a blood specimen" closes it.
- Pooled Se (0.677) and peak Se (0.944) flag no zone. This is the intended wrong easy route, not an ambiguity: the estimand fixes timing and the panel is banded by days since onset.
- Estimand drift to "all onsets since Oct 2026" flags nine. This is excluded by the register's 1 January.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 19 | yes |
| Formats | 3 or more | 6 (csv, pdf, xlsx, docx, eml, md) | yes |
| Large file | 25,000 rows or more | line list 44,196 rows | yes |
| Distractors in metadata.json, none labelled in a file name | 2 or more | ncmc_rain_gauges_daily.csv, ncmc_fogging_log_2027.csv; neither name labels one | yes |
| Distractors unused yet weighable | unused, relevant, ruled out by a shipped fact | vector-control and rainfall context; neither enters any graded figure (the judge recomputed all of them without either file) | yes |
| Deliverables | 1 to 3, all in the golden | 2 (xlsx, pptx), both present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 12-zone grids; per cent to one decimal, BI to one decimal, stated in the prompt | yes |
| Prompt shape, 25 or more criteria | shape identifiable | shape 07, a 12-row grid by 5 measures plus the slide and the flagged set, more than 25 | yes |
| Not LLM-reading, goldens realistic | no tells | the judge saw no authoring disclosure; README.md is a tidy file listing (minor) | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: gate_g method_or_model_selection, stump_class analytical, no official, validated or filed decoy, decisive_rule_filed false. Match. The thread did not name either declared distractor (rain gauges, fogging log) as carrying the task. It named the vector SOP's CI/HI definitions as an "arguable" distractor, which is not a declared one and does not decide any figure. Gate G: PASS, no ranking artifact, and the difficulty survives deleting every wrong number.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical. This matches the card's analyst_test (pooled, 5-day or 5-to-60-day sensitivity flags no zone, where the golden flags six) and domain_test (an attack rate from a recent-infection marker's detection curve convolved with the zone's epidemic curve). It matches the design note's `## Three rules`. The thread's easy route (0.68 or 0.94 pooled/peak gives no flags) is the one the card declares; the thread's described figures differ by a few hundredths from the card's 0.708 and 0.868 variants but the note's route is the same.

## Stump power (Gate F)
Strong. Every single-sensitivity route (pooled 0.677, from day 5 0.708, kit window 0.868, peak 0.944) flags no zone. Median-day flags four, peak-day five, mean-day seven, a fixed 90-day window three, and the city's pooled curve nine. Only the zone-timed curve gives the six. The asks add independent cleaning work (ward renumbering, first inspection per house, last call per household).

## Findings, ranked
1. None blocking.
2. Minor: the Sp=1 fork (Kottaivayal at 1.68x) rests on the SOP wording alone. Consider a one-line closure in the fork table if one is not already there.
3. Minor: README.md is tidy; the thread would leave it.
4. No Gate G or Gate H mismatch.

## Next action for the author
Ship: proceed to stage 5 with target.zip as built, with no generator change and no re-judge.

# determinism-check report, task162, 2026-10-27

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting (method selection validated out of sample), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread: one general-purpose sonnet thread, medium effort, scratch /tmp/determinism-check-task162-r1/ (target.zip sha256 begins 62e91745404c). It reports it kept the order (literal_derivation.md written before graded_blocks.md was opened). Its literal derivation got the supplementary figures right and the main call wrong (6 triagers, about 700 items, position-in-cycle forecast); that is the intended easy route.

## Why
Every supplementary figure reproduces exactly from the bundle. The main call (8 triagers, about 900 items) is what a restart-wave model fitted on version_share_daily.csv, active_installs_daily.csv and the old export gives (about 875-910; ceil(/120) = 8 for any value from 841 to 960). The counting rules are filed in the runbook, working agreement and e-mail. The wave is data-native: the Windows share jumps about 24.5 points on the Wednesday after the second Tuesday every month. All three 2027 releases sit on that Tuesday.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Unique form reports in run | 1592 (implied) | 1592 = old CSV Archive/MOVED rows; 68 bridge replay copies excluded | yes |
| Security excluded / items | 59 / 1533 | 59 / 1533 (json security field = csv core-security) | yes |
| 2-8 Nov no-action / closed | 109 / 319 | 109 / 319 | yes |
| 9-15 Nov | 101 / 262 | 101 / 262 | yes |
| 16-22 Nov | 45 / 119 | 45 / 119 | yes |
| 23-29 Nov | 85 / 76 | 85 / 76 | yes |
| Groups by arrival component | 451/136/109/169/468/75/70/55 | same, sum 1533 | yes |
| Windows wave | Wed ~60%, Thu ~46% of pending, ~79% combined, ~12% ordinary day | consistent | yes |
| Max weekly reach in record | 48% | 47-48% | yes |
| First-use rate | 1.1 per 10,000 reaching | 1.08, r 0.98, RMSE 27 per week | yes |
| Release-week reach 2027 | about 75% | about 72-75% | yes |
| Busiest week forecast | about 900 | 875-910 | yes (within about 3%) |
| Triagers | 8 | 8 | yes |

## Competing answers that survived
1. Replay copies (68, closed Duplicate with a link to the original) are documented in no shipped file. Counting them under "duplicates included" adds 68 items to weeks 16-22 Nov. The report form wording, the old bug number on every copy and the 1592 Archive count all point against it. Residual risk low to moderate; the golden does not state the exclusion.
2. The 900 rounding: a lower release-week reach or no install growth gives 840-870, which could round to 800. The triager count stays 8 above 840. The margin on "900" is thin, about 3-4%.
3. "Patch Tuesday" appears in no file; it is recoverable from the share series, and every candidate rule gives 13 Jan, 10 Feb, 10 Mar.
None reaches a committed triager count. Items 1 and 2 touch graded figures (the replay copies the weekly cells, the rounding the 900).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 (the thread said 14; the zip lists 13) | yes |
| Formats | 3 or more | 6 (csv, docx, eml, json, pdf, xlsx) | yes |
| Large file | 25,000 rows or more | old tracker CSV, 29,275 rows | yes |
| Distractors in metadata.json | 2 or more, none labelled by file name | public_bug_statistics_monthly.csv, stability_monthly.csv; names carry no label | yes |
| Distractors unused yet weighable | yes | stability and public statistics answer their own questions; the dashboard's old basis (peak about 300, files 3) is ruled out by the runbook counting rule. The dashboard is not named in metadata | yes (see finding 3) |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, svg), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | weekly pair, 8 groups, whole numbers, nearest 100 stated | yes |
| Prompt shape and 25 or more criteria | identifiable, 25 or more | shape identified; about 2 + 8 + 8 + chart + 3 components, near 25; the generated rubric was not available to check | not verified |
| Reads as real work product | yes | thread saw no authoring language | yes |

## Gate G reconciliation
Thread: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card and note: gate_g forecasting, stump_strategy time_semantics, decisive_rule_filed false, official_decoy false, validated_decoy false, stump class analytical. These match. No distractor carries the task: the dashboard basis gives 3, the dropped Web-compat counting gives 5, the position-in-cycle forecast gives 6, and none is a shipped answer. Note the card's strategy label "time_semantics" sits oddly beside the note's analytical class. The thread's finding is that the decisive step is method choice under a regime shift, not a field reading.

## Gate H line
domain: pass; layers: pass; decisive_step: analytical. Thread: release-driven first-use reports and the OS patch cycle are software-release analysis, not a backdrop. Layer 1 is the bridge outage, replay copies, UTC vs Helsinki and the dashboard basis. Layer 2 is forecasting a regime the history only partly shows. The note's Three rules agree (decisive step: build adoption from ordinary restarts plus the Patch Tuesday burst; analyst test 6 vs 8, executed in checks.py R3a/R3b). The thread did not report that the golden is reached by applying a field standard with no judgment; the 2027 regime appears in no past week, so the model choice is a judgment the data must settle, validated on the 12 Oct and 9 Nov weeks.

## Stump power (Gate F)
Good. Position-in-cycle forecasting fits 13 of 15 releases and files about 700 / 6. Only the restart-wave model, checked on the two off-cycle releases, files 900 / 8. A solver who also misses the counting traps files 3 or 5. The restart model is the product-analytics diffusion method and a strong solver may reach it, but the 2027 regime has no record, so the route has to be reasoned out. The main thread should weigh this against the ladder.

## Findings, ranked
1. Low to moderate: the 68 replay copies are undocumented in shipped text (fork 1). The weekly 16-22 Nov cells hold only through the old-bug-number reading. The thread suggests noting the exclusion in the write-up.
2. Low: 900 sits about 3-4% from the 800/900 boundary; the triager count is robust.
3. Low: triage_dashboard_weekly.xlsx is a wrong-basis artifact not named in metadata.json distractors. It ranks nothing and the runbook rules it out, but the declared list and the shipped set differ.
4. Info: the 25-criteria rubric count was not verified.

## Next action for the author
Approve; optionally add one sentence to submission.md step 1 saying bridge replay copies (closed Duplicate, old bug number repeated) are excluded, so 1592 is not read as a miscount.

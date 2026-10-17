# determinism-check report, task234, 2026-10-17

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW (one dictionary pin; no change to the call, ladder or graded figures)
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
FCP-2 files completeness against the week's aggregate, which does not exist on escalation day, so the denominator must be estimated. The 224-week history separates the candidate estimators in a rolling backtest (mean abs log error 0.039 for the positivity-aware volume model, 0.064 for last week's report; 0.074 vs 0.177 in epidemic weeks). Every positivity-aware variant (positivity only, no holiday exclusion, last 52 or 26 weeks) escalates exactly Wexmoor and Westmarch, six streams at 0.53 to 0.66, with the other 23 at 0.87 or more. One fork sits in supplementary ask 2 only: the dictionary says `received` is UTC, but the golden needs county time before the 19 Jan 2027 06:00 migration.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Week-3 tests collapsed | 80,671 | 80,671 | yes |
| Wexmoor / Westmarch week-3 tests | 3128/607/1234, 1943/621/1454 | same | yes |
| Positivity | 33.1/7.9/9.6, 23.3/9.0/17.0 | same | yes |
| Predicted tests | 5732/1061/2216, 3521/1103/2381 | exact | yes |
| Completeness | 55/57/56, 55/56/61; others 87+ | 0.546/0.572/0.557, 0.552/0.563/0.611; min other 0.873 | yes |
| Week-2 completeness, 29 values | 93.8 to 98.0 | all 29 | yes, only under the county-time reading of `received` |
| Specimens, 10 labs | 2,835 to 9,204 | all 10 (patient + collection time) | yes |

## Competing answers that survived
1. `received` read as UTC, as DATA_DICTIONARY.md says: week-2 completeness is 99.1 to 99.7 for every stream. The golden needs pre-migration `received` in county time; the data force it (received precedes released by about 5.9 h on 124,890 messages, and the offset vanishes after the migration), but a word-for-word reader of the dictionary does not get it. Closing rule: reword the dictionary so it does not assert UTC for the whole file, without naming the switch. Affects ask 2 only.
2. Specimen key, patient plus collection date: gives 2848/6799/4043/5435/4404/9178/9052/7197/4200/2825. FCP-2 section 6 and the timestamped column favour the golden. Low risk; optionally say "same collection time" in ask 3.
The estimator fork on the main call is closed by the files (backtest), not open.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 11 | yes |
| Formats | 3+ | 4 (csv, pdf, xlsx, md) | yes |
| Large file | 25,000+ rows | 217,357 rows | yes |
| Distractors | 2+ named in metadata.json, none labelled by file name | 3 (ED ILI, state positivity, county admissions), none labelled, none used | yes |
| Distractor weight | relevant, ruled out by a shipped fact | judge found them unused; I did not independently test that they reproduce a graded quantity | partial, see findings |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 29 marks, 29 week-2 percentages (one decimal), 10 specimen counts | yes |
| Prompt shape | identifiable, 25+ criteria | shape 07 grid, 68 graded cells plus the call | yes |
| Reads as real | no LLM tells | judge saw none; README is a plain index; goldens not re-read by me | yes (judge) |

## Gate G reconciliation
Thread: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_class analytical. The analyst_test (last week's aggregate gives 15 escalations, 9 cells wrong) matches the thread's easy route exactly (15 streams, 9 complete). Gate G is a pass, with no ranking artifact and no distractor carrying the task. No mismatch.

## Stump power (Gate F)
Good. The prompt's "now that the week 2 aggregate reports are in" tempts the last-week denominator, which over-escalates 15 streams. The seasonal baseline and peer-change routes also file wrong sets. The volume-positivity link is visible in the history, so a strong model could still find it.

Gate H: domain pass, layers pass, decisive_step analytical (estimating the unreported week's tests from its own positivity, validated against history). It matches the card's domain_test.

## Findings, ranked
1. DATA_DICTIONARY.md line for `received` ("time the platform received the message, UTC") contradicts the data and makes ask 2 depend on an unfiled convention (FIX_NOW).
2. Specimen key wording (patient plus collection date against time) is a minor fork in ask 3.
3. Rule 3 watch: the HOW (positivity model) is not filed, only the WHAT, which is correct. The fix must not file the model.

## Next action for the author
Reword the `received` row in target/DATA_DICTIONARY.md so it does not state UTC for the whole column, for example "time the platform received the message, in the receiving system's clock", without naming the migration. Optionally add "same collection time" to ask 3. Rebuild the generator, confirm byte-identical zips, and re-judge once.


---

# Round 2 (after the FIX_NOW), 2026-10-17

Scratch: /tmp/determinism-check-task234-r2/ (fresh unzip of the rebuilt target.zip; verdict at /tmp/determinism-check-task234-r2/verdict.md). One thread, literal reading first. The spawn was made by the main session because this runtime has no Agent tool.

## Verdict
NOT_DETERMINISTIC (underspecified_objective)
**Disposition:** SEND_BACK (borderline: the margin is wide and the data favours the golden's estimator family; the fault is that no filed text directs the solver to it)
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no
**Gate G:** pass. **Gate H:** pass (domain pass, layers pass, decisive_step analytical).

## Why
The round-1 fix worked: the `received` fork is closed (stamps as written against 08:00 county give the golden's 29 week-2 values; the six-hour offset in the data and the dated migration in the change log close it). The specimen key (patient plus collection time) is held forced by FCP-2 section 6. What remains is the main call. FCP-2 sections 3 and 4 name only the week's aggregate report as the denominator, and that report does not exist for week 3. The golden's estimator (log tests on the week's positivity and a trend, premise that lost messages drop positives and negatives alike) is in no shipped text, and no selection criterion (no filed back-test, no governing standard) tells a solver to choose it. A literal reader using the only denominator on file (week 2) escalates 15 streams, fully reproducible. Round 1 judged the same fork closed by the data (a back-test separates the candidates); round 2 judges the data leans the same way (MAE 2.9 per cent against 5.7 per cent over 52 weeks) but that nothing directs a solver to run it. Under the project's rule that the method stays open only where the design, a standard or a filed selection criterion forces it, round 2's reading stands: the criterion is not filed. Gate C fails for the main call, ask item 1 (marks) and item 4 (chart); items 2 and 3 are forced.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Week-3 tests collapsed | 80,671 | 80,671 | yes |
| Wexmoor / Westmarch week-3 tests | 3128/607/1234, 1943/621/1454 | same | yes |
| Positivity | 33.1/7.9/9.6, 23.3/9.0/17.0 | same | yes |
| Predicted tests | 5732/1061/2216, 3521/1103/2381 | 5732.2/1061.5/2216.4/3520.7/1103.5/2380.9 | yes |
| Completeness | 55/57/56, 55/56/61; others 87+ | 54.6/57.2/55.7, 55.2/56.3/61.1; min other 87.3 | yes |
| Week-2 completeness, 29 values | 93.8 to 98.0 | all match to one decimal | yes |
| Specimens, 10 labs | 2,835 to 9,204 | all 10 | yes |

## Competing answers that survived
1. Week-3 denominator = week-2 report of record (the only denominator FCP-2 s.3 names that is on file): 15 streams escalated. Closing rule missing: no filed criterion makes the positivity-conditioned estimate the week's denominator.
2. Week-2 tests times the mean 2023 to 2026 week-3 over week-2 ratio: 14 streams (L03 flu 62.3, L10 flu 79.9).
3. Time trend alone: a different set (L03 RSV 75.7 and SARS-CoV-2 67.8, L10 RSV 80.0 borderline, L10 flu 129).
Within the positivity family every specification gives the same six streams (all weeks, no trend, last 104, last 52, linear form).

## Spec gates (checked by me against the unzipped bundle, metadata.json and golden/)
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 11 | yes |
| Formats | 3+ | 4 (csv, pdf, xlsx, md) | yes |
| Large file | 25,000+ rows | 217,357 | yes |
| Distractors | 2+ named, none by file name | 3 named in metadata.json (ED ILI, state positivity, county admissions), unused | yes |
| Distractor weight | relevant, ruled out by a shipped fact | not independently tested by me | partial |
| Deliverables | 1 to 3, all in golden | 2 (xlsx with four sheets, png) | yes |
| Asks | multi-dimensional, unit and rounding | 29 marks, 29 week-2 percentages, 10 specimen counts | yes |
| Prompt shape and rubric | shape found, 25+ criteria | shape 07 grid, about 69 graded cells | yes |
| Reads as real | no LLM tells | judge saw none; goldens not re-read by me | yes (judge) |

## Gate G reconciliation
Thread: forecasting, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Matches the card (stump_class analytical) and the design note's strategy (forecast_method_backtest, with the clean-truth analyst test of 15 escalations, 9 wrong cells), which is exactly the thread's easy route. No distractor carries the task. Gate H (domain pass, layers pass, decisive step analytical) matches the card's domain_test. The one divergence from the design note: it treats the back-test as separating the candidates, but the back-test is nowhere filed for the solver, which is the send-back reason.

## Stump power (Gate F)
Strong. Last week's aggregate (or a seasonal ratio) files 14 to 15 streams, nine of them complete streams whose epidemic moved in the week; the positivity-conditioned estimate files the six.

## Findings, ranked
1. Open estimator fork on the main call: no filed selection criterion or premise for the week-3 denominator (send-back).
2. Fix constraint (Rule 3): file the WHAT or a selection criterion, not the HOW. Acceptable: a protocol sentence that the week's denominator is the laboratory's tests for that week given the week's own positivity, or a filed back-test criterion (lowest one-step-ahead error on the aggregate history over a stated window), plus the premise that lost messages do not change positivity. Do not file the regression. A filed back-test is a recognisable organ and must not follow in consecutive builds. Filing the positivity-conditioned denominator outright risks turning the decisive step into rule application, so the back-test route is preferred.
3. The round-1 findings (received row, specimen key) are closed.

## Next action for the author
Add to FCP-2 (or the prompt) a filed selection criterion for the week-3 denominator (a stated one-step-ahead back-test on the aggregate history, with window and error measure) together with the missing-at-random premise, regenerate, keep every graded figure unchanged, and re-judge. This is a design-level change, so /fix-determinism's frozen-stump constraint should be checked first.

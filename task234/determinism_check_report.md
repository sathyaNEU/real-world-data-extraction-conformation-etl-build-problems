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


---

# Architecture 2, round 1, 2026-10-17

Scratch: /tmp/determinism-check-task234-a2r1/ (judged unzip in target/, current shipped zip in new/, verdict at /tmp/determinism-check-task234-a2r1/verdict.md). One thread, literal reading first, spawned by the main session from judge_brief.md (this runtime has no Agent tool).

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
FCP-2 s.2 pins the test and the week, s.3 the ratio and its denominator (the aggregate report's tests), s.5 the choice of the week's tests estimate (the way whose largest week-2 miss is smallest). The judge back-tested about 40 estimators on week 2. Every positivity-conditioned variant (Poisson or log-OLS, with or without trend, holiday exclusion, 26/52/full window) escalates exactly Wexmoor and Westmarch, six streams at 54.7 to 60.8 per cent, the other 23 at 87.4 or more. Non-positivity ways miss by 54 to 73 per cent and escalate 0 to 15 streams. All 68 graded cells reproduced. Architecture 1's open fork (no filed check) is closed by s.5; the round-1/2 findings (received clock, specimen key) are closed by the change log row and s.6.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Me, on shipped zip | Reproduced |
|---|---|---|---|---|
| Week-3 tests collapsed | 80,671, 29 streams | 80,671 | 80,671, 29 | yes |
| Wexmoor / Westmarch week-3 tests | 3128/607/1234, 1943/621/1454 | same | same | yes |
| Positivity | 33.1/7.9/9.6, 23.3/9.0/17.0 | same | same | yes |
| Predicted tests | 5714/1064/2219, 3514/1102/2391 | same | same | yes |
| Completeness | 55/57/56, 55/56/61; others 87+ | 54.7/57.1/55.6, 55.3/56.3/60.8; min other 87.4 (Bluestem RSV) | same | yes |
| Week-2 largest miss: model / held / last week | 7.8 / 52.6 / 54.0 | same | 7.78 / 52.62 / 53.99 | yes |
| Last week's report as estimate | 15 streams escalated | 15 | 15 | yes |
| Week-2 completeness, 29 values | 47.4 (Brandmoor RSV) to 98.0 | all match | all 29 match to 0.1 | yes |
| Specimens, 10 laboratories | 2,850 ... 9,204 ... 2,835 | all match | all match | yes |

## Competing answers that survived
None on the call. Residuals, none moving a graded figure:
- Ask 2 clock: `received` is county time before the 19 Jan 2027 06:00 hub migration and UTC after. The data dictionary says only "as the state hub's message broker stamped it"; the change log gives the migration and the data force the reading (pre-migration `received` precedes `released` by 5.75 to 6.0 hours). Read as UTC, nine laboratories sit near 99 and Brandmoor near 50 to 52, a different grid. The judge calls it forced by data; it is the one place a reading is inferred, not stated, and it sits in ask 2 only.
- Specimens by collection week instead of test week (Westmarch 2,333 against 2,835): s.2 and s.6 make test week the literal reading.
- Ellery RSV 97.498 rounds to 97.5 only if the protocol's county date, first release and first received are applied literally.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files, formats, large file | 10+, 3+, 25,000+ rows | 11 files; csv, md, pdf, xlsx; result extract 211,361 rows | yes |
| Distractors | 2+ named in metadata.json, no file name labels one | 3 named (ED ILI, state positivity, county admissions); names are plain; none counts a laboratory's tests or flags a stream | yes |
| Distractors unused yet weighable | yes | all three are relevant surveillance series; judge found none needed | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 29 escalation marks, 29 week-2 percentages (one decimal in prompt), 10 specimen counts (count of specimens) | yes |
| Prompt shape, rubric | shape identifiable, 25+ criteria | shape 07 grid, 68 graded cells plus the call and chart | yes |
| Prompt | one paragraph, question first, under 1,000 characters | 640 characters | yes |
| Reads as real | no LLM tells, real work product | judge saw none; README a plain index; goldens not re-read by me | yes (judge) |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical, layer 2 forecast_uncertainty (tests predicted from the stream's own positivity), stump sentence the past-report default ending on 15 streams, 9 wrong; analyst_test and domain_test as the thread found them. Match. The thread names no declared distractor as the surface read carrying the task: the carrier is last week's aggregate report (an input, not a ranking of the candidates), and the three distractors are unused. Gate G holds: no shipped artifact estimates, flags or ranks a stream.
Gate H line: domain: pass, layers: pass, decisive_step: analytical (estimating expected tests from received positivity, validated by the s.5 week-2 back-test). Agrees with the card and the note's `## Three rules` (No decoy, Not semantics, Not rule application).

## Stump power (Gate F)
Good. The easy route (last week's report, the only report in hand) escalates 15 streams and flags 9 complete streams; the seasonal baseline and other-laboratories' change are also wrong; the rest of the grid and the week-2 and specimen asks reward the same careful handling.

## Findings, ranked
1. Bundle drift (process, not a determinism finding). The judged unzip was cut before the coordinator's cancelled-order change; the shipped target.zip (elr extract 30,832,585 bytes, 211,361 rows, matching metadata.json) differs from the judged one in more than the cancelled rows: accessions are renumbered after the cancelled orders took sequence numbers, and lab_weekly_aggregate_reports.csv, ed_syndromic_ili_weekly.csv, county_respiratory_admissions_weekly.csv and state_respiratory_positivity_by_region.csv are not byte-identical to the judged copies (6,485 of 6,638 report rows differ in `tests`, submission dates also differ). The note that reports were unchanged is therefore not true at the byte level. I reran the whole golden pipeline on the shipped zip (table above) and every graded figure, the 7.8 / 52.6 / 54.0 back-test and the 15-stream failure reproduce, so the verdict carries to the shipped bundle. The verdict rests on the judge's thread for the judged bundle and my own recompute for the shipped one, not a second isolated thread.
2. Ask 2 clock reading inferred from data (low; above).
3. Specimen-week wording (low; above).

## Next action for the author
None required to ship. Optionally, if the byte differences in the four context files were not intended, confirm they are only seeded noise draws shifting with the new accession sequence; no graded figure moved.

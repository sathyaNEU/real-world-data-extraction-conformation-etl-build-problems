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

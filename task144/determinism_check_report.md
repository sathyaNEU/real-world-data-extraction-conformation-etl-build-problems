# determinism-check report, task144, 2026-10-27 (architecture 2, /build stage 4)

## Verdict
DETERMINISTIC, plus SOLUTION_WRONG on one stated statistic only (the back-test RMSE pair in section 1 and step 7 of submission.md; the call and every graded figure reproduce).
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection (forecast validated out of sample), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Executed literally, the memo (external star = first star by a non-bot, non-member account, UTC day, day 1 = made-public day, 90-day window, unseen stars counted) supports one model on the shipped lottery: a no-spotlight baseline from the runners-up plus newsletter stars times a follower-view cascade at the rate after the launch week. Kilnkit leads (about 12,100 against 9,900 to 10,000 for slidewell and tracewire), and the lead holds for every exposure-window start of day 5 or later and for linear and fitted-cascade variants (11.5k to 11.7k). The two wrong routes (whole-life rate gives slidewell about 14,300; mean lift gives tracewire) are separated by the shipped back-test. The filed RMSE pair "300 / 1,110" does not reproduce.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| External stars by 27 Sep (kilnkit, slidewell, tracewire) | 1,523; 4,175; 4,534 | same; all 7 and all 21 drawn repos equal the daily file | yes |
| Newsletter stars per subscriber x October list | 0.71% x 433,812, about 3,000 | 0.711% -> 3,085 | yes |
| Mean followers, newsletter / feed starrers | 85 / 10 | 84.9 / 10.1 | yes |
| Day-8 feed rate kilnkit / slidewell / tracewire | 1.8% / 0.7% / 0.1% | 1.82% (356/19,548) / 0.74% / 0.117% | yes |
| Whole-life slidewell rate | 2.0% | 1.98% | yes |
| No-spotlight day 90 | 3,000 / 5,000 / 7,000 | 3,158 / 4,756 / 6,527 (median-ratio tracewire 6,495) | yes at the filed rounding, tracewire pooled-ratio only |
| Totals if spotlighted, all seven | 12k, 10k, 10k, 8k, 8k, 7k, 6k | 12,083; 9,950; 9,923; 8,187; 8,070; 6,923; 5,874 | yes |
| Kilnkit added | 9,000 | 8,925 (8.4k to 8.6k under linear or fitted lift) | yes under the filed cascade |
| Back-test RMSE day-8 rate | 300 | 317 | NO (about 320) |
| Back-test RMSE whole-life rate | 1,110 | 1,241 (design note says 1,115) | NO |
| Mean-lift RMSE (design note) | 1,321 | about 1,320 | yes |
| Ask 3 delivered / click share, Apr to Sep | 391,299 ... 429,949; 1.49, 1.52, 1.53, 1.52, 1.44, 1.49% | identical | yes |
| Ask 4 nominators and outside shares | 27/58/47/31/37/26/19; 81.48, 91.49, 90.32, 81.08, 88.46% | identical | yes |
| Chart stars to date | 2k/4k/5k/2k/2k/2k/1k | reproduce (PNG not in the thread's bundle, not reviewed) | yes |

## Competing answers that survived
None on the call. Slidewell (whole-life rate, or exposure start day 1 to 3) and tracewire (mean lift) both fail the shipped back-test, which falls from RMSE 1,241 at day 1 to 495 at day 4 and 382 at day 5, so the data select a start of day 5 or later. Residual non-pick forks: (a) kilnkit "added" 9k vs 8k under other lift models (total 12k stable); (b) tracewire baseline 7k only under the pooled ratio (median-ratio gives 6k), which moves only the chart split; (c) the ask 3 denominator rests on the Thursday send being a resend (supported by the files: sum of sends exceeds the log list size, 0 hard bounces on Thursday, small clicker overlap).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 17 | yes |
| Formats | 3 or more | 5 (csv, json, parquet, pdf, xlsx) | yes |
| Large file | 25,000 rows or database | events 61,929 and 93,450 rows, accounts 110,790, relaymark about 110k | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | repository_traffic, trending_daily named; neither answers a graded quantity (judge: present and unused) | yes |
| Distractors weigh and are ruled out by a shipped fact | required | judge found them present and unused; the ruling-out fact was not separately probed | partly unverified |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | seven totals; six issues x two measures; seven nominators; units and rounding in the prompt | yes |
| Rubric | prompt shape identifiable, 25 or more criteria | shape "other" (pick, seven totals, chart, two tables); about 5 + 7 + 12 + 14 + 7 gradable figures; count not generated at this stage | yes (by figure count) |
| Not LLM generated / goldens realistic | required | judge: no authoring disclosures, coherent dates; golden-realism passed upstream | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: the stump is the forecast_uncertainty rate window, whole-life vs day-8 rate, validated on the lottery's 19 closed spotlights. Match. The declared distractors (traffic, trending) are not named by the thread as carrying the task, so they are not too load-bearing.
Gate H line from the thread: domain pass, layers pass, decisive_step analytical. Matches the note's Three rules. One caution: the memo files no feed or window sentence, which is what keeps the decisive step out of rule application, and the thread agrees no sentence closes it. The "RMSE 300 vs 1,110" in the filed answer (design note says 1,115) is the only claim that disagrees with the thread's recompute.

## Stump power (Gate F)
Moderate. The whole-life rate (slidewell about 14k) and the flat mean lift (tracewire) are the two easy wrong routes. A solver who excludes the launch burst, or regresses lift on exposure rate, reaches kilnkit by several routes, so many strong solvers may still land the call; the graded decimals, the "added" 9,000 and asks 3 and 4 carry the rest. The main thread should weigh this with the scored readers' result.

## Findings, ranked
1. FIX_NOW, solution text: back-test RMSE "300 / 1,110" (submission.md section 1, step 7; design note 300 / 1,115 / 1,321) reproduces as about 317 / 1,241 / 1,320. Same ordering, ratio about 4. Restate as "about 320 against about 1,240" or regenerate from the final script, and align the design note and any checks.py assertion.
2. Optional, prompt: pin ask 3 with "counting each subscriber once". It changes what solvers read, so weigh it against the rest; the denominator already resolves to one computable value.
3. Note: "added 9,000" and tracewire's 7,000 baseline depend on the pooled-ratio, filed-cascade choice; neither moves the pick or any of the seven totals.

## Next action for the author
Correct the RMSE pair in submission.md (section 1 and step 7) and the design note to the recomputed values, rerun checks.py, then proceed. No change to target/ or the goldens is needed for that fix, so no rebuild or re-judge of the data is required.

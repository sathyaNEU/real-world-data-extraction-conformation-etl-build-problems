# determinism-check report, task259, loop 1, 2026-10-13

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated sonnet thread (Bash only, fresh unzip at /tmp/determinism-check-task259-loop1/target/) executed the policy (4.2 to 4.4) literally and reproduced every golden figure. The only silent point is the rate that carries a report to the 1 October 2026 benchmark date. Only the employer-and-level fixed-effects slope (2.70 per cent a year, SE 0.17) measures what a job and level commands at constant composition, and the data separate it from the alternatives. Rounded midpoints are stable across log or simple compounding, 2.70 or 2.74 per cent, and every quantile interpolation method. The thread's source: /tmp/determinism-check-task259-loop1/verdict.md.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Matched respondents DE I to IV | 788 / 1,234 / 1,366 / 844 | 788 / 1,234 / 1,366 / 844 (extract + profiles + crosswalk + architecture xlsx) | yes |
| Within-employer slope | 2.7% a year | 0.02701 log (2.74% simple); same by level (0.0269 to 0.0271) | yes |
| Midpoints I to IV | 119k / 145k / 170k / 204k | 118.9-119.0k / 144.9-145.1k / 169.8-170.05k / 203.8-204.0k | yes |
| DE III P25 / P75 | 158k / 183k | 157.9k / 182.9k | yes |
| Employed by level x zone (159) | 19/6/5, 29/12/10, 27/14/14, 14/6/3 | identical (hris + pay_zones) | yes |
| Open requisitions (19) | 3 / 5 / 8 / 3 | identical (ats) | yes |

## Competing answers that survived
None on the main call. Tested and failed: no carry (164k), cross-section slope 1.77% (168k), re-reporters' growth about 4.7 to 5.1% (175k to 176k), Tallyband normalised level or current crosswalk (fails 4.2, Quarry Systems), stale recorded pay_zone column (4 cells differ; readme says recorded when written), postings instead of requisitions (10/7/19/4).
Residual low-risk fork on ask 3 only: "employed" excluding workers on leave gives 147 against 159. Leave is a job state in the hris readme, not a separation, so the golden reading is natural; optional one-clause closure in the prompt or an ask line if the author wants zero risk. It does not touch the main recommendation.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | yes |
| Formats | 3 or more | 4 (csv, md, pdf, xlsx) | yes |
| Large file | 25,000 rows or more | tallyband_extract 35,851 rows | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | tallyband_offers_extract, oews_database_architects; neither name says distractor; unused by the solution | yes |
| Distractor weighs but ruled out | relevant, reproduces, ruled out by a shipped fact | thread found both unused; offers extract and OEWS are not on any graded path; OEWS margins are not the population per policy 4.2 | yes (not independently probed beyond the thread) |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, svg), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | midpoints x 4 levels, percentiles, level x zone grid, requisitions by level; the prompt states "nearest thousand dollars" for pay, counts are integers | yes |
| Prompt shape and rubric | identifiable shape, 25 or more criteria | shape 07 grid; design note counts about 12 cells, the call, 4 matched counts, plus the ask figures; the rubric is generated and I did not count it | not verified |
| Reads as real | no LLM tells, goldens real | thread found no authoring or solver-facing language; golden realism not re-read by me | yes per thread |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: strategy grain_or_unit for the first move, composition_mix noted for the second; analyst test ends on $175,000 against golden $170,000; stump class analytical; metadata declares the two distractors. Thread names no distractor as carrying the task. Match: no send-back signal. Minor wording difference: the thread's cross-section alternative is 1.77% giving 168k (no controls), while the design note's pooled 1.1% giving 166k is the level-controlled pooled slope; the thread also saw 1.07% with level control only. Both are alternatives that miss 170k, so the reconciliation holds.
Gate G line: no shipped artifact ranks the candidates wrongly; difficulty survives deleting the wrong numbers (no wrong number is shipped); declared distractors unused.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical. This matches the design note's Three rules (domain test: survey ageing at a fixed level within matched employers, as the ECI and salary-survey practice; no decoy; not semantics; not rule application).

## Stump power (Gate F)
Good. The data do not announce the carry rate. The previous_ columns are the attractive wrong source (175k), the pooled slope gives 166k or 168k, no carry gives 164k, and a strong analyst who cleans correctly can land on any of these. Asks 3 and 4 add dated-zone, future-dated, leave and posting devices that separate careless runs.

## Findings, ranked
1. None blocking.
2. Low: ask 3 "employed" does not say workers on leave count (147 against 159).
3. Info: rubric criteria count (25 or more) not verified by me.

## Next action for the author
Proceed to stage 5 ship. Optionally close the leave reading in ask 3 with a few words; no regeneration is needed otherwise.

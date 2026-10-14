# determinism-check report, task230, 2026-10-14 (pass 1)

Pass 1 judged the build as first rebuilt (prompt asked "hours ... it logged that month" and "households they enumerated at those calls"). Bundle judged: /tmp/determinism-check-task230-024732/target/. Verdict file: /tmp/determinism-check-task230-024732/verdict.md.

## Verdict
NOT_DETERMINISTIC (main recommendation DETERMINISTIC and reproduced; two supplementary asks open)
**Disposition:** SEND_BACK
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The main call is forced: the judge rebuilt the 24, 25, 35, 41, 71, 93 list and all 40 biases from the bundle. Governing label underspecified_objective on two supplementary asks:
1. Ask 3 hours "it logged that month": timesheets carry work_date (shift start) and entered_on; six correction lines are entered 1 to 8 days after the shift. Golden uses shift month with corrections netted (295.75 / 274.25 / 280.00 / 229.50 / 201.25); month entered gives 312.00 / 276.00 / 278.75 / 246.50 / 224.50. Both readings licensed.
2. Ask 4 households "enumerated at those calls": golden counts outcome 10 and 20 calls, so a household interviewed by proxy then by a member in September is counted twice (field manual 5.5 withdraws the proxy questionnaire). Once-each gives 10,697 / 5,662 / 5,014 / 5,358 / 4,525 / 4,735 / 4,529 / 3,975; every region moves 4 to 17.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Coded by route (online, paper, member, proxy), extract + register | 321,660 / 122,864 / 71,258 / 15,330 | same | yes |
| Still to code by route | 3,344 / 1,925 / 44,986 / 53,112 | same | yes |
| Release population | 634,479 | 634,479 (register occupation_writeins) | yes |
| Biases 24, 25, 35, 41, 71, 93 | -3.1, -2.5, +4.6, +3.2, -2.3, +6.9 | -3.08, -2.51, +4.63, +3.20, -2.27, +6.88; next largest 72 at -1.09; all 40 match | yes |
| Competing lists (coded-so-far, pooled follow-up, 0.90 score) | 35+93; 24,35,41,93; 24,35,71,93 | same | yes |
| Team write-ins, October | 4,160 / 3,746 / 4,206 / 3,112 / 2,825 | same (shift-date assignment gives the same) | yes |
| Team hours, OCC, shift in October | 295.75 / 274.25 / 280.00 / 229.50 / 201.25 | same under work_date; differs under entered_on | yes, fork |
| Region calls, September | 20,016 / 10,468 / 9,289 / 10,084 / 8,380 / 8,867 / 8,438 / 7,435 | same | yes |
| Region households (outcome 10/20 calls) | 10,714 / 5,666 / 5,020 / 5,365 / 4,531 / 4,744 / 4,534 / 3,983 | same as calls only; once-each differs | calls only, fork |

## Competing answers that survived
- Ask 3: shift-month vs month-entered hours, all five teams move (the prompt and files do not pick). Closing rule: none shipped.
- Ask 4: households as completed-interview calls vs distinct households, every region moves. Closing rule: none shipped.
- Main call: none. Remaining judgment: the route split of the follow-up study (study has batch_type only); the judge counted it as forced because the data separates candidates (backlog 54% proxy vs 17% coded). Margin is thin-but-clean: 25 and 71 sit about 1.4 sd from the line (bootstrap sd 0.36 and 0.28); OQ-4 4.1 tests the unrounded bias with no significance step.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 17 | yes |
| Formats | 3+ | 5 (csv, parquet, pdf, xlsx, docx) | yes |
| Large file | 25,000+ rows | register 541,954; visit log 483,295; study 101,948; extract 531,112 | yes |
| Distractors | 2+ in metadata.json, none named in a file | lfs_2026q3_employment_by_occupation.csv, census2021_occupation_by_region.csv; names carry no label | yes |
| Distractors weigh, unused, ruled out | yes | other sources' levels, not an answer to a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | multi-cut, but ask 3 hours and ask 4 households not determinate as worded; rounding stated | no (asks 3, 4) |
| Prompt shape, rubric 25+ | yes | shape 10 scorecard; 40 biases + call + 10 + 16 figures + chart, well over 25 | yes |
| Not LLM-generated; goldens real work products | yes | judge found system-export mess (tablet re-sends, reused coder ids, correction lines), no authoring language | yes |

## Gate G reconciliation
Judge: mechanism decomposition_attribution (stratified projection of the backlog by route), family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical, Gate G `forecasting` (layer 2 `forecast_uncertainty`), strategy maturity_censoring, decisive step route-by-route build under the 0.80 rule. Same stump in different vocabulary; no contradiction on what decides the call. The declared distractors (LFS Q3, census 2021) are not named as the surface read. Finding: the processing plan's pooled "Clerical share" sheet reads to the judge as a pooled-rate decoy, while the note says the plan answers capacity only and no decoy exists; it was not used as the answer and no shipped artifact ranks the groups, so Gate G is held.
Gate H line: domain: pass, layers: pass, decisive_step: analytical. Caveat from the judge: the route stratification is not a stated rule (consistent with the design: method open, data separates the candidates).

## Stump power (Gate F)
Probable. Easy routes (coded-so-far bias warns 35 and 93; follow-up batches pooled warns 24, 35, 41, 93; the 0.90 score leaves 25 and 41 inside) each file a plausible wrong list.

## Findings, ranked
1. Ask 3 hours: month of shift vs month entered (open fork, SEND_BACK).
2. Ask 4 households: per call vs distinct household (open fork).
3. Thin margin on groups 25 and 71 (not a fork; the filed rule tests the unrounded value).
4. Pooled "Clerical share" sheet in the processing plan reads as a decoy against the note's no-decoy line.

## Next action for the author
Pin ask 3 and ask 4 in prompt.txt (WHAT, not HOW) and regenerate only those golden figures; main call, files and stump stay frozen. Then one re-judge (pass 2).

---

# determinism-check report, task230, 2026-10-14 (pass 2)

Pass 2 judged the rebuilt bundle (asks now "hours it spent on occupation coding that month" and "calls that made no contact"). Scratch: /tmp/determinism-check-task230-p2-030126/. Verdict file: /tmp/determinism-check-task230-p2-030126/verdict.md. Before the thread ran, the bundle was refreshed with a fresh unzip of the cut at sha256 0a14c05b95af1e81d52a3359dfcceef5a39678cac656d0826df6436574dec508; prompt and submission were unchanged, so the brief stood.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting (with method_or_model_selection; etl_conformance on the asks), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The warned set 24, 25, 35, 41, 71, 93 reproduces from OQ-4 3.1, 3.3 and 4.1, field manual 5.3 and 5.5, the processing-plan Decision (0.80 from 16 November) and the study's selection intervals. Both pass 1 forks are closed: hours are pinned to the occupation-coding hours of shifts in the month, and the second region figure is no-contact calls, which has no household double count. Every supplementary figure recomputes exactly.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Coded by route | 321,660 / 122,864 / 71,258 / 15,330 | same | yes |
| Still to code | 3,344 / 1,925 / 44,986 / 53,112; population 634,479 | same | yes |
| Biases 24, 25, 35, 41, 71, 93 | -3.1, -2.5, +4.6, +3.2, -2.3, +6.9 | -3.08, -2.51, +4.63, +3.20, -2.27, +6.88; nearest others 72 -1.09, 26 -1.07; all 40 match | yes |
| Difference estimator cross-check | same set | -3.09, -2.48, +4.65, +3.20, -2.25, +6.89 | yes |
| October write-ins by team | 4,160 / 3,746 / 4,206 / 3,112 / 2,680 | same | yes |
| October OCC hours, shift-start month, corrections netted | 295.75 / 270.75 / 283.00 / 229.50 / 176.00 | same | yes |
| September calls by region | 20,016 / 10,468 / 9,289 / 10,084 / 8,380 / 8,867 / 8,438 / 7,435 | same | yes |
| September no-contact calls | 8,208 / 4,215 / 3,798 / 4,163 / 3,367 / 3,611 / 3,471 / 3,055 | same | yes |

## Competing answers that survived
None on the main call or the asks. Competing lists excluded by filed text or data: coded-so-far bias {35, 93} (OQ-4 2.1), 0.90 score {24, 35, 71, 93} (plan Decision), follow-up pooled {24, 35, 41, 93} (data separate it: proxy error about 3.7% against 0.8% for household members, backlog mix differs from coded mix). Two advisory forks, neither flips the call:
1. Unpaired literal reading of 3.1 (exact extract count against sampled reference) warns 17 groups; rejected on statistical grounds, text did not forbid it. Closed after the pass by the OQ-4 3.3 sentence (post-approval note).
2. Groups 71 (-2.27) and 25 (-2.51) are thin; an August-only backlog rate would drop 71, an unlicensed narrowing.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 17 | yes |
| Formats | 3+ | 5 (csv 11, pdf 2, xlsx 2, docx 1, parquet 1) | yes |
| Large file | 25,000+ rows | register 541,954; visit log 483,295 | yes |
| Distractors | 2+ in metadata.json, none named in a file | LFS Q3 employment, census 2021 by region; names carry no label | yes |
| Distractors weigh, unused, ruled out | yes | other sources' levels, unused by the solution | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png) | yes |
| Asks multi-dimensional, unit and rounding stated | yes | team x write-ins and hours, region x calls and no-contact calls; hours two decimals; counts are whole numbers | yes |
| Prompt shape, rubric 25+ | yes | shape 10 scorecard; 40 biases, call, 10 team figures, 16 region figures, chart | yes |
| Not LLM-generated; goldens real work products | yes | system-export mess, no authoring language | yes |

## Gate G reconciliation
Judge: mechanism forecasting, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: Gate G `forecasting`, stump_class analytical, strategy maturity_censoring; design note decisive step is the route-by-route build under the 0.80 rule. Match. Neither declared distractor (LFS Q3, census 2021) is named as the surface read; the surface read is the study's coded-so-far bias, which no shipped artifact states as a group ranking. The pass 1 decoy worry about the pooled "Clerical share" sheet does not recur. Gate G holds.
Gate H line: domain: pass, layers: pass, decisive_step: analytical. Card analyst_test and domain_test agree: the strong analyst's easy route ({35, 93} or pooled follow-up {24, 35, 41, 93}) is wrong, and the swap test fails to transplant.

## Stump power (Gate F)
Adequate. Three plausible wrong lists exist (coded-so-far, pooled follow-up, 0.90 score), the docs do not say to stratify by route, and the asks carry their own devices (reused coder ids, correction lines, tablet re-sends).

## Findings, ranked
1. None blocking.
2. Advisory: the unpaired literal reading of 3.1 (closed, see post-approval note).
3. Advisory: thin margin on 25 and 71, computed identically by every full-window rigorous solver.

## Next action for the author
Ship. Leak read 4 is running on the shipped cut.

## Post-approval note: changes after the pass 2 bundle
One generator pass; no graded figure moved (generator/figures.json byte-identical, 121 generator checks, verify green, rebuilds byte-identical). Shipped cut sha256 c0157a4749dd1cf25ae32d26bc0e6922d09ce6b7975cd617eaf821554bb4f1c0. Reported by the coordinator, not re-judged (no second thread):
(a) Judge's optional advice applied: OQ-4 3.3 now reads "In an estimate from the coding quality study, each studied write-in stands for as many coded write-ins as its selection interval, and the number that the release codes to a group and the number that the reference coding puts in it are both estimated from the same studied write-ins." checks.py SF14 asserts the exact-extract-against-study reading warns 17 groups, the difference estimator gives the golden flags within 0.06, and the sentence ships.
(b) The processing plan's single-row "Clerical share" sheet is folded into its Capacity sheet as input rows with per-row number formats; figures unchanged.
(c) Autocoder coded_at stamps follow a nightly first-in-first-out run from about 01:00, every save stamped to the second; no date moves.
Earlier, the cut feeding pass 2 also fixed the second leak read's findings: the procedures' month-end night closure matches the records, and the LFS distractor's CVs are no longer smooth.

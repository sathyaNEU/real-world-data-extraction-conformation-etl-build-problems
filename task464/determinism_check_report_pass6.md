# determinism-check report, task464, 2026-10-28 (pass 6)

## Verdict
DETERMINISTIC on the bundle the judge read (stale, see Findings 1). Not confirmed for the target.zip now on disk.
**Disposition:** APPROVE for the judged bundle, provisional. The shipped zip differs from the judged one, so the sign-off does not carry until the changed files are re-judged (re-run once, not a retry for a verdict).
**Stumping type:** mechanism: forecasting (method selection on honest data), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The judge (sonnet, one thread, isolated to /tmp/determinism-check-task464-1793180641/) reproduced the brief population (8,648; Marrick House 1,648), the 12% lapse (12.01% of 13,590 repeats), the order and Marrick = 170, and all 14 R1/R2 values. The seven-way order held under every variant it tried (Marrick lead over Cobbet 33 to 60).

Fork on the figure only, not the call: Marrick = 164 (no stops or no over-three-weeks rule, rounds to 160); 169 to 174 (golden family, 170); 180 (baseline hazard 0.6% from dating new starts "since first issue in the extract"); about 160 if the repeat with most unused issues is picked for double-active patients. The judge read the prompt and brief as not saying whether stops are included or how acute-only and double-active patients are handled.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Brief population | 8,648 | 8,648 (P81066 1017, P81177 829, P81283 877, P81402 1961, P81555 1648, P81719 1192, P81940 1124) | yes |
| CC1 lapse | 12% | 12.01% of 13,590 (11.8 to 12.1 by practice) | yes |
| CC2 Marrick population | 1,648 | 1,648 | yes |
| New-start stop hazard | 0.93% per 28 days | about 0.96% | yes (close) |
| Post-six-month hazard | 0.20% | about 0.2% only with proper new-start dating; 0.6% if dated from first issue in extract | yes, method-dependent |
| Marrick expected | 170 | 168.7 to 173.8 | yes |
| Order | Marrick, Cobbet, Fennbridge, Wyndhollow, Thistlecombe, Larkspur, Pellow Green | same (Cobbet 131-137, Fennbridge 98-103, Wyndhollow 71-73, Thistlecombe 58-62, Larkspur 53-55, Pellow 45-48) | yes |
| R1 % (81.0, 80.3, 81.9, 77.8, 79.9, 75.8, 92.9) | as golden | 562/694, 420/523, 481/587, 1114/1432, 897/1123, 507/669, 697/750 | yes, all 7 |
| R2 % (82, 83, 83, 71, 84, 58, 55) | as golden | 9/11, 5/6, 10/12, 20/28, 16/19, 7/12, 6/11 | yes, all 7 (strict "later than" anniversary; "on or after" would move Fennbridge to 79 and Cobbet to 67) |

## Competing answers that survived
- The call: none. The trailing same-window rate gives Cobbet Street 147 (12.3%), the wrong route; run-out count gives Marrick at about 1,350, a wrong figure.
- The figure: 160 / 170 / 180 spread from the stops, attrition, new-start dating and double-active choices above (judge's reading; the design note's own family of ten forms gives 168.5 to 171.8, all 170). The judge's optional fix is to file in the brief that the figure includes patients who stop between reviews and excludes those who leave.
- A 28-day supply interval lifts Wyndhollow to 133, above Fennbridge 126, which the data rule out (records' own gaps about 59 days).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files, formats | 10+, 3+ | 14; csv, jsonl, pdf, xlsx | yes |
| Large file | 25,000+ rows | 300k-row issues A, 43 MB jsonl | yes |
| Distractors | 2+ named, none labelled in a file name | metadata names qof_cvd_achievement and dispensed_items_cvd; pcn_practice_profiles xlsx also unused; judge: unused, weighed (QOF gap Cobbet, dispensing flag Wyndhollow) | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, csv), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | ranking, top figure to nearest 10, 14 percentages with stated decimals | yes |
| Prompt shape | identifiable, 25+ criteria | shape 01 (ranked list); rubric criteria not generated here, not checkable by me | not verified |
| Realism | no LLM tells | judge found no authoring strings, one visible sheet; events file named 2023-2026 starts 2022-11 (minor) | yes |

## Gate G reconciliation
Judge: forecasting / analytical_non_defect / surface_read_dependency no / sole_data_defect no, passes Gate G. Card and design note: Gate G method_or_model_selection, stump_class analytical, strategy time_semantics, decisive step the clock a forward persistence estimate runs on (run to each patient's own re-authorisation, priced at the record's lapse share). Same mechanism in different labels; no mismatch. The judge names the trailing same-window rate (Cobbet 147) as the wrong route, which is design-note ladder rung 1 (Cobbet 147.1), not a declared distractor. The declared distractors (QOF, dispensed items) are weighed but are not the surface read carrying the task, so no distractor-too-load-bearing finding. Gate G line: PASS, no ranked wrong artifact ships, difficulty survives deleting every wrong number.

## Gate H
domain: pass, layers: pass, decisive_step: analytical (judge). Design note: Layer 2 family field_method, "Not semantics" and "Not rule application" lines assert the same. R1/R2 are rule application on reconstructed doses but are asks, free of rule 3. Match.

## Stump power (Gate F)
Judge: moderate. The practice alone is easy to land by a run-out count (about 1,350, Marrick), though that fails the figure; the full order, the figure and R1/R2 carry the difficulty. Note for the main thread: the decisive step is the field's standard forward-to-renewal projection, a route a strong solver can reach (stumping 1.3). The design note ladder (rungs 0 to 2 all file Cobbet) argues the easy route fails; the judge's finding that a run-out count also files Marrick means at least one error route lands the call, so the ladder's "off the call" count should be weighed against that. Judge's lever if harder is wanted: make Marrick's lead over Cobbet depend on the lapse rate or stop hazard.

## Findings, ranked
1. STALE BUNDLE. The judged unzip was made from a target.zip with md5 a113113256424f0cf34cf7fb6c1900af (the md5 given at spawn). The zip on disk now (mtime 09:58:12) has md5 cc4a5bd0c384c3ac32c179b2e428077d, and the coordinator quoted a third md5, 6f02be38c83189e069b2f6fa89a71a8f. The current zip differs in three files: repeat_issues_system_a (300,495 rows judged, 300,753 now), repeat_issues_system_b jsonl, and eps_item_cancellations (1,603 rows judged, 2,044 now). Golden CSV/xlsx and submission.md were rewritten at 09:58 too. The submission figures I inlined equal the current golden CSV values, but the judge's reproduction ran on the old issue and cancellation files. The design note's SF11 asserts no statin item was cancelled, and R1 depends on cancellations, so R1 and the figure are unverified on the shipped data.
2. Figure fork 160/170/180 from unfiled stops, attrition treatment, new-start dating, double-active selection (judge). Call and order unaffected.
3. R2 depends on strict "later than" the anniversary, filed in the spec (SF19), judge accepted.
4. Minor: events file name vs coverage.

## Next action for the author
Confirm which target.zip is final (three md5s have been named), then re-invoke determinism-check once on that exact zip; optionally file in the brief that the expected number includes patients who stop between reviews and excludes leavers.

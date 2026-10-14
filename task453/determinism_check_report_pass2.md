# determinism-check report, task453, 2026-10-14 (pass 2, re-judge on the final pack)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread: one isolated Sonnet medium-effort thread on a fresh unzip of the final target.zip (13 files) at /tmp/determinism-check-task453-r3/; its verdict is /tmp/determinism-check-task453-r3/verdict.md. The r2 scratch and its stopped thread are discarded.

## Why
The Act s9(2) fixes the estimand (the national rate published from the changed survey in full use against what the previous survey would have published for the same months, rounded to one decimal, added to 6.0). The methodology note s1 supplies the replacement schedule (interview number per rotation group) and s4 the CSV rule. The thread recomputed the six interview effects (-0.52, +0.73, +0.73, +0.71, +0.66, +0.60), average +0.4848, so the change is +0.5, the trigger 6.5, and the four regions designate. Every committed figure reproduced.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Cells conformed vs Tables 1 and 2 | reproduce | Table 1 diff 0 at 1 dp over 60 months; Table 2 540 of 540 match | yes |
| Pre-July 2025 first-interview excess | +1.3 | +1.303 | yes |
| July to November 2025 arm gap | 1.2 | 1.17 (monthly 0.99 to 1.37) | yes |
| Change (region-month FE, weighted, 2022-01 to 2026-12) | 0.4848, +0.5 | 0.4848 | yes |
| Trigger | 6.5 | 6.0 + 0.4848, rounds to 6.5 | yes |
| 2026 averages from Table 2 | ER 6.58, WC 6.64, RD 7.44, HL 8.32, NC 6.44 | 6.583, 6.642, 7.442, 8.317, 6.442 | yes |
| Q4 2026 responding dwellings, once each | 14,827 / 11,749 / 9,532 / 10,842 / 7,981 / 9,007 / 7,532 / 10,008 / 6,562; 88,040 | identical, sum 88,040 | yes |
| CSV | 324 rows | 9 x 36; 18 months published + 0.5, 5 transition months and 13 months as published | yes |

## Competing answers that survived
None on the main call. Silent options and their results (all round to 0.5 unless noted): weighting (0.483 to 0.508); fitting window (full data, 2024-2026, 2025-2026: 0.483 to 0.485); drop any one region (0.459 to 0.511); drop 2022, 2023 or 2024 (0.481 to 0.488). Truncated windows that leave out most ICS interview 5 and 6 observations fall below 0.45 (2025 only 0.423; dropping 2026 0.424; 2025-06 to 2026-06 0.452) and no filed text licenses them. Dwelling identity: unique dwelling_ref gives 73,051 against 88,040 for reference plus entry month, closed by the note s1 and the prompt's "however many months it responded"; this is a data-semantics device confined to ask 4.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | yes |
| Formats | 3 or more | 4 (csv, parquet, xlsx, pdf) | yes |
| Large file | 25,000 rows or more | CAI cells 72,090; parquet 254,964 | yes |
| Distractors | 2 or more named in metadata.json, no file name labels one | 3 (population benchmarks, projected seasonal factors, response-rate workbook), none labelled | yes |
| Distractor relevance | unused by the solution, weighable, ruled out by a shipped fact | thread confirms unused; none carries a change or answers a graded quantity | yes |
| Deliverables | 1 to 3, all in the golden | 2 (PDF, CSV), both in golden/ (CSV 324 rows plus header) | yes |
| Asks | multi-dimensional, unit and rounding stated | trigger, change and CSV to one decimal; counts are whole dwellings; 10 counts, chart, 324 rows | yes |
| Prompt shape and rubric | identifiable shape, 25 or more criteria | shape "other" with arithmetic; design note counts about 30 criteria. The rubric itself is generated later, not verified here | yes (by the note) |
| Realism | nothing reads LLM generated | thread: no tells; fictional agency, no synthetic disclosure | yes |

## Gate G reconciliation
Gate G: pass. The thread names mechanism decomposition_attribution, family analytical_non_defect, no surface-read dependency and no sole data defect. The design note and the card name the stump as estimand identification (right comparison group: like interview against like interview, six effects averaged) with the easy route at the arm gap (+1.2, 7.2) or one effect (6.3 or 6.4). The two agree in substance (the label differs, the content does not). No shipped artifact ranks the regions wrongly; the thread's wrong routes (1.2, raw step 0.8, no restatement) exist only as its own reconstructions. The declared distractors (benchmarks, projected seasonal factors, response rates) carry no change and are not the surface read. No mismatch.

## Gate H
Gate H: domain pass, layers pass, decisive_step analytical. This matches the design note's `## Three rules` (domain test: bridging a questionnaire redesign through a rotating panel; Layer 1 two collection systems, thousands vs persons, 2019 vs 2025 codes, release headers; Layer 2 estimand identification; not semantics, not rule application, no decoy).

## Stump power (Gate F)
Strong. The easy routes (group gap 1.2, raw published step 0.8, no restatement) each give a different trigger and a two-region or six-region designation. The 0.4848 is stated nowhere in the files.

## Findings, ranked
1. Low to medium, margin. The change sits 0.035 above the lower edge of the 0.45 to 0.55 rounding band, and Eastern Ranges clears the restated trigger by 0.02 points (6.58 against 6.6 if the change were 0.6, flipping it out; North Coast 6.44 would flip in at 0.4). Estimators that use the late ICS interviews all agree; windows that exclude them give 0.42 to 0.45. No fork, but the call is thin. The Act's "once the change is in full use" does not name a window, and the design closes it as same call (SF5). No change required; the author should be aware of it at portal regrade.
2. Low. Chart ask 5 says "as published"; Table 1 carries original and seasonally adjusted series. The original series is the natural reading (cells, change and CSV rule are all original). State it in the golden and rubric.
3. Low. CSV column names and layout are not fixed by the prompt; values are determinate. Grade values, not headers.
4. Informational. dwelling_ref reuse is data semantics inside ask 4 only (allowed for asks). Closed by the note s1 and the interview_no reset.
5. Informational. The thread did not run a cross-batch fingerprint check (forbidden by its isolation); the author-side guard owns it.
No finding requires a generator, prompt or pack change.

## Next action for the author
Proceed to ship task453 on the current pack. Optionally note the original-series choice for the chart in the golden or rubric guidance. Do not re-judge.

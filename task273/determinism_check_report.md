# determinism-check report, task273, 2026-10-22

## Verdict
DETERMINISTIC
**Disposition:** APPROVE on determinism. Stump power is a separate matter (see Stump power): isolated reader r273b landed the main call and all 48 ask figures, so architecture 1 is spent at Gate F whatever this verdict says.
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no (borderline, route to live testing), sole_data_defect: no

## Why
The standard (1.2, 2.1, 2.2) files the estimand as the 99th percentile over "the requests customers send", with every pod pause counted. The judge thread rebuilt it from the raw logs and got exactly five endpoints above 800 ms (EP01, EP02, EP05, EP16, EP22), each by 120 ms or more, with every other endpoint at 675 ms or below. The result held across round-robin pods, pod-specific service pools, Poisson arrivals, window by start, end or both, a 2 s run-start shift and another seed. All 24 volumes and all 24 credit figures reproduced. The judge thread was one isolated sonnet thread that saw only a fresh unzip and the inlined blocks (spawned by the main session because this runtime had no Agent tool).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Recorded p99 EP01 / EP05 | 574 / 740 ms | 573.7 / 740.4 | yes |
| Recorded p99 EP02 / EP16 / EP22 | 874 / 963 / 1,084 ms | 874.3 / 962.8 / 1083.9 | yes |
| Rebuilt p99, freeze list | all five over 800 ms | EP01 1065, EP02 976, EP05 920, EP16 1125, EP22 1238 | yes |
| Rebuilt p99, nearest others | below 800 ms | EP08 675, EP20 602, EP09 587, EP06 448 | yes |
| Runs of record | last complete run, minutes 3 to 13; EP05, EP13, EP20 first runs set aside | stops at 5.7, 1.6, 4.2 min confirmed | yes |
| GC pauses | Pause lines only, two stamp kinds | 29,714 lines; ingest minus pause end 0.15 to 2.5 s for both kinds | yes |
| 24 volumes | e.g. EP01 22,706; EP05 30,284; EP16 31,925; EP22 35,149 | exact, to the unit | yes |
| 24 credits | e.g. EP01 6,989; EP22 23,872 | exact, to the dollar | yes |

## Competing answers that survived
None survive. Rejected by the shipped text:
- Recorded percentiles (3 endpoints): ruled out by standard 2.1 and 1.2 and by the plan's closed-loop statement.
- HdrHistogram back-fill (10 endpoints, 9 to 10 with other intervals): ruled out by the plan's statement that the edge rotates pods; it also varies with the interval chosen.
- Not subtracting the in-flight pause (EP06 reads 1030 ms): not licensed, since the recorded time already includes the pause.
- Minor literal forks, closed by text: 5xx not subtracted from volumes (standard 4.1, "as the edge counted them", moves volumes 2 to 35); credits at the legacy issued amount (5.2, "issued"); no incident sits on the 1 Jan or 1 Nov Eastern boundary; no rounding ties.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 18 (17 data and documents plus contents.txt) | yes |
| Formats | 3 or more | pdf, docx, xlsx, jtl, csv, log, json, yaml, html, txt | yes |
| Large file | 25,000 rows or more | k6 csv 119,388 lines; JTL 71,963 | yes |
| Distractors | 2 or more in metadata.json, none named in a file name | apm_traces_perf_2026-11-18.json, payroll_db_slow_queries_2026-11.csv; neither name labels one | yes |
| Distractor behaviour | unused by the solution, relevant enough to weigh | unused by the golden path; judge flags them as relevant but unused | yes |
| Deliverables | 1 to 3, all in the golden | 2 (xlsx, png), both present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 24 verdicts, 24 volumes (whole requests an hour), 24 credits (nearest dollar), chart; 48 ask figures plus verdicts | yes |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | cuts of a distribution (shape 14); 24 endpoints times three fields plus the call and chart exceeds 25 | yes |
| LLM-generated tells | none | judge found none; build tell only (docx zip dates of 1980), FIX_NOW at most | yes, one minor note |

## Gate G reconciliation
Judge: mechanism method_or_model_selection, family analytical_non_defect, surface_read_dependency no (borderline), sole_data_defect no. Design note and card: Gate G `method_or_model_selection`, strategy `population_selection`, `stump_class: analytical`. These match. The declared distractors (APM traces, slow-query log) are not the surface read carrying the task. The surface read is the recorded p99 of the load test (3 endpoints), a faithful figure of the closed-loop test and not a distractor or a wrong ranking shipped as an answer. Gate G: PASS. Borderline surface_read_dependency is routed to live testing.

## Gate H
domain: pass, layers: pass, decisive_step: analytical. The judge's reading and the design note's `## Three rules` agree (Layer 1: JMeter against k6 timestamps, UTC against Eastern, two GC stamp kinds with restarts, route renames, legacy billing carry-forward; Layer 2: coordinated-omission correction and open-arrival percentile rebuild). The thread classed it analytical, and it recomputed by the rebuild method itself, so this is the library's textbook-route case: the thread describes a call that the blind readers measure as landable (see below).

## Stump power (Gate F)
The judge rated stump power good: the easy routes give 3 (recorded) or 10 (back-fill), and the clean-up chain before the rebuild is costly. The coordinator reports the measured result: isolated reader r273b landed the main call (EP01, EP02, EP05, EP16, EP22) and all 48 ask figures (score_reader FAIL), so architecture 1 is spent at Gate F regardless of this verdict. Coordinated omission and its correction are a known textbook route that a strong solver takes (stumping 1.3), and the filed text (standard 1.2, 2.1, 2.2, plan sections 2 and 3) closes the closed-loop and rotation facts so well that the rebuild is reachable. The main thread weighs this with the scored readers' result. This is not a determinism defect.

## Findings, ranked
1. Gate F: r273b landed the call and every ask figure. The stump is too landable and the asks do not hold the top solver (outside determinism; main-thread decision, redesign or harden).
2. Minor: docx zip timestamps of 1980 (build tell), FIX_NOW at most.
3. Minor: contents.txt is the only README-like file; acceptable.
4. Cross-batch clone check not run (the thread may not read other task folders); no duplicate asserted. The design note records seven older generator signatures, each differentiated on the card.

## Next action for the author
Do not spend a determinism repair here: no fork is open. Decide on the Gate F result: harden or re-root the stump, and the supplemental asks, so that a solver who applies the standard's open-arrival rebuild does not also land the 48 ask figures.

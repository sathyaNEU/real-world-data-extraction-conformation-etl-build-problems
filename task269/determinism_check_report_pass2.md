# determinism-check report, task269, 2026-10-26 (stage 4 round 4)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Bundle judged: target.zip md5 ab7b95ffa1cc933f78b6b00992f2f408, fresh unzip at /tmp/determinism-check-task269-045602/target/. Judge verdict: /tmp/determinism-check-task269-045602/verdict.md. One thread, one pass, spawned by the main session (this runtime has no Agent tool).

## Why
The terms file the estimand literally (every AM and PM shift of 2025-26, shifts weighted by required care hours, funded below 80 per cent, at most six). The audits cover 13 per cent of ward shifts and avoid short-staffed ones (5.3 per cent of audited moments on shifts over 10 per cent short, against 18.8 per cent of care hours; compliance 58.9 against 87.1). Eight staffing-adjusted model variants fund the same five (73.9 to 77.6); the lowest unfunded ward is 82.8 or above in the judge's fits, so the cap of six never binds. All 14 Ask A rows and all 28 Ask B and C figures reproduced.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Audits as they stand | 9B 77.0, others 82.8 or above | same (ESSU 82.8, AMU 83.2) | yes |
| Audited moments on short shifts vs care hours | 5.3 vs 18.8 | same | yes |
| Compliance short vs rest | 58.9 vs 87.1 | same | yes |
| Funded set | AMU, ESSU, 4A, 7A, 9B | same five under 8 variants | yes |
| Ask A, 14 wards (count, rate) | AMU 29/37.4 ... ICU 41/67.7 | all 14 match | yes |
| Asks B and C, 28 litre and per-1,000 figures | per the answers | all match | yes |

## Competing answers that survived
No fork on the main call. Forks on the asks, each closed by the data and not by a stated rule (the judge does not count them as open on the call):
- Merging admissions that begin the minute the previous one ended (Ask A): not stated in the prompt; rests on definition 3 and zero-gap readmissions. Per-admission_no counting gives 4A 29, 5A 27.
- Handheld resend dedup (Asks B, C): no shipped file states the rule; the injected pattern is clean (same dispenser, same minute of day, lag 1 to 15 days, 246 records), so any window from 15 days up agrees. Not deduplicating gives 4A rub 450.6 against 445.6.
- Terminal-clean job quantity (Ask C): quantity repeats the job total on each record; summing quantity gives 7B soap 162.0 against 118.8. Inferred from the data, not stated.
Location as ward against the ward the patient was on is closed by definition 5 and the data note.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 18 | yes |
| Formats | 3 or more | 4 (csv, pdf, txt, xlsx) | yes |
| Large file | 25,000 rows or more | 224,319 rows (audit moments) | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | patient_experience_survey, staff_influenza_vaccination; names carry no label | yes |
| Distractor unused yet weighable | unused, a shipped fact rules it out | judge found them unused; not checked beyond that, neither answers a graded quantity | yes |
| Deliverables | 1 to 3, all in the golden | 2 (xlsx, png), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | each | litres and per 1,000 bed days, one decimal, in the prompt | yes |
| Prompt shape and 25 or more criteria | identifiable, 25 or more | per-ward grid of 14 wards across counts, rates, litres, rates and the chart far exceeds 25; rubric itself not inspected | yes (inferred) |
| Reads as real, not LLM generated | | judge found no authoring leakage | yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: Layer 2 `estimation_fit`, audited moments reweighted to each shift's care-hour shortfall, nothing planted, "No decoy" line. The card has stump_class analytical and an analyst_test whose easy route (audits as they stand or care-weighted) funds 9B alone, which is the same wrong answer the thread names. No mismatch. The declared distractors are not the surface read, and the surface read carrying the task is the raw audit share, not a distractor.

Gate H: domain pass, layers pass, decisive_step analytical. Matches the design note's `## Three rules` (domain test, Layer 1 and Layer 2, decisive step: model compliance by the care-to-worked-hours ratio and carry it across all shifts). The thread reached the golden by fitting that model, not by executing a filed method, so it is not the "standard method applied without judgment" case.

## Stump power (Gate F)
High and analytical per the judge: stopping at the audits or the care-hour weighting funds 9B alone, and the fix needs an acuity and roster join the prompt never names. The judge's own fit landed on the golden five under every specification tried. The main thread should weigh this with the scored readers' result, since a strong solver who suspects selection in the audits may find the route.

## Findings, ranked
1. None blocking. The three undocumented conventions on Asks A to C (admission merge, handheld resend dedup, job quantity) are data-detectable and sit in the asks, not the main call, but they are inferred and not filed; the design note's fork table should name each with its closing sentence if it does not already.
2. The chart bar heights are model-dependent by about 2 to 3 points; grading should rest on the funded colour, the 80 per cent line and the order, not the exact heights.
3. Cross-batch hygiene check not done (no batch archive available).

## Next action for the author
Confirm the fork table names the admission merge, the resend dedup and the job-quantity convention for Asks A to C; otherwise ship.

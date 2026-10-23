# determinism-check report, task478 (architecture 7, re-judge after FIX_NOW), 2026-10-23

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated sonnet thread (fresh unzip of target.zip, md5 77f6a96a6b67922579f65d575e9286bc) reproduced every graded figure. The order is Ashgrove 25.96, Lindqvist 12.09, Merriwell 9.03, Valmora 8.12, Sedge Hollow 8.08, then Tamsett State 6.95. All 14 rounded tons match item 2. The three earlier FIX_NOW forks are closed by shipped data: the hours.minutes log reading (no fraction reaches .60, all multiples of .03), the READ_TO 1 July step in billed gas against plan fuel, and the rise's basis (Lindqvist PB1 slope 6.14, Westside tests 6.26; the call is stable for any slope from about 4 to 8). Verdict file: /tmp/determinism-check-task478-v7r2/verdict.md.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| CEMS tons (4 units) | 32 | 31.6 (Ashgrove 23.30, Lindqvist 8.28) | yes |
| Five facilities' tons | 26, 8, 8, 12, 9 | 25.96, 8.12, 8.08, 12.09, 9.03 | yes |
| Tamsett State, sixth | 7 | 6.95 | yes |
| Rise per cent of heat content | about 6 | 6.14 (PB1), 6.26 (Westside tests) | yes |
| Gas, all facilities | 22,372,114 MMBtu | each of 14 values and the total | yes |
| Engines | 9,943 lb | 9,942.8; every facility value | yes |

## Competing answers that survived
None on the main call. Plain mean or latest test gives Tamsett State in and Merriwell out; the data separates this (PB1 and the Westside tests both show the heat-content rise), so it is the analytical wrong route, not an open fork. Gas read as-is gives 22,025,170 (the data rules it out: billed over plan fuel steps at READ_TO 1 July). Engines as decimal hours, or without the OUTAGE correction, give 7,442 or 11,036 lb (hour meters and the doubled lines rule them out). Both are in the asks, not the call.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 in the bundle | yes |
| Formats | 3 or more | csv, xlsx, pdf | yes |
| Large file | 25,000 rows or more | cems 34,065 rows; no2 26,280 rows | yes |
| Distractors | 2 or more named, no file name labels one | no2_hourly, onroad_nox in metadata.json; unused, relevant to weigh, ruled out by shipped fact (not facility emissions) | yes |
| Deliverables | 1 to 3, all in golden | 3 (xlsx, csv, svg), all in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 14-facility cuts, whole tons / MMBtu / lb in the prompt | yes |
| Prompt shape and rubric | 25 or more criteria | 14 tons + 14 gas + 14 engines + call and files, well over 25 (rubric not inspected; generated downstream) | yes |
| Realism | no LLM tells | thread found no authoring language; goldens not re-read here | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: the stump sentence is the rate-carried-by-heat-content route against the latest-test default; card stump_class analytical. They match. The declared distractors (NO2 monitors, on-road NOx) are not the surface read carrying the task. No mismatch.

## Gate H (thread)
domain: pass, layers: pass, decisive_step: analytical. Matches the card's analyst_test (carry each unmonitored burner's latest test across 2026 fuel gives the wrong five) and domain_test. The thread did not class the step analytical merely because the method is standard: the golden needs a covariate-adjusted rate that the data (PB1 plus 248 tests) must supply.

## Stump power (Gate F)
Likely effective: the mean or latest-test route files Tamsett State fifth and drops Merriwell. Three silent conventions in the asks (CCF to therms at July, hours.minutes, doubled parallel-engine lines) each move a whole column. Mild over-help risk: guidance section 6 names the hour meter's warm-up counting. The portal measures the real result.

## Findings, ranked
1. None blocking.
2. Minor: the heat-content dependence is stated nowhere and is found only from the data; the thread judged this analytical, not a fork, and the call is stable across slope 3 and up (fifth place flips only near slope 0).
3. Minor: the thread could not run the cross-batch fingerprint check (outside its allow-list).

## Next action for the author
Ship (stage 5); no re-judge is needed. The optional guidance-section-3 pin the thread listed would make the call easier and is not recommended.

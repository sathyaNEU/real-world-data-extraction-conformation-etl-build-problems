# determinism-check report, task270, 2026-10-28 (pass 1)

## Verdict
NOT_DETERMINISTIC (underspecified_objective), plus SOLUTION_WRONG on one attribution (step 3 cites "guidelines 3.2" for the half-year rule; 3.2 does not contain it).
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judge: one thread (general-purpose, sonnet, medium) on target.zip sha256 prefix 4f72f776, scratch /tmp/determinism-check-task270-170821b/. Verdict file: /tmp/determinism-check-task270-170821b/verdict.md.

## Why
Every golden figure reproduces, but the main call holds only under a rate-to-years convention no shipped file states. Guidelines 3.2 says the rate at each age "held for the rest of their life"; 3.3 defines the rate as deaths over summed 30 June ERP. Nothing says how that rate becomes survival or years lived. Converting the central rate (q = m/(1+m/2), or a constant hazard) gives the golden four. Reading the rate directly as the probability of dying (q = m) gives seven areas below 7.0 on the same correct populations: Cobbleton 6.87, Spraymouth 6.93 and Merriwold 6.98 join the four, and the call flips. The design note's SF10 closes only half a year against 0.45; it has no row for q = m, so the fork table is incomplete on the main recommendation.

My view for the main thread: the constant-hazard reading ("a rate held") is the more natural literal one and agrees with the golden to 0.003, so the q = m reading is the weaker competitor. A literal judge still treats it as open, and the real reviewer will too. Filing one sentence is cheap.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Deaths 85+ 2024 to 2026 (BDM plus interstate, ASGS map) | 7,485 | 7,485 (7,433 + 52) | yes |
| LE at 85, 12 areas (Windermoor 6.6, Coldwater Plains 6.8, Dunesford 6.9, Saltwick Shoals 6.9, Cobbleton 7.1, Spraymouth 7.2, Merriwold 7.2, Bannockvale 7.3, Wolfram Ranges 7.3, Kestrelmoor 7.4, Mallowmere 7.4, Gannetmouth 7.5) | as listed | 6.588, 6.819, 6.876, 6.919, 7.122, 7.190, 7.227, 7.295, 7.309, 7.385, 7.423, 7.477 | yes, under q = m/(1+m/2) only |
| Qualifying set | 4 areas | same 4 | yes under golden convention; 7 under q = m |
| After-hours visits, 12 areas (e.g. Bannockvale 1,002) | listed | all 12 match | yes |
| Distinct residents, 12 areas (e.g. Bannockvale 697) | listed | all 12 match | yes |

## Competing answers that survived
1. Rate-to-years convention. q = m names 7 areas; the golden convention names 4. No shipped sentence closes it. Missing fork row in the design note. Open, blocking.
2. Visit grain (minor): cases (Bannockvale 923) or clinician rows (1,069) against visits (1,002). The asking sentence ("how many times visited") and the data (no gap between -10 and +60 minutes, so any same-visit threshold from 0 to 60 gives the same counts) close it. The 30-minute rule in step 5 is in no file but is harmless.
3. Census-shape and NSW-shape splits (Windermoor, Coldwater Plains, Spraymouth; or Windermoor and Coldwater Plains) are the intended wrong easy route, ruled out by the data (cohort totals match ERP 85+ within about 2%, the census shape cannot be reconciled). Not an open fork.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats | 10+ / 3+ | 10 / csv, xlsx, pdf | yes |
| Large file | 25,000+ rows | BDM 73,066; after-hours 28,873 | yes |
| Distractors | 2+ in metadata.json, none named in a file | 3 (erp_nsw_single_year_age_sex csv, residential_aged_care xlsx, falls_injury csv); names are neutral | yes |
| Distractor weighing | unused, relevant, ruled out by a shipped fact | none answers a graded quantity; the NSW shape reproduces as a wrong route and the data rule it out | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 12 areas x 3 figures; years to one decimal, whole numbers | yes |
| Prompt shape / rubric 25+ | identifiable; 25+ | scorecard against a threshold; rubric is generated at portal, count not verifiable here (12 x 3 figures plus call and chart parts, plausibly met) | not verifiable, likely |
| Reads as LLM generated / real work product | no | judge found realistic headers, preliminary ERP sheet, mixed UTC offsets, repeated registration numbers; no provenance leakage | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Gate H: domain pass, layers pass, decisive_step analytical.
Card (stump_class analytical, analyst_test, domain_test) and design note: the decisive step is rebuilding each age's population by following census cohorts forward with deaths since census night, against splitting the 85+ estimate by the census age mix. The analyst_test names {Coldwater Plains, Spraymouth, Windermoor}, which is exactly the thread's census-shape result; the thread's own number for it (Windermoor 6.45, Coldwater Plains 6.83, Spraymouth 6.69) agrees. No mismatch. The declared distractors do not carry the task (the NSW shape is a second wrong route to the same kind of miss, not the surface read the call turns on). Layer 1 (system change, SA2 keys, interstate deaths, offsets) does not carry the stump. The design note's Three rules lines are consistent with the thread's reading. The one divergence is the missing convention row: the note's "Not rule application" paragraph enumerates a standing family but omits q = m.

## Stump power (Gate F)
Strong and analytical per the thread: the cohort-component rebuild validated against ERP totals decides the call, and the easy census split lands a wrong named set, missing Dunesford and Saltwick Shoals. The thread did not class the step as a field-standard method reached without judgment. The margins (Saltwick Shoals 0.08 below the line, Cobbleton 0.12 above) are clean at the golden convention; they are also why q = m flips the set. Main thread to weigh against the ladder.

## Findings, ranked
1. Blocking: rate-to-years convention unfiled (above); q = m flips the call from 4 to 7 areas.
2. Solution blocks: step 3 attributes "half a year lived in the year of death" to guidelines 3.2; it is in no file. Fix the attribution once the sentence is filed (cite the new clause).
3. Step 5 states a 30-minute same-visit rule that is in no file; the data separate it (any threshold 0 to 60 gives the same counts). Reword to the data-separated rule or file it.
4. Design note: add a fork row for the rate-to-probability convention, closed by the new guidelines sentence and asserted in checks.py; SF10's "ruled out by agreement" does not cover it.

## Next action for the author
Add one WHAT sentence to the guidelines PDF section 3.2, for example: "A death rate is deaths per person-year of exposure, and a person who dies at an age is counted as having lived half of that year." File the population, never the HOW of the single-year rebuild. Then add the fork row and a checks.py assertion, correct steps 3 and 5 in submission.md, rebuild twice byte-identical (pack and figures unchanged), and re-judge once under /fix-determinism rules (the guidelines PDF changes what solvers see).

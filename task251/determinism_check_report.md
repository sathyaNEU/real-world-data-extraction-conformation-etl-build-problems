# determinism-check report, task251, 2026-10-21

## Verdict
NOT_DETERMINISTIC (ask 2 only; the main call reproduces and is robust). No SOLUTION_WRONG on the main call.
**Disposition:** FIX_NOW for ask 2 (the main call, ladder and goldens of asks 1, 3, 4 stay frozen); SEND_BACK only if the author keeps the remote-reset device without a shipped fact that separates it.
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no
Context (from the coordinator, not the thread): at stage 4 one of the two scored readers landed the main call, so this architecture is spent whatever this report says.

## Why
The main list (R03-02, R04-03, R05-01, R08-05, R10-03) is forced by the files and holds across seven loss-curve variants (binned, monotone, hinge-linear, NB-only, SB-only, TCX-2 bridges only, TCX-4 bridges only); the listed five sit between -6.3 and -7.9, the highest unlisted at -3.6 to -4.9.
Ask 2 (maintenance visits) fails Gate C (underspecified_objective): the golden removes "Controller reset" days only at TCX-4 stations whose cabinet door logged nothing. All 24 of 24 TCX-4 reset-order days are door-less, and all 21 TCX-2 reset-order days carry the identical order text ("No data from controller since hh:mm" / "Controller reset, data recovered"). No shipped file says a TCX-2 reset is done on site or from the office. A rigorous analyst who generalises the evidence removes all 45 reset days and files Ashby 1/15/5/18, Kessel 3/16/1/18, Marlow 3/7/4/6 against the golden Ashby 3/18/10/19, Kessel 6/18/1/19, Marlow 3/10/5/6.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Max filmed-hour occupancy | 8.8 per cent | 8.82 (R05-01, R14-01), Northline vs hourly csv | yes |
| R14-01 / R18-01 sensitivity | +6 / +8 | +5.4 to 5.7 / +8.0 (loops over video) | yes (rounding) |
| Loss at 40 per cent occupancy | about 1 in 5 | adjusted ratio 0.80-0.82 at 38-40, 0.73 at 46+, 0.995 below 10; bridge pairs | yes |
| Listed five errors | beyond -6 | -7.0 to -7.5 (binned curve) | yes |
| Largest unlisted | within 4.5 | R22-02 -3.9 to -4.9 by curve | partly: "4.5" is loose |
| Ask 1 list | 5 stations | same 5 | yes |
| Ask 3 power failures | Ashby 3/2/4/11, Kessel 12/4/9/4, Marlow 2/5/4/4 | identical under the golden rule | yes (rule is derived, not filed) |
| Ask 2 visits | Ashby 3/18/10/19, Kessel 6/18/1/19, Marlow 3/10/5/6 | identical under the golden rule (142 labour station-days, 24 TCX-4 door-less days removed) | yes under the golden rule only |

## Competing answers that survived
1. Ask 2, TCX-2 reset days: golden keeps the 21 as visits; the generalised reading removes them (45 reset days removed in all). Cells differ (see Why). No shipped rule closes it.
2. Passed vehicles outside the filmed days: loops as truth (flags 0), filmed-day sensitivity only (flags R03-02, R14-01, R18-01), sensitivity plus occupancy loss (flags the five). This is analysis, not wording; the files force the third.
3. Sensitivity carried across a controller swap (R08-05, R19-03): R08-05 stays flagged unless the old controller differs by more than 5 points; R19-03 (-4.4) would cross -5 if the new TCX-4 read 2 to 3 points lower. Unstated, does not flip the call on the evidence.
4. Ask 3: "breaks in the hourly record" as power failures at a TCX-2 and "as many as the COMMS_LOST inside" are corroborated by the data but not filed.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 11 | yes |
| Formats | 3 or more | 5 (csv, xlsx, pdf, md, eml) | yes |
| Large file | 25,000 rows or more | trafficvault_hourly_counts_2027.csv, 525,386 rows | yes |
| Distractors named, none labelled by file name | 2 or more | weather_daily_2027.csv, collisions_regional_roads_2027.xlsx in metadata.json; file names neutral | yes |
| Distractors unused yet weighable | yes | unused by the solution; neither answers a graded quantity (the design note says they carry no figure any route needs) | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 12 + 12 district-quarter cells, errors in per cent, counts whole | yes |
| Prompt shape and 25 or more criteria | yes | shape "other"; the design note estimates about 35 criteria (not generated here) | yes, unverified |
| Not LLM generated, goldens real | yes | thread saw no authoring leakage; golden realism not re-read by me | not contradicted |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical; stump sentence and analyst test name the validation list (R03-02, R14-01, R18-01) as the easy route, matching the thread's easy route exactly. Declared distractors (weather, collisions) were not named by the thread as the surface read: no finding. Gate H: domain pass, layers pass, decisive_step analytical; the note's Three rules line and the thread agree (measurement-error model with a load-dependent term fitted on bridge pairs). No mismatch.

## Stump power (Gate F)
Strong on paper: the validation list is a plausible wrong answer (two false positives, four misses), and the decisive work is recovering an unobserved occupancy-dependent loss from the right comparison. The thread did not reach the golden by applying a textbook method with no judgment. The scored readers measured otherwise: one landed the main call, so the architecture is spent.

## Findings, ranked
1. Ask 2 is not forced (Gate C): TCX-2 reset days are indistinguishable from TCX-4 office resets in the shipped text.
2. "No other station is beyond 4.5 per cent" is loose; nearest R22-02 is -4.6 to -4.9 by curve. Say 5.
3. Sensitivity across a controller replacement (R08-05, R19-03) is an unfiled assumption.
4. Ask 3's TCX-2 failure rule is derived, not filed (corroborated by the data).

## Next action for the author
Pin ask 2 without touching the main call: either file the visit definition in the asking sentence and add a shipped on-site versus remote signal that separates the 21 TCX-2 reset days (for example an access field on the order), or drop the remote-reset device and count every labour day. Then tighten "4.5" to "5" in submission.md and re-judge once.

# determinism-check report, task478, 2026-10-21 (pass 2)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread: one sonnet/medium judge over a fresh unzip at /tmp/determinism-check-task478-r2/target/ (verdict at /tmp/determinism-check-task478-r2/verdict.md). The pass-1 forks (pounds reading, service-days charge) are gone: the service-days ask is dropped and the dictionary wording is neutral.

## Why
The program text counts every pothole "whether or not a Kerbline unit recorded it", and the scope of work says the detection inventory is not complete, so the unrecorded potholes must be completed. The files fix the completion: a unit re-records a defect on 99.7 per cent of its later days, a second unit finds it 54.2 per cent of the time, so coverage depends on distinct units, not passes. That gives the seven designated sections (Holloway Run, Fenwick Gap, Carrow Point, Kestrelton, Elmscourt, Thistlebank, Norvelle) at 6.0 or more, with Rushmead next at about 5.0. All five asks, the designations and the chart ask reproduce.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Program lane-miles | 2,428.9 | 2,428.938 (road_inventory_2026.csv less 5 turnback segments) | yes |
| Confirmed potholes | 1,080 | 1,085 before turnback, 1,080 after (qa review xlsx) | yes |
| Cross-unit find rate | 54.2% | 1,724/3,178 = 54.25% (q 0.4575, golden 0.458) | yes |
| Own-unit repeat rate | 99.7% | 21,987/22,052 | yes |
| Ask 1 per ten lane-miles | 8,7,8,4,4,7,9,3,8,4,5,3,8,2 | identical | yes |
| Ask 2 designations | 7 sections | identical | yes |
| Ask 3 patched potholes | 20,27,70,8,13,13,85,4,21,4,48,13,9,5 | identical | yes |
| Ask 4 pounds | 1,255 ... 350 | identical | yes |
| Ask 5 camera miles | 2,084 ... 1,774 | identical | yes |

## Competing answers that survived
- Recorded count only, and pass-weighted completion: both designate Carrow Point and Elmscourt only. Both are the easy route and are ruled out by the program text and the 99.7 per cent persistence in the files.
- Robustness: the seven designations hold for q 0.40 to 0.52, the zero-truncated MLE (0.452), fleet-group and unit-specific rates, a UTC month, and ignoring install dates.
- Integer fork on ask 1 only: q = 0.48 gives Norvelle 9, and a noisy unit-specific rate gives Norvelle 7 and Halverton 4. Integers are identical for q 0.43 to 0.47. No literal reading prefers those estimators. Not a call fork.
- Ask-only residual forks, closed by the data and not by a filed sentence: (1) the pre-17 March ext_ref (prefix 26) links to no Kerbline number, so it is matched by route and milepost (all 382 match exactly, no ties); (2) repeated-total pounds on multi-line orders (summing every line gives Holloway Run 2,375 against 1,255); (3) the 12 to 13 March re-run overlaps (keeping them gives Holloway Run 2,122 against 2,084). These sit in asks, which may turn on layer-1 hazards. They are the main residual risk of an alternate golden on asks 3 to 5.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files, formats, size | 10+ files, 3+ formats, one 25k+ rows | 16 files; csv, pdf, xlsx, json; detections 37,995 and traversals 65,867 rows | yes |
| Distractors | 2+ in metadata.json, none labelled in a file name | pavement_condition_2026.csv, winter_operations_2027-03.csv, kerbline_unit_sessions_2027-03.json; reasons filed; no file name labels one | yes |
| Distractor behaviour | unused by solution, relevant to weigh, ruled out by a shipped fact | the judge found none decisive (condition survey and storm hours are causes, not counts; sessions are settled by traversals and register); none answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (CSV, PDF); both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 14-section vectors, whole numbers and units stated in the prompt | yes |
| Prompt shape and rubric | identifiable shape, 25+ criteria | shape `other`, designation over 14 candidates; about 76 criteria now (14+14+1+3+2+42), 81 in the stale design note | yes |
| Not LLM generated, real work product | | the judge found no authoring language; provenance and dates coherent. I did not open the golden PDF for realism | yes, with that caveat |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_class analytical, with an analyst_test (pass-as-chance route designates two of seven) and a domain_test (imperfect-detection completion by distinct units). These match. The declared distractors are not named as the surface read. The thread's easy routes (recorded count, pass-weighted) are the card's easy route. Gate G line: no shipped artifact ranks the candidates wrongly; the recorded counts are honest but incomplete.

Gate H line (thread): domain pass, layers pass (layer 1: renumbering and crosswalk, UTC against ET, provider re-run, repeated order pounds, mid-month turnback; layer 2: detection-probability completion by distinct units), decisive_step analytical. This matches the design note's `## Three rules`.

## Stump power (Gate F)
The judge calls it good. The trap is the persistence of detection by a unit. The program text does say "whether or not a Kerbline unit recorded it", so a strong solver may infer an undercount. Pulling the 99.7 and 54.2 per cent rates from the files and using distinct units is the real work, and the pass-weighted route gives the wrong two. The asks add independent layer-1 hazards. Capture-recapture is a textbook route, and the filed data pins the occasion unit. The main thread should weigh this against the scored readers.

## Findings, ranked
1. Low: the design note's Shape paragraph (lines 57-58 of DESIGN_NOTE.md) still counts 47 ask figures with the dropped service-days and charge ask and 81 criteria. It is stale after the pass-1 fix, so refresh it (the true count is about 76).
2. Low: the integer fork on ask 1 at the Norvelle and Halverton edge (q 0.48 or unit-specific rates), and the three ask-only forks above. Each is closed by the data, not by a filed sentence. Consider whether the design note's fork table lists the ext_ref prefix match, repeated-total pounds and the re-run overlap.
3. Info: the 17 March renumbering and the re-run are in no shipped file. This is layer 1 mess and not a defect.

## Next action for the author
Update the design note's Shape paragraph to the post-fix criteria count (service-days ask removed), confirm the fork table covers the three ask-only forks, and then ship.

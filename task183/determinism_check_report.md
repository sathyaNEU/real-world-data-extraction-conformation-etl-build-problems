# determinism-check report, task183 (architecture 3), 2026-11-02

## Verdict
NOT_DETERMINISTIC (every golden figure reproduces, so not SOLUTION_WRONG)
**Disposition:** SEND_BACK
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
SP-07 3.5 says only "a full-service application in normal rail conditions" and never says whose deceleration tests it. The only filed rate is the Class 162 data sheet FE-162-07 step 3, 0.88 m/s2 (dry rail, level tangent track). Executed literally with 0.88 the winner is SK112 (3), with CJ53 and SK115 on 2 and CJ58 on 0. The golden (CJ58 6 v SK112 3) holds only on a rate taken from each signal's own routine step 3 stands in the OTMR extract (CJ58 0.667), which no sentence directs. Competing defensible answer on the main call. Both asks also carry an unfiled second reading. Source: judge thread verdict, /tmp/determinism-check-task183-a3r1/verdict.md.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| CJ58 step 3 median rate (extract, n=556) | 0.667 | 0.667 | yes |
| SK112 step 3 median rate (n=282) | 0.88 | 0.880 | yes |
| Driver braking SPADs CJ58 / SK112 | 6 / 3 | 6 / 3 (CJ58 2,2,2; SK112 1,1,1) | yes, stable p25 to p95 of own stands |
| Slide 2 other signals | OW4 2, SK115 2, HD69 1, RV17 1, RV20 1, RV23 1, SK108 1 | same | yes |
| TPWS by box (golden reading) | Helmsdyke 9/11/9, Ravensholme 5/1/5, Cauldwell 6/6/5, Owlsden 5/3/6, Skelby 9/8/11 | same | yes |
| Hours (golden reading) | Helmsdyke 10,780/10,740/9,850; Skelby 11,000/10,960/10,050; Owlsden 5,810/5,800/5,320; All 27,590/27,490/25,220 | same | yes |

## Competing answers that survived
1. Main call, rate source. Fleet sheet 0.88 for every signal gives SK112 3, CJ53 2, SK115 2, five signals on 1, CJ58 0. Winner SK112, runner-up 2. The fleet-wide median of all B3 stands (0.861) also gives SK112 3. No shipped sentence closes it. The sheet's "level tangent track" scope is a condition, not a directive to substitute a measured rate.
2. TPWS ask. The extract's signal_ref is filled on every event, including those on speed-restriction and buffer-stop loops. Counting by signal_ref gives Helmsdyke 11/12/12, Ravensholme 8/4/7, Cauldwell 10/7/6, Owlsden 6/5/8, Skelby 13/13/15. The prompt's "at its signals" does not rule that out. Golden counts only events on a signal's own loop (99 of 137 within 18 m of a signal loop; 22 on speed-restriction loops, 16 on buffer-stop loops).
3. Hours ask. No filed sentence extends a turn past its booked off to the last train's arrival plus ten minutes. Booked on to booked off, deduplicated, gives All 27,380/27,300/25,040 (Helmsdyke 10,690/10,660/9,780; Skelby 10,920/10,890/9,990; Owlsden 5,770/5,750/5,280). Arrival plus ten whenever off is earlier gives All 27,680/27,580/25,300; extend to arrival only gives 27,490/27,400/25,130; always arrival plus ten gives 27,640/27,540/25,260.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats | 10+ / 3+ | 12 / 5 (pdf, xlsx, docx, csv, json) | yes |
| Large file | 25,000+ rows | train_running 90,512; extract 26,598 | yes |
| Distractors | 2+ in metadata.json, none labelled by file name | spad_register_export_20261201.csv, class162_brake_overhaul_history.xlsx; names do not label them | yes |
| Distractor behaviour | unused, weighs, ruled out by a shipped fact | stale export gives same counts, overhaul history changes no count; neither answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden, no format family | 3 (pptx, csv, xlsx), all present in submission | yes |
| Asks | multi-dimensional, unit and rounding stated | by box/depot by year; whole numbers, nearest ten stated in prompt | yes |
| Prompt shape / 25 criteria | identifiable, 25+ | shape 08 named in metadata; criterion count not verified (rubric generated downstream) | not verified |
| Reads as real work | no LLM tells | judge found no authoring disclosures | yes |
Spec gates pass, but the determinism failure stands on its own.

## Gate G reconciliation
Thread: mechanism method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no. The design note's stump sentence (rated 0.88 files SK112 3; the approach's own stands give CJ58 6) matches the thread's description of the easy and golden routes, so the stump is the one declared. The declared distractors are not the surface read, so they are not too load-bearing. The finding is that the easy route rests on a figure a shipped document states, so a literal reading licenses it. The design note's own post-verdict entry in Tried and rejected reaches the same conclusion: the sentence that would close the fork names what the decisive step works out, so filing it turns the step into rule application. No pin saves this architecture.

## Gate H
domain: pass (braking-distance and deceleration estimation is rail safety analysis; swap test does not read the same). layers: pass (Layer 1 is ID formats, duplicates, UTC, units; Layer 2 is the approach's own achievable rate). decisive_step: analytical, but unfiled.

## Stump power (Gate F)
Moderate if the rate source were pinned. As shipped, a miss is a reading of an unfiled definition, not a clean analytical stump. The 0.88 route is textbook and stated in the only brake document.

## Findings, ranked
1. Main call fork on the rate source (0.88 fleet sheet gives SK112 3; golden CJ58 6). Gate C/E.
2. TPWS ask: signal_ref on speed-restriction and buffer-stop loop events.
3. Hours ask: unfiled extension of turns to last arrival plus ten minutes.

## Next action for the author
Re-root at stage 1 into another world and dataset. A pin on the rate source would file the HOW and turn the decisive step into rule application, so the re-root should be designed so that a stated rate cannot be the literal route. Close fork 2 and 3 as asks in the new build.

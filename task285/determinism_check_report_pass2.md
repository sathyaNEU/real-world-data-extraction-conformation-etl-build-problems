# determinism-check report (pass 2), task285, 2026-11-04

## Verdict
DETERMINISTIC, with a minor SOLUTION_WRONG (two wrong citations in SOLUTION_STEPS step 5).
**Disposition:** FIX_NOW (submission wording only; no file the solver sees changes, so no re-run).
**Stumping type:** mechanism: other (time-coincident network connectivity, analytical), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no
Bundle: target.zip sha256 f2bd06c463b2004bb7f83a5e133a0550081cdad6d81bc196be2f156f5c48591b, unzipped to 18 files. One thread, one pass.

## Order
Kept. The thread wrote derivation.md from the bundle alone before opening graded_blocks.md. Its derivation matched every graded figure before it saw the submission: six cut-off parishes, 2,093 households, six grants, all 18 dwelling counts (1,254), nine closure-hour figures, eleven unpaid amounts. It differed only in the solution wording.

## Why
Every committed answer reproduces from the shipped files. The main call turns on guidance s2 ("floodwater stands deeper than 0.25 m") read against the hourly D100CC stages: a village is cut off if at some hour no route is open, which gives six parishes. Beck dips close h12-24 and Quarnell links h30-57, never together. Each cut-off parish is stranded for 8 to 11 consecutive hours. The peak-envelope reading (nine parishes, 3,828 households) survives only as the easy route, ruled out by "stands" (a state at a time) and the staggered peak hours. No file sentence says "simultaneously", so the thread records residual risk. It is the intended analytical stump, not a lottery.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Beck / Quarnell closure windows | h12-24 / h30-57 | same (survey points via polygon and crosswalk, QRN25 D100CC) | yes |
| Cut off | Hollinside, Ravelsby Bridge, Lunnerby, Burnishaw, Wrennick, Cottergill | same, hour by hour from HBN-3224 | yes |
| Households | 2,093 | 2,093 (council tax list) | yes |
| Grants | 4,789 / 4,416 / 5,786 / 6,400 / 3,998 / 4,611 | same, sum 30,000 | yes |
| Dwellings reached | 1,254 in total, per parish as golden | same | yes |
| Closure hours | 17,15,16,5,6,8,13,3,7 | same (unrounded 16.82, 15.02, 15.75, 5.02, 6.02, 8.12, 12.80, 3.15, 7.10) | yes |
| Unpaid 2026 | eleven amounts, sum 10,574 | same | yes |

## Competing answers that survived
1. Peak versus hourly closure (main call): nine parishes against six. Closed by "stands deeper" and the stage series, with no file sentence saying "same hour". This is the declared stump, not a fork.
2. SURV08 datum sign (ask 2). The model report s5 says "the Quarnell Navigation Datum, which lies 0.42 m below Ordnance Datum Newlyn". A datum zero below ODN makes its levels read higher, so QND to ODN is subtract 0.42. The data (SURV08 sits 0.42 m below the survey's own mAOD ground at the shared UPRNs, 477 by the thread, mean -0.4206, sd 0.03) and the golden add 0.42. So a filed sentence contradicts the data. I confirmed the arithmetic. The overlap settles it (unconverted or subtracted give different counts, e.g. Cottergill 70 or 73 against 60), but a solver who maps SURV08 to QND from the report is wrong. Record as a contradiction between a filed sentence and the data, not as a pass. It is the weakest-grounded convention in the pack. The design note's own text repeats the "0.42 below" reading and cites report s3; both are wrong, and the datum is in s5.
3. Register class codes (ask 2): the register has no CLASS legend, and guidance s4 says only "home". Treating RD02-RD08 as homes is the natural reading, and the golden does. Excluding RD08 (1,023 records) moves 36 dwellings across 13 parishes (Hawkesbridge South 315 to 304). It moves the ask 2 cells only, 13 of 18 plus the total. The thread's suggested hardening, a shipped code legend, would state a data fact in plain words. It would not state an ask device, because the ask's silent device is the datum found by overlap. It does change what solvers see, so it needs a rerun.
4. Payee rule (ask 4): guidance s3 pays a clerk or village body "at the parish council's written request", and no request is shipped. If those payments are not counted, Hollinside, Burnishaw and Upper Quarnell become 1,260, 950 and 550 (from 420, 238, 132), three of eleven cells. The ledger posts each payment against the award's own reference, which supports the golden. The thread's suggested hardening, a one-line ledger note naming a request letter, would put the payee rule's condition in plain words. That removes the fork but also hands over the device of ask 4's third layer, so the author weighs it against the ask's difficulty. Posted FR25-reference instalments (Tolmarsh, Cottergill, Whinnerby) are closed by the nil-balance closed 2025 sheet and by Tolmarsh's 2,080 + 520 clearing 2,600 exactly.
Closed by the files: boundary and points readings (all give the same six, no link within 0.1 m of 0.25 m), closure site key (highways location), police row with no opening time (3.15 h either way, 3), merged parish code (guidance footnote), parent shells and flats (s4 and survey).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 18 | yes |
| Formats | 3 or more | csv, xlsx, pdf, geojson (4) | yes |
| Large file | 25,000 or more rows | address register, 27,816 rows | yes |
| Distractors | 2 or more named, none labelled in a file name | metadata.json names rest_centres_2026.xlsx, flood_warning_areas_2025.geojson, storage_area_stages_QRN25_JUL21_hindcast.csv; no file name labels one | yes |
| Distractor weight | unused by solution, relevant, ruled out by a shipped fact | hindcast describes another event; QRN23 (superseded, not named) gives the same six; I did not recompute rest centres or warning areas, and neither feeds a graded quantity | yes, with that caveat |
| Deliverables | 1 to 3, each in the golden | xlsx and pdf, both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | prompt gives whole numbers, nearest hour and pound; 18 + 9 + 11 cells | yes |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | prompt 812 chars, one paragraph, question first; about 50 graded cells plus the call; the generated rubric is not seen | yes (inferred) |
| Realism | nothing LLM-generated; goldens read as work products | thread: no authoring language, schematic geometry only, no legends for `xsp`, `LEVEL_SOURCE`, CLASS; golden realism not re-judged here | yes |

## Gate G reconciliation
Thread: mechanism other (time-coincident connectivity), analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_class analytical, gate_g method_or_model_selection, stump_strategy time_semantics, no decoy, no decisive rule filed. The design note's stump is the peak envelope laid on the roads at once against the hourly read, with the same nine against six split and the same 3,828 against 2,093 households. Match. No declared distractor carries the call: the QRN23 run files the same six, and the hindcast and the rest of the metadata distractors are off the decision. The surface read is the peak table the model report itself prints, which is the stump's easy route and not a distractor.

## Gate H
domain: pass, layers: pass, decisive_step: analytical. This agrees with the card's analyst_test and domain_test and the note's `## Three rules` (network reachability under link failures, read hour by hour; layer 1 renumbered links, BST against UTC, mixed datums, merged parish code). The thread did not class the decisive step analytical merely because the method is textbook: no filed rule performs the hourly read.

## Stump power (Gate F)
Good. A strong solver who carries guidance s4's "peak stage" into s2, or builds the closed-link graph once from the peaks, files nine parishes and a wrong grant for all (Burnishaw 3,465 against 6,400). The peak table is correct, so the failure is a skipped step and not a trap. The four asks add independent layers (datum by overlap, flats test, interval union across two clocks, ledger reconstruction with two reversed cheques). Landable by a strong solver who reads hour by hour, which the main thread weighs against the ladder.

## Findings, ranked
1. Model report s5 contradicts the data on the SURV08 sign (filed sentence against data). Ask 2 still resolves on the overlap, but the design note's "the literal comparison in ODN is the golden" does not hold on the report's words alone.
2. Payee rule's "written request" with no request shipped: three cells (ask 4) rest on the ledger's own references.
3. Register class codes have no legend: RD08 moves 36 dwellings (ask 2).
4. SOLUTION_STEPS step 5 cites model report section 3 (the datum is in section 5) and "RH" (the register has no RH class, only RD). FIX_NOW.
5. Minor: the design note quotes 433 overlap UPRNs where the thread finds 477.

## Next action for the author
Edit submission.md step 5 only: cite model report section 5, state that the 0.42 m offset comes from the SURV08 overlap with the survey's ground levels (the report's wording points the other way), and delete "RH". No re-run. Then decide whether to leave findings 1 to 3 as asks' accepted silent devices or harden (code legend, ledger note), which changes the pack and needs a rebuild and re-check.

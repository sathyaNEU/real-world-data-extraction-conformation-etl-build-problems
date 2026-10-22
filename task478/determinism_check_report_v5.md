# determinism-check report, task478 (architecture 5, run r5b), 2026-10-22

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW (one wording defect in SOLUTION_STEPS step 5; no figure, file or golden changes)
**Stumping type:** mechanism: method_or_model_selection (instrument calibration against the static reference), stumping_family: mixed, surface_read_dependency: yes (partial), sole_data_defect: yes by the clean-data test

## Why
Every committed answer reproduces from the bundle. The top five (Cole Hollow, Elk Ferry, Garnet Ridge, Jessup Fork, Kettle Run) is forced once each WIM station is calibrated against the static-scale tickets on loaded trucks' steer axles. Dunmere is sixth at 6.92 per cent against 10.99 for the fifth place, so the gap is not a near-tie. The set and the whole-per-cent shares do not move across loaded cutoffs of 40k to 65k lb or across median versus mean calibration. No semantic fork survives on the main call.

The one defect: step 5 says a T26 row "stamped up to 16 minutes before" a numeric-id row is the backfill. The files also hold T26 rows within a minute after the numeric stamp (the numeric stamp is truncated to the minute), 266 in all. Read one-sided, these stay in and citations for Ingram Mill and Lowfield become 164 and 59 instead of 165 and 58. Weekday counts do not move. Fix the wording to "within 16 minutes either side of the numeric-id stamp". The data and the main call are unaffected.

Earlier pass on the round-1 pack: run r5a, target.zip md5 feba8739, verdict DETERMINISTIC, disposition APPROVE, its verdict at /tmp/determinism-check-task478-r5a/verdict.md (the asks were re-sited after that pass; the main call and the twelve shares are unchanged between the two packs). This pass: run r5b, target.zip md5 98e0e301cbadad30cb944a1d4e14decf.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Class 9 controller-valid weighings (wim_piezo, wim_bendingplate) | 155,032 valid of 156,948 | same | yes |
| Loaded static steer-axle median (scale_house_tickets, axle sum over 50,000) | 11,420 lb, 2,583 tickets | same | yes |
| Station factors | 0.951 (CT05) to 1.066 (527) | same | yes |
| Calibrated shares, sections 1 to 12 | 5, 3, 11, 7, 16, 3, 21, 6, 4, 11, 11, 5 | same (11.16, 16.14, 21.12, 10.99, 11.13; Dunmere 6.92) | yes |
| Weekday entries per section | 58, 58, 26, 55, 23, 55, 22, 31, 52, 27, 41, 54 | same (total 502) | yes |
| Gross overweight citations | 65, 173, 68, 178, 52, 168, 61, 107, 165, 63, 121, 58 (1,279) | same | yes |
| Station to section (wim_stations.csv, by milepost) | one-to-one, station 514 re-site inside section 2 | same | yes |

## Competing answers that survived
Main call: none. Supplementary asks: one defensible-looking fork, the one-sided backfill window (citations Ingram Mill 164, Lowfield 59), which comes from the step 5 wording and not from the files. The shipped rule that closes it is the data itself (stamps within a minute after the numeric stamp are duplicates) once the wording says "either side". Ruled out by data or shipped rule: keeping backfill rows as UTC, T26 as local, no dedupe, numeric stamps as UTC (the hour-of-day profile shows numeric stamps are local), and keyed `entry_plaza` as placement (program 6.2 rule on the trip on which the scale house weighed it).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | yes |
| Formats | 3 or more | 4 (csv, txt fixed width, xlsx, pdf) | yes |
| Large file | 25,000 rows or more | wim_piezo 141,557; toll_entries 162,926; wim_bendingplate 69,155 | yes |
| Distractors named in metadata.json, none labelled in a file name | 2 or more | 2 (pavement_condition xlsx, bridge_postings csv), names carry no label | yes |
| Distractors unused yet weighable | each | pavement damage and bridge postings are relevant to heavy trucks but answer no graded quantity; metadata states the shipped reason each is not the share over the limit | yes |
| Deliverables | 1 to 3, all in golden | 3 (xlsx, csv, svg), all present in golden/ | yes |
| Asks multi-dimensional with unit and rounding | each | per-section share, weekday entries and gross citations over twelve sections; prompt states whole per cent, whole numbers | yes |
| Prompt shape and rubric 25 or more criteria | identifiable, 25 or more | shape 01 (ranked slate under cap); 12 sections x 3 figures plus the set of five gives about 37 gradable cells plus deliverable and instruction items; not counted by me against a generated rubric | yes (by shape) |
| Reads as real, not LLM generated | all | judge found no authoring or benchmark language, dictionary names clocks but not the calibration; golden files are a section table, a plain csv and a chart | yes |

## Gate G reconciliation
The thread's line: mechanism method_or_model_selection, stumping_family mixed, surface_read_dependency yes (partial), sole_data_defect yes by the clean-data test. The card declares stump_class analytical with layer2_family field_method (an instrument's multiplicative bias measured on a load-independent component, matched by load state to a static reference), stump_strategy other, no decoy, no decisive rule filed. These match: the thread names the same calibration against the static reference as the decisive work, and names the recorded WIM weights (the unadjusted share) as the surface read, which is the card's analyst-test easy route, not a declared distractor. The declared distractors (pavement survey, bridge postings) were not named as carrying the task. The thread's "borderline, route to live testing" on sole_data_defect is recorded: with unbiased stations the task would collapse to ranking raw shares, but the calibration reference and the like-for-like loaded population are a method choice, and the pooled version fails on honest ticket data. No send-back mismatch found.

## Stump power (Gate F)
Two easy routes fail: using the weights as recorded (raw top five is Garnet Ridge, Jessup Fork, Cole Hollow, Ingram Mill, Brannock; Elk Ferry at 2 per cent) and calibrating on all class 9 trucks pooled (Dunmere comes in third). Getting the golden needs the loaded steer-axle matching. Gate H line: `domain: pass`, `layers: pass`, `decisive_step: analytical`. Caution for the main thread: calibration of an instrument against a reference is a field-standard method, and the thread did reach the golden by applying it with a choice (load-state matching) the data had to settle, but stumping power is plausible, not certain. Weigh this with the scored readers' result.

## Findings, ranked
1. Step 5 backfill wording is one-sided ("up to 16 minutes before"); it leaves 266 within-a-minute duplicates in, moving Ingram Mill and Lowfield citations by one each. Wording only.
2. Optional: state in step 3 that the loaded definition is the same 50,000 lb axle sum on the WIM side and the ticket side. Shares do not move across 40k to 65k.
3. Borderline sole_data_defect, routed to live testing; no change.
4. Files and hygiene pass: row counts match the dictionary, dates coherent (program 12 Feb 2027, data to 31 Dec 2026), no answer hints.

## Next action for the author
Reword step 5 of submission.md (SOLUTION_STEPS) so the backfill match reads "a T26 row of the same tag and plaza within 16 minutes either side of the numeric-id stamp is the new host's backfill and goes". No input file, golden or figure changes and no re-judge are needed.

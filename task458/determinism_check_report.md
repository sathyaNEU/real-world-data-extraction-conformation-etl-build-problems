# determinism-check report, task458 (architecture 2), 2026-11-02

## Verdict
NOT_DETERMINISTIC (SOLUTION_WRONG only on one step-wording point: "6 to 11 seconds" does not match the feed)
**Disposition:** SEND_BACK
**Stumping type:** mechanism: etl_conformance, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The golden reproduces from the shipped files (all 18 zones, all 8 pilot cells), but only under conventions no shipped text states.
- **Main call.** Rule 12.04 counts a vehicle "whether or not that vehicle paid". Nothing says how point-in-time plate reads become occupied minutes in the noon-to-2 p.m. window.
  - The neighbourhood routes have only a mid-morning run and a mid-afternoon run, so no read falls inside the window.
  - The golden counts only plates unpaid on both bracketing runs. That rule is in the author's text only, not in the prompt or Rule 12.
  - Reading the mean distinct unpaid plates per run times 120 minutes is equally licensed. It moves 5 zones across a line and the rate decision changes for each.
  - Governing label: underspecified_objective. Gates C and E fail on the main call.
- **Pilot-street asks.** Three conventions are unfiled, and each changes whole-minute or whole-per-cent cells (see the pilot ledger rows below).
  - The flicker threshold.
  - Whether a silent sensor is unmeasured.
  - Which stays count as "begun on those weekdays".

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| 38 weekdays (8 Sep to 30 Oct less 12 Oct) | 38 | 38 (ics, Rule 12.03) | yes |
| Zone occupancy D01, D02, D03, D04, D05, D06 | 89, 78, 73, 53, 91, 67 | 88.98, 78.06, 73.12, 53.06, 91.23, 66.95 | yes |
| Zone occupancy N01 to N06 | 79, 52, 79, 66, 91, 55 | 79.03, 52.11, 79.24, 66.01, 91.11, 55.04 | yes |
| Zone occupancy N07 to N12 | 75, 79, 53, 70, 77, 64 | 74.99, 78.97, 53.03, 70.00, 77.16, 64.19 | yes |
| 2027 schedule (3 raise, 4 lower, 11 hold) | as filed | same | yes |
| Pilot occupancy Sep/Oct: Tamarack, Wexford, Ostrander, Pell | 61/73, 49/52, 78/77, 35/37 | same | yes |
| Pilot average stay Sep/Oct, minutes (same order) | 145/151, 187/163, 140/139, 178/180 | same | yes |
| Solution step 6 flicker gap "6 to 11 seconds" | 6 to 11 s | feed has 6,167 gaps of 2-5 s and none at 6-11 s (next gap 14 s) | no (wording wrong; merging up to 11 s still reproduces) |

## Competing answers that survived
1. **Unpaid-to-window imputation (main call).**

| Zone | Golden (bracket) | Mean-count reading | Rate decision change |
|---|---|---|---|
| Alder Row | 79 | 95 | hold to raise |
| Cascade Avenue | 79 | 95 | hold to raise |
| Hollis Street | 79 | 91 | hold to raise |
| Fernwood | 55 | 71 | lower to hold |
| Irvine Market | 53 | 71 | lower to hold |

   - Under the mean-count reading the schedule is raise D01, D05, N01, N03, N05, N08; lower D04, N02; hold the rest.
   - The other tested readings:
     - Paid sessions only gives 8 lower and 0 raise.
     - Unpaid on either bracketing run gives Alder Row 111, Cascade Avenue 111, Hollis Street 103, Fernwood 87 and Irvine Market 90, all raise.
   - No shipped rule closes the fork. In the neighbourhood zones 2,220 plate-days are unpaid on both runs, against 3,828 on run 1 and 3,543 on M, so the singles are large and their presence in the window is unknowable from the files.
2. **Pilot flicker.** Merging at 11 s gives the golden. No merge gives stays Tamarack 114/117, Wexford 126/117, Ostrander 113/113 and Pell 120/120. Merging up to 60 s changes 5 of 8 cells. Occupancy is unaffected.
3. **Pilot silent sensors.** Counting the stopped sensors as vacant gives occupancy Tamarack 57/66, Wexford 46/46, Ostrander 73/71 and Pell 33/33.
4. **Pilot "stays begun on those weekdays".** Stays begun 08:00-18:00 give Tamarack 115/126, Wexford 127/130, Ostrander 115/120 and Pell 126/122. Stays begun 12:00-14:00 give 85/85, 66/71, 95/92 and 65/64. The all-hours reading is the one that reproduces the golden.
5. **Smaller points that move no decision.** Inclusive versus exclusive session endpoints, 166 reads duplicated at the same second, and plate pairs in different faces of one zone. The one-character plate confusions touch 642 unpaid reads and move no zone at 2 decimals.

## Spec gates
Checked by me against the unzipped bundle, metadata.json and the golden folder.

| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | yes |
| Formats | 3 or more | csv, xlsx, pdf, ics | yes |
| Large file | 25,000 rows or more | feed 160,298 data rows; LPR 87k; CurbTrack 81k; StallPay 78k | yes |
| Distractors | 2 or more, named in metadata, no file name labels one | city_garages_monthly_2026.xlsx and parking_service_requests_2026.csv; neither supplies a decisive input; names carry no label | yes (the judge saw no decisive use) |
| Distractor weighs but is ruled out | relevant enough to weigh; a shipped fact rules it out | Garages are not on-street zones (Rule 12 sets on-street rates only) and complaints are not occupancy; neither reproduces a graded quantity | yes |
| Deliverables | 1 to 3, all in the golden, no format family required | 2 (docx, csv), both present in `golden/` | yes |
| Asks multi-dimensional with unit and rounding | each ask states unit and rounding | Zone and pilot asks cross zone, street and month; prompt gives whole per cents, whole minutes and rates to the cent | yes |
| Prompt shape and rubric | shape identifiable; rubric reaches 25 or more criteria | Shape 10, scorecard (metadata); the rubric is generated at grading, so I did not count it | shape yes; count not verified |
| Not LLM-generated | reads as a real work product | The judge found the pdf and ics read as municipal artifacts; I did not review the golden docx for realism | no finding |

Spec gates pass. The failure is determinism, not spec.

## Gate G reconciliation
Read from the design note, metadata.json and the card after the thread returned.
- **Match on the stump.** The thread's mean-count reading is exactly the design note's declared default path (Alder Row 95, Cascade Avenue 95, Hollis Street 91; Fernwood 71, Irvine Market 71). The thread independently found the five-zone split the author designed.
- **Mismatch on the filing.** The card says `stump_class: analytical`, with the bracket reading as Layer 2 population selection. The thread says the decisive step is `rule_application` under an unfiled convention, and that the data cannot separate the bracket from the mean.
  - The design note states no validating evidence and no filed sentence that forces the bracket.
  - The note's own wording ("a model downtown's in-window 12:30 run confirms") concedes that a shipped run supports the wrong reading. The thread did not name that run as a Gate G breach, and I am flagging it for the main thread to weigh. No other shipped artifact ranks the candidates wrongly.
  - A mismatch of this kind is the finding that most reliably predicts a send-back.
- **Surface read and distractors.** `surface_read_dependency: no`. Neither declared distractor carries the call, so the distractors are not too load-bearing.
- **Gate H.** `domain: pass`, `layers: pass`, `decisive_step: rule_application` (fail).
  - The decisive step executes Rule 12.04 plus a bracket convention that no shipped text gives.
  - That is the "withheld rule" shape the project bans as a decisive step.

## Stump power (Gate F)
- Paid-only files no raise; the mean-count reading files 6 raises; the bracket reading files 3 raises. Solvers would diverge.
- The divergence rests on an unfiled imputation convention, not on a data-forced analytical error, so it is not a valid stump.
- The bracket rule is a defensible lower bound and the mean is a defensible interpolation. A strong analyst who read every file could not tell which the author meant.
- The pilot-street asks stump on conventions the files never state.

## Findings, ranked
1. **(Blocking)** The unpaid-vehicle-to-window convention is unfiled, so the main call has two licensed readings that change 5 zones' rates.
2. **(Blocking)** The pilot conventions are unfiled: flicker threshold, silent sensor treated as unmeasured, and which stays count as begun on those weekdays.
3. **(Wording)** Solution step 6 says "6 to 11 seconds" but the feed's flicker gaps are 2-5 s. This is an integrity mismatch inside the submission.
4. **(Process)** The bracket reading carries the stump but has no filed sentence or in-data validation forcing it.
5. **(Note)** The cross-batch fingerprint check against delivered tasks could not be run from the thread.

## Next action for the author
Rework the generator so the shipped files force one reading.
- **Main call.** File the WHAT in Rule 12.04: which vehicles count as occupying a space for the window, as a population. Do not file the HOW. Alternatively add in-window ground truth so a back-test separates the bracket from the mean.
- **Pilot asks.** File in the sensor documentation or the prompt what a flicker is, that a silent sensor is unmeasured, and the hour range of "stays begun on those weekdays".
- **Step 6.** Correct the "6 to 11 seconds" wording to match the data.

Then rebuild and re-judge once, via `/fix-determinism`.

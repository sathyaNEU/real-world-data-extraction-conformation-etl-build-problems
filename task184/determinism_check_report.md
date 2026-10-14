# Determinism check, task 184 (mobile screening unit posting, summer 2027)

## Verdict and disposition
- **Verdict:** NOT_DETERMINISTIC (Gate C, competing_defensible_answer / underspecified_objective). The figures themselves all reproduce. Arguable call: if the author's reading of "lanes open" is accepted as forced, the verdict is DETERMINISTIC and the task still fails Gates G and H.
- **Disposition:** SEND_BACK. The decisive step has to be rebuilt, which changes what solvers see, so a model rerun is required.

## Reproduced from the bundle (own Python code path)
| Item | Result |
|---|---|
| Passenger lanes vs staff lanes | Two lanes per airport screen only before 05:00 and from 21:00 (624 rows each). Excluded. |
| Bank lanes (own-day open lanes against the roster pattern) | ESK 2, HAL 0, the other six 1. Reproduced. 2027 pattern = 2026 pattern at every airport and interval. |
| Posted-day lane levels | Constant by interval across all posted days (ARD 21 days, CUL 14). Reproduced. |
| Summer effect per standard s.4 and s.6 (37.5 lanes, queue start-of-interval + half arrivals, days 16/31/31) | ESK 342,178; HAL 272,593; ARD 240,764; CUL 231,892; FAR 202,773; GLK 163,701; BRN 145,935; DRM 135,425. All 8 match the golden to the hundred. |
| Flip | ESK scaled by (1 - k%): k = 1 to 12 all above 272,593 (k = 12 gives 286,763). k = 13 gives 266,957, below HAL. Smallest whole cut is 13. Same with arrivals rounded to integers. Reproduced. |
| 2026 summer pax (passenger lanes + unit lanes, staff lanes out) | All 8 reproduced (ESK 842,213 etc.). |
| Hotel EUR per officer-night | All 8 reproduced (invoices + credits by PO, accommodation-line nights; ARD PO-4214 invoice spans two postings, 497 nights). |
| Expense claims EUR per posting week | All 8 reproduced after dropping the 968 exact duplicate (claim_ref, line_no) rows and assigning each claim to the posting week of its SUBS-DAY dates. |
| Not reproduced | None. |

## Gate A: PASS
Every figure reproduces. Blocks agree with each other.

## Gate B: PASS with a note
All inputs are in the files. The note is the same one as in Gate C: no file states that the 2026 bank-lane closures and the posted-day stand-down carry into 2027. Both are recoverable only from lane_counts against roster_plan_summer2026.csv.

## Gate C: FAIL
Literal execution of the shipped text: the prompt and deployment policy say to judge "as the checkpoint planning standard (s.6) sets out on Capacity Planning's summer planning sheet". s.6.1 needs the "lanes open without / with" the change in summer 2027. The only 2027 lane source is roster_pattern_summer2027.xlsx, which extract_notes calls "lanes planned for the checkpoint's own officers". No document says hosts stand lanes down while the unit is posted. No document says the bank lanes stay closed. The unit's lane count (3, 05:00 to 21:00) is filed.

Readings I computed (nearest hundred):
| Reading of the lanes | Winner | ESK | HAL | CUL |
|---|---|---|---|---|
| A. Pattern as lanes open, +3 (the literal 2027 file) | CUL | 398,400 | 360,300 | 697,500 |
| B. Observed own-day lanes (bank lanes closed), +3, no stand-down | CUL | 531,800 | 360,300 | 814,900 |
| C. Golden: observed own-day lanes without; observed posted-day lanes +3 with | ESK | 342,200 | 272,600 | 231,900 |
| D. Pattern without; observed posted-day lanes +3 with (mixed basis) | HAL | 208,700 | 272,600 | 114,500 |
| E. Pattern without; pattern less stand-down +3 with | ESK | 293,300 | 272,600 | 197,700 |

- Reading C is the only one consistent with all the 2026 evidence and with s.3.1 ("open lane = staffed and screening"). That is a real argument for it. But carrying 2026 behaviour (the eight hosts' stand-down and the bank closures) into 2027 is an inferred forecasting assumption, never filed. A rigorous solver who takes the 2027 pattern as the 2027 lanes (A) gets CUL with no arithmetic slip. CUL is also what the golden itself names as the naive answer. Under the "fork closed only by inference is open" rule, this is an open fork on the main call.
- Secondary fork on the graded figures: whether the two staff lanes count as lanes open before 05:00 and from 21:00. The policy sentence ("checkpoints search their own staff and aircrew") and the match to the operator returns close it by inference. Counting them as open gives ESK 336,300 and ARD 236,900, so the hundred-rounded figures move. The call does not.
- Tertiary fork, supplementary 4: two CC-4109 claims have SUBS-DAY dates outside every posting week (EC26-61697 on 11 June, EC26-61698 on 31 August). The golden drops them. Attaching them to the adjacent posting gives CUL 7,166.92 (golden 7,135.92) and ARD 7,384.98 (golden 7,339.69). No sentence in the prompt or files says to drop them.
- Margin: ESK leads HAL by 69,600 under C and by 13 per cent of ESK's forecast. That is robust within C. The risk is the reading, not the margin.

## Gate D: borderline
The split would be on which lanes count as open in 2027 (reading), not on analysis of the same lanes. Contrasting runs were not supplied.

## Gate E: PASS for the main ask
The prompt pins window, standard, unit and rounding. Neither the prompt nor the bundle says that bank-lane closure or host stand-down is to be modelled.

## Gate F: stump power
Substantial. Reading A (CUL, 697,500) is the natural first answer, and a strong model that checks the roster against the feed will find both effects, so it is not trivial. Models that stop at the roster file fail. The trap does the work through "catch that the roster overstates open lanes". Fair chance of at least 2 GPT stumps. The weakness is that this failure is the fork above.

## Gate G: FAIL, banned_stumping_type
`mechanism: planted_defect_flip`, `stumping_family: surface_read_rejection`, `surface_read_dependency: yes`, `sole_data_defect: yes`.
The reported surface read is the 2027 roster pattern (planned lanes). The solver must reject it in two ways: seven checkpoints never open one or two of their bank lanes (HAL none), and hosts stand down 2 to 4 of their own lanes on posted days. Take both out and the clean-data answer is CUL by a wide margin. Adding the second correction does not rescue the shape.
The surface read being wrong is not, by itself, a sufficient trap, and adding more corrections does not fix it. Rebuild the difficulty where the reported numbers are FINE (see Fix).

## Gate H: FAIL
`domain: pass (borderline)`, `layers: pass`, `decisive_step: planted`.
- H1: capacity planning of checkpoint queues is the field's own work. But the queue recurrence and s.6 are filed in full, so computing the effect is rule application. The quantity that decides the call (the lanes open) is not estimated by any method the field uses. It is read from planted regularities.
- H2: Layer 1 is the 15-minute feed with fault gaps, the change of standard 2023 to 2026 (140 to 150 per hour, queue at end to start), the duplicated expense export, the shared ARD invoice and the credit note. Layer 2 should be the net additional capacity of a posting.
- H3: the call turns on a host stand-down on posted days and on bank lanes that the roster plans but the checkpoint never opens. Both are inserted regularities in the lane feed that no document states. This is a planted hidden rule. The easy route (pattern + 3, reading A) gives CUL 697,500; with stand-down left out and bank lanes removed (B) it gives CUL 814,900. A strong analyst who cleaned the data and read every rule correctly would still pick CUL on A or B. That reading is wrong only because of the hidden rule, so H3 fails as planted. Calling the stand-down "additionality / net effect" is the nearest analytical frame, but nothing in the files makes the net effect the filed estimand.

## Hygiene: PASS
- 17 files, 5 formats (csv, pdf, xlsx, md, json). The lane feed has 267,568 rows. Distractors: detector flags json, passenger feedback, queue sensor file, 2023 standard (explicitly replaced by 2026 s.1.2), operator returns.
- Temporal coherence is fine (extract 23 April 2027; roster 21 April; detector 19 April; policy 2 March).
- Business-realistic: duplicated expense rows, credit note, shared invoice, fault log, all plausible.
- No provenance leakage seen. The extract notes are in-fiction.
- Cross-batch check not possible (no other tasks in scope).

## Fix (SEND_BACK)
- Keep the world, the standard and the feed. Make the deciding quantity something the field estimates, with FINE numbers: for example a forecast of the checkpoint arrivals or show-up profile (the planning sheet is itself a forecast) validated out of sample against 2026 actuals, or a method choice between the queue model and the sensor-measured waits, pinned by back-test. Then the lanes open come from the filed pattern and the unit's three lanes, with no unstated stand-down.
- If the stand-down stays as the stump, file the estimand (lanes open on the days the unit is posted = the lanes the 2026 feed shows open on posted days) and drop the bank-lane closures from the decisive step. That fixes the fork but still leaves a rule-recovery stump (H3).
- File how to treat the two stray CC-4109 claims (supplementary 4) and the staff lanes in the 2026 totals (supplementary 2).

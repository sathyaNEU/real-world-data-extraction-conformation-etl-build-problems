# determinism-check report, task192 (architecture 4), 2026-11-04

## Verdict
NOT_DETERMINISTIC (asks 4 and 5 only, taxonomy underspecified_objective). The main recommendation is deterministic and the golden is not wrong on it.
**Disposition:** FIX_NOW
**Stumping type:** mechanism: signal_vs_noise, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The isolated thread reproduced the main call (MLR-2, SYC-3 second) and ask 6 on all 16 feeders. Ask 4 (minutes, 1 dp) and ask 5 (momentary events) carry unfiled conventions.
1. SOE second against OMS minute: the golden minutes reproduce only when a ticketed device interruption is timed from the OMS ticket's minute and a ticketless SOE opening from the SOE second. DRP-04 does not say which clock governs. Timing everything from the SOE second moves nine feeders by 0.1 to 1.5 min, enough to change the 1 dp cell (BLV-1 308.4 against 307.0, NYD-2 411.5 against 410.0, SYC-3 356.1 against 355.0).
2. Planned interruptions: DRP-04 2.2 and 3.1 do not exclude them, and the golden includes them (the literal reading). Excluding them moves 10 minutes values and the CEMI counts of BLV-2 (6 against 7) and MLR-2 (1,026 against 1,030).
3. Customers served at the boundary: service point 56626244 (NYD-3) is disconnected on 31 Oct. The golden treats it as not supplied (generator test `disconnected > day`). DRP-04 2.1 says "supplies on the last day". If it counts, NYD-3 ask 5 moves from 44.83 to about 44.81 or 44.82.
4. CTR-1 and CTR-2 MAIFI-E: the thread gets 43.03 and 37.42 against the golden's 43.00 and 37.35. The golden is the one that departs from the shipped text (see the CTR diagnosis below).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| MLR-F2-52 phase C faults | 11 at 1,423 to 1,448 A | 11, separate days 14 Aug to 31 Oct | yes |
| R-3114 phase A faults | 7 at 996 to 1,005 A | 7 from 23 Sep | yes |
| Next largest same-phase same-current group | at most 5 | at most 4 (BLV-F3-52 phase B has 17 spread 1,266 to 3,085 A) | yes (claim is an upper bound) |
| Customers behind MLR-F2-52 / R-3114 | 2,625 / 863 | 2,625 / 863 | yes |
| MEDs | 19 May, 27 June | 618 and 1,405 min against TMED 38.03; next day 21 min | yes |
| Ask 4 minutes | 16 feeders | exact only under the hybrid timing | conditional (fork) |
| Ask 5 MAIFI-E | 16 feeders | 14 exact; CTR-1 43.03, CTR-2 37.42; NYD-3 at the margin | no (3 feeders) |
| Ask 6 CEMI-2 | 16 feeders | exact | yes (planned-interruption fork moves BLV-2, MLR-2 if excluded) |

## Competing answers that survived
- Ask 4: OMS minute or SOE second for a ticketed device interruption (nine feeders move, the 1 dp cell changes). Nothing shipped closes it.
- Asks 4 to 6: planned interruptions in or out. The literal text keeps them; IEEE practice drops them. Nothing shipped closes it.
- Asks 4 and 5: a service point disconnected on 31 Oct served or not. DRP-04 2.1 is silent on the boundary day.
- Ask 5, CTR-1 and CTR-2: a sustained interruption that starts 1 to 2 minutes after the event's minute absorbs the event (golden) or does not (literal DRP-04 2.5 and the submission's own step 6). Two events carry it.
- Main call: no surviving fork. MLR-2 first under every band, window and grouping the thread tried.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, geojson) | yes |
| Large file | one of 25,000 rows or more | service points 35,907 rows, lightning strokes about 39,364 | yes |
| Distractors named, none labelled by file name | 2 or more | 3 in metadata.json (line_clearance_work, blinking_lights_contacts, lightning_strokes); no file name labels one | yes |
| Distractors unused, weighable, none answers a graded quantity | yes | none feeds a graded figure; each is plausible context (vegetation, customer contacts, lightning); the shipped clearance log rules out the vegetation reading for MLR-2 | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, svg), both in golden/; the xlsx also holds Repeat faults and Notes sheets | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 16 feeders by three indices; minutes to 1 dp and events to 2 dp stated; the count ask has a natural unit | yes |
| Prompt shape and 25 or more criteria | shape identifiable, 25 or more | shape 07 grid; 16 feeders by 3 indices plus call, stretch, second and reason, chart gives well over 25 (no generated rubric is in the folder to count) | yes (on the grid) |
| Prompt form | one paragraph, under 1,000 chars | 775 chars, one paragraph | yes |
| Reads as real, goldens business-realistic | yes | thread found no authoring text and mixed CST and CDT clocks; golden wording reads as a desk note | yes |

## Gate G reconciliation
Thread: mechanism signal_vs_noise, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: strategy grain_or_unit, Layer 2 family field_method, gate_g decomposition_attribution, official_decoy false, stump_class analytical. The vocabularies differ but the substance matches. Both name the decisive step as grouping each device's momentary operations by faulted phase and recorded current across separate days. Both find no planted defect and no shipped ranking. Both name the surface reads as NYD-3 (the default path), NYD-2, BLV-3 and SYC-3. None of the three declared distractors (clearance log, blinking-lights contacts, lightning) is the surface read that carries the task, so the distractors are not too load-bearing (lightning and weather feed only the default path's storm screen). No mismatch.

Gate H (thread): domain pass, layers pass, decisive_step analytical. Card: stump_class analytical with analyst_test and domain_test. Match. The thread did not class the step analytical merely because the method is the field standard: it found the deciding rule unfiled and the data separating 11 against at most 7.

Two design-note gaps the thread surfaced. The fork table has no row for the OMS minute against the SOE second, for planned interruptions, or for the boundary day of a disconnect. SF17 says "in the event's minute" while the generator absorbs sustained starts within five minutes after the first trip.

## Stump power (Gate F)
Strong. The easy routes (momentary count per mile against 2025, damp-morning count, phase share, worst SAIDI) land on NYD-3, NYD-2, BLV-3 or SYC-3 and never MLR-2; only phase-and-current grouping exposes it. Nothing shipped ranks the candidates, and the decisive step needs no judgment about data semantics. The thread did not class the step analytical on the grounds of a standard method. Recorded for the main thread: the asks are the field's indices (SAIDI, MAIFI-E, CEMI-2), executed by rules, so their difficulty is rule application, which is allowed for asks.

## CTR diagnosis (read from the generator, nothing modified)
The thread's reconstruction is the more literal one and the golden departs from the shipped text. I ran a copy of the generator in /tmp and found that exactly two events carry the gap:
- CTR-1, 17 Jun 2026, R-3774 event: fuse F-90681 blew 1 minute after the event's minute and the golden absorbs 47 customers into its sustained interruption.
- CTR-2, 26 Jul 2026, CTR-F2-52 event: fuse F-25481 blew 2 minutes after and the golden absorbs 120 customers.

The golden's rule in `truth.py` absorbs any sustained start from the event's minute to the first trip plus 5 minutes. Submission step 6 says "whose fuse or transformer fuse blew in the event's minute", and DRP-04 2.5 says only that momentary interruptions that "end in a sustained interruption" are part of it. Counted literally, the 47 and 120 customers keep their momentary event. That gives CTR-1 about +47 (43.03) and CTR-2 about +120 (37.42), which matches the thread's +44 to +48 and +126. It is not a Cotter rename error; the rename, the tap transfers and CEMI reproduce. Both cells are therefore wrong under the filed wording or the wording is underspecified; the golden is not the stable reading.

## Findings, ranked
1. Ask 4 timing convention (OMS ticket minute against SOE second) is unfiled and moves nine cells at 1 dp. Competing defensible answer exists.
2. CTR-1 and CTR-2 MAIFI-E: golden uses a 5-minute absorption window that neither DRP-04 2.5 nor step 6 states; literal reading gives 43.03 and 37.42.
3. Planned interruptions in or out: unfiled, moves 10 minutes values and two CEMI counts.
4. Disconnect-on-last-day service point 56626244 (NYD-3): customers served 2,937 against 2,938, ask 5 for NYD-3 at the rounding margin.
5. Design note fork table lacks rows for findings 1, 3 and 4 and SF17 disagrees with the generator (finding 2); `precut.py` would not catch these as written.
6. Minor: golden "no other feeder carries more than 5" is true but the data max is 4; harmless.

## Next action for the author
Fix in the generator and DRP-04 text only; the main call, the faults and the ladder stay frozen. File the WHAT, not the method:
1. DRP-04 2.4 or 2.5: state that an interruption's start and end are taken from the outage record when one exists and from the SCADA log when none does.
2. DRP-04 2.2 or 3.1: state whether planned interruptions count (the golden includes them, so say they do) and in 2.1 that a service point disconnected on or before the last day is not served (as the golden counts it).
3. DRP-04 2.5: file the absorption window (a sustained interruption beginning within five minutes of the first trip), or change the generator to the event's minute as step 6 and SF17 state and regenerate CTR-1 and CTR-2 MAIFI-E (about 43.03 and 37.42). Keep step 6, SF17 and the generator on one reading.
4. Add the fork rows (timing source, planned, boundary day) to the design note, assert them in `checks.py`, rebuild twice byte-identical, then re-judge once (asks 4 and 5 only).

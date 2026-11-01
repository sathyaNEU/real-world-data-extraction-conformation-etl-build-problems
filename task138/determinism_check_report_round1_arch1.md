# determinism-check report, task138, 2026-10-12

The determinism judge's verdict (one isolated thread at medium effort, on the pack and prompt as built at stage 3), verbatim:

## Verdict, task138 (Kestrel Bend Irrigation District 2027 order)

**Verdict:** DETERMINISTIC (conditional on one residual fork, see Why and Evidence). Every committed figure reproduced from the shipped files.

**Disposition:** APPROVE. No solution-block repair is needed. Optional in-house pin: one sentence in WOP 2.4 or the prompt saying the replay starts from the root-zone depletion carried through 31 January 2027 from each field's last delivered 2026 set. That would also remove the fork below. It is a procedure-text edit that changes what solvers see, so it would need a rerun.

**Why:**
- The answer is forced by WOP 2.3, 2.4 and 3.1 to 3.5 read literally. WOP 3.1 defines each day's depletion from the previous day's, and 3.4 resets a field to zero on the day of an irrigation. For 1 February the previous day is 31 January. That value follows from the last Delivered 2026 set in the orders file, the Table 1 coefficients (which include Nov to Jan), and the station records, which run to 31 January 2027.
- The weakest point is that WOP 2.4 never states the 1 February starting depletion. A reader who starts every field at field capacity gets a different order (see Evidence). I judge that reading unlicensed rather than equally licensed, because the files let the 31 January state be computed. The risk is real and I flag it.
- A second boundary risk: the 24th value (202,658 af) sits 42 af below the 202,700 hundred-boundary, so non-literal unit-conversion choices move the order.

**Evidence** (recomputed independently from the bundle; no use of answer_key, generator or submission):

| Item | Recomputed | Golden | Source |
|---|---|---|---|
| Accepted fields / acres | 619 / 39,399.33 | 619 / 39,399 | water_requests Accepted rows; every field has one accepted version, 10 withdrawn have none |
| Acre-weighted depletion at end of 31 Jan 2027 | 3.388 in | 3.39 | last Delivered 2026 set date (set_end), weather splice, Tables 1 to 3 |
| Fields at or past allowable depletion | 446 | 446 | same |
| 24th smallest replay | 2012, 202,658 af | 2012, 202,660 | 30 replays 1997 to 2026 |
| Order | 202,700 | 202,700 | WOP 2.3 |
| Monthly schedule | 13,520 / 970 / 10,290 / 27,190 / 37,470 / 42,010 / 37,270 / 24,010 / 9,970 | identical | WOP 5.1 |
| Chart order | smallest 2024 (156,207), largest 2002 (211,091) | same | |
| Lateral 2026 deliveries (af) | 17,820 / 19,608 / 12,800 / 16,959 / 16,501 / 17,299 / 13,880 / 14,432 / 18,210 | 17,820 / 19,610 / 12,800 / 16,960 / 16,500 / 17,300 / 13,880 / 14,430 / 18,210 | meter book with shop-log register splices, rollover at capacity, hundred-cubic-foot meters converted, Lateral 5 tail turnouts to Lateral 6 after their 15 June read |
| Share not delivered (%) | 8.71 / 9.60 / 8.53 / 14.90 / 8.30 / 13.88 / 8.00 / 12.32 / 13.20 | 8.7 / 9.6 / 8.5 / 14.9 / 8.3 / 13.9 / 8.0 / 12.3 / 13.2 | headings daily including E days |
| Tail weir spill (af) | 579 / 631 / 440 / 270 / 548 / 650 / 511 / 419 / 361 | 580 / 630 / 440 / 270 / 550 / 650 / 510 / 420 / 360 | weir equation, crest raised 2 in per board per the remarks, reading held to the next reading |

- Rank robustness: the 23rd value is 2000 at 201,412 and the 25th is 2003 at 204,982, so the choice of the 24th year is stable.
- Competing answers, with their cause:
  1. Start every replay at field capacity (zero depletion): 24th is 2003 at 189,785, order 189,800. This is the main fork; the text is silent on the start and a common modelling default gives it.
  2. Half-allowable-depletion start: order 190,900. Not licensed by any text.
  3. Rounding the station 39 inch values to 0.01 in (yard convention): 24th is 2012 at 202,398, order 202,400.
  4. Converting at 0.0394 in/mm: order 202,800.
  5. Conversions 3 and 4 are non-literal. The exact 25.4 mm/in is canonical but unstated, and the margin to the 202,700 boundary is only 42 af (0.02 percent). This is a thin-and-mildly-contested margin, not disqualifying.
- Lateral for the 14 reach turnouts (05-045 to 05-058): the register (WOP 6.2) puts them on Lateral 6, while their request turnout prefix says 05. The golden follows the register. 20 fields differ in total.
- No correction factor is shipped for the "bearing worn, under-reading" meters, so as-read values stand. A solver cannot compute a correction, so this does not fork the answer.
- Flashboard sequences resolve unambiguously (set, added, pulled one, pulled boards) from an initial zero. The last delivered sets all start and end on the same day, so there is no start-day versus end-day fork.
- Cross-batch reference check: not performed (other task folders are forbidden to this reader). No overlap seen within the bundle.

**Files/Hygiene:** PASS. 18 files in 5 formats (csv, xlsx, pdf, docx, txt). Large files: irrigation orders 64,887 rows, meter book 16,334 rows. Distractors present (groundwater levels, 2026 crop report, TVWA allocation notice, headings and tail-weir files being used only by the lateral asks). Minor points, none exclusion-level:
- README_order_working_files.txt reads as a tidy index.
- The data dictionary's remark "Both are the District's record of the day" and its Superseded and Cancelled definitions state data semantics a little too cleanly.
- Station 39 looks like a renamed state network download. I found no sign that its canonical analysis equals the golden, so no contamination.
- Dates are consistent with a 1 February 2027 snapshot.

**Stump power:** Moderate to good.
- The trap is the starting state. A solver who starts at field capacity gets 189,800 against 202,700, a 6.4 percent gap.
- Cues that a careful solver can find: Nov to Jan coefficients in Table 1, weather through 31 January 2027, and the last-set data in the orders file. The Cancelled versus Delivered distinction in the late-season orders is a lower decoy.
- The many lateral asks (rollovers, units, shop-log splices, estimated days, connector, flashboards) add separate graded failure points.
- The risk to difficulty validity is the unstated initial condition (see Why).

**Stumping type:**
- mechanism: forecasting
- stumping_family: analytical_non_defect
- surface_read_dependency: no
- sole_data_defect: no

The reported figures are fine and nothing the solver is handed is overturned. The difficulty is carrying the root-zone state through the winter and replaying thirty weather years at the 80th percentile. The task would still stump on perfectly clean data.

**Three rules:**
- domain: pass
- layers: pass (Layer 1 is the splice of two weather stations with unit and gap handling, superseded request versions, former and new field ids, and meters with rollover, units and swaps. Layer 2 is state-carrying soil-water-balance replay with the exceedance order rule.)
- decisive_step: analytical

The deciding quantity is a root-zone water balance with initial condition and an exceedance-quantile of seasonal demand, which irrigation planning would estimate. The easy route is to start each replay at field capacity or at the replay year's own winter, which gives 189,800 against 202,700 (and a different setting year, 2003 against 2012). The easy route is wrong, so H3 passes as analytical. The ambiguity in the initial condition is the one risk to that classification.

**Fix:** none required (location: none). Recommended hardening against the fork: add one sentence to WOP 2.4 stating the replay's starting depletion is the field's depletion at the end of 31 January from its last delivered 2026 set. That would sit in the procedure document as a prompt/input-file pin. Optionally pin exact 25.4 mm per inch in the data dictionary.

## Disposition

- **DETERMINISTIC, APPROVE; no repair required and no re-judge** (no FIX_NOW). Every graded figure reproduced: the 24th
  smallest replay is 2012 at 202,658 acre-feet, the order 202,700, the schedule, the setting year and requirement and
  both asks as filed.
- **The optional pin is refused.** A WOP 2.4 sentence naming each replay's starting depletion would name the decisive
  rung and pin the method; the start stays forced by WOP 3.1 and 3.4 on the record (fork row SF9). Recorded in the
  design note's `## Tried and rejected`.
- **The unit margin is recorded, and the dictionary carries the unit fact.** Rounding station 39's converted values to
  0.01 inch (202,400) and converting at 0.0394 inch per millimetre (202,800) are non-literal readings, fork row SF29,
  both asserted in `checks.py`. The dictionary already stated station 39's units, so its entry now reads "millimetres
  (25.4 millimetres to the inch)": a changed document, and the arithmetic the judge ran.
- **The connector turnouts' lateral** (05-045 to 05-058): fork row SF16 for the call (WOP 6.2, the register as it
  stands, 202,500 under the alternative), SF26 and SF27 for Ask A, each asserted.
- **The pack after the stage 4 fix pass** differs from the judged one in five files (the dictionary and the operations
  log, documents; the meter shop log, the meter book and the requests' remarks, data). `golden/` and
  `generator/figures.json` are byte-identical and `freeze.py check --mode determinism` passes, so no graded figure
  moved.

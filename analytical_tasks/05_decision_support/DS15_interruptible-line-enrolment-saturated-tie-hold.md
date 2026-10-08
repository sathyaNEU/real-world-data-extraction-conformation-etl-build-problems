# DS15 — Which steel-plant line to enrol in the interruptible programme, when five lines tie at a perfect record that the tariff's own meter rule breaks

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · industrial energy procurement |
| Mirrors | Admitting a resource into a firm-capacity product on a performance record measured coarser than the product settles it (Google and Meta data-centre demand response, cloud capacity reservations judged on hourly utilisation, Amazon carrier programmes admitted on daily on-time rates) |
| Decision shape | Hold, forced by a blocking quantity: one line enrolled at the service point next season, or none |
| Committed call | The line enrolled, or that the plant sits the season out; and the number of the 18 test events the best line actually met |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · measured #19's architecture (a saturated tie that the standard's lowest-consistent-reading rule breaks), answered by a hold, with finer controls (#12) at rung 2 and hygiene at rung 1 |
| Gate G mechanism | signal_vs_noise_or_hold, with method_or_model_selection |
| Measured traps engaged | #19 breaks a big tie instead of questioning it · #12 stops at the first control that passes · #14 coarsens the segment it was asked about · #9 picks from the offered options when none passes |
| Calibration form | Settled-transaction ledger: the utility's settlements of last season's 18 test events at the service point, with the revenue meter's interval readings |
| Driving force | The plant's procurement policy enrols a line only if it met its commitment in every test event. On the energy manager's hourly extract five lines did, and the programme guide's tie-break picks the largest. Under the tariff, a line's load in an interval is the lowest figure consistent with every metered record: its own submeter, and the residual of the utility's revenue meter after the other submeters and the base-load meter. The submeters read about 1.5% high, so near-commitment intervals fall under. On that measure no line meets all 18, and the best two meet 17. |

## 1. Situation

A steel plant can enrol one process line at its service point in the utility's interruptible-load programme next season, and it earns a
capacity credit on the line's committed megawatts. The plant's procurement policy is to enrol only a line that met its commitment in every
one of last season's 18 test events. If several did, the plant takes the programme guide's tie-break (largest commitment). If none did, it
sits the season out, because non-performance penalties exceed the credit. Six lines are candidates. The plant has its SCADA historian (hourly
averages), revenue-grade 15-minute submeters on every line and on the base load, the utility's dispatch log and the settlement ledger. The
energy manager says four or five lines have a perfect record.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct and no stakeholder read is overturned. The historian, the submeters, the revenue meter, the
  dispatch log and the ledger are all right, and the plant did meet every test event as a whole. The difficulty is that a perfect line
  record is an artefact of the coarsest file, and the tariff's measure of a line is the lowest reading every record allows.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the energy manager's view and the historian. Fifteen-minute submeters on the dispatch windows still leave three
  lines at 18 of 18, and the tie-break still enrols the oxygen plant.
* **Instrument repair.** Recalibrate every submeter tomorrow. Last season's test events, the only qualification record, were metered as
  they were, and the tariff's measure of them is unchanged.
* **Lens swap.** The naive record reads each line from its own meter. The answer reads it from the residual the service-point meter leaves
  for it: a different population of readings (the utility's) applied to the same events.

## 3. The driving force

A strong solver distrusts the hourly extract. It removes the historian's duplicated feeder tag, moves to 15-minute submeter readings, and
aligns event windows to the dispatch log, because the ledger's interval stamps follow dispatch, not clock hours. Each step is competent, and
three lines still show 18 of 18, so the guide's tie-break enrols the oxygen plant. But the tie itself is the warning. The tariff measures a
line in an interval at the lowest load consistent with every metered record of that interval. The utility's revenue meter, less the other
lines' submeters and the base-load meter, leaves a residual for each line. The submeters read about 1.5% high against the revenue meter, so
wherever a line ran within 1.5% of its commitment the residual falls below it. The oxygen plant falls 0.30 MW short in one interval of event
4. The ladle preheat falls short in event 15, and the compressed-air line in events 9 and 13. No line meets all 18, so the plant sits out.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Historian hourly averages against commitment on clock-hour windows; five lines meet 18 of 18; the guide's tie-break | A, EAF melt shop (24 MW) | The energy manager's extract and the guide's own tie-break | The historian's tag map: for three weeks after the SCADA migration the EAF feeder was recorded under two tags, doubling it in event 7 |
| 1 | Duplicate tag removed (hygiene); four lines at 18 of 18 | B, rolling mill (14 MW) | Clean data and an unbroken tie | The dispatch log and the ledger's interval stamps: windows start at the dispatched minute (#12), and the roll change in event 12's last 20 minutes falls inside them |
| 2 | 15-minute submeter readings on dispatch windows; three lines at 18 of 18 | C, oxygen plant (9 MW) | Matches the ledger's 144 event intervals and every window boundary | The tariff: a line's load in an interval is the lowest figure consistent with every metered record of that interval |
| 3 | **Decisive:** per interval, min(own submeter, revenue meter − other submeters − base-load meter), with the revenue meter's end-stamped intervals aligned; count events with every interval at or above commitment | **Hold: no line meets 18 of 18; the oxygen plant and the ladle preheat meet 17** | — | — |

* **Position table.** Rung leaders are the EAF, the rolling mill and the oxygen plant, chosen by the tie-break on commitments of 24, 14 and
  9 MW (margins 1.71× and 1.56×, with the next at 6 MW). On rung 3 the oxygen plant and the ladle preheat lead at 17, so the hold refuses the
  leaders rather than breaking a new tie.
* **Blocking quantity.** The best record under the tariff's measure is 17 of 18 (94.4%), and the policy requires 18. Events failed: EAF 3,
  rolling mill 2, oxygen plant 1 (event 4, 8.70 MW against 9.0), ladle preheat 1 (event 15, 5.88 against 6.0), compressed air 2, water
  treatment 5.
* **Falsifiability.** The oxygen plant would have been enrolled had its event-4 interval read 0.30 MW higher on the residual. Any line with
  every interval of all 18 events at or above commitment on the lowest consistent reading would have been the pick.
* **Partial correction priced (L3).** Applying the residual at hourly grain averages the shortfalls away and enrols the oxygen plant again.
  Applying it with the revenue meter's intervals read as begin-stamped shifts every dip by one interval, clears the oxygen plant's event 4,
  and enrols it. Each half-insight lands on rung 2's pick.
* **Grid.** Data and windows (historian raw on clock hours, historian clean on clock hours, submeters on clock hours, submeters on
  dispatch windows) × measure (own meter, or lowest consistent, which needs interval data) gives 6 feasible cells. They enrol A, B, B, C
  and C, and only the full cell holds. The nearest pick is the residual on clock-hour windows: the oxygen plant's event-4 shortfall falls
  in the 20 dispatched minutes after the clock hour, so it shows 18 of 18. That costs one omission: the dispatch log.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The tariff states how a line is measured. No document says the five-way tie is an artefact, or that the
   submeters read high against the revenue meter.
2. **No sweepable corpus nominates a pick.** *In every settled test event the service point as a whole met the plant's total commitment,
   because the plant's flexible load exceeded the sum of commitments by more than the submeters' 1.5% bias.* So the ledger reproduces "met"
   for all 18 events under every construction and cannot show a line's residual.
3. **No arithmetic symptom.** Submeters plus base load reconcile to the revenue meter within their stated accuracy class, and every
   event's total ties to the ledger.
4. **Not a row predicate.** It needs the revenue meter's end-stamped intervals aligned to begin-stamped submeters, a residual per line per
   interval, a minimum across records, and then an every-interval test across each event.
5. **The enumeration is arithmetic.** No column records a line's lowest consistent load. It is constructed per interval.
6. **No cutover date.** The bias is stable across the season, and the SCADA migration is decoy material that rung 1 cleans.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The settlement ledger: the 18 test events with the utility's settled service-point performance, and the revenue meter's
  15-minute readings for each event window, end-stamped as its dictionary states.
* **What it certifies.** The plant met every event in aggregate, the event windows (144 intervals with their stamps, matched only by
  dispatch-minute windows), and the revenue meter's readings.
* **What it is blind to.** Any single line's record (above).
* **Twin pair.** The ladle preheat and the compressed-air line are identical on every historian and submeter column: 6.0 MW commitments, the
  same hourly profile (6.4 MW) in every event hour, the same lowest 15-minute submeter reading (6.10 MW). Under the residual the ladle
  preheat fails one event and the compressed-air line two (2×). Only the residual separates them, because their near-commitment intervals
  fall in different events.
* **Every rule exercised.** Two events began mid-hour, which tests dispatch windows. In one event the base-load meter's chiller cycled,
  which tests that the residual subtracts the base-load meter interval by interval.
* **Resemblance points at the decoy.** The oxygen plant's continuous-process profile resembles the lines that settled perfectly in the
  utility's published programme case studies.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The procurement policy: enrol only a line that met its commitment in every test event; if several did, apply the
  programme guide's tie-break; if none did, do not enrol this season. The programme guide: the tie-break is the largest commitment. The
  tariff: a line's load in an interval is the lowest figure consistent with every metered record of that interval. One sentence each.
* **Empirical pins.** Dispatch windows, from the ledger's stamps. The submeter bias, from the residuals.
* **Voices.** The energy manager: "Four or five of our lines never missed an event." The melt-shop superintendent: "The furnace is the
  biggest lever we have." The finance lead: "Every season we sit out is a credit we don't earn."
* **Licensed wrong basis.** The policy records that the parent company's energy committee reviews enrolments on the historian's hourly
  records and will see that basis.

## 8. Determinism by construction

* **Alignment.** The revenue meter is end-stamped and the submeters begin-stamped, each stated in its dictionary. Dispatches fall on interval
  boundaries, so every window holds exactly eight whole intervals.
* **Residual.** The single-line diagram shows no unmetered load, so the residual has one definition.
* **Margins.** Every failing interval sits at least 0.10 MW (1.7%) under commitment on the residual, and every passing one at least 0.08 MW
  over it, beyond the revenue meter's 0.2% accuracy class.
* **Commitments.** Each line's committed MW is filed in the draft enrolment form.

## 9. Prompt sketch and deliverables

> We can enrol one of our lines in the utility's interruptible programme next season, but only one that held its commitment in every test
> event, and the energy manager says several did. Tell me which line we enrol, or that we sit the season out, in one sentence for the plant
> leadership meeting, with how many of the 18 test events the best line really met. Send `enrolment_case.xlsx`, a chart `event_record.png`,
> and a one-page `enrolment_note.pdf`.

* `enrolment_case.xlsx` — each line's events met under each construction, the energy-intensity sheet (ask A), the stops sheet (ask B) and
  the interval sheet (ask C).
* `event_record.png` — a grid of six lines × 18 events coloured met or failed under the tariff's measure, the oxygen plant's event-4 interval
  inset with its own reading, its residual and the commitment as a labelled line, and each line's tally at the row end.
* `enrolment_note.pdf` — the hold, the blocking quantity, and what would have enrolled the oxygen plant.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each line and quarter of last year, energy per tonne of product. *Device:* the production log
  books a heat in progress at month-end to the month it taps, as its dictionary documents. Allocating tonnes by heat start misstates the
  melt shop's and the ladle preheat's January and July figures.
* **Ask B (device-carried).** For each line, unplanned stops longer than 30 minutes last season. *Device:* the maintenance log splits a stop
  across a shift change into two records with a continuation flag. Counting records overstates the two continuous-process lines by about a
  quarter.
* **Ask C (validity).** Each line's events met under the four rung constructions, and each line's worst-interval shortfall on the residual.
* **Decoupling.** Clearing the residual changes no figure in asks A or B. Production heats and maintenance stops never enter an interval
  reading.

## 11. Rubric arithmetic

6 lines × 4 quarters (ask A) + 6 lines (ask B) + 6 × 4 tallies + 6 shortfalls (ask C) + the hold, the blocking quantity and the falsifying
shortfall + 5 named chart parts + 3 files ≈ 71 criteria.

## 12. World-building constraints

* Commitments (MW): EAF 24, rolling mill 14, oxygen plant 9, ladle preheat 6, compressed air 6, water treatment 3. Submeters read 1.5% high
  against the revenue meter.
* Events met (of 18), historian raw / clean / submeter dispatch / residual: EAF 18 / 17 / 17 / 15; rolling mill 18 / 18 / 17 / 16; oxygen
  plant 18 / 18 / 18 / 17; ladle preheat 18 / 18 / 18 / 17; compressed air 18 / 18 / 18 / 16; water treatment 16 / 16 / 14 / 13.
* The oxygen plant's event-4 shortfall falls in the last 20 dispatched minutes, outside the clock hour. The service point meets all 18
  events in the ledger. The twin lines are identical on every historian and submeter column.
* Heats and maintenance records never touch meters, dispatches or commitments.

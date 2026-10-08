# RC05 — Which delay cause gets the subway's one remediation programme, when the costliest cause leaves no delay record

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Policy & Education · public transit administration |
| Mirrors | Reliability investment at networks that log delay per vehicle and judge it per customer (cancelled runs at metro and bus operators, missed pickups against late deliveries at Amazon and parcel carriers, dropped batch jobs against slow ones on cloud platforms), where a run that never happened leaves no delay record and the customers behind it carry the cost |
| Decision shape | Which of N root causes gets the fix: one remediation programme for the coming year |
| Committed call | The programme funded, and the weekday peak customer delay minutes its cause accounted for over the last twelve months, in millions to one decimal |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · E07 (two grains, both flawless: train delay minutes and customer delay minutes differ in shape, because a train minute weighs by the customers it holds and a cancelled trip has no train minute at all; the standard pins the customer grain, rebuilt from fare taps and the trains that actually ran), with E19 (a latent attribution marker: unidentified incidents assigned through the set-out chain) at rung 2 |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #2 counts file rows instead of the real unit · #14 coarsens the segment it was asked about · #7 uses the ready-made measure |
| Calibration form | Counterparty acknowledgement file: the train manufacturer's accepted and rejected warranty delay claims for four closed quarters |
| Driving force | The monthly report counts train delay minutes and staff code each one; the service standard judges a programme on customer delay minutes, the extra time customers spent waiting and riding. A peak trip cancelled for want of an operator has no delay record at all, because the trains around it run to time. Every customer at every station behind it waits an extra headway, and the next train fills so that some are left on the platform for another. Rebuilt from the fare taps and the trains that actually ran, the gaps the crew shortage left are the largest cause of customer delay, ahead of the signal holds on the trunk and the door faults the warranty chain recovers. |

## 1. Situation

A city subway's delay minutes rose almost 90% on last year. The agency launched a programme against passenger-related incidents, its most frequent
code, and the chief operating officer points to two multi-hour switch failures. The board will fund one remediation programme from a catalogue of
five: passenger-incident response (A), door remediation on the new train fleet (B), signal-system remediation (C), switch and track renewal (D) and
crew availability, a spare-operator hiring and training programme (E). The service standard sets how a programme is judged. The fleet is under the
manufacturer's warranty, which pays for delay the manufacturer acknowledges as its own. Since the spring, peak trips have been cancelled most weeks
for want of operators.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: incident counts, coded minutes, the monthly report's table, the occupancy, set-out and repair records,
  the cancellation log, the fare taps, the train movement log and the acknowledgements. "Unidentified" is an honest code, and a cancelled trip
  honestly has no delay. No stakeholder's reading of their own numbers is overturned; the standard counts customers, and the delay file counts
  trains.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the passenger programme, the operating officer's view and the licensed basis. The delay file still records no minute
  for a cancelled trip, and the train-minute tables still name doors once the unidentified minutes are assigned.
* **Instrument repair.** Suspect file: the delay record's cause code, which records what station staff could see ("unidentified" for 19,000 peak
  minutes). Repaired so that every delay carries its true cause, rung 0's count still names A (door incidents rise to 2,400 against 5,200), and
  rungs 1 and 2 both return B, the door faults the chain already recovers (17,700 peak minutes against at most 16,900 for the signal system);
  none returns E. The cancellation log, the taps and the movement log are complete. The answer still needs customer delay minutes rebuilt from
  them, which no delay record, perfect or not, holds.
* **Lens swap.** The naive build counts train delay minutes; the answer counts customers' excess minutes, including trips that never ran: a
  different population (customers, and gaps with no train) over the same peaks.

## 3. The driving force

A strong solver moves from counts to minutes and from the weekday table to the peak periods the standard names. On coded peak minutes the signal
system leads. The manufacturer's acknowledgement file then shows that most unidentified holds are door faults on the new fleet: assigned through
the occupancy, set-out and repair-order chain the acknowledgements follow, door faults lead at 17,700 train minutes. Every one of those is a train
minute, and the standard judges a programme on customer delay minutes. The monthly report is the wrong unit for that in two ways. A train minute
costs the customers aboard and the customers waiting behind it, and door faults strike trains leaving the outer terminals nearly empty while
signal holds stop full trains on the trunk. And a peak trip cancelled for want of an operator has no delay record at all, because the trains
around it run to time: every customer at every station behind it waits an extra headway, and the next train fills so that some are left behind
for another. Rebuilt from the fare taps (each customer's arrival at the platform) and the movement log (the trains that actually left), with the
cancellation log naming each missing trip's cause, crew shortages cost 9.29 million customer minutes, the signal system 7.74 million and door
faults 5.68 million.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Weekday incidents by code, counted | A, passenger incidents (5,200) | The agency's own reading, and the code is by far the most frequent | The service standard judges a programme on weekday peak-period delay minutes (07:00–10:00, 16:00–19:00), not incidents |
| 1 | Weekday peak delay minutes by code, unidentified minutes left out | C, signal system (12,500) | The standard's own periods and minutes, every coded minute accounted for | The acknowledgement file: the manufacturer accepted 61% of closed-quarter unidentified incidents as train defects |
| 2 | Peak minutes with the unidentified assigned through the occupancy, set-out and repair-order chain the acknowledgements follow | B, new-fleet doors (17,700 min) | Every minute assigned, every acknowledgement reproduced | The cancellation log: 2,400 peak trips cancelled for want of an operator, none with a delay record, against the charter's customer minute |
| 3 | **Decisive:** weekday peak customer delay minutes rebuilt from fare taps and the trains that ran, each cancelled trip's gap credited to its cause | **E, crew availability (9.29M)** (4th of 5 on rung 0) | — | — |

* **Position table.** E ranks 4th on rung 0 and 5th on rungs 1 and 2, and leads only rung 3. Rung leaders beat their runners-up by 5.78×, 1.30×,
  1.31× and 1.20× (9.29M against the signal system's 7.74M).
* **Discriminator dominance.** Door faults carry a 6.81× lead over crew shortages into rung 3 (17,700 train minutes against 2,600). Customer
  minutes per train minute are 3,573 for E, its 2,400 cancelled trips included, and 321 for B, an edge of 11.1×, 1.36 times the required 1.2 ×
  6.81 = 8.17; the net margin is 1.64×.
* **Partial correction priced (L3).** Every half-rebuilt customer measure leaves another cause in front. Weighting train minutes by the average
  peak load gives B 7.08M against C's 5.40M (1.31×), E 1.04M. Weighting each delay by its own train's load and the customers waiting behind it,
  with no cancellations, gives C 7.02M against A's 4.61M (1.52×). Adding cancellations at one headway for the missing train's own load, with
  nobody left behind by the train after it, gives C 7.38M against B's 5.14M (1.44×), E 4.97M.
* **Grid.** Grain (weekday, peak) × measure (counts, train minutes, train minutes by load, customer minutes with gaps at one headway, full
  customer minutes) × unidentified (dropped, chain) gives twelve feasible builds. Every train-minute build names A, D, C or B; load-weighted
  builds name B (average load) or C (own load); the one-headway build names C; only full customer minutes in the peaks name E. The nearest wrong
  cell is the one-headway build, which needs the customers left behind added.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The customer charter defines a customer delay minute; the delay guide defines the codes, and the cancellation log its
   fields. No document converts delays or cancellations into customer minutes, or says a cancelled trip's cost falls on the customers behind it.
2. **Corpus blind for a computable reason.** *Every claim in the acknowledgement file concerns a new-fleet train that ran and was delayed, so no
   closed quarter's acknowledged minutes include a cancelled trip or a customer, and the file is arithmetically incapable of pricing a gap.* It
   pins rung 2's chain (1,860 of 1,860 acknowledgements reproduce) and cannot see the unit the standard counts.
3. **No arithmetic symptom.** Train minutes, incidents, codes, cancelled trips and taps all reconcile; a cancelled trip has no delay to
   reconcile.
4. **Not a row predicate.** A customer's excess wait is the gap between their platform arrival and the first later train with room, built from
   the taps, the movement log and the order of trains at each station.
5. **The enumeration is arithmetic.** No column holds a customer delay minute; 9.29 million are built from 2,400 cancelled trips, the gaps they
   left and the taps behind them.
6. **No cutover date.** Cancellations rose as operators retired through the year; the dated events (the switch failures, the passenger
   programme's launch) are the decoys.
7. **Survives deletion.** With every voice gone, the train-minute tables still name doors.

## 6. The calibration corpus

* **Form.** The manufacturer's acknowledgement file: 1,860 incidents claimed in four closed quarters (coded door faults plus unidentified
  incidents on new-fleet trains), each accepted or rejected, with the occupancy, set-out and repair records for those quarters.
* **What it certifies.** The chain for unidentified incidents (rung 2): it reproduces 1,860 of 1,860 acknowledgements, against 1,212 for the
  door code alone, 1,296 for the set-out's recorded reason and 1,251 for the unit's next repair order.
* **What it is blind to.** Customer minutes and cancelled trips (above).
* **Twin pair.** Tuesdays 9 and 16 April carried identical train delay minutes by code, incidents, loads and tap counts, and six crew
  cancellations each. Customer delay minutes were 61,000 and 30,000 (2.03×): on the 9th the cancelled trips ran consecutively on the busiest line
  between 08:10 and 08:30, so the gaps compounded and customers were left behind twice; on the 16th they fell on quieter lines in the shoulders.
  Only the rebuilt customer measure separates the two days.
* **Resemblance points at the decoy.** This year's delay profile matches Q1, the quarter in which the manufacturer accepted the most door
  minutes, on codes, lines and new-fleet share.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The service standard: a remediation programme is judged on the weekday peak-period customer delay minutes its cause accounted
  for over the last twelve months, the peak periods being 07:00–10:00 and 16:00–19:00. The customer charter: a customer delay minute is a minute
  a customer spends waiting or riding beyond the timetable. The programme catalogue lists the delay codes and cancellation reasons each covers.
* **Empirical pins.** The assignment chain, from the acknowledgement file; each customer's platform arrival, from the taps.
* **Voices.** The customer services director: "Passenger alarms are most of our incidents, so that's where the minutes go." The fleet engineer:
  "Those unidentified holds are door faults on the new trains. The manufacturer pays for most of them, and they're still our worst problem."
* **Licensed wrong basis.** The standard records that the board's finance committee reviews remediation on the monthly report's weekday train
  minutes by code group and will present that table.

## 8. Determinism by construction

* **Peak minutes.** Waits and delays crossing a peak boundary are split by minute; every delay record carries a start time and duration.
* **Customer minutes.** A customer's wait runs from tap-in to the departure of the first train with room (crush load less the taps already
  aboard), less the timetabled wait; ride time beyond the timetable counts for every customer aboard. Where a delayed train follows a cancelled
  one, the gap is credited to the cancellation's cause and the delay to its own.
* **Taps.** Every station is gated and exit taps fix each journey's line and direction, so every tap-in resolves to one platform.
* **Window.** Twelve complete months; the cancellation log is final.
* **Rounding.** Millions of customer minutes to one decimal; the committed figure sits mid-bin.

## 9. Prompt sketch and deliverables

> Delay minutes on the subway are up almost 90% on last year and the board will fund one remediation programme. Our chief operating officer
> is sure it's the two switch failures. Tell me which programme we fund and how much delay its cause cost us over the last twelve months, as the
> standard counts it, in millions to one decimal, in one sentence for the board pack. Send `delay_cause_case.xlsx`, a chart
> `delay_by_cause.png` and a short `remediation_memo.pdf`.

* `delay_cause_case.xlsx` — the five causes under each construction, the track-defects sheet (ask A), the lift and escalator sheet (ask B)
  and the acknowledgement reproduction (ask C).
* `delay_by_cause.png` — paired bars per cause of peak train minutes and customer minutes, the customer bar split into delays and cancellation
  gaps, an inset of one cancelled trip's gap station by station, and the funded cause highlighted.
* `remediation_memo.pdf` — the funded programme, its figure, and why the other four are not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the four lines and each of the last twelve months, track-geometry defects found and
  closed. *Device:* a defect re-measured at a later inspection is written as a new row carrying a parent-defect reference, as the track
  inspection guide documents; counting rows overstates defects found on two lines by about a quarter.
* **Ask B (device-carried).** For the 20 busiest stations, lift and escalator outage events and outage hours over the twelve months.
  *Device:* an outage running past midnight is written as one row per calendar day, later rows carrying a continuation flag, as the asset
  log's schema documents; counting rows as events inflates events at eleven stations.
* **Ask C (validity).** For each closed quarter, accepted minutes under each of the four assignment rules; and each cause's figure under each of
  the four rung constructions.
* **Decoupling.** Clearing the customer-minute rebuild changes no figure in asks A or B; neither touches a delay record, a cancellation, a tap
  or a train movement.

## 11. Rubric arithmetic

4 lines × 12 months × 2 figures (ask A) + 20 stations × 2 figures (ask B) + 4 quarters × 4 rules + 5 causes × 4 constructions (ask C) + the
funded programme, its figure and the runner-up's + 5 named chart parts + 3 files ≈ 185 criteria.

## 12. World-building constraints

* Weekday counts A 5,200, D 900, C 800, E 650, B 600 (door incidents with the unidentified ones assigned: 2,400). Weekday coded minutes D 27,000,
  A 21,000, C 15,000, E 8,800, B 5,400 (doors 23,000 with the unidentified assigned); peak coded minutes C 12,500, A 9,600, D 6,800, B 3,100,
  E 2,600; of 19,000 unidentified peak minutes the chain gives B 14,600 and C 1,000 and leaves 3,400 unassigned.
* Customer minutes per train minute: B 260, C 520, A 480, D 300, E 250. Cancelled peak trips: crew 2,400, doors 300, signal 200, track 150; a
  cancelled trip costs 3,600 customer minutes, half in the missing train's own load and half in customers the next train leaves behind.
  Customer minutes (millions): E 9.29, C 7.74, B 5.68, A 4.61, D 2.58.
* Acknowledgements: chain 1,860/1,860; door code 1,212; set-out reason 1,296; next repair order 1,251.
* 9 and 16 April identical on every delay, incident, load, tap-count and cancellation-count column.
* Track-defect rows and outage continuation rows touch no delay record, cancellation, tap or train movement.

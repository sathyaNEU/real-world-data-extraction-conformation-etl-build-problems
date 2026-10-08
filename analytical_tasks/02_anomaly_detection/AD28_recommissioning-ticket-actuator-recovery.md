# AD28 — Which building gets the one recommissioning ticket, when the biggest controllable waste is the one a ticket cannot stop

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Economics · energy measurement and verification |
| Mirrors | Spending one engineering slot on the fault whose fix actually recovers the waste, measured from past fixes rather than assumed (data-centre cooling optimisation at Google and Meta, fulfilment-centre HVAC programmes at Amazon, cloud cost-anomaly remediation where some fixes stick and others only change a setting) |
| Decision shape | Which of N gets one scarce thing: the cycle's single recommissioning ticket among five flagged buildings |
| Committed call | The building that gets the ticket, and the energy it is expected to give back in the year after the ticket |
| Gap · Pattern | Gap 1 (time: the past excess against the forward recovery) over Gap 2 (population) · change-log natural experiments that measure what a fix recovers, with a mixed segment split through a join (process sub-meters) below it |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection support |
| Measured traps engaged | #25 assumes an effect the log could measure · #6 treats a mixed segment all one way · #13 validates on one population, applies to another |
| Calibration form | Existing-book actuals: 40 recommissioning tickets closed 2019–2025, each with its pre-ticket controllable excess and realised first-year savings |
| Driving force | Every building's controllable excess is measured correctly, and the programme's book shows a ticket recovering about 88% of it, because every ticket in the book was on air handlers with electronic valve actuators. On pneumatic reheat valves a sequence reset stops the command but not the leak. The controls team's change log holds nine such resets, and once each one's before and after weeks are weather-normalised they recovered 27–35%. C, the largest controllable excess, is all pneumatic, a fact reached through the equipment register. |

## 1. Situation

A university energy office has one recommissioning ticket this cycle: a controls engineer for six weeks, resetting sequences, schedules and
setpoints in one building. The year-over-year alert flagged five buildings. The programme charter sends the ticket where it recovers the
most energy in the following year, measured under the campus measurement-and-verification protocol. The office holds daily meter data, a
weather-normalised baseline per building, the sub-meter register, the equipment register, the book of closed tickets and the building
automation system's change log. The facilities director wants the ticket on Building A, whose bills rose most.

## 2. Gate G: why this is legal

* **Litmus.** Every reported figure is correct: the year-over-year rises, the weather-normalised excesses, the sub-meter readings and the
  book's realised savings. The book's 88% is a true average of what tickets recovered. Nothing anyone reports is overturned; the difficulty
  is what a ticket will recover in a building the book never reached.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the director's view and the year-over-year alert. The weather-normalised, scope-correct build still multiplies
  each building's controllable excess by the book's recovery and names C.
* **Instrument repair.** Make every meter, sub-meter and baseline perfect. C's excess is real and controllable; the issue is what a reset
  does to a leaking pneumatic valve, which no better meter of the past measures.
* **Lens swap.** The naive figure is waste already incurred; the answer is energy recovered next year after a specific intervention. The
  answer's population is the share of each excess a reset can stop, at a different moment from the excess itself.

## 3. The driving force

A strong solver discards year-over-year bills, fits a change-point baseline per building, strips process sub-meters as the charter
requires, and multiplies the controllable excess by the realised recovery in the programme's book, which predicts every closed ticket to
within 4%. Every step is correct. The book is excellent because it is homogeneous: until this cycle the intake checklist routed every
simultaneous-heating-and-cooling complaint to maintenance, so no ticket ever touched a pneumatic reheat valve. The controls team, answering
complaints, did reset sequences on nine pneumatic air handlers, and the change log records each reset with its date and the units it
touched. Read as an audit trail it says nothing. Read as nine natural experiments, each weather-normalised before against after, it shows a
reset recovering 27–35% of the excess on pneumatic actuators and 84–91% on electronic ones (22 resets). Which actuator a building has sits
in the equipment register, one join from the air-handler tags in the change log and in the meter map.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Year-over-year increase in metered energy over the flagged months (MWh): A 430, B 360, C 300, D 240, E 190 | A | The office's own alert and the bills everyone sees | The site weather file: A's rise tracks a winter with 31% more heating degree days, and A's weather-normalised excess is 60 MWh |
| 1 | Annualised excess against each building's change-point baseline: B 820, C 640, D 470, E 330, A 60 | B | The textbook weather normalisation, with the protocol's fit acceptance met by all five | The sub-meter register: 615 MWh of B's excess is a server room commissioned last March, a process load the charter puts outside recommissioning scope |
| 2 | Controllable excess (process sub-meters removed) × the book's realised recovery of 0.88: C 563, D 414, E 290, B 180, A 53 | C | Weather-normalised, scope-correct, and calibrated on 40 closed tickets | The change log: nine resets on pneumatic air handlers recovered 0.27–0.35 of their excess once weather-normalised |
| 3 | **Decisive:** controllable excess × the recovery measured from the change log's resets, conditioned on actuator type through the equipment register: D 414, E 290, C 198, B 180, A 53 | **D** (4th of 5 on rung 0) | — | — |

* **Position table.** D ranks 4th on rung 0, 3rd on rung 1 and 2nd on rung 2 (C leads it by 1.36×), and leads only rung 3. Rung leaders
  beat their runners-up by 1.19×, 1.28×, 1.36× and 1.43×.
* **Discriminator dominance.** C carries a 1.36× controllable-excess advantage into rung 3. D's edge on the decisive axis is its recovery,
  0.88 against 0.31 (2.84×), so the net is 2.84 / 1.36 = 2.09×. At rung 2, B carried a 1.28× excess advantage against C's 4.0× controllable
  share (1.00 against 0.25), a net of 3.1×.
* **Partial correction priced (L3).** A solver who measures recovery from the change log but pools all 31 resets gets 0.71 and still names
  C (454 against D's 334), the rung 2 answer. Conditioning on building use (labs against offices) instead of actuators also names C, because
  C is an office building and office resets average 0.80.
* **Grid.** Weather basis (year-over-year or baseline) × scope (whole meter or controllable) × recovery (book 0.88, pooled 0.71, actuator-
  conditioned) = 12 cells. Year-over-year cells name A, whole-meter baseline cells name B, controllable cells with either uniform recovery
  name C, and only the conditioned cell names D.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The change log records what was changed and when; no document reports what a reset recovered, and nothing links
   actuator type to recovery.
2. **Corpus blind for a computable reason.** *In every closed ticket the air handlers carried electronic actuators, because the intake
   checklist routed every simultaneous-heating-and-cooling complaint to maintenance and pneumatic reheat never reached the programme.* The
   book reproduces rung 2 to within 4% on all 40 tickets and cannot see the pneumatic case.
3. **No arithmetic symptom.** Baselines meet the protocol's fit acceptance, sub-meters sum to main meters, and the book's realised savings
   reconcile to its own M&V reports.
4. **Not a row predicate.** Each reset's recovery is a weather-normalised before-and-after fit within one air handler's meter, computed
   for 31 events, then joined to the equipment register and transported to each candidate's actuator mix.
5. **The enumeration is arithmetic.** No column records a reset's effect, and no candidate carries a recovery figure.
6. **No cutover date.** The decision turns on a stable per-actuator effect measured across 31 resets spread over six years; no candidate's
   series steps on a date that explains it.
7. **Survives deletion.** Remove both voices and the alert: the book-calibrated build is still the natural one and still names C.

## 6. The calibration corpus

* **Form.** The book of 40 recommissioning tickets closed 2019–2025: building, air handlers touched, pre-ticket controllable excess and
  realised first-year savings under the M&V protocol.
* **What it certifies.** The baseline method, the scope rule and a recovery of 0.88 (0.84 to 0.91) on electronic actuators. A back-tester
  is confirmed at rung 2.
* **What it is blind to.** Pneumatic reheat (above). The refusal sits in the less inviting record, the change log: 31 controls resets with
  dates and air-handler tags, 22 on electronic actuators (0.84–0.91) and 9 on pneumatic (0.27–0.35), with no reset between 0.35 and 0.84.
* **Twin pair.** Resets CL-2023-114 and CL-2024-037 are identical on every change-log column (building type, air-handler size class,
  pre-reset excess within 2%, change text "reheat sequence reset", season). One recovered 0.88 and the other 0.31, a 2.84× gap, separated
  only by the actuator type in the equipment register.
* **Resemblance points at the decoy.** By use, size and age, C most resembles six closed tickets that each recovered about 0.88.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The programme charter: the ticket goes where it recovers the most energy in the year after the ticket, under the M&V
  protocol, and process loads are outside recommissioning scope. The equipment register is the campus record of each air handler's
  components. One sentence each.
* **Empirical pins.** Per-actuator recovery, from the change log's resets; the baseline form, from the protocol's fit acceptance.
* **Voices.** The facilities director: "Building A's bills jumped the most; that is where the money is." The energy manager: "Our tickets
  get back most of what is wasted, and the book proves it."
* **Licensed wrong basis.** The charter records that the sustainability office ranks buildings on year-over-year bill increases and will
  present that ranking at the ticket meeting.

## 8. Determinism by construction

* **Baseline form.** The protocol's selection rule picks the same change-point form for each building under daily or weekly fitting, and
  every candidate passes fit acceptance.
* **Measurement windows.** Eight-, twelve- and sixteen-week windows either side of each reset give recoveries within 0.03 of each other,
  and no reset overlaps another change on the same air handler.
* **Actuators.** Every air handler in the five buildings is wholly pneumatic or wholly electronic; C's are all pneumatic, D's and E's all
  electronic, B's controllable load sits on electronic units.
* **Rounding.** The committed recovery is given to the nearest 10 MWh, and D's 414 sits mid-bin.

## 9. Prompt sketch and deliverables

> I can put one controls engineer into one building for six weeks this cycle, and five buildings look wasteful. Facilities would put him in
> Building A because its bills jumped most. Tell me which building gets the ticket and how much energy it should give back in the first
> year, in MWh to the nearest ten, in a sentence I can send to the vice-president. Send `ticket_case.xlsx`, a chart `recovery_evidence.png`,
> and a one-page `ticket_memo.pdf`.

* `ticket_case.xlsx` — the five buildings on all four bases (ask C), the occupancy sheet (ask A) and the complaints sheet (ask B).
* `recovery_evidence.png` — the 31 resets as points of recovered share, grouped by actuator type, with the book's 0.88 as a reference line,
  the empty band between 0.35 and 0.84 shaded, and a second panel of the five candidates' expected first-year recovery.
* `ticket_memo.pdf` — the committed building, its recovery figure, and why each other building falls away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each building, mean weekday occupancy per occupied hour and the busiest hour over the last
  twelve months, from the card-access system. *Device:* readers at airlock door pairs log one passage twice within ten seconds, and the
  security system guide counts reads within 15 seconds at a pair as one passage. Raw counts double occupancy in three buildings. The
  recovery build never uses access data.
* **Ask B (device-carried).** For each building, comfort complaints in the last twelve months and the median days to close. *Device:* the
  service desk merges duplicate complaints into a parent ticket, and the merged children stay in the export as closed tickets with status
  "merged", which the desk guide says are not complaints. Counting them inflates two buildings and shortens their median close time.
* **Ask C (validity).** Each building's figure under each of the four rung bases.
* **Decoupling.** Clearing the actuator conditioning and the sub-meter split changes no figure in asks A or B.

## 11. Rubric arithmetic

5 buildings × 2 (ask A) + 5 × 2 (ask B) + 5 × 4 bases (ask C) + the committed building, its recovery, the runner-up and the margin + 5 named
chart parts + 3 files ≈ 52 criteria.

## 12. World-building constraints

* Rung figures as in the ladder: A 430 / B 820 / C 563 / D 414 lead their rungs, with D 4th, 3rd, 2nd (1.36× behind C) and 1st.
* B's server-room sub-meter carries 615 of its 820 MWh excess. C's 640 MWh is all on pneumatic air handlers.
* The book holds 40 tickets, all electronic, realising 0.84–0.91. The change log holds 22 electronic resets (0.84–0.91) and 9 pneumatic
  (0.27–0.35), none between.
* CL-2023-114 and CL-2024-037 are identical on every change-log column.
* Card-access reads and service-desk tickets never touch meters, sub-meters, the change log or the equipment register.

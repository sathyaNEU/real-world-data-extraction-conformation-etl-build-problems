# task165: which Clay Street storage tank brings combined sewer Outfall 014 to the consent decree's four overflows a year (architecture 2)

Private, never ships. Architecture 1 (Quellbrook's seasonal rock salt after a bus network redesign) was landed on the
portal on 2026-11-07 by one response at 100 per cent while the other kept 70 per cent off the call; its world is spent
(one architecture per world) and this is a re-root with a new world, dataset, generator and shell. Its lines stay in
`## Tried and rejected`.

The Quessling Sewer Authority (fictional, Pennsylvania) runs the city's combined sewers and two water reclamation
plants under a federal and state consent decree whose Appendix C holds every combined sewer outfall to no more than
four untreated overflow events in an average year of the 2014 to 2025 metered record. Clay Street (Outfall 014) is
the last outfall over the limit. Ostrem Calder Engineers' technical memorandum TM-7 offers four storage tanks at the
Clay Street regulator, each with a dewatering pump station that sends the stored flow back into the Southside
interceptor at the Southside plant's headworks once the overflow stops. The authority must name one alternative in the
design task order it issues by 1 March 2026; the selection then goes to the regulators in the facility plan. Every
file was pulled on Friday 16 January 2026.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task165.json`, architecture v2; `guard.py check` WARN only at filing (`repeat.question_form` against task156, answered below), two NOTEs (`test.same_puzzle_older`, `test.same_driver_older`) differentiated on the card against task105, task460, task127 v1 and task87; nearest driver 0.08 (task118 v5, differentiated on the card) |
| Domain / task type | `physical-environmental-sciences`, task type `hydrology-flood-frequency` (serves Forecasting): the deciding quantity is the exceedance frequency of a storage-regulated outfall over a period of record, found as hydrologists find overflow and flood frequency for a regulated system, by continuous simulation of the record through the storage with its outflow bounded by what receives it |
| Objective | Forecasting & Predictive Modeling: the untreated overflow events a year Outfall 014 will see in service (from 2029) behind each tank, predicted from the 2014 to 2025 record the decree evaluates on; no tank has ever stood at Clay Street, so the history does not pin the figure by itself |
| Shape | `08` rule replayed on history: each of the four alternatives replayed through the twelve-year record, the call the smallest that meets four events, carried by two decoupled asks (each rain gauge's rainfall in each month of 2025, 48 figures; the Northside tank's returned volume in each year 2021 to 2025, 5 figures) and the board chart of the call's own figures |
| Decision | `pick_one_of_n`, answer unit `named_option` (Alternative C, 38 MG) |
| Mechanism | gap time (decisive: the tank's free volume when each storm starts is carried from the storms before it and is set by how fast the tank can empty, which depends on the receiving plant's room after each storm), pattern none; generators G7 (the operating window: the dewatering pumps can only run into the room the Southside plant has left), G3 (the record of a pump station's rating against its operation); Gate G `binding_constraint`; strategy `binding_constraint` |
| Layer 2 family / pattern | `allocation_constraints` (capacity on a receiving system binding through a stored state); `own:storage-drawdown-bound-by-receiving-plant-headroom` |
| Layer 1 | the Outfall 014 meter replaced in June 2019 (cubic feet per second in Eastern Standard Time all year, then million gallons a day in UTC, the loggers overlapping a dry week); the plant historian's hourly export in local time with the daylight saving repeat and gap and its 2021 tag rename; on the asks' rows only, two rain gauge loggers replaced in May 2024 by cellular loggers stamping UTC, technicians' calibration pours logged as tips (monthly from the July 2025 maintenance contract), every gauge's tipping mechanism swapped for a 0.2 mm one at the contract's July visit without the inventory changing, the Northside SCADA's local clock with its repeated November hour, a dewatering pump rebuilt in March 2023 on its old tag, the level transducer re-mounted 0.45 ft lower after the August 2023 cleanout, and the diversion gate passing dry weather flow into the tank while its seals failed (full inventory in `## Layer 1 inventory`) |
| Furniture | forum `regulator_or_inspector` (the selection is filed with EPA and the state in the facility plan), forcing event `purchase_order_or_contract` (the design task order to Ostrem Calder names one tank by 1 March 2026), organisation family `utility_or_infrastructure`, role family `capacity_planner` (the authority's director of engineering and planning), context artifact `filed_standard` (the decree's Appendix C), calibration `existing_book_actuals` (the Northside tank's own record), opening `question-first`, question form `which` |
| Spine | the Outfall 014 overflow pipe's flow meter, 15-minute readings from 1 January 2014 to 31 December 2025 (about 420,000 rows across the two loggers), beside both plants' hourly influent from the plant historian (about 210,000 rows) |
| Deliverables | `clay_street_storage_evaluation.xlsx` (the replay, the events a year by alternative and by year, the two ask tables) and `clay_street_tank_selection_board.pptx` (four slides for the board with the chart of events a year by alternative against the limit) |
| People | drawn with `guard.py names --geo "United States" --seed 165`: Tammy Williams (superintendent, Southside WRP, on the historian export's header), Nicholas Hernandez (field services, rain gauge program, in the field log), Jesus Thompson (Ostrem Calder project engineer, TM-7's author); the requester is in no file and not in the prompt |
| World | Quessling (checked: no United States place of the name), a fictional river city in Pennsylvania of about 180,000 with a combined sewer system discharging to the fictional Wennick River; the Quessling Sewer Authority, its Southside and Northside water reclamation plants, Ostrem Calder Engineers, the people, systems and data are fictional |

**Guard.** The first card drew shape 10, forum `board_of_directors` and forcing event `statutory_or_regulatory_filing`;
each repeated task156 v3, the build registered last, and was redrawn (shape 08, the regulator receiving the facility
plan, the design task order). Three first names warned against older builds and were redrawn from the same list.
`repeat.question_form` (which) stays: a pick of one of four asks which. `repeat.deliverables` cleared by drawing a
board deck instead of a memo.

**Same-puzzle and same-driver tests.** Gap time, pattern G7 and `pick_one_of_n`: task105 (a new outlet wins only its
side of the bisector) and task460 (a zero-rate source displaces the margin of the intervals it runs in); gap time, G7
and `binding_constraint`: task127 v1 (a team's spare capacity seen only as an earlier ceiling) and task87 (two owed
items in one slot). None carries a stored volume from one event to the next through another system's room.

**Abstraction test.** Stripped of nouns: a buffer that captures a discharge empties only through a receiving channel
whose spare capacity vanishes for days after each wet event, so the buffer meets the next event still partly full;
counting events against an empty buffer, or a buffer emptied at its outlet's rated pace, understates how often it
spills, and only a replay with the outlet bounded by the receiving channel's own record prices the size the limit
needs. Against `guard.py nearest`: task118 v5 (0.08: a resource drawn from a buffer that refills only partly between
consecutive calls) is the one a reviewer would set beside this. There the partial refill between calls is the decisive
step; here the partial emptying between storms is the field's own continuous simulation and sits at rung 1, where the
default path already takes it, and the decisive step is that the emptying runs into another system whose headroom,
read from that system's own record, bounds it. task196 v2, task106, task252 and task501 map onto nothing here.

**Kinship, answered.** task156 v2 (a New Zealand pump station's consented overflows, landed and re-rooted) is the one
wastewater build on file: there infiltration scaled with sewer below a fluctuating water table and the decisive step
was a response fitted on a dry record; here nothing scales the inflow (the metered overflows are taken as recorded) and
what decides is a tank's drawdown into a receiving plant. task162 (valves acting in the hours their inlet runs above
the setting) is an hourly threshold with no memory. task32 (a constraint binding at a finer resolution than the
forecast) binds within a period; here the limit binds through a state carried between storms.

**WHAT screen (stumping 1.2).** The decisive step estimates the filed quantity and settles none of the estimand's
parts, each filed: population (Outfall 014's discharges to the Wennick River, Appendix C 2.1), outcome (untreated
overflow events, discharges less than 24 hours apart one event, Appendix C 2.2), window (the 2014 to 2025 metered
record, Appendix C 2.3), unit (events in an average year, the record's events over its twelve years, Appendix C 2.3)
and comparison (each TM-7 alternative against four events, Appendix C 2.4 and TM-7 3). No shipped sentence says how
fast a tank empties after a storm or that the plant's room bounds it; TM-7 gives each pump station's firm capacity and
says where it discharges, as a design memorandum does.

**Data-native sentence.** Quessling's Southside sewershed lets groundwater in for days after rain, most of all in
spring, so the Southside plant's historian shows it at its 140 MGD headworks limit through and after most wet-season
storms; Clay Street's tank must pump back into the interceptor at that plant's headworks, while the Northside tank,
whose plant has room within hours, empties at its pumps' rating, so the one tank on record that replays exactly at its
rating sits on the one plant that never holds its limit.

**Sources read, one line each.**
- `guard.py mechanisms --objective forecasting`: the binding-constraint drivers on file bind within a period (task32,
  task64, task79, task94); none carries a stored state between events through another system's room.
- `two-layer-task-design.md`, allocation under real constraints ("capacity and queueing"): learned, not copied; here
  the capacity sits on the receiving system, read from its own record.
- The US EPA's 1994 CSO Control Policy presumption approach (no more than an average of four overflow events a year)
  for the Appendix C wording; written in the decree's own voice, no figure copied.
- `guide-to-prompt/references/examples.md` 1: the decisive step is a quantity a careful analyst computes by default the
  wrong way, here the pace a tank empties.

## Default path

Every figure below is built by `generator/golden.py` from the shipped pack and asserted in `generator/checks.py`.

1. Read the decree's Appendix C: an untreated overflow event is a discharge from the outfall, discharges less than 24
   hours apart one event; an average year is the 2014 to 2025 record's events over its twelve years; the limit is four.
2. Read TM-7: the four alternatives (A 19 MG with a 23 MGD dewatering station, B 26 MG with 31, C 38 MG with 45, D 50
   MG with 60), each tank filling from the Clay Street overflow and pumped back once the overflow stops.
3. Join the two Outfall 014 loggers (the old one in cubic feet per second on Eastern Standard Time, the new one in MGD
   on UTC, the overlap week taken once) into one 15-minute overflow record.
4. Replay the record through each tank emptied at its station's firm capacity, the field's continuous simulation, and
   check the method on the Northside tank: its 2020 to 2025 inflow replayed through 8.0 MG at its station curve gives
   the detector's own overflow events at Outfall 006, year by year.
5. Count events a year: A 5.8, B 2.8, C 0.6, D 0.1. The smallest under four is B.

Ends on: Alternative B (26 MG), 2.8 events a year.

Golden: Alternative C (38 MG), 2.9 events a year, with B at 6.8.

## Stump sentence

A competent solver replays Outfall 014's metered overflows through each TM-7 tank emptied at its pump station's firm
capacity, the continuous simulation the Northside tank's own record confirms, and selects Alternative B, the 26 MG
tank, at 2.8 events a year; the step that lands it there is taking the pumps' rating as the pace the tank empties, when
the tank empties into the interceptor at the headworks of a plant that holds its 140 MGD limit for days after
wet-season storms, so only a replay whose dewatering is bounded hour by hour by the Southside plant's own room shows the
26 MG tank at 6.8 events and selects Alternative C, the 38 MG tank, at 2.9.

## Three rules

- **Task type:** physical-environmental-sciences `hydrology-flood-frequency`, which serves Forecasting: the frequency
  with which a storage-regulated outfall exceeds its capacity, predicted over the period of record for a configuration
  not yet built.
- **Domain test:** the deciding quantity is the exceedance frequency of a storage-regulated outfall over the period of
  record, which hydrologists estimate by continuous simulation of the metered record through the storage, its outflow
  bounded by what receives it; with hospital beds or school places in place of million gallons there is no storm
  record, no event separation and no receiving plant whose wet-weather recession sets the storage's drawdown.
- **Swap:** "which tank keeps the outfall to four overflows a year" becomes "which ward keeps the hospital to four
  diversions a year"; a ward has no storm record, no 24-hour event rule and nothing it drains into whose room after a
  storm bounds it, so the sentence stops making sense.
- **Layer 1:** the Outfall 014 meter's replacement (units, clock, overlap week), the historian's local time with its
  daylight saving repeat and gap and its tag rename, and on the asks' rows the rain gauge loggers' UTC, calibration
  pours, the 0.2 mm mechanism, the Northside SCADA's local clock, the rebuilt pump on its old tag and the re-mounted
  transducer; each is produced by the authority's own systems and staff, none placed to be caught, and none carries the
  call (the meter's overlap week is dry, so the main path is mess-neutral).
- **Layer 2:** allocation under real constraints: a storage's drawdown bounded by the receiving system's capacity, a
  binding limit that acts through a state carried between storms; the choice that flips the call is whether the tank
  empties at its pumps' rating or at the room the Southside plant has left.
- **Decisive step:** recognising that the dewatering station's firm capacity is not the pace the tank empties, because
  it discharges into an interceptor whose plant sits at its headworks limit for days after wet-season storms, and
  bounding the drawdown hour by hour by that plant's room read from its own historian.
- **Not semantics:** every field read correctly (cubic feet per second converted, both clocks aligned, the event rule
  applied, each station's capacity taken from TM-7) still files B at 2.8 events a year; nothing in any column, code or
  unit changes when the plant's room is read, because no column holds the room or the tank's state.
- **Not rule application:** no filed rule or procedure says how fast a tank empties or names the plant's room; executing
  Appendix C, TM-7 and every convention files B. The enumerated family (event volumes against an empty tank, the
  continuous replay at the station's rating with or without pumping during inflow, the replay bounded by the plant's
  room at 15-minute, hourly or daily grain, with the room taken as 139 or 140 MGD) spans 0.0 to 9.8 events a year
  across the four tanks and picks A, B or C; the standing family (the replays bounded by the room, the literal 24-hour
  rule and TM-7's start-after-overflow) spans 6.4 to 7.0 events at B and 2.8 to 3.1 at C and picks C in every member; the
  ruling-out is quiet: the room is read from the plant's own historian, where a flat 140.0 top is the only sign.
- **Analyst test:** a strong analyst who converts the old meter, aligns the clocks, applies the 24-hour rule, replays
  each alternative through its tank emptied at its pump station's firm capacity and checks the method on the Northside
  tank files Alternative B (26 MG), 2.8 events a year, the default path's `Ends on:`.
- **Estimand:** Appendix C 2.1 to 2.4: the untreated overflow events from Outfall 014 to the Wennick River, discharges
  less than 24 hours apart one event, averaged over the twelve years of the 2014 to 2025 metered record, for each
  alternative TM-7 offers, against no more than four; the file is `consent_decree_appendix_C_cso_control.pdf`.
- **No decoy:** nothing is planted: the Northside tank's record is the authority's own and replays its own overflows
  exactly because its plant has room, no memo argues for B, TM-7 states no performance figure, and no document ranks
  the alternatives on the decision.
- **No certified replay:** the method is not recovered by reproducing certified figures; no shipped table prints events
  for any tank, and the Northside check passes under both the rating and the room.
- **Lesson:** a storage's performance is set by what receives it, so a continuous simulation that empties the tank at
  its pumps' rating overstates a tank that drains into a plant at its limit; no build on file prices a stored state
  carried between events through another system's headroom.

## Survivor anatomy

- **Actor:** each storm's starting tank volume decides, a state no file stores: it is rebuilt from the overflow
  record, the station's capacity and the Southside plant's hourly influent, and no column of any file holds a tank
  level at Clay Street, a plant room or a dewatering rate in service (test: the 17 columns of the five main-path files
  listed in the column audit; none is the property or one join from it).
- **Link:** the signal is read through a time join between the outfall meter (15 minutes, Eastern Standard Time then
  UTC) and the plant historian (hourly, local time with daylight saving), two systems with no shared key, invited by no
  sentence; TM-7 names where the pumps discharge, as any design memorandum must, and nothing names the room.
- **Reflex:** the field's method, continuous simulation of the record with the tank emptied at its pump station's
  rating, is rung 1 and files B at 2.8 events a year; the event-volume screen beneath it, rung 0, files B at 3.7.
- **Back-test:** the textbook route validates: the Northside tank's 2020 to 2025 inflow replayed through its 8.0 MG at
  its station curve reproduces the overflow detector's events at Outfall 006 in every year, because the Northside plant
  always has room within hours.
- **Second use:** the plant historian is in the pack because the facility plan's baseline flows chapter is built from
  it and both plants' records come in one export; the Northside SCADA carries the returned-volume ask; the outfall
  meter is the decree's own evaluation record; TM-7 and Appendix C carry the alternatives and the estimand. Deleting the
  decisive step drops no file.
- **Shock:** the Southside plant at its limit after storms is the ordinary behaviour of a combined system's plant, the
  historian's flat tops look like every wet-weather month and sort on no shipped statistic as an anomaly; Outfall 014's
  record holds no event set apart.
- **Pins:** the WHAT sits in the decree's Appendix C (population, event, window, unit, limit) and TM-7 (the
  alternatives and their stations); no filed sentence names the tank's drawdown, the plant's room or a dewatering
  rate in service; deleting either document unforces the call by removing the estimand, never by removing a hint.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 event volumes against an empty tank | TM-7 sizes | event table | yes | Northside check refutes it at the margin | no | yes | no | readable |
| R1 continuous replay at the station's firm capacity | TM-7 capacities | none | yes, the field's method | Northside check confirms it | no | no | no | readable |
| R1b R1 with pumping during the overflow | TM-7 says pumping starts after the overflow | none | yes | Northside confirms | no | no | no | readable |
| R2 (decisive) replay bounded by the Southside plant's hourly room | none: no sentence names the room or the drawdown | no column holds room or tank state | no: the reflex empties at the rating | none: the Northside bench passes under both | no | no: a stateful replay over 420,000 steps | no: the historian is the baseline-flows export, and carries both plants | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternatives and their call | Ruled out by |
|---|---|---|---|---|
| SF1 | untreated overflow event | discharges from Outfall 014 less than 24 hours apart are one event | a discharge per 15-minute run with any gap: more events, same call (C) | Appendix C 2.2 |
| SF2 | average year | the record's events over twelve years | the mean of yearly counts: identical (twelve full years) | same call, asserted |
| SF3 | the record | 1 January 2014 to 31 December 2025, Eastern time | UTC year ends: same call | Appendix C 2.3; same call asserted |
| SF4 | meets the limit | no more than four events a year | under four: same call (C at 2.9) | Appendix C 2.4 |
| SF5 | dewatering start | once flow to the tank has stopped | pumping during the overflow: B 6.7, C 2.9, same call | TM-7 3.2; same call asserted |
| SF6 | the meter overlap week | each interval once | both loggers summed: the week is dry, same call | same call, asserted (no discharge in the overlap) |
| SF7 | replay grain | the meter's 15 minutes with the plant's hour held | hourly means of the meter: identical counts | same call, asserted |
| SF8 | the plant's limit | 140 MGD, the headworks limit | 139 MGD (a margin): B 5.9, C 3.2, same call | Appendix C 1.3 (the plant's rated peak); same call asserted |
| SF9 | the tank's start | empty on 1 January 2014 | full: same call | same call, asserted |
| SF10 | the plant clock | local time converted with its daylight saving hour | the clock taken as standard time or UTC (misread by one to five hours): B 6.8 to 7.0, C 2.9 to 3.1, same call | same call, asserted |
| SF11 | the alternative carried | the smallest that meets the limit | a larger one with margin: D, not the decree's test; costs in TM-7 rise with size | TM-7 4 (the authority carries the least-cost alternative that meets Appendix C) |

## Ladder

| Rung | Construction | A | B | C | D | Pick | Dies to |
|---|---|---|---|---|---|---|---|
| R0 | each event's volume against an empty tank | 6.8 | 3.7 | 1.3 | 0.3 | B | the replay: storms within a day of an emptying tank |
| R1 | continuous replay at the station's firm capacity | 5.8 | 2.8 | 0.6 | 0.1 | B | the Southside room |
| R1b | R1 with pumping during the overflow, against TM-7 3.2 | 3.9 | 1.1 | 0.1 | 0.0 | A | TM-7 3.2 and the room |
| R2 | replay bounded by the Southside plant's hourly room (golden) | 9.7 | 6.8 | 2.9 | 1.3 | C | nothing |

- Position: the default path's B is one size below the golden; A fails every rung, D passes every rung.
- Margins: R1's B sits 1.2 events under the limit, so no hedge reaches C from it; R2's B sits 2.8 over and C 1.1
  under; every standing member keeps B over and C under (6.4 to 7.0, 2.8 to 3.1).
- Dominance: the room moves every alternative by 1.2 to 4.0 events a year, more than any convention (at most 0.4).
- Pricing (stumping Part 3): 1) the residue the WHAT leaves is the drawdown pace, a method; 2) the move the call needs
  at B is 1.2 events, the room produces 4.0; 3) the one-group-by route (events a year off the event volumes) files B;
  4) the step estimates nothing (a deterministic replay on the record), so its standard error is the record's own;
  5) the lever is the plant's room, not the outfall's noise; 6) not a change call; 7) no subset of rows hands over the
  room except the flat 140.0 tops, which are the plant's whole wet-weather record; 8) the reflex sweep (event volumes,
  rating replay, pumping in the overflow, rain-driven event counts) files B in every member.
- Worth: the call moves one size (USD 32.5 million in TM-7's estimates) and every graded per-alternative figure.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | Outfall 014's discharges | Appendix C 2.1 |
| 2 Unit of account | events, one per discharge run with the 24-hour rule | Appendix C 2.2 |
| 3 Attribution window | 2014 to 2025, Eastern time | Appendix C 2.3; UTC year ends same call (SF3) |
| 4 As-of dating | the record as metered | C1: one record, no revisions |
| 5 Version basis | the meter's readings | C1: no revised releases |
| 6 Denominator | twelve years | Appendix C 2.3 |
| 7 Weighting | every year equal | C1 (SF2) |
| 8 Window length | the whole record | Appendix C 2.3 |
| 9 Boundary inclusivity | no more than four | Appendix C 2.4; no alternative sits on four |
| 10 Rounding path | events a year to one decimal, counts over twelve; no count at a twelfth's half | asserted |
| 11 Tie-break | none needed | C1 |
| 12 Maturity and censoring | full years only | C1 |
| 13 Order of operations | convert, align, replay, count | C1: the replay is the only order |
| 14 Row order | the meter sorted by time | asserted over the two loggers' orders |
| 15 Duplicate resolution | the overlap week once | C1, dry week (SF6) |
| 16 Identity normalisation | the two loggers one outfall | the meter's site field |
| 17 Netting against gross | none | C1 |
| 18 Dimensional units | MGD and MG | the headers (cfs, MGD) |
| 19 Code and status semantics | the historian's tag rename | the tags' plant prefix |
| 20 Integerisation | event counts | C1 |
| 21 Clause scope | Appendix C per outfall | Appendix C 2.1 |
| 22 Forward window contents | the record replayed for the tank in service | Appendix C 2.3 files the record as the evaluation basis |

## Literal reader

Executing Appendix C and TM-7 word for word on the pack (the record, the 24-hour rule, the four tanks, pumping after the
overflow stops) leaves one method choice open, the pace the tank empties, and every member that reads the plant's own
record for that pace picks C; the literal reader who takes the stations' firm capacity as the pace picks B, the
default path, which is an easy method on the same literal estimand, not another reading.

## Oracles

The Northside tank's record confirms the rating replay at Northside and confirms the room replay equally (its plant
always has room), so it ties under both bases and arbitrates nothing at Clay Street. No published or certified figure
prints events for any tank. The overflow detectors' public notification log for 2025 (a distractor) counts Outfall
014's own untreated events without a tank and ties under every basis.

## Ask sheet

Two asks, 53 figures, plus the deck's chart of the call's own figures (a main-call deliverable, not an ask). Both are
the annual report's own items (Appendix C 4.1), wanted from the same pull; neither reads a row the call reads. Every
figure a device moves is moved by a second, independent reconstruction across another system or grain as well, so no
single fix hands over the figures the first one moves.

**Ask 1: each rain gauge's recorded rainfall in each month of 2025** (48 figures, inches to the hundredth).
- H18 home: the annual report's rainfall table; use: the decree requires it each year.
- Files and columns on the path: `rain_gauge_tips_2014-2025.csv` (gauge_id, tip_time), `rain_gauge_field_service_2014-2025.xlsx`
  (Date, Gauge, Arrived, Departed, Notes), `rain_gauge_inventory.csv` (gauge_id, depth_per_tip_in, logger_model,
  logger_installed), `consent_decree_appendix_C_cso_control.pdf` (4.1, months in Eastern time).
- Primary device 1 (D5, out-of-scope rows known by structure): the technicians' calibration pours are logged as tips.
  From July 2025 the field maintenance contract visits every gauge monthly and every visit carries a cal check, the
  crew waiting for a dry spell on the day; before it, visits come every five to eight weeks and most carry one. The
  field log gives arrival and departure to the five minutes, departure as the van leaves, which a pour's tail often
  outlasts, so only the steady run of tips (one every 8 to 10 seconds) finds all of it. 29 cells move if the pours stay.
- Primary device 2 (D2 across a second system, layered on the same cells): the contract's July visit fitted every
  gauge with a new 0.2 mm tipping mechanism (field log: "new TB mechanism installed (0.2mm unit, contract stock)"); the
  inventory still says 0.01 in a tip for all four. Every July to December cell carries a pour and the new mechanism,
  so finding either alone keeps none of them. 24 cells move on the mechanism alone.
- Primary device 3 (D8, clocks): the HOBO loggers stamp Eastern Standard Time all year, the TipLink C200 cellular
  loggers installed at RG-3 and RG-4 in May 2024 stamp UTC; nothing in the file says so (the inventory gives the model
  and the date). Pours cut by the logged window miss at RG-3 and RG-4 and in summer at RG-1 and RG-2; month-end
  storms move between months.
- Hazard (D1): the cellular platform re-sent four buffered batches at each TipLink gauge, exact duplicates.
- Pin test: the asking sentence pins the gauge, the month and the unit; Appendix C 4.1 pins Eastern time and "recorded
  at the Authority's rain gauges"; no pin names a pour, a clock or a mechanism.
- Realism: a tipping-bucket network's export, field log and inventory, as a utility's field services keep them.

**Ask 2: the volume the Northside tank returned to the Northside interceptor in each year 2021 to 2025** (5 figures,
nearest million gallons).
- H18 home: the annual report's storage facility line; use: Appendix C 4.1.
- Files and columns: `northside_tank_scada_2020-2025.csv` (Timestamp, NT_LIT601_FT, NT_FIT600_MGD, NT_P1_RUN to
  NT_P3_RUN), `northside_tank_om_manual_section4.pdf` (Table 4-1, the station curve, the control),
  `cmms_work_orders_2020-2025.csv`.
- Primary device 1 (D3, a reading re-referenced): LIT-601 was re-mounted on a new bracket on 23 August 2023 and reads
  0.45 ft with the tank empty; the hopper floor's stage-storage is not linear, so every fall read uncorrected is
  wrong, most of all the lead pump's short cycles near the floor; 2023 to 2025 move.
- Primary device 2 (another system, layered on the same years): the diversion's sluice gate SG-600 passed dry weather
  flow into the tank while its seals were failing (June 2022 to February 2023, September 2023 to January 2024, July
  2024 to March 2025, August 2025 on; the work orders record the operators' reports and the seal replacements), and
  storm tails under O&M 4.3's 1.0 MGD hold enter while the pumps run; what the pumps returned is the fall in storage
  plus FIT-600's inflow over each pumping quarter hour. Level falls alone miss 2022 to 2025.
- Primary device 3 (D2, a silent switch): P-2 came back from rebuild on 14 March 2023 with a trimmed impeller; the
  run states times the O&M station curve miss every year (they also count a full quarter hour where the tank emptied
  part way through it).
- Pin test: the sentence pins the tank, the year and the unit; no pin names the transducer, the gate, the meter or the
  route.

**Main population, zero counts:** the Outfall 014 meter carries no duplicate quarter hour outside the dry overlap
week and no ask device; the Southside historian rows carry none (asserted, `SEP` in `checks.py`).

**Referee:** none arbitrates a device; the Northside detector ties under every handling.

| Path (cracker = lands the call, runs the battery, executes filed documents) | Rainfall kept | Returns kept | Verdict |
|---|---|---|---|
| Ask 1, cracker: duplicates dropped, pours cut by the logged window, stamps as logged, 0.01 in a tip | 12 of 48 | | miss |
| Ask 2, cracker: the better of run states times the station curve and the uncorrected level falls | | 1 of 5 | miss |
| Ask 1, one crack: pours by their steady run | 16 of 48 | | miss |
| Ask 1, one crack: the loggers' clocks | 18 of 48 | | miss |
| Ask 1, one crack: the 0.2 mm mechanisms | 12 of 48 | | miss |
| Ask 2, one crack: the re-mounted transducer | | 1 of 5 | miss |
| Ask 2, one crack: FIT-600's inflow while pumping | | 2 of 5 | miss |

Single cracks keep 24.5 to 35.8 per cent of ask weight; the worst, the loggers' clocks found by both top responses,
puts the pair at 48.2. Two cracks on one ask (pours and mechanisms) keep 75.5 per cent of the ask weight, which is the
full includer's ground, not the reflex.

Mirror leakage: 24.5 per cent of ask weight (the mirror takes the cracker's ask paths off the call).

Pair ceiling: 42.0 (cracker on the call 58.5, mirror off it 25.5); worst single crack 48.2.

Measured by: generator/ceiling.py, run on the cut pack.

## Layer 1 inventory

| Item | System that produces it | Where | Moves the call? |
|---|---|---|---|
| Outfall 014 meter replaced June 2019: cfs on Eastern Standard Time, then MGD on UTC; one week of overlap | the flow monitoring contractor's two loggers | meter parquet | no: the overlap week is dry; the conversion is a header (flow_unit) |
| Plant historian in local time, the November hour twice and the March hour missing; tags renamed 15 March 2021 | the plant SCADA historian and its upgrade | influent csv | no (SF10 asserted) |
| Ten spells of BAD-quality hours in settled weather, value 0 | historian communication drops | influent csv | no: every tank is empty then (asserted) |
| Southside readings at the limit hover a little under 140.0 | the headworks gates throttling | influent csv | no (SF8) |
| Work order numbering and date format change in July 2022 | the CMMS replacement | work orders | no |
| Calibration pours as tips; field times to five minutes | technicians' practice | tips, field log | ask 1 only |
| TipLink loggers stamping UTC from May 2024 | the cellular logger replacement | tips | ask 1 only |
| Every gauge's 0.2 mm mechanism from the July 2025 contract visit, inventory unchanged | the field maintenance contract | tips, field log | ask 1 only |
| Monthly contract visits from July 2025, each with a cal check | the field maintenance contract | field log, tips | ask 1 only |
| Re-sent duplicate batches | the cellular platform | tips | ask 1 only |
| LIT-601 re-mounted 23 August 2023, reading 0.45 ft high; blank during the cleanout | maintenance | SCADA | ask 2 only |
| P-2 rebuilt March 2023 on its old tag | maintenance | SCADA, work orders | ask 2 only |
| SG-600 passing dry weather flow into the tank while its seals failed; the lead pump cycling | the diversion gate, operations | SCADA (FIT-600), work orders | ask 2 only |
| Northside overflow detector firing through the August 2023 cleanout bypass | operations | SCADA | the back-test only (asserted within 3 events) |

## Tried and rejected

Architecture 1 (Quellbrook rock salt), carried from its note:


- Pattern E on the card: E's discriminator is an absolute split, which this build does not have (the gain falls
  continuously with coverage), and the structural tests collided with five older builds; the pattern is none with G14.
- The city named Halbrook: within one letter of Holbrook (a real place); renamed Quellbrook after a check.
- The first collector parameters (Priority 1 hazard spots at 10.0 t and Priority 2 at 9.0 t a lane-km): the golden
  (2,206 t) sat on the midpoint of the default (2,652 t) and the pooled gain (1,768 t), so a response averaging two
  rivals filed the call; the hazard rates were re-set (9.7 and 10.2) and the earlier transit moves given inner-suburb
  coverage, so every midpoint of rivals now files 2,000 to 2,100 t.
- Centreline km asserted as neutral on the call: rates and lengths taken in centreline km throughout file 1,900 t,
  because collectors have two or four lanes; closed by the plan's application rates set per lane-km (SF3), not by data.
- One device carrying Ask B (the run totals alone): a cracker who dedupes per run recovered all twelve figures; the
  combined salt and brine mass (B1b) was added on the same controllers.
- Ask A's second device as transfers alone: it moved two yards only; the weighings at another yard's scale (A2) move
  all four, and the transfers stay as a hazard.
- Passes of one truck overlapping in time (two runs entering one segment in the same second): the sweep found them; a
  circuit's passes now run one after another on its one truck, with every tonnage unchanged.
- The forum `line_manager_or_team` (the director of roads signing the commitment): `ban.forum` blocked registration
  against task247, so the forum was redrawn to `council_or_assembly` in the build itself: procedure RO-PR-07 5 sends
  spending above the contract quantity to council under the procurement by-law, the deliverable became a one-page
  report to council, and the prompt names council; every figure unchanged.
- The supplier named Brackwater and the contractor Pellard: one letter from Blackwater and Pollard (H21); renamed
  Northgrit and Kettlewood after a search, every tonnage unchanged.
- The 2025-26 winter at 52.6 WSI points: the default netting at last winter's severity, or last winter's totals netted
  with no planning severity, landed 2,200 t by coincidence (52.6 sat inside the band, about 51 to 54 points, where the
  netting's figure scales into the golden's bin); the storm sequence was redrawn to 58.4 points, the per-point golden
  unchanged, and the route now files 2,400 t (asserted, LADDER R1c and HEDGE).
- Street rates as steady as a model (a 4 per cent winter-to-winter variation, the gain line at r = -0.98) and coverage
  blind to block length: each street now carries its own winter-to-winter multiplier, Priority 2 salt rises as blocks
  shorten, and the earlier moves were raised from 202 to 431 so that one standard error stays under 16 t; the golden
  came out at 2,202.6 t, inside the re-centring rule's 15 t, so R_MID did not move.
- The earlier flat moves given less coverage than the new streets (a different hazard share): the banded estimators
  then filed 2,100 t; the flat streets each reason brought in now carry the redesign's own hazard share, and every
  standard banding files 2,200 t.
- Ask B's arterial figures to one decimal with the yard basis left to the reader: the judge found the register's
  current yard a licensed second reading (about 800 t a winter at Kelvin Road and Mapleford) and no exact route for the
  older controllers; the ask now files the yard each circuit belonged to that winter, the plan files the pre-wet rate
  that makes the combined mass exactly checkable, and the figures are asked to the nearest tonne, which every honest
  construction shares.
- Every circuit run by one truck for three winters: trucks now swap between circuits of their yard and kind about one
  storm in seven; every tonnage unchanged in kind.
- The council item filed as a memo: a council item is a staff report, so the deliverable is
  `seasonal_salt_commitment_council_report.docx`, with the chart introduced as the programme the rolled-over contract
  carries.
- Cross streets named without a suffix (a naming bug in the second round of street names): fixed in the generator,
  every tonnage unchanged.
- Winters as steady as the index (the Priority 1 collector rate per point within 2 per cent across winters of 38.9 to
  67.2 points, the recheck's realism finding): each winter now carries a swing the index does not carry, common to every
  road (a winter's multiplier drawn with a 3 per cent spread, the realised rate per point spanning 14 per cent, inside the
  10 to 25 per cent real fleets show); R_MID then moved by the re-centring rule alone.
- Salt in proportion to severity closed by the data (the never-moved collectors' intercept near nil): under each
  winter's swing five winters tilt the line (an intercept of about a fifth of a winter's salt), so the plan now files
  that salt is planned per WSI point (SF6).
- One-winter windows as plain family members: each carries its winter's own swing; the family reads them netted against
  the never-moved collectors' same winter, and un-netted they stay in the bin, no longer a quarter-bin clear.
- 431 earlier moves in steady yearly counts (122, 112, 107, 90): each year now carries its own programmes (136, 69, 119,
  53, 377 in all); one standard error rose from 14.7 to 15.0 t.
- Three equal-count bands as a family member: on the new draw its second band (2.2 to 5.2 t a lane-km) holds the new
  streets' upper eighth and sits 1.1 t above them, and it files 2,147.8 t; it is listed with the median split and the
  wide kernels as a coarse setting that closes on the golden as it is refined, and nothing was moved to bring it back.
- The 10 earlier moves nearest the pool's mean as a crude setting that lands: it files 2,294.9 t on this draw; thin
  settings are asserted from 30 streets up, where they settle in the bin.
- R2i (the earlier moves inside the new streets' range, averaged) as a rung 100 t or more from the golden: it now sits
  77 t below (2,136.4 t), so it is listed with the crude conditioned forms.
- The gain component at one decimal (5.2, 0.045 from its edge, with four family members at 5.1 on the previous draw):
  stated as about 5 t a lane-km, the precision every construction shares (SF12).
- The own-salt component at one decimal (1.7 lane-km weighted against 1.8 as the streets' unweighted mean, the
  recheck's fork): stated over the five winters as about 700 t, under 2 t a lane-km, which every basis shares (SF13).
- The arterial figures to the nearest tonne: the loading-log calibration came within 0.2 to 6.6 t of the records'
  route, so the correction of the older controllers was unpinned at the tonne; the figures are asked to the nearest
  50 t and every cell sits a quarter-bin or more from its edge under both routes (asserted), while the brine left in
  still lands a full cell high and the run totals summed every row miss by a tonne a row.
- Route audit entries keyed row by row (the redesign over 52 days, a segment's priority and route rows on one day 2.8
  per cent of the time): the audit keys each change in a few sittings on working days, both rows of a segment together,
  and the change numbers follow the keying order.
- The one-sigma claim as written (every family member within one standard error): it holds with the golden's own
  error, not each member's; restated in `## Ladder` and in SIGMA.
- "On every pool alike" for the length effect: measured, it shows plainly on the redesign's streets and hardly on the
  earlier moves; the note now says what the data show and both pools are asserted.
- A2, the weighings at another yard's scale with the receiving dome in the remarks: the stage 4 blind reader read the
  four spellings and moved each load to the dome they name (Lakeshore's only after its flight), keeping all eight dome
  figures; re-sited as A3 and A4, the trucks still weighed on the way for a day after each scale came back, which the same
  remark routing counts twice or keeps at the weighing yard; the outage weighings stay as texture (HA5).
- A1, the survey's capture window in UTC: the reader converted the flight log to Eastern daylight time and cut at each
  flight's start; a clock re-sited onto the scale houses (a terminal on standard time, or one stamping UTC) was tried and
  dropped, since the yards held deliveries through every flight, so a cut at the flight's start agrees with one at its
  end for any offset under an hour, and a log stamped in UTC has nothing in the pack that forces the reading; it stays as
  texture (HA4).
- HA1, the dispatch re-issue: the reader took the latest issue's BOOKED October lines; re-siting it as an October booking
  delivered early in late September was tried and dropped, since nothing in the pack ties a September weighing to an
  October booking without a filed note; it stays as texture.
- B2, the contractor's circuits: the reader added every row of Kettlewood's returns, which is right; two re-sitings were
  tried and dropped, relief operators on City trucks reported in the returns (the rows would have to name City units,
  which announces it, and a contractor reporting a City truck's salt reads as planted) and returns by billing period, the
  26th to the 25th (it moves only Kelvin Road's and Mapleford's 2024-25 cells, the one winter with storms after 25
  March); it stays as the mirror device.
- HB2, the register's current yard: the reader took the yard from the route code as run and kept MPF-A01 and MPF-A02 at
  Mapleford; re-sited as B3, the platform carrying the two circuits' current Kelvin Road codes on every pass they made,
  so the code a pass carries is the misreading and the revision log's 1 July 2026 entries are the key.
- B1 and B1b, the run totals and the combined mass: they held six cells, and the reader landed the other six by halving
  the fleet list's M410 rows after reading them double against the loader log (a yard's runs average about two segments,
  so halving sits inside a cell where the brine and the run lengths offset); the evidence is re-sited from the fleet
  list's controller columns and the loader log to the rows' own run references and litres, the rows untouched (R0 and R0b
  read them as written).
- The yard loading log: each unit's winter at its loader tonnes is the salt it spread within its hopper's carry, so a
  loader-only route lands every arterial cell and the per-unit ratio hands any reader the halving, an oracle under ban 3;
  withdrawn, with the settle that kept the loader calibration inside each cell left as it was so the arterial rows stay
  byte for byte.
- The changeover weighings as one device: with every copy on the receiving yard's stored tare, dropping exact repeats gave
  back all eight dome figures (a pair of 42.8 with one device found, against the build's 40); the two unremarked copies
  carry their own scale house's older stored tare, so only the truck, the day and the gross tie them (A4).
- HB1, the UTC season dates: the reader converted them; nothing at a season boundary carries enough salt to move a cell,
  so it stays as texture.
- A3 and A4 as built in the repair's first round: invisible to a grader who checks consistency, since the supplier's
  trucks were drawn at random for each load (some at two scale houses minutes apart on ordinary days) and the tares at
  random for each weighing, so nothing contradicted a load weighed twice; the re-judge (judge-task165d) kept both
  weighings and could not find the golden's rule. The trucks now run round trips from the terminal and each scale house
  keeps one stored tare a truck for each account, so the five pairs are the only trucks back inside a round trip.
- B1 and B1b with nothing naming the controllers (the first round): the re-judge read the counting once as inferred and
  the brine as an unfiled convention, its brine's salt off every row keeping seven cells; Fleet Services' work orders
  now carry the four replacements and every tandem's calibration at 40 L/t, so the litres a tonne force the brine's whole
  weight and the work orders tie the repeated totals to the controller.
- A supplier's delivery statement by docket as Ask A's referee: one reconciliation would expose all five weighings at
  once and its loadout weights would offer a second dome basis beside the scale houses; the trucks' own times between
  scale houses do the work inside the log the ask already reads.
- Filing the older controllers' conventions in the dictionary (the re-judge's fix): a filed sentence that adjudicates,
  handing B1 and B1b to every reader; not taken.
- The controller model on every calibration work order: a controller list by unit and winter, the fleet list's
  withdrawn columns in another file; the model is named only where a controller was replaced.
- The asks' handling left to the pack alone (rounds 1 and 2): both re-judges, cold on the pack, took the readers' paths,
  and judge-task165e never tested the trucks' round trips, so the dome figures read as wrong although every arterial
  cell reproduced; block 3 now names each ask's handling, its filed basis and its result (steps 6 and 7), the pack
  unchanged.
- Step 6's first wording (round 3): the dome stocks followed the dispatch file's BOOKED October loads, and
  judge-task165f read them as the booked loads; each figure now carries its label, and the home yard's ticket cites
  RO-PR-07 section 2's "weighed at the yard's scale house".
- 2026-10-31, reship under the learning loop's rules: the data dictionary and the export manifest withdrawn (shipped
  files may not describe the data); the conventions they carried are the data's own (the KG and applied_t headers, UTC
  in entry_utc, the crosswalk file), and the plan's materials section names the codes RS, SALT, SS and SAND/SALT in the
  organisation's own words. The prompt dropped the 424 lane-km (a count the register holds) and drew a fresh shell.
- 2026-10-31, remarks on the two A4 pairs to close the judge's Gate C residual: rejected before cutting; it moves A4's double count onto Lakeshore and Mapleford and hands back Ridge's and Kelvin Road's four dome figures on every careful path.
- 2026-11-07, architecture 1 on the portal: R1 regressed each earlier move's gain on its own Priority 2 salt, read it at
  the new streets' and filed 2,200 t (100 per cent); R2 filed the default 2,600 t and kept 70 per cent through the asks.
  Conditioning a carried gain on a covariate every unit's own history prints is the strong solver's reflex, and the
  ask devices (double weighings, older controllers, realigned circuits) were found and handled; the world is spent and
  the slot re-roots (architecture 2, the Clay Street tank).

Architecture 2 (the Clay Street tank):

- 2026-11-07, a redesign inside the salt world (a stronger decisive step on the same streets): rejected before any
  data; one architecture per world, and every candidate step there was again a covariate the record prints.
- 2026-11-07, a sewer overflow world first framed with shape 10, a board forum and a statutory filing: blocked by the
  guard against task156 v3; redrawn to shape 08, the regulator receiving the facility plan and the design task order.
- 2026-11-07, the city named Vellmore, then Marrowgate and Tarnhollow: within two letters of Fillmore, Harrowgate and
  Tar Hollow; named Quessling after a search.
- 2026-11-07, tanks of 12, 20, 26 and 34 MG on the first tuning: the room moved the counts by under one event at the
  smaller tanks with too little rain (33 inches a year); the storms were deepened to about 40 inches a year (the
  Pennsylvania norm), the regulator raised to 26 MGD and the sizes redrawn to 19, 26, 38 and 50 MG.
- 2026-11-07, Alternative A at 18 MG: its golden count (111 events, 9.25 a year) sat on a twelfth's half at one
  decimal; moved to 19 MG (104 events, 8.7).
- 2026-11-07, storms wettest by far in late April (8 inches in April 2025, 0.3 in July): unlike Pennsylvania; the storm
  season was flattened and the spring weight left to the groundwater's reach into the Southside sewers.
- 2026-11-07, calibration pours whose logged visit always covered them: a path that found the loggers' clocks and cut
  the pours by the logged window kept 43 of 48 rainfall cells; the log now gives times to five minutes and departure
  as the van leaves, which a pour's tail often outlasts (35 of 48 on that path).
- 2026-11-07, RG-4's 0.2 mm mechanism from August 2025: it moved five cells; moved to 15 May 2025 (eight cells), the
  hour chosen so that no cell sits within 0.03 hundredths of a rounding edge.
- 2026-11-07, Northside returns at the first draw of Outfall 006's runoff: 2022 sat 0.02 MG from a rounding edge; the
  runoff factor moved from 9.5 to 9.9, every Northside year now 0.1 MG or more from an edge.
- 2026-11-07, the Northside plant at 110 MGD: its room bound the tank's pumps in a few hours, so the rating replay and
  the room replay could part at Northside; rated 125 MGD, the room never binds while the station pumps (asserted).
- 2026-11-07, Appendix C 1.3 saying flow above the headworks capacity is held back in the interceptor: it states the
  mechanism the decisive step recognises; cut to the plant's rating alone.
- 2026-11-07, the first ask layer at stage 3 (pours in about half the gauge-months, one gauge's 0.2 mm mechanism,
  the transducer alone on the Northside returns): the cracker kept 43.4 per cent of the ask weight and one crack (the
  loggers' clocks, or the pours by their run) kept 70, a pair near 67 if both top responses found it. Each figure a
  device moves now carries a second, independent reconstruction: the contract's monthly cal checks and every gauge's
  new mechanism from July 2025 on the same cells; SG-600's leak-by metered by FIT-600 on the same years as the
  transducer. The main call, the stump and every main-call figure frozen (freeze.py rubric PASS).
- 2026-11-07, the contract and the new mechanisms from January 2025: no device-free cell was left (the cracker kept
  0 of 53), harder than the ask layer needs and short of the third the asks aim at; moved to July 2025 (24.5 per cent
  kept, worst single crack 35.8).
- 2026-11-07, O&M Table 4-1 printed at 0.25 ft steps with levels to one decimal: the extracted table paired 0.25 ft
  rows with 0.2 ft labels; printed at 0.1 ft in the hopper, levels to two decimals and volumes to four, so the
  mass balance reproduces the delivered volume within 0.4 MG a year.
- 2026-11-07, the Northside tank's inflow added before its pumps ran in a quarter hour: a full tank sent the storm
  tail over the crest in the same quarter hour the pumps started, which no meter sees; the pumps now draw down while
  the trickle enters.

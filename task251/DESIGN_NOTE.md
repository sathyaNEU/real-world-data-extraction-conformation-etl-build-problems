# task251 design note

## Draw

Card `cards/task251.json` (architecture 5, re-rooted 2026-10-21 from architecture 4, spent at stage 4; drawn fresh at
the author's standing instruction, see Tried and rejected and the card's lineage). Guard verdict WARN, no BLOCK. The
WARNs, answered: overuse.gate_g (method_or_model_selection in 5 of the last 12: the two methods are the validation day's
error and an error model with a load term and a cold term, each pinned by the data's own pairs, which is the
vocabulary's definition; no other mechanism is honest here); repeat.decision (designation_set after task479: the decision
is the set of stations the report flags and the contractor recalibrates); repeat.deliverables (xlsx and png after
task272: the list goes to the contractor as a workbook and the report prints the chart); repeat.question_form (which
after task479: a pick of stations). driver.near 0.46 against architecture 4 is differentiated on the card: architecture
4 read one condition, which a stage 4 reader found from the bridge pairs; architecture 5 needs a second, independent one.

- **Pairing.** General Statistics & Data Science / missing-data-censoring-measurement-error, drawn for Data Quality
  Monitoring & Alerting. The object is the health of a regional municipality's permanent traffic counts, and the call
  is a monitoring decision: which count stations the 2027 report flags as not meeting the counting standard, the same
  stations the maintenance contractor recalibrates in the spring 2028 round.
- **The seed, re-found.** DQ24 gave the world (instruments checked against a reference), the decision (which instruments
  go for recalibration) and the quantity (each instrument's error against a tolerance). Architectures 1 to 4 spent a
  reference chain, a wear clock, a selection on the measured value and a single load-dependent loss read from
  conservation pairs. Architecture 5 keeps architecture 4's world and makes the decisive step a conjunction found in the
  data's own structure: the summer filming sees neither the vehicles the loops lose in term-time queues nor the vehicles
  the older TCX-2 cards miss on cold days; the river bridges' paired approaches measure the first, the bridges whose two
  approaches run different controllers measure the second against the airport's temperatures, and occupancy per counted
  vehicle, which holds flat on the TCX-4s and climbs on the TCX-2s in the cold, says which generation errs. Either
  correction alone files a different list.
- **Probes before the build.** Three isolated readers (Sonnet, medium) on the seed-303 pack, asked the call only: A filed
  R10-03, R23-01 and R25-01 (the cold effect read as a TCX-4 overcount, no queue loss), B R04-03, R14-01 and R25-01
  (the queue loss from the same-road pairs, the cold effect read as a TCX-4 overcount), C R04-03, R06-01, R14-01 and
  R25-01 (the TCX-2 cold miss from occupancy per counted vehicle, the queues seen and left out). None landed.
- **Niche.** The Regional Municipality of Halbrook (fictional, southern Ontario) counts traffic at 30 permanent stations
  on its regional roads, inductive loops in every lane reporting each hour's vehicles and occupancy to the count
  management system through one of two controller generations, 15 older TCX-2 and 15 newer TCX-4 (two stations moved
  from the first to the second during 2027 and were renumbered). Five of the stations' pairs stand on the two approaches
  of its Kessel River bridges, counted since a 2019 crossings study; three of the five pairs run one controller of each
  generation. Every July and August a contractor films each station for one weekday and counts every vehicle. TDP-03,
  the region's counting standard, flags a station whose year's count misstates the vehicles that passed by more than 5
  per cent, and the flagged stations go to the maintenance contractor's spring recalibration.
- **The call.** Which stations' 2027 counts are beyond 5 per cent either way, if any.
- **Shape.** other: the list (each of the 30 stations in or out; the validation days keep five of the seven out and
  neither correction alone brings in all seven), the chart of every station's error against the band with the list
  marked, and the asks' 24 figures (maintenance visits and power failures by district and quarter): about 35 criteria.
  No station's error is a graded figure; the list and the margin every licensed estimate keeps are.
- **Strategy.** `composition_mix`: a station's error depends on the traffic state and the weather its controller works
  in, the validation day's states (summer free flow only) differ from the year's (term-time queues, frost), and the
  queued state's loss and the cold days' miss have to be measured elsewhere and carried through each station's own mix
  of hours by the controller in force. Gate G method_or_model_selection; generators G5, G7, G17; gap population;
  calibration other (conservation pairs, see the card); context artifact operations_log (the maintenance contractor's
  2027 work orders, which answer their own question and rank nothing); Layer 2 field_method, pattern
  own:conservation-pairs-load-dependent-detector-loss.
- **Forum, event, organisation.** customer_or_counterparty (the maintenance contractor receives the recalibration list),
  statutory_or_regulatory_filing (the annual count report the region files with the province by 31 March 2028, flags
  included), local_government. Role compliance_or_audit (the traffic data coordinator answers for the counts' accuracy).
- **People** (`guard.py names --geo Canada --seed 251`, locale en_CA): Miranda Harris, the traffic data coordinator, who
  asks; Andrew Wong, the validation contractor's project manager; Yvonne Larson, the maintenance contractor's service
  manager. None appears in the prompt.
- **Data-native sentence.** A loop counts a vehicle when its occupancy pulse starts and ends; in a crawling queue two
  vehicles hold one pulse, and on the older cards, whose tuning drifts as the pavement freezes, the gap between close
  vehicles stops registering on cold days, while the time the loop is covered, its occupancy, is unchanged; the summer
  filming sees neither, a bridge's two approaches count one stream with nothing joining or leaving, and where they run
  different generations the pair's ratio moves with the temperature.

## Default path

1. Read TDP-03 (the year's error: the vehicles counted in the hours counted against the vehicles that passed, both
   directions, beyond 5 per cent flagged) and the station register.
2. Read the contractor's 2027 validation counts: for each station, 24 hours on a July or August weekday, the video
   count and the loops' count by direction and 15 minutes.
3. Take each station's error as its loops' count against the video count over the validation day, both directions.
4. Flag the stations beyond 5 per cent.

Ends on: R14-01 and R25-01
Golden: R02-01, R04-03, R06-01, R08-05, R14-01, R25-01 and R29-03

## Stump sentence

A competent solver takes each station's 2027 error from its summer validation count and flags R14-01 and R25-01; the
filmed days were July and August weekdays with no hour above 8.2 per cent occupancy and no day below 13 degrees, so they
miss the vehicles the loops lose in term-time queues, which the bridges' paired approaches show growing with occupancy,
and the vehicles the older TCX-2 cards miss on cold days, which the bridges whose approaches run different controllers
show against the airport's temperatures; the queue loss alone files R02-01, R04-03, R08-05, R14-01 and R25-01, the cold
miss alone R04-03, R06-01, R14-01 and R25-01, and only both file R02-01, R04-03, R06-01, R08-05, R14-01, R25-01 and
R29-03.

## Three rules

Task type: missing-data-censoring-measurement-error (General Statistics & Data Science), tagged in the taxonomy for Data Quality Monitoring: a measurement-error model with a load-dependent term and a temperature-dependent term confined to one instrument generation, each estimated from a natural pairing of instruments on one conserved stream because the validation design never sampled the load or the temperatures at which the errors arise.
Domain test: The deciding quantity is each count station's error over the traffic it carried in 2027, the loops' sensitivity together with a loss that grows with occupancy in queued traffic and the older detector cards' miss on cold days: a measurement-error model the traffic data field estimates where the same vehicles are counted twice with nothing joining or leaving and carries through each detector's own hours by the controller in force; replacing it with each station's validation-day error, the generic calibration summary, changes the list.
Swap: "the stations whose count is beyond 5 per cent once the loss the bridges' paired approaches show in queued traffic and the older cards' cold miss the mixed pairs show against the temperature are carried through each station's hours" put into a hospital's glucose meters loses its mechanism, since no two meters read the same blood with nothing added or taken between them while one of them sits in a queue, and no meter generation loses readings when the pavement freezes; replacing the model with each station's validation-day error changes the list.
Layer 1: the count management system's hourly export in local time with each hour's UTC offset (the autumn hour twice, the spring hour missing); the contractor's own site codes against the region's station numbers; two stations renumbered when their controllers were replaced; occupancy to one decimal from the older controllers and to two from the newer ones; the hours a controller lost to a power failure absent from the export; the contractor's sheets per station, direction and 15 minutes on different days; the network file keyed by road and kilometre point; the airport's daily summary in the weather service's own export layout with its flags and a missing day; for the asks, TrafficVault's event log in UTC with the repeats a controller sends after a lost poll and a cold start's unset clock, and the maintenance contractor's work orders with route orders, two-technician lines and multi-day jobs.
Layer 2: field_method under composition_mix: the error depends on the traffic state and the weather, the validation day sampled only summer free flow, and the queued state's loss is measured on the conservation pairs and the cold miss on the pairs whose two approaches run different controller generations, both carried through each station's own hours by the controller in force.
Decisive step: estimating each station's 2027 error with both a loss term that grows with occupancy, fitted on the bridges' paired approaches, and a cold-day miss on the TCX-2 cards, fitted on the mixed-generation pairs' free-flowing days against the airport's daily mean temperature and placed on the TCX-2 because their occupancy per counted vehicle climbs in the cold while the TCX-4s' holds flat, carried through every hour by the controller in force, rather than the summer validation day's error or either correction alone.
Not semantics: every field reads as what it is (vehicles counted in the hour, occupancy, the video count of the vehicles that passed, the day's temperatures), and nothing in any field, code, unit or definition says that loops lose vehicles in queues, that either controller generation misses vehicles in the cold, or that the validation days held neither; the bridges are structures in the network file, the controllers a column of the register and the temperatures the airport's daily summary.
Not rule application: no filed sentence says how a station's year error is estimated; TDP-03 defines the error over the hours counted and states the validation programme's facts, so executing every filed rule on the validation counts files the validation list, and no rule names the temperature, the controller generation or the bridges.
Analyst test: A strong analyst who reads the standard, the register, the validation counts and the hourly counts takes each station's 2027 error from its validation day and flags R14-01 and R25-01; one who reads the queue loss from the bridges' pairs flags R02-01, R04-03, R08-05, R14-01 and R25-01, and one who reads only the cold miss R04-03, R06-01, R14-01 and R25-01; only both file the seven (checks.py runs every route on the clean world and on the pack).
Estimand: each of the 30 stations' 2027 count error, the vehicles it counted in the hours of 2027 it counted (both directions, every lane) against the vehicles that passed it in those hours, less one; a station is flagged when its error is beyond 5 per cent either way (TDP-03 section 5 and the prompt).
No decoy: nothing is planted: the validation counts are true counts of the vehicles on their days, the loops' counts are what the loops counted, the temperatures are the airport's own daily summary, no memo, draft or figure argues for any list, and no file ranks the stations by error.
No certified replay: no certified or published figure sits in the pack; the validation workbook states counts and no accuracy verdict, and no file states a station's error, flag or annual traffic.
Lesson: a validation that never samples the conditions in which an instrument errs cannot give its error over a year that holds them, and when two conditions act on different instruments each needs its own natural experiment: a stream counted twice with nothing joining or leaving measures the queue loss, the same stream counted by two instrument generations measures one generation's weather miss, and a second channel the miss does not touch says which generation it is; no shipped build reads a counting error from conservation between counters of two generations.

## Ask sheet

Ask A: for each district and quarter of 2027, the maintenance visits to the count stations (12 figures). Ask B: for
each district and quarter, the power failures the stations had (12 figures). Both read the maintenance contractor's
work orders and TrafficVault's event log, which the call never reads, and ask B the breaks in the hourly record, which
the call's estimand leaves out (the hours counted); the call on the full world record files the same list, every error
within 0.2 points (separation asserted).

Devices, silent (no filed sentence points at any of them):
- Ask A: at TCX-4 stations the contractor clears some communications faults by resetting the controller from its
  office and books the half hour against the work order like any visit, with the same description and resolution; two
  or more in every district and quarter. Only the cabinet door log's silence that day shows the technician was not
  there. Moves every figure of ask A.
- Ask B: a TCX-2 has no battery and reports nothing, so its power failures exist only as breaks in its hourly record,
  at least one in every district and quarter; and where a feeder recloses and trips again within the hour the TCX-2
  discards both partial hours and its record shows one break, while TrafficVault's polls inside it failed, succeeded
  and failed again (re-trips at TCX-2 stations in five cells).
Hazards: route orders covering four stations on one labour line, two-technician lines, multi-day orders, the
validation crew's and the Region's own cabinet openings (the door log read as a roster), the replacement controllers'
DOOR_OPEN under the unset clock, the register's current controller for the two renumbered stations' TCX-2 months, an
evening call-out on 30 June; the spring hour of the local clock, the drained TCX-4 batteries' breaks beside their
MAINS_FAIL, the controller replacements' breaks, the event log's exact repeats, COMMS_LOST from communications faults
and single failed polls, the 30 September evening outage on UTC dates.

| Path | Ask A visits | Ask B failures | Keeps |
| --- | --- | --- | --- |
| labour days, one per station and day; MAINS_FAIL, repeats removed | 0 of 12 | 0 of 12 | 0 of 24 |
| labour lines, each a visit; MAINS_FAIL rows | 0 | 2 | 2 |
| each order at each of its stations; COMMS_LOST | 1 | 0 | 1 |
| door days at TCX-4 and labour days at TCX-2; every break plus MAINS_FAIL | 0 | 6 | 6 |
| the door rule with the register's controller all year; TCX-2 breaks plus MAINS_FAIL, one per break | 7 | 7 | 14 |
| the door rule on DOOR_OPEN only; TCX-2 breaks with the replacements kept | 10 | 5 | 15 |
| the door rule on UTC dates; the golden on UTC quarters | 11 | 10 | 21 |

| Ask | Cracker (the call landed, labour days and MAINS_FAIL) | Verdict |
| --- | --- | --- |
| A maintenance visits by district and quarter | 0 of 12 | miss |
| B power failures by district and quarter | 0 of 12 | miss |

Pair ceiling: 28.5 ((45.0 + 12.0) / 2), the cracker keeping none of the 24 ask figures on the call and the mirror the same.
Mirror leakage: 0 per cent of ask weight.
Measured by: generator/pair.py on the cut pack. A reader who finds the office resets keeps 12 of 24 and one who also
finds the TCX-2 breaks without the re-trips 19; the stage 4 readers are the measurement.

## Tried and rejected

- The seed's own pitfall (the errors-in-variables slope between two noisy instruments): spent by task249 v1, landed
  by its reader.
- One key, the loss per supplier (the draw as filed, prototype 4): a single insight readers enumerate once they see the
  changes' jumps, the coin-flip shape of the measured drivers (task249's five architectures each landed on one reflex);
  prototype 5 sets the loss by the cylinder's interior, which one supplier changed in 2026, so the per-supplier rate is
  a mixture and is a rung.
- The ask layer with the check hour named invalid in the manual (valid hours and hours above 350): the counts do not
  move when a dropped hour shifts by one, so a reader executing section 5 on the stamps as written kept the valid hours
  whatever the clock; measured pair 76.0. The check hour is now left to the 45-minute rule and the check's times, the
  old firmware stored ppb, and the mean joins the asks.
- Physical & Environmental Sciences, sensor calibration and measurement, shape 10, monitoring_export: BLOCKed by
  task250's shipment (pairing, subdomain, artifact) and task471 (shape); redrawn as above.
- Architecture 1 (the SO2 analyzers' gain against true SO2 read through span gas that loses SO2 with its age since
  certification at a rate the cylinder's interior sets, fitted on the 31 cylinder changes): spent 10-20 at stage 4.
  Both scored readers landed the four analyzers, each by fitting the change readings' jumps to an exponential loss from
  the certificate date and splitting on the certificates' passivation once the per-supplier fit left a 4.5 per cent
  residual; reader B also kept 32 of 33 ask figures, finding the firmware update's 2.62 level jump, the standard-time
  stamps and the unmarked check hour. The estimand's own words (gain against true SO2) sent both straight to the
  reference's truth, and the change readings measured it in one division: a chain a careful reader models, with a
  misfit that points to its second link. Judge pass 1 DETERMINISTIC, FIX_NOW (the visit edge, pinned before the
  readers came back).
- The ask devices as first drafted (stage 2): section 5 named the hours of verification and maintenance not valid and
  the spare's hours as the station's, so a literal executor of the rule found both devices; the rule now files only the
  45 minutes of station air, visits are shaped so every hour they touch holds 16 minutes of them or more, and the spare's
  hours sit under the store's code.
- A 25 degrees C logger setting on integer micrograms (stage 2): too weak to move a mean at one decimal, and rescaling
  the database against reading the archive's ppb split two 19th values at whole micrograms; now 0 degrees C, the
  database at one decimal and the archive at two, both routes agreeing at the asked rounding.
- Architecture 2 (the NOx converters' efficiency clocked in the NO2 they reduce, a pooled curve steepening past about
  90 ppm-hours carried on each station's seasonal load to the 2028 service): spent 10-20 at stage 4. Both scored
  readers landed the seven (BP01, BP02, BP03, BP04, BP05, BP08, BP13), each going straight to the converter's
  accumulated NO2 as the wear clock (reader A: "modelling converter decay from the exposure it accumulates"); the
  field's own wear model is inside a strong reader's hypothesis space, and the stations' different loads, which the
  stump needs, make it visible in the first plot. The ask layer held for both (4 of 48 each): the new contractor's
  titration hours coded valid were missed by both, MAG and the 0 degrees C loggers found by both. Judge pass 1: the
  isolated thread's Bash calls were refused by the auto-mode classifier and no verdict was issued.
- Architecture 2's judge pass 1b (the same pack, the isolated thread re-run once from the scratchpad): DETERMINISTIC
  APPROVE; the architecture stays spent on Gate F.
- Architecture 3's first world (each meter's random error proportional only, pairings twice a week): the confirmations
  moved a neonatal meter's pooled mean by about 1.5 points against a 0.8-point standard error, so no seed held a clear
  golden and a pooled list two meters off; the meters' constant error at low glucose (5 mg/dL beside the proportional
  5 per cent) and three plan days a week on the neonatal wards give the confirmations about 4 points there.
- The route that keeps every pairing whose meter value is not critical landed the golden list while the nursery's median
  sat at 70 mg/dL; at 60 the plan's own low pairings leave with the confirmations and the route files a ninth meter.
- Regression with an intercept (Passing-Bablok, least squares) in the golden family: the slope spread several points on
  the narrow-range wards and broke the margin; section 7 defines a single factor, which the intercept forms do not
  estimate, and files the mean of ratios because the printed error still spread half a point among the single-factor
  estimators.
- The analyzer parallel run as a pack file (calibration parallel_run_overlap): BLOCKed by ban.calibration against task481
  at registration; the run's relation is a lower rung, so the laboratory's note files the factor and no corpus ships.
- Architecture 3 (52 bedside glucose meters, each meter's systematic error read on the plan's pairings, the critical-value
  confirmations being selected on the meter's own reading): spent 2026-10-20 at stage 4 on target.zip dfd2d32a. Scored
  reader A landed the call by keeping only the planned morning-round pairings (it quoted section 5's "almeno nei giorni
  del piano" and read every confirmation's meter value beyond 50 or 400 as selection on the meter result); reader B filed
  the default path (every pairing since the calibration: GX2-M707F in, GX2-K532W out). Both kept 25 of 25 ask figures:
  the re-sent copies (a duplicate check on matricola and n_memoria), the solar clocks (the planned pairings' summer gap)
  and the register's location history are battery work, the measured-as-executed list. Judge DETERMINISTIC APPROVE, Gate H
  analytical. Selection on the measured value is a textbook reflex once the data shows it in one column; a fourth
  architecture is the author's call.
- Each listed station's error in whole per cent as a graded figure (the draft prompt): the licensed estimates spread a
  station's error by up to 0.6 points (the queued spells' first and last hours carry the bridge's lag, and leaving them
  out moves the loss at 30 per cent occupancy from 5 to 9 per cent), so two listed stations printed -6 or -7 by
  method; the list and a margin every estimate keeps (beyond 6, within 4.5) are graded instead.
- Ask A with the door log alone as the visits' evidence (stage 2 draft): a reader taking door days at the TCX-4s and
  labour at the TCX-2s kept 9 of 12; the validation crew's nights, the Region's own cabinet checks and the renumbered
  stations' TCX-2 months now sit on that route.
- Ask B with one loss per outage (stage 2 draft): a reader on the TCX-2 breaks kept 9 of 12; feeder re-trips (two
  losses inside one break at a TCX-2, two MAINS_FAIL at a TCX-4) now hold that route to 7.
- Architecture 4 (30 loop count stations, each station's 2027 error with the loss its loops take in queued traffic,
  fitted on the river bridges' paired approaches): spent 2026-10-21 at stage 4 on target.zip 555ce293. Scored reader A
  landed the five by the bridge pairs (it saw that no filmed hour passes 9 per cent occupancy while term-time peaks run
  to 49, paired the stations on either side of each bridge with no junction between, and fitted counted over true
  against occupancy); reader B filed the validation list. Both kept 0 of 24 ask figures (labour station-days with the
  office resets in; MAINS_FAIL alone, the TCX-2 breaks missed). Judge NOT_DETERMINISTIC on ask 2, FIX_NOW: the TCX-2
  reset days carry the office resets' text and nothing filed says a TCX-2 is reset on site; Gate H analytical. A
  validation that visibly misses a condition invites a reader to look for an independent reference, and the network's
  own pairs were one.
- 2026-10-21, architecture 5 draw: the four candidates written for it (analyzers' imprecision under a repeat-until-accepted practice, polled analyzers aliasing a blower cycle, a service desk's resolution time by Little's law, a network intercompared against its own median) were set aside: each carried one decisive move on a second rung, the shape one reader of architecture 4 and both of task249's architecture 5 landed, while a conjunction in architecture 4's own world (the queue loss and a cold miss confined to one controller generation, either alone filing another list) could be probed with readers before any build.

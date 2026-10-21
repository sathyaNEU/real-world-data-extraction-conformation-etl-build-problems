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
At stage 3 the window moved: task482, filed in another session nine seconds before this card, holds composition_mix and
leads with G5, so `heart` BLOCKed on ban.strategy and ban.pattern. Both axes were redrawn on the card in place:
population_selection, because the validation is a selected sample of hours (summer free flow only) outside which both
error terms arise while the estimand runs over every hour, which names the stump more exactly than a mix shift; and G6
(composition shift) to lead, the filmed days' composition of traffic states and weather against the year's, with G7 kept
second (G7 leading repeats task271's architecture 2 on gap, pattern and Gate G inside the batch). The older
same-puzzle and same-driver collisions this opened (task465 and task253 lineage, task455 lineage, task68, task230
lineage) carry differentiation lines on the card. heart then WARNs only: repeat.gate_g against task478 and
overuse.gate_g (answered above), repeat.question_form against task478 and task482 (which: a pick of stations).

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
- **Strategy.** `population_selection`: the validation is a selected sample of each station's hours (one summer
  weekday, free flow, no frost) while the estimand runs over every hour it counted, and the two error terms live only
  outside the sample; the queued state's loss and the cold days' miss have to be measured elsewhere and carried through
  each station's own mix of hours by the controller in force. Gate G method_or_model_selection; generators G6, G7, G5,
  G17; gap population;
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
Layer 2: field_method under population_selection: the error depends on the traffic state and the weather, the validation day sampled only summer free flow, and the queued state's loss is measured on the conservation pairs and the cold miss on the pairs whose two approaches run different controller generations, both carried through each station's own hours by the controller in force.
Decisive step: estimating each station's 2027 error with both a loss term that grows with occupancy, fitted on the bridges' paired approaches, and a cold-day miss on the TCX-2 cards, fitted on the mixed-generation pairs' free-flowing days against the airport's daily mean temperature and placed on the TCX-2 because their occupancy per counted vehicle climbs in the cold while the TCX-4s' holds flat, carried through every hour by the controller in force, rather than the summer validation day's error or either correction alone.
Not semantics: every field reads as what it is (vehicles counted in the hour, occupancy, the video count of the vehicles that passed, the day's temperatures), and nothing in any field, code, unit or definition says that loops lose vehicles in queues, that either controller generation misses vehicles in the cold, or that the validation days held neither; the bridges are structures in the network file, the controllers a column of the register and the temperatures the airport's daily summary.
Not rule application: no filed sentence says how a station's year error is estimated; TDP-03 defines the error over the hours counted and states the validation programme's facts, so executing every filed rule on the validation counts files the validation list, and no rule names the temperature, the controller generation or the bridges.
Analyst test: A strong analyst who reads the standard, the register, the validation counts and the hourly counts takes each station's 2027 error from its validation day and flags R14-01 and R25-01; one who reads the queue loss from the bridges' pairs flags R02-01, R04-03, R08-05, R14-01 and R25-01, and one who reads only the cold miss R04-03, R06-01, R14-01 and R25-01; only both file the seven (checks.py runs every route on the clean world and on the pack).
Estimand: each of the 30 stations' 2027 count error, the vehicles it counted in the hours of 2027 it counted (both directions, every lane) against the vehicles that passed it in those hours, less one; a station is flagged when its error is beyond 5 per cent either way (TDP-03 section 5 and the prompt).
No decoy: nothing is planted: the validation counts are true counts of the vehicles on their days, the loops' counts are what the loops counted, the temperatures are the airport's own daily summary, no memo, draft or figure argues for any list, and no file ranks the stations by error.
No certified replay: no certified or published figure sits in the pack; the validation workbook states counts and no accuracy verdict, and no file states a station's error, flag or annual traffic.
Lesson: a validation that never samples the conditions in which an instrument errs cannot give its error over a year that holds them, and when two conditions act on different instruments each needs its own natural experiment: a stream counted twice with nothing joining or leaving measures the queue loss, the same stream counted by two instrument generations measures one generation's weather miss, and a second channel the miss does not touch says which generation it is; no shipped build reads a counting error from conservation between counters of two generations.

## Readability screen

| Rung | Where a reader meets it | Verdict |
|---|---|---|
| 1. Each station's validation-day error (R14-01, R25-01) | the validation workbook, TDP-03 sections 4 and 5 | readable |
| 2. The queue loss alone, fitted on the bridges' paired approaches (R02-01, R04-03, R08-05, R14-01, R25-01) | nothing names it: the bridges are structures in the network file, and only the filmed days' low occupancy against the year's peaks sends a reader to look for a second reference | silent |
| 3. The cold miss alone, placed on the TCX-2 by occupancy per counted vehicle or read on the mixed pairs (R04-03, R06-01, R14-01, R25-01) | nothing names it: the controllers are a column of the register, the temperatures the airport's daily data, and no file says either generation misses vehicles in the cold | silent |
| 4. (decisive) Both: the cold miss on the TCX-2s from the mixed pairs against the day's mean temperature, the loss fitted with it taken out, both carried through every hour by the controller in force (the seven) | nothing names either condition or their combination; each correction alone looks finished and files a list of its own, and the cold effect read on the pairs alone points at either generation | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the stations | the 30 in the register, a renumbered station once under its current number | each number in the export a station | another list (R08-01 and R08-05 both) | the register's Code history; TDP-03 section 3 (the record continues under the new number) |
| SF2 | 2027 | the local calendar year of the export | the UTC year | same call | asserted |
| SF3 | the vehicles that passed | each hour's count over its sensitivity, one less the loss at its occupancy and, on a TCX-2, one less the cold miss at the day's temperature | five loss forms; a constant loss above 22, 25 or 28 per cent; the queued spells' edges out; two-hour blocks; vehicle weights; the pairs on their own free-flow ratio; each direction alone; the one-generation or the mixed bridges alone; the cold pairs' free flow below 12 or 25 per cent; the loss fitted before the cold miss is taken out | same list | asserted over every licensed estimate (50 in the family): listed beyond 6.5 per cent, others within 4.5 |
| SF4 | the error | counted over passed, less one | passed over counted, less one | same list | TDP-03 section 5; asserted |
| SF5 | beyond 5 per cent | strictly | at or beyond | same call | no station within 1.5 points of the line (asserted at 1.0) |
| SF6 | the hours | the hours each station counted | every hour, the lost ones estimated | same call | TDP-03 section 5; asserted on the world's full record |
| SF7 | the sensitivity | per station and direction | per station | same list | asserted |
| SF8 | occupancy | per cent at the precision each controller reports | every hour at one decimal | same list | the dictionary; asserted |
| SF9 | a renumbered station's hours | joined under the current number | the old number's hours dropped | same list | the register's Code history; asserted |
| SF10 | the validation sites | the register's validation_site | none | same call | asserted, one station per site |
| SF11 | the bridge pairs | each bridge's nearest stations either side, no junction between | none | same call | the network file; asserted |
| SF12 | the validation day | the filmed day, midnight to midnight, both directions | none | same call | TDP-03 section 4; asserted (96 quarter hours each direction) |
| SF13 | an error's rounding | no station's error is graded | a printed error | not graded | the prompt asks for the list; asserted |
| SF14 | a maintenance visit (asks) | a day a maintenance contractor's technician is at a station | each labour line, each order, each door day, every reset order dropped | the asks only | TDP-03 section 7 (two technicians are one visit); a TCX-2 has no remote reset and its communications faults name the cabinet work done (asserted); the office resets read as a RESET with the cabinet shut give the same counts (asserted) |
| SF15 | a power failure (asks) | each loss of mains power at a controller, a feeder's re-trip a second loss | each outage once, each break once | the asks only | section 7 (a loss counted once however long it lasts); the TCX-4s log two MAINS_FAIL for a re-trip and TrafficVault's polls two losses at a TCX-2 (asserted) |
| SF16 | a quarter (asks) | calendar quarter by local date | by UTC date | the asks only | TDP-03 sections 3 and 7 |
| SF17 | a district (asks) | the register's district | none | same figures | one district per station (asserted) |
| SF18 | the validation crew (asks) | not a maintenance visit | a visit | the asks only | TDP-03 sections 4 and 7 (the maintenance contractor's technicians) |
| SF19 | a controller replacement (asks) | a visit, not a power failure | a power failure | the asks only | section 7 (a loss of mains power); the work order and the Code history |
| SF20 | the year-2000 stamps (asks) | a cold start's unset clock | events of 2000 | same figures | no MAINS_FAIL carries one (asserted) |
| SF21 | the log's repeats (asks) | one event | two | the asks only | exact repeats after a lost poll (asserted) |
| SF22 | a visit's or failure's day (asks) | local date | UTC date | the asks only | TDP-03 section 3; asserted (aimed) |
| SF23 | the generation that misses vehicles in the cold | the TCX-2 | the TCX-4 counting more | another list (R10-03, R23-01 and R25-01; with the queue loss R04-03, R14-01 and R25-01) | the data: occupancy, the time the loops are covered (the dictionary), climbs per counted vehicle on the TCX-2s by 10 per cent from July to January while the TCX-4s' holds within 1 per cent, so the TCX-2 counts fewer, not the TCX-4 more (asserted) |
| SF24 | the day's temperature | the airport's daily mean | the maximum, the minimum, a curve or bins, the occupancy channel day by day | same list | asserted (every reading in the family) |
| SF25 | a day with no temperature | the mean of the days either side | no miss that day; the day's hours dropped | same list | the weather file's M flag; asserted |
| SF26 | the controller in force | the register's controller, a TCX-2 before a replacement date | the register's current controller all year | same list | the register's Code history ("controller replaced, TCX-2 to TCX-4"); asserted |

## Ladder

| Route | Withdraws | Count | Golden |
|---|---|---|---|
| Each station's validation-day error (the default path) | R14-01, R25-01 | 2 | no |
| Each direction's validated sensitivity carried through the year, nothing else | the same two | 2 | no |
| The cold effect read as a TCX-4 overcount, no loss (probe A) | R10-03, R23-01, R25-01 | 3 | no |
| The queue loss with the cold effect read as a TCX-4 overcount (probe B) | R04-03, R14-01, R25-01 | 3 | no |
| The cold miss on the TCX-2s alone (probe C) | R04-03, R06-01, R14-01, R25-01 | 4 | no |
| The queue loss alone (architecture 4's golden construction) | R02-01, R04-03, R08-05, R14-01, R25-01 | 5 | no |
| Golden: both, the cold miss placed by the occupancy channel, carried through every hour by the controller in force | R02-01, R04-03, R06-01, R08-05, R14-01, R25-01, R29-03 | 7 | yes |

R29-03 enters only with both corrections (the queue loss alone puts it at 4.9 per cent, the cold miss alone at 4.7);
R06-01 needs the cold miss and R02-01 and R08-05 the loss. The golden family agrees on the seven under five loss forms
times nine readings of the cold miss and every pair variant (asserted, listed beyond 6.5, others within 4.5). On the
clean world the validation day, the loss alone and the cold miss alone each file a wrong list and both the truth
(checks.py, dataset-generation 7.1).

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | the 30 stations in the register | filed (register) |
| 2 | Unit of account | a station, both directions and every lane together | filed (TDP-03 section 5) |
| 3 | Attribution window | the hours of 2027 the station counted | filed (section 5) |
| 4 | As-of dating | the record to 31 December 2027, the list due 3 March 2028 | filed (export, mail) |
| 5 | Version basis | TDP-03 revision 4 | filed |
| 6 | Denominator | the vehicles that passed in the hours counted | filed (section 5) |
| 7 | Weighting | each vehicle once (a ratio of totals) | filed (section 5) |
| 8 | Window length | the calendar year | filed |
| 9 | Boundary inclusivity | beyond 5 per cent | C1 (1.5 points clear, asserted) |
| 10 | Rounding path | no error graded; visits and failures whole counts | C1 |
| 11 | Tie-break | none open | asserted |
| 12 | Maturity and censoring | every hour of 2027 delivered by 7 January 2028; the airport's daily data complete but one day, flagged M | filed (dictionary, export, the weather file's flag) |
| 13 | Order of operations | sensitivity, the cold miss, the loss, then the year's ratio | C1 (the loss fitted first files the same list, asserted) |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | the autumn hour twice by offset; the event log's exact repeats once | filed (offsets); asserted |
| 16 | Identity normalisation | current station numbers, site codes through the register | filed (register) |
| 17 | Netting against gross | none | not applicable |
| 18 | Dimensional units | vehicles, per cent occupancy, degrees Celsius | filed (dictionary, the weather file's headers) |
| 19 | Code and status semantics | event codes, work order categories, the weather service's flags | filed (dictionary, the weather file); never the stump |
| 20 | Integerisation | whole counts on the asks | filed (the asks count) |
| 21 | Clause scope | section 5 for every station; section 7 for every district and quarter | filed |
| 22 | Forward window contents | the spring 2028 round recalibrates the flagged stations | filed (section 5, the mail) |

## Literal reader

Executing the prompt and every filed sentence word for word (TDP-03 sections 2 to 7, the dictionary, the register, the
network file) leaves one open move, how the vehicles that passed each station are estimated; the data's structure
forces it: the filmed days hold no hour above 8.2 per cent occupancy and no day's mean below 13 degrees, while the
year's queued hours run to 49 per cent and its days to minus 17; only the bridges' paired approaches count one stream
twice, three of them with one controller of each generation; and occupancy per counted vehicle says which generation
errs. Every licensed estimate of that one quantity files the same seven (asserted, 50 in the family, listed beyond 6.5
per cent, others within 4.5).

## Oracles

- No file ranks the stations or carries a station's error, flag, list or annual traffic.
- The validation workbook carries counts only; every route reads it and none is told its days are unrepresentative.
- The weather file is the airport's own daily data, in the weather service's layout; it names no station, no
  controller and no count.
- The contractor's mail asks for the list and a note if there are none; it carries no station.
- The collision and pavement condition files (the distractors) carry no figure any route needs.

## Ask sheet

Ask A: for each district and quarter of 2027, the maintenance visits to the count stations (12 figures). Ask B: for
each district and quarter, the power failures the stations had (12 figures). Both read the maintenance contractor's
work orders and TrafficVault's event log, which the call never reads, and ask B the breaks in the hourly record, which
the call's estimand leaves out (the hours counted); the call on the full world record files the same list, every error
within 0.3 points (separation asserted).

Devices, silent (no filed sentence points at any of them):
- Ask A: at TCX-4 stations the contractor clears some communications faults by resetting the controller from its
  office and books the half hour against the work order like any visit, with the same description and resolution as
  the resets done at the cabinet's keypad; two or more office resets and at least one keypad reset in every district
  and quarter, so neither counting every reset order nor dropping every one holds. Only the cabinet door log's silence
  that day shows the technician was not there. A TCX-2 has no remote reset, so its communications faults are cleared
  at the cabinet and the order says what was done there. Moves every figure of ask A.
- Ask B: a TCX-2 has no battery and reports nothing, so its power failures exist only as breaks in its hourly record,
  at least one in every district and quarter. A recloser's momentary interruption (under five minutes) drops the hour
  a TCX-2 is in while TrafficVault's 15-minute poll usually misses it, so a break with no failed poll is still a
  failure (one in every cell, some others caught by a poll, so the poll log marks nothing); and where a feeder recloses
  and trips again within the hour the TCX-2 discards both partial hours and its record shows one break, while
  TrafficVault's polls inside it failed, succeeded and failed again (re-trips at TCX-2 stations in eight cells).
  Counting the failed-poll episodes inside the breaks, the path both architecture 5 stage 4 readers took, misses the
  first; counting each break once misses the second.
Hazards: route orders covering four stations on one labour line, two-technician lines, multi-day orders, the
validation crew's and the Region's own cabinet openings (the door log read as a roster), the replacement controllers'
DOOR_OPEN under the unset clock, the register's current controller for the two renumbered stations' TCX-2 months, an
evening call-out on 30 June; the spring hour of the local clock, the drained TCX-4 batteries' breaks beside their
MAINS_FAIL, the controller replacements' breaks, the event log's exact repeats, COMMS_LOST from communications faults
and single failed polls, the 30 September evening outage on UTC dates.

| Path | Ask A visits | Ask B failures | Keeps |
| --- | --- | --- | --- |
| labour days, one per station and day; the failed-poll episodes inside the TCX-2 breaks plus MAINS_FAIL (both architecture 5 stage 4 readers, round 1) | 0 of 12 | 0 of 12 | 0 of 24 |
| labour days; MAINS_FAIL, repeats removed | 0 | 0 | 0 |
| labour lines, each a visit; MAINS_FAIL rows | 0 | 0 | 0 |
| each order at each of its stations; COMMS_LOST | 1 | 0 | 1 |
| labour days less every reset order's labour; every break plus MAINS_FAIL | 0 | 4 | 4 |
| door days at TCX-4 and labour days at TCX-2; TCX-2 breaks plus MAINS_FAIL, one per break | 0 | 4 | 4 |
| the door rule with the register's controller all year; TCX-2 breaks with the replacements kept | 7 | 5 | 12 |
| the door rule on DOOR_OPEN only; breaks on the local clock at TCX-2 | 10 | 2 | 12 |
| the door rule on UTC dates; the golden on UTC quarters | 11 | 10 | 21 |

| Ask | Cracker (the call landed, the stage 4 readers' ask paths) | Verdict |
| --- | --- | --- |
| A maintenance visits by district and quarter | 0 of 12 | miss |
| B power failures by district and quarter | 0 of 12 | miss |

Pair ceiling: 28.5 ((45.0 + 12.0) / 2), the cracker keeping none of the 24 ask figures on the call and the mirror the same.
Mirror leakage: 0 per cent of ask weight.
Measured by: generator/pair.py on the cut pack. Round 1 of stage 4 (target.zip 41198eaa): both readers kept 12 of 24
(all of ask B, by the failed-poll episodes inside the TCX-2 breaks), so ask B's device was re-sited onto that path
(momentary interruptions no poll caught) and the cracker now carries the readers' measured path; round 2 readers on
the re-cut pack are the measurement.

## Pre-ship check

- Free gates (stage 3, re-run on the final pack): generator checks 78 passed (the golden list against the world's truth over the hours counted,
  50 licensed estimates filing the seven with listed beyond 6.5 and others within 4.5, the loss on each direction and
  each bridge subset, the cold pairs' thresholds and the fit order, SF1 to SF26 with the occupancy channel placing the
  cold miss on the TCX-2 (January over July 1.098 against 0.993), the TCX-4-overcount routes filing the probes' lists,
  the missing temperature day and the current-controller reading, the four rungs on the pack and on the clean world, R1
  to R3, the separation line, the asks against the truth with both devices in every cell, the input gates); verify.py
  0 failures (the cold miss in temperature bins and the loss in occupancy classes); two builds byte-identical
  (target.zip 41198eaa at stage 3; the final pack, after ask B's re-cut at stage 4 and the standard's revision table
  wrapped, is 6283c112); figures_check 14 of 14; precut 51 of 51; voice-check PASS.
- leak.py REVIEW, no LEAK: TDP-03 carries the call's words (its own estimand and the spring round), and TDP-03 and the
  dictionary carry the field's terms (validation, occupancy, controller); neither names a queue, a temperature or a
  generation's error, and the bridges and the weather sit in files that state no relation to counting.
- guard heart WARN after the in-place relabel (population_selection, G6 leading); surface promotes task243 (surface
  wording, no shared mechanism) and task68 (gap, pattern and Gate G), both differentiated on the card; people Miranda
  Harris and Yvonne Larson only, as drawn.
- Containers scrubbed (the organisation's producer and the fiction's dates) in target/ and golden/.
- Golden realism: the workbook leads with the finding as its title, lists the seven with road, location, district,
  controller (R08-05's swap date beside its TCX-4) and validation site, carries the maintenance sheet by district and
  quarter with totals, and a notes sheet stating the estimand, both error terms and where each is measured; the chart
  shows every station's error against the band by district with the controller in each label, the seven marked, and
  the two swaps noted under the source line.
- The 10/10 rules re-read against the built pack: the decisive step is the two error terms estimated from the network's
  own pairs and carried through each station's hours, which no filed sentence performs; every Layer 1 item mishandled
  leaves the call unchanged (asserted: the clock offset, the renumbered hours, the occupancy precision, the missing
  temperature day, the current controller all year).
- Open risk, stated: a reader who fits the queue loss on the bridge pairs and also places the cold miss on the TCX-2 by
  occupancy per counted vehicle lands the call; the three probes each made one of the two moves or misplaced the cold
  effect. The stage 4 readers are the measurement.

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

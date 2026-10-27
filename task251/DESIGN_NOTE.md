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
| SF8 | occupancy | per cent at the precision each controller reports | every hour at one decimal | same list | TDP-03 section 3; asserted |
| SF9 | a renumbered station's hours | joined under the current number | the old number's hours dropped | same list | the register's Code history; asserted |
| SF10 | the validation sites | the register's validation_site | none | same call | asserted, one station per site |
| SF11 | the bridge pairs | each bridge's nearest stations either side, no junction between | none | same call | the network file; asserted |
| SF12 | the validation day | the filmed day, midnight to midnight, both directions | none | same call | TDP-03 section 4; asserted (96 quarter hours each direction) |
| SF13 | an error's rounding | no station's error is graded | a printed error | not graded | the prompt asks for the list; asserted |
| SF14 | a maintenance visit (asks) | a local day a maintenance contractor's technician attended the station, so an attendance the cabinet door log shows running past midnight is a day either side of it | each labour line; each order at each of its stations; each door day; the labour day alone for an attendance that ran past midnight; every reset order dropped | the asks only | TDP-03 section 7 (two technicians on one day are one visit, and work the contractor carries out from its own premises is not a visit); the TCX-4 logs the cabinet door switch on every opening and closing (section 7), so the office days read off the labour with the cabinet shut and read off a RESET the door log does not answer are the same days (asserted); a TCX-2 has no remote reset and its communications faults name the cabinet work done (asserted) |
| SF15 | a power failure (asks) | each loss of mains power at a controller: the MAINS_FAIL a controller that survived the loss reported, and a break in the station's hourly record where it did not, with one more for each time the station answered a poll inside the break and failed again | each MAINS_FAIL only; each break once; the breaks at the TCX-2 stations only; a restore inside a break with no further loss counted as a second failure | the asks only | section 7 (a loss counted once however long it lasts, and a supply restored and lost again a second failure, so a restore with nothing after it is not one); section 3 (a TCX-2 has no standby supply and reports no event of its own; a part hour is discarded); the losses in a break read as the polls that failed inside it give the same figures (asserted); a TCX-4 that stopped reports no MAINS_FAIL for the loss that stopped it and its cold start carries the unset clock (asserted) |
| SF16 | a quarter (asks) | calendar quarter by local date | by UTC date | the asks only | TDP-03 sections 3 and 7 |
| SF17 | a district (asks) | the register's district | none | same figures | one district per station (asserted) |
| SF18 | the validation crew (asks) | not a maintenance visit | a visit | the asks only | TDP-03 sections 4 and 7 (the maintenance contractor's technicians) |
| SF19 | a controller replacement (asks) | a visit, not a power failure | a power failure | the asks only | section 7 (a loss of mains power); the work order and the Code history |
| SF20 | the year-2000 stamps (asks) | a cold start's unset clock | events of 2000 | same figures | no MAINS_FAIL carries one (asserted) |
| SF21 | the log's repeats (asks) | one event | two | the asks only | exact repeats after a lost poll (asserted) |
| SF22 | a visit's or failure's day (asks) | local date | UTC date | the asks only | TDP-03 section 3; asserted (aimed) |
| SF23 | the generation that misses vehicles in the cold | the TCX-2 | the TCX-4 counting more | another list (R10-03, R23-01 and R25-01; with the queue loss R04-03, R14-01 and R25-01) | the data: occupancy, the share of the hour the loops were occupied (TDP-03 sections 2 and 3), climbs per counted vehicle on the TCX-2s by 10 per cent from July to January while the TCX-4s' holds within 1 per cent, so the TCX-2 counts fewer, not the TCX-4 more (asserted) |
| SF24 | the day's temperature | the airport's daily mean | the maximum, the minimum, a curve or bins, the occupancy channel day by day | same list | asserted (every reading in the family) |
| SF25 | a day with no temperature | the mean of the days either side | no miss that day; the day's hours dropped | same list | the weather file's M flag; asserted |
| SF26 | the controller in force | the register's controller, a TCX-2 before a replacement date | the register's current controller all year | same list | the register's Code history ("controller replaced, TCX-2 to TCX-4"); asserted |
| SF27 | the filmed day's sensitivity against the rest of its year | the filmed day's loops over video is the station's sensitivity for every hour of the controller's time in service | the counting changed inside the year, so the filmed ratio holds for part of it only | another list at 10 per cent or more (R08-05 out) | no work order of the year replaces anything on the counting path, the spring and autumn inspections test the loops at every station, and the stations that ran one controller all year read 1.0000 to 1.0084 (sd 0.0028) on their own occupancy per counted vehicle at matched free-flowing flow between July and the winter, so nothing in the counting moved by more than 0.85 per cent (asserted) |
| SF28 | the two curves carried to a station that is not on a bridge | one function of occupancy and one of temperature, the loops cut to one detail at every station (TDP-03 section 2) | a loss or a miss of its own at each station | another list once a station's loss is 1.4 times the pooled curve or 0.4 of it | the loss fitted at each of the five bridges on its own gives 0.1775 to 0.1864 at 40 per cent occupancy (sd 2.0 per cent of the mean) and the list is invariant over a per-station scale of 0.5 to 1.35, twelve times that spread; the cold miss read at every station from its own occupancy channel, with no bridge pair, no register and no temperature, files the golden list, and the list is invariant over a cold scale of 0.7 to 1.3 (asserted) |
| SF29 | a drift the two controller generations share | none: the winter moves the TCX-2 cards' counting only | a count drift at every station in the cold, which a bridge pair cannot see because it cancels in the ratio | another list at 0.006 per degree (R18-01 in) or at minus 0.012 (four out) | a shared drift moves occupancy per counted vehicle one for one, and the thirteen stations that ran a TCX-4 all year hold within 0.84 per cent over December to February, so the record allows at most 0.00095 per degree against the 0.006 the list needs, 6.3 times as much (asserted) |
| SF30 | the regime no filmed day covers at the two renumbered stations | each station's own hours carry its own counting, which its occupancy channel measures | the unfilmed regime counted differently, the filmed ratio assumed for it | another list at 1.10 of the unfilmed regime's sensitivity (R08-05 out) | R08-05 before its replacement reads 1.0686 against the all-year TCX-2 stations' 1.0617 (sd 0.0039) and R19-03 after its replacement 1.0026 against the all-year TCX-4 stations' 1.0059 (sd 0.0033), so each matches its own generation to 0.6 per cent, while the list is invariant from 0.90 to 1.05 and needs 1.10 to move (asserted) |

**SF28, third pass.** The shipped claim is deliberately narrower than the asserted band. On the generator's own fitted loss curve the golden list holds at a per-station loss scale of 1.20 (largest unlisted error R18-01 at 4.29 per cent against the 5 per cent line) and still at 1.35 (R18-01 at 4.95 per cent), and breaks only at 1.40 (R18-01 at 5.18 per cent). A loss curve fitted independently from the shipped bridges crosses earlier: the third-pass judge read R18-01 at 5.2 per cent at a scale of 1.3333, the "a third again" step 5 of the write-up first claimed. Step 5 therefore claims invariance over "any scale from a half to a fifth again" (0.5 to 1.20, 0.71 points of headroom, and the judge confirmed plus 25 per cent in its own fit), while checks.py SF28 keeps measuring 0.5 to 1.35 holding and 1.40 breaking, which is the design's robustness rather than a shipped claim.

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
| 12 | Maturity and censoring | every hour of 2027 delivered by 7 January 2028; the airport's daily data complete but one day, flagged M | filed (TDP-03 section 3, the export, the weather file's flag) |
| 13 | Order of operations | sensitivity, the cold miss, the loss, then the year's ratio | C1 (the loss fitted first files the same list, asserted) |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | the autumn hour twice by offset; the event log's exact repeats once | filed (offsets); asserted |
| 16 | Identity normalisation | current station numbers, site codes through the register | filed (register) |
| 17 | Netting against gross | none | not applicable |
| 18 | Dimensional units | vehicles, per cent occupancy, degrees Celsius | filed (TDP-03 sections 2 and 3, the weather file's headers) |
| 19 | Code and status semantics | event codes, work order categories, the weather service's flags | filed (TDP-03 section 7, the weather file); never the stump |
| 20 | Integerisation | whole counts on the asks | filed (the asks count) |
| 21 | Clause scope | section 5 for every station; section 7 for every district and quarter | filed |
| 22 | Forward window contents | the spring 2028 round recalibrates the flagged stations | filed (section 5, the mail) |

## Literal reader

Executing the prompt and every filed sentence word for word (TDP-03 sections 2 to 7, the register, the
network file) leaves one open move, how the vehicles that passed each station are estimated; the data's structure
forces it: the filmed days hold no hour above 8.2 per cent occupancy and no day's mean below 13 degrees, while the
year's queued hours run to 49 per cent and its days to minus 17; only the bridges' paired approaches count one stream
twice, three of them with one controller of each generation; and occupancy per counted vehicle says which generation
errs. Every licensed estimate of that one quantity files the same seven (asserted, 50 in the family, listed beyond 6.5
per cent, others within 4.5).

Leaving the correction out altogether is not a reading of the estimand but a wrong estimate of it, and the record
refuses it in one subtraction: with each approach on its own filmed sensitivity, a bridge's upstream station counts
20.07 per cent fewer vehicles than its downstream station in the hours above 30 per cent occupancy (se 0.075, t 267)
against 0.69 per cent in free flow, with a one-lane deck between them and nothing joining or leaving.

The four free parameters a literal reader is left with are each measured rather than assumed, and each corridor the
list survives is several times the range the record allows (SF27 to SF30, asserted in `checks.py` and recomputed in
`verify.py` from the shipped files alone). The instrument under all four is the occupancy a station reports per
vehicle it counts: a vehicle covers the loop whether the controller counts it or not, so read between two sets of
months at the same counted flow, that ratio moves one for one with a change in the station's counting and not at all
with the traffic.

| Free parameter | What the record allows | What the list needs to move | Margin |
|---|---|---|---|
| a change in a station's counting inside the year | 0.85 per cent (the all-year TCX-4 stations, max 1.0084, sd 0.0028) | a regime of its own at 10 per cent | 11 times |
| the loss carried to a station that is on no bridge | 2.0 per cent between the five bridges' own fits | a per-station scale of 1.40 or 0.40 | 20 times |
| a drift the two generations share | 0.00095 per degree below 2 degrees | 0.006 per degree | 6.3 times |
| the regime no filmed day covers at R08-05 and R19-03 | 0.6 per cent (each matches its own generation's cohort) | 1.10 | 17 times |

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
within 0.3 points (separation asserted). Both definitions sit in TDP-03 section 7 and are executed, not inferred: an
ask may turn on rule application (supplemental-stumping 2.1), and what each pin leaves is a reconstruction with one
right answer and a silent primary underneath it.

Devices, silent (no filed sentence points at any of them, and each is found only by an inconsistency between two
grains of the record):
- Ask A, the primary: the contractor's after-hours call-out reaches the cabinet before midnight and leaves after it,
  so one labour line, booked to the day the technician was called out, covers two local days at the station. Only the
  cabinet door log, whose DOOR_CLOSE falls on the next local date, carries the second day; one such attendance in
  every district and quarter, and the labour sheet alone, the door-open dates alone and the door rule all miss it.
  Moves every figure of ask A.
- Ask A, the second: at TCX-4 stations the contractor clears some communications faults by resetting the controller
  over the link and books the half hour against the work order like any visit, with the same description and
  resolution as the resets done at the cabinet's keypad; two or three in every district and quarter, so the two
  devices never cancel in a cell (measured: the labour days alone are one or two too high in all twelve). Section 7
  excludes work done from the contractor's own premises, and the cabinet door log's silence that day is the only
  record of where the technician was. A TCX-2 has no remote reset, so its communications faults are cleared at the
  cabinet and the order says what was done there.
- Ask B, the primary: an interruption that outlasts a TCX-4's battery stops the controller, and what it had logged
  while its modem was down with it goes with the supply, so the loss that stopped it has no MAINS_FAIL at all. It is
  in the station's own record instead, as absent hours, with the cold start it raises on the way back under an unset
  clock. One in every district and quarter (measured: one to three), and the path both round 1 readers and the portal
  response took, MAINS_FAIL plus the breaks at the TCX-2 stations, misses every one of them. TDP-03 section 3 states
  the TCX-2's behaviour and the TCX-4's battery and says nothing about what happens when the battery runs out.
- Ask B, the second: a recloser's momentary interruption (under five minutes) drops the hour a TCX-2 is in while
  TrafficVault's 15-minute poll usually misses it, so a break with no failed poll is still a failure (one in every
  cell, some others caught by a poll, so the poll log marks nothing); and where a feeder recloses and trips again
  inside the hour the TCX-2 discards both part hours and its record shows one break, while TrafficVault's polls inside
  it failed, succeeded and failed again (a re-trip at a TCX-2 in every cell).

Hazards: route orders covering four stations on one labour line, two-technician lines, multi-day orders, the
validation crew's and the Region's own cabinet openings (the door log read as a roster), the replacement controllers'
DOOR_OPEN under the unset clock, the register's current controller for the two renumbered stations' TCX-2 months, an
evening call-out on 30 June; the spring hour of the local clock, the controller replacements' breaks, the event log's
exact repeats, COMMS_LOST from communications faults and single failed polls, the 30 September evening outage on UTC
dates.

| Path | Ask A visits | Ask B failures | Keeps |
| --- | --- | --- | --- |
| labour days, one per station and day | 0 of 12 | | 0 |
| labour lines, each a visit | 0 | | 0 |
| each order at each of its stations | 2 | | 2 |
| door days at TCX-4, labour days at TCX-2 | 0 | | 0 |
| the door rule with the register's controller all year | 0 | | 0 |
| the door rule on DOOR_OPEN only | 0 | | 0 |
| the door rule on UTC dates | 0 | | 0 |
| labour days less every controller reset order's labour | 0 | | 0 |
| labour days where the cabinet opened at a TCX-4, the office resets out and the night work's second day missed (round 1 readers and the portal response) | 0 | | 0 |
| the same with the second day taken on UTC dates | 0 | | 0 |
| MAINS_FAIL rows | | 0 of 12 | 0 |
| MAINS_FAIL, repeats removed (the determinism judge's model response, 56 failures) | | 0 | 0 |
| COMMS_LOST | | 0 | 0 |
| every break of any controller once, plus MAINS_FAIL | | 1 | 1 |
| the TCX-2 breaks plus MAINS_FAIL, one per break | | 0 | 0 |
| the TCX-2 breaks plus MAINS_FAIL, the replacements kept | | 0 | 0 |
| the breaks on the local clock at TCX-2, plus MAINS_FAIL | | 0 | 0 |
| the episodes inside the TCX-2 breaks plus MAINS_FAIL (round 1 readers and the portal response) | | 0 | 0 |
| the golden with the episodes at TCX-2 only | | 0 | 0 |
| the golden on UTC quarters | | 10 | 10 |

| Ask | Cracker (the call landed, the round 1 readers' and the portal response's ask paths, every filed rule executed) | Verdict |
| --- | --- | --- |
| A maintenance visits by district and quarter | 0 of 12 | miss |
| B power failures by district and quarter | 0 of 12 | miss |

Pair ceiling: 28.5 ((45.0 + 12.0) / 2), the cracker keeping none of the 24 ask figures on the call and the mirror the same.
Mirror leakage: 0 per cent of ask weight. The two rows agree by construction rather than by measurement: the asks
consume nothing the call's construction produces (the separation assertions), so the mirror's ask score is the
cracker's and only its recommendation weight differs.
Measured by: generator/pair.py on the cut pack (target.zip 5266e879, 21 complete pipelines). Round 1 of stage 4
(target.zip 41198eaa): both readers kept 12 of 24 (all of ask B, by the failed-poll episodes inside the TCX-2 breaks),
so ask B's device was re-sited onto that path; round 2 readers kept 0 of 24. The portal then returned the build with
one response at 95 per cent, which is the measurement that both devices as shipped were inside a strong reader's
path, so both asks were re-devised onto a second grain of the same records (the attendance that crosses midnight, the
loss the controller could not report) and each pinned in section 7, with every earlier path above measured at 0.

Worst credible route in the table: a response that reconstructs both asks correctly and takes the quarters on UTC
dates keeps 10 of 24, which is 67.9 for a landed call and a pair of 51.4, still under the build target of 60. Local
dates are filed (TDP-03 section 3, and the export is in local time with its offsets), so the cracker does not take
that reading; it is recorded because it is the only path in the table above 2 of 24.

## Pre-ship check

- Free gates, re-run on the repaired pack (target.zip 5266e879): generator checks 94 passed, 0 failed (the golden list
  against the world's truth over the hours counted, 50 licensed estimates filing the seven with listed beyond 6.5 and
  others within 4.5, the loss on each direction and each bridge subset, the cold pairs' thresholds and the fit order,
  SF1 to SF30, the four free parameters with the record's bound and the list's corridor side by side, the pairs'
  imbalance refusing no correction at all, the TCX-4-overcount routes filing the probes' lists, the four rungs on the
  pack and on the clean world, R1 to R3, the separation line, both asks against the truth with both devices in every
  cell, no file or sheet describing the data, the input gates); verify.py 0 failures, recomputing the list, the
  margin, the components, the matched-flow instrument, the per-station cold route, the three corridors and both asks
  from the shipped files alone; two builds byte-identical; figures_check 15 of 15; precut 52 of 52, 0 WARN;
  voice-check PASS.
- leak.py REVIEW, no LEAK: one line, TDP-03 carrying the field's own terms (validation, occupancy, controller,
  contractor, traffic) and its own estimand and spring round. It names no queue, no temperature and no generation's
  error. `traffic_data_dictionary.md` was dropped (sweep 1 reads a dictionary's file name as a leak,
  `dataset-generation` section 3) and what it carried sits in TDP-03 at authority.
- freeze.py, both modes recorded, because the author asked for a determinism repair and an ask-layer repair in one
  pass and neither mode's contract covers both (`build-pipeline`, freeze.py and status.py): `--mode rubric` with four
  keys allowed is the control and PASSES, so the Final Recommendation and Critical Components numbers, every
  main-call figures.json value, the stump sentence, the card's stump and driver, the ladder, the default path and the
  prompt's call sentence are all unchanged while 18 ask figures moved. `--mode determinism` fails on those 18 ask
  figures and on the Deliverable Answers block, which is the ask repair the author ordered and not a finding. The
  four `--allow` keys (`asks.visits.Ashby.1`, `asks.visits.Kessel.3`, `asks.failures.Marlow.2`,
  `asks.failures.Marlow.3`) are ask figures whose old values (2, 6, 7, 7) happened to equal a number the
  recommendation blocks also state (2 degrees, 6 per cent, 7 stations), so freeze.py classes them as main-call
  figures; no figure the recommendation rests on moved.
- guard validate 1 card, 0 invalid. guard heart BLOCK, from the corpus and not from this repair: task269's fifth
  architecture was registered 2026-10-26, five days after this build shipped, with the same gap (population),
  pattern and Gate G mechanism, and task255 (v1) the same three, so `test.same_puzzle_older` and
  `test.same_driver_older` now fire where the shipped build read WARN. No card axis moved in this repair. The fix is
  two differentiation lines on `cards/task251.json` (against task269 and task255), which this pass was not permitted
  to write; the author owns it before the re-ship.
- Containers scrubbed (the organisation's producer and the fiction's dates) in target/ and golden/.
- Golden realism: the workbook leads with the finding as its title, lists the seven with road, location, district,
  controller (R08-05's swap date beside its TCX-4) and validation site, carries the maintenance sheet by district and
  quarter with totals, and a notes sheet stating the estimand, both error terms, where each is measured and how a
  visit and a failure were counted; the chart shows every station's error against the band by district with the
  controller in each label, the seven marked, and the two swaps noted under the source line.
- The 10/10 rules re-read against the repaired pack: the decisive step is still the two error terms estimated from
  the network's own pairs and carried through each station's hours, which no filed sentence performs, and no sentence
  added in this repair names a queue, a temperature, a generation's counting or the bridges. Every Layer 1 item
  mishandled leaves the call unchanged (asserted: the clock offset, the renumbered hours, the occupancy precision,
  the missing temperature day, the current controller all year). The four closures file facts about the world and the
  equipment (one loop detail at every station, what the record holds and what the system raises), never a method.
- Open risk, stated: a reader who fits the queue loss on the bridge pairs and also places the cold miss on the TCX-2
  by occupancy per counted vehicle lands the call, and one portal response did. The ladder is unchanged, so that
  response lands it again and banks 45 of the rubric; what changed is that it now keeps none of the 24 ask figures,
  which puts the pair at 28.5 against the build target of 60.

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
- 2026-10-27, the portal's determinism block (two judges, both `competing_defensible_answer`, `fix_location
  input_files`) and one portal response at 95 per cent. The stump test first (`/fix-determinism` step 3): closing any
  of the four free parameters in either direction leaves the default path on R14-01 and R25-01 and the golden on the
  seven, measured over every value the record allows and past it (SF27 to SF30), so the fork was not the stump and
  this is a repair. Both judges offered a governing document prescribing the full-year estimation method; filing the
  method is rule application and `CLAUDE.md` rule 3 bans it as the decisive step, so their second option was taken
  instead and every parameter is measured on the record.
- The second instrument the repair rests on was already in the pack and unused: the occupancy a station reports per
  vehicle it counts, read between two sets of months at the same counted free-flowing flow. A vehicle covers the loop
  whether the controller counts it or not, so that ratio moves one for one with a change in the station's counting and
  not at all with the traffic, and it closes three of the four parameters at once (a drift inside a regime, a drift the
  two generations share, the regime no filmed day covers) and gives the cold miss a second, pair-free measurement at
  every station. A coarse version of it (occupancy per vehicle binned by flow) was tried first and refused: a 40
  vehicle bin left a 4.6 per cent seasonal residual at the TCX-4 stations, too loose to bound anything, and fitting
  occupancy against the counted vehicles inside the free-flowing range and reading the fit where the two periods
  overlap took the residual to 0.4 per cent.
- The detector-card replacements (seven surge orders and the 30 June call-out) were removed from the counting path:
  surge damage now takes the surge protector and the modem. Five of the eight preceded their station's filmed day,
  three of them at a flagged station, so a literal reader had no ground for carrying the filmed ratio back over the
  months before the card changed. Nothing else in the year's work touches a loop or a detector, and the spring and
  autumn inspections test the loops at every station.
- An extra validation film in the thirty days before each controller replacement was drafted as the anchor for the
  unfilmed regime and refused: the filming season is July and August by section 4, an April or October film at a
  congested station would hold queued hours and colder days, and the two facts the recommendation rests on (no filmed
  hour above 8.2 per cent occupancy, no filmed day below 13 degrees) would have stopped being true. The station's own
  occupancy channel measures the same thing with no new file.
- Moving the two controller replacements into the first week of January was also refused: it re-rolls the sensitivity
  draw and with it the four rung lists, which a determinism repair may not move.
- `traffic_data_dictionary.md` was dropped from the pack and the facts it carried that anything depends on moved into
  TDP-03 at authority (section 3: the station number in force for the hour, occupancy in per cent at the controller's
  precision, a part hour discarded, the TCX-2 with no standby supply and the TCX-4's battery; section 7: what
  TrafficVault polls and raises and what a controller reports). A shipped file whose job is to describe the data is a
  leak (`dataset-generation` section 3) and `leak.py` sweep 1 now reads the file name as one; the pack is 11 files and
  4 formats without it, and a generator assertion refuses any file or sheet that describes the data.
- The ask layer was re-devised onto a second grain of the same records after the portal measured both shipped devices
  inside a strong reader's path. Ask A first took the office-reset exclusion as its primary; it is now pinned in
  section 7 and the primary is the after-hours attendance that crosses midnight, where the labour line carries one date
  and the cabinet door log carries two. Ask B first took the TCX-2 breaks as its primary; the TCX-2's behaviour is now
  filed in section 3 and the primary is the loss that stopped a TCX-4, which has no MAINS_FAIL at all because the
  controller lost what it had buffered. Both of judge 2's ask findings are closed with it: section 7 excludes work done
  from the contractor's own premises, and it counts a supply restored and lost again as a second failure, which the
  two licensed readings of a break then agree on (asserted).
- The office resets were forced to two or three a cell rather than exactly two after the first measurement: with one
  night attendance a cell, exactly two resets made the labour-day route right in eight cells of twelve, the two
  devices cancelling. Two or three against one leaves the labour days one or two too high in every cell.
- The battery endurance was shortened from six hours to three so that an interruption outlasting it occurs in every
  district and quarter rather than once in the year, and the automatic battery-replacement order was held to the one
  December outage over six hours: an order reading "controller restarted cold after power failure" at every drained
  station would have handed the device to anyone reading the work orders for ask A.
- Step 5's invariance claim at "a third again" (a per-station loss scale of 1.3333): true on the generator's own
  fitted curve, which holds the list to 1.35 (R18-01, the largest unlisted error, at 4.95 per cent) and breaks at
  1.40 (5.18 per cent), but only 0.12 points clear of the 5 per cent line at 1.3333 (4.88 per cent), and the
  third-pass judge, fitting the loss curve itself from the shipped bridges, read R18-01 at 5.2 per cent there and
  called the sentence a defect. Narrowed in the shipped sentence to "a fifth again" (1.20, R18-01 at 4.29 per cent,
  0.71 points clear, confirmed in the judge's own fit); the asserted invariance band stays wider than the shipped
  claim because an independently fitted curve crosses earlier, so checks.py SF28 goes on measuring 0.5 to 1.35.

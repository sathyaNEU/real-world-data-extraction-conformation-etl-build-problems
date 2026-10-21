# task251 design note

## Draw

Card `cards/task251.json` (architecture 4, re-rooted 2026-10-21 from architecture 3, spent at stage 4; a fresh rebuild
at the author's standing instruction, see Tried and rejected and the card's lineage). Guard verdict WARN, no BLOCK. The
WARNs, answered: repeat.gate_g and overuse.gate_g (method_or_model_selection after task484 and task271: the two methods
are the validation day's error and a load-dependent error model, and the data's own conservation pairs pin the second,
which is the vocabulary's definition; no other mechanism is honest here); repeat.decision (designation_set after task271:
the decision is the set of stations the report flags and the contractor recalibrates); repeat.deliverables (xlsx and png:
the list goes to the contractor as a workbook and the report prints the chart); repeat.question_form (which: a pick of
stations). At filing task484 held statistical_office_head and register, task478 monitoring_export, task479 published_series and
task271 line_manager_or_team, and test.same_driver matched population, G7 and method_or_model_selection against task271 v2 and
task471 v1 lineage: role, artifact and forum were redrawn to the honest neighbours below (the artifact twice, as task479 filed) and G5 leads the generators.

- **Pairing.** General Statistics & Data Science / missing-data-censoring-measurement-error, drawn for Data Quality
  Monitoring & Alerting. The object is the health of a regional municipality's permanent traffic counts, and the call
  is a monitoring decision: which count stations the 2027 report flags as not meeting the counting standard, the same
  stations the maintenance contractor recalibrates in the spring 2028 round.
- **The seed, re-found.** DQ24 gave the world (instruments checked against a reference), the decision (which instruments
  go for recalibration) and the quantity (each instrument's error against a tolerance). Architectures 1 to 3 spent a
  reference chain, a wear clock and a selection on the measured value. The decisive step is re-found in the data's own
  structure: the only validation each station gets is filmed on a summer weekday, when nothing queues, while its loops
  lose vehicles in the term-time queues that only the river bridges' two approaches, counting the same stream, reveal.
- **Niche.** The Regional Municipality of Halbrook (fictional, southern Ontario) counts traffic at 30 permanent stations
  on its regional roads, inductive loops in every lane reporting each hour's vehicles and occupancy to the count
  management system. Five of the stations stand in pairs on the two approaches of its Kessel River bridges, counted since
  a 2019 crossings study. Every July and August a contractor films each station for one weekday and counts every vehicle.
  TDP-03, the region's counting standard, flags a station whose year's count misstates the vehicles that passed by more
  than 5 per cent, and the flagged stations go to the maintenance contractor's spring recalibration.
- **The call.** Which stations' 2027 counts are beyond 5 per cent either way, if any.
- **Shape.** other: the list (each of the 30 stations in or out, the two the validation days keep out of it), the
  chart of every station's error against the band with the list marked, and the asks' 24 figures (maintenance visits
  and power failures by district and quarter): about 35 criteria. No station's error is a graded figure: the
  licensed estimates spread a station's error by up to 0.6 points, so the list and the margin are graded, never a
  printed error.
- **Strategy.** `composition_mix`: a station's error depends on the traffic state, the validation day's states (free
  flow only) differ from the year's (term-time queues), and the queued state's loss has to be measured elsewhere and
  carried through each station's own mix of states. Gate G method_or_model_selection; generators G5, G7, G17; gap
  population; calibration other (a conservation pair, see the card); context artifact operations_log (the maintenance
  contractor's 2027 work orders at the stations, which answer their own question and rank nothing); Layer 2 field_method, pattern
  own:conservation-pairs-load-dependent-detector-loss.
- **Forum, event, organisation.** customer_or_counterparty (the maintenance contractor receives the recalibration list),
  statutory_or_regulatory_filing (the annual count report the region files with the province by 31 March 2028, flags
  included), local_government. Role compliance_or_audit (the traffic data coordinator answers for the counts' accuracy).
- **People** (`guard.py names --geo Canada --seed 251`, locale en_CA): Miranda Harris, the traffic data coordinator, who
  asks; Andrew Wong, the validation contractor's project manager; Yvonne Larson, the maintenance contractor's service
  manager. None appears in the prompt.
- **Data-native sentence.** A loop counts a vehicle when its occupancy pulse starts and ends; in a crawling queue the
  gaps between vehicles close and two vehicles hold one pulse, so the loops lose vehicles as occupancy rises, the summer
  validation day never sees that state, and on a bridge, where nothing joins or leaves, the queued approach's count
  falls short of the free approach's by exactly the vehicles lost.

## Default path

1. Read TDP-03 (the year's error: the vehicles counted in the hours counted against the vehicles that passed, both
   directions, beyond 5 per cent flagged) and the station register.
2. Read the contractor's 2027 validation counts: for each station, 24 hours on a July or August weekday, the video
   count and the loops' count by direction and 15 minutes.
3. Take each station's error as its loops' count against the video count over the validation day, both directions.
4. Flag the stations beyond 5 per cent.

Ends on: R03-02, R14-01 and R18-01
Golden: R03-02, R04-03, R05-01, R08-05 and R10-03

## Stump sentence

A competent solver takes each station's 2027 error from its summer validation count and flags R03-02, R14-01 and
R18-01; the validation days were July and August weekdays with no hour above 8.8 per cent occupancy, so they miss the
vehicles the loops lose in term-time queues, which the bridges' two approaches show growing with occupancy, and the list
misses R04-03, R05-01, R08-05 and R10-03 and keeps R14-01 and R18-01, which the loss brings back inside.

## Three rules

Task type: missing-data-censoring-measurement-error (General Statistics & Data Science), tagged in the taxonomy for Data Quality Monitoring: a measurement-error model with a load-dependent term, estimated from a natural pairing of instruments on one conserved stream because the validation design never sampled the load at which the error arises.
Domain test: The deciding quantity is each count station's error over the traffic it carried in 2027, the loops' sensitivity together with a loss that grows with occupancy in queued traffic: a measurement-error model with a load-dependent term, which the traffic data field estimates where the same vehicles are counted twice with nothing joining or leaving and carries through each detector's own hours; replacing it with each station's validation-day error, the generic calibration summary, changes the list.
Swap: "the stations whose count is beyond 5 per cent once the loss the bridges' paired approaches show in queued traffic is carried through each station's own occupancy" put into a hospital's glucose meters loses its mechanism, since no two meters read the same blood with nothing added or taken between them while one of them sits in a queue; replacing the load-dependent model with each station's validation-day error changes the list.
Layer 1: the count management system's hourly export in local time with each hour's UTC offset (the autumn hour twice, the spring hour missing); the contractor's own site codes against the region's station numbers; two stations renumbered when their controllers were replaced; occupancy to one decimal from the older controllers and to two from the newer ones; the hours a controller lost to a power failure absent from the export; the contractor's sheets per station, direction and 15 minutes on different days; the network file keyed by road and kilometre point; for the asks, TrafficVault's event log in UTC with the repeats a controller sends after a lost poll and a cold start's unset clock, and the maintenance contractor's work orders with route orders, two-technician lines and multi-day jobs.
Layer 2: field_method under composition_mix: the error depends on the traffic state, the validation day sampled only free flow, and the queued state's loss is measured on the conservation pairs and carried through each station's own state mix.
Decisive step: estimating each station's 2027 error with a loss term that grows with occupancy, fitted on the bridges' paired approaches (the queued side's count against the free side's, each on its validated sensitivity) and carried through each station's own hourly occupancy, rather than taking the summer validation day's error as the year's.
Not semantics: every field reads as what it is (vehicles counted in the hour, occupancy, the video count of the vehicles that passed), and nothing in any field, code, unit or definition says that loops lose vehicles in queues or that the validation days held no queue; the bridges are in the network file only as structures with a road and kilometre points.
Not rule application: no filed sentence says how a station's year error is estimated; TDP-03 defines the error over the hours counted and states the validation programme's facts, so executing every filed rule on the validation counts files the validation list.
Analyst test: A strong analyst who reads the standard, the register, the validation counts and the hourly counts takes each station's 2027 error from its validation day and flags R03-02, R14-01 and R18-01; the validation days held no queue, so the list misses R04-03, R05-01, R08-05 and R10-03, which the loss pushes past 5 per cent, and keeps R14-01 and R18-01, which it brings back inside (checks.py runs both on the clean world and on the pack).
Estimand: each of the 30 stations' 2027 count error, the vehicles it counted in the hours of 2027 it counted (both directions, every lane) against the vehicles that passed it in those hours, less one; a station is flagged when its error is beyond 5 per cent either way (TDP-03 section 5 and the prompt).
No decoy: nothing is planted: the validation counts are true counts of the vehicles on their days, the loops' counts are what the loops counted, no memo, draft or figure argues for the validation list, and no file ranks the stations by error.
No certified replay: no certified or published figure sits in the pack; the validation workbook states counts and no accuracy verdict, and no file states a station's error, flag or annual traffic.
Lesson: a validation that never samples the condition in which an instrument errs cannot give its error over a year that holds that condition, and a stream counted twice with nothing joining or leaving measures the loss where the condition occurs; no build on file reads a counting error from conservation between paired counters.

## Readability screen

| Rung | Where a reader meets it | Verdict |
|---|---|---|
| 1. Each station's validation-day error (R03-02, R14-01, R18-01) | the validation workbook, TDP-03 sections 4 and 5 | readable |
| 2. Each bridge station read against its far approach, the others at their validation error (R03-02, R04-03, R14-01, R18-01) | nothing names it: the bridges are structures in the network file | silent |
| 3. (decisive) A loss that grows with occupancy, fitted on the bridges' paired approaches in each direction and carried through every station's own hours (the five) | nothing names it: no file says loops lose vehicles in queues or that the filmed days held none; the bridges are structures, the occupancy a column of the hourly export, and only the reasoning that a queued approach and a free approach count the same vehicles sends a reader to the pairs | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the stations | the 30 in the register, a renumbered station once under its current number | each number in the export a station | another list (R08-01 and R08-05 both) | the register's Code history; TDP-03 section 3 (the record continues under the new number) |
| SF2 | 2027 | the local calendar year of the export | the UTC year | same call | asserted |
| SF3 | the vehicles that passed | each hour's count over its sensitivity and one less the loss at its occupancy | five curve forms, the queued spells' edges out, two-hour blocks, vehicle weights, a constant loss above 22, 25 or 28 per cent | same list | asserted over every licensed estimate; listed beyond 6, others within 4.5 per cent |
| SF4 | the error | counted over passed, less one | passed over counted, less one | same list | TDP-03 section 5; asserted |
| SF5 | beyond 5 per cent | strictly | at or beyond | same call | no station within 1.1 points of the line (asserted) |
| SF6 | the hours | the hours each station counted | every hour, the lost ones estimated | same call | TDP-03 section 5; asserted on the world's full record |
| SF7 | the sensitivity | per station and direction | per station | same list | asserted |
| SF8 | occupancy | per cent at the precision each controller reports | every hour at one decimal | same list | the dictionary; asserted |
| SF9 | a renumbered station's hours | joined under the current number | the old number's hours dropped | same list | the register's Code history; asserted |
| SF10 | the validation sites | the register's validation_site | none | same call | asserted, one station per site |
| SF11 | the bridge pairs | each bridge's nearest stations either side, no junction between | none | same call | the network file; asserted |
| SF12 | the validation day | the filmed day, midnight to midnight, both directions | none | same call | TDP-03 section 4; asserted (96 quarter hours each direction) |
| SF13 | an error's rounding | no station's error is graded | a printed error | not graded | the prompt asks for the list; asserted |
| SF14 | a maintenance visit (asks) | a day a maintenance contractor's technician is at a station | each labour line, each order, each door day | the asks only | TDP-03 section 7 (two technicians are one visit); the office resets read as a RESET with the cabinet shut give the same counts (asserted) |
| SF15 | a power failure (asks) | each loss of mains power at a controller, a feeder's re-trip a second loss | each outage once, each break once | the asks only | section 7 (a loss counted once however long it lasts); the TCX-4s log two MAINS_FAIL for a re-trip and TrafficVault's polls two losses at a TCX-2 (asserted) |
| SF16 | a quarter (asks) | calendar quarter by local date | by UTC date | the asks only | TDP-03 sections 3 and 7 |
| SF17 | a district (asks) | the register's district | none | same figures | one district per station (asserted) |
| SF18 | the validation crew (asks) | not a maintenance visit | a visit | the asks only | TDP-03 sections 4 and 7 (the maintenance contractor's technicians) |
| SF19 | a controller replacement (asks) | a visit, not a power failure | a power failure | the asks only | section 7 (a loss of mains power); the work order and the Code history |
| SF20 | the year-2000 stamps (asks) | a cold start's unset clock | events of 2000 | same figures | no MAINS_FAIL carries one (asserted) |
| SF21 | the log's repeats (asks) | one event | two | the asks only | exact repeats after a lost poll (asserted) |
| SF22 | a visit's or failure's day (asks) | local date | UTC date | the asks only | TDP-03 section 3; asserted (aimed) |

## Ladder

| Route | Withdraws | Count | Golden |
|---|---|---|---|
| Each station's validation-day error (the default path) | R03-02, R14-01, R18-01 | 3 | no |
| Each direction's validated sensitivity carried through the year, no loss | the same three | 3 | no |
| The validation day's own quarter hours as the loss's evidence | the same three (no quarter hour above 9 per cent occupancy) | 3 | no |
| Each bridge station against its far approach, the others at their validation error | R03-02, R04-03, R14-01, R18-01 | 4 | no |
| A constant loss above 22, 25 or 28 per cent occupancy from the pairs | the golden five | 5 | yes (licensed) |
| Golden: a loss growing with occupancy from the pairs, carried through every station's hours | R03-02, R04-03, R05-01, R08-05, R10-03 | 5 | yes |

The golden family agrees on the five under every curve form (piecewise linear, power, quadratic, linear above 22 per
cent, two-point bins), with the queued spells' first and last hours left out, over two-hour blocks, with each pair
weighted by its vehicles and with one sensitivity per station; every one keeps the listed stations beyond 6 per cent
and the others within 4.5 (asserted). On the clean world the validation day files the wrong list and the loss
construction the truth (checks.py, dataset-generation 7.1).

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
| 9 | Boundary inclusivity | beyond 5 per cent | C1 (1.1 points clear, asserted) |
| 10 | Rounding path | no error graded; visits and failures whole counts | C1 |
| 11 | Tie-break | none open | asserted |
| 12 | Maturity and censoring | every hour of 2027 delivered by 7 January 2028 | filed (dictionary, export) |
| 13 | Order of operations | sensitivity, then the loss, then the year's ratio | C1 (every order agrees, asserted) |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | the autumn hour twice by offset; the event log's exact repeats once | filed (offsets); asserted |
| 16 | Identity normalisation | current station numbers, site codes through the register | filed (register) |
| 17 | Netting against gross | none | not applicable |
| 18 | Dimensional units | vehicles, per cent occupancy | filed (dictionary) |
| 19 | Code and status semantics | event codes, work order categories | filed (dictionary); never the stump |
| 20 | Integerisation | whole counts on the asks | filed (the asks count) |
| 21 | Clause scope | section 5 for every station; section 7 for every district and quarter | filed |
| 22 | Forward window contents | the spring 2028 round recalibrates the flagged stations | filed (section 5, the mail) |

## Literal reader

Executing the prompt and every filed sentence word for word (TDP-03 sections 2 to 7, the dictionary, the register, the
network file) leaves one open move, how the vehicles that passed each station are estimated; the data's structure
forces it (the filmed days hold no hour above 8.8 per cent occupancy while the year's queued hours run to 50, and only
the bridges' paired approaches count one stream twice), and every licensed estimate of that one quantity files the same
five (asserted, listed beyond 6 per cent, others within 4.5).

## Oracles

- No file ranks the stations or carries a station's error, flag, list or annual traffic.
- The validation workbook carries counts only; every route reads it and none is told its days are unrepresentative.
- The contractor's mail asks for the list and a note if there are none; it carries no station.
- The weather and collision files (the distractors) carry no figure any route needs.

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

## Candidates for architecture 5

Architecture 4 is spent at stage 4, and a re-root past the third architecture is the author's call; at the author's
standing instruction (spent and retired builds are rebuilt fresh, never retired unasked) the next draw takes one of
these. Each carries a default path and a screen, and each puts the reachable correction on the first rung and the
decisive step on a second that no visible contrast invites.

1. **Laboratory analyzers' imprecision under a repeat-until-accepted practice** (General Statistics, measurement error
   x DQ). Which of a laboratory network's chemistry analyzers' between-run imprecision breaches the allowable
   coefficient of variation and goes to the vendor's service visit. Default: the CV of the accepted quality-control
   results in the laboratory system flags few. Reflex rung: within-lot standard deviations (material lot changes move
   the means) flag fewer. Decisive: the accepted results are what survived the repeat rule, the analyzers' own run logs
   count the discarded runs day by day, and the standard deviation is estimated on the truncated sample. Screen: the
   thinning beyond the control limits must not show as a hard edge, and the repeat practice must sit in routine text.
2. **Polled analyzers aliasing a process cycle** (Physical & Environmental Sciences, environmental monitoring x DQ). A
   utility's online analyzers are polled every 15 minutes in step with the aeration blowers' timer, so the stored
   values sample the cycle at a fixed phase. Default: the mean of the polled values. Reflex rung: the verification
   day's offset carried as a constant. Decisive: each plant's phase from the blower event log, which moved when the
   poll schedule or the timer was reset, against the cycle profile from the commissioning logs. Screen: no beat
   pattern in daily means; the aeration control, not generic sampling, must decide.
3. **A service desk's resolution-time indicator** (Business & Operations, service operations x DQ, General Statistics
   task type). Which service centres' reported mean time to resolve understates the truth by more than 10 per cent.
   Default: the dashboard's mean over closed tickets. Reflex rung: the closed tickets with the open backlog dropped or
   imputed. Decisive: the mean time in the system from the daily backlog counts and arrivals (Little's law over the
   year with the opening and closing backlogs). Screen: Little's law is a named identity a strong operations reader may
   apply; the backlog file must read as the desk's own staffing report.
4. **A network intercompared against its own median** (Physical & Environmental Sciences, sensor calibration x DQ).
   Instruments are checked daily against the network median, so a drift most instruments of one model share moves the
   median and reads as no error; external audits with a transfer standard see the shared part only at their sites.
   Default: the error against the median. Reflex rung: each audited instrument's own offset. Decisive: the shared drift
   by model as a function of temperature, from the audits, carried to every instrument through its model and its
   site's temperature. Screen: the audit file invites a cross-check, so the decisive dependence must not be readable
   off one column.

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


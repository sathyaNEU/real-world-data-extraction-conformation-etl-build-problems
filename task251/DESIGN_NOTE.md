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
- **Shape.** other: the list (each of the 30 stations in or out), each listed station's error, the chart of every
  station's error against the band with the list marked, and the asks' figures (stage 2): 25 or more criteria.
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

1. Read TDP-03 (the year's error: vehicles counted against vehicles that passed, both directions, beyond 5 per cent
   flagged) and the station register.
2. Read the contractor's 2027 validation counts: for each station, 24 hours on a July or August weekday, the video
   count and the loops' count by direction and 15 minutes.
3. Take each station's error as its loops' count against the video count over the validation day, both directions.
4. Flag the stations beyond 5 per cent.

Ends on: the validation list (computed by the generator and written here at stage 2).

## Stump sentence

A competent solver takes each station's 2027 error from its summer validation count and flags the stations beyond
5 per cent; the validation days were July and August weekdays when no approach queues, so they miss the vehicles the
loops lose in term-time queues, which the bridges' two approaches show growing with occupancy, and the list misses the
queued stations past 5 per cent and keeps one the loss brings back inside.

## Three rules

Task type: missing-data-censoring-measurement-error (General Statistics & Data Science), tagged in the taxonomy for Data Quality Monitoring: a measurement-error model with a load-dependent term, estimated from a natural pairing of instruments on one conserved stream because the validation design never sampled the load at which the error arises.
Domain test: The deciding quantity is each count station's error over the traffic it carried in 2027, the loops' sensitivity together with a loss that grows with occupancy in queued traffic: a measurement-error model with a load-dependent term, which the traffic data field estimates where the same vehicles are counted twice with nothing joining or leaving and carries through each detector's own hours; replacing it with each station's validation-day error, the generic calibration summary, changes the list.
Swap: "the stations whose count is beyond 5 per cent once the loss the bridges' paired approaches show in queued traffic is carried through each station's own occupancy" put into a hospital's glucose meters loses its mechanism, since no two meters read the same blood with nothing added or taken between them while one of them sits in a queue; replacing the load-dependent model with each station's validation-day error changes the list.
Layer 1: the count management system's hourly export in local time, the autumn hour twice and the spring hour missing; the contractor's own site codes against the region's station codes; two stations renumbered when their controllers were replaced; occupancy to one decimal from the older controllers and as integer tenths of a per cent from the newer ones; the contractor's sheets per station, direction and 15 minutes on different days; the network file keyed by road and kilometre point.
Layer 2: field_method under composition_mix: the error depends on the traffic state, the validation day sampled only free flow, and the queued state's loss is measured on the conservation pairs and carried through each station's own state mix.
Decisive step: estimating each station's 2027 error with a loss term that grows with occupancy, fitted on the bridges' paired approaches (the queued side's count against the free side's, each on its validated sensitivity) and carried through each station's own hourly occupancy, rather than taking the summer validation day's error as the year's.
Not semantics: every field reads as what it is (vehicles counted in the hour, occupancy, the video count of the vehicles that passed), and nothing in any field, code, unit or definition says that loops lose vehicles in queues or that the validation days held no queue; the bridges are in the network file only as structures with a road and kilometre points.
Not rule application: no filed sentence says how a station's year error is estimated; TDP-03 defines the error over the year and states the validation programme's facts, so executing every filed rule on the validation counts files the validation list.
Analyst test: A strong analyst who reads the standard, the register, the validation counts and the hourly counts takes each station's 2027 error from its validation day and flags the stations beyond 5 per cent; the validation days held no queue, so the list misses the queued stations the loss pushes past 5 per cent and keeps one it brings back inside (the generator asserts the lists at stage 2).
Estimand: each of the 30 stations' 2027 count error, the vehicles it counted in 2027 (both directions, every lane) against the vehicles that passed it in 2027, less one; a station is flagged when its error is beyond 5 per cent either way (TDP-03 and the prompt).
No decoy: nothing is planted: the validation counts are true counts of the vehicles on their days, the loops' counts are what the loops counted, no memo, draft or figure argues for the validation list, and no file ranks the stations by error.
No certified replay: no certified or published figure reproduces only under one method; the 2026 report publishes each station's AADT and no error or flag, and the contractor's report states its counts and no accuracy verdict.
Lesson: a validation that never samples the condition in which an instrument errs cannot give its error over a year that holds that condition, and a stream counted twice with nothing joining or leaving measures the loss where the condition occurs; no build on file reads a counting error from conservation between paired counters.

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

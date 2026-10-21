# task252 design note

## Draw

Card `cards/task252.json` (architecture 1). Guard verdict PASS after one redraw: the forcing event was drawn as
launch_or_rollout (a chlorine dose trim going live) and BLOCKed against task177, so it was redrawn to period_close, the
honester label anyway: the quarter has closed, its online monitoring return is being compiled, and the flags decide
which readings the return marks provisional and which channels the technicians take on before the next quarter.
`guard.py slots` finds no earlier screen on carryover with a zero or span error (both searches empty); nearest drivers
task91 (0.09) and task229's lineage (0.07), neither a measurement-error read.

- **Pairing.** Physical & Environmental Sciences / sensor-calibration-measurement, drawn for Data Quality Monitoring &
  Alerting. The object is the health of a district council's online ammonia monitoring, and the call is a monitoring
  decision: which treated-water channels the fourth-quarter 2027 online monitoring return flags as reading more than
  0.005 mg/l as N off the water they sample.
- **The seed, re-found.** DQ25 gave the world (low-level channels whose laboratory grabs sit under the detection
  limit), the decision (the channels escalated this quarter) and the quantity (each channel's error at its own low
  level against a tolerance). Its censored-mean pitfall is not used: the treated grabs are censored, so the error has
  to come from the analysers' own structure. A three-stream analyser carries part of each sample into the next two
  readings through its shared sample line, and a check at one level cannot say whether an analyser's error is a zero
  or a span error, which decides its size at the treated level.
- **Probes before the build.** Call-only rounds, three isolated readers each (Sonnet, medium), on packs cut from the
  prototypes: carryover alone, 3 of 3 landed; carryover with a zero error at a healthy analyser and a span error at
  another, 1 of 3 (the one that landed read the raw ports against the raw grabs); this design, the zero error on a worn
  analyser, 0 of 3 (A2 filed eight, Hollins' final water and a borderline third port included, never using the
  checks; B2 three, from a censored fit to the grabs; C2 five, fitting the previous port only and so missing Garth
  Hill's final water). See Tried and rejected.
- **Niche.** Turangawai District Council (fictional, New Zealand) runs eight water treatment plants on river intakes:
  Ashcombe, Brayford, Calderwood, Dunmere, Elstow, Fenwick, Garthmore and Hollins. After dairy-catchment incidents each
  plant was given one colorimetric ammonia analyser with a three-stream sequencer: it reads raw, filtered and final
  water in turn through one sample line and one measuring cell, ten minutes a port, a 30-minute cycle, in the port
  order the register gives (raw, final, filtered at five plants; raw, filtered, final at Calderwood, Garthmore and
  Hollins). Readings go to the control system's historian; each analyser is checked monthly on a 0.100 mg/l as N
  standard through its check port on a flushed cell (three readings, 10 per cent tolerance); the contract laboratory
  takes weekly grabs at all 24 sample points (detection limit 0.030 mg/l as N). Five analysers are worn (Brayford,
  Dunmere, Elstow, Garthmore, Hollins: each reading carries about 6 to 7 per cent of the sample before it and about a
  third of that of the one before that); Hollins' zero water is contaminated (it reads about 0.0085 low at every
  level); Calderwood's reagent is weak (it reads about 9 per cent low, a span error); three plants (Ashcombe, Dunmere,
  Fenwick) pass raw-water ammonia through to treated water after their transit times; three catchments (Calderwood,
  Garthmore, Hollins) run raw ammonia two to three times the others'. WQ-DS-04, the council's online monitoring data
  standard, flags a treated-water channel whose quarter offset (the mean, over its readings coded G, of the reading less
  the ammonia in the water at its sample point) is beyond 0.005 either way.
- **The call.** Which of the 16 treated-water channels are beyond 0.005 for the fourth quarter of 2027, if any.
- **Shape.** 07: the 16 channels, eight plants by two waters, each in or out; the chart of every channel's offset
  against the band with the flagged channels marked; the asks' figures. No channel's offset is a graded figure (the
  licensed carryover fits differ by up to 0.0015 on a channel); the list, and the margin every licensed estimate keeps,
  are.
- **Strategy.** `decomposition_attribution`: each channel's offset is split into the sequencer's carryover and the
  analyser's calibration error, and the calibration error's form is attributed from two levels, the check standard and
  the raw grabs, once the raw port's own carryover is taken out. Gate G decomposition_attribution; generators G7 (the
  check's single operating level against the channel's), G16, G4, G17; gap population (the readings are not the
  water); calibration physical_verification (the check standard); context artifact monitoring_export; Layer 2
  field_method, pattern own:sequencer-carryover-plus-zero-versus-span-two-point-calibration.
- **Forum, event, organisation.** operations_desk (the water services operations desk receives the flags and the
  technicians' list), period_close (the quarter's return), local_government. Role compliance_or_audit (the water
  quality compliance officer answers for the return).
- **People** (`guard.py names --geo NZ --seed 252`, locale en_NZ): Emily Butler, the water quality compliance officer,
  who asks; Cameron Waugh, the instrument and controls technician who runs the checks; Suzanne Nelson, the contract
  laboratory's client services coordinator. None appears in the prompt.
- **Data-native sentence.** A multi-stream analyser's measuring cell never fully empties between ports, so each
  reading holds a share of the sample before it and a smaller share of the one before that, which shows as a response
  to the previous ports at no lag while the treated water itself answers the raw water only after the plant's transit
  time; the same carryover dilutes the raw port toward the treated samples ahead of it, so at a worn analyser the raw
  port reads low in proportion against the laboratory's raw grabs, and a check shortfall at 0.100 read beside those
  grabs looks like a span error until that dilution is taken out and the constant zero error is left.

## Default path

1. Read WQ-DS-04 (a treated channel's quarter offset, the mean over its G readings of the reading less the water's
   ammonia, flagged beyond 0.005 either way), the register (port orders, ten-minute ports) and the process summary
   (transit times).
2. See that the treated grabs are mostly under the 0.030 limit, so the offsets have to come from the readings.
3. Fit each treated channel's readings on the readings of the ports before it in the cycle, with the raw readings at
   the plant's transit lags for the real breakthrough: the zero-lag response is carryover, about 6 to 7 per cent of
   the port before and 2 per cent of the one before that at five analysers.
4. Read the checks: every one passes; Hollins and Calderwood read about 8 per cent low, and both raw ports read about
   9 to 11 per cent low against the laboratory's raw grabs, so both are span errors worth about 0.002 at treated levels.
5. Flag the channels whose carryover offset, with the span correction, is beyond 0.005.

Ends on: BRF-FW1, DUN-FW1, ELS-FW1, GAR-FI1, GAR-FW1, HOL-FI1 and HOL-FW1
Golden: BRF-FW1, DUN-FW1, ELS-FW1, GAR-FI1, GAR-FW1 and HOL-FI1

## Stump sentence

A competent solver fits each treated channel's carryover from the two ports before it, reads Hollins' and Calderwood's
low checks as span errors because both raw ports read about as low against the laboratory's raw grabs as their checks
do, and flags HOL-FW1 beside BRF-FW1, DUN-FW1, ELS-FW1, GAR-FI1, GAR-FW1 and HOL-FI1; Hollins is a worn analyser, so its
raw port reads low through its own carryover from the treated ports ahead of it, and with that dilution taken out its
grabs show the same 0.008 shortfall at 0.4 as its check shows at 0.100, a zero error that cancels HOL-FW1's carryover
from the raw sample two ports back, while Calderwood's analyser, with no carryover, has a true span error that is
worth 0.002 at treated levels; the list is the six.

## Three rules

Task type: sensor-calibration-measurement (Physical & Environmental Sciences), tagged in the taxonomy for Data Quality Monitoring: each online channel's quarter error against the water it samples, split into the sequencer's carryover and the analyser's calibration error, whose zero and span are separated by a two-point calibration on the check standard and the raw grabs.
Domain test: The deciding quantity is each treated channel's mean offset from the ammonia in its water: the carryover a three-stream sequencer leaves from the two samples before it (fitted on the zero-lag response, apart from the raw-water breakthrough that reaches treated water only after the plant's transit time) plus the analyser's calibration error at the channel's own level, its zero and its span read from the 0.100 check standard against the weekly raw-water grabs once the raw port's own carryover is taken out, the instrument field's two-point calibration; replacing it with carryover alone, or with the check's shortfall read as a span or added as an offset, changes the list.
Swap: "the channels more than 0.005 off once each analyser's carryover from the two ports before it and its zero and span, read from the check standard against the raw-water grabs with the raw port's own carryover taken out, are carried to the channel's own level" put into a hospital's ward glucose meters loses its mechanism, since no meter reads three bloods in turn through one cell, no blood reaches a meter hours after it passed another, and no meter's reference reading is diluted by the patient before; replacing the two-point read with one check changes the list.
Layer 1: the historian's readings export stamped in UTC against the laboratory's sample times in New Zealand daylight time; the check-port readings inside the readings stream under quality code V and the fault slots under F; treated-water laboratory results reported below the 0.030 detection limit; the laboratory's own sample point codes against the control system's tags; the register's port sequence history, two analysers resequenced at their mid-2027 annual service. Nothing is placed to be caught.
Layer 2: field_method under decomposition_attribution: each channel's offset is carryover (the zero-lag response to the two ports before it, separated from the real breakthrough by the transit lag) plus a calibration error whose form decides its size at the channel's level, and the form is read from two levels, the check standard and the raw grabs, after the raw port's own carryover is removed.
Decisive step: reading each low-checking analyser's error as a zero or a span error from the weekly raw-water grabs against its raw port with the raw port's own carryover from the ports ahead of it taken out (a zero error keeps the check's absolute shortfall at the raw level, a span error grows in proportion), and carrying it to each treated channel's own level beside that channel's fitted carryover from both ports before it, rather than ignoring the passed checks, reading both shortfalls as span errors because both raw ports read low in proportion, or adding the shortfall to every channel as an offset.
Not semantics: every field reads as what it is (the analyser's reading at its sample point, the check standard's value and three readings, the laboratory's result and its detection limit, the port order), and nothing in any field, code, unit or definition says that a cell carries one sample into the next, that an analyser's error is a zero or a span error, or that a raw port reads low because of the treated ports ahead of it; the check workbook states readings and a pass against a 10 per cent band, no cause.
Not rule application: WQ-DS-04 defines the offset (the mean over the quarter's G readings of the reading less the ammonia in the water at that time) and the 0.005 band, and says nothing on how the water's ammonia is to be estimated; executing every filed rule on the files gives no offset at all, and no rule names carryover, the transit times, the zero, the span or the raw port's dilution.
Analyst test: A strong analyst who fits each channel's carryover from the ports before it and reads the two low checks as span errors (both raw ports read low in proportion against the raw grabs) or sets them aside because every check passed flags HOL-FW1 with the six; one who adds the check shortfall to every channel as an offset flags CAL-FI1 and CAL-FW1 instead; one who fits the previous port only misses GAR-FW1 and flags three filtered channels low; only the two-point read with Hollins' raw port carryover taken out files the six (checks.py runs every route on the clean world and on the pack).
Estimand: each of the 16 treated-water channels' offset for the fourth quarter of 2027 (New Zealand time), the mean over the readings it reported with quality code G in the quarter of the reading less the ammonia in the water at its sample point at that time, in mg/l as N; flagged when more than 0.005 either way (WQ-DS-04 sections 3 and 4 and the prompt).
No decoy: nothing is planted: the readings are what the analysers reported, the checks what they read on the standard, the grabs the laboratory's results; Calderwood's span error and Hollins' zero error are faults of the instruments being monitored, each shown only by the data; no memo, draft or figure argues for any list, and no file ranks the channels by offset.
No certified replay: no certified or published figure sits in the pack; the check workbook states readings and a pass, the laboratory file results, and no file states a channel's offset or flag.
Lesson: a check at one level measures an instrument's error at that level only; whether it is a zero (the same at every level) or a span (in proportion) is read by setting the check beside a reference at another level, and when the reference channel is itself diluted in proportion by the instrument's carryover, that dilution has to come out first or every zero error reads as a span; no shipped build separates a zero from a span error, or reads a reference through the instrument's own carryover.

## Tried and rejected

- Sample-line lag plus bottle decay (online analysers against weekly grabs, prototype p3): the lag needs grabs taken
  while the level climbs on the morning round, task249 v5's sampling phase set by access; the decay is task248's loss
  in transit. Dropped on paper before any pack.
- PCR Ct assay shift net of each region's epidemic phase and variant replacement (prototypes p1 to p3): the phase
  effect on positives' Ct is a function of each region's whole recent incidence curve, so every regression form left
  about a cycle of residual and four licensed forms disagreed in four of eight seeds. Not determinate.
- Tide-gauge logger clock error read from high-water timing with the tide's flow and spring-neap travel time taken
  out (prototypes t1 to t3): per-tide timing at the upper gauges scatters 5 to 14 minutes from surge and asymmetry,
  so without clock-free gauges upstream a 5-minute clock error is not pinned, and with them the stump is one insight
  read straight off those gauges.
- Filter effluent turbidimeters' ripening-peak capture read against each gallery's combined effluent (flow shares,
  the channel's smoothing calibrated on the four laser units; probe pack seed 25): all three call-only probes filed the
  five (rebuilt each filter's rise from the combined effluent and fitted the channel on the laser units). A sluggish
  unit shows in its own record and the reference is the first thing a reader reaches for. Dead at 3 of 3.
- Each laboratory's PCR assay offset read from patients tested at two laboratories within days (prototype q1): the Ct
  change between a patient's two tests depends on where each falls in the infection, so one per-day slope from
  same-laboratory retests mis-corrects the outbreak-sweep pairs that anchor the network; the golden missed the truth
  in all six seeds.
- Multi-stream ammonia analyser carryover separated from real treatment breakthrough by lag (8 plants, 16 treated
  channels, seed 45 of cw3; licensed distributed-lag and first-difference fits agree on 4 at 0.003 margins): call-only
  probes A, B and C all filed the four in about two minutes each. The register's three-stream sequencer and the
  process summary's transit hours put the physics in plain view: "treated water cannot respond to the raw stream
  within ten minutes, so the zero-lag coefficient is carryover" was each reader's first idea. Dead at 3 of 3; kept as
  the loud first effect of the design that followed.
- Paper screens set aside before any pack: CO2 sensors' automatic baseline correction in rooms that never reach
  outdoor air (the physics is in plain view once a datasheet names the baseline logic); water meters' low-flow
  under-registration weighted by a flow profile (the reference logging study is the natural source, so the profile leg
  is no leg); closed-loop dissolved-oxygen sensors read through airflow between parallel lanes (diffuser fouling and
  the oxygen-transfer model leave the offsets undeterminate at the 0.3 mg/l scale); copy-forward and heaping in nursing
  observations (the client's own example of a planted copied block); GNSS velocity uncertainty under flicker noise
  (the literal "standard error" is the white-noise formula, a fork).
- Major-ion biases from the ion balance and calculated conductivity with no anchors (prototypes i2, i3): the ion
  balance fixes the methods' biases only up to a common scale, the conductivity model sets the scale, and its
  ionic-strength term or the two equations' weighting moved every bias by 5 to 15 per cent. Not determinate.
- A regional laboratory's major-ion methods, two of eight biased by their own stock or titrant standard, read from the
  quarter's ion balances with the six CRM-checked methods as anchors (probe pack ions/probe, 1,497 samples): probes A
  and B filed potassium and alkalinity by regressing the anchored imbalance on the two unverified ions; C regressed on
  all eight unanchored and filed none. Dead at 2 of 3: the electroneutrality constraint is the natural independent
  check once the QC's circularity is seen.
- Carryover plus a zero-water blank at Elstow (worn) and Hollins (healthy), checks 7 per cent low (probe pack probe5,
  seed 128 of cw5): 0 of 3 landed, but Elstow's blank is not determinate under its own raw carryover at its low raw
  level (one probe read it as a span error, slope 0.91, from its raw port). Moved the blank to a healthy analyser and
  gave a second healthy analyser a span error with the same check shortfall.
- Carryover plus a zero error at healthy Hollins and a span error at healthy Calderwood, both checks about 9 per cent
  low (probe pack probe9, seed 59 of cw9): 1 of 3 landed. A compared each raw port with the raw grabs, storm samples
  above 1 mg/l included, read Hollins as a zero error and Calderwood as a span error and filed the six; B read both
  checks as span errors; C compared the raw ports too but called both span. At about one in three the portal's top two
  land together too often, so Hollins was made worn as well, with high raw water: its raw port then reads low in
  proportion through its own carryover, about as much as its check, and only a reader who takes that carryover out
  first sees the constant zero error, which now cancels the final water channel's memory carryover (probe pack
  probe11, seed 45 of cw11: 0 of 3).

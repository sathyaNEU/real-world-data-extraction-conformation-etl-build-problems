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
  analyser, 0 of 3 (A2 filed eight, Holmedale's final water and a borderline third port included, never using the
  checks; B2 three, from a censored fit to the grabs; C2 five, fitting the previous port only and so missing Garth
  Hill's final water). See Tried and rejected.
- **Niche.** Fernvale District Council (fictional, New Zealand) runs eight water treatment plants on river intakes:
  Ashcombe, Brannock, Calderwood, Dunmere, Elstow, Fenwick, Garrick and Holmedale. After dairy-catchment incidents each
  plant was given one colorimetric ammonia analyser with a three-stream sequencer: it reads raw, filtered and final
  water in turn through one sample line and one measuring cell, ten minutes a port, a 30-minute cycle, in the port
  order the register gives (raw, final, filtered at five plants; raw, filtered, final at Calderwood, Garrick and
  Holmedale). Readings go to the control system's historian; each analyser is checked monthly on a 0.100 mg/l as N
  standard through its check port on a flushed cell (three readings, 10 per cent tolerance); the contract laboratory
  takes weekly grabs at all 24 sample points (detection limit 0.030 mg/l as N). Five analysers are worn (Brannock,
  Dunmere, Elstow, Garrick, Holmedale: each reading carries about 6 to 7 per cent of the sample before it and about a
  third of that of the one before that); Holmedale's zero water is contaminated (it reads about 0.0085 low at every
  level); Calderwood's reagent is weak (it reads about 9 per cent low, a span error); three plants (Ashcombe, Dunmere,
  Fenwick) pass raw-water ammonia through to treated water after their transit times; three catchments (Calderwood,
  Garrick, Holmedale) run raw ammonia two to three times the others'. WQ-DS-04, the council's online monitoring data
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
  who asks; Cameron Waugh and Caleb MacDonald, the instrument and controls technicians who run the checks; Suzanne
  Nelson, the contract laboratory's client services coordinator. None appears in the prompt. The guard's one people
  WARN (the first name Caleb in task196, an older build) is left: the name is the draw's own, and no
  build in the window shares it.
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
4. Read the checks: every one passes; Holmedale and Calderwood read about 8 per cent low, and both raw ports read about
   9 to 11 per cent low against the laboratory's raw grabs, so both are span errors worth about 0.002 at treated levels.
5. Flag the channels whose carryover offset, with the span correction, is beyond 0.005.

Ends on: BRN-FW1, DUN-FW1, ELS-FW1, GAR-FI1, GAR-FW1, HOL-FI1 and HOL-FW1
Golden: BRN-FW1, DUN-FW1, ELS-FW1, GAR-FI1, GAR-FW1 and HOL-FI1

## Stump sentence

A competent solver fits each treated channel's carryover from the two ports before it, reads Holmedale's and Calderwood's
low checks as span errors because both raw ports read about as low against the laboratory's raw grabs as their checks
do, and flags HOL-FW1 beside BRN-FW1, DUN-FW1, ELS-FW1, GAR-FI1, GAR-FW1 and HOL-FI1; Holmedale is a worn analyser, so its
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
Analyst test: A strong analyst who fits each channel's carryover from the ports before it and reads the two low checks as span errors (both raw ports read low in proportion against the raw grabs) or sets them aside because every check passed flags HOL-FW1 with the six; one who adds the check shortfall to every channel as an offset flags CAL-FI1 and CAL-FW1 instead; one who fits the previous port only misses GAR-FW1 and flags three filtered channels low; only the two-point read with Holmedale's raw port carryover taken out files the six (checks.py runs every route on the clean world and on the pack).
Estimand: each of the 16 treated-water channels' offset for the fourth quarter of 2027 (New Zealand time), the mean over the readings it reported with quality code G in the quarter of the reading less the ammonia in the water at its sample point at that time, in mg/l as N; flagged when more than 0.005 either way (WQ-DS-04 sections 3 and 4 and the prompt).
No decoy: nothing is planted: the readings are what the analysers reported, the checks what they read on the standard, the grabs the laboratory's results; Calderwood's span error and Holmedale's zero error are faults of the instruments being monitored, each shown only by the data; no memo, draft or figure argues for any list, and no file ranks the channels by offset.
No certified replay: no certified or published figure sits in the pack; the check workbook states readings and a pass, the laboratory file results, and no file states a channel's offset or flag.
Lesson: a check at one level measures an instrument's error at that level only; whether it is a zero (the same at every level) or a span (in proportion) is read by setting the check beside a reference at another level, and when the reference channel is itself diluted in proportion by the instrument's carryover, that dilution has to come out first or every zero error reads as a span; no shipped build separates a zero from a span error, or reads a reference through the instrument's own carryover.

## Readability screen

| Rung | Where a reader meets it | Verdict |
|---|---|---|
| 1. Carryover into the port read straight after raw water only, the checks set aside (BRN-FW1, DUN-FW1, ELS-FW1, GAR-FI1, HOL-FI1) | the register's port sequences and the process summary's one sample line and cell; the zero-lag response to the raw reading is plain in every worn analyser's record | readable |
| 2. Carryover from the two ports before (adds GAR-FW1 and HOL-FW1: the default path's seven with the checks set aside) | nothing names a second sample's share; the reading two slots back carries it at no lag, large at Garrick and Holmedale because their raw water is high | silent |
| 3. The low checks read as span errors (the seven) | the check workbook; both analysers' raw ports read low in proportion against the laboratory's raw grabs, so the reading reconciles | readable |
| 4. The check shortfall added to every channel as an offset (the six with CAL-FI1 and CAL-FW1, eight) | the check workbook | readable |
| 5. (decisive) The two-point read with each raw port's own carryover taken out: Holmedale a zero error, Calderwood a span error (the six) | nothing names it: no file gives an error's form, says a raw port is diluted by the ports ahead of it, or that Holmedale's analyser is worn as well as low | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the channels | the 16 filtered and final water sample points | the raw water points too | another list only if raw is counted | the prompt; WQ-DS-04 section 4 (treated water channels) |
| SF2 | the fourth quarter of 2027 | 1 October to 31 December, New Zealand time | UTC dates | same call | WQ-DS-04 section 1; asserted |
| SF3 | the readings | the channel's rows held with quality G, a reloaded slot's G row included | a reloaded slot's F row kept and its G row dropped | same call | section 3 (readings held with code G); asserted |
| SF4 | the ammonia actually in the water | the water at the sample point at each reading's time | the laboratory's treated grabs | no quarter mean (most treated grabs below 0.030) | section 3 (over every G reading); section 6 (the limit) |
| SF5 | more than 0.005 | strictly | at or beyond | same call | every licensed estimate 0.0022 or more from the line (asserted) |
| SF6 | above or below | either sign | above only | same call (all six read high) | the prompt; section 4 |
| SF7 | the carryover's form | a mix in the cell: each reading 1 - k1 - k2 of its own water, k1 and k2 of the two samples before | the shares of the readings before added on (the additive law) | another list (DUN-FI1 at 0.0055) | the worn analysers' raw ports read their raw grabs low by 0.010 to 0.039, as a mix does and an added carryover cannot (asserted) |
| SF8 | the treated water's own response | the raw readings 2 to 8 hours earlier | 1.5 to 6 hours; 1 to 10 hours; every slot 2 to 6 hours; hourly 2 to 8 hours | same list | asserted |
| SF21 | the carryover shares | one pair per analyser, fitted on both treated ports together | a pair per channel; the unscaled form | same list | asserted |
| SF9 | the check shortfall | the quarter's nine readings' mean | a month's mean | same call | every month within 0.001 of the quarter (Holmedale 0.0080, Calderwood 0.0084 low) |
| SF10 | the two-point test | squared residuals under each form | a mean test; a weighted joint fit with the check; readings interpolated to the grab; carryover from the same-cycle raw fits | same list | asserted |
| SF11 | the zero error's size | the check's shortfall | the corrected grabs' mean shortfall; the two averaged | same list | asserted (HOL-FW1 within 0.003 of zero either way) |
| SF12 | a span error at the channel's level | the shortfall in proportion to the channel's mean reading | to its estimated level in the water | same list | asserted |
| SF13 | an offset's rounding | no offset is graded | a printed offset | not graded | the prompt asks for the channels; the chart's offsets are read at sight |
| SF14 | analysed more than 24 hours after collection (asks) | the analysis an hour after its stamp, against the collection time | the stamp as given; the stamp as UTC; only the stamps before reception moved | the asks only | the stamps run behind the laboratory's reception and release times: 16 rows are stamped up to 53 minutes before reception logged them and none is released within 64 minutes of its stamp, so every shift the records allow counts as the hour does (asserted); the dictionary gives the collection and reception times in New Zealand time and the release time likewise |
| SF15 | the filtered and final water samples (asks) | every treated sample of the quarter, October's under the old codes | raw samples too; the register's codes only | the asks only | the prompt; the laboratory's notice of 28 October |
| SF16 | a sample's quarter (asks) | collected in the quarter, the 28 December round included though analysed on 5 January | analysed in the quarter | the asks only | section 7(b) (the quarter's samples) |
| SF17 | the hours at the fixed dose (asks) | each gap between good filtered readings at the PLC, less the two-hour hold | the gap whole | the asks only | the process summary's dose control |
| SF18 | not available to the dose control (asks) | the slots no filtered reading reached the PLC (the analyser's faults, the filtered port's lost signal) and its check cycles | every F row; the historian's lost hours too; only the runs a check followed | the asks only | the process summary's dose control (no good filtered reading reaching the PLC) and telemetry (the PLC reads the analyser directly; the outstation keeps 72 hours and the historian fills failed polls from it); the dictionary (a filled slot's G row follows its F row; a slot with no row is the historian's own loss, the plants ran normally) |
| SF20 | the unfilled runs (asks) | a run of unfilled F rows at every port that no check followed was the telemetry's, the PLC reading its analyser throughout; a port's own unfilled F rows, the other ports read between them, are readings that never reached the PLC | any run no check followed the telemetry's; any run at every port the telemetry's | the asks only | the process summary (the historian polls the plant's outstation, which reads the PLC, and fills a failed poll from its store once the link is back; a fault stops the readings until a technician clears it) and the check procedure (the check after clearing any fault); asserted: every fault followed at once by the check, the outstation changes the only whole-plant runs with none, each plant's filtered port losing its signal once with the other ports read between |
| SF22 | a sample (asks) | a bottle: two rows with the same point, analysis stamp, result and release are one bottle logged twice | every row; one row per point and collection time; rows equal but for the number | the asks only | the 7 December round's second logging carries the courier docket's one pickup time for every bottle and shares each bottle's analysis stamp, result and release (one analysis cannot serve two bottles on a four-minute bench); no two treated rows share a point and collection time (asserted) |
| SF19 | a gap at the quarter's ends (asks) | within the quarter, New Zealand time | UTC | same figures | no fault within two days of either end (asserted) |

## Ladder

| Route | Flags | Count | Golden |
|---|---|---|---|
| The first port after raw only, the checks set aside (probe C2) | BRN-FW1, DUN-FW1, ELS-FW1, GAR-FI1, HOL-FI1 | 5 | no |
| The previous port only, the low checks as span errors | the six, HOL-FW1, and BRN-FI1, DUN-FI1, ELS-FI1 reading low | 10 | no |
| Two ports before, the checks set aside (probe A2's main list) | the six and HOL-FW1 | 7 | no |
| Two ports before, the low checks as span errors (the default path) | the six and HOL-FW1 | 7 | no |
| Two ports before, the two-point read with the raw ports as they read (Holmedale a span error) | the six and HOL-FW1 | 7 | no |
| Two ports before, the shortfall added to every channel as an offset | the six, CAL-FI1 and CAL-FW1 | 8 | no |
| Golden: two ports before, the two-point read with each raw port's carryover taken out | BRN-FW1, DUN-FW1, ELS-FW1, GAR-FI1, GAR-FW1, HOL-FI1 | 6 | yes |

HOL-FW1 leaves the list only with both moves: its carryover from the raw sample two ports back (about 0.009) is real, and
Holmedale's zero error (0.008 low) cancels it; Calderwood's channels stay off only if its shortfall is a span. On the
clean world (every slot read, nothing lost) the default path files the seven and the decisive step alone the six
(checks.py, dataset-generation 7.1).

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | the 16 treated channels | filed (register; WQ-DS-04 sections 2 and 4) |
| 2 | Unit of account | a channel, one analyser reading one sample point | filed (section 2) |
| 3 | Attribution window | the channel's readings held with code G in the quarter | filed (section 3) |
| 4 | As-of dating | the historian's export of the quarter; the laboratory's export of 14 January 2028 | filed |
| 5 | Version basis | WQ-DS-04 issue 3 | filed |
| 6 | Denominator | the channel's G readings | filed (section 3) |
| 7 | Weighting | each G reading once | filed (section 3) |
| 8 | Window length | the calendar quarter, New Zealand time | filed (section 1) |
| 9 | Boundary inclusivity | more than 0.005 | C1 (0.0022 clear, asserted) |
| 10 | Rounding path | no offset graded; sample counts whole; hours to one decimal | filed (the prompt) |
| 11 | Tie-break | none open | asserted |
| 12 | Maturity and censoring | treated results below 0.030; the 28 December round analysed on 5 January, inside the export | filed (section 6; the export) |
| 13 | Order of operations | carryover fitted, then the calibration error at the channel's level | C1 (asserted) |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | a reloaded slot's F row and G row: the G row is the reading | filed (section 3); asserted both ways for the call |
| 16 | Identity normalisation | sample points by the register's codes; October's treated samples through the laboratory's notice | filed |
| 17 | Netting against gross | none | not applicable |
| 18 | Dimensional units | mg/L as N throughout | filed |
| 19 | Code and status semantics | G, F and V (the dictionary); the below-limit results (section 6) | filed; never the stump |
| 20 | Integerisation | sample counts whole | filed |
| 21 | Clause scope | section 4 for every treated channel; section 7 items (b) and (c) for every plant | filed |
| 22 | Forward window contents | the flagged channels go on the technicians' list before the next quarter | filed (section 4) |

## Literal reader

Executing the prompt and every filed sentence word for word (WQ-DS-04 sections 1 to 7, the register, the dictionary,
the process summary) leaves one open move, how the ammonia actually in the water is estimated at each reading; the
data's structure forces it: the treated grabs are mostly below the 0.030 limit, so the water's level has to come from
the readings; a response at no lag to the two slots before is the analyser's own (the treated water answers the raw
water only after hours); and a check at one level cannot give an error's form, which the raw grabs settle only once
the raw port's own carryover from the ports ahead of it is taken out. Every licensed estimate files the same six
(asserted: the pooled and the per-channel mixing fits, five lag windows, the unscaled form, four two-point variants,
two zero-error sizes; margin 0.0022). The additive law, the shares of the readings before added on, is a rival the
raw grabs rule out.

## Oracles

- No file ranks the channels or states a channel's offset, flag or error form.
- The check workbook states readings and a pass against the 10 per cent band; every check passes.
- The laboratory export states results and times and no holding-time verdict.
- The process summary states the dose control and the telemetry; it names no fault, outage or gap.
- The notice maps the treated points' codes; it names no sample.
- No file lists the outstation changes, the lost signals or the second logging; the check procedure states the
  check after clearing a fault and the historian's check-port rows show where one was run.
- The dictionary names the laboratory analyser's run record and no clock for it; the reception and release times
  bracket it.
- The daily output and rainfall files (the distractors) carry no figure any route needs.

## Ask sheet

Ask A, return item (b): for each plant, how many of its filtered and final water samples the laboratory analysed more
than 24 hours after collection (8 figures). Ask B, return item (c): for each plant, the hours its chlorine dose ran at
the fixed dose because the filtered water reading was not available to the dose control (8 figures). Both are measures
each plant's channels carry that the call does not turn on (H18: an input's audit trail and a second measure per
channel). The call reads the G readings, the check readings and the laboratory's raw samples' collection times and
results; ask A reads the treated samples' analysis, reception and release stamps, ask B where the filtered port has no
reading at the plant, the F rows and the rows that are missing (separation asserted: the call is unchanged with no
failed polls, no lost hours, no outstation changes and no lost signals).

Devices, silent (no filed sentence points at any of them):
- Ask A, the clock: the laboratory analyser's run record keeps New Zealand standard time all year, an hour behind the
  collection, reception and release times, and no file says so (the dictionary names the run record and no clock). The
  records fix it: 16 rows are stamped up to 53 minutes before reception logged their bottles (the morning the analyst
  ran ammonia as the bins came in) and no result is released within 64 minutes of its stamp, so every shift the
  records allow lies between 53 and 64 minutes, and the bench is set so no treated sample sits within ten minutes of
  24 hours: every shift in that range counts as the hour does. The stamps as given miss every plant (one, three or
  more samples a plant between 24 hours 10 minutes and 25 hours, never two).
- Ask A, the second logging: reception logged the delayed 7 December round's 16 treated bottles a second time when the
  bins were unpacked, keying from the courier's docket rather than the labels, so the second rows carry the docket's
  one pickup time as the collection time, new sample numbers and a reception 25 minutes later, with the bottle's one
  analysis stamp, result and release. One row per point and collection time (the round 3 readers' rule) keeps both
  loggings and adds two late samples at every plant; only the same point, analysis stamp and result is one bottle.
  The clock never moves a plant by two, so missing both never nets back to the golden.
- Ask B, the lost signals: each plant's filtered water port lost its signal to the PLC once (a wet junction box or a
  failed loop isolator, cleared by the electrician; three final water ports did too), 4 to 9 hours: F rows at that
  port only, the other ports read between them and nothing filled, and no check after (the analyser was never
  touched). No reading reached the PLC, so the dose ran fixed beyond the hold. The round 3 readers' rule (a run a
  check followed is the analyser's, any other the telemetry's) reads these as the telemetry's and misses every plant
  by 3 hours or more; the whole-plant rule alone (a run at every port is the telemetry's) reads the reagent and cell
  faults as the telemetry's and misses every plant too. Only a run at every port with no check after it was the
  telemetry's (the November outstation changes, now a hazard).
Hazards: on ask A, October's treated samples under the old codes (the notice), the 28 December round analysed on 5
January, two courier breakdowns, the raw samples out of scope; on ask B, the outstation changes, the failed polls
filled from the outstation (an F row with a G row beneath), the historian's own lost night of 17 November (no rows at
all, stated in the dictionary), the check cycles inside the hold, the two-hour hold, the quarter in New Zealand time.

| Path (from generator/pair.py) | Ask A | Ask B | Keeps |
| --- | --- | --- | --- |
| the analyser's stamps as given (rounds 1 and 2, three of four readers) | 0 of 8 | | 0 |
| stamps as given, one row per point and collection time | 0 of 8 | | 0 |
| stamps before reception moved to reception, the rest as given | 0 of 8 | | 0 |
| stamps as given, raw samples included | 2 of 8 | | 2 |
| stamps as given, the register's codes only | 0 of 8 | | 0 |
| stamps read as UTC | 0 of 8 | | 0 |
| the hour added, raw samples included | 0 of 8 | | 0 |
| the hour added, the register's codes only | 0 of 8 | | 0 |
| the hour added, every row a sample | 0 of 8 | | 0 |
| the hour added, one row per point and collection time (round 3, both readers) | 0 of 8 | | 0 |
| the hour added, rows equal but for the number dropped | 0 of 8 | | 0 |
| unfilled runs a check followed the analyser's faults, the rest the telemetry's (round 3, both readers) | | 0 of 8 | 0 |
| unfilled runs at every port the telemetry's, checks aside | | 0 of 8 | 0 |
| F rows with nothing filled back as the analyser's faults (rounds 1 and 2, all four readers) | | 0 of 8 | 0 |
| gaps in the historian's G rows, two-hour hold | | 0 of 8 | 0 |
| every F row a gap, the lost hours not, two-hour hold | | 0 of 8 | 0 |
| the PLC's gaps summed whole, no hold | | 0 of 8 | 0 |

| Ask | Cracker (the call landed, the best path that misses the device) | Verdict |
| --- | --- | --- |
| A samples analysed late | 0 to 2 of 8 (the stamps as given; with raw samples wrongly counted two plants net back) | miss |
| B hours at the fixed dose | 0 of 8 (the round 3 readers' check rule) | miss |

Pair ceiling: 35.4 ((51.9 + 18.9) / 2), the cracker keeping 2 of the 16 ask figures on the call and the mirror the same.
Mirror leakage: 12.5 per cent of ask weight.
Measured by: generator/pair.py on the cut pack (target.zip f52cad28). Round 3 (db101482) measured the readers' own
paths: both took the hour from the dictionary and one row per point and collection time (0 of 8 on ask A, a fork the
judge returned), and both took ask B by the check rule (8 of 8). The clock is no longer filed, the duplicate bottles
are gone, and ask B rests on the lost signals; the round 4 readers on this pack are the measurement.

## Pre-ship check (written for the round 4 pack; the build did not ship)

- Free gates (stage 3, re-run on the final pack): generator checks 98 passed (the golden list against the world's
  truth, every licensed estimate filing the six with the listed 0.0022 or more from the line, the additive law ruled
  out by the worn analysers' raw ports reading their grabs low, the zero and span forms read from the raw grabs with
  the raw port's own carryover out, SF1 to SF23, the analyst test on the clean truth, R1 to R3, the separation line
  with no failed polls, lost hours, outstation changes or lost signals, the asks against the world with every natural
  path missing every plant, the clock bracket 53 to 64 minutes with every shift inside it counting as the hour, the
  input gates); verify.py 0 failures; two builds byte-identical (target.zip f52cad28); figures_check 28 of 28; precut
  51 of 51; voice-check PASS.
- leak.py REVIEW, no LEAK: WQ-DS-04 carries the call's words (its own estimand and the return), and WQ-DS-04, the
  dictionary and the process summary carry the field's terms (analyser, readings, Holmedale, Calderwood); none names
  carryover, a zero error, a span error, the sequencer's memory, a clock or a lost signal.
- guard heart WARN (people.first Caleb, answered in the Draw); surface promotes task251, task250, task254, task202 and
  task243, each differentiated on the card; people Emily Butler and Suzanne Nelson in the pack, as drawn.
- Containers clean (no producer signature, no out-of-band timestamp) in target/ and golden/.
- Golden realism: the workbook leads with the six as its title, lists them with plant, water, analyser and direction,
  carries every channel's carryover, calibration and offset, the analysers sheet with the pooled shares and the
  error's form, the return's two items by plant, and a notes sheet stating the estimand, the carryover, the
  calibration, and how each item was counted; the chart shows every channel's offset by plant against the 0.005 band,
  the six marked.
- Stage 4 round 4 judge (target.zip f52cad28): DETERMINISTIC, APPROVE; Gate G method_or_model_selection,
  analytical_non_defect, no surface read, no sole data defect; Gate H domain, layers and decisive step pass; one watch
  item (the analysis stamps' clock, closed by the reception and release bracket, asks only).
- The 10/10 rules re-read against the built pack: the decisive step is the analyser's carryover and the form of its
  calibration error estimated from the readings, the checks and the raw grabs, which no filed sentence performs; every
  Layer 1 item mishandled leaves the call unchanged (asserted: the check port's rows, October's old codes, the failed
  polls, the lost night, the outstation changes, the lost signals).

## Candidates for architecture 2

Round 4 measured the ceiling of this decisive step: reader H fitted each analyser's carryover from both slots before,
checked it against the raw grabs, read Holmedale's error as a zero shift and Calderwood's as a span error from the
raw pairs, and filed the six; reader G fitted the slot before only and filed HOL-FW1 for GAR-FW1. A measurement model
whose every term the readings and the grabs identify is solved by a careful reader once in eight, which the
two-reader rule counts as spent. The next architecture keeps the world only if its decisive step is not a richer fit
to the same data:
- A second view the fit cannot supply: the deciding quantity identified only through a structure in how the grabs or
  the checks were taken (which samples exist and why), so a reader who fits the readings perfectly still files the
  wrong list. Screen before drawing: the selection must be data-native and fixed by the records, never a planted rule.
- A new world for the seed's quantity (low-level channels near a detection limit), drawn fresh at stage 1 with call-only
  probes before any build, the ask layer's shape kept: the analyser clock bracketed by reception and release, and a
  port's lost signal at the PLC, held 0 of 16 for reader G and 8 of 16 for reader H (the signal faults read as the
  analyser's own lost readings).
- Whatever is drawn names, at the draw, the step a careful reader with a full carryover model still gets wrong; a
  design whose answer that reader files is dead before the generator.

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
- Carryover plus a zero-water blank at Elstow (worn) and Holmedale (healthy), checks 7 per cent low (probe pack probe5,
  seed 128 of cw5): 0 of 3 landed, but Elstow's blank is not determinate under its own raw carryover at its low raw
  level (one probe read it as a span error, slope 0.91, from its raw port). Moved the blank to a healthy analyser and
  gave a second healthy analyser a span error with the same check shortfall.
- Carryover plus a zero error at healthy Holmedale and a span error at healthy Calderwood, both checks about 9 per cent
  low (probe pack probe9, seed 59 of cw9): 1 of 3 landed. A compared each raw port with the raw grabs, storm samples
  above 1 mg/l included, read Holmedale as a zero error and Calderwood as a span error and filed the six; B read both
  checks as span errors; C compared the raw ports too but called both span. At about one in three the portal's top two
  land together too often, so Holmedale was made worn as well, with high raw water: its raw port then reads low in
  proportion through its own carryover, about as much as its check, and only a reader who takes that carryover out
  first sees the constant zero error, which now cancels the final water channel's memory carryover (probe pack
  probe11, seed 45 of cw11: 0 of 3).
- Stage 4 round 1 (target.zip c2a2789e): both scored readers filed the default path's seven and missed ask A (the
  stamps as given), but took all of ask B, reading the filled polls and the lost night as the historian's by the
  process summary's PLC sentence; the judge found ask A's hour fixed only by outside knowledge (the eleven early stamps
  give a 42-minute floor) and step 2's wording executable as an additive carryover that puts DUN-FI1 on the line. Kept
  ask A's clock and pinned it by the notice's run times; re-sited ask B onto the November outstation changes; rewrote
  the carryover as a mix with one pair of shares per analyser (the golden pools them; the per-channel fit stays a
  licensed variant, the additive law a rival the raw grabs rule out).
- Stage 4 round 2 (target.zip 9251d6a1): readers C and D both filed five channels (the port after raw only) and so
  missed the call; C took all 16 ask figures by the notice's stated run times for one round and the register's list of
  outstation changes, D took ask B by the list. The judge accepted the call and ask B and held ask A open: one round's
  pin does not fix the other nine. Explicit lists are read: the clock is now filed in the dictionary (a hazard), ask A's
  device is the bottle (duplicate bottles beside a round logged twice), and ask B's changes are found only by the
  missing post-repair check. The listed channels' printed bound is 0.007 (the judge's tightest fit put ELS-FW1 at
  0.0080).
- Stage 4 round 3 (target.zip db101482): readers E and F missed the call (E filed five, F the default seven) and both
  kept all of ask B by the check rule (a run a check followed is the analyser's fault, any other the telemetry's) and
  none of ask A (one row per point and collection time dropped the duplicate bottles); the judge returned ask A as a
  fork, a weekly pair being a second bottle or a repeat analysis of one, which no file decides. The duplicate bottles
  are gone, ask A's primary is the analyser's clock again with nothing filed and the reception and release stamps
  bracketing it, the 7 December second logging carries the docket's pickup time, and ask B's primary is each filtered
  port's lost signal, which the check rule reads as the telemetry's.
- Stage 4 round 4 (target.zip f52cad28): reader H landed the call (carryover from both slots before fitted per
  analyser, Holmedale's zero shift and Calderwood's span error read from the raw pairs) and all 8 of ask B (a port's
  own unfilled F rows read as the analyser producing no reading), none of ask A (the stamps as given, the second
  logging counted); reader G fitted the slot before only and filed HOL-FW1 in place of GAR-FW1, 0 of 16 ask figures;
  the judge returned DETERMINISTIC APPROVE. A call any reader lands is spent: architecture 1 is spent at stage 4.

# task252 design note

## Draw

Card `cards/task252.json` (architecture 2; architecture 1 in its lineage, spent at stage 4 round 4). Guard verdict
WARN after one redraw of the structural axes: the draft's gap population with G9 first repeated a spent signature in
five builds (`test.same_driver_older`) and two puzzles (`test.same_puzzle_older`), so the gap is objective (the checks
and the grabs are correct, and the return is scored on the water at the sample point, upstream of where the check
enters) and Gate G decomposition_attribution (the rise after each flush is a correctly recorded movement assigned to
its driver). The two WARNs are answered: `driver.near` 0.16 against the slot's own lineage (differentiated on the
card), and the first name Caleb in task196, an older build (the draw's own persona, kept from architecture 1). Nearest
other drivers task251 v1 (0.09, a reference cylinder's loss read at cylinder changes, differentiated: here the
references are sound and blind to the loss by where they enter) and task230 v3 (0.06). `guard.py slots` and a search of
every note find no sample-line loss, biofilm or nitrification mechanism on file.

- **Pairing.** Physical & Environmental Sciences / sensor-calibration-measurement, drawn for Data Quality Monitoring &
  Alerting, as architecture 1. The object is the health of a district council's online ammonia monitoring, and the call
  is a monitoring decision: which treated-water channels the fourth-quarter 2027 online monitoring return flags as
  reading more than 0.005 mg/l as N off the water at their sample points.
- **Why a new architecture.** Architecture 1's decisive step (each analyser's carryover from the two samples before and
  the zero or span form of its calibration error, read from the checks and the raw grabs) was solved by one careful
  reader in eight: every term of that model is identified by the readings, the checks and the grabs. The step that
  decides here survives a perfect fit to all three, because it sits upstream of every reference: the ammonia each
  filtered sample line takes before the cell.
- **The seed, re-found.** DQ25 gave the world (low-level channels whose laboratory grabs sit under the detection limit),
  the decision (the channels escalated this quarter) and the quantity (each channel's error at its own low level against
  a tolerance). The censored grabs are why the line's loss stays hidden: at a filtered line whose water sits above the
  limit, the grabs would show it.
- **Probes before the draw.** Call-only rounds, isolated readers (Sonnet, medium), on packs cut from the prototype. Pack
  1, the loss on Brannock's and Elstow's filtered lines (grabs above the limit): probes A, B and C flagged both straight
  from the lab pairs. Pack 2, the loss on Calderwood's and Holmedale's (grabs all censored): probes D and F filed the
  default list or the one-slot list and never read the flushes; probe E returned nothing. See Tried and rejected.
- **Niche.** Fernvale District Council (fictional, New Zealand) runs eight water treatment plants on river intakes:
  Ashcombe, Brannock, Calderwood, Dunmere, Elstow, Fenwick, Garrick and Holmedale. Each has one colorimetric ammonia
  analyser with a three-stream sequencer: each sample point's water comes in its own sample line, and the sequencer
  passes raw, filtered and final water in turn through one measuring cell, ten minutes a port, in the register's port
  order. Readings go to the historian; each analyser is checked monthly on a 0.100 mg/l as N standard through its check
  port (three readings, 10 per cent tolerance); the contract laboratory takes weekly grabs at the taps of all 24 sample
  points (detection limit 0.030); the instrument technicians flush every sample line with dilute hypochlorite on a
  monthly planned visit, logged in the register. Architecture 1's analyser faults stand as the lower rungs: five worn
  analysers carry part of the two samples before each reading, Holmedale's zero water reads 0.0085 low, Calderwood's
  reagent reads about 9 per cent low. New here: the filtered water is unchlorinated, and the filtered sample lines at
  Calderwood and Holmedale carry a nitrifying biofilm that takes about two thirds and nearly all of the filtered water's
  ammonia when grown; each monthly flush clears it and it grows back over about two days. The final water lines carry
  chlorinated water and stay clean; the raw lines are short.
- **The call.** Which of the 16 treated-water channels are beyond 0.005 for the fourth quarter of 2027, if any.
- **Shape.** 07: the 16 channels, eight plants by two waters, each in or out; the chart of every channel's offset
  against the band with the flagged channels marked; the asks' figures. No channel's offset is a graded figure (the
  licensed estimates differ by up to 0.006 on a fouled channel); the list, and the margin every licensed estimate keeps,
  are.
- **Strategy.** `decomposition_attribution`: each channel's offset is split into the sequencer's carryover, the
  analyser's calibration error and the sample line's loss, and the loss is attributed from the readings' recovery after
  each line flush. Gate G decomposition_attribution; generators G9 (what reaches the cell against what was in the water
  at the sample point), G4 (read at each flush), G16, G17; gap objective, population; calibration physical_verification;
  context artifact monitoring_export; Layer 2 field_method, pattern own:sample-line-loss-read-from-the-recovery-after-
  each-line-flush.
- **Forum, event, organisation.** operations_desk, period_close (the quarter's return), local_government. Role
  compliance_or_audit (the water quality compliance officer answers for the return).
- **People** (`guard.py names --geo NZ --seed 252`, locale en_NZ, kept from architecture 1): Emily Butler, the water
  quality compliance officer, who asks; Cameron Waugh and Caleb MacDonald, the instrument and controls technicians who
  run the checks and the planned visits; Suzanne Nelson, the contract laboratory's client services coordinator. None
  appears in the prompt.
- **Data-native sentence.** Filtered water reaches each analyser through its own unchlorinated sample line, where a
  nitrifying film grows and takes part of the ammonia before the cell; the check standard enters at the check port after
  the line and the laboratory's grab comes from the tap before it and reads below its limit, so neither sees the loss,
  and it shows only in the channel's own readings, which jump at every monthly line flush and fall back as the film
  grows again.

## Default path

1. Read WQ-DS-04 (a treated channel's quarter offset, the mean over its G readings of the reading less the ammonia in
   the water at its sample point, flagged beyond 0.005 either way), the register (port orders, ten-minute ports) and
   the process summary (one measuring cell, the transit times).
2. See that the treated grabs are mostly under the 0.030 limit, so the offsets have to come from the readings.
3. Fit each analyser's carryover from the two slots before each reading, apart from the treated water's own lagged
   response to the raw water: about 7 per cent of the slot before and 2 per cent of the one before that at five
   analysers.
4. Read the checks against the raw grabs, the raw port's own carryover taken out: Holmedale's shortfall is a zero error,
   Calderwood's a span error worth about 0.002 at treated levels.
5. Take the passing checks and the censored treated grabs as showing nothing more, and flag the channels whose
   carryover and calibration error together are beyond 0.005.

Ends on: BRN-FW1, DUN-FW1, ELS-FW1, GAR-FI1, GAR-FW1 and HOL-FI1
Golden: BRN-FW1, CAL-FI1, DUN-FW1, ELS-FW1, GAR-FI1 and GAR-FW1

## Stump sentence

A competent solver fits each analyser's carryover from both slots before, reads Holmedale's check shortfall as a zero
error and Calderwood's as a span error from the raw pairs, and flags BRN-FW1, DUN-FW1, ELS-FW1, GAR-FI1, GAR-FW1 and
HOL-FI1, leaving CAL-FI1 at about +0.001; the filtered sample lines at Calderwood and Holmedale lose ammonia to a
biofilm that each monthly line flush clears, which no check (it enters after the line) and no grab (below the limit)
sees, and which the readings' recovery after the flushes measures: with it HOL-FI1's carryover is cancelled and it sits
inside the band, while CAL-FI1 reads about 0.010 low, so the list swaps HOL-FI1 for CAL-FI1.

## Three rules

Task type: sensor-calibration-measurement (Physical & Environmental Sciences), tagged in the taxonomy for Data Quality Monitoring: each online channel's quarter error against the water at its sample point, split into the sequencer's carryover, the analyser's two-point calibration and the sample line's own loss, the last read from the response to the line's cleaning.
Domain test: The deciding quantity is each treated channel's mean offset from the ammonia in the water at its sample point, and what decides it here is the ammonia each filtered sample line consumes before the cell, which the instrument field reads from the readings' response to cleaning the line (an unchlorinated line grows a nitrifying film that a hypochlorite flush clears and that grows back over days, while a chlorinated final water line stays clean), set beside the sequencer's carryover and the two-point calibration; replacing it with the checks and the grabs, which enter after the line or sit below the limit, changes the list.
Swap: "the channels more than 0.005 off once each sample line's loss, read from the readings' recovery after each monthly line flush, is added to the carryover and the calibration error" put into a hospital's ward glucose meters loses its mechanism, since no meter draws its blood through a line that a biofilm colonises between cleanings, no cleaning log resets a loss in the meter's readings, and no reference standard enters the meter downstream of where the loss happens; a grid's meters have no line at all.
Layer 1: the historian's readings export stamped in UTC against the laboratory's sample times and the planned maintenance log in New Zealand daylight time; the check-port readings inside the readings stream under quality code V and the fault slots under F; treated-water results below the 0.030 limit; the laboratory's own sample point codes, recoded on 1 November; the register's port sequence history; the analysis stamps on standard time; the delayed 7 December round logged twice; failed polls filled from the outstation, the November outstation changes unfilled, each filtered port's lost signal; two storm nights that tripped each analyser's supply once, its sequence starting again at the raw water port. Nothing is placed to be caught.
Layer 2: field_method under decomposition_attribution: each channel's offset is the carryover (the zero-lag response to the two slots before, apart from the treated water's lagged response), the calibration error at the channel's level (zero or span, read from two levels), and the sample line's loss, a share of the water that the line's biofilm takes as it grows back after each flush, fitted on the time since the flush and averaged over the quarter.
Decisive step: reading the ammonia the filtered sample lines take before the cell from the readings' recovery after each monthly line flush in the register's planned maintenance log (the readings, carryover and calibration taken out, rise at the flush and fall back as a share that grows with the days since it), and adding its quarter mean to each channel's offset, rather than taking the passing checks and the censored grabs as showing that nothing upstream of the cell is wrong.
Not semantics: every field reads as what it is (the reading at the sample point, the check standard's readings through the check port, the laboratory's result and limit, the maintenance visit's time and the work done), and no field, code, unit or definition says that a line loses ammonia, that a flush changes a reading, or by how much; the planned maintenance log records visits and the work done, no effect.
Not rule application: WQ-DS-04 defines the offset against the water at the sample point and the 0.005 band and says nothing on how that water is estimated; no rule names carryover, a zero or a span error, a sample line's loss, a biofilm or a flush's effect, so executing every filed rule files no offset at all, and every filed procedure (the checks, the grabs) sees the cell or the tap, not the line.
Analyst test: A strong analyst who reads every file correctly, fits each analyser's carryover from both slots before, reads Holmedale's check shortfall as a zero error and Calderwood's as a span error from the raw pairs, and takes the passing checks and the censored treated grabs as showing nothing more flags BRN-FW1, DUN-FW1, ELS-FW1, GAR-FI1, GAR-FW1 and HOL-FI1; the same analyst who also reads each filtered line's recovery after the monthly flushes files the golden (checks.py runs both on the clean world and on the pack).
Estimand: each of the 16 treated-water channels' offset for the fourth quarter of 2027 (New Zealand time), the mean over the readings it reported with quality code G in the quarter of the reading less the ammonia in the water at its sample point at that time, in mg/l as N; flagged when more than 0.005 either way (WQ-DS-04 sections 3 and 4 and the prompt).
No decoy: nothing is planted: the readings are what the analysers reported, the checks what they read on the standard, the grabs the laboratory's results, the maintenance log the technicians' visits; the biofilm is a fault of the monitoring being reviewed, shown only by the data; no memo, draft or figure argues for any list, and no file ranks the channels by offset or names a line loss.
No certified replay: no certified or published figure sits in the pack; the check workbook states readings and a pass, the laboratory file results, the maintenance log visits, and no file states a channel's offset, flag or loss.
Lesson: a reference that enters a measuring system part-way along measures only the part after it; an error arising upstream of every reference is invisible to them all however well they agree, and is read from the system's own response to an intervention that resets it, here the readings' recovery after each line flush; no shipped build reads an error upstream of its references from the response to a maintenance reset.

## Readability screen

| Rung | Where a reader meets it | Verdict |
|---|---|---|
| 1. Carryover into the port read straight after raw water only, the checks set aside (BRN-FW1, DUN-FW1, ELS-FW1, GAR-FI1, HOL-FI1) | the register's port sequences and the process summary's one measuring cell; the zero-lag response to the raw reading is plain in every worn analyser's record | readable |
| 2. Carryover from the two slots before (adds GAR-FW1) | nothing names a second sample's share; the reading two slots back carries it at no lag, large at Garrick and Holmedale | silent |
| 3. The low checks read as span errors (adds HOL-FW1) | the check workbook; both analysers' raw ports read low in proportion against the raw grabs | readable |
| 4. Holmedale's zero error read from the raw grabs once the raw port's own carryover is out (drops HOL-FW1: the default path's six) | nothing names it; architecture 1's decisive step, landed by one reader in eight | silent |
| 5. (decisive) The filtered sample lines' loss read from the readings' recovery after each monthly line flush (swaps HOL-FI1 for CAL-FI1: the golden) | nothing names a line loss, a biofilm or a flush's effect; the planned maintenance log records the visits and the work done, and the checks pass | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the channels | the 16 filtered and final water sample points | the raw water points too | another list only if raw is counted | the prompt; WQ-DS-04 section 4 (treated water channels) |
| SF2 | the fourth quarter of 2027 | 1 October to 31 December, New Zealand time | UTC dates | same call | WQ-DS-04 section 1; asserted |
| SF3 | the readings | the channel's rows held with quality G, a reloaded slot's G row included | a reloaded slot's F row kept and its G row dropped | same call | section 3 (readings held with code G); asserted |
| SF4 | the ammonia actually in the water | the water at the sample point at each reading's time, before the sample line | the water as it reaches the measuring cell; the laboratory's treated grabs | another list (the cell's water drops the line's loss); no quarter mean (most grabs below 0.030) | section 3 (the water at its sample point); the register's sample points (the taps) and the process summary (each point's own sample line to the analyser); section 6 (the limit) |
| SF5 | more than 0.005 | strictly | at or beyond | same call | every licensed estimate 0.0019 or more from the line (asserted, 24 estimates) |
| SF6 | above or below | either sign | above only | another list (CAL-FI1 reads low) | the prompt ("above or below"); section 4 |
| SF7 | the carryover's form | a mix in the cell: each reading 1 - k1 - k2 of its own water, k1 and k2 of the two samples before | the shares of the readings before added on (the additive law) | same list or another (asserted) | the worn analysers' raw ports read their raw grabs low by 0.010 to 0.039, as a mix does and an added carryover cannot (asserted) |
| SF8 | the treated water's own response | the raw readings 2 to 8 hours earlier | 1.5 to 6 hours; 1 to 10 hours | same list | asserted |
| SF21 | the carryover shares | one pair per analyser, fitted on both treated ports together | a pair per channel; the same-cycle raw reading | same list | asserted |
| SF9 | the check shortfall | the quarter's nine readings' mean | a month's mean | same call | every month within 0.001 of the quarter (asserted) |
| SF10 | the two-point test | squared residuals under each form | a mean test; readings interpolated to the grab | same list | asserted |
| SF11 | the zero error's size | the check's shortfall | the corrected grabs' mean shortfall | same list | asserted |
| SF12 | a span error at the channel's level | the shortfall in proportion to the channel's mean reading | to its estimated level in the water | same list | asserted |
| SF24 | the line's loss | a share of the water that grows back as one less an exponential in the days since the last flush, fitted with the raw water's lagged response | a straight-line regrowth to a plateau; the clean level as the mean of the first 1 to 24 hours after each flush; the fit on the readings uncorrected | same list | asserted: every form files the six, HOL-FI1 between -0.0031 and +0.0029, CAL-FI1 between -0.0107 and -0.0073 |
| SF25 | which channels lose ammonia in the line | the two whose readings rise after every flush of the quarter (CAL-FI1 and HOL-FI1) | the fitted loss applied to every channel | same list | asserted: every other channel's fitted loss moves it by 0.002 or less and its steps change sign between flushes |
| SF26 | the flush's moment | the visit time in the planned maintenance log, New Zealand time | the time read as UTC | same list | the log's column ("Visit (NZ time)"); asserted |
| SF27 | the loss in the quarter's offset | the mean over the channel's G readings of the loss at each reading's days since the flush | the grown loss over the whole quarter | same list | asserted |
| SF13 | an offset's rounding | no offset is graded | a printed offset | not graded | the prompt asks for the channels; the chart's offsets are read at sight |
| SF14 | analysed more than 24 hours after collection (asks) | the analysis an hour after its stamp, against the collection time | the stamp as given; the stamp as UTC; only the stamps before reception moved | the asks only | the stamps run behind the laboratory's reception and release times: every shift the records allow (53 to 64 minutes) counts as the hour does (asserted) |
| SF15 | the filtered and final water samples (asks) | every treated sample of the quarter, October's under the old codes | raw samples too; the register's codes only | the asks only | the prompt; the laboratory's notice |
| SF16 | a sample's quarter (asks) | collected in the quarter, the 28 December round included though analysed on 5 January | analysed in the quarter | the asks only | section 7(b) (the quarter's samples) |
| SF22 | a sample (asks) | a bottle: two rows with the same point, analysis stamp, result and release are one bottle logged twice | every row; one row per point and collection time | the asks only | the 7 December second logging carries the courier docket's one pickup time and shares each bottle's analysis, result and release; no two treated rows share a point and collection time (asserted) |
| SF17 | the hours at the fixed dose (asks) | each gap between good filtered readings at the PLC, less the two-hour hold | the gap whole | the asks only | the process summary's dose control |
| SF18 | not available to the dose control (asks) | the slots no filtered reading reached the PLC (the analyser's faults, its storm-night stops, the filtered port's lost signal) and its check cycles | every F row; the historian's lost hours too | the asks only | the process summary's dose control and telemetry (the PLC reads the analyser directly; the outstation keeps 72 hours and the historian fills failed polls from it); the dictionary |
| SF20 | the unfilled runs (asks) | a run of unfilled F rows at every port, no check after it and the analyser's port sequence running on unbroken across it was the telemetry's; a port's own unfilled F rows, the other ports read between, never reached the PLC | any run no check followed the telemetry's; any run at every port the telemetry's | the asks only | the process summary (the historian polls the outstation, which reads the PLC; a fault stops the readings until a technician clears it) and the check procedure; asserted: every fault followed at once by the check, each filtered port's lost signal once with the other ports read between |
| SF28 | a run after which the sequence starts again (asks) | the analyser stopped: its port sequence starts again at the raw water port, at slots the running sequence would not have reached, so it had been switched off and the PLC had no reading | the telemetry's, as a run with no check after it | the asks only | the register's port sequence and the readings' own sample points (a running sequencer keeps its order and its slots); asserted: each analyser's sequence restarts once, straight after its storm-night run, and nowhere else |
| SF19 | a gap at the quarter's ends (asks) | within the quarter, New Zealand time | UTC | same figures | no fault within two days of either end (asserted) |

## Ladder

| Route | Flags | Count | Golden |
|---|---|---|---|
| The first port after raw only, the checks set aside, no line | BRN-FW1, DUN-FW1, ELS-FW1, GAR-FI1, HOL-FI1 | 5 | no |
| The previous slot only, the low checks as span errors, no line | the default six, BRN-FI1, DUN-FI1, ELS-FI1 reading low | 9 | no |
| Two slots before, both low checks as span errors, no line | the default six and HOL-FW1 | 7 | no |
| Two slots before, the shortfall added to every channel as an offset, no line | the golden six, CAL-FW1 and HOL-FI1 | 8 | no |
| Two slots before, the two-point read with each raw port's carryover out, no line (the default path) | BRN-FW1, DUN-FW1, ELS-FW1, GAR-FI1, GAR-FW1, HOL-FI1 | 6 | no |
| The line's loss read, the previous slot only | the golden six, BRN-FI1, DUN-FI1, ELS-FI1, HOL-FW1 | 10 | no |
| The line's loss read, Holmedale's shortfall a span error | the golden six and HOL-FW1 | 7 | no |
| The line's loss read, the checks set aside | the golden six, HOL-FI1 and HOL-FW1 | 8 | no |
| Golden: two slots before, the two-point read, the line's loss from the recovery after each flush | BRN-FW1, CAL-FI1, DUN-FW1, ELS-FW1, GAR-FI1, GAR-FW1 | 6 | yes |

Three moves together file the six: the carryover from both slots before (GAR-FW1), Holmedale's zero error (keeps
HOL-FW1 off), and the filtered lines' loss (CAL-FI1 on, HOL-FI1 off). On the clean world (every slot read, nothing
lost, no trips) the default path files its six and the decisive step alone the golden (checks.py, dataset-generation
7.1).

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | the 16 treated channels | filed (register; WQ-DS-04 sections 2 and 4) |
| 2 | Unit of account | a channel, one analyser reading one sample point | filed (section 2) |
| 3 | Attribution window | the channel's readings held with code G in the quarter | filed (section 3) |
| 4 | As-of dating | the historian's export of the quarter; the laboratory's export of 14 January 2028; the register as saved in January | filed |
| 5 | Version basis | WQ-DS-04 issue 3 | filed |
| 6 | Denominator | the channel's G readings | filed (section 3) |
| 7 | Weighting | each G reading once | filed (section 3) |
| 8 | Window length | the calendar quarter, New Zealand time | filed (section 1) |
| 9 | Boundary inclusivity | more than 0.005 | C1 (0.0019 clear, asserted) |
| 10 | Rounding path | no offset graded; sample counts whole; hours to one decimal | filed (the prompt) |
| 11 | Tie-break | none open | asserted |
| 12 | Maturity and censoring | treated results below 0.030; the 28 December round analysed on 5 January, inside the export | filed (section 6; the export) |
| 13 | Order of operations | carryover and calibration taken out reading by reading, then the line's recovery fitted, then each channel's mean | C1 (asserted) |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | a reloaded slot's F row and G row: the G row is the reading | filed (section 3); asserted both ways for the call |
| 16 | Identity normalisation | sample points by the register's codes and the readings' own labels; October's treated samples through the notice | filed |
| 17 | Netting against gross | none | not applicable |
| 18 | Dimensional units | mg/L as N throughout | filed |
| 19 | Code and status semantics | G, F and V (the dictionary); the below-limit results (section 6) | filed; never the stump |
| 20 | Integerisation | sample counts whole | filed |
| 21 | Clause scope | section 4 for every treated channel; section 7 items (b) and (c) for every plant | filed |
| 22 | Forward window contents | the flagged channels go on the technicians' list before the next quarter | filed (section 4) |

## Literal reader

Executing the prompt and every filed sentence word for word (WQ-DS-04 sections 1 to 7, the register with its planned
maintenance log, the dictionary, the process summary) leaves one open move, how the ammonia in the water at each sample
point is estimated, and the data's structure forces it: the treated grabs are mostly below the 0.030 limit, so the
water's level comes from the readings; a response at no lag to the two slots before is the analyser's own; a check at
one level cannot give an error's form, which the raw grabs settle once the raw port's own carryover is out; and the
filtered readings at Calderwood and Holmedale rise at every logged line flush and fall back over two days while no
other channel moves, so the line takes ammonia between the tap and the cell, and the reading straight after a flush is
the clean line's. Every licensed estimate files the same six (asserted: the pooled and per-channel mixing fits, two lag
windows, the exponential and straight-line regrowth, the clean level from the first 1 to 24 hours after each flush, the
fit on the readings uncorrected, the loss applied to every channel or at full growth all quarter; margin 0.0019
over 24 estimates). The mix without its one-less-both-shares scaling is an algebra slip, not an estimate: a reading that
is 1 - k1 - k2 of its own water and k1 and k2 of the two before differs from its water by the shares of the differences
divided by 1 - k1 - k2, which the golden's step states.

## Oracles

- No file ranks the channels or states a channel's offset, flag, error form or loss.
- The check workbook states readings and a pass against the 10 per cent band; every check passes.
- The planned maintenance log states each visit's time, the work done and who did it; it names no effect on a reading.
- The laboratory export states results and times and no holding-time verdict.
- The process summary states the dose control and the telemetry; it names no fault, outage, trip or gap.
- The notice maps the treated points' codes; it names no sample.
- No file lists the outstation changes, the lost signals, the storm-night trips or the second logging; the check
  procedure states the check after clearing a fault and the historian's check-port rows show where one was run.
- The dictionary names the laboratory analyser's run record and no clock for it; the reception and release times
  bracket it.
- The daily output and rainfall files (the distractors) carry no figure any route needs; the rainfall shows the two
  storm nights as wet days among others.

## Ask sheet

Ask A, return item (b): for each plant, how many of its filtered and final water samples the laboratory analysed more
than 24 hours after collection (8 figures). Ask B, return item (c): for each plant, the hours its chlorine dose ran at
the fixed dose because the filtered water reading was not available to the dose control (8 figures). Both are measures
each plant's channels carry that the call does not turn on (H18: an input's audit trail and a second measure per
plant). The call reads the G readings, the check readings, the laboratory's raw samples and the planned maintenance
log; ask A reads the treated samples' analysis, reception and release stamps, ask B where the filtered port had no
reading at the PLC: the F rows, the rows that are missing and the sequence's restarts (separation asserted: the call is
unchanged with no failed polls, no lost hours, no outstation changes, no lost signals and no trips).

Devices, silent (no filed sentence points at any of them):
- Ask A, the clock: the laboratory analyser's run record keeps New Zealand standard time all year, an hour behind the
  collection, reception and release times, and no file says so. The records fix it: rows are stamped up to 53 minutes
  before reception logged their bottles and no result is released within 64 minutes of its stamp, so every shift the
  records allow lies between 53 and 64 minutes, and the bench is set so no treated sample sits within ten minutes of 24
  hours: every shift in that range counts as the hour does. Held 0 of 8 against both round 4 readers.
- Ask A, the second logging: reception logged the delayed 7 December round's 16 treated bottles a second time from the
  courier's docket, so the second rows carry the docket's one pickup time as the collection time, new sample numbers and
  a reception 25 minutes later, with each bottle's one analysis stamp, result and release.
- Ask B, the storm-night stops: on the nights of 26 October and 3 December lightning tripped the supply to four analysers each
  (the PLC and the outstation have their own backed-up supply), and each stood off for 4.8 to 7.5 hours until the morning
  operator reset it: F rows at every port with nothing filled (the polls went on and returned no reading) and no check
  after, the same face as an outstation change. The analyser's sequencer starts again at the raw water port when it is
  switched on, so its ports fall in other slots from then on: the run is the analyser's, the PLC had no reading, and the
  dose ran fixed beyond the hold. Round 4's reader H rule (a whole-plant unfilled run with no check after is the
  telemetry's) reads these as the telemetry's and misses every plant by 3.7 hours or more; reading every whole-plant
  run as the analyser's counts the outstation changes too and misses every plant.
- Ask B, the lost signals: each plant's filtered port lost its signal to the PLC once (a wet junction box or a failed
  loop isolator), 4 to 9 hours of F rows at that port only, the other ports read between and nothing filled, no check
  after; the round 3 readers' check rule reads them as the telemetry's.
Hazards: on ask A, October's treated samples under the old codes (the notice), the 28 December round analysed on 5
January, two courier breakdowns, the raw samples out of scope; on ask B, the November outstation changes, the failed
polls filled from the outstation (an F row with a G row beneath), the historian's own lost night of 17 November (no rows
at all, stated in the dictionary), the check cycles inside the hold, the two-hour hold, the quarter in New Zealand time.

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
| the hour added, one row per point and collection time | 0 of 8 | | 0 |
| the hour added, rows equal but for the number dropped | 0 of 8 | | 0 |
| unfilled runs a check followed the analyser's faults, the rest the telemetry's (round 3, both readers) | | 0 of 8 | 0 |
| unfilled runs at every port with no check after the telemetry's, a port's own the PLC's (round 4, reader H) | | 0 of 8 | 0 |
| unfilled runs at every port the telemetry's, checks aside | | 0 of 8 | 0 |
| F rows with nothing filled back as the analyser's faults (rounds 1 and 2, all four readers) | | 0 of 8 | 0 |
| gaps in the historian's G rows, two-hour hold | | 0 of 8 | 0 |
| every F row a gap, the lost hours not, two-hour hold | | 0 of 8 | 0 |
| the PLC's gaps summed whole, no hold | | 0 of 8 | 0 |

| Ask | Cracker (the call landed, the best path that misses the device) | Verdict |
| --- | --- | --- |
| A samples analysed late | 0 to 2 of 8 (the stamps as given; with raw samples wrongly counted two plants net back) | miss |
| B hours at the fixed dose | 0 of 8 (round 4 reader H's rule) | miss |

Pair ceiling: 35.4 ((51.9 + 18.9) / 2), the cracker keeping 2 of the 16 ask figures on the call and the mirror the same.
Mirror leakage: 12.5 per cent of ask weight.
Measured by: generator/pair.py on the cut pack (target.zip af7016cf).

## Pre-ship check

- Free gates (stage 3, on the cut pack): generator checks 130 passed (the golden list against the world's truth; 24
  licensed estimates each filing the six with 0.0019 or more from the line; the line's recovery read at CAL-FI1 and
  HOL-FI1 only, every other channel moved 0.002 or less; the analyst test on the clean world, architecture 1's full
  model filing its six and the line alone the golden; SF1 to SF28; R1 to R3; the separation line with no failed polls,
  lost hours, outstation changes or lost signals, and in a world with no storm nights; the asks against the world with
  every natural path, round 4 reader H's rule included, missing every plant; the input gates); verify.py 0 failures;
  two builds byte-identical (target.zip af7016cf); figures_check 35 of 35; precut 51 of 51; voice-check PASS.
- leak.py REVIEW, no LEAK: WQ-DS-04 carries the call's words (its estimand and the return) and the documents carry
  the field's terms; none names a line loss, a film, a flush's effect, a trip or a restart.
- guard heart WARN (driver.near 0.16 against the slot's own lineage, differentiated on the card; people.first Caleb);
  surface people Emily Butler and Suzanne Nelson, as drawn.
- Containers clean (no producer signature, no out-of-band timestamp) in target/ and golden/.
- Golden realism: the workbook leads with the six as its title, lists them with plant, water, analyser and direction;
  the channels sheet carries each channel's carryover, calibration error at its level, sample-line loss and offset;
  the analysers sheet the shares, the error's form and the filtered line's loss with its rise at the flushes; the
  notes sheet states the estimand, the carryover, the calibration, the lines and how each item was counted. The chart
  shows every channel by plant against the 0.005 band, the six marked, both Holmedale channels annotated.
- The 10/10 rules re-read against the built pack: the decisive step (each filtered line's loss read from the readings'
  recovery after the flushes) is an estimate no filed sentence performs; every Layer 1 item mishandled leaves the call
  unchanged (asserted: the check port's rows, the quarter on UTC dates, October's old codes, the failed polls, the lost
  night, the outstation changes, the lost signals, the storm-night stops).
- Probes on the near-final pack (pr252m): G filed exactly the default path's six, H the first-port five; neither read
  the flushes.

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
- Architecture 2, pack 1 (the filtered lines' loss at Brannock and Elstow, whose filtered water sits above the 0.030
  limit): call-only probes A, B and C flagged both channels straight from the lab pairs (each read low against every
  uncensored grab) without finding the mechanism. A loss the grabs can see is read off the grabs; it moved to the two
  filtered lines whose grabs are all censored, Calderwood and Holmedale.
- Architecture 2, pack 2 (losses of 0.55 and 0.85 regrowing over 1.5 days, Holmedale's filtered water as drawn): probes
  D and F filed the default list or the one-slot list and never read the flushes; probe E returned nothing. The licensed
  recovery forms put HOL-FI1 between +0.0010 and +0.0052 (a straight-line regrowth crossed the band). Holmedale's
  filtered water was lifted 0.0035 (its 14 filtered grabs still all below the limit), the losses set to 0.65 and 0.95
  and the regrowth to two days: every form now files the same six, 0.0019 or more from the line.
- Ask B's lost signals alone (round 4: reader H kept 8 of 8 by the rule that a whole-plant unfilled run with no check
  after it is the telemetry's): that rule is right on every run the round 4 pack carried, so no re-siting of the lost
  signals beats it; the storm-night stops are runs it misreads, found by the analyser's sequence starting again.
- The per-channel carryover fit taken into the two-point read (stage 3): at a fouled filtered line the regression on the
  two slots before takes the line's recovery into its share two slots back (Holmedale's filtered port 0.098 against its
  final port's 0.020, one cell), and the raw port corrected with those shares moves Holmedale's zero error by 0.012. The
  two-point read uses the analyser's pooled shares, as one cell implies; the per-channel route itself (its offsets with
  the line read) files the six.

# task468 design note: Glenbrae Water's 2026 trade waste COD masses, converted from TOC on the samples' own chloride

Status lives in `pipeline.json`; this note holds the design of architecture 6, drawn on 2026-11-01 as a batch 1
re-root. Read `## Tried and rejected` first: architectures 1 to 4 (transit nominations, specialty pharmacy staffing, a
Medicaid plan's linkage-corrected mortality bonus) and architecture 5 (Harrowmere's repeat-sales pressured wards, sent
back by its stage 4 judge) are spent. Nothing of their worlds is kept.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task468.json`, architecture v6, registered 2026-11-01T01:02:25Z after a
  pull; `guard.py check` PASS on the filed card. The first filings were refused on the window and redrawn honestly:
  shape 10 (task231), pattern G4 (task146), G14 and the statutory filing (task445 v3, registered minutes earlier),
  purchase order or contract (task145), G16 and G6 (same-puzzle and same-driver records); architecture 5 and the
  earlier four are in the card's lineage.
- **Pairing:** Physical & Environmental Sciences / emissions-inventory (serves ETL and DD) / Data Extraction &
  Conformation (ETL). Healthcare delivery and survey research are spent for this slot; education's equating cell
  carries task445 v3 (registered this hour) and three in-cell builds. The inventory is a utility's releases to sewer:
  each trade waste customer's mass of chemical oxygen demand discharged in 2026, conformed from two laboratory
  systems, hourly flow telemetry and the field job log.
- **The ETL move:** conform a year of measurements made on two bases onto the agreement's reference basis. From
  2 February 2026 the laboratory reports total organic carbon in place of dichromate COD; the policy makes the COD of
  a TOC sample the COD the reference method would have reported, estimated from the samples tested both ways in the
  October to December 2025 parallel run.
- **World:** Glenbrae Water, a fictional regional water and sewerage utility in south-east Queensland, its trade
  waste unit and its laboratory; its industrial customers, among them Coolabah Olives (an olive and pickle packer),
  Tallowood Tannery, Mt Edwin Cheese, Glenbrae Meats (an abattoir), Riverbend Poultry and Sunvale Dairy Ingredients.
- **Furniture:** forum customer_or_counterparty (the review notices go to the customers), forcing event
  audit_or_inspection (the state regulator's audit of the trade waste programme in March 2027), organisation
  utility_or_infrastructure; none repeats the last three builds.
- **Personas** (`guard.py names --geo au --seed 468`): Erik Marks, Trade Waste Manager; Mitchell Boyd, Laboratory
  Manager; Brent Fisher, Field Services Coordinator (the first draw's Diane sat in an older build and was redrawn).
- **Retrospective quantity, forward call:** the agreement reviews and the regulator's audit fall in 2027; the test
  reads the closed 2026 discharge year, as the policy files it.

## Tried and rejected

- 2026-10-17, at the draw: Urban & Regional Science for a transit seed: none of its task types serves ETL, so the
  pairing cannot be filed.
- 2026-10-17, at the draw: a passenger's average wait from the timetable's gaps (half the mean gap against the
  length-biased mean): generic arithmetic of any periodic service, so the domain reads as a backdrop, and it is not the
  data-integration task type's method (it survives as Ask C's device, which the 10/10 rules leave free).
- 2026-10-17, at the draw: two operators' stops linked across feeds to build combined corridor frequency: the right
  link is read off direction and stop sequence, a field reading, and the guard's identity risk lands on it.
- 2026-10-17, at the draw: delivered frequency from the planned schedule less cancellations cancelled by whole runs:
  needs a dispatch log, and a complete log counts delivered departures exactly, bypassing any estimate.
- 2026-10-17, stage 2: the review as a simple random sample of the unmatched events, its raw route mix the decisive
  step: a single insight the review file signposts (133 v1 died on a development sample pointing at its decisive
  step); the review is now a bus-day sample with one event each, so using it is R2 and weighting it is the move.
- 2026-10-17, stage 2: the composition varying by time band (trunk routes late in the afternoon only, pull-in deadheads
  at night): pooled and band-level shares gave different calls on Route 17, a grain fork (H14); lateness now flat
  through the day and out-of-service movements spread over it, so every stratification agrees.
- 2026-10-17, stage 2: Riverside failing on a four-an-hour timetable: Good Friday's Saturday service pulled its
  timetable average under four too, so the timetable rung landed on the golden; Riverside now runs five an hour and
  its afternoon runs went a quarter short of operators.
- 2026-10-17, stage 2: each candidate's lowest hourly average graded to one decimal: the weighted variants spread up
  to 0.3 on Route 2, so the prompt asks for the verdicts and the workbook carries the figures as supporting detail.
- 2026-10-17, stage 3: on-time shares to one decimal of a per cent: two routes' shares sat within a hundredth of a
  rounding edge, so the shares are graded to the whole per cent (every share further from its edge than one departure
  moves it, asserted); Hillcrest's lateness and timetable jitter moved so its share and its wait sit clear of their edges.
- 2026-10-17, stage 2: a scheduled-departures table from both feeds as an ask: a GTFS-literate cracker executes the
  calendar, calendar_dates and frequencies correctly, so no device held; replaced by the waits (an analytical device).
- 2026-10-17, stage 4: Ask A, Quinnell's April to June record by stop and service-day month: both outside readers
  found the file-head repeats by bus, stop and second and assigned the service days, the judge read the repeats as a
  fork, and no silent device reaches the record without touching the review's frame; dropped (the repeats, the 31
  March copy and the after-midnight service stay as Layer 1 on the call's path, asserted neutral).
- 2026-10-17, stage 4: Ask C, the scheduled wait on 13 May: the prompt's definition made the waiting-time paradox a
  literal integral both readers computed, the frequency window's end read two ways, and no representation of the feed
  hides a departure from a careful reader; dropped (the frequency trips now exact times, each block ending between
  two trips).
- 2026-10-17, stage 4: the on-time device as Quinnell's DeviationSec taken at arrival: both readers timed the
  departures from the timestamps and read the field as noise, and guidance 4.2's "as the AVL system records it"
  invited it; DeviationSec is now the departure against ScheduledDeparture, and the device is Arbor's minute-held
  schedule against the feeds' half minute.
- 2026-10-17, stage 4: Route 6's on-time share at 47.46, 0.04 from its edge (a reader rounding to one decimal first
  filed 48): the half-minute bands, set per transfer point, put every share at least 0.19 from its edge.
- 2026-10-17, stage 4: the eleven candidates named only by route colour in routes.txt (the judge's Gate B and E
  finding): Planning's candidate list now ships with each route's designated stop.
- 2026-10-17, stage 4: the on-time device as Arbor's minute-held schedule against the feeds' half minute: judge pass 2
  read the two schedule sources as an open fork (FIX_NOW), the pin naming the published timetable in guidance 4.1 and
  4.2 closed it, and reader round 3 then timed all eleven shares against the feeds. A device whose basis a filed
  sentence must name dies with the pin, and every other column the ask reads (the departure, the trip tie, the window,
  the days) is the call's own population, so no device on this ask can stay off the call's rows.
- 2026-10-19, repair: the stop-hour grain fork (reader round 3): the review drew 250 bus-days a month, so the
  stop-by-clock-hour cells held one to seven reviewed events and the minimum of thirteen noisy hourly estimates sat
  biased low; at 400 bus-days a month, with the within-bus-day draw on its own stream, every weighted grain (stop, stop
  and hour, band, month, vendor, the within-bus-day weight, counting-day reviews) files the golden and every raw grain
  the R2 slate (checks.py R3b, verify.py's stop-hour estimator).
- 2026-10-19, repair: replacing the dead on-time ask, measures tried on paper and dropped: the average scheduled wait
  (computed exactly from the feeds by any GTFS-literate solver, and "a weekday of current service" splits on the class
  days); missed trips from a dispatch log (it would hand every solver each route's delivered departures, the call's own
  quantity); APC boardings at the designated stops (doors open only in service, which would identify the out-of-service
  passes the review estimates); the fleet roster's asset tags moved between buses (it would move the review's bus-day
  join on the call's path); evening and Saturday counts (Quinnell's repeats and the cutover overlap are seen, not
  silent). The shelter ask takes none of the call's rows.
- 2026-10-19, architecture 1 spent (the transit nominations): four isolated readers landed the call, so the review
  weighted by its design was read off the memo's sampling procedure by every careful solver (Gate F, score_reader exit
  1), and judge pass 3 found the shelter ask NOT_DETERMINISTIC (no file states the moved-stop rule, and stating it
  hands over the device). The author chose to re-root.
- 2026-10-19, architecture 2 spent at stage 4 (the specialty pharmacists by months on therapy): the isolated reader
  projected the caseload by tenure since first fill from past month ends, its first move once it saw the program year
  unobserved, and landed the call (10 of 10) and 27 of 28 ask figures (score_reader exit 1); the bulletin's step-therapy
  sentence and the caseloads' 2026 starters made the duration mix visible, and the rebate statement's repeated
  product-quarter amount was caught on sight. A forward window over a record that shows the process invites the
  conditional development; the next architecture needs a decisive step the record does not display.
- 2026-10-19, architecture 3 drawn: the same world, the decisive step moved to the clock. Members who stopped a drug
  and came back after a lapse restart its persistence curve, so the development is indexed by months in the current
  episode; v2's first-fill development is now the analyst test's wrong answer (57 against 54). Tried first: a wave of
  returners 30 per cent of the step-therapy classes' past stoppers (GLP 177 of 1,809 back, first-fill clock only half
  a pharmacist off), raised to 60 per cent; a separation by back-test (both clocks pass the earlier Junes alike,
  returns being rare before 2026), replaced by the record's own comparison of returners with continuing members and
  new starters. The rebate statement's repeated product-quarter amount (caught on sight by v2's reader) kept as a
  hazard; the primary moved to the contract year's February start.
- 2026-10-19, architecture 3 spent at stage 4 (the specialty pharmacists by months in the current episode): the
  isolated reader built persistence by time since episode start, an episode broken by a gap of more than 100 days,
  because the refill gaps were a few days and the returns months, and landed the call (10 of 10; score_reader exit 1).
  A clock the gap distribution displays is not silent; architecture 4 is drawn fresh.
- 2026-10-20, the three architectures read together (the author's rule: no retirement, so a fresh architecture 4
  follows): architecture 1 fell to readers who read the review's weighting off the memo; architecture 2 (judged
  DETERMINISTIC and APPROVE) to a reader whose first move on an unobserved window was the tenure-conditioned
  projection; architecture 3 to a reader who read the episodes off the bimodal refill gaps. A forward window over a
  record that displays the process invites the careful reader's persistence model, and every clock the record shows
  plainly is a reflex at medium effort: the next architecture needs a decisive step the record does not display.
- 2026-10-20, architecture 4 calibration: the pooled rate by the link's pass was first the only stratification other
  than the class that the hospitals' mixes separated; hospital-by-pass rates also landed the golden set while each
  hospital's members without a number were mostly one surname type, and stopped doing so once Varden's members
  without a number became low-risk workers whose recorded deaths include none without a number, so its own rates
  borrow the pass's (R4c). Kept: the class is what drives the error, and a hospital's own rates are not identified
  where its controls are empty.
- 2026-10-20, architecture 4 build: dropping Carrisford's encounters moved Tamsin General (1.05) over the line on a third
  fewer admissions, so Layer 1 was not neutral; Tamsin General now sits at 0.93 and Calloway at 1.32, and every Layer 1
  mishandling leaves the five (SF1, SF6, SF7).
- 2026-10-20, architecture 4 build: a two-part surname read from a hyphen only puts most two-part surnames with the
  single ones and adds Varden; dropped from the fork table as no reading of the enrollment file (88 per cent of two-part
  surnames are written with a space), while a space-only reading files the five (SF8b).
- 2026-10-20, architecture 4 asks: interim bills carrying a stay's payment to date (a summed interim history double
  counts) and newborns billed under the mother's identifier (a stay-key deduplication drops them) were drafted for the
  bonus ask and dropped: the first is not how a plan's paid column behaves, the second reaches only the hospitals with
  deliveries, so no device moved all fifteen figures. The platform conversion's conventions move all fifteen and live
  in a column the call never reads.
- 2026-10-20, architecture 4 ask device: the CPS and platform replacement conventions, left unfiled, were the primary.
  Reader round 1 (on b1bc148c) read them off the amounts (CPS replacements centred on zero, 63 per cent negative, none
  on the platform) and confirmed them on hospital totals landing within a few dollars of round bonus figures, 15 of 15
  (score_reader exit 1), and the judge's first pass required the convention filed (inferable, not filed). A convention is
  a fork, not a device: filed in the extract notes, it is a hazard, and the device moved to the dispute log's awards
  that a reprocessed bill already carries. The base rates that had centred every bonus in its cell were retuned so each
  sits 15 to 35 dollars off centre.
- 2026-10-20, architecture 4 estimator: seven hospital classes with no links among the admissions no control reaches
  gave estimates below zero, which the golden floored and step 6 did not, so the judge's unfloored recompute differed
  at the first decimal (Calloway 189.5 against 189.8 deaths, Varden 24.3 against 24.5, Fairhaven 1.05 against 1.06).
  Filing a floor would be rule application on the decisive step; instead each such class now carries the links its
  false-link share expects (one more of its members found by the Office), so floored and unfloored agree (C1, C1b). The
  call is unchanged; Varden moves to 1.03 and Fairhaven to 1.09.
- 2026-10-31, architecture 4 retired at the batch audit (re-rooted, not repaired): it fell short of the survivor
  anatomy on the Reflex. Its golden was the field's own linkage-error correction (each class's false-link and
  missed-link rates applied to the Office's matches), so the field's named method sat at the top of the ladder,
  where a reader who knows record linkage applies it as a first move, and the Office's shipped match file was the key
  the link rode on; architecture 5 is drawn fresh in another client domain.
- 2026-10-31, architecture 5 draw: a constant-quality house price designation on hedonic attributes or a stock
  aggregation is spent (task482 architectures 4 and 5, both landed by readers who fitted the handbook's model); the
  draw keeps the field's repeat-sales index at rung 1 and moves the decisive step to the identifying assumption no
  sales file shows, the dwelling unchanged between its sales.
- 2026-10-31, architecture 5 stage 2: the developers' works at four to five residual standard deviations on a
  noise-only price model: a 3-sd residual trim on every pair dropped them and landed the golden set without the
  register; each dwelling now drifts about its ward's path (a spread growing with the holding period, as repeat-sales
  records show) and the works add 14 to 23 per cent, so no filter on the sales sees them (SF9).
- 2026-10-31, architecture 5 stage 2: owner works of every kind in the register, structural alterations among them:
  a reading that counts only enlarging work moved Kestrel Rise's published change by 0.2, a fork at the graded
  decimal; owners' works are now extensions, lofts and garage conversions, and every reading of "building work"
  files the same figures (SF2).
- 2026-10-31, architecture 5 stage 2: June 2021 postcode recodes split pairs across the recode and moved two wards'
  figures at the decimal between the literal address and a linked reading: dropped (SF4b).
- 2026-10-31, architecture 5 stage 2: a block of flats certified at its last flat's date let a flat's first sale
  precede its block's certificate, so a postcode-and-number match set aside pairs the full address kept (Calder Bank
  8.0 against 8.1): each block is now certified complete on one date (SF4).
- 2026-10-31, architecture 5 asks: the register's ward column holding the 2019 wards (a label stored before the
  boundary review) as Ask A's primary: an asking sentence naming the May 2023 wards kills it, and without one the
  register's own column is a literal reading of "ward", a fork; the column now carries the current wards and the
  primary is the approver's blank loss.
- 2026-10-31, architecture 5 asks: Ask B as a count of additional entries: every handling of the update reproduces
  the count (the battery's latest-version rule), so the count carried no device; the ask is the money paid.
- 2026-10-31, architecture 5 asks: Ask C's re-claims as one-to-one repeats of Brackwell's claims (postcode, start and
  homes): the battery's re-keyed-record match finds them; Brackwell now claims its sites phase by phase and
  Calderstone each site once, so a re-claim equals only the phases' sum.
- 2026-10-31, architecture 5 shock: Pellbury's 2024 and 2025 company purchases made it the largest count of
  additional entries in those years; the city-centre and student-let wards now carry their own company buying, and
  Pellbury sits second of the twelve.
- 2026-10-31, architecture 5 leak screen: the price paid field guide (a PDF listing every column) is a dictionary
  under leak sweep 1 and 12; dropped, and the price paid files carry the publisher's header row instead.
- 2026-11-01, architecture 5 dead at its stage 4 judge (NOT_DETERMINISTIC, SEND_BACK): Harrowmere's pressured wards on a
  repeat-sales index with the pairs spanning building work set aside. The methodology's section 3, executed word for
  word, pairs every two consecutive sales, so Pellbury reads 6.0 per cent and the uplift splits four ways; the golden's
  set-aside rested on the intent phrase "same dwelling at the same quality", a narrower certificate reading (new
  dwellings and conversions only) was equally licensed, and filing the set-aside would have made linking the
  completions register a rule executed (task445 architecture 2's death). Ask 3's net additional dwellings also failed
  to reproduce (365 against 348). An inclusion or exclusion over a second source has no safe filing; the report is
  kept as determinism_check_report_arch5.md, and architecture 6 re-roots into another domain with the decisive step an
  estimate.

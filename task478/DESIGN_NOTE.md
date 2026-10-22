# task478 design note: the Tamsett Basin district's 2027 NOx agreements, by the NOx each facility's SCR-controlled units emitted in 2026

Status lives in `pipeline.json`; this note holds the design. Read the Tried and rejected section first. Architecture 6
(re-rooted 2026-10-22); the records of architectures 1 to 5 are at the end.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task478.json` (architecture v6), registered 2026-10-22 after a pull, the
  architecture 1 to 5 identities in its lineage. `check` on the registered card: WARN only, answered here.
  `repeat.gate_g` and `overuse.gate_g` (method_or_model_selection, task273 among the last two): the label is the honest
  one, since the decisive step is the model of each unit's rate across the year, and the driver it carries (a spot test
  integrated over the hours on a renewable component) is on no other card. `test.same_puzzle_older` and
  `test.same_driver_older` (gap objective, G16, a ranked slate) against task190, task195 and task228 v2: differentiated
  on the card, none of them carries a measured rate that climbs with a component's operating hours. Nearest drivers on
  file at 0.09 (task474 v2 and v3, monitor gaps filled by the hour's state).
- **Redrawn at the draw, and why the replacements are the honester labels.** The live window (task249, task273,
  task169) bans the statutory filing, the budget cycle, the vote, the council, the regulator, the government agency, the
  policy adviser and the capacity planner. The decision is the slate of the plan's NOx reduction agreements, contracts
  the district signs with each named facility (`purchase_order_or_contract`); a regional air district is a local public
  agency of the counties it serves (`local_government`), governed by its board of directors (`board_of_directors`), and
  the plan is the planning and rules manager's (`programme_officer`). Gap time with G13 first BLOCKed against five older
  builds on the same signature; gap objective is the honester one, since a source test is a correct reading of the test
  day's rate and the plan is scored on the year's tons, and G16 leads because the decisive step is the model of the rate
  across the year. Personas redrawn from `guard.py names --geo "United States" --seed 478` after Leslie, Ricardo,
  Zachary and Mary each warned against an older build: Nancy Hansen (planning and rules manager), Brian Daniels (senior
  air quality engineer, emission inventory).
- **Pairing:** Physical & Environmental Sciences, task type `emissions-inventory`, which serves Data Extraction &
  Conformation (ETL). The ETL work conforms thirty-four SCR-controlled combustion units at fourteen facilities onto one
  2026 NOx inventory: nine units' continuous monitor hours (local standard time, substitute-data codes, the monitoring
  plan's unit ids against the district's device numbers), twenty-five units' source tests from two test databases (one in
  ppmvd at 15 or 3 per cent oxygen and lb/hr, one adding lb/MMBtu), the facilities' monthly fuel statements in therms,
  MMscf and MMBtu, run-hour readings, and the compliance event log. Objective: Data Extraction & Conformation (ETL).
- **The decision and the quantity:** the Tamsett Basin Air Pollution Control District (fictional) names in its 2027
  Community Emissions Reduction Plan for the Lowry Creek corridor the five facilities, of the fourteen there with
  SCR-controlled combustion units, whose units emitted the most NOx in calendar 2026, and signs a NOx reduction agreement
  with each by 1 April 2027. A retrospective quantity with its reason: the plan sizes its agreements on the last closed
  year's emissions, and the agreements run from 2027.
- **Shape:** 01, a ranked list under a cap of five: fourteen facilities' 2026 NOx at the whole ton (14), the five (1),
  a chart's named parts (the fourteen bars, the five marked, the labels: 3), the files (3), and the asks' figures (two
  per facility, designed at stage 2: 28): 49.
- **Strategy:** `other`, named on the card: a clock already in the data (the operating hours on each unit's catalyst
  since it was last replaced), estimated from every unit that went through it. Gate G `method_or_model_selection`: the
  conformed inventory is the object and no shipped artifact ranks the facilities. Gap objective, pattern none,
  generators G16 (decisive) and G13. Layer 2 family `estimation_fit`, pattern `own:a spot test of an emission rate read
  at its catalyst's age, carried across the year, against the rate integrated over each month's catalyst operating
  hours by the climb the units' test histories trace`.
- **World:** United States, an unnamed state's Tamsett Basin, its air district's Lowry Creek corridor with fourteen
  facilities holding SCR-controlled boilers, process heaters, gas turbines, a glass furnace and lean-burn engines (a
  combined-cycle plant, a refinery, a glass works, a paperboard mill, a peaking plant, a landfill gas plant, a
  compressor station, a cannery, a medical centre, a university, a water reclamation plant, an almond processor, a tire
  retreader and a data centre). The large units carry continuous monitors and close their ammonia injection on the
  monitor's NOx; the rest inject ammonia open-loop on load and are source tested every one or two years under the
  district's NOx rule.
- **Forcing fact:** the agreements are signed by 1 April 2027; the pack is as of 19 February 2027 (exports pulled 8 to
  16 February).
- **Data-native sentence:** an SCR catalyst loses activity with every hour its unit fires, and a unit without a monitor
  injects ammonia on load, open-loop, so its NOx rate climbs from the day its catalyst is replaced until the next, while
  a source test reads the rate at whatever catalyst hours its test day fell on; the units' own test histories, set
  against the operating hours their catalysts had run at each test, trace the climb.
- **The WHAT screen.** Population: the SCR-controlled combustion units the district's NOx rule covers at the fourteen
  facilities (plan section 2). Outcome: the NOx each unit emitted. Window: calendar 2026. Unit: tons a facility, summed
  over its units. Comparison: the five highest of fourteen. The decisive step settles none of them: it is how a source
  test's rate is carried onto the year's emissions, which nothing files.
- **Sources, one line each:**
  - The stationary-source inventory field's own hierarchy (continuous monitors, then source tests, then factors) and its
    rule that a test is used only where it represents the year's operation: here a test is a correct reading of one day.
  - SCR operating practice: catalyst activity falls with exposure, closed-loop ammonia control holds a monitored unit's
    NOx while open-loop control lets an unmonitored one climb, and catalysts are replaced on hours and on test results.
  - This slot's architecture 5 (an instrument's bias read on a load-independent component): the measurement here is
    unbiased on its day; what moves is the rate itself, with the hours on a renewable part.
- **Same-puzzle and same-driver tests:** (objective, G16, ranked_slate_under_cap) and (objective, G16,
  method_or_model_selection) against the older builds: task190, task195, task228 v2, differentiated on the card.
- **Abstraction test:** the nearest drivers stripped of nouns (task474 v2 and v3, monitor hours filled at the state the
  gap ran in; task138, traces started from each unit's actual store) carry no spot measurement of a rate that climbs
  with the operating hours on a renewable component, integrated over the hours a period ran through.

## Default path

1. Read the plan: the agreements go to the five facilities whose SCR-controlled units emitted the most NOx in 2026
   (section 2), each unit's emissions as the district's inventory guidance computes them: the monitored units from their
   hourly NOx mass, the others from their fuel and an emission rate that represents the year's operation.
2. Summed the nine monitored units' hourly NOx mass for 2026 (local standard time, substitute hours as reported).
3. Converted every unmonitored unit's source tests to lb/MMBtu (lb/hr over the test's heat input, or ppmvd through the
   fuel F-factor at the oxygen the test reports), took the latest test, and multiplied by the unit's 2026 heat input
   from its fuel statements.

Ends on: Ashgrove Refining, Haskett Ridge Compressor Station, Lindqvist Paperboard, Valmora Glass and Wexley Point
(design target, fixed at the build).

Golden: Ashgrove Refining, Sedge Hollow Landfill Gas, St. Aldric Medical Center, Valmora Glass and Wexley Point
(design target, fixed at the build).

## Stump sentence

The default path carries each unmonitored unit's latest source test across its 2026 fuel and names Ashgrove Refining,
Haskett Ridge, Lindqvist Paperboard, Valmora Glass and Wexley Point, because a unit that injects ammonia open-loop emits
NOx at a rate that climbs with the operating hours on its catalyst since the last replacement: Sedge Hollow's engines
and St. Aldric's cogeneration engine were tested weeks after new catalysts went in and ran on them through 2026, and
Haskett Ridge's engines were tested on worn catalysts replaced that December; the climb the units' test histories trace
against catalyst hours (about 0.6 in the log a 10,000 hours), integrated over each month's catalyst hours, names
Ashgrove Refining, Sedge Hollow, St. Aldric Medical Center, Valmora Glass and Wexley Point.

## Three rules

Task type: emissions-inventory (Physical & Environmental Sciences): thirty-four SCR-controlled units' monitor hours,
source tests, fuel statements, run hours and catalyst events conformed onto one 2026 NOx inventory, a task type
serving Data Extraction & Conformation (ETL).

Domain test: stationary-source inventory practice: the deciding quantity is each facility's 2026 NOx, which for the
units without a monitor is fuel times a rate that represents the year; an SCR catalyst loses activity with every hour
it fires and open-loop ammonia injection does not follow it, so the field reads such a unit's rate along its catalyst's
hours, not off one test day; with another field's nouns there is no catalyst, no ammonia control loop and no source test
to carry, so nothing is left to decide.

Swap: put "hospital" for "facility" or "visits" for "tons" and nothing reads: there is no renewable catalyst whose
operating hours move a measured rate, no test day read against a year and no closed-loop control that holds some units
flat; the abstract move (a spot measurement integrated over the hours on a renewable part) needs the field's own
catalyst and control physics.

Layer 1: the source tests split across two databases, the older reporting ppmvd at 15 per cent oxygen (turbines,
engines) or 3 per cent (boilers, heaters) and lb/hr, the newer adding lb/MMBtu; the fuel statements in therms, MMscf or
MMBtu by facility; monitor hours in local standard time with substitute-data codes and the monitoring plan's unit ids
against the district's device numbers; an event log of mixed date formats and free text; a facility renamed after a
change of owner; run-hour meters read at inspections, one replaced. Each is written by the system named, none is placed
to be caught, and each read the natural wrong way leaves the call where it is (checked in checks.py at the build).

Layer 2: estimation_fit, each unmonitored unit's NOx rate carried across 2026 along its catalyst's operating hours by
the climb the units' test histories trace against those hours, instead of a test day's rate held for the year.

Decisive step: fitting each unmonitored unit's tests against the operating hours its catalyst had run at each test
(a common climb, each unit its own level) and summing 2026 month by month at each month's catalyst hours, which moves
the five from Ashgrove Refining, Haskett Ridge, Lindqvist Paperboard, Valmora Glass and Wexley Point to Ashgrove
Refining, Sedge Hollow, St. Aldric Medical Center, Valmora Glass and Wexley Point.

No decoy: nothing is planted: the monitor exports, the test databases, the fuel statements, the event log and the
documents are what each system writes; no report ranks the facilities, states a unit's 2026 rate or says a test is
unrepresentative; every catalyst's climb and every replacement is the kind every SCR fleet without monitors runs.

Not semantics: every field, unit, oxygen basis, clock and code read correctly (ppmvd at 15 and 3 per cent, lb/hr, the
F-factor, therms and MMscf, substitute hours, device numbers) still leaves the careful route on the latest test; no
column holds a unit's 2026 rate or its catalyst hours and nothing says the rate moves with them; the step is an
estimate (the climb and each unit's level) and the integration it sets, not a reading.

Not rule application: the plan files the population, the outcome, the window and the cap (the WHAT), and the guidance
asks for a rate that represents the year; no filed rule or procedure says how a test is carried onto the year or that
the rate moves with catalyst hours.

Analyst test: a strong analyst who conforms every test to lb/MMBtu, every fuel statement to heat input and every
monitor hour to 2026, and reads the plan and the guidance correctly, carries each unmonitored unit's latest test across
its 2026 fuel and names Ashgrove Refining, Haskett Ridge, Lindqvist Paperboard, Valmora Glass and Wexley Point; only the
rate integrated along each catalyst's hours names Ashgrove Refining, Sedge Hollow, St. Aldric Medical Center, Valmora
Glass and Wexley Point (checks.py on the generator's clean truth at the build: the true 2026 NOx gives the same five).

Estimand: the 2027 Community Emissions Reduction Plan section 2: the five facilities whose SCR-controlled combustion
units covered by the district's NOx rule emitted the most NOx in calendar 2026, in tons, each facility the sum of its
units.

No certified replay: no facility total, unit rate or 2026 inventory figure ships; the source tests are what each test
day read and the monitor hours what each monitor read, so no published figure ties under either route.

Lesson: a source test is a correct reading of one day's rate, and a year's emissions need the rate the year ran at; an
SCR catalyst loses activity with its operating hours and open-loop ammonia does not follow it, so an unmonitored unit's
rate is read along its catalyst's hours since the last replacement, which the units' own test histories trace, and a
test taken weeks after a new catalyst understates a unit that ran on it all year while one taken on a worn catalyst
overstates a unit replaced since.

## Architecture 5 record (spent 2026-10-22)

Architecture 5 put each weigh-in-motion station's weights on the static basis through its loaded tractors' steer-axle
median against the scale houses' loaded tickets before counting class 9 trucks over 80,000 lb. Round 1's two readers
missed the call on the gross as recorded and kept all 24 ask figures; with the asks re-sited, round 2's reader C landed
the call by measuring each station's gain on the vehicle classes other than 9 against the four stations that agree, and
kept all 24 ask figures. Judge r5a and r5b DETERMINISTIC (determinism_check_report_v5.md). A call any reader lands is
spent, so the architecture is spent.

## Architecture 4 record (spent 2026-10-22)

Architecture 4 resolved Kerbline's detections into potholes after moving each one back along its pass by its unit's
GPS latency, fitted on the surveyed utility covers, times the pass's speed. Over four stage 4 rounds seven of eight
readers missed the call, and reader F (round 3) landed it by fitting each unit's lag from the detections' offsets
inside rough clusters on the pass's signed speed; the judge's last pass (r4e) was DETERMINISTIC and APPROVE. A call any
reader lands is spent (leak-check), so the architecture is spent.

## Architecture 3 record (spent 2026-10-21)

Architecture 3 completed the unrecorded potholes with the fleet groups that drove a segment as the capture occasions
(units of one kind seeing the same potholes); three readers and the judge missed or confirmed it, the fourth landed the
call by estimating each group's visibility by maximum likelihood.

## Architecture 1 record (spent 2026-10-21)

Architecture 1 completed the unrecorded potholes over the distinct units that drove each segment (each unit either
always or never seeing a given pothole); eight readers and the judge missed or confirmed it, the ninth landed the call
by fitting each unit as an independent list. In architecture 3 that route is the careful wrong one.

## Architecture 2 record (spent 2026-10-21)

Architecture 2 resolved Kerbline's raw detections into potholes with a linkage tolerance set by each unit's positional
error, measured on surveyed utility covers; two readers missed it, two landed it by folding the sweepers' visibly
scattered reports into the precise units' potholes. Judge APPROVE (v2).

## Tried and rejected

- Architecture 6 draw (2026-10-22): re-rooted on the author's standing rule (no retirement) with a fresh world, the
  lesson of architectures 1 to 5 taken first: each golden was the field's standard method and a strong reader took
  it, so here the standard (a source test carried across the year) is the default path. Screened before it and dead:
  the weigh-in-motion world again with each station's random error deconvolved from its shares (the deconvolution's
  method choices leave every share open at the whole per cent); fare inspections chosen by crowding, reweighted by
  the trips' loads (a sample reweighted to its population, task482 v2's reflex); pavement condition carried from the
  last survey across treatments (this draw's clock, one build at a time); double deflation of a region's value added
  (a filed definition, or beside the national-deflator practice a competing defensible answer); direct against
  indirect seasonal adjustment of a channel-mixed total (two defensible methods, the adjustment settings open every
  figure); a plan year's deductible clock on plan-paid seasonality (a forecast of open months, not a conformation);
  common-person concordance across a summer (the growth model's choices open the cut); fuel sold against fuel burned
  in a fuel-based mobile inventory (two standard methods, the reader's pick a coin flip); days supply against fill
  date in pharmacy claims (a field read); tests timed by catalyst replacements (task229 v2's insight inverted, checks
  timed by the reset, solved in-house).
- 2026-10-22, architecture 5 spent at stage 4 round 2 (zip md5 98e0e301): reader C landed the call without the
  tickets. It measured each station's gain on the vehicle classes other than 9 (two-axle, three-axle and six-axle trucks
  weigh alike at every station), referenced it to the four stations that agree within half a per cent, divided class 9
  by it and filed the golden five (Elk Ferry 20 and Garnet Ridge 23 against 16 and 21, the set unmoved), and it kept all
  24 ask figures (the backfill paired within 15 minutes, the other new-host rows read as UTC, each trip rebuilt from the
  tags). A multiplicative bias every class carries is measured by comparing across stations any population that should
  weigh the same everywhere, and an instrument calibrated before counting is the field's own standard method, so a
  golden that is that calibration is a strong reader's reflex: the next architecture's golden has to go past the
  field's standard method, with that method the default path. Judge r5b DETERMINISTIC with a FIX_NOW on step 5's
  one-sided backfill window (determinism_check_report_v5.md); reader D stopped at the spend.
- 2026-10-22, architecture 5 stage 4 round 1 (zip md5 feba8739): both readers missed the call on the default path and
  the judge (r5a) returned DETERMINISTIC and APPROVE, but both kept all 24 ask figures: the new host's re-import showed
  as two id schemes overlapping from 15 June (reader A cut once at the new host's first row, reader B paired within 60
  seconds, both right on that pack), and program 6.2 sent both to rebuild each trip from the toll tags, where the paper
  citations' overwritten entry plaza showed. The switch is now staged by plaza with a backfill and late receipt stamps
  (every global cut and tight pairing misses), and the old host's rows keep local stamps under the new host's UTC
  column while cited trucks come back through the barrier after offloading, so the tag rebuild read on one clock files
  the barrier (checks.py A1, A2).
- 2026-10-22, architecture 5 build: with the golden five also the five sections running the most loaded tractors,
  every station scaled to the tickets' gross (median, mean, loaded median) landed the five, because the share over a
  fixed fraction of a station's own gross ranks the sections by loaded share. Ashford Gap and Halbrook now run 84 and
  86 per cent loaded with light loads, Cole Hollow and Kettle Run 62 and 66 per cent with heavier ones, and every gross
  scaling files another five (checks.py L1).
- 2026-10-22, architecture 5 build: the network-relative loaded gross scaling landed the five while Elk Ferry and Garnet
  Ridge carried ordinary freight; their bulk haulers now load to the limit (a tight loaded gross near 77,000 lb), so
  scaling them to the network erases genuine overweights (L4).
- 2026-10-22, architecture 5 build: a loaded line of 70,000 lb moved Elk Ferry's share across a bin edge (a steer
  axle's own random error correlates with a gross cut through the loaded peak); a steer axle's random error is now half
  the other axles' (its single tires bounce less) and the bulk sections sit mid-bin, so every line from 45,000 to 72,000
  lb prints the same twelve figures (G2).
- 2026-10-22, architecture 5 build: with 3.5 per cent of the tickets empty, the stations' loaded steer axles against
  every ticket printed 15 and 20 for Elk Ferry and Garnet Ridge (a 20-lb shift in the reference); the scale houses'
  pull-ins are now loaded trucks bar 17, and the all-ticket reference prints the golden's figures (SF8).
- 2026-10-22, architecture 5 build: a ticketed truck's tag could enter again between its trip and its stop, so the
  tag's last entry before the stop missed the trip weighed on a handful of citations; a weighed trip is now an entry its
  tag does not follow for eight hours.
- Architecture 5 draw (2026-10-22): re-rooted on the author's standing rule (no retirement) with a fresh world.
  Screened before it and dead: competing exits read as censoring (task134's main call); landfill first-order decay
  (set aside at task486's draw against task480); the inspection paradox on headways (task135); unconstrained demand
  behind a capacity (task147, task168); triple collocation of three series (task228, landed); startup emissions by
  thermal state (task273's screen); risk pooling of a health trust's reserve (the careful route sums the members' claims
  and lands it); coincident peaks (task117); a register's overcoverage by signs of life (the register count reads as a
  surface figure overturned, Gate G); coding completeness from switchers (a data defect corrected); GPS chord length
  from sparse pings (a known pitfall, and the swap test reads it as geometry); departmental against hospital-wide
  cost-to-charge ratios (the cost-centre organ hands it over); an inventory trend's correlated factor errors (the
  variance-only screen in mirror image: the point estimate lands the golden); seasonal shares of the calendar year
  against detrended factors (classical decomposition is the reflex and the shares route can beat it); generic erosion
  after loss of exclusivity (task484 v1's ramp curve); a one-time service depleting its pool (task83's lesson).
- Architecture 4, potholes resolved after a per-unit GPS latency fitted on surveyed covers (2026-10-22, spent at stage
  4): reader F fitted each unit's lag from the offsets of its detections inside rough clusters, regressed on the pass's
  signed speed, and landed the call exactly (1,441 potholes, 1,427 on the roadway); seven other readers and the judges'
  first derivations missed. A displacement proportional to speed is identifiable from the clusters themselves once
  passes at different speeds see one pothole, so the covers are a convenience, not the only route.
- 2026-10-22, architecture 4 stage 4 (r4d): the section yards' stores, added to make summing an app order's lines
  impossible, became an oracle (reader E: each crew-day's use rounded up to the bag reproduced every net draw) and a
  third reading (the judge read the net draws as the pounds used); the judge again asked for the order entry to be
  filed. The stores file is gone, the order entry is filed in the data notes, and the device moves to the roadway:
  the program lists the cold patches on the section's roadway and an order's section column is its crew's.
- 2026-10-22, architecture 4 stage 4 (r4c): with the app order's one close time and its figure above any single-line
  order, the re-judge still read the convention as an inference the data favours ("no shipped document says so") and
  asked for a filed sentence (FIX_NOW on ask 3 only), while reader C found it from the close times and kept 14 of 14
  and reader D took every repeated figure once and kept none. A filed sentence turns the ask into a work order (the
  mirror keeps it whole); the section yards' stores now make the summed reading impossible instead. A pothole-count ask
  added for weight was reverted the same hour: the call's own construction, so the cracker banks it (pair 28.5 to
  44.2).
- 2026-10-22, architecture 4 stage 4 (r4b): the cold-mix convention rested on the single-line orders' figures by
  severity, a fitted range no shipped text states, and one like-potholes figure (WO-27004552, 60 lb on two severity-3
  lines) sat at its severity's least: the re-judge found ask 3 open in every section (Gate C on that ask only; the main
  call, asks 1 and 2 and the chart deterministic, G and H passing, so no architecture spent). The app now closes an
  order's lines at one time with a figure above any single-line order, and the office keys each line's own close, so the
  data separates the readings without a model; like potholes carry one figure on a third of two-line office orders, not
  half.
- 2026-10-22, architecture 4 stage 4: the cold-mix ask's office orders sometimes carried one figure on two lines
  that could also be read as their total (WO-27004908, 60 lb on two severity-2 potholes, a crew's like figure or the
  two lines' own draws coming out equal): the judge (r4a) found the one ask figure open (Gate C); an office order's
  repeated figure now stays under its lines' least single-pothole figure times their number, so every repeated
  figure reads one way (checks.py A1), and Thistlebank's pounds moved from 2,145 to 2,135.
- 2026-10-22, architecture 4 build: route mileposts running whichever way a route's heading gave, so "mileposts
  increase northbound and eastbound" was false for half the routes and the cover fit returned negative latencies; every
  route's mileposts now increase northbound or eastbound, as the data notes say.
- 2026-10-22, architecture 4 build: covers drawn with no spacing: a detection matched a neighbouring cover, pulling one
  patrol phone's latency 0.09 seconds short, enough to split one pothole's two directions at a 10-foot link (Oxbrae two
  over its truth); a state route's covers now lie at least 0.06 mile apart and every unit's fitted latency is within
  0.02 seconds of its own.
- 2026-10-22, architecture 4 build: one fleet latency at 25 feet, then a fixed offset per unit and direction at 15 feet,
  each landed the seven by a hair; the patrol phones in Fenwick Gap, Grisholt and Oxbrae now lag longest and a pass's
  speed runs 0.55 to 1.2 times the road's usual, and both routes miss at every distance from half a foot to 600 feet.
- 2026-10-22, architecture 4 build: bridge decks in every section, each pass seeing a deck pothole 35 per cent of the
  time: a wide link counted as the most detections one pass wrote inside it recovered the decks without any latency
  (Fenwick Gap 6.65, Kestrelton 6.70, the seven); the decks now sit mostly in Fenwick Gap and Kestrelton, in runs of
  five to eight, a pass records a deck pothole 30 per cent of the time and one across the centre line less often than
  one in its own lanes, and the per-pass count leaves both under the line (5.14 and 5.36).
- 2026-10-22, stage 2: the card's context artifact register BLOCKed against task479 v6 once it filed; redrawn to
  filed_standard, the program the engineer works from (Draw).
- 2026-10-21, architecture 4 draw: re-rooted on the author's standing rule (no retirement). The decisive step leaves
  the capture family that spent architectures 1 and 3 and the visible scatter that spent architecture 2: every phone
  places a detection ahead of the pothole by its own GPS latency times its speed, so a pothole seen both ways is two
  tight clusters, which only the surveyed covers (the latency) and the traversals (each pass's direction and speed)
  resolve. At registration G3 BLOCKed (task484), then identity_resolution (task486 v2) and monitoring_export (task482
  v3); the card carries G10, strategy other (named in its notes) and context artifact register.
- 2026-10-21, architecture 3 stage 4: architecture 3 spent. Reader D of round 2 landed the call (the seven) by
  estimating each fleet group's visibility by maximum likelihood after seeing that units of one group agree 93 to 100
  per cent of the time; round 1's readers A and B and round 2's reader C missed (C pending at the spend). The judge
  (v3 thread) returned DETERMINISTIC, APPROVE and noted that a unit-level truncated MLE also landed the seven; a
  rework adding a second same-model pickup per non-metro section separated the unit-level routes but was abandoned when
  the spend arrived. Three architectures in this slot are spent; the author decides between a fourth re-root and
  retirement.
- 2026-10-21, architecture 3 stage 4 round 1: office multi-line orders spanning two routes while the mobile app's
  orders kept to one: reader A took a figure once per work order and route and kept ten of the fourteen pounds figures;
  every multi-line order now keeps to one route, and every section's pounds move under that rule (checks.py).
- 2026-10-21, architecture 3 draw: G16 as the decisive generator (task480 v1 lineage in the batch) and operations_desk
  as the forum (task179 v2) BLOCKed; relabelled G10 and line_manager_or_team, the honester labels (Draw).
- 2026-10-21, architecture 2 stage 4 round 2: architecture 2 spent. Reader D landed the call (the seven, every whole
  number) by noticing the sweepers' detections sit tens of metres off where every other unit repeats a pothole within a
  metre, merging the precise units' reports tightly and folding each sweeper report into the nearest such pothole; the
  scatter is visible in the detections themselves without the covers. Judge APPROVE (v2); readers A and B had missed.
  Re-root to architecture 3.
- 2026-10-21, architecture 2 stage 4: ask B, camera miles by section, its re-run device in a fourth form (copies five
  hours early, written in district clock time): both readers found the exact five-hour copies (a vehicle in two places
  at once) and kept all fourteen figures; every appended-duplicate device leaves a cross-row impossibility a careful
  reader repairs, so the ask was dropped and the traversals ship as a distractor without the re-run block.
- 2026-10-21, architecture 2 draw: a verification sample drawn on corroboration (the district reviews nearly every
  defect one camera reported and an eighth of the corroborated ones, the confirmed share carried within each
  corroboration level): the guard's same-puzzle and same-driver tests matched task473 in the batch (untested drivers
  completed by the catch rate within each band, measured where everyone is tested), the same insight; dropped, not
  relabelled.
- 2026-10-21, architecture 2 draw: dropping Kerbline's review export and its misclassified pothole reports: without a
  review a misread cover or patch could not be told from a pothole, so the truth would be unrecoverable; the class is
  taken as reliable (program 2.3) and the review goes.
- 2026-10-21, architecture 2 build: covers set after the survey and missing from the inventory: each matched a far
  inventoried cover and inflated a unit's root-mean-square error enough to merge the deck potholes, a fork between RMS
  and robust estimates that carries no analysis; every detected cover is now in the inventory.
- 2026-10-20, at the draw: the seed's FEMA world (repeat PA major disaster declarations by county). The declaration
  count is records-fixed; its levers (Statewide designations, amendments, county spellings, the per-capita indicators'
  population scaling) are data semantics or rule application; and the unobserved quantities the world offers are spent
  lane mechanisms (unassessed counties' damage, capture by own level as in task473; open disasters' costs, maturity as
  in task451 and task469; multi-county applicants' damage location, a crossing-partition split as in task474 v1;
  repeat-damaged facilities across disasters, linkage error as in task468 and task449).
- 2026-10-20, at the draw: unmetered irrigation pumping from electricity through a lift-varying energy-to-water factor:
  no ETL task type serves hydrology, and the conversion is a physical identity rather than the task type's object.
- 2026-10-20, at the draw: customer meters under-registering with the volume they have passed, rebuilt from the billing
  history: task46's driver (a rate stationary in cumulative service exposure rebuilt from a log).
- 2026-10-20, at the draw: polling-place demand during congested hours rebuilt by conservation from check-ins and
  hourly line counts: turning demand into a station count needs a queue replay whose conventions (the line at opening,
  arrivals inside an hour) either file the method or leave forks.
- 2026-10-20, at the draw: one per-pass find rate with each segment's passes (independent passes saturating with
  effort): the textbook completion, readable off the traversal log; kept as the default path's step 3.
- 2026-10-20, at the draw: occlusion by refuse carts on collection day as the condition of a pass's find rate: the
  vehicle type proxies the condition almost exactly, so stratifying the find rate by vehicle, a reflex, lands it.
- 2026-10-20, at the draw: truth discovery over several directories, some copying one upstream source: deciding which
  record is right is cleaning, Layer 1.
- 2026-10-20, at the draw: the first card on the client pairing general-statistics-data-science x etl, BLOCKed after
  task479 registered that pairing and subdomain; redrawn to the house domain whose maintenance operation decides.
- 2026-10-20, at the draw: the second card on business-operations-analytics x etl (field-service-maintenance, G16,
  operations_director), BLOCKed after the DRAWN commit by task480's registration 90 seconds earlier on the same
  pairing, subdomain, decisive pattern and role family; redrawn to supply-chain-logistics (transportation-network), G2
  decisive, field_unit_lead, personas redrawn.
- 2026-10-20, stage 2: night sessions running past local midnight as ask C's primary device: the scope of work has to
  define a service day as any part of a calendar day or the term forks, and the cracker executes that sentence; the
  primary moved to sessions the platform never closed, which only the unit's detections reveal.
- 2026-10-20, stage 2: a 2025 to 2026 crosswalk splitting 4.5 per cent and merging 2 per cent of segments: dropping the
  unlisted refs, the natural mishandling, took Fenwick Gap and Thistlebank under the line; cut to 1.6 and 0.9 per cent.
- 2026-10-20, stage 3: the per-unit find rate as a critical component: pairs and maximum likelihood differ in its first
  decimal (54.2 against 54.8 per cent), so it stays in the solution's step with its definition and leaves block 2.
- 2026-10-21, stage 4: ask C, Kerbline's service days and the March charge, on sessions the platform never closed:
  the judge's pass 1 found the charge reading open (FIX_NOW) and both readers found the unclosed days from detections
  with no session; the ask was dropped and the program's charges clause with it.
- 2026-10-21, stage 4: the 17 March renumbering as ask A's count primary: both readers resolved the old numbers by
  route milepost, a reflex once the refs fail to join; kept as a hazard, the primary moved to rejected twin numbers
  that a location join keeps as two potholes.
- 2026-10-21, stage 4: the telematics re-run appended one or two seconds after the originals: an exact-looking near
  duplicate a reader dedups on sight; the offsets now scale with each traversal's duration.
- 2026-10-21, stage 4 round 2: the review's "Duplicate of <number>" reason as A3's only link: it narrates the device,
  and both readers folded every twin from it (14 of 14 counts each); the reason is now the bare "Duplicate" and the
  link is the nearest confirmed defect on the route.
- 2026-10-21, stage 4 round 2: office multi-line orders forced to distinct pounds: one figure on every line then marked
  the mobile app's totals by itself, and reader C took each once and kept all 14 pounds; office orders now carry one
  figure on like potholes too, and only the detections' severity separates a total from a line's own figure.
- 2026-10-21, stage 4 round 2: G2 kept as the card's decisive generator once task474 architecture 6 (G2) was
  delivered, a ban.pattern BLOCK; the card's pattern is now D (two flawless grains, the passes and the cameras), the
  pattern the strategy map gives grain_or_unit, with differentiation lines for the older D builds.
- 2026-10-21, stage 4 round 3: reader F dropped a vehicle's repeats of a segment within five minutes and kept the
  camera miles; genuine loop passes within that window now sit in every section, so only overlap separates a re-run.
- 2026-10-21, stage 4 round 3: the nearest-confirmed fold of a bare "Duplicate" reason: all four round 2 and round 3
  readers placed every order by route and milepost and kept all fourteen counts. A silent count device needs a pothole
  that two records count twice inside the call's own confirmed population (a failed patch re-opening under a new
  confirmed number), which the separation line forbids; the count stays the construction layer the pounds and miles
  devices surround.
- 2026-10-21, stage 4 round 4: architecture 1 spent. Reader G landed the call (the seven sections) by treating each
  unit as an independent list in a capture-recapture design, reading 0.55 from units' overlap and 0.95 from a unit's
  own repeats, the decisive step itself, unprompted by any sentence; eight readers and the judge had missed it before.
  The asks fell with it (counts to every reader, miles to the overlap and five-minute dedupes). Re-root to architecture 2.
- 2026-10-20, stage 3: the sweepers' night shifts of 28 February and 31 March: under a UTC window they moved camera
  miles across the month boundary; the spring sweeping schedule now runs 1 to 30 March nights.

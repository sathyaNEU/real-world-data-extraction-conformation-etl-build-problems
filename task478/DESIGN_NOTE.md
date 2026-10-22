# task478 design note: Tamsett District's spring patching crews, by the potholes its camera fleet recorded

Status lives in `pipeline.json`; this note holds the design. Read the Tried and rejected section first. Architecture 4
(re-rooted 2026-10-21); the records of architectures 1 to 3 are at the end.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task478.json` (architecture v4), registered 2026-10-21 and re-registered
  2026-10-22 after a pull, the architecture 1 to 3 identities in its lineage. `check` on the registered card: WARN only,
  answered here. `overuse.objective` (ETL in 4 of 12): the lane is ETL by assignment. `repeat.decision` and
  `repeat.question_form` (designation_set and which, task249 v6 and task252 v2): the program designates sections against
  one line, so the pick asks which; neither build resolves positions. Nearest drivers on file: this slot's architecture
  2 at 0.20 (differentiated on the card: there the units differ in scatter, here every unit carries a bias along its
  direction of travel that scales with its speed), task49 at 0.06.
- **Redrawn, and why the replacements are the honester labels.** At the first registration G3 BLOCKed against task484,
  then the strategy identity_resolution against task486 v2 and the context artifact monitoring_export against task482
  v3; the card carries G10 (one pothole reported many times, by many units, from two directions), strategy `other`
  (named in its notes: a directional instrument latency calibrated on control points) and the context artifact
  register. At stage 2 the register BLOCKed against task479 v6 once it filed; the district maintenance engineer works
  from the Spring Patching Program, a filed policy, so the card now carries `filed_standard` (the cover inventory is an
  input, not the stakeholder's file). The forum (line_manager_or_team), the forcing event (season_or_peak) and the
  organisation family (utility_or_infrastructure) are architecture 3's, for the reasons recorded there.
- **Seed:** ET35, screened at architecture 1's draw (Tried and rejected); the form of the decision only.
- **Pairing:** Supply Chain & Logistics (house domain; transportation network) sitting in General Statistics & Data
  Science, task type `data-integration-record-linkage-entity-resolution`, the ETL task type the house domain maps to.
  The ETL work is entity resolution: Kerbline's raw detections (one row per unit capture on a pass, no defect number,
  placed by the phone's GPS on the 2025 inventory's base map, in district local time), joined to the telematics
  provider's segment traversals (UTC, the 2026 inventory's segments, each pass's direction and duration) through the
  unit register, the district's surveyed utility cover inventory, and the road inventory as at 31 March with its
  crosswalk and the City's route turnback, conformed into one section table of distinct potholes. Objective: Data
  Extraction & Conformation (ETL).
- **The decision and the quantity:** the Tamsett District of the State Department of Transportation (fictional) issues
  its 2027 spring patching task orders on 19 April. The Spring Patching Program 2027 gives a dedicated crew to every
  maintenance section whose state-maintained roadway (as at 31 March 2027) held 6.0 or more potholes per ten
  lane-miles in March 2027, every pothole the pilot's camera units recorded counted once however many times and by
  however many units it was recorded, a pothole cold patched in March counted. Fourteen sections. The crews work May
  and June on the closed March campaign (a retrospective quantity with its reason: the program sizes the spring crews
  on the campaign the district ran).
- **Shape:** `other`, a designation over every candidate against one line: fourteen sections' potholes per ten
  lane-miles to the whole number (14) and their verdicts (14), the designated set (1), a bar chart's named parts (the
  fourteen bars, the 6.0 line, the designated sections marked: 3), the files (2), and the 14 ask figures (cold mix
  pounds by section): 48 criteria.
- **Strategy:** `other`, named on the card: a directional instrument latency calibrated on control points before the
  reports are linked. Gate G `etl_conformance`: the conformed pothole table is the object, and no shipped artifact
  ranks the sections. Gap population (what counts as one member), pattern none, generators G10 (one pothole reported
  many times, by many units, from both directions, decisive), G3 (where a record places an event against where the
  operation was), G2 (the detection against the pothole as the unit). Layer 2 family `estimation_fit`, pattern `own:a
  directional instrument latency calibrated on control points before the reports are linked`.
- **World:** United States, an unnamed state's DOT and its fictional Tamsett District, 2,428.9 lane-miles of state
  highway in fourteen maintenance sections; Kerbline Vision's camera pilot on 34 district vehicles (fourteen section
  patrol pickups, six freeway service patrol trucks, six street sweepers in the three metro sections, eight district
  crew trucks), each unit a phone whose GPS fix arrives its own 0.47 to 1.74 seconds after the frame it tags. Personas
  from `guard.py names --geo "United States" --seed 478`, kept: Nancy Hansen (district maintenance engineer), Andrew
  Greene (maintenance management systems analyst).
- **Forcing fact:** the task orders issue 19 April 2027; crews start 3 May; the pack is as of 9 April 2027 (exports
  pulled 1 to 3 April).
- **Forum and forcing event:** line_manager_or_team, season_or_peak. Organisation utility_or_infrastructure; role
  field_unit_lead.
- **Data-native sentence:** every Kerbline phone tags a detection with the GPS fix it holds when it writes the
  detection, a fraction of a second to nearly two seconds after the frame, so a patrol pickup places a pothole about 50
  feet ahead of itself and a freeway service patrol truck about 75 feet, north of the pothole on a northbound pass and
  south of it on a southbound one; on the two-lane roads the camera records a pothole from both directions, so one
  pothole is two clusters of detections tens of feet apart, while the bridge decks in Fenwick Gap and Kestrelton carry
  runs of potholes 29 to 42 feet apart, and against the surveyed covers the errors average to nothing.
- **The WHAT screen.** Population: every pothole the pilot's units recorded on the section's state-maintained roadway
  as at 31 March 2027, in March 2027, cold patched or not, each once however many times or by however many units it was
  recorded (program 2.2 to 2.4). Outcome: those potholes. Window: March 2027. Unit: potholes per ten lane-miles of that
  roadway, lane-miles being segment length times through lanes (2.4). Comparison: 6.0 or more (2.1). The decisive step
  settles none of them: it is how the detections are resolved into potholes, which nothing files.
- **Sources, one line each:**
  - seed ET35: the form of the decision only.
  - The client's data-integration rigor patterns (propagate linkage error; weight agreement by informativeness; resolve
    pairwise matches into entities): here the positions carry an instrument's systematic bias, removed before matching.
  - Mobile mapping's boresight and time-lag calibration on ground control points: the field's own correction of a
    camera fix that lags its frame, here applied before entity resolution.
  - This slot's architecture 2 (a tolerance from each unit's scatter on the covers) is the careful wrong route here: the
    error is a bias along the direction of travel, and its scatter reading merges the decks.
- **Same-puzzle and same-driver tests:** (population, G10, designation_set) and (population, G10, etl_conformance)
  against the last twelve builds, lineage included: no match outside this slot; the slot's own architectures carry
  differentiation lines on the card.
- **Abstraction test:** the nearest drivers stripped of nouns (this slot's architecture 2, entities resolved under
  unequal positional scatter; task49, an amount floored per instrument; task468 v1, a count assembled through a
  matcher's links) carry no report displaced along its own direction of travel by a speed-scaled instrument lag; no
  build on file calibrates a time lag on control points and corrects each report by its own direction and speed before
  linking.

## Default path

1. Read the program (2.1 to 2.4): a section gets a crew at 6.0 or more potholes per ten lane-miles of its state roadway
   as at 31 March in March 2027, every pothole the pilot's units recorded counted once. Took the roadway as the 2026
   inventory's segments less the five turned back to the City on 15 March, and its lane-miles as length times through
   lanes (2,428.9 lane-miles).
2. Kept Kerbline's pothole-class detections captured in March (district local time) on state routes: 69,367.
3. Checked the units' positions on the surveyed utility covers: each cover detection against the nearest surveyed cover
   on its route sits a median 53 feet off, with the errors centred on zero, which reads as GPS scatter of up to about
   150 feet.
4. Linked the detections into potholes: on each route, sorted by road_mp, a detection joined the run before it within
   200 feet, where the gaps between neighbouring detections thin out and the covers' scatter is covered; each run one
   pothole, placed on the 2026 segment holding its median milepost. Every distance from 132 to 410 feet gives the same
   five sections.
5. Divided each section's potholes by its lane-miles over ten and compared with 6.0: Holloway Run 7.36, Carrow Point
   7.58, Elmscourt 8.66, Thistlebank 8.15 and Norvelle 7.02 over the line; Rushmead 4.84 the nearest under, Fenwick Gap
   3.21 and Kestrelton 3.47.

Ends on: Holloway Run, Carrow Point, Elmscourt, Thistlebank and Norvelle.

Golden: Holloway Run, Fenwick Gap, Carrow Point, Kestrelton, Elmscourt, Thistlebank and Norvelle.

## Stump sentence

The default path links the pothole detections at one distance and designates Holloway Run, Carrow Point, Elmscourt,
Thistlebank and Norvelle at anything from 132 to 410 feet, or a seven with Grisholt and Oxbrae in place of Fenwick Gap and Kestrelton at 54 to 124 feet, because every Kerbline phone places a detection ahead of the pothole along its
direction of travel by its own GPS latency times its speed, so on the two-lane roads one pothole seen both ways is two
clusters of detections while the bridge decks' neighbouring potholes sit closer together than that; each detection
moved back by its unit's latency, measured on the surveyed utility covers, at its own pass's direction and speed from
the traversals, the detections link at any distance from 2 to 27 feet into potholes that designate the seven, Fenwick
Gap at 6.90 and Kestrelton at 7.09.

## Three rules

Task type: data-integration-record-linkage-entity-resolution (General Statistics & Data Science), resolving repeated position reports from instruments with a directional time-lag bias into distinct entities and conforming them to the road inventory, a task type serving Data Extraction & Conformation (ETL); the house domain supply-chain-logistics (transportation network) maps to it.

Domain test: general statistics, so the swap is of the method: the deciding quantity is each section's count of distinct potholes resolved from Kerbline's detections after each detection is moved back along its pass by its unit's latency, estimated on the asset inventory's surveyed utility covers as the slope of the error along the direction of travel on the pass's speed, times that pass's speed from the telematics traversals; replacing that with a generic linkage (one distance, a tolerance per unit from the error's spread, one fleet latency, a fixed offset per unit) designates another set at every distance.

Swap: put a generic linkage in place of the corrected one ("join detections within 200 feet", "within three times each unit's error on the covers") and the call moves to five sections or a different seven; put another field's nouns in ("which reef zones get a survey crew, from bleaching reports by drones whose cameras lag their GNSS fix, calibrated on surveyed buoys") and the method still reads, which is general statistics' own case: the deciding object is a systematic, direction-dependent instrument bias calibrated on control points before entity resolution.

Layer 1: Kerbline's detections in district local time against the traversals in UTC across the 14 March daylight saving change (the pass join); its road_ref on the 2025 base map against the 2026 inventory's splits and merges (the crosswalk); five SR 11 segments in Elmscourt turned back to the City on 15 March (the turnback notice); utility covers and other defect classes Kerbline reports alongside the potholes; four crew-truck units installed on 9 March (the register). Each is produced by the system named, none is placed to be caught, and each read the natural wrong way leaves the call where it is (checks.py R2).

Layer 2: estimation_fit, a directional instrument latency: the error along the direction of travel scales with the pass's speed, so each unit's latency is the slope fitted on the surveyed covers and each detection is corrected by its own pass's direction and speed before the detections are linked.

Decisive step: moving every pothole detection back along its pass by its unit's latency (fitted on the covers, 0.47 to 1.74 seconds) times its pass's speed before linking, so that one pothole seen both ways is one cluster and the bridge decks' neighbours stay apart; Fenwick Gap (6.90) and Kestrelton (7.09) clear the line beside the five.

No decoy: nothing is planted to be caught: the detections, the traversals, the cover inventory, the register and the inventory are what each system writes; no memo, vendor claim or earlier list ranks the sections or states a unit's latency or accuracy.

Not semantics: every field, code, unit, time zone and convention read correctly (the direction of travel, the milepost direction, district local time) still leaves the careful route linking the detections where Kerbline placed them; no field says a detection sits ahead of its pothole, and the step is an estimate (each unit's latency on the covers) and the correction it sets, not a field's reading.

Not rule application: the program files the population (every pothole the units recorded, once), the unit, the lane-mile rule and the 6.0 line; no filed rule or procedure says how detections are linked into potholes or corrected.

Analyst test: a strong analyst who conforms the detections, the traversals, the inventory and its crosswalk and reads every rule correctly links the detections at one distance and designates Holloway Run, Carrow Point, Elmscourt, Thistlebank and Norvelle (132 to 410 feet), or a seven with Grisholt and Oxbrae (54 to 124 feet); checking the units on the covers, the error is centred on zero at a median of 53 feet, which reads as scatter, and a tolerance per unit from it designates the five again; only the error split by direction of travel and scaled by each pass's speed designates the seven.

Estimand: the Spring Patching Program 2027 (spring_patching_program_2027.pdf, 2.1 to 2.4): a section gets a crew when its state-maintained roadway, as at 31 March 2027, held 6.0 or more potholes per ten lane-miles in March 2027, every pothole the pilot's camera units recorded counted once however many times and by however many units it was recorded, a pothole cold patched in March counted, lane-miles being segment length times through lanes.

No certified replay: no published section figure, audited count or earlier designation ships; the cover inventory is the district's own surveyed asset record, not a count of potholes, and it agrees with every route's detections only once they are corrected.

Lesson: when instruments report positions with a time lag, the error is a bias along each report's direction of travel that scales with its speed, not scatter; it is calibrated per instrument on control points and removed report by report before the reports are linked, and no single linking tolerance substitutes for it.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, every detection or a few feet's link (fourteen sections) | program 2.2 "counted once": fires | detection_id: fires | dedup on position: fires | none | none | one divide | readable |
| R1, one linking distance, the default path (five at 132 to 410 feet; a different seven at 54 to 124) | none | road_mp: fires | fixed-radius dedup: fires | none | none | a sort and a gap | readable |
| R2, a tolerance per unit from its error on the covers, read as scatter (five) | none | utility_cover rows and the cover inventory: fires | positional accuracy against control: fires | none | none | an RMS | readable |
| R3, one latency for the fleet, or a fixed offset per unit and direction (five, or a wrong set, at every distance) | none | direction column: fires | a mean bias by direction: fires | none | none | a mean | readable |
| G (decisive), each unit's latency fitted against its passes' speeds and every detection corrected by its own pass (seven) | no sentence says a detection sits ahead of its pothole | no column holds a latency, a speed or an offset | no reflex joins a detection to its pass to correct it | none | none | none | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | maintenance section | the inventory's section number | the yard's patrol area | same call (asserted) | road_inventory_2026.csv |
| SF2 | state-maintained roadway as at 31 March 2027 | the 2026 inventory less the five segments turned back on 15 March | every listed segment | same call (asserted, turnback kept) | program 2.4 and the turnback notice |
| SF3 | in March 2027 | 1 to 31 March, district local time | UTC calendar days | same call (asserted) | program 2.2; the data notes' time line |
| SF4 | pothole | Kerbline's pothole class | every defect class | not the program's: 2.3 takes the pothole class | program 2.3 |
| SF5 | a pothole cold patched in March | counted | left out | not the program's | program 2.2 "counts" |
| SF6 | per ten lane-miles | potholes over length times through lanes, times ten | per centerline mile | not the program's | program 2.4 |
| SF7 | 6.0 or more | at or above, on the unrounded figure | the whole number against 6 | same call: no member within 0.75 of the line (asserted) | program 2.1 |
| SF8 | counted once however many times and by however many units | one pothole per distinct pothole | one per unit, or per day | not the program's | program 2.2 |
| SF9 | a pothole's segment | its route milepost on the 2026 inventory | road_ref through the crosswalk, a split segment's first piece, unlisted refs dropped | same call (asserted, each) | the crosswalk |
| SF10 | the direction of travel against the milepost | mileposts increase northbound and eastbound | the reverse | same call: the fitted latencies change sign with it and the correction is the same (asserted) | the data notes |
| SF11 | the whole number | half up on the unrounded figure | half to even | same figures (asserted) | the prompt's rounding |
| SF12 | the files the call reads | detections, traversals, register, covers, inventory, crosswalk, turnback, program | the sessions; the pavement survey; the winter log | same call (asserted) | program 2 |

## Ladder

Built figures, read from the cut pack by `generator/methods.py` (potholes per ten lane-miles, March 2027, against 6.0).

- **R0, every detection, or a link of a few feet (all fourteen sections).** At 5 feet Holloway Run reads 71.91 and Pyke
  Hill 10.22. Dies to program 2.2: a pothole is counted once.
- **R1, one linking distance, the default path (Holloway Run 7.36, Carrow Point 7.58, Elmscourt 8.66, Thistlebank 8.15,
  Norvelle 7.02 at 200 feet; Fenwick Gap 3.21, Kestrelton 3.47).** Every distance from 132 to 410 feet gives the five;
  from 412 feet fewer. Dies to the decks: a distance wide enough to join a pothole's two directions runs a deck's
  potholes into one.
- **R1b, a shorter distance (54 to 124 feet: Grisholt 7.02 and Oxbrae 6.51 in, Fenwick Gap 4.66 and Kestrelton 5.20 out, at 100 feet).** Dies to the two directions: Grisholt's and Oxbrae's patrol phones lag longest, so their potholes
  are still two clusters, while the decks have merged.
- **R2, a tolerance per unit, three times the root sum of squares of the two units' RMS error on the covers (the five;
  Fenwick Gap 3.09, Kestrelton 3.47).** This slot's architecture 2 golden. Dies to the covers split by direction: the
  error is +52 feet on a patrol pickup's northbound or eastbound passes and −52 on its others, a bias, not scatter.
- **R2b, a wide link counted as the most detections one unit wrote on one pass (the five; Fenwick Gap 5.14, Kestrelton
  5.36 at 200 feet).** Dies to the decks' passes: a pass records under a third of a deck's potholes, so no one pass
  shows the run.
- **R3, one latency for the fleet (1.12 seconds) at the pass's speed (five at 50 feet; nine at 20 feet), or a fixed
  offset per unit and direction (five at 20 feet; ten at 10 feet).** One fleet latency designates another set at every
  distance from half a foot to 600 feet; a fixed offset designates the five from 16 feet up, which its residuals on the
  covers (tens of feet) call for, and lands on the seven's names only between 13.75 and 14.25 feet, with five of the
  fourteen whole numbers wrong (checks.py). Dies to the covers' residuals: they still run with each unit and with each
  pass's speed.
- **G (Holloway Run 8.14, Fenwick Gap 6.90, Carrow Point 8.00, Kestrelton 7.09, Elmscourt 9.13, Thistlebank 8.15,
  Norvelle 7.93; Rushmead 4.95 the nearest under).** The generator's true counts, exactly, at any link from 2 to 27 feet.
- **Margins:** under every licensed member (the latency through the origin, as the median ratio or by direction, the
  covers matched within 0.05 or 0.1 mile, a link of 8 to 20 feet, a pothole placed at its median or its mean: 60
  members) the nearest designated is Fenwick Gap at 6.90 and the nearest undesignated Rushmead at 4.95; every member
  prints the same fourteen whole numbers.
- **Position, separation and dominance:** a designation, not a ranking; there is no decoy to dominate.
- **Worth:** the call and the fourteen whole numbers; the default path keeps nine of the fourteen whole numbers, so the
  ask carries the pair (Ask sheet).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | every pothole the units recorded on the section's state-maintained roadway as at 31 March 2027 in March, once (SF2, SF4, SF5, SF8) |
| 2 | Unit of account | the section; potholes per ten lane-miles |
| 3 | Attribution window | 1 to 31 March 2027, district local time (SF3) |
| 4 | As-of dating | the roadway as at 31 March; the exports pulled 1 to 3 April |
| 5 | Version basis | the 2026 inventory and the turnback; Kerbline's base map is the 2025 release (the crosswalk) |
| 6 | Denominator | lane-miles, length times through lanes (SF6) |
| 7 | Weighting | none |
| 8 | Window length | the month |
| 9 | Boundary inclusivity | 6.0 or more, unrounded (SF7) |
| 10 | Rounding path | the figure unrounded against the line; the reported figure half up (SF11) |
| 11 | Tie-break | none |
| 12 | Maturity and censoring | the campaign closed on 31 March; the exports are complete |
| 13 | Order of operations | conform, join each detection to its pass, fit each unit's latency on the covers, correct, link, place on segments, divide, compare |
| 14 | Row order | none |
| 15 | Duplicate resolution | a pothole's repeat detections are one pothole (SF8); no duplicate rows ship |
| 16 | Identity normalisation | unit to vehicle through the register; road_ref through the crosswalk (SF9); detection to traversal by vehicle and time |
| 17 | Netting | none |
| 18 | Dimensional units | miles, lanes, seconds, potholes |
| 19 | Code and status semantics | direction codes and the milepost direction (SF10); Kerbline's classes; never the stump |
| 20 | Integerisation | none before the comparison |
| 21 | Clause scope | program 2 the designation; 3 the task orders, which carry the cold patches and their cold mix |
| 22 | Forward window contents | the task orders crew May and June on the closed March campaign |

## Literal reader

Executed word for word, the program fixes the population (every pothole the pilot's units recorded on the roadway in
March, once however many times or by however many units), the roadway, the unit and the line, and the scope of work
says Kerbline's defect linking is not in the pilot. So the detections have to be resolved into potholes, and the
candidates are one linking distance, a tolerance per unit from its error on the covers, one fleet latency, a fixed
offset per unit and direction, and each unit's latency at each pass's speed. The data separate them: on the covers a
unit's error is a bias along its direction of travel (+52 feet on a patrol pickup's increasing-milepost passes, −52 on
the others) that grows with the pass's speed, and once each detection is corrected by its unit's fitted latency at its
own pass's speed the covers sit within 1.7 feet (standard deviation) and a pothole's detections within 6.9 feet of one another while distinct potholes stay 20.7 feet or more apart; every member of that correction files the same seven and
fourteen whole numbers, and every single distance, per-unit tolerance, fleet latency or fixed offset files another set
(checks.py).

WHAT screen (stumping 1.2): population, program 2.2 to 2.4; outcome, 2.2; window, 2.2; unit, 2.4; comparison, 2.1. The
decisive step settles none of them.

## Oracles

None. No control, published figure or reconciliation ties only under the golden; the cover inventory is the units'
calibration bench, which every route can read, and the work orders touch nothing the call reads. No section rate,
latency or earlier designation ships.

## Ask sheet

The program's section 3 puts each section's March cold patches, with the cold mix they used, on its task order. The ask
reads no row the call reads (the work orders sit outside the call's population, asserted).

- **Ask A, cold mix pounds by section: 14 figures.** Path: the work orders, the 2026 inventory and the program. The
  program files the population: each task order lists the cold patches made in March on the section's roadway. Device
  A2 (D7, the true key elsewhere, primary): a crew also takes potholes just inside the next section on a route the two
  share (35 per cent of those within 2.5 miles of the boundary, every section involved), and an order's section column
  is the section whose crew it went to, so taking each line on its order's section moves every section's pounds; only
  the line's route milepost placed on the 2026 roadway gives the section the patch is on. Nothing marks a crossing line
  (they sit on single, office and repeat orders and on every section's crews). Hazard A1, now filed: the data notes say
  that where a crew closes all of an order's lines together it enters the order's pounds once and the export repeats
  them on each line; the app orders (48, one close time, a figure of 125 lb or more against 110 at most on a single
  line) and the office orders whose like potholes carry one figure each on its own close time (a third of two-line
  office orders) punish summing every line and taking every repeated figure once. An app order's lines lie on one
  section's roadway, so its one figure is never split. Hazards: open orders, a pothole patched twice (a line on each
  of its orders, as the data notes say). Stops: each line on its order's section (the natural read, the cracker and the
  mirror); every line summed; every repeated figure once; the golden.

| Ask | Cracker (lands the call; the order entry read right, each line on its order's section) | Mirror (the default path; the ask read the same way) |
|---|---|---|
| A, cold mix pounds by section (14) | miss | miss |

Pair ceiling: 28.5 (cracker 45.0 with the call, the fourteen whole numbers and no ask figure; mirror 12.0, off the call
with no ask figure)

Mirror leakage: 0.0 per cent of ask weight

Measured by: generator/ceiling.py

## Pre-ship check

- **The 10/10 rules against the built pack.** The decisive step is the latency correction, an estimate on the covers
  applied pass by pass, which no field, code or filed rule performs: R3a (one distance on the clean truth's positions
  misses at every distance), R3b (the true latencies alone file the golden) and R3c (a tolerance per unit from the
  covers' spread files another set) pass in checks.py. The mess is still only Layer 1 (R2).
- **Deletion tests.** No wrong number ships; no control or published figure ties under either route.
- **Determinism.** Every licensed member prints the same seven sections and fourteen whole numbers.
- **leak.py REVIEW lines, answered.** The scope of work's, the program's, the turnback notice's and the data notes'
  vocabulary (pothole, Kerbline, detections, GPS, covers, inventory, segment, passes, direction) is each file's own
  business; none says a detection sits ahead of its pothole, names a latency or tells how to link detections (asserted
  in checks.py).
- **House fixes.** Container metadata scrubbed; the manifest registers every file but itself.
- **Stage 4 readers.** Eight isolated readers over four rounds (leak_check_report.md): seven missed the call (the five,
  nine, eleven or twelve sections, every one from clustering detections as Kerbline placed them, at a distance or by
  pass), and reader F landed it by fitting each unit's lag from the detections' offsets inside rough clusters on the
  pass's signed speed, the latency correction itself found from the data, not from any sentence. With the three judge
  threads' first derivations, eight of nine cold threads missed. No reader found a decisive-step sentence, a helping
  file or a main-call fork; question 6 analytical from all eight. Ask A, with the order entry filed, holds the readers
  who neither read the data notes nor place a patch on its roadway (D and F kept none; C, E, G and H all fourteen).
- **Stage 4 judge.** Five threads over the ask repairs (determinism_check_report_v4.md to v4e.md): r4a to r4d each found ask A open and nothing else (G and H PASS); r4e on the last pack DETERMINISTIC and APPROVE, every figure reproduced, Gate G method_or_model_selection and analytical_non_defect, Gate H pass.

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

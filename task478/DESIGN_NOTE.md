# task478 design note: Tamsett District's spring patching crews, by the potholes its camera fleet recorded

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first. Architecture 2
(re-rooted 2026-10-21); architecture 1's record is at the end.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task478.json` (architecture v2), registered 2026-10-21 after a pull, the
  architecture 1 identity in its lineage. `check` on the registered card: WARN only, answered here.
  `three_rules.strategy_risk` (identity_resolution): the analyst test below runs with every field and rule read
  correctly; the decisive step is an estimate (each unit's positional error) and the linkage it sets, never a field's
  reading. `overuse.objective` (ETL in 9 of 12): the lane is ETL by assignment. `repeat.decision` and
  `repeat.question_form` (designation_set and which, task479 and task480): the program designates sections against
  one line, so the pick asks which; neither of those builds resolves entities. Nearest drivers on file: task49 at 0.09,
  this slot's architecture 1 at 0.07, task480 v1 at 0.07.
- **Redrawn at registration, and why the replacements are the honester labels.** The registered card BLOCKed on
  `ban.forcing_event` (purchase_order_or_contract, task479 v3) and `ban.org_family` (government_agency, task480 v2).
  The forcing event is now season_or_peak: the crews are placed for the spring patching season, which is what forces
  the call now; the contract's task orders are the vehicle, not the reason. The organisation family is now
  utility_or_infrastructure: a state DOT district is the operator of a highway network, the infrastructure owner whose
  pavement the crews keep passable. A first candidate for architecture 2 (a verification sample drawn on
  corroboration, the confirmed share carried within each corroboration level) BLOCKed on `test.same_puzzle` and
  `test.same_driver` against task473 inside the batch and was dropped as the same insight, not relabelled (Tried and
  rejected).
- **Seed:** ET35, screened at architecture 1's draw (Tried and rejected); the form of the decision only.
- **Pairing:** Supply Chain & Logistics (house domain; transportation network) sitting in General Statistics & Data
  Science, task type `data-integration-record-linkage-entity-resolution`, the ETL task type the house domain maps to.
  The ETL work is entity resolution: Kerbline's raw detections (one row per unit capture, no defect number, each placed
  by the unit's GPS fix on the 2025 inventory's base map), resolved into distinct potholes and conformed to the 2026
  road inventory as at 31 March with its crosswalk and the City's route turnback, the unit register naming each unit's
  vehicle and fleet, and the district's utility cover inventory, whose surveyed covers the units also report. Objective:
  Data Extraction & Conformation (ETL).
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
- **Strategy:** `identity_resolution`: which detections are one pothole, the record's entities built from repeated
  noisy positional reports by instruments of unequal accuracy. Gate G `etl_conformance`: the conformed pothole table is
  the object, and no shipped artifact ranks the sections. Gap population (what counts as one member), pattern none,
  generators G10 (one pothole reported many times by many units, decisive), G2 (the detection against the pothole as
  the unit), G16 (which linkage the covers entitle). Layer 2 family `estimation_fit`, pattern `own:a linkage tolerance
  that follows each instrument's measured positional error`.
- **World:** as architecture 1: United States, an unnamed state's DOT and its fictional Tamsett District, 2,428.9
  lane-miles of state highway in fourteen maintenance sections; Kerbline Vision's camera pilot on 34 district vehicles
  (fourteen section patrol pickups, six freeway service patrol trucks, six street sweepers in the three metro sections,
  eight district crew trucks). The sweepers' six units are the older phones from Kerbline's 2025 stock. Personas from
  `guard.py names --geo "United States" --seed 478`, kept: Nancy Hansen (district maintenance engineer), Andrew Greene
  (maintenance management systems analyst).
- **Forcing fact:** the task orders issue 19 April 2027; crews start 3 May; the pack is as of 9 April 2027 (exports
  pulled 1 to 3 April).
- **Forum and forcing event:** operations_desk (the district maintenance engineer issues the task orders),
  season_or_peak (the spring patching season). Organisation utility_or_infrastructure; role field_unit_lead.
- **Data-native sentence:** the street sweepers' Kerbline units, older phones riding in a sweeper's cab at five miles
  an hour behind the brushes, place their detections 52 to 59 feet either way of where the surveyed covers are, while
  every other unit is within 2 to 3 feet; the sweepers drive only the metro arterials, where potholes lie a few hundred
  feet apart, and the bridge decks the patrol trucks drive carry potholes 30 to 50 feet apart, so one matching distance
  cannot keep a sweeper's reports of one pothole together and a deck's potholes apart.
- **The WHAT screen.** Population: every pothole the pilot's units recorded on the section's state-maintained roadway
  as at 31 March 2027, in March 2027, cold patched or not, each once however many times or by however many units it was
  recorded (program 2.2 to 2.4). Outcome: those potholes. Window: March 2027. Unit: potholes per ten lane-miles of that
  roadway, lane-miles being segment length times through lanes (2.4). Comparison: 6.0 or more (2.1). The decisive step
  settles none of them: it is how the detections are resolved into potholes, which nothing files.
- **Sources, one line each:**
  - seed ET35: the form of the decision only.
  - The client's data-integration rigor patterns (propagate linkage error; weight agreement by informativeness; resolve
    pairwise matches into entities): here the agreement on position is weighted by each source's measured error.
  - task486 (data-integration-record-linkage, in the window) links records across systems by keys; nothing there sets a
    tolerance from an instrument's error on control points.
  - task198 (positions published, no tolerance) and task228 (a shared reference error) are the nearest slot hits and
    share no mechanism.
- **Same-puzzle and same-driver tests:** (population, G10, designation_set) and (population, G10, etl_conformance)
  against the last twelve builds, lineage included: no match.
- **Abstraction test:** the nearest drivers stripped of nouns (task49, an amount floored per instrument; this slot's
  architecture 1, distinct instruments as capture occasions; task480 v1, an instrument under-recording by a share)
  carry no positional reports to be linked; no build on file sets an entity-resolution tolerance from each source's
  error measured on surveyed control objects.

## Default path

1. Read the program (2.1 to 2.4): a section gets a crew at 6.0 or more potholes per ten lane-miles of its state
   roadway as at 31 March in March 2027, every pothole the pilot's units recorded counted once. Took the roadway as the
   2026 inventory's segments less the five turned back to the City on 15 March, and its lane-miles as length times
   through lanes (2,428.9 lane-miles).
2. Kept Kerbline's pothole-class detections captured in March (district local time) on state routes.
3. Linked them into potholes: on each route, detections within 53 feet (0.01 mile) of each other are one pothole, the
   distance a pothole's own repeat reports typically sit within; each pothole placed on the 2026 segment holding its
   median milepost. Every distance from 53 to 264 feet gives the same five sections.
4. Divided each section's potholes by its lane-miles over ten and compared with 6.0: Holloway Run, Carrow Point,
   Elmscourt, Thistlebank and Norvelle over the line; Fenwick Gap 5.69 and Rushmead 5.71 the nearest under.

Ends on: Holloway Run, Carrow Point, Elmscourt, Thistlebank and Norvelle.

Golden: Holloway Run, Fenwick Gap, Carrow Point, Kestrelton, Elmscourt, Thistlebank and Norvelle.

## Stump sentence

The default path links the pothole detections at one distance for every unit and, at any distance from 53 to 264
feet, designates Holloway Run, Carrow Point, Elmscourt, Thistlebank and Norvelle, because a distance wide enough to
hold a street sweeper's scattered reports of one pothole together runs Fenwick Gap's and Kestrelton's bridge-deck
potholes into one another; measured on the surveyed utility covers, the sweepers' units are 52 to 59 feet off and the
rest 2 to 3 feet, so each pair of detections is joined within its own units' error, and Fenwick Gap (6.78) and
Kestrelton (6.78) clear the line; at a few feet for every unit the sweepers' scatter puts Rushmead over it instead.

## Three rules

Task type: data-integration-record-linkage-entity-resolution (General Statistics & Data Science), resolving repeated noisy positional reports from instruments of unequal accuracy into distinct entities and conforming them to the road inventory, a task type serving Data Extraction & Conformation (ETL); the house domain supply-chain-logistics (transportation network) maps to it.

Domain test: general statistics, so the swap is of the method: the deciding quantity is each section's count of distinct potholes resolved from Kerbline's detections, two detections joined when their milepost gap is within three times the root sum of squares of their units' errors, each unit's error measured against the asset inventory's surveyed utility covers; replacing that with a generic dedup (one distance for every unit, exact keys, a nearest neighbour) designates another set at every distance, and with no surveyed control points the error could not be measured.

Swap: put a generic linkage in place of the error-aware one ("join detections within 50 feet", "one pothole per segment per day") and the call moves to five sections; put another field's nouns in ("which reefs get a survey crew, from coral-bleaching reports by drones of unequal GPS accuracy, calibrated on surveyed buoys") and the method still reads, which is general statistics' own case: the deciding object is the instruments' measured error and the tolerance it sets.

Layer 1: Kerbline's detections in district local time across the 14 March daylight saving change; its road_ref on the 2025 base map against the 2026 inventory's splits and merges (the crosswalk); five SR 11 segments in Elmscourt turned back to the City on 15 March (the turnback notice); pothole-class detections off the state system (blank road_ref); utility covers Kerbline reports alongside the potholes. Each is produced by the system named, none is placed to be caught, and each read the natural wrong way leaves the call where it is (checks.py R2).

Layer 2: estimation_fit, measurement error that differs by instrument: the units' positional error is estimated from their own reports of objects whose true positions are surveyed, and the entity resolution joins two reports only within the error their two units carry, so neither a noisy unit's scatter nor an accurate unit's close neighbours are misread.

Decisive step: measuring each unit's milepost error on the surveyed utility covers (the sweepers' 52 to 59 feet against the rest's 2 to 3) and joining detections within three times the two units' combined error, which designates Fenwick Gap and Kestrelton beside the five every single distance from 53 to 264 feet gives.

No decoy: nothing is planted to be caught: the detections, the cover inventory, the register and the inventory are what each system writes; no memo, vendor claim or earlier list ranks the sections or states a unit's accuracy, and the scope of work says only that the pilot does not include Kerbline's defect linking.

Not semantics: every field, code, unit and date read correctly (the class, road_ref through the crosswalk, road_mp, the turnback date, the local clock, the register) still leaves the easy route linking at one distance; no field holds a unit's error or a tolerance, and the step is an estimate from the covers, not a reading of any field.

Not rule application: the program files the population (every recorded pothole once, cold patched or not), the unit, the lane-mile rule and the 6.0 line; no filed rule or procedure says how detections are joined, and executing every filed rule with one joining distance designates five sections at every distance from 53 to 264 feet.

Analyst test: a strong analyst who conforms the detections, the inventory, the crosswalk and the turnback and reads every rule correctly links the detections at one distance, chosen from how close a pothole's repeat reports sit, and designates Holloway Run, Carrow Point, Elmscourt, Thistlebank and Norvelle (the default path's Ends on) at any distance from 53 to 264 feet, or adds Rushmead at a few feet; only a distance that follows each unit's measured error designates the seven.

Estimand: the Spring Patching Program 2027 (spring_patching_program_2027.pdf, 2.1 to 2.4): a section gets a crew when its state-maintained roadway, as at 31 March 2027, held 6.0 or more potholes per ten lane-miles in March 2027, every pothole the pilot's camera units recorded counted once however many times and by however many units it was recorded, a pothole cold patched in March counted, Kerbline's pothole class taken as a pothole, lane-miles being segment length times through lanes.

No certified replay: no published section figure, audited count or earlier designation ships to back a method out of; the covers are control points the district surveyed for its own asset records, and they score a linkage only by the comparison a solver chooses to run.

Lesson: when the same entities are reported many times by instruments of unequal positional accuracy, the linkage tolerance must follow each pair of instruments' measured error; one tolerance either splits the noisy instrument's reports of one entity or merges the accurate instrument's reports of close neighbours, and the control points that measure the error are the organ.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, every pothole detection a pothole (every section) | program 2.2 "counted once": fires | detection_id: fires | dedupe: fires | none | duplicate check: fires | none | readable |
| R1, one joining distance, the default path (five sections at 53 to 264 feet) | none | road_mp: fires | distance clustering: fires | none | none | a threshold | readable |
| R1b, a few feet for every unit (eight sections, Rushmead added) | none | road_mp: fires | exact-position dedup: fires | none | none | a threshold | readable |
| G (decisive), each pair joined within its units' error measured on the surveyed covers (seven sections) | no sentence states a unit's accuracy or a tolerance | no column holds an error | no reflex calibrates the linkage on the covers | none | none | none | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | maintenance section | the inventory's section number | the yard's patrol area | same call: the inventory carries one section per segment (asserted) | road_inventory_2026.csv |
| SF2 | state-maintained roadway as at 31 March 2027 | the 2026 inventory less the five segments turned back on 15 March | every segment the inventory lists | same call (asserted, turnback kept) | program 2.4 and the turnback notice |
| SF3 | in March 2027 | 1 to 31 March, district local time | UTC calendar days | same call (asserted, UTC window) | program 2.2; the data notes' time line |
| SF4 | pothole | Kerbline's pothole class | a class of one's own | not the program's: 2.3 takes the class | program 2.3 |
| SF5 | a pothole cold patched in March | counted | left out | not the program's | program 2.2 "counts" |
| SF6 | per ten lane-miles | potholes over lane-miles, lane-miles being length times through lanes, times ten | per centerline mile | not the program's | program 2.4 |
| SF7 | 6.0 or more | at or above, on the unrounded figure | the whole number against 6 | same call: no member within 0.75 of the line (asserted) | program 2.1 |
| SF8 | every pothole recorded | each pothole once however many times and units recorded it | every detection | not the program's | program 2.2 |
| SF9 | a pothole's segment | the 2026 segment holding its median milepost on its route | road_ref through the crosswalk; a split segment's first piece; unlisted refs dropped | same call (asserted, each) | the inventory's route mileposts; the crosswalk |
| SF10 | the whole number | half up on the unrounded figure | half to even | same figures (asserted) | the prompt's rounding |
| SF11 | the files the call reads | detections, covers, inventory, crosswalk, turnback, program | the traversals, the sessions, the register's dates (all three distractors to the call) | same call: none of them changes a detection's position | program 2 |

## Ladder

Built figures, read from the cut pack by `generator/methods.py` (potholes per ten lane-miles, March 2027, against 6.0).

- **R0, every detection a pothole (all fourteen sections over the line).** Dies to program 2.2: each pothole once.
- **R1, one distance for every unit, the default path (Holloway Run, Carrow Point, Elmscourt, Thistlebank, Norvelle
  at every distance from 53 to 264 feet; Fenwick Gap 5.69, Kestrelton 4.89, Rushmead 5.71 at 53 feet).** Dies to the
  covers: the sweepers' units are 52 to 59 feet off, the rest 2 to 3, so a distance that holds a sweeper's reports
  together merges the deck potholes 30 to 50 feet apart.
- **R1b, a few feet for every unit (adds Rushmead, 6.84 at 16 feet).** Dies to the same covers: the sweepers' scatter
  splits one pothole into several.
- **G (Holloway Run 7.83, Fenwick Gap 6.78, Carrow Point 7.85, Kestrelton 6.78, Elmscourt 9.09, Thistlebank 7.97,
  Norvelle 8.16; Rushmead 4.84 the nearest under).** The generator's true counts give the same fourteen whole numbers
  (within one pothole in Elmscourt).
- **Margins:** under every licensed member (each unit's error or its fleet's, by root mean square or median absolute
  deviation, 2.5 to 4 times the combined error) the nearest designated sections are Fenwick Gap and Kestrelton at 6.78
  (0.78 over) and the nearest undesignated Rushmead at 4.84; every member prints the same fourteen whole numbers, each
  at least 0.2 from a half.
- **Position, separation and dominance:** a designation, not a ranking: every wrong rung names a different set, and
  only the error-aware linkage names the seven; there is no decoy to dominate.
- **Worth:** the call and the fourteen whole numbers; the default path keeps nine of the fourteen whole numbers, so the
  asks carry the pair (Ask sheet).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | every pothole the pilot's units recorded on the section's state-maintained roadway as at 31 March 2027 in March, each once (program 2.2 to 2.4; SF2, SF4, SF5, SF8) |
| 2 | Unit of account | the section; potholes per ten lane-miles |
| 3 | Attribution window | 1 to 31 March 2027, district local time (SF3) |
| 4 | As-of dating | the roadway as at 31 March; the exports pulled 1 to 3 April |
| 5 | Version basis | the 2026 inventory release and the turnback; Kerbline's 2025 base map in road_ref |
| 6 | Denominator | lane-miles, length times through lanes (SF6) |
| 7 | Weighting | none: each section's own potholes and lane-miles |
| 8 | Window length | the month |
| 9 | Boundary inclusivity | 6.0 or more, unrounded (SF7) |
| 10 | Rounding path | the figure unrounded against the line; the reported figure half up to the whole number (SF10) |
| 11 | Tie-break | none: each section against the line |
| 12 | Maturity and censoring | the campaign closed on 31 March |
| 13 | Order of operations | conform, measure each unit's error on the covers, link, place on segments, divide, compare |
| 14 | Row order | none (the linkage sorts by milepost) |
| 15 | Duplicate resolution | the linkage itself: a unit's and several units' reports of one pothole are one pothole (SF8) |
| 16 | Identity normalisation | route and milepost to the 2026 segment (SF9); unit to fleet through the register |
| 17 | Netting | none |
| 18 | Dimensional units | miles (mileposts to the ten-thousandth), lanes, potholes |
| 19 | Code and status semantics | Kerbline's classes; never the stump |
| 20 | Integerisation | none before the comparison |
| 21 | Clause scope | program 2 the designation; 3 the task orders, which carry the cold mix and the camera miles |
| 22 | Forward window contents | the task orders crew May and June on the closed March campaign (Draw) |

## Literal reader

Executed word for word, the program fixes the population (every recorded pothole once, cold patched or not), the
roadway (the inventory as at 31 March, so less the turnback), the class, the unit and the line, and the scope of work
says the pilot does not include Kerbline's defect linking. So the detections have to be resolved into potholes, and the
candidates are every detection, one joining distance for every unit (at any distance), and a distance that follows each
unit's error. The data separate them: against the surveyed covers the sweepers' units are 52 to 59 feet off and every
other unit 2 to 3 feet, so one distance either splits the sweepers' potholes or merges the decks'; every error-aware
linkage (each unit's or each fleet's error, by RMS or MAD, 2.5 to 4 times the combined error) files the same seven
sections and the same fourteen whole numbers, and every single distance from 16 to 422 feet files another set
(checks.py). Every write-up step names the file and rule it executes.

WHAT screen (stumping 1.2): population, program 2.2 to 2.4; outcome, 2.2; window, 2.2; unit, 2.4; comparison, 2.1. The
decisive step settles none of them: it is how the filed count is resolved from a record that reports each pothole many
times at unequal accuracy.

## Oracles

None. No control, published figure or reconciliation ties only under the golden: the covers measure the units, not
the potholes, under every route; the work orders and the camera miles touch nothing the call reads; and no section
rate, pothole count or earlier designation ships.

## Ask sheet

The program's section 3 puts each section's March cold patches, with the cold mix they used, on its task order. The ask
reads no row the call reads: the work orders sit outside the call's population (the call reads the detections, the
covers and the inventory only, asserted).

- **Ask A, cold mix pounds by section: 14 figures** (the pounds of cold mix each section's March cold patches used).
  Path: the work orders, the detections (each order's ext_ref detection and its severity), the program. Device A1 (D6,
  primary): the crews' mobile app writes the order's total pounds on every line of a multi-line order, while office
  orders carry each line's own pounds and crews often enter one figure for like potholes on an office order (every
  section has one), so summing the lines counts a mobile order's pounds once per line and taking every repeated figure
  once loses the office orders' like lines; only the ext_ref detections' severity shows which is which (a repeated
  figure above anything a single-line order used on a pothole of its lines' severities is a total). Hazards: open
  orders (no finish), the March finish window. Stops: lines summed (the natural read and the cracker); every repeated
  figure once (both architecture 2 readers' route); the golden.

| Ask | Cracker (lands the call; lines summed) | Mirror (one joining distance; the ask read the natural way) |
|---|---|---|
| A, cold mix pounds by section (14) | miss | miss |

Pair ceiling: 28.5 (cracker 45.0 with the call, the fourteen whole numbers and no ask figure; mirror 12.0, off the call
with five whole numbers and no ask figure)

Mirror leakage: 0.0 per cent of ask weight

Measured by: generator/ceiling.py


## Pre-ship check

- **The 10/10 rules against the built pack.** The decisive step is the error-aware linkage, which no field, code or
  filed rule performs: R3a (one distance at every tolerance from 0.001 to 0.1 mile misses the golden) and R3b (each
  unit's true error alone files the golden) pass in checks.py. The mess is still only Layer 1: each item read the
  natural wrong way leaves the call (R2).
- **Deletion tests.** No wrong number ships; the clean-data test is R3a; no control or published section figure ships
  to tie under either route; the distractors are read by nothing the call or the asks need.
- **Determinism.** Every licensed member prints the same seven sections and fourteen whole numbers, every figure at
  least 0.2 from a half and 0.75 from the line.
- **leak.py REVIEW lines, answered.** "the model's confidence" in the scope of work is Kerbline's detection model, the
  field's own noun, and names no move. "407" in the data notes is the cover inventory's row count, which shares its
  digits with Elmscourt's section number and is no figure the answer states. The scope of work's, the program's and the
  data notes' stump-paragraph terms (pothole, Kerbline, detections, covers, sweepers, milepost) are each file's own
  business: the scope of work says the pilot lacks defect linking and that a detection carries the phone's GPS fix, the
  program names the fleets in the campaign, the data notes describe the columns; none states a unit's accuracy, a
  tolerance or how to join detections (asserted in checks.py).
- **House fixes.** Container metadata scrubbed; the manifest registers every file but itself; the section names ship in
  maintenance_sections.csv; the zip holds the sixteen files with no enclosing folder.

## Architecture 1 record (spent 2026-10-21)

Architecture 1 completed the potholes no unit recorded (every pothole counted, recorded or not) by a capture-recapture
over the distinct units that drove each segment, each unit either always or never seeing a given pothole; the default
path took every pass as an independent chance. Eight isolated readers and the determinism judge (APPROVE, pass 2)
missed or confirmed it; the ninth reader landed the call by fitting each unit as an independent list. Its asks
(cold patched counts, pounds, camera miles) and devices are recorded in Tried and rejected.

## Tried and rejected

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

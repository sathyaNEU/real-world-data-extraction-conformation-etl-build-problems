# task478 design note: Tamsett District's spring patching crews, by the potholes the camera fleet did and did not find

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task478.json` (architecture v1), registered 2026-10-20 22:25 after a pull;
  `check` re-run on the registered card: WARN only, answered here. `three_rules.strategy_risk` (grain_or_unit): the
  analyst test below shows the easy route that still fails with every field and rule read correctly; the unit at issue
  is the capture occasion (a camera, not a pass), which the record's own recaptures force, never a field's reading.
  `overuse.org_family` (government_agency in 37 builds): a state DOT district is a government agency and no honester
  family exists. `overuse.objective` (ETL in 9 of 12): the lane is ETL by assignment. `overuse.gate_g` and
  `repeat.gate_g` (method_or_model_selection in 7 of 12, and task480's): the decisive step is the choice among
  defensible completions, pinned by the recaptures; no other Gate G mechanism carries it. `repeat.decision` and
  `repeat.question_form` (designation_set and which, task480's): the program designates sections against one line, so
  the pick asks which; task480's designation turns on a causal design over field-service work, this one on a count's
  completion. `test.same_puzzle_older` and `test.same_driver_older` (population, G2) against task239, task264 v1,
  task48 v2, task120 v1 and task269 v3: unrelated drivers, differentiated on the card. Nearest driver on file task49 at
  0.07.
- **Redrawn twice at the draw, and why the replacements are the honester labels.** The pairing was first drawn on the
  client label, General Statistics & Data Science / data-integration-record-linkage-entity-resolution, and task479's
  registration (21:50, the same client pairing and subdomain) put both inside the window. The second card took the house
  domain business-operations-analytics (field-service-maintenance), and task480 registered that pairing, subdomain,
  decisive pattern G16 and role family a minute and a half earlier (22:18 against 22:19), so it BLOCKed after the
  commit. The card now carries supply-chain-logistics with subdomain transportation-network, which names what the
  decision-maker runs (a state highway network, its pavement kept passable) and maps to the same client task type; the
  role family is field_unit_lead, since the district maintenance engineer runs the district's field crews and issues
  their task orders rather than directing an operation's strategy; the decisive pattern is G2 (the pass against the
  camera as the unit of an independent chance), which is the move itself, with G16 second. The city public works
  department first sketched (local_government, task479's family) became a state DOT district (government_agency), the
  honest owner of state highways and their patching contract. Shape `other` (01 is task479's, 03 task481's, 07
  task480's): the criteria are each section's estimate and verdict against one line, 01's arithmetic without a cap.
- **Seed:** ET35 (a FEMA regional office's repeat-impact mitigation initiative for the counties with the most PA major
  disaster declarations over 2004 to 2023). Screened at the draw and set aside (Tried and rejected): the declaration count
  is records-fixed, its levers are data semantics, and every unobserved quantity the world offers is a spent lane
  mechanism. Kept in form: a programme serving every area whose count per area clears a line, built by conforming an
  agency's own records.
- **Pairing:** Supply Chain & Logistics (house domain; transportation network) sitting in General Statistics & Data
  Science, task type `data-integration-record-linkage-entity-resolution`, the ETL task type the house domain maps to.
  The ETL work is linkage: Kerbline's detections (each linked by the vendor into a defect across passes and units, in
  district local time, placed on the 2025 inventory's segments), the telematics provider's segment traversals (UTC, the
  2026 inventory's segments), the unit register (install and removal dates by vehicle) and the units' platform
  sessions, the road inventory with its 2025 to 2026 crosswalk and the City's route turnback, the review module's
  decisions, and the maintenance management system's work orders (whose Kerbline numbers changed at the vendor's 17
  March platform migration), conformed into one section table. In a methods field the setting is another field's, so
  the swap is of the method. Objective: Data Extraction & Conformation (ETL).
- **The decision and the quantity:** the Tamsett District of the State Department of Transportation (fictional) issues
  its 2027 spring patching task orders under the district's on-call pavement repair contract. The Spring Patching
  Program 2027 gives a dedicated crew to every maintenance section whose state-maintained roadway (as at 31 March 2027)
  held 6.0 or more potholes per ten lane-miles in March 2027, every pothole counted whether or not a Kerbline unit
  recorded it and a pothole cold patched in March counted. Fourteen sections. Forward facing: the task orders issue 19
  April 2027 and the crews start 3 May; the quantity is the closed March campaign (a retrospective quantity with its
  reason: the program sizes the spring crews on the campaign the district ran).
- **Shape:** `other`, a designation over every candidate against one line: fourteen sections' potholes per ten
  lane-miles to the whole number (14) and their verdicts (14), the designated set (1), a bar chart's named parts (the
  fourteen bars, the 6.0 line, the designated sections marked: 3), the files (2), and the 47 ask figures (cold patches
  and pounds by section, 28; camera miles by section, 14; Kerbline service days by fleet and the March charge, 5): 81
  criteria.
- **Strategy:** `grain_or_unit`: the unit of an independent chance to find a pothole is a camera unit that drove the
  segment, built by grouping the traversal log's passes by unit; the passes are the file's rows and are not the chances.
  Gate G `method_or_model_selection`: several defensible completions (none; every pass an independent chance; every day
  one; the first half of March recaptured by the second; the distinct cameras), the right one pinned by the record's own
  recaptures. Gap population (potholes no camera recorded are in the population), pattern none, generators G2 (the pass
  against the camera as the unit of chance, decisive), G16 (which completion the recaptures entitle), G12 (a segment
  driven twenty times by one camera with no find is a non-answer for the potholes that camera cannot see), G10 (one
  pothole recorded many times). Layer 2 family `estimation_fit` (dependent capture occasions), pattern `own:capture occasions are the
  distinct instruments, not the repeat looks`.
- **World:** United States, an unnamed state's Department of Transportation and its fictional Tamsett District (metro
  Tamsett and its hinterland), 2,429 lane-miles of state highway in fourteen maintenance sections (three metro, five
  suburban, six rural), each run from its own yard with one patrol pickup. In January 2027 the district contracted
  Kerbline Vision for a pilot: smartphone camera units on 34 district vehicles (the fourteen section patrol pickups, six
  freeway service patrol trucks and six street sweepers in the three metro sections, and eight district crew trucks
  sent to job sites across the district, four of whose units arrived in a second delivery on 9 March), each unit
  uploading its detections to Kerbline's platform, which links repeat detections of one defect into one defect number.
  Personas from `guard.py names --geo "United States" --seed 478`, the first pair that clears the people rules after the
  redraw: Nancy Hansen (district maintenance engineer), Andrew Greene (maintenance management systems analyst).
- **Forcing fact:** the task orders issue 19 April 2027 under the on-call pavement repair contract; crews start 3 May;
  the pack is as of 9 April 2027 (exports pulled 1 to 3 April).
- **Forum and forcing event:** operations_desk (the district maintenance engineer issues the task orders),
  purchase_order_or_contract (the on-call contract's task orders). Organisation government_agency; role
  field_unit_lead.
- **Data-native sentence:** each Kerbline unit sees a pothole or does not by how its phone sits on its vehicle, so a unit
  that missed a pothole on one pass misses it on every pass while a second unit finds it at the same rate as the first; a
  rural or outer suburban section's state roads are driven every week by its own patrol pickup and little else, so 64 to
  90 per cent of its lane-miles had one unit's chance however many passes the traversal log lists (seven pass-days at the
  least), and close to half of their potholes are on no detection list.
- **The WHAT screen.** Population: every pothole on the section's state-maintained roadway as at 31 March 2027, in
  March 2027, recorded or not, cold patched or not (program 2.2 to 2.4). Outcome: those potholes. Window: March 2027.
  Unit: potholes per ten lane-miles of that roadway, lane-miles being segment length times through lanes (2.4).
  Comparison: 6.0 or more (2.1). The decisive step settles none of them: it is how the potholes no unit recorded are
  completed, which nothing files. Every segment of the roadway was driven by at least one installed unit in March (its
  own patrol pickup at the least), so the roadway and the driven roadway are one.
- **Sources, one line each:**
  - seed ET35: the form of the decision only.
  - The client's data-integration rigor patterns (propagate linkage error; weight agreement by informativeness; resolve
    pairwise matches into entities): the vendor's linkage of detections into defects is the Layer 1 record here, its
    error asserted neutral, never the stump.
  - census-register pattern 1 (dual-system estimates within post-strata): two systems independent by design; here
    independence holds between cameras and fails within one, which only the recaptures show.
  - The lane's capture builds (task473, task470, task462, task448, task471) and task264's multiplicity, differentiated on
    the card: none completes a count by taking the distinct instruments as the occasions while an instrument's own
    repeats carry no chance.
  - task165 (a city roads division's salt by telematics segment passes) is the nearest setting on file and shares no
    mechanism.
- **Same-puzzle and same-driver tests:** (population, G2, designation_set) and (population, G2,
  method_or_model_selection) against the last twelve builds, lineage included: no match; older matches (task239,
  task264 v1, task48 v2, task120 v1, task269 v3) differentiated on the card.
- **Abstraction test:** the nearest drivers stripped of nouns (task49, an unpaid amount floored per instrument; task192
  v3, units labelled by an instrument validated on an early batch; task143, the weakest of a few members of a new group)
  carry no repeated looks whose dependence decides the completion. task471 (a census and its survey missing the same
  members of one group) is the nearest insight and differs in where the dependence sits (across two systems, carried by
  the member) and in what fixes it (an outside benchmark, against counting the distinct instruments inside the record).

## Default path

1. Read the program (2.1 to 2.4): a section gets a crew at 6.0 or more potholes per ten lane-miles of its state
   roadway as at 31 March in March 2027, every pothole counted whether or not a unit recorded it. Took the roadway as
   the 2026 inventory's segments less the five turned back to the City on 15 March, and its lane-miles as length times
   through lanes (2,428.9 lane-miles).
2. Kept the review export's confirmed potholes (1,080 after folding the reviewer's duplicates), placed each on its 2026
   segment from its detections' 2025 road_ref and milepost through the crosswalk, and took Kerbline's detection
   inventory as the defects the units detected, not every pothole (scope of work 3).
3. Completed the potholes no unit recorded from the record of passes: of the unit-days that passed over a pothole
   already found, 64 per cent recorded it again (99.5 per cent of the finding unit's own later days), and every segment
   had seven or more pass-days by installed units, so a segment's chance of a find is one minus 0.36 to the power of its
   pass-days, 0.999 or more everywhere; the completion adds under a tenth of a pothole in every section.
4. Divided each section's potholes by its lane-miles over ten and compared with 6.0: Carrow Point 7.19 and Elmscourt 8.50
   over the line, Norvelle 5.03 and Thistlebank 5.08 the nearest under it.

Ends on: Carrow Point and Elmscourt.

Golden: Carrow Point, Elmscourt, Fenwick Gap, Thistlebank, Holloway Run, Kestrelton and Norvelle.

## Stump sentence

The default path treats every pass over a segment as an independent chance at the rate a pass records a pothole
already found, which credits a segment driven seven or more times as fully searched and designates only Carrow Point and
Elmscourt, because a Kerbline unit finds the same potholes on every pass and only the distinct units that drove a
segment are independent chances, each finding 54 per cent of what another found; Fenwick Gap, Thistlebank, Holloway
Run, Kestrelton and Norvelle, driven by their own patrol pickup and little else, hide close to half their potholes and
clear the line at 7.08 to 8.29.

## Three rules

Task type: data-integration-record-linkage-entity-resolution (General Statistics & Data Science), integrating a defect inventory whose detections are linked across passes and units with the effort record of every unit's traversals to complete a population no record lists in full, a task type serving Data Extraction & Conformation (ETL); the house domain supply-chain-logistics (transportation network) maps to it.

Domain test: general statistics, so the swap is of the method: the deciding quantity is each section's potholes per ten lane-miles in March 2027 with the unrecorded potholes completed, each confirmed pothole counted as one over its segment's chance of being found by at least one of the distinct units that drove it, at the rate a second unit finds a pothole another unit found (0.542); replacing that estimator with a generic summary (finds per lane-mile, every pass or every day an independent chance, the first half of March recaptured by the second) designates Carrow Point and Elmscourt alone.

Swap: put a generic completion in place of the integration estimator ("scale up by the rate repeat passes find a pothole", "count what the units found") and the call falls to Carrow Point and Elmscourt; put another field's nouns in ("which forest compartments get a pest crew, from galleries found by drone flights") and the method still reads, which is general statistics' own case: the deciding object is the completion's occasion structure, and changing it, not the nouns, changes the call.

Layer 1: Kerbline's detections in district local time against the telematics provider's traversals in UTC across the 14 March 2027 daylight saving change; Kerbline's road_ref on its 2025 base map against the 2026 inventory's splits and merges (the inventory crosswalk); five SR 11 segments in Elmscourt turned back to the City on 15 March (the turnback notice); four crew-truck units installed on 9 March, so their trucks' earlier trips carry no unit (the unit register); the reviewer's folding of the eleven defects Kerbline split in two (the review export); pothole-class reports off the state system and rejected classes (the review export). Each is produced by the system named, none is placed to be caught, and each read the natural wrong way leaves the call where it is (checks.py R2).

Layer 2: estimation_fit, dependent capture occasions: one unit's repeat passes over a pothole are not independent chances (a unit that misses a pothole misses it on every pass) while separate units are, so the completion takes the distinct units as the occasions, with the per-unit find rate read from how often a second unit finds a pothole a first unit found.

Decisive step: completing each segment's unrecorded potholes as one over one minus 0.458 to the power of the number of distinct installed units that drove it in March (0.542 being the share of second-unit looks at an already-found pothole that found it), not over its passes or its days, which designates Fenwick Gap, Thistlebank, Holloway Run, Kestrelton and Norvelle beside Carrow Point and Elmscourt.

Not semantics: every field, code, unit and date read correctly (the review decisions and duplicates, the 2025 to 2026 crosswalk, the turnback date, the two clocks, the register's install dates) still leaves the easy route completing the unrecorded potholes from the passes; no field marks a unit's blind spots or says a unit's repeat passes are dependent, and the step is the choice of the capture occasion, a property of the recaptures, not of any field.

Not rule application: the program files the population (every pothole on the roadway, recorded or not, cold patched or not), the unit, the lane-mile rule and the 6.0 line; no filed rule or procedure completes the unrecorded potholes, and executing every filed rule with each pass taken as an independent chance designates Carrow Point and Elmscourt.

Analyst test: a strong analyst who conforms the detections, the review, the traversals and the inventory and reads every rule correctly completes the unrecorded potholes at the rate passes re-find a found pothole over each segment's passes and designates Carrow Point and Elmscourt (the default path's Ends on); taking each day as the chance, recapturing the first half of March against the second, or recapturing between units only where two drove land on the same two; only the distinct units, at a second unit's find rate, designate the seven.

Estimand: the Spring Patching Program 2027 (spring_patching_program_2027.pdf, 2.1 to 2.4): a section gets a crew when its state-maintained roadway, as at 31 March 2027, held 6.0 or more potholes per ten lane-miles in March 2027, every pothole on that roadway counted whether or not a Kerbline unit recorded it, a pothole cold patched in March counted, lane-miles being segment length times through lanes.

No decoy: nothing is planted to be caught: the detections, the traversals, the register, the review and the work orders are what each system writes; no memo, draft, vendor claim or earlier list ranks the sections or states a find rate, and Kerbline's scope of work describes the units, the review, the data and the charges, not how often a unit finds a pothole.

No certified replay: no published section figure, audited count or earlier designation ships to back a method out of; the recaptures are the record's own evidence of how the units find potholes, and they score a completion only by the comparison a solver chooses to run.

Lesson: when several instruments look repeatedly at the same units and each instrument either always or never sees a given member, the independent chances are the distinct instruments that looked, not the looks, and the per-instrument rate comes from how often a second instrument finds what a first one found; no build on file completes a count by taking the distinct instruments as the capture occasions while each instrument's own repeats carry no chance.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, the confirmed potholes as found (Carrow Point, Elmscourt) | program 2.2 "whether or not a Kerbline unit recorded it": fires | defect_id: fires | count the confirmed: fires | none | none | one divide | readable |
| R1, every pass an independent chance, the default path (Carrow Point, Elmscourt) | scope of work 3 "not an inventory of every defect": fires | detections against traversals: fires | per-pass detection rate: fires | none | none | a ratio | readable |
| R1b, the first half of March recaptured by the second (Carrow Point, Elmscourt) | none | captured_local: fires | two-sample recapture: fires | none | none | a product over a count | readable |
| R2, two units' recapture only where two or more drove (Carrow Point, Elmscourt) | none | unit_serial: fires | dual-system estimate: fires | none | none | a product over a count | readable |
| G (decisive), each segment's potholes completed over the distinct installed units that drove it, at the rate a second unit finds what a first found (seven sections) | no sentence says a unit's passes repeat its own misses | no column holds a unit's find rate or a segment's units | no reflex takes the instrument rather than the look as the occasion | none | none | none | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | maintenance section | the inventory's section number | the yard's patrol area | same call: the inventory carries one section per segment (asserted) | road_inventory_2026.csv |
| SF2 | state-maintained roadway as at 31 March 2027 | the 2026 inventory less the five segments turned back on 15 March | every segment the inventory lists | same call (asserted, turnback kept) | program 2.4 and the turnback notice |
| SF3 | in March 2027 | 1 to 31 March, district local time | UTC calendar days | same call (asserted, UTC window) | program 2.2; the data notes' time line |
| SF4 | pothole | a defect the reviewer confirmed, and every pothole no unit recorded | every pothole-class defect Kerbline reported | not the program's: 2.3 drops what the reviewer rejects | program 2.3 |
| SF5 | a pothole cold patched in March | counted | left out | not the program's | program 2.2 "counts" |
| SF6 | per ten lane-miles | potholes over lane-miles, lane-miles being length times through lanes, times ten | per centerline mile | not the program's | program 2.4 |
| SF7 | 6.0 or more | at or above, on the unrounded estimate | the whole-number figure against 6 | same call: no estimate in any member lies within 0.75 of the line (asserted) | program 2.1 |
| SF8 | a defect the reviewer marks a duplicate | folded into the defect it names, its units with it | a defect of its own, unconfirmed | same call (asserted, duplicates unmerged) | the review export's reason |
| SF9 | a detection's segment | road_ref through the crosswalk, a split segment's detections by milepost | a split segment's first piece; or unlisted refs dropped | same call (asserted, both) | the crosswalk and the data notes |
| SF10 | a unit drove a segment | a March traversal by its vehicle on a day the register shows it installed | every March traversal by a pilot vehicle | same call (asserted, install dates ignored) | the unit register |
| SF11 | the whole number | half up on the unrounded estimate | half to even | same figures: no member's estimate within 0.1 of a half (asserted) | the prompt's rounding |
| SF12 | the files the call reads | detections, review, traversals, register, inventory, crosswalk, turnback, program | the sessions gating the passes; the pavement survey; the winter log | same call (asserted, sessions gating; the two distractors deleted) | program 2 |

## Ladder

Built figures, read from the cut pack by `generator/methods.py` (potholes per ten lane-miles, March 2027, against 6.0).

- **R0, the confirmed potholes as found (Carrow Point 7.19, Elmscourt 8.50).** No completion. Dies to program 2.2: a
  pothole counts whether or not a unit recorded it. Nearest under: Norvelle 5.03, Thistlebank 5.08.
- **R1, every pass an independent chance, the default path (Carrow Point, Elmscourt).** 64 per cent of unit-days over a
  found pothole recorded it again; every segment had seven or more pass-days, so the completion adds under 0.01 per ten
  lane-miles anywhere. Dies to the recaptures: the unit that found a pothole records it again on 99.5 per cent of its
  later days, a second unit on 54 per cent, so a pass by the same unit is no second chance.
- **R1b, the first half of March against the second (Carrow Point 7.19, Elmscourt 8.51).** The same units drive both
  halves, so the halves recapture each other almost completely. Dies to the same recaptures.
- **R2, two units' recapture only where two or more drove (Carrow Point 7.95, Elmscourt 9.24; Thistlebank 5.48,
  Fenwick Gap 5.40, Norvelle 5.40 under).** Completes the metro sections and leaves every one-unit segment as found.
  Dies to the patrol pickups' own rate where they drive with others (0.569 against 0.542 pooled): the unit that drives a
  segment alone finds at the rate it finds where it does not.
- **G (Fenwick Gap 7.08, Thistlebank 8.12, Holloway Run 8.08, Kestrelton 7.17, Norvelle 8.29 over the line beside
  Carrow Point 7.95 and Elmscourt 9.24; Rushmead 5.02 the nearest under).** The generator's true counts designate the
  same seven.
- **Margins:** under every licensed member (one rate by pairs 0.542 or by maximum likelihood 0.548, a rate per kind of
  section, a rate per fleet) the nearest designated section is Kestrelton at 6.80 (1.13x the line) and the nearest
  undesignated Rushmead at 5.04 (1.19x under); every member prints the same fourteen whole numbers. The default path's
  nearest are Thistlebank 5.08 (1.18x under) and Carrow Point 7.19 (1.20x over).
- **Position, separation and dominance:** a designation, not a ranking: every wrong rung names Carrow Point and
  Elmscourt alone, and only the completion over distinct units adds the five; there is no decoy to dominate.
- **Worth:** the call and the fourteen whole numbers; the default path keeps one of the fourteen (Rushmead's 5), so the
  asks carry the pair (Ask sheet).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | every pothole on the section's state-maintained roadway as at 31 March 2027 in March, recorded or not, cold patched or not (program 2.2 to 2.4; SF2, SF4, SF5) |
| 2 | Unit of account | the section; potholes per ten lane-miles |
| 3 | Attribution window | 1 to 31 March 2027, district local time (SF3) |
| 4 | As-of dating | the roadway as at 31 March; the exports pulled 1 to 3 April |
| 5 | Version basis | the 2026 inventory release and the turnback; Kerbline's current defect numbers in the detections and review exports |
| 6 | Denominator | lane-miles, length times through lanes (SF6) |
| 7 | Weighting | none: each section's own potholes and lane-miles |
| 8 | Window length | the month |
| 9 | Boundary inclusivity | 6.0 or more, unrounded (SF7) |
| 10 | Rounding path | the estimate unrounded against the line; the reported figure half up to the whole number (SF11) |
| 11 | Tie-break | none: each section against the line |
| 12 | Maturity and censoring | the campaign closed on 31 March; reviews of March reports complete by the 2 April export |
| 13 | Order of operations | conform, fold duplicates, place on segments, units per segment, the rate, the completion, the comparison |
| 14 | Row order | none (asserted over a reshuffled traversal file) |
| 15 | Duplicate resolution | the reviewer's duplicates folded (SF8); a unit's repeat detections are one capture |
| 16 | Identity normalisation | road_ref to the 2026 segment through the crosswalk (SF9); unit to vehicle through the register (SF10) |
| 17 | Netting | none |
| 18 | Dimensional units | miles, lanes, potholes |
| 19 | Code and status semantics | review decisions and reasons; Kerbline's classes; never the stump |
| 20 | Integerisation | none before the comparison |
| 21 | Clause scope | program 2 the designation; 3 the task orders, which carry the cold patches; scope of work 6 the charges |
| 22 | Forward window contents | the task orders crew May and June on the closed March campaign (Draw) |

## Literal reader

Executed word for word, the program fixes the population (every pothole on the roadway in March, recorded or not,
cold patched or not), the roadway (the inventory as at 31 March, so less the turnback), the unit and the line, and the
scope of work says the detection inventory is not every defect. So the unrecorded potholes have to be estimated, and the
candidates are no completion, every pass or day an independent chance, a recapture between halves of the month, a
recapture between units only where two drove, and the completion over the distinct units that drove each segment. The
data separate them: a unit that recorded a pothole records it again on 99.5 per cent of its later days while another
unit that drove the same segment records it on 54 per cent, so a unit's passes are one chance and the distinct units are
the chances; every completion over distinct units (by pairs, by maximum likelihood, per kind of section, per fleet) files
the same seven sections and the same fourteen whole numbers, and every pass-, day- or half-month completion files Carrow
Point and Elmscourt (checks.py). Every write-up step names the file and rule it executes.

WHAT screen (stumping 1.2): population, program 2.2 to 2.4; outcome, 2.2; window, 2.2; unit, 2.4; comparison, 2.1. The
decisive step settles none of them: it is how the filed count is completed from a record that misses some of it.

## Oracles

None. No control, published figure or reconciliation ties only under the golden: the review export's confirmed count is
the same under every route (records-fixed), the sessions cover every installed unit's traversals under every route, the
work orders and the camera miles touch nothing the call reads, and no section rate, find rate or earlier designation
ships.

## Ask sheet

The program's section 3 puts each section's March cold patches on its task order for replacement, with the miles the
pilot's camera units were driven on the section's roadway in March. No ask reads a row the call reads: the work orders
and the camera miles' traversal duplicates sit outside the call's population (zero device rows in it, asserted).

- **Ask A, cold patches by section: 28 figures** (the potholes cold patched in March, a pothole patched more than once
  counting once, and the pounds of cold mix those patches used, for each of the fourteen sections). Path: the work
  orders, the review export (defect numbers, decisions, reasons and route mileposts), the detections, the program.
  Devices: A1 (D6, primary for the pounds), the crews' mobile app writes the order's total pounds on every line of a
  multi-line order, while office orders carry each line's own pounds and crews often enter one figure for like potholes
  on an office order (every section has one), so summing the lines counts a mobile order's pounds once per line and
  taking every repeated figure once loses the office orders' like lines; only the detections' severity shows which is
  which (a repeated figure above anything a single-line order used on a pothole of its lines' severities is a total).
  A3 (D7, primary for the counts), when Kerbline split one pothole into two defect numbers, a crew sometimes raised the
  order on the second number before the reviewer rejected it as a duplicate (the review's reason is the bare word
  "Duplicate", naming no defect); in every section one pothole's only order carries the rejected number, and one
  pothole's first order carries it while its re-patch carries the surviving number, a few thousandths of a mile apart.
  Only the review's milepost joined across rows shows which confirmed defect the duplicate is (the nearest on its
  route, within 0.01 mile and no other within 0.02, asserted): counting by location keeps the twin as a second pothole,
  dropping orders on rejected numbers loses a patched pothole. Hazard A2 (D7), the 17 March renumbering: an order raised
  before it carries the old number, which only the order's route milepost resolves. Other hazards: open orders (no
  finish), the March finish window. Stops: refs as written and lines summed (the natural read); refs resolved by
  location and lines summed (the cracker); every repeated figure once; rejected numbers dropped; the golden.
- **Ask B, camera miles by section: 14 figures** (the miles the pilot's units were driven on the program's roadway in
  March, each pass at its segment's inventory length). Path: the traversals, the register, the inventory, the turnback,
  the program. Device B1 (D1, primary): the telematics provider re-ran its map matching over 12 March 00:00 to 13 March
  06:00 UTC and appended the re-run's traversals beside the originals, offset by a fraction of each traversal's own
  duration, under that day's traversal numbers; no row repeats another and every key is unique, and only a vehicle's
  overlapping traversals of one segment show it, because patrol trucks working an interchange come round its loop and
  drive a short segment again the same way a minute or three after leaving it (every section has some), so dropping a
  vehicle's repeats inside a few minutes loses real passes; only a traversal that begins before the vehicle's previous
  one of the segment has ended is a re-run. Hazards: the crew trucks' trips before their units were installed, the
  UTC export window, the turnback segments. Stops: every row (the natural read), the installed and local-window filters
  without the overlap, the golden.

| Ask | Cracker (lands the call; refs resolved by location, no duplicate fold, lines summed, every traversal row kept) | Mirror (no completion; every ask read the natural way) |
|---|---|---|
| A, cold patches and pounds by section (28) | miss | miss |
| B, camera miles by section (14) | miss | miss |

Pair ceiling: 28.5 (cracker 45.0 with the call, the fourteen whole numbers and no ask figure; mirror 12.0, off the call
with one whole number and no ask figure)

Mirror leakage: 0.0 per cent of ask weight

Measured by: generator/ceiling.py


## Pre-ship check

- **The 10/10 rules against the built pack.** The decisive step is still the choice of capture occasion (distinct
  installed units, not passes), which no field, code or filed rule performs: R3a (the easy route on the clean truth
  files Carrow Point and Elmscourt) and R3b (the decisive step alone files the seven) pass in checks.py. The mess is
  still only Layer 1: each item read the natural wrong way leaves the call, and all but dropping unlisted 2025 refs
  leave the fourteen whole numbers too (R2 in checks.py).
- **Deletion tests.** No wrong number ships, so deleting every wrong number changes nothing and the task stays hard;
  the clean-data test is R3a; no control, published section figure or rate ships to tie under either route; the two
  distractors are read by nothing the call or the asks need.
- **Determinism.** Every licensed member of the completion (pairs 0.542, maximum likelihood 0.548, per kind of section,
  per fleet) prints the same seven sections and fourteen whole numbers, every estimate at least 0.17 from a half; the
  per-unit rate itself is not a critical component, because pairs and maximum likelihood differ in its first decimal.
- **leak.py REVIEW lines, answered.** The scope of work's "repeated detections of one defect" and "records the roadway
  ahead", the program's "whether or not a Kerbline unit recorded it" and the data notes' "a unit's capture of a defect"
  are each file's own business (the vendor's linkage, the estimand, the detections file's grain); none says that a unit's
  passes repeat its misses or that units differ in what they see. Column names and dates are clean after renaming
  actual_finish and generated_utc and passing the as-of date.
- **House fixes.** Container metadata clean in target and golden (scrub audit); the manifest registers every file but
  itself; four section names that are real towns renamed (Rushmead, Kestrelton, Halverton, Grisholt, Oxbrae); the zip
  holds the sixteen files with no enclosing folder; the section names the answer uses ship in maintenance_sections.csv.

## Tried and rejected

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
- 2026-10-20, stage 3: the sweepers' night shifts of 28 February and 31 March: under a UTC window they moved camera
  miles across the month boundary; the spring sweeping schedule now runs 1 to 30 March nights.

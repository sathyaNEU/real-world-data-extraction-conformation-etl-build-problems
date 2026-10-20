# task478 design note: Tamsett District's spring patching crews, by the potholes the camera fleet did and did not find

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task478.json` (architecture v1), registered 2026-10-20 after a pull;
  `check` re-run on the registered card: WARN only, answered here. `three_rules.strategy_risk` (grain_or_unit): the
  analyst test below shows the easy route that still fails with every field and rule read correctly; the unit at issue
  is the capture occasion (a camera, not a pass), which the record's own recaptures force, never a field's reading.
  `overuse.org_family` (government_agency in 37 builds): a state DOT district is a government agency and no honester
  family exists. `overuse.objective` (ETL in 8 of 12): the lane is ETL by assignment. `overuse.gate_g`
  (method_or_model_selection in 7 of 12): the decisive step is the choice among defensible completions, pinned by the
  recaptures; no other Gate G mechanism carries it. `test.same_puzzle_older` and `test.same_driver_older` (population,
  G16) against task236, task453 v1, task463, task104, task134 v1, task177, task501 v4 and task70 v2: unrelated drivers,
  differentiated on the card. Nearest driver on file task49 at 0.07.
- **Redrawn at the draw, and why the replacements are the honester labels.** The pairing was first drawn on the client
  label, General Statistics & Data Science / data-integration-record-linkage-entity-resolution, and task479's
  registration (21:50, the same client pairing and subdomain) put both inside the window; the card carries the house
  domain business-operations-analytics with subdomain field-service-maintenance, which names the decision-maker (a DOT
  district's road maintenance operation) and maps to the same client task type. The city public works department first
  sketched (local_government, task479's family) became a state DOT district (government_agency), the honest owner of
  state highways and their patching contract. Shape `other` (01 is task479's, 03 task481's): the criteria are each
  section's estimate and verdict against one line, 01's arithmetic without a cap.
- **Seed:** ET35 (a FEMA regional office's repeat-impact mitigation initiative for the counties with the most PA major
  disaster declarations over 2004 to 2023). Screened at the draw and set aside (Tried and rejected): the declaration count
  is records-fixed, its levers are data semantics, and every unobserved quantity the world offers is a spent lane
  mechanism. Kept in form: a programme serving every area whose count per area clears a line, built by conforming an
  agency's own records.
- **Pairing:** Business Operations Analytics (house domain; field service and maintenance) sitting in General Statistics
  & Data Science, task type `data-integration-record-linkage-entity-resolution`, the ETL task type the house domain maps
  to. The ETL work is linkage: a detection vendor's defect inventory (each detection linked by the vendor into a defect
  across passes and cameras, keyed to the 2025 road inventory, re-keyed at a mid-month platform migration), the fleet's
  telematics segment traversals (UTC, the 2026 road inventory's segments), the camera register (units moved between
  vehicles by date) and device health log, the road inventory with its 2025 to 2026 crosswalk and jurisdiction
  transfers, the district QA reviewer's log and the maintenance management system's work orders, conformed into one
  section table. In a methods field the setting is another field's, so the swap is of the method. Objective: Data
  Extraction & Conformation (ETL).
- **The decision and the quantity:** the Tamsett District of the State Department of Transportation (fictional) issues
  its 2027 spring patching task orders under the district's on-call pavement patching contract. The Spring Patching
  Program 2027 gives a dedicated crew to every maintenance section whose state-maintained roadway that a camera-equipped
  district vehicle drove in March 2027 held 6.0 or more potholes per ten lane-miles on 31 March 2027, every pothole
  counted whether or not a camera recorded it, a pothole patched before 31 March left out. Fourteen sections. Forward
  facing: the task orders issue 19 April 2027 and the crews start 3 May; the quantity is the closed March campaign (a
  retrospective quantity with its reason: the program sizes the spring crews on the campaign the district ran).
- **Shape:** `other`, a designation over every candidate against one line: fourteen sections' estimated potholes per ten
  lane-miles (14), the designated set (1), the section nearest the line on either side and its gap (2), a bar chart's
  named parts (the fourteen bars, the 6.0 line, the designated sections marked: 3), the files (2), and the asks designed
  at stage 2.
- **Strategy:** `grain_or_unit`: the unit of an independent chance to find a pothole is a camera that drove the segment,
  built by grouping the traversal log's passes by camera unit; the passes are the file's rows and are not the chances.
  Gate G `method_or_model_selection`: several defensible completions (none; every pass an independent chance; every day
  one; the first half of March recaptured by the second; the distinct cameras), the right one pinned by the record's own
  recaptures. Gap population (potholes no camera recorded are in the population), pattern none, generators G16 (which
  completion the recaptures entitle), G12 (a segment driven twenty times by one camera with no find is a non-answer for
  the potholes that camera cannot see), G2 (the pass against the camera as the unit of chance), G10 (one pothole recorded
  many times). Layer 2 family `estimation_fit` (dependent capture occasions), pattern `own:capture occasions are the
  distinct instruments, not the repeat looks`.
- **World:** United States, an unnamed state's Department of Transportation and its fictional Tamsett District (metro
  Tamsett and its hinterland), about 2,300 lane-miles of state highway in fourteen maintenance sections, each run from its
  own yard with one patrol pickup. In February 2027 the district contracted Kerbline Vision for a pilot: smartphone camera
  units on 38 district vehicles (the fourteen section patrol pickups, ten freeway service patrol trucks and six sweepers in
  the three metro sections, and eight plow trucks dispatched district-wide in the two March snow events), each unit
  uploading its detections to Kerbline's platform, which links repeat detections of one defect into one defect ID.
  Personas from `guard.py names --geo "United States" --seed 478`: Tamara Copeland (district maintenance engineer),
  Darin Smith (maintenance management systems analyst).
- **Forcing fact:** the task orders issue 19 April 2027 under the on-call patching contract; crews start 3 May; as-of
  9 April 2027.
- **Forum and forcing event:** operations_desk (the district maintenance engineer issues the task orders),
  purchase_order_or_contract (the on-call contract's task orders). Organisation government_agency; role
  operations_director.
- **Data-native sentence:** each Kerbline unit sees a pothole or does not by how its phone sits on its vehicle, so a unit
  that missed a pothole on one pass misses it on every pass while a second unit finds it at the same rate as the first; a
  rural section's state roads are driven daily by its own patrol pickup and little else, so its potholes have had one
  camera's chance however many passes the traversal log lists, and close to half of them are on no detection list.
- **The WHAT screen.** Population: every pothole on state-maintained roadway in the section that a camera-equipped
  district vehicle drove in March 2027, standing on 31 March, recorded or not (the guidelines). Outcome: those potholes.
  Window: the March 2027 campaign, as standing on 31 March. Unit: potholes per ten lane-miles of that roadway, lane-miles
  being segment length times through lanes. Comparison: 6.0 or more. The decisive step settles none of them: it is how
  the potholes no camera recorded are completed, which nothing files.
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
- **Same-puzzle and same-driver tests:** (population, G16, designation_set) and (population, G16,
  method_or_model_selection) against the last twelve builds, lineage included: no match; older matches differentiated
  on the card.
- **Abstraction test:** the nearest drivers stripped of nouns (task49, an unpaid amount floored per instrument; task192
  v3, units labelled by an instrument validated on an early batch; task143, the weakest of a few members of a new group)
  carry no repeated looks whose dependence decides the completion. task471 (a census and its survey missing the same
  members of one group) is the nearest insight and differs in where the dependence sits (across two systems, carried by
  the member) and in what fixes it (an outside benchmark, against counting the distinct instruments inside the record).

## Default path

1. Read the Kerbline defect inventory, kept the detections the district's QA review confirmed as potholes, mapped each
   defect's 2025 segment to the 2026 road inventory, and kept the defects on state-maintained segments that no work
   order patched before 31 March (the maintenance management system's cold-patch orders carry the Kerbline defect ID).
2. Built each section's lane-miles from the 2026 road inventory (length times through lanes) over the segments the
   telematics log shows a camera-equipped vehicle drove in March.
3. Completed the potholes no camera recorded: of the passes that drove over a pothole already found, 95 per cent found
   it again, so each segment's chance of a find is one minus 0.05 to the power of its passes, 1.000 on every segment
   driven more than twice; the completion adds under one pothole in every section.
4. Divided each section's potholes by its lane-miles over ten and compared with 6.0.

Ends on: Carrow Point and Elmscourt.

Golden: Carrow Point, Elmscourt, Fenwick Gap, Lorimer, Holloway Run, Kellerton and Norvelle.

(The names and figures are the design's targets; the generator confirms them at stage 3 and this section is rewritten
to the cut pack's figures.)

## Stump sentence

The default path treats every pass over a segment as an independent chance at the 95 per cent find rate of repeat
passes, which credits a segment driven daily as fully searched and designates only Carrow Point and Elmscourt, because a
Kerbline unit finds the same potholes on every pass and only the distinct cameras that drove a segment are independent
chances; the rural and suburban sections, driven by their own patrol pickup and little else, hide close to half their
potholes, and Fenwick Gap, Lorimer, Holloway Run, Kellerton and Norvelle clear the line.

## Three rules

Task type: data-integration-record-linkage-entity-resolution (General Statistics & Data Science), integrating a defect
inventory whose detections are linked across passes and cameras with the effort record of every camera's traversals to
complete a population no record lists in full, a task type serving Data Extraction & Conformation (ETL); the house
domain business-operations-analytics (field service and maintenance) maps to it.

Domain test: general statistics, so the swap is of the method: the deciding quantity is each section's potholes per ten
lane-miles on 31 March 2027 with the unrecorded potholes completed, each recorded pothole counted as one over its
segment's chance of being found by at least one of the distinct cameras that drove it, at the rate a second camera finds
a pothole another camera found; replacing that estimator with a generic summary (finds per lane-mile, finds per pass,
every pass or every day an independent chance) designates other sections.

Swap: put a generic completion in place of the integration estimator ("scale up by the find rate of repeat passes",
"count what the cameras found") and the call changes to Carrow Point and Elmscourt alone; put another field's nouns in
("which forest compartments get a pest crew, from galleries found by drone flights") and the method still reads, which
is general statistics' own case: the deciding object is the completion's occasion structure, and changing it, not the
nouns, changes the call.

Layer 1: the vendor's detections in local time against the telematics log in UTC across the 14 March 2027 daylight saving
change (Kerbline's platform and the telematics provider); defect IDs re-keyed at Kerbline's 17 March platform migration,
with the vendor's migration map; segment IDs from the 2025 road inventory in the vendor feed against the 2026
renumbering, splits and merges in the inventory crosswalk (the district's inventory update); segments transferred to
municipal jurisdiction mid-month (the transfer agreements); the district QA reviewer's log keyed by pre-migration IDs
before the 17th (the review workflow); camera units moved between vehicles (the camera register's install and removal
dates); units offline (the device health log); cold patches in the maintenance management system. Each is produced by
the system named, none is placed to be caught, and each is asserted neutral on the call.

Layer 2: estimation_fit, dependent capture occasions: one camera's repeat passes over a pothole are not independent
chances (a unit that misses a pothole misses it on every pass) while separate cameras are, so the completion counts the
distinct cameras as the occasions, with the per-camera find rate read from how often a second camera finds a pothole a
first camera found.

Decisive step: completing each segment's unrecorded potholes as one over one minus 0.44 to the power of the number of
distinct camera units that drove it in March (0.56 being the share of second-camera looks at an already-found pothole
that found it), not over its passes or its days, which designates Fenwick Gap, Lorimer, Holloway Run, Kellerton and
Norvelle beside Carrow Point and Elmscourt.

Not semantics: every field, code, unit and date read correctly (the defect classes and QA outcomes, the migration map,
the 2025 to 2026 segment crosswalk, the transfer dates, the two clocks, the camera register's dates) still leaves the
easy route completing the unrecorded potholes from the passes; no field marks a camera's blind spots or says that a
camera's repeat passes are dependent, and the step is the choice of the capture occasion, a property of the recaptures,
not of any field.

Not rule application: the guidelines file the population (every pothole on the driven state roadway on 31 March,
recorded or not), the unit, the lane-mile rule and the 6.0 line; no filed rule or procedure completes the unrecorded
potholes, and executing every filed rule with each pass taken as an independent chance designates Carrow Point and
Elmscourt.

Analyst test: a strong analyst who conforms the inventory, the traversals and the road inventory and reads every rule
correctly completes the unrecorded potholes at the 95 per cent find rate of repeat passes over each segment's passes and
designates Carrow Point and Elmscourt (the default path's Ends on); taking each day a segment was driven as the chance, or
recapturing the first half of March against the second, lands on the same two; only the distinct cameras, at a second
camera's find rate, designate the seven.

Estimand: the District's Spring Patching Program 2027 guidelines (in the pack): a section gets a crew when the
state-maintained roadway in the section that a camera-equipped district vehicle drove during the March 2027 detection
campaign held 6.0 or more potholes per ten lane-miles on 31 March 2027, every pothole on that roadway counted whether or
not a camera recorded it and a pothole patched before 31 March not counted, lane-miles being segment length times
through lanes.

No decoy: nothing is planted to be caught: the defect inventory, the traversals, the registers and the work orders are
what each system writes; no memo, draft, vendor claim or earlier list ranks the sections or states a find rate, and
Kerbline's scope of work describes the hardware, the review and the data delivery, not how often a unit finds a pothole.

No certified replay: no published section figure, audited count or earlier designation ships to back a method out of;
the recaptures are the record's own evidence of how the cameras find potholes, and they score a completion only by the
comparison a solver chooses to run.

Lesson: when several instruments look repeatedly at the same units and each instrument either always or never sees a
given member, the independent chances are the distinct instruments that looked, not the looks, and the per-instrument
rate comes from how often a second instrument finds what a first one found; no build on file completes a count by
taking the distinct instruments as the capture occasions while each instrument's own repeats carry no chance.

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

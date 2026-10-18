# task470 design note: Corrisan Valley's 2027 unleaded avgas grants

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task470.json` (architecture v1), registered 2026-10-18 after a pull, so
  every card filed before it was in the check. Guard check PASS. Two bans cleared at the draw by redrawing the axis:
  the context artifact (monitoring_export, against task190) is now operations_log, the receiver network's record of
  each field's operations; the organisation family (government_agency, against task190) is now local_government, a
  regional air district. The structural test's older matches (gap population, pattern E, Gate G
  decomposition_attribution) are differentiated on the card: task107 v1 (a check's reach set by each source's delivery
  kind), task129 v1 (two causes separated through a per-record state), task36 (a candidate excluded by a filed remedy)
  and task44 v2 (a pilot's pooled effect split by a behavioural moderator). Nearest driver task153 at 0.08.
- **Seed:** ET27 (a state aviation office funds first the airport with the highest 2019 share of departures flown by
  aircraft of 50 seats or fewer; analysts joined the flights' tail numbers to today's aircraft register, many tails did
  not match and some matched small private aircraft). Kept: the world (a public body funding airfields one by one, the
  FAA aircraft register read through identifiers that change hands, emissions inventories), the decision (which fields
  are funded first, on a quantity of activity by one class of aircraft at each field) and the quantity's kind (each
  field's activity by the class that matters, here piston-engine aircraft, priced in lead). Made forward facing: the
  2027 grant round, qualified on the 2026 inventory year. Dropped as the decisive step: the seed's move (reading old
  tail numbers through today's register), which is identity resolution and data semantics; it survives as Layer 1
  (a transponder's 24-bit address follows its N-number, and an N-number reissued or an aircraft re-registered since
  2026 reads differently in the register as it stands now).
- **Pairing:** Physical & Environmental Sciences / emissions-inventory / ETL. The district's evidence is a conformed
  inventory built from sources never designed to join: its receiver network's record of every operation it heard at
  each field (24-bit address, UTC time, event type), the FAA register's fixed-width files (master, deregistered,
  aircraft reference, engine reference), the state aviation office's based aircraft list keyed by N-number, six
  control towers' daily counts, four fields' count studies and the fields' master records. The deciding quantity is
  each field's 2026 lead from piston aircraft, which airport lead inventories build from piston operations by engine
  class and operation type times lead per operation; at a field without a count the operations come from the network,
  and what the network misses has to be completed.
- **Shape:** 01, a list of candidates against a cap: each of the 24 non-towered fields' 2026 lead from piston-engine
  aircraft against the round's 12.5 kg, the count of qualifying fields and which they are.
- **Strategy:** composition_mix (the network's seen-to-counted rate pooled over the counted fields does not fit a field
  whose based fleet differs in the share that never broadcasts), pattern E, decisive generator G14 (the conditioned
  yield), with G12 (a field the network hears little at is not a field with little activity) and G6 (the pool shifted
  under the rate). Gate G decomposition_attribution: the decisive move books the missing operations to the aircraft
  that generate them.
- **World:** United States, an unnamed state. The Corrisan Valley Air Quality District, a regional air district run by
  a governing board of county and city representatives, inventories lead from piston-engine aircraft at the 30
  public-use general aviation fields in its valley: six with a control tower and 24 without. In 2025 it put an ADS-B
  receiver on every field. Its Unleaded Avgas Transition Grants pay for an unleaded fuel tank and dispenser at a field
  without a tower; the 2027 round funds every such field whose 2026 lead from piston-engine aircraft is 12.5 kg or
  more, under the district's inventory method (CVAQD-AQ-17, Revision 3).
- **Forcing fact:** the Governing Board adopts the 2027 grant round with the district's 2027 budget at its 10 March 2027
  meeting; the air toxics planner's qualification memo and the field inventory go to it. As-of: 12 February 2027. The
  call faces forward (the 2027 grant round); its quantity is the closed 2026 inventory year, which the round's
  guidelines name as the basis (a retrospective quantity with its reason: the round qualifies on the latest complete
  year).
- **Forum and forcing event:** council_or_assembly (the governing board), budget_or_appropriation (the 2027 grant
  round adopted with the budget). Organisation local_government; role policy_adviser. Personas from `guard.py names
  --geo "United States" --seed 470`: Jeanette Steele (Air Toxics Planner, who writes the qualification memo), Yolanda
  Cortez (Air Quality Specialist, who runs the receiver network) and Tonya Krause (Grants Program Manager); Brian Rowe
  replaced (his first name in task445).
- **Data-native sentence:** the district's receivers sit on every field and record every operation of an aircraft
  that broadcasts ADS-B Out and none of one that does not; the aircraft that do not broadcast are not spread evenly but
  based where old, privately flown piston aircraft are kept, so the operations the network misses are concentrated at
  those fields and absent at the flight-school fields whose rental fleets all broadcast.
- **The WHAT screen.** Population: every piston-engine aircraft operation (a takeoff or a landing, a touch-and-go being
  one of each) at a field in 2026, by any aircraft, heard by the network or not (filed in the district's method).
  Outcome: lead emitted, at the method's per-operation factors by engine class and operation type, an unrecorded
  operation at 1.625 g. Window: calendar 2026, local time. Unit: kilograms of lead per field. Comparison: 12.5 kg or
  more (the guidelines). The decisive step settles none of them: it is how the operations the network did not hear
  are estimated at a field without a count, which method 4.4 leaves to "the fields with a count".
- **Deliverables:** `corrisan_2026_field_piston_lead.csv` (each of the 24 fields' 2026 lead, whole kilograms) and
  `cvaqd_2027_unleaded_grant_qualification.docx` (the memo to the Governing Board: the qualifying fields, the bar chart
  of the 24 fields against the 12.5 kg line, the six towered fields' operations and lead).
- **Sources, one line each:**
  - `stumping/references/client/two-layer-task-design.md`: Physical & Environmental Sciences has Layer 1 techniques
    and no Layer 2 patterns on file, so the pitfall comes from the five families: estimation_fit (survivorship,
    weighting and post-stratification), here the missed activity placed with the units that never register.
  - `dataset-generation/references/layer1-messiness.md`: detections in UTC against tower counts kept by local day and
    tower hours, 24-bit addresses against N-numbers, the register's fixed-width layouts, based aircraft lists in mixed
    N-number formats, consultants' count study layouts, master records carried for years; each to be asserted neutral
    on the call.
  - The lane's spent drivers (`guard.py mechanisms --objective etl`): task462 (aerial plume detection weighted by a
    probability that rises with rate and wind) is the nearest family, a sensor that misses some activity; here the
    miss is not a per-event probability but a property of the unit (it never broadcasts), and the missing activity is
    rebuilt from which units were never heard anywhere in the year. task448 (a register's capture depending on the
    filing route) and task456 (three imperfect records of one state) are capture problems on lists, not on a sensor.

## Default path

1. Read `adsb_field_events_20251230_20270102.csv`, times from UTC to Pacific time, kept local 2026; gave each event
   its aircraft through `icao24` and MASTER.txt (DEREG.txt for an address MASTER no longer lists) and priced each
   piston-engine operation by ACFTREF's engines and the method's Table 1, a touch-and-go two operations.
2. At the six towers took the civil count in tower hours less the civil events recorded in those hours (method 4.2);
   at the four count fields the study's piston-engine operations less those recorded (4.3).
3. Took the network's share of the counted fields' operations: recorded over counted, 0.815.
4. At each of the 20 fields without a count, put the unrecorded operations at the recorded piston operations times
   (1 - 0.815) / 0.815, priced at 1.625 g (method 3.2, 4.4), and added the recorded lead.
5. Compared each field with the guidelines' 12.5 kg.

Ends on: eight fields, A71 F37 K58 L08 P05 S27 T13 T61 (Kestrel Ridge, Pellow, Saltry and Tavish in; Orrin Flats,
Umber Creek and Wickrow out).

Golden: seven fields, A71 F37 L08 O16 T13 U44 W33.

## Stump sentence

The default path scales every field's recorded operations by the counted fields' 0.815 share and qualifies eight
fields, A71 F37 K58 L08 P05 S27 T13 T61, putting the missed operations where the network already hears the most (the
flight-school fields, whose rental fleets all broadcast) instead of with the based airplanes that never broadcast, so
it drops the three vintage fields O16, U44 and W33 whose missed operations are a third of their lead.

## Three rules

Task type: emissions inventory compilation (an activity-based airport lead inventory: operations by engine class and
operation type conformed from a receiver network, the FAA register and counts, times factors per operation, the
unobserved activity completed by estimation), a task type serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is each field's 2026 lead from piston-engine aircraft, built the way airport lead
inventories build it (landing and takeoff operations by engine class and operation type times lead per operation), with
the operations the activity data misses estimated from the fields where the activity is fully counted; the field's
completion estimator here is a ratio estimator whose auxiliary is the airplanes that generate the missed activity.

Swap: "which hospitals' 2026 sharps waste qualifies for a disposal grant, from a scanner network that reads only tagged
containers" keeps the arithmetic but loses the domain's structure: here the misses are a property of the airplane
(ADS-B Out or not), the airplanes are based unevenly by field type, the counts are towers' and counters', and the lead
per operation is an engine-class factor; without them nothing fixes which auxiliary completes the inventory.

Layer 1: the network's export in UTC against an inventory in Pacific local time (padding days, daylight time), the
towers' counts kept in local tower hours with winter hours and closed days, the FAA register's padded layout (N-NUMBER
without the N, upper-case MODE S CODE HEX against the export's lower-case `icao24`), N-numbers changed, exported or
lapsed in 2026 (addresses only DEREG holds), the state's based list written four ways by county, the count studies in
four layouts (L08's touch-and-go circuits), flight IDs blank or stale; each asserted neutral on the call and on every
non-towered field's whole-kilogram lead (checks.py L1, SF2, SF9, SF10, SF12).

Layer 2: estimation_fit: completing an undercounted activity record, where the choice of auxiliary decides the
estimate; the missed operations are generated by the never-broadcasting airplanes, so they scale with the airplanes
the network never recorded, not with what it recorded or with every based airplane.

Decisive step: estimating each uncounted field's unrecorded operations as the counted fields' unrecorded operations per
based piston airplane the network never recorded (23,376 over 338, 69.2) times that field's never-recorded airplanes,
which qualifies O16, U44 and W33 and drops K58, P05, S27 and T61.

Not semantics: every field, code, unit and definition read correctly (Pacific time, tower hours, civil columns, a
touch-and-go two operations, TYPE ENGINE 1, the register's history, the network notes' sentence that aircraft without
ADS-B Out are not recorded) still leaves the easy route scaling each field's recorded operations by one capture share;
no field marks an airplane as non-broadcasting, and the step is the choice of estimator, not a reading.

Not rule application: the method files the population (every piston-engine operation, recorded or not), the factors,
the unrecorded operation's 1.625 g and the counted fields' unrecorded operations; 4.4 says only that the others are
estimated from the fields with a count, and executing every filed rule with a capture share qualifies the default
eight.

Analyst test: a strong analyst who reads every file and rule correctly takes the counted fields' capture (0.815),
completes each field's recorded operations with it and qualifies the eight fields A71 F37 K58 L08 P05 S27 T13 T61 (the
default path's Ends on); split by flight training it qualifies nine; only the unrecorded operations per never-recorded
airplane qualify the seven.

Estimand: guidelines 2.1 and 2.2 (cvaqd_2027_unleaded_avgas_transition_grants.pdf): a public-use field in the district
without a control tower whose 2026 lead from piston-engine aircraft, as method CVAQD-AQ-17 Revision 3 estimates it, is
12.5 kg or more; method 1.1, 2.2 and 3 (cvaqd_aircraft_lead_inventory_method_rev3.pdf): every operation by a
piston-engine aircraft at the field in calendar 2026 local time, recorded or not, at Table 1 or 1.625 g.

No decoy: nothing is planted to be caught: the export, the register, the counts and the studies are what each system
writes; no memo, draft, briefing or stakeholder figure argues a method or a list; the 5010 records are the airports'
own filings, declared as the wrong-basis distractor and ruled out by their own dates and estimates.

No certified replay: no published inventory, earlier qualification or certified figure ships to back a method out of;
the counted fields are the method's own evidence (4.2, 4.3) and score candidates only by leave-one-out, which every
analyst can run.

Lesson: when a sensor misses whole units rather than a share of events, the activity it misses scales with the units
it never detected, measured where the activity is fully counted, never with what it did detect; no build on file
completes an undercounted record from the units that never registered.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, one capture share from the counted fields (eight fields) | method 4.4 points to the fields with a count: fires | the towers' counts and the export side by side: fires | a capture or correction factor is the reflex for an undercounting sensor: fires | none | none | one ratio: fires | readable |
| R1, the capture share split by the directory's flight training flag (nine fields) | none | the Flight Training column: fires | holding the pool to every visible attribute: fires | the counted fields' capture spreads 0.56 to 0.99: fires | none | two ratios: fires | readable |
| R2, operations per based airplane at the counted fields (nine fields) | none | the based list beside the counts: fires | operations per based aircraft is the planner's textbook ratio: fires | none | none | one ratio: fires | readable |
| R3, unrecorded operations per based airplane (eight fields) | none | the based list: fires | none | none | none | one ratio: fires | readable |
| R4, never-recorded airplanes flying like the recorded ones (five fields) | the network notes' mechanism sentence: fires | none | none | none | none | none | readable |
| R4b, the never-recorded share of a field's based airplanes as its unrecorded share (five fields) | the network notes' mechanism sentence: fires | the based list beside the export: fires | none | it matches the unrecorded share at F37, G42 and D19: fires | none | one share per field: fires | readable |
| G (decisive), unrecorded operations per never-recorded airplane measured at the counted fields (seven fields) | no clause names never-recorded airplanes, a rate per airplane or an auxiliary; 4.4 says only "from the fields with a count": silent | no column flags an airplane as broadcasting or not; the never-recorded set is built by joining the based list through the register to the export: silent | the reflexes are the capture share and its splits; testing which auxiliary the misses scale with is no battery step: silent | the counted fields score the candidates only by a leave-one-out nobody asks for: silent | every file reconciles; nothing is anomalous: silent | a join across three files and a ratio over ten fields: silent | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | qualifies | 12.5 kg or more | more than 12.5 kg | same call: no field within 1 kg of the line (asserted) | guidelines 2.2 "is 12.5 kg or more" |
| SF2 | 2026 | the local (Pacific) calendar year | the UTC year | same call and every lead in its whole kilogram (asserted) | method 1.1 "in local time (Pacific time)" |
| SF3 | an operation | a takeoff or a landing, a touch-and-go two | a touch-and-go one, as the export's one event | same call (asserted) | method 2.1 "A touch-and-go is two operations" |
| SF4 | piston-engine aircraft | TYPE ENGINE 1 (reciprocating) on a fixed wing | every fixed-wing airplane, turboprops and jets included | same call (asserted) | method 1.2 "Aircraft with turbine engines ... are outside the inventory" |
| SF5 | fields without a control tower | the 24 public-use fields with ATCT N | the private strips too | not candidates | guidelines 2.1 "a public-use airfield"; the directory's Use column |
| SF6 | lead at a field | its takeoffs and landings | flight away from the field | none ships | method 1.2 "lead emitted in flight away from the field" is outside |
| SF7 | an unrecorded operation's lead | 1.625 g | class factors | none ships the class of an unrecorded operation | method 3.2 |
| SF8 | the fields with a count | the six towers and the four count fields | towers only, studies only | same call and leads (asserted, SF13 rows) | method 4.2 and 4.3 name both |
| SF9 | the tower's civil operations | air carrier, air taxi and general aviation itinerant, local civil | total operations, military included | same call and leads (asserted) | method 4.2 "civil operations"; the counts' column names |
| SF10 | the tower's hours | the directory's hours, winter hours and closed days | the summer hours all year | same call and leads (asserted) | the directory's ATCT Hours (local) |
| SF11 | based airplanes | the state's 2027 validation by N-number | the 5010 based counts | the 5010 counts carry no N-number to test | the 5010 notes: as last filed, the manager's report |
| SF12 | recorded in 2026 | under any address the airplane carried in 2026 | under its current address only | same call and leads (asserted) | the register's history (DEREG) |
| SF13 | the rate per never-recorded airplane | the ratio of totals at the ten counted fields | mean or median of the ten ratios, least squares through the origin, towers or studies alone | same call and every lead in its whole kilogram (asserted) | the data's structure: the ten ratios run 65 to 73 |
| SF14 | lead in whole kilograms | rounded for reporting, qualified unrounded | qualified on the rounded lead | same call (asserted) | no field within 1 kg of the line |

## Ladder

- **R0, the default path: one capture share (eight fields).** The counted fields' recorded share is 0.815 (towers'
  civil operations in tower hours and the studies' piston operations); completing each field's recorded operations
  with it qualifies A71 F37 K58 L08 P05 S27 T13 T61. The variant that scales the recorded lead by the share names the
  same eight. Dies to the counted fields themselves: their shares run from 0.56 (D19) to 0.99 (L08), and the share
  predicts a left-out counted field's unrecorded operations with a mean error of 342 per cent (L08 +3,162).
- **R1, the reflex correction: the share split by flight training (nine fields).** 0.858 at the training fields, 0.734
  elsewhere; adds N26. Dies to the same fact: within each group the shares still spread 0.71 to 0.99 and 0.56 to 0.80.
- **R2, operations per based airplane (nine fields).** 79.7 at the counted fields; adds H52 and W85, keeps the golden
  seven. Dies to the leave-one-out (90 per cent mean error): based fleets differ in how much they fly at home.
- **R3, unrecorded operations per based airplane (eight fields).** 15.3; adds K58, P05, T61 and U44, drops O16 and W33.
  Dies to the counted fields: 1.4 per based airplane at L08, 28.5 at D19 (122 per cent mean error).
- **R4, the sophisticated near miss: the never-recorded airplanes fly like the recorded ones (five fields).** Finds
  the never-recorded airplanes but gives them the field's recorded airplanes' operations; keeps W33, drops O16 and U44.
  Dies to the counted fields: the never-recorded airplanes fly 65 to 73 operations a year there, the recorded ones
  28 to 76 at the vintage fields (31 per cent mean error).
- **R4b, R4's variant: each field's recorded lead scaled up by the share of its based piston airplanes the network
  never recorded (five fields, the same as R4).** The route reader round 1 took. It validates at three count fields
  (F37 19.5 per cent never recorded against 20.2 per cent of operations unrecorded) and fails where the recorded
  airplanes fly less than the never-recorded ones: W33 in at 5.2 per cent over the line, O16 and U44 out.
- **R5, the network's record alone (four fields).**
- **G, the decisive move (seven fields).** 23,376 unrecorded operations over 338 never-recorded airplanes at the
  counted fields, 69.2 each, 65 to 73 field by field (4 per cent mean leave-one-out error, worst CRV +7).
- **Margins:** the golden's nearest field is P05 at 11.1 per cent below the line (W33 13.0 above); every wrong rung's
  nearest field is at least 3.8 per cent from it (R3's T61 and S27), R0's 7.5. Every lead is at least 0.28 kg from its
  whole-kilogram edge; five other rate estimators give the same call and every lead in the same kilogram.
- **Position, separation and dominance:** every rung names its own set (eight, nine, nine, eight, five, four against
  seven); the corrections from R0 move fields in both directions and only the rate per never-recorded airplane takes
  out the four training and park fields and brings in the three vintage ones together.
- **Worth on the graded quantities:** the call (8) and the 24 leads (1.25 each): R0 keeps 11 leads, R0b 12, R1 5, R2
  10, R3 8, R4 21, R4b 19, R5 9; none lands the call (generator/ceiling.py).
- **Grid:** the Layer 1 items mishandled one at a time and the rate estimators swapped leave the call and every lead
  in place (checks.py); the capture share, its split and the per-based rates each land on a named wrong set.

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | every piston-engine operation at the field in 2026, recorded or not (method 2.2); the 24 public-use fields without a tower (guidelines 2.1) |
| 2 | Unit of account | the field; lead in kilograms (method 3.3); an operation a takeoff or a landing (2.1) |
| 3 | Attribution window | calendar 2026 in Pacific time (method 1.1); padding days and the UTC year change no figure (SF2, L1) |
| 4 | As-of dating | the export of 8 January 2027, the register of 1 February 2027 with its cancelled registrations, the based validation of 1 January 2027 |
| 5 | Version basis | one version of every file; the call reads each address through the register by date (Layer 1); the ask reads each operation as the aircraft that flew it, the register by date and, where the flight ID names another airframe registered that day, that airframe |
| 6 | Denominator | the rate per never-recorded airplane over the ten counted fields (SF13); the decisive step (HOW), every member of the family agreeing |
| 7 | Weighting | the ratio of totals; mean of ratios, median and least squares agree (SF13) |
| 8 | Window length | the whole 2026 year at every counted field |
| 9 | Boundary inclusivity | 12.5 kg or more (SF1); nothing within 1 kg |
| 10 | Rounding path | lead summed in grams, reported in whole kilograms, qualified unrounded (SF14); operations to the nearest hundred |
| 11 | Tie-break | none: each field is judged on its own lead |
| 12 | Maturity and censoring | the 2026 year is closed; the unrecorded operations are completed by estimation, the decisive step |
| 13 | Order of operations | events, aircraft, priced operations, counted fields' unrecorded, never-recorded airplanes, rate, completion, comparison |
| 14 | Row order | no dependence |
| 15 | Duplicate resolution | no repeated event id or registration; a touch-and-go one event, two operations (SF3) |
| 16 | Identity normalisation | N-numbers normalised across the four county sheets, the register's N-NUMBER without the N, hex case (Layer 1, asserted every based N-number matches) |
| 17 | Netting | a tower's unrecorded operations are its civil count less the recorded civil events in its hours (method 4.2); military columns out (SF9) |
| 18 | Dimensional units | grams per operation to kilograms per field; UTC to Pacific with daylight time from 8 March to 1 November 2026 (network notes) |
| 19 | Code and status semantics | TYPE ENGINE 1 on TYPE AIRCRAFT 4 or 5 is a piston-engine airplane (SF4); never the stump |
| 20 | Integerisation | whole kilograms; operations to the nearest hundred |
| 21 | Clause scope | guidelines 2.2: the 2027 round on the 2026 inventory; method 4.4: the fields without a count |
| 22 | Forward window contents | the 2027 round's qualifying list on the closed 2026 inventory (a retrospective quantity with its reason, Draw) |

## Literal reader

Executed word for word, the guidelines and method fix the population (every piston-engine operation at each field in
2026 Pacific time, recorded or not), the factors, 1.625 g for an unrecorded operation, the counted fields' unrecorded
operations (4.2, 4.3) and the 12.5 kg line, and leave one thing open: how 4.4's estimate is made "from the fields with
a count". The candidates are the capture share (R0, R1), the per-based rates (R2, R3), the never-recorded airplanes at
the recorded ones' rate (R4) and the never-recorded airplanes at the counted fields' rate (G). The data separates them:
the network notes say an aircraft without ADS-B Out is not recorded, the counted fields' unrecorded operations per
never-recorded airplane run 65 to 73 while their capture runs 0.56 to 0.99 and their unrecorded operations per based
airplane 1.4 to 28.5, and a leave-one-out at the ten counted fields gives mean errors of 4, 31, 90, 122 and 342 per
cent for G, R4, R2, R3 and R0 (checks.py). Every member of G's family (ratio of totals, mean and median of ratios,
least squares through the origin, towers or studies alone) gives the same seven fields and every lead in the same
kilogram. Every write-up step names the file and rule it executes.

## Oracles

None that ties only under the golden. The counted fields score every candidate on equal terms by the leave-one-out a
solver chooses to run; no published inventory, earlier round or certified figure ships. The 5010 records give
operations and based counts per field on another basis (managers' estimates for twelve months ending 2018 to 2025,
every aircraft) and qualify 19 fields priced at 1.625 g, neither the golden nor rung 0 (the declared wrong-basis
distractor). The lead monitors sit at two towered fields and rank no candidate.

## Ask sheet

- **Ask A, each towered field's 2026 piston-engine operations (nearest hundred) and lead (whole kilograms): twelve
  figures.** H18 home: the six towered fields complete the district's 2026 inventory that the board reads beside the
  round; they are the counted fields whose counts the call consumes, and their piston lead is the trail from those
  counts and the network's events through rows the call never prices (which aircraft flew each recorded operation).
  Use: the inventory goes to the board whole. Path: the export (event_time_utc, site, event, icao24, flight_id),
  MASTER.txt (N-NUMBER, MODE S CODE HEX, MFR MDL CODE, SERIAL NUMBER, CERT ISSUE DATE), DEREG.txt (MODE S CODE HEX,
  MFR-MDL-CODE, SERIAL-NUMBER, CERT-ISSUE-DATE, CANCEL-DATE), ACFTREF.txt (TYPE-ACFT, TYPE-ENG, NO-ENG), the towers'
  daily counts (Date, Facility, the civil columns), the directory's tower hours, the method (2.1, 3, 4.2), the network
  notes (UTC, flight_id) and the register notes (codes): nine files, nineteen columns.
  Primary device: D2 with D9, a label stored before a silent switch that the register's own history dates wrongly. At
  each tower an owner or operator moved its N-number in 2026 from a piston airplane (Chieftain, 310, Baron, Seneca,
  T210) to the turbine that replaced it (three at CRV). The Registry moved each number on paper 30 to 150 days before
  the turbine came out of completion and arrived; until then the piston airplane, its transponder not yet
  reprogrammed, kept flying at home on the old address with its pilot broadcasting its own new N-number as flight_id,
  and it left the day before the turbine first appeared under the address. DEREG holds the piston airplane's
  registration cancelled on the Registry's date, MASTER the turbine's issued that day and the piston airplane's new
  registration (same serial and model). Read by the register's own dates, which is how a careful analyst resolves the
  MASTER and DEREG fan-out, the piston airplane's last weeks or months price as the turbine's (nothing); read as the
  aircraft that flew each operation, they are the piston airplane's, its broadcast identity naming it on every one.
  No sweep sees it: every address resolves, nothing repeats, the dates tie, and flight IDs that are not the address's
  own N-number are common texture (charter call signs, owners' changed numbers left in the avionics, four owners at the
  towers who moved a number to an airplane of the same kind the same way, where both readings price alike).
  Hazards: daylight time in the tower-hours filter (moves all six towers' figures when ignored), the winter hours and
  closed days at VNL and DMR, the military columns (HWK, CRV), a touch-and-go two operations, turboprops on TYPE
  AIRCRAFT 4 with TYPE ENGINE 2.
  Stops (asserted, checks.py and generator/ceiling.py): the register's own dates misses all 12 (HWK 17,200 and 21 kg,
  CRV 9,300 and 16, OSY 19,000 and 22, VNL 11,800 and 15, KTY 13,100 and 15, DMR 7,600 and 12); today's register misses
  all 12; the moved addresses' events dropped and the moved addresses read as the piston airplane all year miss at
  least 6; the aircraft that flew each operation gives all 12. The register's dates move every tower by 0.82 kg and 336
  operations or more and land every figure at least 0.28 kg and 250 operations outside the golden's bin.
  Realism: owners keep a personalised number across aircraft; the Registry's dates are its processing dates, and a
  number change waits on the avionics shop; flight IDs are entered by the crew and change when they do.
- **The construction layer:** the seven qualifying fields, the 24 leads and the chart; the cracker has them.
- **Main population zero-counts (asserted):** under the register's own dates and under today's register every
  non-towered field's lead, the counted fields' unrecorded operations and the rate are unchanged; every operation the
  two readings price differently (2,257) is at a towered field.
- **Hazard table (asserted):** the device moves all 12 figures; daylight time ignored moves six; winter hours ignored
  one; military as civil two; none moves the call or a non-towered lead.
- **Referee:** none; the towers' counts tie under every pricing (they count operations, not engines).

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, each towered field's 2026 piston-engine operations and lead | converts UTC with daylight time, keeps tower hours with the winter hours and closed days and the civil columns, counts a touch-and-go twice, prices by TYPE ENGINE and NO-ENG, resolves every address's MASTER and DEREG rows by issue and cancel dates (reader round 2's route); the moved addresses' last piston weeks resolve to the turbines and price at nothing | miss |

- Mirror leakage: 0.0 per cent of ask weight (every rung reads the towers' register the cracker's way and misses all 12:
  generator/ceiling.py).
- Pair ceiling: 39.1 (weights 38 / 7 / 55: the call 8, each of the 24 leads 1.25; the cracker keeps the main block and
  instructions, 45.0; the best mirror, R4, keeps 21 of the 24 leads, 33.2; average 39.1), rerun from the generated
  rubric at ship.
- Measured by: generator/ceiling.py on the cut pack.

## Pre-ship check

- **Three rules, re-read against the built pack.** Domain: the deciding quantity is each field's 2026 lead from piston
  aircraft, built the way airport lead inventories build it (piston operations by engine class and kind times lead per
  operation), the operations at a field without a count completed for the aircraft the receiver network never hears;
  the capture rate qualifies eight, the rate per never-recorded based airplane seven, on the clean truth and on the pack
  (checks.py R3a, R3b). Two layers: the Layer 1 inventory in `## Three rules`, each item asserted neutral on the call
  and on every non-towered lead (L1, SF2, SF9, SF10, SF12); the ask's device confined to the towered fields (separation
  rows: every operation the register's own dates price differently is at a tower); Layer 2 the choice of auxiliary.
  The decisive step is none of the three banned kinds, each executed in checks.py: not a plant (R3c: no document names
  the never-recorded airplanes, a capture or correction factor, an estimator per airplane or a verdict; no memo, draft
  or briefing ships); not data semantics (the fork table: every term read right still leaves the capture rate on eight
  fields); not rule application (R3a: every filed rule executed with one capture rate files the default path's eight;
  R3b: the per-airplane rate alone files the golden seven).
- **Gates.** 18 files in 4 formats (csv, pdf, txt, xlsx); the export at 187,609 rows; two distractors (the 5010 records,
  the declared wrong-basis distractor, and the lead monitoring samples), each deletion asserted; checks.py green (103
  rows); verify.py from the bundle alone (its own readers, time zone rule, tower-hours parser and flight-ID reading of
  the register) matches the golden; two builds byte-identical (target.zip e7020bf9dcfe1912); figures_check.py (52
  figures), precut.py (50) and voice-check.py exit 0; leak.py REVIEW (no LEAK) and three isolated readers (the last two
  landing the call, the last missing all twelve towered figures on the rebuilt device); guard heart PASS; the surface
  screen promotes task468 (two builds apart, the same calibration form and context artifact) and task36 (differentiated
  on the card) for the author; the containers normalised (PDF stamps, OOXML properties) in build.py.
- **Pair ceiling.** 39.1 measured by generator/ceiling.py with the cracker reading the register by its own dates (0 of
  12) and the best mirror on R4 (33.2), mirror leakage 0; a response that reads the flight IDs against the register
  lands the asks.

## Leak check

`leak.py --asof 2027-02-12`: REVIEW, no LEAK. Each REVIEW line answered: the guidelines carry 12.5 kg, the round's
threshold, which every literal reading uses; the method, the network and register notes and the two count reports
share the inventory's own words (operation, network, register, recorded, counts) and name no estimator, rate per
airplane or never-recorded set; the 5010 records (the declared wrong-basis distractor), the directory and the based
list name the fields beside counts, elevations and N-numbers and rank nothing on the call. Harmless.

Reader, round 1 (answers appended to `leak_check_report.md`): nothing quoted for question 1 beyond method 4.4, which
names no estimator; no file ranks the fields; question 6 an analytical choice. Its own answer qualified four fields
(A71 F37 L08 T13): it read only the first county sheet of the based validation, estimated the never-recorded share of
based airplanes there (R4b's route, checked against F37) and a median share elsewhere; on the towered fields it read
today's register for the 198 addresses MASTER and DEREG share and missed all twelve figures (16,900 and 20 kg at HWK
and so on, today's-register stop exactly). Fixed in the generator in one pass with the judge's note: MASTER now
carries pending registrations (status R) among the county's other aircraft and no current registration expires before
the download; the export's event ids take the network database's irregular share of keys; trips over more than a day
are commoner (odd daily counts at D19 on about three days in ten); method 4.2 says the towers' unrecorded operations are
taken as piston-engine operations; W33's recorded lead raised so R4b clears the line by 5.2 per cent. Harmless as
the systems' own: no air carrier operations at the towers (general aviation towers), the lead monitors at two towered
fields, a flight ID left at a cancelled number after an owner's N-number change, the 5010 records' stale and rounded
estimates (their own notes say so).

Judge, pass 1 (`determinism_check_report.md`): DETERMINISTIC, APPROVE. Every figure reproduced (23,376 over 338,
69.16; the 20 never-recorded counts; the 24 leads; the towers' operations and lead); the seven hold for any rate from
56 to 923 operations an airplane. Gate G method_or_model_selection, analytical_non_defect, surface_read_dependency no;
Gate H domain, layers, decisive step analytical. Advisory notes: method 4.4 names no estimator (closed by the data:
the per-airplane rate's coefficient of variation is 4 per cent at the counted fields against 42 to 50 for the others);
the towers' unrecorded operations taken whole as piston (now pinned in method 4.2 and write-up step 7).

Reader, round 2 (answers appended to `leak_check_report.md`): no leak; question 1 quotes method 2.2 and 4.4 and calls
the network notes' sentence on aircraft without ADS-B Out and the based list the hint (the mechanism the determinism
rule requires the network notes to state, never which or how many); no file ranks the fields; question 6 an analytical
choice. It landed the call (the pooled rate per silent based airplane, 68.96) and all twelve towered figures: it read
the 2026 DEREG rows of the moved addresses by their cancel dates, so the device of the time (today's register) was a
mirror device the register notes' DEREG description resolves, and the cracker sheet had described the mirror. Rebuilt
in the generator: the Registry's move now precedes each swap by 30 to 150 days, the old airplanes fly on under the old
address broadcasting their new numbers, the turbines arrive on the swap day; ceiling.py's cracker reads the register by
date (0 of 12). Realism fixed in the same pass: the register carries 141 aircraft models and 111 engines, each airframe
on a model of its own class built in its year, strips flying Cubs, Champs, Huskies and RVs, engines corrected per model
(the Chieftain's TIO-540-J2BD, the Baron's IO-550-C); the based list writes make and model as each sponsor does; a
lapsed airplane validated before its cancellation; two charter operators' call signs; S27 sells 100LL; the network
notes give the commissioning comparison's counts (9,603 of 9,617); the guidelines carry eligible costs, acceptance and
reporting. Harmless: one emitter category per address (set at installation), the towers' counts a full 365-day grid (as
the FAA's daily counts are), D19's daily spread (weather and weekends), even monthly turbine counts at G42 (each visit
an arrival and a departure).

Judge, pass 2 (`determinism_check_report_pass2.md`, the one re-judge): DETERMINISTIC, APPROVE on the fix-pass build.
Every figure reproduced, the seven unchanged under eight fork combinations; Gate G method_or_model_selection,
analytical_non_defect; Gate H domain, layers, decisive step analytical. Notes: method 4.4 names no estimator (the data
separates); the L08 tow-plane reading (69.75 against 69.16, no graded figure moves); the DEREG same-day boundary (17
events, no rounded figure moves). The ask's device was rebuilt after this pass with every main figure byte-identical;
its golden is the aircraft that flew each operation, asserted in checks.py and recomputed by verify.py's own reading of
the flight ID.

Reader, round 3 (answers appended to `leak_check_report.md`; a first attempt stopped before writing and was rerun on a
fresh copy of the same pack): no leak; question 1 nothing names the decisive step; question 5 method 4.2's literal
reading gives the golden's unrecorded tower operations; question 6 an analytical choice. It landed the call (the rate
per silent based airplane at the four count fields, 69.76) and read the moved addresses by the register's own dates,
missing all twelve towered figures on the cracker's stop: the rebuilt device held. Fixed (data only, no graded figure
moved): validation dates now run to the month's end and the 5010 managers round small fields to the hundred, so no two
fields' rows coincide. Harmless: the near-constant rate per silent airplane (what forces the estimator), the
commissioning counts, a number's move recorded on one date and mostly to turbines, the towers counting every operation
the network records in their hours, the counties' N-number formats, the September to December validation campaign,
two lapsed registrations still on the list, the lead monitoring file.

## Tried and rejected

- 2026-10-18, at the draw: the seed's own move, reading 2019 tail numbers through today's register, is identity
  resolution decided by reading the register right (data semantics); kept as Layer 1.
- 2026-10-18, at the draw: a 2027 projection of commercial aircraft NOx after the 50-seat jets retire, decided by a
  departure queue's relief at the hub's runway: the same lesson as task459 (a rate read at the decision's operating
  level, not the period average) in the same pairing, and a second hub ground-time task after task469.
- 2026-10-18, at the draw: the transition effect read against not-yet-transitioned airports (staggered adoption):
  already taught by task136 and task230.
- 2026-10-18, at the draw: operations at untowered fields from a rate per based aircraft learned at towered fields
  (selection on the outcome) as the decisive step alone: one live degree of freedom (every rung a different rate on
  the same based-aircraft list); kept as a lower rung beside the network route.
- 2026-10-18, at design: based broadcasting airplanes laid up for the year counted among the never-recorded: the small
  count fields' ratios split (L08 2 airplanes to 5) and the family of rate estimators spread 3 per cent; dropped.
- 2026-10-18, at design: an N-number changed late in 2026 at a count field read as never recorded by its current
  address and moved L08's ratio; changes kept to fields without a count and before September (SF12 asserted).
- 2026-10-18, at design: piston helicopters in the fleet: Table 1 is airplanes only and would need a rotorcraft factor;
  the valley's helicopters are turbine.
- 2026-10-18, at design: field targets on whole kilograms gave leads of exactly 22.00 and 3.00; offsets added so no lead
  sits within 0.02 kg of a whole kilogram and no tower's operations on a hundred.
- 2026-10-18, at stage 4: W33 under R4b (the never-recorded share of based airplanes as the unrecorded share, reader
  round 1's route) sat 0.1 per cent under the line, so that rung named no set; W33's recorded lead raised 0.38 kg, R4b
  now 5.2 per cent over, the golden W33 at 14.1 kg.
- 2026-10-18, at stage 4: today's register as the ask's primary device (the moved addresses' piston months priced as
  the turbines): reader round 2 resolved MASTER and DEREG by issue and cancel dates and hit all twelve figures, so the
  honest cracker scored 100 and the pair 66.6; the device became the Registry's dates leading the swap.
- 2026-10-18, at stage 4: the Registry's dates trailing the swap (the turbine flying under the number before its
  certificate): the turbines visit fields without a tower in that window, so the register's dates would price
  untowered operations as piston and move the call, and four towers' turbines fly too little to clear the bins.

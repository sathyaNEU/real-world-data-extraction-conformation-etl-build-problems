# task461 design note

Architecture 3, drawn 2026-11-04: a re-root of the number into a new world, dataset, generator and prompt shell.
Architecture 2 (a fuel terminal's 2026 loading VOC) died at the stage-4 determinism judge the same day and
architecture 1 (a battery's cycling threshold) at the 2026-11-02 re-check; each has its line in `## Tried and
rejected`, their build files are cleared from the folder and kept in history, and architecture 1's shipped pack stays
at the portal, pending. This build replaces it at ship. No seed: the world, the decision and the quantity are new.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task461.json`, architecture v3, registered 2026-11-04T05:38:59Z, v1 and
  v2 in its lineage with their fates. `guard.py check`: WARN only (Gate G etl_conformance and decision quantity_figure
  repeat task476 v3; answered here: the Gate G label is the honest one for a residual whose subtracted set is
  conformed from the meters' own data, on another driver in another domain).
- **Pairing:** Physical & Environmental Sciences / emissions-inventory / ETL. The call is read from a conformed set:
  the supplier's half-hourly settlement data for the building's import, the building management system's cumulative
  sub-meter registers, the meter register and the tenancy schedule conformed into the loan's base building electricity
  and its Scope 2 intensity, beside the building's Scope 1 lines (generator diesel, chiller refrigerant).
- **Why this cell:** the last three draws hold record linkage (task476 v3), groundwater exceedance (task193 v3) and
  grid reliability (task192 v4); architecture 2's card is spent and holds no axis. Emissions-inventory's twelve cards
  spend activity levels, rates by operating level, detection, leak dating, a control device's capped draw and (spent)
  a container's previous use; none subtracts a metered set whose members nest.
- **Forum and forcing event:** customer_or_counterparty (Corvane Bank, the lender) and audit_or_inspection (the
  facility's annual KPI verification). Organisation other (a listed office property trust); role portfolio_manager.
  Personas from `guard.py names --geo "United Kingdom" --seed 461`: Alice Evans (head of sustainability, signs the
  report), Kate Harding (facilities manager).
- **World:** Wexmoor Office Trust owns Pellow House, a fourteen-storey office tower in Wexmoor (a fictional northern
  English city), let floor by floor to eight occupiers, two of them on a second premises line of their own (a ground
  floor data room, a second floor taken under a later lease), with the roof licensed to Mastlink Networks for a mobile
  network equipment room. The trust's revolving credit facility with Corvane Bank is sustainability-linked: the margin
  steps up if the base building's Scope 2 emissions intensity for 2026 exceeds the schedule's target.
- **Forcing fact:** the KPI report for calendar 2026, verified in January 2027. The call is retrospective by nature: a
  covenant test reports the closed year. As of 15 January 2027 (the folder's assembly date, the `--asof` for
  `leak.py`).
- **Data-native sentence:** the building management system meters seventeen tenant circuits for recharge, all
  listed alike in the register; four of them (two comms rooms, a server room, a staff kitchen) are wired inside their
  occupiers' own supply meters, while four occupiers take a second supply on a tap-off of its own (a data room, a later
  floor, a clinic's cold room, a second floor of one lease), so neither the register, the occupier nor the location
  says which meters nest; the half-hourly registers do (each nested meter inside its parent all year and at zero
  exactly when the June switchboard maintenance isolated that parent, each independent one live through every other
  isolation).
- **Abstraction sentence:** "a remainder taken by subtracting metered parts double-counts the parts that sit inside
  other parts; the parts' own time series show which do." Nearest drivers on file at 0.06 (task471 v3 lineage,
  task270 v4 lineage), neither a hierarchy.
- **Sources, one line each:**
  - `stumping/references/client/two-layer-task-design.md`: estimand identification (which meters measure the
    estimand's subtracted set), the data's real structure.
  - `dataset-generation/references/layer1-messiness.md`: settlement periods on the local clock (46 and 50 on the
    change days), a building management system logging local time with the autumn hour twice and a server gap,
    registers in watt-hours on two older meters, a meter replaced under a new tag, a contractor's own plant codes.

## Default path

1. Conform the supplier's half-hourly settlement data into the building's monthly import (settlement date and period
   on the local clock).
2. Read each tenancy meter in the meter register from the building management system's cumulative registers at each
   month's local midnight boundaries (the replaced meter's two tags joined, the watt-hour registers converted).
3. Subtract every meter the register lists as recharged to an occupier (seventeen circuits, the replaced meter's two
   tags as one) from the import, month by month, and sum the year.
4. Multiply by the schedule's conversion factor and divide by the schedule's net lettable area; set the intensity
   against the 2026 target.

- **Ends on:** 15.6 kg CO2e per square metre for 2026, inside the 17.6 kg target.
- **Golden:** 18.5 kg CO2e per square metre, over the target by 0.9.

## Stump sentence

The default path subtracts every tenancy meter in the register from the building's import and files 15.6 kg CO2e per
square metre for 2026, inside the loan's 17.6 kg target; four of those meters measure circuits wired inside other
tenancy meters, so the default takes them out twice, and the base building's intensity is 18.5 kg, over the target by
0.9.

## Three rules

- **Task type:** emissions-inventory (Physical & Environmental Sciences), which the taxonomy tags for ETL: a building's
  Scope 2 and Scope 1 lines estimated from metered activity conformed across the supplier's settlement data, the
  building management system's registers, the meter register and the tenancy schedule.
- **Domain test:** the deciding quantity is the base building's electricity, worked the way an energy auditor works a
  sub-metered building: the building's import less each tenancy's supply, every supply counted once where it leaves
  the landlord's switchboard, with the metering hierarchy verified from the interval data rather than taken from the
  register's flat list.
- **Swap:** in a hospital's nouns ("the ward's cost less each department's metered cost") the sentence survives and the
  task does not: what decides here is that an electrical sub-circuit's half-hours sit inside its parent's and fall to
  zero when the parent supply is isolated, which no cost ledger has.
- **Layer 1:** settlement periods numbered on the local clock (46 on 29 March, 50 on 25 October); the building
  management system logging local time, the autumn hour twice, a nine-hour server gap; two older meters registering in
  watt-hours; a tenancy main replaced in August under a new tag; the generator tank dipped in millimetres; fuel
  dockets split across two notes; the refrigerant contractor's own plant codes. Each is what the producing system
  writes and none carries the call (asserted in checks.py's R2 block).
- **Layer 2:** estimand identification: the base building residual is defined on each tenancy's supply, and which
  meters are supplies is a structure of the metering the register does not record and the data show.
- **Decisive step:** read the metering hierarchy from the half-hourly registers: a tenancy meter that never exceeds
  another and reads zero exactly when that one was isolated in the June maintenance sits inside it and is not
  subtracted again; every meter that stayed live through the others' isolations is a supply of its own and is.
- **Not semantics:** no label, occupier or location field resolves which meters are nested: every tenancy meter has
  one description, three occupiers have two independent supplies each (so a shared occupier does not mean a nest),
  an independent pair shares a riser location while a nested meter sits on another floor from its parent; only the
  interval counters and the isolations do. Every field read correctly still leaves the default at 15.6 kg.
- **Not rule application:** the KPI schedule files the WHAT (the import less the electricity supplied to the tenancies,
  metered at each tenancy's supply, over the net lettable area, at the filed factor); executing it with the register's
  list files the default, and no rule says which meters are supplies.
- **Analyst test:** with the settlement data and the registers conformed and the KPI schedule applied, a strong
  analyst subtracts every meter the register marks as recharged to an occupier and files 15.6 kg CO2e per square
  metre, inside the 17.6 kg target, because no field says that four of those meters sit inside others; the readings
  that try to sort them by occupier, premises, size, profile or location each file another figure (the Ladder).
- **Estimand:** the KPI schedule: Base Building Electricity for calendar 2026 (the building's local time) is the
  electricity imported through the revenue meter less the electricity supplied to the tenancies (every part let or
  licensed, the roof licence included) as metered at each tenancy's supply; its Scope 2 emissions at the schedule's
  factor; the intensity over the schedule's net lettable area; the target.
- **No decoy:** nothing is planted: sub-meters on comms rooms, server rooms and kitchens downstream of an occupier's
  supply are how fitted offices are wired and recharged; the independent second supplies are the occupiers' own
  premises and circuits (the tenancy schedule's data room and later floor, a clinic's cold room, a two-floor lease fed
  floor by floor), and the June maintenance isolates supplies because it tests the switchboard; no memo, prior report,
  draft or stakeholder figure ships.
- **No certified replay:** no certified figure carries a base building total; the energy performance certificate (a
  declared distractor) is an asset rating, not an operational figure.
- **Lesson:** a remainder after subtracting metered parts is only right when the parts are disjoint, and a flat meter
  list does not say whether they are; the interval data do. No build on file teaches it.

## Survivor anatomy

- **Actor:** pass. The deciding property, whether a tenancy meter sits inside another, has no column in any file: it
  is a relation between two meters' half-hourly series.
- **Link:** pass. The relation is between rows of one export under different tags, and no key, column or sentence
  pairs a nested meter with its parent; the register, the occupier and the location columns point both ways.
- **Reflex:** pass. The field's reflex (import less every listed tenancy meter) is rung 0 and files the `Ends on:`
  figure.
- **Back-test:** pass. The reflex passes the auditor's usual control: the tenancy meters sum to well under the import
  in every half-hour, so nothing looks double counted.
- **Second use:** pass. Every file the decisive step reads has its own use: the registers and the settlement data are
  the KPI's inputs on every path, the meter register is the recharge list, the tenancy schedule carries the lettable
  areas.
- **Shock:** pass. The nested meters are four of seventeen tenancy circuits, ordinary loads running all year; nothing
  in the pack singles them out.
- **Pins:** pass. The schedule files the WHAT (import, tenancy supplies, area, factor, period) and no sentence names
  a comms room, a hierarchy or the maintenance.

## Readability screen

Each rung against the seven tests (1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear, 7 second
use); the reflex row comes from the field's vocabulary for sub-metered buildings (base building, tenancy supply, the
meter list).

| Rung | 1 | 2 | 3 | 4 | 5 | 6 | 7 | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 every tenancy meter in the register subtracted (15.6 kg) | schedule 1.4 read against the register's list | the register's Recharged to occupier column | yes | the meters sum under the import in every half-hour | no | yes | no | readable |
| R1 one meter per occupier, per premises line, the smallest or the flat ones dropped, or by location (17.7 to 22.1 kg) | no | the occupier, location and tenancy schedule columns | no | no | no | yes | no | readable |
| G (decisive) the tenancy meters whose half-hours sit inside another tenancy meter's, at zero with it in the June isolations, counted once (18.5 kg) | no sentence names a hierarchy, a circuit or the maintenance | no column holds a parent, a feed or a board | no: the reflex subtracts the list | no control ties only under it | no | no: a pairwise test across seventeen meters' series | the registers are the KPI's inputs on every path | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the Measurement Period | the local calendar year | a UTC year | same call, same figures | schedule 1.2; both year ends fall in GMT, so the two years coincide |
| SF2 | the roof licensee's room | a Tenancy, its supply subtracted | not a Tenancy | missed, a higher figure | schedule 1.3: "including any licence of the roof" |
| SF3 | the area divided by | 21,460 m2 | the let area alone | missed, a higher figure | schedule 1.5 files the figure; the tenancy schedule's areas sum to it |
| SF4 | the conversion factor and the target | 0.20705 kg per kWh; 17.6 kg per m2 | another year's factor or target | not open | schedule 2.1 and part 3 |
| SF5 | the replaced meter | EM-110 to its last reading, EM-118 from zero | either tag alone | missed | asserted: EM-110's last register sits at the swap and EM-118 starts there at zero |
| SF6 | the watt-hour registers | divided by 1,000 | read as kWh | absurd (every month below zero) | the export's Units column and the register's units |
| SF7 | a month's boundaries | local midnights | the autumn repeat or the spring gap | same call | asserted: no boundary sits in either |
| SF8 | over the target | strictly above it | at or above | same call, 0.9 clear | schedule 3.1 ("exceeds") |
| SF9 | rounding | the prompt's closing sentence | other precisions | same call | the prompt |
| SF10 | a quarter's stock in the day tank | the week's burn placed on that week's runs | a straight line between dips; the nearer dip | asks only | asserted: every quarter's midnight sits in a dip week whose runs all fall on one side of it |
| SF11 | a quarter | three calendar months of the local year | another cut | asks only | schedule 1.2 |
| SF12 | a dip's litres | the calibration chart's row for the dip | a straight line from the diameter | asks only | the chart lists every millimetre |
| SF13 | the Scope 1 factors | 2.6594 kg CO2e per litre; GWP 1,430 | others | asks only | schedule 4.2 and 4.3 |
| SF14 | a recovery's chiller | the job reference both records carry | the contractor's plant code read as the chiller number | asks only | asserted: every recovery job is a recharge job in the F-gas log, one per chiller |
| SF15 | refrigerant released | the charge added less the charge recovered to cylinders | every kilogram added; the top-ups alone | asks only | asserted: each golden figure is positive and below the chiller's top-ups plus a tenth of its charge |
| SF16 | the year | the sum of the unrounded months | the sum of rounded months | same call | asserted |
| SF17 | the rounded months against the rounded year | the twelve rounded months sum to the rounded year | months rounded and summed | same figure, 1,914 MWh | C1 in the data, asserted |
| SF18 | the Scope 2 rounding path | the unrounded year times the factor | the rounded year times the factor | same figure, 396.3 t | C1 in the data, asserted: both paths print one tenth, clear of its edge |
| SF19 | the first dip week's runs | none before 1 January (the controller export opens on 15 December 2025) | an unrecorded run | asks only, same quarter | the export's own window, asserted |

## Ladder

Every reading priced on the cut pack (golden.py's subtracted(), asserted in checks.py R3b: none files the golden's
18.5):
- **Rung 0, the field's reflex (15.6 kg, met by 2.0):** every meter the register marks as recharged subtracted, the
  four nested meters taken out twice.
- **Readings that sort without the counters, each over the target at another figure:** one meter per occupier (21.4,
  drops the second supplies), first-listed meter per occupier (22.1), one meter per premises line (19.7, drops the cold
  room and one of a two-floor lease's supplies), each multi-meter occupier's smallest left out (19.3), flat-profile
  meters of multi-meter occupiers left out (19.5, drops the data room and the cold room, keeps the kitchen), flat
  meters sharing premises with an office meter left out (18.7, drops the cold room, keeps the kitchen), a meter
  sharing its location with a larger one of its occupier left out (17.7, keeps the comms room on another floor from its
  parent, drops the cold room).
- **The counters with the maintenance day cleaned out (31.3 kg):** containment alone, the shutdown zeros dropped as a
  data gap, nests independent supplies inside larger ones.
- **Rung 1, decisive (18.5 kg, missed by 0.9):** EM-102, EM-105, EM-108 and EM-117 sit inside EM-101, EM-104, EM-115
  and EM-112 (never above them all year, at zero exactly when those supplies were isolated on 13 June); the thirteen
  other circuits stayed live through every other isolation and are supplies of their own.
- **Separation:** the call flips between rung 0 and the golden; every other reading files another figure at least 0.2
  away; the golden reproduces the clean truth within the meters' accuracy.
- **Mess neutrality:** every Layer 1 item mishandled keeps the golden over the target and rung 0 under it (checks.py's
  R2 block); the watt-hour misreading gives an absurd negative base building.

## Closure table

| Axis | Reading here | Move |
|---|---|---|
| 1 Population | the import less every Tenancy's supply, the roof licence included | filed: schedule 1.3, 1.4 |
| 2 Unit of account | kWh, t CO2e, kg CO2e per m2 | filed: schedule part 2 |
| 3 Attribution window | the local calendar year and its months | filed: schedule 1.2; SF1 |
| 4 As-of dating | the 2026 records exported in January 2027, every month closed | static |
| 5 Version basis | the 2025 facility agreement's Schedule 9, the only version shipped | filed |
| 6 Denominator | 21,460 m2 | filed: schedule 1.5; SF3 |
| 7 Weighting | none, sums | not applicable |
| 8 Window length | one calendar year | filed: schedule 1.2 |
| 9 Boundary inclusivity | registers read at local midnights | SF7 |
| 10 Rounding path | unrounded months summed, each figure rounded once at print | SF16, asserted bins |
| 11 Tie-break | none | not applicable |
| 12 Maturity and censoring | no month open; the supplier data all actual reads | static |
| 13 Order of operations | the residual first, then the factor, then the area | filed: schedule part 2 |
| 14 Row order | sums independent of order | C1 |
| 15 Duplicate resolution | each supply once; the autumn hour's two passes of a register never differenced across | SF7 |
| 16 Identity normalisation | EM-110 and EM-118 one supply | SF5 |
| 17 Netting against gross | the import at the revenue meter, gross of losses inside the building | filed: schedule 1.4 |
| 18 Dimensional units | Wh to kWh on two registers; kWh to MWh | SF6 |
| 19 Code and status semantics | the supplier's read type A on every period | static |
| 20 Integerisation | none in the call | not applicable |
| 21 Clause scope | Scope 1 lines are reported beside the KPI and do not enter it | filed: schedule 2.2, 4.1 |
| 22 Forward window contents | none: retrospective, the closed 2026 year | the reason in Draw |

## Literal reader

Executed word for word, the schedule fixes the population (the import through the revenue meter less the electricity
supplied to the Tenancies, the roof licence a Tenancy), the period (the local calendar year), the factor, the area
and the target. "As metered at each Tenancy's supply" names where each Tenancy's electricity is counted and says
nothing about which meters those are; read with the building's own half-hourly registers, a meter that never draws
more than another and goes dark exactly when that one is isolated is inside it, so the literal reading files the golden
(18.5 kg, missed). No filed sentence lists the meters to subtract, so no sentence executes to rung 0; the register's
list is data, and its fields sort nothing.

## Oracles

None arbitrates the decisive step. The supplier's import is the same on every rung; the base building's own
sub-meters (mechanical, lifts, common lighting, car park) leave an unmetered remainder and tie to no rung; the energy
performance certificate (a declared distractor) is an asset rating. The hierarchy is read only from the meters' own
half-hourly series.

## Leak review

`leak.py task461 --asof 2027-01-15` on the final cut: REVIEW, no LEAK. One line per REVIEW:
- Sweep 2, "generator" in schedule 4.2: the standby generator, a field term declared in metadata.json. Harmless.
- Sweep 3, the schedule carries 9 of the call's 11 distinctive words: the schedule's own nouns (the building, the
  base building, the target, the bank); it states no result. Harmless.
- Sweep 4, the schedule carries 4 stump terms (tenancy, supply, metered, import): the words of the definition the KPI
  is filed in, which names no meter, room or hierarchy (checks.py reads it back). Harmless.
- Sweep 12, the schedule names 4 column words (MPAN, refrigerant, litres): its own vocabulary; it describes no column
  or join. Harmless.
- Fixed on this cut: the weather columns (temp read as a generator's word) and the registers' dates (written in the
  UK form the trust's spreadsheets use, so the lease expiries are no longer ISO dates after the as-of).

Rulings on the stage-4 reader and sweeps (the reader's answers sit under `## Solver's-eye read` in
leak_check_report.md; the judge returned DETERMINISTIC, APPROVE on the first pass):
- Reader question 6 ("leans toward data semantics and rule application"): a surface read, the reader never found the
  nesting; the judge recomputed it (0 exceedances in 17,596 intervals, zeros at the 13 June isolations) and classed
  the decisive step analytical. No return to stage 2.
- Sweep 2 ("generator" in the schedule): harmless, the field's own noun (the standby generator), declared under
  field_terms in metadata.json.
- Sweep 4 (tenancy, supply, import, metered, occupier in Schedule 9): harmless, the KPI definition's own words, the
  WHAT; the schedule names no meter, hierarchy, comms room or nesting.
- Sweeps 3 and 12 on Schedule 9: harmless, per the reader: the parties' executed agreement, standing terms and no 2026
  result.
- Fixed after stage 4, results unchanged: the prompt pins both one-decimal roundings ("each to one decimal"); the
  goldens say the months and the year are rounded independently (after the data closure below the twelve months
  add to the year's 1,914); each workbook carries its own organisation as author (the trust's asset manager, the BMS integrator with no
  author, the tank maker, the contractor); the split gas oil delivery reads as two consecutive dockets, each as its
  compartment's discharge ends.
- Re-sited after the re-judge's Gate H note (the register's descriptions had sorted the meters on the
  decisive property): one description on every tenancy meter, four occupiers' independent second supplies (two on
  their own premises lines, a clinic's cold room, a two-floor lease fed floor by floor) and a nested kitchen with an
  office-like profile, so neither the labels, the occupier, the location nor the profile resolves the hierarchy;
  the call holds (18.5 kg, missed by 0.9), rung 0 moves to 15.6 and the gas oil quarters move with the world's
  draws.

- Closed by C1 in the data before ship (asserted in checks.py SF17 to SF19): the unmetered base load moved by 0.352
  kW so the twelve rounded months sum to the rounded year (1,914 MWh) and Scope 2 prints 396.3 t from the unrounded or
  the rounded year; the call holds (18.5 kg, missed by 0.9). The generator controller export now opens on 15 December
  2025, so the first dip week's days without a run are on record.
- Second reader, CT ratios and shared risers: a circumstantial hint, harmless; EM-119 (independent, whole current) and
  EM-102 (nested, whole current) look alike, so neither sorts the hierarchy.
- Second reader, Calbrook's PH plant references and dates against the F-gas log's CH tags: harmless; they read as two
  separate systems, joined by the job reference.

## Ask sheet

Planning weights 38 / 7 / 55. The monthly base building figures, the year, the Scope 2 tonnes, the KPI, the result and
the margin are the call's own construction and are scored with it. The asks are the building's Scope 1 lines, which
Schedule 9 part 4 requires beside the KPI: A, the gas oil the standby generator burned in each quarter with its
emissions (8 figures); B, the refrigerant each chiller released with its emissions (8 figures).

- **Ask A, gas oil by quarter:** H18 home: the KPI report's Scope 1 lines (schedule 4.1 and 4.2). Path: the weekly
  dips (5 columns), the calibration chart (2), the dockets (7), the controller events (4). Primary: the tank is dipped
  on Monday mornings and each quarter's local midnight falls mid-week; the burn between two dips belongs to that week's
  runs (controller events), all on one side of the midnight, so the quarter's stock is the dip on that side; a straight
  line between dips moves every quarter (569, 253, 391, 484 litres against 575, 312, 325, 446) and so does the nearer
  dip. Hazards: the non-linear chart, a delivery split across two dockets. Pin test: the asking sentence pins the
  quarter and the unit; no pin names the dip day, the runs or the placement. Realism: weekly dips and weekly off-load
  tests are how standby plant is kept; the tests move for holidays.
- **Ask B, refrigerant by chiller:** H18 home: the KPI report's Scope 1 lines (schedule 4.3). Path: the F-gas log (8
  columns) and the contractor's recovery record (8). Primary: every chiller was re-tubed in 2026 and its full charge
  recovered to cylinders before the recharge; the F-gas log shows the recharge as an addition and only the contractor's
  record shows what was recovered, joined by job reference; every kilogram added (193.7, 200.3, 249.6, 251.6) or the
  top-ups alone (7.7, 14.3, 9.6, 11.6) miss every chiller (golden 10.8, 20.7, 14.8, 20.5). Hazards: the contractor's
  plant codes in another order (PH-03 is CH-1), leak checks with nothing added, recoveries split across cylinders.
  Pin test: schedule 4.3 files "released" and the GWP, not the method.
- **Main population zero-counts:** no ask organ sits in a file the main call reads (checks.py separation); the asks'
  six files are never read by the KPI.
- **The full includer:** a response that places each week's burn on its runs and joins each recovery by its job keeps
  both asks; neither ask carries a second device from another family, a known limit of this layer recorded here.
- **Referee:** none; every ask figure is recomputed on `generator/verify.py`'s own path.

| Ask figure | Cracker (a straight line between dips, the re-tube recharges left out) | Golden | Cracker |
|---|---|---|---|
| A: Q1 gas oil (litres) | 569 | 575 | miss |
| A: Q1 gas oil (kg CO2e) | 1514 | 1529 | miss |
| A: Q2 gas oil (litres) | 253 | 312 | miss |
| A: Q2 gas oil (kg CO2e) | 672 | 830 | miss |
| A: Q3 gas oil (litres) | 391 | 325 | miss |
| A: Q3 gas oil (kg CO2e) | 1039 | 864 | miss |
| A: Q4 gas oil (litres) | 484 | 446 | miss |
| A: Q4 gas oil (kg CO2e) | 1288 | 1186 | miss |
| B: CH-1 refrigerant (kg) | 7.7 | 10.8 | miss |
| B: CH-1 refrigerant (kg CO2e) | 11011 | 15444 | miss |
| B: CH-2 refrigerant (kg) | 14.3 | 20.7 | miss |
| B: CH-2 refrigerant (kg CO2e) | 20449 | 29601 | miss |
| B: CH-3 refrigerant (kg) | 9.6 | 14.8 | miss |
| B: CH-3 refrigerant (kg CO2e) | 13728 | 21164 | miss |
| B: CH-4 refrigerant (kg) | 11.6 | 20.5 | miss |
| B: CH-4 refrigerant (kg CO2e) | 16588 | 29315 | miss |

Pair ceiling: 26.0 (the cracker 45.0 on the call keeping no ask figure, the mirror 7.0 off it at 15.6 kg, keeping no
monthly figure, r 0.0).
Mirror leakage: 0.0 per cent of ask weight (the mirror, stopping at rung 0, takes the same route on the asks).
Measured by: generator/ceiling.py, on the cut pack.

## Tried and rejected

- 2026-10-15, draw: the seed's own stump, a replay grouped by UTC dates that moves the charge and discharge hours across
  the operating day. Rejected: catching the clock is reading a field correctly (data semantics), banned as the decisive
  step; the clocks stay as Layer 1 mess and must leave the call where it is.
- 2026-10-15, design: a mild 2026 that lowered every day's swing (the year's average spread 34 per cent under the
  others). Rejected: an average that low after seven flat years reads as a structural break, a defensible reason to
  keep the node's year, and the additive premium landed within a dollar of the golden's level; the windy year that
  widens the tail and keeps the average, with an earlier windy year that reverted, replaced it.
- 2026-10-15, design: the BMS's own cumulative cycle counter in the export. Dropped: it recovered the dropped hours'
  energy at the BMS's usable-energy denominator, a second recovery that disagreed with warranty 4.3 at two decimals.
- 2026-10-15, design: the node's spread exactly 2.2 times the hub's every day (correlation 1.000). Replaced by a daily
  congestion variation (the ratio's spread 0.25), which reads as a market and leaves every rung where it was.
- 2026-11-02, re-check under the new gates: architecture 1 found spent, no repair made. The node's-own-year reading is
  either refuted by the data, and then the standing family (every pooled extension, every persistence model fitted
  to the record) is unanimous on $20 and the golden is the field's textbook long-term correction applied as stated
  (the Reflex line fails, standing spread zero), or it stays open on the current stretch's persistence and is a fork
  whose only closing sentence names the record the step recognises (the fork-is-the-stump test). Either way a gate
  fails; the shipped cut also fails leak.py (the data dictionary and the manifest by name; metadata.json carrying 300)
  and precut (no Measured by line on the ask sheet), and guard heart now BLOCKs (same puzzle and same driver against
  task174, task178, task242 and task476, not caused by this re-check). The re-root is the orchestrating session's call.
- 2026-11-04, re-root: architecture 1 left as spent (above), its build files cleared from the folder (kept in
  history); architecture 2 drawn in Physical & Environmental Sciences on a new world, dataset and prompt shell, one
  architecture per world. The screens of this draw, each with a default path ending wrong, the swap test, the anatomy
  lines and the bin test on paper, follow; the thirteenth was priced in code and carded.
- 2026-11-04, screen 1, emissions-inventory, a river port's transit emissions from AIS speed over ground in a tidal
  current: for vessels holding their speed through the water the round trip's bias is STW^4 / (STW^4 - c^4), 1.006 at
  11 knots in a 3-knot current, so the decisive step is worth under one per cent (bin test dead); the current record
  would ship only for the step (dedicated organ) and its spread along the channel forks.
- 2026-11-04, screen 2, emissions-inventory, a landfill's methane with collection efficiency weighted by cover area
  against by modelled generation (young cells under daily cover generate most): the area weighting is the reporting
  rule's own formula, so filed it is an official decoy and unfiled the golden is a model of the measurement whose every
  input is a default (decay rate, generation potential, efficiency by cover), forking past the step's worth.
- 2026-11-04, screen 3, emissions-inventory, floating-roof landings at a tank farm: the level record against each
  tank's leg height on the register is a row predicate on two shipped columns, and landing losses are a named term of
  the field's own tank equations (readable, a reflex).
- 2026-11-04, screen 4, emissions-inventory, a flare's destruction falling at low vent-gas flow under minimum steam:
  the combustion-zone heating value test is the field's named check, and the abstraction equals task479 v7's (a control
  device's tested removal fails in the intervals where coincident flows breach its operating condition).
- 2026-11-04, screen 5, emissions-inventory, catalyst warm-up after cold starts at peaking engines: with the dosing log
  shipped the uncontrolled minutes are present in the records (rule application); without it the cool-down constant is
  a free parameter (Gate C).
- 2026-11-04, screen 6, emissions-inventory, a river's phosphorus load with storm hysteresis on the rising limb: the
  rating regression is the field's method and the limb term is a specification extension, closed as a class by the
  bin-test identity (determinism-check section 3).
- 2026-11-04, screen 7, payment-claims, a plan's cost per member month with capitated encounters at zero paid: paid zero
  beside the capitation flag is a column, and repricing at the fee schedule is a filed rule.
- 2026-11-04, screen 8, item-response-theory-test-equating, optional essay questions of unequal difficulty linked
  through the compulsory section: task450's driver (two groups that differ in instrument and in group, linked only
  through a shared subset).
- 2026-11-04, screen 9, seasonal-adjustment-official-time-series-production, traffic count expansion factors for short
  counts near a single facility: task474's driver (sites serving one facility follow its own schedule, which the
  reference sites never see).
- 2026-11-04, screen 10, data-integration, a plant's mass-balance reconciliation with meter errors correlated through a
  shared densitometer: finding a drifted shared instrument is a planted defect when it flips the call (Gate G), and the
  covariance is a fitted structure (Gate C).
- 2026-11-04, screen 11, emissions-inventory, ammonia from broiler houses on litter reused across flocks: the
  emission-by-litter-age curve is a fitted dose response (a model of the measurement), and the honest label
  composition_mix BLOCKs ban.strategy against task200.
- 2026-11-04, screen 12, emissions-inventory, ethylene oxide off-gassing from product after shortened aeration: the
  desorption needs two rate constants (heated aeration, ambient warehouse) fitted from residual tests (Gate C).
- 2026-11-04, prototype 1 of screen 13 (proto_switch.py, three seeds): a 22-set fleet put 363 ML of diesel through the
  bays and lifted the partner's petrol inside mixed trips, so the terminal-exports-only compartment history landed
  within 5 per cent of the dockets' (no rung) at volumes no regional terminal moves; retuned (proto_switch2.py) to six
  semi-trailers, three B-doubles and a five-trailer dedicated carrier, with the exchange as all-petrol trips: rung 0 at
  0.33 tonnes on the distillate bays, the exports-only history at 0.84 of the golden, every retail diesel load at petrol
  vapour at 1.89, the dockets' construction about 47 tonnes, the temperature convention inert (0.998), saturation 0.6
  at 0.60 of the golden, on three seeds.
- 2026-11-04, build: dockets stamped in UTC with the terminal on local time. Dropped: reading the UTC stamps as local
  moved every compartment's previous delivery by ten or eleven hours and left the release at 16.2 tonnes, inside the
  limit, so Layer 1 carried the call; the dockets now carry each time with its own offset.
- 2026-11-04, build: a fixed bin floor (0.01 t on every quarter, 0.06 kL on the first-half gains) chosen by hand.
  Replaced by the spreads the readings put on each figure, measured in checks.py (the equation's US-unit form and the
  exact gas constant on every loading figure; per-load rounding and the unrounded 54B VCF on every gain), with the
  world seed searched until every figure keeps its bin under them.
- 2026-11-04, build: the stock account and the tank method with five cells no device reached (TK-2 and TK-3 in the
  third quarter and TK-3 in the fourth, whose boundaries fall in standard time; TK-4 and TK-5, whose register entry was
  their whole 2026 history), so the careful route kept them. Re-sited onto the terminal's own records: VRU-1's absorber
  moved to TK-2 and TK-3 during three valve repairs (the shift log's line-ups), and the diesel tanks' vents changed in
  March and August (the work orders); the careful route now keeps none of the 25.
- 2026-11-04, build: the dispatch dockets read only by the decisive step (the second-use test). Given their own use: the
  petrol rack's loads on manual bills of lading during two controller faults, which the dispatch system holds and the
  terminal system never received, enter the stock account from the dockets; the delivery sites list, read by nothing,
  is declared a distractor.
- 2026-11-04, architecture 2 died at the stage-4 determinism judge (NOT_DETERMINISTIC, SEND_BACK; report in
  determinism_check_report.md): gates B, C and E on external dependency (the golden needed a previous-cargo
  displaced-vapour rule, the saturation factors 1.0 and 0.6 and the loading-loss equation, none in a shipped file, and
  protocol 4.4 read literally charged bays 4 and 5 at diesel's own vapour, the easy answer), nothing in the pack
  separated the readings (vr1_hose was Y on every petrol line and blank on every diesel one, a product flag, and bays
  4 and 5 had no measurement), and Gate H read the step as rule application bordering a withheld rule; the leak reader
  found the call decided by stated procedure and two ask devices stated in plain words (a shift log and a work order
  naming the gauging clock). Re-rooted, never resumed; the lesson carried into architecture 3: the filed WHAT executes
  literally to the golden, no filed sentence executes to the easy answer, the correction is forced by the shipped data
  with margin and needs no outside constant, and no log line or work order states a clock or unit convention.

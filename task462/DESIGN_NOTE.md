# task462 design note

Architecture 2, drawn 2026-11-04: a re-root of the number into a new domain, world, dataset, generator and prompt shell.
Architecture 1 (a gas basin's methane ratings from aerial surveys) was found spent at the 2026-11-02 re-check; its line
is in `## Tried and rejected`, its build files are cleared from the folder and kept in history, and its shipped pack
(target.zip 33e6d0c4) stays at the portal, pending. This build replaces it at ship. No seed: the world, the decision and
the quantity are new.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task462.json`, architecture v2, registered 2026-11-04T08:40:22Z, v1 in its
  lineage with its fate. First drawn in a steelworks' ore yard (registered 08:31) and redrawn the same morning into a
  power plant's coal yard when task476 v4 and task488 v2, registered earlier in parallel, took six of its axes (line in
  `## Tried and rejected`). `guard.py check`: WARN (overuse.objective, the lane's own objective) and a NOTE
  (test.same_driver_older against task190 v6, task195, task228's lineage and task478 v7, each differentiated on the
  card: none takes a volume against a surface).
- **Pairing:** house domain Business & Operations Analytics (subdomain other: a utility's fuel stock measurement), mapped
  to the client domain General Statistics & Data Science, task type data-integration-record-linkage-entity-resolution,
  objective ETL. The call is read from a conformed set: a year of monthly drone surveys of the coal yard by two survey
  contractors (two grids, two height systems, two export formats) conformed into one surface record, each pile's
  December volume taken against the pad beneath it, times the fuel laboratory's bulk density for its coal.
- **Why this cell:** the last three draws hold emissions inventory (task461 v3), record linkage (task476 v4) and a
  hydrant's recalled fuel in supply chain (task488 v2), so the pairing leaves those three domains; the draw screened
  every ETL task type (the screens below, each with its death), and the survivor is a stock measurement on a physical
  record, where the forcing file pins a surface rather than an identity, a grain or a clock.
- **Forum and forcing event:** executive_team (the energy company's management team signs the winter fuel statement and
  any purchase it triggers) and purchase_order_or_contract (the coal supply agreement's winter option, nominated by 8
  January for an ice-class loading in late January; after it nothing reaches the harbour in volume until the spring
  opening). Organisation utility_or_infrastructure (a city-owned combined heat and power company); role capacity_planner
  (the fuel manager plans the yard's stock against the plants' burn plan). Personas from `guard.py names --geo Finland
  --seed 462`: Kirsi Salo (fuel manager, signs the statement), Aaro Miettinen (survey engineer), Maarit Vainio (fuel
  laboratory), Pekka Jalonen (yard supervisor), Marianne Kosonen and Karoliina Huttunen (the two contractors' surveyors).
- **World:** Rannikon Lämpö Oy, a city-owned energy company on the Gulf of Bothnia coast, runs a combined heat and power
  plant at the harbour whose coal unit and peak boilers burn coal from a yard of six piles on reclaimed harbour land, fed
  by a grab unloader at the plant quay, a stacker and reclaimers on rails. Coal comes from Carbones Montoya Vélez S.A.S.
  (Colombia), Tygart Run Energy Sales LLC (United States) and Silesia Fuels Sp. z o.o. (Poland), with spot cargoes bought
  through Kattegat Bulk Trading ApS. The yard is surveyed each month by drone, by Mittaus-Saarinen Oy to June 2026 (the
  plant grid, N60 heights, ESRI ASCII grids) and by Pohjoisen Dronekartoitus Oy from July (ETRS-TM35FIN, N2000 heights,
  XYZ text).
- **Forcing fact:** the fuel security procedure's floor (60 days of the first-quarter burn plan at the December survey)
  and the Silesia agreement's winter option, nominated by 8 January 2027. The call faces forward (the first quarter of
  2027 is not yet run). As of 4 January 2027 (the folder's assembly date, the `--asof` for `leak.py`).
- **Data-native sentence:** the piles stand on reclaimed harbour land and have been stacked on the same footprints for
  decades, so the pad has consolidated into a bowl under each long-standing pile, which the December survey cannot see
  because the pile covers it; the year's monthly surveys show each such pile reclaimed to the pad once (the yard rotates
  its coal against weathering and self-heating), in one or the other contractor's grid and height system, while the
  pile area added in 2025 has no bowl and so confirms the base through the toe wherever anyone checks it.
- **Abstraction sentence:** "an amount held above a surface that has sunk under its loads is understated by a surface
  through the loads' edges; the record shows the true surface only where a load was taken away." Nearest drivers on
  file at 0.07 (task251 v4 lineage) and 0.05, none a base surface.
- **Sources, one line each:**
  - `stumping/references/client/two-layer-task-design.md`: the field's method at rung 0 and the decisive step its
    violated precondition (a base through the toe assumes the pad under a pile continues the pad at its edge).
  - `dataset-generation/references/layer1-messiness.md`: two contractors on two grids and height systems, ESRI ASCII
    grids against semicolon XYZ with decimal commas, NODATA where a machine stood, a laboratory unit change, a port
    system in UTC against the plant's Finnish time, a plant historian's catch-up after communication losses, a
    belt-scale integrator replaced mid-year, a trading house shipping a producer's coal under its own name.

## Default path

1. Read the 16 December 2026 survey (contractor B's XYZ lattice in ETRS-TM35FIN, N2000 heights, decimal commas) and
   place the pile area register's plant grid corners on it with the July 2026 control report's transformation.
2. In each pile area, find the pile's edge on the December surface and fit a plane through the ring of yard pad just
   outside the toe, the stock surveyor's standard base for a pile with no base survey under it.
3. Take each pile's volume above its toe plane, multiply by the fuel laboratory's latest density for its coal (PR-07
   3.2) and sum the six areas.
4. Divide by the approved plan's first-quarter burn per day (218,740 t over 90 days, PR-07 3.3), set the days of cover
   against the 60-day floor and apply PR-07 5.

- **Ends on:** 138,000 t, 57 days of cover, under the 60-day floor: nominate Silesia's winter option cargo.
- **Golden:** 150,000 t, 62 days of cover, over the floor by 4,000 t: do not nominate; the option lapses.

## Stump sentence

The default path takes each pile's December volume above a plane fitted through its toe and files 138,000 t, 57 days of
cover, under the 60-day floor, so it nominates the winter option cargo; the yard pad has settled into bowls up to about
two metres deep under the five long-standing pile areas, which the year's surveys show where each area was rotated to
its pad, and measured against that pad the reserve is 150,000 t, 62 days, and no cargo is needed.

## Three rules

- **Task type:** data-integration-record-linkage-entity-resolution (General Statistics & Data Science, mapped from the
  house domain Business & Operations Analytics), which the taxonomy tags for ETL: a year of surveys from two
  contractors in two grids, two height systems and two export formats conformed into one surface record of the yard,
  each pile measured against the pad beneath it.
- **Domain test:** the deciding quantity is a stockpile inventory worked the way a stock-survey team works it: the
  volume between the survey surface and the surface the pile stands on, times the material's tested bulk density,
  with the standing surface conformed from the survey archive rather than assumed.
- **Swap:** in a warehouse's nouns ("pallets above the floor") the sentence survives and the task does not: what
  decides here is a yard pad on reclaimed harbour land consolidating under decades of coal loads, so the surface a pile
  stands on lies below the surface at its edge, a geometry no count of discrete units has.
- **Layer 1:** contractor A's ESRI ASCII grids on the plant grid with N60 heights and NODATA where a machine stood;
  contractor B's semicolon XYZ lattice with decimal commas and Finnish headers in ETRS-TM35FIN with N2000 heights,
  machines cut out; the laboratory writing kg/m3 until July and t/m3 after; the port's berth log in UTC; a historian
  computing interval tonnage from totalisers with catch-ups after communication losses; the CV-21 integrator replaced in
  June with its totaliser restarting; a trading house shipping two producers' coal. Each is what its system writes and
  none carries the call (checks.py: SF4, SF8, SF16, SF17; leaving the height shift out still lets the cargo lapse).
- **Layer 2:** the field's method (a base through the pile's toe) assumes the ground under a pile continues the ground
  at its edge; on this yard that precondition fails under the long-standing areas, and only the year's own surveys,
  conformed across the two contractors, show where the pad really is.
- **Decisive step:** take as each area's pad the surface the year's surveys recorded with that area bare (its rotation
  survey, in whichever contractor's grid and height system it was flown), not a surface drawn through the December
  pile's toe.
- **Not semantics:** no field, code, unit or label records the pad under a pile; every field read correctly (both
  grids, both height systems, the decimal commas, the density units, the register's corners) still leaves the toe
  route at 138,000 t, and the procedure's "above the yard pad" is read the same way on every route.
- **Not rule application:** PR-07 files the WHAT (coal above the yard pad at the December survey, times the latest
  density, over the plan's burn per day, against 60 days); executing it needs the pad's surface under each pile, and no
  rule says where that is or which survey shows it.
- **Analyst test:** with both contractors' surveys aligned and PR-07 applied as written, a strong analyst takes each
  pile's December volume above a plane through its toe, the stock surveyor's standard base, which the new pile area's
  own bare surveys and the year's book roll-forward both confirm, and files 138,000 t, 57 days, under the 60-day floor,
  nominating the winter option cargo.
- **Estimand:** PR-07 3.1 to 3.4 and 4: the tonnes of coal held in the coal yard (pile areas P1 to P6, the bunkers and
  coal afloat excluded) at the survey flown in December, each area's volume of coal above the yard pad times the
  density the laboratory last determined for that coal before the survey, divided by the approved plan's
  January-to-March burn over the quarter's days, against 60 days; fewer than 60 nominates the option.
- **No decoy:** nothing is planted: piles stacked on the same footprints for decades settle soft ground, the yard
  rotates its coal against weathering and self-heating so each area is reclaimed to its pad once a year, and the 2025
  extension (P6) has no bowl because it has carried coal for one season; no memo, prior statement, contractor volume
  report or stakeholder figure ships.
- **No certified replay:** no shipped figure is a reserve or a volume; the book roll-forward lands within about 2 per
  cent of the survey under the toe route and under the golden alike (checks.py back-test), so it certifies neither.
- **Lesson:** a stockpile's volume is only as good as the surface under it, and on settling ground the edge of the pile
  is the wrong place to look for that surface; a survey archive that has seen each pile area empty measures it.

## Survivor anatomy

- **Actor:** pass. The deciding property, the pad's level under each pile, has no column in any file: it is a relation
  between the December survey's points and the same ground in another month's survey.
- **Link:** pass. The link is spatial across surveys in two grids and two height systems; no key joins them, and the
  field's toe method reads one survey only, so nothing invites the comparison across months.
- **Reflex:** pass. The field's reflex (a base through each pile's toe, or the lowest or mean level of the ring around
  it) is rung 0 and rung 1 and files 138,000 to 139,000 t, 57 days, under the floor.
- **Back-test:** pass. The reflex validates: on P6 (the 2025 extension) the toe plane agrees with the area's own bare
  surveys within 0.2 per cent, and the year's roll-forward from the December 2025 survey lands within about 2 per cent
  of the toe route's December figure, as it does of the golden's.
- **Second use:** pass. Every survey sits in the pack for the chart of the yard's stock at every survey that the prompt
  asks for; the control report is needed by every route to place the register's corners on the December lattice; the
  register and the densities are read on every route.
- **Shock:** pass. A pile area empty in one month's survey is ordinary yard rotation; the bowls make no anomaly in the
  December survey, whose rings sit on the level pad around each pile (checks.py mechanism block).
- **Pins:** pass. PR-07 files the WHAT in the company's own procedure and no filed sentence names the toe, a base
  surface, settlement, the rotation surveys or any survey but December's (checks.py documents block).

## Readability screen

Each rung against the seven tests (1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear, 7
dedicated organ); the reflex row comes from the field's vocabulary for stockpile volumes (toe base, triangulated toe,
lowest perimeter level, design pad level, base survey).

| Rung | 1 | 2 | 3 | 4 | 5 | 6 | 7 | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 a plane through each pile's toe (138,000 t, 57 days) | PR-07 3.2 read on the December survey alone | the December lattice | yes | P6 and the roll-forward confirm it | no | yes | no | readable |
| R1 the lowest or mean level of the ring round each pile (about 139,000 t on the generator's ring, under the floor) | no | the December lattice | yes | P6 confirms it | no | yes | no | readable |
| R2 a bare base only where contractor B flew it, the toe elsewhere (140,000 t, 58 days) | no | B's lattice matches itself | no | no | no | no | no | readable |
| G (decisive) each area's pad from the survey that recorded it bare, conformed across both contractors (150,000 t, 62 days) | no sentence names a base, the toe, settlement or the rotation surveys | no column holds a pad level or a base | no: the reflex reads the December survey only | no control ties only under it: the roll-forward lands as close under the toe route | no | no: a surface-to-surface volume over a year's conformed surveys | every survey serves the stock chart | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the December survey | the survey flown on 16 December 2026 | another month's survey | not open | PR-07 3.1; the delivery register's only December 2026 row |
| SF2 | the yard pad under a standing pile | the surface the year's surveys recorded bare there | a toe plane, the ring's lowest point, the design level | nominate (the stump, not a reading) | the bare surveys show the pad 1.5 to 2.1 m below the ring under P1 to P5 (asserted) |
| SF3 | the density | the latest test before the survey | the year's average; a later test | same call | PR-07 3.2 "last determined ... before the survey"; the average keeps the call (asserted) |
| SF4 | the density's unit | kg/m3 before July, t/m3 after, per row | kg/m3 read as t/m3 | absurd | each row's unit column |
| SF5 | the planned burn | the quarter total over its 90 days | the mean of the monthly rates | same call, same whole days | PR-07 3.3; asserted |
| SF6 | days of cover | to the whole day | one decimal | same call | the prompt; every golden-family member rounds to 62 (asserted) |
| SF7 | the reserve's population | pile areas P1 to P6 | the bunkers added | same call both ways | PR-07 2 (asserted with the bunkers' 2,453 t) |
| SF8 | the two height systems | N2000 = N60 + 0.384 m | no shift | same call (the reserve overstated) | the control report 4; asserted |
| SF9 | the pad surface's estimator | each area's own bare survey | the lowest of all the year's surveys; nearest-cell sampling | same call and same bins | asserted for every pile figure, the reserve and the margin |
| SF10 | fewer than 60 days | strictly fewer | at most 60 | same call | PR-07 5; 61.65 days |
| SF11 | the receipts' window | the two December flights | flight start or end; calendar 2026 | asks only | no call within 12 hours of a flight (asserted); the prompt names the surveys |
| SF12 | received | the CV-01 weight | the bill of lading; the draft survey | asks only | OH-12 1.1 |
| SF13 | each coal | the contract's fuel code | the shipper's name | asks only | the contract register covers every call (asserted) |
| SF14 | a quarter | a calendar quarter in Finnish time | UTC quarters | asks only | OH-12 2.1 |
| SF15 | sent to the boiler house | the CV-21 weight | the burn plan; the bunkers | asks only | OH-12 1.2 |
| SF16 | a catch-up interval | the tonnage of its outage, placed on the outage's shifts | the interval it lands in | asks only | the shift log's readings reproduce the re-split (asserted) |
| SF17 | the June integrator restart | bridged at the restart | a negative shift | asks only | nothing weighed between the 08:00 reading and the restart (asserted) |
| SF18 | rounding path | each figure rounded once from the unrounded value | sums of rounded figures | same call | the prompt; asserted |

## Ladder

- **Rung 0, the field's reflex (137,884 t, 56.73 days, nominate):** each pile's volume above a plane fitted through the
  ring just outside its toe on the December survey.
- **Rung 1, a flat base at the ring's lowest or mean level (139,217 and 137,883 t, 57.28 and 56.73 days,
  nominate):** the variants of the same idea; the design level (2.40 m N60) files 137,826 t. These rung figures are the
  generator's own construction (the ring 1.6 to 6 m outside the toe it detects) and move with the ring: the judge's
  toe plane landed near 139,000 t, and a low percentile of each area's levels gave it about 156,000 t, a flat base no
  survey measures that happens to sit in the bowls. None of them is a reading of the pad, so they stay out of
  submission.md, which carries only the golden's own figures.
- **Rung 2, half the insight (139,881 t, 57.55 days, nominate):** the bare survey used only where contractor B flew it
  (P4's October rotation), the toe elsewhere, the cross-contractor conformation skipped.
- **Rung 3, decisive (149,846 t, 61.65 days, no nomination):** each area's pad from its own bare survey (P1 18 March,
  P2 15 April, P5 13 May, P3 17 June, P4 14 October; P6 13 May, no bowl), contractor A's grids taken onto B's lattice
  with the plant grid rotation and N2000 = N60 + 0.384 m.
- **Over-correction (162,939 t, 67.04 days, no nomination):** the bare surveys without the height shift: the right call
  on wrong pile figures.
- **Separation:** the call flips between every easy rung and the golden; the golden reproduces the clean truth within
  0.5 per cent; the golden family (the lowest of all surveys 150,244 t, nearest-cell sampling 149,866 t) keeps every
  graded bin.
- **Mess neutrality:** every Layer 1 item mishandled keeps the golden over the floor and the toe route under it
  (checks.py SF3, SF5, SF7, SF8).

## Closure table

| Axis | Reading here | Move |
|---|---|---|
| 1 Population | pile areas P1 to P6; bunkers and coal afloat out | filed: PR-07 2; SF7 |
| 2 Unit of account | cubic metres, wet tonnes as weighed, days | filed: PR-07 3.2 to 3.4; the prompt |
| 3 Attribution window | the December survey's flight; the asks between the two December flights and by calendar quarter | filed: PR-07 3.1; OH-12 2.1; SF11, SF14 |
| 4 As-of dating | the folder assembled on 4 January 2027, every survey delivered | static |
| 5 Version basis | PR-07 revision 4, OH-12 revision 2, plan version 3 | filed, the only versions shipped |
| 6 Denominator | the plan's 218,740 t over 90 days | filed: PR-07 3.3; SF5 |
| 7 Weighting | none, sums | not applicable |
| 8 Window length | the first quarter of 2027 for the burn | filed: PR-07 3.3 |
| 9 Boundary inclusivity | fewer than 60 days nominates | filed: PR-07 5; SF10 |
| 10 Rounding path | each figure rounded once from unrounded values | SF18 |
| 11 Tie-break | none | not applicable |
| 12 Maturity and censoring | every survey and month closed; the plan approved | static |
| 13 Order of operations | volume, then density, then the sum, then the burn | filed: PR-07 3.2 to 3.4 |
| 14 Row order | sums independent of order | C1 |
| 15 Duplicate resolution | each lattice point once; each call once by its port call | static |
| 16 Identity normalisation | each call's coal through its contract | SF13 |
| 17 Netting against gross | wet tonnes as weighed and tested | filed: PR-07 3.2 |
| 18 Dimensional units | kg/m3 to t/m3; N60 to N2000 | SF4, SF8 |
| 19 Code and status semantics | GU-1's start and stop events | static |
| 20 Integerisation | days of cover to the whole day | SF6 |
| 21 Clause scope | the floor binds the December survey only | filed: PR-07 4 |
| 22 Forward window contents | the first quarter of 2027, the plan's burn | the plan; forward by design |

## Literal reader

Executed word for word, PR-07 fixes the population (the coal yard's pile areas, the bunkers out), the survey (the one
flown in December), the quantity (each area's volume of coal above the yard pad times the latest density), the burn
(the plan's quarter total over its days) and the rule (fewer than 60 days nominates). "Above the yard pad" names the
surface each volume stands on and says nothing about how to find it under a pile; the year's surveys record that
surface directly in the months each area was bare, so the literal reading files the golden (150,000 t, 62 days, no
nomination). No filed sentence directs the volume to the December survey alone or to the pile's toe, so no sentence
executes to rung 0.

## Oracles

None arbitrates the decisive step. The book roll-forward (OH-12 1.3) lands within about 2 per cent of the survey under
the toe route and under the golden (adjustments of -2.2 and -2.0 per cent); the plan, the densities and the register
read the same on every rung; the bunker levels and the cargo analyses (declared distractors) touch no figure. The pad's
level under each pile is read only from the surveys themselves.

## Leak review

`leak.py task462 --asof 2027-01-04` on the final cut: REVIEW, no LEAK. One line per REVIEW:
- Sweep 3, PR-07 carries 14 of the call's 16 distinctive words: the procedure's own nouns (the coal yard, the December
  survey, days of cover, the floor, the winter option, Silesia, nominate); it states no reserve, no days and no
  decision for 2026. Harmless.
- Sweep 4, PR-07 carries 4 stump terms (contractor, register, density, record) and the control report 5 (surface,
  height, register, systems, lattice): the vocabulary of the reserve's definition and of geodetic control; neither names
  a base, a toe, settlement or the rotation surveys (checks.py documents block reads them back). Harmless.
- Sweep 9, the burn plan's two dates in February 2027: peak boiler K3's planned burner inspection, a plan's forward
  dates by nature. Harmless.
- Sweep 12, PR-07 names seven words that are also column names (Days, cargo, contractor, date, tonnes, unit): ordinary
  words of the procedure (unit 2, the survey contractor, cargo afloat), none describing a column or a join. Harmless.
- Single-use test: every survey serves the stock chart, the control report places the register on every route, the
  historian, shift log, unloader log, berth log and contract register carry the asks, and the bunker levels and cargo
  analyses are declared distractors; no file's only use is the decisive step.

Stage 4 (2026-11-04): the leak reader quoted nothing for question 1 and found no ranking or helper file and no realism
tell. The determinism judge returned DETERMINISTIC, APPROVE on the first pass (determinism_check_report_arch2.md):
every committed answer reproduced, stump power strong, the decisive step analytical, sole_data_defect no. Rulings, one
line each, with nothing in the pack changed:
- Reader q6 ("stated procedure plus datum handling", no pad level filed anywhere): that unfiled pad under each pile is
  the intended analytical step, and the judge classed it analytical (Gate H). No change.
- The chart's intermediate survey points carry PR-07 3.2's "last determined before the survey" density to every survey;
  the judge found it touches no gated figure. The convention is named for the graders in submission.md's chart line,
  not in the pack.
- The xlsx files' 1980 zip entry dates are what Excel writes; leak.py's container sweep passed. No change.
- The burn plan's February 2027 dates belong to a forward plan (sweep 9 above). No change.
- submission.md section 1 no longer carries any wrong-route figure: the toe-plane and lowest-point tonnages are the
  generator's construction and do not reproduce from the files (Gate A risk), so the rival clause names why the toe
  base loses and states no figure; the ladder above keeps them.

## Ask sheet

Planning weights 38 / 7 / 55. Each pile's volume and tonnes, the reserve, the days of cover and the call are the call's
own construction and are scored with it. The asks are the yard's book flows behind the December survey, which OH-12
1.3 rolls forward to compare with it: A, the coal received into the yard between the two December surveys by coal (3
figures); B, the coal sent to the boiler house in each quarter of 2026 (4 figures).

- **Ask A, receipts by coal:** H18 home: the book roll-forward against which the survey is compared before the winter
  fuel statement is signed (OH-12 1.3). Path: the berth log (6 columns), the contract register (2), GU-1's event log
  (3), the historian (3), the delivery register (3). Primary: CV-01 also weighs coal moved between pile areas through
  the crossover, and some of those moves ran inside a ship's berth window while the unloader was stopped for wind; only
  the unloader's running intervals are receipts. Second device: three historian communication losses fell while a ship
  discharged and returned after its last grab, so the outage's tonnage lands in one impossible interval outside the
  window. Every berth-window interval (COL 137,418, POL 290,687, USA 180,093 t) and the running intervals without the
  catch-ups (131,933, 283,580, 173,785 t) miss every coal (golden 143,979, 285,944, 175,934 t). Hazards: the berth log in
  UTC, the trading house's calls, the bill of lading and draft survey beside the weight. Pin test: OH-12 1.1 pins the
  weight and "from vessels"; no pin names the crossover, the stops or the catch-ups.
- **Ask B, deliveries by quarter:** H18 home: the other side of the same roll-forward (OH-12 1.3). Path: the
  historian (3 columns), the shift log (5), GU-1's event log (3), the accounting instruction. Primary: CV-21 weighs the
  coal reclaimed for the crossover moves too, identified only because CV-01 carries coal at the same time with the
  unloader stopped. Second device: two communication losses straddle the quarter ends of 31 March and 30 September, so a
  historian route places their catch-ups in the next quarter; the shift log's 00:00 readings fix it. The shift log's
  quarters (227,248, 125,899, 49,049, 231,732 t) and the historian by its own intervals (225,156, 127,992, 47,514,
  233,271 t) miss every quarter (golden 218,358, 111,853, 43,312, 217,186 t). Hazards: UTC stamps against Finnish
  quarters; the June integrator restart. Pin test: OH-12 1.2 and 2.1 pin the weight and the clock; no pin names the
  crossover or the outages.
- **Main population zero-counts:** no ask organ sits in a file the main call reads; no crossover move or outage falls
  within 12 hours of a survey flight (checks.py separation).
- **The full includer:** a response that reconstructs the unloader's running state and the crossover blocks, and
  returns each catch-up to its outage, keeps both asks; both devices share one real cause (the crossover moves) and the
  outages feed both asks, a known limit of this layer recorded here.
- **Referee:** none; every ask figure is recomputed on `generator/verify.py`'s own path.

| Ask figure | Cracker (berth windows; the shift log's quarters) | Golden | Cracker |
|---|---|---|---|
| A: KH-COL received (t) | 137,418 | 144,000 | miss |
| A: KH-POL received (t) | 290,687 | 286,000 | miss |
| A: KH-USA received (t) | 180,093 | 176,000 | miss |
| B: Q1 delivered (t) | 227,248 | 218,000 | miss |
| B: Q2 delivered (t) | 125,899 | 112,000 | miss |
| B: Q3 delivered (t) | 49,049 | 43,000 | miss |
| B: Q4 delivered (t) | 231,732 | 217,000 | miss |

Pair ceiling: 28.5 (the cracker 45.0 on the call keeping no ask figure, the mirror 12.0 off it at 138,000 t, keeping no
ask figure, r 5.0).
Mirror leakage: 0.0 per cent of ask weight (the mirror, stopping at rung 0, takes the same route on the asks).
Measured by: generator/ceiling.py, on the cut pack.

## Tried and rejected

- 2026-10-15, draw: the seed's own world, plant CO2 per MWh across CAMD, GHGRP and EIA through the EPA-EIA crosswalk.
  Rejected: task459 shipped those files, and in that world the decisive candidates were the crosswalk key, scope and
  net-against-gross readings (data semantics) or the operating level (task459's step); the many-to-many keys stay as
  Layer 1 here.
- 2026-10-15, build: each producer's tonnes with the detection curve's form left open. Rejected: the call held under
  every form, but a complementary log-log, a wind-normalised or a binned curve moved the tonnes 5 to 25 per cent from the
  logistic, so a judge choosing its own form would not reproduce the graded figures; Talmora's note now gives the
  curve's form and the standard how campaigns combine into the year, the weighting itself left unstated.
- 2026-10-15, build: the production extract from July 2025. Rejected: summing the whole extract moves the call, a Layer
  1 item carrying weight; the extract holds the rating year.
- 2026-10-15, build: a permit shared by a pad and a battery on different flight lines. Rejected: the coverage file gave
  the pad passes it never had; a permit is shared only where both sit under the same lines.
- 2026-10-15, build: gas to one decimal of a million cubic feet. Rejected: sums of whole Mcf sat within 2 Mcf of a
  rounding edge; whole million cubic feet, with the plant's and the commission's streams drawn so every ask figure sits
  0.04 MMcf or more from its edge.
- 2026-10-15, build: every producer's site count a multiple of five and its year of gas a round level. Rejected as
  realism tells; the register leaves out a few imaged sites that carry no source and sit 400 m or more from every
  plume, and each producer's gas takes a non-round level.
- 2026-11-02, re-check under the new gates: architecture 1 spent, not re-rooted. The easy routes on the clean truth
  file wrong slates (blanks as zeros eight, carried sources none, detected share ten), but the golden is the field's
  own POD-corrected aerial inventory (each plume over its detection probability from controlled releases) applied as
  the textbook states it, with nothing in the data violating its precondition, every curve form and the coarse
  correction landing the same four, the release study read by the decisive step alone, and the four the bottom four of
  the default sort (Reflex, Link, Back-test, Second use and Shock fail on the honest anatomy).
- 2026-11-04, re-root: architecture 1 left as spent (above), its build files cleared from the folder (kept in history);
  architecture 2 drawn in a house world (supply chain inventory) mapped to GSDS data integration, on a new world,
  dataset and prompt shell. The screens of this draw follow, each with the default path ending wrong, the swap test,
  the anatomy lines or the bin test priced on paper or in a prototype; the last was carded.
- 2026-11-04, screen 1, seasonal-adjustment-official-time-series-production, inventories in the national accounts
  revalued from book values to current prices (the inventory valuation adjustment) with FIFO stock turning over: a
  prototype (proto_fifo.py) put the standard turnover-window adjustment within 1 to 3 per cent of a full FIFO replay,
  so the decisive step was worth under one bin; the end-price and quarter-average deflations missed by about 15 per
  cent, but they are not what the field does.
- 2026-11-04, screen 2, stockpile volume above a plane through the toe on a crowned pad (the pad's drainage crown under
  the pile): a prototype (proto_pad.py) put the toe plane about 1 per cent from the truth, a lever no call can stand on.
- 2026-11-04, screen 3, payment claims, backdated pay-award arrears paid in one month for several earlier months: the
  arrears month carries several periods' amounts in one field, so the answer turns on reading that field correctly
  (data semantics), like the client's own rainfall example.
- 2026-11-04, screen 4, census-register, automatic bicycle counters that also count e-scooters after a firmware change:
  the loop counter's capture is traffic engineering on a register backdrop (task229 rejected the same cycle-counter
  draw as a domain backdrop).
- 2026-11-04, screen 5, payment claims, a hospital's cost-to-charge ratio after a chargemaster increase: the swap test
  fails (the ratio is a ledger quotient in any field), as task476's S3.31 found.
- 2026-11-04, screen 6, item-response-theory-test-equating, a spiralled old form with drifting anchor items: random
  groups equating is the field's reflex for spiralled forms and lands the golden, so the decisive step is the method.
- 2026-11-04, screen 7, item-response-theory-test-equating, anchor items affected by a scrolling display change: which
  anchors to drop is a fork resolved by a filed list or not at all, and the method is heavy for its worth.
- 2026-11-04, screen 8, item-response-theory-test-equating, remote-proctored candidates allowed scratch paper on one
  form: the condition is a column read (a proctoring code), data semantics.
- 2026-11-04, screen 9, emissions-inventory, a plastic packaging levy whose recycled-content share lags through a
  dryer's FIFO buffer: the swap test fails (a generic buffer delay), and the annual totals are invariant to the delay.
- 2026-11-04, screen 10, emissions-inventory, a ship's sulphur during an emission-control-area fuel changeover mixing in
  the service tank: the object is an exceedance in a window (anomaly detection), not a conformed inventory.
- 2026-11-04, screen 11, seasonal-adjustment, shrinkflation in scanner data for a price index: the product identity
  across a pack-size change is identity resolution and grain, both barred as the decisive step.
- 2026-11-04, screen 12, seasonal-adjustment, direct against indirect adjustment of an aggregate: a method fork the
  shipped files cannot close without naming X-13's options (an external dependency).
- 2026-11-04, screen 13, census-register, a deposit return scheme's return rate with cross-border returns: the
  population of eligible containers is the WHAT, so filing it is rule application and leaving it open is a fork.
- 2026-11-04, screen 14, stockpile reserve with the survey contractor's own volume report computed on the toe base:
  the report ranks the decision quantity wrongly (Gate G) and the step becomes rejecting a document.
- 2026-11-04, screen 15, stockpile reserve with the pad's as-built surface model shipped: surface-to-surface against a
  base survey is the field's reflex when a base survey exists, so the golden would be the method, not its violated
  precondition.
- 2026-11-04, screen 16, census-register, age heaping in birth dates from a register migration: a Layer 1 grouping
  item, and the smoothing is an estimator choice (the grouping dichotomy).
- 2026-11-04, prototype of the carded draw (proto_dish.py, proto_yard.py to proto_yard4.py): bowls 0.5 to 1.1 m under
  5.5 to 7 m piles put the toe plane at 0.93 of the truth; at yard scale with the crest at the stacker's fixed height
  and the slopes running down into the bowl, a bed only partly stacked at the December survey left its bowl's open
  end in view, where the lowest ring point fell into the hollow and landed within 1 per cent of the truth; with every
  bed stacked to its full length in December (the yard full before the ice season, crest heights varying) the base
  through the toe lands at 0.923, the ring's lowest and mean points at 0.931 and 0.923, every bed's own bare survey at
  1.001 and the lowest of all aligned surveys at 1.002, and using the bare surveys only where the December contractor
  flew them lands at 0.956. The December piles are full length in the build for that reason.
- 2026-11-04, prototype: one survey window per bed reaching into its neighbour's footprint double-counted the
  neighbour's pile against the lowest surface of every survey; each cell belongs to one bed, the beds 20 m apart.
- 2026-11-04, redraw: the carded steelworks draw (an integrated works' ore yard of six beds, pellets and lump ore,
  supply-chain-logistics inventory planning, registered 08:31) collided after the rebase with task476 v4 and task488 v2,
  drawn in parallel and registered first: the pairing (supply chain with ETL), the decisive pattern G5, the context
  artifact (a monitoring export), the forum (a committee), the forcing event (the season) and the organisation family
  (a manufacturer, which a steelworks honestly is) all BLOCKed. The mechanism, the survey archive and the asks moved to a
  city-owned power plant's coal yard (business and operations analytics mapped to GSDS data integration, a utility, the
  management team, the supply agreement's option deadline, the burn plan as the capacity report, method selection as
  the decisive pattern), priced again before carding (proto_coal.py: the base through the toe 0.927, the ring's lowest
  point 0.935, every pile's own bare survey 1.001, the lowest of all aligned surveys 1.003).
- 2026-11-04, design: the pile tonnes and the reserve to the nearest 1,000 with volumes to the nearest 100 m3 and days
  of cover to one decimal. Rejected: the golden family (each area's own bare survey, the lowest of all the year's
  surveys, nearest-cell sampling) spreads about 0.2 days and 400 t on the reserve, so one decimal of days and 100 m3
  forked; volumes and tonnes now go to the nearest 1,000 and days to the whole day, and each pile area's December fill
  was set so every figure, the reserve and its margin over the floor keep one bin across the family (checks.py SF9).
- 2026-11-04, design: the toe ring's lowest point landing within 2.6 per cent of the floor. Rejected as too thin a
  margin for a rung a strong analyst may take; the bowls were given a steeper edge and deeper centres (1.5 to 2.1 m)
  so every easy rung sits 4 per cent or more under the floor and the golden 2.7 per cent over it.
- 2026-11-04, build: one call of 2,051 t in the September interval (the surveys' stock fell almost as fast as the
  burn). Rejected as no cargo a power plant charters; the August and September fills were rebalanced so the interval
  takes one Baltic cargo of about 14,600 t.
- 2026-11-04, build: three historian outages at fixed clock times. Rejected: a change to one call's size moved every
  later call's grabs, and the outage meant to fall in a ship's last hours missed it; the three outages that fall during
  a discharge are now placed from that call's own last grab.
- 2026-11-04, build: two calls of equal tonnage in one interval and a quarter's deliveries landing within a tonne of a
  round figure. Rejected as realism tells; the calls' shares were split unevenly and December's burn nudged.
- 2026-11-04, build: suppliers named Altamar Coal and Ridgeline Energy Sales and ships named Kvarken Trader, Saga
  Sandpiper and Auk Venture. Rejected under H21 (two real company names, a real strait, near-matches to Riga and SUEK);
  renamed Carbones Montoya Vélez, Tygart Run Energy Sales, Bothnian Trader, Sanderling and Guillemot Venture.

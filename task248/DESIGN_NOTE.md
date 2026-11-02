# task248 design note: Highbank Marinas, the tank charts to redo before the 2027 wetstock service

Private, never ships. Architecture 2, drawn 2026-11-02 at the Batch 3 queue reset. Architecture 1 (a regional public
health service's wastewater surveillance, epidemiology-public-health) shipped on 2026-10-18 with no portal result; its
world is closed (one architecture per world) and its note is kept below as `## Architecture 1 record`. The lessons this
draw applies, from the batch's judges: the filed WHAT names the quantity (the gallons a chart misstates between three
register heights, against the gallons that actually went in or out) and never the procedure; the default is an easier
method on correct data that the WHAT visibly leaves short (a delivery check cannot see a half-range), never a shipped
artifact the truth contradicts; no record is missing or planted, and with every reported figure complete and correct
the easy routes still file the wrong list (the FINE-numbers test); every licensed estimator is measured and asserted
on the same side of the filed threshold for every tank.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task248.json`, architecture v2, registered 2026-11-02T02:12:12Z; architecture 1's identity moved into `lineage` with fate "re-rooted 2026-11-02 at the Batch 3 queue reset" and its prompt shell into `lineage_shells` |
| Guard | WARN, no BLOCK. repeat.gate_g and repeat.decision against task238 v2 (registered minutes earlier): the gate is method_or_model_selection because the decisive step is which observation design the filed quantity entitles, and the call is a list because the service onboards tanks one by one; task238's driver (price scans against shelf labels) shares neither. test.same_puzzle_older NOTE against task445 v2's lineage, differentiated on the card (a coverage completion there; here no record is added or missing). Nearest drivers 0.08 (task252 v1 lineage), 0.06 (task464), 0.05 (task461, task135, task459) |
| Domain / task type | physical-environmental-sciences / sensor-calibration-measurement (serves DQ): an automatic tank gauge is a sensor whose chart is its calibration, and the release detection it feeds protects the reservoirs and the groundwater. Moved off epidemiology-public-health, whose data-quality cell holds five surveillance-feed worlds |
| Objective | Data Quality Monitoring & Alerting. The object is the health of each tank's gauge data (the chart that turns a probe height into gallons); the call is a monitoring decision taken before a cutover: which tanks are re-charted over the winter so the wetstock monitoring service does not alarm on chart error from its first day. Retag test: not Anomaly Detection (no event is separated from an artifact, every tank carries some chart error and the call grades its size against a filed limit), not Forecasting (no future value is predicted; the misstatement is a standing property of each tank read from the closed season) |
| World | Highbank Marinas, a marina management group running eight marinas with fuel docks on two fictional Corps of Engineers reservoirs in south-central Kentucky (Central time). Twenty underground tanks (ethanol-free REC-90 gasoline, E10 gasoline and diesel; 6,000 to 12,000 gallons, horizontal cylinders), each with a magnetostrictive probe on its marina's tank gauge console; dock sales on the marinas' point-of-sale system (replaced in mid-November); deliveries by one fuel distributor on bills of lading in gross and net gallons |
| The call | How many tanks, and which, go on the winter re-charting list, under Fuel Systems Standard FS-3 section 3.4: a chart is redone when it misstates the change in stock between any two of the tank's reorder, half-full and maximum fill heights (the register) by more than 25 gallons, read from the 2026 boating season (1 April to 31 October) |
| As-of | Tuesday 12 January 2027; the calibration contractor's winter programme is booked by 29 January; the service starts on 1 April 2027 |
| Shape | other: the list (each tank named), its count, each listed tank's largest misstatement and the heights it lies between, a chart of each listed tank's two half-range misstatements, and three asks (feed readiness per tank, the leak-test record per marina, dock gallons by marina and product); well over 25 criteria. Decision designation_set, answer set_of_items, question form how-many (which is over its corpus quota) |
| Strategy | other: a conversion error that varies with level, identified by combining two observation designs that each see a different part of it. Gap time (sub-cycle intervals against complete fill-and-draw cycles) then objective; pattern none; G3 decisive (the gauge's record against the gallons the operation actually moved), G16, G2; Gate G method_or_model_selection; calibration counterparty_acknowledgement (the distributor's net gallons on each bill of lading); context artifact filed_standard (FS-3); Layer 2 family estimation_fit, pattern `own:gauge-chart-error-shape-from-sub-cycle-intervals-scale-from-deliveries` |
| Forum, event, organisation | line_manager_or_team (the director of marina operations signs the winter works list), cutover_or_migration (the marinas move onto the wetstock monitoring service on 1 April 2027), hospitality_or_tourism. Role programme_officer (the group's fuel systems and underground tank compliance manager asks) |
| People | `guard.py names --geo "United States" --locale en_US --seed 248`: Theresa Shelton (the compliance manager, who asks), Harold Mathis (director of marina operations), Miranda Collins (the monitoring service's onboarding analyst), Lucas Walter (the distributor's dispatcher). None appears in the prompt |

- **Candidates written before choosing** (each dropped one has its line in `## Tried and rejected`): (1) this draw; (2)
  a quarry's blast vibration monitors and the trigger each runs, from a censored attenuation law; (3) a hospital
  laboratory's delta-check limits judged on wrong-blood-in-tube swaps between co-collected patients; (4) an in-line
  near-infrared model's error against the laboratory assay, matched by the material's travel time; (5) each clinic's
  score reliability from a scale's conditional standard error; (6) an assay laboratory's batch release on certified
  reference materials; (7) a metered network's meter error variances read from the covariance of the balances they
  share; (8) the same tank-chart mechanism at a fuel retailer's stores and at a transportation department's yards.
- **Data-native sentence.** A probe height becomes gallons through the chart, and in a horizontal cylinder a probe set
  an inch off (or a tank settled a few tenths of a degree) misstates gallons in proportion to the width of the
  product surface, most through the middle of the tank and little near its reorder and full heights, while a chart
  drawn for the wrong tank misstates every gallon alike; a delivery runs from about the reorder height to about full,
  so it sees the second and almost none of the first, every fill-and-draw cycle cancels both in the monthly
  reconciliation, and the dock sales between two readings see both but cannot tell a proportional chart error from
  the dock meters' own small errors, which only the deliveries (no dock meter involved) separate.
- **Abstraction sentence** (what a reviewer holding this build and its nearest approved build would call the same):
  none can be written. Against task120 (a day's use is the wells' production less the storage the tanks gained) the
  shared nouns are tanks and a storage identity, but there the identity computes a quantity directly; here the
  quantity is a conversion's error and the step is which of two observation designs identifies which part of it.
  Against task182 (each bore's own lagged driver response) and task133 v4 (density from paired tickets) nothing
  matches: no driver, no pairing of two records of one event.
- **Same-puzzle and library tests.** Gap time, decisive G3, designation_set repeat only task445 v2's lineage
  (differentiated). Library test: the stump sentence does not read "use X on Y"; the field's methods (the monthly
  reconciliation, the delivery check) sit at rungs 0 and 1 and file wrong lists.
- **Sources.** The client's two-layer standard (estimation_fit); US EPA underground storage tank rules (monthly
  inventory control at 1 per cent of throughput plus 130 gallons, 0.2 gallon-per-hour leak tests); horizontal
  cylinder geometry; magnetostrictive probe practice; bills of lading in net gallons at 60 F. The group, its
  marinas, reservoirs, distributor, systems and people are fictional.

## Survivor anatomy

- **Actor:** each tank's chart error between two heights has no column anywhere: the gauge prints gallons through the
  chart it was given, the dock sales and the bills of lading print gallons that moved, and the error is a relation
  between a reading's height, the next reading's height and the gallons metered or delivered in between.
- **Link:** the gauge change between two readings is set against the dock gallons its hoses metered in that interval
  (dock sales windowed by the readings' times through the piping record's hose-to-tank map) and, separately, each
  gauged delivery against its bill of lading's net gallons; no key joins a reading to a sale, and no sentence asks for
  either comparison, let alone both at once.
- **Reflex:** the field's methods for a chart's health sit at rungs 0 and 1: the monthly inventory reconciliation
  passes every tank (none), and the delivery check against the bills of lading, the trade's chart check, files 2 tanks
  (the two charts drawn for the wrong tank) and passes every probe-offset chart.
- **Back-test:** the textbook route validates: every tank's 2026 monthly reconciliation sits inside its tolerance on
  the marinas' own close-out sheets, the delivery check's discrepancies are small and steady on the offset tanks, and
  the dock meters' registered gallons tie to the point-of-sale totals.
- **Second use:** every file the decisive step reads is in the pack for its own reason: the gauge export for the
  feed-readiness ask and the monthly reconciliation, the dock sales for the gallons ask and the stock book, the bills
  of lading for the stock book, the register for the heights FS-3 names, the piping record for any reconciliation,
  the charts because the gauge cannot be read without them.
- **Shock:** the offset tanks look ordinary on every monthly statistic and on every delivery; no tank is the pack's
  largest anomaly, and the list is not an interval of any one-dimensional sort (capacity, throughput, delivery
  discrepancy or monthly over/short).
- **Pins:** the WHAT is filed once in FS-3 section 3.4 (the three register heights, the 25-gallon limit, the 2026
  season, misstatement against the gallons that actually went in or out); no filed sentence names the sales
  intervals, the deliveries as an anchor, the dock meters' error or the shape of an offset error, and deleting 3.4
  unforces the call because it holds the estimand, not the step.

## Default path

1. Read FS-3 section 3.4 and the tank register (twenty tanks, each with its chart number, reorder height, half-full
   height and maximum fill height).
2. Take each tank's monthly reconciliation for the 2026 season (the marinas' close-out sheets, or rebuilt from the
   gauge export, the dock sales and the bills of lading): every tank sits inside 1 per cent of throughput plus 130
   gallons, so no chart shows a problem on the monthly test.
3. Check each chart the way the trade does, against its deliveries: pair each gauged delivery in the season with its
   bill of lading, take the gauge's net rise less the bill's net gallons, and express each tank's mean discrepancy
   per gallon delivered over its working range from reorder to maximum fill.
4. List the tanks whose delivery-based misstatement passes 25 gallons.
Ends on: 2 tanks (CF-2 and GC-1, the two charts drawn for the wrong tank length).
Golden: 6 tanks (BP-2, CF-2, DH-1, FL-1, GC-1, HS-2).

## Stump sentence

The default path files 2 tanks (CF-2 and GC-1) because it checks each chart against its deliveries, and a delivery
runs from about the reorder height to about full, where a probe offset or a settled tank misstates almost nothing at
either end, so the four offset charts (BP-2, DH-1, FL-1, HS-2), each misstating 40 to 60 gallons across a half of its
range, pass; reading the half-ranges from the dock sales between readings alone files 9 tanks, because inside those
intervals a dock meter's small error is indistinguishable from a chart drawn for the wrong tank, so three tanks with
fast or slow meters and one with a small offset come in and GC-1, whose chart error its meter offsets, drops out;
only the intervals' half-range shape with the proportional part anchored by the deliveries files the 6.

## Three rules

- **Task type:** physical-environmental-sciences sensor-calibration-measurement, which serves data-quality-monitoring:
  the gauge's chart is the sensor's calibration and the call decides which calibrations are redone.
- **Domain test:** the quantity that decides is each tank's chart error between its register heights, which tank
  gauging reads by reconciling the gauge's change in gallons against metered flows; in a horizontal cylinder a probe
  offset misstates gallons in proportion to the product surface's width and a wrong-tank chart misstates every gallon
  alike, so with another field's nouns there is no cylinder, chart or metered delivery and the task stops making sense.
- **Swap:** "how many of our wards need their bed charts redone before the new monitoring service, judged on the
  misstatement between three heights" reads as nonsense: no cylinder geometry, no gallons moved between two gauge
  readings, no delivered quantity on an independent document.
- **Layer 1:** the gauge export in UTC beside dock sales in Central local time across both clock changes; the dock
  point-of-sale replaced in mid-November with a cut-over week in both exports; one marina's hoses re-piped to another
  tank at a dated refit in May; bills of lading in gross and net gallons at 60 F against the gauge's gross and
  temperature-compensated volumes; delivery reports the console opens and closes itself while dock sales run; charts
  as quarter-inch tables under register chart numbers; winter weeks with docks closed. Each is produced by the
  systems named, and none decides the call (`generator/checks.py` R3c).
- **Layer 2:** estimation_fit: the decisive choice is the observation design that identifies each part of the chart
  error, the shape from sub-cycle intervals and the proportional part from deliveries, against the cycle-level
  reconciliation and the delivery check that each see only one part or none.
- **Decisive step:** read each tank's misstatement at the half-full height from the gauge change against the gallons
  sold between readings, and carry the proportional part from the gauged deliveries against their bills of lading,
  because between readings a proportional chart error and a dock meter's error look the same and only a delivery,
  with no dock meter in it, tells them apart.
- **Not semantics:** every field, unit, chart number and height read correctly, the monthly reconciliation still
  passes every tank and the delivery check still files 2 tanks; nothing flips on reading a code or a definition, and
  the gross against net gallons conventions move no tank across 25 gallons (asserted).
- **Not rule application:** no filed rule or procedure says to read the intervals, to anchor them on the deliveries or
  that a dock meter's error aliases a chart's; executing FS-3 and every other filed sentence leaves the estimator
  open, and the enumerated family (monthly reconciliation, delivery check, intervals alone, intervals with a free
  meter term, intervals anchored by deliveries, a two-component geometric fit) spreads from 0 to 9 tanks while the
  standing family (the anchored constructions the data leave defensible) files the same 6 tanks, each at least 12
  gallons from the limit (measured in `generator/checks.py`, the loudness being the deliveries' disagreement with the
  intervals' full range on four tanks).
- **Analyst test:** a strong analyst who reads the register, the gauge export, the dock sales and the bills of lading
  correctly checks each chart against its deliveries, the trade's chart check, and files 2 tanks (CF-2 and GC-1),
  passing every offset chart because its deliveries span both ends of the range where the offset misstates little.
- **Estimand:** FS-3 section 3.4 (`target/FS-3_fuel_systems_standard.pdf`): every tank on the register; the gallons
  its chart's change between any two of its reorder, half-full and maximum fill heights differs from the gallons that
  actually went into or out of the tank between them; read from the 2026 season, 1 April to 31 October; a tank is
  re-charted when any of the three exceeds 25 gallons.
- **No decoy:** nothing is planted: no copied block, hidden rule, memo, draft, briefing or stakeholder figure carries
  a wrong list; the close-out sheets are the marinas' own correct monthly tests, and no file ranks the tanks on chart
  error.
- **No certified replay:** no published or certified figure is reproduced to recover the method; the golden is built
  forward from readings, sales and bills of lading, and no shipped artifact carries a chart-error figure.
- **Lesson:** a calibration error that varies with level can be invisible to every whole-cycle and whole-transfer
  check, and an error proportional to throughput is confounded with the flow meters' own error until an observation
  with no flow meter in it separates them; no build on file teaches identifying two parts of one error from two
  observation designs.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 monthly reconciliation (none) | the close-out sheets and the 1 per cent rule state it | close-out columns | yes, the field's routine test | none | none | one sum per month | no | readable |
| R1 delivery check (2 tanks) | FS-3 section 5 names the bill of lading as the delivered quantity | delivery report rows | yes, the trade's chart check | none | none | one ratio per tank | no | readable |
| R2 half-ranges from the dock sales alone (9 tanks) | FS-3 3.4 names the half-full height, which only intervals cross | none | partly: a strong analyst reaches it from 3.4 | none | none | no | no | readable |
| R3 (decisive) proportional part anchored by the deliveries (6 tanks) | no sentence names the dock meters' error, the aliasing or the anchor | no column holds a meter error or a chart error | no: the field checks meters and charts separately | none | the battery finds nothing (every row is correct) | no: a joint construction over two observation sets | no: every file it reads has its own use | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "misstates the change in stock between two heights" | chart change between the heights less the gallons that actually moved | chart volume at one height against a strapping of the tank | no strapping ships; same 6 | FS-3 3.4 defines it on the gallons that went in or out |
| SF2 | the three heights | the register's reorder, half-full and maximum fill heights | heights read off the chart table's percentage rows | same 6 | FS-3 3.4 names the register |
| SF3 | the window | 1 April to 31 October 2026, local | the calendar year | same 6 (asserted) | FS-3 3.4 names the season |
| SF4 | gross against net gallons | sales intervals gross to gross, deliveries net to net | everything gross, or everything net | same 6, every listed figure in its 10-gallon bin (asserted) | same call |
| SF5 | the day and time base | readings and sales on one clock (UTC to Central) | sales windowed on the raw UTC stamp | same 6 (asserted) | same call |
| SF6 | a delivery with dock sales running | the gauge's rise plus the gallons sold during it | the rise alone | same 6 (asserted) | same call; FS-3 5 counts sales during a delivery |
| SF7 | the re-piped hoses | each hose to the tank the piping record gives on the sale's date | the current map for the whole season | same 6 (asserted) | the piping record dates the refit |
| SF8 | "largest misstatement" | the largest of the three in absolute gallons | the signed largest | same 6, same figures | FS-3 3.4 states the limit on the size |
| SF9 | rounding | each listed misstatement to the nearest 10 gallons | truncation | every listed figure clear of its bin edges (asserted) | the prompt's rounding sentence |
| SF10 | the construction of the half-range figure | any estimator taking the anchored step (cycle sub-totals, interval fit with knots at 6 or 12 inches, two-component geometric fit) | intervals without the anchor | anchored: same 6 under each; unanchored is R2 | same call within the anchored family (asserted) |

## Ladder

| Rung | Construction | Set | Dies to |
|---|---|---|---|
| R0 | monthly over/short against 1 per cent of throughput plus 130 gallons | none | FS-3 3.4 asks for the misstatement between heights, which a whole month nets away |
| R1 | delivery check: gauged rise against bill of lading, carried over the working range | 2: CF-2, GC-1 | the half-full height is never a delivery's start or end, and an offset error is small at both ends |
| R2 | half-ranges from the dock sales between readings, no anchor | 9: AH-1, BP-2, CF-2, DH-1, DH-2, EB-2, FL-1, HS-1, HS-2 | the intervals' full range disagrees with the deliveries' on AH-1, EB-2, HS-1 and GC-1: the dock meters' error sits in it |
| R2' | delivery full range with unanchored sales half-ranges | 7: BP-2, CF-2, DH-1, DH-2, FL-1, GC-1, HS-2 | the half-ranges still carry DH-2's meter error |
| R3 | half-ranges and full range from the intervals with the proportional part anchored by the deliveries | 6: BP-2, CF-2, DH-1, FL-1, GC-1, HS-2 | golden |

Design targets (the build replaces each with its measured value): every listed tank's largest misstatement 40 to 65
gallons and every unlisted tank's 13 or under under every anchored construction; each wrong rung's false entries at
27 gallons or more under that rung and each of its misses under 22. Pricing sequence: (1) the residue the WHAT leaves
is the observation design, a method; (2) the move is worth the four offset tanks' 40 to 60 gallons against a delivery
signal under 15; (3) the one-group-by route (mean delivery discrepancy per tank) is R1 and files 2; (4) the standard
error of a half-range figure is about 2 gallons over a season's eight to twelve draw-downs; (5) the lever is a bias,
not a variance; (6) no history series; (7) no subset prints the error exactly (every interval carries meter error,
every delivery the bill's noise); (8) the reflex sweep (monthly, delivery, intervals with and without a meter term,
geometric fit) runs as code in `generator/analysis.py`.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | every tank on the register | filed in FS-3 3.4; the register lists twenty |
| 2 | Unit of account | the tank | the question names tanks |
| 3 | Attribution window | the 2026 season | FS-3 3.4; C1, no listed tank moves on the calendar year (asserted) |
| 4 | As-of dating | the season's records as exported on 12 January 2027 | static export |
| 5 | Version basis | the register's current chart numbers | C1, no chart number changed in 2026 |
| 6 | Denominator | none (a gallon difference, not a rate) | not applicable, asserted inert |
| 7 | Weighting | none | not applicable |
| 8 | Window length | one season | filed |
| 9 | Boundary inclusivity | "more than 25 gallons" | C1, nothing within 12 gallons of 25 |
| 10 | Rounding path | the figure rounded once, after the estimate | filed in the prompt; C1 across estimators |
| 11 | Tie-break | not needed | C1 |
| 12 | Maturity and censoring | none | every interval closed |
| 13 | Order of operations | anchor then read the halves, or jointly | C1 (asserted, same figures) |
| 14 | Row order | none | sums and fits invariant to order |
| 15 | Duplicate resolution | the point-of-sale cut-over week (outside the season) | ask-only; season rows carry none |
| 16 | Identity normalisation | console tank numbers against register tank IDs | the console's tank setup export names each tank's product and chart |
| 17 | Netting against gross | sales during a delivery | SF6; C1 |
| 18 | Dimensional units | gallons, inches, gross and net | SF4; units in each export's legend |
| 19 | Code and status semantics | delivery and inventory record types | the export's legend; never the stump |
| 20 | Integerisation | the 10-gallon rounding | SF9 |
| 21 | Clause scope | 3.4 applies to every tank going onto the service | filed |
| 22 | Forward window contents | the winter programme and the 1 April start | the onboarding letter dates the start; nothing forward is estimated |

## Literal reader

Executing the prompt, FS-3 and every legend word for word: the population (every register tank), the quantity (the
chart's change between each pair of the three register heights against the gallons that actually went in or out),
the window (the season) and the limit (more than 25 gallons) are fixed, so the literal reader must estimate gallons
that actually moved: the bills of lading give them for deliveries, the dock meters (within their tolerance, not
exactly) for sales; a reader who takes the meters as exact files R2's 9 and is ruled out by the deliveries' gallons
on the same tanks, a reader who uses only deliveries cannot place the half-full height (non-compliant with 3.4), and
every reading that takes both files the 6 (asserted in `generator/checks.py`).

## Oracles

- The marinas' monthly close-out sheets: confirm every tank's monthly test passes; tie under every reading and name no
  chart (a back-test of the routine check, not an oracle).
- The bills of lading: give delivered net gallons, the anchor; they tie only to deliveries and carry no chart figure.
- The point-of-sale totals: tie to the dock meters' registered gallons under every reading (they cannot see a meter's
  error).
- none ties only under the golden.

## Ask sheet

The main call's declared row population: the 2026 season's (1 April to 31 October, local) gauge inventory and
delivery records, dock sales and bills of lading, the register's heights and chart numbers, the charts and the
piping record. Every ask device sits outside it (off-season rows or an ask-only file); `generator/checks.py` asserts
the zero-counts from the shipped rows.

**A1, feed readiness (H18: the onboarding letter's readiness requirement, a qualifier of the cutover).** For each
tank, the days of 2026 (local calendar days, as the onboarding letter defines a day) on which its gauge sent no
inventory reading. 20 figures, whole days. Files: `atg_inventory_2026.csv`, `atg_tank_setup.csv`, the register, the
onboarding letter. Primary device (D8 with a sequence reconstruction): the January ice storm's power cuts reset the
clocks of the older consoles at five marinas to their factory date; each console kept logging, its readings carrying
the console's running sequence number, until the technician's visit re-set the clock two to nine days later; those
readings are stamped 2016 and are re-dated by the sequence chain, so the days are not missing. Second device (D7):
Dellwood Harbor's console was replaced on 17 February and the new console numbers its two tanks the other way round;
the tank setup export gives each console's tanks by product and chart number, and the old probe's January fault days
belong to the register tank the old numbering names. Hazard: UTC stamps against local days at outage edges. Stops:
drop the 2016 rows (each reset marina's tanks two to nine days high); key tanks by console number all year (Dellwood's
two tanks swapped in January); count UTC days (several tanks one day off); the answer.

**A2, the release-detection record (H18: the 2026 monthly test record the service takes over, an audit trail of the
cutover).** For each marina, the tank-months of 2026 without a passing 0.2 gallon-per-hour test. 8 figures, whole
tank-months. Files: `atg_leak_tests_2026.csv`, `atg_tank_setup.csv`, the register, FS-3 section 6. Primary device
(D1, identity by the console's test number): after each modem outage the remote monitor re-polls the console and logs
the console's last test result again, with the poll's time and its own row number but the console's test number and
leak rate unchanged; a reprint printed in the next month makes a month without a test look passed. Hazards: the reset
consoles' tests stamped 2016 (re-dated by the test numbers), Dellwood's renumbered tanks. Stops: count every PASS row
(the reprints fill gap months); drop the 2016 rows (the reset weeks' tests lost); the answer.

**A3, the sales input's annual trail (H18: the trail of the dock sales the reconciliation consumes, to the year's
total by product, which the onboarding form asks).** For each marina, the 2026 dock gallons by product, to the
nearest gallon. 18 figures. Files: `dock_sales_legacy_2026.csv`, `dock_sales_2026-11-09_2026-12-31.jsonl`,
`pos_product_setup.csv`. Primary device (D2, version): the new point-of-sale ran in shadow from 9 to 15 November
beside the legacy system and its shadow export captured card sales only; that week the legacy export is the complete
version and the new export's card rows repeat it with other transaction numbers and stamps. Second device (D5,
scope): at go-live on 16 November each marina's pumps were proved with test volumes returned to the tank, recorded by
the new system as zero-price sales. Hazard: the new export's UTC stamps put New Year's Eve evening sales into 2027.
Stops: keep both exports whole (the shadow week's card sales twice); drop the legacy week (its cash sales lost);
count the proving volumes as sold; the answer.

Main population zero-counts (asserted): season rows with a 2016 stamp 0; season rows from a shadow export 0; season
zero-price proving rows 0; season reprinted test rows not applicable (ask-only file); season inventory rows keyed by
the pre-February numbering 0.

| Hazard | Asks moved | Per-ask delta |
|---|---|---|
| UTC against local time | A1, A2, A3 | measured in `generator/ceiling.py` |
| the January clock resets | A1, A2 | measured |
| Dellwood's console replacement | A1, A2 | measured |

Referee: none arbitrates a designed disagreement; every control ties under every handling.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule) | Its stop | Kept |
|---|---|---|---|
| A1 feed readiness | drops the 2016 rows as out of range | 2016 rows dropped | miss |
| A2 leak-test record | counts each PASS row in its month | reprints counted | miss |
| A3 dock gallons | dedupes the shadow week by matching pairs, keeps the proving volumes as sales | proving volumes kept | miss |
| full includer | finds the resets, reprints and shadow week but keys Dellwood by console number and counts proving volumes | partial | miss |

Mirror leakage: 34.0 per cent of ask weight (design target; `generator/ceiling.py` measures it on the cut pack).
Pair ceiling: 52.0 (design target; replaced by the measured value).
Measured by: generator/ceiling.py

## Architecture 1 record

A regional public health service's wastewater surveillance of SARS-CoV-2 at 24 treatment plants (epidemiology-public-health, disease-surveillance-outbreak-anomaly-detection), shipped 2026-10-18 with no portal result (judge DETERMINISTIC on 4733488b, `determinism_check_report_arch1.md`; leak reader `leak_check_report_arch1.md`) and re-rooted 2026-11-02 at the Batch 3 queue reset: one architecture per world, so the wastewater world is closed. Its note as it stood, headings demoted.

### Draw

Card `cards/task248.json` (architecture 1, registered 2026-10-18). Guard verdict WARN, no BLOCK. test.same_puzzle_older
is a NOTE, differentiated on the card against task133's v1 lineage: there a filed outcome curve is conditioned on each
unit's own survival to date; here a measurement loses part of what it carries in transit at a rate that moves with
the season, read against each unit's own baseline. Each WARN, answered: overuse.org_family (government_agency): a
regional public health service is a government agency and no other key is true of it; repeat.decision
(quantity_figure after task165): the desk plans on a count of episodes; repeat.deliverables (docx and xlsx after
task165): a planning note to the surveillance manager and the workbook behind it are what a coordinator sends. Nearest
driver 0.06 (task170, task99 lineage, task234 v1 lineage).

- **Pairing.** Epidemiology & Public Health / disease-surveillance-outbreak-anomaly-detection, a task type serving
  Anomaly Detection and Data Quality Monitoring; drawn for Data Quality Monitoring & Alerting. Not banned against the
  last three builds (task201 energy anomaly detection, task247 physical and environmental sciences data quality,
  task165 urban forecasting). The object is the health of the wastewater dashboard's levels, how much of each plant's
  winter rise is the sewer destroying less of the virus's RNA in cold water rather than more virus, and the call is a
  monitoring decision: how many alert episodes the verification desk plans for once the dashboard reads every sample
  on the shed load.
- **The seed, re-found.** DQ21 gave the world (a duty desk that checks every alert episode a monitoring system
  raises), the decision (the desk sized for the coming season on episodes) and the quantity (alert episodes). Its
  air quality network is left, its pairing banned against task247, and its pitfall (consecutive exceedances counted as
  one episode under the policy's gap rule) is rule application: here the episode rule is filed and executed by every
  route, and the decisive step is the reconstruction of the record the episodes are read on.
- **Niche.** A regional public health service in New Zealand runs wastewater surveillance of SARS-CoV-2 at 24
  treatment plants: two 24-hour composite samples a week, the laboratory's concentrations of the N1 gene and of PMMoV,
  the plants' flows and inlet temperatures from the water services company. The dashboard gives each plant a weekly
  level against its own baseline and the verification desk checks every alert episode (a run of weeks at High or
  above) before the public health team acts on it. From 1 May 2028 the dashboard reads every sample on the shed load:
  the plant's concentration with the RNA the sewer destroyed on the way from the town to the plant restored.
- **The call.** How many alert episodes the desk plans for over winter 2028, on the planning basis the service uses:
  last winter's samples (May to September 2027) read as the dashboard will read them, with every plant's episode
  count on the published basis and on the shed load.
- **Shape.** 03, a bridge from the published total to the shed-load total, plant by plant (24 plants by two counts),
  the total, the plants whose count moves, a chart of each plant's winter levels or counts on both bases, and the asks;
  well over 25 criteria. Decision quantity_figure, answer count, question form how many.
- **Strategy.** other, named in the card's notes: a measurement's in-transit loss whose rate moves with the season,
  read against each unit's own baseline (neither censoring nor a composition shift). G9 decisive (what reaches the
  plant is what survived the sewer, not what the town shed), G16 (one decay rate, PMMoV normalization, a temperature
  term beside travel time, or the rate as a function of temperature over travel time), G4; gap time then population;
  Gate G decomposition_attribution (each plant's winter rise assigned to its two drivers, more virus and less decay);
  calibration physical_verification (the paired study's upstream composites, taken where the town's sewage enters the
  trunk sewer); context artifact monitoring_export (the dashboard's level and episode export); Layer 2 family
  field_method, pattern own:temperature-dependent-in-sewer-decay-over-travel-time-against-own-baseline.
- **Forum, event, organisation.** line_manager_or_team (the service's surveillance manager signs the desk's winter
  rota), cutover_or_migration (the dashboard moves to the shed load on 1 May 2028), government_agency (a regional
  public health service). Role capacity_planner (the wastewater surveillance coordinator rosters the desk and asks).
- **People** (`guard.py names --geo "New Zealand" --seed 248`, locale en_NZ): Fiona Chandler, the wastewater
  surveillance coordinator, who asks; Luke Jefferies, the molecular laboratory's scientist; Craig Stuart, the water
  services company's network modeller (travel times); Alana Costello, who ran the paired upstream study. None appears
  in the prompt.
- **Data-native sentence.** The virus's RNA decays on its way down the sewer at a rate that rises with the water's
  temperature, so a plant at the end of a long trunk sewer loses far more of it in summer than in winter; its baseline
  is set by the summer lull, when the losses are largest, and its winter samples arrive with much more of their RNA,
  so on the plant's concentration the cold months look higher against the baseline than the town's shedding was, and
  only a loss that moves with the temperature can take that out, since anything constant over the year scales the
  winter samples and the baseline alike.
- **As-of.** Wednesday 12 April 2028, before the cutover on 1 May.
- **Sources.** The client's two-layer standard (field_method: the field's own method done right); published wastewater
  studies of SARS-CoV-2 RNA decay in sewage (first order, faster in warm water) and the use of population-weighted
  travel times from network models. No build on file takes wastewater surveillance as its object (task160 lists
  wastewater results as one input to a hospital surge plan; task121 names a wastewater plant as an odour source);
  task189 and task190 spent detection-limit censoring, which this build does not use.

### Default path

1. Read the laboratory's export: the accepted run of each sample and target (the export notes); each sample's N1 load
   per person is the concentration times the composite's flow on the chain-of-custody form times 1,000 over the
   register's population served (methods note section 3).
2. Weekly values by the week of the day the composite ended, each plant's baseline the 10th percentile (PERCENTILE.INC)
   of its weekly values of the weeks starting 6 April 2026 to 29 March 2027, the levels, the episodes (open at 1.0 or
   more, close below 0.5), winter 2027's those opening in the weeks starting 3 May to 27 September (sections 4 and 5):
   30, the dashboard's export.
3. The shed load (section 6.1) restores the RNA the sewer destroyed, resting on the paired study and the travel times:
   fit one first-order decay rate to the study's ratios of plant to upstream N1 against the travel time (0.0408 an
   hour) and multiply every sample's load by exp(that rate times the plant's travel time in hours).
4. Recompute the weekly values, baselines, levels and episodes on the shed load per person, as section 6.1 says.

Ends on: 30 alert episodes on the shed load, every plant's count as published, no plant moving.

Golden: 26 alert episodes: Ardenmouth South, Ardenmouth East, Tarnbrook, Cleaveland Flat and Saltmarsh Point one fewer
each and Ardenmouth West one more, with each sample's RNA restored at the paired study's decay rate for the composite's
own inlet temperature (0.050 an hour at 20 degrees, rising about 9 per cent a degree) over the plant's travel time.

### Stump sentence

A competent analyst restores each sample's shed load with the paired study's single decay rate over the plant's travel
time (or reads the samples on PMMoV-normalised concentrations) and ends on 30 alert episodes, every plant as published;
the step that lands it there is treating the sewer's loss as a constant, when the RNA's decay rate rises with the
water's temperature, so at the long trunk sewers the summer samples that set each plant's baseline lost far more than
the winter samples (at Cleaveland Flat the study's composites lost 0.69 log10 in December to February and 0.31 in June
to August), and a correction constant over the year lifts a plant's baseline and its winter samples alike; only the rate
at each composite's own temperature over the travel time lifts the baselines at the long sewers more than their winter
samples (by 0.52 to 0.68 log10 against winter peaks that fall from 1.06 to 1.14 to under 0.81), removes the five
episodes the colder water alone raised and splits Ardenmouth West's merged one in two, 26.

### Three rules

- **Task type:** epidemiology-public-health / disease-surveillance-outbreak-anomaly-detection, which serves Data
  Quality Monitoring & Alerting (the dashboard's levels and alert episodes are the monitored data product, and the call
  is the monitoring decision taken on them: how many episodes the verification desk checks once the levels are read on
  the shed load).
- **Domain test:** the quantity that decides is each plant's weekly level on the shed load, which wastewater-based
  epidemiology recovers from the plant's concentration by treating the RNA's in-sewer decay as first order over the
  population-weighted travel time at a rate that rises with the water's temperature, the rate measured by paired
  composites at the trunk sewer's head and at the plant.
- **Swap:** "how many alerts should our hospital desk plan for, reading last winter's admissions on the corrected
  count" keeps the sentence and loses the task: there is no sewer, no travel time over which a virus's RNA decays
  faster in warm water, no paired upstream composite and no faecal marker riding along, so a temperature-dependent
  restoration has nothing to act on.
- **Layer 1:** the laboratory's export by analysis run (rejected and check runs beside the accepted), the composite's
  flow from the operator's form, the paired study's copies per millilitre in triplicate with probe readings and missed
  visits, the travel times in the network modeller's memo table, the historian's local time across both daylight saving
  changes; each written by the laboratory's system, the operator, the field team, the modeller or the historian, none
  placed, and the call is the same under every handling (SF2, SF5, SF11, the R2 block). The contract report, the second
  inlet channels and the historian's faults since October 2027 lie outside the call's rows (S1).
- **Layer 2:** field_method, the field's own method done right: the in-sewer decay of SARS-CoV-2 RNA as first order at a
  rate depending on the water's temperature, applied at each composite's own temperature over the travel time, where
  the easy routes take the loss as a constant or divide by the faecal marker.
- **Decisive step:** fitting the paired study's loss as a temperature-dependent first-order rate, k(T) = k20 times
  theta^(T - 20), and restoring each composite at its own inlet temperature over the plant's travel time, rather than
  with one rate, a PMMoV ratio or a temperature term beside the travel time.
- **Not semantics:** reading every field, code, unit and definition right (the accepted run, the form's flow, copies per
  millilitre, the memo's minutes, the weeks, PERCENTILE.INC, the episode rule, the shed load's definition) still leaves
  the single-rate route on 30: the methods note defines the shed load as the load with the destroyed RNA restored and
  points to the study and the travel times, and nothing says how the destruction varies.
- **Not rule application:** the methods note files the estimand (the shed load, the levels, baselines and episodes
  computed on it exactly as on the load per person, the winter's weeks) and no model of the decay; executing every
  stated rule with the study's average decay gives back the published 30, and no filed rule ties the decay to the
  temperature.
- **Analyst test:** a strong analyst who reads every file right fits one decay rate to the study's ratios against the
  travel time, restores every sample with it, recomputes the baselines and levels and ends on 30 alert episodes, every
  plant as published; on the simulator's clean truth the same route files 30 and the temperature-dependent rate alone
  files 26, the towns' true shedding also 26 (R3a, R3b in checks.py).
- **Estimand:** the methods note (`wastewater_dashboard_methods_v4.pdf`, sections 3 to 6.1) with the prompt: the alert
  episodes of the 24 plants that open in the weeks starting 3 May to 27 September 2027, each plant's weekly value the
  mean log10 shed load per person of the week's samples, its baseline the 10th percentile of its weekly values of the
  weeks starting 6 April 2026 to 29 March 2027, an episode opening at 1.0 and closing below 0.5; the count against the
  published count.
- **No decoy:** nothing is planted: no memo, draft or stakeholder figure argues a count; the request names none; the
  dashboard's export is its published levels and episodes, correct on their basis and the bridge's starting total the
  prompt asks for; the study's field report gives its design and no result; the two distractors (rain gauges, the
  laboratory's quality assessment returns) give no plant a level.
- **No certified replay:** no certified or published shed-load figure exists for a method to reproduce; the method is
  found from the study's own pairs (the loss at the long trunk sewers more than doubling from winter to summer) and the
  field's first-order model.
- **Lesson:** a measurement's in-transit loss whose rate moves with a seasonal covariate does not cancel against a
  unit's own baseline the way a constant loss does; restoring it at the covariate's value for each measurement is what
  moves the levels, and the units with the longest transits move most. No build on file spends it (task247 refilled
  cloud gaps from both sides; task133 conditioned a curve on survival; no build takes wastewater as its object).

### Readability screen

Six tests per rung (stumping 2.1): 1 a filed sentence names the decisive quantity or sends the solver to it; 2 a
column, key or marker makes it a row predicate or a header-found join; 3 an opponent reflex reaches it; 4 a control or
corpus scores the rules or refutes the naive read; 5 the hygiene battery finds it; 6 one subtraction, ratio or half of
a reported figure.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 the published levels: 30 | the dashboard's export | the episodes sheet | yes, the operational record | none | no | read off | readable |
| 1 (default) one decay rate over each travel time: 30 | the methods note's shed load and the study | the study's ratios, the memo's travel times | yes, a decay constant from the study | the study's pairs fit one rate on average | no | one factor per plant | readable |
| 2 the samples divided by their PMMoV: 30 | none | the PMMoV rows | yes, the field's habit of normalising by the faecal marker | none | no | a ratio | readable |
| 3 a temperature term beside the travel time: 22 | none | the study's water_temperature_c | partly, a regression on the study's columns | the study's pairs | no | one regression | readable |
| 4 the temperature-dependent rate at the four study plants only: 28 | none | the study's plant codes | partly | the study | no | a fit | readable |
| 5 (decisive) the rate as a function of temperature at each composite's inlet temperature over every plant's travel time: 26 | no sentence names a temperature dependence; the methods note says the restoration rests on the study and the travel times | the study's water_temperature_c sits beside pH and conductivity, the historian's inlet_temperature_c beside the flow | no: the reflex is a constant rate or the marker | the study refutes the constant rate only when its ratios are read against the water's temperature or the season (0.69 against 0.31 log10 at Cleaveland Flat) | no | not linear: a rate per composite, then each plant's baseline, levels and episodes | silent |

### Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | winter 2027's episodes | those opening in the weeks starting 3 May to 27 September 2027 | those open at any time in the winter | same call | no plant is open on 26 April 2027 (SF9); methods section 5 |
| SF2 | a sample's week | the week of the day its composite ended | the week of the day it started | same call | same counts at every plant on both bases (asserted); methods section 4 |
| SF3 | the baseline | PERCENTILE.INC, the 10th percentile | PERCENTILE.EXC | same call | same counts (asserted); methods section 4 |
| SF4 | the reference weeks | the weeks starting 6 April 2026 to 29 March 2027 | none differs | converge | 52 weeks (asserted); methods section 4 |
| SF5 | the composite's flow | the form's (the published basis) | the historian's 24-hour inflow | same call | same counts on both bases (asserted); methods sections 3 and 6.2 |
| SF6 | the temperature | each composite's mean inlet temperature over its 24 hours | the month's or the season's mean; the study's plant, upstream or mean reading for the fit | same call | same counts at every plant (asserted, the variants) |
| SF7 | the travel time | the memo's population-weighted minutes | the shortest or longest sub-catchment | ruled out | methods section 6.1 "each plant's population-weighted travel time" (SF7 asserted on the memo) |
| SF8 | an episode's close | the first week back at Low (below 0.5) | the first week below High | ruled out | methods section 5 "back at Low" |
| SF9 | where episodes are followed from | the record's first week | the reference year's or the winter's first week | same call | every plant below 0.45 in the week of 26 April 2027 on both bases (asserted) |
| SF10 | the shed load's baseline | recomputed on the shed load | the published baseline kept | 28, ruled out | methods section 6.1 "exactly as sections 4 and 5 compute them" (asserted) |
| SF11 | a sample's result | the accepted run | the latest, the first or the mean run | same call | same counts (asserted); methods section 2 and the export notes |
| SF12 | the faecal-strength check on last winter's samples | no composite of April 2026 to September 2027 fails it | none differs | converge | asserted |
| SF13 | the decay's units | the study's natural-log ratios per hour, levels in log10 | the rate fitted on log10 ratios | same call | one rate in either unit (the fit's form) |
| SF14 | the population | the register's population served | none differs | converge | methods section 3 |
| SF15 | the published total | the dashboard's export | recomputed from the laboratory | converge | the same 30 and the same plants (asserted) |
| SF16 | counts and hours | whole numbers | none | converge | the prompt |
| SF17 | Ask A's window | local days, 1 April 2027 to 31 March 2028 | UTC days | same figures | no fault within a day of either edge (asserted) |
| SF18 | Ask B's composites | by the day the composite ended | by the day it started | same figures | no failing composite among the window's first or last two (asserted) |
| SF19 | Ask B's inflow where an hour lacks a reading | the mean of the valid readings times 24 | the raw sum, the valid sum, interpolation | same figures | every fill gives the same failures (asserted) |
| SF20 | Ask B's failure | more than 0.5 log10 above or below the median | below only | same figures | methods section 6.3; same failures (asserted) |
| SF21 | Ask B's 365 days before the composite's day | the 365 days before it | including the day 365 or 366 days before | same figures | no composite falls 365 or 366 days before another (asserted) |
| SF22 | Ask A's hour | an hour of the clock as it ran (8,784 in the year, two at 02:00 on 4 April 2027, none at 02:00 on 26 September 2027) | each wall-clock label of the year once | +1 at every plant, ruled out | the export note's span, "23:00 on 9 April 2028, 19,825 hours", one more than its 826 days of 24 labels (asserted) |

### Ladder

Five wrong rungs and the golden, each a defensible way to restore the shed load, each dying to one fact of the study
(per-plant counts on the cut pack, printed by `generator/pair.py --ladder`, asserted in `checks.py`).

| Rung | Construction | Answer | Dies to |
|---|---|---|---|
| 0 | the published levels (the dashboard's export) | 30, every plant as published | the dashboard moves to the shed load on 1 May (methods 6.1) |
| 1 (default) | one first-order rate fitted to the study (0.0408 an hour) over each travel time | 30, every plant as published | the study's own loss at the long sewers more than doubles from winter to summer, so a rate constant over the year is not the sewer's |
| 2 | the samples divided by their PMMoV | 30, every plant as published | PMMoV barely decays, so the ratio keeps the N1's own loss in, as constant over the year as the marker |
| 3 | a temperature term beside the travel time, ln(plant/upstream) = c0 + c1 tt + c2 T | 22: CRF, FNK, GLO and INB also lose their episode | the loss does not move with temperature at the short sewers (Dunkerley's 0.06 against 0.04 log10), so the term corrects them as much as the long |
| 4 | the temperature-dependent rate at the four study plants only | 28: ADS and CLF move | every plant's sewer decays by the same law over its own travel time (methods 6.1 names every plant's) |
| 5 (golden) | the temperature-dependent rate at each composite's inlet temperature over every plant's travel time | 26: ADS, ADE, TRN, CLF, SLT -1, ADW +1 | |

- **Margins.** The smallest uniform shift of a plant's weekly levels that moves its winter count is 0.10 at Ardenmouth
  West and 0.16 or more everywhere else on the shed load, 0.06 (Ardenmouth South) on the published basis. Every
  temperature-dependent route (linear in temperature, plant by plant, the upstream or plant reading, the composite's,
  the month's or the season's temperature, the historian's flow, the marker-normalised ratio in the study) gives every
  plant's count (asserted).
- **Position.** No wrong rung reaches 26; the four plants of the study reach two of the six moves.
- **Dominance.** The decisive step lifts the long sewers' baselines by 0.52 to 0.68 log10 (Ardenmouth West 0.37) while
  their winter peaks fall from 1.06 to 1.14 to 0.78 to 0.80; at the short sewers it moves nothing.
- **Grid.** Published, constant rate, PMMoV, additive term, study plants only, the rate at temperature: 30, 30, 30, 22,
  28, 26; the flows (form, historian) and runs (accepted, latest, first, mean) cross every cell with the same counts.
- **Worth.** Four episodes on the total and six plants' counts; the clean truth's towns shed 26 with the same six moves.

### Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | the register's 24 plants, every one in the count |
| 2 | Unit of account | one alert episode (methods 5) |
| 3 | Attribution window | episodes opening in the weeks starting 3 May to 27 September 2027 (methods 5, SF1) |
| 4 | As-of dating | Wednesday 12 April 2028: the laboratory to the composites of 6 April, the historian to 9 April; the cutover 1 May |
| 5 | Version basis | methods note v4 (section 6 from 1 May 2028); the study's 2026 pairs; the memo of November 2025 |
| 6 | Denominator | the register's population served (SF14) |
| 7 | Weighting | each week the plain mean of its samples' log10 loads (methods 4) |
| 8 | Window length | the 52 reference weeks (SF4); the composite's 24 hours |
| 9 | Boundary inclusivity | High at 1.0 or more, Low below 0.5 (methods 5); the winter's first and last weeks included |
| 10 | Rounding path | none before the count; whole numbers (SF16) |
| 11 | Tie-break | none needed |
| 12 | Maturity and censoring | every composite of the window analysed and accepted; no result is pending for winter 2027 |
| 13 | Order of operations | accepted runs, loads, the restoration, weekly values, baseline, levels, episodes |
| 14 | Row order | no step depends on file order |
| 15 | Duplicate resolution | the accepted run (SF11) |
| 16 | Identity normalisation | plant codes across the export, register and historian; the memo's codes |
| 17 | Netting against gross | none |
| 18 | Dimensional units | gene copies a litre; the study's per millilitre (ratios unit-free, SF13); minutes to hours; cubic metres |
| 19 | Code and status semantics | accepted, rejected, check (SF11); the bands (methods 5) |
| 20 | Integerisation | counts whole (SF16) |
| 21 | Clause scope | section 6.1 applies to every plant (rung 4); sections 4 and 5 on both bases (SF10) |
| 22 | Forward window contents | winter 2028 is planned on winter 2027's samples read on the shed load (the prompt, the request) |

### Literal reader

Executing the prompt and the methods note word for word: the episodes of the 24 plants opening in the weeks starting 3
May to 27 September 2027, on the shed load per person, its baselines and levels computed exactly as on the load. The
shed load needs the RNA the sewer destroyed restored, which no sentence quantifies; every restoration that takes the
study's decay as a first-order rate depending on the water's temperature at each composite's own temperature, over
each plant's travel time, files 26 with the same six moves (linear or exponential in temperature, pooled or plant by
plant, the plant's, upstream or mean probe reading, the composite's, the month's or the season's temperature, either
flow), and every convention row of the fork table files 26. The easy answer, 30, comes from an easy method (a constant
rate or the marker) on the same literal estimand, never from another reading.

### Oracles

None for the call: no shed-load figure, earlier restoration or ranking on it ships. The dashboard's export ties the
published basis under every handling; a constant restoration reproduces its levels by algebra, which is the stump's own
identity and holds whether or not the export ships. The paired study confirms the temperature dependence only when its
ratios are read against the water's temperature or the season. For the asks, the historian's export note (the
definition of a valid reading) and the year's own clock referee Ask A, and the contract report's method line referees
Ask B; neither names a row or a plant.

### Ask sheet

**Ask A, each plant's hours from 1 April 2027 to 31 March 2028 with no valid inlet flow reading in the historian (24
figures, whole hours).** H18: the historian becomes the dashboard's flow source at the cutover (methods 6.2), so its
hours without a valid reading are the input audit of the new basis; the call reads the historian only for each
composite's temperature over its 24 hours from April 2026 to September 2027, which no fault reaches. Use: the desk fills
by hand every composite whose flow the historian cannot give. Primary devices: D8 (a clock against the window): the
historian keeps New Zealand local time, so the year has 8,784 real hours, 02:00 on 26 September 2027 never happens and
02:00 on 4 April 2027 happens twice with a row each; a grid of every wall-clock hour counts the skipped hour as a gap at
every plant (+1), and removing duplicate plant-and-timestamp rows, the reflex repair for the 165 rows the historian
re-sent after outages, deletes one of the two real 02:00 readings at every plant (+1). D4 (absence as the signal): an
hour the historian received nothing for has no row, so counting the invalid rows the export holds misses every
drop-out (-12 to -47 at every plant). The export note gives its span as 19,825 hours, one more than its days of 24
wall-clock labels, so the clock's hours are the record's (SF22), with no sentence naming the clocks. Hazards: held readings (every reading after the first of four or more identical
consecutive readings; counting the whole run adds 1 to 3 at 17 plants), blank flows, zero and negative readings, the
re-sent exact duplicates. Path: the historian, its export note, the dictionary, the request (4 files, 4 columns).
Realism: the outstations moved to a new cellular network in October 2027; hourly historians export local time and skip
or repeat the changing hour.

**Ask B, each plant's composites from 4 October 2027 to 30 March 2028 that fail the faecal-strength check (24 figures,
whole counts).** H18: the check starts with the cutover (methods 6.3) and every failing composite comes to the desk
before its result enters the level, the desk's second stream of work; the call reads no PMMoV row and no composite after
September 2027. Primary device: D3 (units set per source): the contract laboratory that analysed the closure's
composites (23 December 2027 to 6 January 2028, five at every plant) reports gene copies per microlitre of extract, its
method line giving the volumes (100 mL concentrated, the pellet resuspended in 2 mL, 200 microlitres extracted, eluted in
100), so a copy per microlitre of extract is 10,000 a litre; read as copies a litre, scaled to the litre without the
aliquot (x1,000) or as microlitres to litres (x1,000,000), every closure composite fails at every plant (+3 to +5 at all
24). Hazards: the form's flow at the three plants with a second inlet channel since 18 October 2027 (the sampler's
controller sees one channel: +31 to +43 at KSB, PLH and UWD); the first analysis run of a re-extracted sample (+1 to +3
at 20 plants); the report left out (-1 to -2 at 5 plants, the closure's own failures missed); the historian's faults
inside composite windows (every fill gives the same failures, SF19); the report's abbreviated site names. Path: the
results export, its notes, the contract report, the register, the historian, its note, the methods note, the dictionary
(8 files, 12 columns: plant_code, composite_end, target, status, result_gc_per_l, composite_flow_m3, client site,
sampled, analyte, result, population_served, inlet_flow_m3h). Realism: contract laboratories report per microlitre of
extract with their method's volumes, and a second inlet channel's flow reaches the historian before the sampler's
controller.

Main population zero-counts: the call reads the laboratory's N1 accepted runs of the composites of January 2026 to
September 2027 and the historian's temperatures over their 24 hours; no fault, spoiled composite, contract composite or
second channel sits in those rows, and the call computes the same without the contract report and the distractors (S1).

| Hazard | Asks moved | Per-ask deltas (largest) |
|---|---|---|
| the skipped and repeated clock hours (D8, primary) | A | +1 at every plant |
| drop-outs without a row (D4, primary) | A | -47 |
| held readings counted whole | A | +3 |
| the contract report's units (D3, primary) | B | +5 at every plant |
| the form's flow at the two-channel plants | B | +43 |
| the first analysis run | B | +3 |
| the contract report left out | B | -2 |

| Ask row | The cracker (landed the call, hygiene battery, every filed rule executed) | Verdict |
|---|---|---|
| Ask A, hours, all 24 plants | the historian with duplicate plant-and-timestamp rows removed, on the year's local clock hours (or every wall-clock hour) | miss |
| Ask B, failing composites, all 24 plants | the historian's inflow, the accepted runs, the contract report's copies per microlitre of extract scaled to the litre through the concentrate (x1,000) | miss |

Measured by: generator/pair.py on the cut pack: the cracker keeps 0 of the 48 ask figures; the lazier paths keep 0 to
4 (the form's flow with first runs keeps 4); a response meeting every device keeps all 48 (58.1 with it on the call).

Pair ceiling: 30.6 ((38 + 7 + 55 x 0) and (4.6 + 7 + 55 x 0.083), averaged)

Mirror leakage: 8.3 per cent of ask weight

### Pre-ship check

1. Domain: the call stands on each plant's weekly level on the shed load, recovered from the plant's concentration by
   the field's first-order model of the RNA's in-sewer decay at a rate that rises with the water's temperature, over
   the population-weighted travel time, the rate measured by paired composites at the trunk's head and at the plant;
   with another field's nouns (a hospital's admissions, a utility's meter reads) there is no sewer, no travel time over
   which a virus's RNA decays faster in warm water and no paired upstream composite, so the task stops making sense.
2. Two layers: Layer 1 (the export by analysis run, the form's flow, the study's copies per millilitre in triplicate
   and its missed visits, the memo's minutes, the historian's local time across both clock changes) is neutral on the
   call (SF2, SF5, SF11, the R2 block, S1). Layer 2 is the temperature-dependent restoration, asserted alone to move the
   easy route (30) to the golden (26) on the simulator's clean truth, where the towns' true shedding also gives 26 (R3).
3. No banned stump decides: nothing is planted (the dashboard's export is its published basis, correct and asked for
   as the bridge's start; the field report gives no result); not semantics (every field read right, the single-rate
   route still files 30); not rule application (the methods note files the estimand and no model of the decay).
4. Gate G: no shipped artifact counts episodes on the shed load; the dashboard's export is the context artifact
   (correct on its own basis, declared in metadata.json); the two distractors (rain gauges, the laboratory's quality
   assessment returns) give no plant a level.
5. Determinism: thirteen temperature-dependent routes (linear, exponential or plant-by-plant in temperature, the
   plant's, upstream or mean reading, the composite's, month's or season's temperature, either flow, the N1 over
   PMMoV ratio in the study) give every plant's count; 20 fork rows asserted; the verifier recomputes every graded
   figure by its own code (the IANA zone, a non-linear fit; 242 checks); two builds byte-identical.
6. Fingerprint: heart WARN (overuse.org_family, repeat.deliverables, answered in the Draw; same_puzzle_older NOTE
   differentiated against task133); the surface screen promotes no pair and reads the four card personas only.
7. Judge (one isolated thread, Sonnet, medium, the bundle and the graded blocks only, on target.zip 4733488b):
   DETERMINISTIC, APPROVE; every graded figure reproduced (30 published, 26 on the shed load with the same six moves,
   the decay fit, the seasonal losses, all 48 ask figures); Gate G method_or_model_selection, analytical_non_defect;
   Gate H domain, layers and decisive step pass; spec gates pass. It varied theta from 1.07 to 1.10, scaled the rate
   0.5 to 2 times and tried linear, plant-only, upstream-only and monthly temperatures and the historian's flow: 26
   every time; the temperature term cuts the study's residual sum of squares from 7.57 to 1.02 (F = 637). Taken from
   it: its fit gave theta 1.0875, on the 1.087/1.088 edge, so the write-up states 0.050 an hour, about 9 per cent a
   degree and theta 1.09, the figures every fitting route prints (asserted); and its finding 1, the hour at the clock
   changes in Ask A, closed by stating the export's span in hours in the historian note (19,825, one more than its
   days of 24 labels, SF22), the fact the reader then used to settle the hour without any sentence naming the clocks.
   The shipped bundle differs from the judged one by that sentence only; no graded figure moved.

### Leak check

leak.py (as-of 2028-04-12): REVIEW, no LEAK; author vocabulary, column names, announcements, hidden content, dates
and the prompt gate clean. Each REVIEW line, answered:

- The field report names Ardenmouth South and Cleaveland Flat beside "travel times": they are two of the study's four
  plants, named as its design; harmless.
- The dictionary, the folder's contents and the methods note carry the words of the call (verification desk, alert
  episodes, winter): the fiction's own vocabulary; none states a count; harmless.
- Design-note vocabulary in the documents (wastewater, episode, baseline, composite, travel, temperature): the
  domain's own words; no document says how the decay varies or names a restoration (R1 asserts no "decay rate", "per
  degree", "warm water" or temperature dependence in any document, through a control sentence found first); harmless.
- The prompt's second sentence carries plant, level and shed load: the asks' own nouns; harmless.
- The travel-time memo names plants beside numbers: a lookup of travel times, not a ranking on the decision; harmless.

Reader (isolated, Sonnet, medium, the prompt and a fresh pack only), three reads: the first on 4733488b, the second
after the span sentence, the third after its rewording. Q1 to Q4 none in every read; Q6 analytical; each read the
decisive step as a decay-per-travel-time fit from the study and none named the water's temperature. Taken from them:
the clock-change hour (closed as above), the span sentence first worded as if every plant held 19,825 rows (reworded
as the export's span, with a row for each hour the historian holds), and two ask readings answered by assertions
already in place (the median window's boundary, SF21; the closure's composites as the plant's composites, methods
6.3). Left as they are: the main wave's episodes opening within three weeks of each other at most plants (a regional
wave), the register's tidy populations.


## Tried and rejected

- 2026-10-18, the seed's own air quality network and any environmental-monitoring pairing: banned against task247
  (domain plus objective), and a fourth environmental build in the wave reads as a monoculture.
- 2026-10-18, wastewater levels with non-detects below the detection limit: the substitution-against-censored-estimator
  driver is task189's (left-censoring at limits that differ by laboratory).
- 2026-10-18, two-source capture-recapture of notified cases before electronic laboratory reporting: the estimate
  moves with every defensible stratification (Chapman against Lincoln-Petersen, setting against setting by district
  by age), so the count is not determinate; capture-recapture is spent in task199 and named in task243.
- 2026-10-18, coders' drift against a master coder on a stratified double-coded sample: the rater analysis reads the
  same with any field's raters (the noun swap fails), and measurers against a reference repeats task246's world.
- 2026-10-18, the episode count read on weekly levels without a way out of High: with no exit rule each plant's count
  chatters with the noise around the threshold, so the count moved with the fitted decay model; the filed episode rule
  needs an entry level and a lower exit level.
- 2026-11-02, architecture 1 (temperature-dependent RNA decay over each plant's travel time, 26 against the published 30
  alert episodes): re-rooted at the Batch 3 queue reset, not on a judge's or the portal's word; the world is closed.
- 2026-11-02, architecture 2 draw, a quarry's blast vibration monitors and the trigger each runs for the 2027
  programme, from an attenuation law fitted with the untriggered blasts as censored observations: task180's driver
  ("an event enters the record only when it rises above the noise at the instruments"), and the threshold-shaped
  record family (task104 approved, task250 v2, task251 v3).
- 2026-11-02, architecture 2 draw, a hospital laboratory's delta-check limits judged on wrong-blood-in-tube swaps
  between patients collected on the same round: the WHAT screen kills it (which pairs represent a swap is the
  population; filed it is rule application, unfiled it forks).
- 2026-11-02, architecture 2 draw, an in-line near-infrared model's error against the laboratory assay, matched by the
  material's travel time at the line's speed: two records of one event joined by time is task133's link, and a travel
  time sits on this slot's own lineage (the sewer).
- 2026-11-02, architecture 2 draw, each clinic's score reliability from a scale's conditional standard error: the share
  of score variance due to the trait is task237's quantity, and per-site alpha against marginal reliability forks.
- 2026-11-02, architecture 2 draw, an assay laboratory's batch release on certified reference materials: no decisive
  structure beyond batch-bias variance components (task228, task229 v1) or check-assay selection (task251 v3).
- 2026-11-02, architecture 2 draw, meter error variances read from the covariance of the balances two networks share:
  exact balances exist only in plant or utility networks (Energy Systems serves no data-quality task type) and the
  counting worlds are task251's and task114's.
- 2026-11-02, architecture 2 draw, the tank-chart mechanism at a fuel retailer's stores: task238 v2 (a grocery chain's
  price integrity) registered in parallel and holds retail; at a transportation department's maintenance yards:
  task153 holds a fleet-yard fuel world with bills of lading and a fuel management system. Moved to marina fuel docks.
- 2026-11-02, architecture 2, the filed quantity as the largest misstatement between any two heights of the working
  range (a max minus min over a continuous range): the prototype's interval fits inflated the range with estimator
  noise (unlisted tanks 2 to 23 gallons depending on knot spacing, two fits blowing up where no reading fell), so the
  limit is read at three register heights instead.
- 2026-11-02, architecture 2, a free dock-meter term in the interval fit as a rung: the proportional chart error and the
  meter error are collinear inside the intervals, so the fit is rank-deficient and no analyst stops there; the rung is
  the intervals with no anchor.
- 2026-11-02, architecture 2, deliveries running from a 22 per cent reorder height to 88 per cent: an offset chart then
  shows a quarter to two fifths of its range on its deliveries and two offset tanks crossed 25 gallons on the delivery
  check; the reorder and fill heights now sit near-symmetric about the middle, as an ordering policy that reorders low
  and fills to the overfill alarm's margin does.
- 2026-11-02, architecture 2, the weights-and-measures dock meter test records: a second anchor that makes the
  decisive step a lookup, and an ask on them teaches the rung; not shipped.

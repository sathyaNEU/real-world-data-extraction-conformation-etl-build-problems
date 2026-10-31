# task478 design note: the Tamsett Basin district's 2027 NOx agreements, by the NOx each facility's Rule 4306 boilers and heaters emitted in 2026

Status lives in `pipeline.json`; this note holds the design. Read the Tried and rejected section first. Architecture 7
(re-rooted 2026-10-23); the records of architectures 1 to 6 are at the end.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task478.json` (architecture v7), registered 2026-10-23 after a pull, the
  architecture 1 to 6 identities in its lineage. `check` on the registered card: WARN only, answered here.
  `repeat.gate_g` and `overuse.gate_g` (method_or_model_selection, task273 among the last two): the label is the honest
  one, since the decisive step is which construction carries a source test onto the year's emissions, pinned by the
  monitored burner and the units' own tests, and the driver it carries (a spot rate that follows a property of the fuel
  a third party supplies, carried by that supplier's monthly record) is on no other card. `test.same_puzzle_older` and
  `test.same_driver_older` (gap objective, G16, a ranked slate, method selection) against task190, task195 and task228
  v2: differentiated on the card. Nearest drivers on file at 0.06 (task85 v2.5, task196 v1, task229 v3, task480 v1);
  this slot's architecture 6 at 0.33, differentiated (its rate followed a clock the unit's own maintenance builds).
- **Redrawn at the draw, and why the replacements are the honester labels.** task482's architecture 6 is spent, so the
  live window is task249, task273 and task169. G7 (operating window) as the decisive generator BLOCKed against task249
  on the pattern ban and the same-driver test in the batch; G16 leads, because the decisive step is the method that
  carries a spot test to the year, and G5 sits under it, because what moves the rate is provided by a record outside
  the unit (the supplier's heat content). The decision's owner is the district's director of compliance, who negotiates
  the enforceable agreements with each facility (`compliance_or_audit`); the board of directors adopts the plan
  (`board_of_directors`), the agreements are contracts (`purchase_order_or_contract`) and the district is a local public
  agency of the counties it serves (`local_government`). Personas from `guard.py names --geo "United States" --seed
  478`: Kevin warned against task73 and was replaced; Andrew Greene (director of compliance), Anna Haynes (senior air
  quality engineer, emission inventory).
- **Pairing:** Physical & Environmental Sciences, task type `emissions-inventory`, which serves Data Extraction &
  Conformation (ETL). The ETL work conforms the boilers, steam generators and process heaters at fourteen facilities onto
  one 2026 NOx inventory: four units' continuous monitor hours (local standard time, substitute-data codes, the
  monitoring plan's unit ids against the district's device numbers), thirty-four units' source tests from two test
  databases (the older in ppmvd at 3 per cent oxygen and lb/hr, the newer adding lb/MMBtu), the facilities' monthly fuel
  statements in therms, MMscf and MMBtu (MMscf at the gas utility's heat content for the facility's BTU area and month),
  the utility's monthly heat content table and the permit list. Objective: Data Extraction & Conformation (ETL).
- **The decision and the quantity:** the Tamsett Basin Air Pollution Control District (fictional) names in its 2027
  Community Emissions Reduction Plan for the Lowry Creek corridor the five facilities, of the fourteen in its Appendix A,
  whose Rule 4306 units emitted the most NOx in calendar 2026, and signs a NOx reduction agreement with each by 1 April
  2027. A retrospective quantity with its reason: the plan sizes its agreements on the last closed year's emissions, and
  the agreements run from 2027.
- **Shape:** 01, a ranked list under a cap of five: fourteen facilities' 2026 NOx at the whole ton (14), the five (1),
  a chart's named parts (the fourteen bars, the five marked, the labels: 3), the files (3), and the asks' figures (the
  gas delivered and the standby engines' NOx for each facility: 28): 49.
- **Strategy:** `other`, named on the card: a property of the fuel a third party supplies, recorded month by month in
  its heat content table, carries each spot test across the year. Gate G `method_or_model_selection`: the conformed
  inventory is the object and no shipped artifact ranks the facilities. Gap objective, pattern none, generators G16
  (decisive) and G5. Layer 2 family `estimation_fit`, pattern `own:a spot test of an emission rate read on its day's
  fuel, carried across the year month by month by the fuel's heating value, the sensitivity read from a monitored unit
  of the same burner type and the units' own test histories against the supplier's monthly record`.
- **World:** United States, an unnamed state's Tamsett Basin, its air district's Lowry Creek corridor with fourteen
  facilities holding Rule 4306 boilers, steam generators and process heaters (a refinery, a paperboard mill, a fuel
  ethanol plant, a tomato cannery, a creamery, a university central plant, a medical centre, an almond processor, a
  poultry processor, a correctional facility, a commercial laundry, a tire retreader, a water reclamation plant and a
  combined-cycle plant's auxiliary boiler). The refinery's heaters and boiler run SCR and close their ammonia injection
  on their monitors' NOx; the paperboard mill's power boiler fires low-NOx burners under a monitor; every other unit
  fires low-NOx or ultra-low NOx burners whose combustion air is set by volume at tuning, with no oxygen trim, and is
  source tested every one or two years under the district's NOx rule. The gas utility serves the corridor through two
  BTU areas: Eastside on interstate gas of steady heat content, Westside blended with the Lowry Creek gas plant's
  residue gas, whose heat content follows the plant's ethane recovery from month to month.
- **Forcing fact:** the agreements are signed by 1 April 2027; the pack is as of 19 February 2027 (exports pulled 5 to
  16 February).
- **Data-native sentence:** a low-NOx burner whose combustion air is set by volume at its tuning burns a richer gas
  hotter, so its NOx rate rises about six per cent for each per cent the gas's heating value rises; a source test reads
  the rate on whatever gas its test month brought, and the Westside BTU area's heat content follows the gas plant's
  ethane recovery from month to month, which the monitored Lindqvist power boiler's hours and the units' own test
  histories trace against the utility's monthly heat content table.
- **The WHAT screen.** Population: the boilers, steam generators and process heaters Rule 4306 covers at the fourteen
  facilities (plan section 2). Outcome: the NOx each unit emitted. Window: calendar 2026. Unit: tons a facility, summed
  over its units. Comparison: the five highest of fourteen. The decisive step settles none of them: it is how a source
  test's rate is carried onto the year's emissions, which nothing files.
- **Sources, one line each:**
  - The stationary-source inventory field's own hierarchy (continuous monitors, then source tests, then factors) and its
    rule that a test is used only where it represents the year's operation: here a test is a correct reading of one day.
  - Gas interchangeability practice: a burner tuned on gas of one heating value runs richer and hotter on gas of a
    higher one when nothing trims its air, which is why utilities publish heat content by area and month and why such
    burners are retuned when a supply changes; a gas processing plant that rejects ethane into its residue gas raises
    that gas's heat content, and one that recovers it lowers it.
  - This slot's architecture 6 (a rate climbing with a catalyst's operating hours): there the unit's own maintenance
    clock moved the rate; here nothing at the unit changes and the cause is a property of a third party's delivery.
- **Same-puzzle and same-driver tests:** (objective, G16, ranked_slate_under_cap) and (objective, G16,
  method_or_model_selection) against the older builds task190, task195 and task228 v2, differentiated on the card.
- **Abstraction test:** the nearest drivers stripped of nouns (task85 v2.5, an observation window built from an
  intermediary's lead time; task196 v1, a rate that is the product of two factors; task229 v3, a daily value through a
  convex conversion; task480 v1, an instrument's under-recording) carry no spot measurement of a rate that follows a
  property of a supplied input, carried month by month by the supplier's own record of that property.

## Default path

1. Read the plan: the agreements go to the five facilities whose Rule 4306 units emitted the most NOx in 2026
   (section 2), each unit's emissions as the district's inventory guidance computes them: the monitored units from their
   hourly NOx mass, the others from their heat input and their NOx emission rate in lb/MMBtu.
2. Summed the four monitored units' hourly NOx mass for 2026 (local standard time, substitute hours as reported).
3. Converted every unmonitored unit's source tests to lb/MMBtu (the newer database's lb/MMBtu, the older one's ppmvd at
   3 per cent oxygen through Method 19), took the latest test, and multiplied by the unit's 2026 heat input from its
   fuel statements (MMscf at the utility's heat content for the facility's BTU area and month).

Ends on: Ashgrove Refining, Lindqvist Paperboard, Sedge Hollow Creamery, Tamsett State University and Valmora Renewable
Fuels (checks.py R3a and L0: Tamsett State University 8 tons against Merriwell Foods' 7).

Golden: Ashgrove Refining, Lindqvist Paperboard, Merriwell Foods, Sedge Hollow Creamery and Valmora Renewable Fuels
(Merriwell Foods 9 tons and Sedge Hollow 8 against Tamsett State University's 7).

## Stump sentence

The default path carries each unmonitored burner's latest source test across its 2026 fuel and names Ashgrove Refining,
Lindqvist Paperboard, Sedge Hollow Creamery, Tamsett State University and Valmora Renewable Fuels, Tamsett at 8 tons
against Merriwell Foods' 7; a low-NOx burner that meters its combustion air by volume burns a richer gas hotter, so its
NOx rises with the heat content of the gas its BTU area receives, which the Westside gas plant's ethane recovery moves
from month to month: Merriwell Foods' boilers were last tested in August 2025 on lean gas and fired their 2026 canning
season on rich gas, and Tamsett State University's were tested in May 2026 on rich gas and fired the winter on lean;
the rise the monitored Lindqvist power boiler traces against the utility's monthly heat content (about 6 per cent a per
cent), carried from each test's month to each 2026 month, names Ashgrove Refining, Lindqvist Paperboard, Merriwell
Foods, Sedge Hollow Creamery and Valmora Renewable Fuels.

## Three rules

Task type: emissions-inventory (Physical & Environmental Sciences): the Rule 4306 boilers' and heaters' monitor hours,
source tests, fuel statements and the gas utility's heat content conformed onto one 2026 NOx inventory, a task type
serving Data Extraction & Conformation (ETL).

Domain test: stationary-source inventory practice: the deciding quantity is each facility's 2026 NOx, which for the
units without a monitor is fuel times a rate that represents the year; a low-NOx burner that meters its air by volume
burns a richer gas hotter, so the field reads such a unit's rate on the heat content of each month's gas, not off one
test day; with another field's nouns there is no burner air-fuel ratio, no gas heat content and no source test to
carry, so nothing is left to decide.

Swap: put "hospital" for "facility" or "visits" for "tons" and nothing reads: there is no burner whose excess air a
supplied gas's heating value moves, no test day read against a year and no monitored unit of the same burner; the
abstract move (a spot measurement carried by a property of a third party's delivery) needs the field's own combustion
physics and the gas utility's heat content record.

Layer 1: the source tests split across two databases, the older reporting ppmvd at 3 per cent oxygen, lb/hr and the
load, the newer adding lb/MMBtu and heat input; the fuel statements in therms, MMscf or MMBtu by facility and year, MMscf
converted at the utility's heat content for the facility's BTU area and month; monitor hours in local standard time
with substitute-data codes and the monitoring plan's unit ids against the district's device numbers; a facility
renumbered after a change of owner; the older database's keys without their leading zeros and device prefixes; a test
deferred under a plant turnaround. Each is written by the system named, none is placed to be caught, and each read the
natural wrong way leaves the call where it is (checks.py R2a to R2f).

Layer 2: estimation_fit, each unmonitored low-NOx burner's rate carried across 2026 from the heat content of its tests'
months to each 2026 month's, by the rise of NOx with heat content the monitored burner of the same type and the units'
own test histories trace against the utility's table, instead of a test day's rate held for the year.

Decisive step: estimating the rise of a low-NOx burner's NOx rate with the gas's heat content (about six per cent a
per cent, from the monitored Lindqvist boiler's hours against the Westside table and the units' tests against the table
at their months) and carrying each unmonitored burner's tests from their months' heat content to each 2026 month's,
which moves the five from Ashgrove Refining, Lindqvist Paperboard, Sedge Hollow Creamery, Tamsett State University and
Valmora Renewable Fuels to Ashgrove Refining, Lindqvist Paperboard, Merriwell Foods, Sedge Hollow Creamery and Valmora
Renewable Fuels.

No decoy: nothing is planted: the monitor exports, the test databases, the fuel statements, the heat content table, the
event log and the documents are what each system writes; no report ranks the facilities, states a unit's 2026 rate or
says a test is unrepresentative; the heat content moves as a gas plant's ethane recovery moves it, every burner's
response is the one low-NOx burners without oxygen trim have, and every test passed its limit, so no notice or retest
sits beside any test.

Not semantics: every field, unit, oxygen basis, clock and code read correctly (ppmvd at 3 per cent, lb/hr, the
F-factor, therms, MMscf at the area's monthly heat content, substitute hours, device numbers) still leaves the careful
route on the latest test; the heat content is read correctly on the default path itself, to convert MMscf (every 2026
MMscf reporter is Eastside, where it barely moves), and no column or sentence says a burner's NOx moves with it; the
step is an estimate (the rise and each unit's level) and the carrying it sets, not a reading.

Not rule application: the plan files the population, the outcome, the window and the cap (the WHAT) and the guidance
the NOx the unit emitted over the year from its heat input and its rate; nothing filed says how a test becomes that
rate. Measured on the cut pack (checks.py L0 to L3, G2): the ten enumerated constructions short of the carrying (the
latest test; the mean, median, highest or last two tests; the permit limit; the limit where the last test predates
2026; the tests trended on the calendar; the monitored boiler's 2026 months as an index on each latest test, Westside or
every burner) file two fives other than the golden, nine of the ten the default's; the thirty the data leave standing
(the rise from the monitored boiler's hours, its monthly means, the Westside burners' tests or every burner's tests;
each unit's level from all its carried tests, their mean, median, latest, last two or three or those since 2022; the
power law; the older tests from lb/hr) file one five and the same 14 whole tons, Merriwell Foods at 9.01 to 9.13 tons
and Sedge Hollow at 7.97 to 8.17 against Tamsett State University's 6.89 to 6.97; what rules the rest out is no clause
but the monitored boiler's hours and the tests set against the utility's heat content by month, a join nothing in the
pack invites, where the heat content takes the Westside burners' within-unit test scatter from 0.071 to 0.029 in the
log and the monitored boiler's monthly mean rate follows the Westside heat content at a correlation of 0.999.

Analyst test: a strong analyst who conforms every test to lb/MMBtu, every fuel statement to heat input and every monitor
hour to 2026, and reads the plan and the guidance correctly, carries each unmonitored burner's latest test (or the mean
of its tests, or the monitored boiler's 2026 months as an index) across its 2026 fuel and names Ashgrove Refining,
Lindqvist Paperboard, Sedge Hollow Creamery, Tamsett State University and Valmora Renewable Fuels, Tamsett at 8 tons;
only each burner's tests carried by the heat content of each month's gas name Ashgrove Refining, Lindqvist Paperboard,
Merriwell Foods, Sedge Hollow Creamery and Valmora Renewable Fuels (checks.py R3a and R3b on the generator's clean
truth).

Estimand: the 2027 Community Emissions Reduction Plan section 2: the five facilities whose boilers, steam generators and
process heaters covered by Rule 4306 emitted the most NOx in calendar 2026, in tons, each facility the sum of its units.

No certified replay: no facility total, unit rate or 2026 inventory figure ships; the source tests are what each test
day read, the monitor hours what each monitor read and the heat content what the utility published, so no published
figure ties under either route.

Lesson: a source test is a correct reading of one day's rate on that day's fuel, and a year's emissions need the rate
the year ran at; a low-NOx burner that meters its air by volume burns a richer gas hotter, so where a supply's heat
content moves from month to month a burner's rate moves with it, and a test read on a lean month understates a season
fired on rich gas while one read on a rich month overstates a winter on lean; no build on file carries a measured rate
by a property of a third party's delivery.

## Survivor anatomy

Actor: how a low-NOx burner's NOx rate moves with the heat content of the gas it fires has no column in any file; it exists only as the relation between each source test's month, the heat content the utility reported for the burner's BTU area that month, and the monitored Lindqvist boiler's hourly NOx rate against the utility's monthly table.
Link: each test is set against its area's heat content in its month through Appendix A's BTU area and the utility's published table, two organisations' records with no shared key, and the monitored boiler's CEMS rate against that table is a comparison the inventory method never asks for, since the method carries a test's rate across the year.
Reflex: the field's inventory method, each unmonitored burner's latest source test carried across its 2026 heat input (with every filed rule applied), is rung 0 and files Tamsett State University fifth at 8 tons against Merriwell Foods' 7; the mean of each burner's tests files the same five (R3a, asserted on the clean truth).
Back-test: the textbook route validates: the monitored units' NOx is the sum of their hourly mass as the guidance files it, every unmonitored burner's latest test passes its permit limit, and carrying a passing test across the year is the guidance's own section 3 read plainly; nothing in the pack scores the carried rates against a measured year.
Second use: every file the step reads is in the pack for its own reason: the utility's heat content table converts the statements' MMSCF to MMBtu (guidance section 4), the CEMS export carries the monitored units' NOx, the two test databases the unmonitored units' rates, Appendix A each facility's BTU area.
Shock: nothing reads as an anomaly: the Westside heat content swings month to month with the gas plant's ethane recovery, Merriwell Foods' August test sits on lean gas like other summer tests, and no facility's 2026 total stands out on a sort of the default path's figures.
Pins: the plan's 2.1 and 2.2 and the guidance's sections 2 to 6 file the WHAT (NOx as NO2, the Rule 4306 units, local standard time, substitute hours, heat input, Method 19, the engines' factor); no filed sentence names a heat content effect on NOx, a burner's air metering or carrying a rate from its test month, and the counter-pins in `checks.py` assert none does.

## Readability screen
| Rung | What it takes | Verdict |
|---|---|---|
| 1 Monitored units | each 2026 CEMS hour's nox_mass_lb summed, joined to its device through the permit list's FAC_NO and CEMS_UNIT_ID (guidance section 2) | readable |
| 2 Tests on one basis | the newer database's lb/MMBtu; the older one's NOX_PPMVD at 3 per cent oxygen through Method 19, or its NOX_LB_HR over the rating times the load (guidance section 5) | readable |
| 3 Heat input | the statements' therms, MMBtu and MMSCF at the utility's heat content for the facility's BTU area and month (guidance section 4) | readable |
| 4 The rise with heat content (decisive) | the monitored Lindqvist power boiler's measured hourly rate set against its BTU area's heat content by month, or the burners' tests against the heat content of their months, fitted in the log | silent |
| 5 The year carried | each burner's tests carried from their months' heat content to each 2026 month's, each month's heat input at that month's rate | silent |

Rung 4 is silent: no file holds a unit's 2026 rate or a sensitivity, no column or sentence ties a burner's NOx to the
gas's heat content, the heat content table is read on the default path only to convert MMscf (all four 2026 MMscf
reporters are Eastside, where it holds at 1.033 to 1.038), and the guidance's "its NOx emission rate in lb/MMBtu"
reads, on the default path, as the latest test's figure. Rungs 1 to 3 are conversions the guidance files and every
route takes them.

## Semantic fork table

| ID | Term or convention | Alternative reading | Ruled out by |
|---|---|---|---|
| SF1 | NOx | NOx as NO and not NO2 | plan 2.1 "expressed as NO2"; the newer database's lb/MMBtu is Method 19's NO2 figure from its ppm (checks.py SF1) |
| SF2 | a facility's units | its emergency engines or Rule 4307 units added | plan 2.2 names the Rule 4306 units; with the engines added the five stands; the Rule 4307 units have no fuel record (SF2) |
| SF3 | calendar 2026 | the CEMS hours read as UTC | guidance section 2, local standard time; same call and 14 whole tons on UTC (R2c, SF3) |
| SF4 | a monitored unit's NOx | substitute data hours left out | guidance section 2 counts them; same call without them (R2d, SF4) |
| SF5 | heat input | MMscf at a fixed 1,020 Btu/scf | guidance section 4, the area's monthly heat content; same call and 14 whole tons at 1,020 (R2b, SF5) |
| SF6 | a test's lb/MMBtu | the older tests from lb/hr over rating times load, not Method 19 from ppm | guidance section 5 gives both as equal; same 14 whole tons (R2a, SF6) |
| SF7 | the heat content's month | the month after the gas, as a billing month | guidance section 4 (section 7 until the 10-31 reship): the average heat content of the gas delivered in the month; the boiler's fit falls from 6.01 to 4.65 on the lag (SF7) |
| SF8 | the heat content's unit | Btu/scf to the whole Btu, not therms a CCF | same 14 whole tons (SF8) |
| SF9 | the year's NOx | the year's fuel at the mean of the months' rates | guidance section 3, the NOx emitted over the year's operation, month by month at each month's rate; the five stands either way (SF9) |
| SF10 | the facility of a device | Haskett Ridge's rows under 0705 as another facility | the permit list's device numbers carry every test and statement row (R2e, SF10) |
| SF11 | whole tons | half to even, not half up | no figure within 0.297 tons of a half under any standing construction (G3, SF11) |
| SF12 | the five | a tie for fifth | fifth clears sixth by 14.3 per cent or more under every standing construction (G4, SF12) |
| SF13 | the call's inputs | a billing line, log, inspection or event moving the call | the call and the 14 whole tons from the CEMS, tests, statements, heat content and permit list alone (SF13) |
| SF14 | the rise's form | a power of the heat content, not an exponential | same 14 whole tons (SF14) |
| SF15 | the rise's source | the monitored boiler's monthly means or the burners' tests, not its hours | same 14 whole tons (G2, SF15) |
| SF16 | a read period's days | the day after the prior read through the current read | plan 4.2: from the day of the prior read to the day before the current read (SF16) |
| SF17 | MMBtu | therms at another ratio | guidance section 4, therms divided by 10 (SF17) |
| SF18 | a line's facility | an address read to two facilities | each service address matches one Appendix A address (SF18) |
| SF19 | a corrected CCF line's therms | rounded to the whole therm, not kept unrounded | same 14 whole MMBtu (SF19) |
| SF20 | an engine's hours | the hour meters' advance, not the logs | guidance section 6, the time it ran; the meters also count warm-up and cool-down (SF20) |
| SF21 | grams a pound | 453.59237 | guidance section 6 writes 453.6 (SF21) |
| SF22 | the engine a run is charged to | a run on a replacement day | no replaced engine runs on its replacement date or in the four days before (SF22) |
| SF23 | a banked engine's outage line | halved, not set at the outage's hours | same 14 whole pounds (SF23) |
| SF24 | an estimated read | trued up against a later read | each estimated meter's next read is actual and the extract carries no adjustment line (SF24) |
| SF25 | the rise's grouping | the low-NOx burners' own rise apart from the ultra-low NOx burners' | the low-NOx class's own tests give 6.04 (se 1.53) against 6.13 and the monitor's 6.01; same five and 14 whole tons (SF25) |
| SF26 | the rise's grouping | each facility's own rise from its own tests | Merriwell Foods' tests all sit on lean August gas, so its own rise is unidentified (se 3.23) and a fit pools; with each facility's own rise where its tests identify it, same five and 14 whole tons (SF26) |
| SF27 | the billing conversion's boundary | the bill date in place of the read date | no line read before 1 July 2026 was billed on or after it, so both boundaries split the extract alike (SF27) |
| SF28 | the logs' "Run hours" | decimal hours | no entry's fraction reaches .60 in 1,557 entries, and the hour meters agree with hours and minutes at every engine (SF28, B fair) |

## Ladder

| Rung | Route | Five | Fifth over sixth |
|---|---|---|---|
| L0 | each burner's latest test across its 2026 heat input (the default path) | Ashgrove, Lindqvist, Sedge Hollow, Tamsett State, Valmora | 1.159 |
| L1 | the mean, median or last two of each burner's tests | the same five | 1.071 to 1.148 |
| L1 | each burner's highest test | the same five | 1.165 |
| L1 | each burner at its permit limit | the same five | 1.054 |
| L1 | each burner's tests trended on the calendar to mid-2026 | the same five | 1.138 |
| L2 | the monitored boiler's 2026 months as an index on each latest test, Westside or every burner | the same five | 1.047 |
| L3 | the permit limit where a burner's last test predates 2026 | Ashgrove, Haskett Ridge, Lindqvist, Merriwell, Sedge Hollow | 1.058 |
| L4 | each burner's tests carried from their months' heat content to each 2026 month's by the monitored boiler's rise (the golden) | Ashgrove, Lindqvist, Merriwell, Sedge Hollow, Valmora | 1.163 |

Every route short of L4 keeps Tamsett State University in the five or puts Haskett Ridge in (checks.py L0 to L3). L2 is
the near miss: the monitored boiler's 2026 months do carry the season, but Merriwell's latest tests were read in August
2025 on lean gas and the index reads them against August 2026's rich gas, so Merriwell falls further (6.59 tons). A
response that carries the tests by heat content but applies the mean of the months' factors to the year's fuel (SF9)
still files the golden five, Merriwell at 8 tons in place of 9. The standing family (G2) files L4's five and 14 whole
tons under every member.

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | the 38 Rule 4306 devices at the fourteen Appendix A facilities (plan 2.2, the permit list's RULE column; SF2) |
| 2 | Unit of account | the facility, the sum of its units; for the asks the facility's meters and its emergency engines |
| 3 | Attribution window | calendar 2026 in local standard time (SF3); the gas by the days of each read period inside 2026 (SF16) |
| 4 | As-of dating | the extracts of 5 to 16 February 2027; the plan of 19 February 2027 |
| 5 | Version basis | the permit list as permitted in February 2027, devices keyed by number across owners (SF10, SF22) |
| 6 | Denominator | none; tons, MMBtu and pounds are totals |
| 7 | Weighting | each 2026 month's heat input at that month's rate (SF9); each unit's level from all its tests, each once |
| 8 | Window length | one calendar year |
| 9 | Boundary inclusivity | a read period from its prior read's day to the day before its current read (plan 4.2) |
| 10 | Rounding path | half up from the unrounded figure: whole tons, whole MMBtu, whole pounds (SF11, SF19) |
| 11 | Tie-break | none needed (SF12) |
| 12 | Maturity and censoring | 2026 closed; Valmora's B-2 test deferred from April to June 2026 for a turnaround, in the newer database |
| 13 | Order of operations | conform the tests and statements, fit the rise, carry each burner's tests to each 2026 month, sum by facility, rank |
| 14 | Row order | none |
| 15 | Duplicate resolution | none in the call's files; a combined account's usage once a period (ask A) |
| 16 | Identity normalisation | devices with and without their D- prefix, facility numbers with and without leading zeros, 0705 to 0912 |
| 17 | Netting | none |
| 18 | Dimensional units | ppmvd at 3 per cent oxygen, lb/hr, lb/MMBtu; therms, MMscf, MMBtu; therms a CCF and Btu/scf; hours and minutes |
| 19 | Code and status semantics | substitute data code 12 counted (SF4); READ_TYPE E stands as billed (SF24); never the stump |
| 20 | Integerisation | whole tons, MMBtu and pounds |
| 21 | Clause scope | plan 2 governs the call, 4.2 the gas, 4.3 and guidance 6 the engines |
| 22 | Forward window contents | the 2027 agreements, signed by 1 April 2027, with the five |

## Literal reader

A literal reader executes plan 2.1 and 2.2 over the permit list's Rule 4306 devices and the guidance's sections 2 to
5: sums the monitored hours, puts every test on lb/MMBtu and every statement on MMBtu, and computes each unmonitored
unit's "NOx it emitted over the year's operation ... from its heat input and its NOx emission rate". Nothing filed
names that rate, so the literal reading is an estimate of the rate each month's fuel burned at, and the data decide it:
each burner's tests rise and fall with the heat content of their months' gas, as the monitored boiler of the same
burner does hour by hour, so a test-day figure is a reading of one month's gas, and every construction the data leave
standing files the golden's five and its 14 whole tons (G2). The gas and engine asks execute plan 4.2 and guidance
section 6 word for word, with the billed usage read in the unit the utility billed it, each combined account's usage
once, the log read in the unit its logbook wrote it, and each run at the engine then installed.

## Oracles

- The main call has none: no shipped figure states a facility's or unit's 2026 NOx, a unit's rate for the year or a
  sensitivity, and the CEMS mass, the tests and the heat content are each system's own readings, so nothing ties under
  one route only.
- Ask A: the plan units' own fuel in the emission statements arbitrates the unit of the billed usage (read as labelled,
  the bills fall below the units' fuel on 45 of 62 periods read before July 2026 and on none of 82 after) without
  handing over a level; the combined accounts show by their meters carrying identical usage every period.
- Ask B: the hour meters arbitrate the log's unit (read as hours and minutes, every engine's meter runs 0.06 to 0.07
  hours a start beyond its log over the first inspection interval, the warm-up and cool-down; read as decimal hours,
  0.23 to 0.26) without handing over a figure; the compliance log's OUTAGE entries give each outage's whole hours,
  which the banked engines' emergency lines double; the replaced engines' meters are first read after the
  replacement, so only the EQUIPMENT entries carry the old engines.

## Ask sheet

Two asks, both on rows the call never reads (X1, X3): the plan's community tables beside each facility.

- **Ask A, the gas Tamsett Valley Gas delivered in calendar 2026, whole MMBtu (14 figures).** User: the plan's fuel
  balance (plan 4.2). Devices: D2 a label stored before a silent switch (USAGE_THERMS holds corrected CCF on the lines
  read before 1 July 2026, the utility's billing conversion, and therms from the July reads; the plan units' fuel in the
  statements shows it), and D6 an account's quantity on every line it covers (the five combined-billing accounts' usage
  repeated on each of their meters' lines). Rungs: every line as labelled moves 14 of 14; as labelled with the combined
  usage once 14; every line CCF times its factor 14; the conversion handled, every line summed, 5; each bill in its
  current read's year 14.
- **Ask B, the emergency standby engines' 2026 NOx, whole pounds (14 figures).** User: the plan's community table
  (plan 4.3, guidance section 6). Devices: D3 hours and minutes in the "Run hours" column at every facility (the
  District's e-logbook writes 0.30 for half an hour; no entry's fraction reaches .60, where the same runs in decimal
  hours would show one on about a fifth of entries, and the hour meters run 0.06 to 0.07 hours a start beyond the logs
  read that way against 0.23 to 0.26 read as decimal hours); D6 the banked engines' emergency lines at four facilities
  carrying the bank's engine-hours (twice the outage the compliance log records); and D2 an attribute at the wrong
  vintage at two (an engine replaced in 2026 under the same device number, the permit list showing the new engine, the
  EQUIPMENT entry the old one's rating and tier). The decimal reading moves all 14 figures, the bank lines 4, the
  current engine 2. The outages are whole hours, so no outage entry reads differently either way.

| Ask | What the cracker does | Cracker |
|---|---|---|
| A | USAGE_THERMS as the dictionary names it (the usage billed), each combined account's repeated usage once, spread by plan 4.2 | miss |
| B | the logs as decimal hours, the bank lines at the compliance log's outage hours, each replaced engine's earlier runs at the old engine (guidance section 6, as both round 1 readers did) | miss |

Pair ceiling: 28.5 (cracker 45.0 on the call with 0 of 28 ask figures, mirror 12.0 off it with 0 of 28; a response that
reconciles the billed usage against the plan units' fuel keeps 14 of 28, for a pair of 56.0 with one on the call).

Mirror leakage: 0.0 per cent of ask weight.

Measured by: generator/ceiling.py on the cut pack.

Measured at stage 4 (score_reader.py): round 1 (zip 2936a1ef) gas 0 of 5 for both readers, engines 4 of 5 and 5 of 5,
so ask B was re-sited (Tried and rejected); round 2 (zip 77f6a96a) both readers 0 of 14 gas and 0 of 14 engines, 11 of
42 deliverable figures each, every hit a ton the default path keeps at a facility the heat content does not move.

## Pre-ship check

1. Domain: stationary-source inventory practice's own estimate of an unmonitored low-NOx burner's year from its source
   tests, read on the heat content of each month's gas; with another field's nouns there is no burner air-fuel ratio,
   no supplied heating value and no test day to carry.
2. Real work, nothing planted: every Layer 1 item is what the district's, the facilities' or the utility's systems
   write (two test databases, oxygen bases, fuel units, the monitoring plan's ids, the renumbered facility, the deferred
   test); none is on the decisive step (checks.py R2a to R2f), and every test passed its limit.
3. The step that flips the call is analytical: estimating the rise of a burner's NOx with heat content and carrying
   each burner's tests to each 2026 month's gas; no clause makes the choice (the guidance files the NOx emitted over the
   year, not how a test becomes it).
4. Analyst test: every field and rule read correctly, the latest test files the default five (asserted on the clean
   truth, R3a, and on the pack, L0); the decisive step alone files the golden on the clean truth (R3b).
5. The plan files the estimand (the Rule 4306 units, NOx, calendar 2026, tons by facility, the five) and the guidance
   the year's NOx from heat input and rate; the thirty standing constructions file the golden five and the same 14 whole
   tons (G2), the rise by burner class and by facility where identified files them too (SF25, SF26), and the asks'
   conventions are filed in plan 4.2 and guidance sections 4 and 6 or closed by the data (SF16 to SF24, SF27, SF28).
6. No decoy, no withheld rule against a stated one, no certified replay.
7. The lesson is on no other card: nearest drivers 0.06 (task85 v2.5, task196 v1, task229 v3, task480 v1); this
   slot's architecture 6 at 0.33, differentiated.
8. Re-read against the built pack at stage 4: four isolated readers over two rounds filed the default five, none
   joined a burner's tests or the monitored boiler's hours to the heat content, and each answered question 1 "none".
9. Judge pass 1 (zip 2936a1ef) DETERMINISTIC, FIX_NOW on Wexley Point's log cut-over, the gas conversion's read-to
   boundary, the rise's basis and two fork rows (fixed: logs in hours and minutes all year, the June reads moved off the
   month's last days, SF27 and SF28 asserted, step 5 names READ_TO); pass 2 (zip 77f6a96a) DETERMINISTIC, APPROVE, Gate G
   method_or_model_selection and analytical_non_defect, Gate H domain pass, layers pass, decisive step analytical, the
   five stable for any rise from about 4 to 8. Its optional pin (a month's rate is the rate at that month's delivered
   gas, in guidance section 3) declined: it names the decisive step's object and leans the call easier.

## Architecture 6 record (spent 2026-10-23)

Architecture 6 named the five facilities whose Rule 4306 units emitted the most NOx in 2026 with each unmonitored
unit's source tests carried along its SCR catalyst's operating hours by one climb fitted on the units' test histories.
Round 1 (zip md5 946c7506): reader A plotted the tests against operating hours since each unit's last catalyst event,
found the climb and landed the call, and kept all 14 gas figures; reader B carried each test forward from its test date
and missed the call, and kept all 14 engine figures. The judge (thread on the agent's brief) returned DETERMINISTIC
with a FIX_NOW on a placeholder in the guidance's file dictionary (determinism_check_report_v6.md). A call any reader
lands is spent, so the architecture is spent.

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

- Ask B's hours-and-minutes log switched mid-2026 at seven facilities (2026-10-23, stage 4 round 1): reader v7b read
  the switch off the weekly readiness runs, which dropped from 0.40 to 0.60 to 0.24 to 0.36 at each facility's first
  e-logbook entry, and off an outage logged 14.30 against the compliance log's 14.5 hours, and kept every engine figure
  it reported; reader v7a missed it. A switch inside the year is a step any reader who plots the weekly runs sees, and
  a fractional outage is an oracle for the unit. Re-sited to hours and minutes all year at every facility with
  whole-hour outages, the meters the arbiter.
- Architecture 7 draw (2026-10-23): re-rooted on the author's standing rule (no retirement); the lesson of
  architecture 6 taken first (a relation the units' own measurements show against a clock the pack builds is a fit a
  strong reader makes), so the rate here follows a property of a third party's delivery that nothing at the unit
  records and no maintenance log suggests. Screened before it and dead: low-load SCR dropout from a monitored unit's
  low-load hours (the minimum injection temperature is common knowledge, and a seasonal processor's low winter fuel
  invites it); cold starts before the catalyst warms (task273's screen); a reagent mass balance from the urea
  deliveries (the delivery file announces what it is for); the combustion air's density with the season (a seasonal
  index from the monitored units lands it); operators tuning before a test, read from portable-analyzer checks (two
  measurements of one unit, a reader's pick); a CHP engine's fuel split from the electric utility's output (the
  part-load heat rate forks it); a dairy lagoon's volatile solids carried across its emptying dates (either a filed
  method or a kinetic fork); line-haul fuel by gross ton-miles against grade (a train-resistance model forks it);
  Tier 4 standby generators whose SCR never warms on light-load test runs (the run log shows the load, and the
  monitored sets show the step); fumigant VOC by application method (filed adjustment factors, rule application).
- 2026-10-23, architecture 6 spent at stage 4 round 1 (zip md5 946c7506): reader A built each unit's operating hours
  since its last SCR INSTALLED or CATALYST entry from the statements and the compliance log, saw its test rates fall on a
  clean exponential in those hours (about 5 per cent scatter), fitted one shared climb (4.8e-5 an hour) with a level for
  each unit and filed the golden five; it read the July billing switch on every meter (usage over the BTU factor runs on
  across it) and kept 14 of 14 gas figures, and the replaced engines (7 of 14 engine figures). Reader B carried each
  test forward from its test date and filed the default five, but read the hours-and-minutes sheets off their "Hours"
  header and the replacements off the log (14 of 14 engine figures) and found the switch on the index meters only (3 of
  14). A rate that moves with an exposure clock the pack carries is found by plotting a unit's own repeated
  measurements against that clock: a clean structure the measurements display is a fit a strong reader makes, so the
  next architecture's decisive step cannot be a relation the field's own measurements show when plotted.
- 2026-10-23, architecture 6 build: the gas ask's switch was bypassed by the meter index (read difference times
  multiplier times BTU factor files every figure without meeting the switch); the elevated-pressure meters now bill on
  volume correctors and show no multiplier, and plan 4.2 files the billed usage (SF14), so the index lands 5 of 14.
- 2026-10-23, architecture 6 build: the engines' hour meters tied the logs exactly under the hours-and-minutes reading
  (an oracle handing over the level) and restarted at each replacement; the meters now run through each start's warm-up
  and cool-down and the replaced engines are first read after their replacement (checks.py B).
- 2026-10-23, architecture 6 build: source tests over their limits drew no notice and no corrective work (Merriwell's
  boilers failed three years running on a 2017 catalyst); every failed test now brings a notice of violation, a
  corrective catalyst where none was due and a retest, the boiler limit is 9 ppm, and Merriwell, Orchard Basin and
  Penrose were resized off rounding halves (G3).
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
- 2026-10-31, re-check under the 10-30 gates: `leak.py` LEAK on the inventory guidance's section 7 (a file-by-file data dictionary inside the governing document: columns, codes, units and row counts). Section 7 removed; its one closure (SF7, the heat content is the gas delivered in the month) moved into section 4's own sentence on heat input, and the rest is in the files (the reference oxygen in every test file's columns, the compliance log's dates readable as written: month first before 2021, ISO after). The newer test database's Field notes sheet dropped for the same reason. The prompt drops its counts and asks who. Every graded figure unchanged (118 checks).

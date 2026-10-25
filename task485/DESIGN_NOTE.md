# task485 design note: the Ammonia Reduction Programme's 2027 Ammonia Action Regions from a herd that moves with the seasons (architecture 2)

Status lives in `pipeline.json`; this note holds the design. Architecture 2, drawn 2026-10-25 on the author's standing
rule (no retirement) after architecture 1 (an electoral review's 2032 electorate, a new dwelling's electors joining the
register over its first canvasses) was spent at stage 4 when both scored readers fitted the ramp. A fresh world and
mechanism on the lane's objective; the candidates screened before it are in `## Tried and rejected`. The slot's seed
(ET42) was set aside at the first draw and stays set aside.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task485.json` (architecture v2, lineage v1 spent). The window the axis bans
  read (task121, task303 and task301, the live cards filed last; task485's own v1 card is spent and skipped) closes the
  strategies decomposition_attribution, composition_mix and population_selection, the forums committee_or_panel,
  board_of_directors and executive_team, the forcing events statutory_or_regulatory_filing, launch_or_rollout and
  budget_or_appropriation, the organisations utility_or_infrastructure, financial_institution and foundation_or_funder,
  the roles compliance_or_audit, portfolio_manager and research_desk, the context artifacts published_series, other and
  register, and the shapes 03 and other. The draw's honest labels clear all of them: the Minister designates the
  regions (minister_or_cabinet) for the spreading season that opens in January (season_or_peak), the Ministry is the
  organisation (government_agency), the requester heads the Ministry's Ammonia Programme Unit (programme_officer),
  and the stakeholder's own file is the programme's designation rules (filed_standard).
- **BLOCKs differentiated on the card** (similarity rules only, never an axis): `test.same_puzzle_older` and
  `test.same_driver_older` (population, pattern D, designation_set and etl_conformance) against task181 v4 (crossings of
  moving units), task229 v1 (a shared-node standard error), task98 v3 (units chained by distance) and task70 v1 (a
  per-record date rebuilt from a movement log). None places a unit's days across places by a seasonal stage.
- **WARNs answered.** `three_rules.strategy_risk` (grain_or_unit): the analyst test below is a route that reads every
  field and rule correctly and still files the wrong regions, because the census counts every animal correctly and the
  factor is right for an animal that stays put. `overuse.org_family` (government_agency in 40 builds): the programme is
  the Ministry's and the Minister designates under it; no other body decides a region's measures. `repeat.deliverables`
  (png and xlsx): a scorecard against a line reads at a glance as a bar chart, and the workbook carries the regional
  figures and the asks' tables. `repeat.question_form` (which): the Minister names the regions, so the question asks
  which.
- **Pairing:** Physical & Environmental Sciences / `emissions-inventory`, drawn for Data Extraction & Conformation
  (ETL). The deliverable is the conformed 2025-26 regional inventory of ammonia from cattle manure, built from the
  National Bovine Register's two exports (one row per animal, one row per movement), the statistics office's June
  livestock census by holding, the herd register, the land parcel register's farmed area, the farm practices survey's
  housing seasons by region and the national inventory's ammonia factors for cattle.
- **The decision and the quantity:** an unnamed Atlantic country runs an Ammonia Reduction Programme for 2025 to 2030.
  Each autumn the Minister designates Ammonia Action Regions for the next spreading season: a region whose ammonia from
  cattle manure over the programme year (1 November to 31 October) is at or above the programme's line in kilograms of
  ammonia per hectare of its farmed land is designated, and in a designated region every farm above the programme's
  stocking threshold must spread slurry by low-emission equipment and cover its slurry store from 13 January 2027, when
  the closed period ends. The Minister designates by 1 December 2026 on the Ammonia Programme Unit's figures for the
  programme year 2025-26. Twelve regions; the line and the regions' farmed areas are set at stage 2.
- **Timing (the pack's present is November 2026).** The bovine register's exports of 9 November 2026 cover every animal
  present at any time from 1 November 2025 to 31 October 2026 and every movement in that span; the census holds each
  holding's cattle on 1 June 2026 and was published in September 2026; the inventory methodology is the 2025 edition;
  the farm practices survey's housing seasons are from its 2025 round. The call is retrospective by design: the
  programme designates on the emission year just closed, so the measures reach the next spreading season.
- **Shape:** `10`, a scorecard against thresholds: each region's cattle-manure ammonia per hectare against the line
  beside the call, with asks of many figures on the register's own conformation.
- **The default path holds the field's method (stumping 1.1b).** The inventory's Tier 2 factor per head is built the
  field's way, from nitrogen excretion by category and the share lost at each stage (housing, storage, spreading,
  grazing), with a region's housing season setting the housed and grass days. Multiply each region's census cattle by
  category by the region's annual factor per head, divide by farmed area and test the line. That is how the national
  inventory states its regional table, and the route an inventory compiler builds first.
- **The decisive step:** the annual factor per head is right for an animal kept in one region all year, housed in that
  region's season and at grass outside it. A large share of the herd is not. Lowland dairy farms send their yearling
  heifers out on summer grazing lets in the grassland and western regions in May and house them at home from October;
  western rearers buy the dairy regions' calves in spring; and the finishers of Midland Basin, Inner Basin and Lower Basin buy
  stores in the autumn, house them all winter and send them to slaughter before June. The census counts the summer
  grazers and the spring calves where they are on 1 June and never sees the winter stores, so the annual factor hands
  the grassland and western regions a housed season they do not have and takes one from the finishing regions. Placing
  each animal-day in the region where the animal is that day, at the housed rate inside that region's housing season and
  the grass rate outside it, from the register's movement histories, takes the grassland and western regions under the
  line and puts Inner Basin and Lower Basin over it. Averaging the register's count over the year moves the days but not the
  season: it still files Lake Uplands, Middle Uplands and Western Seaboard over the line, because their summer grazers' housed-season
  ammonia arises where they winter.
- **Data-native sentence (restated from the generator):** the census route puts the five grassland and western
  regions' cattle ammonia 42 to 51 per cent above what their animal-days give and the three finishing regions' 13 to 16
  per cent below; the mean of the register's count over the year still puts the grassland and western regions 15 to 20
  per cent above; the three routes file three different sets of regions.
- **People:** drawn with `guard.py names --geo ie --seed 485` (Gary Farnon, Tiegan Ferry, Emily McAleer, Anna McKenna,
  Eimhear Rhattigan, Kerri Cunneen, Aislinn Mullane, Graham Mansfield, Noel Herity, Pearce Delaney): Emily McAleer,
  head of the Ministry's Ammonia Programme Unit and requester; Noel Herity, the National Bovine Register's data
  manager, who supplied the exports. Owners in file properties and sign-offs only.

## Three rules

Task type: Physical & Environmental Sciences, emissions-inventory, which serves ETL in the taxonomy (a regional inventory conformed from the bovine register's animal and movement exports, the June census by holding, the herd and land parcel registers, the housing seasons and the inventory's factors).
Domain test: the quantity that decides is each region's ammonia from cattle manure over the programme year per hectare of farmed land; the field estimates it by the inventory's mass-flow stages (housing, storage, spreading, grazing) on activity data, and for a herd that moves with the seasons the activity data are animal-days by region and stage rebuilt from the movement register, not the census day times the region's factor per head.
Swap: "which of 12 health boards' hospital infections per 1,000 bed-days exceed the line" (patients for cattle, bed-days for animal-days) leaves nothing to place: a patient's day carries no rate set by the season and the ward it falls in, so the census day stands for the year and the step has nothing to act on.
Layer 1: the register in two exports (one row per animal with birth and exit dates, one row per movement with departure and arrival dates that can differ by a day), marts and dealers' premises as intermediate herds on many moves, herd numbers reissued when a holding changes hands and farmers keeping more than one herd number, the herd register's region codes revised in 2024 with the census still on the old codes, the census keyed by the statistics office's farm number and joined to herd numbers through the herd register, census categories against the categories the register implies from sex, breed, age and calving, the factor note's mass flow in kilograms of ammonia-nitrogen beside its per-day factors and the programme's line in kilograms of ammonia, day-month-year dates in the register and ISO dates elsewhere, the programme year from November to October against the census's June date, farmed area by herd with commonage shares split across herds, and, on the ask's side, three slurry contractors' exports in three units with herd numbers written two ways; each written by the system that holds it, none placed to be caught, each asserted neutral on the call (R2).
Layer 2: field_method, exposure windows: the activity data an inventory multiplies by its factors are the animal-days in each stage in each place; the choice that flips the call is rebuilding them by region and housing stage from the movement histories rather than taking the census day times the region's annual factor, or an average count times it.
Decisive step: recognising that the inventory's annual factor per head holds only for an animal kept in one region all year, and placing each animal-day in the region where the animal is that day, at the housed rate inside that region's housing season and the grass rate outside it, from the bovine register's movement histories.
Not semantics: with every field read correctly (herd numbers across both exports and the census's farm numbers, the 2024 region codes, the categories, ammonia-nitrogen against ammonia, the programme year), the census route still files the wrong regions, because the census counts every animal correctly on 1 June and the annual factor is correct for an animal that stays put; no field records that an animal's housed season falls in another region, and the register's 1 June stock agrees with the census.
Not rule application: no filed rule places an animal's days by region and stage; the factor note's Table 5 states the annual factor for an animal kept in one region and the census counts every holding's cattle on 1 June, and executing the two files the wrong set. Measured on the generator's clean truth, the enumerated family (the census times Table 5; the register's 1 June stock times it; the register's mean count over the year times it; animal-days at each location's housing season; animal-days at the home region's housing season) files three distinct designated sets of the twelve regions (the census and the register's stock file the same nine), and the standing family (animal-days at the season of the region the animal is in, or at its home region's season, the two members the estimand and the closure sentence leave defensible) files one, a spread of zero, the home-season member moving Western Seaboard and Atlantic Coast by 5.7 and 6.5 per cent with no region across the line; the easy route sits outside that family because the register refutes it, so unanimity is the cell the build wants (stumping 1.1), and what rules the easy route out is quiet: the register's 1 June stock agrees with the census, and the seasonal flows show only when the moves are aggregated by month and region against the census day; no column or summary states them.
Analyst test: a strong analyst conforms the 1 June 2026 census holdings to the 2024 regions, applies the factor note's annual ammonia factor per head by category and region (Table 5), divides by each region's farmed land and designates the regions at or over the line, filing nine regions: it adds Lake Uplands, Middle Uplands, Eastern Uplands, Western Seaboard and Atlantic Coast, whose June herds hold summer grazers and spring-bought calves, and misses Inner Basin and Lower Basin, whose finishers house stores all winter and send them to slaughter before June (the default path's `Ends on:`).
Estimand: each region's ammonia from cattle manure arising in the region from 1 November 2025 to 31 October 2026, in kilograms of ammonia per hectare of the region's farmed land, against the programme's line; filed in the programme's designation rules, with each stage's emissions arising where the animal is on the day, as the inventory methodology's mass-flow states it.
No decoy: nothing is planted to be caught: the census counts who it counts on 1 June, the register records every move as the herds and marts report it, the methodology's factors are correct for an animal kept in one region, and no memo, draft, briefing or stakeholder figure argues the census route.
No certified replay: the method is not recovered by reproducing published figures; the census tables and the inventory's national total are context, and the national total is the same under every route to within a few per cent, so no published figure separates the routes.
Lesson: a regional inventory of a herd that moves with the seasons has to place each day's emissions where the animal is that day and at the rate of the stage it is in there; the census day hands a whole year's housed-season ammonia to the region where the summer grazing is, and an average of the animals present still leaves the housed season with the region the animal grazes in; no build on file teaches it (the card's nearest drivers sit at 0.07 and below, and no slot note screens a herd's seasonal movements).

## Layer 1 inventory

Each item is written by the system that holds it, none is placed to be caught, and each is asserted in `checks.py`
(R2): the golden method run with the item mishandled files the same six regions, or the item moves only the census
route or the ask. The register's readings are asserted together, as a cross product of 288 readings (transit, premises,
exit day, presence, region map, commonage), and every one files the golden six.

| Item | System that writes it | File | Natural mishandling | Effect on the call |
|---|---|---|---|---|
| departure and arrival dates that differ by a day | hauliers' overnight loads, recorded at both ends | movements | the animal in the arrival herd from the departure date | same six (cross product) |
| marts, dealers' premises and export assembly centres as herds | the register records each leg | movements, herd register | their days dropped, or counted at the seller | same six (cross product) |
| herd numbers reissued after a holding changed hands | the register's herd allocation | herd register (a row per holder, with validity dates) | the number's first row (the earlier holder's region) | same six (cross product) |
| farmers keeping a second herd number on an out-farm | the register's herd allocation; the census asks per farm | herd register (main herd number), census | the census farm placed in one herd's region | the census route only (an out-farm sits in its main herd's district) |
| region codes revised in 2024 (three Coastal Vale districts to Southern Vale, their herds keeping L numbers) | the Ministry's reorganisation; the census keeps the old codes | herd register (both codes), census | the pre-2024 codes, or a herd's region read from its number's letter | same six (cross product) |
| census farm numbers written without their leading zeros | the census frame's export | census, herd register | a raw join | loud: the raw join matches no farm |
| census categories against the register's sex, breed, age and calving | two classifications | census, animals | categories mapped by hand | the census route only |
| day-month-year dates in the register, ISO elsewhere | the register's export format | animals, movements | month and day swapped | loud: most birth dates have a day after the twelfth |
| births registered up to 27 days late | farmers' registration window | animals (birth and registration dates) | presence from registration | same six (cross product) |
| the exit date | the plant, knackery or export centre recording the exit | animals | the exit day counted | same six (cross product) |
| commonage parcels shared across herds | the land parcel register's declarations | `lpr_farmed_area_2026.csv` | a parcel's whole area on each sharing herd, or commonage left out | same six (cross product; commonage sits only in Eastern Uplands and Atlantic Coast, more than 22 per cent under the line) |
| the factor note's mass flow in kilograms of ammonia-nitrogen beside its factors in kilograms of ammonia | the inventory's method | `epo_cattle_ammonia_factors_2025.pdf` | Table 3 converted to ammonia a second time | not invited: Table 3 and the line are both in kilograms of ammonia, and the note applies its rates as printed |
| Countrywide's herd numbers written with a space | the contractor's account system | `countrywide_invoice_lines_2026.xlsx` | a raw join | the ask only, loud (no line matches) |
| three units across the contractors (loads at each tanker's gallons, thousands of gallons, metered cubic metres) | each contractor's own system | the three contractor exports | Vale Agri's loads at a standard 2,000 gallons | the ask only |
| pig slurry and digestate jobs beside cattle slurry, jobs into May | the contractors' job systems | the three contractor exports | kept | the ask only |

## Default path

1. Conform the 1 June 2026 census holdings to the 2024 regions through the herd register's farm numbers, and map the
   census's categories to the factor note's five (dairy cows, suckler cows, other cattle over two years, cattle one to
   two years, calves).
2. Multiply each region's census cattle by category by the note's annual factor per head for that category and region
   (Table 5, the per-day rates over the region's housed and grass days in a 365-day year).
3. Divide each region's tonnes by its farmed land in the land parcel register (2026, the 2024 regions, commonage shares
   included) and designate every region at or above the programme's 26 kilograms of ammonia a hectare.

Ends on: Northern Vale, Eastern Vale, Southern Vale, Midland Basin, Lake Uplands, Middle Uplands, Eastern Uplands, Western Seaboard and Atlantic Coast
(nine regions).

Golden: Northern Vale, Eastern Vale, Southern Vale, Midland Basin, Inner Basin and Lower Basin (six regions).

## Stump sentence

The default path multiplies each region's 1 June 2026 census by the factor note's annual factor per head and divides by farmed land, designating nine regions: it adds Lake Uplands, Middle Uplands, Eastern Uplands, Western Seaboard and Atlantic Coast, whose June herds hold lowland yearlings out on summer grazing lets and calves bought from dairy farms that spring, and it misses Inner Basin and Lower Basin, whose finishing units house stores all winter and send them to slaughter before June; averaging the bovine register's count over the year still adds Lake Uplands, Middle Uplands and Western Seaboard, because the annual factor's housed days never happen there; placing each animal-day in the region where the animal is that day, at the housed rate inside that region's housing season and the grass rate outside it, designates Northern Vale, Eastern Vale, Southern Vale, Midland Basin, Inner Basin and Lower Basin.

## Readability screen

Measured by the generator on the clean truth (`checks.py` restates every figure on each build). Kilograms of ammonia a
hectare, golden against the census route and the mean count: Northern Vale 31.53 (31.94, 31.69), Eastern Vale 29.74 (30.33,
29.93), Southern Vale 28.48 (29.09, 28.70), Coastal Vale 22.91 (23.04, 22.90), Midland Basin 34.23 (29.73, 32.41), Inner Basin 28.10
(23.63, 26.31), Lower Basin 28.31 (24.19, 26.63), Lake Uplands 24.23 (34.41, 27.88), Middle Uplands 23.62 (34.02, 27.23), Eastern Uplands
20.27 (28.79, 23.30), Western Seaboard 23.92 (36.05, 28.76), Atlantic Coast 20.10 (29.28, 23.60).

| Rung | What the response does | What in the pack points at it | Verdict |
|---|---|---|---|
| L0 the census at the annual factor (default) | each region's 1 June census by category times Table 5 | the census is the national livestock count; Table 5 is per head per year | readable |
| L1 the register's 1 June stock at the annual factor | the same cattle rebuilt from the register | the register's exports; it agrees with the census | readable |
| L2 a uniform correction | L0 or L3 scaled to any national figure | nothing ships a national total | readable |
| L3 the register's mean count at the annual factor | each region's animal-days by category over the year, divided by 365, times Table 5 | the measure is a year's; the register shows births, moves and exits | readable |
| L4 animal-days at the home region's season | each animal's days at the stage of the region of its first herd | nothing | silent |
| G golden (decisive) | each animal-day in the region of the herd holding it, at Table 3's housed rate inside that region's housing season and its grass rate outside it | nothing labels an animal's housed days or sets the census day against the year; Table 3's caption reads as the factor's derivation, and the register's seasonal moves show only when aggregated by month and region against the census day | silent |

L2 never lands the golden set: scaling the census to the golden's national total files the default nine, and scaling
the mean count designates Northern Vale, Eastern Vale, Southern Vale, Midland Basin, Lake Uplands, Middle Uplands and Western Seaboard. L4 files the
golden set (Western Seaboard and Atlantic Coast move 5.7 and 6.5 per cent, both far under the line).

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the programme year | 1 November 2025 to 31 October 2026, by calendar day | the twelve months to the extract | same call (the extract ends 31 October) | rules section 2 |
| SF2 | ammonia from cattle manure | housing, storage, spreading and grazing, cattle of all ages, at the factor note's factors | fertiliser or other livestock added | not computable on the measure; the fertiliser and pig files are distractors | rules section 3 |
| SF3 | arising in the region | each animal-day in the region of the herd holding the animal that day | each animal in the region it was counted in on 1 June | another set (the default) | rules section 3 with the note's Table 3 caption |
| SF4 | a day in transit | the animal in its departure herd until its arrival date | in the arrival herd from the departure date | same call (asserted) | the export notes' arrival date |
| SF5 | a day at a mart, a dealer's premises or an export centre | counted where those premises are | dropped, or counted at the seller | same call (asserted) | the herd register's herd types |
| SF6 | the exit day | not counted (present on days before the exit date) | counted | same call (asserted) | the export notes |
| SF7 | the birth day | present from the birth date | from the registration date | same call (asserted) | the export notes |
| SF8 | a housed day | a day inside the housing season of the region where the animal is that day (Table 4) | the season of the animal's home region | same call (asserted) | the note's Table 3 caption |
| SF9 | an animal's category on a day | calf under 365 days; cow from its first calving, dairy or suckler by breed; otherwise one to two years or over two years | the census's categories on 1 June held all year | another set (the default) | the note's section 2 |
| SF10 | a dairy cow | a cow of a dairy breed on the note's list | a cow in a dairy herd | identical (every cow in a dairy herd is a dairy breed; asserted) | the note's breed list |
| SF11 | farmed land | the 2026 declared area by herd, commonage shares included, by the herd's 2024 region | commonage shares left out or counted whole | same call (asserted) | rules section 4 |
| SF12 | the regions | the 2024 regions | the census's pre-2024 codes | same call (asserted) | rules section 4 |
| SF13 | a reissued herd number | the herd register's record valid on the day | the current record for every day | same call (asserted) | the herd register's validity dates |
| SF14 | at or above the line | unrounded kilograms a hectare at or above 26 | rounded to two decimals first | same call (the nearest region sits 6.8 per cent from the line) | rules section 5 |
| SF15 | ammonia against ammonia-nitrogen | the note's factors are kilograms of ammonia | not applicable | not applicable | the note's units |

## Ladder

Measured by the generator on the clean truth; `checks.py` asserts every row on each build.

| Rung | Regions designated | Flips from the golden | Call kept |
|---|---|---|---|
| L0 the census at the annual factor (default) | Northern Vale, Eastern Vale, Southern Vale, Midland Basin, Lake Uplands, Middle Uplands, Eastern Uplands, Western Seaboard, Atlantic Coast | 7 | no |
| L1 the register's 1 June stock | as L0 | 7 | no |
| L2a the census scaled to the golden's national total | as L0 | 7 | no |
| L3 the register's mean count at the annual factor | Northern Vale, Eastern Vale, Southern Vale, Midland Basin, Inner Basin, Lower Basin, Lake Uplands, Middle Uplands, Western Seaboard | 3 | no |
| L2b the mean count scaled to the golden's national total | Northern Vale, Eastern Vale, Southern Vale, Midland Basin, Lake Uplands, Middle Uplands, Western Seaboard | 5 | no |
| L4 animal-days at the home region's season | the golden six | none | yes |
| G golden | Northern Vale, Eastern Vale, Southern Vale, Midland Basin, Inner Basin, Lower Basin | none | yes |

The golden's margins from the line are +21.3, +14.4, +9.5, -11.9, +31.6, +8.1, +8.9, -6.8, -9.2, -22.1, -8.0 and
-22.7 per cent (in the order of the regions); the default's wrong cells sit 9.1 and 7.0 per cent under the line
(Inner Basin, Lower Basin) and 10.7 to 38.7 per cent over it (the five it adds); the mean count's three wrong cells sit 4.7
to 10.6 per cent over. The national total is 1,352.2 tonnes on the golden, 1,475.4 on the census and 1,396.1 on the mean
count; nothing in the pack publishes one.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | cattle of all ages present in the country at any time in the programme year | filed (rules section 3); the register's export covers every animal present |
| 2 | Unit of account | a region's tonnes of ammonia from cattle manure, and its kilograms a hectare of farmed land | filed (rules sections 3 and 5) |
| 3 | Attribution window | 1 November 2025 to 31 October 2026 | filed (rules section 2); SF1 |
| 4 | As-of dating | the register's extract of 9 November 2026, the herd register of the same date, the census of 1 June 2026 | C1 |
| 5 | Version basis | the factor note's 2025 edition; the 2024 regions | filed (rules sections 3 and 4); SF12 |
| 6 | Denominator | farmed land, the 2026 declared area with commonage shares | filed (rules section 4); SF11 |
| 7 | Weighting | none: animal-days at per-day rates | not applicable |
| 8 | Window length | one programme year | filed |
| 9 | Boundary inclusivity | designated at or above 26 kilograms a hectare | filed (rules section 5); SF14 |
| 10 | Rounding path | the line tested on unrounded figures; tonnes to one decimal and kilograms a hectare to two in the file | the prompt's rounding sentence |
| 11 | Tie-break | none needed | asserted: no region within 2 per cent of the line |
| 12 | Maturity and censoring | none: the year closed on 31 October and the extract runs to 9 November | not applicable |
| 13 | Order of operations | animal-days by herd, region and stage, then rates, then sums | linear |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | one row per animal and per movement | C1, asserted (no tag repeats in the animal file) |
| 16 | Identity normalisation | herd numbers with and without the county prefix's separator, the census's farm numbers | Layer 1; every movement herd and census farm resolves in the herd register (asserted) |
| 17 | Netting against gross | none | not applicable |
| 18 | Dimensional units | kilograms of ammonia a head a day, days, hectares, tonnes | filed (the note's units); SF15 |
| 19 | Code and status semantics | herd types, exit types, breed codes | filed (the export notes, the note's breed list); SF5, SF10 |
| 20 | Integerisation | none | not applicable |
| 21 | Clause scope | cattle manure only; fertiliser and other livestock outside the measure | filed (rules section 3); SF2 |
| 22 | Forward window contents | the designation governs the 2027 spreading season; nothing forward is estimated | not applicable |

## Literal reader

Executing the prompt and every filed sentence word for word: the rules measure each region's ammonia from cattle
manure arising in the region over the programme year, computed with the Environmental Protection Office's 2025
factors, against 26 kilograms a hectare of farmed land. The factor note states its rates per head per day, housed on
the days inside the housing season of the region where the animal is kept and at grass on the others, and its Table 5
sums them over a 365-day year for an animal kept in one region. No file states which cattle were in which region on
which day except the bovine register; the census states the cattle on each holding on 1 June. A literal reader
therefore computes the ammonia arising in each region from the cattle there on each day, at the stage of that day,
from the register's animal and movement records; taking the 1 June census for the year assumes the cattle on a
holding on 1 June were there all year, which the register contradicts for the yearlings out on summer lets, the
spring calves and the stores slaughtered before June. The golden is what those records give.

## Oracles

No file ties only under the golden or only on a wrong read. The census tables state the cattle on holdings on 1 June,
and the register's 1 June stock agrees with them under both routes, so they referee the conforming (herd and farm
numbers, regions, categories) and never the year; no shipped file states a region's ammonia, a national total or a
ranking of the regions on the measure. The ask's referee: one contractor's invoice lines carry the other contractor's
docket number in their reference field, the device's evidence, never an answer.

## Ask sheet

The call's declared population is the bovine register's animals and movements, the herd register, the census, the
land parcel register's farmed area and the factor note. Ask A reads only the three slurry contractors' exports and the
herd register's 2024 regions for their customers' herds, which the call never reads for spreading (the herd register's
region field is shared; the contractors' rows are outside the call's population, asserted by count). The fertiliser
sales by region, the creameries' milk supply and the pig and poultry census ship as distractors: the rules' section 3
scopes the measure to cattle manure, and no golden figure opens them (asserted).

- **Ask A, each region's cattle slurry spread by contractors on its farms from 13 January to 30 April 2026, cubic
  metres to the nearest hundred, and the share of it spread by low-emission equipment (trailing shoe, trailing hose or
  injection), per cent to one decimal (24 figures).** H18 home: a measure every region carries that the designation
  does not turn on, the low-emission spreading its farms already buy, beside its ammonia. User: the Unit's head, whose
  measures in designated regions require low-emission spreading. Primary device (silent, D1 the same records under two
  sources beside genuine same-day pairs, with D7 the true key in a reference string): in its busy weeks (9 February to
  27 March) Countrywide Slurry Services passes about a third of its jobs to the local contractor, Vale Agri in six
  regions and Basin Agri in the other six. Countrywide invoices the farmer at the service the farmer ordered and at
  its own two-thousand-gallon load (Vale Agri's load count at two thousand gallons whatever the tanker; Basin Agri's
  metered volume in whole loads, rounded up), dated when the local docket reaches it three to ten days later, with the
  local job number in the invoice line's reference field; the local job sheet records the same job on its day, at the
  farm's herd, with its own volume and the spreader it used (Basin Agri's fleet runs only trailing shoes and dribble
  bars, and Vale Agri sends a low-emission tanker to a third of the splash-plate orders it takes on). 149 of Countrywide's
  935 lines are such jobs, in every region. Twin: 47 farms where Countrywide and the local contractor each spread part of
  a store on the same day carry two genuine jobs at unrelated volumes. Only the reference field, read against the
  local contractors' job numbers, says which invoice lines bill another contractor's job. Hazards: Vale Agri's loads at
  each tanker's gallons, Countrywide's herd numbers written with a space, pig slurry and digestate jobs in all three
  exports, Countrywide's agitation hours, jobs into May. Stops, measured on the cut pack: every job once as exported (0 of
  24), a Countrywide line beside a same-day job on the herd dropped (0 of 24), Countrywide's lines kept and the job sheets
  they bill dropped (4 of 24), the reference read with Vale Agri's loads at two thousand gallons (12 of 24), the
  reference read with pig slurry, digestate and May kept (1 of 24), the golden.

| Ask | What the cracker does | Cracker |
|---|---|---|
| A | converts every export to cubic metres, keeps cattle slurry in the window, maps each customer herd to its 2024 region and sums every job as exported | misses |

Measured by: `generator/ceiling.py` on the cut pack.

| Ask | Graded figures | Cracker keeps | Mirror keeps | Naive handling keeps | Cracker |
|---|---|---|---|---|---|
| A contractors' spreading by region, cubic metres and low-emission share | 24 | 0 | 0 | 0 | misses |

Over the 24 figures the cracker keeps 0.0 per cent of ask weight (scores 45.0 with the call), the mirror 0.0 per cent
(12.0), the naive handling (a Countrywide line beside a same-day job dropped) 0.0 per cent; the best half-handled stop
keeps 12 of 24 and needs the reference field read.

Pair ceiling: 28.5.
Mirror leakage: 0.0 per cent of ask weight.
The construction layer is the chart, each region's kilograms a hectare against the line, which the cracker has with
the call and the mirror misses with it.

## Architecture 2 record (spent 2026-10-25)

Zip 37f7e1986e84036128ca2496b64197b3 (checks.py 61 PASS, verify.py 66 of 66, byte-identical rebuilds, precut 51 checks
with no FAIL, pair ceiling 28.5 by ceiling.py, leak.py REVIEW with no LEAK, guard heart WARN, surface four promotions
answered on the card). Round 1: both scored readers (sonnet, medium, fresh copies) went straight to the bovine register,
rebuilt every animal's days by herd from HERD_AT_START and the arrival dates, charged Table 3's housed rate inside the
housing season of the region the animal was in and the grass rate outside it, and landed the golden six with every
regional tonnage (kilograms a hectare a hundredth off on three regions); both named the census at Table 5 as the easy
route that files a different list and set it aside. score_reader exited FAIL on both; ask A held at 0 of 24 on both
(the Countrywide lines that bill a local contractor's job counted twice). Reader B called the decisive step closer to
rule application than to an analytical choice, because the factor note's Table 3 caption and Table 4 and the rules'
sections 3 to 5 spell the construction out. The judge thread was stopped at the spend. Lesson: where the record covers
every unit for the whole window at the grain the estimand names, and the governing documents state per-day rates by
place and season, building the estimand from the record is the careful analyst's first move rather than a step past a
finished-looking default; the census at the annual factor was a lazy rung no reader took. Reader B also noted two
generator tells to fix in any reuse of this world: exit dates running past the extract date (to 23 November 2026) and
registration lags uniform on 1 to 27 days.

## Architecture 1 record (spent 2026-10-25)

Zip 237917da9ecb5387a7250b4fde842cf2 (checks.py 58 PASS, verify.py 10 of 10, precut 51 checks with no FAIL, pair
ceiling 28.5, leak.py REVIEW with no LEAK, guard heart WARN). Round 1: both scored readers (sonnet, medium, fresh
copies) landed the call, the golden five, and score_reader exited 1 on both (asks 6 and 2 of 25). Reader A held the
settled stock flat and fitted the share of the settled level a new dwelling holds to its age since completion on the
2022 to 2025 registers (about 0.08 in its first quarter, 0.45 at a year, 0.80 at two and a half years, 1.0 from about
six), applied it to every completion since April 2014 and every trajectory dwelling, and filed Kettermere +16.1,
Quenbrook +14.8, Caldenstow Park +13.9, Lorrimere West +13.2 and Ebborby -13.4. Reader B built the same
electors-per-dwelling curve by age and type and filed the same five. Both named the step an analytical choice nothing
in the pack states. Both also found ask A's device: the 2021 report's run date (4 March 2022) and the notices beside it
told them the report held the January to March 2022 alterations, and both backed them out, missing the golden on
handling only (reader A 4 of 23 wards exact; reader B also removed additions it took to be under 18). The judge thread
(v1r1) returned DETERMINISTIC and APPROVE (Gate G forecasting and etl_conformance, analytical_non_defect; Gate H domain
and layers pass, decisive step analytical); it was not taken to a report, the call being spent. The readers' realism
notes: the settled stock barely moves from 2020 to 2025, the ramp is a near-exact exponential alike in every ward and
type, the trajectory's site sizes are round, and no register row lacks a UPRN.

## Tried and rejected
- 2026-10-25, at the draw: the seed's own world, each employer's FY2025 H-1B workers at Level I read from labour
  condition applications through USCIS's employer data hub, positions converting to approved petitions at very
  different rates by petition type (cap lottery against continuations) so the position share overstates Level I where
  it sits in new employment: the per-type apportionment is one join and one group-by once seen, the hub's initial and
  continuing columns invite it, and the employer-level conversion that leaves the share unchanged is the only partial
  fix; the cheapest licensed member is the golden, a single insight a reader has or does not. Not drawn.
- 2026-10-25, at the draw: the FY2027 weighted wage-level selection, each employer's Level I intake read through
  selection probabilities by level: executing the stated selection procedure is rule application, and its separation
  from the linear reading is small (Level I at 0.174 against 0.154 on a plausible pool). Not drawn.
- 2026-10-25, at the draw: regression to the mean and retransformation bias (spent in five slot notes each), landfill
  first-order decay (set aside three times in this lane against task480), overdose deaths with unspecified drugs
  (task455 v1's certificates corrected by drug class), age heaping (task230's rejected draw), areal interpolation
  (task253), a business register's head-office employment (a reflex join once the local unit register ships), a
  housing trajectory's lead-in times for unstarted sites (the trajectory reproduces the started sites by construction
  and fails forward on the rest, a validated decoy), spiralled forms in a random-groups equating (a balance check is a
  reflex and presmoothing forks the cut), a business register's industry codes maturing with the enterprise's age (a
  completion reskin). Spent or not drawn.
- 2026-10-25, architecture 1 (each dwelling's electors aged to its canvasses on the 2032 register on the build-up the
  registers show), spent at stage 4: both scored readers fitted electors per dwelling to the dwelling's age since
  completion on the property-level registers and applied the ramp to every dwelling built and to come, landing the
  golden five. A register panel at property level beside every new dwelling's completion date makes a new unit's ramp to
  the settled level the forecaster's first move, not a skipped step; task484 v1's lease-up curve (a fill record of
  earlier additions beside a flat stock) was the same insight and fell the same way, and the draw's slot screen missed it
  because it searched the mechanism's words (build-up, canvass, register) rather than the setting's (lease-up,
  occupancy, new premises). The ask's switch-off device fell to the report's own run date beside a notices file: a
  file-level stamp that differs from the register's date is read by every careful reader.

- 2026-10-25, architecture 2 draw: a national forest inventory's rotating panels, the drought year's carbon change read
  by year effects across overlapping remeasurement intervals against the panels' moving average. Prototyped: at a
  district's 900 plots the year effect scattered 3 to 12 tC/ha a year around truths of -5 to +1.6, lumpy mortality and
  fellings swamping one year's signal; at a province's 6,000 plots it recovered the drought (-0.4 to -1.9 against
  -1.05) where the moving average said +2.2, but spreading interval changes onto calendar years is task123's
  calendarization driver, and the latest panel's own contrast cues it. Not drawn.
- 2026-10-25, architecture 2 draw, set aside on their records: length-biased sampling (task182 v4, 264, 130, 135, 268,
  272, 282, 120), plausible-value conditioning (task482 v11), at-berth reefer load (task482 v8 and task484 v3 screens),
  death distribution methods (task243), capacity-censored demand (task168), competing risks (task266, task133), rater
  drift (task471 v2, sent back as planted), rapid guessing (task479 v4), speededness (an anchor-drift screen catches
  it), ecological inference (forks, task279), trend uncertainty with shared factors (task482 v10, margin fragility), a
  birth-death model (task482 v12), a lunar new year shutdown (a calendar reflex), catalyst age in throughput (task478
  v6, landed), intermittent aerial plumes annualised (task462, task484's own screen, task450's), three imperfect sources
  read by a latent class model (task456; task271's screen), linkage error carried into a linked rate (task449, task454,
  task468), queueing at a runway or a desk (task148, task156, task159, task198), deductible leveraging on large
  claimants (task479 v3, landed), and in-progress treatment courses or prior authorisations (task482 v14's open
  episodes).
- 2026-10-25, architecture 2 draw, not drawn on the merits: children ageing into the electorate (the linkage chains for
  the probabilities fork and the lifecycle shows in the panel's cross-section); free school meal registration under
  universal meals (the year-group jumps show in one file); holiday-let flipping, demand response generators, fuel
  tourism, heat pump savings and insulation rebound (each a change read by a difference-in-differences in a side file,
  task484 v3's driver); hull fouling (a weak ETL fit, and the fouling curve forks); under-reported venting and
  capitated encounters (defects to catch); nutrient-neutrality credits, tankering, the authorised vehicle register and
  a free-meals expansion (rule application); developer absorption against a filed trajectory (a competing defensible
  answer); the payroll survey's four- and five-week months (smaller than the noise); embedded solar (semantics plus a
  calibration, and no ETL task type); coroner routes (a task181 replica); provisional industry codes maturing (a
  completion reskin); subset-sum remittance matching (a client exemplar's replica); list inflation in a patient
  register (a defect risk); continuous-monitor substitution, a feed additive, crop abandonment, a refrigerant
  retirement wave and an occupant-turnover rebuild (each on file or v1-adjacent).
- 2026-10-25, architecture 2 draw, screened this session and set aside: truncation at a facility reporting threshold
  (calibrating on reporters selects on the outcome, but every correction forks and a gas customer file gives the
  answer directly); differential order effects in a counterbalanced bridge study (task464's world and decision); a
  link error accumulated over chained equatings (task482 v10's trend-uncertainty shape, margin-fragile); survey weights
  recalibrated to new population estimates (the official weights execute literally, so the recalibration reads
  unlicensed, as task484 v2 died); business-survey imputation with a payroll auxiliary (the class imputation is a member
  of the licensed family and the late returns hand over the back-test); a fuel's reclassification after a rebate
  ended (a code's meaning, semantics); a broiler flock's crop phase on the census day (the estimand's own definition
  invites the placements; its insight is kept, and widened, in the herd draw).
- 2026-10-25, architecture 2 (each region's cattle-manure ammonia from animal-days placed by region and housing season, against the June census at the annual factor): spent at stage 4 round 1. Both scored readers rebuilt the animal-days from the register at Table 3's per-day rates by region and season and landed the golden six; with the register covering the whole year at the estimand's grain and the factor note stating per-day rates by place and season, the golden was the careful route, not a step past a default.

# task484 design note: Halvard County's 2025-26 wood smoke zone determinations after a propane price spike (architecture 3)

Drawn 2026-10-24 on the author's standing rule (no retirement) after architecture 2 was spent at stage 4 on the
judge's SEND_BACK; a fresh world and mechanism. The candidates screened before it are in Tried and rejected.

## Draw

- **Pairing:** Physical & Environmental Sciences / `emissions-inventory`, drawn for Data Extraction & Conformation
  (ETL). The task type builds an inventory from activity data and emission factors. ETL because the deliverable is
  the conformed 2025-26 inventory by burn zone and SCC, built from the device registry, the household survey's
  responses, three propane distributors' exports in three layouts (a ticket csv, a fixed-width billing export with
  account and transaction records, a workbook of monthly gallons by member account), the airport station's daily
  readings, the state tool's documentation, the state's fuel and factor tables and the Census files the tool reads,
  which disagree in layout, units and keys.
- **Objective check:** the call is a determination per burn zone read off the conformed inventory; nothing future
  is predicted (not Forecasting), and the work is the conformation and the season's activity estimate (not
  Descriptive or Causal: the comparison is a means of estimating one season's wood burned, not a policy effect).
- **Shape:** 07, a grid of cells: the five burn zones by PM2.5, determination and share of the fund, the PM2.5 from
  wood burned in place of propane beside them, and the asks' grids (each zone's commercial propane in gallons and
  tons of NOx; the county outside the maintenance area, appliances and PM2.5 by SCC). Criteria: the call 1, zone PM2.5
  5, determinations 5, shares 5, the propane component 5, ask A 10, ask B 12, the two files 2: 45.
- **Decision and window:** which of the maintenance area's five burn zones, if any, had 2025-26 PM2.5 from
  residential wood combustion above its allotment in Table 4-2 of the maintenance plan, and so shares the 2026-27
  changeout fund, which the county ordinance splits equally among the zones over their allotments. The quantity is
  retrospective with its reason: the ordinance reads the latest complete heating season (1 October 2025 to 30 April
  2026), and the decision it drives (the 2026-27 changeout season, opening 1 November) is forward.
- **World:** Halvard County Air Quality Program, a county program in Montana for the Halvard Valley PM2.5
  maintenance area: five burn zones (Valley Floor North and South on the gas utility; East Bench, West Bench and
  Upper Valley mostly on propane), a solid fuel device registry kept since 2008, a 2024-25 household heating survey
  (the program surveys every third winter), and three propane distributors' exports under a 2019 data sharing
  agreement. Winter 2025-26 had the degree days of 2024-25 to within 0.02 per cent (2023-24 ran 7 per cent colder);
  propane prices spiked from December to February, which no shipped file records. Personas from `guard.py names
  --geo us --seed 484`: Billy Davis, Kimberly Rogers, Martin Booth.
- **Pack (21 files):** the registry (csv), the burn zone parcel list (csv), the device code crosswalk (csv), the
  survey responses (csv) and methods note (pdf), Wapiti Propane's accounts and tickets (csv, 43,811 tickets),
  Coldwater Fuel & Propane's fixed-width export and its record layout (txt, 64,123 lines), the Halvard Valley Farmers
  Cooperative's monthly workbook (xlsx), the station's daily readings (csv), the fuel equivalents and the 2023 factor
  table (csv), the maintenance plan's Chapter 4 with the changeout fund ordinance (pdf), the state tool's
  documentation (pdf), two ACS block-group releases, the assessor's housing units on 2010 block groups and the
  Census relationship file (csv); distractors in metadata.json: the burn curtailment calls and the national forest's
  firewood permits.
- **Deliverables:** `rwc_inventory_2025_26.xlsx` (the inventory by zone and SCC, the propane comparison it rests on,
  the commercial propane category, the county outside the area) and `zone_determinations_2026_27.csv` (one row per
  zone in the program's determination layout).
- **Card:** `.claude/skills/fingerprint/cards/task484.json` (architecture v3, lineage v1 and v2 spent), checked
  before registration: WARN only. Differentiation lines are filed against task123 (the same decisive gap, G4 and
  decision type) and task152, task232 and task269 (the same decisive gap, G4 and Gate G).
- **WARN answers:** repeat.question_form (which): the decision is a designation set, so the question asks which
  zones, with "if any" so that none is a grammatical answer.
- **Data-native sentence:** the propane price spike moved part of the heat in propane homes with a heating
  appliance onto the appliance, which no meter records; it shows only in the propane exports, as deliveries falling
  26 to 32 per cent at the accounts whose parcel has a registered heating appliance while the zone's other propane
  accounts took what they took in 2024-25, where the two groups moved alike in proportion from 2023-24 to 2024-25.
- **Strategy label:** causal_design: the season's wood burned is recovered through a difference-in-differences on
  the displaced fuel, with the comparison group (propane homes without a heating appliance) and the pre-period
  check the design's organs. Gate G decomposition_attribution: the exports' change is split between what every
  propane home shared and the switch only the appliance owners could make.
- **Measured on the generator's world** (`generator/golden.py` on the cut pack): carrying the survey's 2024-25 wood
  per appliance into 2025-26 puts the zones at 57.5, 56.3, 77.9, 68.2 and 47.3 tons; adding the wood burned in place
  of propane puts them at 59.2, 59.0, 98.1, 83.0 and 54.2 (the world's truth 59.1, 58.7, 95.9, 77.9 and 50.4, the
  same set). Every member that reads the switch (the zone's comparison ratio, a pooled one, no comparison at all, the
  comparison in gallons, fireplaces out, fill years) lands within 0.21 tons of the golden and prints the same whole
  tons in every zone; the comparison in gallons fails the 2023-24 to 2024-25 check at z 4.3 to 14.8 where the ratio
  passes at |z| 1.3 or less.

## Three rules

Task type: Physical & Environmental Sciences, emissions-inventory, which serves ETL in the taxonomy.
Domain test: the quantity that decides is each burn zone's 2025-26 PM2.5 from residential wood combustion, the wood its appliances burned that winter times the 2023 emission factors, estimated for a season the household survey did not cover; a winter's fuel switching is measured where the displaced fuel is metered, a difference-in-differences on propane deliveries between the homes with and without a registered heating appliance, checked on the earlier pair of winters, carried through the heat balance at the furnace's and each appliance's seasonal efficiency.
Swap: "which of our five burn zones were over their wood smoke allotment" with clinics for stoves and patient visits for cords has no fuel a household switches between, no heat balance and no propane home without an appliance to compare against, so it stops making sense.
Layer 1: three propane distributors export in three layouts (a ticket csv, a fixed-width billing export with account and transaction records and an implied decimal, a monthly workbook by fiscal year), each its own billing system; geocodes are written with separators by one, without by another and not at all by the cooperative, whose system spells street words out; the survey vendor's instrument takes cords, face cords, pickup loads, tons or 40-pound bags; the county registry keeps every device with its removal history and year-only install dates for devices older than the 2008 program; the station reports daily maxima and minima with summer gaps, not degree days; the distributors send their whole valley book, accounts outside the maintenance area included; nothing is placed to be caught.
Layer 2: estimand identification, a difference-in-differences with a pre-period check: a season's wood burned is not measured, the survey's rates describe the winter before, and a price shock on the competing fuel moved heat onto the appliances of the homes that heat with it; the choice that flips the call is reading that switch from the propane deliveries against the zone's homes without a heating appliance, in proportion, against carrying the survey's rates into the new winter.
Decisive step: estimating each zone's 2025-26 wood burned as the survey's wood per appliance plus the heat the propane homes with a registered heating appliance moved off propane, measured by how much further their deliveries fell than at the zone's propane homes without one (in proportion, as the two groups moved alike from 2023-24 to 2024-25) and carried into cords at the propane furnace's and each appliance's seasonal efficiency.
Not semantics: with every field read correctly (tickets in gallons, accounts joined to parcels, the fixed-width decimal placed, face cords and pickup loads converted, device codes mapped to SCCs, zones from the parcel list, degree days from the readings) the easy route still carries the survey's wood into 2025-26 and reads the propane exports only for the commercial category, and no field, code, unit or definition read differently moves it.
Not rule application: the plan's 4.3 files the estimand (the PM2.5 emitted from the wood burned that season by the appliances in use, at the 2023 factors, against Table 4-2) and says nothing on how the season's wood burned is estimated; on the cut pack the enumerated family (the survey carried as reported or at the degree days, plus the switch read by the zone's comparison ratio, by a pooled ratio, against no change at all, in gallons, or over fill years) spans 77.9 to 98.2 tons on the East Bench and files two different sets, the standing family (every member that reads the switch) spans 98.00 to 98.21 there and prints the same whole tons in every zone, and what rules out the survey carried alone is the exports' own 26 to 32 per cent shortfall at the homes with a heating appliance against 0.996 to 1.002 at the homes without one, which no filed clause states and no table displays; the cheapest licensed member (each home's 2024-25 gallons less its 2025-26 gallons, no comparison at all) files the golden set at 98.03 on the East Bench, so the step is the recognition, not a choice inside the family.
Analyst test: A strong analyst who reads every file correctly builds the 2025-26 inventory from the 2024-25 household survey's wood per appliance class, carried at the two winters' (equal) degree days, times the registry's appliances in use, uses the propane distributors' exports only for the commercial propane category, and names Valley Floor South alone as over its allotment, where the benches' propane homes with a heating appliance took 26 to 32 per cent less propane and both benches are over.
Estimand: each burn zone's PM2.5 from residential wood combustion in the 2025-26 heating season (1 October 2025 to 30 April 2026), the PM2.5 emitted from the wood burned that season by the appliances in use, at the 2023 emission factors, against the zone's allotment in Table 4-2; filed in the plan's 4.2 and 4.3 and the ordinance's 8.30.140 (pdf).
No decoy: nothing is planted; the registry, survey, exports, readings and conversion factors are the program's and its suppliers' own records as their systems produce them, no memo, draft, briefing or stakeholder figure carries a wrong answer, and no filed sentence prescribes carrying the survey into a later winter.
No certified replay: no certified or published figure is reproduced to recover the method; the construction follows from the estimand and from the data.
Lesson: an unmetered fuel's use in a season the survey missed can be read off the metered fuel the households left, but only against the households that could not switch and only in proportion, as the earlier winters show; no build on file teaches recovering one fuel's use from another fuel's deliveries by appliance ownership.

## Default path

1. Conform the registry, the survey responses, the three distributors' exports, the station's readings and the state's
   tables: device codes to SCCs, survey units to cords and tons, accounts to parcels and burn zones.
2. Count each zone's appliances in use in 2025-26 by class from the registry (installed before 1 October 2025, not
   removed).
3. Take the 2024-25 survey's wood per appliance for each zone and class as its methods note estimates it, carried
   into 2025-26 as reported or at the two winters' degree days (equal to 0.02 per cent).
4. PM2.5 at the 2023 factors, each zone against Table 4-2; the propane exports read for the commercial and
   institutional category, the county outside the area on the state tool.

Ends on: Valley Floor South alone exceeds its allotment and takes the whole fund.

Golden: Valley Floor South, East Bench and West Bench exceed their allotments and share the fund at USD 155,000 each.

## Stump sentence

The default path carries the 2024-25 survey's wood per appliance into 2025-26 (the two winters had the same degree days) and reads the propane exports only for the commercial category, so the benches' appliances burn at last winter's rate, their PM2.5 sits at 78 and 68 tons under allotments of 89.9 and 77.6, and Valley Floor South alone exceeds its allotment and takes the whole fund, where the benches' propane homes with a heating appliance took 26 to 32 per cent less propane in 2025-26 while their neighbours without one took the same, and the wood burned in its place puts both benches over.

## Readability screen

Measured on the cut pack (`generator/golden.py`); zones Valley Floor North, Valley Floor South, East Bench, West
Bench and Upper Valley, allotments 63.9, 52.6, 89.9, 77.6 and 58.6 tons.

| Rung | What the response does | What in the pack points at it | Verdict |
|---|---|---|---|
| L0 the survey as reported | each zone's appliances in use at the survey's 2024-25 wood per appliance | the survey is the only file that states burning | readable |
| L1 the survey at the degree days (default) | the same, scaled by the two seasons' degree days from the station (1.0001) | the station's readings | readable |
| L2 a uniform uplift | every zone's burning raised by one share for a dearer or colder winter | nothing: no price or burning series ships | readable |
| L3 the commercial category | the exports summed by account class for their own category | the plan's 4.4, the prompt | readable |
| G golden (decisive) | the propane homes split by the registry's heating appliances, the 2025-26 shortfall against the zone's homes without one, carried into wood at the efficiencies | nothing labels a propane account by appliance or compares its seasons; the split runs account to parcel to registry, and the exports' only stated use is the propane categories | silent |

L2 never lands the golden set: Valley Floor North goes over at an 11.1 per cent uplift, before the West Bench
(13.8) and the East Bench (15.5), so any uniform uplift that puts a bench over puts Valley Floor North over first.

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | PM2.5 from residential wood combustion | the wood-burning appliances' PM2.5 at the 2023 factors by SCC | the zone's residential propane combustion added | same call (propane PM2.5 is under a ton a zone) | plan 4.4: those categories do not count against the allotments |
| SF2 | the 2025-26 heating season | 1 October 2025 to 30 April 2026, deliveries by delivery date | the July to June fill years for the comparison | same call and whole tons (asserted) | plan 4.2 names the season; the fill-year comparison converges |
| SF3 | appliances in use | registry devices installed before 1 October 2025 and not removed | every device Active at the 15 May 2026 extract | identical counts (asserted) | plan 4.3; nothing was installed or removed after 30 April |
| SF4 | exceeded its allotment | unrounded PM2.5 above the allotment | whole tons against the allotment | same call: every zone 4.45 tons or more from its allotment (asserted) | plan 4.2 and the ordinance's A |
| SF5 | a parcel's burn zone | the burn zone parcel list | the registry's burn_zone field | identical for every device (asserted) | plan 4.1 |
| SF6 | survey units | a face cord a third of a cord, a pickup load half, 40-pound bags | pickup loads at a third of a cord | same call (asserted) | the survey methods note |
| SF7 | the survey's grain | each zone's weighted class mean, classes under 10 respondents at the five-zone mean | classes pooled across zones | another set (Valley Floor North over, 64.6) | the survey methods note's estimator |
| SF8 | the survey's weights | each respondent's weight | unweighted means | same call and whole tons (asserted) | the survey methods note |
| SF9 | the weather between the winters | degree days from the station's daily maximum and minimum, base 65, ratio 1.0001 | no weather adjustment | same call and whole tons (asserted) | the readings make the readings converge |
| SF10 | a heating appliance home's expected 2025-26 gallons | its 2024-25 gallons at the ratio of the zone's propane homes without a heating appliance | a pooled ratio; no change; the change in gallons; fireplaces out of the comparison | same call and whole tons under every one (asserted) | the records converge; the gallon form fails the 2023-24 to 2024-25 check |
| SF11 | a heating appliance | a class the state tool gives a seasonal heating efficiency | fireplaces counted as appliances that took heat | not computable (no efficiency); fireplace homes in or out of the comparison, same whole tons (asserted) | the tool's Table 1 |
| SF12 | the propane furnace's efficiency | 85 per cent, the fuel sheet's existing furnace or boiler | any other value | not available | heating_fuel_equivalents.csv carries one propane row |
| SF13 | heat in a gallon of propane | 91,500 Btu | a lower heating value | not available | heating_fuel_equivalents.csv |
| SF14 | a cord's heat and weight | 18.5 million Btu and 1.163 tons; pellets 16.4 million Btu a ton | another wood | not available | the tool's section 2 |
| SF15 | the propane homes | the residential accounts on parcels in the zones | commercial accounts or accounts outside the area in the comparison | same call and whole tons (asserted) | the accounts' class and the parcel list |
| SF16 | the homes compared | accounts with deliveries in all three seasons | an unbalanced panel | identical (every residential account in the zones has all three; asserted) | the records converge |
| SF17 | a home whose 2025-26 gallons exceed its expectation | netted in its class's sum | floored at zero | same call and whole tons (asserted) | 14 of 3,813 homes; the records converge |
| SF18 | the fund's split | equally among the zones over their allotments | in proportion to the excess | USD 155,000 each | the ordinance's B |

## Ladder

Measured in the generator (`golden.py` on the cut pack, `checks.py` on the world's clean truth; allotments 63.9,
52.6, 89.9, 77.6 and 58.6 tons for Valley Floor North, Valley Floor South, East Bench, West Bench and Upper Valley).

| Rung | Zones over their allotment | Flips from the golden | Call kept |
|---|---|---|---|
| L0 the survey as reported | Valley Floor South | 2 | no |
| L1 the survey at the degree days (default) | Valley Floor South (57.5, 56.3, 77.9, 68.2, 47.3 tons) | 2 | no |
| L2 a uniform uplift of any size | Valley Floor North joins before either bench | 1 or more | no |
| L3 the switch read in gallons (fails the 2023-24 to 2024-25 check) | Valley Floor South, East Bench, West Bench | none | yes |
| G golden | Valley Floor South, East Bench, West Bench (59.2, 59.0, 98.1, 83.0, 54.2 tons) | none | yes |
| T the world's true burning | Valley Floor South, East Bench, West Bench (59.1, 58.7, 95.9, 77.9, 50.4 tons) | none | yes |

The golden's margins are 4.70 tons under, 6.37 over, 8.19 over, 5.39 over and 4.45 under; the default's are 6.36
under, 3.72 over, 12.03 under, 9.38 under and 11.26 under. The correction tracks each zone's propane homes with a
heating appliance (184, 262, 1,586, 1,218 and 563 accounts), not its size.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | each zone's wood-burning appliances in use in the season | filed (plan 4.3); SF3, C1 on the extract date |
| 2 | Unit of account | a zone's tons of PM2.5 from residential wood combustion in the season | filed (plan 4.2 and 4.3) |
| 3 | Attribution window | the 2025-26 heating season, deliveries by delivery date | filed (plan 4.2); SF2, C1 (no device installed or removed inside a season, the cooperative's months whole) |
| 4 | As-of dating | the registry of 15 May 2026, nothing installed or removed after 30 April | C1, asserted |
| 5 | Version basis | the 2023 factor table, the tool's 2023 edition, the 2019-2023 ACS release the tool names | filed (plan 4.3, the tool) |
| 6 | Denominator | none: tons against tons | not applicable |
| 7 | Weighting | the survey's respondent weights; the comparison as a ratio of summed season gallons | filed (methods note); SF8, SF10 converge, asserted |
| 8 | Window length | one season for the inventory; the comparison on the two seasons either side of the price spike with the season before as its check | the design; SF2 converges, asserted |
| 9 | Boundary inclusivity | exceeded means above the allotment | filed (the ordinance's A); SF4, margins asserted |
| 10 | Rounding path | determinations on unrounded tons; whole tons in the file; the asks at the prompt's rounding from unrounded sums | the prompt's rounding sentence; bin distances asserted |
| 11 | Tie-break | none needed | asserted: no zone within 4.45 tons of its allotment |
| 12 | Maturity and censoring | none: the season closed on 30 April | not applicable |
| 13 | Order of operations | units converted, zone and class means, counts, the switch's wood added, factors | linear, the same in any order |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | one account per propane home; a removed device and its replacement are separate devices | C1 (no residential account repeats a parcel; asserted) |
| 16 | Identity normalisation | accounts to parcels by geocode with or without separators, the cooperative's by spelled-out address | Layer 1; every residential account in the zones matches exactly one parcel (asserted) |
| 17 | Netting against gross | a home whose 2025-26 gallons exceed its expectation nets within its class | SF17 converges, asserted |
| 18 | Dimensional units | gallons, Btu, cords, tons of wood, pounds per ton, short tons | filed (fuel sheet, tool, factor table); SF6, SF12 to SF14 |
| 19 | Code and status semantics | device codes to SCCs, registry status, account class | filed (the crosswalk, the exports' layouts); SF15 |
| 20 | Integerisation | none for the call; fund shares divide evenly | not applicable |
| 21 | Clause scope | plan 4.3 covers residential wood combustion; 4.4's other categories do not count | filed; SF1 |
| 22 | Forward window contents | the determination governs the 2026-27 changeout season; nothing forward is estimated | not applicable |

## Literal reader

Executing the prompt and every filed sentence word for word: the plan's 4.3 measures each zone's PM2.5 as what the
appliances in use emitted from the wood they burned in the 2025-26 season at the 2023 factors, and the ordinance
compares it with Table 4-2. No file states what any appliance burned in 2025-26: the survey's methods note scopes its
estimates to the 2024-25 heating season, and the plan, the tool and the ordinance file no method for a season the
survey did not cover. A literal reader therefore has to estimate the 2025-26 burning from what the pack measures of
that season, and the only 2025-26 household heating record is the propane exports, which show the homes with a
registered heating appliance taking 26 to 32 per cent less propane while the zone's other propane homes took what
they took in 2024-25. Carrying the survey into 2025-26 unchanged assumes those homes heated the same way, which the
exports contradict; the golden is the burning those records imply.

## Oracles

No file ties only under the golden or only on a wrong read. No shipped file states a zone's 2025-26 wood burned or
PM2.5, or ranks the zones; the survey states 2024-25 burning per device, the exports state deliveries per account,
the curtailment calls and the forest's permits carry no zone's burning, and the plan states allotments only. The
asks' referees: the Coldwater ticket reference carries each delivery's date (the device's evidence, never an answer),
and the Census relationship file carries the 2010 block groups to 2020.

## Ask sheet

The call's declared population is each zone's appliances in use in 2025-26 (the registry's devices in the zones),
the survey's respondents and the residential propane accounts on parcels in the zones in all three seasons. No ask
computes over it.

| Ask | Quantity (unit, rounding in the prompt's closing sentence) | Population, outside the call's | Primary device (silent) | How it enters the call (H18) |
|---|---|---|---|---|
| A | each zone's commercial and institutional propane delivered in the 2025-26 season, gallons (nearest hundred) and tons of NOx (two decimals) | the distributors' commercial accounts, which the call never reads | D8 a settlement date for the event date: Coldwater's statement accounts post a month's deliveries on the first of the next month, so the export's TRANS-DT moves late-April deliveries out of the season and September top-offs into it; the delivery date sits only in the ticket reference, and residential accounts post on delivery | a measure every zone carries that the call does not turn on: the inventory's commercial and institutional heating category (plan 4.4) |
| B | Halvard County outside the maintenance area, 2025-26 appliances (whole) and tons of PM2.5 (one decimal) by SCC on the state tool | the county's households outside the area, from the Census and assessor files the call never reads | D7 codes valid in both vintages but drawn differently: the assessor's housing units sit on 2010 block groups whose codes match the ACS's 2020 block groups while the valley's edge was redrawn, so a code join reads the outer block group's rural units into a block group inside the area; the relationship file carries them across | the inventory's rows outside the maintenance area, which the program submits with the zones (plan 4.4) |

Shared hazards: survey units (the call path, neutral: pickup loads at a third of a cord keep the call); geocodes
with and without separators and the cooperative's spelled-out addresses (the call path and ask A); accounts
outside the maintenance area in every export (the call path and ask A); the ACS release the tool names against the
latest one in the pack (ask B). Fair handling, asserted: reading Coldwater's delivery date from the ticket reference
reproduces all 10 of ask A, and carrying the assessor's 2010 block groups to 2020 through the relationship file
reproduces all 12 of ask B. Separation, asserted by count: every Coldwater account whose transaction date differs
from its ticket reference is a commercial account, and no ask B file is read by the call.

Measured by: `generator/ceiling.py` on the cut pack (target.zip 87a0101c91c1a4ef).

| Ask | Graded figures | Cracker keeps | Mirror keeps | Naive handling keeps | Cracker |
|---|---|---|---|---|---|
| A commercial propane by zone, gallons and NOx | 10 | 0 | 0 | 0 | misses |
| B outside the maintenance area by SCC, appliances and PM2.5 | 12 | 0 | 0 | 0 | misses |

Over the 22 figures the cracker keeps 0.0 per cent of ask weight (scores 45.0 with the call), the mirror 0.0 per cent
(12.0), the naive handling 0.0 per cent.

Pair ceiling: 28.5.
Mirror leakage: 0.0 per cent of ask weight.
The cracker reads each export's own date field as the delivery date and joins the assessor's housing units to the
ACS on the block-group code, as the tool documentation's words invite; neither leaves a symptom in the hygiene
battery (no duplicate, no unmatched join, no fan-out). This is the paper measurement of the cracker the script
models; the stage 4 readers measure the real one.

## Tried and rejected

- 2026-10-20, at the draw: ET41's own world, broadband grant allocation from the FCC map: served, underserved,
  reliable technology, enforceable commitments and the location fabric are filed BEAD definitions and the base is a
  recorded count, so every lever was a filed definition, a fabric clean-up (Layer 1) or maturity of pending
  challenges; re-worlded.
- 2026-10-20, at stage 4 (architecture 1 spent): isolated reader 2 (sonnet, medium, fresh unzip) landed the call
  (Fairhaven and Linden) and all 24 ask figures. It read rule 2.2's "occupied housing units on 1 April 2026" as units
  occupied, not units existing, saw in the utility file that premises first billed after January 2021 start near
  empty while the older ones sit flat at 0.947, built the lease-up curve and applied it to every city; and it keyed
  the permits on city and parcel, which exposed every expired-and-reissued permit. Lessons: a fill record whose new
  premises begin at zero beside a flat stock is a ready-made curve one step from use, so it is the reflex, not a
  skipped step; the word "occupied" in the estimand points at it; a parcel key exposes re-issues to any hygiene
  pass. Reader 1 and the judge were stopped.
- 2026-10-24, architecture 2 draw: the payroll survey's birth-death model against the lagged QCEW census (reserved
  in task482's note). The months after the benchmark need a forecast of the net birth-death residual, and no filed
  criterion closes that carry-forward family; survey-research/etl is also under ban.pairing while task483 sits in
  the window. Not drawn.
- 2026-10-24, architecture 2 draw: a health plan's paid claims completed by received-date development after a
  processing speed-up. Spent in task451 (received-date development against the paid-date chain ladder).
- 2026-10-24, architecture 2 draw: a scanner-data price index's chain drift under sales, a multilateral index
  against linked Tornqvist. Spent in task463.
- 2026-10-24, architecture 2 draw: the variance of a year-on-year change over an overlapping member panel (a cost
  growth target read through a confidence interval). Spent in task195 (the paired difference), where a reader landed
  it.
- 2026-10-24, architecture 2 draw: rapid guessing read from response times. Spent in task479 (Gate G
  planted_defect_flip).
- 2026-10-24, architecture 2 draw: an aerial survey's intermittent plumes annualised as detections over overflights.
  That is task478 architectures 1 to 4's insight (detections over the coverage that could have seen them), and
  readers landed it there.
- 2026-10-24, architecture 2 draw: orphan wells' methane from a measurement campaign after worst-first plugging. The
  surviving wells' domain is one hygiene filter from the golden: a reader who counts unplugged wells drops the
  plugged ones from the sample too, so the reflex lands it.
- 2026-10-24, architecture 2 draw: an inventory base year recalculated after a method change, where the per-class
  recalculation (the reflex) is wrong because worst-first replacement left a cleaner surviving stock. Unspent at the
  slot screens, but its natural world is gas distribution mains, which is task476's (a niche repeat); a vehicle
  fleet's model-year rates tangle age with model year and reopen the family. Carried to the next draw as a lead, not
  drawn.
- 2026-10-24, architecture 2 ask draft (first cut pack 8b1df16c3144cafa): ask A on re-registrations linked by a
  predecessor id and ask B on a filed ACS vintage rule with labelled split block groups; ceiling.py measured the
  cracker and the mirror keeping 54 of 54 figures (pair ceiling 83.5), because every device was a field or a filed
  rule. Re-site both with silent devices (supplemental-stumping Part 3).
- 2026-10-24, ask A re-sited (second cut pack c7ccb8e1679941e1): the predecessor id removed and the split's old
  record closed as an ordinary closed record beside genuine same-day pairs; the cracker now keeps 3 of 36. Ask B unchanged.
- 2026-10-24, ask B re-sited (third cut pack 79bf825cac69ff18): the assessors' housing units keyed to 2010 block
  groups, the relationship file shipped, and every area-and-class cell given a genuine same-day pair; ceiling.py measures
  the cracker keeping 0 of 54 and a pair ceiling of 28.5.
- 2026-10-24, architecture 2 spent at stage 4 (zip 79bf825cac69ff18): both scored readers missed the call (each
  filed all six areas) and kept none of the 54 ask figures, but the judge returned NOT_DETERMINISTIC, SEND_BACK,
  competing_defensible_answer: the provision's 4.2 with the appendix's "by appliance class" executes literally as
  the survey's class mean times the plan's 2014 count, so the survivorship correction the golden makes is licensed
  by no shipped sentence, and filing that the base year means the stock that burned then, changed-out units
  included, would name the move. The judge also failed the golden's 2014 cells to one decimal (its fireplace rate
  0.372 against a class mean of 0.383, unexplained). Lesson: where the reflex is the literal execution of the filed
  estimand, the stump is a fork, not a step; the decisive population must follow from the WHAT as filed, with the
  easy route a different reading of the data rather than of the text.
- 2026-10-24, architecture 3 draw: road fuel sold at border stations to drivers from a neighbouring state (fuel
  tourism) read by a difference-in-differences around the neighbour's tax change. The swap test fails (cigarette
  sales read the same), and the territorial estimand's reading, not an analysis, decides. Not drawn.
- 2026-10-24, architecture 3 draw: a staggered rollout read with not-yet-treated comparisons against two-way fixed
  effects. Spent in task177's note.
- 2026-10-24, architecture 3 draw: a gas utility's unaccounted-for gas split into billing lag, the temperature
  under-registration of uncompensated residential meters and meter drift, leaving leaks as the residual. task476's
  gas distribution niche; the billing lag is task123's calendarization, and the temperature term executes Charles's
  law as a formula once seen. Not drawn.
- 2026-10-24, architecture 3 draw: landfill methane by first-order decay (task480's age-declining increments and
  four slot notes), capture-recapture across overlapping lists (task123, task180, task196, task253, task269,
  task448), gross flows corrected for reinterview misclassification (task244), equivalent soil mass for a soil
  carbon stock change (task279's conserved-component insight), glider kits' engine age (task474's ask device) and a
  replaceable component's own age (task132). Spent.
- 2026-10-24, architecture 3 draw: container ships' at-berth load by the reefers on board, calibrated on shore
  power meters. Rejected in task482's architecture 8 screens (a reader calibrating on the meters sees the per-call
  spread with reefers its first explanation).
- 2026-10-24, architecture 3 draw: hydropower turbine degassing of hypolimnetic methane. The pathway is either
  named by the filed estimand (then executed as a rule) or left to a reading of "reservoir emissions" (a fork, as
  architecture 2's judge ruled). Not drawn.
- 2026-10-24, architecture 3 draw: low-voltage anode effects emitting CF4 outside the potline's anode effect log.
  The cheapest licensed member is one regression with an intercept on the logged anode-effect minutes, task263's
  unmixing lesson. Not drawn.
- 2026-10-24, architecture 3 draw: flared gas booked as the balancing item of a production report and recovered
  by weighted least squares on the meters' stated uncertainties. Pro-rata and uncertainty-based allocation are both
  industry methods and the flare meter alone is a third defensible reading; filing one names the move. Not drawn.
- 2026-10-24, architecture 3 draw: N2O outside a growing-season chamber window (the spring thaw pulse) carried by
  fall-applied nitrogen. The gap is read off the estimand's dates (semantics), and the off-season transport forks
  between a ratio to the season and a ratio to fall nitrogen. Not drawn.
- 2026-10-24, architecture 3 draw: the leveraged trend of stop-loss excess claims (a reader with claimant-level
  claims trends each claimant by reflex), commercial cooking PM by device from health inspection equipment lists (a
  device-based inventory joins the season's device counts by reflex), bunching below a regulatory threshold (the
  counterfactual density's polynomial and window fork), and residential wood use moved by heat pumps or read from the
  assessor's heating type (architecture 2's heat-status variable, a composition one table hands over). Not drawn.
- 2026-10-24, architecture 3 draw: a Lunar New Year factory shutdown reaching a US port's container imports a
  Pacific crossing later, for its official seasonally adjusted series. The calendar regressor is a reflex in
  official statistics (task135, task467), and survey-research/etl sits under ban.pairing while task483 is in the
  window. Kept as a lead for task482's next architecture once the pairing frees.
- 2026-10-24, stage 2: thrift at the propane homes without a heating appliance (their deliveries falling with the
  price) dropped. The appliances' own burning then forks between the degree days and the comparison's ratio (the
  propane thrift applied to the wood), about 2 tons on the East Bench at whole tons, and no file can tell the two
  apart; with no thrift the comparison holds flat (0.996 to 1.002) and every member lands the same whole tons.
- 2026-10-24, stage 2: a 2025-26 four per cent colder than 2024-25 dropped. Carrying the survey with or without the
  degree days moved every zone by 2 to 3 tons and the comparison in gallons sat 1 to 2 tons from the ratio; equal
  degree days close both (C1), and the 2023-24 to 2024-25 check (7 per cent colder) still refutes the gallon form.
- 2026-10-24, stage 2: fireplaces in the switch dropped. At a 10 per cent efficiency each gallon of delivery noise is
  0.05 tons of wood, so the fireplace class swung 0.2 to 0.5 tons a zone between members; the tool gives fireplaces
  no heating efficiency and their propane homes join the comparison (fireplaces out of it: the same whole tons).
- 2026-10-24, stage 2: a fill-year (July to June) comparison printed the East Bench at 97 and the Upper Valley at 53
  against 98 and 54 while each year's summer top-off was drawn afresh; each account's top-off and spring fill are now
  a habit (a fixed amount with 5 per cent variation), and the fill-year member lands the same whole tons.
- 2026-10-24, stage 2: zone figures at one decimal rejected: the standing family spans 0.21 tons on the East Bench,
  so the zones are graded in whole tons with every member mid-bin (the survey's draw searched over 300 seeds,
  clearance 0.28 or more).
- 2026-10-24, ask B first cut: the redrawn tracts' 2010 codes read as 2020 moved the county's outside households by
  0.2 per cent and kept four of the twelve figures. The redraw now moves the outer block group's rural units into the
  first as the valley's edge built out, so the code join undercounts them by 7.5 per cent and misses all twelve.
- 2026-10-24, names: the first distributor was Larkspur (task483's college) and the survey vendor Bitterbrush
  (task135's note); renamed Wapiti Propane and Arrowleaf Survey Research.
- 2026-10-24, stage 4 round 1 (zip d51a7c26815e683b): both scored readers missed the call (Valley Floor South alone,
  the survey carried into 2025-26 at the equal degree days; neither read the propane exports beyond the commercial
  accounts) and missed all 10 of ask A (each took Coldwater's TRANS-DT as the delivery date), but both kept all 12 of
  ask B: the assessor file's name said 2010 block groups, so both carried its units through the relationship file.
  Scored 17 of 37 (ask B's 12 and the five determination figures the default gets right). The assessor file renamed to
  its housing units by block group as the assessor issues it, and the two commercial accounts whose parcel draw landed
  on a home's geocode (reader A found one) given parcels of their own; no figure moved (zip 87a0101c91c1a4ef).

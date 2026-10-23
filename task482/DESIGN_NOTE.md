# task482 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 7, drawn 2026-10-23 after architectures 1
to 6 were spent at stage 4: a fresh world and pack in the ETL objective, a state air agency's 2026 press VOC inventory
of the printing and converting plants its new VOC rule would cover.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task482.json` (architecture v7, lineage v1 to v6 spent), registered
  2026-10-23 after a pull, `check` re-run on the filed card. Guard WARN only, answered here: `overuse.org_family`
  (government_agency in 36 builds; the rule's applicability is a state air agency's call, and no other organisation
  adopts it) and, after the pull, `repeat.question_form` (which, against task178 v2, retired: the decision is a set of plants
  named, so the question asks which). Heart WARN on the organisation line only; nearest drivers 0.08 and below (task478 v6 and v7, then task181 at
  0.06). The first check ran against the old card's registration stamp and BLOCKed on that stale window (pattern,
  role, forum, organisation against task273 and task169); with the stamp dropped the window is today's.
- **Pairing:** Physical & Environmental Sciences, task type `emissions-inventory`, which serves ETL: fourteen plants'
  information-request returns (ink, coating, adhesive and solvent purchases with their safety data sheets, press
  logs, oxidizer data-historian exports, capture determinations and oxidizer performance tests, each plant in its own
  layout) conformed into the agency's 2026 press VOC inventory, the facility-by-process file the rule's applicability
  list and the state's ozone plan read.
- **The decision and the quantity:** the state's Department of Environmental Quality has drafted Rule 18-4 (Printing
  and Converting Operations) for the Kestle Valley ozone nonattainment area. The rule applies from 2027 to every plant
  whose presses emitted 25 tons or more of VOC in calendar year 2026, the VOC in the inks, coatings, adhesives and
  press wash solvents its presses used less what its capture and control systems destroyed (the draft rule's
  applicability section files this). The Environmental Quality Council votes on the rule with its applicability list.
  The quantity is each plant's 2026 press VOC; the call is the set at or above 25 tons. Forward facing: the list sets
  which plants carry the rule's controls and recordkeeping from 2027.
- **Shape:** `01`, every candidate's figure and verdict and the first below the line: fourteen plants' 2026 press VOC
  in whole tons, in or out, the nearest plant under 25 tons and its shortfall; two asks on records the call never
  reads (each plant's cleaning VOC away from its presses, and the inks, coatings and adhesives each plant received
  and cannot account for), a chart's named parts and the three files: about 70 criteria (1 call, 14 tons, 14
  verdicts, 2 for the nearest below, 14 and 14 ask figures, 6 chart parts, 3 files).
- **Strategy:** `other` (no family on the list states it: a control device's removal measured at one inlet condition
  is carried to the inlet each operating day ran at, through the device's outlet floor that the tests across the
  devices trace); Gate G `method_or_model_selection`; gap `objective` (a test's destruction efficiency is correct for
  the concentrated inlet it was measured at, not for the year's dilute days); pattern none; generators G14 (does the
  tested yield apply to this day's inlet, decisive) and G16. Layer 2 family `field_method`, pattern `own:an oxidizer's
  destruction measured at maximum production carried to each operating day through the outlet-against-inlet relation
  the tests trace, the day's inlet built from its captured VOC and its airflow`.
- **World:** an unnamed U.S. state; the Department's air quality division; fourteen printing and converting plants in
  the Kestle Valley (flexible packaging, gravure, labels, laminating, folding cartons), ten of them with regenerative
  thermal oxidizers on their presses. People from `guard.py names --geo us --seed 482`: Jeremy Cortez (rule
  development manager) and Audrey Bautista (emissions inventory lead). The first draw's names (Robert Meyers, Amanda
  Beck) were set aside on `people.first` against task104.
- **Forcing fact:** the Council votes on Rule 18-4 and its applicability list at its March 2027 meeting; the rule's
  controls apply from 1 July 2027.
- **Forum and forcing event:** council_or_assembly, vote_or_meeting. Organisation government_agency; role
  policy_adviser.
- **The physics:** a regenerative thermal oxidizer destroys about 98 per cent of a concentrated inlet, but its outlet
  holds near a floor of VOC per cubic foot however dilute the inlet grows, so the share it destroys falls on a dilute
  inlet (to the low 90s and below). Every oxidizer performance test runs at maximum production, as the permits
  require; on the days a plant runs part of its presses, a fixed-speed fan still draws its full air through every
  press's duct, so the inlet is dilute. Plants with variable-speed fans keep their inlets concentrated as presses
  drop out.
- **Data-native sentence:** the oxidizer tests were all run at maximum production while the press logs and the
  oxidizer historians show most 2026 operating days at part production with the fixed-speed fans at full air, and the
  tests across the plants trace an outlet that holds near a floor, so a test's destruction efficiency belongs to its
  own concentrated inlet and not to the year's dilute days.
- **Default path and golden, by name:** each plant's latest oxidizer test efficiency applied to its 2026 captured VOC
  names Carrow Gravure, Merrion Flexibles and Ravensbrook Gravure Packaging; each operating day's outlet read from the
  floor relation at the inlet the day's captured VOC and airflow imply adds Ashcombe Flexible Packaging and Kelvedon
  Laminates. Figures are set at the build from `generator/figures.json`.
- **The WHAT screen.** Population: the fourteen plants in the nonattainment area and every press each operated in
  2026. Outcome: the VOC the presses emitted (used less destroyed). Unit: tons. Window: calendar 2026. Comparison: 25
  tons. The decisive step settles none of them: it is how much of each day's captured VOC the oxidizer destroyed,
  which no filed rule or procedure states.
- **Sources, one line each:**
  - EPA's Air Pollution Control Cost Manual (incinerators and oxidizers): thermal oxidizers are designed to 98 per cent
    destruction or an outlet of about 20 ppmv, whichever is less stringent; the floor is the field's own model of a
    dilute inlet.
  - The printing and converting control techniques guidelines and the coating NESHAPs, which pair a destruction
    efficiency with an outlet concentration alternative for the same reason.
  - AP-42 and EIIP printing chapters: press VOC as material used, less retained, less captured times destroyed.
- **Same-puzzle and same-driver tests:** (objective, none, designation_set) and (objective, none,
  method_or_model_selection) against the last twelve builds, lineage included: no match (the guard's tests pass).
- **Abstraction test:** the nearest drivers stripped of nouns: task478 v7 carries a spot rate across a period by a
  property of a supplied input recorded by its supplier; task478 v6 along a clock since a part was replaced; task459
  reads a unit's own ratio at a level on its operating curve; task263 unmixes blended samples. Here no input property,
  clock or own curve moves the figure: a shared removal device's outlet holds a floor, and how much it removes on a
  day follows the concentration its own fan delivers, the joint result of the presses running and the fan's drive.

## Default path

1. Read the draft rule's section 2: a plant in the Kestle Valley ozone nonattainment area is covered from 1 July 2027
   if its presses emitted 25 tons or more of VOC in calendar year 2026, a press's VOC being the VOC in the inks,
   coatings, adhesives and press wash solvents used on it less what the plant's capture and control systems destroyed.
2. Converted each plant's 2026 press log to pounds of VOC used, press by press and day by day, through each product's
   safety data sheet (gallons times density times the VOC weight fraction, or gallons times pounds of VOC per gallon
   less water and exempt compounds), the job-based and the shift-based logs alike.
3. Split each controlled plant's VOC into captured and uncaptured by its capture determination (a permanent total
   enclosure verification at four plants, a capture test at six); the four plants without an oxidizer emit what
   they used.
4. Took each oxidizer's latest performance test, conformed both testing firms' inlet and outlet rates to one basis
   and read its destruction efficiency (96.71 to 98.23 per cent across the ten oxidizers).
5. Applied each plant's tested efficiency to its 2026 captured VOC, added the uncaptured VOC and compared each plant's
   total with 25 tons.

Ends on: Rule 18-4 covers Carrow Gravure, Merrion Flexibles and Ravensbrook Gravure Packaging.

Golden: Rule 18-4 covers Ashcombe Flexible Packaging, Carrow Gravure, Kelvedon Laminates, Merrion Flexibles and Ravensbrook Gravure Packaging.

## Stump sentence

The default path applies each plant's latest oxidizer test efficiency to its 2026 captured VOC and finds Carrow
Gravure, Merrion Flexibles and Ravensbrook Gravure Packaging at or above 25 tons, because a regenerative thermal
oxidizer's outlet holds near a floor (about 45 ppmv as carbon) however dilute its inlet, every test ran at maximum
production, and at Ashcombe Flexible Packaging and Kelvedon Laminates the fixed-speed oxidizer fans drew their full
air through days when the presses ran a fraction of their capacity, so those oxidizers destroyed far less than their
tests show; each operating day's outlet read from the floor the ten oxidizers' tests trace, at the inlet the day's
captured VOC and airflow imply, carries Ashcombe from 21 to 29 tons and Kelvedon from 20 to 28, and the rule covers
five plants.

## Three rules

Task type: emissions-inventory (Physical & Environmental Sciences), a point-source VOC inventory conformed from each
plant's material, production, control-device and test records, a task type serving Data Extraction & Conformation
(ETL): fourteen plants' information-request returns, each in its own layout, conformed into the agency's 2026
facility-by-process press VOC inventory that the rule's applicability list reads.

Domain test: stationary-source VOC inventory work: the deciding quantity is each plant's 2026 controlled press VOC,
which needs how much of each operating day's captured VOC its oxidizer destroyed; a thermal oxidizer's outlet holds
near a floor concentration whatever its inlet (the control cost manual's 98 per cent or about 20 ppmv), so its
destruction falls as the inlet grows dilute, and the field's method reads each day's outlet from its inlet through
the relation the performance tests trace; with hospital or traffic nouns there is no oxidizer, no outlet floor and no
fan diluting a control device's inlet, so nothing is left to decide.

Swap: put "hospital" for "plant" or "megawatt-hours" for "pounds of VOC" and nothing reads: there is no captured
stream, no add-on device whose removal depends on the concentration it is fed and no test at maximum production to
carry to a part-production day; the abstract move (a removal measured at one inlet carried to another) needs the
device's outlet relation and the day's inlet concentration, which only the oxidizer tests, the press logs and the
historians supply together.

Layer 1: purchases from two ink suppliers' invoice layouts in gallons, VOC content from safety data sheets in per cent
by weight or pounds per gallon less water and exempt compounds; press logs by shift at some plants and by job at
others; oxidizer historian exports in per cent of fan speed at some plants (each fan's curve to airflow) and in UTC
against the plants' local press logs; performance tests from two testing firms, one reporting VOC as carbon and the
other as propane; capture by permanent total enclosure verification at some plants and by a capture test at others;
a plant renamed after an acquisition, its older returns under the former name. Each is written by the system named
and none is placed to be caught; read the natural wrong way, some leave the call where it is (UTC days, a shift's
date, rated airflow, one carbon content) and some move it to another wrong set (pounds less water and exempt read as
pounds per gallon, every capture at 100 per cent, the former name's rows dropped, propane read as carbon), and none
turns the default path into the golden call (checks.py R2a to R2h).

Layer 2: field_method, a control device's tested efficiency carried to the operating day: a test's destruction
efficiency is the oxidizer's removal at the test's concentrated inlet; the tests across the ten oxidizers trace an
outlet that holds near a floor however dilute the inlet, and each operating day's outlet is read from that relation at
the inlet the day's captured VOC and the oxidizer's airflow imply.

Decisive step: reading each operating day's oxidizer outlet from the floor relation the performance tests trace, at
the inlet concentration the day's captured VOC (press logs through the safety data sheets and the capture
determination) and the oxidizer's airflow (the historian) imply, which lowers the year's destruction at the plants
whose fixed-speed fans ran at full air through part-production days and carries Ashcombe Flexible Packaging and
Kelvedon Laminates over 25 tons.

No decoy: nothing is planted: the purchases, data sheets, press logs, historians, capture determinations and tests
are what each plant's systems and testing firms write; no memo, statement, permit condition or earlier inventory
states a plant's 2026 press VOC, a destruction efficiency for 2026 or the outlet floor, and no document says how the
tested efficiencies are to be applied.

Not semantics: every field, unit, basis and clock read correctly (gallons to pounds of VOC through each data sheet,
VOC as carbon against as propane, fan speed to airflow, UTC to local, the renamed plant) still leaves the careful
route applying each plant's tested efficiency to its captured VOC; no field holds a day's destruction efficiency or
says that a test's efficiency depends on its inlet; the step is an estimate (the outlet relation) and the carry it
sets, not a reading.

Not rule application: the draft rule files the population, the outcome (VOC used less destroyed), the year, the unit
and the 25-ton comparison (the WHAT); no filed rule or procedure says how much of a day's captured VOC an oxidizer
destroyed. The family the rule leaves open, measured on the cut pack (checks.py R0 to R5, G1 to G4): the enumerated
family (each plant's latest test, the mean of its tests, the permits' minimum, the relation at the year's or each
month's mean inlet, each test's outlet concentration or rate carried to the year, each oxidizer's own tests, the
relation day by day) spans five designated sets of three to eight plants; the standing family (14 members: three
estimators of the hard floor, three smooth knees, an interpolation of the tests, the relation fitted by vendor and by
testing firm, the hour grain, two cut points) files one set and the same 14 whole tons, each plant's figure within
0.37 tons across it, every member at least 0.19 tons from a rounding half; what rules out the tested-efficiency routes
is the tests' own outlets, which hold within about 2 per cent of 45 ppmv as carbon while the dilute runs' inlets
double, and what rules out the outlet-concentration routes is the runs above the knee, whose outlets rise with their
inlets.

Analyst test: a strong analyst who conforms every purchase to pounds of VOC from its safety data sheet, every press
log to daily VOC used, applies each plant's capture determination and reads the draft rule and the information
request correctly applies each plant's latest oxidizer test efficiency to its 2026 captured VOC and files "Rule 18-4
covers Carrow Gravure, Merrion Flexibles and Ravensbrook Gravure Packaging"; only each operating day's outlet read
from the floor relation at the day's inlet adds Ashcombe Flexible Packaging and Kelvedon Laminates (checks.py R3a on
the generator's clean truth).

Estimand: draft Rule 18-4, section 2 (applicability): a plant in the Kestle Valley ozone nonattainment area is subject
from 1 July 2027 if the VOC its printing presses emitted in calendar year 2026 was 25 tons or more, a press's VOC being
the VOC in the inks, coatings, adhesives and press wash solvents used on it less the VOC the plant's capture and
control systems destroyed; the information request's cover letter files which records each plant returned.

No certified replay: no plant's 2026 press VOC, inventory figure or emissions statement ships, and no earlier
inventory, permit record or memo states one; nothing certifies either route, so no figure ties under the default path.

Lesson: an add-on oxidizer's tested destruction efficiency belongs to the concentrated inlet it was tested at; its
outlet holds near a floor, so on the days a plant runs part of its presses with the fan at full air the inlet is
dilute and the device destroys less, and the year's controlled emissions need each day's inlet put through the outlet
relation the tests trace; no build on file carries a control device's removal across the concentration its own fan
delivers.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, each plant's latest test efficiency on its 2026 captured VOC, the default path (Carrow, Merrion, Ravensbrook) | rule s.2 "less what ... destroyed" beside the tests' efficiencies: fires | the tests' efficiency column: fires | apply a measured control efficiency: fires | none | none | one product per plant | readable |
| R1, the mean of each plant's tests (the same three) | as R0: fires | as R0: fires | average the tests: fires | none | none | one product per plant | readable |
| R2, the permits' minimum destruction, 95 per cent, on every controlled plant (eight plants: the golden five, Elsworth, Hartmoor, Larkmoor) | the permits' control condition: fires | none | a conservative assumption: fires | none | none | one product per plant | readable |
| R3, the floor relation at each plant's 2026 mean inlet, or each month's (Ashcombe, Carrow, Merrion, Ravensbrook) | none | none | none: it needs the floor first | none | none | one ratio per plant | silent |
| R4, each oxidizer's latest test outlet (its concentration on each day's air, or its rate over the year's hours) (the golden five and Larkmoor) | none | the tests' outlet columns: fires | an outlet emission rate times hours: fires | none | none | one product per plant | readable |
| R5, each oxidizer's own tests (Ashcombe, Carrow, Merrion, Ravensbrook) | none | none | fit each unit's own data: fires | none | none | one line per plant | readable |
| G (decisive), each operating day's outlet from the floor the tests trace, at the inlet the day's captured VOC and airflow imply (Ashcombe, Carrow, Kelvedon, Merrion, Ravensbrook) | no sentence says an oxidizer's efficiency depends on its inlet | no column holds a day's inlet or efficiency | no reflex rebuilds a control device's inlet from press logs and fan airflow | none | none | none | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | VOC | the rule's definition, exempt compounds (acetone) excluded | every organic solvent | not the rule's; the call asserted under both | rule s.1; the safety data sheets' VOC less water and exempt compounds |
| SF2 | VOC used on a press | inks, coatings, adhesives and press wash solvents logged to the press | cleaning away from the presses added | same call (asserted; Larkmoor comes to 24.7) | rule 18-4-3(b) and 18-4-5 |
| SF3 | 2026 | local calendar days | the historians' UTC days | same call (asserted) | rule s.2; the request letter |
| SF4 | captured | each plant's capture determination | 100 per cent at every plant | the call moves: the capture-tested plants lose their uncaptured VOC (asserted) | the register's Capture sheet, one determination per plant; the request letter |
| SF5 | destroyed | what each oxidizer destroyed on each operating day | the latest test's efficiency; the permit's minimum | three plants (R0); six (R2) | rule s.2 (destroyed, not required or demonstrated); the tests' outlets refute one efficiency for every inlet (asserted) |
| SF6 | the tests' VOC basis | one basis for inlets and outlets, as carbon | firm A's as-propane figures read as carbon | the floor estimate off by a factor of three at firm A's plants; ruled out | each test report's method section (Method 25A as propane; as carbon) |
| SF7 | the carbon content of a plant's VOC | each return's reported carbon fraction | one default fraction | same call (asserted) | the request letter |
| SF8 | the oxidizer's airflow | the historian's standard airflow, through the fan curve where the historian logs speed only | actual airflow | same call (asserted) | the historians' tag lists; the fan curves |
| SF9 | an operating day's hours | the oxidizer's PROCESS hours, the press days' shifts | every hour not OFF | the call moves (asserted) | the historians' mode tag; the press logs' shift and job times |
| SF10 | the floor relation's form | the greater of the floor and a fixed share of the inlet | a smooth fit of outlet on inlet | same call (asserted) | the tests |
| SF11 | the floor's grouping | the ten oxidizers' tests together (one design, one combustion temperature) | each oxidizer's own tests | Kelvedon's own tests carry no dilute run and leave its dilute days unmeasured; the pooled floor holds within a narrow band at four plants | the tests; the plants' oxidizer descriptions |
| SF12 | rounding | press VOC and the shortfall to the whole ton, cleaning VOC to a tenth, gallons whole, each from the unrounded figure | none | none | the prompt |
| SF13 | retention in the substrate | none (inks and adhesives on films, foils and paperboard; no heatset press) | heatset retention | none applies | the plant register |
| SF14 | the renamed plant | Kelvedon Laminates with its records as Thameside Laminating (facility 0117) before 1 May 2026 | the 0117 rows left out | Kelvedon falls to 18.9 and the call moves (asserted) | the request letter; the register's former name |
| SF15 | press wash solvents | automatic blanket, plate and anilox wash logged to the presses | manual cleaning | Ask A's population | rule s.2 and s.4 |
| SF16 | cleaning away from the presses (Ask A) | cleaning materials issued to ink kitchens, parts cleaning and roll cleaning, less the VOC shipped off site under the cleaning profiles, plus the parts washers' added less removed solvent | issues alone | 13 of 14 figures move (asserted) | rule 18-4-5(b) |
| SF17 | the VOC in waste (Ask A) | the waste profile's solvent fraction times the manifest's weight times the solvent's VOC fraction | the manifest's weight as VOC | not rule s.4 | rule s.4; the waste profiles |
| SF18 | a parts washer's VOC (Ask A) | fresh solvent added less spent solvent removed, from the service tickets | solvent added alone | not rule s.4 | rule s.4 |
| SF19 | received in 2026 (Ask B) | delivered from 1 January to 31 December 2026, local dates | invoiced in 2026 | not the prompt's | the prompt ("received") |
| SF20 | the stock counts (Ask B) | the physical counts of 1 January 2026 and 31 December 2026 | book stock | not the request letter's | the request letter |
| SF21 | returns (Ask B) | inks, coatings and adhesives returned to the supplier for credit | none | not the request letter's | the request letter |
| SF22 | a product sold by the pound (Ask B) | gallons through its safety data sheet's density | pounds read as gallons | not the prompt's | the prompt (gallons); the supplier's catalog |

## Ladder

Figures from the cut pack (`generator/bundle.py`), asserted by `generator/checks.py` (whole tons are the deliverable's).

- **R0, each plant's latest test efficiency on its 2026 captured VOC, the default path: Carrow Gravure 37.1, Merrion
  Flexibles 31.1 and Ravensbrook Gravure Packaging 55.6 tons covered; Ashcombe Flexible Packaging 21.3 and Kelvedon
  Laminates 20.3.** Dies to the tests' own outlets: the runs under 2,000 ppmv as carbon hold within about 2 per cent of
  45 while their inlets run from 926 to 1,915, so an efficiency belongs to its inlet, and the press logs and historians
  put Ashcombe's and Kelvedon's 2026 days far more dilute than their tests (Ashcombe 980 to 1,871 against a test at
  about 1,880; 58 per cent of Kelvedon's days near 1,100 against tests at about 4,300).
- **R1, the mean of each plant's tests: Ashcombe (27.3) in, Kelvedon (20.1) out.** Ashcombe's 2018 test, run with two
  presses installed, lowers its mean efficiency; Kelvedon's three tests all ran concentrated. Dies the same way.
- **R2, the permits' minimum destruction (95 per cent) on every oxidizer: eight plants, the golden five with Elsworth
  Film Converting (44.2), Hartmoor Packaging (29.6) and Larkmoor Graphics (33.7).** Dies to rule 18-4-3(b): destroyed,
  not required; every test shows more.
- **R3, the relation at each plant's 2026 mean inlet (or each month's, R3m): Kelvedon 23.1 (23.6 by month) out.** Dies
  to Kelvedon's days: its mean inlet (about 2,190) sits under the knee while its concentrated days run near 4,100, and
  a year's releases are the days' sum, not the relation at the mean.
- **R4, each oxidizer's latest test outlet concentration on each day's air (R4m the mean of its tests' outlets, R4b the
  latest outlet rate over the year's process hours): Larkmoor 31.1 in.** Dies to the runs above the knee, whose outlets
  rise with their inlets: Larkmoor's tests ran on its concentrated gravure days, and 82 per cent of its 2026 days ran
  only the flexo press, at about 1,100.
- **R5, each oxidizer's own tests: Kelvedon 20.1 out.** Kelvedon's tests never ran dilute, so its own line has nothing
  to say about its dilute days; the ten oxidizers share one design and set point and the floor shows at both vendors'
  units and in both firms' tests.
- **G: Ashcombe 28.9, Carrow 37.2, Kelvedon 27.9, Merrion 31.1 and Ravensbrook 56.1 covered (29, 37, 28, 31 and 56);
  Larkmoor Graphics 20.9 the nearest below (21), 4 tons short.**
- **Margins:** the 14 standing members file the same five and the same 14 whole tons; the lowest covered plant clears
  25 by 2.9 tons and the nearest below falls 4.1 short; every member's every plant sits 0.19 tons or more from a
  rounding half (checks.py G1 to G4). The refuted straight line also files the five (G6).
- **Position, separation and dominance:** a set at a threshold; no decoy to dominate.
- **Worth:** the call, every plant's 2026 press VOC and the nearest below; the default path keeps the nine plants whose
  whole tons do not move (Garrowby and Norhaven move by one ton, Ashcombe, Kelvedon and Larkmoor by 8 or 9).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | the fourteen plants in the nonattainment area and every press each operated in 2026 (rule s.2); Ask A every plant's cleaning away from its presses (rule s.4); Ask B every plant's inks, coatings and adhesives |
| 2 | Unit of account | the plant; tons of VOC; gallons |
| 3 | Attribution window | calendar 2026, local dates (SF3, SF19) |
| 4 | As-of dating | the returns as filed for the information request of 12 January 2027; the stock counts of 1 January 2026 and 31 December 2026 |
| 5 | Version basis | each product's safety data sheet in force on the day it was used or issued (the revision log) |
| 6 | Denominator | none |
| 7 | Weighting | none: every pound counts once |
| 8 | Window length | the calendar year |
| 9 | Boundary inclusivity | 25 tons or more (rule s.2) |
| 10 | Rounding path | press VOC and the shortfall to the whole ton, cleaning VOC to a tenth, gallons to the whole gallon, each from the unrounded figure (SF12) |
| 11 | Tie-break | none: no plant sits within 2 tons of 25 (asserted) |
| 12 | Maturity and censoring | the year closed on 31 December 2026; every return covers it |
| 13 | Order of operations | used, then captured, then destroyed day by day, then summed; Ask A issued less waste plus washers; Ask B opening plus received less returns less closing less used |
| 14 | Row order | none |
| 15 | Duplicate resolution | the historians' daylight-saving hour once; no duplicate press log row ships |
| 16 | Identity normalisation | the renamed plant (SF14); product codes through the safety data sheet master and its revision log; supplier item numbers through each plant's cross-reference and the supplier's catalog |
| 17 | Netting | waste shipped and washer solvent removed net against cleaning issued (Ask A); returns net against received (Ask B) |
| 18 | Dimensional units | gallons, pounds, ppmv as carbon and as propane, scfm and fan speed (SF6, SF8, SF22) |
| 19 | Code and status semantics | the historians' mode tag; the press logs' material type codes; never the stump |
| 20 | Integerisation | none: tons and gallons are continuous |
| 21 | Clause scope | rule s.2 governs the call; rule s.4 governs Ask A; the request letter governs the returns' contents and Ask B |
| 22 | Forward window contents | the rule applies from 1 July 2027 to the plants covered on their 2026 press VOC |

## Literal reader

Executed word for word, the draft rule fixes the estimand: the VOC each plant's presses emitted in calendar 2026,
used less destroyed, against 25 tons. "Destroyed" is what each plant's oxidizer destroyed of what reached it, a
property of how the oxidizer ran on the year's days, so the candidates are a test's efficiency held for the year and
the efficiency each day's inlet implies. The data separate them: the ten oxidizers' 28 tests, all at maximum
production, show outlets within about 2 per cent of 45 ppmv as carbon at inlets from 926 to 1,915 and 1.8 per cent of
the inlet above 3,000, so an efficiency is a property of its inlet; the press logs and historians give each
production day's captured VOC and airflow, hence its inlet, and every form of the outlet relation the tests support
files the same five plants, while a test's efficiency held for the year files three (checks.py R3, G2). Every 2026
production day's inlet falls inside the tested range at its low end (944 to 980 at the dilute plants against the
runs' 926), so no member extrapolates the relation below the tests.

WHAT screen (stumping 1.2): population, rule 18-4-3(a); outcome, rule 18-4-3(b) (used less destroyed); window, rule
18-4-3(a) (calendar 2026); unit, tons; comparison, 25 tons. The decisive step settles none of them.

## Oracles

None. No plant's 2026 press VOC, emissions statement or earlier inventory ships, and no figure ties only under the
golden: the tests certify efficiencies at their own inlets and say nothing about 2026. The asks' files carry no total
that ties under one handling: the stores' issue totals, the hauler's manifest totals and the suppliers' statements
tie under every handling of the devices.

## Ask sheet

The Council's packet carries each plant's cleaning VOC beside its press VOC, because rule 18-4-5's cleaning provisions
apply to every plant in the area whether or not its presses are covered, and the inventory section's audit of each
return: the inks, coatings and adhesives each plant received in 2026 that its stock counts and press logs leave
unaccounted for (H18: an audit trail of the input the call consumes, through rows it never reads, to its control
total). No ask device or hazard row sits in the call's population (checks.py X3): the call reads the press logs, the
press materials' safety data sheet rows, the register, the historians and the tests; ask A reads the stores' issues,
the cleaning materials' sheet rows and the revision log, the hauler's manifests and profiles, the washer tickets and
the solvent vendors' payment lines; ask B reads the two suppliers' invoices, Haldane's catalog, the stock counts and
the press logs' gallon totals, device-free (checks.py X1 and X2 compute each side from its own files).

- **Ask A, each plant's 2026 VOC from cleaning away from its presses: 14 figures, tons to one decimal.** Path: the
  stores' issues, the safety data sheet master and its revision log, the hauler's manifests and waste profiles, the
  washer tickets, the solvent vendors' payment lines and rule 18-4-5(b) (seven files, about fourteen columns). Primary
  device: D2, an attribute at the wrong vintage: Haldane reformulated its equipment cleaning solvent HW-CS-210 on 1
  June 2026 from 7.10 to 3.20 pounds of VOC a gallon, the master carries the current revision, and the earlier formula
  sits only in the revision log among nine benign revisions, so issues before June read through the master understate
  every plant (every plant issues it; the least move is 0.11 tons). Hazards: D4, absence as the signal (at six plants
  Wexcombe's tickets stop at the end of June when the washers moved to Ostrander, whose services sit only in the
  payment lines with their gallons); D3, the hauler's weights in kilograms at two plants from its September system
  change, the unit column saying so. Stops (measured, `generator/ceiling.py`): the master for every issue and the
  tickets alone (the cracker and the mirror) 0 of 14; the revision log without the payment lines 8 of 14; the golden.
  Realism: a supplier reformulates ahead of a cleaning-solvent limit and the master shows the sheet in force today.
- **Ask B, each plant's 2026 inks, coatings and adhesives received that its stock counts and press logs leave
  unaccounted for: 14 figures, whole gallons.** Path: Corvane's invoice export, Haldane's statement and catalog, the
  stock counts, the press logs' gallons and the safety data sheet master's densities and product types (six files,
  about twelve columns). Primary device: D7, codes reissued: Haldane renumbered its catalog on 1 April 2026 by
  category, its documents before then carry the old numbers, and four of them (its 55-gallon drums of HW-CS-210,
  HW-PW-710, HW-IK-260 and HW-RC-240) are now the numbers of its coating pails, so the statement joins the current
  catalog without an unmatched line and every plant's January to March cleaning and press-wash drums read as coatings;
  the catalog's replaces_item column is the chain (every plant's figure rises; the least move is 110 gallons). Hazards:
  D8, deliveries shipped in late December 2025 and invoiced in January 2026, already in the 1 January count, and
  deliveries shipped in late December 2026 and invoiced in January 2027 (the document date in place of the ship date
  moves 13 of 14); D3, Haldane's adhesives sold by the pound with no unit on the line, the catalog's sold_by naming it
  (Kelvedon). Stops (measured): the current catalog (the cracker and the mirror) 0 of 14; the replaces column 14 of 14.
  Realism: an ERP catalog change keeps old numbers only as a replaces field.
- **The construction layer:** the call, every plant's press VOC and the nearest below; the cracker has them.
- **Main population zero-counts (asserted):** no press material is a cleaning material and the reformulated product is
  never logged on a press; the renumbered items are cleaning and press-wash drums the call never reads (X3).
- **Referee:** none.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, each plant's cleaning VOC away from its presses | issues on the master's current revision, cleaning-profile waste credited at its unit, washers from the tickets: 0 of 14 (measured on the cut pack) | miss |
| B, each plant's unaccounted gallons | lines shipped in 2026 on the current catalog, pounds by density, returns netted: 0 of 14 (measured on the cut pack) | miss |

Pair ceiling: 28.5 (weights 38 / 7 / 55, r 5: the cracker keeps the call, the 14 whole tons and the instructions,
45.0; the mirror at the default path keeps r and the instructions, 12.0; neither keeps an ask figure; measured on the
cut pack; a cracker who also reads the revision log and the payment lines, or walks the replaces column, keeps 72.5,
which stage 4's readers measure)

Mirror leakage: 0.0 per cent of ask weight

Measured by: generator/ceiling.py

## Layer 1 inventory

| Item | System that writes it | File | Natural mishandling | Effect (checks.py) |
|---|---|---|---|---|
| VOC in per cent by weight or pounds per gallon less water and exempt compounds | the suppliers' safety data sheets | the sheet master | the less-water-and-exempt figure read as pounds per gallon of product | the water-based plants more than double; Garrowby reaches 25.0, a wrong set (R2a) |
| press logs by shift and by job, a third shift across midnight | each plant's production system | the press logs | Merrion's third shift put on the day it ends | the call holds (R2b) |
| fan speed in per cent at the speed-logging historians | the oxidizer vendors' historians | the historians, the register's rated airflow | the variable-speed fans read at their rated airflow | the call holds (R2d) |
| UTC historians against local press logs | the historians | the historians | the hours joined on their UTC dates | the call holds (R2c) |
| VOC as propane against as carbon | the two testing firms | the tests | Marlow's propane figures read as carbon | the relation stops fitting one floor and the call moves (R2e) |
| capture by enclosure verification or capture test | the plants' compliance records | the register's Capture sheet | 100 per cent at every plant | the capture-tested plants lose their uncaptured VOC and the call moves (R2f) |
| Thameside Laminating, facility 0117, before 1 May 2026 | the acquired plant's old systems | the press logs, issues, tickets, manifests, the historian tags | the 0117 rows left out | Kelvedon falls to 18.9 and the call moves (R2g) |

None of these readings turns the default path into the golden call (R2h).

## Pre-ship check

1. Domain: stationary-source VOC inventory practice: a controlled press line's emissions are its uncaptured VOC plus
   what its oxidizer lets through, and an oxidizer's outlet holds near a floor, so its destruction belongs to the inlet
   it was tested at; with another field's nouns there is no captured stream, no oxidizer outlet and no fan diluting a
   control device's inlet.
2. Real work, nothing planted: every Layer 1 item is what the plants', the vendors', the testing firms' or the
   suppliers' systems write (two VOC bases, shift and job logs, fan speed against airflow, UTC historians, propane
   against carbon, two capture determinations, the acquired plant's former number); none is the decisive step
   (checks.py R2a to R2h), and every test passed its permit's 95 per cent at maximum production.
3. The step that flips the call is analytical: estimating the outlet relation the ten oxidizers' tests trace and
   reading each production day's outlet from the inlet its captured VOC and airflow imply; no clause makes the choice
   (rule 18-4-3(b) files used less destroyed, not how a test becomes a year).
4. Analyst test: every field and rule read correctly, each plant's latest test efficiency files the default three on
   the clean truth (R3a) and on the pack (R0); the decisive step alone files the golden five on the clean truth (R3b).
5. The rule files the estimand (the area's plants, their presses' VOC, calendar 2026, tons, 25 or more); the 14
   standing constructions file the golden five and the same 14 whole tons (G2); the asks' conventions are filed in
   rule 18-4-5(b), the letter and the prompt, or closed by the data (SF15 to SF22).
6. No decoy, no withheld rule against a stated one, no certified replay: no plant's 2026 press VOC or emission
   statement ships, and the permits' 95 per cent is the permits' own condition, a rung the rule's wording rules out.
7. The lesson is on no other card: nearest drivers 0.08 (task478 v7 and v6, a burner's tests carried by a supplied
   gas property or a clock since a part change), 0.06 (task181), differentiated on the card.

## Architecture 7 record (spent 2026-10-23)

Architecture 7 read each production day's oxidizer outlet from the relation the ten oxidizers' tests trace (a floor of
about 45 ppmv as carbon, 1.8 per cent of the inlet above about 2,500) at the inlet the day's captured VOC and airflow
imply, against each plant's latest test efficiency (Ashcombe 21 and Kelvedon 20 against 29 and 28). At stage 4 (zip
5ab18e48) reader A read the floor straight off the test tables (Ashcombe's 2018 two-press test holds the same 45 ppmv
at half the inlet), rebuilt each hour's outlet as the greater of the floor and 1.8 per cent of the inlet and landed the
five and all 14 whole tons, Part 2 question 1 "none" and question 6 "an analytical choice"; reader B carried each
fixed-fan unit's test outlet to the year through the register's fan-drive column (R4, six plants). Both readers kept
all 28 ask figures: the revision log read, the payment lines parsed, Haldane matched on description. The judge thread
was stopped at the spend.

## Architecture 6 record (spent 2026-10-22)

Architecture 6 set Form 27A's placement scores from the bank difficulties carried from the old platform's field-test
section (positions 61 to 70) to the positions 21 to 70 the unique items take on Northgate Assess, by the position term
the 2026 attempts measure, against the default path's difficulties as filed (29 and 18 against 30 and 19). At stage 4
reader A rebuilt every response at its delivered position, fitted the Rasch model with the anchor block fixed, found
items harder later in the test on both platforms and landed 30 and 19 exactly (29.48 and 18.50), Part 2 question 1
"none" and question 6 "an analytical choice"; it kept 13 of 62 ask figures (the system totals and some twice counts).
Reader B and the judge thread were stopped at the spend.

## Architecture 5 record (spent 2026-10-22)

Architecture 5 designated rapid price growth areas on each dwelling type's own year effect weighted by the census
stock's value, with a pooled hedonic year term as the default path. At stage 4 both readers and the judge's own
derivation took the type-by-stock aggregation by reflex (type medians or type year effects weighted by the census
stock) and missed the call only on the location control (electoral division), which the judge read as unfiled; filing
it hands all three the call, so the decisive step as designed does not stump and the one that held is a fork.

## Tried and rejected
- Architecture 6, item position effects in pre-equating (2026-10-22, spent at stage 4): reader A fitted a Rasch model
  with a position term to the rebuilt attempts and carried the field-test difficulties to Form 27A's positions,
  unprompted by any sentence. The calibration context has to be recoverable for the truth to be fair (the report's
  delivery section and both exports' positions), and once it is, an analyst who knows the field checks the effect the
  context invites; a context effect measured by an obvious model term is a reflex for the field's own analysts.
- Architecture 6 draw (2026-10-22): re-rooted on the author's standing rule (no retirement) with a fresh world. Screened
  before it and dead: a CEMS gap fill on load (guard BLOCK on pattern G12 and strategy population_selection against
  task273, same-puzzle and same-driver spent in five to seven builds, the statutory filing against task249);
  multiplicative against additive seasonality (task146, task147); a moving holiday (task162, task467, task135);
  Denton benchmarking (this slot, below); retroactive eligibility as a denominator still developing (the completion
  driver of task451 and task479 v5); Fellegi-Sunter frequency weights (set aside at task486's draw against task468's
  linker error); the oldest old by extinct generations (task228); non-detects under several limits (task189).
- Architecture 5, the stock's price change as each dwelling type's own year effect weighted by the census stock's
  value (2026-10-22, spent at stage 4): both readers and the judge's first derivation weighted dwelling types by the
  census stock by reflex (the note's "dwellings the 2022 census counts" and the census workbook by type invite it) and
  missed only on the electoral-division control, which the judge read as unfiled (r5a); filing it hands them the call.
  A stock aggregation over a tabulated type mix is a reflex once the stock is the filed population.
- Architecture 5 draw (2026-10-22): re-rooted on the author's standing rule (no retirement); the world and pack of architecture 4 kept, the decisive step moved from the constant-quality regression its reader 9 found to the aggregation that regression skips (each type's own year effect over the stock's value), with the pooled regression now the default path. At registration the v4 identity BLOCKed on own_lineage, gap population on same-puzzle and same-driver (task251 v5), shape 10 and the statutory filing (task249 v6) and filed_standard (task478 v4); redrawn as recorded in the Draw, the circular changed to settle the 2027 fund allocations.
- Ask B's reissued student ids as a 7-digit id equal to the old one plus a campus constant, linked by birth date, sex and ZIP (2026-10-21, stage 4 round 1): both readers resolved it on the person columns and kept all six headcounts (score_reader 50 per cent); re-sited so the new ids share the old form with no arithmetic tie, birth date, sex and ZIP are shared by different students, and the movers' majors are recoded, so only the four-field key resolves it.
- Architecture 1, a coordinating board's instructional grant with four parents' consolidated returns apportioned by a cost model (2026-10-21, spent at stage 4): round 1's two readers split by FTE or total credit hours and missed; both round 2 readers fitted instruction expense on credit hours by level across the standalone campuses, split each parent's return by the modelled cost and landed the call (exit 1). Pricing activity by level from the units that report alone is a strong reader's reflex once the activity file by level ships beside the combined return.
- Architecture 2, regional register error rates from an audit drawn unequally by a risk screen (2026-10-21, spent at stage 4): both readers checked the audit's composition against the register (35 per cent referred against 8), weighted each stratum to the 30 April register and landed the call; both also read the UTC times into local time and dropped the restored companies (asks 28 of 28). A sample whose composition differs from its frame on a shipped flag is reweighted by a strong reader; a stated clock and a restoration notice are seen devices.
- Architecture 3, registration offices put on a timeliness plan from a quarter's median working days with part of the quarter still open at the extract (2026-10-21, spent at stage 4): both readers censored the open applications at their age, took the Kaplan-Meier median and landed the call, and dated payments by the batch terminal day (asks 28 of 28). An open caseload shipped beside a duration cohort, with a paper saying the open ones count, is read as right-censored by a strong reader; a settlement batch file carrying the terminal day is a seen device.
- Architecture 4, areas' house price change for the rapid price growth designation read from a shifting sample of the stock (2026-10-21, spent at stage 4): reader 9 fitted log price on type, floor area, age, newness and the address point file's electoral division with a year term and landed the call; reader 10 left location out and missed; the block purchases' one consideration on every line held both readers (0 ask totals of 32). A constant-quality index is a strong reader's reflex once the note cites the handbook and the attributes ship; location one join away is not a hidden dimension.
- A district's register error rise tested with the spread of the audit's sampled blocks (2026-10-21, screened at the draw): the guard put it beside task261 (subgroup statistics from one clustered sample, their difference's error from the clusters), the same driver.
- Regional quarterly output benchmarked to annual totals by Denton against pro-rata (2026-10-21, screened): Denton's extrapolation holds the end-of-year ratio, which sits within a few tenths of a point of pro-rata's annual ratio, while a trending ratio puts the truth far from both; the separation is too small and the truth not recoverable without forecasting the ratio.
- Architecture 7 draw (2026-10-23): re-rooted on the author's standing rule (no retirement) with a fresh world.
  Screened before it and dead: gross labour-force flows corrected for reinterview misclassification (task244's
  driver); speededness on a timed form (task249's screen); a winner's curse in form assembly (task471's shrinkage
  coin flip); generic price erosion by entrant count (task484 v1's ramp, screened at task478's draw); percent-of-charges
  hospital contracts carried to each hospital's current chargemaster (the swap test reads it as any list-price
  contract); laboratory results harmonised by proficiency-test bias (the reported result is the measurement, so the
  correction is a fork); a cancer registry's completeness by the flow method (task249's screen); common-stack
  apportionment from single-unit hours (task263's unmixing); a concentration-discharge load (task452 v1, task135);
  change of support for block grades (task270, task254, task273 screens); linkage on an address the outcome changes
  (task468's linker error); calculator-type DIF and released-item drift on the item bank (architecture 6's lesson: a
  context an obvious model term measures).
- v7 stage 3, 2026-10-23: the first tuning let each oxidizer's test outlet carried to the year (its concentration on
  each day's air, or its rate over the year's hours) file the golden five, because a fixed-fan plant at the floor emits
  the same rate every day; Larkmoor Graphics was made a concentrated-test, mostly-dilute plant under 25 tons so those
  routes file six (R4, R4m, R4b).
- v7 stage 3, 2026-10-23: press VOC to one decimal: the standing family spreads up to 0.37 tons on a plant, so the
  figure is graded in whole tons, every member 0.19 tons or more from a half (G4); the CSV's used and captured
  columns went with it (free to both top responses), the CSV now the press VOC and coverage.
- v7 stage 3, 2026-10-23: the tuned plants landed on whole tons (29.00, 37.00); moved to ordinary offsets (G5). Days
  below the tests' lowest inlet at three plants opened an extrapolation fork (interpolated efficiency against the
  floor); the low days were raised inside the tested range.
- Architecture 7, 2026-10-23: spent at stage 4. The decisive relation was visible inside one oxidizer's own tests (the
  same outlet at two inlets) and in the register's fan-drive column, and a regenerative oxidizer's outlet floor is
  field knowledge both readers carried; the asks' devices each sat one file away from a careful reader's path (the
  master's revision log in the same workbook, the washer gallons in readable payment text, descriptions beside the
  renumbered items). Next architecture: a decisive step no table displays as a pattern and no column labels.

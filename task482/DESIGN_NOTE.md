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
- **Shape:** `01`, every candidate's figure and verdict and the first below the line: fourteen plants' 2026 press VOC,
  in or out, the nearest plant under 25 tons; the asks on populations the call never reads (the plants' VOC outside
  their presses, and their combustion emissions), a chart's named parts and the three files. About 50 criteria,
  sized at stage 2.
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
a plant renamed after an acquisition, its older returns under the former name. Each is written by the system named,
none is placed to be caught, and each read the natural wrong way leaves the call where it is (checks.py, stage 3).

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
destroyed. The family the rule leaves open, measured on the generator's clean truth at stage 3 (checks.py R3): the
enumerated family (each plant's latest test, the mean of its tests, the permit's minimum efficiency, the floor
relation at the year's mean inlet, the floor relation day by day, a smooth outlet-against-inlet fit day by day) spans
three designated sets; the standing family the data leave defensible (the outlet relation carried to each day's
inlet, by any functional form the tests support) files one set, and what rules out the tested-efficiency routes is
the tests' own outlets, which hold within a narrow band across the dilute tests while their inlets vary several fold.

Analyst test: a strong analyst who conforms every purchase to pounds of VOC from its safety data sheet, every press
log to daily VOC used, applies each plant's capture determination and reads the draft rule and the information
request correctly applies each plant's latest oxidizer test efficiency to its 2026 captured VOC and names Carrow
Gravure, Merrion Flexibles and Ravensbrook Gravure Packaging; only each operating day's outlet read from the floor
relation at the day's inlet adds Ashcombe Flexible Packaging and Kelvedon Laminates (checks.py R3a on the generator's
clean truth, set at stage 3).

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

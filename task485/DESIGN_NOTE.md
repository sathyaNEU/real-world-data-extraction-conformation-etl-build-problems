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
  regions (minister_or_cabinet) for the spreading season that opens in January (season_or_peak), the Department is the
  organisation (government_agency), the requester heads the Department's Ammonia Programme Unit (programme_officer),
  and the stakeholder's own file is the programme's designation rules (filed_standard).
- **BLOCKs differentiated on the card** (similarity rules only, never an axis): `test.same_puzzle_older` and
  `test.same_driver_older` (population, pattern D, designation_set and etl_conformance) against task181 v4 (crossings of
  moving units), task229 v1 (a shared-node standard error), task98 v3 (units chained by distance) and task70 v1 (a
  per-record date rebuilt from a movement log). None places a unit's days across places by a seasonal stage.
- **WARNs answered.** `three_rules.strategy_risk` (grain_or_unit): the analyst test below is a route that reads every
  field and rule correctly and still files the wrong regions, because the census counts every animal correctly and the
  factor is right for an animal that stays put. `overuse.org_family` (government_agency in 40 builds): the programme is
  the Department's and the Minister designates under it; no other body decides a region's measures. `repeat.deliverables`
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
  region's season and at grass outside it. A large share of lowland youngstock is not: they go out on upland and
  western grazing lets in May and come home in October, so the census counts them where they graze and their whole
  housed season, which is most of a beast's ammonia, falls in the lowland region that winters them. Upland suckler
  calves born in spring leave for lowland finishers in October, so they are counted upland but are never housed there,
  and dairy bull calves leave for rearers within weeks of birth. Placing each animal-day in the region where the animal
  is that day, at the housed rate inside that region's housing season and the grass rate outside it, from the
  register's movement histories, takes the upland regions under the line and puts lowland dairy regions over it.
  Averaging the register's count over the year moves the days but not the season: it still files the uplands over the
  line, because their summer grazers' housed-season ammonia arises where they winter.
- **Data-native sentence (paper prototype, restated at stage 2):** the census route puts the three upland regions'
  cattle ammonia 25 to 29 per cent above what their animal-days give, the mean of the register's count over the year
  still 9 to 11 per cent above, and it puts the lowland dairy regions 5 to 6 per cent below; the three routes file
  three different sets of regions.
- **People:** drawn with `guard.py names --geo ie --seed 485` (Gary Farnon, Tiegan Ferry, Emily McAleer, Anna McKenna,
  Eimhear Rhattigan, Kerri Cunneen, Aislinn Mullane, Graham Mansfield, Noel Herity, Pearce Delaney): Emily McAleer,
  head of the Department's Ammonia Programme Unit and requester; Noel Herity, the National Bovine Register's data
  manager, who supplied the exports. Owners in file properties and sign-offs only.

## Three rules

Task type: Physical & Environmental Sciences, emissions-inventory, which serves ETL in the taxonomy (a regional inventory conformed from the bovine register's animal and movement exports, the June census by holding, the herd and land parcel registers, the housing seasons and the inventory's factors).
Domain test: the quantity that decides is each region's ammonia from cattle manure over the programme year per hectare of farmed land; the field estimates it by the inventory's mass-flow stages (housing, storage, spreading, grazing) on activity data, and for a herd that moves with the seasons the activity data are animal-days by region and stage rebuilt from the movement register, not the census day times the region's factor per head.
Swap: "which of 12 health boards' hospital infections per 1,000 bed-days exceed the line" (patients for cattle, bed-days for animal-days) leaves nothing to place: a patient's day carries no rate set by the season and the ward it falls in, so the census day stands for the year and the step has nothing to act on.
Layer 1: the register in two exports (one row per animal with birth and exit dates, one row per movement with departure and arrival dates that can differ by a day), marts and dealers' premises as intermediate herds on many moves, herd numbers reissued when a holding changes hands and farmers keeping more than one herd number, the herd register's region codes revised in 2024 with the census still on the old codes, the census keyed by the statistics office's farm number and joined to herd numbers through the herd register, census categories against the categories the register implies from sex, breed, age and calving, the inventory's factors in kilograms of ammonia-nitrogen against the programme's line in kilograms of ammonia, day-month-year dates in the register and ISO dates elsewhere, the programme year from November to October against the census's June date, and farmed area by herd with commonage shares split across herds; each written by the system that holds it, none placed to be caught, each asserted neutral on the call (R2).
Layer 2: field_method, exposure windows: the activity data an inventory multiplies by its factors are the animal-days in each stage in each place; the choice that flips the call is rebuilding them by region and housing stage from the movement histories rather than taking the census day times the region's annual factor, or an average count times it.
Decisive step: recognising that the inventory's annual factor per head holds only for an animal kept in one region all year, and placing each animal-day in the region where the animal is that day, at the housed rate inside that region's housing season and the grass rate outside it, from the bovine register's movement histories.
Not semantics: with every field read correctly (herd numbers across both exports and the census's farm numbers, the 2024 region codes, the categories, ammonia-nitrogen against ammonia, the programme year), the census route still files the wrong regions, because the census counts every animal correctly on 1 June and the annual factor is correct for an animal that stays put; no field records that an animal's housed season falls in another region, and the register's 1 June stock agrees with the census.
Not rule application: no filed rule places an animal's days by region and stage; the methodology's regional factor per head and the census are the stated route, and executing them files the wrong set. On the paper prototype the enumerated family (the census times the annual factor; the register's 1 June stock times it; the register's mean count over the year times it; animal-days at each location's housing season; animal-days at the home region's housing season) files four distinct designated sets of the twelve regions, and the standing family (animal-days placed at the season of the region the animal is in, as the estimand and the closure sentence file it) files one, a spread of zero; the easy route sits outside that family because the register refutes it, so unanimity is the cell the build wants (stumping 1.1), and what rules it out is quiet: no column or summary states the seasonal flows, which show only when the moves are aggregated by month and region against the census day.
Analyst test: a strong analyst conforms the 1 June 2026 census holdings to regions, applies the inventory's annual ammonia factor per head by category and region, divides by each region's farmed area and designates the regions at or over the line, filing the upland regions where lowland youngstock spend the summer and missing lowland dairy regions that house them all winter (the default path's `Ends on:`).
Estimand: each region's ammonia from cattle manure arising in the region from 1 November 2025 to 31 October 2026, in kilograms of ammonia per hectare of the region's farmed land, against the programme's line; filed in the programme's designation rules, with each stage's emissions arising where the animal is on the day, as the inventory methodology's mass-flow states it.
No decoy: nothing is planted to be caught: the census counts who it counts on 1 June, the register records every move as the herds and marts report it, the methodology's factors are correct for an animal kept in one region, and no memo, draft, briefing or stakeholder figure argues the census route.
No certified replay: the method is not recovered by reproducing published figures; the census tables and the inventory's national total are context, and the national total is the same under every route to within a few per cent, so no published figure separates the routes.
Lesson: a regional inventory of a herd that moves with the seasons has to place each day's emissions where the animal is that day and at the rate of the stage it is in there; the census day hands a whole year's housed-season ammonia to the region where the summer grazing is, and an average of the animals present still leaves the housed season with the region the animal grazes in; no build on file teaches it (the card's nearest drivers sit at 0.07 and below, and no slot note screens a herd's seasonal movements).

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

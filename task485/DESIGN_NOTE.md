# task485 design note: Esklett's provisional long-term immigration by employment sector for the year to 30 June 2026, each open stay completed on earlier arrivals with the same migration history (architecture 4)

Status lives in `pipeline.json`; this note holds the design. Architecture 4, drawn 2026-10-26 on the author's standing
rule (no retirement) after architecture 3 (each scrubber's year closed on the limestone it consumed) was spent at stage
4 when both scored readers took the removal from the reagent balance. A fresh world and mechanism on the lane's
objective; the candidates screened before it are in `## Tried and rejected`. The slot's seed (ET42) was set aside at the
first draw and stays set aside.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task485.json` (architecture v4, lineage v1 to v3 spent), registered
  2026-10-26T03:15:36Z and checked again after filing (WARN only). The window the axis bans read (task137 v2, task303 v2
  and task166 v2, the live cards filed last; task486 v3, task308 v1, task269 v4 and task121 v5 are spent and skipped)
  closes the strategies population_selection, decomposition_attribution and composition_mix, the forums executive_team,
  regulator_or_inspector and committee_or_panel, the forcing events purchase_order_or_contract,
  statutory_or_regulatory_filing and launch_or_rollout, the organisations hospital_or_health_provider,
  utility_or_infrastructure and financial_institution, the roles operations_director, capacity_planner and
  finance_controller and the context artifacts capacity_report, operations_log and close_out_summary. The draw's honest
  labels clear all of them: the Council of Ministers sets the 2027 work permit quotas (minister_or_cabinet) at its
  meeting of 15 October 2026 (vote_or_meeting), the Statistics Unit is the organisation (research_or_statistics_office),
  the requester is its Chief Statistician (statistical_office_head), the stakeholder file is the Unit's published series
  of final long-term immigration by sector (published_series), and the year's count is not finished at the cut
  (maturity_censoring). The first draft carried pattern E and composition_mix, which BLOCKed against task166 v2 and are
  the less honest labels: no column holds the groups being mixed, and what the decision needs is the completion of stays
  still open at the cut, so the pattern is none and the strategy maturity_censoring.
- **BLOCKs differentiated on the card** (similarity rules, never an axis): `test.same_puzzle_older` against task100 v2,
  where a member's exit is fixed by a course structure and found by matching the member to the prior period's snapshot,
  and `test.same_driver_older` against task136 v1, where an intervention's enrolments overstate its addition against
  sites not yet treated; here nothing fixes a stay's length and nothing is treated: a provisional count of stays reaching
  twelve months is completed from the year-before arrivals' retention, which the arrival's own migration history splits.
  Nearest drivers 0.07 (task466, task471 v4) and 0.06.
- **WARNs answered.** `repeat.deliverables` (png and xlsx, as task166 v2): the Unit's provisional release is a workbook
  of the table and one chart for the Council paper, which is what a statistics office sends a cabinet.
  `repeat.question_form` (which, as task486 v3): the Council names the sectors whose quotas it cuts, so the question asks
  which.
- **Pairing:** Survey Research & Official Statistics / `census-register-administrative-data-quality`, drawn for Data
  Extraction & Conformation (ETL). The deliverable is the conformed provisional table of long-term immigration by
  employment sector for the year to 30 June 2026, built from the Population Register's current extract and its legacy
  archive (two systems, two registration numbers and a crosswalk), the 2019 and 2026 sector lists, and the Unit's final
  series for earlier years.
- **The decision and the quantity:** Esklett, a self-governing island of about 86,000 people in the Irish Sea, sets
  each employment sector an annual allowance of long-term immigration in its Population Policy 2024 to 2028. Where a
  sector's provisional long-term immigration for the year to 30 June exceeds its allowance, the Council of Ministers
  cuts the sector's work permit quota for the next calendar year by the excess. Long-term immigration counts the
  arrivals whose stay on the island lasts twelve months or more (the UN's twelve-month usual residence rule, as the
  Unit's methods set it for a register count). At the provisional release the register is cut at 31 August 2026, so the
  arrivals of July and August 2025 have run their twelve months and every later arrival still on the island is open:
  its stay has to be completed from the year-before arrivals.
- **Timing (the pack's present is early October 2026).** The Population Register's extract of 30 September 2026 holds
  every stay to the 31 August cut; the Council meets on 15 October. The call is forward facing: the quantity is the
  number of 2025-26 arrivals whose stays will reach twelve months, most of which have not yet run.
- **Shape:** `10`, a scorecard against thresholds: each of eight sectors' provisional long-term immigration against its
  allowance beside the call.
- **The default path holds the field's method (stumping 1.1b).** A provisional register count completes each open stay
  at the chance that an arrival still present after the same time goes on to stay twelve months, read from the last
  cohort whose stays are all resolved, by the domain the figure is published for: here each sector's 2024-25 arrivals
  by whole months present. That is the life-table completion a migration statistician builds first, and it files
  construction, health and social care and retail over their allowances beside the three sectors that are.
- **The decisive step:** an arrival whose previous stay on the island ended within the twelve months before it arrived
  is a returning circular worker, and returning workers almost never stay twelve months: in the 2024-25 arrivals they
  stay a year one time in twenty-five against one time in two for the sector's first arrivals. From the autumn of 2025
  the island's care, construction and retail staffing agencies re-placed their workers after a short break rather than
  recruiting new ones each season, so returning workers' share of those sectors' arrivals doubled, to about a quarter,
  while their placements (under eleven and a half months) keep every one of them on the island at the cut. Completing
  each open stay on the 2024-25 arrivals with the same migration history (whether a stay ended in the twelve months
  before arriving, rebuilt from the person's earlier stays across both register systems) puts those three sectors under
  their allowances. No column carries the history and the Unit's classification sentence ("each stay is classified on
  its own length, whatever the person's earlier stays") is true and makes the earlier stays look beside the point.
- **Data-native sentence (prototype, seed 23, to be restated from the generator):** the sector-by-months completion puts
  construction at 320, health and social care at 451 and retail at 185 against allowances of 295, 420 and 170; the
  completion that conditions on migration history puts them at 269, 381 and 154, because returning workers make 26 to 28
  per cent of their 2025-26 arrivals against 12 to 13 per cent in 2024-25.
- **People:** drawn earlier with `guard.py names` for the slot (Conor set aside on the guard's first-name warning against
  task245): Jean Grant, Chief Statistician of the Esklett Statistics Unit and requester; Gordon Hope, manager of the
  Population Register, who signs the extract specification; Melanie Hilton, head of population policy in the Cabinet
  Office, who signs the Population Policy's allowance schedule. Owners in file properties and sign-offs only.

## Three rules

Task type: Survey Research & Official Statistics, census-register-administrative-data-quality, which serves ETL in the taxonomy (a register-based migration statistic conformed from a population register's two systems, its crosswalk and two sector classifications, completed for stays still open at the cut).
Domain test: the quantity that decides is each sector's long-term immigration for the year to 30 June 2026 under the twelve-month rule, most of whose stays have not yet run; official migration statistics completes a provisional register count by modelling each traveller's final migrant status from what is known at the cut, travel history included (the outcomes-based measures' own practice), and the decisive step is conditioning that completion on the arrival's own migration history.
Swap: "which hotel departments' long-staying guests exceeded their allowance" (guests for migrants, a hotel for the island) loses the twelve-month usual residence rule, the sector of employment a work permit quota is set on and the circular labour migration whose earlier stays decide the completion, so the task stops making sense.
Layer 1: the register's current extract and its legacy archive from before the 2023 system move (legacy registration numbers through a crosswalk, day-first dates in the archive, stays open at the move closed in the archive and reopened in the extract), leaving notices filed in September for departures before the cut, declared arrival dates beside later registration dates, the 2019 sector codes on registrations before 1 January 2026 with several merged into one 2026 sector, dependants under their sponsor's number with no sector, and two parishes merged in 2025. Each is how a register's systems hold their records; none is placed to be caught, and none moves a sector across its allowance once read correctly.
Layer 2: field_method, the completion of a provisional migration count done right: an open stay's chance of reaching twelve months is read from earlier arrivals with the same migration history, not from its sector's retention by time present; the choice that flips the call is conditioning on whether the person's previous stay ended within the year before arrival.
Decisive step: recognising that a returning circular worker's chance of staying twelve months is a twenty-fifth of a first arrival's and that returning workers' share of three sectors' arrivals doubled in 2025-26, so the completion is conditioned on each arrival's migration history rebuilt from its earlier stays.
Not semantics: with every field read correctly (the crosswalk, both date formats, the move's split stays, the late leaving notices, the sector code merges, the dependants), the sector-by-months completion still files construction, health and social care and retail over their allowances, because it reads the 2024-25 arrivals' retention correctly and that retention is right for the mix of arrivals the 2024-25 year had.
Not rule application: no filed rule names the conditioning; the methods note files the estimand (arrivals in the year to 30 June 2026 whose stay lasts twelve months or more, each stay on its own length, open stays completed from the 2024-25 arrivals given what the register shows of each at the cut) and leaves the completion to the compiler. Enumerated family on the prototype: every arrival counted (8 sectors over), resolved stays only (0), every open stay counted long (6), sector retention, sector by whole months, sector by arrival month and months, a pooled Kaplan-Meier on the 2024-26 arrivals and the 2023-25 reference (6 each, the default set), and the history-conditioned completion (3), so the enumerated spread runs to eight sectors and three between the history-conditioned completion and every route without it; the standing family (the completions that hold the reference's own split by history: a previous stay ended within six months, within twelve months or at any time, with or without months present, on the 2024-25 or the 2023-25 arrivals) designates the same three sectors in five of five members and spreads at most 16 arrivals on any sector; the ruling-out is quiet, because only the self-join that rebuilds the history shows the returning workers' retention.
Analyst test: a strong analyst conforms both register systems through the crosswalk, counts each sector's arrivals in the year to 30 June 2026, resolves those whose twelve months had run or who had left by the cut, and gives each open arrival the share of the 2024-25 arrivals of its sector still on the island after the same whole months who stayed twelve months; that files construction, health and social care and retail over their allowances beside hospitality, financial services and digital, because the returning circular workers, whose share of those sectors' arrivals doubled in 2025-26, are counted at the rate of the first arrivals among whom the 2024-25 retention hides them.
Estimand: each employment sector's long-term immigration for the year to 30 June 2026: the arrivals registered to work in the sector whose arrival date falls in the year and whose stay on the island lasts twelve months or more, stays still open at the 31 August 2026 cut counted at their chance of reaching twelve months; against the sector's allowance in the Population Policy's schedule; filed in the Statistics Unit's methods note for the provisional release and the Population Policy's allowance schedule.
No decoy: nothing is planted to be caught: the register records every arrival and departure as its two systems hold them, the 2024-25 retention is computed correctly by any route, the agencies' re-placements are ordinary stays, and no memo, draft, briefing or stakeholder figure states or ranks a sector's 2025-26 figure; the published series holds final figures for completed years only.
No certified replay: the method is not recovered by reproducing certified or published figures; the published series is of final counts that need no completion, and no earlier provisional release is shipped.
Lesson: a provisional count's completion is only as good as the reference's mix, and the person's own earlier records are the covariate a register holds that no column shows; no build on file completes a censored count on a history rebuilt from the unit's own earlier spells (task482 v14 completed open inpatient episodes by length of stay so far, task471 v4 read a register's presence from signs of life).

## Architecture 3 record (spent 2026-10-25)

Zip 9263b80dcd8ccb1c8722ce81d63f66d3 (checks.py 77 PASS, verify.py 48 of 48, byte-identical rebuilds, precut 51 checks
with no FAIL, pair ceiling 30.2 by ceiling.py, leak.py REVIEW with no LEAK, guard heart WARN, surface exit 0, the H21
rename of 33 invented names). Round 1: both scored readers (sonnet, medium, fresh copies) read the guidance's section 3.1
("less the sulphur dioxide its abatement plant removed over the year"), set the design and the one-day test removals
aside as not covering the year, and took each scrubber's removal from the limestone balance: the 2026 tickets plus the
first quarter's opening less the fourth quarter's closing silo stock, each ticket at its ISO week's certificate as
delivered, over the guarantee schedule's stoichiometry at 64.066 grams a mole. Both landed the golden six with all 18
boilers' tonnes and listings (score_reader FAIL on both); ask A held at 1 of 32 on both (the one coincidental share),
both counting Whinmoss's lines that bill a local contractor's collection beside the local's own record. Both called the
step an analytical choice nothing in the pack states and named "over the year" as the words that set the test aside.
The judge thread was stopped at the spend. Lesson: a reagent consumed in a fixed ratio to what the device removes,
recorded for the whole year beside a governing sentence that measures the year, is the careful analyst's first route to
the removal, not a step past a finished-looking default; the one-day test reads as a snapshot against the year, and the
silo stocks, the weekly certificates and the stoichiometry column lay the balance out. This draw's own screen had set
AdBlue dosing aside for the same reason (a fleet's reagent sits beside its fuel and reads at once); a stationary
scrubber's reagent sits beside its coal the same way. The readers' realism notes: load weights in narrow bands (coal 27.5
to 32 tonnes, limestone 26.0 to 29.6), one analysis shared by every truck of a certificate, weekly carbonate in a narrow
band, the tests evenly spaced, and Whinmoss's repeated 26.0 tonne lines (the device's standard loads, noticed and not
acted on).

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
- 2026-10-25, architecture 3 draw, screened and set aside before the scrubber balance: a gas bill's therms split by the
  daily profile (task123's calendarisation), register over-coverage by signs of life (screened in task478's and
  task482's notes), extinct cohorts for the oldest old (task173, task271), rater severity (task471 v2), pooled tests
  (task188), a common stack's units unmixed from single-unit hours (task263), a warranty's usage clock against months in
  service (task478 v6's hours since renewal, landed), a flare's destruction read from steam dilution (task478 v7's
  driver: a rate set by a metered condition, read on test days), AdBlue dosing against type-approval NOx (a fleet's
  reagent sits beside its fuel and reads at once), a district heat network's fixed losses (no ETL task type, and the
  loss model forks on ground temperature), a heat pump fleet's coefficient of performance integrated over the hours (no
  ETL task type), the time-of-observation bias in manual maximum thermometers (the carry-over day's true maximum is
  unobserved, so every correction forks), a continuous monitor's flow bias read from the fuel's carbon balance (an
  instrument bias is Layer 1 cleaning, never the stump), and the scrubber balance read from gypsum to landfill (the waste
  return's FGD code names the link).
- 2026-10-25, architecture 3 stage 3: two suppliers' laboratories reporting sulphur on an air-dried basis with the
  moisture beside it, set aside before the pack was cut. A scrubber that runs all year passes about 5 per cent of its
  flue gas sulphur, so a basis misread moves that boiler's tonnage about twentyfold and would carry the call, which
  Layer 1 may not; every supplier now reports as received. Per-truck certificates set aside too: a supplier's
  laboratory analyses a day's dispatch or a train as one lot, so the trucks and wagons of one dispatch share a
  certificate.
- 2026-10-25, architecture 3 (each scrubber's year closed on the limestone it consumed, against its one-day test removal
  carried across the year), spent at stage 4 round 1: both scored readers took the removal from the reagent balance,
  reading the test as a snapshot against the guidance's "removed over the year", and landed the golden six with every
  boiler's tonnes. A consumable whose year is on record beside a governing sentence that names the year is the first
  route, not a skipped one.
- 2026-10-26, architecture 4 draw, screened and set aside before the returner completion: chain-linked volume indices
  across a base-year change (a stated formula executes the answer), a space-mean against a time-mean speed from loop
  detectors (a textbook conversion the reader states), trip chaining in a travel diary (the textbook linking rule is
  rule application), a coincident peak's share of a network charge (the settlement calendar names the hours), age and
  digit heaping in a register's birth dates (spent in task230's screen), and a shared control's capacity split across
  premises (task486 v3's density driver). Not drawn.
- 2026-10-26, architecture 4 draw, the returner completion prototyped five ways before the card was filed. With every
  arrival on six- to ten-month placements and a flat circular intake, the history-conditioned completion and the
  sector-by-months completion differed by 10 to 20 on sectors of 200 to 400 (smaller than the family's own spread); with
  returns concentrated in the 2025-26 year the gap widened to 35 to 70 but the 2025-26 returners' early departures
  showed in the cohort's own first months (6 to 9 per cent left within six months against 3 to 5 per cent), which a
  pooled Kaplan-Meier on the current arrivals partly reads; with placements of nine and a half to eleven and a half
  months no returner leaves before the cut, the first months match between cohorts (3 to 5 per cent both years), and
  the gap holds at 40 to 70 on care and construction and 25 to 35 on retail, the history-conditioned family agreeing to
  within 16. The chain ladder on the July and August 2025 arrivals scatters by 30 to 120 on a sector between seeds and is
  set aside as a route.

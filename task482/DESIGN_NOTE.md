# task482 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 9, drawn 2026-10-23 after architectures 1
to 8 were spent at stage 4: a fresh world and pack in the ETL objective, a mid-sized Ontario city's bike-share
programme naming its Q1 2027 priority stations from each station's share of Q4 2026 service minutes with a bike in
working order docked.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task482.json` (architecture v9, lineage v1 to v8 spent), registered
  2026-10-23 after a fetch of main, `check` re-run on the filed card: WARN, no BLOCK. The first draft carried G3 as its decisive generator and BLOCKed on `ban.pattern` against
  task275, `test.own_lineage` against this slot's v8 and `test.same_driver_older` against task477; the decisive
  generator is G12 (absence of record against record of absence: a renter's choice not to take a bike is the record),
  which is the honest one, with G3 (the feed's record against the fleet's operation) as the frame. Against G12 the
  older task270 v2 and task192 v3 repeat gap, pattern and decision type or Gate G and are answered on the card:
  task270 scales a reported count by a size distribution and task192 carries a validation batch's rates; here nothing
  is scaled or carried, a listed bike's working order is read from renters' choices among the bikes in front of them.
- **WARNs answered.** `repeat.gate_g` and `overuse.gate_g` (method or model selection, against task275): the decisive
  step is an estimate of a state no record holds, which is what the mechanism names; no other mechanism on the list
  carries it. `repeat.question_form` (which, against task275): the decision is a set of stations, so the question asks
  which. The deliverable set was moved off svg plus xlsx (task483) and png plus xlsx (task179, task275) to a workbook
  and an HTML chart page, the form a city publishes its station figures in.
- **Pairing:** General Statistics & Data Science, task type `data-integration-record-linkage-entity-resolution`, which
  serves ETL, through the supply-chain-logistics house domain's transportation network: the operator's station status
  feed archive, its trip records, its van moves and the station register conformed into the agreement's monthly
  availability file for each public station, the file the priority designations read. Four records of one fleet are
  integrated by reading each docked bike's state from what the renters at its station did.
- **The decision and the quantity:** the City of Wellhaven's bike-share programme runs about thirty public stations and
  360 bikes (classic bikes and e-assist bikes) under an operating agreement with Northlane Mobility. Schedule C of the
  agreement makes every station that had a bike in working order docked for under 90 per cent of a calendar month's
  service minutes (6:00 to midnight local) in Q4 2026 a priority station for Q1 2027: the operator keeps a rebalancing
  crew within ten minutes of each priority station through the weekday peaks of February to April 2027. The quantity
  is each station's monthly share of service minutes with a bike in working order docked; the call is the set of
  stations under 90 per cent in a month of the quarter. Forward facing: the set fixes where the crews stand through the
  spring ramp-up.
- **Shape:** `07`, a grid: each station's availability in each month of the quarter, the stations designated, the
  nearest station clear of the line and its margin; asks on records the call never reads (fixed at stage 2), a chart's
  named parts and the two files. The station count and the graded cells are fixed at stage 2 from the simulation so the
  criteria clear 25 on structure.
- **Strategy:** `other` (no family on the list states it: a unit's usable state, held in no record, is read from users'
  choices among the units in front of them); Gate G `method_or_model_selection`; gap `objective` (the feed's count is
  correct for what the operator knew and is not the bikes in working order the designation is decided on); pattern
  none; generators G12 (decisive) and G3. Layer 2 family `estimation_fit`, pattern `own:a listed unit's unusability read
  from users passing it over for units of its own type`. Calibration organ: none.
- **World:** an Ontario city, CAD; the City of Wellhaven's Transportation Services and its bike-share programme; the
  operator Northlane Mobility; the payment processor and the van telematics vendor named at stage 2. People from
  `guard.py names --geo canada --seed 482`: Audrey Bautista (the City's bike-share contract manager) and Lawrence
  Hughes (Northlane's general manager for Wellhaven). All invented names are screened against real organisations,
  products and places before any reader sees the pack (H21).
- **Forcing fact:** Schedule C has the City name the next quarter's priority stations by 15 January 2027, from the
  quarter just closed.
- **Forum and forcing event:** customer_or_counterparty (the City designates under the agreement and the operator is
  bound by the notice), purchase_order_or_contract. Organisation local_government; role procurement_lead (the contract
  manager administers the agreement's schedules).
- **The physics:** a bike that breaks on a ride (a flat tire, a slipped chain, a seized brake) is docked by its rider at
  the end of the ride. About a third of riders report it in the app, and the operator takes a reported bike out of
  rental within about two hours, after which the feed counts it in `num_bikes_disabled`. An unreported broken bike stays
  in `num_bikes_available` until a mechanic's station check or a rebalancing visit finds it and the van takes it to the
  depot, hours to days later. Renters look at a bike before they unlock it, so while a broken bike is docked every
  renter at its station takes another bike; at a busy origin station the working bikes go first and the broken one is
  left as the last bike listed. The feed then shows the station with a bike available, raises no empty alert, and the
  van is not sent; the station is empty to every arriving renter until a returning rider docks a bike or a scheduled
  visit removes the broken one.
- **Data-native sentence:** in the trip records a broken bike shows only as a bike that stays docked while renter after
  renter at its station rides away on another bike of the same type, until the van takes it to the depot.
- **Default path and golden, by count:** the feed's available bikes taken as the bikes in working order designate the
  two stations rebalancing left short; the same feed with the passed-over bikes taken out of it designates about six,
  the busiest origin stations where broken bikes were left as the last bikes listed. Names and figures are set at the
  build from `generator/figures.json`.
- **The WHAT screen.** Population: the public stations in service in Q4 2026. Outcome: the minutes of service hours with
  a bike in working order docked (a bike a customer can unlock and ride). Unit: per cent of the month's service
  minutes. Window: each calendar month of Q4 2026, 6:00 to midnight local. Comparison: 90 per cent. The decisive step
  settles none of them: it is which docked bikes were in working order, which no record or filed rule states.
- **Sources, one line each:**
  - the General Bikeshare Feed Specification's station status fields (`num_bikes_available`, `num_bikes_disabled`,
    `num_docks_available`, `last_reported`);
  - bike-share operations practice: riders' problem reports in the app, mechanics' station checks, and rebalancing
    dispatched on the feed's empty and full alerts;
  - operators' published trip export layouts (one row per trip, the bike, its start and end station and times).
- **Same-puzzle and same-driver tests:** (objective, G12, designation_set) and (objective, G12,
  method_or_model_selection) against the last twelve builds, lineage included: no match in the last twelve; the older
  task270 v2 and task192 v3 matches are differentiated on the card.
- **Abstraction test:** the nearest drivers stripped of nouns: task230 v1 reads a switch's effect against users not yet
  switched; task478 v1 completes a count no instrument recorded by the units that passed; task471 v3 weights a trait
  sampled from two overlapping lists; task486 v2 counts distinct units joined only by pairwise findings. Here nothing is
  completed, weighted or linked: the listed count is kept, and the listed units that users passed over for units of
  their own type are taken out of it minute by minute.

## Default path

1. Read Schedule C: a station is available in a minute of service hours (6:00 to midnight local) when a bike in working
   order is docked there; a station under 90 per cent of a month's service minutes in any month of Q4 2026 is a
   priority station for Q1 2027.
2. Took the status feed archive (one poll a minute, `last_reported` in UTC epoch seconds), converted to local time,
   filled the spells the City's poller was down from the trips and van moves, and kept each public station's minutes
   inside service hours.
3. Took `num_bikes_available` (the bikes the operator had not taken out of rental, the disabled ones already excluded)
   as the bikes in working order docked; a minute is available when it is at least 1.
4. Divided each station's available minutes by the month's service minutes and listed the stations under 90 per cent
   in any month.

Ends on: two priority stations, the two rebalancing left short (names set at the build).

Golden: about six priority stations, those two and the busiest origin stations where broken bikes were left as the last
bikes listed (names set at the build).

## Stump sentence

The default path counts a station available in every minute the status feed lists a bike there and designates two
priority stations; a bike that breaks on a ride is docked by its rider and stays listed until the operator's van takes
it to the depot, and at the busiest origin stations every renter in between took another bike of its type, so read
from those choices, with the minutes when only such bikes were docked counted as empty, about six stations fall under
90 per cent in a month of the quarter.

## Three rules

Task type: data-integration-record-linkage-entity-resolution (General Statistics & Data Science), through the
supply-chain-logistics house domain's transportation network, a task type serving Data Extraction & Conformation
(ETL): the operator's station status feed archive, trip records, van moves and station register conformed into the
agreement's monthly availability file for each public station, the file the priority designations read.

Domain test: the deciding quantity is each station's monthly share of service minutes with a bike in working order
docked; integrating the feed with the trip records reads each docked bike's working order from the renters' own
choices (a bike every renter at its station passes over for one of its type is one nobody can ride), and the generic
count of the bikes the feed lists designates about a third of the stations the golden does.

Swap: General Statistics, so the swap is of the method: replace the choice-read working order with the feed's listing
and the designated set falls from about six stations to two; with another field's nouns ("beds open" for "bikes
docked") there is no renter choosing among the units in front of them, and the evidence the decision rests on is gone.

Layer 1: the status feed archive the City's poller kept at one-minute intervals in UTC epoch seconds, with spells when
the poller was down; trips exported in local time across the 1 November 2026 clock change; a station relocated in
November under a new station ID and the same name; staff and test rides in the trip export; e-bike IDs carried with a
prefix in the van log and without it in the trips; a dock expansion at two stations in the quarter; one November week of
trips repeated by a re-export; and in the ask files the payment processor's and the van telematics vendor's own
layouts (fixed at stage 2): each is what these systems write, none is placed to be caught, and none moves the call when
handled the obvious way (to be asserted in checks.py).

Layer 2: estimation that fits the data (estimation_fit): whether a docked bike could be ridden is recorded nowhere and
has to be read from how the renters at its station chose among the bikes docked there; the feed's count counts every
broken bike the operator had not yet found.

Decisive step: reading each docked bike's working order from the trip records, a bike passed over by renters who took
bikes of its own type from the end of the ride on which it was docked until the van took it away being out of working
order, and counting a station's minute as available only when a bike in working order was docked.

Not semantics: every field reads as written (the feed's `num_bikes_available` as the bikes the operator had not taken
out of rental and `num_bikes_disabled` as the ones it had, the trips' bikes, stations and times, the van's moves); read
correctly, the listed count still includes every broken bike the operator had not found, the easy route takes it as the
bikes in working order, and only the renters' choices, which no field states, separate the two.

Not rule application: the agreement files the WHAT (the public stations in service, the minutes of service hours with
a bike in working order docked, each month of Q4 2026, per cent of the month's service minutes, 90 per cent) and no rule
or procedure says which docked bikes were in working order. The enumerated family (the feed as listed, the feed less
the bikes riders reported, dwell cut-offs of 12, 24 and 48 hours, every bike later taken to the depot counted from its
last ride, any bike passed over, bikes passed over for one of their own type at 3 to 30 passes) and the standing family
(same-type passes at any count the data leave in the corridor, from the ride's end or from the first pass, with or
without the depot move as confirmation) are measured on the clean truth at stage 2 with their spreads on the designated
set and on every station's monthly figure; what rules out the rest is the data (classic bikes passed over only while
e-bikes were docked, bikes left alone at quiet stations and ridden when the next renter came, bikes taken from full
stations at night for storage).

Analyst test: with every field and rule read correctly, a strong analyst takes the status feed's `num_bikes_available`
at each station each minute as the bikes in working order (the operator's own count of the bikes it had not taken out
of rental), computes each station's share of each month's service minutes with one docked, and designates two
priority stations: the default path's Ends on (checks.py T1 on the clean truth, T2 on the pack).

Estimand: the operating agreement's Schedule C (Station Availability): the population (every public station in service
in Q4 2026), the outcome (the minutes of service hours, 6:00 to midnight local, with at least one bike in working order
docked, a bike being in working order when a customer can unlock it and ride it), the window (each calendar month of
Q4 2026), the unit (per cent of the month's service minutes at the station) and the comparison (90 per cent; a station
under it in any month is a priority station for Q1 2027).

No decoy: nothing is planted: the bikes broke on rides as bikes do and were docked by their riders, the feed is the
operator's ordinary status feed as the City's poller kept it, and no memo, report, draft or stakeholder figure states
any station's availability or argues for the listed count.

No certified replay: the method is not recovered by reproducing certified or published figures; the operator's monthly
report states no station's availability, and no figure in the pack ties only under the golden.

Lesson: a count of units a system lists as available includes units nobody can use; integrated with the record of what
users took, a listed unit passed over for units of its own type is read as unusable and availability is counted from
the usable ones; no build on file reads a unit's state from users' choices among the units in front of them.

## Architecture 8 record (spent 2026-10-23)

Architecture 8 carried each store's data logger record through the vaccine's thermal lag, a first-order response
fitted per logger make on the two weeks each pilot store's old logger kept recording beside its new in-carton sensor
(42.2, 42.2 and 41.9 minutes), against the loggers' readings taken as the vaccine's temperature (six stores against
ten). At stage 4 (zip ad958ec9) reader B set the pilot stores' loggers beside their in-carton sensors over the overlap
unprompted, fitted the lag as a first-order filter (0.21 of the gap closed per ten minutes, about 42 minutes) and
landed the six stores and every store's whole hours, answering question 6 "an analytical choice" on standard 7.2; it
kept every ask figure too (122 of 122 graded figures, exit 1): the counts' own closing times, the credits found when
per-item balances went negative, the vial write-offs by cost over the per-dose cost, the tax switch by the
maintenance-only invoices at Schedule B's prices, and the two-store routes split by Schedule B. Reader A and the judge
thread were stopped at the spend.

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
- Architecture 8 draw (2026-10-23): re-rooted on the author's standing rule (no retirement) with a fresh world, aimed
  at architecture 7's lesson (no table displays the decisive relation, no column labels it). Screened before it and
  dead: vessel propulsion from AIS speed over ground carried to speed through the water by an estuary's tidal streams
  (a port world beside task472 and task474, and a tidal stream table has no other use in an emissions pack, so its
  presence announces the correction); container ships' at-berth auxiliary load by the reefers on board, calibrated on
  shore power meters (a port world, and a reader calibrating on the meters sees the per-call spread with reefers its
  first explanation); a tanker's boiler load at berth by its own steam cargo pumps on discharge (the at-berth tanker
  rules' own reasoning, a reflex once the transfer log is joined); dairy lagoon methane through the lagoon's
  temperature lag behind the air (the rate model is a filed procedure, and four inspection readings a year cannot fix
  the lag deterministically); switcher locomotives' idling through the start-stop system's restart temperature (a
  rate carried across a weather covariate, task478 v7's driver); crematory mercury by the decedents' dental cohort (a
  composition mix one survey table hands over); breaker SF6 leak rates from temperature-uncompensated pressures (the
  gas temperature at each reading is not recoverable). A cold-chain prototype (thirty-six refrigerators, probe 6 minutes,
  carton 48) put the logger's own hours at two to ten times the vaccine's, the default qualifying 29 against 12, with
  a 45-minute lag fitted on ten fourteen-day overlaps at 0.04 degrees C reproducing the carton's set exactly, while 30
  and 60 minute duration filters (17 and 6) and a 45-minute moving average (20) fell elsewhere and a 90-minute moving
  average missed by one refrigerator: the stage 2 world keeps the default's count plausible and every store clear of the
  line under the standing family.
- v8 stage 3, 2026-10-23: standard 7.1 first read "the records of each store's device of record are its vaccine
  temperature records", which a literal reader takes as the logger's readings being the vaccine's temperature (an
  official decoy for the default path); it became a records-custody clause.
- v8 stage 3, 2026-10-23: under the interval-mean reading of a record's vaccine temperature five stores' whole hours
  moved by one while the call held; 7.3 now files the counting (a record counts its ten minutes by the vaccine's
  temperature at its time stamp), WHAT and not HOW (SF17).
- v8 stage 3, 2026-10-23: return credits from both manufacturers put the cracker's balance below zero at eleven
  stores, a loud failure that points at the double count; only Halvorsen's standard-dose products are returnable, the
  leftovers leaner and the unrecorded losses scaled to each store's volume (cracker 15 doses or more, A6).
- v8 stage 3, 2026-10-23: maintenance-only invoices at one price per unit type tied ten stores' service figures (a
  constant response would have kept them); per-model prices and add-on parts at some visits, every store's figure now
  distinct (B5). With the tax switch as ask B's only silent device a reader who found it kept 23 to 30 of 30; the
  pre-move two-store maintenance routes on one invoice were added, so the tax switch alone keeps 10.
- v8 stage 3, 2026-10-23: the first names sat on real organisations, products or places in or near the field (H21):
  Coldline (a refrigeration manufacturer), Polarwatch (an ocean-data programme), Vaxtor, Homeline, Arctis, Glacier
  Medical, and the acquired chains Rookwood Drug and Saltash Apothecary; renamed Tellvane, Brumal, Stellane, Keswell,
  Brannon, Pendry Medical, Vollmer Drug and Lindqvist Apothecary before any reader saw the pack.
- Architecture 8, 2026-10-23: spent at stage 4. Two instruments recording one unit side by side are compared by a
  strong reader on reflex: the pilot stores' logger and in-carton series parted at every restock and defrost swing, so
  reader B fitted a first-order lag on the overlap with no sentence asking for it. Every ask device had one natural
  check that exposed it (per-item balances, cost per unit, a list price met exactly, one invoice on two sites).
  Next architecture: a decisive step whose evidence no single side-by-side comparison shows, and ask devices that no
  per-item reconciliation or unit-price check reveals.
- Architecture 9 draw (2026-10-23): re-rooted on the author's standing rule (no retirement) with a fresh world. Screened before it and set aside: phantom shelf inventory under a vendor-managed availability guarantee (on-shelf availability is an industry term that names its own correction); a plan directory's ghost providers read from claims (the directory and the claims sit side by side, architecture 8's reflex); a starting dose as the mark of a true initiator in an outcomes contract (population_selection, in the window against task275); rectifying inspection's over-weighted rejected lots (population_selection again); left truncation of a fleet's lifetimes (task133's delayed entry for a taken-over book); GPS chord distance by terrain for fuel-tax jurisdiction miles (the call would sit on a few per cent of one state's miles); meter error read off a system balance (the instrument-bias family task478 v5 and task480 v1 lost to readers); charger uptime from failed sessions (the failure is written in the session record itself). The bike-share draw keeps the listed count correct for what the operator knew and puts the difference in renters' choices, which no record states.

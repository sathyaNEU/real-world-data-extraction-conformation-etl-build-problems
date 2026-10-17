# task465 design note: the Ardley Plains growers' 2027 area-yield drought covers

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first: the first draft
(a rainfall index with dormant gauge seasons) was superseded before any data was cut and is recorded there and in
the card's lineage.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task465.json`, re-registered 2026-10-17, guard WARN only (answered
  below). The first keying of this draft blocked on the forum and organisation family of task153 and task154 and on
  task234's pattern and context artifact (all registered by other authors since the first draft); re-keyed to the
  cooperative as the deciding organisation (its board), generators G6 and G12, a published series as the context
  artifact, and differentiated against task124, task132, task133, task144, task180, task230, task448, task456 and
  task462, whose decisive gap, pattern and decision or Gate G it shares on the card's keys.
- **Seed:** ET22 (`analytical_tasks/07_data_extraction_conformation`), world, decision and quantity kept: a farmers'
  cooperative's drought cover priced by burn analysis over the seasons since 1991. The index is the county's official
  dryland yield (an area-yield cover, an index product like the seed's rainfall cover) rather than a gauge's rainfall,
  whose own cruxes are spent (`## Tried and rejected`); the seed's mechanism (tenths of millimetres, quality flags,
  weekend totals) is not used.
- **Pairing:** General Statistics & Data Science / data-integration-record-linkage-entity-resolution / ETL. Physical
  sciences x ETL is task464's pairing in the last three, and data integration is the task type doing this work: each
  county's yield history conformed from the statistics service's county, district and state tables of the same
  statistics, whose withheld cells the tables' additive structure fixes. General statistics sets its tasks in another
  field's world, so the swap test is of the method (`## Three rules`).
- **Why this mechanism:** the ETL builds on file spent completion of open periods (445, 451, 457), capture and coverage
  of registers (448, 454, 455), links and continuity (449, 455), a link through shared items (450), a rotating panel's
  measurement change (453), a stratified sample on a revised map (452), latent classes (456), observation selected on
  the trait (458), an operating level (459), a dispatch margin (460), an overlap extension (461), detection-weighted
  snapshots (462), a drift-free price index (463) and a change in each unit's own record (464 v1). None turns on a
  publisher withholding a unit's figures in exactly the periods the decision is about, with the withheld figures
  recoverable from the publisher's own group totals.
- **Shape:** 07, a grid of cells: five county covers, each with its expected loss rate, its quoted premium rate, their
  ratio and buy-or-not; the conformed county yield record and the asks add the rest (sum at stage 2).
- **Strategy:** population_selection (the published years are a sample of years selected on the outcome: the
  withheld years are the drought years), on the population gap (which years the expected loss runs over) with the
  objective gap behind it (each quote is judged on the cover's expected loss). Generators G6 and G12. Gate G
  forecasting (each cover's expected 2027 loss).
- **World:** an invented High Plains region of the United States. The Ardley Plains Growers' Cooperative has members
  growing dryland grain sorghum in five counties (Ardley, Corvin, Elster, Pallard, Tresham) in two agricultural
  statistics districts. For 2027 it is buying area-yield covers from Quillfield Re, a reinsurer: each county's cover
  pays when the county's official dryland sorghum yield for 2027 falls below a trigger (a share of the county's
  expected yield, from the trend the term sheet fixes), in proportion to the shortfall. Quillfield Re has quoted a
  premium for each county; the cooperative's risk policy buys a county's cover only when its quoted premium is at most
  1.4 times its expected loss, the average indemnity over the 1991 to 2025 seasons with each season's yield brought to
  2027 by the term sheet's trend. The statistics service publishes county, district and state estimates of harvested
  acres, production and yield by practice, and withholds a county's figures when too few farms harvest the crop there
  (to keep any one farm's figures from being disclosed), which in the region's drought years, when dryland fields are
  abandoned, falls on the small counties. Data: the service's county estimates export 1991 to 2025, its notes on
  methods and revisions, the term sheet, Quillfield Re's quotes, the cooperative's risk policy and request, the members'
  delivery records and the region's drought monitor history.
- **Forcing fact:** the covers attach for the 2027 crop year and the board decides at its 19 November 2026 meeting; the
  call faces forward (each cover's expected 2027 loss) on a record that closes with the 2025 crop.
- **Forum and forcing event:** board_of_directors (the cooperative's board buys the covers), season_or_peak (the 2027
  crop year). Organisation cooperative_or_member_body; role finance_controller. Personas from `guard.py names --geo
  us --seed 465`: Brent Little (the cooperative's risk manager, who prepares the recommendation), Martha Dalton (the
  cooperative's board chair).
- **Data-native sentence:** the statistics service withholds a county's acres and production in the years too few
  farms harvest dryland sorghum there, and in the High Plains those are the drought years, when growers abandon their
  dryland fields; so a small county's published yield history is missing exactly its worst years, while the district's
  published totals, which include it, less its published neighbours give each of those years back.
- **WARN answers:** `repeat.decision` (designation set after task235): the decision is which covers to buy;
  `repeat.question_form` (which after task235): the decision is a pick of covers.

## Default path

1. Read the service's export: county non-irrigated sorghum harvested acres, production and yield, 1991 to 2025, the
   withheld marks as not published (not zeros).
2. For each county, fit the term sheet's trend on its published yields, bring each published year to 2027 by the
   trend, set the trigger, compute each year's indemnity rate and average them: the expected loss rate.
3. Price: the quoted premium rate against 1.4 times the expected loss rate; buy where the quote is at most that.
- **Ends on:** buys Corvin's and Pallard's covers and declines Ardley's, Elster's and Tresham's (Elster's and
  Tresham's published years leave out their drought years, so their quotes look dear against their expected loss;
  Ardley's quote is dear on every reading). Calibrated at stage 2.
- **Golden:** buys Corvin's, Elster's, Pallard's and Tresham's covers and declines Ardley's: each withheld county-year
  recovered as the district's published acres and production less the district's published counties', the trend and
  the burn run over all 35 years.

## Stump sentence

The default path prices each cover over the years its county's yield is published and treats the withheld years as
missing, so Elster's and Tresham's drought years, withheld because too few farms harvested, drop out of their burns and
it declines both covers as dear; recovered from the district totals less the published counties, those years carry
the covers' largest losses and both covers clear the board's rule.

## Three rules

- **Task type:** data integration (data-integration-record-linkage-entity-resolution): each county's yield history
  conformed from the service's county, district and state tables of the same statistics, the withheld cells recovered
  through the tables' additive structure; the ETL objective's conformed record is the dataset the quotes are judged
  on.
- **Domain test:** the deciding quantity is each cover's expected loss over the 35 crop years, which needs each
  county's yield in every year; the data-integration estimate restores the withheld years from the district totals
  less the published counties, and the burn is run on the integrated history.
- **Swap:** General Statistics, so the swap is of the method: replace the integrated history with the published years
  alone (or with withheld years filled from the district's yield) and the set of covers bought changes; a noun swap
  ("a clinic network's expected excess cost over months whose figures the registry withheld") keeps the sentence only
  where the withheld periods are the bad ones and a group total contains them.
- **Layer 1:** the value column written with thousands separators and withheld or not-published marks, a coefficient
  of variation on some rows (the service's export); data items as long strings naming crop, practice, statistic and
  unit, with dryland and irrigated rows beside all-practice rows and some years published only for all practices (the
  service's estimating programme); district and county codes with leading zeros and one district renumbered in a
  redefinition (the service's geography); preliminary estimates beside revised ones for the latest years (the
  service's release cycle); the liability written as insured acres times an expected yield and a price (the
  cooperative's request). Each is what the system that writes the file produces; none carries the call (asserted at
  stage 3).
- **Layer 2:** estimation that fits the data: a long-run average over periods, where the periods the record does not
  show are not missing at random but selected on the outcome, and the record's own group totals give them back.
- **Decisive step:** recover each withheld county-year from the district's published acres and production less those
  of the district's published counties, and run the trend and the burn over all 35 years.
- **Not semantics:** every mark, unit, code and practice read correctly (a withheld mark read as not published, not as
  zero) still leaves the easy route pricing on the published years; what moves the call is the analysis that the
  withheld years are the drought years and that the district totals hold them.
- **Not rule application:** the term sheet and the risk policy file the estimand (each cover's average indemnity over
  the 1991 to 2025 crop years, each year brought to 2027 by the trend, against 1.4 times the premium), the trigger and
  the trend; no file says how a withheld year enters, and executing every filed rule on the published years buys the
  wrong set.
- **Analyst test:** a strong analyst who reads the export correctly, applies every filed rule and detrends as the term
  sheet says prices each cover on its county's published years and declines Elster's and Tresham's covers (the default
  path's `Ends on:`); one who fills the withheld years with the district's yield files another wrong set.
- **Estimand:** the cooperative's risk policy (`ardley_plains_cooperative_risk_policy_2026.pdf`) files it: a county
  cover is bought when its quoted premium is at most 1.4 times its expected loss, the average indemnity over the crop
  years 1991 to 2025 of the county's official dryland yield, each year brought to 2027 by the term sheet's trend.
- **No decoy:** nothing is planted: the withheld years are the service's own disclosure rule at work, no memo or
  stakeholder figure argues a price, and no file ranks the covers.
- **No certified replay:** no published loss history or certified figure is shipped to be reproduced.
- **Lesson:** a published series can be missing its decisive periods by the publisher's own rule, and the publisher's
  group totals often hold them; no build on file teaches recovering withheld cells from the totals that contain them.

## Tried and rejected

- A rainfall index on cooperative-observer gauges with dormant seasons rebuilt from the airport, the decisive move
  averaging the kinked payout over the rebuilding's error: the expectation-of-a-nonlinear-payout lesson is already
  task151's (a stepped payout over the season total's distribution), task187's and task229's; superseded before any
  data was cut.
- A district index averaged over a network that grew from three gauges to seven: the variance of a three-gauge mean
  exceeds a seven-gauge mean's by only 5 to 15 per cent at the region's inter-gauge correlations, and in a prototype the
  burn's sampling noise swamped it in half the draws; no stable call.
- Station breaks (a gauge moved, an instrument changed): the change found in a unit's own record is task464's spent
  architecture.
- Carrying a short gauge record through a long airport record by the overlap's ratio: task461's driver.

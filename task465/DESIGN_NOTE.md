# task465 design note: the Ardley Plains growers' 2027 area-yield drought covers

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first: the first draft
(a rainfall index with dormant gauge seasons) was superseded before any data was cut, and the area-yield design was
re-calibrated at stage 2 (the withholding rule, the district layout and the golden set); both are recorded there and
in the card's lineage.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task465.json`, registered 2026-10-17, re-checked at stage 2 after the
  world was re-laid (WARN only, answered below). The first keying of this draft blocked on the forum and organisation
  family of task153 and task154 and on task234's pattern and context artifact; re-keyed to the cooperative as the
  deciding organisation (its board), generators G6 and G12, a published series as the context artifact, and
  differentiated against task124, task132, task133, task144, task180, task182, task189, task228, task230, task233,
  task448, task456, task461 and task462.
- **Seed:** ET22 (`analytical_tasks/07_data_extraction_conformation`), world, decision and quantity kept: a farmers'
  cooperative's drought cover priced by burn analysis over the seasons since 1991. The index is the county's official
  dryland yield (an area-yield cover, an index product like the seed's rainfall cover) rather than a gauge's rainfall,
  whose own cruxes are spent (`## Tried and rejected`); the seed's mechanism (tenths of millimetres, quality flags,
  weekend totals) is not used.
- **Pairing:** General Statistics & Data Science / data-integration-record-linkage-entity-resolution / ETL. Physical
  sciences x ETL is task464's pairing, and data integration is the task type doing this work: each county's yield
  history conformed from the statistics service's county, district and state tables of the same statistics, two
  downloads of different vintages, whose withheld cells the tables' additive structure fixes.
- **Why this mechanism:** the ETL builds on file spent completion of open periods (445, 451, 457), capture and coverage
  of registers (448, 454, 455), links and continuity (449, 455), a link through shared items (450), a rotating panel's
  measurement change (453), a stratified sample on a revised map (452), latent classes (456), observation selected on
  the trait (458), an operating level (459), a dispatch margin (460), an overlap extension (461), detection-weighted
  snapshots (462), a drift-free price index (463) and a change in each unit's own record (464 v1). None turns on a
  publisher withholding a unit's figures in exactly the periods the decision is about, with the withheld figures fixed
  by the publisher's own group totals.
- **Shape:** 07, a grid of cells: five county covers, each with its expected loss, its quoted rate as a multiple of
  that loss, the quoted rate at which the call changes and buy or decline (20 cells), the call, the chart's three named
  parts and the two files (26 before the asks); the asks add 15 figures.
- **Strategy:** population_selection (the published years are a sample of years selected on the outcome: the
  withheld years are the drought years), on the population gap (which years the expected loss runs over) with the
  objective gap behind it (each quote is judged on the cover's expected loss). Generators G6 and G12. Gate G
  forecasting (each cover's expected 2027 loss).
- **World:** an unnamed High Plains state. Its Crop and Livestock Reporting Service (the service) publishes county,
  district and state estimates of planted and harvested acres, production and yield by crop and practice; a county's
  estimate for a practice is not published when it rests on fewer than five reports or its coefficient of variation is
  above 30 per cent, and the service builds its district and state estimates up from all its county estimates,
  published or not. The Ardley Plains Growers' Cooperative's members grow dryland grain sorghum in five counties on
  the sandy ground where four agricultural statistics districts meet: Ardley (district 20, West Central), Tresham (30,
  Southwest), Corvin and Elster (50, Central) and Pallard (60, South Central). Each district's other counties
  (Brannock, Lindqvist, Pellow, Ruddock, Tolsey; Cobbett, Durrance, Kestner, Quenby, Varga; Fothergill, Gaddis,
  Iverly, Stannard; Dornick, Halvorsen, Ingleby, Rumbold, Treloar) are bigger sorghum counties whose estimates are
  always published. For 2027 the cooperative is buying area-yield covers from Quillfield Re, a reinsurer: each county's
  cover pays when the county's official non-irrigated sorghum yield for 2027 falls below a trigger (90 per cent of the
  county's expected yield in the term sheet), in proportion to the shortfall. The cooperative's risk policy buys a
  county's cover only when its quoted rate is at most 1.4 times its expected loss, the average indemnity over the 1991
  to 2025 crop years with each year's yield brought to 2027 by the term sheet's trend. Data: the service's estimates in
  two downloads (March 2024, 1991 to 2023; October 2026, 2016 to 2025, with 2017 to 2021 revised to the 2022 Census of
  Agriculture), its methods and symbols notes, the term sheet, Quillfield Re's quote schedule, the risk policy, the
  cooperative's 2027 enrolment, its elevators' scale tickets and transfer log, its member roster, a drought-monitor
  extract and its prior covers' statements (the last two declared distractors).
- **Forcing fact:** the covers attach for the 2027 crop year and the board decides at its 19 November 2026 meeting; the
  call faces forward (each cover's expected 2027 loss) on a record that closes with the 2025 crop.
- **Forum and forcing event:** board_of_directors (the cooperative's board buys the covers), season_or_peak (the 2027
  crop year). Organisation cooperative_or_member_body; role finance_controller. Personas from `guard.py names --geo
  us --seed 465`: Brent Little (the cooperative's risk manager, who prepares the recommendation), Martha Dalton (the
  cooperative's board chair).
- **Data-native sentence:** the service withholds a sandy county's dryland sorghum estimate in the years too few farms
  harvest there, and in the High Plains those are the drought years, when growers abandon their dryland fields; so
  each sandy county's published yield history is missing exactly its worst years, while the district's estimates,
  built up from every county's, less the district's published counties give each of those years back.
- **WARN answers:** `repeat.decision` (designation set after task235): the decision is which covers to buy;
  `repeat.question_form` (which after task235): the decision is a pick of covers, "none" a grammatical answer.

## Default path

1. Read the two downloads, the 2026 one for the years it holds; filter county, grain sorghum, non-irrigated; harvested
   acres, production and yield, 1991 to 2025, a withheld mark read as not published (not a zero).
2. For each county, bring each published year's yield to 2027 by the term sheet's trend, compute the year's indemnity
   share against the trigger and average the shares: the expected loss.
3. Price: each quoted rate against 1.4 times the expected loss; buy where it is at most that.
- **Ends on:** buys none of the five covers.
- Ardley's, Elster's and Pallard's published years leave out their drought years, so their quotes run 4.3 to 5.6
  times their expected loss; Tresham's runs 3.6 times; Corvin's, the one county with every year published, 1.71 times.
- **Golden:** buys Ardley's, Elster's and Pallard's covers and declines Corvin's and Tresham's: each withheld
  county-year recovered as the district's harvested acres and production less those of the district's published
  counties, and the burn run over all 35 years.

## Stump sentence

The default path prices each cover over the years its county's yield is published and treats the withheld years as
missing, so Ardley's, Elster's and Pallard's drought years, withheld because too few farms harvested, drop out of their
burns and it buys none of the five covers; recovered from the district totals less the published counties, those
years carry the three covers' largest losses and their quotes clear the board's rule, while Tresham's, its two withheld
years back in, stays dear.

## Three rules

- **Task type:** data integration (data-integration-record-linkage-entity-resolution): each county's yield history
  conformed from the service's county, district and state tables of the same statistics across two downloads, the
  withheld cells fixed through the tables' additive structure; the ETL objective's conformed record is the dataset
  the quotes are judged on.
- **Domain test:** the deciding quantity is each cover's expected loss over the 35 crop years, which needs each
  county's yield in every year; the data-integration estimate restores the withheld years from the district totals
  less the published counties, and the burn is run on the integrated history.
- **Swap:** General Statistics, so the swap is of the method: replace the integrated history with the published years
  alone (or with withheld years filled from the district's yield, the county's ratio to it or its worst year) and the
  set of covers bought changes; a noun swap ("a clinic network's expected excess cost over months whose figures the
  registry withheld") keeps the sentence only where the withheld periods are the bad ones and a group total holds them.
- **Layer 1:** two downloads of the service's export overlapping 2016 to 2023, the later one revised for 2017 to 2021
  (the service's benchmark revision); values written with thousands separators and the service's symbols, a
  coefficient-of-variation column from 2008 (the service's export); data items as long strings naming crop, practice,
  statistic and unit across six crops and three practice rows (the service's estimating programme); district codes
  one digit before the 2008 recode and two after, county codes without their leading zeros in the 2024 download (a
  spreadsheet save); the enrolment's timestamps in UTC, the ticket weights in pounds at delivery moisture and the
  price per hundredweight (the cooperative's systems). Each is what the system that writes the file produces; none
  carries the call (`## Layer 1 inventory`).
- **Layer 2:** the data's real structure, selection on the outcome: a long-run average over periods where the periods
  the record does not show are not missing at random but selected on the outcome (the drought years), and the
  record's own group totals give them back.
- **Decisive step:** recover each withheld county-year from the district's published harvested acres and production
  less those of the district's published counties, and run the trend and the burn over all 35 years.
- **Not semantics:** every mark, unit, code and practice read correctly (a withheld mark read as not published, not as
  zero) still leaves the easy route pricing on the published years; what moves the call is the analysis that the
  withheld years are the drought years and that the district totals hold them.
- **Not rule application:** the term sheet and the risk policy file the estimand (each cover's average indemnity share
  over the 1991 to 2025 crop years, each year brought to 2027 by the trend, against 1.4 times the quoted rate), the
  trigger and the trend; no file says how a withheld year enters, and executing every filed rule on the published
  years buys none of the covers.
- **Analyst test:** a strong analyst who reads the export correctly, applies every filed rule and detrends as the term
  sheet says prices each cover on its county's published years and buys none of the five covers (the default path's
  `Ends on:`); one who fills the withheld years from the district's yield, the county's ratio to it, a regression on
  it or its worst published year also buys none, and one who reads every withheld year as a total failure buys
  Tresham's too.
- **Estimand:** the cooperative's risk policy (`apgc_risk_policy_2026.pdf`) files it: a county cover is bought when
  its quoted rate is at most 1.4 times its expected loss, the average over the crop years 1991 to 2025 of the share of
  the liability the cover would pay on the county's official dryland sorghum yield for that year, each year brought
  to 2027 by the term sheet's trend; the term sheet makes the index the county's yield as the service estimates it.
- **No decoy:** nothing is planted: the withheld years are the service's publication standard at work, no memo or
  stakeholder figure argues a price, and no file ranks the covers.
- **No certified replay:** no published loss history or certified figure is shipped to be reproduced; the prior covers'
  statements (a distractor) cover Corvin's and Tresham's counties only and settle on published years.
- **Lesson:** a published series can be missing its decisive periods by the publisher's own rule, and the publisher's
  group totals often hold them; no build on file teaches recovering withheld cells from the totals that contain them.

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the published years only (the default path; buys none) | the service's symbols note: a withheld estimate is not published | `(S)` in the value column | yes: drop the missing years | no | the battery flags the marks | an average of the published shares | readable |
| R1 each withheld year filled with the district's yield, or the published counties' pooled yield (buys none) | none names a fill | district rows beside county rows | yes: fill a member from its group | no | no | one lookup per year | readable |
| R2 the county's average ratio to the district, a regression on it, or the county's worst published year (buys none) | none | the county and district series side by side | yes: impute from the published years' relationship | no | no | a ratio or a line per county | readable |
| R2x every withheld year a total failure (buys Tresham's too) | none | `(S)` | a cautious reading | no | no | a zero per year | readable |
| R3 each withheld year as the district's acres and production less its published counties' (decisive) | no: the methods note says the service builds a district's estimates up from all its county estimates, in its section on how estimates are made, not in the symbols legend; nothing says the withheld years are droughts or that a county can be had back by subtraction | no column flags a withheld year as recoverable; the export carries no "other counties" row | no: the reflexes (drop, fill from the district, impute from the published years, a total failure) land on none of the covers or on four | no | no: the battery flags the marks; a footing of counties to the district shows a residual only for someone already asking what the district total holds, and a county burn has no reason to foot it | no: two sums over every published county of the district and a ratio, per withheld year, after the question is asked | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | a county cover's index | the county's non-irrigated (dryland) grain sorghum yield | the all-practices yield | same call: the four sandy counties grow no irrigated sorghum, and Corvin's all-practices burn stays dear (asserted) | the term sheet's index definition |
| SF2 | a year's yield | bushels per harvested acre as the service estimates it, to one decimal | production over planted acres; unrounded production over harvested acres | planted acres: not the index; unrounded: same call (asserted) | the term sheet; the service's yield definition |
| SF3 | the crop years | 1991 to 2025, 35 years | 1991 to 2023 (the long download); 2016 to 2025 (the refresh) | not the policy's window | the risk policy |
| SF4 | a year the service withheld the county's dryland estimate | the county's yield as the service estimated it, which the district's estimates hold with every county's | the district's yield; a zero | district: buys none; zero: buys Tresham's too | the term sheet (the index is the county's yield as the service estimates it); the methods note (district estimates built up from all county estimates, published or not); the symbols note (a withheld estimate is not published, not nil) |
| SF5 | bringing a year to 2027 | adding the term sheet's trend per year times the years to 2027 | scaling by the ratio of trend yields; a trend refitted by the analyst | ratio: adds Corvin's cover (asserted); refit: not the term sheet's trend | the term sheet's rating basis ("each brought to the 2027 level by adding the county's trend in the table below for each year from that crop year to 2027") |
| SF6 | the trigger | 90 per cent of the term sheet's expected 2027 yield | 90 per cent of the average of the adjusted years | not the term sheet's trigger | the term sheet |
| SF7 | a year's indemnity share | the trigger less the adjusted yield, over the trigger, nil above the trigger and at most one | the shortfall over the expected yield | not the term sheet's payment | the term sheet's payment formula |
| SF8 | the expected loss | the average of the 35 shares | the average over years with a loss | not the policy's average | the risk policy |
| SF9 | the quoted rate | per cent of the cover's liability, as scheduled | per insured acre | not the schedule's basis | the quote schedule's header |
| SF10 | at most 1.4 times | quoted rate not above 1.4 times the expected loss | strictly below | same call: no cover within 1.2 of the line either way (asserted) | the risk policy |
| SF11 | an estimate in both downloads | the October 2026 download's (revised for 2017 to 2021) | the March 2024 download's | same call (asserted) | the methods note on revisions (a revised estimate replaces the earlier) |
| SF12 | the 2025 estimates | the preliminary estimates as published | left out until revised | same call (asserted) | the risk policy (crop years to 2025); the methods note (preliminary estimates are the current estimates) |
| SF13 | a district's counties in a year | the counties carrying the district's code that year, one-digit codes before 2008 read as the two-digit ones | the 2026 grouping for every year | same call: no county changed district (asserted) | the methods note on the 2008 recode |
| SF14 | a county across the two downloads | the county code with its leading zeros, or the county name | the code as written | same call | the data dictionary |
| SF15 | rounding | expected losses, multiples and rates to two decimals of a per cent, the comparison on unrounded figures; a recovered yield to one decimal or unrounded | rounded figures compared | same call and the same rounded figures (asserted) | the prompt's rounding sentence |

## Ladder

| Rung | Construction | Buys | Ardley / Elster / Pallard / Tresham expected loss, per cent |
|---|---|---|---|
| R0 | the published years only (the default path) | none | 1.25 / 1.91 / 1.00 / 2.01 |
| R1 | withheld years filled with the district's yield (the published counties' pooled yield the same to 0.02) | none | 3.16 / 3.46 / 2.50 / 3.12 |
| R2 | withheld years by the county's average ratio to the district; a regression on it; the worst published year | none | ratio 3.84 / 4.58 / 2.80 / 3.70; regression 3.84 / 4.63 / 2.56 / 3.45; worst 3.04 / 4.08 / 2.01 / 3.42 |
| R2x | every withheld year a total failure | Ardley, Elster, Pallard, Tresham | 8.25 / 9.39 / 5.99 / 6.84 |
| R3 | withheld years recovered from the district's totals less its published counties (golden) | Ardley, Elster, Pallard | 6.47 / 7.46 / 4.73 / 3.94 |

- **Golden figures (as built):** expected loss 6.47 (Ardley), 3.30 (Corvin), 7.46 (Elster), 4.73 (Pallard), 3.94
  (Tresham) per cent; quoted rates 7.00, 5.65, 8.20, 5.10 and 7.25 per cent; multiples 1.08, 1.71, 1.10, 1.08 and 1.84;
  the quoted rate at which each call changes (1.4 times the expected loss) 9.06, 4.62, 10.45, 6.62 and 5.52 per cent.
  Every main figure sits 0.4 or more of a half-bin from its rounding edge (asserted).
- **Margins:** each bought cover's quoted rate sits 1.27 to 1.30 under its limit and 1.26 to 1.30 over the limit the
  best fill (R1, R2) gives it; Tresham's sits 1.31 over its limit and 1.32 under the limit the total-failure reading
  gives; Corvin's 1.22 over its limit on every rung.
- **Dominance:** in the three sandy counties bought, the withheld years are crop failures (recovered yields 8.0 to 13.2
  bushels an acre against 27.3 to 38.6 for the district) and carry 0.50 to 0.72 of the liability each; the district
  fill puts them at the district's yield and pays 0.14 to 0.30; Tresham's withheld years are heavy abandonment with
  middling yields (22.6 and 24.5 bushels), so recovery adds less than the total-failure reading.
- **Grid:** the withheld-year choice (drop, district fill, ratio, regression, worst year, zero, recover) against the
  vintage (2026 or 2024 for 2017 to 2021) gives fourteen cells; the vintage moves no call (asserted), so seven calls:
  six buy none, zero buys four, recover buys the golden three.
- **Worth:** recovery moves the three bought covers' expected losses 3.73 to 5.55 points over the default and 1.93 to
  2.83 over the best fill; Corvin's, with no withheld year, moves 0.00.
- **Every reflex lands wrong:** dropping, filling from the district or the published counties, imputing from the
  published years' ratio or regression, the worst year and the total failure all file another set; only recovery
  files the three.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the five county covers; for each, the crop years 1991 to 2025, withheld years included | the risk policy (SF3); SF4 |
| 2 | Unit of account | the county cover; a year's indemnity share of its liability | the term sheet; the policy |
| 3 | Attribution window | the crop year as the service dates its estimates | the service's reference year; C1 (no estimate spans two years) |
| 4 | As-of dating | the estimates as the October 2026 download holds them; the quotes as scheduled | the file register; SF11 |
| 5 | Version basis | the latest estimate of each year | SF11 asserted |
| 6 | Denominator | the trigger, for the share; 35 years, for the average | the term sheet; SF8 |
| 7 | Weighting | every crop year equal | the policy's average (SF8) |
| 8 | Window length | 35 crop years | the policy (SF3) |
| 9 | Boundary inclusivity | at most 1.4 times buys | the policy (SF10) |
| 10 | Rounding path | the comparison on unrounded figures; figures reported to two decimals | SF15 asserted |
| 11 | Tie-break | none needed | no cover within 1.2 of its line (asserted) |
| 12 | Maturity and censoring | every crop year to 2025 estimated; 2025 preliminary | SF12 asserted |
| 13 | Order of operations | recover, bring to 2027, share, average | C1: bringing to 2027 before or after recovery gives the same shares (asserted) |
| 14 | Row order | none matters | C1 |
| 15 | Duplicate resolution | an estimate in both downloads: the later | SF11 |
| 16 | Identity normalisation | county by code with leading zeros or by name; districts by the recoded code | SF13, SF14 |
| 17 | Netting against gross | none | n/a |
| 18 | Dimensional units | bushels and harvested acres throughout | the service's data items; SF2 |
| 19 | Code and status semantics | `(S)` not published; `(NA)` not estimated; `(Z)` under half a unit | the symbols note (SF4) |
| 20 | Integerisation | none | n/a |
| 21 | Clause scope | the 1.4 rule applies to each cover alone | the policy |
| 22 | Forward window contents | the 2027 crop year each cover attaches for, priced on the 35 years | the term sheet; the policy |

## Literal reader

Executed word for word, the risk policy asks for each cover's average, over the crop years 1991 to 2025, of the share
of its liability it would pay on the county's official dryland sorghum yield for each year brought to 2027 by the term
sheet's trend, and buys the cover when its quoted rate is at most 1.4 times that average; the term sheet makes the
index the county's yield as the service estimates it, and the methods note says the service builds each district's
estimates up from all its county estimates, published or not. The text names 35 crop years; for a withheld year it
leaves open only how the county's estimate is found. The district's estimates less its published counties' give it
exactly (the residual is 300 to 800 acres and 2,400 to 19,600 bushels, positive, in every withheld year and nowhere
else; the counties foot to the district to the acre and the bushel in every other year, asserted); the district's
yield, a fill or a zero are other quantities, not the county's estimate. A reader who executes the text therefore files
Ardley's, Elster's and Pallard's covers.

## Oracles

None ties only under the golden. The quotes are market prices and tie to no basis. The prior covers' statements (a
distractor) are for Corvin's and Tresham's counties in 2019 to 2025, years both counties' estimates were published,
and settle on those published yields under other triggers. The drought-monitor extract (a distractor) dates the
region's droughts and holds no yield. The service's state rows foot to its nine districts, seven of which the downloads
hold only as districts, so no state residual isolates a county.

## Ask sheet

- **Ask A, each cover's 2027 liability and premium in dollars, to the nearest hundred (10 figures).** H18 home: the cost
  of each quote, a measure every cover carries that the call does not turn on. Path: the cooperative's 2027 enrolment
  (field, county of the field, practice, acres, submission time), the enrolment notice's closing time, the term
  sheet's liability terms (enrolled dryland acres times the expected yield times 90 per cent times the projected
  price) and the quote schedule's rates (four files, nine columns). Primary device: D8, a clock against a filed
  cutoff: the enrolment portal stamps each submission in UTC and the notice closes enrolment at 5:00 p.m. Central time
  on Friday 30 October 2026 (UTC-5 until 1 November), so fields submitted between 5:00 and 7:00 p.m. Central carry the
  closing date in UTC and pass a date filter while arriving late; every county has some. Hazards: H1 irrigated sorghum
  fields in the enrolment (practice column); H2 fields amended before the close (the later submission replaces the
  earlier); H3 the projected price per hundredweight against yields in bushels (56 pounds). Stops (asserted at build):
  the UTC date filter (the cracker) moves every county's liability and premium out of its bin; irrigated fields kept
  (Corvin's); the first submission kept (every county with an amended field); the price read per bushel (every
  figure); the golden.
  Realism: a member portal that logs in UTC while the cooperative's notices run on local time.
- **Ask B, the cooperative's 2016 to 2020 grain sorghum receipts from each county as a share of the county's 2016 to
  2020 grain sorghum production, per cent to one decimal (5 figures).** H18 home: how much of each county's crop the
  cooperative handles, a measure every cover carries that the call does not turn on (the members' weight in the index).
  Path: the elevators' scale tickets (site, account, commodity, origin county, net pounds, moisture, reference), the
  transfer log, the service's all-practices sorghum production 2016 to 2020 (the October 2026 download) and the data
  dictionary's conversion to bushels at standard moisture (four files, eleven columns). Primary device: D1, the same records
  under two key schemes: grain a member delivered to a satellite site and later moved to the main terminal is
  ticketed again at the terminal under the member's account, the transfer's number in the ticket's reference field
  beside contract and settlement numbers on ordinary tickets; only the transfer log ties the two. Hazards: H4 tickets
  at delivery moisture against production at 14 per cent (the dictionary gives the conversion, so H4 catches only a
  reader who skips it); H5 pounds against bushels (56 pounds); H6 wheat and corn
  tickets in the same file; H7 the 2024 download's unrevised 2017 to 2020 production (shared with the main path, where
  it moves no call). Stops (asserted at build): transfers counted twice (the cracker); moisture unshrunk; the 2024
  download's production; wheat and corn kept; the golden, each stop moving every county's share out of its bin.
  Realism: a cooperative's terminal re-tickets transferred grain to the member of record.
- **The construction layer:** each cover's expected loss, multiple, change rate and call, the burn by year, the chart
  and the conformed county record; the cracker has them.
- **Main population zero-counts (asserted):** the main call reads no enrolment, ticket, transfer, roster, drought or
  prior-cover row (the call and every rung computed with those files deleted are identical); the asks read no
  dryland sorghum county or district row of the main path except Ask B's all-practices production, which H7 moves
  without moving the call. No device or hazard row sits in a file the call reads.
- **Hazard table (asserted at build):** H1 moves the liability of every county with irrigated enrolled fields; H2 the
  counties with amended fields; H3 every Ask A figure; H4 and H5 every Ask B figure; H6 every Ask B figure if kept; H7
  every Ask B figure.
- **Referee:** none; no total in an ask file ties only under one handling.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule) | Verdict |
|---|---|---|
| A, liability and premium by cover | filters irrigated fields, keeps each field's later submission, converts the price per hundredweight, reads the closing date on the UTC stamp | miss |
| B, receipts as a share of production | shrinks to 14 per cent moisture, converts pounds to bushels, keeps sorghum, takes the 2026 download, counts every ticket | miss |

- Mirror leakage: about 6 per cent of ask weight (a response on R0 to R2 keeps the conformed file's layout and units;
  it misses its withheld years and every Ask A and Ask B figure on the same devices as the cracker).
- Pair ceiling: 34.6 (planning weights 38 / 7 / 55 with the call, each cover's expected loss, multiple, change rate
  and call and the chart in the main block and r = 5; the ask weight spread over 18 criteria: A 10, B 5, the conformed
  file 3; the cracker keeps the file, 3 of 18 or 0.167, 38 + 7 + 9.2 = 54.2; the mirror keeps r, instruction-following
  and one file criterion, 5 + 7 + 3.1 = 15.1; average 34.6), rerun from the generated rubric at ship.

## Layer 1 inventory

| Item | System that writes it | File | Natural mishandling | Effect (asserted at build) |
|---|---|---|---|---|
| Two downloads overlapping 2016 to 2023, 2017 to 2021 revised in the later | the cooperative's two pulls of the service's export | both downloads | the earlier download's values kept | call unchanged; expected losses within 0.08 |
| Symbols in the value column | the service's export | both downloads | a symbol read as zero (outside the golden method) | none on the golden method |
| Thousands separators in values | the service's export | both downloads | parsed as text | loud; call unchanged once parsed |
| Six crops, three practice rows | the service's estimating programme | both downloads | all-practices sorghum read as the index | call unchanged (SF1) |
| District codes recoded in 2008 | the service's geography | the 2024 download | one-digit codes grouped apart | call unchanged (recovery is within a year) |
| County codes without leading zeros | a spreadsheet save of the 2024 download | the 2024 download | the two downloads joined on the raw code | loud; call unchanged once matched |
| Coefficient of variation from 2008 | the service's export | both downloads | none | none |
| UTC submission stamps | the cooperative's enrolment portal | the enrolment | the closing date read on the stamp | Ask A only |
| Weights in pounds at delivery moisture | the elevators' scales | the scale tickets | unshrunk pounds over 56 | Ask B only |

## Leak check

Architecture 1, `leak.py --asof 2026-11-02`: REVIEW, no LEAK. The risk policy's 1.4 is its filed buy rule; the
exports' 593,300, 827,200, 831,700, 781,600, 151,500, 43,000, 19,600 and 11,300 are other counties', districts', crops'
and years' figures sharing digits with a golden figure by chance in 63,454 rows; the term sheet's county names are the
candidate set; the policy's, term sheet's and methods note's vocabulary is their genre's; "None" is the drought
monitor's own no-drought column. All harmless. The isolated reader (Sonnet, medium) quoted no decisive-step sentence
(nearest: methods 2.1, 6.1), found no ranking, helper or answer file, executed the literal estimand to the golden (all
35 years, a withheld year rebuilt as the district less its published counties) and answered question 6 "an analytical
choice, partly rule application: once the district-differencing text is read, the steps are mechanical". Its ask
readings (receipts over dryland or all-practice production; premium from the rounded liability) were closed in the
generator; its "duplicate county keys" was a misreading (no key repeats in either download, asserted).

## Determinism judge

Architecture 1, round 1 (`determinism_check_report.md`): DETERMINISTIC, every figure and the call reproduced;
disposition SEND_BACK on Gate H: `domain: pass`, `layers: pass`, `decisive_step: rule_application`. Gate G
`mechanism: etl_conformance` (borderline `planted_defect_flip`), `surface_read_dependency: yes`, `sole_data_defect:
yes`: the methods note's district-total identity (2.1) makes the recovery an executed identity, and with the cells
restored the call is the policy's filed expected-loss formula (5.3), the term sheet's trend and the 1.4 test (5.2).
Minor forks it listed (no call moves): the change rate from the rounded or unrounded expected loss (Elster 10.44 or
10.45); the trend-year count; the policy's 60 per cent counterparty cap.

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
- Withholding framed as a disclosure rule (fewer than three farms, to protect individual operations): a confidentiality
  rule needs complementary suppression, which would stop the single-county subtraction and make the design read as a
  leak engineered for the solver; re-framed as the service's publication standard for reliability (fewer than five
  reports or a coefficient of variation above 30 per cent), which needs none (stage 2, 2026-10-17).
- Two sandy counties in two districts with a golden buying both their covers (the drawn calibration): a reading of
  every withheld mark as a total crop failure buys the same pair, and with the other three counties' calls the same on
  every route the grid left a wrong call four of five covers right; re-laid at stage 2 with four sandy counties in four
  districts, three bought on recovery, one (Tresham) dear even with its years back so the total-failure reading files
  another set, and Corvin, with every year published, dear on every route.
- Re-rooting the decisive step on the same world was weighed at stage 2 and dropped: carrying past shortfalls forward
  in proportion to the trend level (a regression diagnostic, not this task type's analysis, and additive against
  proportional reads as a convention to a literal judge); allocating district counts by an ancillary density, a stop-loss
  layer's leveraged trend and pooled medians against averaged ones (each a weaker default path in another world).
- Architecture 1, the withheld drought years recovered from the district totals as the decisive step (selection on the
  outcome): judge SEND_BACK at stage 4 (2026-10-17), Gate H `decisive_step: rule_application`. The recovery is an
  identity the methods note files (2.1), and with the cells restored the call is the policy's filed formula, so the
  stump sat in Layer 1 (suppressed cells) and the term sheet's filed additive rating basis left no estimation choice.
  The world, the pack and the recovery stay usable as Layer 1 cleaning for architecture 2.

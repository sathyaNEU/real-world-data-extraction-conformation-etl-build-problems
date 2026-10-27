# task305 design note

Architecture 2, re-rooted 2026-10-27 at the author's direction after the portal's determinism return on architecture 1
(both judges competing_defensible_answer: the filed model's origins were the census households and the guests' spend
per pitch was pinned nowhere; the decisive step settled the population, so the WHAT screen killed it). The world, the
people, the shortlist and the three asks' files are kept; the population is now filed, and the decisive step is how a
holiday park's grocery spend is recovered from the one share of it our stores take.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task305.json`, architecture v2 (v1 in `lineage`, spent), registered
  2026-10-27. Guard verdict WARN after two axis redraws at check: forum `committee_or_panel` (BLOCK against task270)
  to `executive_team`, the chain's executive approving its one 2027 opening at its November meeting, which is who
  approves a store opening in a ten-store grocer; context artifact `monitoring_export` (BLOCK against task310) to
  `filed_model`, the property team's model sheet, which is the stakeholder's own file and now files the share the
  decisive step turns on. `test.same_puzzle_older` against task128 v3 is answered by a differentiation line (a queue's
  overflow against a team's capacity there; an origin's unobserved spend recovered from one outlet's modelled share
  here). Nearest driver on file 0.06 (task16 lineage), then 0.05 (task105 v2, task501 v2 lineage, task171 lineage);
  this slot's v1 at 0.10.
- **WARNs answered:** `overuse.objective` (the number's own objective); `repeat.decision` (pick_one_of_n against
  task311: the committee's decision is a pick of one of six sites); `repeat.deliverables` (docx and xlsx against
  task311: an appraisal workbook and a paper are what a property team sends).
- **Pairing:** Urban & Regional Science / `accessibility-agglomeration-location-analysis`, for Opportunity Sizing &
  Decision Support (kept): a new store's trade from the retail geographer's spatial-interaction model, pool (the
  grocery spend of every origin within reach) to realisable (what the new store wins net of what it takes from the
  chain's own stores, less its running costs).
- **Strategy:** `decomposition_attribution`, Gate G `decomposition_attribution`, generators G5 (provision elsewhere:
  most of a park's grocery spend goes to the competitor beside it), G3 (the card feed records our stores' take, not
  the park's spend), G6; gap population (what one row of the card feed is: our share of an origin's spend, not the
  origin's spend); Layer 2 `field_method`, pattern
  `own:spatial-interaction-origin-spend-recovered-from-one-outlet's-share`.
- **The population, filed:** the model sheet's section 1 now says spend starts where people are, a household's at its
  output area and anyone else's where they stay; it names no kind of place, no count and no rate.
- **The world change:** a Fairbasket superstore beside each of the two park-side stores, at Raddleford and at
  Withybeck, so our stores take about a quarter of those parks' guests' grocery spend; measured on the clean truth
  before any file: recovered through our modelled share, a pitch's season spend is GBP 2,500 and S3 Wrentoft leads at
  0.785; read directly off our store's take over the park's pitches it is about GBP 570 and S1 Bellingtoft leads at
  0.446 (the resident route S1 at 0.444).
- **Forum, event, organisation:** executive_team (redrawn), vote_or_meeting, retailer_or_ecommerce; role
  finance_controller (the finance director, who asks); calibration form `existing_book_actuals` (the card feed at our
  own stores).
- **People** (kept from v1, `guard.py names --geo GB --seed 305`): Pauline Sullivan, finance director, who asks; Joshua
  Ingram, head of property and network planning; Hazel Lucas (GIS), Hollie Richardson (workforce planning), Kathryn
  Hughes (transport). None appears in the prompt.
- **Spent mechanisms on the objective** (`guard.py mechanisms --objective opportunity-sizing-decision`, eighteen
  builds): none recovers an origin's unobserved total from one outlet's modelled share of it; the nearest in nouns,
  task105 v2 (a new outlet's market is the part of its catchment nearer to it than to a sister outlet), allocates a
  catchment among outlets rather than inverting one outlet's take to the origin's total.
- **Data-native sentence:** beside Raddleford Water and Withybeck Lakes a Fairbasket superstore larger than our store
  sits between the park and the town, so the out-of-region cardholders our stores see in season are about a quarter
  of what those parks' guests spend on groceries; the rest goes through tills in no file we hold.

## Default path

1. Reads the model sheet: spend starts where people are, a household's at its output area and anyone else's where they
   are staying; shares each output area's grocery spend (households x weekly spend x 52 x 0.88) among the 27 grocery
   stores of 280 m2 or more on the rating list, by floor area over exp(-0.22 x 1.25 x km).
2. Finds where visitors stay: the four pitch-measured caravan parks on the rating list. Takes what such guests spend
   from the card feed: cardholders with homes outside LQ at our stores beside the parks, March to October above the
   store's winter level, grossed up by its card share.
3. Prices a pitch at that spend over the park's pitches: Raddleford Water's guests at store 107 over its 640 pitches,
   Withybeck Lakes' at 105 over 520, Sallowmere Mill's at 104 over 160, about GBP 380 a pitch for a season.
4. Adds every park as an origin at its pitches times that spend and appraises the six sites by the model sheet's rule:
   S1 0.410, S3 0.238 (million pounds).

Ends on: S1 Bellingtoft, Fenton Road, GBP 0.4 million
Golden: S3 Wrentoft, Mill Lane, GBP 0.8 million

## Stump sentence

A competent analyst reads the model sheet, carries the holiday parks as origins, prices a pitch from the out-of-region
cardholders' season spend at our stores beside Raddleford Water, Withybeck Lakes and Sallowmere Mill over those parks'
pitches (about GBP 380) and approves S1 Bellingtoft, Fenton Road, at GBP 0.4 million, where the golden is S3 Wrentoft,
Mill Lane, at GBP 0.8 million; the step that lands them there is reading our store's take as the park's spend, when a
larger competitor at each park's gate takes most of it and our stores' take is only the model's share of it (19, 11 and
17 per cent), so a pitch spends about GBP 2,480.

## Three rules

Task type: accessibility-agglomeration-location-analysis (Urban & Regional Science), tagged for Opportunity Sizing & Decision Support: a new grocery store's trade from a spatial-interaction model of every origin's grocery spend within reach, sized as its addition to the chain's annual contribution, pool to realisable.
Domain test: The deciding quantity is the new store's trade from the retail geographer's spatial-interaction model, every origin's spend shared among the stores in reach by floor area and distance deterrence; a holiday park's spend is seen only as our stores' take of it, which the same model shares with the competitors beside the park, so the park's spend is the take over our modelled share; a hospital's patients or a utility's megawatt-hours have no origin whose demand is seen only as one competitor's share of it among stores priced by floor area and distance.
Swap: "which site adds most once the holiday park's guests are carried at their spend recovered from our stores' share of the parks they stay at" put into a hospital (wards, beds) or a feeder (megawatt-hours) loses its mechanism: no ward's demand is observed as one rival hospital's take divided by a floor-area-over-distance share, and no feeder's load is a competitor's till receipts.
Layer 1: Census 2021 output areas with population-weighted centroids on the British National Grid; an ONSPD extract with terminated postcodes; the VOA rating list in its own asterisk layout and descriptions, with the summary valuation's main measure in m2, parking spaces or pitches; a payment acquirer's merchant-insight feed by month and cardholder home postcode sector, out-of-region sectors included, with year-round visitors in every store's rows; modelled grocery spend per household by output area; the chain's April to March year against calendar-month feeds; nothing is placed to be caught.
Layer 2: field_method: an origin of spend no file counts (a holiday park) is priced from what our stores take of the spend of similar origins, and in the spatial-interaction model our store's take of a park is only its modelled share of the park's spend, the competitors in reach taking the rest; the park's spend per pitch is the take over the share, read through the same model, not the take over the pitches.
Decisive step: recovering a park's grocery spend per pitch from our park-side stores' season take divided by the share of that park's spend the model gives our stores (19, 11 and 17 per cent), rather than dividing the take by the park's pitches.
Not semantics: every field reads as what it is (households, spend per household, each list entry's description and measure, each cardholder's home sector, each store's card share), the model's parameters are read as filed, and the population is filed; no field, code or definition says that our stores' out-of-region take is a share of the parks' spend, and an analyst who reads all of it correctly and prices a pitch at our take over the pitches files S1.
Not rule application: no filed rule performs the step: the model sheet files the population and how a store's share of a place's spend is formed, and says nothing about how an unseen place's spend is measured; executing every filed rule with the direct reading files S1 at 0.4. Enumerated family (eleven constructions, direct and recovered): S3's addition 0.184 to 0.829, 6.45 printed units, two calls. Standing family (eight constructions recovering through our share: pooled, three single stores, two stores, two other winter windows, no gross-up): 0.768 to 0.829, 0.61 of a printed unit, every member S3 at 0.8. What rules the direct reading out is the filed share formula read on the park, not a sentence naming the step, and it is quiet: the direct reading reconciles with every file.
Analyst test: A strong analyst who reads every file correctly carries the parks as the model sheet's population requires, prices a pitch from our park-side stores' out-of-region season spend over the parks' pitches (about GBP 380) and approves S1 Bellingtoft at GBP 0.4 million where the golden is S3 Wrentoft at GBP 0.8 million; checks.py runs it on the generator's clean truth and on the pack.
Estimand: the addition to Marrable Foodstores' annual contribution of the one store the executive approves, once it is trading: 26 per cent of its sales, less 26 per cent of the sales it takes from the chain's ten existing stores, less its running costs, its sales the sum of its shares of the grocery spend that starts at every place, a household's at its output area and anyone else's where they are staying (`spend_share_model_2025.pdf`, sections 1 and 4).
No decoy: nothing is planted: the census is ONS's count, the rating list the VOA's, the feed the acquirer's record; the competitors are ordinary list entries the share model needs anyway; no memo, draft or figure argues for a site, no file ranks the six, no stakeholder figure is set up to be overturned.
No certified replay: no certified or published figure is reproduced; the estate's sales are actuals the model is never fitted to, and the spend per pitch is recovered from the feed through the filed model, not from any figure.
Lesson: a spatial-interaction model sees an origin's demand only through the outlets it observes, and what one outlet takes is its share of the origin's total; an origin priced on one outlet's take without dividing by that outlet's modelled share is understated by the competitors' part, which is largest where a bigger rival stands nearest; no build on file recovers an origin's total from one outlet's modelled share of it.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 the census households alone | the population sentence names anyone else's spend | no | no, the sheet sends the solver beyond it | the estate ratio 1.00 fits it | no | no | no | readable |
| R1 R0 scaled to the estate | no | the estate's sales | yes | the estate | no | yes, one ratio | no | readable |
| R2a/R2b a park-side store's guest share or take carried to Wrentoft | no | the card feed's out-of-region rows | yes | no | no | yes | no | readable |
| R2c a park-side store's take scaled by pitches | no | the list's pitch measures | yes, an analog by size | no | no | yes | no | readable |
| R3 every park an origin at our take over its pitches | the population sentence | pitches, the feed | yes, price a unit from evidence | no | no | yes, a ratio | no | readable |
| R4 our take over our modelled share of each park's spend (decisive) | no sentence says a store's take of a place is a share of it to be divided out; section 1 forms shares forward | no column: the share is computed from every store in reach | no: every reflex prices the pitch on what our stores see | none: the direct reading reconciles with every file | no | no: the share is a model output over 27 stores, not a reported figure | no: the competitors are list entries the share model needs for every origin | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | add to the chain's annual contribution | 26 per cent of its sales, less 26 per cent of what it takes from ours, less its running costs | the new store's own contribution | another figure | the model sheet, section 4 |
| SF2 | annual | a year of trading at 2026 prices | 2027 prices or a part year | another figure | section 4 |
| SF3 | households | the census count by output area | another base | none shipped | the pack carries one count (asserted) |
| SF4 | the guests' spend and the in-store share | measured in store, so 88 per cent applies to households only | the measured spend times 0.88 | S3 at 0.7 (0.721) | the model sheet: 88 per cent of households' grocery spend; the feed is spend at our stores |
| SF5 | the stores in the share | grocery descriptions of 280 m2 or more | every grocery entry | another figure | section 2 |
| SF6 | distance | 1.25 x straight-line km | straight-line km | another figure | the parameter table |
| SF7 | a site's location | its postcode's grid reference | its output area's centroid | another figure | the parameter table |
| SF8 | what the new store takes from ours | residents' and guests' spend alike | residents' only | same call | asserted |
| SF9 | a park's location | its postcode's grid reference | its output area's centroid | S3 at 0.7 (0.651) | the parameter table: any other address at its postcode's grid reference (asserted) |
| SF10 | the guests' spend at a store | the season's out-of-region spend above the store's November to February level, over its card share | no gross-up; every out-of-region pound | same call (0.768); S3 at 1.0 (0.958) | the record: stores no park reaches carry much the same out-of-region spend all year (asserted) |
| SF11 | which pitches | every pitch-measured site | caravan parks only | same call (all four are caravan parks) | C1 |
| SF12 | the season | March to October, where the excess runs | April to September | another figure | the record (asserted) |
| SF13 | rounding | once, at the end | the parts first | same figure | asserted |
| SF14 | once it is trading | a year of trading, no ramp | a first-year ramp | another figure | the prompt and section 4 |
| SF15 | the small park near S6 | carried alike | left out | same call | asserted |
| SF16 | the margin | S3 clear of S1 by 0.38 million | a tie | none | asserted |
| SF17 | households rolled forward | as Census 2021 counted them | grown five per cent | another figure | the parameter table |
| SF18 | ask A, the 25 weeks | UK arrival date | the export's UTC date | same ten figures | asserted |
| SF19 | ask B, the 25 weeks | a shift by its clock-in date | by the line's date | same ten figures | asserted |
| SF20 | ask C, departures | calls with pickup allowed | every call | another count at S1 and S3 | the prompt (pick up passengers) and pickup_type (asserted) |
| SF21 | ask C, within 400 m | straight-line from the postcode | another point | same figures | no stop at 360 to 440 m (asserted) |
| SF22 | ask C, a departure or a journey | a bus leaving a stop | the journeys | same figures | asserted |
| SF23 | ask B, which of a night's two lines goes | either, both carry one paid figure | keep the earlier or the later | same ten figures | asserted |
| SF24 | ask C, a weekday journey the Friday-late timetable lists again | one bus: the same block at the same calls | two departures | another count | GTFS block_id, one vehicle's working (asserted) |
| SF25 | ask C, each bus once | each block once at a stop and time | every same-time call once | another count | the feeds (asserted) |
| SF26 | whose spend the model shares | a household's at its output area and anyone else's where they are staying | the census households only | S1 at 0.4 | the model sheet, section 1 (asserted) |
| SF27 | scaling a park by pitches or by rateable value | pitches | rateable value | same call (one value a pitch, asserted) | C1 |
| SF28 | ask A, a load turned away | closed as delivered, the same load again the next day on its own trip | delivered | another figure | the DC procedure TP-04, section 2 (asserted) |
| SF29 | ask B, the report's grain | a shift on every date it covers | one line a shift | another figure | the paid hours report's own header (asserted) |
| SF30 | ask C, the joint routes and blocks | both feeds list the joint journeys; a block is one vehicle's working | two buses | another count | each feed's routes.txt marks routes 4 and 41 a joint service; GTFS defines block_id (asserted) |
| SF31 | the year-round out-of-region cardholders | people staying with residents, carried at the output areas or not | parked at the holiday parks | same call and figure either way (asserted); the parks reading is SF10's every-pound rival | SF10's record |
| SF32 | ask A, which stops were turned away | the stops closed too soon for their cases, re-sent the next day | a dwell cut-off chosen otherwise | same stops at a flat 8.5, 9 or 10 minutes (asserted) | C1 |

The decisive step is not a reading of any term: the population, the share formula and every convention are filed or converge, and S1 comes from an easy method on the same literal estimand, pricing a pitch at our take over the pitches.

## Ladder

| Rung | Construction | Names (margin) | Killed by |
|---|---|---|---|
| R0 | the census households alone | S1 0.409 (2.98x over S3) | the model sheet's population sentence |
| R1 | R0 scaled to the estate's sales (ratio 0.999) | S1 0.406 (2.99x) | the same sentence |
| R2a | Wrentoft uplifted at Raddleford's guest share of its sales (6.4 per cent) | S1 0.409 (1.93x over S3 0.212) | the parks carried as origins |
| R2b | Raddleford's guest take credited to Wrentoft as it stands | S1 0.409 (1.93x) | the same |
| R2c | a park-side store's take scaled by the pitch ratio, all to Wrentoft | S1 0.409 (1.20x at 107, 1.53x at 105, 1.30x at 104) | the model's shares of Wrentoft Lakes' spend |
| R3 (default) | every park an origin at our take over its pitches (GBP 376 a pitch; 447, 284 and 390 one store at a time; 174 over every pitch) | S1 0.410 (1.73x over S3 0.238; 1.60x to 2.23x) | our take is the model's share of the park's spend |
| R4 (golden) | the take over our modelled share (GBP 2,484 a pitch) | S3 0.801 (1.91x over S1 0.420) | (answer) |

Worth of the decisive step: a pitch at 6.6 times the direct reading; S3 moves from 0.238 to 0.801. Standing family 0.768 to 0.829. Rivals off the call's figure: every out-of-region pound 0.958, the 0.88 applied 0.721, a park at its output area's centroid 0.651.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | a household's spend at its output area and anyone else's where they are staying | filed (section 1, SF26); which places and how much is the analysis |
| 2 | Unit of account | the site; pounds of contribution a year | filed (the prompt, section 4) |
| 3 | Attribution window | a year of trading at 2026 prices; the feed's FY2025/26 for the spend per pitch | filed |
| 4 | As-of dating | the 2026 list, ONSPD May 2026, households as Census 2021 counted them | filed |
| 5 | Version basis | the June 2025 parameters | filed |
| 6 | Denominator | the pitches weighted by our stores' modelled share of each park's spend | the share formula (section 1) read on the park; the direct reading is C4, wrong on section 1 |
| 7 | Weighting | pooled over our stores, or one or two stores | C1 (0.768 to 0.829, asserted) |
| 8 | Window length | the winter level over November to February, December to February or January to February | C1 (asserted) |
| 9 | Boundary inclusivity | 280 m2; 400 m; the 25 weeks; the dwell cut-off | C1 (asserted, SF32) |
| 10 | Rounding path | once, at the end | asserted (SF13) |
| 11 | Tie-break | none | asserted (0.38 million clear) |
| 12 | Maturity | a year of trading, no ramp | filed (SF14) |
| 13 | Order of operations | shares, then sums, then the appraisal | filed |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | ask A's turned-away loads, ask B's night lines, ask C's joint and Friday-late journeys, in the asks' files only | filed where each system states it (SF28 to SF30), the records deciding which rows |
| 16 | Identity normalisation | postcodes and store numbers in one format across files | asserted |
| 17 | Netting against gross | what the new store takes from ours is netted | filed (section 4) |
| 18 | Dimensional units | m2, pitches, pounds, metres, cases, hours, departures | the data and the prompt |
| 19 | Code and status semantics | descriptions and pitch measures; DEL and COL; IN and OUT; pickup_type | the files' own documentation |
| 20 | Integerisation | none on the call; asks rounded once | the prompt |
| 21 | Clause scope | 88 per cent applies to households; 26 per cent to sales and to what is taken | filed (SF4) |
| 22 | Forward window contents | the trading year: the 2026 list's stores and the measured season carried | filed (section 4, the list as the share's stores) |

## Literal reader

Executing the prompt and every filed sentence word for word (the model sheet's sections 1 to 5 and its parameter table, the DC's procedure, the report and feed headers, the shortlist) fixes the estimand whole: the population is every household at its output area and anyone else where they are staying, each place's spend shared by the filed formula. What stays open is how a park's spend is measured, and the filed formula forces it: our stores' take of a park is their share of its spend, so the park's spend is the take over that share; every construction doing that files S3 at 0.8 (eight, asserted). The direct reading (the take over the pitches) is an easy method on the same literal estimand that the share formula contradicts, never another reading of a term. Each differing reading of a term (SF4, SF9, SF10, SF12, SF14, SF17, SF26) violates a quotable shipped sentence or the record.

## Oracles

None on the call: no file ties only under the golden and no past appraisal ships. The estate's sales run 0.91 to 1.06 times the residents' model, the park-side stores inside that spread, so they corroborate nothing. On the asks nothing ties only under the golden: the receipts tie with the TMS under both handlings of ask A (no turned-away load falls where the handhelds count), the workforce export's paid hours equal each line's elapsed time less its break whichever line stands, and the two feeds agree on every stop they share.

## Ask sheet

The three asks and their devices are architecture 1's, kept; the portal's judges found each one's convention unfiled, so each is now filed where its own system states it (the DC's transport procedure, the paid hours report's header, the feeds' route descriptions), and a silent device stays under each pin. The GIS analyst's data notes no longer ship (dataset-generation section 3): the rating list's layout comes from the VOA's own file specification, the clocks from the column names.

**Ask A, cases a week by store (10 figures, whole cases).** Pin (SF28, the DC's procedure TP-04): a load turned away is closed as delivered and sent again the next day on a trip of its own. Silent under it: which stops they are (no flag; the stop closes too soon for its cases, SF32), against promotion top-ups of 48 to 120 cases that also go again on a trip of their own the next day, so the rule read as "the same load again next day on its own trip" drops genuine deliveries.
**Ask B, paid hours a week by store (10 figures, whole hours).** Pin (SF29, the report's own header): a shift is listed on every date it covers at its paid hours. Silent under it: which lines are one shift, read only against the punches, against genuine same-length shifts on consecutive days and second shifts on one day, and the store worked is the clock-in terminal's.
**Ask C, bus departures by site on Friday 15 January 2027 (6 figures).** Pin (SF30, each feed's route descriptions): both operators list the joint routes; a block is one vehicle's working as GTFS defines it. Silent under it: the Friday by the clock is Friday's services to 24:00 and Thursday's after, against the GTFS service day; school-day duplicates on blocks of their own are second buses.

Main population zero-counts: the call reads the census, the centroids, the spend estimates, ONSPD, the rating list, the estate's Stores sheet, the card feed, the shortlist and the model sheet, and none of the TMS, receipts, workforce, punch, terminal or GTFS files (asserted, separation).

| Ask | Cracker (lands the call, runs the battery, executes every filed rule) | Verdict |
|---|---|---|
| A cases a week | 0 of 10 on every DEL stop, 0 of 10 dropping short stops, 0 of 10 deduplicating next-day repeats, 0 of 10 on TP-04's rule as written | miss |
| B paid hours a week | 0 of 10 by location, by punch store, with exact duplicates removed, one line a colleague a day, clock-in dates only, clocked time, or the report header's grain as written | miss |
| C departures | 0 of 6 on every call, before 24:00 only, both feeds counted, both feeds as one set, the larger feed's count, or the route descriptions and blocks as written, by GTFS service day | miss |

Pair ceiling: 28.5 ((45.0 + 12.0) / 2), the cracker on the call keeping 0 of the 26 ask figures and the mirror on the resident route the same; a cracker that reads one device rises to 39.1 (A or B) or 34.8 (C).
Mirror leakage: 0.0 per cent of ask weight.
Measured by: generator/pair.py on the cut pack.

## Pre-ship check

- Free gates on target.zip 5cbd1f6f (architecture 2): generator checks 225 passed (the resident route and the default
  path on the clean truth and on the pack, every direct reading at each park-side store and over every pitch on S1, the
  decisive share 0.10 to 0.35 at each analog park, the golden S3 at 0.801, every rung clearing S1 by 1.15 or more, the
  eight-member standing family 0.768 to 0.829 all S3 at 0.8, SF1 to SF32, the asks' devices with every wrong path
  missing every figure, separation, no readme, notes or dictionary under target/, the input gates); verify.py
  recomputes the call and all 26 ask figures from the zip alone; two builds byte-identical; figures_check 88 of 88;
  precut 53 checks clean with voice-check PASS; pair.py: pair ceiling 28.5, mirror leakage 0.0 per cent.
- leak.py REVIEW, each line ruled: sweep 1 the rating list file is the VOA's own record in its own layout; sweep 2
  "the model" is the property team's own word for its spend-share model; sweep 3 the numbers that coincide with
  answer figures are house numbers and rateable values on the rating list; sweep 4 the model sheet's population and
  share sentences are its own subject (it names no take, no share of an unseen place and no divide); sweep 6 the
  shortlist lists the sites with their costs and ranks nothing; sweep 7 GTFS is published as a zip.
- Guard: heart WARN (overuse.objective, repeat.decision, repeat.deliverables, answered at the draw). Surface promotes
  three pairs on card axes, each adjudicated clean here: task307 (same pairing, gap and decision type; its mechanism is
  what added network capacity saves when users re-route), task303 (gap and decision type; a shared upstream loss logged
  under each unit's own device), task128 (gap, G5 and decision type; differentiated on the card, a queue's overflow
  against a team's capacity). None recovers an origin's spend from one outlet's modelled share.
- Leak reader, architecture 2 read 1 (5cbd1f6f): no decisive-step sentence (its nearest, the appraisal rule, "states
  the contribution formula, not which site wins"), no ranking file, no answer figure; question 5's sentences execute to
  the golden; question 6 analytical, and its account of the step is not the decisive one. Question 3 named the VOA's file
  specification, ruled harmless as publisher documentation in leak_check_report.md.
- Determinism judge, architecture 2 pass 1 (5cbd1f6f): DETERMINISTIC, APPROVE, derive-then-open kept. Gate G
  analytical_non_defect (mechanism read as "other", the same mechanism as the card's decomposition_attribution); Gate H
  domain, layers and decisive step pass; stump power strong. Its cold derivation reproduced S1 at about 0.4 on the
  households and named, without executing it, "back-solving each park's total spend from the model's own baseline
  capture share": the decisive step is reachable by a reader who takes the population sentence to the parks, which is
  the risk this architecture carries into the portal. Its advisory notes (the per-pitch chain and the bus counts traced
  rather than recomputed; its own TMS recompute 0.3 to 0.5 per cent high from its boundary handling) need no change:
  verify.py recomputes every graded figure from the zip.
- The 10/10 rules re-read on the built pack: the deciding quantity is the spatial-interaction model's trade of a new
  store with every origin's spend in it; the mess (the rating list's layout, the acquirer's sectors, the clocks, the
  report's preamble) only complicates; the decisive step is analytical, recovering a park's spend from our stores'
  modelled share of it, and the population it used to turn on is filed.

## Tried and rejected

- The resort-town version (2026-10-24, scratch `t305/world.py`, never probed): Kelmouth and Porthwyn as seaside towns with 21 and 36 per cent of dwellings having no usual resident, a council tax base of second homes and a comparator resort store. Dropped on paper: a seaside town's name, its second homes in a council file and its summer trade announce visitors to any retail analyst, and the per-dwelling transfer it needed is the natural one; its default and golden margins were also 1.15 and 1.03.
- The park town at twelve output areas and its original running costs (2026-10-24, stage 3): the residents alone put S3 first, so the default path landed the golden; the town was cut to six output areas, its site's running costs raised and its competitor set at 850 m2, which puts Wrentoft fourth on the residents and first with the guests.
- The energy supplier's invoices as an ask B file (2026-10-24, stage 3): their monthly kWh tied only under the golden handling of the closed meter, an oracle for ask B; the file and the MPAN column on the half-hourly export were removed, and the Meters sheet carries the supply.
- A 25,560-entry rating list (2026-10-24, stage 3): a region of about 43,000 households carries about one hereditament per ten households; the list was cut to about 4,200 entries, with every village address in its parish and every grocery store, park and filling station kept, no graded figure moved.
- The first two sets of invented names (2026-10-24, stage 3): several towns, fascias and the bus operator sat within two edits of real places or retailers in OS Open Names; every name was replaced with one clearing the screen (edit distance three or more, no contained place name), the parishes named, no graded figure moved.
- The round-1 asks (2026-10-24, stage 4 on pack bb1aef72): both isolated scored readers missed the call (S1 at 0.5) but kept 26 of 26 and 16 of 26 ask figures, a measured pair of 56.4; the cumulative-load cases fell to a cut against the receipts, the meter changeover to the Meters sheet's shared supply, and the joint journeys to matching route, direction and time. All three were re-sited onto devices no sweep in the hygiene battery makes: the turned-away load re-sent the next day (D1), the clock-in terminal's store (D7) and the GTFS service day past midnight (D8); the electricity ask was replaced by paid hours.
- Route 41 ending at Brackenmere Northfield and Wrentoft (2026-10-24, the re-site): S3 and S4 sat at its termini, where no departure falls after midnight, so the before-24:00 path kept both figures; the route was run through to Garretstead and Skerryby, villages on the region's edge, and every site now has late calls.
- The round-2 asks B and C (2026-10-24, stage 4 on pack 1680766e): both isolated scored readers again missed the call (S1 at 0.5) and every ask A figure, but kept all ten paid-hours figures by attributing each shift to its clock-in terminal's store and all six bus figures by counting the Friday by the clock with the feeds deduplicated, each 16 of 26 for a measured pair of 45.8; both called the asks' handling data semantics. Ask B gained the amended shifts the next extract carries again, with genuine second shifts as the over-cleaning half, and ask C the school-day duplicate buses one feed lists on the same timetable, so both readers' handlings now miss every figure; the judge's pass on 1680766e was DETERMINISTIC, APPROVE, its one note (departures that pick up passengers) taken into the prompt.
- The round-3 asks B and C, and the round-3 call measurement (2026-10-24, stage 4 on pack ec38f0bd): both isolated scored readers kept all ten paid-hours figures, by deduplicating a colleague's rows on date and start and keeping the later (the row the clock-out follows, which is the golden's row), and one kept all six bus figures by the maximum per route, stop and time across the feeds (the golden's count); every ask A figure held for the sixth reader running. Both readers also landed the call (S3, 0.8), the first of six to do so, and both went first to the rating list's holiday parks at Wrentoft, the two words the brief's stump-vocabulary sweep line had named (the four earlier readers had the same line and missed); build-pipeline classes a rung executed because it was announced as an announcement, not a design failure, so the brief was fixed (a SKILLS commit) and the call is measured again cold, with the rule fixed in advance that if either cold reader lands the call, architecture 1 is spent. Ask B's re-extracted amendment and ask C's same-time cross-feed pairs were seen devices (the careful repair is the golden one); ask B moves to a night shift the paid-hours report lists against both dates it touches and ask C to a Friday-late service that repeats the weekday evening journeys on the same blocks.
- Architecture 1's determinism repair (portal return 2026-10-27, both judges competing_defensible_answer, Gates C and D, G pass): the fork is the stump. The judges found the population unpinned (the filed model's origins are the census households, and nothing authorises the holiday parks' guests), and the stump sentence says the easy route leaves out that same population. Measured on the shipped pack: the golden prices a pitch at GBP 2,443 (S3 at 0.804); S3 overtakes S1 at about GBP 1,330 a pitch; the per-pitch reading a solver takes once told that non-residents' spend counts (the guests' spend at our park-side stores over those parks' pitches) gives GBP 1,370 to 1,529 and S3 and S1 near a tie at about 0.5, and over every pitch in the region GBP 469 and S1. So a pin that makes the guests literal hands over the question the stump rests on and leaves the site on an unpinned construction at the crossover; no wording closes it. Redesign at stage 2: file the population at authority (a household's spend at its output area and anyone else's where they stay, never which or how many), move the decisive step into the guests' spend per pitch recovered through the model's own shares at the park-side stores, and widen the gap between that and the direct per-pitch reading (competition beside the park-side stores) so the direct reading files S1; close the three ask conventions the judges named (a shift listed on every date it covers, one vehicle per block, a refused load re-sent) each with a silent device kept under its pin.
- Shrinking Wrentoft's small Brightmart so S3 takes more of Wrentoft Lakes' spend (architecture 2, tuning, 2026-10-27): it also hands S3 the Wrentoft residents' spend, so S3 led even on the resident route and on the direct reading; reverted, and rung 2c was cleared instead by siting a larger competitor at each analog park's gate.
- The Corrinby camping site and the Loderwell touring site (architecture 2, tuning): once our share of the big parks was cut, these 20- and 15-pitch sites, where our stores take most of the spend, carried the recovered spend per pitch and handed the direct reading at their stores a pitch above the crossover; dropped from the world, and a Pettifer's set at Sallowmere Mill's gate for the same reason.
- The GIS analyst's data notes (architecture 2, stage 3): leak.py now refuses any shipped file that describes the data (dataset-generation section 3); the notes were cut, the rating list's layout moved to the VOA's own file specification, the refused-load rule to the DC's procedure TP-04, the report's grain to its own header, the joint routes to the feeds' route descriptions, and the punch clock into its column name.


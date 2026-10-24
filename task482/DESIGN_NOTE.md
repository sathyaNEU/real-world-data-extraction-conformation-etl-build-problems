# task482 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 12, drawn 2026-10-24 after architectures 1
to 11 were spent at stage 4: a fresh world and pack in the ETL objective, a state demographer's certification of the
2026 peak-season population of the eight towns of a northern lake basin for the 2027 Seasonal Communities Aid, each
town's average population present in its busiest month read through the load its sewer carries to its treatment
plant, calibrated per resident in the winter months when only the residents are in town.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task482.json` (architecture v12, lineage v1 to v11 spent), checked
  2026-10-24 after a fetch of main: WARN, no BLOCK. The window the axis bans read (task484 v3, task305 and task306,
  the live cards filed last; task280 and task279 carry `architecture_spent`) closes the strategies causal_design,
  population_selection and maturity_censoring, the forums council_or_assembly, committee_or_panel and
  line_manager_or_team, the forcing events season_or_peak, vote_or_meeting and purchase_order_or_contract, the
  organisations local_government, retailer_or_ecommerce and manufacturer, the roles policy_adviser, finance_controller
  and capacity_planner, the context artifacts register, monitoring_export and capacity_report, and the shapes 07 and
  other. The draw's honest labels clear all of them: the decision is a certification the State Demographer files with
  the Commissioner of Revenue (forum minister_or_cabinet, forcing event statutory_or_regulatory_filing, organisation
  research_or_statistics_office, role statistical_office_head), the shape a scorecard against one threshold (10), the
  context artifact the office's own resident estimates (published_series).
- **WARNs answered.** `overuse.shape` (10 in three of the last twelve): the decision is each town scored against the
  aid's three-times threshold, which is shape 10 and no other. `repeat.decision` (designation_set against task484 v3)
  and `repeat.question_form` (which, against task280 and task484 v3): the statute designates the towns that qualify, so
  the answer is a set and the question asks which. `repeat.deliverables` (png and xlsx against task306): a workbook is
  what the office files and the ratios against the line read at a glance as a chart. People drawn with
  `guard.py names --geo "United States" --seed 482`: Marvin Jordan (the State Demographer, the requester), William
  Terry (the seasonal estimates lead) and Bryce Williams (the basin's wastewater data steward), owners in file
  properties only; Amy Hardin, Robert Meyers and Barbara Frazier (architecture 11), Breanna Graham, Jeremy Cortez and
  John Huang (architecture 10) and Lawrence Hughes and Audrey Bautista (architecture 9) are not reused, and Amanda Beck
  and Christine Ward were set aside on `people.first` against task104.
- **Pairing:** Survey Research & Official Statistics, task type `census-register-administrative-data-quality`, which
  serves ETL: the office's resident estimates, the seven plants' monthly operating reports in two layouts, one joint
  plant's member meters, the Lake Protection Fee returns, the two booking platforms' remittances and the aid
  statute conformed into the certification (a row per town: its busiest month, its average population present
  that month, its ratio to its residents, whether it qualifies and its aid).
- **The decision and the quantity:** the Seasonal Communities Aid (an invented chapter of the Minnesota statutes) pays
  the 2027 appropriation of USD 2,400,000 in equal shares to the towns whose average population present on the days of
  their busiest month of the measurement year (October 2025 to September 2026) was at least three times their resident
  population, the State Demographer certifying
  both to the Commissioner of Revenue by 1 December 2026. The statute counts a town's population present on a day as
  everyone the town carries that day, its residents and every person staying or visiting there, a person counting for
  the share of the day spent in the town. The quantity is retrospective (the 2026 season is closed) because the statute
  fixes the measurement year; the commitment it drives (the 2027 aid) is forward.
- **Shape:** `10`, a scorecard against one threshold: each of the eight towns' busiest month, its average population
  present, its ratio to its residents against three, whether it qualifies and its aid, beside the call (which towns
  qualify and each one's share); the asks (the Lake Protection Fee by city and quarter of fiscal 2026, the plants'
  2025 phosphorus by half-year) are wide.
- **Strategy:** `other` (a population no record lists, measured through a physical load calibrated per resident where
  the residents are the whole population; population_selection would need a choice of who is in, and here the statute
  files everyone, and causal_design a comparison group, which carries nothing here); Gate G `etl_conformance` (the
  conformed certification judged against the statute's population); gap `population` (the lodging records are not the
  people present); pattern none; generators G5 (decisive: the town's visitors are housed outside the taxed lodging, in
  the cottages their owners keep and in the residents' homes, and the asymmetry by town is the trap), G16 (the plant's
  load is the one measure the statute's definition entitles) and G17. Layer 2 family `field_method`, pattern
  `own:a population present measured by its sewer load per resident`. Calibration organ: none. Context artifact
  `published_series` (the office's July 1 resident estimates).
- **World:** the United States, Minnesota, USD; the Quillmere Lake basin, its eight towns (Birchwick, Teskadel,
  Ruddmere, Sorrelton, Pinehold, Tamsen Point, Esker Narrows, Hollin Bay), their sanitary districts, the two booking
  platforms and the aid program invented, the names screened against populated places and counties before the pack is
  cut (H21).
- **Forcing fact:** the certification is due with the Commissioner of Revenue by 1 December 2026 and the 2027 aid is
  paid on it.
- **The physics:** a town's wastewater load is what everyone in the town sends down its sewer, about the same per
  person whether resident or visitor (a person's daily load of biochemical oxygen demand and water), so the plant's
  influent load in a month, divided by the load per person, counts the people present in person-days. From January to April the basin's seasonal cottages are
  closed and its lodges mostly shut, so the winter load is the residents' own
  and calibrates the load per person town by town. In summer the lodges and the platforms' rentals fill, and so do the
  cottages their owners keep and the residents' spare rooms, none of which any lodging return or remittance records,
  and the share the unrecorded stays hold differs widely between the lodge towns and the cottage towns.
- **Data-native sentence:** the Lake Protection Fee returns and the platforms' remittances record only the stays a guest paid
  for, while each town's plant records the load of everyone the town carries, and in the winter months that load is the
  residents' alone.
- **Paper screen** (`scratchpad t482v12/proto/sim2.py`, eight towns, a month-by-component world): residents plus the
  paid stays names one lodge town over three times its residents; the plants' loads per resident name five or six; the
  owners counted at the platforms' occupancy name a different five. The generator measures every rung and the family's
  spread on the cut pack at stage 2.
- **The WHAT screen.** Population: each town's residents and every person present in it (the statute). Outcome: the
  average population present on the days of the town's busiest month, a person counted for the share of the day
  spent there. Unit: persons, against three times the office's 1 July 2026 resident estimate. Window: the measurement
  year, 1 October 2025 to 30 September 2026, the
  busiest month by that average. Comparison: each town against its own residents. The decisive step settles none of
  them: it is how the people no stay record holds are counted, which no record or filed rule states and which only the
  plants' loads, calibrated where the residents are the whole population, measure.
- **Sources, one line each:**
  - population estimates from symptomatic indicators (utility connections and usage, wastewater flow) for seasonal and
    resort populations, the de facto population of a town in its peak season;
  - wastewater engineering's population equivalent: a person's daily load of biochemical oxygen demand and flow, and the
    monthly operating reports a treatment plant files with the state;
  - local lodging fees and the booking platforms' collection agreements: the fee is due on stays a guest pays for.
- **Same-puzzle and same-driver tests:** (population, none, designation_set) and (population, none, etl_conformance)
  against the last twelve builds, lineage included: no match.
- **Abstraction test:** the nearest drivers (0.06 and under) stripped of nouns: task305 counts a recorded body of
  short-stay occupants left out of a resident-based demand model and prices their spend per pitch from analog stores;
  here every recorded stay is already counted and the missing people are those no stay record holds, measured by a
  physical load per resident. task177's spent architecture 1 took a waste series as the given measure of a seasonal
  population and forecast new points from their peers' winter responses; here the series is not offered as a measure,
  and recognising that it is one is the step. task471 v4 counts registered units actually present from a register less
  its exits; task62's lineage counts resident events wherever registered.

## Three rules

Task type: Survey Research & Official Statistics, census-register-administrative-data-quality, which serves ETL in the taxonomy.
Domain test: the quantity that decides is each city's average population present in its busiest month, a de facto population no register, return or survey holds, estimated the way official statistics estimates seasonal and resort populations, from a symptomatic indicator calibrated where the population is known: each plant's influent BOD load, divided by the load per person its own January to April months fix (when the residents and the few recorded paid guests are the whole population), counts everyone present in person-days.
Swap: "which of our eight cities carried three times its residents in its busiest month" with hospitals for cities and admissions for paid stays has no population present beyond the people recorded, no load every person in the place adds to and no winter month that calibrates it, so it stops making sense.
Layer 1: the state's e-reporting export repeats every submission of a period (superseded, accepted, revisions returned after acceptance), the contract operator keeps the two pond systems' reports in its own workbook, one sheet per pond and year, the joint plant's member meters are read in gallons at midnight as each month ends and Esker Narrows' meter was replaced on 14 August 2025 with a new register from zero, the office's estimates carry three vintages with Pinehold's January 2025 annexation inside the 2025 and 2026 columns, the fee office's returns are monthly or quarterly by an operator's size with amended returns replacing and supplemental returns adding, Lakeward Stays writes its cities in capitals and remits with the checkout month, and Kettle & Pine reports a stay in the month after it checked out and carries its departure date only inside the reservation reference; each is how the system that writes it works, and nothing is placed to be caught.
Layer 2: a population estimate from a symptomatic indicator: the paid stays the fee records hold are a fraction of the people present, and the cities differ in that fraction (the owners in their cottages, the residents' guests and the day visitors hold 52 to 60 per cent of the busiest month in Birchwick, Ruddmere and Tamsen Point and 14 to 24 per cent in the lodge cities); the choice that flips the call is counting the people present through the load they send to the plant, calibrated per person on the winter months, against counting the stays the records hold.
Decisive step: recognising that the Act's population present is everyone the city carries, that the fee returns and platform remittances hold only the paid stays, and that each plant's influent load measures everyone, so each city's busiest month is read as its monthly influent load divided by its own January to April 2026 load per person (residents plus the few recorded paid guests).
Not semantics: with every field read correctly (the latest accepted submission per period, the pond workbook's flows in MGD, the meters in gallons with the replacement handled, the 2026 estimates, amended and supplemental returns, Lakeward's cities matched, Kettle & Pine dated from its reference) the easy route still counts residents plus the recorded paid stays and certifies Sorrelton and Esker Narrows alone, and no field, code, unit or definition read differently moves it: the Act's definition says whom to count, not how to count the people no record holds.
Not rule application: the Act files the estimand (everyone present, person-time, the mean over the days of the busiest month of the measurement year, against three times the 1 July 2026 estimate) and no method; on the cut pack the enumerated family (the records route as filed or with any uniform uplift of its paid guests, the plants' loads at design constants, the plants' loads calibrated on the winter months) files four different sets, from Esker Narrows alone (100 gallons a person a day) through Sorrelton and Esker Narrows (the records) to the golden five, the standing family (the 90 calibrated constructions, BOD, flow or TSS over ten winter windows, with or without the paid winter guests, each city's own load per person or the basin's pooled one, and the 0.17 lb population equivalent) has a spread of exactly zero on every certified figure (its worst member 140 people inside its thousand, qualifiers at 3.18 times or more and the rest at 2.68 or less), and what rules out the records route is the plants' own loads, 1.16 to 2.51 times what the residents and the recorded guests send in the busiest month while the January to April months hold the load per person at 0.170 to 0.173 lb in every city, which no filed clause states and no file displays; the cheapest licensed member (residents times the busiest month's load over the January to April mean, one group-by) files the golden, so the step is the recognition, not a choice inside the family.
Analyst test: A strong analyst who reads every file correctly counts each city's busiest month as its residents plus the paid guests the fee returns and both platforms' remittances put in town on an average day, finds Sorrelton (3.40 times) and Esker Narrows (4.35 times) at three times their residents, and certifies those two alone at USD 1,200,000 each, where the plants' loads count the owners in their cottages, the residents' guests and the day visitors too and put Birchwick, Ruddmere and Tamsen Point over as well.
Estimand: each basin city's average population present (everyone in the city on a day, each person for the share of the day spent there, the mean over the days of the month) in its busiest calendar month of the measurement year 1 October 2025 to 30 September 2026, against three times its 1 July 2026 resident estimate, and USD 2,400,000 in equal shares to the cities at or above it; filed in the Act's sections 2 to 5 (seasonal_communities_aid_act.pdf).
No decoy: nothing is planted; the estimates, the plants' reports, the meters, the fee returns and the platforms' files are their systems' own records, no memo, draft, briefing or stakeholder figure carries a wrong answer, and no filed sentence says the fee records count the population present.
No certified replay: no certified or published figure is reproduced to recover the method; the construction follows from the Act's estimand and from the plants' loads.
Lesson: a population nobody records can be counted by a physical load every person adds to, calibrated per person where the population is known, and the share it adds over the records is largest where the visitors stay outside paid lodging; no build on file counts people through a sewer load (task177's spent architecture 1 took a waste series as the given measure of a seasonal population and forecast it, and recognising the load as the measure is the step here).

## Default path

1. Conform the office's 1 July 2026 estimates, the fee office's returns (amended returns replacing, supplemental
   returns adding, quarterly returns spread over their months), Lakeward's stays by night and Kettle & Pine's stays dated
   from its reference into each city's paid guests on an average day of each month.
2. Count each city's population present in each month of the measurement year as its residents plus those paid
   guests, the people the records hold.
3. Take each city's busiest month, compare it with three times its residents and split USD 2,400,000 equally among
   the cities at or above it.

Ends on: Sorrelton and Esker Narrows alone qualify, USD 1,200,000 each.

Golden: Birchwick, Ruddmere, Sorrelton, Tamsen Point and Esker Narrows qualify, USD 480,000 each.

## Stump sentence

The default path counts each city's busiest month as its residents plus the paid stays the fee returns and both platforms record, the people the records hold, and certifies Sorrelton and Esker Narrows alone at USD 1,200,000 each, where the owners in their cottages, the residents' guests and the day visitors hold 52 to 60 per cent of Birchwick's, Ruddmere's and Tamsen Point's busiest month and no stay record holds them, and each plant's influent load divided by the load per person of the January to April months, when the residents are the whole population, counts them and puts those three over as well.

## Readability screen

Measured on the cut pack (`generator/golden.py`); residents 1,851, 3,902, 1,197, 3,052, 2,411, 3,094, 1,603 and
2,706 for Birchwick, Teskadel, Ruddmere, Sorrelton, Pinehold, Tamsen Point, Esker Narrows and Hollin Bay.

| Rung | What the response does | What in the pack points at it | Verdict |
|---|---|---|---|
| L0 the records as filed (default) | residents plus the paid guests the returns and both platforms put in town each month | the fee returns and the platforms are the only files that count anyone but residents; the Act's "staying in or visiting" | readable |
| L1 a uniform uplift | the recorded paid guests raised by one factor for the stays nobody recorded | nothing: no file sizes an unrecorded stay | readable |
| L2 the plants' loads at a design constant | each month's influent flow at 100 gallons a person a day | the e-reporting flows; a textbook planning figure | readable |
| G golden (decisive) | each month's influent load over the load per person its own January to April 2026 fix | nothing labels a plant's load as a population or relates it to people; the export is permit reporting and the fact sheet states only that every developed parcel in a basin city is connected to its sewer | silent |

L1 never lands the golden set: Hollin Bay goes over at 1.56 times its recorded paid guests, Pinehold at 1.82 and
Teskadel at 2.07, before Birchwick (2.29), Ruddmere (2.60) and Tamsen Point (5.41), so any uplift that puts Tamsen
Point over puts every city over first. L2 puts Esker Narrows alone over and every city's January to April population
at 0.60 to 0.62 times its residents.

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | resident population | the 1 July 2026 estimate | the 1 July 2025 estimate (Pinehold's annexation inside both) | same certified figures (asserted) | the Act's 2(b): 1 July of the measurement year |
| SF2 | measurement year | 1 October 2025 to 30 September 2026 | January to September 2026 | same busiest months (asserted) | the Act's 2(c) |
| SF3 | population present | person-time, a day visitor at the share of the day spent in the city | the overnight population alone | same cities qualify (asserted on the clean truth) | the Act's 2(d) |
| SF4 | busiest month | the calendar month with the highest average present | none | the same month in every construction (asserted) | the Act's 2(f) |
| SF5 | average population present | the mean over the days of the month | none: the plants report monthly averages of daily flow and monthly composites | asserted | the Act's 2(e) |
| SF6 | basin city | the eight cities | townships counted | not computable: the townships are on septic systems | the Act's 2(a); the fact sheet |
| SF7 | at least three times | at or above three | above three | same call: every construction 0.18 or more from three (asserted) | the Act's section 3 |
| SF8 | rounding | the test on the unrounded average, the nearest thousand certified | the test on the rounded figure | same cities qualify (asserted) | the Act's section 5 rounds the certified figure |
| SF9 | equal shares | USD 2,400,000 over the cities that qualify | in proportion to the population | USD 480,000 each | the Act's section 4 |
| SF10 | calendar months | each plant's reports by calendar month | none | asserted | the reports |
| SF11 | the joint plant | each city at its member meter's flow and the plant's influent strength | a split by residents or by recorded guests | asserted: the meters sum to the plant's influent within 1 per cent every month | the fact sheet: each city's flow is metered at the headworks |
| SF12 | the plant's load | influent | effluent | not computable for the ponds (no discharge from January to March or in July and August, asserted) | the fact sheet |
| SF13 | e-reporting submissions | the latest accepted submission | any submission | identical influent values in every submission of a period (asserted) | the export |
| SF14 | units | MGD times mg/L times 8.34 | gallons or million gallons for the meters | same call: the load per person cancels the unit (asserted) | the fact sheet |
| SF15 | the calibration's population | residents plus the recorded paid guests of those months | residents alone | same certified figures (the family) | the records converge |
| SF16 | the calibration window | January to April 2026 | any of ten windows from January to April, the 2025 winter, November to March; a single autumn month | same certified figures (asserted); October, November or December alone fork Tamsen Point | those months carry 9 to 23 per cent above the January to April load in every city (asserted) |
| SF17 | the measure | influent BOD | flow or TSS | same certified figures (the family) | the records converge |
| SF18 | the load per person | each city's own | the basin's pooled | same certified figures (the family) | the records converge |
| SF19 | Kettle & Pine's dates in the calibration | nights counted back from the departure in the reference | that date read as the arrival; the reporting period | same certified figures (asserted, with SF20 as a cross product) | the records converge |
| SF20 | a quarterly return's months | spread by days | spread equally | same certified figures (asserted) | the records converge |
| SF21 | the load per person's source | calibrated on the winter months | the 0.17 lb population equivalent, the design 0.20 lb TSS; 100 gallons a person, 0.20 lb BOD, the European 60 g | the first two same certified figures (asserted); the rest other sets | the last three put January to April at 0.60 to 0.62, 0.85 to 0.86 and 1.28 to 1.31 times residents in every city (asserted) |

## Ladder

Measured in the generator (`golden.py` on the cut pack, `checks.py` on the world's clean truth); ratios of the busiest
month's population present to residents for Birchwick, Teskadel, Ruddmere, Sorrelton, Pinehold, Tamsen Point, Esker
Narrows and Hollin Bay.

| Rung | Cities at three times their residents | Flips from the golden | Call kept |
|---|---|---|---|
| L0 residents plus the recorded paid stays (default) | Sorrelton and Esker Narrows (1.87, 1.97, 1.77, 3.40, 2.10, 1.37, 4.35, 2.29) | 3 | no |
| L1 a uniform uplift of the recorded paid guests | Hollin Bay, Pinehold and Teskadel join before Birchwick, Ruddmere or Tamsen Point | 3 or more | no |
| L2 the plants' loads at 100 gallons a person | Esker Narrows alone (2.36, 1.58, 2.64, 2.45, 1.58, 2.00, 3.14, 1.64) | 4 | no |
| L3 the plants' loads at the 0.17 lb population equivalent | the golden five | none | yes |
| G golden | Birchwick, Ruddmere, Sorrelton, Tamsen Point and Esker Narrows (3.88, 2.58, 4.43, 3.95, 2.60, 3.26, 5.11, 2.65) | none | yes |
| T the world's true population present | the same five (3.86, 2.56, 4.41, 3.97, 2.59, 3.28, 5.12, 2.65) | none | yes |

The golden's certified populations sit 196 to 451 people inside their thousands and every busiest month leads the
next by 6 per cent or more. The correction tracks the people no record holds (52, 24, 60, 14, 19, 58, 15 and 14 per
cent of the busiest month), not the cities' size.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | the eight basin cities' residents and every person present in them | filed (the Act's 2(a) and 2(d)); SF6 |
| 2 | Unit of account | persons on an average day of a calendar month, a person for the share of the day spent there | filed (the Act's 2(d) and 2(e)); SF3, SF5 |
| 3 | Attribution window | the measurement year, 1 October 2025 to 30 September 2026; fiscal 2026 for the fee; the halves of 2025 for phosphorus | filed (the Act's 2(c) and section 6); SF2 |
| 4 | As-of dating | the 1 July 2026 estimates; the exports pulled in October 2026 | filed (the Act's 2(b)); SF1 |
| 5 | Version basis | the latest accepted e-reporting submission for each period | the export's statuses; SF13 (influent identical in every submission) |
| 6 | Denominator | three times the resident population | filed (the Act's section 3) |
| 7 | Weighting | none: each day of the month counts once | filed (the Act's 2(e)) |
| 8 | Window length | one calendar month for the busiest month; four winter months for the calibration | the Act; SF16 converges, asserted |
| 9 | Boundary inclusivity | at least three times | filed (the Act's section 3); SF7, margins asserted |
| 10 | Rounding path | the test on the unrounded average; the certified figure to the nearest thousand; the asks at the prompt's rounding from unrounded sums | the Act's section 5 and the prompt; SF8 |
| 11 | Tie-break | none needed | asserted: every busiest month leads the next by 6 per cent or more |
| 12 | Maturity and censoring | none: the measurement year closed on 30 September 2026 and every plant reported September | not applicable |
| 13 | Order of operations | loads, the load per person, monthly populations, the busiest month, the test | linear; the family converges |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | one value per permit, period, location and parameter; one return per account and period with its supplemental returns | the export; the ordinance's section 2 |
| 16 | Identity normalisation | Lakeward's capitals to the cities' names; Kettle & Pine's municipality; the returns' property city | Layer 1; every stay and return names a basin city (asserted) |
| 17 | Netting against gross | a supplemental return adds to its period, an amended return replaces | filed (the ordinance's section 2); R2 asserted |
| 18 | Dimensional units | MGD, mg/L, 8.34, gallons, guest-nights, USD | filed (the fact sheet, the code list, the ordinance); SF14 |
| 19 | Code and status semantics | submission statuses, parameter and location codes, return types | the code list and the field list; SF13 |
| 20 | Integerisation | the aid divides evenly | SF9 (USD 480,000) |
| 21 | Clause scope | the section 6 reports do not affect the aid | filed (the Act's section 6) |
| 22 | Forward window contents | the certification governs the 2027 aid; nothing forward is estimated | not applicable |

## Literal reader

Executing the prompt and every filed sentence word for word: the Act counts a city's population present on a day as
everyone in it, its residents and every other person staying in or visiting, each for the share of the day spent
there, averages it over the days of each month, and tests the busiest month of the measurement year against three
times the 1 July 2026 estimate. No file states any city's population present or counts the people present: the fee
returns and the platforms' files record the paid stays only (the ordinance's fee is due on paid stays), and nothing in
the pack records the owners in their cottages, the residents' guests or the day visitors. A literal reader therefore
has to estimate the population present from what the pack measures of everyone present, and the only such measure is
each city's sewer load, which every person in the city adds to (the fact sheet connects every developed parcel in a
basin city to its sewer). Counting residents plus the paid stays assumes the cities hold no one else, which their own
plants' loads contradict by factors of 1.16 to 2.51 in the busiest month; the golden is the population those loads
imply at the load per person the winter months fix.

## Oracles

No file ties only under the golden or only on a wrong read. No shipped file states a city's population present, a
visitor count, a load per person or a ranking of the cities; the plants' reports state flows and concentrations for
permit reporting, the fee files state stays and fees, the estimates state residents. The asks' referees: the fee
Kettle & Pine remitted on its stays across 1 January 2026 confirms the departure date its reference carries, and the
pond systems' water balance against the fact sheet's statement that they hold the year's wastewater confirms the
basis of their flow (the devices' evidence, never an answer).

## Ask sheet

The call's declared population is each plant's influent from October 2025 to September 2026 and January to April
2026, the meters, the 1 July 2026 estimates, and the paid guests the returns and platforms put in town from January to
April 2026. Ask A reads every stay's nights in fiscal 2026 and so shares the call's January to April paid guests (149 of
34,664 Kettle & Pine stays have a night in those months): every reading of their dates leaves every certified figure
(SF19, asserted), so the device moves no certified figure.

| Ask | Quantity (unit, rounding in the prompt's closing sentence) | Population, outside the call's | Primary device (silent) | How it enters the call (H18) |
|---|---|---|---|---|
| A | the Lake Protection Fee the stays in each city generated in each quarter of fiscal 2026, whole dollars | every stay's nights from July 2025 to June 2026 and the fee on them, which the call never sums | D8 a settlement date for the event date, the true key in a reference string: Kettle & Pine reports each stay in the month after it checked out and carries its departure date only inside the reservation reference, so a stay put in its reporting period, or counted forward from that date as an arrival, lands its nights in the wrong quarter; the fee it remitted on the 165 stays the two readings put on different sides of the 1 January 2026 rate change matches only the departure reading | a measure every city carries that the call does not turn on: the fee office's revenue report (the Act's 6(1)) |
| B | the pounds of total phosphorus each treatment plant discharged in each half of 2025, one decimal | the plants' 2025 effluent, which the call never reads | D2 the record is the latest accepted, not the latest delivered: every e-reporting plant has, in each half of 2025, a revision of an accepted report returned for correction, beside five resubmissions that end accepted; with D3 a per-source convention: the pond systems' effluent flow is the month's average daily flow, at which the ponds release 84 per cent of their 2025 inflow against 28 to 33 per cent at the days discharged | the District's phosphorus grants from the same fund (the Act's 6(2), the ordinance's section 4) |

Shared hazards: quarterly returns spread over their months (the call's calibration and ask A, neutral on the call),
the stays split at quarter ends and the fee at the rate on each night (ask A), supplemental and amended returns (the
call and ask A), Lakeward's capitals (the call and ask A), the meters in gallons and the replacement (the call).
Fair handling, asserted: counting Kettle & Pine's nights back from the departure date reproduces all 32 of ask A and every
fee it remitted; the latest accepted submission and the ponds' flow read as the month's average reproduce all 14 of ask
B. Separation, asserted: every mishandling of an ask device leaves every certified figure (R2, SF19, SF20), and ask B's
rows are effluent rows the call never reads.

Measured by: `generator/ceiling.py` on the cut pack (target.zip be45d7b75ea5cc24).

| Ask | Graded figures | Cracker keeps | Mirror keeps | Naive handling keeps | Cracker |
|---|---|---|---|---|---|
| A fee by city and quarter of fiscal 2026, whole dollars | 32 | 0 | 0 | 0 | misses |
| B total phosphorus by plant and half of 2025, one decimal | 14 | 0 | 0 | 4 | misses |

Over the 46 figures the cracker keeps 0.0 per cent of ask weight (scores 45.0 with the call), the mirror 0.0 per cent
(12.0), the naive handling 8.7 per cent.

Pair ceiling: 28.5.
Mirror leakage: 0.0 per cent of ask weight.
The cracker reads the date in Kettle & Pine's reference as the arrival (the one date that file carries beside its
reporting period), multiplies the pond systems' effluent flow by the days they discharged and keeps each e-reporting
period's latest submission; none leaves a symptom in the hygiene battery. A cracker that also finds the departure
reading keeps 32 of 46 for a pair of 66.8, and one that finds both ask B devices keeps 14 of 46 for 45.2: ask A's
device carries the layer. This is the paper measurement of the cracker the script models; the stage 4 readers measure
the real one.

## Leak review

`leak.py --asof 2026-10-19` on zip be45d7b75ea5cc24: REVIEW, no LEAK. Each line ruled:
- author vocabulary, the Act's "generated by": the Act's section 6 names the fee report in the words the prompt asks
  it in; it says nothing of how a stay is dated. Harmless.
- answer words in the fact sheet and the Act: the Act's 2(a) lists all eight basin cities and names the aid, and the
  fact sheet's plant table lists the cities each plant serves; neither separates the qualifying five. Harmless.
- stump-paragraph terms in the ordinance, the returns' field list and the Act (returns, platforms, person, resident,
  register): each is the document's own subject (the fee's returns and platforms, the Act's residents and persons);
  none relates a plant's load to the people present. Harmless.
- ranking artifacts, the Kettle & Pine report and the returns: stays and returns by city, unsorted by any city
  measure, and summing them is the default path, not a ranking on the Act's test. Harmless.
- container metadata: the audit found no writer signature; the scrub reports both folders clean.

## Architecture 12 record (spent 2026-10-24)

Architecture 12 certified the Quillmere Lake basin's 2027 Seasonal Communities Aid: each city's average population
present in its busiest month of the measurement year read from its plant's influent BOD load divided by the load per
person its own January to April 2026 fix, against the default path that counts residents plus the paid stays the fee
returns and both platforms record (Sorrelton and Esker Narrows alone, USD 1,200,000 each, against the golden's five
cities at USD 480,000 each). At stage 4 round 1 (zip be45d7b75ea5cc24) both scored readers landed the call (exit 1):
each read the Act's "every other person staying in or visiting the city" as a population no record holds, went to the
one file that measures everyone (the plants' influent), divided the load by 0.17 lb a person a day (the population
equivalent the world had been tuned to agree with), checked it against the residents in winter and filed the five
cities; both also counted Kettle & Pine's nights back from the departure in its reference (reader A all 32 of ask A,
reader B 26 of 32 on half-dollar rounding) and missed only the pond systems' flow basis in ask B. The judge thread was
stopped at the spend. A statute that defines the population as everyone present, beside records that plainly hold
only the paid stays, sends a careful reader looking for a measure of everyone, and a pack whose influent rows have
no other use hands it one.

## Architecture 11 record (spent 2026-10-24)

Architecture 11 settled Lumenfold Learning's 2025-26 outcomes guarantee district by district, each partner district's
share of eligible students at or above Proficient on a matrix-sampled spring science assessment re-estimated from its
students' own two-module answers with the district in the population model, against the default path that averages
the contractor's five plausible values by district (19 districts owed USD 32,045.00 against the golden's 16 owed
USD 25,493.75). At stage 4 round 1 both scored readers missed the call, reader A kept all of ask A through the
catalog's hours per session, and the judge's pass 1 returned FIX_NOW on a cent tie in the credits (seat prices moved to
whole half dollars). In round 2 reader C refitted the 2PL latent regression from the item responses with district in
the conditioning model, validated it on the contractor's Table 6, filed the golden 16 districts and USD 25,493.75 and
kept every ask figure: a conditioning model that leaves out the grouping variable is a reflex for a reader who knows
plausible values, so the architecture was spent.

## Architecture 10 record (spent 2026-10-24)

Architecture 10 accrued each Medicare hospice provider number's FY2026 aggregate cap repayment at the December 2026
close, each beneficiary counted under the proportional method on the days to come from their state at the close (an
open stay by its length so far, a live discharge by its time out, returns read at every hospice from the benefit
periods extract), against the default path that runs the open stays on and takes the live discharges as finished
(Fallowmere USD 0.3 million against nothing). At stage 4 all four isolated readers across two rounds missed the call
and the round 1 judge returned DETERMINISTIC, APPROVE; the round 2 judge returned NOT_DETERMINISTIC, SEND_BACK
(margin_or_boundary_fragility and competing_defensible_answer): the printed 0.3 needed Fallowmere's count inside a
window of 2.9 beneficiaries while independent builds of the projection scattered about a beneficiary either way, and
the pool start, the number of later elections and the Kaplan-Meier tail were left unfiled (0.248 to 0.447 on the
judge's variants); ask A's routine-paid days read as an unstated rule. A designation set would have held (every variant
put Fallowmere above its cap); a figure printed to USD 0.1 million on a three-beneficiary window did not.

## Architecture 9 record (spent 2026-10-23)

Architecture 9 read each station's Schedule C availability from the bikes in working order docked, each bike's spells
rebuilt from the trips and fleet moves and a bike counted out of working order from the end of the ride that left it
when renters passed it over and a van then took it to the depot for a day or more, against the status feed's available
count (W-02, W-12, W-16 and W-19 against W-16 alone). At stage 4 (zip 14ceb178) both scored readers missed the call:
reader A subtracted the reported bikes and the bikes mechanics took in without a report, inside the inspection windows
(W-16 and W-19); reader B subtracted the reported bikes only (W-16). Both kept nearly every ask figure (65 and 64 of 74,
exit 1): the sales export's present-location column undone through the work orders' terminal replacements, and the
alarms ended at restarts once the clear pairing ran to hundreds of hours with sales inside them. The isolated judge
thread returned NOT_DETERMINISTIC, SEND_BACK, competing_defensible_answer (Gates B, C and E): no shipped file says that
unreported broken bikes exist or how to find them, so the records read literally (the feed, or the rebuild with the
reported bikes out) file W-16 alone, and the depot-stay cut and the pass test sit only in the solution's steps (at 36
and 48 hours W-17 and W-19 move by a point); Gate G `planted_defect_flip`, `surface_read_rejection`,
`surface_read_dependency: yes`, `sole_data_defect: yes`; Gate H `decisive_step: planted`.

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
- v9 stage 2, 2026-10-23: the fleet's clock ran four hours off Eastern time after the move to absolute instants (its
  local minute of the day counted from midnight UTC), so the pack showed the morning rush at noon; the window's start was
  re-anchored to 20:00 on 23 September so the fleet's own clock is Eastern time, the trajectory byte for byte the same
  (46,883 trips), the station move and the dock expansions read at 23:00, and Schedule C's minutes taken from Eastern
  time itself; the designations held (W-16 alone against W-02, W-12, W-16, W-19).
- v9 stage 2, 2026-10-23: each station's three months to one decimal put nine of 72 cells within two minutes of a
  printed edge and W-12's lowest month (87.652) within a minute; graded at each station's lowest month in whole per cent
  instead (the tightest ten minutes clear, M1), the margin to one decimal (0.684, eleven minutes), the monthly figures
  kept in the workbook as context.
- v9 stage 2, 2026-10-23: ask B's hours to one decimal put W-18 within a second of an edge; graded in whole hours, each
  pay station's alarm stream chosen so its figure sits 0.08 hours or more inside its bin (M3).
- v9 stage 2, 2026-10-23: the union of overlapping alarms as ask B's device: at whole hours the summed and merged
  spans print alike at every station; kept as texture (B3), the restarts carrying the device.
- v9 stage 2, 2026-10-23: with only the alarms and restarts in the log, ending an open alarm at the pay station's next
  event of any kind kept 15 of 24 hours figures (the restart was nearly always the next event), an honest pair of 45.7;
  the cabinet heater's events on cold days and the service door at reader repairs added, the shortcut keeps 4 (33.1).
- v9 stage 2, 2026-10-23: invented names screened by web search (Wellhaven, Northlane Mobility, Corlund Kiosk
  Systems): no organisation, product or place on any of them in or near the field; Welland, Ontario is three edits away.
- Architecture 9, 2026-10-23: spent at stage 4 on the judge's SEND_BACK. A count the operator's system publishes as
  available, read against a state no record holds (a bike's working order inferred from what renters and the vans did
  with it), is a surface read rejected however the evidence is gathered: on clean data the feed would be right, so the
  judge files Gate G surface_read_rejection and Gate H planted, and with nothing filed saying unreported faults exist
  the records read literally give the feed's answer (competing_defensible_answer). The readers missed the call for the
  same reason the judge refused it. Both ask devices were found: a column filled from a present-day register is undone
  by a work-order log that lists every swap, and a pairing that runs alarms to hundreds of hours with sales inside them
  announces its own repair. Next architecture: a quantity every file visibly lacks (so no surface read stands in for it),
  estimated by a method the data forces, and ask devices whose wrong reading is plausible rather than absurd and whose
  evidence no log lists outright.
- Architecture 10 draw (2026-10-23), no card filed. The guard's window closes survey research for ETL (ban.pairing and
  ban.subdomain against task483, so census-register and seasonal adjustment are both out) and the strategies grain_or_unit,
  population_selection and composition_mix (task483, task275, task179); payment claims, emissions, IRT equating and data
  integration clear it. Screened on those four and dead on file or on measurement: competing exits against censoring
  (task169, task266; the competing exit is a reflex, task133); pooled-test infection rates (task188); age-length keys
  (post-stratification, a reflex once the aged subsample's design ships); a pooled tail share from parts' means and spreads
  (task483's lesson); a population's share past a cut from short matrix-sampled booklets (task464's shrinkage lesson);
  direct against indirect adjustment of a net series (task453 v2's fork); time-series consistency by splicing (task123's
  screen); chance agreement on name and birth date in a voter roll (task468's common-identifier lesson); credibility for
  site emission factors (the regulatory standard takes the site's own tests, a fork); tracer flux ratios (the integrated
  ratio is the method's own definition, so the default is the golden); flows traced through intermediaries to end markets
  (task451 v1's swap failure); uncompensated gas meters (a unit read, data semantics); correlated systematic errors in an
  activity-data uncertainty (the call is a monitoring decision, Data Quality); cohort waits from cumulative counts under
  first-in-first-out (generic queueing, the swap reads the same); a pick log matched to put-aways by each lane's access
  order (drive-in lanes are last-in-first-out, field knowledge a strong reader carries, architecture 7's death).
- Architecture 10 draw (2026-10-24): drawn on the hospice cap after a second screen of the four open ETL task types (survey research still closed by task483). Screened and dead: TRI range codes valued at the exact filings inside each range (the midpoint is the programme's own convention, a competing defensible answer, and the exact filings are one group-by away); charge compression in cost-plus repricing (the implant invoices put the cost-to-charge ratio against the charge in plain view, and the functional form forks); a stopped turbine's nacelle anemometer read through the running transfer function (readers impute from neighbours by habit, and Gate G reads an instrument bias as planted); unconstrained demand on sell-out days (the product-limit estimator is a reflex and converges with the intraday route); time-of-observation bias in daily maxima (the calendar-day maximum is not recoverable from a 5 p.m. reset and the nearest hourly station); trend uncertainty with shared emission factors (propagating through the difference carries the shared factor by construction, so the easy route is right); items dropped from scoring rescored through the test characteristic curve (the published conversion table replays the method); best-of-k seed reports deflated by each recipe's seed spread (the client's GSDS Layer 1 list names best seed against mean as harmonisation); inverter clipping, demand ratchets and dead-time counting losses (each leaves a flat top or a ceiling in the records that announces its correction); unit value against a fixed-basket price index for provider unit cost (composition_mix, banned against task179 for this registration); DIF purification, testing-window instruction time and single-group order effects in equating (field reflexes, or no bias in the equating); register status nowcast by a Markov chain (forecasting, and architecture 9's surface-read refusal); interpolation along a process curve between sparse readings (task478 v6's and task480's degradation and life-cycle families). The first card draft BLOCKed on test.same_puzzle against task171 v4 with G13 decisive; G12 is the honest decisive generator for the step that decides.
- v10 stage 2, 2026-10-24: a lifetime projection with Brackwater, Lindmoor and Wexmoor owing beside Fallowmere: the
  standing family (Aalen-Johansen or empirical return chances, three valuations of a return, the open stays' later
  returns overall or from their time so far) moves each core program's cap by USD 30,000 to 70,000 against cells of
  USD 100,000, and the overall-rate route kept three of the four amounts; the core programs were placed under the cap
  and Fallowmere carries the call alone (nothing accrued on the default path, USD 0.3 million on the golden).
- v10 stage 2, 2026-10-24: pooled models across provider numbers and a split by discharge reason each moved
  Fallowmere's count by up to 1.3 per cent on cells of small programs; the policy files the reference class (the same
  provider number and diagnosis group), and Fallowmere's seller's system records no revocation against discharge
  reason, so the reason split is not available for its history.
- v10 stage 2, 2026-10-24: with return stays as long as first stays the overall rate times the census average landed
  the golden's cell (0.325 against 0.300); re-elections run shorter (the beneficiary comes back in decline) and seldom
  end alive again, so that route files 0.53 and the census-average valuation by time out 0.19.
- v10 stage 2, 2026-10-24: the outside share of Fallowmere's returns was raised from a third to four in five, so the
  route that reads returns from Elderglen's own records files nothing (cap ratio 0.971) instead of landing beside the
  golden.
- v10 stage 3, 2026-10-24: the organisation and program names Elderglen, Brackwater, Corrinbrook, Dunsmere, Lindmoor,
  Pennacott, Sallowfield and Wexmoor sat within two edits of real places in the GeoNames register (Eden Glen,
  Blackwater, Swallowfield and Fallowfield, Dunmore and Dinsmore, Wyndmoor, Dixmoor) or carried a place word (Penna,
  and Cornbrook in Manchester two edits from Corrinbrook); renamed Wendleglen, Brindlemoor, Corvelfield, Darrelbrook,
  Marrellford, Rennickdale, Varrowmere and Farrinridge in the generator, every figure unchanged. The lines above keep the
  names they were written with.
- v10 stage 4 round 1, 2026-10-24: both scored readers missed the call (each ran the open stays on and took the
  live discharges as finished, nothing accrued) and the judge returned DETERMINISTIC, APPROVE (Gate G analytical, Gate H
  pass); reader A joined the claim lines to the remittance register and kept all 24 ask A figures (exit 1), so the
  device that the latest version is not the paid one sat off the careful path. Re-sited: the contractor's prepayment
  review pays some held inpatient days at the routine rate, visible only by repricing the paid version, with the
  returned replacements kept as a hazard and moved more than 118 days before the close (reader B had priced them as
  pending, cutting payments); the census report's length-of-stay table, blank on a group key mismatch, now prints.
- v10 stage 4 round 2, 2026-10-24, architecture spent: both fresh scored readers again missed the call (open stays
  run on, live discharges finished, nothing accrued) and kept 0 of 24 ask figures, but the judge thread returned
  NOT_DETERMINISTIC, SEND_BACK (margin_or_boundary_fragility, competing_defensible_answer): Fallowmere's printed 0.3
  needs its count inside 177.6 to 180.5, a window of 2.9 beneficiaries (USD 0.1 million at the cap amount and 98 per
  cent), while independent builds of the same projection scatter about a beneficiary either way (0.248 to 0.311 on the
  judge's variants, 0.279 to 0.314 on the standing family), and it named four choices the policy leaves open (the
  Kaplan-Meier tail, one later election or several, stays begun before 1 October 2016, the last provider number when the
  open stay is at another hospice); it also read ask A's routine-paid days as an unstated counting rule. Lesson: a cap
  repayment printed to USD 0.1 million moves a cell every 2.9 beneficiaries of count, so a projection whose honest
  spread is a beneficiary cannot print one cell; the next architecture's call has to be a quantity whose cell is wider
  than its estimator family's spread, measured on independent builds rather than on the author's own family.
- 2026-10-24, architecture 11 draw, screened on paper before any code against v10's lesson (a call whose cell is wider
  than its estimators' measured spread): Medicare Advantage post-payment recoupments or denial overturns for a
  hospital's 2027 contract notices carry v10's latent structure (a terminal-looking state that is not final) and
  task451's (amounts still to arrive).
- Architecture 11 draw: Medicaid procedural reinstatements and COBRA retroactive elections: retroactive eligibility was
  screened at task451 and task479 v5, and COBRA's selection is population_selection, banned against task275.
- Architecture 11 draw: ACA risk adjustment transfers estimated from competitors' public prior-year transfers: carrying
  a competitor's risk forward is a fork; ACA grace-period cures: rule-heavy, with the cure rate carried across the 2026
  subsidy expiry.
- Architecture 11 draw: censored transplant costs by inverse probability of censoring weights: mature cohorts are
  unbiased without a trend, and a trend makes the stump a dated step; authorization- or ADT-based claims reserves: the
  completion family, and a leading indicator is a reflex.
- Architecture 11 draw: price-standardised total cost of care tiers: the standardisation is a WHAT (filed is rule
  application, unfiled a fork); deductible leveraging is task479 v3's driver; prescription abandonment by out-of-pocket
  cost: the lever is too small; stop-loss and high-cost claimant pooling: non-linear aggregation at claimant level and
  level-dependent counts are closed.
- Architecture 11 draw: hospital coding intensity after an EHR conversion, separated by the same patients' successive
  admissions: adjacent to task453 (a measurement change read from a within-design contrast that nets a drift), the event
  study is the reflex and the WHAT signposts the method.
- Architecture 11 draw: low-voltage anode effect PFCs at aluminium potlines: task459's driver (a ratio with a fixed
  component carried across activity levels), and the IPCC slope method files it; wastewater digester relief-valve
  venting: v9's Gate G risk (an unmetered event inferred from indirect evidence); idle and shut-in wells: a setting clone
  of task462 and task450 v1; stack test-day tune-ups: population_selection and a surface read.
- Architecture 11 draw: a landfill's pre-record waste read from the volume survey: the gas collection record calibrates
  the decay model and absorbs the missing waste; refinery turnaround cycles: a schedule in a file is read; fuel switched
  during gas curtailments: a degree-day normalisation is the reflex.
- Architecture 11 draw: Fellegi-Sunter term-frequency weights: adjacent to task468 (false links on common
  identifiers); address agreement decaying with the gap between records: adjacent to task468 v1.
- Architecture 11 draw: majority-drifted or released anchors (v6, task450); rater severity drift on a shared
  constructed-response subset (task471 v2's driver); rapid guessing in a low-stakes sitting (task479 v4, sent back as
  cleaning contaminated data); speededness and not-reached items (an anchor-drift screen catches them).
- Architecture 11 draw: queue position for open appeals or a coding backlog against timely filing limits: the waiting
  time is a generic queue quantity, so the swap test fails and the domain is a backdrop; censored demand behind
  capacity is task18, task108 and task168; capture-recapture is task199, task243, task248 and task448.
- Architecture 11 draw: newborns and deliveries predicted from current pregnancies in an employer group's renewal: the
  base projection's credibility and trend choices fork, in a large group last year's deliveries already carry the
  component, and the honest strategy (who is in the 2027 population) is population_selection, banned against task275.
- Architecture 11 draw: race and ethnicity imputed from surname and geography for group counts: summing the
  probabilities is the reflex for counts, and the weighting-against-regression choice for rates needs a gold-standard
  subsample, banned against task275.
- Architecture 11 draw: the payroll survey's birth-death model against the lagged QCEW census is reserved for task484
  v2, and drawing it here through a house domain would game the survey x ETL ban against task483.
- Architecture 11 draw, first world: plausible values aggregated by school for a county school system's coaching list
  reskins task450's world and call (a district's own assessment naming the campuses below a share for coaching), so the
  mechanism moved to a company's guarantee settlement with its partner districts.
- Architecture 11 placement, benchmarks by prior tercile (12 to 20 for the lowest, up to 30 for the highest): no
  district the plausible values pull down could cross a benchmark it met, since the strong-implementation districts
  with weak backgrounds sit in the lowest tercile, so benchmarks became whole numbers from 12 to 35 per order form.
- Architecture 11 placement, a 5.5-point margin to the family's envelope with 2.5 points of crossing for every route:
  no maximum likelihood or curve-inversion count crossed anywhere, the routes' upward bias peaking near 9 points; the
  shipped margin is 4 points to the whole family's envelope with 1.5 to 3 points of crossing by route.
- Architecture 11 asks, a series' total on each row with series of up to 12 hours: the hours column summed put most
  districts at two to three times their contract, which reads as wrong at a glance; the series were cut to 3 and 4
  hours and the summer institute booked by day.
- Architecture 11 ask A, the offering's catalog hours on every session row (a series' total on each of its sessions):
  round 1's reader A set the series rows beside the catalog's hours per session and replaced them, keeping all 58 hours
  and 18 credits (exit 1); the catalog every reader opens for the live and recorded formats holds the tell one lookup
  away. Re-sited onto the session times the scheduler holds as hours and minutes after the point, every offering
  scheduled in whole hours so only the sessions that ran short or long carry minutes.
- Architecture 11, credits on quarter-dollar seat prices: a 15 per cent credit on a fee of 11,537.50 is 1,730.625, so the
  cent had a tie that no file breaks (judge pass 1, FIX_NOW); seat prices moved to whole half dollars, every credit a
  whole cent, the call's set unchanged.
Architecture 11 (the contractor's plausible values drawn from a conditioning model with no district term, each district re-estimated with the district in the model), spent at stage 4 round 2 on zip ce5456c3: reader C refitted the 2PL latent regression from the item responses with district in the conditioning model, validated its fit on the contractor's Table 6, filed the golden 16 districts and USD 25,493.75, and kept every ask figure (58 of 58 hours, 20 of 20 shortfall credits, 36 of 36 memo rows) by reading the hours field as hours and minutes from its fractions. A conditioning model that omits the grouping variable is a reflex for a reader who knows plausible values, so the round-3 PD re-site (series credit hours stacked on h.mm) is moot and the slot re-roots.
- 2026-10-24, architecture 12 draw: a Lunar New Year factory shutdown reaching a US East Coast port's container imports
  a Pacific or Cape crossing later, for its calendar-adjusted series: the decisive step is a lag and a window, the
  enumerable single choice the client's measured coin flips share, the effect is famous in trade data, and a port world
  would be this lane's third (task472, task474). Not drawn.
- 2026-10-24, architecture 12 draw: a state's payroll survey estimates early-benchmarked to the lagged unemployment
  insurance census where the birth-death model ran ahead in a slowdown: the two series count the same jobs side by side
  (architecture 8's reflex), the step is a choice between two files, and rejecting the published estimate for the census
  reads as a surface-read rejection at Gate G. Not drawn.
- 2026-10-24, architecture 12 draw: revisions measured from real-time vintages, or rebuilt pseudo-real-time by
  re-adjusting truncated spans: the client's pin makes the triangle rule application once the vintages ship, and the
  truncated re-adjustment forks between X-11 and STL end filters. A seasonal break from a school calendar moved to
  August: the post-break span is a window and the regime regressors are a reflex. Not drawn.
- 2026-10-24, architecture 12 draw: chain drift in a scanner-data price index (economics x ETL is undrawable, and the
  formula is one enumerable switch); suppressed county-industry cells rebuilt from their margins (identification is the
  step, so one linear solve is the easy route landing); custom-area margins of error from replicate tables against the
  approximation (the handbook licenses both, a fork at Gate C); register over-coverage by signs of life (every activity
  window is a threshold read as a fork). Not drawn.
- 2026-10-24, architecture 12 draw: the lake towns' population present also read from their transfer stations' scale
  tickets or their water meters: solid waste is collected on schedules that lag the stays, and summer water use carries
  the irrigation of empty cottages, so neither measures the people present as the sewer does; kept out of the pack.
- 2026-10-24, architecture 12 stage 4: the population present read through the plants' influent load per person,
  calibrated on the winter months; both round 1 readers landed the call at the 0.17 lb population equivalent (exit 1),
  because the Act's definition made the paid-stay records visibly incomplete and the influent rows had no other use in
  the pack. Spent.

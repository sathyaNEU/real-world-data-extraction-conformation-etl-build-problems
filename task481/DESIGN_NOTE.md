# task481 design note: Ellsmere's aggravated assaults across the move to NIBRS

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

## Draw

Architecture 1, drawn 2026-10-20 from seed ET38 (a city performance office's public-safety scorecard, the move from
summary to incident-based crime reporting, a published aggravated assault rise a council member calls a surge, the
department's own figures moving less), taking the world, the decision and the quantity only. Card
`.claude/skills/fingerprint/cards/task481.json` (v1).

- **Pairing.** Survey Research & Official Statistics / seasonal-adjustment-official-time-series-production (client
  domain survey-research-official-statistics), objective Data Extraction & Conformation (ETL): the University of
  Ellsmere's Public Safety Lab, which writes the crime chapter of the city's Public Safety Scorecard under a
  data-sharing agreement with the police department, conforms the department's summary returns (Return A, to December
  2024), its incident-based extract (NIBRS, incidents reported from 1 October 2024), the three months in which every
  victim carries both classifications, and the Domestic Violence Unit's case log into one aggravated assault series on
  the NIBRS basis for the 2026 edition of the scorecard, and conforms the Gun Violence Reduction Unit's shooting log
  with the Medical Examiner's homicide list for the chapter's shootings. Official time-series production is the task
  type: a published series restated across a classification break so that its 2024 and 2025 values measure the same
  thing.
- **Shape 07, a grid of cells.** The criteria come from the shootings grid: non-fatal shooting victims and the
  shootings they were hurt in for each of twelve quarters, 2023 to 2025 (24 cells), beside the call (the change from
  2024 restated to 2025, to the whole per cent), the restated 2024 total (to the nearest hundred) and the 2025 count,
  and the one workbook: 29 graded items. The walk
  from the published 2024 total to the restated one rides in the workbook as working and is not asked for, because
  every line of it but one is the same on the default path (Tried and rejected).
- **Decision.** quantity_figure, answer unit rate_or_share (the 2024-to-2025 change on the NIBRS basis), question form
  how-much; forum the city's executive team, which signs off the scorecard before it goes to council
  (executive_team), forcing event the scorecard's annual edition closing calendar 2025 (period_close), org family
  university_or_school, stakeholder the lab's director of the city partnership (policy_adviser), context artifact the
  State UCR Program's published series (published_series). The call is retrospective because the scorecard reports a
  closed year: the restatement is what the published history needs before the 2026 edition goes to council, and no
  window is open that a forecast would serve.
- **Strategy.** composition_mix (pattern E, generators G14 conditioned yield and G6 composition): a conversion rate
  measured on three dual-coded months does not fit the nine months it is applied to, because within the other-assaults
  line (4e) the rate is a mixture of a domestic rate near a fifth and a street rate near three in a thousand, and the
  mixture's weights move through the year. Gate G etl_conformance; Layer 2 family estimation_fit, pattern
  own:conversion-rates-applied-where-stable-with-each-period-composition.
- **Data-native sentence.** The new records system went live on 1 October, so the only months in which every victim
  carries both its Return A line and its NIBRS offense are October to December, when domestic victims (almost all of
  the other assaults NIBRS counts as aggravated, through strangulation and household objects used as weapons) are a
  larger share of other assaults than in the spring and summer, when street assaults that almost never convert fill
  the line; a rate per Return A line carries October to December's mix into January to September.
- **Sources.**
  - Client card seasonal-adjustment/1 (model level shifts before seasonal filtering) and the official practice for
    conversion matrices across a classification change (dual-coded samples, rates applied at the detailed level where
    they are stable, each period at its own detailed weights): the textbook route is the conversion per summary line,
    and this build's decisive step is the judgment it takes for granted (that the line's rate is stable across the
    year), which the data settle.
  - Client card census-register/2 (net and gross classification error differ): the published rise nets two gross flows
    in opposite directions, assaults gained from the other-assaults line and assaults lost to simple assault, each with
    its own driver.
  - `measured-drivers.md`, held group: "the forward population differs from the validated one on an axis the pack
    shows only in the case log" and "the back-test passes by construction". Any rate set from the dual-coded months
    reproduces those months exactly; the axis that separates them from January to September (each month's domestic
    share of other assaults) sits only in the Domestic Violence Unit's case log.
  - `strategies.md` F5 (composition): held when the property is rebuilt from a history, not read off a column. Here
    the summary returns carry no domestic split; it is rebuilt by month from the unit's case log.
  - Differentiation lines on the card against task117, task137, task37, task44 and task97 (older builds sharing gap
    time, pattern E and quantity_figure): none restates a closed year of a recorded count across a coding break.
- **WARNs answered.** overuse.objective: the ETL lane is this author's lane. repeat.gate_g against task479: the honest
  key for a stump that lives in how the history is conformed; task479's driver (flood claims replayed on elevated
  buildings) shares nothing else.
- **Personas** (`guard.py names --geo "United States" --seed 481`): Darlene Ford (the lab's director of the city
  partnership), Steven Barnett (NIBRS coordinator, the police department's Records Division).

## Default path

1. Read the scorecard's crime chapter methods: from the 2026 edition the chapter reports aggravated assault as NIBRS
   offense 13A, one offense per victim, in the month the offense was reported in Ellsmere local time, from the
   department's extract, and shows 2024 restated as NIBRS would have recorded it had the department reported to NIBRS
   all year.
2. Read the 2024 Return A workbook (a sheet per month, lines 4a to 4e by weapon and the robbery and homicide lines,
   actual offenses in column 4) and the NIBRS offense extract (one row per offense against each victim, incidents
   reported from 1 October 2024); the extract's ucr_summary_class is filled for the victims reported in October to
   December 2024, the months the department produced both returns.
3. Tabulated the dual-coded months' victims by Return A line against NIBRS offense: for each line (4a firearm, 4b
   knife, 4c other weapon, 4d hands and feet, 4e other assaults) the share its victims NIBRS coded 13A, and for robbery
   and homicide the 13A victims the hierarchy rule left unscored per Return A incident or victim.
4. Applied each line's rate to the same line's January to September 2024 counts month by month, added October to
   December's 13A count, and summed: 2024 restated, 5,419 (about 5,400).
5. Took 2025's 13A offenses by month reported from the extract (5,254) and compared: the change from 2024 to 2025 on
   the NIBRS basis.

Ends on: a fall of 3 per cent from 2024 to 2025 on the NIBRS basis (2024 restated at about 5,400), the whole
published rise put down to the change in counting.
Golden: a rise of 1 per cent on the NIBRS basis (2024 restated at about 5,200).

## Stump sentence

Restating January to September 2024 at the dual-coded months' rate per Return A line files a fall of 3 per cent from
2024 to 2025 (2024 restated at about 5,400, the default path's `Ends on:` figure), because the other-assaults line's rate is
set in October to December, when domestic victims, who convert to aggravated at about a fifth, are 35.8 per cent of
the line against 29.1 per cent in January to September, and the street assaults that fill the rest of the year convert
at about three in a thousand; converting the line separately for domestic and other victims, each month at its own
domestic count from the Domestic Violence Unit's case log, gives about 5,200 and a rise of 1 per cent.

## Three rules

- Task type: survey-research-official-statistics / seasonal-adjustment-official-time-series-production, which serves
  ETL in the taxonomy: a published official series restated across a classification break.
- Domain test: the deciding quantity is 2024's aggravated assault count restated onto the NIBRS basis, estimated the
  way statistical producers back-cast a series over a coding change: conversion rates measured where both codings
  exist and applied at the level where they are stable, each period at its own composition; a single link factor or a
  before-and-after comparison changes the call.
- Swap: "By how much did aggravated assaults change once 2024 is counted the way NIBRS counts them" read with hospital
  nouns ("by how much did sepsis admissions change once 2024 is coded the way the new grouper codes them") keeps the
  official-statistics method, which is the domain here, but loses everything that decides this call: the hierarchy
  rule's unscored victims, strangulation and household objects counted as weapons, the autumn and holiday weeks of the
  dual-coded months and the Domestic Violence Unit's log; and replacing the conversion with a generic summary (the
  published rise, a link factor, a quarter-on-quarter comparison) changes the answer.
- Layer 1: Return A workbooks whose layout changed in 2022 (the department's own template, then the state program's),
  a summary-class column filled only in the three dual-coded months, legacy, interim and renumbered incident numbers
  in the Domestic Violence Unit's log and the shooting log, the log's case-opened date against the report date, the
  extract's UTC timestamps against local time, the state program's repository counted by incident date at its freeze
  against the department's count by month reported, and a shooting log carried across the records move; each is
  produced by the department's, the unit's and the state program's own systems and none is placed to be caught.
- Layer 2: estimation_fit; the methodological choice that flips the call is the level at which the dual-coded
  conversion rates are applied, and with which period's composition.
- Decisive step: converting the other-assaults line separately for domestic and other victims, each January to
  September month at its own domestic count, because the line's pooled rate in the dual-coded months is a mixture whose
  weights are October to December's.
- Not semantics: every field read correctly (the summary class, the NIBRS offense, the weapon and force codes, the
  relationship codes, the methods' definition of the restated year) still leaves the per-line conversion, which is the
  standard practice, on a fall of 3 per cent; no field, code or definition says that the other-assaults line's rate
  moves with its domestic share or which months to weight it by.
- Not rule application: no filed rule says how to restate January to September; executing the NIBRS definitions, the
  hierarchy rule's end and the methods word for word fixes the target and the dual-coded months' rates, and still files
  the per-line conversion's fall; which rates to apply to which months' counts is an estimation choice.
- Analyst test: with the data cleaned and every rule read correctly, a strong analyst builds the conversion per Return
  A line from the dual-coded months, applies it month by month to January to September 2024 and files a fall of 3 per
  cent (the `Ends on:` figure, 2024 restated at about 5,400), where converting the other-assaults line by domestic and
  other victims at each month's own count gives about 5,200 and a rise of 1 per cent; on the generator's clean truth
  (expected counts, no sampling noise) the same two routes give a fall of 2.1 and a rise of 2.1 per cent (checks.py).
- Estimand: the chapter methods (`scorecard_crime_chapter_methods_2026.docx`, section 2) file the population (offenses
  against victims reported to the Ellsmere Police Department, from the department's extract), the outcome (NIBRS
  offense 13A, one per victim), the window (calendar 2024 and 2025 by month reported, Ellsmere local time), the unit
  (offenses) and the comparison (2025 against 2024 as NIBRS would have recorded it had the department reported to NIBRS
  all year); section 5 gives the restated figure to the nearest hundred and the change to the whole per cent.
- No decoy: nothing is planted; the state program's certification letter reports its own comparison of the two
  October to December returns by category and recommends no restatement; the published series is the program's own
  table; no memo, draft or stakeholder figure argues a method.
- No certified replay: the method is not hidden and recovered by reproducing certified figures; every rate set from the
  dual-coded months reproduces those months by construction, the golden included, so nothing certified arbitrates.
- Lesson: a conversion rate measured on a short window where both codings exist holds only at the level where it is
  stable; carried per published line it imports the window's mix, and the mix has to be rebuilt period by period from
  the record that carries it; the composition builds on file (task68, task83, task473, task477) price a pooled rate on a
  population or a forecast, and none restates an official series across a coding break.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, the published rise taken as real (+10.2 per cent in the state's table, +8.8 against the department's own 2025 count) | the methods' restated-2024 sentence sends the solver past it: fires | the state's table: fires | none | the certification letter warns against comparing the two: fires | none | one ratio: fires | readable |
| R1, one link factor (October to December's 13A count over its Return A aggravated count) on January to September (-2.8 per cent) | the methods' "had the department reported to NIBRS all year" invites a conversion: fires | the summary class beside the offense: fires | the first bridge to hand: fires | none | none | one ratio: fires | readable |
| R2, a rate per Return A line on January to September (-3 per cent, the default path) | the methods file the target; the dual-coded months make the lines' rates the obvious tool: fires | ucr_summary_class against offense_code: fires | the textbook conversion matrix: fires | none | none | five ratios and a sum: fires | readable |
| R3 (decisive), the other-assaults line split by domestic and other victims, each month at its own domestic count from the unit's log (+1 per cent) | no clause names a domestic split, a seasonal mix or the unit's log as a weight: silent | no column of Return A splits 4e; the domestic count is in another unit's case log: silent | the reflex stops at the line's rate: silent | no control ties under either route; every rate reproduces the dual-coded months: silent | every record valid; the battery finds nothing: silent | a split rate and nine months of counts from a second file: silent | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | month reported | the report stamp in Ellsmere local time | the stamp as stored (UTC) | another figure (asserted) | methods 2: "in Ellsmere local time"; dictionary: report_datetime_utc "in UTC" with the offsets |
| SF2 | domestic victim of line 4e | relationship_1 a family or intimate partner code; in January to September the unit's log | another split | same call (asserted: the codes give the log's count in every dual-coded month, and the log's monthly 4e counts equal the records) | the unit's field notes: the log takes every domestic victim the department receives |
| SF3 | the log's cases counted | case_status not UNFOUNDED | every case | another figure (asserted) | Return A's column 4 counts actual offenses, unfounded excluded; the field notes' status codes |
| SF4 | the log's month | report_date | case_opened | another figure or the same (asserted) | methods 2: "the month the offense was reported" |
| SF5 | victim | individual victims; every 13A row is one | officers and businesses | same call (asserted) | NIBRS: 13A has individual victims only |
| SF6 | 2024 as published | Return A column 4, actual offenses, lines 4a to 4d | column 2, offenses reported | another published figure (asserted) | the state table's 2024 figure, 4,829, is column 4's |
| SF7 | 2025 count | the department's extract, 5,254 | the state's published 5,320 | another change (asserted) | methods 2: "from the department's extract" |
| SF8 | October to December 2024 | counted from the extract | converted like January to September | same call within the bin, but not the golden's figures (asserted counted) | methods 2: 2024 restated is what NIBRS "would have recorded"; for October to December NIBRS did record it |
| SF9 | non-fatal | did not die of the shooting, whenever the death | alive when the log's outcome was entered | the careful path (asserted) | the word; the Medical Examiner's list carries the deaths |
| SF10 | in the City of Ellsmere | within the city's limits, each block placed by where it is whichever system recorded it | the log's flag row by row, the contract township's blocks kept where the old database flagged them Y | the careful path (asserted) | methods 3: "within the City of Ellsmere's limits"; the log names the township on the same blocks from October 2024 and the Medical Examiner places its deaths there |
| SF11 | the quarter they were shot | shot_datetime's quarter | the quarter entered | another grid (asserted) | methods 3: "by the quarter they were shot" |
| SF12 | a shooting | the people struck at one block and minute | one report number | another grid (asserted) | methods 3: "the people struck at the same place and time, however many there were" |
| SF13 | each person | once, however often the log lists them | each row | another grid (asserted) | "people": a person entered twice is one person |
| SF15 | the quarter shot | the shot time in Ellsmere local time, the records system's rows (entered from October 2024) converted from UTC, as the system stores every time | every row read as stored | the careful path (asserted) | methods 3: "in Ellsmere local time"; a person entered in both systems sits exactly 5 or 6 hours apart as stored, and the records system's times put in local time fall on the extract's incident dates (asserted) |
| SF14 | the grain of the conversion | 4e by domestic and other victims | every line by domestic and other; domestic split again by intimate partner and other family, by assault and threat, or by sex; hidden robbery victims per robbery line | same call (asserted: every grain gives a rise of 1 per cent and about 5,200; the spread is 5,190 to 5,200 and 1.0 to 1.2 per cent) | methods 5: the restated figure "to the nearest hundred", the change "to the nearest whole per cent" |

## Ladder

The graded quantity is the change from 2024 restated to 2025, to the whole per cent (golden 1.175, printed +1, 0.325
from the nearest bin edge), with the restated total to the nearest hundred (5,192.98, printed 5,200, 43 from the edge);
2025 is 5,254 on every route, so each rung's worth is its 2024 restated total.

| Rung | Route | 2024 restated | Change | Distance from the golden |
|---|---|---|---|---|
| R0 | the published rise taken as real | 4,829 (Return A as published) | +9 (department), +10 (state table) | 7.6 points |
| R1 | one link factor | 5,403 (5,400) | -3 | 3.9 points |
| R2 | a rate per Return A line (default path) | 5,419 (5,400) | -3 | 4.2 points |
| R2b | one pooled rate for 4a to 4d and one for 4e | 5,392 (5,400) | -3 | 3.7 points |
| R3 | 4e split by domestic and other, each month at its own count (golden) | 5,193 (5,200) | +1 | |
| side | 4e split, 4a to 4d pooled | 5,166 (5,200) | +2 | 0.5 points (another whole per cent) |
| side | October to December 2025 against 2024 | | -3 | 3.8 points |
| side | R3 with the report stamps read as stored (UTC) | | +2 | 0.6 points |

- **Position and dominance.** Every route but the decisive one files a fall; the decisive split alone reverses the sign
  (clean truth: per line -2.1, split +2.1, asserted). Each correction below R3 walks the same way (a lower or higher
  link, pooled or per line); only the domestic split reverses.
- **Margin.** The decisive step moves 2024 restated by 226 victims (5,419 to 5,193), 4.2 points of the change; the
  nearest wrong route (4a to 4d pooled with the split) rounds to another whole per cent, 0.5 points off, and needs the
  split already taken. Every finer grain of the decisive step (SF14) stays inside the golden's bins.
- **Grid.** Split or not (2) by 4a to 4d per line or pooled (2) by local or UTC months (2): every cell files a figure
  outside the golden's bin but the golden's own (asserted on the four main cells; UTC is filed).
- **Worth.** The split is worth 226 restated victims and the sign of the call; the per-line rates for 4a to 4d are
  worth 27 (pooled 5,392 against 5,419).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | offenses against victims reported to the department, from its extract (methods 2, SF5, SF7); shootings: people struck in an assault in the city (methods 3, SF10) |
| 2 | Unit of account | the offense (one per victim, 13A); the person and the shooting for the grid (SF12, SF13) |
| 3 | Attribution window | calendar 2024 and 2025 by month reported (methods 2); the grid by quarter shot, 2023 to 2025 (SF11) |
| 4 | As-of dating | the extract run 5 October 2026; the unit's log of 2 October 2026; the shooting log of 1 October 2026; the Medical Examiner's list of 6 October 2026 |
| 5 | Version basis | one extract, one Return A workbook a year, one log of each; nothing superseded ships |
| 6 | Denominator | each dual-coded line's victims (the rates); the domestic and other victims of 4e separately |
| 7 | Weighting | each January to September month at its own line counts and its own domestic count (the decisive step, an estimation choice no filed rule makes) |
| 8 | Window length | twelve months a year; the dual-coded quarter October to December 2024 (dictionary, certification letter) |
| 9 | Boundary inclusivity | local calendar months and quarters, the shooting log's records-system rows converted from UTC (SF1, SF15) |
| 10 | Rounding path | 2024 restated summed unrounded and rounded once, to the nearest hundred; the change from the unrounded total to the whole per cent (methods 5) |
| 11 | Tie-break | none: the golden sits 0.325 from its bin's edge and the restated total 43 from its hundred's |
| 12 | Maturity and censoring | 2025 closed nine months before the extract; deaths to October 2026 in the Medical Examiner's list |
| 13 | Order of operations | count the dual-coded months, take the rates, convert each month, sum, compare |
| 14 | Row order | none matters |
| 15 | Duplicate resolution | one extract row per offense per victim; a person the shooting log lists twice counted once (SF13) |
| 16 | Identity normalisation | not needed for the call; the grid's person key is the report number, time, age and sex |
| 17 | Netting | unfounded offenses out of Return A's column 4 and out of the unit's log (SF3, SF6) |
| 18 | Dimensional units | victims and offenses; UTC stamps against local time in the extract (SF1) and in the shooting log's records-system rows (SF15) |
| 19 | Code and status semantics | 13A, 13B, 13C; ucr_summary_class with NS and P2; relationship codes (SF2); the log's circumstance, outcome and inside_city |
| 20 | Integerisation | whole victims; the restated total rounded once to the hundred |
| 21 | Clause scope | methods 2 for the call, methods 3 for the grid |
| 22 | Forward window contents | none: the scorecard reports closed years (retrospective call, reason in Draw) |

## Literal reader

Executing the prompt, the chapter methods and the dictionary word for word fixes the target, the window, the unit and
the dual-coded months, and leaves one place open, how January to September 2024 are converted; every conversion that
uses all the shipped evidence (the unit's log for the domestic count) files the golden, every conversion that does not
files a fall (asserted), every finer grain of the conversion the log supports lands in the same hundred and the same
whole per cent (SF14, asserted), and no literal reading of a filed sentence gives another answer; for the grid, the methods'
definitions of the people and the shootings (within the city's limits, by the quarter shot in local time), executed on
every row with the Medical Examiner's list for the deaths, the log's own later rows for the township's blocks and the
records system's UTC times put in local time, give the golden's 24 cells (asserted against the simulation's truth).

## Oracles

- The certification letter's October to December comparison (Return A against the NIBRS test submissions by category):
  true under every route, because every route counts those months the same way; it ranks nothing.
- The state table's 2024 and 2025 figures (4,829 and 5,320): the published series; 2025 is the repository's count by
  incident date at the freeze, not the department's (SF7); it confirms no route.
- The state repository download, the population estimates and the dispatch calls: declared distractors in
  `metadata.json`; none ties to any route.
- No restated figure, link factor or conversion rate ships; none.

## Ask sheet

- **Ask A, non-fatal shooting victims and the shootings they were hurt in, each quarter of 2023 to 2025 (24 figures,
  whole numbers).** H18 home: the chapter's shootings section (methods 3), the measure the executive team reads beside
  the restated series because it was counted the same way before and after the move to NIBRS. Path:
  `gvr_shooting_log_2023_2026.csv` (gvr_id, rms_number, shot_datetime, block, inside_city, victim_age, victim_sex,
  circumstance, outcome, entered), `medical_examiner_homicide_list_2023_2026.csv` (date_of_injury, injury_location,
  age, sex, cause), the chapter methods: three files, fifteen columns. No row of it is in the call's population.
  Primary device 1: D2, a label stored before a silent switch. The old shooting database marked a shooting inside the
  city by the patrol beat, and the department's beats take in North Ellsmere Township, which it patrols under contract;
  the records system it moved into on 1 October 2024 marks it from the address and names the municipality. So seven
  township blocks are Y before October 2024 and N, "(NORTH ELLSMERE TWP)", after it: 30 rows, a township shooting in
  every quarter before the move. Only a cut by block across the move shows it; trusting the flag keeps them in every
  quarter from 2023 to the third quarter of 2024.
  Primary device 2: D8, a clock on the rows the records system wrote. The log moved into the records system on 1
  October 2024, and that system stores every time in UTC (the extract's dictionary says so of its own stamps); the rows
  it entered carry shot_datetime in UTC, the old database's rows local time. The records system also keeps the outcome
  entered with the shooting, so a victim who died days later stays WOUNDED and only the Medical Examiner's list, which
  dates the injury in local time, shows the death. A join of the list on the date as stored misses every victim shot
  after 7 p.m. (6 p.m. in winter), and every quarter after the move has such deaths (a few evening shootings a quarter
  whose victim died days later); the summer 2024 shootings entered again at the move sit five hours from their first
  rows, so a person key with the time in it counts them twice; and a shooting on a quarter's last evening falls into the
  next quarter. Both round-1 readers joined the list on the stored date: this is the device their path misses. The
  old database marked a death within its 30-day review, so the quarters before the move need the list too.
  Hazards: the summer 2024 shootings entered again at the move under the same report number; multi-victim shootings with
  a later victim under the hospital notification's own report number (a shooting by report number moves 11 quarters);
  one row a report number merges real pairs (every quarter's victims); self-inflicted, unintentional and police
  shootings; shootings in other towns, named in the block and flagged N.
  Each device alone is not enough: the clock found with the township kept leaves the seven quarters before the move
  wrong (keeps 10 of 24); the township found with the stored times kept leaves every quarter after the move wrong
  (keeps 12 of 24).

| Ask figure | The cracker's reading (the round-1 readers' path: the list joined on the stored date, the flag trusted) | Golden | Cracker |
|---|---|---|---|
| 2023 Q1 victims, shootings | 118, 108 | 110, 105 | misses |
| 2023 Q2 victims, shootings | 163, 150 | 160, 148 | misses |
| 2023 Q3 victims, shootings | 157, 142 | 153, 140 | misses |
| 2023 Q4 victims, shootings | 134, 123 | 129, 120 | misses |
| 2024 Q1 victims, shootings | 122, 111 | 121, 110 | misses |
| 2024 Q2 victims, shootings | 170, 155 | 164, 151 | misses |
| 2024 Q3 victims, shootings | 191, 173 | 169, 153 | misses |
| 2024 Q4 victims, shootings | 102, 97 | 100, 96 | misses |
| 2025 Q1 victims, shootings | 115, 107 | 109, 103 | misses |
| 2025 Q2 victims, shootings | 159, 145 | 157, 144 | misses |
| 2025 Q3 victims, shootings | 164, 155 | 159, 150 | misses |
| 2025 Q4 victims, shootings | 129, 118 | 126, 115 | misses |

- **Mirror.** The best response off the call (R2, the per-line conversion) keeps the 2025 count (8 of the 38 call-side
  points) and reads the grid the careful way: 0 of 24.
- Pair ceiling: 30.0 (cracker 45.0, mirror 15.0, weights 38 / 7 / 55 with the change 20, the restated total 10, the
  2025 count 8 and each grid figure 55/24).
- Mirror leakage: 0.0 per cent of the ask weight.
- Measured by: generator/ceiling.py on the cut pack.
- **Sensitivity.** A cracker that also converts the records system's times keeps 10 of 24 (pair 41.5; 52.9 if the
  mirror does too); one that finds the township blocks keeps 12 (pair 43.8); both keeps 24 (pair 57.5). Round 1 measured
  the readers' path on the earlier device (both kept 11 of 25); round 2 measures this one.

## Pre-ship check

- **The 10/10 rules re-read against the built pack.** Domain: the deciding quantity is 2024's aggravated assault count
  back-cast onto the NIBRS basis the way a statistical producer restates a series across a coding change, conversion
  rates from the dual-coded months applied where they are stable and each month at its own composition; checks.py
  executes the analyst test on the clean truth (the per-line conversion files a fall of 2.1 per cent, the decisive
  step alone a rise of 2.1). Layers: the Return A layout change, the summary class filled only in the dual-coded months,
  the renumbering, UTC against local time, the state repository's freeze and the shooting log's carry-over across the
  records move are the department's, the unit's and the state program's own systems and are neutral on the call; the
  call opens neither the shooting log nor the Medical Examiner's list, and the extract's dictionary names neither
  (asserted). Three rules: no decoy, memo or earlier
  restatement ships; no field reading decides; executing every filed rule files the per-line fall.
- **Judge:** round 1 on a17767bf7704a407 DETERMINISTIC, SOLUTION_WRONG minor and FIX_NOW (step 6's township wording,
  filed as the city's limits in the methods); round 2 on ee83d775b423fed3 DETERMINISTIC and APPROVE, every graded
  figure reproduced (5,193 restated, 5,200 and +1 per cent; 5,254; all 24 shooting figures), Gate G
  method_or_model_selection and analytical_non_defect, Gate H pass with the decisive step analytical; the estimator
  variants it tried (line 4D split by domestic status 5,196, hierarchy-hidden victims scaled to all Return A lines
  5,229) all give 5,200 and +1. Its one note: the records system's UTC on the shooting log's new rows is unstated and
  derivable from the hour profile and the 21 re-entered rows five hours apart; ask 2 only, the silent device as built.
- **Readers:** four scored readers in two rounds, all four on the default path (about 5,400 and a fall of 3 per cent),
  none naming a sentence that gives the method; round 1 kept 11 of 25 ask figures each through the Medical Examiner
  join, so the post-move device was re-sited onto the records system's clock; round 2 on ee83d775b423fed3 kept 2 and 3
  of 25 (8.0 and 12.0 per cent, 5,254 plus one or two quarters by coincidence), score_reader exit 0 on both.
- **Free gates (2026-10-20):** checks.py 117 of 117, verify.py PASS on the call and the shootings, two builds
  byte-identical, target.zip ee83d775b423fed3 cut from the final build (16 files), figures_check.py 56 of 56,
  precut.py 51 checks clean, voice-check clean, ceiling.py pair 30.0 with mirror leakage 0.0; guard.py heart WARN
  (overuse.objective, the lane's, and repeat.gate_g against task479, answered in the draw; nearest driver task265's
  lineage at 0.07) and surface exit 0 with 5 pairs promoted for the author's adjudication on card labels alone (gap
  time, pattern E and a quantity figure, shared with task117, task137, task37, task97 and task44; no shared name,
  surface 0.077 to 0.093), the people screen's one name the Gun Violence Reduction unit's.
- **leak.py REVIEW lines, each harmless:** 100 and 120 appear as a table heading's population band and as NIBRS offense
  codes, not as shooting counts; the methods docx carries the chapter's own wording of the comparison and none of its
  figures; five documents use the program's words (months, October, offense, return) without naming a domestic share,
  a mix or a weighting.

## Tried and rejected

- A go-live of 1 November with November and December the only dual-coded months (the draw's first sketch): replaced by
  1 October, so that the rates rest on three months of victims; the stump is the same.
- The State UCR Program's reconciliation (the department's 2025 count walked to the state's published 5,320) as a
  graded ask: every line of it falls to a careful incident-level match against the repository download, so it carries
  no silent device; the download ships as a distractor.
- The walk from the published 2024 total to the restated one (one line per change in counting) and a chart of the
  published and restated series as graded asks: three of the walk's five lines (published, hidden, lost) and the
  chart's published series are the same on the default path, and a cracker on the call banks all of them, so the pair
  measured 44 or more before any shooting figure; the walk rides in the workbook as working and the chart is dropped.
- The shooting grid for 2024 and 2025 only, with later deaths the one device in every quarter: a single cross-check of
  the Medical Examiner's list cracked all sixteen figures; the grid now runs from 2023 with the township's beat flag
  before the move and the outcomes after it, and the 30-day review leaves deaths unmarked on both sides of it.
- The change graded to one decimal place and the restated total to the unit: finer grains the pack supports (every line
  by domestic and other, the domestic victims split by intimate partner and other family, by assault and threat, or by
  sex) spread the restated total over 9 victims and the change over 0.2 points, more than a tenth's bin, and with
  strangulation drawn mostly from intimate partners the relationship split alone moved the change by 0.35 points; the
  domestic kinds now share one relationship mix, and the figures are given at the precision the data carries (the
  restated total to the nearest hundred, the change to the whole per cent), where every grain agrees.
- Later deaths visible only in the Medical Examiner's list as the device on the quarters after the move (stage 4 round
  1): both readers joined the list on date, block, age and sex and kept 11 of 25 ask figures (score_reader exit 1 on
  each); re-sited onto the records system's clock, under which the same join on the stored date misses the evening
  shootings.
- Split reports numbered as the original report plus a few: in the records system those numbers belonged to unrelated
  incidents in the extract; a split victim now carries the number of the hospital notification report, which the
  system numbers in the same sequence and which holds no offense.

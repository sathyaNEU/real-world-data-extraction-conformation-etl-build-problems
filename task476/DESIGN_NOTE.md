# task476 design note: Hollister Gas's 2027 accelerated main replacement districts

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first. Architecture 2, a
re-root drawn 2026-10-20 after architecture 1 (ACS tract poverty change across the 2020 redrawing) was spent at
stage 4; its identity is in the card's lineage.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task476.json` (architecture v2), registered 2026-10-20 (the flag
  --force was passed over the slot's spent v1 card; the draft and the filed card showed WARNs only). Redrawn at the
  draw: the organisation family (utility_or_infrastructure is task472's; a city-owned gas utility is
  local_government), the forcing event (statutory_or_regulatory_filing is task471's; the council's capital budget
  round), the context artifact (operations_log and register are task472's and task471's; the program's filed
  guidelines). Structural matches on older builds differentiated on the card (task229 v2, task242, task461,
  task501 v2). WARNs answered: time_semantics' strategy risk (the analyst test runs on the clean truth with every
  field and rule read correctly and still files the wrong set); ETL in 5 of 12 (the lane); Gate G
  method_or_model_selection in 9 of 12 and after task471 (the decisive step is how each surveyed leak's unobserved
  start is estimated, among defensible methods, forced by the reports made at a leak's start); designation_set and
  "which" after task471 (the program funds every district over its line). Nearest driver task468 v2 at 0.07.
- **Seed:** ET33's number, re-rooted; nothing of ET33's world is kept. The lane's objective stays.
- **Pairing:** Physical & Environmental Sciences / emissions-inventory / Data Extraction & Conformation (ETL). The
  utility conforms its leak survey finds, the public odor-report log, the repair orders, the survey schedule and the
  GIS main inventory into a district leak-methane inventory, each leak's emission rate times the time it emitted,
  for the replacement program's designation.
- **Shape:** 07, a grid: each of the 12 districts' leaks found, methane, methane per mile of cast-iron and bare-steel
  main and its verdict against the line, the designated districts, the chart, the files.
- **Strategy:** time_semantics. A leak found at a survey began at an unrecorded time since the district's previous
  yearly survey; cast-iron and bare-steel leaks begin mostly in the frost months; so how long a found leak emitted
  before the find depends on when in the year its district is surveyed. Decisive generator G13 (the record's horizon,
  from the find, against the emission's, from the start), with G17 (the expectation of the start under the season's
  profile). Gate G method_or_model_selection.
- **World:** United States, a fictional northern city (unnamed state). Hollister Gas, the city-owned gas utility,
  funds accelerated replacement of cast-iron and bare-steel mains district by district; the City Council approves the
  2027 to 2029 capital program in its budget round. The program's guidelines designate every district whose 2026 leak
  methane per mile of cast-iron and bare-steel main is at or above the program line. Personas from `guard.py names
  --geo us --seed 476`: Marissa Harmon (distribution integrity engineer), Nicholas Wolf (gas operations manager).
- **Forcing fact:** the capital program goes to the Council's budget hearing on 18 May 2027; the inventory is for
  calendar 2026, closed with the repair orders through 15 March 2027. The call faces forward (the 2027 to 2029
  program); its quantity is the closed 2026 inventory the guidelines name (retrospective by the program's rule).
- **Forum and forcing event:** council_or_assembly (the Council approves the program), budget_or_appropriation (the
  2027 capital budget round). Organisation local_government; role compliance_or_audit (distribution integrity).
- **Data-native sentence:** Hollister's leak crews walk each district once a year in that district's own month, and
  cast-iron joints and bare-steel mains crack when the ground freezes, so a district walked in April finds leaks a few
  weeks old while one walked in October finds leaks that have been emitting since the winter; the public's odor
  reports, made within days of a leak starting near a building, are the only record of when in the year leaks begin.
- **The WHAT screen.** Population: the leaks found in 2026 on each district's mains and services (the leak survey
  finds and the odor reports, guidelines 2.1). Outcome: the methane each emitted from when it began to its repair, or
  to 31 December 2026 if still open, at the guidelines' emission rate for its grade. Window: leaks found in calendar
  2026. Unit: tonnes of methane per mile of cast-iron and bare-steel main in the district (the GIS inventory at 31
  December 2026). Comparison: the program line. The decisive step settles none of them: it is how each surveyed
  leak's unrecorded start is estimated.
- **Deliverables:** `leak_methane_inventory_2026.xlsx` (each district's figures and each leak's estimated start) and
  `main_replacement_designations_2027.pdf` (the recommendation to the Council with a chart of the districts against
  the line).
- **Sources, one line each:**
  - `stumping/references/client/layer2-rigor-patterns.md`, emissions inventory: activity times emission factor with
    the activity measured over the right exposure; here the activity is leak-hours and its unobserved part is the time
    before discovery.
  - The field's leaker-based inventories: a found leak is assigned a duration (the full interval since the last
    survey, the regulatory convention, or half of it, the textbook one); here both conventions are rungs, and the
    data's own start profile decides.
  - `dataset-generation/references/layer1-messiness.md`: repair orders with several visits per leak, address-keyed
    finds against GIS segment ids, a 2025 grade recode, local time against UTC, a GIS snapshot with abandoned
    segments.
  - The lane's spent drivers (`guard.py mechanisms --objective etl`): task462 (snapshot surveys whose detection rises
    with source size) and task470 (a sensor missing whole units) complete what a survey does not see; here every
    leak is seen and the quantity is how long it emitted before it was.

## Default path

1. Read the program guidelines: designate every district whose 2026 leak methane per mile of cast-iron and
   bare-steel main is at or above the line; a leak emits at its grade's rate from when it began to its repair, and a
   called leak began at the call.
2. Take the leaks found in 2026 from the survey finds and the confirmed odor calls, join each to its repair orders for
   the repair date (open leaks to 31 December 2026), and to its segment's district.
3. Start each surveyed leak halfway between its segment's 2025 survey and the find (the leak is known only to have
   begun since the last walk), each called leak at the call; sum each leak's rate times its hours by district; divide
   by the district's cast-iron and bare-steel miles; compare with the line.

Ends on: three districts designated, Ashby, Elmwood and Ivers.

Golden: five districts designated, Brennan Hill, Elmwood, Fenwick, Harlow and Ivers.

## Stump sentence

The default path counts each 2026 leak's methane only from its find to its repair, and the textbook correction starts
each surveyed leak halfway back to the district's previous survey (Ends on), so both designate districts by how many
leaks they find and how slowly they repair; leaks begin mostly in the frost months, so the districts walked in late
autumn found leaks that had emitted since winter, and only starts estimated from the odor reports' monthly profile
designate the districts the program should fund.

## Three rules

Task type: Physical & Environmental Sciences, emissions-inventory, which the taxonomy tags for ETL: conforming leak
survey finds, odor reports, repair orders, the survey schedule and the main inventory into the district methane
inventory the program designates on.

Domain test: the quantity that decides the call is each district's 2026 leak methane per mile of cast-iron and
bare-steel main, worked as a leaker-based emissions inventory works it: each leak's emission rate for its grade times
the time it emitted, the unobserved time before discovery estimated from when leaks begin, which the odor reports
measure.

Swap: "which school districts' absence days per pupil exceed the line, counting each absence from when the child fell
ill" keeps the words but loses what makes the step: no second record catches every case at its start by a separate
route, and the freeze-thaw cracking of cast-iron and bare-steel mains, a survey calendar walked district by district
and the public smelling gas near buildings are what fix when leaks begin and how long they emit unseen.

Layer 1: repair orders with several visits under one leak number, survey finds keyed by street address against main
segments keyed by GIS id, the 2025 recode of leak grades, the odor-call system's UTC times against the work orders'
local time, the GIS snapshot carrying abandoned segments, a regrade that keeps the leak number; each the utility's
own systems' output, each asserted neutral on the call.

Layer 2: estimation_fit. The methodological choice is how each surveyed leak's unrecorded start is estimated: at the
find (the record), at the previous survey (the regulatory convention), halfway between (the textbook convention), or
as the expectation under the monthly profile of leak starts the odor reports measure.

Decisive step: estimating each surveyed leak's start as its expected start between the district's previous survey and
the find, weighted by the monthly profile of leak starts in the odor reports, before its methane is summed.

Not semantics: every field, code, unit and definition read correctly (the grades, the visits under one leak number,
the addresses, the time zones, the abandoned segments) still leaves the record route or a convention for the start;
no field records when a surveyed leak began, and the step is the choice of estimate, not a reading.

Not rule application: the guidelines file the population (leaks found in 2026), the outcome (methane from start to
repair at the grade's rate), the unit (per mile of cast-iron and bare-steel main) and the line; no filed rule or
procedure says how a surveyed leak's start is estimated, and executing every stated rule with either convention
designates the wrong set.

Analyst test: a strong analyst who reads every file and rule correctly counts each surveyed leak from the midpoint
between its segment's previous survey and the find and files three districts designated, Ashby, Elmwood and Ivers (the
default path's Ends on); only starts estimated from the odor reports' monthly profile designate Brennan Hill, Elmwood,
Fenwick, Harlow and Ivers.

Estimand: the program guidelines (section 2) file the population (leaks found in calendar 2026 on the district's mains
and services, by survey or by odor report), the outcome (methane from the leak's start to its repair or 31 December
2026, at the grade's rate in the guidelines' table), the window, the unit (tonnes per mile of cast-iron and bare-steel
main at 31 December 2026) and the comparison (at or above the line).

No decoy: nothing is planted to be caught; no memo, draft, earlier list or stakeholder figure ships, and the survey
schedule, the odor log and the repair orders are the utility's ordinary records, true as kept.

No certified replay: no certified or published figure is reproduced to recover the method; the start profile is
measured directly in the odor reports, not fitted to a reported total.

Lesson: an inspection finds a defect long after it began, and how long depends on when in the year the inspection
falls against the season defects begin in; a convention for the unseen time that ignores the season misprices every
unit inspected far from it. No build on file teaches the start of an unseen interval estimated from a second record of
starts.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, each leak from its find (none designated) | guidelines 2.2, "from when the leak began": fires | none | none | none | none | one subtraction: fires | readable |
| R1, each surveyed leak from the previous survey (all 12) | none | the survey schedule: fires | the regulatory leaker convention: fires | none | none | one lookup: fires | readable |
| R2 (default path), each surveyed leak from the midpoint between surveys (Ashby, Elmwood, Ivers) | none | the survey schedule: fires | the textbook start for an interval-censored event: fires | none | none | one average: fires | readable |
| G (decisive), each surveyed leak's expected start between its segment's surveys under the monthly profile of called-leak starts (Brennan Hill, Elmwood, Fenwick, Harlow, Ivers) | no clause names a season, a profile or a weighting; 2.2 files only that a called leak began at the call | the profile is in no column: it is the odor log's call months counted, a file the inventory reads for other leaks | none of the duration conventions uses the season | none | none | none | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | at or above the line | 3.30 tonnes per mile or more, unrounded | more than 3.30; the rounded figure | same call: no district within 0.10 of the line (asserted) | guidelines 2.1 |
| SF2 | found in 2026 | the find in local time; a called leak's call converted from UTC | the call's UTC date | same call (asserted) | guidelines 2.2 "Dates and times are local" |
| SF3 | the grade | the grade when found | a later regrade | same call (asserted by the guidelines' own wording) | guidelines 2.2 "the grade the leak was given when it was found" |
| SF4 | a called leak's start | the call | the call less a reporting delay | same call (the calls are within days of the start) | guidelines 2.2 "began when the call was received" |
| SF5 | the season's profile | the confirmed odor calls of 2016 to 2026 | 2026's calls only; 2016 to 2025 | same call; no per-mile figure is graded (asserted: the largest move, 0.130 for 2026 only, is under the nearest district's 0.346 from the line) | the call's discretisation; the prompt grades the set |
| SF6 | until repaired | the REPAIRED visit; an open leak to 31 December 2026 | the last visit | same call | guidelines 2.2 |
| SF7 | the previous survey | the segment's own 2025 survey date | the district's first survey day | same call (segments are walked within days of each other) | the survey schedule |
| SF8 | miles | in-service cast-iron and bare-steel segments on 31 December 2026, feet over 5,280 | all mains | not the program's denominator | guidelines 2.3 |
| SF9 | the weighting within the interval | day by day | month by month | same call (asserted) | the call's discretisation |
| SF10 | a leak's district | its segment's district in the GIS | the crew's district | same call (the inventory reads no cost line) | guidelines 3.1 "a district's leaks are those on its own mains" |

## Ladder

Built figures, read from the cut pack by `generator/checks.py` (tonnes of methane per mile of cast-iron and bare-steel
main, 2026, against 3.30).

- **R0, each leak from its find (none designated).** The record's own interval leaves out most of a surveyed leak's
  life: no district reaches 1.5. Dies to guidelines 2.2 (from when the leak began).
- **R1, each surveyed leak from its segment's previous survey (all 12).** The regulatory convention charges a whole
  year to every surveyed leak: 4.29 to 7.67. Dies to the called leaks themselves: a leak found within days of starting
  shows that leaks do not all start the day after a walk.
- **R2, the default path: the midpoint between surveys (Ashby 3.38, Elmwood 4.58, Ivers 3.46).** The textbook start
  for an event known only to lie in an interval; it ignores the season, so every district's surveyed leaks get half a
  year before the find. Dies to the odor log: 62.6 per cent of called leaks started in December to March.
- **G, the decisive move (Brennan Hill 3.78, Elmwood 3.76, Fenwick 3.75, Harlow 3.68, Ivers 3.74).** Each surveyed
  leak's expected start under the monthly profile: an October or November walk finds leaks most of a year old, a
  March or April walk leaks a few weeks old; Ashby falls to 2.74 and the late-walked districts rise over the line.
  The truth (every start known, generator only) designates the same five.
- **Margins (cut pack):** the golden's nearest district is Juniper at 2.95, 0.35 below the line, and its lowest above
  is Harlow at 3.68; the golden family (the profile from 2026 only or 2016 to 2025, the weighting by month, the calls
  in UTC) moves no district more than 0.13 and names the same five.
- **Position, separation and dominance:** a designation, not a ranking: the four routes name four different sets;
  only the seasonal start brings Brennan Hill, Fenwick and Harlow in and keeps Ashby out together.
- **Worth:** the call and the grid of 12 districts' leaks and verdicts; R2 keeps every district's leaks and 8 of 12
  verdicts, so the asks carry the pair (Ask sheet).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | leaks found in calendar 2026 on cast-iron and bare-steel mains and their services, by survey or after an odor call (guidelines 2.2) |
| 2 | Unit of account | the district; tonnes of methane per mile of cast-iron and bare-steel main |
| 3 | Attribution window | the find date in 2026, local time (SF2) |
| 4 | As-of dating | the integrity extract of 15 March 2027; the GIS at 31 December 2026 |
| 5 | Version basis | repairs as recorded by 15 March 2027; open leaks to 31 December 2026 |
| 6 | Denominator | in-service cast-iron and bare-steel miles (SF8) |
| 7 | Weighting | each leak's rate times its hours; no weighting across districts |
| 8 | Window length | each leak's own life to 31 December 2026 |
| 9 | Boundary inclusivity | at or above 3.30 (SF1) |
| 10 | Rounding path | per mile compared unrounded; leaks and costs and interruptions whole |
| 11 | Tie-break | none: each district against the line |
| 12 | Maturity and censoring | a leak open at the year's end is counted to 31 December 2026 (guidelines 2.2) |
| 13 | Order of operations | each leak's start, its hours, its methane, the district's sum, the per-mile |
| 14 | Row order | no dependence |
| 15 | Duplicate resolution | one leak per leak number; a leak's several visits are its visits |
| 16 | Identity normalisation | grades A to C before 2025 and 1 to 3 after |
| 17 | Netting | none |
| 18 | Dimensional units | kilograms per hour, hours, tonnes; feet over 5,280 |
| 19 | Code and status semantics | REPAIRED against CHECKED and MONITORED; never the stump |
| 20 | Integerisation | none before the comparison |
| 21 | Clause scope | guidelines 2: the 2027 to 2029 program |
| 22 | Forward window contents | the 2027 to 2029 program designated on the closed 2026 inventory (a retrospective quantity, Draw) |

## Literal reader

Executed word for word, the guidelines fix the population (leaks found in 2026 on cast-iron and bare-steel mains), the
outcome (methane from each leak's start to its repair or 31 December 2026 at its grade's rate), that a called leak
began at the call, the unit (per mile of in-service cast-iron and bare-steel main) and the line. One thing is left
open: when a leak found by the survey began, which no file records. The candidates are the find, the previous survey,
the midpoint and the expected start under the season leaks begin in. The data separate them: the called leaks, which
2.2 dates at the call, are leaks the public smelled within days of their start, and they show the season directly
(62.6 per cent in December to March); the survey schedule puts each segment's previous walk a year before the find;
only the expected start under that season estimates the filed quantity, the methane from when the leak began, without
assuming leaks start evenly or at a walk. Every variant of it (the profile's years, the weighting by day or month, the
calls read in UTC) names the same five districts (checks.py). Every write-up step names the file and rule it executes.

## Oracles

None. No control, published figure or reconciliation ties only under the golden: the LAUF report is system-wide and
not allocated to districts, and no earlier designation, memo or ranking ships.

## Ask sheet

- **Ask A, each district's 2026 leak repair cost: 12 figures.** H18 home: guidelines 3.1, the Council's budget hearing
  weighs the program against what leaks already cost each district; a measure every district carries that the call
  does not turn on. Path: the work-order cost lines, the closeouts, the finds and odor log (each leak's segment), the
  GIS (the segment's district), the guidelines: six files, nine columns. Primary device: D6/D9, a ledger at another
  grain than its name: each cost line carries the work order's cost of that type to date, so the 2026 lines summed
  count the earlier postings again; only the year-end values less the prior year-end give 2026's cost, and the
  closeouts' totals equal the last values, not the sums. Second device: D7, the true key elsewhere: the cost center is
  the crew's district, and about one work order in eleven was worked by a neighbouring district's crew.
- **Ask B, each district's 2026 customer interruptions from leak repairs: 12 figures.** H18 home: guidelines 3.1, the
  disruption the program would add or avoid. Path: the interruption tickets, the meter premises, the guidelines:
  three files, seven columns. Primary device (re-sited after stage 4 readers 1 and 2, which joined each ticket's
  address to its meters and took all 12): D7, the true key elsewhere. A ticket names the premise where the crew shut
  off the service line, and on older streets one service line feeds two to four neighbouring premises, so every
  premise on the line was interrupted; only the premises file's service-line id finds the others. Hazards: an address
  can carry several meters (apartment buildings up to 24), and dispatch and the field crew sometimes both opened a
  ticket for the same address and leak.
- **The construction layer:** the designated set, each district's leaks and verdict, the chart; the cracker has them.
- **Main population zero-counts (asserted):** the call reads no cost line, closeout, ticket or premise.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, 2026 leak repair cost | the 2026 cost lines summed by the leak's district, every hazard repaired; the lines are costs to date, so every district's cost falls outside its bin | miss |
| B, 2026 customer interruptions | tickets for 2026 deduplicated by address and leak, the meters at each ticket's address counted; the other premises on each shared service line are left out, so every district's count falls outside its bin | miss |

- Mirror leakage: 0.0 per cent of ask weight (the asks read no rung's construction).
- Pair ceiling: 37.9 on the cut pack (weights 38 / 7 / 55; the cracker keeps the main block and instructions, 45.0,
  and none of the 24 ask figures; the mirror, R2, keeps every district's leaks and 8 of 12 verdicts, 30.8).
- Measured by: generator/ceiling.py


## Tried and rejected

- 2026-10-20, at the draw: the seed's moves (overlapping periods, a GEOID match, point estimates) as the decisive step;
  each is a filed fact or a reading here and sits on a lower rung. A period-specific population weight for split
  tracts' children was screened and set aside: it is task474's driver (a coarse total split by a period-specific
  indicator), and for a pure split any common weight leaves the child's rate equal to the parent's.
- 2026-10-20, architecture 1 spent at stage 4 (judge pass 1 SEND_BACK, Gate H rule_application; reader B landed the
  call and all 140 tract figures in about two minutes): a split 2020 tract's 2014 to 2018 rate rebuilt from the 2010
  block groups that tile it. The rebuild is exact arithmetic on published estimates, so once guidelines 3.2 files the
  estimand as the rate for the area the 2020 tract covers, the block-group table and the block relationship file
  leave only execution; without the sentence the unit is unfiled. No position holds both gates (the WHAT screen's
  own case), so the number re-roots. Ask A's reopened cases were also read straight off the event history, and the
  prompt's "median" contradicted guidelines 4.2's average.
- 2026-10-20, architecture 2 stage 4 readers 1 and 2 (pack 543b59b9): both missed the call on the default path
  (the midpoint start: Ashby, Elmwood and Ivers) and every repair-cost figure, and both took all 12 interruption
  figures by joining each ticket's address to its meters. That device kept as a hazard; Ask B's primary re-sited to
  the shared service lines. Reader 1 also read "local" as Eastern time: guidelines 2.2 now names Central time.

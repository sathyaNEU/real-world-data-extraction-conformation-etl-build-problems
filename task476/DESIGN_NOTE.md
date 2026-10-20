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
   bare-steel main is at or above the line; a leak emits at its grade's rate from when it began to its repair.
2. Take the leaks found in 2026 from the survey finds and the odor reports, join each to its repair orders for the
   repair date (open leaks to 31 December 2026), and to its district.
3. Count each leak's emitting time from its find to its repair, at its grade's rate; sum by district; divide by the
   district's cast-iron and bare-steel miles from the GIS inventory; compare with the line.

Ends on: designates the wrong set (provisional; fixed on the generator at stage 3).

Golden: designates the set where each surveyed leak's start is estimated from the odor reports' monthly profile.

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
between the district's previous survey and the find (the default path's correction, Ends on) and designates the wrong
set; only starts estimated from the odor reports' monthly profile designate the golden set.

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

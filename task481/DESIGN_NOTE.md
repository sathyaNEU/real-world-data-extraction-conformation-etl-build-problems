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
  data-sharing agreement with the police department, conforms the department's summary returns (SRS Return A, January to December
  2024), its incident-based extract (NIBRS, from November 2024), the two months in which every victim carries both
  classifications, and the Domestic Violence Unit's case log into one aggravated assault series on the NIBRS basis for
  the 2026 edition of the scorecard. Official time-series production is the task type: a published series restated
  across a classification break so that its 2024 and 2025 values measure the same thing.
- **Shape 03, bridge between two totals.** The 2024 published (SRS) figure walked to the 2025 NIBRS figure: one line
  per kind of change in counting (assaults hidden behind a robbery or homicide under the hierarchy rule, simple assaults
  NIBRS counts as aggravated, aggravated assaults NIBRS counts as simple), the restated 2024 total, the real change; the
  restated series by month (twelve 2024 months, twelve 2025 months); the chart's named parts; the asks.
- **Decision.** quantity_figure, answer unit rate_or_share (the 2024-to-2025 change on the NIBRS basis, and the share of
  the published rise that is counting), question form how-much; forum the city's executive team, which signs off the
  scorecard before it goes to council (executive_team), forcing event the scorecard's annual edition closing calendar
  2025 (period_close), org family university_or_school, stakeholder the lab's director of the city partnership
  (policy_adviser), context artifact the department's published Return A series (published_series). The call is
  retrospective because the scorecard reports a closed year: the restatement is what the published history needs
  before the 2026 edition goes to council, and no window is open that a forecast would serve.
- **Strategy.** composition_mix (pattern E, generators G14 conditioned yield and G6 composition): a conversion rate
  measured on two dual-coded months does not fit the ten months it is applied to, because within the simple-assault
  line the rate is a mixture of a domestic rate near a fifth and a street rate near one in a hundred, and the mixture's
  weights move with the season. Gate G etl_conformance; Layer 2 family estimation_fit, pattern
  own:conversion-rates-applied-where-stable-with-each-period-composition.
- **Data-native sentence.** The new records system went live on 1 November, so the only months in which every victim
  carries both its summary line and its NIBRS offense are the holiday weeks, when domestic assaults (almost all of the
  simple assaults NIBRS counts as aggravated, through strangulation and household objects used as weapons) are their
  largest share of simple assaults; the January to October months the restatement has to reach are full of street
  assaults that almost never convert, so a rate per summary line carries November and December's mix into the summer.
- **Sources.**
  - Client card seasonal-adjustment/1 (model level shifts before seasonal filtering) and the official practice for
    conversion matrices across a classification change (dual-coded samples, rates applied at the detailed level where
    they are stable, each period at its own detailed weights): the textbook route is the conversion per summary line,
    and this build's decisive step is the judgment it takes for granted (that the line's rate is stable across the
    year), which the data settle.
  - Client card census-register/2 (net and gross classification error differ): the published rise nets two gross flows
    in opposite directions, assaults gained from the simple line and assaults lost to it, each with its own driver.
  - `measured-drivers.md`, held group: "the forward population differs from the validated one on an axis the pack
    shows only in the case log" and "the back-test passes by construction". Any rate set from the two dual-coded months
    reproduces those months exactly; the axis that separates them from January to October (each month's domestic
    share of simple assaults) sits only in the Domestic Violence Unit's case log.
  - `strategies.md` F5 (composition): held when the property is rebuilt from a history, not read off a column. Here
    the summary returns carry no domestic split; it is rebuilt by month from the unit's case log.
  - Differentiation lines on the card against task117, task137, task37, task44 and task97 (older builds sharing gap
    time, pattern E and quantity_figure): none restates a closed year of a recorded count across a coding break.
- **WARNs answered.** overuse.objective: the ETL lane is this author's lane. repeat.gate_g against task479: the
  honest key for a stump that lives in how the history is conformed; task479's driver (flood claims replayed on
  elevated buildings) shares nothing else. repeat.deliverables (png and xlsx against
  task271): a workbook and a chart are what a scorecard office sends; the formats are revisited when the prompt is
  written.
- **Personas** (`guard.py names --geo "United States" --seed 481`): Darlene Ford (the lab's director of the city
  partnership), Steven Barnett (NIBRS coordinator, the police department's Records Division).

## Default path

1. Read the scorecard methodology note: from the 2026 edition the scorecard reports aggravated assault as NIBRS
   offense 13A, one offense per victim, in the month the offense was reported, and shows 2024 restated as NIBRS would
   have counted it had the department reported to NIBRS all year.
2. Read the 2024 Return A workbook (one row per month, the assault lines 4a to 4e by weapon and the robbery and homicide
   lines) and the NIBRS offense extract (one row per offense against each victim, incidents reported from 1 November
   2024); the extract's summary-class column is filled for the victims reported in November and December 2024, the
   months the department produced both returns.
3. Tabulated the dual-coded months' victims by summary line against NIBRS offense: for each Return A line (4a firearm,
   4b knife, 4c other weapon, 4d hands and feet, 4e simple assault, and the robbery and homicide lines for the 13A
   victims the hierarchy rule left unscored) the number of NIBRS 13A offenses per victim the line counted.
4. Applied each line's rate to the same line's January to October 2024 counts month by month, added November and
   December's NIBRS 13A count, and summed: the 2024 restated total.
5. Took 2025's NIBRS 13A offenses by month reported from the extract and compared: the change from 2024 to 2025 on the
   NIBRS basis.

Ends on: a fall of about 3.3 per cent from 2024 to 2025 on the NIBRS basis (calibrated on the generator's expected
values; the built pack's figure replaces it), the whole published rise of about 9 per cent put down to the change in
counting.
Golden: a rise of about 2.4 per cent on the NIBRS basis, about a quarter of the published rise real.

## Stump sentence

Restating January to October 2024 at the dual-coded months' rate per Return A line files a fall of about 3.3 per cent
from 2024 to 2025 (the default path's `Ends on:` figure), because the simple-assault line's rate is set in November and
December, when domestic assaults, which convert to aggravated at about a fifth, are the largest share of simple
assaults they are all year, and the street assaults that dominate the spring and summer convert at about one in a
hundred; converting the line separately for domestic and other assaults, each month at its own domestic share from the
Domestic Violence Unit's case log, gives a rise of about 2.4 per cent.

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
  rule's unscored victims, strangulation and household objects counted as weapons, the holiday weeks of the dual-coded
  months and the Domestic Violence Unit's log; and replacing the conversion with a generic summary (the published
  rise, a link factor, a quarter-on-quarter comparison) changes the answer.
- Layer 1: Return A workbooks whose layout changed in 2022 (the department's own template, then the state program's),
  a summary-class column filled only in the two dual-coded months, legacy and new records-system incident numbers in
  the Domestic Violence Unit's log, the log's case-opened date against the report date, the extract's UTC timestamps
  against local time, a preliminary and a final 2024 Return A overlapping, and the city's July-to-June fiscal year
  against the calendar year the scorecard reports; each is produced by the department's and the state program's own
  systems and none is placed to be caught.
- Layer 2: estimation_fit; the methodological choice that flips the call is the level at which the dual-coded
  conversion rates are applied, and with which period's composition.
- Decisive step: converting the simple-assault line separately for domestic and other assaults, each January to
  October month at its own domestic share, because the line's pooled rate in the dual-coded months is a mixture whose
  weights are the holiday weeks'.
- Not semantics: every field read correctly (the summary class, the NIBRS offense, the weapon and force codes, the
  relationship codes, the methodology note's definition of the restated year) still leaves the per-line conversion,
  which is the standard practice, on a fall of about 3 per cent; no field, code or definition says that the
  simple-assault line's rate moves with its domestic share or which months to weight it by.
- Not rule application: no filed rule says how to restate January to October; executing the NIBRS definitions, the
  hierarchy rule's end and the methodology note word for word fixes the target and the dual-coded months' rates, and
  still files the per-line conversion's fall; which rates to apply to which months' counts is an estimation choice.
- Analyst test: with the data cleaned and every rule read correctly, a strong analyst builds the conversion per Return
  A line from the dual-coded months, applies it month by month to January to October 2024 and files a fall of about
  3.3 per cent (the `Ends on:` figure), where converting the simple-assault line by domestic and other assaults at
  each month's own mix gives a rise of about 2.4 per cent.
- Estimand: the scorecard methodology note files the population (offenses against victims reported to the Ellsmere
  Police Department), the outcome (NIBRS offense 13A, one per victim), the window (calendar 2024 and 2025 by month
  reported), the unit (offenses) and the comparison (2025 against 2024 as NIBRS would have counted it had the
  department reported to NIBRS all year).
- No decoy: nothing is planted; the state program's certification letter reports its own comparison of the two
  November and December returns and recommends no restatement; no memo, draft or stakeholder figure argues a method.
- No certified replay: the method is not hidden and recovered by reproducing certified figures; every rate set from the
  dual-coded months reproduces those months by construction, the golden included, so nothing certified arbitrates.
- Lesson: a conversion rate measured on a short window where both codings exist holds only at the level where it is
  stable; carried per published line it imports the window's mix, and the mix has to be rebuilt period by period from
  the record that carries it; the composition builds on file (task68, task83, task473, task477) price a pooled rate on a
  population or a forecast, and none restates an official series across a coding break.

## Tried and rejected


# task272 design note

Architecture 2, drawn 2026-10-21 (wave 4, Descriptive lane, sathay3012) after architecture 1 was spent at stage 4 (its record below), in seed DA22's world, decision and quantity: a health foundation's FY2027 coaching grants, one per qualifying organisation, a six-point line, 31 applicants and the board's budget vote on 12 March 2027. The Vellacott Health Foundation in Portland, Oregon funds decision coaching for the financial-assistance teams of the Fair Assistance Collaborative's 31 hospitals in Oregon and Washington, whose three billing hubs pool their determination extracts. The collaborative's 2026 standard assesses a household's income over the twelve full calendar months before the month it applies; in 2025 the common policy read it from the three full months before, times four. From 1 July 2027 the foundation funds one coaching grant for each hospital where at least six percent of the 2025 applications from households within the free-care limit on their twelve-month income left the household owing more than half of its balance (a denial, or an approval at a 25 percent discount). Kristin Robertson, the foundation's program officer, needs the number of grants for the FY2027 budget.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task272.json`, architecture 2, registered 2026-10-21 03:54Z at WARN (item 9), architecture 1's identity in `lineage` with its fate. The foundation funds the coaching (`foundation_or_funder`); its board votes the FY2027 budget on 12 March 2027 (`board_of_directors`, `vote_or_meeting`); the requester is the foundation's program officer (`programme_officer`). Context artifact `operations_log`: the three hubs' determination logs, which carry each application's household, income quarter and decision and are what the call is read from. Calibration organ `retry_or_revision_log`: the households' own further applications in another season, the only record of a household's income outside the quarter it applied in.
2. Pairing: demographic-social-science (house domain) / income-poverty-inequality, client domain Sociology & Demography, task type social-mobility-inequality-measurement (the README tags it DD). The task type's own object decides the call: a household's income over a year against the poverty line, read from one period's income, the reference-period problem of income and poverty measurement.
3. Niche: a health foundation's FY2027 decision-coaching grants for its collaborative's hospital financial-assistance teams, one per hospital whose 2025 decisions most often left households that the 2026 standard makes eligible on their twelve-month income owing more than half of their balance, when the 2025 policy read income from the three months before the application and much of the region's work follows harvest, fishing and resort seasons.
4. Call and shape: how many grants the FY2027 budget carries (`quantity_figure`, a count; question form how-many). Shape 08 (a rule replayed on history): the collaborative's 2026 income standard, already decided, replayed on each hospital's 2025 applications to see how the 2025 decisions did against it; each hospital's share of the applications the standard makes eligible that left the household owing more than half of its balance is checked against six, the qualifying hospitals named and the count, the shares charted.
5. Gate G `method_or_model_selection`, strategy `time_semantics`: every record states the 2025 decision and the income it was made on correctly; the quantity the criteria file is each household's income over the twelve months before it applied, which no record holds. Two estimators of it stand, the 2025 policy's own (the three months before the application times four) and a calendar estimate (the quarter put on a yearly basis by its share of the year of that kind of work in that region), and the households seen in more than one season decide between them: their quarters differ by the calendar's ratio, which the quarter-times-four reading says is one. Decisive generators G13 (horizon mismatch: the quarter against the year) then G16 (method selection). The strategy label is the honest one (the income's reference period read through the local seasonal calendar); its `three_rules.strategy_risk` WARN is answered in item 9.
6. Data-native sentence: a third of the collaborative's hospitals serve towns whose work follows a season (tree fruit in the Yakima and Wenatchee valleys, berries in the Skagit and Whatcom, potatoes and onions in the Columbia Basin, crab and resort seasons on the coast and at Bend), and the 2025 policy read each household's income from the three months before it applied, so a household that applied after its season was assessed on its best quarter and one that applied in the slack months on its worst.
7. Sources, one line each:
   - The client's rigor library, social-mobility-inequality-measurement 2 (single-year income attenuates persistence; permanent income from multi-year averages): the cousin of this build's step, a reference period too short for the income it stands for; there the pin files the averaging window, here no record holds the twelve months and the calendar of each kind of work has to be read from the households seen twice.
   - The lane's builds (task263 BISG unmixing, task264 visit-weighted exits, task267 design weights, task268 losses to follow-up, task269 a decision study, task270 range restriction, task271 the kin-cohort, task272 v1 serial dependence): none estimates a household's income over a reference period it was not measured in.
   - `guard.py slots` on seasonal, annualised, harvest, twelve-month income, farmworker and reference period: no screen of this mechanism on file (task157's seasonal workers are a return wave to a funding date; task135's twelve-month income is a custodian's entitlement report).
   - The nearest idea on file, below the text screen (0.05): task17's third revision applies a mandated, filed calendar factor before carrying a part-period rate forward; here no factor is filed, each region's calendar for each kind of work is estimated from the applications, and the trap is pooling it across places or kinds of work (recorded in the card's `differentiation`).
8. People: kept from architecture 1, drawn with `guard.py names --geo "United States" --seed 272`: Kristin Robertson (the foundation's program officer, the requester) and Spencer Frank (the foundation's director of programs, who takes the budget to the board). Invented names Vellacott Health Foundation and Fair Assistance Collaborative, screened against the H21 register at architecture 1's stage 3.
9. BLOCKs cleared and WARNs answered. The pull before registration brought task482 v4, task478 v4 and task486 v2 into the window, and three axes were redrawn: `ban.artifact` filed_standard against task482 v4 (the context artifact is the hubs' determination logs, `operations_log`, which is what the call is read from; the criteria are the estimand's home, not the stakeholder's working file), `ban.shape` 10 against task482 v4 (shape 08 is the more exact label: the 2026 standard is a decided rule replayed on 2025's applications, and each hospital's replayed outcome is checked against six), `ban.forcing_event` budget_or_appropriation against task486 v2 (the board's vote on 12 March 2027 is the meeting that forces the count, `vote_or_meeting`). WARNs: `three_rules.strategy_risk` time_semantics (the analyst test reads every field, code and rule correctly, the 2025 policy and the 2026 standard included, and still files the policy's quarter times four as the twelve-month income, so the call does not turn on a reading); `repeat.gate_g` method_or_model_selection against task482 v4 and `overuse.gate_g` (6 of the last 12): the honest key, two estimators of one filed quantity with the records choosing, and no other mechanism carries this step.
10. Screens, run as code at the draw (scratch `t272/p2/p1.py` and `p2.py`; the world's own generator to come), to be asserted on the built world in `generator/checks.py`:
    - WHAT screen: population (each hospital's 2025 applications decided by a counsellor on first review), outcome (a denial or a 25 percent discount, which leave the household owing more than half), window (decided in calendar 2025), unit (percent of the eligible applications), comparison (against six) and the eligibility line (income over the twelve full calendar months before the month of application at or below 200 percent of the 2025 poverty guideline for the household's size) are filed in the criteria; the decisive step settles none of them, it estimates the twelve-month income that the records hold only as one quarter.
    - 1.2a: the filed quantity is unobserved (no record holds a household's twelve months); the policy's quarter times four and the calendar estimate are estimators of it, and the households seen in two seasons decide between them.
    - 1.2b: the change from the 2025 policy to the 2026 standard is filed in words, and filing it does not perform the computation: the sentence says what is wanted and no record carries it, while the reapplications measure each calendar themselves (case two).
    - Ladder, built (Ladder below): the policy's quarter times four files 5 of 31; one calendar for every seasonal kind of work 6; one calendar per kind of work across regions 10; one per region or per hospital across kinds of work 10; region by kind of work 16, every member of the family agreeing; the generator's own twelve-month incomes 16. The prototype (p2, seed 1) had filed 10, 20, 20, 22 and 23; the world was rebuilt to widen each pooled calendar's gap.
    - Determinism screen: the within-household and the cross-sectional calendars by region and kind of work agree (no selection on level by month); the year is each month counted once (the arithmetic mean of the windows), against a log-mean normalisation, which is an execution error and not a reading.

## Default path

1. Read the criteria: a hospital qualifies when at least six percent of its counsellors' 2025 first-review decisions on households within the free-care limit (income over the twelve full calendar months before the month of application at or below 200 percent of the 2025 guideline for the household's size) left the household owing more than half of its balance (a denial for any reason, or an approval at 25 percent).
2. Conform the three hub extracts by the data guide: the Puget hub's three-month total times four, the Willamette hub's yearly figure, the Columbia hub's monthly average times twelve; the Columbia hub's UTC clock put on Pacific time; H23's rows joined across the two hubs through the crosswalk; each application's first approval or denial by a counsellor kept, without reconsiderations, pends, withdrawals or the presumptive screening.
3. Take each application's recorded income on the 2025 policy's yearly basis as the household's income over the twelve months before it applied (the only income the records hold for the application), and keep the applications at or below 200 percent of the 2025 guideline for the household's size.
4. Count the denials and the 25 percent approvals among them, divide by the applications kept, and compare each hospital's share with six.

Ends on: 5 grants (H11, H15, H17, H23 and H26).
Golden: 16 grants (H02, H08, H10, H11, H12, H14, H15, H17, H20, H22, H23, H24, H26, H28, H29 and H30).

## Stump sentence

A competent analyst who conforms the three hubs, keeps each application's first review and takes the 2025 policy's yearly figure (the three months before the application times four) as the household's income over the twelve months before it applied names 5 hospitals for the FY2027 grants, H11, H15, H17, H23 and H26, because a household whose main earner's pay follows a harvest, packing, fishing, logging or resort season was assessed on one quarter of its year, its best when it applied after the season; one calendar for every seasonal kind of work files 6, one for each kind of work across regions 10, one for each region or each hospital across kinds of work 10; only each region's calendar for each kind of work, read from how the yearly figure on the applications moves with the month of application, puts each quarter on a twelve-month basis and names the 16.

## Three rules

Task type: social-mobility-inequality-measurement (Sociology & Demography), which serves Descriptive & Distribution Analysis in the taxonomy: a household's income over a year set against the poverty line for its size, read from income measured over a shorter period.
Domain test: the quantity that decides the call is each household's income over the twelve months before it applied, against 200 percent of the 2025 poverty guideline for its size; income and poverty measurement estimates an annual income from a short reference period by putting the period on a yearly basis with the seasonal pattern of the household's income source, the main earner's kind of work in its region, which is the reference-period problem every survey that measures income over a month or a quarter meets when it reports a year's poverty.
Swap: "which of our 31 stores get a coaching grant, where at least six percent of the 2025 loyalty sign-ups from shoppers within the value tier on their twelve-month spend paid the full price": a shopper's spend has no main earner whose pay follows a harvest, packing, fishing or resort season in its region and no household size or poverty guideline, so the step that decides the call (each quarter's income put on a yearly basis by the calendar of the earner's kind of work in the household's region) has nothing to act on.
Layer 1: the three hubs' own layouts and income conventions (the Puget hub's three-month total, the Willamette hub's yearly figure in whole dollars, the Columbia hub's monthly average and UTC clock); the work list as text, number and short code by hub; H23's billing conversion between hubs on 2 June 2025 with counsellor and guarantor numbers re-keyed (the two-sheet crosswalk); pends, withdrawals, reconsiderations and the nightly presumptive screening among the decisions; the denial reason list renumbered on 1 July 2025; write-offs carried on every account an approval covers; the Willamette hub's December 2025 adjustment lines loaded twice; reversals posting into 2026. Each is what the hubs' and the warehouse's systems produce and nothing is placed to be caught; on the call's path each mishandled keeps the call or is closed by a filed clause (SF1 to SF13 asserted).
Layer 2: method_or_model_selection: the twelve-month income estimated from one quarter through the seasonal calendar of each kind of work in each region, read from how the yearly figure on the 2024 and 2025 applications moves with the month of application, against the 2025 policy's quarter times four (a flat year) and against calendars pooled over regions or over kinds of work whose seasons fall in different months.
Decisive step: putting each application's three-month income on a twelve-month basis with its region's seasonal factors for the main earner's kind of work, rather than reading the quarter times four as the year, or pooling one calendar across regions or across kinds of work.
Not semantics: every field read correctly (each hub's income convention, the work codes, the outcomes and discounts, the clocks, the H23 crosswalk) and every definition in the criteria applied still leaves the twelve months' income unrecorded: no field holds it, the guide says exactly what the three-month figure is, and the easy route on correctly read records (the 2025 policy's yearly figure as the twelve-month income) files 5 hospitals.
Not rule application: the criteria fix the population (each hospital's 2025 first reviews by counsellors), the outcome (a denial or a 25 percent discount), the eligibility line (twelve months' income at or below 200 percent of the 2025 guideline), the unit and the comparison; no filed rule or procedure says how a twelve-month income is had from a three-month record, and executing every stated rule on the records' own figure files H11, H15, H17, H23 and H26.
Analyst test: a strong analyst who conforms every hub correctly, applies criteria 2.1 to 2.5 and takes the 2025 policy's yearly figure (the three months before the application times four) as the household's income over the twelve months before it applied files 5 grants (H11, H15, H17, H23 and H26); only each region's seasonal calendar for each kind of work names the 16 (`checks.py`, ANALYST TEST, on the generator's clean records).
Estimand: the criteria (`fac_decision_coaching_criteria_fy2027.pdf`): 2.1 "at least six percent of the applications its counsellors decided in 2025 from households within the free-care limit left the household owing more than half of its balance"; 2.2 each application's first approval or denial by a counsellor, 1 January to 31 December 2025 by the hospital's local date, each application counting once; 2.3 "its income over the twelve full calendar months before the month in which it applied was no more than 200 percent of the 2025 federal poverty guideline for its size"; 2.4 a denial for any reason or a 25 percent discount; 2.5 percent of the applications within the limit, compared with six unrounded; section 3 the guideline and the limit by household size.
No decoy: no memo, briefing, draft, published table or stakeholder figure states a hospital's share, a seasonal factor or a twelve-month income, or ranks the hospitals; the data guide says what each hub's income field records (the 2025 policy's basis) and makes no claim about the twelve months; the patient-experience survey and the state charity care filings answer other questions.
No certified replay: no published or certified share, calendar or seasonal factor is shipped to be reproduced; the calendars are estimated from the extracts' own applications and are checked against nothing the pack certifies.
Lesson: an income measured over a quarter stands for a year only where the year is flat; where a household's pay follows a season, the quarter before an application says as much about the month as about the household, and the factors that put it on a yearly basis come from the place and the kind of work together, because the same work keeps different months in different regions. No build on file puts a short reference period's income on an annual basis (the lane's builds estimate exits, design weights, losses to follow-up, reliability, range restriction, penetrance and a sequence effect).

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R1 (the default path) the 2025 policy's yearly figure as the twelve-month income | the guide: the figure is the three full months before the month received, times four | the income field in each extract | the record's own income, already on a yearly basis | none | none | one comparison per application | readable |
| R1b each household's own applications within the twelve months averaged | none | the household key across applications | a household's other records | none | none | a group-by on the household | readable |
| R1c the applications from seasonal work left out | none | the work field | drop the rows the policy assessed worst | none | none | one filter | readable |
| R1d one calendar for every seasonal kind of work | none | the work field and the received month | a seasonal adjustment of the seasonal applicants | none | none | a group-by on month | readable |
| R1e one calendar for each kind of work across regions | none | the work field and the received month | a seasonal factor per occupation | none | none | a group-by on kind and month | readable |
| R1f one calendar for each region or each hospital across kinds of work | none | the member file's region and the received month | a seasonal factor per area | none | none | a group-by on region and month | readable |
| (decisive) R2 each region's calendar for each kind of work, the yearly figure divided by its month's factor | none: the criteria name the twelve months and the guide the three, and no file says that a household's pay follows its work through the year or that one kind of work keeps different months in different regions | no column holds a month factor or a twelve-month income; the region sits in the member file, not in the extracts | none: the reflexes for a short reference period (the quarter times four, the household's other applications, one seasonal factor per occupation or per area) leave the regions' different seasons pooled | none: no shipped figure ties under either reading | none: the battery passes on the records as written (one first review an application, every hub conformed, every join complete) | a group-by on region, kind of work and month, once the season is seen | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | by the hospital's local date | the Columbia hub's UTC clock put on Pacific time | the UTC clock read as local | same call (asserted) | criteria 2.2; the data guide section 4 (ts_utc) |
| SF2 | a counsellor decided on first review | each application's first approval or denial | reconsiderations counted as first reviews | same call (asserted) | criteria 2.2: "A reconsideration, a pend or a withdrawal is not a first review" |
| SF3 | a decision | an approval or a denial | pends and withdrawals counted as denials | 30 hospitals (asserted different) | criteria 2.2 |
| SF4 | denies the application, for any reason | every denial, documents not received included | a denial for documents not received left out (the household could send them and apply again) | 0 hospitals (asserted different) | criteria 2.4: "for any reason" |
| SF5 | the month in which it applied | the month the hospital received the application | the month of the decision | same call (asserted) | criteria 2.3; the data guide (the received-date columns) |
| SF6 | owing more than half of its balance | a denial or a 25 percent discount | a 50 percent discount counted as well | 22 hospitals (asserted different) | criteria 2.4 |
| SF7 | the 2025 federal poverty guideline | the 2025 guideline for every application | the guideline of the year the application was received | same call (asserted) | criteria 2.3 and section 3 |
| SF8 | each application counts | a household that applied more than once counts once for each application | each household once, its last 2025 decision | same call (asserted) | criteria 2.2: "counts once for each application" |
| SF9 | decided in 2025 | first reviews from 1 January to 31 December 2025 | applications received in 2025 | same call (asserted) | criteria 2.2 |
| SF10 | at least six percent | six or more, unrounded | above six; the share rounded first | same call: no hospital within 0.88 points of six under any member of the family (asserted) | criteria 2.1 and 2.5 |
| SF11 | each application's first approval or denial | the first review's outcome | the application's last decision, a reconsideration's in place of the first | 6 hospitals (asserted different) | criteria 2.2 |
| SF12 | H23's applications | each first review in the extract of the hub that held the hospital on its date, joined through the crosswalk | the Columbia rows alone, or the Puget rows alone | not a fork: every H23 first review sits in exactly one extract (asserted) | the data guide section 1; the crosswalk |
| SF13 | no more than 200 percent | at or below the limit | strictly below | same call (asserted) | criteria 2.3: "no more than 200 percent" |

## Ladder

Built figures from the cut pack (`generator/analysis.py`, every route in `generator/models.py`, asserted in `generator/checks.py`, recomputed by `generator/verify.py`). Each hospital's share of its counsellors' 2025 first reviews on households within the free-care limit that left the household owing more than half of its balance, percent:

| Rung | Construction | Grants | Hospitals over the line | What kills it |
|---|---|---|---|---|
| R1 (the default path) | the 2025 policy's yearly figure (three months times four) as the twelve-month income | 5 | H11, H15, H17, H23, H26 | assumes a flat year; a household that applied after its season was assessed on its best quarter |
| R1b | each household's own applications within the twelve months, averaged | 6 | H11, H12, H15, H17, H23, H26 | three in four 2025 applications have no other from the household in the twelve months before, so the average is the same quarter |
| R1c | the applications from seasonal work left out | 5 | H11, H15, H17, H23, H26 | leaves out the households the 2025 policy assessed worst |
| R1d | one calendar for every seasonal kind of work | 6 | H11, H12, H15, H17, H23, H26 | a farm, a fishing and a resort household peak in different months |
| R1e | one calendar for each kind of work across regions | 10 | H11, H12, H14, H15, H17, H20, H23, H24, H26, H30 | the same work keeps different months in different regions |
| R1f | one calendar for each region across kinds of work | 10 | H11, H12, H14, H15, H17, H22, H23, H26, H29, H30 | a region's farm, packing and resort households keep different months |
| R1g | one calendar for each hospital across kinds of work | 10 | H11, H12, H14, H15, H17, H22, H23, H26, H29, H30 | as R1f, hospital by hospital |
| R2 (golden) | each region's calendar for each kind of work, month means (golden) | 16 | the golden 16 | none |
| R2 | the same, geometric month means | 16 | the golden 16 | none |
| R2 | the same, two-way fixed effects on the households seen in more than one month | 16 | the golden 16 | none |
| R2 | the same, the seasonal kinds of work only | 16 | the golden 16 | none |
| R2 | each hospital's own calendar for each kind of work | 16 | the golden 16 | none |
| R2 | each region's calendar for each kind of work from 2025's applications alone | 16 | the golden 16 | none |

Shares by hospital under the routes that pool the calendar, the golden and its fixed-effects member (R2 FE: the households-seen-twice calendar where a cell identifies one, the cell's month means where it does not):

| Hospital | R1 | R1d | R1e | R1f | R1g | R2 | R2 FE |
|---|---|---|---|---|---|---|---|
| H01 | 4.5 | 4.5 | 4.6 | 4.5 | 4.5 | 4.6 | 4.6 |
| H02 | 5.5 | 5.6 | 5.8 | 5.5 | 5.5 | 7.7 | 7.6 |
| H03 | 2.8 | 2.8 | 2.8 | 2.8 | 2.8 | 3.9 | 3.9 |
| H04 | 3.2 | 3.2 | 3.5 | 3.3 | 3.3 | 4.7 | 4.8 |
| H05 | 4.2 | 4.3 | 5.0 | 4.2 | 4.2 | 4.8 | 4.9 |
| H06 | 3.0 | 3.0 | 3.1 | 3.0 | 3.1 | 3.6 | 3.6 |
| H07 | 3.1 | 3.1 | 3.7 | 3.4 | 3.5 | 4.3 | 4.4 |
| H08 | 4.5 | 4.6 | 5.9 | 5.5 | 5.5 | 7.4 | 7.0 |
| H09 | 2.7 | 2.6 | 2.9 | 2.9 | 3.0 | 4.4 | 4.4 |
| H10 | 4.6 | 4.8 | 5.4 | 6.0 | 6.0 | 7.9 | 8.1 |
| H11 | 6.1 | 6.2 | 6.1 | 6.5 | 6.5 | 7.4 | 7.5 |
| H12 | 5.9 | 6.1 | 6.0 | 6.1 | 6.1 | 8.6 | 8.7 |
| H13 | 3.4 | 3.5 | 4.2 | 3.8 | 3.7 | 5.0 | 4.9 |
| H14 | 5.8 | 5.8 | 6.4 | 6.3 | 6.1 | 7.4 | 7.5 |
| H15 | 8.7 | 8.8 | 8.8 | 8.8 | 8.8 | 8.8 | 8.7 |
| H16 | 3.1 | 3.1 | 3.1 | 3.1 | 3.1 | 3.1 | 3.2 |
| H17 | 9.5 | 9.5 | 9.5 | 9.6 | 9.6 | 9.7 | 9.6 |
| H18 | 2.4 | 2.4 | 2.4 | 2.4 | 2.4 | 2.5 | 2.5 |
| H19 | 4.2 | 4.1 | 4.2 | 4.2 | 4.1 | 4.2 | 4.1 |
| H20 | 5.3 | 5.4 | 7.1 | 5.3 | 5.3 | 8.4 | 8.2 |
| H21 | 3.7 | 3.7 | 3.8 | 3.8 | 3.7 | 3.8 | 3.8 |
| H22 | 4.7 | 4.6 | 5.0 | 7.2 | 7.1 | 7.7 | 7.7 |
| H23 | 6.2 | 6.3 | 7.1 | 6.7 | 6.8 | 7.8 | 8.0 |
| H24 | 4.9 | 4.8 | 6.5 | 4.8 | 4.8 | 7.3 | 7.1 |
| H25 | 3.9 | 4.0 | 3.8 | 3.9 | 4.2 | 4.7 | 4.7 |
| H26 | 6.6 | 6.6 | 7.3 | 7.0 | 7.5 | 8.2 | 8.2 |
| H27 | 3.3 | 3.4 | 3.4 | 3.5 | 3.3 | 4.5 | 4.5 |
| H28 | 4.9 | 5.2 | 5.1 | 5.3 | 5.3 | 7.6 | 7.2 |
| H29 | 5.3 | 5.2 | 5.7 | 8.9 | 9.1 | 9.1 | 9.2 |
| H30 | 5.1 | 4.9 | 6.5 | 6.1 | 6.0 | 7.5 | 7.5 |
| H31 | 2.5 | 2.5 | 3.0 | 2.6 | 2.6 | 4.3 | 4.0 |

The family closes on the call: every member names the same 16, the closest any member comes to the line is 0.88 points, and medians by month name the 16 too; geometric scaling of the factors (the year's factors averaging one geometrically rather than arithmetically, an execution error) names the 16 as well. The generator's own twelve-month incomes name the same 16. Golden shares run 7.27 to 9.72 percent at the qualifying hospitals and 2.46 to 4.96 at the others.

The world under it: 31 hospitals in 14 regions; at each, households in up to six seasonal kinds of work (farm and orchard, packing, fishing, resort, logging, construction) with a calendar of their own by region, and households in year-round work; pay rises unevenly from year to year (about 3 percent) and varies month to month; a household denied or given part of its balance applies again, now and then, once its work takes its pay down; 2023 is simulated so coverage reaches its steady state before the extracts open. Each hospital's documents-denial rate is set so its golden share lands on a designed value, irregular between 7.27 and 9.71 at the qualifying hospitals and between 2.46 and 4.92 at the others.

Position and separation: the easy route (R1) files 5, the calendars pooled by kind of work, by region or by hospital file 10, 10 and 10; 11 hospitals (H02, H08, H10, H12, H14, H20, H22, H24, H28, H29, H30) qualify on the golden and not on the easy route. The clean-data test (ANALYST TEST in `checks.py`): on the generator's own records, every field read and every filed rule applied, the 2025 policy's yearly figure files the 5, and the decisive step alone files the 16.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | each hospital's applications decided on first review by a counsellor in 2025 | filed: criteria 2.1 and 2.2 |
| 2 Unit of account | the application; a household that applied more than once counts once for each | filed: criteria 2.2 (SF8) |
| 3 Attribution window | decided 1 January to 31 December 2025 by the hospital's local date | filed: criteria 2.2 (SF1, SF9) |
| 4 As-of dating | the twelve full calendar months before the month in which the household applied; the received date marks the month | filed: criteria 2.3; the data guide's received-date columns (SF5) |
| 5 Version basis | the 2025 decisions as recorded; the income as the 2026 standard counts it | filed: criteria 2.3 |
| 6 Denominator | the applications from households within the free-care limit | filed: criteria 2.1, 2.3 and 2.5 |
| 7 Weighting | none: each application counts once | filed: criteria 2.2 and 2.5 |
| 8 Window length | twelve full calendar months | filed: criteria 2.3 |
| 9 Boundary inclusivity | no more than 200 percent of the guideline; at least six percent | filed: criteria 2.1, 2.3 and 2.5 (SF10, SF13) |
| 10 Rounding path | compared unrounded; the verdicts and the count are graded, not the shares | filed: criteria 2.5; the prompt |
| 11 Tie-break | none needed: no hospital within 0.75 points of six under any member of the family | C1 asserted (SF10) |
| 12 Maturity and censoring | every 2025 first review is decided by definition; a pend or a withdrawal is not a first review | filed: criteria 2.2 (SF3) |
| 13 Order of operations | conform the hubs, the first reviews, the twelve-month income, the eligible, the owing, the share, the comparison | C1 |
| 14 Row order | none matters | C1 |
| 15 Duplicate resolution | one first review an application, its first approval or denial | filed: criteria 2.2 (SF2, SF11) |
| 16 Identity normalisation | H23's guarantor numbers across the conversion; the hospital codes common to the hubs | the data guide section 1; the crosswalk (SF12) |
| 17 Netting against gross | none on the call | C1 |
| 18 Dimensional units | each hub's income convention: a three-month total, a yearly figure, a monthly average | the data guide sections 1 to 4 |
| 19 Code and status semantics | outcomes and discounts by hub; denial reasons | the data guide sections 2 to 5; criteria 2.4 (SF3, SF4, SF6) |
| 20 Integerisation | grants in whole hospitals | C1 |
| 21 Clause scope | section 2 for the call; section 3 for the limit by household size | filed |
| 22 Forward window contents | the 2025 decisions measured against the 2026 standard stand for the coaching each team needs from 1 July 2027 | filed: criteria 1.1 to 1.3 and 2.1 |

## Literal reader

Executed word for word, the criteria file each hospital's share as the percent of its counsellors' 2025 first-review decisions on households whose income over the twelve full calendar months before the month of application was no more than 200 percent of the 2025 guideline for their size that denied the application or approved it at 25 percent, compared with six unrounded. The records give every one of those decisions and, for each, the household's income in the three full calendar months before the month of application (on the three hubs' bases), the main earner's kind of work and, through the member file, the hospital's region; no field holds the twelve months, and the literal estimand still asks for them. The quarter times four estimates them only if a household's income is the same in every quarter, which the records refute: across 2024 and 2025 the mean yearly figure, as a share of the guideline, on the applications from one region's households in one kind of seasonal work is 4.21 times higher in its best month of application than in its worst at the median of the 32 seasonal cells (9.56 times for the Northwest Washington fishing households), the same kind of work peaks in different months in different regions (farm and orchard work on applications received in November in the Columbia Basin and Central Washington, in September in Northwest Washington and the Columbia Gorge, in August in the Willamette Valley), and 10,050 pairs of a seasonal household's own applications in different months move with that calendar's ratio (the log ratios correlate at 0.989; EVIDENCE in `checks.py`). Putting each quarter on a yearly basis by its region's factor for its kind of work and month is the estimate the records support, and every member of the family (arithmetic or geometric month means, the two-way fixed effects on the households seen in more than one month, the seasonal kinds of work only, each hospital's own calendar for each kind, 2025's applications alone, monthly medians) names the same 16; the households' own twelve months in the generator name them too.

## Oracles

No shipped figure states a hospital's share, a twelve-month income, a seasonal factor or a calendar, and none ranks the hospitals. The data guide states what each hub's income field records (the 2025 policy's basis and its discount schedule), which every reading shares. The state charity care filings are each hospital's own fiscal year at full charges and the survey is by payer group; neither ties to any share under any reading. No control total ties only under the golden or only under the easy route.

## Ask sheet

The asks are decoupled from the call: neither reads an application's income, its kind of work or its month, and the call computes from the three extracts, the crosswalk and the member file alone, reads no adjustment, account, survey or filing, and is unchanged with every reason code blanked (SEPARATION, asserted). They are the two scorecard columns the foundation's workbook carries for every hospital beside the verdict: what the counsellors' approvals gave in assistance, and the denials the coaching's documentation work addresses. Each is a measure every hospital carries that the call does not turn on.

**Ask A. For each hospital, the assistance written off on its counsellors' 2025 approvals, net of the reversals posted by 31 March 2026, thousands of dollars to one decimal (31 figures).**
- H18 home: the scorecard's assistance column, the size of each team's approvals beside its share.
- Use: the workbook's Grants FY2027 sheet.
- Path: the three extracts (approvals: hospital, application, guarantor, user, local date and type), the crosswalk's guarantor sheet (H23's numbers across the conversion), the adjustments (hospital, application the line posted under, account, posted date, code, amount) and the accounts (account, guarantor, balance): six files, about twelve columns.
- Primary device (D7, the true key elsewhere): an approval on a household's later application for the same bill posts its write-offs under the number the household's first application carried, so a write-off joined by the number on the line lands on a denied application, on an earlier approval (2024's as well as 2025's) or on no approval at all; the household's approval decided last before the line posted is the one that made it. Evidence, split and silent: at every hospital a write-off posts under a denied application, a second write-off posts under one number, or a write-off posts weeks after its number's own decision (asserted), and only the extracts' guarantor and decision dates tie each to the approval behind it.
- Shared hazards: D6 grain (each write-off repeats the approval's total on every account it covers, so a line can exceed its own account's balance at every hospital, asserted: one amount per number and posting date); D8 clock (write-offs and reversals on 2025 approvals posting in January to March 2026); D1 (the Willamette hub's December 2025 lines loaded twice, exact duplicates); the presumptive screening's approvals, which are not a counsellor's; reversals charged to the write-off they reverse, through the account.
- Stops (asserted): each application's write-off once, joined by its number (the cracker), misses all 31; every line as the extract gives it misses all 31; one amount per number and posting date joined by number misses all 31; every 2025 posting under an approval's number misses all 31; the golden's attribution with the presumptive screening kept misses all 31; with the reversals ignored misses all 31; with the twice-loaded lines kept misses the Willamette hub's hospitals.

**Ask B. For each hospital, its counsellors' 2025 denials for documents not received, whole counts (31 figures).**
- H18 home: the scorecard's documents column, the denials the coaching's case reviews and refresher work on.
- Use: the workbook's Grants FY2027 sheet.
- Path: the three extracts' denial rows (reason, local date, user, type) and the guide's reason list: four files, five columns.
- Primary device (D2, a vintage change): the collaborative's reason list was renumbered on 1 July 2025; documents not received was code 2 before and is code 1 from 1 July, and the guide prints only the current list. Evidence, silent: the denials a reconsideration reopens (the documents arrived) carry code 2 to 30 June and code 1 from 1 July at every hub (asserted), and codes 1 and 2 trade their monthly volumes at 1 July (the renumbering swapped them); nothing filed says so.
- Shared hazards: the reconsiderations' own denials (a counsellor's 2025 denial counts whatever the review); 2024's denials; the Columbia hub's UTC clock at the turn of the year and of 1 July.
- Stops (asserted): the guide's list for the whole year (the cracker) misses 30 of 31, equal only at H20, where the first half's income and documents denials happen to be equal (asserted: a tie is allowed only there); the old list for the whole year misses 30 of 31, equal only at H22, the second half's like case; both years on the right list misses all 31.

Main population zero-counts: device rows in the call's declared population: 0 (the adjustments and accounts are files the call never opens; the reason code is a column it never reads, asserted by blanking).

| Hazard | Asks moved | Per-ask delta (measured on the cut pack) |
|---|---|---|
| write-offs under the case's first number (D7) | A | every A off under the line's own number |
| the approval's total on every account (D6) | A | every A high when every line is summed |
| postings to 31 March 2026 (D8) | A | every A off when only 2025's postings count |
| the twice-loaded December lines (D1) | A | the Willamette hub's hospitals high |
| the reason list renumbered on 1 July 2025 (D2) | B | every B off on either list for the whole year |
| 2024's denials | B | every B high |

Referee: none (Oracles).

| Ask figure | The cracker's figure against the golden | Cracker (lands the call, runs the battery: exact duplicates dropped, one write-off per application where its lines repeat one amount, every join checked; reads the codes by the guide's list) |
|---|---|---|
| A, each hospital's assistance net of reversals (31) | off at every hospital: joined by the number on the line, write-offs from later approvals fall on denied or earlier applications | miss |
| B, each hospital's documents denials (31) | off at 30 hospitals: the first half of 2025 read on the current list; equal at H20, where that half's income and documents denials are equal | miss |

Mirror leakage: 1.6 per cent of the ask weight (the mirror, off the call at the 2025 policy's figure, reads the asks as the cracker does and keeps 1 of 62 figures, the H20 tie).
Pair ceiling: 29.4 (the cracker 45.9: the call, its components and instruction-following, 1 of the 62 ask figures; the mirror 12.9), measured on the cut pack.
Measured by: `generator/cracker.py` on the cut pack (`checks.py` runs it and asserts every miss).

## Leak check

`leak.py task272 --asof 2027-01-26`: REVIEW, no LEAK. Each REVIEW line, harmless:
- contents.txt and the criteria carry the program's name (Decision Coaching Grants, FY2027, budget): the call's words because they are the program's.
- The criteria carry the estimand's words (household, income, twelve full calendar months, percent, application): filed WHAT, the window and the line; "calendar" appears only in "calendar months". No file names a season, a harvest, a month factor, a calendar of a kind of work or a region's calendar (asserted in `checks.py`, LEAK words).
- The guide carries the extracts' own vocabulary (income, household, months, region, percent, application): column descriptions, the 2025 policy's basis and its discount schedule, and the member file's region column.
- contents.txt names the files (regions, applications, determinations): titles.
- The member hospitals workbook names the 31 hospitals beside region, hub, licensed beds and the date each joined; the state filings beside charity care at charges for each hospital's own fiscal year and the patients granted it: neither ranks them on the question, and the filings tie to Ask A under no reading.

## Architecture 1 record (spent 2026-10-21)

- Draw: the Vellacott Health Foundation's FY2027 Decision Coaching Grants, one per Fair Assistance Collaborative hospital whose financial-assistance counsellors are at least six points less likely to approve right after an approval than right after a denial on the same working day, on 2025 determinations pooled from three billing hubs. Golden: 11 grants ($704,000), H03, H06, H09, H10, H17, H19, H20, H21, H22, H26 and H31, from the within-day contrast less its expectation with each counsellor-day's determinations in every order; the counsellor-day fixed-effects slope files 23 and the pooled contrast 2.
- Build: stage 3 green on target.zip 90774da6 (checks 0 failed, the independent verifier PASS, two byte-identical builds, figures_check 82 of 82, precut 51, leak.py REVIEW answered, heart WARN), committed PAUSED at a84ba0db and 24b56b9e.
- Stage 4, two isolated scored readers (`score_reader.py --call-key call.qualify`): both landed the call with the golden set. Reader 1 (r272a) corrected each within-day contrast by shuffling the day's determinations and kept no ask figure (every FAWO line summed, 816,026.2 thousand; code 1 read for the whole year). Reader 2 (r272b) fitted counsellor-day fixed effects, named their bias at about 19 determinations a day unprompted and subtracted the null of 150 within-day permutations per hospital; it kept every Ask A figure (31 of 31: the write-off once per application, the twice-loaded lines dropped on adjustment_id, reversals per account) and no Ask B figure (code 1 for the whole year).
- Judge (the isolated thread's verdict.md, `determinism_check_report.md`): DETERMINISTIC, FIX_NOW on documentation only: every figure reproduced (197,939 determinations, the 11, $704,000, all 62 ask figures); the one live main-call reading is the uncorrected within-day contrast (23), which is the stump itself; the two ask conventions (the write-off once per application, the 1 July 2025 renumbering) recoverable from the data and unstated. Gate G method_or_model_selection and analytical_non_defect; Gate H pass.
- Fate: Gate F failed at both readers, so the architecture is spent. The small-sample bias of conditioning on the previous outcome inside a short sequence (the Miller and Sanjurjo hot-hand correction) is a named reflex for these readers: criteria that compare "the chance" within the same working day, beside queues of about 19, hand over the within-day permutation null. Ask B's renumbering held against both readers; Ask A's repeated write-off held against one.

## Tried and rejected

- The seed's own quantity (the Medicaid gap on the "would recommend" top-box rate across a state report's hospitals), every route screened at the draw: composition and patient mix settle the comparison population (WHAT screen); shrinkage of small cells repeats task253; design weighting repeats task264's lesson and task268 v2's reflex; nonresponse either fails determinacy or repeats the inverse-probability weighting of task264, task267 and task268; survey mode effects belong to Experiment & Causal Analysis; misclassification is the spent sensitivity-and-specificity family; nowcasting the late returns repeats task181; telescoping sits next to task453.
- A race-probability (BISG) regression for the equity gap (prototype `p1.py`): a strong ladder, but the same linear unmixing of a mixed population as task263, a clone of its driver.
- Traffic count factor groups for an annual average (prototype `t1.py`): count differences of one or two units at tiny margins, and the ground overlaps task474.
- The sequence effect at queues of 4 to 14 determinations with effects of 2 to 13 points (`s1.py`, `s2.py`): the two corrected estimators (the excess over reordering by counts, the held-day slope less its reordering expectation) disagreed on 1 to 3 hospitals a seed, with the closest margins 0.01 to 0.3 points; the queues were lengthened and the effect hospitals separated from the line.
- Effects of 12 to 17 points (`s4.py`, `s5.py`): the family agreed, but the day's rate without the pair as a control landed 10 or 11 of the 11 hospitals, its bias of 3 to 5 points smaller than the gap to the line; the effects were lowered to 9.5 to 12.5 with a wider day mix (`s6.py`), where it lands 9.
- Ask B as presumptive approvals with nightly re-runs replayed under fresh application numbers (D1): dropped at stage 2, because no asking sentence makes the count determinate without naming the device (a replay is a fresh application record, so "each application once" counts it, and any wording that excludes it narrates the re-run); replaced by the reason list renumbered on 1 July 2025 (D2).
- Queues of 6 to 28 a day with counsellors sitting on 55 percent of working days: the held-day route filed 28 of 31, an answer a reader distrusts on sight; queues of 8 to 32 on 48 percent of days put it at 23 with the family still closed (1.81 points).
- Effects of 9.5 to 12.5 points with the day's rate over the other determinations as a reflex: it landed the golden set (the others' count is the day's sufficient statistic), so it was moved into the family and the construction made every member agree, rather than the world bent to break it.
- Architecture 1 (each counsellor's sequence effect measured against the reordering of each working day's own determinations): spent at stage 4, both scored readers corrected the within-day contrast for the short-queue bias by permuting each day's determinations and landed the 11; a decisive step that is a named small-sample bias correction falls to a reader who knows the bias by name, however the ladder below it is tuned.
- The outcome "did not get free care in full" (a denial or any discount below 100 percent): noise in the year-round households' calendars inflated the shares at the 200 percent line, where the 2025 policy's full-care boundary sits on the eligibility line; the outcome moved to owing more than half of the balance (a denial or a 25 percent discount), whose policy boundary at 300 percent no year-round household's pay crosses.
- Households timing their applications to a low quarter (selection on the quarter): dropped in the prototype, no separation the seasons did not already give.
- Every hospital's designed share at 7.5 or 4.5 percent (the first build of this architecture): under the golden calendars 13 hospitals landed between 7.50 and 7.56 percent and 8 between 4.50 and 4.54, a cluster that confirms the golden route to a reader trying several calendars and reads as made in the chart; the designed shares were spread to irregular values, and the three set below what misassessment alone gives them (H04, H07 and H27, which then denied almost no one for documents) were raised to 4.29 to 4.68.
- Flat pay for year-round households and a fixed seasonal shape (the first builds of this architecture): a household's repeat applications carried the same three-month total to the cent, which reads as made; pay now rises unevenly from year to year and varies month to month, a household reapplies when its work takes its pay down (the season it knows) rather than on a month's luck, and the fixed-effects member falls back to a cell's month means where the cell does not identify its own calendar (the Olympic Peninsula's resort households: left unadjusted there, it had read H28 at 6.31; the reapplication change did not move that figure, the missing cell did).
- Also weighed at the re-root draw and dropped before any prototype, no reasons written down at the time: CGM, cash fills, TTR, a hungry-judges time-of-day effect, and heaping (already on file as spent in this lane).

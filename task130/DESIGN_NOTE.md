# task130: Elkhorn County's 2027 return-inspection officer (architecture 5, a re-root into psychology-behavioral-science)

Architecture 4 (Corvane Health's claims-made trust, shipped 10-16 at $1,250,000) is spent at the batch 1 triage
and sits in the card's lineage with every earlier architecture; `## Tried and rejected` keeps their record. This
architecture is a new client domain, world and dataset under the same objective and number.

## Draw

- **Pairing.** Client domain `psychology-behavioral-science`, task type
  `decision-making-computational-behavioral-modeling`, objective Forecasting & Predictive Modeling. Batch 1's live
  re-roots use energy (task118), epidemiology (task181), marketing (task268), actuarial (task306), survey research
  (task470), general statistics (task250), biomedical (task191), healthcare delivery (task482) and product analytics
  (task156); psychology is none of them, and psychology with forecasting has never been built.
- **The call.** Whether Elkhorn County Public Health adds a third return-inspection officer for 2027 under the 2027
  Food Safety Program Plan's staffing rule (a third officer when the routine inspections in the 2027 schedule that
  will be marked unsatisfactory exceed 540, the two officers' capacity), with the forecast the rule compares, to the
  nearest 100. Forward facing: the plan is issued on 11 January 2027 on the record to 31 December 2026, the decision
  falls by 29 January, and the window is calendar 2027.
- **Furniture.** Forum `line_manager_or_team` (the Environmental Health Director takes the decision on the program
  manager's forecast under section 3 of the plan); forcing event `budget_or_appropriation` (the third position is a
  2027 budget decision taken by 29 January so that the officer starts in March); organisation `local_government`;
  role `field_unit_lead` (the food safety program manager); context artifact `capacity_report` (the return team's
  2026 capacity report, which answers a past question, the team's 2026 return inspections against its capacity, and
  keeps the day-sheet log); calibration `none`.
- **World.** Elkhorn County, Washington (fictional, Pacific Time), county seat Marlow (fictional). The food safety
  program schedules 5,512 routine inspections at 2,648 establishments for 2027, ran eleven district inspectors in 2026
  and two return-inspection officers since February 2022. Erik Mayer and Andrew Mason retire on 31 December 2026 and
  are not replaced; the plan redraws the districts from eleven to nine, so about half of the scheduled establishments
  pass to another inspector than 2026's and 23 per cent fall to an inspector with no earlier inspection of the
  establishment on the record (4.8 to 9.2 per cent a year in 2022 to 2026).
- **Personas** (`guard.py names --geo "United States" --seed 130`, and `--seed 1130 --n 40` for the roster): Teresa
  Hansen (Environmental Health Director), Valerie Wood (Food Safety Program Manager), Mariah Ramirez and Tina Rivera
  (district inspectors who carry on into 2027), Erik Mayer and Andrew Mason (the two who retire); the rest of the
  roster is drawn the same way and screened by `guard.py surface`.
- **Structural labels.** Gap `population` first (an establishment's record is its inspectors' record, not the
  kitchen's), generators G14 (the pooled criterion does not fit first visits), G3 and G13; Gate G `forecasting`;
  strategy `forecast_method_backtest` (F6: the natural fit validates on the latest years and is wrong for 2027
  because each mark belongs to the pair that made it; only a hold-out on the 2023 appointee's first year separates
  the two); shape `other`.
- **Guard.** `check` on the registered card (2026-10-31T19:05:15Z): WARN only. `repeat.deliverables` (pdf+xlsx)
  against task250: the memo is the director's decision record, a PDF in the county's practice, and the prompt's
  openers differ from task250's. `repeat.question_form` (whether) against task250: the decision is a gate, the form
  the guide takes from it, at 11 per cent of prompts on file. `test.same_driver_older` differentiated against
  task134 v3, task146, task165 and task173 v1 (the card's lines). Nearest driver 0.06.
- **Screens.** `mechanisms --objective forecasting` read in full; `slots` on the mechanism words (inspector,
  examiner, leniency, strictness, rookie; familiarity, rotation, fresh eyes, capture, reassignment; first visit,
  repeat visit, redraw, district map, covering) and the setting words (restaurant, re-inspection, food safety,
  driving test, retest, test centre, pass rate). No note screens a judge's familiarity with the unit. The nearest
  records are task173 v1's service-desk opener tenure (abandoned unregistered at a guard window, never built) and the
  tenure deaths in task182, task202 and task171, on which this world's first-year-inspector variant was set aside.
- **Abstraction against the nearest approved builds.** task132 carries an item's wear past its probable replacement,
  a physical renewal of the unit; task141 reads a capped term's petitions at the rate of terms already at their
  maximum, a property of the term; task175 reads a lot's permit chance at the homes on the street it faces, a
  neighbour's state; task179 lifts a supervisee's risk by a victim record linked by name and birth date. task130
  reads a judge's mark at the number of earlier visits that judge has made to the unit, a property of the pair that
  no record holds and the redraw resets.
- **Shape (other), as built.** Call side: the call, the 2027 forecast to the nearest 100 and its comparison with 540
  (three criteria), the memo on one page and the two files (three). Asks on 2026, for each of the eleven 2026
  districts: the median return timeliness in working days (eleven), the median complaint response time in hours
  (eleven) and the return visit fees in dollars (eleven), 33 criteria. About 39 in all.
- **Data-native sentence.** A county's inspection record is written by a small team whose members see the same
  kitchens year after year, so every mark carries the pair's history, and when the map is redrawn that history goes
  with the inspector, not with the kitchen.

## Survivor anatomy

Actor: the property that decides is how many times the inspector named for each 2027 district has already inspected each scheduled establishment, and no file stores it: the exports list visits with an inspector and a permit, the schedule lists establishments with a 2027 district, Table 1 names a person, and the pair's history is a relation across the two exports and the roster that no column holds (R1 asserts that no column holds an earlier-visit count, a visit number or a tenure).
Link: the pair is read through a link no key offers: the legacy export keys inspectors by three initials, the new export by employee number and the plan's Table 1 by name, so the count needs the initials resolved through the roster's names ("Last, First M.") across the March 2024 migration and each 2027 inspector placed against each establishment's record in both systems; the field's rater methods cross the inspector with nothing, and no sentence or column invites crossing the inspector with the establishment's history.
Reflex: the field's methods for the deciding quantity sit at rungs 0 and 1 and file 424 to 458 with no third officer: base rates by risk category, each establishment's own record, one criterion per inspector (a rater-severity term read at Table 1's inspectors) and a first-year criterion for newly appointed inspectors, of whom 2027 has none.
Back-test: the textbook route validates: risk-category rates fitted on 2022 to 2024 predict 878 unsatisfactory routine inspections for 2025 to 2026 against 834 recorded (5.3 per cent over), and the golden's construction predicts 852 (2.2 per cent), so the latest-years hold-out does not separate them; only a hold-out on the 2023 appointee's first year does (137 recorded, category rates 47, visit classes 110).
Second use: every file the decisive step reads sits in the pack for a reason of its own: the two exports are every rung's data and every ask's, the roster is how any inspector rung reads the legacy initials and how ask A finds the return officers, the permits file carries the risk category every rung reads and the asks' 2026 districts, and the schedule and Table 1 are what every rung forecasts; deleting the decisive step drops no file.
Shock: the movement the step recovers reads as ordinary: in 2022 to 2026 an inspector's first visit to an establishment is 4.8 to 9.2 per cent of a year's routine inspections (covering days and the 2023 appointment), the yearly unsatisfactory counts run 362 to 480 with no break, the largest year (2023, 480) carries the year's retirement and appointment, and the 2027 redraw is the plan's own answer to two retirements.
Pins: the plan files the WHAT in its own genre (section 3: the routine inspections in the 2027 schedule that will be marked unsatisfactory, each counted as the inspector named in Table 1 for its district will make it, against 540; section 1: what makes a routine inspection unsatisfactory; section 2 and the schedule workbook: the population), and no filed sentence names earlier visits, familiarity, a first visit, rotation, tenure or experience (asserted on both PDFs).

## Default path

1. From the 2027 Food Safety Program Plan: the staffing rule (a third return-inspection officer when the routine
   inspections in the 2027 schedule that will be marked unsatisfactory exceed 540), the definition of an
   unsatisfactory routine inspection (25 red points or more, or a closure for an imminent health hazard), Table 1's
   inspector for each 2027 district and the schedule workbook's routine inspections for each establishment.
2. Stack the legacy export (January 2019 to March 2024: local times, inspector initials) and the new export (March
   2024 to December 2026: UTC stamps, employee numbers), resolve the initials through the roster's names, convert the
   UTC stamps to Pacific time and keep the routine inspections made (closed-premises calls out).
3. Rung 0, the base-rate model: each risk category's unsatisfactory share over 2022 to 2026 (or a logistic on risk
   category and establishment type), carried to the 2027 schedule: 437 (fitted on 2025 to 2026 only, 424; a linear
   trend in the yearly counts, 437). Fitted on 2022 to 2024 it predicts 2025 to 2026 within 5.3 per cent.
4. Rung 1, the field's rater models: each establishment's own record shrunk to its category (458), or one criterion
   per inspector (observed against expected unsatisfactory shares, or an inspector term) read at each 2027 district's
   named inspector (451); a first-year criterion for newly appointed inspectors changes nothing, since 2027 has none
   (437).
5. Compare with 540: no third officer.

Ends on: about 450 unsatisfactory routine inspections in 2027 (437 to 458) and no third return-inspection officer
Golden: 693.4, about 700, and the third return-inspection officer is added

## Stump sentence

Carrying the risk categories' rates, each establishment's own record or one criterion per inspector into the 2027
schedule files about 450 unsatisfactory routine inspections and no third officer, because in the county's record an
inspector marks an establishment unsatisfactory about four to six times as often on a first visit as on a third or
later one, and the 2027 redraw makes 23 per cent of the schedule's routine inspections first visits for their named
inspector, against 4.8 to 9.2 per cent a year in 2022 to 2026; read at the number of earlier visits each named inspector
will have made, the schedule gives about 700, past the plan's 540.

## Three rules

Task type: decision-making-computational-behavioral-modeling in psychology-behavioral-science, which serves forecasting: a model of a human judgment (an inspector's decision to mark a routine inspection unsatisfactory) fitted to the inspectors' own recorded decisions and used to forecast the decisions the 2027 schedule will produce.

Domain test: the deciding quantity is the chance that the inspector named for a 2027 district marks a scheduled routine inspection unsatisfactory, a human judgment the decision-making task type models from the judges' own recorded decisions (the criterion each judgment applies, as a function of the case's risk and the judge's state), checked on decisions held out of the fit; the call is that model summed over the 2027 schedule against 540.

Swap: "does the water utility need a third meter-reading crew for 2027, sized on the reads that will be estimated?" keeps the sentence's shape and loses its substance: a meter read does not depend on how often the reader has read that meter, no judge's criterion relaxes with acquaintance, and a redrawn route changes who walks it but not what the meter shows, so the deciding quantity, a person's judgment shaped by the person's history with the case, stops making sense.

Layer 1: two inspection exports either side of the March 2024 migration (the legacy system's local times and inspector initials, the new system's UTC stamps and employee numbers, the roster's names); routine, return, complaint and pre-opening visits and closed-premises calls in one file; changes of ownership reissuing a permit at the same address; seasonal establishments with one routine inspection; covering inspectors on the district inspector's leave days; the return team's paper day sheets keyed into the new system at a later stamp until 31 August 2026; several reports per complaint incident; closed-premises return calls of the paper era never keyed, evidenced only in the correspondence log. Nothing is placed to be caught, and the call's construction is mess-neutral (R2: UTC read as local 693.4, ownership merged by address 714.1, closures left out 683.6, closed-premises calls counted 695.7, each keeping the call and the bin).

Layer 2: forecast validity under a shift in the decision model's covariate: the state each judgment depends on (the pair's earlier visits) moves out of its historical range in the forecast window, so a model that validates on the recent years, where new pairs make 5 to 6 per cent of inspections, misses when the redraw makes 23 per cent of the schedule new pairs; the methodological choice that flips the call is to carry the pair's visit count as the judgment's state rather than the inspector or the establishment.

Decisive step: recognise that an inspector's criterion is not one per inspector but relaxes with that inspector's earlier visits to the establishment, so count for each scheduled 2027 inspection its named inspector's earlier inspected visits there across both exports (the legacy initials resolved through the roster) and through the schedule's own earlier 2027 inspections, and read it at the first, second or later visit rates the 2022 to 2026 record gives within each risk category: 693.4, about 700.

Not semantics: every field, code and definition read correctly (the 25-point threshold and the imminent-hazard closures, the UTC stamps converted, the initials resolved, closed-premises calls left out, the schedule's inspections and Table 1's inspectors taken) still leaves the easy route at 437 to 458, because the pair's visit count is not a field: it is a state of the judge and the case that the analyst has to recognise the decision depends on and rebuild from two exports.

Not rule application: no filed rule says the mark depends on earlier visits or tells the analyst how to read it, so executing the plan's staffing sentence (each inspection as the named inspector will make it) and its definition correctly still files 424 to 458 with any per-inspector or per-establishment model. The enumerated family (category rates on 2022 to 2026 or 2025 to 2026, a yearly trend, each establishment's own record, one criterion per inspector, a first-year criterion, pair classes fitted from 2019, first against any later visit, every 2027 inspection at its end-2026 count, and the standing members) spreads the total from 424 to 951 and splits the call; the standing family (48 crossed members: rates from 2021, 2022 or 2023 onward, classes 0, 1, 2+ or 0, 1, 2, 3+, every visit or routine visits only, any or a 36-month count, cell rates or a main-effects logistic; the classes with an inspector term, an establishment term or both; the four Layer 1 readings) spreads 675.7 to 730.2, unanimous on the call and on the nearest-100 bin; what rules out the rest is loud on a cut by the pair's visit (first visits run 3.9 to 5.9 times later visits in every risk category, second against later visits at a Mantel-Haenszel z of 8.5) and silent on every cut by inspector, establishment or year.

Analyst test: a strong analyst who reads every field and rule correctly stacks the two exports, resolves the inspectors, converts the clock, keeps the routine inspections made, fits the unsatisfactory share on risk category with each establishment's own record or one criterion per inspector, validates it on 2025 to 2026 within about 5 per cent, carries it to the 2027 schedule with Table 1's inspectors and files about 450 (437 to 458) and no third officer; read at each named inspector's earlier visits to each establishment, the schedule gives about 700 and the third officer is added.

Estimand: the plan (`food_safety_program_plan_2027.pdf`, section 3) files it: the routine inspections in the 2027 schedule that will be marked unsatisfactory, each scheduled routine inspection counted as the inspector named in Table 1 for its district will make it, against 540, the two officers' capacity; section 1 defines unsatisfactory (25 red points or more, or a closure for an imminent health hazard), and the schedule workbook issued with the plan lists the population (every permitted establishment, its 2027 district and its 2027 routine inspections).

No decoy: nothing is planted to be caught: no memo, briefing, draft or stakeholder figure states a 2027 forecast, a rate or a count; the capacity report states the team's 2026 returns against its capacity, a past quantity it answers correctly; the illness investigations and the permit invoices are distractors named in metadata.json that rank nothing.

No certified replay: the method is not recovered by reproducing certified or published figures: no published table carries an unsatisfactory rate by visit or by inspector, and the pair counts are rebuilt from raw visit rows in two systems.

Lesson: a judged outcome is a property of the judge and the case together, so a forecast for a window that resets the pairs is wrong by every model keyed on the judge or the case alone, however well it validates on years when the pairs held; no build on file reads a human judgment at the judge's history with the case.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 risk-category rates carried to the 2027 schedule | the plan's staffing rule invites a forecast of the schedule | `risk_category` in the permits file | the field's base-rate forecast | the 2025 to 2026 hold-out validates it | none | one group-by | none | readable |
| R1a each establishment's own record shrunk to its category | none | the permit on every visit | a repeat-offender reading | validates on 2025 to 2026 | none | one group-by | none | readable |
| R1b one criterion per inspector read at Table 1's inspectors | section 3 names the inspector who makes each inspection | the inspector on every visit | the field's rater-severity model | validates on 2025 to 2026 | the initials resolved through the roster | one ratio | none | readable |
| R1c a first-year criterion for appointees | none | the roster's hire dates | tenure, the reflex of task182 and task202 | none | none | one join | none | readable |
| R2 (decisive) each scheduled inspection read at its named inspector's earlier visits to the establishment | silent: no sentence names earlier visits, a first visit, familiarity, rotation or tenure (asserted on both PDFs) | silent: no column holds a pair count (R1), and the pair is rebuilt from two exports with different inspector keys | silent: the field's rater models key on the judge, not on the judge's history with the case | silent: the latest-years hold-out validates R0 and R1, and no file scores a pair reading | silent: no duplicate, clock or key issue points at it | silent: a running count over two exports keyed through the roster, crossed with Table 1 and the schedule | silent: the exports, roster, permits, schedule and plan each serve every rung and the asks | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "marked unsatisfactory" | 25 red points or more, or a closure for an imminent health hazard (UNSAT and IHH CLOSURE in the legacy export, Unsatisfactory and Closed - imminent health hazard in the new one) | closures left out | 683.6, same call and bin | plan section 1 names the closure; same call |
| SF2 | "the routine inspections in the 2027 schedule" | the schedule workbook's routine inspections (5,512 at 2,648 establishments) | establishments, or the record's 2026 count | the establishment count is not the plan's unit and the 2026 count is not the schedule | plan section 3 counts inspections and the workbook lists them (asserted) |
| SF3 | "as the inspector named in Table 1 for its district will make it" | every scheduled inspection made by its 2027 district's named inspector | 2027 covering days modelled, or the 2026 district inspector | outside the filed WHAT | plan section 3's sentence; every scheduled district has its named inspector (asserted) |
| SF4 | an inspector's earlier visits | inspected visits of every type at the permit (routine, return, complaint, pre-opening) | routine visits only | 690.0, same call and bin | same call |
| SF5 | a closed-premises call | not a visit: the inspector did not inspect | counted as an earlier visit | 695.7, same call and bin | same call |
| SF6 | the years the rates come from | 2022 to 2026, visits counted from January 2019 | 2021 or 2023 onward; 2019 onward | 699.0 and 708.3, same call and bin; 2019 onward 521.5 | 2019 onward reads a pair's first visit on the record as a first visit although the record starts in January 2019, most permits are dated before it and section 1 sets one to three routine inspections a year (2019's first-visit share 50 per cent against 4.8 to 10.4 in every later year) |
| SF7 | the visit classes | first, second, third or later | 0, 1, 2, 3 or more; first against any later | 709.6, same call and bin; first against later 626.2, the call in another bin | the record: second visits run above later visits in every risk category (Mantel-Haenszel z 8.5, asserted) |
| SF8 | how far back the count reaches | every earlier visit on the record | within 36 months | 694.8, same call and bin | same call |
| SF9 | 2027's own earlier inspections | a pair's second 2027 inspection is its second visit (the count advances through the schedule) | every 2027 inspection at its end-2026 count | 951.1, the call in another bin | the record's classes count the same year's earlier visits (asserted), so the end-2026 count reads the classes another way than they were fitted; section 3 counts each inspection as the inspector will make it |
| SF10 | the new export's clock | `inspected_at_utc` converted to Pacific time | read as local | 693.4, same call and bin | the column's name; same call |
| SF11 | an establishment across a change of ownership | the permit (a new owner's permit starts a new record) | merged by street address | 714.1, same call and bin | same call |
| SF12 | "exceed 540" | strictly greater | at or above | same call: 693.4 is not 540 | same call |
| SF13 | the nearest 100 | 693.4 to 700, 43.4 from the nearer edge; the standing family 675.7 to 730.2 in the same bin | none | same call | the prompt's rounding sentence (asserted) |
| SF14 | ask A's population and count | 2026 unsatisfactory routine inspections whose first completed return inspection fell in 2026; county working days from the routine inspection to the day of that return | the inspection system's date for the return; a closed-premises call ending the count | equals the truth for every district (asserted) | plan section 4 ("a return visit that finds the premises closed does not end the count") |
| SF15 | county working days | weekdays less the days in the county holidays file (Thanksgiving, the day after, Juneteenth among them) | federal holidays | the county's own calendar (asserted) | plan section 4 names county holidays |
| SF16 | a paper-era closed-premises return call | dated by its RV-NA letter's visit date | the letter's date | every RV-NA letter carries a visit date (asserted) | the fee schedule charges at the rate on the day of the visit |
| SF17 | complaint response time | the earliest report of the conditions since the permit's previous investigation, to the inspector's arrival | the report the investigation carries | equals the truth for every district (asserted) | plan section 4 ("from the program's first notice of the conditions a complaint reports") |
| SF18 | the asks' districts | the eleven 2026 districts (`district_2026` in the permits file) | the nine 2027 districts | every 2026 district has investigations and returns (asserted) | the measures are 2026's, and plan section 2 begins the nine districts on 1 January 2027 |
| SF19 | return visit fees | each further return visit after the first for the same routine inspection, made or found closed, at the rate on the day of the visit, for 2026 visits after 2026 unsatisfactory routine inspections | the inspection system's return visits only | equals the truth for every district (asserted) | the fee schedule's return-visit paragraph |
| SF20 | a district with no fees | every 2026 district owes fees | none | asserted | the record |
| SF21 | fees to the dollar | sums of 152 and 168 | none | every total divides by 8 (asserted) | the fee schedule's two rates |

## Ladder

| Rung | Route | 2027 forecast | Third officer |
|---|---|---|---|
| R0 | risk-category rates, 2022 to 2026 | 437.3 | no |
| R0b | risk-category rates, 2025 to 2026 | 424.1 | no |
| R0c | a linear trend in the yearly counts | 436.8 | no |
| R1a | each establishment's own record shrunk to its category | 458.4 | no |
| R1b | one criterion per inspector at Table 1's inspectors | 451.0 | no |
| R1c | a first-year criterion for appointees (none in 2027) | 437.3 | no |
| R2a | pair classes counted and fitted from 2019 (left truncation unhandled) | 521.5 | no |
| R2b | first visit against any later visit | 626.2 | yes, 600 at the nearest 100 |
| R2c | every 2027 inspection at its end-2026 count | 951.1 | yes, 1,000 at the nearest 100 |
| Golden | first, second and later visit rates by risk category, counted from 2019, fitted on 2022 to 2026, advancing through 2027 | 693.4 | yes, 700 |
| Standing | the 48 crossed members, the inspector and establishment terms (698.2, 695.0, 701.5, 699.9), the Layer 1 readings | 675.7 to 730.2 | yes, 700 |
| Truth | the simulation's own expected count | 637.5 | yes |

Separation: the highest easy rung (458.4) sits 1.18 under 540 and the lowest standing member (675.7) 1.25 over it,
both asserted against a 1.15 floor; the decisive step alone moves R0 from 437.3 to the golden's 693.4 (R3b). No cheap
route reaches the call: every route keyed on the inspector, the establishment or the year lands under 540, and the
two routes that reach it in another bin (R2b, R2c) both need the pair count first. The golden sits 8.8 per cent above
the truth's expected count (asserted within 12): the record counts from 2019, so pairs with only pre-2019 visits read
as new, and the first-visit cells carry their sampling error (about 300 to 700 inspections each).

## Closure table

| Axis | Reading | Move |
|---|---|---|
| 1 Population | the 2027 schedule's routine inspections, as the workbook lists them | filed: plan section 3 and the workbook (SF2) |
| 2 Unit of account | one routine inspection, marked unsatisfactory or not | filed: plan section 3 |
| 3 Attribution window | calendar 2027 | filed: the plan's year and the schedule |
| 4 As-of dating | the record to 31 December 2026, the plan issued 11 January 2027 | filed: the plan's header; C1, nothing after 2026 ships |
| 5 Version basis | one export per system, no revisions or re-pulls | C1 |
| 6 Denominator | inspections made; a closed-premises call is not an inspection | C1: SF5 same bin |
| 7 Weighting | each scheduled inspection counts once | filed: a count |
| 8 Window length | rates from 2022 to 2026, visits counted from 2019 | C3: rates from 2021 or 2023 onward keep the bin (SF6); 2019 onward refuted by the record's start |
| 9 Boundary inclusivity | "exceed 540" strictly | C1: same call (SF12) |
| 10 Rounding path | the unrounded sum, rounded once to the nearest 100 | filed: the prompt's last sentence (SF13) |
| 11 Tie-break | no tie at the threshold or at a bin edge | C1: 693.4 is 43.4 from the nearer edge |
| 12 Maturity and censoring | the record's start truncates every pair's history | C2: rates start three years after the record, and every standing window agrees (SF6) |
| 13 Order of operations | count the pair's visits, take the class rates, sum over the schedule | C1: the steps commute |
| 14 Row order | visits in local time order, across both exports | C1: UTC read as local keeps the figure (SF10) |
| 15 Duplicate resolution | no duplicate visits; a complaint's several reports belong to ask B | C1 for the call |
| 16 Identity normalisation | legacy initials to employee numbers through the roster; permits keep their numbers across the migration | C1: no two staff share initials (asserted) |
| 17 Netting against gross | a count, nothing netted | C1 |
| 18 Dimensional units | inspections | C1 |
| 19 Code and status semantics | UNSAT and IHH CLOSURE, Unsatisfactory and Closed - imminent health hazard are unsatisfactory; NO ACCESS and No access are not inspections | filed: plan section 1; C1 (SF1, SF5) |
| 20 Integerisation | the expected count is not an integer and is rounded once | filed: the prompt |
| 21 Clause scope | section 3 counts routine inspections only; other visits count only as earlier visits | filed: section 3; C3 (SF4) |
| 22 Forward window contents | 2027's own earlier scheduled inspections advance the count; 2027 complaint visits are not forecast | C2: the record's classes count same-year visits (SF9); no member forecasts 2027 complaints |

## Literal reader

On paper and on the cut pack: the prompt asks for the call and the forecast the rule compares; the plan's section 3
files the rule and its WHAT (the 2027 schedule's routine inspections that will be marked unsatisfactory, each as
Table 1's inspector will make it, against 540), section 1 the definition and section 2 with the workbook the
population. Executed word for word, the WHAT leaves open only how an inspector's mark is forecast, and the record
forces it: the per-inspector and per-establishment models validate on the latest years and land under 540, while the
pair's visit count separates first, second and later visits (second against later at z 8.5) and a hold-out on the
2023 appointee's first year refutes the per-inspector rates (47 against 137 recorded, visit classes 110). Every
literal reading of a convention on the call (SF1 to SF13) gives the golden's call and bin or is ruled out by a
quotable fact, and every ask reading (SF14 to SF21) equals the simulation's own measure. Pass.

## Oracles

- The truth's expected 2027 count from the simulation's own criteria, 637.5: the golden sits 8.8 per cent above it
  (asserted within 12 per cent), on the same call.
- The asks: every ask A, B and C figure equals the simulation's own measure for its district, 33 of 33 (SF14, SF17,
  SF19).
- No shipped oracle: no file ties only under the golden reading; the capacity report states 2026's returns against
  capacity, a past quantity; the latest-years hold-out validates both the easy route and the golden.

## Ask sheet

Pair ceiling: 28.5 (the cracker 45.0, the mirror 12.0, on the planning weights of 38, 7 and 55)
Mirror leakage: 0.0 per cent of the ask weight
Measured by: generator/ceiling.py, run on the cut pack

| Ask | Primary device | Golden | The cracker's figures | Cracker |
|---|---|---|---|---|
| A, median return timeliness in working days, eleven 2026 districts | D8: the return team's inspections keyed from paper day sheets until 31 August 2026 carry the keying stamp (the next Monday or Tuesday, sometimes a week later); the day sheets' own dates sit in the capacity report's day-sheet log, matched by officer and address as written | 8.5 to 13.0 | 11.0 to 15.5, every district off | miss |
| B, median complaint response in hours, eleven 2026 districts | D1: an incident's several reports (telephone, online form, email, referral) sit as separate complaint records, and the investigation carries the report it was dispatched on, the latest before dispatch, while the plan measures from first notice | 60.3 to 155.5 | 35.5 to 121.4, every district off | miss |
| C, return visit fees in dollars, eleven 2026 districts | D4: paper-era closed-premises return calls were never keyed and are evidenced only by the correspondence log's RV-NA letters; D8's day-sheet dates move visits across the 1 July rate change | 1,416 to 4,376 | 792 to 3,464, every district off | miss |

The full includer (day sheets, first notice and the letters, a stress row) keeps 33 of 33; the letters without the day
sheets keep 7 of 11 fee cells, so ask C carries two devices from two families on disjoint blocks. Every ask reads rows
the call never reads (return and complaint visits, complaint records, letters, the day-sheet log), and no device sits
on a routine inspection (asserted). Each ask B median sits at least 0.03 hours from a rounding edge (a clearance pass
makes ten nudges of 150 seconds to complaint visit times, asserted), and the ask A medians are whole or half days.

## Build record

- Seed 1302027; `generator/make.py` builds the pack, the goldens, metadata.json and figures.json, runs checks.py (245
  assertions), verify.py (an independent recomputation of the forecast and all 33 ask figures from the bundle alone,
  against the golden workbook and memo), a second build in a fresh folder compared byte for byte, and writes
  target.zip.
- Pack: 13 files in four formats; the legacy export 30,164 rows, the new export 18,077; distractors
  `foodborne_illness_investigations_2019-2026.xlsx` and `permit_fee_invoices_2026.csv`.

## Tried and rejected

v1 (large-holder designation, failed on the portal), carried over:

- The blueprint's stated-memo architecture (a methodology memo fixing the holdings rows, the amendment semantics, the unit-by-filing-date rule, CUSIP repair and the denominator source): rejected because a strong solver implements every stated clause, so the bridge becomes a computation; its traps are kept only as lower rungs.
- Capital-markets ownership kept literally (13F holders, issuers, shares outstanding) under an accepted domain label: rejected, markets trading is outside Economics and none of the nine owns a vendor's crowding flag without a relabel a reviewer would not accept.
- Confidentially omitted holdings recovered from another public disclosure as the decisive rung: rejected on the clean-data test, the public returns are a filtered file whose repair hands the natural pipeline the answer (sole_data_defect yes).
- Denominator timing (dwellings or shares outstanding taken at a later date than the holdings) as the decisive rung: rejected on the clean-data test (a stale file whose repair collapses the task) and as a single-fact flip.
- Holders whose returns are not yet due completed from the title register: rejected, the incomplete feed is a suspect file under the clean-data test, and the register-to-titles route is a schema-visible two-hop join a strong solver takes.
- Double reporting under a non-exclusive holding definition: rejected, the regime text that makes both returns correct concedes the overlap, and dwelling-level returns are deduplicated by reference by default.
- Agent-filed returns and nominee title holders as the decisive rung: rejected as a lens swap, registrant against owner of the same dwellings on the same date.
- Employer concentration with PEO look-through as the re-skin: rejected, it drops the ownership scenario and co-employment look-through is textbook.
- Passive holders re-derived at a forward date around an index change: rejected, out-of-scope domain and textbook.
- The agency's takeovers evidenced by preventive annotations in the deed extract: rejected, the evidence would sit in the forward roll's own source.
- Settled large-holder takeovers as the clock's evidence: rejected, a back-test mismatch sends the solver to the ledger.
- The programme order naming the first-offer programme: rejected, a sentence in the document that defines the quantity sends every solver looking.
- A bridge from the raw lodged rows to the conformed total, and a bridge with one bar per kind of movement: rejected, free weight and a taxonomy fork.
- Round 1 (plain) landed v1's six-section answer: the agency's first-offer takeovers in a budget ledger with a 120-day clock recovered from settled deeds died because the solver audited the ledger for transfers unprompted.
- Hardening loop 1's pre-registered repair (re-key the ledger by expedient in a second file): rejected before building, it only hides a step the solver completed.
- Portal 2026-10-10, the hardened v1 (holders inscribed after 30 June rung): failed, both top models filed the golden seven sections. Any rung that is a record a diligent solver can find and join is solved; the certified-bulletin reproduction blessed the path instead of hiding it.

Re-root (v2):

- Staying in the large-holder world with a property-against-dwelling grain stump (undivided buildings counted as one return row but holding several flats): rejected, the judge's lens-swap example (rank by logo count when the decision needs seats) is this move, and a dwelling-grain return collapses it.
- Staying in the large-holder world with any further hidden record (a licence register for new blocks, an inheritance date, a section split): rejected, the portal solvers join every record they can reach.
- The tensioned-zone rent burden from a deposit register (stock against flow, rents indexed on each anniversary): rejected, the update rules would have to be filed and a filed rule is a computation; the stock-and-flow reading is also close to a semantic fork on "rent".
- A survival-curve stump on the whole TA population (length-biased stock, pooled leaving rate as the decoy): rejected after simulation, in near steady state the pooled rate and the duration-conditional forecast agree within 4 per cent on the TA total because the stock's slow leavers and the new entrants' fast leavers offset; and "last year's stock survival" lands within 3 per cent.
- The same survival stump on a closed cohort: rejected, the gap opens (12 per cent against a rate) but a survival curve is the textbook answer to a closed-cohort question and a strong solver fits one; it is kept as a wrong rung (R3) because the departures are rationed, not hazards.
- Tenter House filled in order of each household's first move out of emergency accommodation: rejected after simulation, the block's positions in the lists were left to chance and swung from front-heavy to back-heavy between seeds, so the call was an accident of the history; the 2023 longest-in-nightly-paid lettings rule makes the positions a property of the world.
- v2 as first shipped: the move-on order left unfiled and recoverable only from the lets log; replaced by a filed allocations scheme extract under the client's two-layer standard, which caps a method hidden and recovered from records. A scheme clause letting main-duty households also bid through HomeChoice was drafted and cut, because it opens a second exit route the plan does not count.

Hardening loop 1 (after the v2 portal failure, 2026-10-11):

- Portal 2026-10-11, v2 as shipped: failed; the reported model built the filed duty-date queue on the case record's need against the revised plan, took the accepted October lets out once and filed the golden 46 (0 / 7 / 20 / 19) at GBP 21,615. Once the order was filed, the queue was a computation.
- Ageing alone (the members' birthdays inside the window moving households between lists) as the decisive device: rejected after measurement on seeds 130 to 166, it moves two to four Tenter House households in six months and leaves a solver who freezes need on 30 September within one unit, often on the same total; kept as the second-level rung R6.
- Exact-size lists for households needing five or more as the decisive device: rejected, it is one filed sentence and a plan row away and moves only the four-bed count; kept as R8.
- Tenter House flats let on the case record's need (the record then stale for 27 per cent of the block): rejected, it fills the block with families in flats too small for them, which reads as a data defect; flats go on the need checked on the day, as a TA move would.
- Reassessing the record for every household near the front of a list before each round, so that a replay on the record reproduces every let: rejected before building, the lets log would then bless the record until the forward rounds broke it, the validated-record shape the client bans; the record is reassessed only for the household offered.
- Hardening loop 1 as built (the move-on lists on Part 3 need worked out from the household members on each round day, against a case record that lags it; 52 units against the record's 66): rejected at the clone pre-flight, reject tier (Template, Track B) against task73 world ten, whose stump is the same move (carry the class the household's record holds, when a filed rule re-derives it from the circumstances on file); task86's v2 first cut carried the same move (the bedroom standard applied with ages on the offer date) and both platform responses solved it on 2026-09-12. Its realism read (birth histories, working-day dates, the 56-day relief period, TA sizing and voids, procedure dating) was not repaired, since the device is spent. With rate-against-queue (v2) and record-against-re-derived-class (loop 1) both gone, the Tenter House queue world has no honest decisive device left that a filed rule does not turn into a computation; v2 is spent and task130 is re-rooted as architecture v3 in the same objective.

v3 build (2026-10-11):

- The first acuity score (claims dollars with pharmacy at full weight): rejected after measurement, specialty-drug members dominated every list and persistence came out only 1.1 to 1.5 times the golden, because a specialty regimen persists; the score now weights pharmacy at 0.2 of medical and the world carries the one-off medical episodes a top-of-plan list really holds (major surgery, stroke, post-acute stays, readmissions, longer cancer courses).
- Model noise keyed by a member's position on the list: rejected, the draft and the final list scored the same member differently; noise is keyed by member and year.
- Tiers from a rank on the rounded score: rejected, it tied at place 140; ranks use the unrounded score and the lists show one decimal, as the cover sheets say.
- Scores on nominal dollars: rejected, the 2024 and 2026 scores drifted apart with prices and the bid and final tiers stopped meaning the same acuity; dollars are restated to a 2023 base.
- Model noise salted with the world seed: rejected, the seed sweep and the build drew different lists; the salt is fixed (41730).
- Seeds 100000 and 102002: passed every gate but their tier baselines fell out of order (a lower tier costing more than a higher one in total), which a board reads as a broken model; seed 101005 kept.
- A tier total column in the workbook: rejected, Schedule C.2 forbids intermediate rounding and tier 4's unrounded total rounds to 2,630 against 2,629 from its rounded parts; the medical and pharmacy figures stand alone and Note 1 says why.
- R3b, R5b and R6c land within 5 per cent of the golden total: accepted rather than forced apart, they are the arithmetic of 18 against 24 months of trend, weights only, and two offsetting errors; each still misses the whole-dollar tier cells it touches.
- R4b equal to the golden in tier 3: accepted as structural, no tier-3 bid member left the plan during the year; checks.py reports it.
- The renewal letter restating Schedule C's member-month and incurred-date rules: cut, each convention is stated once, in Schedule C.
- Procedure lines carrying diagnoses drawn at random: replaced by procedure-appropriate diagnosis maps for outpatient surgery and hospital services.
- context_artifact register, asked for at the card update to clear filed_model's collision with task133: BLOCK ban.artifact against task131; redrawn to operations_log, the plan's claims and eligibility feeds the baseline is built on.

Repair 1 (2026-10-11):

- Seed 101005 under the rebuilt claims engine: bid tier 1 fell to 8 members and the tier baselines fell out of order at every acuity base from 2,200 to 2,500; a sweep of seeds 101000 to 101053 at four bases kept 101050 at 2,500, which passes every gate at all four.
- A simulation that started in January 2024: the 2024 selection year had a shallower history than 2026, so the bid's tier 1 shrank against the final's; the simulation starts in January 2023 as burn-in.
- A plan-wide medical PMPM near $425 under the first fee schedule: low for a school district plan; facility charges, consults and the commercial multiple (1.14 of the reference schedule) bring it to $468.
- Home health priced as a case rate: allowed ran above billed; it is priced per visit at a share of charges.
- A wrong-member claim drawn from any family member: it put PSA tests on women and deliveries on men; the wrong member is drawn from the same sex and age band.
- Birth-date corrections drawn freely: five-year changes no conversion produces; one digit of the year, on two-child families.
- Pharmacy pickups on the day a fill fell due: a Monday spike; pickups spread over five days on a weekday profile.
- A hepatitis C first visit dated the first of the month: a Sunday office visit; moved to the next business day, no graded figure moved.
- The duplicate assertion counting a wrong-member claim that was later voided as a second payment: the assertion reads only live claims.
- The first rebuild's programme pharmacy ($1,689.88) rounded with the persistence rung's ($1,690.46): centring now holds the programme figures a dollar clear of persistence's, and checks.py asserts no rung lands on either programme figure.
- Centring that let one pharmacy fill move 7 per cent: a fill now moves at most 2.5 per cent and a facility claim 4 per cent.
- The memo's "a transplant, a premature baby, a cancer course or an accident" and the chart title "pharmacy moves much less": false on this seed (no enrolled member had a transplant in 2026; tier pharmacy baselines run 0.29 to 3.18 times 2026); rewritten to the enrolled members' own 2026 and to "pharmacy moves both ways", both asserted.
- Implementation plan tables that opened with the role and the milestone: the guard's name reader joined cells into "Ellery Final", "Ellery Welcome", "Kelley Enrolment" and "Santiago Direct" (a BLOCK on two Ellerys); the tables open with the name and the date.
- Jessica Petty from the draw as outreach supervisor: a first-name WARN against task104; Edward Miller from the same draw.
- LibreOffice's /DocChecksum left as exported: it hashes the run clock and broke byte identity between rebuilds; it is recomputed over the pinned file.

Repair 2 (2026-10-11, the second reader's forks and signposts):

- Seed 101050 with pharmacy at 0.2 of medical in the score: pharmacy persisted (0.99 of its selection-year level in real terms), so carrying the enrolled members' own 2026 pharmacy forward landed a dollar from the golden programme pharmacy; the score now counts pharmacy at 0.4 of medical and the world carries one-off pharmacy (hepatitis C cures, G-CSF and capecitabine with chemotherapy, fixed-length venetoclax and adjuvant oral oncology, CMV prophylaxis after a transplant, teriparatide after a hip fracture, biologic starts with a loading dose, stops and switches, weight-loss GLP-1s started and stopped).
- Recital C's "no agreement was executed and Northcourt provided no services": read as certifying the untreated control; the recitals are now procurement history, and the untreated status follows from the cancelled RFP, the second RFP and the implementation plan's dates.
- One member carrying 26 to 31 per cent of each bid tier's medical, and one or two specialty-drug members 63 to 89 per cent of its pharmacy: a credibility argument for pooling; the new seed and score hold the largest member to 25 and 22 per cent.
- r2's first seed choice, 102002 with pharmacy at 0.75 of medical: chosen on a world before the sim's last incidence fixes and never rebuilt; superseded by a 160-seed sweep of score weights, pharmacy weights and tier splits on the final simulation.
- Seed 102016 (the sweep's first pick: pharmacy at 0.4, persistence 2.44 times the golden): its world let a spouse dropped at open enrolment come back after the employee had remarried, two spouses on person code 02 at once, and the PBM join refused it. The re-add now waits for no other spouse on the plan; that changes the random stream of any world where it bites, so 102016's world was redrawn and dropped, and 102037, whose world the guard leaves unchanged, was taken.
- Centring blind to the full-year-only rung: tier 4's pharmacy baseline and R4c rounded to the same $2,114; baseline cells are now centred off R4c's whole dollar on a part-year member's claim, which leaves R4c in place.

Repair 3 (2026-10-11, the third reader's forks on the main call):

- Repair 2's eligibility churn under lists drawn on the simulation's own coverage: RCV8692544 left on 31 October 2026 and was rehired from 1 March 2027, so he scored onto the final list at rank 18, Tier 1, while the eligibility file, cut at 28 February, ends his coverage in October and Tier 1 read 35 or 34; the model now scores only members the eligibility file of the run carries on the list's date (the administrator's file of the first of the month, through the day before), which leaves the RFP and draft lists as they were and takes RCV9058604 (Tier 4, an RFP list member) onto the final list in his place.
- Schedule C.1(e) as repair 2 left it ("a member's Risk Tier is the tier assigned to the member on the Final Enrolment List"): it gave the members on both lists their final tier for the RFP cohort's year too, a reading that moves every tier cell and the programme total by 3.3 per cent; C.1(e) now defines a Risk Tier as the tier the model places a member in when it draws a list.

Repair 4 (2026-10-11, the tuner's round targets):

- The tuner's round-value targets (each tier baseline aimed at a two-decimal value such as 3,017.30 and landing within 0.00002 of it, each 2026 PMPM moved onto a quarter-dollar such as 4,335.25): a confirming bell, since a solver printing full precision saw a figure come out exact only under the intended method; each graded figure now lands at an offset drawn for it from a seeded generator, clear of the cent grid, and a draw is kept only once it is built and every rung's and fork's programme total sits off that grid too (taking the cheapest tier combination in every draw left R2 within 0.0005 of $4,427.31 in both draws tried, so a draw now takes one of the thirty cheapest).

Hardening loop 1 (after v3 round 1, 2026-10-11):

- v3 round 1: the analog cohort's tier PMPM, trended and count-weighted, landed in four minutes. The in-house solver read the selection on 2026 claims as regression to the mean, took the cancelled RFP 2025-07 cohort as the untreated comparison (Schedule C.1(e)'s Risk Tier "when it draws a list", Recital B's cancellation before an award, the bid cover's proposed programme year), measured its April 2025 to March 2026 allowed PMPM in its RFP tiers (41, 30, 23, 46), trended it 24 months, weighted by the final list's 34, 37, 38 and 31 and filed $4,060 ($1,438 medical, $2,622 pharmacy) with every ask figure; its netting tied to the renewal letter's Exhibit 1 to the dollar on claims paid through 31 January 2027, which confirmed it for free.
- Exposure weighting as the next rung (C.1(i) rewritten so the Programme Baseline is expected claims over expected Member Months, each tier weighted by its members times their expected months): rejected after measurement. The analog's Member Months per member enrolled at its start (1 April 2025) run 11.28, 11.48, 11.00 and 11.48 by tier and move the total 0.05 per cent ($4,058.14); per listed member (10.73, 11.10, 11.00, 11.48) they move it 0.59 per cent ($4,036.04). The effect is two dollars on the estimator a careful reader takes (every Enrolled Member is enrolled on 1 April 2027), the two estimators are a fork 0.54 per cent apart with no closure, and the count weighting it would replace is filed.
- Case-mix normalisation by age and sex (each analog tier indirectly standardised to the enrolled tier's ages in the Programme Year, the score being claims-only): rejected after measurement. Nothing in the pack forces it (C.1(h) takes a tier's experience from the members in that tier, and no clause or standard makes the unadjusted reading a violation), a consulting actuary's funding-rate letter carries no age and sex rating table, so the table is the solver's choice, and four defensible tables from the plan's own 2025 and 2026 experience move the total -3.56, -2.03, -1.20 and +0.18 per cent ($3,915.75, $3,977.78, $4,011.55, $4,067.64; raw and smoothed, by benefit and combined). The adjustment's size is the table, it is under 5 per cent in every reading, and the raw tables move the baseline away from the simulated truth ($4,348.19), not towards it.
- The analog's selection rule against the final list's (the top 140 of a different pool, cut into fixed score bands): rejected after measurement. The bid list's lowest score is 33.0 and the final list's 34.1, so tier 4 spans different bands; restricting the analog's tier 4 to the final list's floor (24 of 46 members) moves the total +1.39 per cent ($4,116.55), contradicts C.1(e) (a Risk Tier is the tier the model places a member in when it draws a list), and the gradient inside the band is noise (the analog's April 2025 to March 2026 allowed PMPM for tier-4 scores below 34.0, 34.0 to 34.4, 34.5 to 34.9 and 35.0 to 35.6: $2,056, $4,829, $2,143 and $2,840).
- Part of the analog treated by another programme: nothing in the world treats the bid cohort (no administrator or PBM programme reaches it in 2025-26), and adding one to make a rung bite would be a planted defect; not built.
- A bridge from the first two months after each selection year (the analog's January and February 2025 against the enrolled members' January and February 2027, as a ratio on the analog's year): rejected after measurement. It moves the total +8.98 per cent ($4,424.87) on tier ratios of 0.17 to 2.70, two months of a heavy-tailed cohort; nothing files it, and its medical half needs a completion factor for February 2027 that the renewal letter does not derive. The enrolled members' own January and February 2027 pharmacy, trended to the Programme Year's midpoint, runs 12.8 per cent above the golden programme pharmacy: a reading of C.1(h)'s "experience of members in that Risk Tier" the pack does not rule out, which any architecture that keeps this world has to close.
- Weakening the three pins that announce the analog as the hardening on its own: rejected, hardening by deletion. Each pin closes a fork (the comparator tier for the 20 members on both lists, the cohort's untreated status, the analog window), and the bid list in the folder still announces the analog to any solver who knows regression to the mean.
- Verdict: v3 is spent. With the analog construction forced and found, every deeper adjustment measured is optional with no shipped sentence the unadjusted reading violates (case mix, the bridge), contrary to a filed clause (the score floor) or worth two dollars (exposure); none moves the call by 5 per cent on a forced, fork-free path, and a plant is the only fix left. v3 is the number's third architecture, so the pipeline's cap retires task130 unless the author grants a fourth root.

Architecture 4 draw (2026-10-12):

- Draws weighed and not taken. A zone substation's peak after rooftop solar moves it into the evening: with
  half-hourly load and a solar profile in the pack, netting the two half-hour by half-hour is the solver's first move,
  so the default lands. A drought outlook whose evaporation scales with a shrinking lake's surface area: the planning
  scenario has to file evaporation as a depth to be deterministic, and a depth sends every solver to the area table.
  Bowel screening demand by prevalent and incident rounds: "first screen or repeat" is the first cut any screening
  analyst makes, and the colonoscopy yields of first-time and repeat attenders nearly cancel per invitation. Mortality
  after the end of a level term: the analog cohorts' post-level experience lands when it transfers, and a model is a
  fork when it does not. Fiscal drag under frozen thresholds: with taxpayer records in the pack the microsimulation is
  the first move. Increased limits factors after a minimum-limits change and leveraged trend in an excess layer:
  per-claim trending under the new limit or retention is the actuarial reflex. Override bias against a random
  low-side test: the decision reason code and the test's own description name the unbiased sample. Real-time data
  vintages and mixed flood populations: neither method is forced by the estimand, so both are forks. Group quarters
  in a cohort-change projection: the error moves only with the local cohort's size and stays a few per cent.
- Claims-made funding with one entity joining on 1 January: the decisive step collapses to one filter (the claims
  made in the same calendar year as their incident, costed on their own), which the coverage clause prompts and a
  careful solver writes in one line; the draw keeps the claims-made window but staggers the transitions on each
  entity's policy anniversary, so a part-year window catches a share of claims that falls faster than its length,
  and keeps the cost of each claim tied to how soon it is made.
- Card variants blocked at check: gap time with pattern E (test.same_puzzle and test.same_driver against task117,
  task37, task44, task97); gap population with pattern E (test.same_driver inside the window against task124's
  lineage); forcing event cutover_or_migration (it would have banned task180, drawn later today with that event).

Architecture 4 build (2026-10-12):

- Ask B as it stood at precut (each entity's covered FTE by specialty class, 22 cells): rejected at the build. The
  October movers moved only the hospitalist, emergency, family medicine and advanced practice cells, so the careful
  path that reads the home entity kept 14 of 22 cells; recast to one figure per entity, which the moves, the dual
  appointments and the earning-code lines all reach.
- Ask A worded "under its expiring policy": rejected before the build. An occurrence policy's last term covers only
  incidents since its last anniversary (Brennick's began on 1 October 2026, after the valuation), so the literal
  reading empties the ask; reworded "under its occurrence policies", the coverage line's programme.
- Early Resolution Program requests a median of six weeks after the incident: rejected after measurement. A part-year
  window then catches nearly the full-year share and the prorated full-year rung fell within 15 per cent of the golden
  for the six-month entity; requests come a median of about twelve weeks after.
- Escalation of 9 per cent of requests: rejected after measurement. The escalated suits carried most of the window's
  cost and the count at the average cost fell to 1.7 to 2.0 times the golden; 6.5 per cent keeps it above 2.
- Claims received, closed and noticed on any day of the week, and medical group incidents on weekends: rejected at the
  realism read of the first build (seed 5546). Risk management logs receipts on business days and the clinics see
  patients on weekdays; the seed search was re-run on the business-day world and 5546 was dropped.
- A claims transaction ledger and the Early Resolution Program's case log as separate files: not built. The ledger only
  splits paid amounts the register already carries, and the case log would mark the quick, cheap route as a population
  (a readable rung).
- Seed 843 ($480,000): dropped as a round headline total. Seeds whose rounded counts did not add to the rounded total
  count were passed over while one that adds was available.
- A check that no experience Claim exceeds the $2,000,000 limit: replaced by SF18, which asks only that no Claim able to
  be made inside the window reaches it. Seed 5546 carried a Claim valued above the limit at 2027 cost level, made more
  than a year after its incident, so a cap could not have moved its golden; on seed 3671 the largest Claim is
  $1,748,066.
- Ashgrove Medical Center as the flagship's name: renamed Alderwick Medical Center at the house-fix pass (H21), since an
  Ashgrove Medical Centre is a plausible real clinic name; the code AMC and every figure are unchanged.
- The trust's aggregate limit at $6,000,000: `leak.py` matched the medical group's Ask A reserve figure, $6,000, inside
  it; the aggregate is $4,000,000 (each Claim stays $2,000,000, so SF18 is unchanged).
- The forcing event `purchase_order_or_contract` (each entity's expiring policy): after the PAUSED commit's rebase,
  task127 v2 (drawn 2026-10-12, a lower number, so earlier in draw order) carried the same event and `guard.py check`
  blocked on `ban.forcing_event`; the card now names the trustees' November meeting (`vote_or_meeting`), which is what
  forces the call, and the check is back to WARN. No later-drawn build carries that event.

Round 2 and the author's decision (2026-10-14):

- Round 2 (PAUSED f44902f): the Early Resolution Program's class experience as the decisive step, $587,000; sent back by the judge, because funding policy 3.2's "the System's own claims experience" read literally gives the pooled $312,000 (a main-call fork) and two ask bases were left open; the author kept round 1 as shipped ($784,000) and every task130 file was restored to 9bf3cbc.
- The 10/10 audit's verdict on round 1: COMPLIANT_WEAK (domain, layers and the three rules hold, but the claim-by-claim lag truncation is close to a reflex once 3.1 to 3.4 are read and both asks were cracked by the judge unaided), from the audit file /tmp/claude-0/-home-user-real-world-data-extraction-conformation-etl-build-problems/98ff0d30-fbdb-590b-8f7a-decafc622b0e/scratchpad/audit/task130.md; its nine missing ## Three rules lines were added true to round 1.

Rule 3 rework (2026-10-15):

- Shipped design: decisive step read as rule application per the rule 3 audit, because funding policy 3.4 ("used as
  recorded ... no development or tail factor ... no distribution is fitted") eliminated every rival estimator and left
  the per-claim lag truncation as nearly the only admissible construction once 3.1 and agreement 2.1 and 2.4 were read,
  and 3.2's exposure sentence read as a cost-per-FTE-year recipe; measured on round 1's own world, a log-log severity
  curve landed 1.01 times its golden and the pooled lag share 0.99, so the cost carried no structure of its own and the
  window was the whole stump. 3.4 is cut back to valuation and trend, 3.2 defines the two exposures, 3.3 the
  experience period and its pooling within class.
- A costly early hump (the program's quick settlements dearer than its later ones) as the cost-by-lag structure:
  rejected on the prototype, the window's count at the class average fell to 1.2 to 1.7 times the golden and the
  golden's standard error rose to 9 to 11 per cent on the experience's size.
- Specialty timing alone (each class's lags its own, cost flat in the lag): rejected, a pooled construction landed
  within 2 to 4 per cent, so nothing but the class split decided.
- A clean step in cost at one lag: rejected, a gamma GLM linear in the lag landed 1.02 to 1.09 times the golden and a
  log-linear curve 1.08 to 1.15; a monotone curve fits a step.
- A cheap segment from patients who waive a claim at the prompt (very short lags, near nothing): rejected, a spline
  landed 0.89 and 90-day bands 1.09 to 1.11, both inside the bin at some seeds and outside at others.
- Program requests a median of six weeks to four months after the care: rejected, the prorated full-year share fell
  within 15 per cent of the golden; requests come a median of about eight months after, once treatment and bills are
  done.
- The experience at a smaller size (incidents from 2017, the establishment at 1.8 times round 1's): rejected, the
  golden's standard error was 6.5 to 7.5 per cent of it, too wide for one sigma to stay inside a $250,000 bin with
  room; the establishment is twice round 1's and the experience starts in 2016 (filed in 3.3): 6.0 per cent.
- Every pooled empirical build as a must-miss: rejected as infeasible, by linearity a construction that costs each
  Claim at its own lag lands within 6 to 8 per cent whether or not the classes are pooled, because each entity's class
  mix in 2027 is close to the experience's; the pooled builds of the frequency-severity reflex (a pooled average, a
  pooled curve) miss by a bin and more, and the filed pooling within class closes the rest (same call anyway).
- Escalation of 4.4 per cent of program requests: rejected after measurement, the escalation chain mishandled (each
  claim number its own Claim) moved the call a bin on some seeds (0.885 to 0.92 of the golden), a Layer 1 item carrying
  part of the stump; at 2.2 per cent it is neutral (0.94, asserted R2).
- Card strategy `composition_mix` for the new decisive step: blocked against task125 and it would have blocked task137;
  the strategy stays `maturity_censoring`, which still names the window's censoring.
- Forcing event `vote_or_meeting`: blocked against task128, whose later re-root carries it; `launch_or_rollout` (the
  trust's launch) blocks nothing on either side; Elizabeth Nelson and Jerome Warren, named in no shipped file, dropped
  for the same re-root's Elizabeth.
- The carriers' changes in 2018 at both Quillan entities and in 2020 at Brennick: rejected after measurement, Tolliver
  Falls and Brennick then held no open claim under a former carrier on most seeds, so the cracker would have kept their
  Ask A figures; moved to 2021 (Tolliver Falls) and 2022 (Brennick), Alderwick to 2019.
- Trust agreement 5.2 ("report every Claim ... to the carrier whose occurrence policy was in force on the date it
  occurred"): cut, a filed rule on Ask A's path that adjudicates its device; 2.2 keeps the occurrence policies' scope.
- The expected number of 2027 Claims (46.87) as a critical component: cut, the one-day day-count variants give 46.41
  and 47.22, so its whole number is not forced; the 2027 exposure total (1,105.75 FTE-years, a tie at one decimal) cut
  for the same reason; the goldens show months in the trust instead.
- Per-diem shifts on the regular salary earning code: an HCM pays shift work on its own code; PDM.
- Entity and class breakdowns of the call in the workbook and the ask list: cut, they rode on the call (the audit's
  22 coupled figures); the asks are now reconciliations the call does not reach.

Rule 3 rework, round 3b (2026-10-15):

- Round 3a: the dollar-weighted step factor lands the golden, per the rule 3 re-audit. The field's claims-made step
  factor on loss dollars, applied to the occurrence pure premium and convolved over each entity's days left, is the
  golden's own construction (the re-audit's monthly probe gave $1,263,621 on 3a's $1,263,838), so a strong solver
  landed 3a without seeing the lag-cost link; 3b keeps that construction as the default and adds the experience period
  as a second layer it misses by a bin.
- Claims seed 2077 (3a's) under the second layer: rejected, the golden $1,232,055 with every route right but Ask A
  answered yes at every entity, so "none" was no longer a graded answer.
- A larger world (the establishment scaled three to four times) to tighten the smaller post-start sample: rejected on
  the prototype, the golden's standard error in dollars grows with the square root of the scale, so a fixed $250,000
  bin holds one sigma less well; the disclosure settlements carry four fifths of the mean and nine tenths of the
  variance, so more and cheaper settlements (twice 3a's frequency at 0.41 of its cost) are what tighten it.
- Later starts (2020 and 2021 at the larger entities): rejected, the pooled-date constructions (incident years from
  2020 or 2021, the latest start for every entity) scattered 0.84 to 1.10 of the golden on the smaller post-start
  sample and incident years from 2019 took in a year of the old process; the starts sit between January and July
  2019 and every start handling lands within 3 per cent.
- The program's requests starting with the disclosure arm (no requests before each entity's start): rejected on the
  prototype, claim counts by incident year jump three to six fold at each start, a break any count by year shows, and
  the prorated full-year share on the whole experience still landed within 15 per cent of the golden; only the
  disclosure arm is staggered, the requests have run since 2015, and the change shows only in the lag mix.
- Requests later in the year (medians of nine to ten months, none before four) to push the prorated full-year share
  on the whole experience off the golden: rejected after four configurations, the share stayed within 5 per cent of the
  golden (its over-count of the part-year entities' requests is what offsets the pooled years' missing settlements)
  while the golden fell to $1.05 to $1.17 million and its error rose to 6 per cent.
- Every whole-experience route a full bin off: rejected as infeasible. With the pooled years at 0.75 of the golden, any
  round 1 route whose own error on that experience lies between 1.07 and 1.6 lands within a bin, and the round 1 routes
  fill that range (the quadratic on log cost 1.12, the prorated full-year share 1.42); they are recorded in the ladder
  as two errors that offset and never asserted to miss, and seed 3006 holds only the prorated share in the golden's
  bin.
- A programme or channel code on the register marking the disclosure settlements: rejected, the break would become a
  field reading (the call flipping on one code) and a column a schema test finds; the change lives only in the claim
  dates.
- Funding policy 3.3 "pooled within each specialty class" over 2016 to 2024: cut, it reads as an instruction to pool
  every year equally; 3.3 now says what the trust holds (2016 to 2024, rated by the classes of Schedule B), 3.1 files
  the estimand as the Claims as they will arise and be made in the Plan Year, and nothing instructs the reverse.
- Funding policy 3.2 "over the experience period": cut, it tied the exposure to the whole period held; 3.2 now says only
  how exposure is measured in the experience and in the Plan Year.
- The start read at 30 days alone: kept as the golden's reading with 14 and 39 days as constructions (they move one
  entity by a month and the call by under 0.2 per cent); 40 days or more would take in the earliest program requests,
  which are not the settlements.

Rule 3 rework, round 3c (2026-10-16):

- 3b: any recent-years trim lands, and 3.3 reads as whole-experience pooling (Gate C), per the rule 3 read.
- 3c, the disclosure starts spread entity by entity (Alderwick April 2017, Tolliver Falls April 2019, Brennick April
  2021, the medical group January 2023, the starts the rework proposed): rejected on the prototype. A trim from a year
  after the last start keeps no month before any start, so it is the golden's estimand on fewer years: on seed 4106
  (golden $1,248,083) 2023+ gives $1,222,915 and 2024+ $1,141,681, both in the golden's bin, 2022+ $1,102,768 and
  2021+ $1,052,748 round elsewhere inside a bin, and the prorated in-year share on the whole experience lands at
  $1,242,674; over twelve seeds 2023+ and 2024+ sit $11,000 and $46,000 from the golden on average.
- 3c with the largest entity last, its start in the fourth quarter of 2024 (the medical group from October 2024 after
  Alderwick 2017, Tolliver Falls 2019 and Brennick 2021, or Alderwick last after the medical group 2017), the only
  kind of layout an exhaustive search of quarterly starts found where every calendar trim through 2024+ misses by a
  full bin
  ($373,019 to $498,254 on seed 4107): rejected on the own-start constructions. The last entity has three months
  since its start in the 2016 to 2024 experience, so a start read a quarter or six months on leaves Primary Care, rated
  only at the medical group, with no exposure (mean $87,198 and $89,693 low over twelve seeds, up to $155,301), each
  entity on its own experience scatters (s.d. $119,668, worst $267,913; with Alderwick last $181,828 and $395,255),
  the classes pooled carry the hospitals' post-start mix into a window half the medical group's (mean $181,065 high;
  with Alderwick last $236,643 low), the golden's own s.d. rises to $56,542 to $86,472, and the prorated in-year share
  on the whole experience still lands ($1,138,831 against $1,237,613 on seed 4107).
- More and cheaper settlements (twice 3b's frequency at half the cost, defence included) to steady the late-start
  layout: measured, they cut the golden's s.d. from $86,058 to $129,721 to the figures above, and leave the
  start-handling and pooling biases, which are structural.
- 3c's Gate C closure, a WHAT in 3.1 ("as each entity's claims arise and are made under its practice at its
  Transition Date") with 3.3 left as what the trust holds: rejected on its signpost cost. A solver who reads it looks
  for each entity's practice change, and the only change in the pack is the onset, in that entity's lag table, of Claims
  made within weeks of the care (none before, some in every year after); landing then needs only each entity's months
  from its onset, so the closure turns the decisive step into the check it prompts.

Round 3a restored, the asks hardened (2026-10-16):

- The pair at or under 40 with both top responses on the call: infeasible under the planning weights. A response on
  the call banks the contribution and the two experience components (38) and instruction following (7), 45 before any
  ask, and the two "yes" answers and the chart's structure are any careful response's, so two responses on the call
  score 53.1 however hard the asks (49.1 if the rubric folds each "whether" into its count).
- A precautionary notice the carrier still carries as an Incident for a claim not yet reported, as Ask A's second
  device: rejected, the world holds two such matters (the September claims of noticed incidents, one at Alderwick and
  one at the medical group), too few to reach Tolliver Falls and Brennick, and an incident record standing for a claim
  opens a second reading of "missing".
- References the carrier keyed in another scheme (incident numbers, transposed digits) as Ask A's second device:
  rejected, a two-way match of the run against the register shows them at once; texture, not a device.
- A payout with hours, or leavers' payouts counted as paid FTE, for Ask B: rejected, a payout's hours read two ways
  against "hours paid on the line"; the TRM line carries no hours and the dictionary dates it to the month paid.
- New positions for the graduates, or a Brennick physician hire: rejected, position months are drawn in position order,
  so an added position moves every later position's claims and the 2027 staffing plan, and with them the call; the
  graduates take vacancies the roster already fills, under their own ids, and Brennick, with no physician vacancy from
  July to September, keeps only the moonlighting device.
- A second carrier for allied health, or a gap inside an expiring carrier's run of terms, for Ask A: rejected, the
  world's carrier histories stay as built, and two carriers left at once read two ways against "the carrier it is
  leaving".

Architecture 5 draw (2026-10-31), each screened on paper and set aside before any code:

- Theatre list overrun cancellations under 2027 lists booked to full session time (each case's position and the
  booked time before it): the client domain is task482's, a live batch 1 re-root, and task301's note already screened
  theatre cancellations sized by a start standard.
- High-tide flood days for 2027 from the published tide table and the surge record (coastal climate extremes): the
  2027 nodal factor sits with 2022 to 2026's, so replaying the recent observed high waters at 2027's mean sea level
  lands, and the tide-plus-surge decomposition is the field's reflex once a tide table ships.
- A fund's redemptions read from each holding's gain or loss against its own purchase price (behavioural finance):
  the effect needs a V-shaped or break-even selling schedule whose specification spreads wider than the call's
  margin, and the disposition effect is the field's named reflex.
- Burial ground capacity with reopened graves forecast from the stock of part-used double graves (municipal
  service demand): the stock model and a trend in the reopening share differ only in curvature, too thin for a call.
- Ozone exceedance days under a low-emission zone read from the weekday-weekend contrast: NOx titration is the
  field's named reflex, and no physical-environmental forecasting task type carries air quality.
- Parole grants read by each hearing's position since the board's last break: the field's best-known result, primed
  by the session schedule change that would force it.
- A low-emission zone's charge revenue by each plate's entry frequency, and a reopened line's ridership by each
  card's choice during the closure: composition on a derived property, and the behavioural response follows from
  the forcing event on its face.
- This world's first variant, the 2027 districts passing to first-year inspectors read at earlier appointees'
  first-year criterion (and the same variant with driving examiners and retests): tenure is a hire date one join
  away on the roster, the reflex death recorded in task182 (service-length standardisation reaching the golden slate
  20 of 20), task202 (C4) and task171 (the screeners' new-hire cohort); replaced by the pair's visit history, which no
  roster or column holds.

Architecture 5 build (2026-10-31):

- Permits renumbered at the March 2024 migration with a crosswalk in the permit register: rejected at the build, the
  renumbering split every pair's history at the migration for a solver who missed the crosswalk, a Layer 1 item that
  moved the call; permits keep their numbers across the migration and the crosswalk column is gone.
- The draw's calibration (threshold 800, about two fifths of 2027's inspections first visits, a first visit marked
  about two and a half times as often as a fourth): rejected on the prototype; the redraw on drive time made far fewer
  first visits than two fifths and the call's margins were thin; the retirees moved to districts 2 and 4, the base
  rates were lowered and the first- and second-visit terms raised, the threshold became the team's own capacity (two
  officers at 270), and the asks took more device mass (the paper era to the end of August, later keying, more
  closed-premises calls, more reports per incident).
- A routine inspection made while a return sequence was still open at the permit: removed, a district holds the next
  routine inspection until the returns close, as a program does.
- Asks A and C over every return made in 2026: restricted to 2026 routine inspections, since a December 2025
  inspection's January 2026 return reads two ways against the asking sentence.
- Day-sheet matching on a narrow window: widened to 1 to 20 days before the stamp, the earliest unused line first,
  through 15 September 2026, since the late keying of the paper era's last weeks fell outside it.
- Overlapping complaint incidents at one permit: removed, starts are drawn in order and an incident never opens
  inside another.
- The forecast to the nearest 50: rejected at the build. The crossed standing family (rates from 2021, 2022 or 2023
  onward, classes 0, 1, 2+ or 0, 1, 2, 3+, every visit or routine visits only, any or a 36-month count, cell rates or
  a main-effects logistic) spans 675.7 to 730.2, across the 725 edge, so the forecast is graded to the nearest 100,
  the precision the record carries; every member sits in the 700 bin at least 19.8 from an edge (asserted at an
  eighth of a bin, the single-axis members at a quarter).
- The memo's "not how most of 2027's inspections will be made": false, first and second visits are 42 per cent of the
  schedule; rewritten to the record's first-visit share against the schedule's, both asserted. Its "an inspector
  making a first visit": true only on the record from 2019; rewritten to no earlier inspection of the establishment
  on the record since January 2019.
- SF5 asserted only as the golden's own visit types, and R2 carried only by fork rows: SF5 now prices the reading it
  names (closed-premises calls counted as visits, 695.7, same bin), and the Layer 1 readings carry their own R2
  labels.
- The card's decisive pattern G14 with strategy forecast_method_backtest, and the organisation local_government:
  blocked at stage 3 by `guard.py heart` against task156 v2, registered at 18:27Z, 38 minutes before this draw and not
  yet in this tree at the draw's check (ban.pattern, ban.strategy, test.same_puzzle, test.same_driver,
  ban.org_family). The decisive step is a mix shift with the cell rates holding, the labels task175 carries for a
  chance held within a class and carried to a new mix (G6, composition_mix), and the organisation moves to a state
  department of health's county office in a fictional state (government_agency), as states that run their county
  health units do; the mechanism, the data and every graded figure stay as built.

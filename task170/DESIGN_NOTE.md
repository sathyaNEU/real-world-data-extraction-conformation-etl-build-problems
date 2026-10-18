# task170 design note

Architecture 1, wave 7 (new), Forecasting lane (sathya8571), numbered from seed FC41. The seed (a national Central
Medical Stores filing its order of the adult first-line pack, tenofovir, lamivudine and dolutegravir in one tablet
(TLD), for the January to June cycle C7 at the quantification review, while the children of a paediatric scale-up five
years ago grow into it) was read at its header and Situation only. Its world, decision and quantity are kept. Its
mechanism (a certified cohort model and a register read off one field) is not used: no document vouches for any
model, the paediatric register ships as honest data, and the SOP's stock-out wording is replaced by a filed maximum
stock level so no distribution-against-mean step can decide the call. The pitfall is re-found from how a child moves
onto TLD: at the first clinic weighing that reads 30 kg or more, while a single clinic weighing scatters more than a
kilogram either side of the child's own growth line and the line rises about a fifth of a kilogram a month.

The country is fictional and never named in the pack: a southern African ministry of health whose Central Medical
Stores (CMS) buys antiretrovirals for a national programme of about 310,000 adults on TLD and 12,000 children on treatment,
in US dollars, every product on a six-month cycle (C7 is January to June 2027). The TLD order has two lines (SOP QP-04
4.3): line 1 for the patients of the programme's projection, net of the stock and the lots on order, and line 2,
funded by the paediatric grant, for the children under 15 at the count in the paediatric and adolescent ART register.
The register holds every child's clinic visits, weighings and regimens since January 2023: children diagnosed in
infancy (born 2005 to 2026, fewer each year as PMTCT improved) and the 2021-22 catch-up campaign's children (born 2011
to 2018, diagnosed at three to ten, the more stunted and the slower growing the older they were found). The 2026
edition of the national guidelines, effective 1 March 2026, lowered the weight from which a child takes TLD from 35 kg
to 30 kg and gave children who are well two or three months of medicines at a visit; by the 31 August count most
stable children were on two or three months.

The call is line 2 in whole pallets (84 cartons of 96 bottles, 8,064 bottles): **11 pallets (88,704 bottles)**.

## Stage 4 repair (round 1)

The judge's finding (the 5,000-bottle step of the whole order was not forced: the textbook per-visit prediction
variance, shrinkage and attrition choices crossed its edges) and the rule-3 audit's materiality and realism findings
were answered inside the architecture, the mechanism and the cycle kept:
- The call moved to line 2, the children's part of the order as its own line, where the transition is material: the
  default path lands 7,859 bottles (8.9 per cent of the line, one pallet) short. Line 2 is rounded to the unit the
  order is placed in, the whole pallet of 8,064 bottles, wide enough to hold every defensible construction of the
  decisive step, the prediction-variance and shrinkage routes included, a quarter pallet plus one sigma from its
  edges (FAM asserted). Line 1 (the adults, net of stock and lots) stays in the order as a component.
- Annex 7.1 files that a child started on TLD stays on it whatever the weight recorded (SF15).
- The register was made real: birth years 2011 to 2018 for the campaign, none above 14 per cent of the children under
  15; two- and three-month dispensing from the March 2026 rollout (70 per cent of the children aged five and over at
  the count, 37 per cent on three months); each site's scale its own offset and scatter (site residual SDs 0.89 to
  1.74 kg against a sampling spread of 0.06); a season of 0.08 kg either side, heaviest in September; puberty's gain
  (velocity 2.6 kg a year at 9 to 13, 5.4 kg at 15 to 17); about one first reading in ten over the band held back to
  the next visit (276 first-line readings of 30 kg or more since March); the estimates' children on treatment equal to
  the register's at mid-2026.
- The dictionary files ARV0412D as TLD 30s from partner-donated stock, and the accounts' delivery region as the
  region when the account was opened (the registry carries the current region), which settles account 408891 as
  Layer 1.
- The context artifact is the paediatric register's encounter extract, an operations log (`operations_log`):
  `monitoring_export` collided with task246's redraw, and the stock status report no longer carries the call.
- Built to the two skills commits of the round (dffc213, 7896909). `score_reader.py` on the round-1 reader's
  answers: it committed no line or order figure (it declined the children's part as having no filed method) and
  none of the 24 ask figures; the four figures it did commit, the projection's consumption and maximum stock, the
  usable stock and the confirmed lots, are the order's filed parts (now line 1's), which the script scores in its
  ask class (4 of 4, exit 1) and which every reader is meant to land. The call is keyed `call` in `figures.json` so
  the gate reads it. Screened before the cut for the reader's three causes: Ask A's refusal device tied with netting
  the return lines (the judge saw it), so returns of short-dated stock collected from facilities now ride the same
  return document series and netting every return moves all 12 delivery figures (asserted); the dictionary's
  ARV0412D line, filed as the judge asked, makes the donation a filed reading, so Ask B rests on the reissued codes.
  H25: every shipped PDF opens under pdfminer.six, pdfplumber, pypdf (strict and lenient) and pdftotext with its
  decisive sentences in each (REAL asserted).

## Draw

1. Card: `.claude/skills/fingerprint/cards/task170.json`, architecture v1, registered 2026-10-18T09:10:20Z; `guard.py
   check` WARN, answered below. Nearest driver 0.08 (task119 v1).
2. Pairing: Healthcare Delivery & Health Economics (client domain) / `utilization-access-demand-forecasting` /
   Forecasting & Predictive Modeling. The task type serves Forecasting in the taxonomy. The deciding analysis is a
   pharmaceutical quantification's patient-transition forecast: the patient-months on the adult pack of children who
   will be weighed into the 30 kg dosing band at their scheduled visits before the cycle closes. Free against the last
   three registrations before the draw (task168 supply-chain-logistics x forecasting, task167 nonprofit-grant-making x
   forecasting, task246 general-statistics x data-quality-monitoring). task142 sits in the same task type (a
   purchasing alliance's Hospital in the Home overflow block, an upper percentile built from stays) and is
   differentiated on the card.
3. Niche: national ARV quantification of the children's line of the adult first-line TLD order across the paediatric
   weight-band transition, when the guidelines have just lowered the band to 30 kg and thinned the children's visits.
4. Call and shape: line 2 of the C7 TLD order, the children's line, in whole pallets of 8,064 bottles
   (`quantity_figure`, count, question form how-many), with line 1, its parts and the children counted as critical
   components. Shape `other`: the call with its critical components, the asks' tables on rows the call never reads, and
   a chart; criteria counted in `## Ask sheet`.
5. Mechanism keys: gap time (the evidence is past weighings and past switches; the order bets on when each child's
   switch falls against a window not yet open), then population; decisive generator G7 (a switch can only happen at a
   scheduled clinic weighing, and the forecast is each scheduled weighing's chance of reading 30 kg or more), then G13
   (the cycle window holds the part of the children's switches that their first qualifying weighings, not their growth
   lines, put there) and G6 (the register's switches came under the 35 kg band and at monthly visits, so rates measured
   on them do not carry to the 30 kg band at two- and three-month visits); Gate G `forecasting`; strategy `other` (the
   first passage of noisy scheduled measurements over a dosing band; `forecast_method_backtest` is spent by task167
   and `composition_mix` is task165's). Time with G13 decisive was blocked by task162 inside the batch; G7 with time is
   differentiated on the card against task161, task259, task87, task105 and task229.
6. Layer 2: `estimation_fit` (the data's real structure: repeated measurements scattering around each unit's own path,
   and a decision taken on a single reading at scheduled visits), pattern
   `own:first-scheduled-weighing-over-the-dosing-band-from-each-childs-growth-line-and-the-scale-scatter`. The method
   is tried out of sample on the register's closed windows under the band then in force.
7. Furniture: forum `committee_or_panel` (the national quantification review committee); forcing event
   `purchase_order_or_contract` (the C7 order goes to the supplier from the review; bans reach only this build's
   predecessors); organisation family `government_agency` (a ministry's medical stores); role family
   `procurement_lead` (the CMS quantification lead); context artifact `operations_log` (the paediatric register's
   encounter extract the forecast is built from: one row per clinic encounter with its sync time; redrawn at stage 4
   from `monitoring_export`, which collided with task246's redraw); calibration `none`.
8. Spine: the paediatric register's visit extract (child x clinic visit, January 2023 to August 2026, two layouts across
   the EPR migration), constructed in the layout of a national electronic patient register's paediatric module.
9. Deliverables: `c7_tld_order.xlsx` (both lines and their parts, the children by month, the out-of-sample record and
   the ask table) and `c4_c5_tld_flows.png` (each region's deliveries and dispensing in C4 and C5, every bar labelled;
   never on the order).
10. People, drawn with `guard.py names --locale zu_ZA --seed 170`: Nomalanga Magubane (the CMS quantification lead, the
    SOP and the stock status report), Thabisile Mahlinza (the paediatric ART programme officer, the register extract)
    and Sibongile Sikhosana (the ART programme's monitoring officer, the adult projection), the draw's seventh, fifth
    and tenth names.

**Data-native sentence.** The paediatric register records every child's clinic weighings to 0.1 kg at each scheduled
visit, and a child moves onto TLD at the first weighing that reads the band (35 kg until March 2026, 30 kg since); the
weighings scatter about 1.3 kg around each child's own straight growth line while the line rises about a fifth of a
kilogram a month, so most moves come at a single reading over the band months before the child's line reaches it, and
in August 2026 7,151 children under 15 sit below the band, more and more of them seen every two or three months.
The same structure is why architecture 1 is spent on strength: the first-passage lead is a fixed multiple of the
scatter over the growth rate, and so are the spreads of the estimator family (prediction variance, shrinkage,
windows, scatter estimates), so the lever runs about 2.5 times the family's spread whatever the rounding; any
honest bin wide enough to hold the family (about 7,600 bottles here, against a lever of 7,859) leaves the default
one bin out at most and lets every knob set near the right value land.

**Guard and similarity.** `guard.py check` WARN at registration, re-pulled before the check and before register (the
ban window held task168, task167 and task246). WARNs answered: `overuse.org_family` (government_agency): a ministry's
medical stores is a government agency and no other family is honest; `overuse.objective` (forecasting in 6 of 12):
this lane is Forecasting; `repeat.question_form` (how-many, task246): the call is a count of pallets and a count asks
how many. NOTES: `test.same_puzzle_older` and `test.same_driver_older` (time, G7) against task161, task259 v1, task87
v9, task105 v1 and task229 v3, each differentiated on the card. `guard.py heart` after the stage 4 redraw: see
`## Leak review`.

**Abstraction test.** Stripped of nouns: units move to another line at the first of their scheduled measurements that
reads at or above a fixed level, and a single measurement scatters around each unit's own path by more than the path
rises between measurements, so most moves come months before the paths reach the level; only the chance that each
scheduled measurement reads over the level, taken from each unit's own path, the record's scatter and each unit's
schedule, forecasts them. Nearest by mechanism, read for latent structure:
- task253 v3 counts units whose latent level sits below a line, seen through averages of noisy readings; here the
  decision is taken on one reading, not on the latent level, and the quantity is when the first qualifying reading
  falls, not how many units sit below the line.
- task258 counts units an intervention moves across a threshold; here nothing intervenes, and the crossing is a first
  passage of scheduled readings along each unit's own growth.
- task132 ages a fitted item along a wear curve with replacement; here no hazard by age is carried, and the
  replacement structure is absent.
- task157 and task160 time a wave from a calendar or a lag; here the timing in the window comes from each child's line,
  the scale's scatter and its visit schedule, not from any earlier wave.
None shares the latent structure, the default path and the correction.

**Sources, one line each.**
- Seed FC41 header and Situation (`status.py task170`): the world, the decision (the C7 order at the quantification
  review) and the quantity (bottle-months of adult TLD); nothing else of the seed is read or kept.
- `guard.py mechanisms --objective forecasting`: no spent driver forecasts a threshold crossing read through scattered
  repeated measurements.
- WHO consolidated HIV guidelines' weight-band dosing (dolutegravir-based first line, the adult TLD tablet from 30 kg
  since the 2021 update, 35 kg before) and paediatric multi-month dispensing for children who are well: the decision
  rule is a dosing band applied at the visit's weighing; the fictional programme's guideline states its own table.
- `stumping/references/strategies.md` F1 (a clock process estimated from every unit that went through it) and F5 (a
  pooled rate that does not fit the pool): the clock is each child's growth seen through its weighings, and the
  register's rates come from switches at another band and another visit frequency.
- `two-layer-task-design.md`: the client's example of validating a forecast on data it was not built on; the growth
  projection fails on the register's closed windows.

## Default path

Built figures from `generator/ladder.py` on the cut pack, asserted in `generator/checks.py` (R3a, R3b) and recomputed
by `generator/verify.py`. Line 2 is bottles over the window with six months of June 2027, in whole pallets.

1. Read the SOP: line 2 carries the children under 15 at the 31 August count with no outcome entered, forecast from
   the register to 30 June 2027 whatever their age (4.2): their forecast consumption from 1 September 2026, one bottle
   for each child in care on TLD at a month's end (4.1), plus six months of June 2027's (4.3), to the nearest pallet of
   8,064 bottles (4.4); the stock and the lots are netted on line 1 alone (4.3).
2. Read Annex 7, 2026 edition: a child on a first-line regimen moves onto TLD at a clinical visit whose recorded weight
   is 30 kg or more (35 kg before 1 March 2026), and stays on it.
3. Join the register's two layouts through the crosswalk, take the 4,527 children under 15 on TLD and the 7,151 on a
   paediatric first-line regimen at the count, carry them at the register's exit rates, and for each first-line child
   fit a straight line through its weighings since January 2023 and move it onto TLD at the first scheduled visit, at
   its own months-dispensed interval, on or after the date the line reaches 30 kg.
4. Count one bottle per child on TLD at each month's end, add six months of June 2027 and round to the nearest pallet.

Ends on: 10 pallets (80,640 bottles; the forecast at 80,128 bottles against the golden's 87,987).

Golden: 11 pallets (88,704 bottles).

## Stump sentence

Fitting each child's growth line from the register and moving the child onto TLD when the line reaches 30 kg files
line 2 at 10 pallets, one pallet and 7,859 bottles short of 11; the step that lands it there is reading the switch off
the growth line when the switch is taken on a single clinic weighing, and the weighings scatter about 1.3 kg around
each child's line while the line rises about a fifth of a kilogram a month, so most children are first weighed at 30 kg
months before their line gets there; the analyst who carries the register's own switch rates by recorded weight band
(9 pallets) or its recent switch count (12 pallets) also misses, because those switches came under the 35 kg band and
at the monthly visits the 2026 guidelines replaced.

## Three rules

Task type: utilization-access-demand-forecasting (Healthcare Delivery & Health Economics), which serves Forecasting & Predictive Modeling in the taxonomy; the forecast is a national programme's demand for a medicine over a window not yet open.
Domain test: the deciding quantity is the paediatric regimen-transition demand inside a national ARV quantification, the patient-months on the adult TLD pack of children under 15 who will move into the 30 kg dosing band at their scheduled visits, forecast the way a quantification analyst builds patient transitions: from each child's own weighings, the scatter of a clinic weighing, the visit schedule each child is on and the register's retention.
Swap: "how many megawatt-hours should the utility contract for January to June" keeps a forecast and a window but loses the dosing band applied at a clinic weighing, the dispensing interval that decides when a child can be moved, the guideline that lowered the band and the bottle a patient takes each month, so nothing places a switch months before the growth it reads off.
Layer 1: the register's migration from the legacy system to the national EPR in 2024 (legacy rows with day/month/year dates and free-text regimen lines, EPR rows with ISO dates and national regimen codes, the June 2024 migration month in both); facility ART numbers in the legacy rows against the national patient identifier, linked by the crosswalk, a new ART number at each transfer; paper sites recording to the half kilogram until May 2024; estimated dates of birth entered as 1 July; drug collections by a caregiver with no weighing; visit rows re-sent by clinic tablets after a failed sync; exits entered weeks after the last visit; the guideline edition of March 2026 in force from its effective date, the register's earlier moves made at 35 kg; the warehouse stock by batch with a quarantined lot and a planned call-off beside the confirmed lots on line 1; the programme projection in its own layout; on the asks' rows, the warehouse system's posting dates, depot transfers, returns and refusals, the customer master's region as set when each account opened, the eLMIS reports' resubmissions and submission-time region, a partner's donated TLD on its own product line, and facility codes reissued after closures. Each is how those systems write their files and none carries the call (asserted neutral, R2; the ask items sit outside the call's rows, SEP).
Layer 2: estimation_fit, the data's real structure: a decision taken on a single scattered reading of each child's growth at the visits its dispensing interval schedules, so the switch month is the first scheduled weighing that reads 30 kg, forecast from each child's own line, the scatter around it and its schedule; the choice that flips the call is modelling the weighing rather than the line.
Decisive step: forecast each child's switch as the first scheduled weighing that reads 30 kg or more, each weighing a draw around the child's own growth line at the scatter the register shows, at the child's own visit interval, rather than as the month the line reaches 30 kg, the register's switches by recorded band or its recent switch count.
Not semantics: every field is read correctly on the default path (weights to 0.1 kg, regimen codes in both layouts, visit dates, months dispensed, next appointments, the crosswalk, exits, the dosing table and its effective date, the SOP's terms); reading every one right still leaves the analyst choosing how to forecast when each child is first weighed at 30 kg, and the growth line files 10 pallets.
Not rule application: the guideline files the dosing band, its effective date and that a child on TLD stays on it, and the SOP files the estimand (the window, the population, one bottle per child in care on TLD at a month's end, the maximum stock months, the line and the pallet); no filed rule or procedure says when a child will be weighed at 30 kg or how to forecast it, and executing every filed rule on projected growth lines files the short line.
No decoy: no memo, draft, forecast, stakeholder figure or earlier order argues a figure for line 2; the stock status report states past stock and issues correctly and ranks nothing; no document describes how children's weights behave or how switches were forecast before.
Analyst test: a strong analyst who reads both register layouts, links the children, applies the 2026 dosing band and the SOP correctly and moves each child onto TLD when the child's fitted growth line reaches 30 kg files 10 pallets against the golden 11 (executed in checks.py on the generator's clean truth, R3a); the analyst who carries the register's switch rates by recorded weight band files 9 pallets and the recent switch count 12, and forecasting each scheduled weighing's chance of reading 30 kg files the golden (R3b).
Estimand: the CMS quantification SOP files the population (children under 15 on treatment at the 31 August 2026 count from the paediatric register, followed to 30 June 2027 whatever their age), the outcome (forecast consumption, one 30-tablet bottle for each child in care on TLD at the end of a month, a child who leaves care not counted), the window (1 September 2026 to 30 June 2027, plus six months of June's), the line (line 2, stock netted on line 1 alone) and the unit (the whole pallet of 8,064 bottles, to the nearest pallet); there is no comparison.
No certified replay: no shipped figure is reproduced to recover a method; the register's closed windows are the analyst's own out-of-sample record, read alike by every method.
Lesson: a model learns that a transition taken on a single measurement happens at the first reading over the line, not when the underlying path crosses it, so a noisy repeated measurement pulls switches forward by months; that the number of readings a unit will have is set by its own schedule, so a rate measured when units were read every month does not carry to units read every two or three; that a rule's history does not forecast under a changed rule; and that a fitted line's scatter is part of the forecast, not noise to be smoothed away; no build on file forecasts a first passage of scheduled noisy measurements over a dosing band.

## Readability screen

Six tests per rung (1 a filed sentence names it or sends the solver looking, 2 a column, key or marker makes it a row
predicate or a header join, 3 an opponent reflex, 4 a control or corpus scores it, 5 the hygiene battery finds it, 6
one subtraction, ratio or half of a figure). Figures from `generator/ladder.py` on the cut pack, asserted in
`generator/checks.py` (R3a, R3b, LAD, OOS).

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the children on TLD at the count carried, nobody switching (9 pallets) | SOP 4.2 asks for the register's children to the window's end | the regimen column | yes, the patients on the regimen carried | the register's own switches: thousands of children moved in each closed year | no | yes | readable |
| R1 each child's growth line through its weighings reaching 30 kg (10 pallets) | Annex 7.1 and 7.2 file the band and the weighing; nothing says how to forecast it | weights at the visit grain | yes, the default: project growth to the threshold | the analyst's own back-test under the band then in force: the line misses the closed windows' switches by -51.9, -54.3, -73.1 per cent | no | no | readable |
| R1b the register's switch rates by last recorded weight band (9 pallets) | the annex's change table dates the band | the weight and regimen columns | yes, transition rates by band | measured before March 2026 they are rates of reaching 35 kg | no | no | readable |
| R1c the last months' switch count carried, or its trend (12 to 16 pallets) | the annex's effective date | the month of each regimen change | yes, the trailing count | the count holds the March to May 2026 backlog of children moved at 30 to 35 kg | no | yes | readable |
| R1d an age rule: a fixed switch age, the register's median switch age, ten and over, or the age at which its median weight for age reaches 30 kg, each waiting for the child's age (9 to 15 pallets) | no | dates of birth | yes, age as a proxy | the cohort is small for its age: an age carries the wrong children | no | yes | readable |
| R1e the line moved by the register's median lead of a switch over its line (9 pallets) | no | no | partly: calibrate the line on past switches | the register's leads were measured at 35 kg | no | no | readable |
| R2 (decisive) each scheduled weighing's chance of reading 30.0 kg or more around the child's own line through its weighings, at the register's scatter and the child's own interval, the first such reading the switch (87,987 bottles) | no sentence describes a weighing's scatter or a first passage; the annex files the band of the weight recorded at the visit, the SOP files the population, the month-end bottle, the line and the window | no column carries a residual, a switch probability or a forecast; the register holds weights, regimens, months dispensed and appointments | no: the reflexes are the growth line, band rates, the trailing count, age and a calibrated lead, each measured wrong | none ships: no document scores a forecast; the register's closed windows are read alike by every method | no: nothing duplicated, missing or mis-keyed points at it | no: a line and a residual scatter per child, a normal tail at each scheduled visit, a first passage, then retention | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative and its call | Ruled out by |
|---|---|---|---|---|
| SF1 | "under 15 at the count" | born after 31 August 2011 | born on or after it | same call: no child in the register was born on 31 August 2011 (asserted) |
| SF2 | "on treatment" | no outcome entered (SOP 4.2), outcomes dated after the count read as not yet happened | the 12 candidates last seen over three months before the count dropped (11 pallets) | SOP 4.2 "(no outcome entered)"; same call |
| SF3 | a month's consumption | one bottle for each child in care on TLD at the month's end (SOP 4.1) | half a bottle in the month a child moves (11 pallets) | SOP 4.1; same call |
| SF4 | line 2's maximum stock | six months of June 2027's forecast (SOP 4.3) | six months of the cycle's average month (11 pallets) | SOP 4.3; same call |
| SF5 | "usable stock" (line 1) | the batches neither quarantined nor expired | the quarantined batch counted (line 1, 339 pallets against 342) | SOP 3.3 |
| SF6 | "quantities on order" (line 1) | the three lots with a confirmed delivery date | the planned C7 call-off counted (line 1, 265 pallets) | SOP 3.3 ("not quantities on order until the supplier confirms a delivery date") |
| SF7 | the window | 1 September 2026 to 30 June 2027 | January to June 2027 only (8 pallets) | SOP 3.1 and 4.3 ("from the first day of the month after the count") |
| SF8 | "on or before the last day of the cycle ordered" (line 1) | every confirmed lot is due by November 2026 | lots due within C6, or before the window closes | same call: the same three lots on every reading (asserted) |
| SF9 | rounding path | line 2 rounded once to the nearest pallet | its consumption and maximum stock rounded to pallets first (11 pallets) | SOP 4.4 ("each line is ordered in whole pallets ... rounded to the nearest pallet"); same call |
| SF10 | the paediatric second line | moves to the adult second line at 30 kg | moved onto TLD (adds the 223 second-line children's switches) | Annex 7.3 |
| SF11 | the weight a band applies to | the weight recorded at the visit | a smoothed or average weight | Annex 7.1 ("the band of the weight recorded at that visit"); no other reading is filed |
| SF12 | patients starting after the count | the projection's (line 1) | the register's children who started after 31 August | same call: the register holds none (asserted) |
| SF13 | children who turn 15 in the window | stay in line 2 | dropped at their fifteenth birthday (887 children; 10 pallets) | SOP 4.2 ("whatever their age by then") |
| SF14 | the count (line 1) | both warehouses | the Main warehouse alone (line 1, 359 pallets) | SOP 2.1 |
| SF15 | a TLD child's later reading under 30 kg | stays on TLD | dosed back to the paediatric band at the visit's weight (Annex 7.1's first sentence read alone) | Annex 7.1 ("A child or adolescent started on TLD stays on TLD at later visits, whatever the weight recorded"); the register moves none back (asserted) |
| SF16 | the band for the window | 30 kg (the 2026 edition, effective 1 March 2026) | the 35 kg band of the register's earlier moves (9 pallets) | Annex 7.1 ("This edition lowers the weight from which TLD is given from 35 kg to 30 kg") and 7.5 |
| SF17 | where the stock is netted | on line 1 alone | the children's share of the stock netted on line 2 (8 pallets) | SOP 4.3 ("which are netted on line 1 alone") |
| SF18 | children who leave care | not counted from the month they leave | every child kept in care to June 2027 (89,639 bottles, 11 pallets) | SOP 4.1 ("is not counted from the month the patient leaves"); same call |

## Ladder

Built figures from `generator/ladder.py` on the cut pack, every row asserted in `generator/checks.py` (FAM, LAD, R3a,
R3b, OOS, SHR) and the golden recomputed from the bundle by `generator/verify.py`. Line 2 in bottles over the window
with six months of June 2027; 11 pallets hold 84,672 to 92,735 bottles.

| Rung | Construction | Line 2, bottles | Pallets | Dies to |
|---|---|---|---|---|
| R0 | the children on TLD at the count carried, nobody switching | 71,103 | 9 | the register: children move onto TLD every month |
| R1 default | each child's line through every weighing reaching 30 kg, at its own visits (36 and 24 months: 80,155; 80,176) | 80,128 | 10 | out of sample: -51.9, -54.3, -73.1 per cent |
| R1a | the same on 12-month lines, or exponential lines (24 and 12 months) | 82,465; 83,250; 84,481 | 10 | the same projection to the threshold as R1 |
| R1b | switch rates by last recorded weight band, half-kilogram and one-kilogram bands | 75,298; 75,293 | 9 | measured on moves at 35 kg |
| R1c | the band chain over 24 months | 79,483 | 10 | the same, its 25 to 29.9 kg band almost never moving before March |
| R1d | the last 3, 6 or 12 months' switches carried, or their trend | 96,057; 126,052; 102,134; 130,740 | 12 to 16 | the March to May 2026 backlog of children moved at 30 to 35 kg, and visits since thinned |
| R1e | the line moved by the register's median lead of a switch over its line | 72,545 | 9 | the leads were measured at 35 kg |
| R1f | age rules waiting for each child's age: the median switch age, the age at which the register's median weight for age reaches 30 kg (12 binnings) | 75,965 to 76,629 | 9 to 10 | the cohort is small for its age |
| R1g | fixed ages 10 and 11 with the backlog, ten and over | 104,445 to 121,773 | 13 to 15 | an age carries the wrong children |
| R1h | the last recorded weight at 27 or 29 kg moved at the first visit | 97,210; 77,487 | 12; 10 | one reading is one draw: the scatter cuts both ways |
| R1i | each child along the register's median weight-for-age curve from its own level | 81,761 | 10 | the cohort grows more slowly than the curve |
| R2 decisive | each scheduled weighing's chance of reading 30.0 kg or more around the child's own line, the first such reading the move, the register's held-back share moving at the next weighed visit | 87,987 | 11 | golden |

**Position and margins.** The golden's line 2 is 87,984 bottles counted in whole children each month (87,987
unrounded), 11 pallets, 3,312 bottles inside its pallet. The pallet holds 8,064 bottles; a quarter pallet with one
sigma (the switch increment's spread with the candidates resampled, 360 bottles) is 2,376. The default path sits one
pallet below, 4,544 bottles under the pallet's edge.

**Convergence (C3, asserted, FAM).** Twenty-six constructions of the decisive step file line 2 between 87,173 and
90,258 bottles, every one 11 pallets and each 2,478 bottles or more inside the pallet (a quarter pallet and one sigma
is 2,376):

| Member | Choice | Bottles | From the golden | Inside the pallet |
|---|---|---|---|---|
| golden | every weighing, pooled residual SD (1.29 kg), the register's weighed share, the held-back share, exits by age | 87,987 | 0 | 3,315 |
| plain | nobody held back | 88,399 | +412 | 3,727 |
| thr2995 | the band at 29.95 kg (readings to 0.1 kg) | 88,441 | +454 | 3,769 |
| win36, win24 | lines on the last 36 or 24 months | 87,803; 87,835 | -184; -152 | 3,131; 3,163 |
| q1 | every scheduled visit weighed | 88,344 | +357 | 3,672 |
| sig_rms, sig_mad, sig_diff, sig_near, own_sd | the scatter as the residuals' root mean square, 1.4826 MAD, from consecutive weighings, from the children whose line stands within 6 kg of the band, each child's own | 87,601; 87,430; 87,740; 87,968; 87,877 | -386; -556; -246; -19; -109 | 2,929; 2,758; 3,068; 3,296; 3,205 |
| pv, pv_win36, pv_win24 | the textbook OLS prediction variance s2 (1 + 1/n + (t - tbar)2 / Sxx) at each visit, the visits independent, on every weighing, 36- or 24-month lines | 89,065; 89,200; 90,258 | +1,078; +1,213; +2,271 | 3,671; 3,536; 2,478 |
| eb_plug (and 36, 24 months) | each slope shrunk toward the random-effects mean (DerSimonian and Laird), plug-in | 87,657; 87,424; 87,173 | -330; -563; -813 | 2,985; 2,752; 2,501 |
| eb_pred (and 36, 24 months) | the shrunk slope with its posterior variance at each visit | 88,639; 88,650; 88,960 | +653; +663; +974 | 3,967; 3,978; 3,776 |
| eb_joint, mc_joint | each child's line drawn jointly from its estimation error, around the shrunk or the OLS slope | 87,890; 88,245 | -97; +258 | 3,218; 3,573 |
| monte_carlo | the golden's model simulated | 87,994 | +7 | 3,322 |
| hazard24, hazard_pooled | exit rates over 24 months, or pooled over ages | 87,982; 88,105 | -5; +118 | 3,310; 3,433 |
| seasonal | the register's calendar-month residual added at each visit | 87,888 | -99 | 3,216 |

A solver may make two of the single choices at once: the pair that pushes the line furthest up (nobody held back, the
29.95 kg band) files 88,860 and the pair that pushes it furthest down (the MAD scatter, 36-month lines) 87,336, each
2,664 bottles or more inside (FAM asserted, one sigma or more). The family spans 3,085 bottles, 0.38 of a pallet: the
per-visit prediction variance on 24-month lines (+2,271) and the shrunk plug-in slopes on 24-month lines (-813) set its
ends.

**Slopes pooled (asserted, SHR).** The register's per-child slopes vary between children by more than their
estimation error (DerSimonian and Laird tau 0.054 kg a month, Q 70,823 on 7,109 degrees of freedom); slopes pooled by
sex and year of age over the candidates (86,680), over every paediatric child (87,527) or over every child (89,680),
and the candidates' one mean slope (87,498), all take the decisive step and all land in the pallet; they are reported,
not counted as the family, and they under-forecast every closed window by 8 to 30 per cent.

**The out-of-sample record (asserted, OOS).** Every closed window lies under the 35 kg band, before the 2026 edition:
each construction stood at 31 August 2024 and 28 February 2025 over 12 months and at 31 August 2025 over 6 months, on
the children in care on a paediatric first line at that date, against the bottle-months the register shows they took
on TLD: the golden -7.9, -8.7, -13.0 per cent; every construction that reads the move off a scheduled weighing within
a fifth (the per-visit prediction variance +10.1, +4.1, -2.4 per cent; a weighing at every month -0.1, -1.1, -3.1 per
cent); the growth line -51.9, -54.3, -73.1 per cent; the shrunk plug-in slopes -25.2, -22.0, -26.1 per cent. Under the
old band the register's own rates did not mislead (band rates +5.5, +5.6, +15.0 per cent; the last three months'
switches +0.2, -13.7, +12.9 per cent): what kills them in the window is the band and the visit frequency the 2026
guidelines changed, which no closed window can show. The back-test separates the line from the first passage; it
cannot rank inside the family, and the pallet holds the whole family.

**The crossing-age rule (asserted, LAD).** Each child moved on reaching the age at which the register's median weight
for age reaches 30 kg misses the pallet under all 12 binnings that wait for each child's age (9 to 10 pallets); the 12
binnings that move every child already past that age at its next visit land under 11 (the crossing near 12 years), as
do a fixed age of 12 with the backlog (89,758) and the register's median switch age with the backlog (90,817).

**Routes that land without the decisive step (reported, LAD).** Calibration knobs: the line moved earlier by 3 to 6
months (85,427 to 91,514) or raised by 0.75 to 1.25 kg (86,596 to 91,870); the last recorded weight at 28 kg moved at
the next visit (86,637); exponential lines through every weighing (87,676); the band chain over the last 12 months
(86,116, half of its window before March). The decisive step taken with a variation the family does not hold also
lands: 12-month lines with the scatter (88,819), exponential lines with the scatter (90,325; 90,370), a weighing at
every month (91,724) and every child kept in care (89,639).

**Strength.** P(one strong solver lands) about 0.4: about a quarter take the decisive step (each scheduled weighing
read around the child's own line at the register's scatter), and roughly 0.13 more reach 11 pallets by a knob or a
rule that happens to land (a chosen lead or margin, the crossing age with the backlog, the 28 kg last weight, the
12-month band chain); the growth line, the register's band rates, its trailing counts, its calibrated lead and the age
rules that wait for each child's age, the habitual routes, each file elsewhere. P(both land) about 0.2.

**Residual.** (1) The pallet is 0.38 of the family span plus margin: the per-visit prediction variance on 24-month
lines sits 102 bottles above the quarter-pallet-and-sigma line, the tightest member. (2) The cheap landers above raise
P(one): an 8,064-bottle pallet is 1.03 times the default path's lever, so knobs set near the right value land. (3) The
golden under-forecasts the closed windows by 8 to 13 per cent at the 35 kg band while the per-visit prediction variance
and a monthly weighing come closer: the back-test cannot choose inside the family. (4) Multi-month dispensing arrived
with the 2026 edition: before March 2026 87 per cent of visits dispensed one month, so the median first-line child has
40 weighings since January 2023. (5) The call turns on the timing of the children's switches, which moves line 2 by
one pallet (8.9 per cent of the line) between the default and the golden.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | line 2: children under 15 on treatment at the 31 August 2026 count from the register, followed to 30 June 2027 whatever their age; line 1: everyone else from the projection | filed (SOP 4.2, 4.3); SF1, SF2, SF12, SF13 |
| 2 | Unit of account | the 30-tablet bottle, one for each child in care on TLD at a month's end; the line in whole pallets | filed (SOP 1.2, 4.1, 4.4); SF3 |
| 3 | Attribution window | 1 September 2026 to 30 June 2027 | filed (SOP 3.1, 4.3); SF7 |
| 4 | As-of dating | the count of 31 August 2026; the register and the stock report as pulled on 2 September | filed (SOP 2.1, 2.2; the extract manifest); outcomes entered after the count: same call (R2 asserted) |
| 5 | Version basis | the 2026 edition of Annex 7, effective 1 March 2026; the projection round of September 2026; the stock status report of the count; SOP version 3 | each file carries one version and its effective date; SF16 |
| 6 | Denominator | none: the line is a count of bottles | n/a |
| 7 | Weighting | each child counted once in each month on TLD | filed (SOP 4.1) |
| 8 | Window length | the weighings each child's line is fitted to | C3: every weighing since January 2023, the last 36 or 24 months, each with or without the prediction variance or shrinkage, all in the pallet (FAM asserted) |
| 9 | Boundary inclusivity | 30 kg and over takes TLD; under 15 at the count | filed (Annex 7.1, 7.2 "30 and over"); a 29.95 kg cut inside the pallet (FAM asserted); SF1 converges |
| 10 | Rounding path | line 2 rounded once to the nearest pallet of 8,064 bottles | filed (SOP 4.4); SF9 |
| 11 | Tie-break | none | n/a |
| 12 | Maturity and censoring | exits entered weeks after the last visit; children whose switch the window has not reached; readings held back to the next visit | C3: exit rates over 12 or 24 months, by age or pooled, and nobody held back, all in the pallet (FAM asserted); R2 asserted on late-entered outcomes; SF18 |
| 13 | Order of operations | each month's children on TLD, summed, with six months of June, rounded | filed (SOP 4.1, 4.3, 4.4); SF4, SF17 |
| 14 | Row order | sums | C1 |
| 15 | Duplicate resolution | the June 2024 migration month in both layouts; EPR rows re-sent after a failed sync | C1: kept twice or dropped, same call (R2 asserted) |
| 16 | Identity normalisation | legacy ART numbers to the national identifier | the crosswalk; C1: unlinked legacy rows leave the call (R2 asserted) |
| 17 | Netting against gross | line 2 gross; the stock and the lots netted on line 1 | filed (SOP 3.1, 3.3, 4.3); SF5, SF6, SF8, SF14, SF17 |
| 18 | Dimensional units | kilograms to 0.1 (paper sites to 0.5 until May 2024), bottles, pallets of 8,064 | the dictionary states each layout's precision; the window's readings are the EPR's 0.1 kg; the 29.95 kg member covers the recording (FAM) |
| 19 | Code and status semantics | regimen codes in both layouts, outcome codes, batch status, lot status | the code list and the dictionary; SF5, SF6, SF10, SF15 |
| 20 | Integerisation | whole children in each month's bottles, the line rounded once | the golden mid-pallet (FAM asserted, a quarter pallet and one sigma or more inside) |
| 21 | Clause scope | SOP QP-04 version 3, effective 1 March 2026, governs the September 2026 review; Annex 7 of 2026 governs every visit from 1 March 2026 | filed (the SOP's header; the annex's header and 7.1) |
| 22 | Forward window contents | each child's switch month inside the window | forecast from the records (the decisive step); no file covers the window |

## Literal reader

Executing the prompt, SOP QP-04 sections 1 to 4 and Annex 7 word for word gives line 2 of the C7 order: the children
under 15 at the count with no outcome entered, followed to June 2027 whatever their age, one bottle for each child in
care on TLD at each month's end from 1 September 2026 to 30 June 2027, plus six months of June 2027's, to the nearest
pallet of 8,064 bottles, each child moving onto TLD at the visit whose recorded weight is 30 kg or more and staying on
it; no shipped sentence says when each child's recorded weight will first reach 30 kg, so a literal reader must
forecast it from the register; the easy method on the same literal estimand (each child's growth line reaching 30 kg)
files 10 pallets, and the fork table leaves no reading under which a rung is the golden.

## Oracles

- The register's closed windows: every method reads them alike; on the wrong path they supply the band rates, the
  trailing count and the calibrated lead, all measured at 35 kg and at monthly visits, and the analyst's own back-test
  on them rejects the growth line and the shrunk slopes. No closed window holds a C7 figure.
- The annex's change table: it dates the band and the dispensing interval, true for every reader; it ranks nothing.
- The stock status report and the projection: line 1's inputs, filed, read alike by every route.
- The ask files' totals: the eLMIS reports and the warehouse documents tie to nothing the call reads.
- No control ties only under the golden.

## Ask sheet

**Main call's declared row population:** the register's visits in both layouts, its patient file, the crosswalk and
the code list; SOP sections 1 to 4 and Annex 7 (line 1's components add the projection's national row and the stock
status report's Stock on hand and On order sheets). Device and hazard rows in it: 0 (asserted, SEP: the call's
computation opens no ask file, and the call's files and the ask files are disjoint).

**Ask A. Bottles CMS delivered to each region's ART facilities in C4 and in C5, each facility in its current region,
each delivery dated by when it was signed for** (12 figures, whole bottles).
- H18 home: SOP 5.1, the review's comparison before the order is filed, region by region, of the dispensing facilities
  reported for the last two closed cycles with the deliveries CMS made to them.
- Use: the workbook's region table and the chart.
- Basis (the prompt): the facility's current region; the delivery's signature date.
- Primary A1 (D7, codes reissued to other entities): seven facility codes of sites closed in March 2026 reissued to
  new sites opened in April and May 2026 in other regions; the registry carries both records under each code, the
  closed one with its closure date. Joined to the operational record, the closed sites' C4 and C5 deliveries land in
  the new sites' regions: moves 12 of 12 figures by 72 to 16,584 bottles. Fair: the registry's opening and closure
  dates and the customer accounts' own dates place every delivery. Silent: every code joins; the repeated code reads as
  a duplicate the battery resolves to the operational record.
- Primary A2 (D5, delivered only on the face of the record): 81 customer delivery lines whose proof of delivery
  records a refusal at the gate, the goods back on a return document days later; counted as delivered, moves 12 of 12 figures by 1,224 to 28,020 bottles.
  Fair: the proof of delivery's signer field. Silent: each refused delivery has a proof of delivery with a date and is
  a customer delivery in the warehouse file; its return sits on the same return document series as the 187
  returns of short-dated stock collected from facilities for redistribution (12,432 bottles), so netting every
  return does not tie with leaving the refusals out (moves 12 of 12 figures by 372 to 1,344 bottles).
- Hazards: the customer master's delivery region as set when each account opened, before the April 2026 boundary
  change (the dictionary says so; moves 12 of 12 figures by 7,896 to 114,084 bottles); posting dates one to twelve days
  before signature (moves 12 of 12 figures by 5,076 to 16,464 bottles); the Northern depot's restocking transfers
  counted as deliveries (Northern's figure rises 604,032 in C4; Northern's figure rises 564,384 in C5).
- Stops (built and asserted): S1 the cracker (signature dates, customer deliveries, the operational record, refusals
  counted): all 12 miss; S1a A1 cracked alone: all 12 miss; S1b A2 cracked alone: all 12 miss; S2 both: the golden.
- Span: the deliveries, the proofs of delivery, the customer accounts, the facility registry, the dictionary and the
  manifest (6 files).
- Realism: a facility registry reissues a closed site's code; a warehouse system keeps an account's region as set when
  it was opened; a delivery refused at the gate keeps its delivery note and returns on a return document.

**Ask B. Bottles those facilities reported dispensing in their monthly reports for C4 and for C5** (12 figures, whole
bottles).
- H18 home: the same SOP 5.1 comparison, its dispensing side.
- Use: the workbook's region table and the chart.
- Basis (the prompt): the facility's current region; the reports for the cycle's months.
- Primary B1 (D7, the same reissued codes on the reports' path): joined to the operational record, the closed sites'
  reports land in the new sites' regions: moves 12 of 12 figures by 64 to 14,574 bottles.
- Primary B2 (D5, a category crossed by its code): a partner's emergency donation of TLD in November 2025 at about one
  site in eight in every region, dispensed before CMS stock and reported on its own line (product code ARV0412D, which
  the dictionary files as the same tablet and bottle from partner-donated stock) in 154 reports from November 2025 to
  February 2026; taking the CMS product code alone, moves 12 of 12 figures by 1,500 to 27,785 bottles. Filed: the dictionary names ARV0412D as the same
  bottle from partner-donated stock, so B2 is a filed reading and Ask B's silent device is B1.
- Hazards: the region stamped on each report at submission (moves 12 of 12 figures by 2,303 to 111,815 bottles); 198
  returned submissions, each resubmitted and approved (summed, moves 12 of 12 figures by 7,077 to 86,893 bottles);
  August 2026 reports still awaiting review, outside both cycles.
- Stops (built and asserted): S1 the cracker (approved reports, the operational record, the CMS code): all 12 miss;
  S1a B1 cracked alone: all 12 miss; S1b B2 cracked alone: all 12 miss; S2 both: the golden.
- Span: the eLMIS reports, the facility registry, the dictionary and the manifest (4 files; 7 across both asks).
- Realism: an eLMIS requisition stamps its requisition group's region when submitted; a donated batch is reported on
  its own product line.

**Hazard table.**

| Hazard | Asks moved | Per-ask delta read the easy way |
|---|---|---|
| A1 and B1 reissued codes | A, B | A moves 12 of 12 figures by 72 to 16,584 bottles; B moves 12 of 12 figures by 64 to 14,574 bottles |
| A2 refusals | A | moves 12 of 12 figures by 1,224 to 28,020 bottles |
| every return netted | A | moves 12 of 12 figures by 372 to 1,344 bottles |
| B2 the partner donation (filed) | B | moves 12 of 12 figures by 1,500 to 27,785 bottles |
| the account's region as opened | A, B | A moves 12 of 12 figures by 7,896 to 114,084 bottles; B (the report's submission region) moves 12 of 12 figures by 2,303 to 111,815 bottles |
| posting dates | A | moves 12 of 12 figures by 5,076 to 16,464 bottles |
| depot transfers | A | Northern's figure rises 604,032 in C4; Northern's figure rises 564,384 in C5 |
| returned submissions summed | B | moves 12 of 12 figures by 7,077 to 86,893 bottles |

**Referee.** None: the prompt files each ask's basis and nothing shipped totals a graded figure on the golden path.

**Cracker sheet** (the cracker landed the call, ran the hygiene battery, executed every filed definition and took each
file's columns as they stand):

| Ask figures | The cracker's route | Device that holds | Verdict |
|---|---|---|---|
| A, delivered in C4 by region (6) | deliveries dated by the proof of delivery, joined by code to the operational record, refusals counted | A1 and A2 at every region | miss |
| A, delivered in C5 by region (6) | the same | A1 and A2 at every region | miss |
| B, dispensed in C4 by region (6) | approved reports joined by code to the operational record, the CMS product code | B1 and B2 at every region | miss |
| B, dispensed in C5 by region (6) | the same | B1 and B2 at every region | miss |

**Single cracks.** Any one device cracked alone keeps none of the 24 (measured: the reissued codes, the refusals, the
donation, the refusals and the donation together, and every return netted, alone and with the reissued codes). Both
devices of one ask cracked keep that ask's 12 (measured), and the pair then reads 42.3. The isolated reader of stage 4
is the measurement (`score_reader.py`); this sheet is the author's model of the opponent.

**Mirror sheet.** The mirror stops at the growth line (10 pallets) and reads each row's own region (the customer
master's for a delivery, the requisition group's for a report), dating deliveries by the proof of delivery as asked:
it keeps none of the 24.

Measured by: `generator/cracker.py` (run on the cut pack by `checks.py` on every build).

Mirror leakage: 0.0 per cent of ask weight (24 ask criteria; the chart carries the same figures).

Pair ceiling: 28.5 (the cracker at 38 + 7 + 55 x 0/24 = 45.0, the mirror at 5 + 7 + 0 = 12.0); both top responses on
the call: 45.0. Criteria supplied: line 2 in pallets (1), line 1 in pallets with its consumption, maximum stock,
usable stock and confirmed shipments (5), the children on TLD and on a first line (2), the table's 24 figures, the
chart's two panels and labels (2) and the two files: 36. Line 2's bottles before rounding vary by up to 3,085 across
the family and are not a graded figure; the write-up states the golden's as its working.

## Leak review

`leak.py --asof 2026-09-02`: REVIEW, no LEAK. Each line:
- Sweep 3, the SOP carries 7 of 8 words of the committed call: they are the estimand's own terms (line 2, the C7
  order, pallets, TLD 30s, the children of the register) in sections 4.2 to 4.4; the SOP states no figure for any
  line and no forecast; harmless.
- Sweep 4, the SOP (forecast, months, pallet, quantification, national, carries): 4.2 to 4.4 file the population, the
  window, the line and the pallet; it names no weighing, scatter, growth line or switch timing; harmless.
- Sweep 4, Annex 7 (months, weight, dosing, visits, national, recorded): the guideline's dosing by the band of the
  weight recorded at the visit, its effective date and the 35 to 30 kg change, that a child on TLD stays on it, and
  the two- and three-month dispensing rule; it says nothing about how a weighing scatters or when a child will be
  weighed into a band; harmless (the band rule is the filed WHAT, SF11, SF15, SF16).
- Sweep 9, the stock status report's dates after 2 September 2026: the lots' due dates and the batches' expiry dates,
  forward by nature; harmless.
- Sweep 9, the EPR encounters' dates after 2 September 2026: the next_appointment column, forward by nature; no visit,
  sync or outcome date passes the pull (REAL asserted); harmless.

`guard.py heart` after the stage 4 redraw of the context artifact (`operations_log`): WARN, no BLOCK (overuse
of the organisation family and the objective, the how-many form against task246, answered in `## Draw`).

## Tried and rejected
- A national adult forecast left to the solver (consumption trend or the cohort model of the seed): the adult projection's own spread swamps the children's wave, so no estimator family agrees to a step of the order; the adult part is filed as the programme projection.
- The children's growth on reference centile curves (CDC-shaped weight-for-age) as the truth: per-child functional forms fitted to scattered weighings disagreed by more than a step; growth is straight in kg from age six in this world, and the pooled weighings show it.
- A transient dolutegravir supply constraint as the driver: a dated cause whose effect is a step in the switch series, read off the date.
- An adult nowcast of undetected exits filled by multi-month dispensing: the driver of task231 again, and the adult trend is immune to it.
- A report-back device on the call's own rows: banned by the separation line.
- The wave's peak inside the window (the 2015-16 cohort born half a year earlier): every estimator agreed, but the trailing switch count and its linear trend landed inside the golden's step; the cohort was set later so the window holds the rise.
- Twelve-month per-child growth fits as the golden family's member: on scattered weighings their slopes carry so much error that the first passage is overstated by about a sixth in the forecast and by 30 to 50 per cent on every closed window; the family is the fits on each child's whole register history, which the closed windows validate within five per cent.
- A chart of the national months of deliveries and dispensing labelled at its peak: the peak month was a figure the cracker landed; the chart carries the table's 24 figures by region.
- Reissued codes closing in December 2025: the cracker's region route cancelled across the two cycles and kept Capital C5 and Central C5; the closures moved to March 2026 with larger, varied sites.
- A rival list that included the pooled-velocity and shrinkage constructions as members of the golden's family: after the infants' scatter fix they spread the family over 4,700 bottles, the 29.95 kg member four bottles inside the step's edge; each under-forecasts every closed window by 9 to 24 per cent while the register measures the slopes' spread between children, so they are reported as decisive-step routes, not members, and the step is centred on the per-child family.
- The empirical Bayes member with the between-child variance from unweighted moments: on this register it comes out at zero and shrinks every child to one mean slope; the DerSimonian and Laird estimate stands beside it, and both fail out of sample.
- The same scatter for an infant's weighing as for a 25 kg child's: readings under 3 kg and one below zero; a reading's scatter and clothing allowance shrink below 15 kg (an infant scale), which moved no switch and lowered the pooled scatter from 1.31 to 1.28 kg.
- New sites' customer accounts opened after their first delivery, and opening stock signed for before the registry's opening date: accounts now open two to six weeks before a site opens and its opening stock arrives on the day it opens.
- Other products' eLMIS lines with a loss larger than the stock on hand: the balance identity broke on 12 lines; the loss is capped at the stock.
- "Bottles it allows for patients aged 15 and over" as one figure: a reader could leave the maximum stock out of it; consumption and maximum stock are asked apart.
- Back-test percentages for every rival in the write-up: the band and trailing-count constructions vary with the bin and window a reader picks; the write-up bounds only the golden and the growth line.
- A delivery picked from two batches split on two different draws: its two lines summed to more or less than the quantity the facility received, so CMS's deliveries and the facility's eLMIS receipts disagreed on every such delivery; the split now shares one draw (the stream of later draws kept), which moved the asks' delivery figures and nothing the call reads.
- A family placed on its single choices' midpoint: two upward choices made together (the 29.95 kg threshold with 24-month lines) then sat 58 bottles inside the step's edge; the step is now centred on the span of the members and of the two compound choices that push the need furthest up and down.
- The whole C7 order at the nearest 5,000 bottles as the call (stage 4, round 1): the judge found the step unforced (the textbook per-visit prediction variance crossed its edge by 380 bottles, 24-month lines with it and the shrunk slopes by more), and the audit found the children's part 0.93 per cent of the order; the call moved to line 2, the children's part as its own line, in whole pallets.
- The repaired register with paediatric multi-month dispensing from July 2024 (most stable children on three months for two years): the lever between the growth line and the golden fell to 4,000 to 5,000 bottles while the family, with the prediction-variance and shrinkage routes in it, spread over 3,300, and the register's band rates, band chain and trailing counts sat inside any rounding wide enough to hold the family; the rollout moved to March to August 2026, with the guidelines.
- A stationary register with TLD at 30 kg throughout: every history-based route (band rates, the band chain, the trailing counts) measured the same flow the golden forecasts and landed in its pallet; the 2026 edition's change from 35 kg follows the WHO update of 2021 that many programmes adopted late, and it makes every rate measured on the register's history a rate of a band no longer in force.
- Line 2 rounded to 5,000 bottles with every prediction-variance construction in the family: the per-visit prediction variance on 24-month lines sits 2,271 bottles above the golden and the shrunk 24-month plug-in 813 below, so no 5,000-bottle step holds both a quarter step and one sigma from its edges; the order is placed in pallets of 84 cartons of 96 bottles, and a pallet holds them.
- The paediatric line the moving children leave (ABC/3TC with DTG 50 mg, 20 to 29.9 kg) as the call: its inflow at 20 kg is dosed visit by visit, so the noisy first passage moves only its outflow, the lever is the same number of child-months as on the children's TLD line, and the line carries two transitions to forecast.
- The children who move onto TLD in the window as the line alone (about 16,000 bottles): a pallet is half the line, so the call would be two pallets against one.
- A season of 0.2 kg peaking in May, and a velocity ramp from 2 to 6 years: windows opening at the season's peak under-forecast by a fifth on every route, and the all-weighings lines of 9- and 10-year-olds under-projected their June weight by 0.3 kg; the season is 0.08 kg peaking in September and growth is the child's own line from five and a half.
- The campaign's size changed by redrawing the world: every child's draws moved with the size and the family's centre jumped; every child of the campaign's largest size is drawn and the first 7,040 kept, the size set so the family's centre sits at the pallet's.
- The scatter of a 10 to 15 kg child's weighing shrunk like an infant's: the pooled scatter fell below the near-band children's by 0.07 kg and the MAD member drifted; infant scales stop at 10 kg.
- A crossing-age rule left out of the asserted misses: 11 of its 24 binnings, those that move every child already past the crossing age at the next visit, land in the pallet; they are reported, and the binnings that wait for each child's age are asserted to miss.
- The whole C7 TLD order as the call: the children's switch timing moved it by under 1 per cent (the default 25,000 bottles short on 2.69 million), so the 5,000-bottle step was finer than the estimator family could hold and the lever was immaterial to the order.
- Line 2 in whole pallets (8,064 bottles) as the call: the lever between the default and the golden is 1.03 pallets, so the default misses by one pallet and P(both) is about 0.2, twice the bar; routes that land the pallet without the decisive step include a chosen lead of 3 to 6 months, a margin of 0.75 to 1.25 kg, the last weight at 28 kg, age 12 with the backlog and a weighing every month; architecture 1 is spent on strength and the number needs a re-root.

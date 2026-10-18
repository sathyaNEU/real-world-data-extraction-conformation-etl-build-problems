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
Stores (CMS) buys antiretrovirals for a national programme of about 13 million people, in US dollars, every product
on a six-month cycle (C7 is January to June 2027). The national ART programme files a monthly projection of adult
patients on TLD; the paediatric and adolescent ART register (the national electronic patient register's paediatric
module) holds every child's clinic visits, weighings and regimens. A 2021-22 paediatric catch-up testing campaign put
about 14,000 children born in 2015 and 2016 on treatment; diagnosed late, they are small for their age and grow
slowly, and in August 2026 most weigh 25 to 28 kg.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task170.json`, architecture v1, registered 2026-10-18T09:10:20Z; `guard.py
   check` WARN, answered below. Nearest driver 0.08 (task119 v1).
2. Pairing: Healthcare Delivery & Health Economics (client domain) / `utilization-access-demand-forecasting` /
   Forecasting & Predictive Modeling. The task type serves Forecasting in the taxonomy. The deciding analysis is a
   pharmaceutical quantification's patient-transition forecast: the patient-months on the adult pack of children who
   will be weighed into the 30 kg dosing band at their scheduled visits before the cycle closes. Free against the last
   three registrations (task168 supply-chain-logistics x forecasting, task167 nonprofit-grant-making x forecasting,
   task246 general-statistics x data-quality-monitoring). task142 sits in the same task type (a purchasing alliance's
   Hospital in the Home overflow block, an upper percentile built from stays) and is differentiated on the card.
3. Niche: national ARV quantification of the adult first-line pack across the paediatric weight-band transition, when
   a late-diagnosed cohort born in 2015-16 is reaching 30 kg and clinic weighings scatter more than the cohort grows
   between visits.
4. Call and shape: the C7 order of TLD 30-tablet bottles filed at the quantification review (`quantity_figure`, count,
   question form how-many), to the nearest 5,000 bottles. Shape `other`: the call with its critical components, the
   asks' tables on rows the call never reads, and a chart; criteria counted in `## Ask sheet`.
5. Mechanism keys: gap time (the evidence is past weighings and past switches; the order bets on when each child's
   switch falls against a window not yet open), then population; decisive generator G7 (a switch can only happen at a
   scheduled clinic weighing, and the forecast is each scheduled weighing's chance of reading 30 kg or more), then G13
   (the cycle window holds the part of the cohort's switches that its first qualifying weighings, not its growth lines,
   put there) and G6 (the children crossing now grow more slowly than the children whose switches the record holds, so
   band transition rates measured on them do not carry); Gate G `forecasting`; strategy `other` (the first passage of
   noisy scheduled measurements over a dosing band; `forecast_method_backtest` is spent by task167 and
   `composition_mix` is task165's). Time with G13 decisive was blocked by task162 inside the batch; G7 with time is
   differentiated on the card against task161, task259, task87, task105 and task229.
6. Layer 2: `estimation_fit` (the data's real structure: repeated measurements scattering around each unit's own path,
   and a decision taken on a single reading), pattern
   `own:first-scheduled-weighing-over-the-dosing-band-from-each-childs-growth-line-and-the-scale-scatter`. The forecast
   is validated out of sample on the register's closed windows.
7. Furniture: forum `committee_or_panel` (the national quantification review committee); forcing event
   `purchase_order_or_contract` (the C7 order goes to the supplier from the review; the honest key for a cycle order,
   and also the value of task165, which is built and not yet registered: flagged for the main session);
   organisation family `government_agency` (a ministry's medical stores); role family `procurement_lead` (the CMS
   quantification lead); context artifact `monitoring_export` (the CMS monthly stock status report); calibration
   `none`. Each is free against task168, task167 and task246.
8. Spine: the paediatric register's visit extract (child x clinic visit, January 2023 to August 2026, two layouts across
   the EPR migration), constructed in the layout of a national electronic patient register's paediatric module.
9. Deliverables: `c7_tld_order.xlsx` (the order, its components, the children by month, the out-of-sample record and
   the ask table) and `c4_c5_tld_flows.png` (each region's deliveries and dispensing in C4 and C5, every bar labelled;
   never on the order).
10. People, drawn with `guard.py names --locale zu_ZA --seed 170`: Nomalanga Magubane (the CMS quantification lead, the
    SOP and the stock status report), Thabisile Mahlinza (the paediatric ART programme officer, the register extract)
    and Sibongile Sikhosana (the ART programme's monitoring officer, the adult projection), the draw's seventh, fifth
    and tenth names.

**Data-native sentence.** The paediatric register records every child's clinic weighings to 0.1 kg at each scheduled
visit, and a child moves onto TLD at the first weighing that reads 30.0 kg or more; the weighings scatter about 1.3 kg
around each child's own straight growth line while the line of a child from the 2015-16 cohort rises about 0.2 kg a
month, so most of the register's switches came at a single reading over 30 kg months before the child's line reached
it (those of the last 24 months a median 7.2 months before, `calc.P_lead_shift`), and in August 2026 about 12,200 children under 15 sit below the band, most of them that cohort at 25 to 28 kg.

**Guard and similarity.** `guard.py check` WARN at registration, re-pulled before the check and before register (the
ban window held task168, task167 and task246). WARNs answered: `overuse.org_family` (government_agency): a ministry's
medical stores is a government agency and no other family is honest; `overuse.objective` (forecasting in 6 of 12):
this lane is Forecasting; `repeat.question_form` (how-many, task246): the call is a count of bottles and a count asks
how many. NOTES: `test.same_puzzle_older` and `test.same_driver_older` (time, G7) against task161, task259 v1, task87
v9, task105 v1 and task229 v3, each differentiated on the card.

**Abstraction test.** Stripped of nouns: units move to another line at the first of their scheduled measurements that
reads at or above a fixed level, and a single measurement scatters around each unit's own path by more than the path
rises between measurements, so most moves come months before the paths reach the level; only the chance that each
scheduled measurement reads over the level, taken from each unit's own path and the record's scatter, forecasts them.
Nearest by mechanism, read for latent structure:
- task253 v3 counts units whose latent level sits below a line, seen through averages of noisy readings; here the
  decision is taken on one reading, not on the latent level, and the quantity is when the first qualifying reading
  falls, not how many units sit below the line.
- task258 counts units an intervention moves across a threshold; here nothing intervenes, and the crossing is a first
  passage of scheduled readings along each unit's own growth.
- task132 ages a fitted item along a wear curve with replacement; here no hazard by age is carried, and the
  replacement structure is absent.
- task157 and task160 time a wave from a calendar or a lag; here the wave is a cohort's growth into a band, and its
  timing in the window comes from each child's line and the scale's scatter, not from any earlier wave.
None shares the latent structure, the default path and the correction.

**Sources, one line each.**
- Seed FC41 header and Situation (`status.py task170`): the world, the decision (the C7 order at the quantification
  review) and the quantity (bottle-months of adult TLD); nothing else of the seed is read or kept.
- `guard.py mechanisms --objective forecasting`: no spent driver forecasts a threshold crossing read through scattered
  repeated measurements.
- WHO consolidated HIV guidelines' weight-band dosing (dolutegravir-based first line, the adult TLD tablet from 30 kg)
  and the paediatric ARV forecasting practice of moving patients between weight bands: the decision rule is a dosing
  band applied at the visit's weighing; the fictional programme's guideline states its own table.
- `stumping/references/strategies.md` F1 (a clock process estimated from every unit that went through it) and F5 (a
  pooled rate that does not fit the pool): the clock is each child's growth seen through its weighings, and the band
  rates of the record come from children who grew faster and sat elsewhere in the band.
- `two-layer-task-design.md`: the client's example of validating a forecast on data it was not built on; the growth
  projection, the band rates and the trailing counts all fail on the register's closed windows.

## Default path

Built figures from `generator/ladder.py` on the cut pack, asserted in `generator/checks.py` (R3a, R3b) and recomputed
by `generator/verify.py`. Children's need is bottles over the window with the six months of June 2027.

1. Read the SOP: the cycle order is the forecast consumption from 1 September 2026 to 30 June 2027 plus the maximum
   stock level (six months of June 2027's forecast consumption), less the usable stock on hand at the 31 August count
   and the quantities on order with a confirmed delivery date on or before 30 June 2027; one bottle for each patient
   on TLD at the end of a month; patients aged 15 and over at the count and every new starter from the programme's
   projection, children under 15 at the count from the paediatric register.
2. Sum the projection's national months (3,142,937 bottles) and six months of June 2027 (1,908,822); take the
   usable stock at both warehouses (1,376,018) and the three confirmed lots (1,072,992) from the stock status report.
3. Join the register's two layouts through the crosswalk, take the 3,348 children under 15 on TLD and the 12,232 on a
   paediatric first line at the count, carry them at the register's exit rates, and for each first-line child fit a
   straight line through its weighings since January 2023 and move it onto TLD at the first scheduled visit on or
   after the date the line reaches 30 kg.
4. Count one bottle per child on TLD at each month's end, add six months of June 2027, add the adults' bottles, net
   the stock and shipments and round to the nearest 5,000.

Ends on: 2,665,000 bottles (the children's need at 63,416 bottles against the golden's 86,858).

Golden: 2,690,000 bottles.

## Stump sentence

Fitting each child's growth line from the register and moving the child onto TLD when the line reaches 30 kg files a
C7 order of 2,665,000 bottles, 25,000 short; the step that lands it there is reading the switch off the
growth line when the switch is taken on a single clinic weighing, and the weighings scatter about 1.3 kg around
each child's line while the line rises about a fifth of a kilogram a month, so most children are first weighed at
30 kg months before their line gets there; the analyst who carries the register's own switch rates by recorded weight
band (2,685,000) or its recent switch count (2,675,000) also files short.

## Three rules

Task type: utilization-access-demand-forecasting (Healthcare Delivery & Health Economics), which serves Forecasting & Predictive Modeling in the taxonomy; the forecast is a national programme's demand for a medicine over a window not yet open.
Domain test: the deciding quantity is the paediatric regimen-transition demand inside a national ARV quantification, the patient-months on the adult TLD pack of children under 15 who will move into the 30 kg dosing band at their scheduled visits, forecast the way a quantification analyst builds patient transitions: from each child's own weighings, the scatter of a clinic weighing, the visit schedule each child is on and the register's retention.
Swap: "how many megawatt-hours should the utility contract for January to June" keeps a forecast and a window but loses the dosing band applied at a clinic weighing, the visit schedule that decides when a child can be moved, the late-diagnosed cohort that grows slowly into the band and the bottle a patient takes each month, so nothing places a switch months before the growth it reads off.
Layer 1: the register's migration from the legacy system to the national EPR in 2024 (legacy rows with day/month/year dates and free-text regimen lines, EPR rows with ISO dates and national regimen codes, the June 2024 migration month in both); facility ART numbers in the legacy rows against the national patient identifier, linked by the crosswalk, a new ART number at each transfer; paper sites recording to the half kilogram until May 2024; estimated dates of birth entered as 1 July; drug collections by a caregiver with no weighing; visit rows re-sent by clinic tablets after a failed sync; exits entered weeks after the last visit; the warehouse stock by batch with a quarantined lot and a planned call-off beside the confirmed lots; the programme projection in its own layout; on the asks' rows, the warehouse system's posting dates, depot transfers, returns and refusals, the customer master's region left at the old boundary, the eLMIS reports' resubmissions and submission-time region, and facility codes reissued after closures. Each is how those systems write their files and none carries the call (asserted neutral, R2; the ask items sit outside the call's rows, SEP).
Layer 2: estimation_fit, the data's real structure: a decision taken on a single scattered reading of each child's growth, so the switch month is the first scheduled weighing that reads 30 kg, forecast from each child's own line, the scatter around it and the visit schedule, and validated on the register's closed windows; the choice that flips the call is modelling the weighing rather than the line.
Decisive step: forecast each child's switch as the first scheduled weighing that reads 30 kg or more, each weighing a draw around the child's own growth line at the scatter the register shows, rather than as the month the line reaches 30 kg, the register's switches by recorded band or its recent switch count.
Not semantics: every field is read correctly on the default path (weights to 0.1 kg, regimen codes in both layouts, visit dates, next appointments, the crosswalk, exits, the dosing table, the SOP's terms); reading every one right still leaves the analyst choosing how to forecast when each child is first weighed at 30 kg, and the growth line files 2,665,000.
Not rule application: the guideline files the dosing band and the SOP files the estimand (the window, the population split, one bottle per patient on TLD at a month's end, the maximum stock level, the netting); no filed rule or procedure says when a child will be weighed at 30 kg or how to forecast it, and executing every filed rule on projected growth lines files the short order.
Analyst test: a strong analyst who reads both register layouts, links the children, applies the dosing band and the SOP correctly and moves each child onto TLD when the child's fitted growth line reaches 30 kg files 2,665,000 against the golden 2,690,000 (executed in checks.py on the generator's clean truth, R3a); the analyst who carries the register's switch rates by recorded weight band files 2,685,000 and the recent switch count 2,675,000, and only forecasting each scheduled weighing's chance of reading 30 kg files the golden (R3b).
Estimand: the CMS quantification SOP files the population (patients on TLD; children under 15 on treatment at the 31 August 2026 count from the paediatric register, followed to 30 June 2027 whatever their age, everyone else from the programme projection), the outcome (forecast consumption, one 30-tablet bottle for each patient on TLD at the end of a month), the window (1 September 2026 to 30 June 2027, plus the maximum stock level of six months of June's forecast consumption), the netting (usable stock at the count and confirmed deliveries on or before 30 June 2027) and the unit; the prompt files the rounding (the nearest 5,000 bottles); there is no comparison.
No decoy: no memo, draft, forecast, stakeholder figure or earlier order argues a figure for C7; the stock status report states past stock and issues correctly and ranks nothing; no document describes how children's weights behave or how switches were forecast before.
No certified replay: no shipped figure is reproduced to recover a method; the register's closed windows are the analyst's own out-of-sample record, read alike by every method.
Lesson: a model learns that a transition taken on a single measurement happens at the first reading over the line, not when the underlying path crosses it, so a noisy repeated measurement pulls switches forward by months; that a fitted line's scatter is part of the forecast, not noise to be smoothed away, and that shrinking each unit's path toward the group's removes the spread a first passage depends on; that transition rates measured on one cohort's position in a band do not carry to another; and that a forecast is validated on closed windows before it is trusted; no build on file forecasts a first passage of scheduled noisy measurements over a dosing band.

## Readability screen

Six tests per rung (1 a filed sentence names it or sends the solver looking, 2 a column, key or marker makes it a row
predicate or a header join, 3 an opponent reflex, 4 a control or corpus scores it, 5 the hygiene battery finds it, 6
one subtraction, ratio or half of a figure). Figures from `generator/ladder.py` on the cut pack, asserted in
`generator/checks.py` (R3a, R3b, LAD, OOS).

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the children on TLD at the count carried, nobody switching (2,655,000) | SOP 4.2 asks for the register's children to the window's end | the regimen column | yes, the patients on the regimen carried | the register's own switches: thousands of children moved in each closed year | no | yes | readable |
| R1 each child's growth line through its weighings reaching 30 kg (2,665,000) | Annex 7.1 and 7.2 file the band and the weighing; nothing says how to forecast it | weights at the visit grain | yes, the default: project growth to the threshold | the analyst's own back-test: the line misses the closed windows' switches by -71.0, -87.5, -88.4 per cent | no | no | readable |
| R1b the register's switch rates by last recorded weight band (2,685,000) | no | the weight and regimen columns | yes, transition rates by band | the same back-test: +41.4, +43.3, +26.0 per cent | no | no | readable |
| R1c the last months' switch count carried, or its trend (2,670,000 to 2,680,000) | no | the month of each regimen change | yes, the trailing count | the same back-test: -46.6, -25.2, -36.3 per cent (the trend -52.2, -30.4, -35.2 per cent) | no | yes | readable |
| R1d an age rule: a fixed switch age, the register's median switch age, ten and over, or the age at which its median weight for age reaches 30 kg (2,660,000 to 2,805,000) | no | dates of birth | yes, age as a proxy | the same back-test on the crossing-age rule: +88, -47, +32 per cent | no | yes | readable |
| R1e the scatter added to lines fitted to the last 12 months, or to a weighing at every month (2,695,000) | no | no | partly: a recent window, a monthly schedule | the same back-test: +49.8, +39.3, +30.9 per cent (every month +16.1, +15.2, +13.4 per cent) | no | no | readable |
| R1f the scatter added to slopes pooled by age or shrunk toward the group's (2,685,000 and 2,690,000) | no | no | yes, pooling or shrinking noisy slopes | the same back-test: -24.0 to -9.2 per cent on every window; the register measures the slopes' spread between children (SHR) | no | no | readable |
| R2 (decisive) each scheduled weighing's chance of reading 30.0 kg or more around the child's own line through its weighings, at the register's scatter, the first such reading the switch (86,858) | no sentence describes a weighing's scatter or a first passage; the annex files the band of the weight recorded at the visit, the SOP files the population, the month-end bottle and the window | no column carries a residual, a switch probability or a forecast; the register holds weights, regimens and appointments | no: the reflexes are the growth line, band rates, the trailing count, age, a recent window and pooled slopes, each measured wrong | none ships: no document scores a forecast; the register's closed windows are read alike by every method | no: nothing duplicated, missing or mis-keyed points at it | no: a line and a residual scatter per child, a normal tail at each scheduled visit, a first passage, then retention | silent |

## Semantic fork table

Every term in the main ask and every convention the main computation needs. Every id is asserted in
`generator/checks.py`; orders under each alternative are the checks' computed figures.

| Id | Term or convention | Golden reading | Alternative and its call | Ruled out by |
|---|---|---|---|---|
| SF1 | "under 15 at the count" | born after 31 August 2011 | born on or after it | same call: no child in the register was born on 31 August 2011, nor on the days around it (asserted) |
| SF2 | "on treatment" | no outcome entered (SOP 4.2), outcomes dated after the count read as not yet happened | children last seen over three months before the count dropped (23 children; 2,690,000) | SOP 4.2 "(no outcome entered)"; same call |
| SF3 | a month's consumption | one bottle for each patient on TLD at the month's end (SOP 4.1) | half a bottle in the month a child switches (2,690,000) | SOP 4.1; same call |
| SF4 | "maximum stock level" | six months of June 2027's forecast (SOP 3.2) | six months of the window's average month (2,675,000) | SOP 3.2 |
| SF5 | "usable stock" | the batches neither quarantined nor expired | the quarantined batch counted (2,665,000) | SOP 3.3 |
| SF6 | "quantities on order" | the three lots with a confirmed delivery date | the planned C7 call-off counted (2,000,000) | SOP 3.3 ("not quantities on order until the supplier confirms a delivery date") |
| SF7 | the window | 1 September 2026 to 30 June 2027 | January to June 2027 only (1,425,000) | SOP 3.1 ("from the first day of the month after the count") |
| SF8 | "on or before the last day of the cycle ordered" | every confirmed lot is due by November 2026 | lots due within C6, or before the window closes | same call: the same three lots on every reading (asserted) |
| SF9 | rounding path | the order rounded once at the end | each part rounded to 5,000 first (2,685,000) | the prompt's last sentence; ruled out by the prompt |
| SF10 | the paediatric second line | moves to the adult second line at 30 kg | moved onto TLD (adds the 376 second-line children's switches) | Annex 7.3 |
| SF11 | the weight a band applies to | the weight recorded at the visit | a smoothed or average weight | Annex 7.1 ("the band of the weight recorded at that visit"); no other reading is filed |
| SF12 | patients starting after the count | the projection's | the register's children who started after 31 August | same call: the register holds none (asserted) |
| SF13 | children who turn 15 in the window | stay in the register's forecast | dropped at their fifteenth birthday (405 children; 2,685,000) | SOP 4.2 ("whatever their age by then") |
| SF14 | the count | both warehouses | the Main warehouse alone (2,870,000) | SOP 2.1 |

## Ladder

Built figures from `generator/ladder.py` on the cut pack, every row asserted in `generator/checks.py` (FAM, LAD, R3a,
R3b, OOS, SHR) and the golden recomputed from the bundle by `generator/verify.py`. Children's need in bottles over the
window with six months of June 2027; the order is the adults' 5,051,759 plus the children's need, less 1,376,018 and
1,072,992, to the nearest 5,000. The golden's step holds children's needs from 84,751 to 89,750.

| Rung | Construction | Children's need | Order | Dies to |
|---|---|---|---|---|
| R0 | the children on TLD at the count carried, nobody switching | 51,930 | 2,655,000 | the register: children move onto TLD every month |
| R1 default | each child's line through every weighing reaching 30 kg (36 and 24 months: 63,928, 65,367) | 63,416 | 2,665,000 | out of sample: -71.0, -87.5, -88.4 per cent |
| R1a | the same on 12-month lines, or exponential lines (all weighings, 24, 12 months) | 73,617; 79,356; 72,057; 78,221 | 2,675,000 to 2,680,000 | the same projection to the threshold as R1, every form short of the golden |
| R1b | switch rates by last recorded weight band, half-kilogram and one-kilogram bands | 80,422; 80,032 | 2,685,000 | out of sample: +41.4, +43.3, +26.0 per cent |
| R1c | the band chain (12 and 24 months of transitions) | 72,732; 70,904 | 2,675,000 | the same structure as R1b |
| R1d | the last 3, 6 or 12 months' switches carried, or their trend | 73,651; 70,592; 66,455; 74,986 | 2,670,000 to 2,680,000 | out of sample: -46.6, -25.2, -36.3 per cent (the trend -52.2, -30.4, -35.2 per cent) |
| R1e | age rules: fixed ages 10, 11, 12 with the backlog, the median switch age, ten and over | 55,420 to 200,158 | 2,660,000 to 2,805,000 | the cohort is small for its age: an age carries the wrong children |
| R1f | the last recorded weight at 27, 28 or 29 kg moved at the first visit | 101,715; 77,241; 60,111 | 2,705,000, 2,680,000, 2,665,000 | one reading is one draw: the scatter cuts both ways |
| R1g | each child along the register's median weight-for-age curve from its own level | 100,810 | 2,705,000 | the cohort grows more slowly than the curve |
| R1h | the line moved earlier by the register's median lead of a switch over its line | 97,251 | 2,700,000 | a lead measured on children who crossed is a selected lead |
| R1i | the scatter on 12-month lines, or a weighing at every month | 92,040; 91,334 | 2,695,000 | out of sample: +49.8, +39.3, +30.9 per cent (every month +16.1, +15.2, +13.4 per cent) |
| R1j | the scatter on slopes pooled by sex and year of age (candidates, every paediatric child), the candidates' one mean slope, or random-effects shrinkage | the candidates' one mean slope 83,350; slopes pooled over every paediatric child 84,051 and over the candidates 84,286; random-effects shrinkage 85,113, by sex and year of age 85,390 | 2,685,000 and 2,690,000 | out of sample: -24.0 to -9.2 per cent on every window |
| R2 decisive | each scheduled weighing's chance of reading 30.0 kg or more around the child's own line, the first such reading the switch | 86,858 | 2,690,000 | golden |

**Position and margins.** The golden's unrounded order is 2,689,607, 2,107 bottles inside its step (a
quarter step is 1,250); a one-sigma move of the switch increment, the candidates resampled, is 415 bottles. The
nearest rival outside the step is the scatter with a weighing at every month, 91,334 bottles (2,695,000, 1,583 bottles outside). The default path sits 5 steps below.

**Convergence (C3, asserted, FAM).** Twelve constructions of the decisive step file children's needs from 85,705 to
88,019, every one the golden order and each 750 bottles or more inside it: the threshold at 30.0 or 29.95 kg (the
reading recorded to 0.1 kg); lines through every weighing or the last 36 or 24 months; every scheduled visit weighed
or the register's share; the scatter as the residual SD with or without the fitted parameters' allowance, from
consecutive weighings or from the children near the band (1.22 to 1.31 kg); slopes pooled by age over every child's
weighings; a Monte Carlo of the same model; exit rates over 24 months or pooled over ages. A solver may make two of
those choices at once: the pair that pushes the need furthest up (the 29.95 kg threshold with 24-month lines) files 88,989 and the pair that
pushes it furthest down (24-month exit rates with the residuals' root mean square) 85,568, each 500 bottles or more inside the step. The scatter from the
median absolute deviation over every candidate, pulled down by the infants' smaller scatter, files 85,074, 323
bottles inside. The middle of that span sits at the centre of the step by construction (`pack.place_order`, the third
confirmed lot of the C6 order, a multiple of the 96-bottle carton). The family spans 2,314 bottles, 0.46 of
a step: wider than four tenths of the printed unit because the threshold, the window and the scatter's estimator each
move the need by about a thousand bottles; every single choice and every pair is asserted inside, and only three
upward choices made together reach the step's edge.

**The out-of-sample record (asserted, OOS).** Each route stood at 31 August 2025 over 12 months and at 31 December
2025 and 28 February 2026 over 6 months, on the children in care on a paediatric first line at that date, against the
bottle-months the register shows they took on TLD: the golden +1.7, -1.2, -2.8 per cent; the family's members within a tenth; the
growth line -71.0, -87.5, -88.4 per cent; band rates +41.4, +43.3, +26.0 per cent; the trailing count -46.6, -25.2, -36.3 per cent (the trend -52.2, -30.4, -35.2 per cent); the 12-month lines with scatter
+49.8, +39.3, +30.9 per cent.

**Slopes pooled or shrunk (asserted, SHR).** The register's per-child slopes vary between children by more than their
estimation error (DerSimonian and Laird tau 0.026 kg a month, Q 37,897 on 12,163 degrees of freedom), and every construction
that pools or shrinks them under-forecasts every closed window (-24.0 to -9.2 per cent on every window): the plug-in of a shrunk slope removes the
spread a first passage depends on. On the forecast they file the candidates' one mean slope 83,350; slopes pooled over every paediatric child 84,051 and over the candidates 84,286; random-effects shrinkage 85,113, by sex and year of age 85,390 (2 of 5 in the golden's step); they
take the decisive step and are reported, not counted as the family. The family's own root-mean-square scatter member under-forecasts too (-4.6, -8.3, -9.1 per cent) and stays in the step, while the slopes pooled by age sit 465 to 700 bottles below it, so their exclusion rests on the measured spread of slopes between children more than on the back-test: a residual risk for the judge's Gate C, named here.

**The crossing-age rule (asserted, LAD).** Each child switched on reaching the age at which the register's median
weight for age reaches 30 kg files 2,660,000 to 2,720,000 across 24 binnings (look-back 12 or 24 months, bins of
a quarter, half or whole year, the bin's label or the crossing interpolated, the backlog switched or not); it lands in
the golden's step under 6 of 24, each where the bin label puts the crossing at 11.50 years, never with
the crossing interpolated, and misses every closed window by +88, -47, +32 per cent.

**Strength.** P(one strong solver lands) about 0.25: it must see that the switch is taken on a single weighing whose
scatter is larger than months of growth, model each scheduled weighing's tail around the child's own line, and keep
each child's slope its own; the growth line, band rates and trailing counts are the habitual routes and each files
short, and a solver who back-tests the growth line sees it fail without being told why. P(both land) about 0.06.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | patients on TLD: children under 15 on treatment at the 31 August 2026 count from the register, followed to 30 June 2027 whatever their age; everyone else from the projection | filed (SOP 4.2); SF1, SF2, SF12, SF13 |
| 2 | Unit of account | the 30-tablet bottle, one for each patient on TLD at a month's end | filed (SOP 1.2, 4.1); SF3 |
| 3 | Attribution window | 1 September 2026 to 30 June 2027 | filed (SOP 3.1); SF7 |
| 4 | As-of dating | the count of 31 August 2026; the register and the stock report as pulled on 2 September | filed (SOP 2.1, 2.2; the extract manifest); outcomes entered after the count: same call (R2 asserted) |
| 5 | Version basis | the projection round of September 2026, the stock status report of the count, SOP version 3 | each file carries one version; no superseded cut ships |
| 6 | Denominator | none: the order is a count of bottles | n/a |
| 7 | Weighting | each child counted once in each month on TLD | filed (SOP 4.1) |
| 8 | Window length | the weighings each child's line is fitted to | C3: every weighing since January 2023, the last 36 or 24 months, all in the step (FAM asserted); 12-month lines fall outside and fail out of sample (LAD, OOS asserted) |
| 9 | Boundary inclusivity | 30 kg and over takes TLD; under 15 at the count | filed (Annex 7.2 "30 and over"); a 29.95 kg cut inside the step (FAM asserted); SF1 converges |
| 10 | Rounding path | the unrounded order rounded once to the nearest 5,000 | filed (the prompt); SF9 |
| 11 | Tie-break | none | n/a |
| 12 | Maturity and censoring | exits entered weeks after the last visit; children whose switch the window has not reached | C3: exit rates over 12 or 24 months, by age or pooled, all in the step (FAM asserted); R2 asserted on late-entered outcomes |
| 13 | Order of operations | each month's children on TLD, summed, with six months of June, added to the adults', netted, rounded | filed (SOP 3.1, 3.2, 4.1); SF4 |
| 14 | Row order | sums | C1 |
| 15 | Duplicate resolution | the June 2024 migration month in both layouts; EPR rows re-sent after a failed sync | C1: kept twice or dropped, same call (R2 asserted) |
| 16 | Identity normalisation | legacy ART numbers to the national identifier | the crosswalk; C1: unlinked legacy rows leave the call (R2 asserted) |
| 17 | Netting against gross | usable stock and confirmed shipments | filed (SOP 3.1, 3.3); SF5, SF6, SF8, SF14 |
| 18 | Dimensional units | kilograms to 0.1 (paper sites to 0.5 until May 2024), bottles | the dictionary states each layout's precision; the window's readings are the EPR's 0.1 kg; the 29.95 kg member covers the recording (FAM) |
| 19 | Code and status semantics | regimen codes in both layouts, outcome codes, batch status, lot status | the code list and the dictionary; SF5, SF6, SF10 |
| 20 | Integerisation | whole children in each month's bottles, the order rounded once | the golden mid-step (FAM asserted, a quarter step or more inside) |
| 21 | Clause scope | SOP QP-04 version 3, effective 1 March 2026, governs the September 2026 review | filed (the SOP's header) |
| 22 | Forward window contents | each child's switch month inside the window | forecast from the records (the decisive step); no file covers the window |

## Literal reader

Executing the prompt, SOP QP-04 sections 1 to 4 and Annex 7 word for word gives the order of TLD 30-tablet bottles for
C7: forecast consumption from 1 September 2026 to 30 June 2027, one bottle for each patient on TLD at each month's end,
plus six months of June 2027's consumption, less the usable stock at both warehouses at the 31 August count and the
three lots with a confirmed delivery date, with patients aged 15 and over at the count and new starters from the
projection and the children under 15 at the count with no outcome entered from the register, followed to June 2027
whatever their age, each child moving onto TLD at the visit whose recorded weight is 30 kg or more; no shipped
sentence says when each child's recorded weight will first reach 30 kg, so a literal reader must forecast it from the
register; the easy method on the same literal estimand (each child's growth line reaching 30 kg) files
2,665,000, and the fork table leaves no reading under which a rung is the golden.

## Oracles

- The register's closed windows: every method reads them alike; on the wrong path they supply the band rates and the
  trailing count, and the analyst's own back-test on them rejects the growth line, the band rates, the trailing count
  and pooled or shrunk slopes. No closed window holds a C7 figure.
- The stock status report: stock by batch, lots on order and issues by month, true on every reading; its months of
  stock on the last six months' issues answer another question (the stock's cover) and rank nothing.
- The programme projection: the adults' months, filed; every route reads it alike.
- The ask files' totals: the eLMIS reports and the warehouse documents tie to nothing the call reads.
- No control ties only under the golden.

## Ask sheet

**Main call's declared row population:** the register's visits in both layouts, its patient file, the crosswalk and
the code list; the projection's national row; the stock status report's Stock on hand and On order sheets; SOP
sections 1 to 4 and Annex 7. Device and hazard rows in it: 0 (asserted, SEP: the call's computation opens no ask file,
and the call's files and the ask files are disjoint).

**Ask A. Bottles CMS delivered to each region's ART facilities in C4 and in C5, each facility in its current region,
each delivery dated by when it was signed for** (12 figures, whole bottles).
- H18 home: SOP 5.1, the review's comparison before the order is filed, region by region, of the dispensing facilities
  reported for the last two closed cycles with the deliveries CMS made to them; the table is that comparison, read
  beside the stock the order nets.
- Use: the workbook's region table and the chart.
- Basis (the prompt): the facility's current region; the delivery's signature date.
- Primary A1 (D7, codes reissued to other entities): seven facility codes of sites closed in March 2026 reissued to
  new sites opened in April and May 2026 in other regions; the registry carries both records under each code, the
  closed one with its closure date. Joined to the operational record, the closed sites' C4 and C5 deliveries land in
  the new sites' regions: moves 12 of 12 figures by 204 to 6,648 bottles. Fair: the registry's opening and closure dates and the customer accounts' own
  dates place every delivery (asserted: one record operating in each event's month). Silent: every code joins; the
  repeated code reads as a duplicate the battery resolves to the operational record.
- Primary A2 (D5, delivered only on the face of the record): 67 customer delivery lines whose proof of delivery
  records a refusal at the gate ("Refused: cartons damaged" and three other reasons), the goods back on a return line
  days later; counted as delivered, moves 12 of 12 figures by 888 to 8,844 bottles. Fair: the proof of delivery's signer field and the return lines. Silent:
  each refused delivery has a proof of delivery with a date and is a customer delivery in the warehouse file.
- Hazards: the customer master's delivery region left at the old boundary after April 2026 (moves 12 of 12 figures by 12,924 to 109,224 bottles); posting
  dates one to twelve days before signature (moves 12 of 12 figures by 5,580 to 15,696 bottles); the Northern depot's restocking transfers counted as
  deliveries (Northern's figures rise 591,168 in C4 and 615,840 in C5).
- Stops (built and asserted): S1 the cracker (signature dates, customer deliveries, the operational record, refusals
  counted): all 12 miss; S1a A1 cracked alone: all 12 miss; S1b A2 cracked alone: all 12 miss; S2 both: the golden.
- Span: the deliveries, the proofs of delivery, the customer accounts, the facility registry, the dictionary and the
  manifest (6 files).
- Realism: a facility registry reissues a closed site's code; a warehouse system keeps an account's region as set
  when it was opened; a delivery refused at the gate keeps its delivery note and returns on a return document.

**Ask B. Bottles those facilities reported dispensing in their monthly reports for C4 and for C5** (12 figures, whole
bottles).
- H18 home: the same SOP 5.1 comparison, its dispensing side.
- Use: the workbook's region table and the chart.
- Basis (the prompt): the facility's current region; the reports for the cycle's months.
- Primary B1 (D7, the same reissued codes on the reports' path): joined to the operational record, the closed sites'
  reports land in the new sites' regions: moves 12 of 12 figures by 544 to 5,122 bottles.
- Primary B2 (D5, a category crossed by its code): a partner's emergency donation of TLD in November 2025 at about one
  site in eight in every region, dispensed before CMS stock and reported on its own line (product code ARV0412D, the
  same tablet and bottle) in 153 reports from November 2025 to February 2026; taking the CMS product code
  alone, moves 12 of 12 figures by 765 to 25,432 bottles. Fair: the line's product name is the TLD 30-tablet bottle. Silent: the CMS code is the one every
  other file uses for TLD.
- Hazards: the region stamped on each report at submission (moves 12 of 12 figures by 3,624 to 108,133 bottles); 182 returned submissions, each
  resubmitted and approved (summed, moves 12 of 12 figures by 7,867 to 94,347 bottles); August 2026 reports still awaiting review, outside both cycles.
- Stops (built and asserted): S1 the cracker (approved reports, the operational record, the CMS code): all 12 miss;
  S1a B1 cracked alone: all 12 miss; S1b B2 cracked alone: all 12 miss; S2 both: the golden.
- Span: the eLMIS reports, the facility registry, the dictionary and the manifest (4 files; 7 across both asks).
- Realism: an eLMIS requisition stamps its requisition group's region when submitted; a donated batch is reported on
  its own product line.

**Hazard table.**

| Hazard | Asks moved | Per-ask delta read the easy way |
|---|---|---|
| A1 and B1 reissued codes | A, B | A moves 12 of 12 figures by 204 to 6,648 bottles; B moves 12 of 12 figures by 544 to 5,122 bottles |
| A2 refusals | A | moves 12 of 12 figures by 888 to 8,844 bottles |
| B2 the partner donation | B | moves 12 of 12 figures by 765 to 25,432 bottles |
| the region left at the old boundary | A, B | A moves 12 of 12 figures by 12,924 to 109,224 bottles; B moves 12 of 12 figures by 3,624 to 108,133 bottles |
| posting dates | A | moves 12 of 12 figures by 5,580 to 15,696 bottles |
| depot transfers | A | Northern's figures rise 591,168 in C4 and 615,840 in C5 |
| returned submissions summed | B | moves 12 of 12 figures by 7,867 to 94,347 bottles |

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
donation, and the refusals and the donation together, each cracked). Both devices of one ask cracked keep that ask's 12
(measured), and the pair then reads 42.3.

**Mirror sheet.** The mirror stops at the growth line (2,665,000) and reads each row's own region (the customer
master's for a delivery, the requisition group's for a report), dating deliveries by the proof of delivery as asked:
it keeps none of the 24.

Measured by: `generator/cracker.py` (run on the cut pack by `checks.py` on every build).

Mirror leakage: 0.0 per cent of ask weight (24 ask criteria; the chart carries the same figures).

Pair ceiling: 28.5 (the cracker at 38 + 7 + 55 x 0/24 = 45.0, the mirror at 5 + 7 + 0 = 12.0); both top responses on
the call: 45.0. Criteria supplied: the order, the projection's consumption and maximum stock, the usable stock and the
confirmed shipments (5), the children on TLD and on a first line (2), the table's 24 figures, the chart's two panels
and labels (2) and the two files: 35.

## Leak review

`leak.py --asof 2026-09-02`: REVIEW, no LEAK. Each line:
- Sweep 4, the SOP (register, children, forecast, months, closed, national): 4.2 files the population (the register's
  children under 15 forecast by the Quantification Unit), 3.1 to 3.3 the window, stock and netting, 5.1 the review of
  the last two closed cycles; it names no weighing, scatter, growth line or switch timing; harmless.
- Sweep 4, Annex 7 (register, children, months, national, dosing): the guideline's dosing by the band of the weight
  recorded at the visit, the multi-month dispensing rule and the register's regimen codes; it says nothing about how a
  weighing scatters or when a child will be weighed into a band; harmless (the band rule is the filed WHAT, SF11).
- Sweep 9, the stock status report's dates after 2 September 2026: the lots' due dates and the batches' expiry dates,
  forward by nature; harmless.
- Sweep 9, the EPR encounters' dates after 2 September 2026: the next_appointment column, forward by nature; no visit,
  sync or outcome date passes the pull (REAL asserted); harmless.

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

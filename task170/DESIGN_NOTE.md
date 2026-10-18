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
9. Deliverables: `c7_tld_order.xlsx` (the order, its components and the ask tables) and `transition_forecast.png` (a
   chart on an ask's quantity, never on the order).
10. People, drawn with `guard.py names --locale zu_ZA --seed 170`: Nomalanga Magubane (the CMS quantification lead, the
    SOP and the stock status report), Thabisile Mahlinza (the paediatric ART programme officer, the register extract)
    and Sibongile Sikhosana (the ART programme's monitoring officer, the adult projection), the draw's seventh, fifth
    and tenth names.

**Data-native sentence.** The paediatric register records every child's clinic weighings to 0.1 kg at each scheduled
visit, and a child moves onto TLD at the first weighing that reads 30.0 kg or more; the weighings scatter about 1.3 kg
around each child's own straight growth line while the line of a child from the 2015-16 cohort rises about 0.18 kg a
month, so most of the register's switches came at a single reading over 30 kg months before the child's line reached
it, and in August 2026 about 12,500 children under 15 sit below the band, most of them that cohort at 25 to 28 kg.

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

Design-stage figures from the prototype (`generator/` is not yet cut); stage 2 replaces them with the generator's
built figures and `checks.py` asserts them.

1. Read the SOP: the cycle order is the forecast consumption from 1 September 2026 to 30 June 2027 plus the maximum
   stock level (six months of June 2027's forecast consumption), less the usable stock on hand at the 31 August count
   and the quantities on order with confirmed delivery before 30 June 2027; one bottle for each patient on TLD at the
   end of a month; patients aged 15 and over at the count and every new initiation from the programme's projection,
   children under 15 at the count from the paediatric register.
2. Sum the projection's adult months, take stock on hand and the confirmed shipments from the stock status report.
3. From the register, carry the children on TLD at the count with the register's own retention, and for each child
   below 30 kg fit a growth line to the child's weighings and move the child onto TLD at the first scheduled visit at
   or after the line reaches 30 kg.
4. Add, net, round to the nearest 5,000.

Ends on: an order about 23,000 bottles (four to five steps of 5,000) below the golden, the children's switches
forecast at about 8,400 bottle-months against about 31,600 (prototype).

## Stump sentence

Fitting each child's growth line from the register and moving the child onto TLD when the line reaches 30 kg files a
C7 order about 23,000 bottles short; the step that lands it there is reading the switch off the growth line when the
switch is taken on a single clinic weighing, and the weighings scatter about 1.3 kg around the line while the line
rises about 0.18 kg a month, so most children are first weighed at 30 kg months before their line gets there; the
analyst who carries the register's own switches by recorded weight band, or its recent switch count, also files short,
because those switches came from children who grew faster and the cohort crossing now sits lower in the band.

## Three rules

Task type: utilization-access-demand-forecasting (Healthcare Delivery & Health Economics), which serves Forecasting & Predictive Modeling in the taxonomy; the forecast is a national programme's demand for a medicine over a window not yet open.
Domain test: the deciding quantity is the paediatric regimen-transition demand inside a national ARV quantification, the patient-months on the adult TLD pack of children under 15 who will move into the 30 kg dosing band at their scheduled visits, forecast the way a quantification analyst builds patient transitions: from each child's own weighings, the scatter of a clinic weighing, the visit schedule each child is on and the register's retention.
Swap: "how many megawatt-hours should the utility contract for January to June" keeps a forecast and a window but loses the dosing band applied at a clinic weighing, the visit schedule that decides when a child can be moved, the late-diagnosed cohort that grows slowly into the band and the bottle a patient takes each month, so nothing places a switch months before the growth it reads off.
Layer 1: the register's migration from the legacy system to the national EPR in 2024 (legacy rows with day/month/year dates and free-text regimen lines, EPR rows with ISO dates and national regimen codes, the migration months present in both); facility ART numbers in the legacy rows against the national patient identifier, linked by the crosswalk, a new ART number at each transfer between facilities; drug collections by a caregiver with no weighing; visit rows re-sent by clinic tablets after a failed sync; exits posted weeks after the last visit; the logistics information system's facility reports with resubmitted months and districts reporting tablets; the warehouse stock by batch with quarantined lots and shipments whose dates slip; the programme projection in its own layout. Each is how those systems write their files and none carries the call (asserted neutral, R2).
Layer 2: estimation_fit, the data's real structure: a decision taken on a single scattered reading of each child's growth, so the switch month is the first scheduled weighing that reads 30 kg, forecast from each child's line, the scatter around it and the visit schedule, and validated on the register's closed windows; the choice that flips the call is modelling the weighing rather than the line.
Decisive step: forecast each child's switch as the first scheduled weighing that reads 30 kg or more, each weighing a draw around the child's own growth line at the scatter the register shows, rather than as the month the line reaches 30 kg, the register's switches by recorded band or its recent switch count.
Not semantics: every field is read correctly on the default path (weights to 0.1 kg, regimen codes in both layouts, visit dates, next appointments, the crosswalk, exits, the dosing table, the SOP's terms); reading every one right still leaves the analyst choosing how to forecast when each child is first weighed at 30 kg, and the growth line files about 23,000 bottles short.
Not rule application: the guideline files the dosing band and the SOP files the estimand (the window, the population split, one bottle per patient on TLD at a month's end, the maximum stock level, the netting and the rounding); no filed rule or procedure says when a child will be weighed at 30 kg or how to forecast it, and executing every filed rule on projected growth lines files the short order.
Analyst test: a strong analyst who reads both register layouts, links the children, applies the dosing band and the SOP correctly and moves each child onto TLD when the child's fitted growth line reaches 30 kg files an order about 23,000 bottles short of the golden (to be executed in checks.py on the generator's clean truth); the analyst who carries the register's own switch rates by recorded weight band files about 6,000 short, and only forecasting each scheduled weighing's chance of reading 30 kg files the golden.
Estimand: the CMS quantification SOP files the population (patients on TLD; children under 15 on treatment at the 31 August 2026 count from the paediatric register, followed to 30 June 2027 whatever their age, and everyone else from the programme projection), the outcome (forecast consumption, one 30-tablet bottle for each patient on TLD at the end of a month), the window (1 September 2026 to 30 June 2027, plus the maximum stock level of six months of June's forecast consumption), the netting (usable stock at the count and confirmed deliveries before 30 June 2027) and the unit; the prompt files the rounding (the nearest 5,000 bottles); there is no comparison.
No decoy: no memo, draft, forecast, stakeholder figure or earlier order argues a figure for C7; the stock status report states past stock and issues correctly and ranks nothing; no document describes how children's weights behave or how switches were forecast before.
No certified replay: no shipped figure is reproduced to recover a method; the register's closed windows are the analyst's own out-of-sample record, read alike by every method.
Lesson: a model learns that a transition taken on a single measurement happens at the first reading over the line, not when the underlying path crosses it, so a noisy repeated measurement pulls switches forward by months; that a fitted line's scatter is part of the forecast, not noise to be smoothed away; that transition rates measured on one cohort's position in a band do not carry to a cohort sitting lower in it; and that a forecast is validated on closed windows before it is trusted; no build on file forecasts a first passage of scheduled noisy measurements over a dosing band.

## Tried and rejected
- A national adult forecast left to the solver (consumption trend or the cohort model of the seed): the adult projection's own spread swamps the children's wave, so no estimator family agrees to a step of the order; the adult part is filed as the programme projection.
- The children's growth on reference centile curves (CDC-shaped weight-for-age) as the truth: per-child functional forms fitted to scattered weighings disagreed by more than a step; growth is straight in kg from age six in this world, and the pooled weighings show it.
- A transient dolutegravir supply constraint as the driver: a dated cause whose effect is a step in the switch series, read off the date.
- An adult nowcast of undetected exits filled by multi-month dispensing: the driver of task231 again, and the adult trend is immune to it.
- A report-back device on the call's own rows: banned by the separation line.
- The wave's peak inside the window (the 2015-16 cohort born half a year earlier): every estimator agreed, but the trailing switch count and its linear trend landed inside the golden's step; the cohort was set later so the window holds the rise.
- Twelve-month per-child growth fits as the golden family's member: on scattered weighings their slopes carry so much error that the first passage is overstated by about a sixth in the forecast and by 30 to 50 per cent on every closed window; the family is the fits on each child's whole register history, which the closed windows validate within five per cent.

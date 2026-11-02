# task173: Marlstead and Fennick Hospitals NHS Trust's 2027/28 plan line for emergency admissions with gallstone disease, the year the Wyecross Elective Centre drains the cholecystectomy waiting list (architecture 4)

**Status (2026-11-02).** Architecture 3 (Hollis Bend's water service leaks carried to 2027 through AMI meter exchanges)
is spent at stage 4 on Gate F; its world, decisive step and prompt shell are dead and not re-screened. Architecture 4 is
a new draw at stage 1 in another domain, world and dataset under the same objective and number. Energy Systems &
Utilities was the sheet's domain, but `guard.py check` returned `ban.pairing` (energy x forecasting against task273 v5)
on every Energy probe at this draw, and a ban is redrawn, never waited out (`CLAUDE.md`, a stuck build is unblocked).

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task173.json`, architecture v4 (v1 to v3 in `lineage`, v3 spent at stage 4) |
| Domain / task type | `healthcare-delivery-health-economics`, task type `utilization-access-demand-forecasting` (serves Forecasting): the deciding quantity is the count of emergency admissions with gallstone disease a two-hospital acute trust will have in a plan year, demand that hospital planning forecasts per head of the projected population |
| Objective | Forecasting & Predictive Modeling: emergency gallstone admissions in financial year 2027/28 (1 April 2027 to 31 March 2028), a window not yet open; the records run to 31 October 2026 |
| Shape | `02`, a forecast across periods: the call (the 2027/28 count, nearest 50), the monthly profile by hospital (24 figures, the plan's upload rows), critical components, and the asks (designed at stage 2 in `supplemental-stumping`); about 45 criteria planned |
| Spine | `pas_general_surgery_episodes_2021_2026.csv`, one row per finished consultant episode in general surgery at either hospital, April 2021 to October 2026 (about 130,000 rows), with the monthly admitted PTL snapshots (about 90,000 rows), the theatre case log and the e-referral extract |
| Deliverables | `gallstone_emergency_plan_2027_28.xlsx` (the forecast, its working, the chart, the ask tables) and `gallstone_emergency_profile_2027_28.csv` (the plan's monthly activity rows by hospital, in the ICB upload layout) |
| Decision | `quantity_figure`, answer unit `count`: the planned activity for the 2027/28 non-elective line "emergency admissions, gallstone disease" in the Trust's operational plan, approved by the Trust Board and submitted to NHS England |
| Mechanism | gap time (decisive: the plan year sits after the elective centre drains the list, a list state the record never held, and the list's emergency admissions accrue per month spent waiting) with population (who generates the plan year's emergencies); pattern none; generators G5 (decisive: the need for a cholecystectomy is met electively or surfaces as an emergency, and the plan year meets far more of it electively), G7 (the elective centre's sessions are pinned in the capacity plan), G6 (the emergency population's mix of listed and first-presenting patients shifts); Gate G `forecasting`; strategy `decomposition_attribution` (the emergency series is two components with different drivers, and only the list component follows the plan) |
| Layer 2 family / pattern | `estimation_fit` (a decomposition the data's structure forces); `own:elective-queue-overflow-in-emergency-demand`; the client's utilization card 2 (age-specific rates on the projected population) is the default path's method |
| Furniture | forum `board_of_directors` (the Trust Board approves the operational plan), forcing event `statutory_or_regulatory_filing` (the 2027/28 operational plan submission to NHS England through the ICB), organisation `hospital_or_health_provider`, role `capacity_planner` (head of capacity and demand planning), context artifact `capacity_report` (the 2027/28 elective capacity plan), calibration `none` |
| World | Marlstead and Fennick Hospitals NHS Trust, a fictional English acute trust of two hospitals (Marlstead General Hospital in the city, Fennick Hospital in the market town) serving about 560,000 people across Marlstead and Coldvale districts; Fennick Hospital moved from its own PAS to the Trust EPR in 2023; the Wyecross Elective Centre, four day-case theatres on the Fennick site, opens on 11 January 2027. All fictional; the field's method is real |
| People | `guard.py names --geo uk --seed 173`: Alison Morgan (the planner, the golden workbook's author, in no pack file) and Gordon Wallis drawn; Kirsty Elliott dropped on a `people.last` WARN |

**Guard (registered card, 2026-11-02T02:10:57Z).** `guard.py check` on the registered card: WARN only, no BLOCK.
`overuse.objective`, `overuse.gate_g` and `repeat.gate_g` (task166): the number belongs to the Forecasting lane and the
Gate G mechanism is honestly a forecast. `repeat.decision` (quantity_figure against task166): an operational plan line
is a count, the plan's own unit. The older `test.same_puzzle` and `test.same_driver` signatures (task137 v4, task156
v1, task111 v2, task86 v2) carry a differentiation line each on the card. The deliverable set moved from docx+xlsx
(repeat of task273) and svg+xlsx (repeat of task157) to csv+xlsx, the plan's upload rows beside the workbook; the
shell is read from `prompt.txt` at stage 2 and must differ from architecture 3's (how-many | that | png+xlsx), which
sits in `lineage_shells`. Personas from `guard.py names`; Kirsty Elliott dropped on `people.last` (task453).

**Why this cell.** The held shape in this batch is the field's own method for the deciding quantity at the bottom of the
ladder, filing a wrong answer, with the decisive step the precondition this dataset violates. Hospital demand planning
forecasts emergency admissions per head of population by age and sex (the client's utilization card 2), which takes for
granted that the rate per head does not depend on the hospital's own elective capacity. For gallstone disease it does:
patients waiting for a cholecystectomy are admitted as emergencies while they wait, so part of the emergency series is
the elective list's own overflow, and a plan year that follows a large change in the list breaks the rate per head.

**Data-native sentence.** In this trust the cholecystectomy waiting list has run at about 1,300 patients and a
fifteen-month wait since 2022, and while they wait about one listed patient in forty a month comes back through the
emergency department with biliary colic, cholecystitis, cholangitis or gallstone pancreatitis, so nearly half the
emergency gallstone series is the list's overflow; the Wyecross Elective Centre drains the list in the first half of
2027, before the plan year begins, which a rate per head carried on the population cannot see, and the overflow shows
only when each emergency spell is laid against the PTL snapshot in force on its admission date.

**Abstraction sentence (the test of `stumping` Part 6).** "Part of an outcome series is generated by units waiting in a
second queue at a steady monthly hazard, so the series' rate per head carries the queue at its historical size, and a
plan that drains the queue before the window removes that part." Written against the nearest approved and shipped
drivers it does not describe them: task148 (callers who abandon drain the queue each new caller meets, the waits being
the answer), task137 v4 (demand a capacity-limited service turned away to referrers), task111 v2 (which closed-quarter
cause still operates once a returning provider takes late-day overflow), task156 v1 (a volunteer tier's capacity read
off its shortfall periods) and task134 v2 (inflow from a pool outside the register converting after entry). None has a
queue whose waiting members generate another service's outcome at a hazard per month waited.

**Screen measured before the card** (`scratchpad/t173/proto/w1b.py`, `w1c.py`, `w1d.py`: patient-level monthly
simulation, first presentations at age-sex rates growing 1.8 per cent a year, a list held near 1,300 with a conversion
hazard of 2.4 to 2.5 per cent a month, 40 per cent of converting patients operated in the emergency spell): with the
elective centre opening in January 2027 the age-sex rate route and the linear trend file 1.40 to 1.62 times the
decisive route's expected 2027/28 figure across six seeds, and both back-test within 3 per cent on FY2025/26 in four
seeds of six (up to 11 per cent in two, to be tightened in the generator); with the centre opening in April 2027 the
lever falls to 1.12 to 1.18, and with the day surgery unit closing instead (the list growing) to 1.09 to 1.25 (both in
`## Tried and rejected`). The analyst test runs as code on the generator's clean truth at stage 3.

### Candidate screen (stage 1, 2026-11-02)

Each candidate's default path, swap test, anatomy and bin test; every dead one has its line in `## Tried and rejected`.

| # | Candidate (cell) | Default path ends on | Swap | Anatomy | Bin test | Verdict |
|---|---|---|---|---|---|---|
| A4.1 | Emergency gallstone admissions, the elective centre draining the cholecystectomy list before the plan year (healthcare delivery, utilization forecasting) | age-sex rates on the projected population, about 850, against about 600 | housing repairs read the same structure but have no clinical priority, RTT clock, coded spell or untreated gallbladder | Actor: on the list at admission, a dated join; Link: PTL against spells, no sentence invites; Reflex: the planning method files 850; Back-test: within 3 per cent; Second use: PTL, capacity plan and theatre log each feed an ask; Shock: the list flat 2022 to 2026; Pins: the plan definitions file the WHAT | nearest 50: 850 against 600, lever 1.40 to 1.62 | carded |
| A4.2 | The same cell, the day surgery unit closing March to November 2027 and the list growing | 620 against 670 to 720 | as A4.1 | as A4.1 | lever 1.09 to 1.25: the list's share times its growth bounds it | dead on the bin test |
| A4.3 | The same cell, the elective centre opening in April 2027 | 840 against 700 to 740 | as A4.1 | as A4.1 | lever 1.12 to 1.18: the drain spans the window | dead on the bin test |
| A4.4 | Haemodialysis access-associated bloodstream infections with vascular access surgery delayed (epidemiology, health burden; healthcare delivery) | rates per patient-day, about 70, against about 100 | strong | Reflex fails: the field's surveillance method rates infections by access type and asks for the forward access mix, whose textbook driver is the access surgery queue | lever about 1.4 | dead on readability test 3 |
| A4.5 | Domestic abuse incidents by perpetrators on bail awaiting trial, Crown Court sitting days cut (criminology, recidivism) | the incident trend | moderate | Link holds (police against court records, no key) | bail-period incidents about 15 per cent of the total: lever about 1.1, and the correction is a hazard times bail-days, a linear exposure move | dead on the bin test and linearity |
| A4.6 | Heart-failure outcomes trial events by the cut-off with SGLT2 inhibitor uptake read off the concomitant medication log (biomedical, survival) | the blinded pooled Weibull | strong | the honest label is `composition_mix`, barred by `ban.strategy` against task166 | lever 1.15 to 1.2 | dead on the guard and the bin test |
| A4.7 | Personal-loan defaults with a named plant closure, exposure read from salary-credit narratives (banking, expected credit loss) | the PD bands with the macro overlay | weak (any creditor) | Pins fail: the macro scenario has to name the plant, which sends the solver looking (readability test 1) | large | dead on test 1 and rule 1 |
| A4.8 | Hospital-onset C. difficile with genomic cross-transmission and a single-room building (epidemiology, infectious disease) | rate per bed-day | strong | Reflex fails: single rooms announce cross-transmission, and the single-room effect is a free parameter | about 1.3 | dead on tests 1 and 3 and a fork |
| A4.9 | Energy Systems & Utilities, load forecasting and asset condition (the sheet's domain) | not drawn | | | | barred: `ban.pairing` against task273 v5 on every probe |

## Default path

The pipeline a competent planner builds from the prompt's words and the files' grain, with the field's own method for
emergency demand in it (`stumping` 1.1b; the client's utilization card 2).

1. Read the 2027/28 activity definitions: the line counts hospital provider spells at either hospital with an emergency
   admission method and a first-episode primary diagnosis in the gallstone code list, by admission date.
2. Rebuild spells from the finished consultant episodes, mapping Fennick's pre-2023 PAS numbers through the crosswalk to
   the EPR numbers, normalise the ICD-10 codes, take each spell's first episode, keep the emergency admission methods
   and the code list, and count spells by hospital and month from April 2021 to October 2026.
3. Compute age-sex-specific emergency admission rates per head over FY2024/25 to FY2026/27 to date against the mid-year
   population for the two districts, and back-test the method: the FY2023/24 rates on the FY2024/25 population file
   FY2024/25 within 3 per cent, and the FY2024/25 rates file FY2025/26 within 3 per cent.
4. Apply the rates to the 2022-based projections for mid-2027, phase by the record's month-of-year profile and the
   hospitals' shares, and round.
5. Read the elective capacity plan for the asks: the Wyecross Elective Centre adds general surgery day-case lists from
   January 2027; it is elective capacity and changes nothing in the emergency line.

Ends on: about 850 emergency gallstone admissions for 2027/28 (the measured figure is written here at stage 3).

Golden: about 600: about 470 first presentations (the same age-sex rates, read on the spells of patients not on the
list) and about 130 admissions of patients waiting for a cholecystectomy, at the list's measured monthly rate carried on
the patient-months the capacity plan leaves on the list in 2027/28.

## Stump sentence

A competent planner who rebuilds spells from episodes across the 2023 migration, applies the plan's gallstone code list
and carries the FY2024/25 to FY2026/27 age-sex-specific emergency admission rates on the 2022-based population
projections, a method that back-tests within 3 per cent, files about 850 emergency gallstone admissions for 2027/28;
the step that lands it there is reading the rate per head as one process, when about 45 per cent of the record's
admissions were patients already on the cholecystectomy waiting list, admitted at about 2.4 per cent a month while they
waited, and the Wyecross Elective Centre cuts that list from about 1,300 to about 300 before the plan year begins, so
the plan year carries about 600.

## Three rules

- Task type: healthcare delivery and health economics, utilization, access and demand forecasting
  (`healthcare-delivery-health-economics` / `utilization-access-demand-forecasting`): a hospital's emergency admissions
  for a condition over a plan year not yet begun; it serves Forecasting & Predictive Modeling in the taxonomy.
- Domain test: the deciding quantity is the expected number of emergency admissions with gallstone disease in 2027/28,
  which hospital demand planning forecasts as admission rates per head of the projected population by age and sex; the
  count here is first presentations plus the admissions of patients already listed for a cholecystectomy, whose
  frequency is the natural history of symptomatic gallstones left untreated, so the deciding analysis is clinical
  demand modelling of an elective list's overflow, not a generic count.
- Swap: "how many emergency boiler repairs should a housing association's 2027/28 plan provide for while its kitchen and
  heating renewals clear their backlog" keeps the words and loses the task: there is no elective list with clinical
  priorities and RTT clocks, no spell coded by first-episode diagnosis, no inflamed gallbladder or stone in the bile
  duct that brings an untreated patient back, and no theatre plan counted in lists; the quantity is an emergency
  admission count for a disease and it does not survive the swap.
- Layer 1: the PAS extract is episode-level, a spell carrying several finished consultant episodes (the PAS); Fennick
  Hospital's 2023 move to the Trust EPR leaves two hospital number series and a crosswalk (the migration); ICD-10 codes
  come with and without the dot and with fifth-character and asterisk suffixes (the coding systems); admission methods
  are two-digit codes before the migration and EPR text after it; the PTL is monthly snapshots in which a pathway
  re-listed after a cancellation appears twice (the PTL report); the theatre log stamps local clock time across the
  BST changes (the theatre system); clock starts sit in the e-referral extract, not the PTL (two systems); financial
  years run April to March against mid-year projections. Nothing is placed to be caught.
- Layer 2: estimation that fits the data: the emergency series is the sum of two components with different drivers,
  first presentations, which follow the population, and the waiting list's own conversions, which follow the list, and
  only the second responds to the plan year's elective capacity.
- Decisive step: recognising that the emergency spells include patients already waiting for their cholecystectomy,
  reading each spell against the PTL snapshot in force on its admission date, measuring the listed patients' emergency
  admission hazard per patient-month on the list, and carrying that part on the patient-months the elective capacity
  plan leaves on the list in 2027/28, while the first presentations alone take the rates per head.
- Not semantics: every field, code, unit and definition read correctly (episodes rolled to spells, the migration
  crosswalk applied, the codes normalised, the admission methods mapped, the financial year cut) still leaves the easy
  route on about 850, because no field, code or flag on a spell says the patient was on the waiting list; that is a
  relation between a spell's admission date and a PTL pathway's listing and removal dates in another system.
- Not rule application: no filed rule or procedure performs the step: the activity definitions file what is counted,
  the access policy files the order lists are worked in, the capacity plan files the sessions, and none says anything
  about emergency admissions of listed patients, so executing every stated rule files about 850. The enumerated family
  (age-sex rates over two or three years, a linear trend, seasonal exponential smoothing, rates on the 2018-based or
  2022-based projections, and the list-linked routes with a pooled, priority-specific or wait-banded hazard) spans the
  prototype's 746 to 878 on the rate and trend routes against 528 to 582 on the pooled list-linked route over six seeds;
  the standing family's spread (every route that links the spells to the list and carries the list's planned
  patient-months, under each hazard form and each first-presentation basis) is measured on the generator's clean truth
  at stage 3 and asserted in `generator/checks.py` to sit inside the golden's band of 50; nothing in the record rules the
  easy routes out, because the list held near 1,300 from 2022, so the series never moved with it.
- Analyst test: a strong analyst who rebuilds spells from episodes across the 2023 migration, applies the code list and
  carries the FY2024/25 to FY2026/27 age-sex-specific rates on the 2022-based projections, the planning method that
  back-tests within 3 per cent on FY2024/25 and FY2025/26, files about 850 for 2027/28 (the default path's `Ends on:`),
  against about 600.
- Estimand: the 2027/28 activity definitions (`operational_plan_activity_definitions_2027_28.pdf`, the line "NEL-GS-07
  Emergency admissions, gallstone disease") fix the population (provider spells at Marlstead General Hospital or Fennick
  Hospital, any age, any residence), the outcome (an emergency admission method with the first finished consultant
  episode's primary diagnosis in K80, K81, K83.0 or K85.1), the window (admission date 1 April 2027 to 31 March 2028),
  the unit (a spell, counted once) and the figure planned (the central expectation, not a percentile), and file
  forecasts against the Trust's own capacity plan as written.
- No decoy: nothing is planted to be caught: no copied block of records, no hidden rule, no memo, draft, briefing or
  stakeholder figure carries the wrong answer; the capacity plan is the Trust's real plan and says nothing about
  emergency admissions, and the access policy is the Trust's real policy.
- No certified replay: the method is not hidden and recovered by reproducing certified figures; no published or
  certified emergency figure for the line ships, and the back-test the planner runs is on the record itself.
- Lesson: a model that gets it right learns that a hospital's emergency demand for a condition with an elective cure is
  partly the overflow of its own waiting list, so an emergency forecast has to follow the list's planned size, not the
  population alone; no build on file teaches a queue whose waiting members generate another service's demand.

## Survivor anatomy

- Actor: the deciding property, that an emergency gallstone spell belongs to a patient already listed for a
  cholecystectomy, has no column in any file: it is a relation between the spell's admission date and hospital number
  and a PTL pathway whose listing date precedes it and whose removal date follows it, in a monthly snapshot of another
  system.
- Link: the signal is read through a comparison the field's method never asks for: emergency demand is forecast per head
  of population, and nothing invites laying the emergency spells against the elective PTL; the shared hospital number
  is only usable once Fennick's pre-2023 numbers are crosswalked, and no sentence in any file joins the two.
- Reflex: the field's named method for emergency demand, age-sex-specific admission rates carried on the projected
  population (the NHS planning method; the client's utilization card 2), sits at rung 0 and files about 850; the trend
  and seasonal-smoothing routes at rung 1 file about 840 to 880.
- Back-test: the textbook route validates: the FY2023/24 rates file FY2024/25 within 3 per cent and the FY2024/25 rates
  file FY2025/26 within 3 per cent, because the list held near 1,300 throughout and the series never moved with it.
- Second use: every file the decisive step reads has its own use: the PTL snapshots the RTT asks, the capacity plan the
  elective asks and the plan year's sessions, the theatre log the index cholecystectomy ask and the record of sessions,
  the episodes the default path itself; delete the decisive step and every file stays.
- Shock: the movement the step recovers reads as ordinary: the list's conversions are steady from 2022 to 2026, the
  emergency series is flat with ageing growth, and the elective centre is the plan's own good news for electives; no
  unit appears only in the later period and no statistic sorts to the golden.
- Pins: the WHAT is filed in the Trust's planning genre (the activity definitions for the 2027/28 plan) and the forecast
  basis ("against the Trust's own capacity plan as written"); no filed sentence names the waiting list, a hazard, a
  link or a grouping, and deleting each filed sentence leaves the call forced by the data.

## Tried and rejected

- Lazy abandonment in the 2026 simulation (a customer's patience checked only when an expert came free): it pushed a
  retry before the clock and one expert served two customers at once; abandonment and the queue's close are now events
  in time order, asserted (no event out of order, no overlapping interactions).
- Demand at the 2026 scale of 1.03: the 2026 fortnight served more new cases than the 2027 plan, an implausible fall; the
  2026 scale is 1.00 and the plan grows 3.4 per cent on the CRM's count.
- A graded figure for the fortnight's forecast contacts to the nearest thousand: its constructions spread 400 contacts
  and the golden sat within 100 of a cell edge at every placement the booking allowed; dropped from the prompt, kept in
  the workbook as working.
- Shrinkage at 11 per cent with a handle-time ramp of 0.47: the nearest flat-haircut rival landed the block; the ramp is
  0.455 and shrinkage 12 per cent, every canonical haircut now orders another block.
- Ask B as counts of customers answered after more than three minutes by day: the connect time flips too few customers
  on the quiet days after the deadline, so the cracker landed 2 and 3 May; the daily average wait moves every day by 9
  seconds.
- Crashes drawn per agent-day at a flat rate: some days had none, so the cracker landed them; each day now has at least
  three planned and a blocked one retries later in the shift.
- Hillsborough's Sunday shifts ending at 22:00: one contact ran past 23:00 Eastern, Atlantic midnight, and the invoice
  weeks read in Atlantic and Eastern time split by 0.08 h; Sunday shifts now end by 20:30.
- Frozen sessions all lasting exactly the 90-minute timeout: a uniform organ; team leads now force some out after 10 to
  75 minutes, and the timeout carries the heartbeat's 30 seconds.
- Personal Not Ready of 3 to 8 minutes: put 25 April's billable time on an exact rounding tie (209.05 h); 2 to 9
  minutes, every Ask A figure now clears its tie.
- An invoice header with a street address and an HST registration number: invented details that could match a real
  business; dropped.
- Registering after task165's DRAWN (23bd05a): `guard.py check` on 18 October blocks on the last-three bans on G14,
  `composition_mix` (task165), forum `executive_team` and forcing event `vote_or_meeting` (task247), and beyond them on
  `test.same_puzzle` and `test.same_driver` against task165 in the twelve-build window. Putting G6 first would clear the
  two tests and was rejected as a relabel of a real kinship (both builds carry a conditioned yield to a new mix); stage
  3 is built in scratch and committed without a card, which registers when task165 has left the window.
- Architecture 1 (Ashdale Tax Live's deadline-fortnight outsourcer booking, comebacks set by whoever opened each case) abandoned unregistered on 22 October: the guard's window blocked it for three days on `composition_mix`, G14, `filed_standard`, `executive_team` and `vote_or_meeting` while other lanes kept drawing those axes, and the author chose a fresh draw in a new world rather than wait; nothing of its world, mechanism or blocked axes is carried.
- Redraw cell 1, candidate A (a hospital's ALC census, its patients awaiting long-term care leaving at a fixed weekly placement count set by the region's vacancies, cut after a home closed, while other ALC exits leave in proportion to the stock; default path Little's law on the 12-month ALC stay): measured on the clean truth over 4 seeds (`proto_a2.py`), the textbook rivals bracket the golden instead of missing it on one side (Little on 12-month stays 98 to 128, Little on 13-week stays 150 to 209, occupancy over arrivals 103 to 197, Holt-Winters on the weekly census 112 to 156, against golden 120 to 171), and the golden's own spread from the post-closure placement rate alone is plus or minus 3.5 per cent at one standard error; the closure recency that separates Little's law from the count model is the same dial that starves the post-closure rate, and a census time series is a random walk with drift exactly where the placements are a count. Dead.
- Candidate B (the same placements shared at random across five hospitals' waiting lists, so another hospital's filed rise in designations lengthens every hospital's wait): measured over 3 seeds and two shock sizes (`proto_b.py`), Little on the hospital's own 12-month hazard lands at 32 to 54 against golden 35 to 53, again on both sides, with the golden plus or minus 3 per cent on the pooled placement rate; the spillover moves the level by about 15 per cent, under the 30 per cent the bar needs. Dead.
- Paper screens on the same cell, each killed before a harness: the holiday discharge backlog (the 2026-27 Christmas and New Year run of no-discharge days matches 2025-26 and 2023-24 within a day, so the seasonal naive on aligned dates carries it; `time_semantics` besides); length of stay that shortens with occupancy (the slope's estimator family is open and confounded with season); ED diversion by geography after a neighbour closes (nearest-hospital allocation is the cheap twin of the choice model, one dial); a census capped at staffed beds (the latent demand is either the boarders' count, a population reading, or arrivals times stay, which is the default path itself); new Saturday operating lists (no Saturday surgery in the record, so the weekday discharge model is extrapolated and the family forks); nursing workload from turnover (lever under 10 per cent); float-pool pooling and sickness moving with demand (the empirical daily percentile reaches the golden); a discharge-count cap first binding in the forward peak (the driver of task156, task159 and task172); a transitional unit's 60-day stay limit returning patients (task172's deadline); follow-up echoes of a new-patient surge (task157 and architecture 1's comebacks); nurse retirement at a pension eligibility date (a teachers' plan reads the same, rule 1 fails).
- Redraw cell 2, candidate C1 (a discrete cohort mortality step, the cohorts born 1944 to 1947 carrying 25 per cent excess mortality at every adult age, against Lee-Carter fitted on 1995 to 2025 and a fixed 1.5 per cent improvement; `proto_c.py`, expected values, a fictional country of about 20 million): on the deaths at 75 to 89 in 2027 to 2031, the planning quantity, Lee-Carter files 0.990 of the truth and the fixed improvement 1.012, a one per cent lever, because the step sits on four cohorts among fifteen; it reaches 20 per cent only on the cohort's own ages (83 to 86 in 2030), a quantity no decision funds, and grading it needs the cohort effect separated from age and period, the APC identification fork. Dead on lever.
- Cell 2 paper screens, each dead before code: oldest-old register over-coverage rebuilt by extinct cohorts (already dead twice, task228 candidate 2 and task271's re-root screens, not re-screened); mortality displacement after a severe 2025 winter (one to two per cent of a year's deaths, sized from a handful of past shocks); tempo and recuperation in period fertility, and second births echoing a first-birth surge (task176's paper deaths, not re-screened); depletion of the childless pool after a pulled-forward first-birth wave (about 4 per cent of a year's births, and the time-since-entry family); select mortality in a recently enrolled group (a hazard by time since entry, task468 and task134 v2); exposure bias where adjacent birth cohorts differ sharply in size (a local, sub-per-cent move on any planning total); late registration of inquest deaths at young adult ages (the standard truncation correction, lesson 1 of this round); incomplete death registration estimated by the death distribution methods (a coverage defect, the judge's planted-defect list, as task228 found); the first year deaths exceed births (the difference amplifies the golden family's spread as much as the lever); Lee-Carter's rotation, jump-off and fitting window, and cause-specific forecasting (method forks); a disability-free life table by Sullivan against a multistate projection (prevalence as incidence times duration, cell 1's bracketing death in other nouns); a once-in-sixty-years zodiac dip in births (a single past event).
- Rebuild (2026-10-23), cell `energy-systems-utilities` / `load-forecasting`, paper screens killed before a harness:
  large customers chasing a coincident-peak charge that a 2027 tariff removes (the add-back is the field's known 4CP
  correction and a null region publishes it: the non-alert days are the uncurtailed load); heat build-up over a
  heat wave's days (a lever of 3 to 6 per cent of a peak, and the lag family forks); dual-fuel heat pumps losing gas
  when a gas network is decommissioned (the pre-emption shows in the hybrids' own cold-day load, and the all-electric
  homes publish the answer); rooftop PV export limits raised under a minimum-demand forecast (task136's PV world in the
  same cell, and unclipping a known limit is the reflex); suppressed demand after rotating outages end (the restoration
  rebound is task131's driver); a direct load control programme ending (task131 again, and the non-event days are a
  null region); a district cooling plant with ice storage closing (contrived, one plant); data-centre cooling load by
  design (a visible attribute, stratified by reflex); prepaid metering conversion (stratify by payment type);
  efficiency savings embedded in the trend (about one per cent a year).
- Candidate P1 on code (`proto_p.py`, `proto_p2.py`, 12 seeds): senior plants with separate well and river-lift meters.
  The lever held (the bench wells' fitted energy per curtailed acre-foot carried over filed 1.44 to 2.31 times the
  golden), but each senior well's energy per acre-foot was then one divide of two shipped files (its bills over its
  metered extraction), a single-purpose route to the golden; the wells were moved onto the river lifts' meters, as the
  bottomland plants are built, so the pair has to be fitted (`proto_p3.py`: per-plant fit, pooled fit and the
  separate-plant average within 0.25 GWh of the truth over 16 seeds).
- The decreed allotment against the water actually diverted (the cut is the diversion above a quarter of the
  allotment, not three quarters of the allotment): kept only as a lower rung, because the order files the limit and
  applying it to each right's statements is rule application.
- Architecture 2 (Varner Valley PUD's 2027 Apr-Sep irrigation pumping under the first senior curtailment, bottomland plants a river lift and a well on one meter) spent 2026-10-23 at stage 4 on zip be677673 (Gate F): blind reader A filed 155,000 MWh, the golden, by the path "345 river lift plus well services: energy = a x diverted AF + b x well AF per service (fit 2017-2026) ... Diversion capped at 25 percent of allotment, balance pumped from the service's own well"; reader B filed 130,000 (it read the cap as leaving the land unirrigated). Both readers hit all 56 ask figures: the check meter repeating each revenue meter one interval early was dropped as a duplicate, and the meter clock's missing DST gap gave its standard time away. The judge returned DETERMINISTIC with one FIX_NOW (which meter in each pair is the revenue meter) and warned that the plant strings "RIVER LIFT + WELL" invite the two-source fit. Lessons: a plant description that names both pumps makes the per-service two-regressor fit a reflex, so the decisive quantity was named in the pack; a duplicated series and a clock with a tell-tale gap are visible hygiene and keep nothing.
- Third cell, chosen by this build after architecture 2's Gate F death: `psychology-behavioral-science` / `decision-making-computational-behavioral-modeling` (Forecasting), task177 v1's driver (imposed experiences in a learner) avoided. Why the cell: the field's own quantity, a reference-dependent stopping rule, is read from within-shift choices, no field or string names it, and a pay standard moves every worker's stopping point in a way no shift in the record ran. `guard.py check` on a probe card passes the pairing (its BLOCKs were the probe's own axes, G3 and `capacity_planner` against task169, and the older same-puzzle tests without a differentiation line). Candidate Q1 on code (`proto3/q1.py`, `q1b.py`, scratchpad b173n, 3 and 2 seeds): a food-delivery platform's 19:00 to 23:00 courier-hours after a per-order base fee rise, targeters stopping at the first drop-off past their own day's amount, clock couriers at their planned end. With the base fee from 4.10 to 5.00 (earnings per order up about 11 per cent) and 55 per cent targeters, the late hours fall 8 per cent and the courier-FE elasticity route (minus 0.30, division bias included) files 1.05 times the truth; the lever reaches 32 per cent only with the fee nearly doubled and three quarters of couriers targeting, and the record-only reconstruction of each courier's rule then sits 2 to 3 per cent off the truth. The lever is bounded by the size of the pay change, and the textbook elasticity already moves the right way. Dead.
- Third-cell paper screens and the untouched Forecasting cells beside it, each dead before code: an infectious disease's post-campaign season by the final-size relation (the nonlinearity that makes the lever is the sensitivity: near an effective R of 1.2 a 1 per cent error in R moves the season about 5 per cent, and R and the season-start susceptible share are separately identified only from season-to-season variation, so the golden family spreads past any bin); vaccine effectiveness waning under an earlier campaign (a test-negative record's per-bin effectiveness carries 2 to 3 points of sigma, and campaign timing against waning is the field's open debate a reader raises unprompted); household prophylaxis courses counted per index household (counting households with a case by address is the natural route); stress-test losses convex in unemployment (the logit or probit transform forks, and either is the satellite model's textbook); a percentile of a summed demand under cross-site dependence (resampling whole dates is the natural route); a housing-led small-area projection (net migration regressed on completions, the obvious covariate); a redistricting stripped of incumbents' personal votes (election-polling, excluded by task179's `## Rebuild`); monthly subscribers forced onto annual billing (the per-decision churn hazard does not transfer identified). Infectious disease's two earlier drivers (task179's truncated serial interval, task501's next-generation matrix) were not re-screened.

- Fourth cell, assigned 2026-10-23: `human-factors-ergonomics` / `human-reliability-assessment` (Forecasting), read against task149, task171, task175 and task176's deaths in this task type and task230 v2's driver (detection falling with a shared pool's prevalence), all avoided. Candidate R1 on code (`proto/r1.py`, scratchpad b173h, one seed, 580,000 runs and 15,300 events): a train operator's overspeed events per run rising with the days since the driver last drove that route (route-knowledge decay, truth g = 0.95 + 0.30 ln(1 + days/4)), the December timetable merging two depots' links so every driver signs twelve routes instead of seven. The lever is bounded by the merge: a driver's gap on a route goes from about 6 to about 10 days and about half of all runs are a second or third run of the day at zero recency, so the route-rate default files 0.971 of the truth and the pooled rate 0.981, against a golden family (route by recency bins at three binnings, log-recency fits) at 1.007 to 1.023; the HEART-style binary unfamiliarity split at 14 days lands 1.000. Even a tripled route set with a steep decay moves first runs about 40 per cent and all runs about 20. Dead on the lever, which the size of the roster change caps.
- Candidate R2 on code (`proto/r2.py`, `proto/r2b.py`, three seeds, 596,000 to 599,000 runs): a ten-week blockade of the main line diverting its services over a diversionary route the drivers keep signed but drive only on engineering weekends (every three weeks), the diversion's own base 1.8 times the main line's, truth amplitude 1.2 and decay 25 days; graded the overspeed events on the diverted services (truth 190 to 327). The default (the diversion's historical rate per run) files 1.28 to 1.38 of the truth and the main line's rate 0.53 to 0.58, but the golden family (route by recency bins, three binnings and a coarse one) sits at 1.013 to 1.149 of the truth across seeds (the diversion's base is read from 350 to 680 events, all at long recency, so its own scatter is about 5 per cent), leaving the default only 23 to 26 per cent above the golden; the parametric decay forms spread 0.98 to 1.25 with the likelihood picking the true decay; and the attaining subset, the diversion's own runs at 7 days or less (the second day of a weekend, the return run), files 0.92 to 1.09 of the truth, 4 to 10 per cent from the golden, a filter and a divide once the recency is built. With a three-week analogue closure in the history its rate by week of closure carried the call besides. Dead on the subset screen and the lever.
- Candidate R3 on code (`proto/r3.py`, three seeds, 8,760 shift records and about 1,300 errors in three years): a gas control centre's operator errors as slips per switching operation plus monitoring lapses per console-hour, the forward roster moving four desks on 12-hour shifts to three consolidated desks on 8-hour shifts, the duty cycle unlike the history's. The two single-exposure routes bracket the truth at 1.10 to 1.17 (per operation) and 0.81 to 0.87 (per hour), levers of 13 to 17 per cent, under the 30 the bar needs; with every history shift at 12 hours, a regression on operations leaves its intercept readable per shift (1.13 to 1.21) or per hour (0.93 to 1.05), a form the data cannot settle; with relief shifts of 8 hours in the history the two-exposure fit lands within 4 to 6 per cent, which is the two-regressor fit a medium reader took on architecture 2, and the golden's own scatter is about 4 per cent on that error count. This field's reflex (a human error probability per opportunity) does not split the two, but the data either split them for any regression or not at all. Dead three ways.
- Fourth-cell paper screens, each dead before code: errors by hour of day under a timetable moving work into the night (a stratification on the timestamp, the reflex); handover-related errors under the 12-hour to 8-hour change (the time-on-shift curve inside its observed range, task171's shift death); a workload U-curve at a consolidated desk (the forward load sits outside the record, a form fork); an error taxonomy that types slips and lapses (the split is one group-by, then each type on its natural exposure); a plant-specific HEP updated from a generic prior (a level at a selected unit, the shrinkage law); latent pre-initiator miscalibrations under a surveillance-interval extension (a regression on the interval since the last test, the obvious covariate, and equipment reliability more than human); simulator-derived HEPs for a PSA human failure event (which runs are demands is the estimand's population, the WHAT screen); steps of a procedure lengthened under a new work plan (task176's paper death, the condition in the record or its curve extrapolated). The cell's recurring death: in human reliability the forward condition either moves a performance-shaping factor the record already spans (the attaining subset, or the reflex stratification once the factor is built) or moves it outside the record (a form fork), and the roster or plan changes that are realistic move the factor too little for a 30 per cent lever.

- Rebuild cell 5, chosen by this build shape first on 2026-10-23 (`energy-systems-utilities` /
  `asset-condition-maintenance`), after these directions died on paper in the search: sewer blockages from food
  establishments upstream under a 2027 bypass (grease from restaurants is the field's best-known cause of blockages,
  and the bypass names it); deposit runoff by salary-credit primacy (the field's stable-deposit definition names
  primacy); lapse at the end of a level-term period by premium jump (the post-level-term studies tabulate it); rent
  index lag through the lease stock (the new-tenant rent index is the field's known lead); retirements at unreduced
  eligibility (experience studies tabulate rates by eligibility, and the plan rule is filed); water main breaks after a
  worst-first replacement (a level at selected units, the shrinkage law); fibre take-up by competitor presence (the
  forward areas' defining feature names the covariate); involuntary lapse at card expiry (a calendar-locked trigger,
  task162 by abstraction).
- Architecture 3, stage 3 (2026-10-23), the asks re-sited three times on the cracker script before any reader:
  Item 201 by service centre and quarter (12 figures) left the asks' weight on Items 301 to 305, which a cracker
  reconciling each estimate to its voucher kept whole (16 of 52, pair 37.0), so Item 201 went to months (36); the
  paid revision read one estimate to one voucher fell to that reconciliation, so each fiscal 2026 quarter now has one
  invoice covering two months (one paid at its revision, one as first submitted), and the cracker keeps 0 of 16;
  breaks counted once per main and reported time kept 11 of 36 with nothing to over-clean, so a second break found
  on the same call carries its own crew repair at another location.
- Architecture 3, stage 3, the induced chance per exchange at its first setting (about 1.4 per 100) put the 2027
  forecast near 3,300 with the AMI's added repairs at seven tenths of the base, more than a planner would find
  credible; it was lowered to about 1.0 per 100 (the record's routine exchanges carry about 3 per cent of its
  repairs), which still leaves the record's rate 35 per cent under the expectation.

- Architecture 3 (Hollis Bend Water Utilities' 2027 service leak repairs read on each service's own meter exchange
  visits) spent 2026-10-23 at stage 4 on Gate F (zip c3223db0): blind reader A landed the call at 3,000 by the path
  "About 1 percent of meter sets are followed by a leak repair on the same service within 90 days. I removed that
  effect from history, then fitted seasonality and a linear trend with a February 2021 freeze dummy, giving about
  1,916 organic leaks for 2027. I added about 1,055 meter-exchange leaks from the 108,398 METER EXCHANGE premises on
  the AMI schedule."; the asks held at 11 of 52 (21.2 per cent, one break per main and reported time, the latest
  revision). Reader B and the judge were stopped. Lesson: a shipped file that exists only to carry the forward change
  (here the AMI schedule, whose one use was the decisive step) is joined to the outcome on sight; the forward
  condition has to sit in a file the default path already reads for another reason.


- Architecture 4 draw, Energy Systems & Utilities probes (2026-11-02): `guard.py check` on probe cards for
  `energy-systems-utilities` / `asset-condition-maintenance` and `/ load-forecasting` returned `ban.pairing` (energy x
  forecasting against task273 v5, a live card in the last three) and `ban.subdomain` for load forecasting; task307's
  card registered the same morning carries `architecture_spent`, so it holds no slot and did not move the window. The
  build moved to another client domain under the same objective and number rather than wait for the window.
- A4.2, emergency gallstone admissions with Marlstead's day surgery unit closing March to November 2027 and the
  cholecystectomy list growing (`proto/w1b.py`, four seeds): the trend and age-sex routes file 562 to 646 against an
  expected 2027/28 of 639 to 703, a lever of 1.09 to 1.25, because the list's share of the emergency series (about a
  quarter at a list of 500) times its growth over the window (about half) bounds it; under the 1.2x floor more often
  than not and nowhere near the 1.5 to 2x target. Dead on the bin test.
- A4.3, the same cell with the Wyecross Elective Centre opening in April 2027 (`proto/w1c.py`, four seeds, a list of
  1,300 that is 45 per cent of the emergency series): the expected-value lever is 1.12 to 1.18, because the drain spans
  the plan year and its average list is still about 800. Moving the opening to 11 January 2027 puts most of the drain
  before 1 April and lifts the lever to 1.40 to 1.62 (`proto/w1d.py`, six seeds): carded as A4.1.
- A4.4, haemodialysis access-associated bloodstream infections with vascular access surgery delayed by a surgeon's
  unfilled post: the lever is about 1.4 (catheter days dominate the count at ten to twenty times the fistula rate), but
  the field's surveillance method rates infections by access type and so asks at once for the forward access mix, whose
  textbook driver is the access surgery queue; the decisive step is the reflex's own next line (readability test 3), and
  infections fit neither the utilization task type nor the transmission one cleanly. Dead on paper.
- A4.5, domestic abuse incidents generated by perpetrators on bail awaiting a Crown Court trial whose 2027 sitting days
  are cut: the police-to-court link holds no key, but bail-period incidents are about 15 per cent of a force's domestic
  abuse incidents, a lever of about 1.1, and the correction is a hazard per bail-day times the bail-days, the linear
  exposure move `strategies.md` Part 6 records as landed twice. Dead on paper.
- A4.6, a heart-failure outcomes trial's adjudicated events by the 2027 data cut-off with SGLT2 inhibitor uptake read
  off the concomitant medication log: the honest strategy is `composition_mix` (the at-risk pool's mix on background
  therapy shifts), barred by `ban.strategy` against task166 at this draw, and the lever (a hazard ratio near 0.75 on a
  share moving from a fifth to four fifths) is 1.15 to 1.2. Dead on the guard and the bin test.
- A4.7, a lender's 2027 personal-loan defaults after a named plant closure, exposure read from salary-credit narratives:
  the forward condition has to sit in the macro scenario, which must name the plant and so sends the solver looking
  (readability test 1); the swap reads the same for any creditor of the plant's staff (rule 1), and the honest label is
  population or composition. Dead on paper.
- A4.8, hospital-onset C. difficile after a move to an all-single-room building, cross-transmission read from
  genetically linked isolates whose patients shared a ward: single rooms announce cross-transmission to any infection
  prevention reader (tests 1 and 3), and the single-room effect beyond the record's side rooms is a free parameter (Gate
  C). Dead on paper.

## Retired

**RETIRED 2026-10-22 under this round's rule that a number which dies in its second new cell is retired.** Three
worlds were screened at stage 1 and none held:
- the seed's world (Ashdale Tax Live), architecture 1, built in scratch but never registered, abandoned for a fresh draw
  after three days blocked by the guard's window;
- redraw cell 1, healthcare delivery patient flow (Forecasting): candidates A and B on code, twelve on paper; a
  count-limited exit lands between the textbook routes, not outside them;
- redraw cell 2, sociology and demography life tables (Forecasting): C1 on code, fourteen on paper; national vital
  counts give sigma near one per cent, but every structural judgment the textbook routes take for granted moves a
  planning total by a few per cent, or is a coverage defect, a future-rate assumption or a spent driver.

No card was ever registered, so no guard axis is held. The screens above are the number's record for `guard.py slots`.

## Rebuild (2026-10-23)

Reopened by the author for a from-scratch rebuild under the rule that no number stays retired; architecture 2 drawn
in `energy-systems-utilities` / `load-forecasting` (Forecasting), card v2 registered, `pipeline.json` architecture 2.

Architecture 2 spent at Gate F on be677673 (`## Tried and rejected`). The coordinator then left the next cell to this build under four conditions (a forward window that changes the process in a way not on file, no field or plant string naming the decisive quantity, no ask device that is visible hygiene, every listed cell excluded). Chosen: psychology-behavioral-science / decision-making-computational-behavioral-modeling, for the reason in `## Tried and rejected`; Q1 measured dead on code and eight more directions dead on paper. No card registered for it; v2 stays the card's identity, marked spent. PAUSED at stage 1 for another cell.

Fourth cell (assigned by the main session): human-factors-ergonomics / human-reliability-assessment (Forecasting). R1 (route-knowledge decay under a depot merger), R2 (a blockade's diversion over a route driven only at long recency) and R3 (operator errors per operation against per console-hour under a new duty cycle) measured dead on code, eight more on paper (`## Tried and rejected`). No card registered; v2 stays the card's identity, marked spent. PAUSED at stage 1 for another cell.

Fifth cell (chosen by this build, 2026-10-23): energy-systems-utilities / asset-condition-maintenance (Forecasting),
architecture 3, card v3 registered with v2 moved into `lineage` as spent, `pipeline.json` architecture 3.

Architecture 3 (energy-systems-utilities / asset-condition-maintenance) spent at stage 4 on Gate F on zip c3223db0
(`## Tried and rejected`); card v3 marked `architecture_spent`. PAUSED at stage 1; the next cell comes from the main
session.

## Re-root (2026-11-02)

Architecture 3 spent at stage 4 on Gate F on zip c3223db0 (`## Tried and rejected`); card v3 moved into `lineage` with
its fate and its prompt shell (how-many | that | png+xlsx) into `lineage_shells`. Energy Systems & Utilities was barred
by `ban.pairing` at this draw, so architecture 4 is drawn in `healthcare-delivery-health-economics` /
`utilization-access-demand-forecasting` (Forecasting) in a new world, dataset and shell, card v4 registered, nine
candidates screened across six task types (`## Draw`, candidate screen). Architecture 3's generator, pack, goldens,
prompt, submission, metadata and leak report are removed from the folder at the DRAWN commit (never shipped; git
history keeps them).

# task173: Ashdale Tax Live's 2027 deadline-fortnight booking with Hillsborough Contact Services, when half the experienced bench returns and four new classes fill the rest (architecture 1)

**Status (2026-10-22).** Architecture 1 below (Ashdale Tax Live) is abandoned, never registered: the author chose a fresh
draw. Redraw cell 1 (`healthcare-delivery-health-economics` / `patient-flow-beds-workforce-optimization`, Forecasting, a
fictional health system) was searched and nothing held, and so was redraw cell 2 (`sociology-demography` /
`fertility-mortality-life-table-estimation`, Forecasting); the deaths are the last lines of `## Tried and rejected`.
The number is retired (`## Retired`).

Private, never ships. A new build (wave 8), numbered from seed FC44. The seed was read at its header and Situation only
(`status.py task173`). Its world (a consumer tax-software company's live tax-expert service whose seasonal experts come
back in part each year, with an outsourcer covering the deadline), its decision (the outsourcer's agent hours booked for
the deadline fortnight) and its quantity (the booking in the outsourcer's order blocks, with 150 experts returning against
300 last season and four classes of 60 filling the bench) are kept. The seed's own mechanism is dropped: no table of
contacts per return ships, no routing or planning clause decides the call, and the capacity standard files the estimand
(the fortnight, its load, the capacity per expert and per billed hour, the order blocks) and nothing of the method. The
pitfall is re-found from how the queue works: it offers every contact, a new case or a follow-up, to whichever expert is
free, so whether a case comes back is set by whoever took its first contact, a follow-up comes back at one rate whoever
takes it, and each expert's own share of follow-ups is flat across the bench.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task173.json`, architecture v1; `guard.py check` at filing recorded in `## Guard` below |
| Domain / task type | `business-operations-analytics` (client domain `general-statistics-data-science`), subdomain `workforce-labour-planning`; task type `regression-classification-model-diagnostics` (serves Forecasting): the deciding object is a classification model of whether each case comes back, on who took its first contact and how long they had been on the queue, diagnosed against the contact-level alternative and validated out of sample on five earlier seasons, then carried onto a bench the record never saw |
| Objective | Forecasting & Predictive Modeling: the billed outsourcer hours the 2027 deadline fortnight (19 April to 2 May 2027) will need; every file was pulled by Friday 30 October 2026, the booking goes to the leadership meeting of 2 November and the order is due 15 January 2027 |
| Shape | `other`: the call (whole blocks of 1,000 agent hours) carried by two decoupled checks on the 2026 deadline fortnight, the outsourcer's billable hours in the ACD by day (14 figures) with its invoiced hours the ACD does not support by invoice week (2), and the English queue's average wait by day (14) with each week's share answered within three minutes (2); 32 ask figures, criteria counted in `## Ask sheet` |
| Decision | `quantity_figure`, answer unit `count` (agent hours) |
| Mechanism | gap population (decisive: the 2027 bench's mix of who takes first contacts lies outside every week of the record), with time (the new classes' weeks on the queue in the fortnight); pattern none; generators G14 (the comeback chance conditioned on each opener's group and tenure), G6 (the coming bench's composition far from the record's), G16 (the booking's own agents add the load it carries); Gate G `forecasting`; strategy `composition_mix` |
| Layer 2 family / pattern | `estimation_fit` (each case's comeback modelled on the opener of its first contact, fitted on the 2026 cases, validated on the old seasons, carried to 2027's mix); `own:repeat-load-set-by-the-bench-the-booking-builds` |
| Layer 1 | the CRM in UTC against Eastern planning dates; employee numbers in 2026 against the old ticketing system's agent codes, through the HR history; the old system's two report layouts (hh:mm and minutes, US and ISO dates); both queues in one CRM export; recall answers beyond Confirmed; and on the asks' rows only, the ACD's day-by-day state report, softphone sessions left open to the timeout, the service desk's own logins after lockouts, Atlantic-time invoices and a replacement invoice, re-offered contacts and re-queued video sessions, the video platform's connect time (full inventory in `## Layer 1 inventory`) |
| Furniture | forum `executive_team` (the expert-service leadership meeting of 2 November takes the booking), forcing event `vote_or_meeting` (that meeting, ahead of the outsourcer's 15 January order deadline), organisation family `software_or_platform` (a consumer tax-software company), role family `capacity_planner` (the workforce planning manager), context artifact `filed_standard` (the capacity planning standard), calibration `none`, opening `question-first`, question form `how-many` |
| Spine | the CRM's interaction export for the 2026 filing season, one row per expert interaction on a customer's return case, 199,313 rows over both queues (184,037 on the English queue), with the case number, the interaction type, the handler and the talk and after-contact seconds; constructed in the layout of a CRM interaction export |
| Deliverables | `deadline_fortnight_plan_2027.xlsx` (the booking and its working, the 2026 Hillsborough hours check, the 2026 waits check) |
| People | drawn with `guard.py names --geo Canada --seed 173`: Kimberly Ball (workforce planning manager, owner of the standard; the requester, in no file the prompt names), Mario Barnett (vice-president, expert services), Michelle Russell (training centre lead), Adam Rojas (demand planning analyst), Tammy Gibson (Hillsborough's account manager), James Richards (CRM and ACD administrator), Corey Hughes (finance partner) |
| World | Ashdale Software Inc. (Waterloo, Ontario) sells Ashdale Tax and runs Ashdale Tax Live; Hillsborough Contact Services Ltd. is a contact-centre outsourcer in Moncton, New Brunswick; all fictional, as are the people, systems and data. Searched: no firm named Hillsborough Contact Services, Ashdale Software or Ashdale Tax (the nearest, Ashdale Investments (Holdings) Limited, is a UK holding company); the invoices carry no street address or tax number |

## Guard

The draw waits out bans on its honest keys rather than relabel them: `software_or_platform` while task172 sat in the
last three registrations, `composition_mix` and G14 while task165 does, forum `executive_team` and forcing event
`vote_or_meeting` while task247 does, and the same-puzzle and same-driver tests while task165 sits in the twelve-build
window (below). `guard.py check` and `register` run on the card at the last act of stage 1;
the older-signature BLOCKs the probe raised (task134 v3, task146, task465 v2, task54 on the population and G14 triples)
are cleared only by the differentiation lines on the card, each naming the real difference:
- task134 v3: there a lot's forward yield is its chance of being rebuilt once a permitted option pays; here no unit
  chooses anything, a case comes back by the skill of whoever opened it, and the forward mix of openers is set by the
  bench and by the booking itself.
- task146: there a calendar turn releases refused units at segment rates; here nothing is released or timed, the
  load is the comeback the coming bench's openers generate.
- task465 v2: there a joint count needs a small source's within-cell association; here a comeback chance is fitted
  per opener group and tenure on 230,000 interactions and carried to a new mix.
- task54: there loss per event sits under a rule recovered from closed investigations; here nothing is withheld, the
  comeback depends on the opener and the cases show it.

**Same-puzzle and same-driver tests.** Gap population with G14 and a quantity call: task134 v3, task146, task465 v2,
task54 (above), and task165. The older four clear on the differentiation lines. task165 does not: after its DRAWN
(23bd05a), `guard.py check` blocks `test.same_puzzle` (population, G14, quantity_figure) and `test.same_driver`
(population, G14, forecasting) against it inside the twelve-build window, and the kinship is real, since both builds
carry a yield conditioned on who or what produces it across to a new mix. No line clears that and no generator is
reordered to pass it (G6 first would be a relabel), so the card registers once task165 has left the window.

**Abstraction test.** Stripped of nouns: each first service leaves its requester needing another with a chance set by
how long the server who gave it has been doing the work; the servers share one queue, so every server's share of
repeat work is flat and only linking each request to its first service shows the effect; the coming mix of servers is
far from the record's and partly bought by the decision itself, so the record's repeats per request carried forward
understate the load. Against the driver index the nearest is task140 (a residual struck after a dependent service
whose load rises with the tier being promised): there the dependency is the decision's whole mechanism and its load is
a stated function; here the decisive step is the comeback model by who opened each case, the dependency on the booking
is its second half, and nothing states either.

**Kinship, answered (`guard.py slots` on the driver, and the earlier screens it named).**
- task155 (an open shift's chance of being taken, by adjacency to the member's own schedule): a take-up chance; here a
  comeback chance set by the server of the first contact, on someone else's later contact.
- task156 (a paid tier reached only when a volunteer tier falls short): capacity censored in the record; nothing here is
  censored, the bench's capacity is filed.
- task148 (a queue drained by patience): the 2026 queue abandons, but no figure the call reads turns on patience.
- task149 (a hazard rising with work pace within each unit): a per-unit rate on visible pace; here the opener's tenure
  is visible but its effect is not, because the outcome lands on another server's contact.
- task183 (parts that failed keep failing): the unit's own history; here the server's, not the case's.
- task171, task202, task182 v5, task134 (screens that died on a tenure or cohort effect a solver reads off the schema):
  here the schema-handy read is flat (each group's own contacts are 16 to 17 per cent follow-ups), so the visible
  tenure column does not show the effect; it shows only through the case linkage.
- task140, task127, task253 (fixed points and sized pools): the fixed point here is the booking's own comeback load, the
  second step of the decisive analysis, not its whole.
- task117, task198, task230, task158, task161, task119, task120, task228, task130: word overlaps on capacity and load;
  none forecasts a comeback load by the server of the first contact.

**WHAT screen (stumping 1.2).** The decisive step estimates the filed quantity and settles none of the estimand's five
parts, each filed in the capacity standard (`expert_capacity_planning_standard.docx`): population (the English-queue
cases that open in the fortnight and every follow-up on them, whenever it comes, "Load"), outcome (the billed agent
hours whose handle hours carry the rest of the load at the outsourcer's handle time, "The booking"), window (19 April to
2 May 2027, "The deadline fortnight"), unit (whole blocks of 1,000 agent hours rounded up, "The booking"; Schedule B.5),
comparison (none: a level). The capacity per expert (67.32 handle hours), per billed hour (0.85), the bench (the 150
confirmed, the 240 seats from their go-live dates) and the demand (the plan's 47,169 new cases) are filed too. No
shipped sentence says that a case's comeback depends on who opened it, that a follow-up's own comeback does not, or
that the booking's agents add comebacks of their own.

**Data-native sentence.** Ashdale's queue offers every contact to whichever expert is free, so each expert's own
contacts are 16 to 17 per cent follow-ups whatever their tenure, while a case opened by a returning expert comes back
13.9 per cent of the time, by a first-week class expert 40.6 per cent and by a Hillsborough agent 33.0 per cent; the
2026 fortnight's 1.207 contacts per new case were made by openers 61 per cent experienced, 32 per cent from classes
4 to 16 weeks on the queue (11.8 on average) and 7 per cent Hillsborough's, and the 2027 bench opens 45 per cent of its cases with
classes 1 to 11 weeks in and 22 per cent with Hillsborough's agents, so its cases bring 1.292 contacts each and every
hour booked with Hillsborough opens more cases that come back at its rate.

**Sources read, one line each.**
- Seed FC44 header and Situation: the world, the 150 against 300, the four classes of 60 and the outsourcer; nothing
  else of the seed is kept.
- `guard.py mechanisms --objective forecasting` and `guard.py slots`: the forecasting drivers on file price censored
  clocks, queues with patience, take-ups, composition shifts and dependent residuals; none forecasts a comeback load
  set by the server of the first contact.
- `two-layer-task-design.md`: "the data's real structure"; here the structure is the case, and the contact-level
  reading the schema invites hides the effect.
- `layer2-rigor-patterns.md`, general statistics: model diagnostics before transport; learned, not copied: the
  diagnostic here (a follow-up's own comeback flat across openers and tenure) is what separates the case-level model
  from the contact-level one.
- `strategies.md` F5 (composition): the property (each opener's group and tenure) is rebuilt from the roster, the
  calendar and the case structure, never read off a column, and the coming mix lies outside the record.
- `guide-to-prompt/references/examples.md` 1 (the divisor no sentence names): the decisive quantity is computed by
  default from the wrong grain, here contacts per new case carried as a constant.

## Default path

Every figure below is built by `generator/calc.py` from the shipped pack and asserted in `generator/checks.py`.

1. Read the capacity standard: the fortnight's load is every contact on the cases that open in it; each in-house
   expert gives 90 x 0.88 x 0.85 = 67.32 handle hours, a billed Hillsborough hour 0.85; the outsourcer carries the rest,
   in whole blocks of 1,000 rounded up.
2. Take the bench: the roster's 150 English-queue experts who confirmed the recall, and the training calendar's four
   classes of 60 going live on 15 February, 1 March, 29 March and 12 April 2027.
3. Take the demand plan's 14 fortnight days: 47,169 new expert cases.
4. Take the 2026 fortnight's contacts per new case from the CRM (55,059 English-queue contacts on 45,618 new cases,
   1.207) and multiply: 56,9xx contacts.
5. Take handle time by weeks on the queue from the 2026 CRM (the classes' curve read at each 2027 class's weeks in the
   fortnight, the returning experts' 30.6 minutes, Hillsborough's 35.1), so the bench carries 47,266 contacts; the
   rest at 35.1 minutes over 0.85 handle hours a billed hour is 6,654 hours.

Ends on: 7,000 agent hours.

Golden: 10,000 agent hours.

## Stump sentence

A competent solver carries the 2026 fortnight's 1.207 contacts per new case onto the demand plan's 47,169 cases, gives
the bench its handle time by weeks on the queue and books the rest, 7,000 agent hours; the step that lands it there is
treating comebacks as a property of the season when they are a property of whoever opened each case, so that a 2027
bench opening 45 per cent of its cases with classes 1 to 11 weeks in, and the booked agents' own openings at a third,
bring 1.292 contacts a case, and only the comeback model by opener, carried to the coming mix with the booking's own
openings in it, books 10,000 agent hours.

## Three rules

- **Task type:** `general-statistics-data-science` / `regression-classification-model-diagnostics`, which serves
  Forecasting: the deciding object is a classification model of whether a case comes back, on its opener's group and
  weeks on the queue, checked against the contact-level specification and validated out of sample, then used to
  forecast the 2027 fortnight's load.
- **Domain test:** the quantity that decides the call is the fortnight's forecast load in contacts, which turns on the
  chance each case comes back, modelled the way a statistician specifies and diagnoses a classifier before carrying it
  to a new population: on the opener of the case (not the handler of each contact, which the diagnostic rejects),
  read at the coming bench's mix and fitted out of sample; replacing it with the generic summary (the season's
  contacts per case, or each group's share of follow-ups) moves the call by 3,000 hours.
- **Swap:** "how many megawatt-hours to buy for next winter when half the grid's operators are new" reads as a
  quantity, but a generator's output does not come back for a second service according to who served it first, and
  no booking of extra supply adds load of its own; with hospital beds and new nurses the readmission analogy holds only
  if readmissions were spread at random over the next shift's nurses, which is the property this queue has and the
  swap would have to invent.
- **Layer 1:** each item is how Ashdale's and Hillsborough's systems record a season and none is placed to be caught,
  each asserted neutral on the call in `checks.py` (SF11, SF12, SF5, R2 rows): the CRM in UTC against Eastern dates;
  both queues in one export; employee numbers against old agent codes through the HR history; the old system's two
  layouts; the recall's four answers; and on the asks' rows only, the ACD's state report written day by day, softphone
  sessions left to the timeout, the service desk's logins after lockouts, Atlantic-time invoices and a replacement
  invoice, re-offered contacts and re-queued video sessions, and the video platform's connect time.
- **Layer 2:** `estimation_fit`: the comeback chance of each 2026 case fitted on its opener (returning, Hillsborough, or
  a class expert by weeks on the queue), each follow-up's own comeback at one rate, both checked by diagnostic (a
  follow-up's comeback is flat across openers' groups and tenure, a first contact's is not) and out of sample on the
  2021 to 2025 seasons, carried to the 2027 fortnight's openers with the booking's own agents among them.
- **Decisive step:** recognising that the comeback load is set by who opens each case, measured at case level (the
  first interaction against the case's later ones), so the 2027 bench's far newer mix and the booking's own agents
  raise contacts per case from 1.207 to 1.292, and the booking is the one that carries the load it creates.
- **Not semantics:** every field reads plainly (the case number, the interaction type, the handler, the seconds) and
  reading all of them right still leaves the season's contacts per case or each group's share of follow-ups, both of
  which show no effect of tenure, because the queue spreads follow-ups over whoever is free.
- **Not rule application:** the standard files the load, the capacity and the order and nothing about how comebacks
  arise; executing every stated rule leaves the contacts per case to be estimated, and the natural estimate files the
  default path's figure.
- **Analyst test:** a strong analyst who converts the CRM to Eastern dates, keeps the English queue, maps the roster's
  go-live dates and the calendar's classes, applies the standard's capacity and the demand plan, and carries the 2026
  fortnight's contacts per new case with handle time by weeks on the queue files 7,000 agent hours; one who models
  comebacks by group with the new classes at their 2026 average files 9,000; one who models them by tenure but books
  Hillsborough as pure capacity files 9,000 and at the returning rate 8,000; only the comeback model by opener with the
  booking's own openings in it files 10,000.
- **Estimand:** the capacity standard (`expert_capacity_planning_standard.docx`) fixes the population (the cases that
  open in the fortnight and every follow-up on them whenever it comes), the outcome (the billed hours whose handle
  hours carry the rest of the load at the outsourcer's handle time), the window (19 April to 2 May 2027), the unit
  (whole blocks of 1,000 agent hours rounded up) and the capacity per expert and per billed hour; the demand plan files
  the new cases, the roster and the calendar the bench.
- **No decoy:** nothing is planted to be caught: the 2026 cases are what the queue served, the old seasons are what the
  old system logged, no memo, model, table of contacts per return or stakeholder figure argues for a booking, and no
  record is copied, backfilled or wrong.
- **No certified replay:** the method is not hidden and recovered by reproducing certified figures: nothing certifies a
  comeback rate or a booking, and the old seasons are raw weekly tickets a forecast is tested against.
- **Lesson:** where a queue spreads repeat work over whoever is free, a server's effect on repeats is invisible in its
  own work and shows only by following each request from its first service, so a load forecast for a new mix of
  servers has to be built case by case from who serves first; no build on file teaches a comeback load set by the
  server of the first contact.

## Readability screen

Six tests per rung (1 a filed sentence names it or sends the solver looking, 2 a column, key or marker makes it a row
predicate or a header join, 3 an opponent reflex, 4 a control or corpus scores it, 5 the hygiene battery finds it, 6
one subtraction, ratio or half of a figure).

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 last season's contacts per new case and pooled handle time (5,000) | the standard's handle time | the CRM's seconds | yes, the first rate | the bench's tenure is visible in the roster | no | yes | readable |
| R1 default: last season's contacts per new case, handle time by weeks on queue (7,000) | the standard's load invites a rate | the roster's go-live dates | yes, the careful capacity side | the old seasons' follow-ups per new ticket move with their benches, for an analyst who looks | no | yes, one product | readable |
| R1b each group's own share of follow-ups (7,000) | no | the interaction type by handler | yes, the tenure check | flat across groups, so it confirms R1 | no | yes, a share | readable |
| R2 comebacks by opener's group, the new classes at their 2026 season average (9,000) | no | the case number and type | yes, first contact resolution by group | the old seasons' fortnights miss by the classes' tenure | no | yes, a mean | readable |
| R2c the tenure curve, Hillsborough at the returning rate (8,000) | no | the HCS prefix | a half-step | Hillsborough's own 2026 cases | no | yes | readable |
| R2d the tenure curve, Hillsborough's hours as capacity only (9,000) | the standard's booking reads as capacity | none | yes, book the shortfall | the booked agents' own openings | no | yes | readable |
| R3 (decisive) comebacks by opener, by weeks on the queue, at 2027's mix with the booking's own openings, the booking that carries its own load (10,000) | no shipped sentence says a case's comeback depends on who opened it, or that the booking adds openings | no column holds a comeback flag, a tenure or an opener; the case structure is built from the case number and the start times | no: the reflexes (a season rate, each group's share of follow-ups, first contact resolution by group) land on R1, R1b or R2 | the old seasons score it and score every rival wrong; nothing ties only under it | no: nothing is duplicated, missing or mis-keyed on the call's rows | no: a fitted curve read at four classes' weeks inside a balance solved for the booking | silent |

## Semantic fork table

Every term in the main ask and every convention the main computation needs; every id is asserted in
`generator/checks.py`.

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "agent hours" to book | billed agent hours | handle hours | 9,000 | the standard ("the billed agent hours whose handle hours carry those contacts"); Schedule B bills agent hours |
| SF2 | "the 2027 deadline fortnight" | 19 April to 2 May 2027 | the last two weeks of April | another window | the standard ("For the 2027 season it runs from Monday 19 April to Sunday 2 May 2027") |
| SF3 | the load | every contact on the fortnight's cases, whenever it comes | the contacts that arrive inside the fortnight | same call (60,726 against 60,949 contacts, 9,266 h, asserted) | the standard ("whenever the follow-up comes"); C1 |
| SF4 | "the bench" | the 150 confirmed English-queue experts and the four classes' 240 seats | the French queue, or No response counted in | another bench | the prompt and the standard ("confirmed the recall", "each seat planned as filled") |
| SF5 | handle time | talk plus after-contact work in the CRM | the ACD's accept-to-end time | same call (9,640 h, asserted) | the standard ("the talk time and after-contact work the CRM records"); C1 |
| SF6 | the classes' first contacts | from go-live | from training start | same call: every class is live before the fortnight (asserted) | the standard; the calendar |
| SF7 | capacity per expert | 67.32 handle hours | 90 scheduled hours | another call | the standard ("90 x 0.88 x 0.85 = 67.320") |
| SF8 | rounding | up to the next block of 1,000 | to the nearest block | 9,000 | the standard ("rounded up to the next block"); Schedule B.5 |
| SF9 | the rates' window | the 2026 season | the 2026 fortnight only | same call (9,455 h, asserted) | C1 across windows |
| SF10 | the 12 second-season returners | at the returning rate | at their late-2026 curve | same call (9,436 h, asserted) | C1 |
| SF11 | dates | Eastern | UTC | same call (9,432 h, asserted) | the standard ("Dates and times in this standard are Eastern Time"); C1 |
| SF12 | the queue | English | both queues in the rates | same call (9,453 h, asserted) | the standard's scope; C1 |
| SF13 | Hillsborough's rates | its 2026 agents' own interactions, 13 April to 3 May 2026 | none other exists | same call | the roster's HCS sheet; asserted |
| SF14 | the new cases | the demand plan's 14 fortnight days, 47,169 | finance's Live returns scaled | another demand | the standard ("The fortnight's new cases are the demand plan's daily forecast") |
| SF15 | the seats | 60 a class | the classes' current offers | another bench | the standard ("each seat planned as filled"); the calendar |
| SF16 | comebacks counted | at case level, by the case's opener | each contact's own successor by its handler | same call (contact level 9,677 h; the case counts agree with the rates, asserted) | C1 on the booking; the diagnostic rejects the contact-level form |
| SF17 | handle hours a billed hour | the standard's 0.85 | Hillsborough's realised 2026 fortnight, 2,266 handle hours on 3,216 billable (0.705) | 12,000 | the standard ("Each agent hour billed by the outsourcer gives 0.85 handle hours"): the planning figure is filed, the realised one is the 2026 booking's outcome |

## Ladder

Built figures from `generator/calc.py` on the shipped pack, every row asserted in `generator/checks.py` (LADDER,
RIVALS, FAMILY, SIGMA, FORCED, OOS, SCREEN).

| Rung | Construction | Agent hours | Order | Dies to |
|---|---|---|---|---|
| R0 | last season's contacts per new case, last season's pooled handle time | 4,188 | 5,000 | the classes' handle time and the comebacks |
| R1 default | last season's contacts per new case, handle time by weeks on queue | 6,654 | 7,000 | comebacks are set by who opens each case; the old seasons reject a carried rate |
| R1b | each group's own share of follow-ups carried | 6,545 | 7,000 | as R1: the share is flat because follow-ups go to whoever is free |
| R2 | comebacks by opener's group, the new classes at their 2026 season average | 8,478 | 9,000 | the 2027 classes are far less tenured than the 2026 classes were |
| R2b | the same at the 2026 classes' fortnight rate | 7,826 | 8,000 | as R2, more so |
| R2c | the tenure curve, Hillsborough's openings at the returning rate | 7,814 | 8,000 | Hillsborough's own 2026 cases come back at 33.0 per cent |
| R2d | the tenure curve, Hillsborough's hours as capacity with no openings of their own | 8,380 | 9,000 | the booked agents open cases too |
| R3 decisive | comebacks by opener and weeks on queue at 2027's mix, the booking carrying its own openings | 9,420 | 10,000 | golden |

**Position and margins.** The golden sits above every rival that leaves something out (the nearest below, "new experts
30 per cent slower than returning", 8,768 h, 232 h under the block's edge) and below every rival that piles a haircut
on the carried rate (the nearest above, "30 per cent off new experts' capacity at the returning handle time", 10,279 h,
279 h over it). One iteration of the balance from R2d files 9,328 h, the same block: a solver who adds the booked
agents' openings once has done the decisive step.

**Convergence (C1 on the booking, asserted, FAMILY).** Ten constructions, all ordering 10,000: tenure bands of 1, 2, 3
and 4 weeks (9,304, 9,439, 9,392, 9,547), a logistic in log weeks (9,301), a power law (9,403), the returning rates and
q from the 2026 fortnight only (9,455), the confirmed veterans' own 2026 records (9,427), the contact-level form with
positions pooled (9,677) and the golden (9,420); every one at least 301 h from a block edge.

**One sigma (asserted).** A cluster bootstrap over experts within the returning, class and Hillsborough groups (200
resamples) puts one standard error at 167 h; 9,252 to 9,587 h stays in the block, and 99.5 per cent of the resamples
order 10,000.

**The design forces the model (asserted, FORCED).** A follow-up's own chance of another is flat across openers'
groups (18.0, 17.9 and 20.9 per cent, the largest gap two standard errors on 825 Hillsborough follow-ups) and across the
classes' tenure (16.7 to 18.3 per cent from week 0 to week 30), and inside Hillsborough's own three weeks its agents'
follow-ups come back 20.9 per cent against the bench's 18.3 (z 1.77, the deadline weeks' topics carrying the season gap),
while a first contact's chance differs by 15 standard
errors between groups and falls from 39.3 to 16.8 per cent with tenure; the case-level model is the one the data
supports, and the contact-level form it rejects orders the same block anyway.

**Out of sample (asserted, OOS).** Carried back onto the old ticketing system's weekly reports with each season's own
mix of who took the new tickets, the 2026 fit predicts each season's follow-ups per new ticket within 1.3 per cent
(within 3.6 per cent in each deadline fortnight, 2021 to 2025), while carrying the 2026 fortnight's rate misses by up
to 9.9 per cent (13.0 per cent in a fortnight).

**Screens (stumping 1.2, asserted, SCREEN).** Dispersion: n/a, the deciding quantity is a level. Variance only: the
lever (2,766 h between the default and the golden) is over ten sigma. Common-exposure subset: no 2026 week's
first-contact mix comes within 0.57 (summed absolute shares) of 2027's (33 per cent returning, 45 per cent class
experts, 22 per cent Hillsborough), and no earlier season's follow-ups per new ticket reach 0.230 against 2027's 0.292,
so no filter of the record answers the load by a divide. Truncation: n/a, nothing is censored in the record.

**Strength (adversarial route list, P per strong solver).** The carried rate on any capacity side (R0, R1, R1b, the old
system's rate, 5,000 to 7,000) 0.35; comebacks by group at the 2026 average (R2, R2b, 8,000 to 9,000) 0.12; the tenure
curve with Hillsborough as capacity or at the returning rate (R2c, R2d) 0.10; a flat haircut or uplift on the carried
rate (10, 20 or 30 per cent, 7,000 to 13,000) 0.12, of which a non-canonical value landing 10,000 by coincidence 0.02;
the wrap-up code, the survey or a textbook resolution as the comeback (5,000 to 11,000) 0.05; the comeback model by
opener with the booking's openings, iterated or solved (10,000) 0.10; the contact-level form (10,000) 0.02; anything
else 0.12 (mostly off the call). P(one strong solver lands) about 0.14; P(both land) about 0.04 with the correlation
allowed. The seed is fixed by rule (the task number, then the as-of month and day: 1731030) before any data is
generated and is never searched.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the English-queue cases opening in the fortnight and every follow-up on them | filed (the standard's "Load"); SF3, SF12 |
| 2 | Unit of account | billed agent hours | filed; SF1 |
| 3 | Attribution window | 19 April to 2 May 2027 | filed; SF2 |
| 4 | As-of dating | the files pulled 29 and 30 October 2026; the recall to 23 October | the manifest and the roster; no record after the pull (asserted) |
| 5 | Version basis | the roster's current recall answers; the calendar of 26 October | the roster and the calendar (SF4, SF15) |
| 6 | Denominator | contacts per handle hour by each group's handle time | filed handle time (SF5); C1 |
| 7 | Weighting | contacts weighted by each opener's share of capacity | C1 across constructions (FAMILY) |
| 8 | Window length | the 2026 season's rates against its fortnight's | C1 (SF9) |
| 9 | Boundary inclusivity | the fortnight's first and last days | filed dates; the plan's days sum to 47,169 (asserted) |
| 10 | Rounding path | the booking once, up to the next block | filed (SF8) |
| 11 | Tie-break | none | n/a, one figure |
| 12 | Maturity and censoring | the 2027 cases' follow-ups not yet observed | in the population by the standard's "whenever the follow-up comes"; nothing in the record is censored (the season's late cases close by 31 May) |
| 13 | Order of operations | rates, then the 2027 mix, then the balance | C1 (the balance solved or iterated lands the same block) |
| 14 | Row order | case structure from case number and start time | C1: interactions on a case never share a start (asserted by the case counts in SF16) |
| 15 | Duplicate resolution | none on the call's rows | the realism sweep (no repeated block of CRM rows) |
| 16 | Identity normalisation | employee numbers against old agent codes | the HR history; affects the back-test only |
| 17 | Netting against gross | handle hours net of shrinkage and occupancy | filed (SF7) |
| 18 | Dimensional units | seconds in the CRM, hours in the standard, hh:mm and minutes in the old system | the column names; C1 |
| 19 | Code and status semantics | New case and Follow-up; Confirmed and the other recall answers | the CRM notes and the roster (Layer 1, neutral) |
| 20 | Integerisation | whole blocks | filed (SF8) |
| 21 | Clause scope | the standard covers the English queue's deadline fortnight | filed (SF12) |
| 22 | Forward window contents | the plan's daily new cases; the calendar's classes | the demand plan and the calendar ship as the forward drivers |

## Literal reader

Executing the prompt, the standard, the demand plan, the roster and the calendar word for word gives the billed
Hillsborough hours that carry, at its agents' handle time, the contacts the 150 confirmed experts and the 240 class seats
cannot carry at 67.32 handle hours each, the load being every contact on the 47,169 cases the plan expects from 19 April
to 2 May 2027, rounded up to whole blocks of 1,000; no shipped sentence says how many contacts a case brings, so a
literal reader must estimate it from the 2026 cases, the easy estimates on the same literal estimand (the season's
contacts per case, 7,000; comebacks by group at the 2026 average, 9,000) file other figures, and the fork table leaves no
reading under which a rung is the golden.

## Oracles

- The old ticketing system's weekly reports (2021 to 2025): the evidence for validating any comeback model out of
  sample; on the wrong path they show a season rate moving from season to season, and only a model by opener tracks it.
  They do not tie only under the golden.
- The 2026 CRM's case structure: the evidence every route reads; the carried rate and the model both come from it.
- The demand plan's Basis sheet: the fortnight's new cases by season, an input, not a control.
- The asks' referees (the CRM's conversation start for the waits, the onboarding list and the user list for the logins)
  sit on no row the call reads.
- No control ties only under the golden.

## Ask sheet

**Main call's declared row population:** the CRM's English-queue interactions (the 2026 season), the roster's
English-queue experts and its HCS sheet, the demand plan, the training calendar, the standard, the HR history and the
old ticketing system's English and HCS rows. Device and hazard rows in it: 0 (asserted, SEPARATION: the asks' devices
sit in the ACD exports, the user list, the onboarding list, the invoices, Schedule B and the field guide, none of which
the call reads; the CRM's interactions are read by Ask B through the ACD's CRM Interaction link, row for row as the call
reads them).

**Ask A. For each day of the 2026 deadline fortnight, the billable hours our ACD records show for Hillsborough's agents;
for each invoice week, the hours Hillsborough invoiced that those records do not support, agent by agent** (16 figures,
hours to one decimal).
- H18 home: what the outsourcer actually delivered against what it billed in the period being rebooked; a check read
  beside the booking, decoupled from the call (no row of it enters the call's rates).
- Basis (filed in Schedule B, the contract's voice): billable time is the time an HCS agent is signed in in the
  Available, On Contact or After-Contact Work state as the ACD records it (B.2); the credit is agent by agent, week by
  week (B.4); the invoice weeks run Monday to Sunday (B.3).
- Primary A2 (D1, the same agent's time under two sessions; silent): when a softphone freezes as the agent goes ready,
  the ACD keeps the frozen session Available until its 90-minute timeout or until a team lead forces it out (10 to 75
  minutes), while the agent works on a new session; summed row by row, the overlap counts twice. Every day has at least
  one (asserted); each day's figure moves by 0.2 to 7.2 h, the two weeks' unsupported hours by 14.6 h and 18.2 h. Fair: an agent
  is signed in once at any moment; the union of each agent's billable time reproduces the truth to the second.
- Device A3 (D6, a state's length on every row it covers): the report runs day by day on Eastern dates, so a state open
  at midnight is written on each day with the state's whole length in Duration (s); summed from that column, the
  crossing states count twice. Fair: each row's Start and End give its own part.
- Hazards: HA1 the service desk's logins after four lockouts (ext-...), unmatched to the onboarding list's logins and
  linked by email in the user list; HA2 the replacement week-3 invoice (HCS-26-0478 replaces HCS-26-0446, billed from
  the schedule); HA3 Not Ready reasons (Login, Break, Meal, Personal, No Answer, End of Shift, Team Lead); HA4 Atlantic
  time on the invoices against UTC in the ACD (no billable time after 23:00 Eastern on a Sunday, so the weeks agree,
  asserted); HA5 team leads' sessions in the HCS team.
- Stops (each a complete pipeline in `asks.py`, asserted): the Duration column by the row's start date (every day, 0.35 h
  or more; both weeks); every row's own span summed (the cracker's read, every day 0.2 h or more off, both weeks 14 h or
  more); the onboarding logins only (both weeks, 100 h or more); timed-out sessions dropped whole (every day); Atlantic
  dates (every day); the first week-3 invoice (week 2); the golden. Agent by agent and the week totals converge (no
  agent is invoiced under its records, asserted).
- Span: the agent state detail, the user list, the onboarding list, the invoices, Schedule B, the field guide, the
  manifest (7 files).

**Ask B. For each day, the average wait of the English-queue customers an expert answered; each week's share answered
within three minutes** (16 figures, waits in whole seconds, shares to one decimal).
- H18 home: the service the 2026 deadline fortnight actually gave, read beside a booking the standard says is not sized
  to service level; a measure the call does not turn on.
- Basis (filed in the standard, Service level): a customer's wait runs from the moment they join the expert queue to the
  start of their conversation with an expert, counted on the date they joined; service level is the share of answered
  customers whose wait was three minutes or less. The field guide: Session ID is the customer's session; Answered is
  when the agent accepted the offer. The CRM notes: Started is when the conversation began.
- Primary B5 (D2/D8, the answer time is not the conversation's start; silent, split evidence): the ACD's Answered is
  the expert's accept and the conversation begins when the media connects (6 to 28 seconds on video, 1 to 4 on chat, 0
  to 2 on phone), which only the CRM's Started records, reached through the contact's CRM Interaction; measured to the
  ACD's answer, every day's average is 9.2 to 9.8 seconds short and both weeks' shares 0.3 to 0.4 points high. Fair: the
  CRM's start is linked row for row.
- Device B1 (D8, an anchor on the current row, not the first): an offer the expert does not take is re-offered under the
  same contact with the time it went back in the queue; measured row by row, the wait restarts.
- Device B2 (D7, the customer's key elsewhere): a video session that fails after the accept is queued again as a new
  contact on the same session; measured contact by contact, the customer is counted twice, both times short.
- Hazards: HB1 UTC against Eastern dates of joining; HB2 abandoned customers (not answered, out of both figures); HB3
  customers who abandon and come back are new sessions.
- Stops (asserted): each answered row, queued to answered (every day 10.9 s or more; both weeks); each contact, first
  queued to answered (every day; both weeks); each session, first queued to the first answered row (every day; both
  weeks); each session, first queued to the answered row that reached the CRM (the cracker's read, every day 9.2 s or
  more; both weeks); each answered row's own queue time to the CRM's start (every day 1.3 s or more; both weeks); the
  golden. Every session with an accepted offer reached one conversation (asserted).
- Span: the contact detail, the CRM, the standard, the field guide, the CRM notes (5 files).

**Hazard table.**

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| HA1 service desk logins | MFA lockouts at four sign-ins; new logins under the desk's convention | A weekly | 100 h or more when only onboarding logins are mapped |
| HA2 replacement invoice | the time clock's export was down for week 3 | A weekly | the week of 27 April 17.6 h on the first invoice against 54.7 h |
| HA3 Not Ready reasons | the ACD's states | A | every figure if counted |
| HA4 Atlantic time | Hillsborough's records in Moncton | A | every day if dated in Atlantic time |
| HB1 UTC | the ACD exports UTC | B | the late-evening joins |
| HB2, HB3 abandons and returns | customers leave and come back | B | none under the definitions; counted rows move both figures |

**Referee.** Ask A: the user list's emails against the onboarding list; Ask B: the CRM's Started. Neither hands over a
figure.

**Cracker sheet** (the cracker landed the call, ran the hygiene battery, executed every filed rule and matched every
control; both paths run on the cut pack by `generator/cracker.py`)

| Ask row | Figures | Cracker's path | Device that holds | Verdict |
|---|---|---|---|---|
| Ask A, billable hours by day | 14 | every billable row's own span on its Eastern date, every login in the HCS team, Not Ready excluded | A2 the frozen sessions counted beside the live ones | miss |
| Ask A, unsupported hours by invoice week | 2 | each agent's logins through the onboarding list and the user list's emails, the replacement invoice, Schedule B's credit agent by agent | A2 the frozen sessions read as support | miss |
| Ask B, average wait by day | 14 | each session from its first time in the queue to the accepted offer that reached the CRM | B5 the accept read as the conversation's start | miss |
| Ask B, share within three minutes by week | 2 | the same waits, three minutes or less over answered sessions | B5 | miss |

Blind responses: one constant billable figure for every day recovers at most one of Ask A's days (the days run
68.0 to 393.9 h); one constant wait recovers at most one of Ask B's (33 to 271 s).

Measured by: `generator/cracker.py` (run on the cut pack: each response scored on a rubric modelled on Part 0's weights,
the call and its components 38, the instructions 7, the asks 55 spread evenly over the 32 ask figures).

Mirror leakage: 0.0 per cent of ask weight, measured on the cut pack (the mirror reads the Duration column, the
onboarding logins and each answered row).

Pair ceiling: 28.5 measured on the cut pack (the cracker 45.0, the mirror 12.0); with A2 cracked 42.2, with B5 cracked
42.2, with both 56.0.

## Layer 1 inventory

| Item | System that writes it | File | Natural mishandling | On the call |
|---|---|---|---|---|
| UTC timestamps | the CRM | the interaction export | UTC dates for the season and the tenure | same call (SF11, asserted) |
| both queues in one export | the CRM's saved export | the interaction export | the French queue kept in the rates | same call (SF12, asserted) |
| employee numbers against old agent codes | HR, the old ticketing system | the history, the old reports | the old seasons left unlinked | the back-test only |
| two report layouts (hh:mm and US dates, minutes and ISO dates) | the old ticketing system's 2023 upgrade | the old reports | handle time misread | none: the back-test reads tickets |
| recall answers (Confirmed, Declined, No response, Not invited) | the roster | the roster | No response counted in | the prompt states 150 (SF4) |
| the plan's whole season | Demand Planning | the demand plan | the wrong days summed | the standard's fortnight (SF14) |
| the ACD's day-by-day state report; frozen sessions; desk logins; Atlantic invoices; the replacement invoice | the ACD, Hillsborough | the asks' files | the stops in `## Ask sheet` | none: no row the call reads |
| re-offers, re-queued video sessions, the connect time | the ACD, the video platform | the contact detail, the CRM | the stops in `## Ask sheet` | the connect time sits in the CRM's start and talk, read as filed (SF5, asserted) |

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

# task142: Ironbark Health Alliance, the January to March 2027 Hospital in the Home overflow block (architecture 1)

Private, never ships. A new build (wave 3), numbered from seed FC13. The seed (contract technician visits split across
four data centres for one quarter) was read at its header and Situation only. Its world is not kept: a data-centre
fleet is a compute-capacity world beside task140 (a compute cell's batch guarantee), so the world is drawn fresh in a
client domain no forecasting build has used. Its decision and quantity shape are kept: a capped block of contract
visits placed across sites for one quarter, each site topped up in a filed order to its 90th-percentile visit
requirement above in-house capacity. The pitfall is re-found from how the Hospital in the Home records come to exist:
a nurse visit is one home day of an admitted patient, and the patient stays for as long as the infection's course
runs.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task142.json`, architecture v1, registered 2026-10-15 after `git pull` (task260, task141 and task458 on file); `guard.py check` WARN (repeat.gate_g only, answered below), no BLOCK; `guard.py validate` clean |
| Domain / task type | `healthcare-delivery-health-economics` (client domain, never drawn for forecasting), task type `utilization-access-demand-forecasting` (forecasting): the call rests on each member's 90th-percentile HITH visit requirement for the coming quarter, the planning quantity HITH and bed managers size capacity to, built the way the field builds a period's bed-days, from admissions and their lengths of stay |
| Objective | Forecasting & Predictive Modeling: the distribution of each member's nurse visits from 1 January to 31 March 2027, a window not yet open, around the operating plan's expected visits; the booking is lodged on 6 November 2026 |
| Shape | `05` (allocation to a fixed total): the 850-visit block across five members in lots of 25; criteria from each member's lots and its 90th-percentile requirement (10), the call, the unbooked remainder and the last member reached (3), the two ask tables (30 figures) and the chart's named parts (5), about 48 criteria, arithmetic under `## Ask sheet` |
| Decision | `allocation_to_total`, answer unit `count` (visits booked per member, in lots of 25) |
| Mechanism | gap population (decisive: a visit row is not an independent draw; the quarter's visits are the home days of a random stream of admissions, each staying for its course) then time (the window holds visits from admissions before 1 January, and the stays straddle it); pattern none, generators G2 (what one independent unit of the requirement is), G13 (the window), G6 (the planned mix adds long courses at two members); Gate G `forecasting`; strategy `other` (the dependence structure of a period total, which no listed family names) |
| Layer 2 family / pattern | `estimation_fit` (clustered data: the spread of a total made of multi-day units); `own:quarter-percentile-of-hith-visits-built-from-admissions-and-stays` (nearest library lines: healthcare-delivery-health-economics/utilization-access-demand-forecasting/4, plan capacity to an overdispersed quantile; general-statistics-data-science/resampling-simulation-monte-carlo-methods/1, resample the independent unit) |
| Furniture | forum `operations_desk` (the alliance's HITH program manager lodges the booking with the provider), forcing event `launch_or_rollout` (the bone and joint infection at home pathway opens at Northgate and Westmere on 1 October 2026, so this is the first block that carries it), organisation family `cooperative_or_member_body` (a purchasing alliance of five public health services), role family `programme_officer`, context artifact `capacity_report` (the members' in-house HITH nursing capacity return), calibration `none`, opening `question-first`, question form `how-many` |
| Spine | `hith_census_days_2024-04-01_to_2026-09-30.csv`, the alliance's HITH census warehouse extract: one row per day an admitted HITH patient of a member spent at home, with the day's nurse visits; constructed |
| Deliverables | `hith_overflow_block_2027q1.xlsx` (the booking by member with each member's 90th-percentile requirement, and the two ask tables), `bellbird_weekly_visits_2026q3.png` (an ask chart: the provider's payable visits by week and member, July to September 2026) |
| People | drawn with `guard.py names --geo "Australia" --seed 142`: Joan Rogers (HITH program manager, Ironbark Health Alliance, the requester), Tony Tucker (alliance data officer, the census warehouse and extracts), Dennis McMahon (alliance finance, provider payments), Maureen Phillips (nurse unit manager, Northgate HITH), Miranda Medina (HITH manager, Westmere Health), George Grant (infectious diseases physician, clinical lead of the bone and joint infection at home pathway), Timothy Cardenas (account manager, Bellbird Home Nursing); none appears in the prompt |

**Guard.** `guard.py check` on the registered card: WARN `repeat.gate_g` (Gate G `forecasting` beside task141's), no
BLOCK. Answered: Gate G names where the stump sits (a forecast distribution of a window not yet open), and task141's
mechanism is a selective-labels estimand while this build's is the dependence structure of a period total; the
FINE-numbers mechanism differs though the label is shared. A first draft (a health service's own HITH team booking the
provider) hit four bans against task260 (organisation family `hospital_or_health_provider`, role `procurement_lead`,
forcing event `purchase_order_or_contract`, decisive G16); the decision was moved to the members' purchasing alliance,
whose program manager books the block, and the decisive generator relabelled G2, which is what the step is. People:
Michael (task130) redrawn from the same list.

**Same-puzzle and same-driver tests.** Gap population, decisive G2, decision `allocation_to_total`, Gate G
`forecasting`: no build in the last twelve carries gap, G2 and an allocation together, and none gap, G2 and Gate G
`forecasting` (task257's G2 is a descriptive scale-validation build, method selection). Older allocation builds
(task127, task139) differ on the G-code and the gap.

**Abstraction test.** Stripped of nouns, the driver is: the upper percentile of a period's total is set by how many of
the units that generate it arrive and how long each runs, so it is built from those units and their durations counted
inside the window, and treating the counted rows, or the weeks or months they fall in, as independent draws, or
carrying a site's own past spread onto a planned mix that adds long-running units, understates it. The nearest drivers
on file (`guard.py nearest`): task228 v1 lineage (a false-alarm budget per monitored run over a season, 0.06), task59
v2 (a per-unit yield rebuilt at the filed unit, new episodes capped at the weeks left in the window, 0.06), task123 v2
(a total each unit records over its own reading interval split onto calendar periods, 0.06). None shares the latent
structure: task59's new episodes are capped at the window (a mean) and task123 splits a recorded total across periods
(an allocation of a known amount); here nothing is split or capped, the spread of an unobserved total is what is
estimated. task135 (a portfolio's volatility from daily prices struck at different times) is the nearest variance
build on file: its fix is a return interval long enough to absorb a timing lag between components; here the
dependence comes from the stays themselves, and no choice of interval for the history repairs it, because the history
does not hold the planned mix.

**Data-native sentence.** A member's HITH nurse makes one visit for each day an admitted patient is at home (wound care
every second day), and the patient stays for as long as the infection's course runs, so the alliance's census rows are
the home days of a random stream of admissions whose stays run from two days for a clot to six weeks and more for a
bone and joint infection; the quarter's visits therefore swing with how many long courses happen to start, which no
count of visits, weeks or months treated as independent sees, and two members open the bone and joint infection
pathway on 1 October 2026 with no such course in their own history.

**Sources read, one line each.** `guard.py mechanisms --objective forecasting`: hazards by time since entry (134),
conditional survival (133), selective labels (141), a dependent reservation (140), the forecast-date start state (138),
an intervention's increment at new sites (136), renewal of replaced items (132), a portfolio variance across timing lags
(135): none builds a period total's spread from the units that generate it and their durations. `layer2-rigor-patterns.md`:
utilization-access-demand-forecasting/4 (an overdispersed quantile, shortcut the Poisson margin) is the client's line
for this quantity; this build goes past it, because the field's negative binomial on visit counts, fitted on the
history, is itself one of the rungs. `two-layer-task-design.md`: "the evidence judged with its uncertainty" is the
client's family for this step. The seed's header and Situation (FC13) for the decision and quantity only.

**World.** Ironbark Health Alliance is an incorporated purchasing alliance of five public health services in
Melbourne's north and west (Northgate Health, Riverbend Health, Westmere Health, Kingsdale Health, Hillcrest Health).
Each member runs a Hospital in the Home program: admitted patients treated at home, a member nurse visiting once a day
(wound care patients every second day), the patient staying admitted until the course ends or they return to the ward.
Since July 2024 the alliance has held an overflow agreement with Bellbird Home Nursing, a private home nursing company:
each quarter Bellbird reserves a block of nurse visits for the members' HITH patients the members' own nurses cannot
reach, and the alliance books the block across the members ahead of the quarter. Schedule 2 of the agreement sets the
block for January to March 2027 at 850 visits, booked in lots of 25 in the Schedule's member order, each member taking
the lots that cover the visits by which its 90th-percentile HITH visit requirement for the quarter exceeds its in-house
capacity, until the block is used; the members' 2026-27 operating plans give each member's expected visits by program
stream and month; the capacity return gives each member's in-house visits for the quarter. Riverbend, Kingsdale and
Hillcrest have treated bone and joint infections in HITH for years; Northgate and Westmere open the pathway on 1
October 2026, after the warehouse extract closes on 30 September. The booking is lodged by Friday 6 November 2026.

## Default path

1. Read Schedule 2 (850 visits, lots of 25, the member order, each member topped up to the visits by which its
   90th-percentile requirement for the quarter exceeds its in-house capacity) and the capacity return (each member's
   in-house visits for January to March 2027).
2. From the operating plans, sum each member's planned visits for January, February and March 2027 (every stream) as
   its expected requirement.
3. Take the 90th percentile of the quarter's visits as a Poisson count around that expectation (the expected visits
   plus 1.2816 times their square root, or the Poisson quantile itself).
4. Subtract the in-house capacity, round each shortfall up to lots of 25 and book in the Schedule's order until the
   850 visits run out.

Ends on: Northgate 100 visits, Riverbend 50, Westmere 50, Kingsdale 25, Hillcrest 25, with 600 of the 850 unbooked
(stage 2 design target from the prototype; the generator's figures replace it).
Golden: Northgate 300 visits, Riverbend 225, Westmere 250, Kingsdale 75, Hillcrest none (the block runs out at
Kingsdale; stage 2 design target from the prototype; the generator's figures replace it).

## Stump sentence

A competent solver takes each member's planned January to March 2027 visits as its expected requirement, adds the
90th-percentile margin of a Poisson count, tops each member up above its in-house capacity in Schedule 2's order in
lots of 25 and books Northgate 100 visits, Riverbend 50, Westmere 50, Kingsdale 25 and Hillcrest 25, leaving 600 of
the 850 unbooked (Ends on); the step that lands it there is treating the quarter's visits as independent counts when
they are the home days of admissions whose stays run from a few days to six weeks and more, so the quarter's spread is
the admissions' and their stays': built from the plan's admissions by stream and the stays on file, counted inside the
quarter, Northgate books 300, Riverbend 225, Westmere 250, Kingsdale 75 and Hillcrest none.

## Three rules

- **Task type:** healthcare-delivery-health-economics, utilization-access-demand-forecasting (serves Forecasting): each
  member's HITH visit requirement for January to March 2027, forecast as a distribution around its operating plan and
  read at its 90th percentile, the quantity the alliance's overflow block is booked against.
- **Domain test:** the deciding quantity is a member's 90th-percentile HITH visit requirement for the quarter, the home
  days of a random stream of admissions with stream-specific lengths of stay (days for cellulitis or a clot, weeks for
  a bone and joint infection) counted inside the quarter, the admissions-times-length-of-stay accounting with which
  health services plan bed-days and HITH capacity; the field's estimator is that accounting carried to the plan, not a
  count model of visits.
- **Swap:** "how many contract technician visits should each data centre book, at its 90th-percentile visit
  requirement" keeps a percentile and a block, but a HITH day, an admission that stays until its antibiotic course ends,
  a six-week bone and joint infection course beside a five-day cellulitis course and a wound care patient seen every
  second day have no counterpart there, so what makes the quarter's visits lumpy, and with it the booking, stops making
  sense.
- **Layer 1:** a census warehouse loaded from five members' returns, each member's patient numbers in its own format
  and Westmere's campus code reissued after its 2025 merger with Altona Park; the program streams revised on 1 July 2025,
  earlier days in the old streams (infections in one code, split by principal diagnosis through the alliance crosswalk);
  operating plans by financial year (July to June), one sheet a member with header blocks and footnotes; a course
  interrupted by a ward readmission returned as two episodes under one patient number; episodes still at home on 30
  September 2026 present only to that date; on the ask paths, Bellbird's visit export stamped in UTC by its mobile
  platform, visits re-posted by its app after offline working under fresh visit numbers, referrals resent through the
  alliance portal when the first was not acknowledged. Each is what these systems write; none decides the call (the
  call is unchanged with every ask file removed and with each item mishandled, asserted).
- **Layer 2:** `estimation_fit`: the shortcut puts a count model on visits, or carries the history's spread of weeks,
  months or quarters onto the plan; the expert builds the quarter from its generating units, admissions arriving at
  random and each staying for its course, counted inside the window, which is the only construction that carries the
  planned mix, and the two members opening the bone and joint infection pathway have no such history at all.
- **Decisive step:** build each member's January to March 2027 visit distribution from admissions: the plan's visits by
  stream turned into expected admissions through each stream's mean stay, admissions drawn at random, each given a stay
  from the stream's stays on file (the alliance's bone and joint infection stays for the two pathway members), the visits
  counted that fall between 1 January and 31 March, admissions from October to December included, and the 90th
  percentile read off; this moves Northgate's requirement margin from about 60 visits (Poisson) or about 230 (the
  history's monthly spread) to about 270, and the booking from small lots for all five members to the block running out
  at Kingsdale.
- **Not semantics:** every field, code, unit and definition can be read correctly (the visit, the stream, the plan, the
  in-house capacity, the lot, the order, the window) and the default path reads them all correctly and still books small
  lots across all five members; nothing flips on what a field means, only on how the spread of a total of home days is
  estimated.
- **Not rule application:** Schedule 2 files what is booked (the lots covering the excess of the 90th-percentile
  requirement over in-house capacity, in its order, until the block is used) and the plans file the expected visits; no
  sentence says how the 90th percentile is estimated, that visits come in stays, or that stays must be counted inside
  the window, and executing every filed rule leaves that to the analyst, where the Poisson reflex books 250 of 850.
- **Analyst test:** a strong analyst who reads the agreement, the plans and the capacity return correctly takes each
  member's planned January to March 2027 visits as its mean, adds a Poisson margin and books Northgate 100 visits,
  Riverbend 50, Westmere 50, Kingsdale 25 and Hillcrest 25 with 600 unbooked (Ends on); on the generator's clean truth
  the same route files the same booking, the history's monthly spread files another wrong one, and the admissions-and-stays
  route files the golden (R3a, R3b asserted).
- **Estimand:** Schedule 2, clauses 2.3 to 2.6 (`bellbird_agreement_schedule2_overflow_blocks.pdf`): a member's
  requirement for a quarter is the nurse visits its admitted HITH patients receive on the quarter's days, whoever makes
  them, with patients admitted before the quarter included for their days inside it; its expected value is the
  member's operating-plan visits for the quarter; the member books the lots of 25 that cover the amount by which the
  requirement's 90th percentile exceeds its in-house capacity in the capacity return, in the Schedule's order, until
  the block is used. The population, outcome, window, unit and comparison are filed; the estimator of the percentile is
  not.
- **No decoy:** no memo, briefing, prior booking, scorecard or stakeholder figure states or argues a margin, a
  percentile or a booking; the plans state expected visits only; earlier quarters' bookings are not in the pack; the
  three distractors (the patient experience survey, the 2025-26 declined referrals, Bellbird's 2025-26 service report)
  rank nothing.
- **No certified replay:** no published percentile, past booking, audited requirement or certified figure ships, so the
  estimator cannot be recovered by matching certified numbers; the history's visits are what they are, and no closed
  quarter is graded or reproduced.
- **Lesson:** an upper percentile of a period's total that is made of multi-day stays has the spread of the admissions
  and their stays, so it is built from them and counted inside the window, and a plan that adds long stays changes the
  spread more than its mean; a Poisson margin on the total, or the history's spread of weeks, months or quarters,
  understates it. No build on file teaches the spread of a period total from its generating units (task135 teaches a
  timing lag between priced components, task59 caps new episodes at the window's remaining weeks for a mean).

## Readability screen

To be written at stage 2.

## Semantic fork table

To be written at stage 2.

## Ladder

To be written at stage 2.

## Closure table

To be written at stage 2.

## Literal reader

To be written at stage 2.

## Oracles

To be written at stage 2.

## Ask sheet

To be written at stage 2.

## Tried and rejected

- 2026-10-15, before the card: the seed's world (a storage fleet's contract technician visits across data centres)
  dropped as a compute-capacity world beside task140; only the decision and quantity shape kept.
- 2026-10-15, before the card: a percentile of a quarter's visits as the only decisive step with the members' own
  history as the mean was dropped on paper: with the mean estimated from two or three past first quarters, its own
  error (about 0.4 of the quarter's spread) swamps every margin difference; the operating plan files the expected
  visits so the stump sits in the spread alone.
- 2026-10-15, before the card: the same world with a health service's own HITH team as the decision-maker hit four
  bans against task260 (organisation family, role, forcing event, decisive G16); the decision moved to the alliance.

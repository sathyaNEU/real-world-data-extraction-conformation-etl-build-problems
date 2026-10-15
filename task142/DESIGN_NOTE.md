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
| Shape | `05` (allocation to a fixed total): the 850-visit block across five members in lots of 25; criteria from each member's lots and its 90th-percentile requirement (10), the call, the unbooked remainder and the last member reached (2), the two ask tables (30 figures) and the chart's five Member totals, about 50 criteria, arithmetic in the ask sheet below |
| Decision | `allocation_to_total`, answer unit `count` (visits booked per member, in lots of 25) |
| Mechanism | gap population (decisive: a visit row is not an independent draw; the quarter's visits are the home days of a random stream of admissions, each staying for its course) then time (the window holds visits from admissions before 1 January, and the stays straddle it); pattern none, generators G2 (what one independent unit of the requirement is), G13 (the window), G6 (the planned mix adds long courses at two members); Gate G `forecasting`; strategy `other` (the dependence structure of a period total, which no listed family names) |
| Layer 2 family / pattern | `estimation_fit` (clustered data: the spread of a total made of multi-day units); `own:quarter-percentile-of-hith-visits-built-from-admissions-and-stays` (nearest library lines: healthcare-delivery-health-economics/utilization-access-demand-forecasting/4, plan capacity to an overdispersed quantile; general-statistics-data-science/resampling-simulation-monte-carlo-methods/1, resample the independent unit) |
| Furniture | forum `operations_desk` (the alliance's HITH program manager lodges the booking with the provider), forcing event `launch_or_rollout` (the bone and joint infection at home pathway opens at Northgate and Westmere on 1 October 2026, so this is the first block that carries it), organisation family `cooperative_or_member_body` (a purchasing alliance of five public health services), role family `programme_officer`, context artifact `capacity_report` (the members' in-house HITH nursing capacity return), calibration `none`, opening `question-first`, question form `how-many` |
| Spine | `hith_census_daily_2025-07-01_to_2026-09-30.csv` (32,517 rows), the alliance's HITH census warehouse extract: one row per day an admitted HITH patient of a member spent at home, with the day's nurse visits; beside it `hith_episodes_2024-04-01_to_2026-09-30.csv` (7,703 episodes with admission, separation, mode, stream and diagnosis), the raw material of the decisive step; constructed |
| Deliverables | `hith_overflow_block_2027q1.xlsx` (the booking by member with each member's 90th-percentile requirement, and the two ask tables), `bellbird_weekly_visits_2026q3.png` (an ask chart: the provider's payable visits by pay week and member, July to September 2026, small multiples) |
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
(requirements 2,200, 1,950, 1,600, 1,250 and 1,100 to the nearest 50; generator, asserted R3a).
Golden: Northgate 300 visits, Riverbend 250, Westmere 225, Kingsdale 75, Hillcrest none (the block runs out at
Kingsdale; requirements 2,400, 2,150, 1,800, 1,400 and 1,250 to the nearest 50; generator, asserted).

## Stump sentence

A competent solver takes each member's planned January to March 2027 visits as its expected requirement, adds the
90th-percentile margin of a Poisson count, tops each member up above its in-house capacity in Schedule 2's order in
lots of 25 and books Northgate 100 visits, Riverbend 50, Westmere 50, Kingsdale 25 and Hillcrest 25, leaving 600 of
the 850 unbooked (Ends on); the step that lands it there is treating the quarter's visits as independent counts when
they are the home days of admissions whose stays run from a few days to six weeks and more, so the quarter's spread is
the admissions' and their stays': built from the plan's admissions by stream and the stays on file, counted inside the
quarter, Northgate books 300, Riverbend 250, Westmere 225, Kingsdale 75 and Hillcrest none.

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
  platform with the status codes of two app versions, visits re-posted by its app under fresh visit numbers, and the
  portal outage of 10 to 13 August 2026 (referrals telephoned to Bellbird's intake line, and the patients' first
  visits filed by Bellbird's desk under the Alliance's billing account with the intake log number until it linked the
  files on 14 August). Each is what these systems write; none decides the call (the call is unchanged with every ask
  file removed and with each item mishandled, asserted).
- **Layer 2:** `estimation_fit`: the shortcut puts a count model on visits, or carries the history's spread of weeks,
  months or quarters onto the plan; the expert builds the quarter from its generating units, admissions arriving at
  random and each staying for its course, counted inside the window, which is the only construction that carries the
  planned mix, and the two members opening the bone and joint infection pathway have no such history at all.
- **Decisive step:** build each member's January to March 2027 visit distribution from admissions: the plan's visits by
  stream turned into expected admissions through each stream's mean stay, admissions drawn at random, each given a stay
  from the stream's stays on file (the alliance's bone and joint infection stays for the two pathway members), the visits
  counted that fall between 1 January and 31 March, admissions from October to December included, and the 90th
  percentile read off; this moves Northgate's requirement margin from 59 visits (Poisson), 212 (the history's monthly
  spread) or 176 (an AR(1) on daily visits) to 254, and the booking from small lots for all five members to the block
  running out at Kingsdale.
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
- **Estimand:** Schedule 2, clauses 2.3 to 2.6 (`bellbird_agreement_schedule2_2027q1_block.pdf`): a member's
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

Six tests per rung (`stumping` 2.1): 1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear. A
rung is readable when any test fires.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 plan plus a Poisson margin (the default path) | no | no | yes: a count's 90th percentile as Poisson is the first reflex | no | no | yes: one square root | readable |
| R1 the history's spread of weeks or months, deseasonalised, carried onto the plan (the overdispersion reflex) | no | yes: the census is daily rows, weekly and monthly totals are one group-by | yes | no | no | no | readable |
| R2 the history's quarterly spread, or a negative binomial fitted to quarterly totals, scaled to the plan | no | yes: quarters are one group-by of the episode extract | yes | no | no | yes: one ratio | readable |
| R2b admissions and stays, but each member's own past admissions and own stays (no plan mix, no pooled bone and joint stays) | no | yes: each member's own episodes are one filter; it is the decisive construction on the wrong population, the pathway members having no bone and joint stays of their own | no | no | no | no | readable |
| R2d admissions with stays not varied (each its stream's mean) | no | yes: the episode extract lists every stay, and one stream's stays vary | no | no | no | yes: one mean per stream | readable |
| R2f the quarter's admissions with their whole stays (the cohort) | yes: clause 2.3 counts the visits on the quarter's days, patients admitted before it included | no | no | no | no | no: a compound over stays | readable |
| R3 (decisive) the quarter built from the plan's admissions by stream and the stays on file, counted inside 1 January to 31 March 2027, admissions from the autumn included | no: no sentence says the visits come in stays or how the percentile is estimated | no: no column carries a stay-level spread, a percentile or a margin; the episode extract is the members' routine separations file | no: the reflexes (Poisson, the history's spread, a negative binomial) all land elsewhere | no: no closed quarter, past booking or published percentile ships | no: the battery finds nothing, there is nothing wrong in the files | no: a simulation or a compound over thousands of stays, non-linear in the stays | silent |

## Semantic fork table

Every term of the main ask and every convention the main computation needs, with the golden reading, each
alternative, the call under it, and the shipped sentence that rules it out (or `same call`). Each id is asserted in
`generator/checks.py`.

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "90th-percentile visit requirement" | the number of visits the quarter's requirement stays at or below with probability 0.9 | the 90th percentile of daily or weekly visits times the days or weeks of the quarter | far larger lots, the block gone by Westmere | Schedule 2 clause 2.4: the percentile is of the quarter's requirement, the visits in the quarter taken together |
| SF2 | "requirement" (whose visits) | every nurse visit the member's admitted HITH patients receive on the quarter's days, in-house or Bellbird's | only the visits beyond in-house capacity, or Bellbird's visits only; or visits the treating team orders beyond the schedule added on | the percentile of the wrong total; extra visits: same call | Schedule 2 clause 2.3: "whoever makes them"; visits beyond the schedule (outside the activity returns) at three times the rate Bellbird's records show leave the lots unchanged (asserted) |
| SF3 | the window | visits on 1 January to 31 March 2027, patients admitted before 1 January counted for their days inside it | the visits of admissions made in the quarter, whole stays (the cohort reading), or no patient carried in | one lot over (cohort) or under (no carry-in) at the first three members | Schedule 2 clause 2.3: "on the quarter's days, with patients admitted before the quarter included for their days inside it" |
| SF4 | the expected requirement | the member's operating-plan visits for January to March 2027 (the three months summed) | the history's own level, trended; or the model's own mean | another mean under every rung; the model's mean: same call | Schedule 2 clause 2.5: the expected value is the operating-plan visits; recentring or not gives the same lots (asserted) |
| SF5 | in-house capacity | the capacity return's in-house visits for the quarter | rostered shifts times a planning standard computed afresh, or the plan | same call (the return's figure is that product, stated) | the capacity return, column "in-house visits, January to March 2027" |
| SF6 | lots | the smallest number of lots of 25 whose visits cover the excess (round up) | round to the nearest lot | one lot lower for members whose excess falls in a lot's lower half | Schedule 2 clause 2.6: "the lots of 25 visits that cover" |
| SF7 | a member whose percentile is under its in-house capacity | books nothing | books one lot | same call (no member's 90th percentile is under its capacity under the golden) | Schedule 2 clause 2.6 |
| SF8 | the block running out | members take their lots in the Schedule's order; the member reached when the block cannot cover its lots takes the lots left; later members take none | pro rata across members, or skip to a member whose lots fit | another split at the last two members | Schedule 2 clause 2.7 |
| SF9 | the member order | Northgate, Riverbend, Westmere, Kingsdale, Hillcrest, as listed | an order by size, plan or excess | by size: same call; by excess: another split | Schedule 2 clause 2.2 lists the order for 2026-27 |
| SF10 | which stays describe a stream | the alliance's completed HITH episodes of that stream, every member pooled, the bone and joint pathway members taking the alliance's bone and joint stays | each member's own stays only | the pathway members have no bone and joint stays of their own; per-member stays elsewhere give the same lots (asserted) | the pathway document: "follows the Alliance bone and joint infection protocol", with Riverbend, Kingsdale and Hillcrest's courses already on it |
| SF11 | episodes still at home on 30 September 2026 | out of the stay pool, or completed through a survival estimate | in the pool at their stay to date | same call (asserted: the pool with the open episodes at their stay to date, and completed by Kaplan-Meier, give the same lots) | C1, asserted |
| SF12 | a course interrupted by a ward readmission (two episodes, one patient, under three days apart) | two episodes, as returned | one course | same call (asserted both ways) | C1, asserted |
| SF13 | the stream codes before 1 July 2025 | mapped to the new streams through the crosswalk (infections split by principal diagnosis) | old codes as their own streams, or dropped | same call (asserted: the pooled stays per new stream, built from post-revision episodes only or with the mapped earlier ones, give the same lots; the old heart failure code HF read as a stream of its own, its stays lost, gives the same lots) | C1, asserted |
| SF14 | the requirement's rounding in the deliverable | the 90th percentile rounded to the nearest 50 visits | to the nearest visit or 25 | graded at 50 only | the prompt's last sentence |

## Ladder

Every figure from the generator (`calc.rivals`, `calc.family`), asserted by name in `checks.py` and recomputed by
`verify.py` for the golden and the default path. Lots of 25; the block 850 visits (34 lots); order Northgate,
Riverbend, Westmere, Kingsdale, Hillcrest. Margins are the 90th percentile less the plan's expected visits (2,143,
1,905, 1,570, 1,209, 1,064); in-house visits 2,112, 1,911, 1,589, 1,246, 1,086.

| Rung | Construction | NG | RB | WM | KD | HC | Booking (NG/RB/WM/KD/HC, visits) | Dies to |
|---|---|---|---|---|---|---|---|---|
| R0 | plan plus the Poisson margin (exact Poisson or normal) | 59 | 56 | 51 | 45 | 42 | 100/50/50/25/25, 600 unbooked | the visits are home days of stays, not independent events: the history's own spread is several times a Poisson spread at every member |
| R0b | daily visits as independent days, scaled to the quarter | 77 | 48 | 66 | 41 | 57 | 125/50/50/25/50, 550 unbooked | a stay runs across days |
| R1 | the history's monthly spread (raw; a negative binomial on months gives the same lots) | 212 | 217 | 167 | 144 | 200 | 250/225/150/125/100, the block reaches Hillcrest | a stay runs across months, so months are not independent; and the history has neither the bone and joint pathway nor the planned mix |
| R1b | the monthly spread deseasonalised | 159 | 170 | 133 | 98 | 169 | 200/175/125/75/150, 125 unbooked | the same |
| R1c | the history's weekly spread | 157 | 128 | 133 | 93 | 124 | 200/125/125/75/125, 200 unbooked | the same, more so |
| R1d | an AR(1) with trend on daily visits since July 2024, the quarter's forecast-error spread scaled to the plan | 176 | 153 | 146 | 110 | 144 | 225/150/150/75/125, 125 unbooked | the autocorrelation is the history's, under the history's mix: no bone and joint course at Northgate or Westmere |
| R2 | the history's quarterly spread scaled to the plan | 189 | 309 | 171 | 202 | 244 | 225/325/175/125/0 | ten quarters, four seasons, a growing program and a different mix: no quarter on file is a draw of the planned quarter |
| R2b | admissions and stays on each member's own past rates and stays | 122 | 247 | 96 | 199 | 169 | 175/250/100/175/150 | the plan files the 2026-27 admissions, with the pathway; Northgate and Westmere have no bone and joint stays of their own |
| R2c | the plan's admissions, admissions fixed at the plan (stays random) | 97 | 91 | 87 | 73 | 67 | 150/100/75/50/50, 425 unbooked | admissions arrive at random (daily admissions on file have a variance-to-mean ratio of 0.96 around each month's mean) |
| R2d | the plan's admissions, each given its stream's mean stay | 236 | 225 | 212 | 180 | 169 | 275/225/200/150/0 | stays vary (a bone and joint course runs from two to thirteen weeks): one lot short at the first three |
| R2e | the quarter's admissions only, no patient carried in from the autumn | 232 | 223 | 208 | 179 | 169 | 275/225/200/150/0 | clause 2.3 counts patients admitted before the quarter for their days inside it |
| R2f | the quarter's admissions with their whole stays (the cohort; exact or normal) | 275 | 262 | 249 | 210 | 199 | 325/275/250/0/0 | clause 2.3 counts the visits on the quarter's days: one lot over at the first three |
| R3 (decisive) | plan admissions by stream from October 2026, the alliance's stays, visits counted on 1 January to 31 March 2027, exact compound distribution | 254 | 243 | 228 | 194 | 183 | 300/250/225/75/0, the block out at Kingsdale | (the golden) |

- **Position and margins.** The call is an allocation, graded on each member's lots: R0 books at most four lots
  anywhere and leaves most of the block; R1 to R2 book every member or reach Hillcrest in other lots; R3 books the first
  three members in full, Kingsdale the 3 lots left of its 7 and Hillcrest nothing. Every rung's booking differs from
  R3's at four or five members and at one of the first three (asserted per rung). The near rivals R2d and R2e sit one lot
  under the golden at Northgate, Riverbend and Westmere, R2f one lot over (asserted).
- **Dominance.** The decisive correction moves Northgate's margin by 195 visits from R0, 42 from R1, 95 from R1b and 78
  from R1d, against the golden family's spread (at most 8 visits at the first three members across thirteen admissible
  constructions: stays pools of 12 to 27 months, open episodes at their stay to date or completed by Kaplan-Meier, a
  course split by a ward return joined, per-member stays, recentred or not, admissions from 1 September, the normal
  approximation, a 20,000-quarter simulation), all asserted.
- **Grid.** The golden's excess sits 7 to 12 visits inside its lot at every member; every admissible construction stays
  at least 5.5 visits inside the same lots, and five 20,000-quarter simulations with different seeds book the golden
  (asserted). Every cell outside the family names another booking or is ruled out by a quoted clause (SF3, SF6 to SF9).
- **Worth.** Graded quantities are lots (counts) and requirements to the nearest 50 (each 21 to 24 visits inside its
  50-visit bin), never intermediates (`stumping` Part 3).

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | every admitted HITH patient of the member with a day at home inside the quarter, including patients admitted before it; unobserved (future) admissions are in it | filed (Schedule 2 clause 2.3); the plan carries the future admissions |
| 2 | Unit of account | nurse visits | filed (clause 2.3); lots of 25 visits (clause 2.6) |
| 3 | Attribution window | the quarter's days, 1 January to 31 March 2027 | filed (clause 2.3), SF3 |
| 4 | As-of dating | the plans as approved for 2026-27, the capacity return of October 2026, stays from the extract of 30 September 2026 | each file's own date; nothing re-dated |
| 5 | Version basis | the 2026-27 plans and the October capacity return, the only versions shipped | one version each |
| 6 | Denominator | none (a percentile of a count) | n/a, stated |
| 7 | Weighting | none | n/a |
| 8 | Window length | the stays pool: completed episodes admitted 1 April 2024 to 30 June 2026 | C1: every window from 12 to 27 months of admissions gives the same lots (asserted) |
| 9 | Boundary inclusivity | 1 January and 31 March both inside | filed ("the quarter's days") |
| 10 | Rounding path | the percentile computed unrounded, the excess rounded up to lots once, the requirement shown rounded to 50 | filed (clause 2.6 and the prompt); asserted one arithmetic with the golden |
| 11 | Tie-break | none arises (no excess on a lot boundary; the order is listed) | asserted every excess at least 7 visits from a lot boundary |
| 12 | Maturity and censoring | stays still open on 30 September 2026 | C1 (SF11, asserted) |
| 13 | Order of operations | percentile first, then the excess over capacity, then lots, then the block in order | filed (clauses 2.4 to 2.7) |
| 14 | Row order | none matters | C1, asserted over shuffled rows |
| 15 | Duplicate resolution | none in the call's files (the census and episode extract reconcile) | asserted no duplicate episode or census day |
| 16 | Identity normalisation | patient numbers in five formats, Westmere's reissued campus code | the call needs stays by stream only; asserted the stays pool identical with any patient-number normalisation, and the same lots with Westmere's retired campus codes dropped |
| 17 | Netting against gross | none (visits are not netted against anything) | n/a |
| 18 | Dimensional units | visits throughout; wound care visits every second day and heart failure's two early double days are visits, not days | filed (the visit schedule in the program streams document and the dictionary); asserted |
| 19 | Code and status semantics | stream codes, old and new; separation modes | dictionary semantics; SF13 |
| 20 | Integerisation | whole lots, rounded up | filed (clause 2.6) |
| 21 | Clause scope | Schedule 2 governs the January to March 2027 block only | filed in its title |
| 22 | Forward window contents | admissions from 1 October 2026 to 31 March 2027 under the plan | the plan's months July 2026 to June 2027 cover the span; admissions before 1 October 2026 add no visit inside the quarter (longest stay on file 92 days); starting from 1 September gives the same lots (asserted) |

## Literal reader

Executing the prompt and Schedule 2 word for word (the requirement is the visits on the quarter's days, its expected
value the plan, the 90th percentile of that requirement, the excess over the capacity return's figure rounded up to
lots of 25, members in the listed order until 850 are used) fixes every term but the estimator of the percentile; every
reading of every term converges on the golden or violates a quoted clause (SF1 to SF14), and the easy answer comes
from an easy estimator on the same literal estimand (a Poisson margin), never from another reading.

## Oracles

- The history (census and episodes): no closed quarter is graded, reproduced or certified; the history describes past
  quarters under another mix and confirms no estimator.
- The plans: expected values only, no percentile, margin or range.
- The capacity return: in-house capacity only; its in-file line says it excludes Bellbird.
- Bellbird's 2025-26 service report (distractor): visits by member and quarter and service levels for 2025-26, nothing
  about January to March 2027 and no percentile.
- Nothing ties only under the golden: there is no published booking, percentile or reconciliation for the quarter.

## Ask sheet

Two asks and a chart, all on July to September 2026 records the call never reads (Bellbird's visit export, the
Alliance referral portal, Bellbird's intake line log, Schedules 3 and 4, Bellbird's client accounts, the Alliance
finance calendar). Zero device or hazard rows in the call's files (episodes, census, plans, capacity return, Schedule 2,
stream schedule, crosswalk, campus list, pathway): no Bellbird visit number, client code, intake log number or portal
referral id in any of them (asserted); the call is unchanged with every ask file and every distractor deleted
(asserted). Three devices, each from how these systems really write their records; one real cause, the portal outage
of 10 to 13 August 2026, feeds two of them.

**Ask A. What the Alliance owes Bellbird for July to September 2026, for each Member and month** (15 figures, dollars
to the nearest dollar) and the chart of Bellbird's payable visits by pay week and Member (5 Member totals graded).
- H18 home: the audit trail of the overflow contract the call books (the last quarter's spend on the same agreement).
- Use: the Alliance pays Bellbird monthly and recharges each Member (Schedule 3, clause 3.1); the booking goes with the
  quarter's bill.
- Primary device D1 (a replay under fresh ids beside genuine same-day pairs): Bellbird's app re-posts a visit the nurse
  keyed again when the app showed it unsent; the re-post carries a fresh visit number, the same patient and nurse,
  start and end up to 12 minutes off and a later record time, about 3 to 6 per cent of records, in every Member and
  month. Genuine same-day pairs sit beside them: heart failure patients' two visits on each of the first two days, an
  attempted visit and its revisit hours later, and the treating team's unscheduled returns to intravenous patients
  later the same day (on 0.01 to 0.08 of patient-days, asserted). Only the overlap of one nurse's two records for one
  patient shows a re-post; the exact-duplicate sweep finds nothing, and the same-patient-same-day sweep drops genuine
  visits (it misses 13 of the 15 amounts; the two thin July cells have no genuine pair). The two records of a pair
  start on the same Melbourne day and on the same side of 7.00 am, 6.00 pm, the referral's acceptance and 24 hours
  after it (a re-keyed time that would cross one is redrawn from the record's own stream, so the shared stream and
  every other pair are untouched), so whichever record survives (first or last posted, lowest or highest visit
  number, earliest or latest start) every amount, pay-week count and referral figure is the same: asserted on six
  rules in `checks.py` and four in `verify.py`, 30 pairs, starts 0 to 12 minutes apart.
- Second device D7 (the true key elsewhere, a reflex repair wrong): the patients telephoned through during the outage
  have their visits until 14 August under the Alliance's billing account C4466, which the accounts file lists with no
  Member and no patients, and the intake log number as the patient reference; dropping or parking those records misses
  every Member's August amount and every chart total; the intake log's row for that number names the Member.
- Hazards: D8 the export's times are UTC (the dictionary says so; reading them as Melbourne misses every amount), so
  Melbourne dates, the after-hours and weekend loadings, the Friday 25 September 2026 public holiday (the finance
  calendar) and the month edges all move; D2 the status codes change with app 5.0 on 3 August 2026 (COMPLETE, NOTHOME,
  CANCELLED before; Completed, Attempted, Cancelled after; dropping the old codes misses every July amount); D7
  Westmere's Altona Park campus patients under Bellbird's old Altona Park Health account C3920 (dropping it misses every
  Westmere amount).
- Path: Bellbird visit export (JSON lines), Schedule 3 (fees $146.20, $121.80 and $129.40, loadings, the $68.40 attempted fee),
  the finance calendar (holidays, pay weeks), the client accounts, the intake log, the dictionary.
- Realism: tablets re-post records a nurse keyed twice, mobile platforms store UTC, an intake desk opens a holding file
  when the member system cannot take the patient, and an account note goes stale.
- The chart's readings, closed by a WHAT: the prompt asks for the number of payable visits by pay week; the dictionary
  says the calendar's pay weeks run Monday to Sunday, its week_commencing row that the year's first pay week commences
  Monday 29 June 2026; the export holds visits on the quarter's days only, so the part weeks commencing 29 June and 28
  September carry only the quarter's days however a straddling week is read, and the five graded totals are the
  Members' payable visits for the quarter under any weeks (asserted). Payable visits are completed and attempted
  visits (clauses 3.4 and 3.5); completed visits alone miss every total (asserted).

**Ask B. Bellbird's referral response for July to September 2026, for each Member** (15 figures: the referrals the
Member made, the share Bellbird accepted within two hours, the share of accepted referrals first visited within 24
hours of acceptance; shares in per cent to one decimal).
- H18 home: the service levels of the agreement the call books against (Schedule 4).
- Use: the Alliance reviews Bellbird's referral response each quarter before booking the next block (clause 4.5).
- Primary device D4 (absence as the signal, in a file no habitual join reaches): the portal holds nothing sent from 10
  August 06:00 to 13 August 15:00; the Members telephoned those referrals to Bellbird's intake line, and they sit only
  in Bellbird's intake log among enquiries, roster calls, feedback, other clients' referrals and the Members' own
  follow-up calls about portal referrals (benign rows). A referral is a Member's request, whatever the channel (clause
  4.1); no filed sentence names the log or the outage. Every Member telephoned at least one accepted referral.
- Second device D7 (the true key elsewhere): those patients' first visits are under the intake log number on the
  billing account, so a join on the Member's patient number finds a first visit days later, a plausible reading of a
  slow week; every Member's 24-hour share misses unless the log number is followed.
- Hazards: D8 Bellbird's response time comes from its platform in UTC beside the portal's Melbourne send time (kept as
  UTC, every Member's two-hour share misses); D7 patient references in two formats between the portal and the visit
  export (client account and digits without leading zeros); the follow-up calls (counted as referrals, at least four
  Members' counts miss).
- Path: the portal export, the intake log, the visit export (first visits), Schedule 4, the client accounts, the
  dictionary.
- Realism: portals go down for upgrades that overrun, coordinators phone instead, and the provider's desk works around
  its own system until the link is made.
- The shares' bases, closed by a WHAT: Schedule 4 clause 4.5 reviews, for each Member, the share of the referrals it
  made in the quarter that Bellbird accepted within two hours of the Member making them, and the share of its accepted
  referrals first visited within 24 hours of acceptance, the prompt's own words; clause 4.2's response (accepted or
  declined within two hours) and acceptances over accepted referrals each give another figure for every Member
  (asserted). Bellbird's 2025-26 service report keeps its platform's responded-within-two-hours column, a neighbouring
  measure for another year.

**Criteria.** Call: five Members' lots and five requirements (10), the unbooked remainder or last Member (1), the
booking's sum (1); Ask A 15 figures and 5 chart totals; Ask B 15 figures; files and instruction following (3): about
50.

**Main population's zero counts.** Device and hazard rows in the episode extract, the census, the plans, the capacity
return and Schedule 2: 0 (asserted).

| Hazard | Asks moved | Per-ask delta (measured) |
|---|---|---|
| UTC stamps | A, B | A: every amount; B: every two-hour share |
| status code vintage | A | every July amount |
| Altona Park account | A | every Westmere amount |
| follow-up calls | B | at least four Members' counts |
| holiday on 25 September | A | at least three September amounts |

**Referee.** None ties only under the golden: Schedules 3 and 4 define the bases; no Bellbird invoice, total or
reconciliation ships for the quarter.

**Cracker profiles, measured.** Hits out of the 35 ask figures (15 amounts, 15 referral figures, 5 chart totals) for
every handling of the three devices (asserted in `checks.py`): none handled 2 (Kingsdale's August amount and one chart
total, where its one re-post and its one holding-file visit cancel); intake files alone 0; re-posts alone 10; telephoned
referrals alone 12; telephoned referrals and intake files 15; re-posts and either other 20; all three 35.

| Cracker (landed the call, ran the battery, executed every filed rule) | Ask A (15 + 5 chart totals) | Ask B (15) |
|---|---|---|
| exact duplicates removed, UTC converted, unmatched account parked, portal referrals only | miss | miss |
| re-posts removed by patient and day | miss | miss |
| one of the three devices handled | miss | miss |

Pair ceiling: 39.5 (the strongest response on the call handling the most obvious device, the telephoned referrals: 38
+ 7 + 55 x 12/35 = 63.9; the best response off the call at the no-device profile: 5 + 7 + 55 x 2/35 = 15.1; both on the
call with no device handled average 48.1)
Mirror leakage: 34 per cent of ask weight at most with one device handled (12 of 35 figures); 6 per cent with none; no
ask whole on one device

## Pins

| Pin | Authority | What it fixes | Never says |
|---|---|---|---|
| Schedule 2 (Variation 9), clauses 2.1 to 2.7 | 1, the executed agreement | the block, the order, the requirement's population and window (2.3), the 90th percentile of the quarter taken together (2.4), the plan as the expected value (2.5), lots that cover the excess (2.6), the block used in order (2.7) | how the percentile is estimated, that visits come in stays, any figure but the block |
| Schedules 3 and 4 (Variation 8) | 1 | fees, the one highest loading, the attempted visit fee, Melbourne time and the month of a visit (3.6), a referral as a request whatever the channel (4.1), the two service levels (4.2, 4.3), the two shares the Alliance reviews each quarter (4.5) | the portal, the outage, the intake log, any re-posted record |
| The program streams and visit schedule | 2, clinical governance | the streams, the visit schedule (wound care every second day, heart failure twice on the first two days), days at home both ends included, separation modes, a resumed course as a new episode | any length of stay, any spread |
| The pathway | 2 | that Northgate and Westmere follow the Alliance bone and joint protocol from 1 October 2026 | any stay figure or admission count beyond the plan |
| The dictionary, plans' and capacity return's notes | 4 | fields, UTC on Bellbird's platform, the two status vintages, the calendar's pay weeks (Monday to Sunday, the first commencing 29 June 2026), the plan's visits as every visit on the month's days, the return's in-house visits | anything about selection, the outage or a re-post |

## Prompt

`prompt.txt`, gated by `voice-check.py` (in `precut.py`): the call as a question with the 850-visit block, the
workbook with each member's requirement, the two July to September 2026 tables, the chart, and the rounding once at the
close. The call sentence is unchanged since stage 2; at stage 4 the chart sentence became "the number of Bellbird's
payable visits by pay week and member" (the leak reader's week and count readings). 838 characters.

## Leak review

`leak.py task142 --asof 2026-11-03` on the built pack: REVIEW, no LEAK. Each REVIEW line answered:

- Sweep 3, the committed call's words in Schedule 2, the service report and the pathway: they name the members, the
  provider, the quarter and the block because they are the agreement, the provider's report and the pathway; none
  carries a booking figure or a requirement.
- Sweep 4, stump terms in Schedule 2 (percentile, capacity, inside), Schedules 3 and 4, the service report, the
  pathway (admissions, course) and the stream schedule (admissions, course, episodes): each is the document's own
  vocabulary; none speaks of a stay's spread, a Poisson margin, a simulation or how the percentile is estimated. The
  pathway's four-to-eight-week course is clinical content every such pathway states, and the stays on file carry it
  anyway.
- Sweep 6, members beside numbers in Schedule 2 (clause numbers and the order), the intake log, the service report
  (2025-26 visits and service levels, a distractor), the dictionary (member codes), the capacity return, the plans and
  the survey: none ranks the members on the booking; the capacity return and the plans are inputs the call needs.
- Sweep 9, dates after 3 November 2026 in the finance calendar (the 2026-27 year) and the manifest's coverage column
  (the plans to June 2027, the quarter): forward-looking by nature, on the allow-list.

Stage 4, after the fix pass rebuild: `leak.py --asof 2026-11-03` REVIEW, no LEAK, the same sweeps over the same files
as above; sweep 4's term list follows this note's wording, and Schedules 3 and 4 match only the agreement's own words
(the new clause 4.5 brings none of the terms). The leak reader (no leak, Q6 analytical) is kept under `## Solver's-eye
read` in `leak_check_report.md`, every REVIEW line harmless. Its readings, ruled:

- The referral share's basis (accepted within two hours against clause 4.2's response): fixed by clause 4.5, which
  reviews the share of the referrals made that Bellbird accepted within two hours, the prompt's words (Ask B above).
- The chart's weeks (Monday to Sunday, and the part weeks at 1 July and 30 September): fixed by "pay week" in the
  prompt and the dictionary's week_commencing row; the part weeks cannot move a count, the export holding the
  quarter's days only (Ask A above).
- Payable visits as a count: fixed by "the number of" in the prompt; completed and attempted under clauses 3.4 and 3.5.
- Time bases and status labels: harmless, documented Layer 1 (the dictionary files UTC and both status vintages).
- Realism: the manifest's rows_or_pages now carries every file (rows, sheets or pages, asserted against the files);
  the H04 plan rows are kept, since their October to March months feed the call and no change to them is
  figure-neutral.

## Build record

- Generator `task142/generator/` (common, world, model, records, docs, postprocess, calc, deliver, checks, verify,
  metadata, build): `python3 task142/generator/build.py` builds the world, the pack, the goldens, `metadata.json` and
  `figures.json`, runs `checks.py` and the independent `verify.py` (Panjer's recursion for the call against the
  generator's Fourier transform, zoneinfo for the clocks, its own parsing), then a second full build compared byte for
  byte, then cuts `target.zip`.
- The pack: 20 files in five formats (csv, docx, jsonl, pdf, xlsx); the census 32,517 rows, the episode extract 7,703;
  distractors `hith_patient_experience_survey_2025-26.xlsx`, `bellbird_service_report_2025-26.pdf` and
  `bellbird_declined_referrals_2025-26.csv`, declared in `metadata.json`, each deleted with the call and every ask
  unchanged (asserted).
- Built figures: requirements 2,397.1, 2,147.5, 1,798.3, 1,403.3 and 1,247.2 before the 50 (the verifier agrees to the
  tenth); the booking 300, 250, 225, 75 and none; the default path 100, 50, 50, 25 and 25 with 600 unbooked.
- Stage 3 gates, 2026-10-15: `build.py` green (437 assertions in `checks.py`, the three-rules block R1 to R3c among
  them on the clean truth, every SF row, every rung by name, the family, the cracker profiles; `verify.py` agreeing on
  every graded figure; two builds byte-identical; `target.zip` cut); `precut.py` 49 checks, 0 FAIL; `figures_check.py`
  PASS (98 figures); `voice-check.py` PASS; `leak.py --asof 2026-11-03` REVIEW, no LEAK (answered above); `guard.py
  surface` 0 promoted pairs (after Bellbird's visit export moved to JSON lines, the pack's format set no longer equals
  three builds'), `heart` WARN (`repeat.gate_g`, answered in the Draw, no BLOCK), `validate` clean; the container audit
  (`scrub_producer_metadata.py`) clean on `target/` and `golden/`. Stage 4 (the leak reader and the determinism judge)
  is next.
- Stage 4, 2026-10-15: the reader found no leak (three readings, ruled in `## Leak review`); the judge returned
  NOT_DETERMINISTIC on one cell, FIX_NOW (`determinism_check_report.md`): which record of a re-post pair is the visit
  moved Kingsdale's September amount ($8,787 or $8,755), the one pair whose starts straddled 6.00 pm. Fixed in one
  generator pass: re-post pairs are drawn on one side of every line their fee, day and clocks turn on (one record moved,
  BV6112106 to 6.12 pm), every survivor rule asserted to give every ask figure; clause 4.5, the dictionary's
  week_commencing row, the manifest's sizes and the prompt's chart sentence for the readings. Gates on the final
  rebuild: `build.py` green (490 assertions, the cracker profiles unchanged), `verify.py` agreeing under four survivor
  rules, two builds byte-identical; `freeze.py check --mode determinism` PASS; `figures_check.py` PASS (98);
  `precut.py` 49/0; `voice-check.py` PASS (838 characters); `leak.py` REVIEW, no LEAK; `guard.py surface` 0 promoted,
  `heart` WARN (`repeat.gate_g`), `validate` clean; the container audit clean. Changed under `target/`: the
  Schedules 3 and 4 PDF (clause 4.5), the visit export (one record's times), the data dictionary (one row) and the
  manifest. The single re-judge is next.
- Ship (2026-10-15): the re-judge returned DETERMINISTIC, APPROVE, every graded figure reproduced
  (`determinism_check_report.md`); the targeted leak re-read of clause 4.5, the dictionary row, the manifest and the
  prompt's chart sentence came back clean (`leak_check_report.md`, round 2). `target.zip` is the stage 4 final
  rebuild's cut, byte-identical on the second build (sha256 c0616cc42ee80a2d); no file moved after the re-checks.

## Pre-ship check

Written at stage 5 against the built pack (the stage 4 fix pass in); the reader and judge lines are stage 4's, the
targeted re-read's and the re-judge's.

1. Domain: the deciding quantity is each member's 90th-percentile Hospital in the Home visit requirement for January
   to March 2027, the home days of a random stream of admissions whose stays run by stream (days for cellulitis or a
   clot, weeks for a bone and joint infection) counted inside the quarter, the
   admissions-times-length-of-stay accounting health services plan HITH capacity with; with a data centre's or a
   grid's nouns there is no admission, no infection course and no HITH day, and the spread they create goes with them.
2. Real work, nothing planted: a census warehouse loaded from five members' returns (patient numbers in five formats,
   Westmere's campus codes reissued at the Altona Park merger), program streams revised on 1 July 2025 and joined
   through the crosswalk, plans by financial year one sheet a member, a course split by a ward return, episodes open
   at the extract; on the ask paths Bellbird's UTC export, two app status vintages, re-posted records, the portal
   outage's telephoned referrals and holding files. Each is what these systems write; each mishandled leaves the call
   where it was (R2, asserted), and the call reads no ask file (asserted). The stage 4 changes are a filed WHAT
   (clause 4.5, the dictionary's pay week row, the prompt's chart words) and the re-post pairs' generation rule, all on
   the ask paths.
3. The flip is a method choice: the quarter's distribution built from the plan's admissions and the stays on file,
   counted inside the window, against a Poisson margin on the planned visits or the history's spread of weeks, months
   or quarters; no field, unit or stated rule decides it (Schedule 2 files the estimand and leaves the estimator open),
   and the default path reads every filed rule the same (R3a on the clean truth).
4. The analyst test holds: plan plus a Poisson margin books 100, 50, 50, 25 and 25 with 600 unbooked; the history's
   monthly spread, its weekly spread, an AR(1) on daily visits and the members' own past admissions and stays each
   book otherwise; only the admissions-and-stays construction books 300, 250, 225, 75 and none, on all thirteen
   admissible constructions and on the clean truth (R3b).
5. One defensible answer: Schedule 2 clauses 2.2 to 2.7 file the estimand; the 14 fork rows are asserted and the 22
   closure axes closed; the re-judge reproduced every graded figure (40 of 40 bootstrap resamples of the stays book the
   golden; stay-set variants centred on the plan leave every requirement in its 50-visit bin); the asks' readings were
   closed at stage 4 (every survivor rule of a re-post pair, clause 4.5's two shares, the pay weeks, the count).
6. No decoy: no file states a percentile, margin, requirement or booking; the plans give expected visits only; the
   patient experience survey, Bellbird's 2025-26 service report and its declined referrals are declared distractors,
   read by neither the call nor any ask (asserted).
7. Nothing hidden and recovered: no published percentile, past booking or certified requirement ships to reproduce;
   the history describes past quarters under another mix and confirms no estimator.
8. A new lesson: an upper percentile of a period's total made of multi-day stays has the spread of the admissions and
   their stays, so it is built from them and counted inside the window, and a plan that adds long stays moves the
   spread more than its mean; no build on file teaches the spread of a period total from its generating units.
9. Leak reader (stage 4): no leak; Q1 to Q4 none; Q6 analytical; its three readings (the referral share's basis, the
   chart's weeks, payable visits as a count) fixed in the generator pass, the manifest's sizes filled and the H04 plan
   rows kept. The targeted re-read: clean, Q1, Q2 and Q4 none, Q6 analytical; telephoned referrals under clause 4.1,
   the straddling pay weeks and every accepted portal referral's visit after acceptance (0 missing) all closed in the
   pack.
10. Judge (stage 4): NOT_DETERMINISTIC on one ask cell (which record of a re-post pair is the visit, Kingsdale
   September), FIX_NOW applied in one generator pass with `freeze.py --mode determinism` passing, so no graded figure
   moved; the re-judge DETERMINISTIC, APPROVE, stump power strong, Gate G analytical_non_defect with no surface-read
   dependency, Gate H domain pass, layers pass, decisive step analytical. The asks' devices are as designed (the
   cracker profiles unchanged, pair ceiling 39.5); clause 4.5 removes a reading the design never counted on.

## Tried and rejected

- 2026-10-15, before the card: the seed's world (a storage fleet's contract technician visits across data centres)
  dropped as a compute-capacity world beside task140; only the decision and quantity shape kept.
- 2026-10-15, before the card: a percentile of a quarter's visits as the only decisive step with the members' own
  history as the mean was dropped on paper: with the mean estimated from two or three past first quarters, its own
  error (about 0.4 of the quarter's spread) swamps every margin difference; the operating plan files the expected
  visits so the stump sits in the spread alone.
- 2026-10-15, before the card: the same world with a health service's own HITH team as the decision-maker hit four
  bans against task260 (organisation family, role, forcing event, decisive G16); the decision moved to the alliance.
- 2026-10-15, stage 3: Ask B's second device as portal resends (the first send marked Withdrawn beside genuine
  withdrawals) dropped: it opened two readings, the two-hour clock from the first send or the resend and whether a
  withdrawn referral is a referral made; replaced by the outage's holding files, which a cited sentence closes (clause
  4.1) and an in-world record resolves (the intake log).
- 2026-10-15, stage 3: a clinical care fee of $129.50 put the after-hours loading on a half cent ($161.875), so an
  amount's dollar could depend on rounding each fee; the fee is $129.40 and every loaded fee is whole cents.
- 2026-10-15, stage 3: five lines on one chart ended within a few visits of each other and their end labels left their
  lines; the chart is small multiples, one panel per Member and one for all Members.
- 2026-10-15, stage 3: a guard that pushed every first visit within 36 minutes of 24 hours (and every response within
  8 minutes of two hours) past the threshold left a visible gap under each; times are whole minutes, so the guard now
  clears only near-ties (4 and 2 minutes).
- 2026-10-15, stage 4: the judge's first fix, a dictionary line saying which record of a re-posted pair is the visit,
  was not taken: a filed rule would adjudicate Ask A's device (supplemental-stumping, ban 1) and name it to every
  reader; the pairs are closed in the data instead (never across a fee or clock line), so every survivor rule converges.
- 2026-10-15, stage 4: moving the one Kingsdale record by hand was not taken either: a generation rule keeps any future
  pair off the lines, and redrawing only a crossing draw from the record's own stream leaves the other 29 pairs as built.
- 2026-10-15, stage 4: matching the referral share to clause 4.2 by asking for the share "responded to within two
  hours" was dropped: it moves every graded share (82.1 against 75.0 at Northgate); clause 4.5 files the accepted basis.
- 2026-10-15, stage 4: naturalising the H04 plan rows (a ramp in the pathway's first months) was dropped: October to
  March admissions feed the call's expected visits and percentile, so no change there is figure-neutral.


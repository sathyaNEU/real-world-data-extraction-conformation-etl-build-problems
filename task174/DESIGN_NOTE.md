# task174 design note

**Status: architecture 2, drawn 2026-10-28** in education-learning-sciences / learning-analytics-early-warning-models
(Forecasting), the slot's first registered card. The screens of 2026-10-19 and 2026-10-23 registered nothing and cut
nothing; their record is kept under `## Slot history` and every death is a line in `## Tried and rejected`. This draw
re-enters the early-warning cell with the one family the 2026-10-19 pass never screened: practice logs written under a
mastery stop rule and a daily cap, read for a routine with no night in it.

## Draw

1. **Pairing.** education-learning-sciences / learning-analytics-early-warning-models, Forecasting (the task type
   serves F only). The call forecasts, for each spring unit, the seventh graders who will fall short on a check
   taken after a fixed practice set in one class period, and sets the set length against funded reteach places.
2. **Niche.** Tamberlin County Schools (North Carolina, twelve middle schools, about 2,800 seventh graders a year)
   has run each math unit's practice as a Rungwell Math skill builder done as homework: a student is done at three
   first-attempt answers right in a row, can answer at most ten of a skill builder's problems a day, and the
   skill builder closes ten school days after it opens. From 4 January 2027 the four spring units' skill builders
   move into class: one period holds a set of problems and then a five-problem check from the same skill builder,
   and a student with fewer than three of the five right joins the next day's reteach group with an
   interventionist. The board's amendment funds 4,300 reteach places (one place is one student in one unit's
   group); the math office sets the set length, 6, 8 or 10 problems, as the shortest whose failed checks fit the
   places, and staffs on the seventh graders on roll on 23 October 2026.
3. **Decision.** Which set length (6, 8 or 10 problems), with the failed checks forecast at each length and for
   each spring unit at the chosen one. Forward facing: spring 2027, nothing of it observed.
4. **Data-native sentence.** Rungwell stops a student at the first three right in a row and holds homework to ten
   problems a day, so the log's later problems belong to students who had not yet stopped and sit after a night
   that kept only part of the earlier sitting's gain, while the spring check comes after one sitting with no night
   in it.
5. **Default path's answer against the golden.** The field's learning curve fitted with one practice count per
   student and skill builder files that no allowed set fits (about 5,600 failed checks even at ten problems);
   golden eight problems, about 3,900 failed checks against 4,300 places.
6. **Shape.** 04, setting one dial (F over an open window): the forecast at each of the three lengths, the chosen
   length, and each spring unit's failed checks at it.
7. **Deliverables.** `spring_practice_set_length.xlsx` (the forecast by length and unit, and the asks),
   `spring_reteach_memo.docx` (the case for the length), `spring_reteach_forecast.png` (failed checks by length
   against the places).
8. **Nearest driver.** `guard.py check` on the registered card: PASS; nearest drivers task272 (0.07), task122
   (0.05), task179 and task156 (0.04). `mechanisms --objective forecasting` and `slots` on practice, mastery, learning
   curve, knowledge tracing, streak, stopping rule, survivor, overnight, sitting, forgetting, spacing, homework,
   reteach, interventionist and skill builder: no build on file models learning or forgetting from a practice log.
   The closest insight is task156's frailty (fast leavers go first), which here is the second move only.
9. **Guard.** PASS after six differentiation lines (task178, task461, task229, task242, task476, task501: the
   signature time, G13, method_or_model_selection is crowded, none of the six is the same mechanism). Axes redrawn
   against the live window (task304, task177, task162): forcing event budget_or_appropriation (the places are what
   the board funded; launch_or_rollout is barred and the rollout itself is already decided, so the budget is what
   forces the length now), context artifact planning_thread (operations_log and monitoring_export barred; the
   stakeholder's artifact is the plan thread, the log is the spine), decisive generator G13 (G7 barred; the
   decision's practice window, one sitting, differs from the record's, several evenings), shape 04 (02 barred).
10. **People** (`guard.py names --geo US --seed 174`): Linda Ramos (district mathematics coordinator), Tara
    Richardson (chief academic officer), Heidi Ortega (accountability and data analyst), Bryan Wallace
    (interventionist programme manager), Gregory Griffin (budget director). None appears in the prompt.

## Default path

The competent route, every field and rule read correctly:

1. Read the plan: the shortest of 6, 8 or 10 problems whose failed checks fit the 4,300 places, staffed on the
   seventh graders on roll on 23 October 2026, Units 4 to 7.
2. Clean the log: stack the two export layouts, put the 2025-26 UTC times on Eastern time, keep original problems
   (drop scaffold rows), map platform accounts to students through the crosswalk, drop staff test accounts and the
   re-exported duplicate month.
3. Fit the field's learning curve to the seventh graders' first attempts: each student's ability, each skill
   builder's easiness and a learning slope on the count of the skill builder's problems the student has answered
   (the additive factors model, student effects as random intercepts).
4. For each seventh grader on roll and each spring skill builder, predict the five check problems after a set of
   6, 8 or 10 problems, and add up the chance of fewer than three right.
5. About 6,600 at six, 6,200 at eight and 5,600 at ten: none fits 4,300, so the memo files that no allowed set
   keeps within the places and asks for more.

Ends on: no allowed set fits (about 5,600 failed checks even at ten problems)
Golden: eight problems, about 3,900 failed checks

## Stump sentence

A competent analyst fits the additive factors learning curve to the homework log with one practice count per
student and skill builder, reads the overnight loss as slow learning, and files that no allowed set fits (about
5,600 failed checks even at ten problems); the golden counts the current sitting's problems apart from earlier
sittings' within each student and files eight problems, about 3,900 failed checks against 4,300 places.

## Three rules

Task type: learning-analytics-early-warning-models (education-learning-sciences), which serves Forecasting: the call forecasts which seventh graders will fall short on each spring unit's check and sizes the set length against funded reteach places.
Domain test: the deciding quantity is each student's gain per problem practised within one sitting, the learning slope of the additive factors model estimated within student from first-attempt correctness by practice opportunity, with earlier sittings' practice counted apart, the way learning analytics models practice logs with recency and spacing terms.
Swap: "how many machines fail the bench check after eight cycles in one shift, read from a log where machines stop at three passes in a row and resume next shift" keeps the arithmetic and loses the learner who gains within a sitting and keeps part of it overnight, so the deciding quantity has no counterpart; with nurses on a simulator the task stays in education.
Layer 1: Rungwell changed its export between school years (renamed columns, Eastern local time in 2024-25 and UTC from 2025-26), logs scaffold sub-questions beside original problems, re-exported one school's November 2025, gives a re-enrolled student a second account that the district crosswalk maps, keeps staff test accounts in the log, and the student system records mid-year moves as enrollment spells; none is placed and none decides the call.
Layer 2: estimand_identification: the quantity is the gain within one sitting, estimated within student under the mastery stop, against the pooled curve, the single-count curve or a replay of homework completion, each of which files a different length.
Decisive step: counting each student's problems in the current sitting apart from the problems of earlier sittings while estimating the slope within student, then predicting the check after a set done in one sitting.
Not semantics: every column, code and rule read correctly (original problems, first attempts, the ten-a-day cap on the local day, the crosswalk, the roll date) still leaves the field's learning curve with one practice count per student, which files that no allowed set fits.
Not rule application: no filed rule says how practice carries over a night or how to estimate a gain, the plan states only the routine, the check and the places; the enumerated family (replay, pooled curve, one-count curve within student, log-count curve, pooled sitting-aware, sitting-aware within student) spans about 1,800 to 6,600 failed checks at eight problems and files 6, 10, 8 or none, the standing family (sitting-aware within student with two counts, first sittings only, decay by elapsed days, ability by posterior mode or integrated) spans about 3 per cent and files eight, and the ruling-out is the data's own fit, log-likelihood gaps of about 4,000 against the one-count and log-count curves.
Analyst test: a strong analyst who cleans the log and reads every rule fits the additive factors curve with one practice count per student and skill builder and files that no allowed set fits (about 5,600 failed checks even at ten problems), while the plainer replay of homework completion files six problems.
Estimand: the spring plan (spring_2027_seventh_grade_math_plan) fixes the population (the seventh graders on roll on 23 October 2026), the outcome (fewer than three of the five check problems right on a unit's check, one place each), the window (Units 4 to 7, spring 2027), the unit (one student in one unit's group) and the comparison (sets of 6, 8 or 10 problems, the shortest whose places fit 4,300).
No decoy: nothing is planted: the vendor guide states its own rules, the plan states the routine and the funded places, and no memo, draft, briefing or stakeholder figure argues for a set length or a failed-check count.
No certified replay: no certified or published figure is reproduced to recover a method; the vendor's national benchmark report states homework-mode averages, ranks nothing on the decision question and is a named distractor.
Lesson: a learning curve read from a practice log is the gain under the log's own schedule; carried to a routine with no night in it, the gain within one sitting has to be measured apart from what survives the night and within each learner, because the stop rule takes the fast learners out of the later problems; no build on file models learning or forgetting from practice.

## Readability screen

## Semantic fork table

## Ladder

## Closure table

## Literal reader

## Oracles

## Ask sheet

## Slot history


**Status: PAUSED at stage 1 on 2026-10-23 after six rebuild screens, biomedical survival, media reach, healthcare demand, regression diagnostics, ratemaking and reserving, a second pass over fourteen fresh cells left to the build and a third over stress testing, seasonal adjustment and urban forecasting (`## Rebuild (2026-10-23)`); RETIRED at stage 1 on 2026-10-19, no card ever registered, nothing cut (`## Retired`).** Wave 8, new,
Forecasting. Three worlds were screened on this number and none yields a draw that holds; the third, the
product-analytics retention cell of the same day, is recorded in its own finding below and in the last block of
`## Tried and rejected`. The first is seed FC45's: a north-east
Pennsylvania gas producer committing, in a 2027 incremental firm-sale agreement with an LNG feedgas buyer, the
gas from wells first turned in line on or after 1 January 2027 and delivered in calendar 2027. Two mechanisms in
that world were screened on code, the second at the coordinator's call, and neither held on measurement (its
prototypes stay in the session scratchpad, b174/proto). The second is the redraw of 2026-10-19 in the cell the
coordinator allocated, education-learning-sciences with the task type learning-analytics-early-warning-models
(it serves Forecasting): twenty-one candidates, two screened on code (`proto13.py` and `proto21.py`, scratchpad
r174) and the rest on the structural screens (a spent driver, the WHAT screen, the swap test, the readability
screen, the library test). No architecture is live. This note holds the screen record only; it carries none of
the `precut.py` sections, because no design exists.

**The structural sentence, and the first thing to read.** Calendar-2027 gas from wells first turned in line
in 2027 is mostly each well's first four to six months. Any difference between the coming wells and the
record therefore either arrives after those months, where it moves the figure by less than the bin the noise
allows, or shows inside them, where the youngest wells of the same design already measure it by a filter and
a divide. The one input with a large lever, each pad's turn-in-line date, rides on a delay process noisy
enough that the cheap routes (a flat two-month slip, the slip pooled over every schedule issue) sit within a
bin of the golden. A draw on this quantity needs a difference between the coming year and the record that is
large in the first months, invisible in the young wells' own months and measured in full somewhere else in
the record; none was found in this world.

**The taxonomy finding.** Upstream production forecasting has no client task type of its own. Energy Systems
& Utilities offers load-forecasting (demand on the system), asset-condition-maintenance (equipment health)
and generation-capacity-planning (Opportunity Sizing only), and none of them is a producer's supply forecast.
Economics & Econometrics' forecasting-forecast-evaluation is a home only where the decisive step is itself a
forecast-evaluation judgment (the spacing driver's rejection of the rival at the depth that matters, or the
as-issued evaluation of a schedule), and the domains README keeps Economics to macro, labour, trade and
fiscal reads, which a producer's own operations are not, so even that home is contestable.

**The early-warning cell finding.** A forward question an early-warning lead faces changes one of three
things, and under this round's constraints each is closed. A change in who is coached (a capacity cut, a
retired alert, a coaching contract that ends) is causal: its lever is large only on the band that loses or gains
coaching (29 to 40 per cent there, 6 to 13 per cent on a cohort's total), a call about that band names the change
and its counterfactual, and the band's uncoached rate from a realistic no-contact holdout carries a sigma of 2 to
3 per cent. A change in what the alert outputs (its cadence, its week, its threshold, its model) replays exactly
on the history's own scores, or, where the history's later scores were themselves lifted by the old alert's
coaching, shows that as a step of five to eight sigma in the faculty-by-year series and moves the figure only 11
to 17 per cent. A change in who arrives is composition, out for this round. The shapes that held in today's blind
reads (a cap that truncates waits, a calendar-locked wave, a gain on each unit's own baseline) have their nearest
early-warning forms already spent (task172, task162, task165, task170), and each of the cell's four cards is the
textbook route those readers take.

**The retention cell finding.** In product-analytics / retention-cohort-lifetime-value-modeling the cell's cards
(censored young cohorts, heterogeneous churn, resampled users) hold up: a survival curve by the unit the question
names, taken by the plan or the group the unit sits in, absorbs every stationary structure of a subscription book,
so a stump needs a forward condition the record has not shown at the same tenure. The natural forward conditions in
subscriptions are each closed. A temporary price ending is task137's driver, a stock drawn down before a
cancellation task161's, a return wave task157's, a gain on each account's own headroom task165's, a surge read by
time since entry task134 v2's. A commitment end, a renewal date or a plan is visible, and the plan-level curve
reads it. A response to a policy (reminder laws, cooling-off rights, bundle partners, payment-method sunsets) is
causal, sized from one past event, with causal_design blocked by task249 v4.


### Retired (2026-10-19)

Retired on 2026-10-19 at stage 1, by the author's rule that a number which dies in its second new cell this round
is retired. No card was ever registered, no axis of the guard's window was spent, and nothing was cut. Three
worlds were screened: seed FC45's upstream gas producer (two mechanisms, dead on code), education-learning-sciences
/ learning-analytics-early-warning-models (twenty-one candidates, two on code) and product-analytics /
retention-cohort-lifetime-value-modeling (fifteen candidates, two on code). Every death is a line in `## Tried and
rejected`; the prototypes stay in the session scratchpads (b174/proto and r174).

### Rebuild (2026-10-23)

Reopened by the author's rule that no number stays retired, and screened from scratch in
biomedical-clinical-research / survival-time-to-event-analysis (Forecasting), the cell the coordinator allocated,
with the field's own corrections (Kaplan-Meier for censoring, Aalen-Johansen for competing risks, left truncation)
taken as the default path. No card was registered and nothing was cut: two candidates measured on code
(`s1_backlog.py`, `s3_entry.py`, scratchpad b174n/proto) and twenty-three on the structural screens, every death a
line at the foot of `## Tried and rejected`. The number is PAUSED at stage 1 for the coordinator to assign another
cell.

**Second rebuild pass (2026-10-23, the cell left to this build, shape first).** The coordinator's brief asked for the
shape of the two holds this round (task175: the forward units sit at one end of a covariate the record measures at a
finer grain than the textbook model uses, the grain chosen by fit; task169: a structural estimand choice the textbook
route does not make), with the cells parallel rebuilds hold and the cells that died this round excluded, and with the
stage 4 law that a channel or correction the field teaches is applied by a medium reader unprompted. Fresh ground was
taken first: political-science-public-policy / election-polling-forecasting and the never-drawn actuarial
mortality-longevity, then asset-condition-maintenance, municipal-service-demand-resource-allocation,
population-estimation-demographic-projection, fertility-mortality-life-table-estimation, scaling-laws,
resampling-simulation-monte-carlo-methods, deposit-liquidity-behaviour, expected-credit-loss-provisioning,
churn-propensity-uplift-modeling, feature-adoption-diffusion-modeling, conjoint-choice-willingness-to-pay-analysis and
strategy-backtesting-evaluation. One candidate was measured on code (`cem1.py`, scratchpad b174n/r2) and about twenty
died on the structural screens; no card was registered and nothing was cut. Every death is a line at the foot of
`## Tried and rejected`.

**The finding of the pass.** A one-year-ahead forecast of a process that changes smoothly is matched by the trend of
its own record, so a lever needs a discontinuity at the forecast start (a new population, a new rule, a new area);
the response to it then has to be read on a covariate the record measures at a finer grain. In every cell screened
that covariate was one of four things, each closed: a channel the field names (the at-home vote of first-time voters,
pressure transients from pump starts, garden size, roof orientation, an agent's departure, a boiler's age), which a
medium reader measures on sight; a column or a two-column join, which the log-link regression on the obvious
covariates reaches exactly; a contagion of the same outcome among neighbours, peers or a household, which is task175's
driver and task144's; or a timing exposure, which is task177 v2's. Where the forward condition is a schedule or a rule
applied to units the record already holds, it replays on the record (the careful reader's move and the golden). The
number is PAUSED at stage 1 again for the coordinator to assign a cell.

**Third rebuild pass (2026-10-23, the cell left to the build, shape first, brief rb-task174s).** Read first: this
note's `## Tried and rejected` and `## Retired`, the parallel rebuilds' cells (task176 event history, task179 early
warning, task173's valve world, task170 and task177 still choosing with no DRAWN commit at c9563ae3) and the cells that
died this round in other notes. The F task types left after those exclusions were stress-testing-capital,
seasonal-adjustment-official-time-series-production, urban-regional-science / forecasting (none screened this round),
and, as cross-checks, health-burden-impact-modeling, infectious-disease-transmission-modeling (fictional settings),
dose-response-pk-pd-modeling and recidivism-risk-assessment. The window at the screen (`guard.py recent`): task173,
task179 and task275 live, so `causal_design`, `composition_mix` and `population_selection` are banned (task275, drawn
after the brief's measurement, took `population_selection`). That closes task175's shape outright, because its honest
label is `composition_mix` (a forward population at one end of a covariate the history's rate was measured across),
and leaves task169's shape (`decomposition_attribution`) needing a decomposition other than a pre-empting route.
About twenty-three candidates died on the structural screens, none reached code, no card was registered and nothing
was cut; every death is a line at the foot of `## Tried and rejected`.

**The finding of the third pass.** In the three fresh cells the field's textbook route already sits on the structure a
forward condition activates: roll rates read off the jump-off delinquency buckets, loan-level current LTV, the last
years' seasonal shares, exposures read off the timetable feed. What is left is one of four things, each closed: an
expectation additive over units (a joint default or a shared event moves only the tail, so the variance-only screen
fires), a single-purpose operations file that names the channel (a collections dialer log), a forward population
shifted on a covariate (`composition_mix`, banned in the window), or a route that pre-empted the recorded outcome
(task169's driver by abstraction). task170's ninth cell (1e08bf94, pushed during this pass) screened urban-regional-science / forecasting in parallel and
found the same: its bike-share phase was landed by the textbook origin-destination gravity model and its plateau phase
handed over by a station elevation column. The number is PAUSED at stage 1 again for the main session to assign a
cell.

**The finding, and the first thing a later pass should read.** A forecast of events over a cohort's current risk
set, made from a hazard by time since entry with the field's corrections applied and each member's own follow-up
conditioned on, is unbiased whenever the entry cohorts are exchangeable on the clock the hazard runs on and the
window stays inside the follow-up already observed. Every per-patient refinement (the current progression state, a
response or MRD status, a biomarker path, a recurrent-event history) then buys precision, not a lever. A lever needs
one of four breakers: the cohorts change across entry, the window extrapolates past the observed follow-up, a
forward change rewires the process, or the record is bound to a calendar (a visit schedule, a season, a batch). In
this cell the first is absorbed by the pooled curve (measured at 5 to 7 per cent, inside the noise), the second
forks on the parametric family, the third is either the textbook competing-risks move (task169's driver when a route
closes) or names its own step, and the fourth is task162's or task178's driver in clinical nouns. Event-driven trials
also carry only hundreds of events, so any decisive parameter estimated from a trial carries several per cent of
sigma against the bar's one per cent; only registries of tens of thousands reach it, and there the time-since-entry
curve absorbs the stationary structure.

**The second cell of the day, marketing-consumer-research / media-reach-frequency-audience-measurement
(Forecasting).** Screened with the field's planning routes as the default path (a reach curve fitted on GRPs,
Sainsbury or beta-binomial duplication and frequency, last campaign's reach carried). One candidate measured on
code (`cap1.py`, scratchpad b174n/proto2) and eleven on the structural screens; nothing holds. The finding: with
respondent-level panel or exposure logs, the field's own route is a respondent-level schedule simulation, and like the
survival curve by time since entry it absorbs every stationary structure of the audience; what breaks it is a plan
the record never ran, and each such plan is either a delivery mechanic (a cap, a pacing rule, an ad load), which is
rule application once filed and a hidden rule or a fork when not (the `binding_constraint` pincer of `stumping`
1.2), or a new vehicle, season or audience whose own panelists are the attaining subset.

**The third cell of the day, healthcare-delivery-health-economics / utilization-access-demand-forecasting
(Forecasting),** task170 v1's world and first-passage driver avoided. Screened with the field's demand routes as the
default path (age-sex rates on the projected population, last year's utilization grown by trend, a literature
elasticity applied to a price or access change). One candidate measured on code (`wait1.py`, scratchpad
b174n/proto3) and fifteen on the structural screens; nothing holds. The finding: a forward access or payment change
in this cell does one of four things. It acts on a variable the change itself names (a wait, a booking lead time, a
travel time, a pilot area), so the record's units already at the new level are the attaining subset and the premise
sends the solver to them. It needs a behavioural response never observed before the change (self-referral,
cost-sharing, telehealth, plan choice), which is a literature elasticity, the default, or a fork. It is a filed
mechanic (a triage streaming rule, a capacity queue, a screening round plan), which is rule application. Or it
reroutes demand through a route that used to pre-empt it (task169's driver) or a drain while waiting (task148's).

**The fourth cell of the day, general-statistics-data-science / regression-classification-model-diagnostics
(Forecasting),** task158's and task172's drivers avoided. Screened against the coordinator's criterion (the forward
condition acts through a quantity the change does not name and no unit in the record has reached, the data reveal
it, and the textbook validation passes because the hold-out shares the training regime). One candidate met the
criterion and measured well on code (`tel1.py`, `tel2.py`, scratchpad b174n/proto4), and it died on the abstraction
test against task262; eleven others died on the structural screens. The finding: the cell's natural homes for an
unnamed, unreached quantity are each spent. The noise in a covariate is task262 (a reliability ratio is a property
of the population, the noise variance carries), the selection that produced the labels is task141, a moved base
rate is task446, a group effect shared by a new group is task143, a retransformed log-scale mean is task135, and
what is left (a range extrapolated, an interaction the record never varied, a covariate collinear in the record)
is unidentified in the record, so the method forks.

**The fifth cell of the day, actuarial-science-insurance / pricing-ratemaking-credibility (Forecasting),** task130's
and task270's drivers avoided. Screened with trended and developed loss ratios, credibility against the complement
and a GLM relativity carried forward as the default path. One candidate measured on code (`cred1.py`, scratchpad
b174n/proto5) and fifteen on the structural screens; nothing holds. The finding: a forward coverage or benefit
change is either applied claim by claim, which is the field's benefit-change factor executed (rule application), or
acts on the unobserved part of a claim-size distribution, which is the censored and truncated severity card (the
default) or an extrapolation that forks. A forward change in who buys is selection on recorded attributes (the
policies already holding those attributes are the attaining subset) or on unrecorded ones (unidentified). The
behavioural rewirings the field documents (claims absorbed under a deductible or a no-claims scale, durations
bunched past a retroactive day or a tort threshold) are task270's family, and a credibility weight on drifting risk
is matched by the trailing-years reflex.

**The sixth cell, chosen by this build: actuarial-science-insurance / reserving-development-triangles
(Forecasting).** Why the shape lives there: the field's standard is the aggregate development triangle, while the
claim-level transaction file is finer than anything the triangle carries, and per-claim quantities (each claim's
limit or retention, its scheduled payments, its payment dates against a price index, its trial date) enter a
projection of future payments linearly and by identity for every open claim, so no part of the record escapes them.
One candidate measured on code (`lim1.py`, scratchpad b174n/proto6) and nine on the structural screens; nothing
holds. The finding: each per-claim identity the triangle ignores is a cap (a limit, a retention, a deductible
recoverable), a scheduled date (a trial date, a periodic-payment schedule), a price index or a closure-speed change.
A cap that rarely bound in the older years and binds for most recent claims, and a date that fixes each claim's
payment, are task172's driver (a per-unit ceiling or deadline that the record seldom reached and the forward units
mostly reach). The index is the inflation-adjusted chain ladder, a textbook method. The closure-speed change is the
Berquist-Sherman card.


## Tried and rejected

- **Spacing interference as the decisive step** (the seed's eight-well pads at 660 ft against the 1,000-ft
  type curve), killed at stage 1 on measurement (prototypes `lever.py`, `screen_common_exposure.py`). The
  prototype is self-similar drainage between parallel laterals: a mixture of slab solutions over a spread of
  diffusivities, a managed 60-day plateau, and EUR at 660 ft between 0.63 and 0.73 of 1,000 ft. It ran on
  three 2027 turn-in-line schedules (front-loaded, even, late). The lever and the common-exposure subset are
  one dial. When the onset is late enough that the 2026 eight-well pads' four observed months show under
  2 per cent (S(4) of 0.98 or more), the 1,000-ft curve over the 660-ft curve on calendar-2027 volume is
  only 1.01 to 1.065. A lever of 1.08 to 1.17 needs S(4) between 0.72 and 0.92, which those pads show in
  their own months. Their own months, filtered and divided with the last month's ratio held, then land at
  1.024 to 1.072 of the golden with four observed months and 0.995 to 1.016 with six, and a linear
  extension of the trend lands inside the bin. Where the lever is buildable (1.08 to 1.14), golden over
  default is 0.88 to 0.93, so a flat 10 per cent haircut lands. Clearing 10 and 20 per cent together needs
  about 0.85, which only comes with S(6) near 0.57, not a plausible Marcellus first year. Older 660-ft
  pilots made unrepresentative by a different completion design do not escape: they change which subset the
  filter reads, not the lever that dial caps. Parent-child moves only the one or two edge wells of an
  eight-well pad, 3 to 10 per cent at pad level.
- **The turn-in-line forecast read against the completion group's schedule as issued, at each pad's lead
  time, against the slip read off the revised schedule** (economics-econometrics
  forecasting-forecast-evaluation, the client's real-time-vintage technique), screened at stage 1 and not drawn (prototypes
  `vintage_proto2.py` to `vintage_proto5.py`, seeds 174 to 176 fixed before outcomes).
  - It passes three screens:
    - the repeat screen: no card spends an as-issued evaluation, and the nearest precedent is the client's
      capital-grant drawdown exemplar (trap 13, a re-aligned schedule validating itself), whose fix was a
      recovered rule;
    - the method screen: lead windows of half a month to a month and a half, a piecewise or straight
      regression on lead, and the volume at the mean slip against the expected volume all sit within 0.3 to
      1.1 per cent of the golden;
    - the estimand screen: the expected volume against the volume at the mean slip is 0.1 to 0.3 per cent,
      with the last planned date by early September.
  - It fails on the margins the noise allows, and the dial is the same as the spacing driver's. With delays
    accruing 10 days a month beyond four months' lead and 2 inside, the golden's equivalent flat slip is 69
    to 80 days across seeds, and the cheap routes sit close to the golden:
    - a flat two-month slip: +3.7 to +9.0 per cent;
    - a flat three-month slip: -6 to -11 per cent;
    - the slip pooled over every issue: +6.8 to +17 per cent.
  - Sigma over pads is 1.3 to 2.3 per cent, so no bin both clears those routes by a bin and holds the golden
    within one sigma, a quarter-bin from its edges.
  - Only a delay process with gamma shape 4, more regular than drilling and frac delays run, brings sigma to
    0.9 per cent. More long-lead history lowers sigma but pulls the pooled route toward the golden (+2.4 to
    +3.8 per cent at 14 days a month).
- **Redraw of 2026-10-19, education-learning-sciences / learning-analytics-early-warning-models.** Each line is
  one candidate, written when it died; the two measured ones first.
- **An earlier alert this year pulling withdrawals forward without changing the year's total** (loss-reserving
  card 1's settlement speed-up transplanted), measured on `proto13.py` (seeds 174 to 193, 30,000 entrants a
  year, no alert in 2019 and 2020, a week-6 alert from 2021, a week-3 alert in 2026). Development on withdrawals
  to date overstates the year by 43.6 to 85.8 per cent at forecast weeks 5 and 6 (6.4 at week 8). But the field's
  own landmark model at the forecast week (logistic on the entry profile and current engagement, trained on the
  week-6 cohorts' survivors) lands within +4.0 to +7.5 per cent (sd 0.9), the week-6-era Bornhuetter-Ferguson
  within +10 to +16, and the golden is the plain entry-model sum of probabilities (-0.2 per cent, sd 1.3), the
  cell's most textbook route. The claim that re-timing leaves the total alone rests on one past event (the 2021
  introduction, post over pre 0.998, sd 0.009). The library test fails: the golden is card 1's stable-basis
  projection and the cell's own risk model.
- **The week-6 rule replayed on a history whose week-6 engagement the retired week-3 alert's coaching lifted**
  (the 2027 plan retires the week-3 alert; six faculties went live from 2022 to 2025), measured on `proto21.py`
  (seeds 174 to 193, 30,000 a year). The latest-cohort replay undercounts the 2027 referrals by 11.2 to 17.2 per
  cent (the fitted trend by 13 to 20, the last three years by 10 to 15, every year pooled by 5 to 7), short of the
  lever the bar asks. Each faculty's step at go-live is 2.7 to 4.2 points against a year-to-year sd of 0.5, so an
  event study finds it. With a drift of 0.02 a year the golden constructions split (+7.6, +10.7 and +3.9 per
  cent). The golden is the staggered-rollout card's not-yet-treated comparison.
- **The incumbent model's coached referrals depressing its measured precision against a challenger's** (a pick
  between two models at capacity): causal, and the estimand that makes the call determinate has to name the
  uncoached outcome, which sends the reader to the no-contact holdout (readability test 1); a 10 per cent holdout
  puts sigma near 2 to 3 per cent on the band's uncoached rate. On paper.
- **A coaching capacity cut or a coaching contract ending** (the referred band loses coaching): the lever is 29 to
  40 per cent on the band's withdrawals and 6 to 13 per cent on the cohort's total unless the effect is
  ASAP-sized, and a call about the band names the change. On paper.
- **Lead time** (the registry's withdrawal dates trail the LMS last activity, so many hits are flagged after
  disengagement): the step settles the population, withdrawers still active at the flag; filed it is a filter,
  unfiled a fork (the WHAT screen). On paper.
- **Distinct students flagged once scoring goes weekly** (a noisy score, more looks): task170's driver, and a daily
  score history replays the new cadence exactly. On paper.
- **Precision and recall at capacity carried onto a cohort whose base rate moved**: task446's invariant (error
  rates carry, the yield moves). Spent.
- **Withdrawals triggered by first-marks release, re-timed by the next assessment calendar**: a lag timed off an
  event, the class the blind readers landed today, found by an event study and close to task160. On paper.
- **Flags set by each student's phase against their own deadlines** (activity surges before each deadline):
  calendar-locked like task162, and any past alert run at the forward phase is a common-exposure subset. On paper.
- **A withdrawal hazard stationary in teaching weeks, not calendar weeks**: task46's insight (a rate stationary in
  a constructed exposure), and a weekly plot shows the breaks. On paper.
- **Optimistic predicted entry grades plugged into an entry-tariff model**: a field reading; a shift, regression
  calibration and full integration agree within a bin. On paper.
- **Missing at least one of k assessments when k rises from two to four** (heterogeneous miss propensity): the
  common-exposure subset lands it where any history has four assessments, and moments above the second are not
  identified where none does. On paper.
- **Students with at least one fail across their courses** (a student-level frailty): task143's group effect
  shared by the members. On paper.
- **A year-end chronic-absence count in a school district**: task253's and task464's count beyond a cut from noisy
  or regressed values, and a district is local_government. On paper.
- **Spring registration throttled by advising holds** (a booking curve capped by advisor slots): fails the swap test
  (patients and appointment slots read the same), and booking curves landed today. On paper.
- **Real-time against warehouse feature vintages** (courseware events arriving days late): the cell's card 1 plus a
  load-timestamp filter, a field reading. On paper.
- **Distance-learning exam sitters including the previous presentation's deferrers and resitters**: task150's
  members carried plus arrivals plus transfers. On paper.
- **Attendance-rate referrals under a sparser timetable** (a rate over fewer sessions crosses a fixed line more
  often): fails the swap test (staff attendance over fewer shifts reads the same), close to task170, and
  correlation across a student's sessions leaves the noise model open. On paper.
- **Label shift against covariate shift for a mid-year cohort under an outside shock**: the prior correction is the
  robustness card 3 itself, the shock is a dated cause, and the two shifts differ by about 15 per cent. On paper.
- **A retrained vendor model recalibrating to a falling base rate** (fewer referrals at a fixed probability line):
  with the specification filed, refitting replays the retrain exactly (rule application); without it, the
  retrain is a recovered rule. On paper.
- **Mixed-model predictions for new modules at a zero module effect** (the typical module is not the average one):
  the plain pooled logistic already returns the marginal rate, so only a correcting solver goes wrong. On paper.
- **Redraw of 2026-10-19, product-analytics / retention-cohort-lifetime-value-modeling, the number's last cell by the
  author's rule.** Each line is one candidate, written when it died; the two measured ones first.
- **Users on group plans whose exits are mostly their plan's** (a member leaves when its plan cancels, on the plan's
  own age, or on its own tenure), measured on `protoQ1.py` (seeds 174 to 183, about 150,000 users on plans whose
  hazards are heterogeneous and fall with the plan's age, late joiners going into old plans). The user-level
  Kaplan-Meier by each user's own tenure, the cohort-retention default, lands within -0.3 to -0.9 per cent (sd 0.3)
  of the users still on a plan a year on, and the trailing year's exit rate within -1.6 to -1.9; only the
  plan-level curve with every member staying misses (+11 to +16). The join process is steady enough that the users'
  own curve already carries their plans' ages.
- **Committed plans billed monthly, whose cancellations wait for each subscriber's commitment end, after a spring
  upsell moved a block of monthly subscribers onto the plan**, measured on `protoQ2.py` (seeds 174 to 179, a 30 per
  cent spring upsell). The subscription-tenure curve by plan undercounts the next three months' cancellations by
  11.8 per cent (sd 0.7) and the trailing three months by 12.3, short of the bar's lever, while the curve by time on
  the current plan, the cheap route any plan-level analysis builds, lands at -0.3 (sd 0.9); at a 10 per cent upsell
  the default misses by only 1.7.
- **Seat headroom on per-seat business plans** (expansion is the user growth an account's unused seats cannot
  absorb): task165's driver, a gain conditioned on each unit's own baseline, in other nouns. On paper.
- **A promotional first term's cliff at its first renewal**: task137's driver (units a temporary premium brought in
  take the costly path at the first repricing). On paper.
- **Banked credits drawn down before a cancellation**: task161's driver (a stock leaves only as each holder uses its
  own). On paper.
- **Involuntary churners and win-back returners coming back**: task157's return wave and task134 v2's hazard by time
  since entry. On paper.
- **Card expiry as the involuntary clock**: no forward wave in a steady book, since cards' remaining validity at
  sign-up is spread over about five years. On paper.
- **Renewal-month seasonality and auto-renew-off reversals**: each a stratification on a visible column, the
  opponent's reflex. On paper.
- **The heterogeneity model fitted to every exit reading a flat involuntary floor as heterogeneity**: inside the
  record's tenures the error is a few per cent, and the long-horizon value it moves is an extrapolation whose family
  the data do not close. On paper.
- **Purchase regularity against the buy-till-you-die models' Poisson purchasing (non-contractual value)**: last year's
  recency-by-frequency cells, a filter and a divide, land, and beating them needs a regularity mix shift that only a
  visible category produces. On paper.
- **Payday-locked payment failures on month-end renewal days**: calendar-locked like task162, the lever modest and its
  sign set by the retry schedule. On paper.
- **Device-age wear-out of hardware-linked subscriptions, read on the device file's clock**: collinear with
  subscription tenure except through replacements, which dilute it. On paper.
- **Exits driven by contracts, regulation or partners** (renewal-reminder laws, cooling-off rights after renewal,
  bundle partners, payment-method sunsets, operating-system support drops): each a causal or rule step sized from a
  single past event, with causal_design blocked by task249 v4. On paper.
- **Rebuild of 2026-10-23, biomedical-clinical-research / survival-time-to-event-analysis (Forecasting).** Each line
  is one candidate, written when it died; the two measured ones first.
- **A trial whose first months drain a waiting pool of indolent patients before the incident flow arrives** (the
  backlog at trial opening, each patient's tempo rebuilt from the prior-therapy dates), measured on `s1_backlog.py`
  (seeds 174 to 183, 700 patients, forecast PFS events in the 12 months after the cut among those event-free). The
  pooled piecewise-exponential projection lands at -5.6 per cent of the truth (sd 6.8), an enrolment-period
  covariate at +5.7, the waiting time or first-line PFS as covariates at -5.4 to +4.8: the pooled curve by time
  since randomisation already carries the survivor mix at each time, so the lever is under the noise.
- **Registry entry at a worsening episode, so left truncation's quasi-independence fails** (hazard by disease
  duration times a spike after each episode, members entering at their first episode after the registry opens),
  measured on `s3_entry.py` (seeds 174 to 177, 21,000 members alive at the cut, about 3,000 deaths in the year).
  Time since entry +6.5 per cent (sd 2.7), left-truncated by duration +7.1, time since entry with duration at entry
  -4.7, both clocks -0.4: every route inside 7 per cent, because the later, unrecorded episodes are stationary and
  carry most of the spike.
- **A transient hazard after a formulation switch, with every remaining patient switched in the window**: the rates
  in the months after past individual switches are the attaining subset and the golden at once; turned round (past
  switch transients inflating the record) it is a staggered programme an event study finds, and the swap test reads
  the same with an app release. On paper.
- **Scan-detected progression under a forward imaging-interval amendment**: in steady state detection equals
  occurrence, so the lever is the extra mean delay (about a month on a ten-month trigger, near 10 per cent); a short
  window right after the change is the schedule executed (rule application), and the amendment names the step. On
  paper.
- **Annual-visit endpoints with bunched enrolment** (an event recorded only at a visit on the randomisation
  anniversary): task162's restart-burst driver in clinical nouns, and the history's event dates show the anniversaries.
  On paper.
- **The manufacturing wait before a cell therapy infusion shortened, with pre-infusion deaths competing**: the
  cause-specific hazard recombined under the new wait is the textbook competing-risks move, and closing or
  shortening a competing route is task169's driver. On paper.
- **Delayed events after a forward treatment-duration cap**: the early stoppers' off-treatment person-time is the
  attaining subset, and the cap puts the question in the premise. On paper.
- **A hazard by time since the last dose under a forward dosing-interval change**: the interval is the premise, the
  delayed doses are the attaining subset, and the step is exposure-response, another task type's. On paper.
- **Post-progression therapy uptake rising over calendar time**: a causal effect of subsequent therapy read from
  observational post-progression data, sized against a diffusion curve whose extrapolation forks, and next to a
  dated approval. On paper.
- **Crossover permitted after the PFS analysis**: no data before the amendment measures the crossover effect on
  post-progression survival. On paper.
- **Winter excess deaths in an elderly heart-failure trial**: calendar-locked (task162, task178), the excess 15 to
  25 per cent of a winter quarter, short of the bar and readable on a calendar plot. On paper.
- **A cure plateau** (mixture cure against a Weibull tail): the early cohorts' tail publishes the plateau and a
  piecewise-exponential fit lands (the common-exposure subset). On paper.
- **A biomarker that marks the cured** (MRD or ctDNA at a landmark): with exchangeable cohorts it is precision, not
  bias. On paper.
- **OS events conditioned on each patient's current progression state** (illness-death against the OS curve):
  unbiased without a shift in the state mix; precision only. On paper.
- **A randomisation-ratio change by amendment under blinded event prediction**: the arms' mixture moves the pooled
  hazard by about 9 per cent at a hazard ratio of 0.6. On paper.
- **Secular improvement read by period against cohort analysis**: period analysis is a trailing-window filter, the
  opponent's reflex, and extrapolating the trend forks on the window. On paper.
- **Background mortality for an ageing cohort** (relative survival): 10 to 15 per cent over a two-year window, and
  attained age with delayed entry is the default. On paper.
- **An effect on the excess hazard transported to a younger population**: about 10 per cent from a proportional
  model with age. On paper.
- **Recurrent events** (frailty, event dependence, recency after a discharge): the time-indexed mean cumulative
  function with death as the terminal event is the default and unbiased for the current cohort; a population
  entering at discharge is the attaining subset. On paper.
- **Two data cuts back-testing the parametric extrapolation** (the HTA route): a filed selection criterion makes the
  choice executable, and extrapolated means fork across the families. On paper.
- **The hazard ratio the final analysis will report under non-proportional hazards**: the late-time ratio rests on
  few events (the variance screen). On paper.
- **A funding cap on IVF cycles moved from three to six**: the self-funded continuers past the cap are task268's
  informative censoring by state, or the cycles beyond are extrapolated. On paper.
- **Induction at a gestational-age cap moved earlier**: task172's deadline that cuts the wait. On paper.
- **Paired grafts from one donor, or two eyes of one patient** (shared frailty): task143's shared group effect. On
  paper.
- **OS follow-up capped two years after treatment stops, with the cap lifted for the final analysis**: censoring tied
  to the clinical state at discontinuation, task268's informative censoring. On paper.
- **Rebuild of 2026-10-23, second cell: marketing-consumer-research / media-reach-frequency-audience-measurement
  (Forecasting).** Each line is one candidate, written when it died; the measured one first.
- **A tighter weekly household frequency cap on a guaranteed streaming buy, the impressions it takes from heavy
  households re-served to the households under it**, measured on `cap1.py` (200,000 households, gamma-Poisson ad
  opportunities): where the buy still fills, the cap lifts four-week reach by 12 per cent and three-plus reach from
  50.6 to 65.2 per cent, a real lever; tighter settings leave the buy unfillable. It dies on the
  `binding_constraint` pincer: where the re-serving goes is the ad server's mechanics, so filed it is rule
  application (cap, pacing, guaranteed fill executed on each household's opportunities) and unfiled it is a hidden
  rule recovered from past delivery or a fork between re-served and lost impressions.
- **A plan bought in a few high-rated tentpole spots against a reach curve fitted on many low-rated ones**: the
  respondent-level schedule simulation on last year's analogous programmes is the field's own planning route, so it
  is the default, not the stump. On paper.
- **Cross-media duplication from a fused TV and digital dataset whose matching attenuates the correlation**: the
  file's own documentation names the fusion (a reading), and the true single-source calibration panel is the
  attaining subset. On paper.
- **A twelve-week flight against four-week continuous panel spans** (the beta-binomial extended without audience
  turnover): the panelists in tab for twelve weeks are the attaining subset, reweighted by the panel's projection
  weights (card 4). On paper.
- **Next season's guarantee for a show whose audience a late streaming release swelled with new viewers**: retention
  by each viewer's tenure with the show is task134 v2's hazard by time since entry after a surge filled the pool. On
  paper.
- **Renewed shows regressing after being renewed for strong ratings**: regression to the mean in a selected unit
  (task130 v3 landed), and the historical change among renewed shows already carries it. On paper.
- **A show moved behind a weaker lead-in** (inherited audience against loyal audience): audience flow from the
  respondent-level panel is the field's textbook, and splitting the audience into two sources is
  decomposition_attribution, banned against task169. On paper.
- **Cord-cutting concentrating the remaining TV audience in heavy viewers**: about 7 to 9 per cent on reach at fixed
  GRPs, and projecting who leaves next forks on the trend. On paper.
- **A new ad-supported tier taken mostly by light streamers**: the pilot market's ad-tier households are the
  attaining subset. On paper.
- **Device reach converted to people reach through a device graph as the plan moves to mobile**: the single-source
  panel's person-device links are card 1's textbook route, and a single conversion ratio is the one-number screen. On
  paper.
- **On-target reach of a modelled audience segment**: the segment's error rates carry and its yield moves with the
  base rate, task446's driver. On paper.
- **A rising ad load or a sold-out peak hour capping a platform's opportunities**: a filed capacity, so rule
  application, the same pincer as the cap. On paper.
- **Rebuild of 2026-10-23, third cell: healthcare-delivery-health-economics / utilization-access-demand-forecasting
  (Forecasting).** Each line is one candidate, written when it died; the measured one first.
- **Spontaneous resolution while waiting, with a 2027 pathway guaranteeing a first appointment in three weeks**
  (procedures per referral rise once fewer patients resolve before they are seen), measured on `wait1.py` (seeds 174
  to 179, 40,000 referrals): historical conversion -25 per cent, a real lever; but the patients seen within six
  weeks in locum spells (5 per cent of referrals) land at -3 to -5 per cent (the attaining subset, which the premise
  points at), the current-status logistic forks between log wait (-3 to -4) and wait (-12) where that subset is thin,
  and a drain while waiting is task148's driver.
- **Patient-initiated follow-up replacing scheduled reviews**: flares that fall in the weeks before a scheduled visit
  wait for it, so the unscheduled contacts understate the flare rate; that is task169's driver (one route pre-empting
  the other, the change closing it) in outpatient nouns. On paper.
- **A referral requirement removed** (self-referral to physiotherapy or audiology): the self-referral propensity is
  never observed before the change; a pilot area is the attaining subset and a literature uplift the default. On
  paper.
- **A deductible or copay change read through the spot price each member faces in the year**: the response by
  deductible status is the dynamic-incentive identification the literature contests (a fork), and averaged it is the
  default elasticity. On paper.
- **A site closure redistributing patients by travel time with distance decay**: reads the same for a store closure
  under a Huff model (the swap test). On paper.
- **A new site inducing demand along the distance-decay curve**: the same swap, and the areas already at short
  travel times are the attaining subset. On paper.
- **ED streaming of low-acuity arrivals to a co-located GP service**: the streamed share is the triage rule executed
  (rule application), and induced attendances are sized from a pilot. On paper.
- **Telehealth reimbursement ending**: the share of telehealth that substituted for in-person visits, read from
  staggered practice adoption, is the not-yet-treated card (the default; proto21 died on it). On paper.
- **A shorter booking horizon cutting did-not-attend losses**: the premise names lead time, and short-lead bookings
  are the attaining subset. On paper.
- **Readmissions removed with the index admissions an avoidance pathway diverts**: readmissions per index admission
  of the diverted type is one group-by. On paper.
- **The follow-up cascade after first-appointment capacity rises**: a delay-kernel convolution, generic under the
  swap test, about 15 per cent in-year. On paper.
- **Time to death against age** (the red-herring hypothesis): about 2 per cent a year from mortality decline; a
  larger lever needs a dated mortality shock. On paper.
- **Adverse selection when a high-deductible option is added**: who switches is sized from another employer (the
  attaining subset) or a choice model (a fork). On paper.
- **Case management for frequent attenders**: regression to the mean in a selected unit (task130 v3 landed), and
  shrinkage is the reflex. On paper.
- **Delayed transfers of care after new step-down beds**: a queue on a filed capacity, the binding_constraint
  pincer. On paper.
- **Screening invitations on a rolling round plan**: the round plan is filed (rule application) and calendar-locked.
  On paper.
- **Rebuild of 2026-10-23, fourth cell: general-statistics-data-science / regression-classification-model-diagnostics
  (Forecasting).** Each line is one candidate, written when it died; the measured one first.
- **A motor insurer's direct-book frequency model on a telematics onboarding score (the average of a driver's
  daily scores over the days driven in a two-week assessment) carried to drivers bound through a comparison site,
  whose driving sits well below the direct book**, measured on `me1.py`, `me2.py`, `tel1.py` and `tel2.py` (seeds
  174 to 181, 80,000 direct drivers, 8,000 comparison-site drivers, daily-score noise three times the spread of
  true driving). The cross-validated textbook model files -26.8 per cent (sd 0.8); the slope freed of the daily
  scores' noise with each new driver read against the new book's own spread lands at -0.1 (sd 2.2) with the prior
  conditioned on the rating factors and -3.2 pooled; the data reveal the noise through the slope steepening with
  driving days. A real lever, and it died on the abstraction test: task262 already ships the insight (a reliability
  ratio is a property of the population, the noise variance carries, so a ratio taken from one population
  misprices another), and the forecasting version's extra lever (shrinkage toward the record's mean) is the same
  conditional expectation. `guard.py check` put task262 nearest at 0.12, and the draft card also BLOCKed on the
  window (composition_mix and a filing as the forcing event against task175, registered while this was screened),
  which a redraw clears; the driver does not. Never registered.
- **A score's version or device changing for the new population, with a dual-device sample**: a filed conversion
  (rule application) or the same reliability insight (task262). On paper.
- **New customers' features averaged over one month of history against twelve in the record**: covariate noise
  again, task262. On paper.
- **Outcomes recorded only for the units an earlier decision let through**: task141's selective labels. On paper.
- **A classifier's yield carried to a population whose base rate moved**: task446. On paper.
- **A new group's members sharing an unmodelled group effect**: task143. On paper.
- **A log-scale regression's retransformed mean**: task135 architecture 1. On paper.
- **The old model's own intervention depressing the labels above its threshold** (the programme ends forward): the
  untreated risk above the threshold is never observed, the effect at the threshold is a regression discontinuity
  whose bandwidth and extrapolation fork, and the programme's end names the step. On paper.
- **A forward population beyond the record's predictor range**: no unit reached it and nothing forces the
  functional form, so the method forks. On paper.
- **Two covariates collinear in the record and decoupled forward**: unidentified in the record by construction.
  On paper.
- **A top-coded covariate meeting an uncapped forward feed**: the pile at the cap is visible, and the tail above it
  forks on its form. On paper.
- **Target leakage, a feature built over the outcome window**: the feature's own definition settles it (a reading),
  and the as-of rebuild from the logs is the attaining subset. On paper.
- **Rebuild of 2026-10-23, fifth cell: actuarial-science-insurance / pricing-ratemaking-credibility (Forecasting).**
  Each line is one candidate, written when it died; the measured one first.
- **Credibility on territory risk that drifts year to year** (older experience years worth less than Buhlmann's
  equal weights), measured on `cred1.py` (seeds 174 to 183, 40 territories, six experience years, forecast two
  years out): mean absolute error on the log frequency 0.0517 for the equal-weight five years, 0.0393 for the
  local-level filter fitted by likelihood and 0.0409 for the trailing two years; the lever is about 3 per cent per
  territory and the trailing reflex lands within 0.002 of the golden.
- **A deductible raised or lowered**: losses between the two deductibles are recorded (the attaining subset) or lie
  below every recorded loss (the censored and truncated severity card, then an extrapolation), and the small claims
  policyholders absorb near a deductible are task270's driver. On paper.
- **Accident forgiveness added**: task270's absorbed small claims released, the same driver reversed. On paper.
- **A workers' compensation retroactive period moved**: durations bunched past the retroactive day are an
  incentive response in task270's family, and the counterfactual density forks on the bunching estimator's
  polynomial and window. On paper.
- **A no-fault monetary threshold moved**: the same bunching, the same fork. On paper.
- **Limits raised**: increased-limits factors from a severity fit censored at the old limit (the card's default),
  and the policies already at the higher limit are the attaining subset. On paper.
- **Roofs moved from actual cash value to replacement cost**: each claim re-paid on the depreciation schedule (rule
  application), and whether claims closed without payment enter is the population (the WHAT screen). On paper.
- **A coverage made mandatory, so the former decliners buy**: selection on recorded attributes leaves the buyers with
  the decliners' profile as the attaining subset, and on unrecorded ones it is unidentified (task141's selective
  record). On paper.
- **New business stopped in a territory**: tenure is a rating variable, and the renewal policies are the attaining
  subset. On paper.
- **A pay-per-mile product drawing low-mileage drivers** (frequency concave in miles): the existing low-mileage
  drivers are the attaining subset, and frequency against miles is the product's own premise. On paper.
- **A large rate change re-sorting who renews**: past renewals offered similar increases are the attaining subset,
  and increases beyond them extrapolate the elasticity (a fork). On paper.
- **An experience-rated group whose membership turned over**: removing departed members' claims and pooling shock
  claims is standard practice, and the continuing members' own experience is the attaining subset. On paper.
- **A per-occurrence deductible replacing a per-claim one**: grouping claims into occurrences is identity resolution
  (a reading) or a catastrophe code (a rule). On paper.
- **Named-driver cover widened to any driver**: the claims denied for unlisted drivers re-paid, rule application. On
  paper.
- **Claims-made cover priced from occurrence experience**: task130. On paper.
- **Rebuild of 2026-10-23, sixth cell (chosen by this build): actuarial-science-insurance /
  reserving-development-triangles (Forecasting).** Each line is one candidate, written when it died; the measured one
  first.
- **A fixed per-claim limit that severity inflation has brought within reach of most recent claims**, measured on
  `lim1.py` (seeds 174 to 177, 15 accident years of 400 claims, 7 per cent severity inflation, a 50,000 limit): the
  volume-weighted chain ladder overstates the future paid of the open years by 36 to 47 per cent against the
  claim-level projection capped at each claim's remaining limit, a large lever. It dies on the abstraction test: a
  per-unit ceiling that cut only the older record's largest units and now binds for most forward units is task172's
  driver, and reserving by limit band (the leveraged effect of inflation on a fixed limit) is the field's practice.
- **Net reserves under a per-claim excess-of-loss retention**: the same cap, and the treaty terms are applied claim
  by claim (rule application). On paper.
- **Large-deductible recoverables billed back to the insured**: min(paid, deductible) per claim, rule application.
  On paper.
- **Litigated claims settling at their scheduled trial dates, with a court clearing its backlog in 2027**: each
  claim's own date setting its payment is task172's per-unit deadline. On paper.
- **Periodic-payment orders paying an indexed annual amount for life**: the schedule times survival is an annuity
  calculation (rule application), and separating them from the triangle is the population (the WHAT screen). On
  paper.
- **Future payments re-inflated at a forward wage or medical index**: deflating each payment by its date's index,
  developing in real terms and re-inflating is the inflation-adjusted chain ladder, a textbook method, and the
  forward index is a filed assumption. On paper.
- **Reopened claims after a closure drive**: the closure-rate change is the Berquist-Sherman card, and the reopening
  echo of a synchronised closure is task157's wave. On paper.
- **Formula case reserves replaced by adjuster estimates after a set number of days**: case-reserve adequacy, the
  Berquist-Sherman card's incurred half. On paper.
- **Shock claims inside the triangle**: removing large losses and loading them separately is standard practice. On
  paper.
- **A shift in the report-lag mix within accident years**: composition on a recorded attribute (the report date), and
  the claims with the forward lag profile are the attaining subset. On paper.

- **Second rebuild pass (2026-10-23), the cell left to the build.** Shape first (task175's finer-grain covariate chosen
  by fit, task169's structural estimand), the parallel rebuilds' cells and this round's dead cells excluded, the stage
  4 law (a channel or correction the field teaches is applied unprompted) read first. One candidate on code, the rest
  on the structural screens:
- **New graves a municipal cemetery must provide in 2027 after double-depth graves stopped selling in 2016, reopenings
  using no new plot** (municipal-service-demand-resource-allocation; `r2/cem1.py`, seeds 174 to 179): the reopening
  stock drains smoothly, so the first-interment trend since 2016 files 0.95 to 1.12 of the truth, the last three
  years 0.88 to 1.07 and burials times the recent first-interment share 0.91 to 1.07, every rival inside the year's
  own noise. No lever: a smooth drain is matched by trend at a one-year horizon. Dead on code.
- **Votes at 16: the first council election open to 16- and 17-year-olds, read on the 18- and 19-year-olds who live
  with voting parents** (election-polling-forecasting): with a 16-plus precedent election in the record, the
  all-age turnout ratio carried onto the precedent's 16-17 turnout reproduces the household-concordance golden
  (teen turnout is q0 plus (q1 - q0) times the parents' turnout, so its ratio across elections is the parents'
  ratio); without one, the step from 18 to 16 is a behaviour the record never shows, and the at-home argument is the
  votes-at-16 literature's own, a channel the field teaches. Its abstraction (an outcome read on a household context
  the forward units all share) is task175's contagion in household nouns. On paper.
- **A new estate's ward turnout read on each elector's time at the address, rebuilt from the register's monthly
  change files**: the field's habit model already carries a category for electors not on the previous register at
  the address, which is the recent-mover group, so the habit reflex lands within about 10 per cent. On paper.
- **Breaks on the mains left after a renewal programme that replaced the segments with the most breaks**
  (asset-condition-maintenance): the remaining segments' own history is low by regression to the mean and the cohort
  rate high, but a Poisson regression on prior breaks over a time split is the field's standard pipe-break model and
  files the golden, and regression to the mean is a taught correction. On paper.
- **Main breaks read on pump starts under a 2027 night-tariff pumping schedule**: pressure transients are a channel
  the water industry names, the schedule replays on the start log, and per-start against per-hour exposure reads the
  same for a standby generator (task170's seventh-cell law; the swap test fails). On paper.
- **Main breaks after a 2027 fibre rollout's trenching, read on the trench's lateral offset from the main**: the
  street works register carries the promoter, and stratifying the past works by promoter (gas in the carriageway,
  telecoms in the footway) is the careful reader's group-by, which lands. On paper.
- **Pothole repair jobs once a 2027 contract makes every repair permanent, the record's jobs mostly re-failures of
  temporary patches**: the contract names repair durability, and linking each job to its location's previous patch
  replays the forward rule on 2026's record, which is the golden. On paper.
- **Pothole damage claims against the council under a five-day repair standard, read on open defect-days times
  traffic**: claims proportional to days open times flow is log-additive, so a Poisson regression on the two obvious
  covariates lands exactly. On paper.
- **311 calls offered after added call-takers cut abandonment, abandoned callers' retries one need**: tickets barely
  move (the golden sits within a bin of carrying the record forward), the calls version needs the forward wait from a
  queueing model whose forms fork, and patience drain is task148's driver. On paper.
- **Births to a labour-migration wave read on time since arrival**: elevated fertility after migration is the
  migration-fertility literature's own finding and a hazard by time since entry (task134 v2, task468, task173's cell
  2 deaths). On paper.
- **Ridership at a transit extension's stations read on the street-network walk catchment; EV charger use read on
  nearby registrations; garden-waste take-up read on garden area; shaded or north-facing roofs in a second solar
  wave**: each is task175's rollout-to-where-demand-was with the grain chosen by fit (a clone), or a channel the field
  names on sight. On paper.
- **Orphaned policies lapsing after a tied agency force is disbanded; primary-banking against rate-chasing savers
  after a rate cut; heat-network take-up at each home's boiler age; SaaS upgrades read on recent seat growth**: each
  is a channel the field names, measured as soon as the file that carries it is seen (task177 v3's death).
  On paper.
- **Adoption read on adopted frequent collaborators after a rollout from enterprise to small plans**: task144's
  exposure to adopters on task175's rollout skeleton. On paper.
- **Scaling-law forecasts (intermediate checkpoints, non-embedding against total parameters, repeated tokens)**: the
  cards' textbook, and the fits fork at a loss precision of 0.01. **A contingency reserve at the 95th percentile of a
  clustered total**: task142's independent unit. **Weighting a poll to recalled against recorded past vote**: a
  choice between two columns, a reading. **A conjoint share under store-level assortment**: the distribution-weighted
  simulator is practice. On paper.

- **Third rebuild pass (2026-10-23), the cell left to the build, shape first (rb-task174s).** Window at the screen:
  task173, task179, task275 (`causal_design`, `composition_mix`, `population_selection` banned). All on paper:
- **Stress-testing-capital, joint default of multi-product borrowers after a cross-sell** (one borrower's default
  charges off a card and a personal loan): expected loss is additive over accounts whatever the joint structure, so
  only the tail moves; the variance-only screen fires and a scenario's expected loss has no lever. On paper.
- **A large jump-off delinquency pipeline after a bad 2025 vintage under the 2027 adverse scenario**: the roll-rate
  (flow-rate) model on the delinquency buckets is the field's standard retail stress method and lands; the top-down
  loss-rate regression is the default path but not the stump. On paper.
- **First-year losses small because defaults lag unemployment and charge-offs lag defaults by foreclosure regime**: a
  distributed lag chosen by AIC is the taught construction, and the charge-off clock is accounting the record shows by
  state. On paper.
- **Double-trigger mortgage default under a 30 per cent house-price fall**: the mortgage-default literature's own
  model, and indexed current LTV is a two-column join the loan-level logit carries. On paper.
- **Collections capacity binding when delinquencies triple, cures falling with contacts per account**: the dialer log
  is a single-purpose file that names the channel, and cure on contact is confounded by collectors' prioritisation, so
  the golden family forks. On paper.
- **A card book's loss rate stationary per revolving balance while a rewards launch adds transactors**: revolve rate
  is a named card metric and the mix shift is `composition_mix`, banned in the window. On paper.
- **Junior notes of A/B commercial real estate loans under the scenario**: the capital stack is the sector's core
  vocabulary and the waterfall a filed rule. On paper.
- **A cooperative moving from group to individual liability, peers' covering payments masking members' shortfalls**:
  task169's pre-empting route by abstraction (the route closes forward, the recorded outcome understates). On paper.
- **Seasonal-adjustment F, a seasonal break after a school-calendar or trading-hours law**: the last two or three years'
  monthly shares land, as the cemetery's smooth drain did, and an annual total carries no seasonal lever. On paper.
- **A lunar festival moving across months in a fictional office's monthly series**: task162's calendar-locked wave.
  On paper.
- **Late responders' growth against the flash estimate**: a revision nowcast that retags to data quality, and
  imputing the large missing returns from their own history is the careful reader's move. On paper.
- **Dwelling completions lagging consents by building size after an apartment surge**: building type is a consent
  column, the per-type lag a two-column construction, and the pipeline in flight is task77's. On paper.
- **Withholding receipts in months with a third fortnightly payday**: task102's calendar, a few per cent. On paper.
- **Urban forecasting, passenger incidents per stop departure under a stop-consolidation redesign**: a Poisson on
  vehicle-km and stop departures, both read off the timetable feed, is a two-column regression that lands, and
  per-start against per-km reads the same for any fleet (the swap test fails, task170's seventh-cell law). On paper.
- **Boardings against linked journeys under a grid redesign that adds transfers**: linked and unlinked trips are the
  industry's vocabulary, and the golden needs path choice on the new network, whose rules fork. On paper.
- **Delivery stops per building rather than per household for a high-rise area**: obvious in the trade and carried by
  the stop log. On paper.
- **Redevelopment read per ownership assemblage of contiguous same-owner parcels**: task175's lots-and-permits world
  with a grain chosen by fit (a reviewer reads one project), and lot area already proxies the assembled size. On paper.
- **Turnover in a newly let development whose movers select into new homes**: a hazard by time since entry (task134
  v2), the timing exposure. On paper.
- **Group-quarters residents after a dormitory opens, missed by the housing-unit method**: the method's own standard
  correction. On paper.
- **Health-burden, a PIF on the individual exposure distribution against group means under a curved relative risk**:
  the lever is the fitted curvature's own sensitivity; **first-year burden after an exposure change read on time since
  the change**: a timing exposure and the named cessation lag. On paper.
- **Infectious (fictional, subcritical, every chain seeded by an import) after a new direct air route**: cases per
  import times forward imports is a filter and a divide, a regression of cases on lagged arrivals lands, and
  elimination-setting branching is the field's named model; contagion world besides (task144, task175, task501). On
  paper.
- **Recidivism: churn under shorter revocation terms and time at risk net of jail days**: task169's world and
  act-driven shape, street time a named correction; **exclusion-zone breaches read on home-to-victim distance**:
  `composition_mix` and the GPS traces replay any radius; **the controlling sentence across concurrent sentences**: a
  sentence-computation term carried by a column. On paper.
- **Distinct units with at least one event after a programme thins events at random**: the thinning identity over
  each unit's own count is one group-by (rule application by arithmetic) and fails the swap test. On paper.
- **Social relets set off by a 2027 completion wave through vacancy chains read on linked address histories**: the
  chain is the housing literature's own construct, the direct transfers into new affordable homes are obvious, and the
  private-market chains that reach a social tenancy inside the year are rare, so the lever over the relet trend is a
  few per cent. On paper.
- **Architecture 2 draw, 2026-10-28: the call as the pick of the spring unit with the most failed checks.** The
  replay of homework completion names the same flat unit as the golden (the flat skill builder also leaves the most
  students unfinished at the close), so a pick is landed by the plainest route; the call became the set length
  against funded places, where each route files a different length.
- **Architecture 2 draw, 2026-10-28: a homework cap of fifteen problems a day.** It puts the check inside the
  observed sitting length, but problems 9 to 13 of the log then sit in the first sitting for most students who
  reach them, and that replay lands within about 18 per cent of the golden at eight problems, so a funded-places
  line between them leaves no room; the cap stays at ten, Rungwell's documented limit.

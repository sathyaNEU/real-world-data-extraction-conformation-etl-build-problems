# task156: Millrind's 2027 paid moderation pool, nine sites behind a closing volunteer review community (architecture 1, loop 3)

Private, never ships. A new build (wave 5), numbered from seed FC27, shipped 2026-10-17 and returned by the portal
on 2026-10-27: both responses landed the call (35 FTE, the then golden), building each site's capacity against its
inbox at the saturated pace and carrying each pool at its own lapse rate with almost no new reviewers. That route was
the build's decisive step, so the capacity framing is now the default path, not the stump. Loop 3 moves the decisive
step to how the pool is carried: the reviewers differ, most new reviewers review casually and stop within months while
a steady core stays for years, and since 1 September 2026 review access is by invitation only, so the 2027 pool is a
closed pool shedding its newest reviewers first. The world, decision, quantity, prompt, deliverables and all three asks
are kept; the review platform's data dictionary, the file list and the two markdown notes are gone (every export names
its own columns; the operations handbook and the data platform team's question count standard carry the conventions
the asks and the chart need). The seed's two banned features stay out (no certified need table, the revised close
standard filed as context).

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task156.json`, architecture v1 loop 3, the loop 1 to 2 identity in `lineage` (solved on the portal); `guard.py check` and `heart` run on the re-registered card (Guard below) |
| Domain / task type | `product-analytics`, task type `retention-cohort-lifetime-value-modeling` (serves Forecasting): the deciding quantity is the 2027 survival of a volunteer reviewer cohort that has stopped taking in members, carried on survival by tenure, as product analytics forecasts a closed user cohort's retained activity |
| Objective | Forecasting & Predictive Modeling: each site's paid review hours in calendar 2027, a year not begun at the as-of date (Friday 9 October 2026), built from the network's own inbox, reviewer and flag history and its 2027 question plan |
| Shape | `other`: the pool to request with its nine site needs, the gap to finance's envelope, a council slide charting the network's monthly paid hours with 2027 forecast, and row-set asks on rows the call never reads |
| Decision | `quantity_figure`, answer unit `count` (FTE: each site to the nearest whole FTE, the request their sum) |
| Mechanism | population then time (decisive: the pool's overall lapse rate is the rate of an open pool full of newcomers, not the rate of the closed 2027 pool, because stop rates fall steeply with tenure; the roster opens in January 2024, so the tenure curve needs each reviewer counted from the month the record first sees them); generators G6 (composition shift: the pool's tenure mix ages once grants stop), G9, G16; Gate G `forecasting`; strategy `population_selection` |
| Layer 2 family / pattern | `estimation_fit` (survival with left truncation and heterogeneous hazards); `own:closed-cohort-survival-by-tenure-left-truncated-against-capacity` |
| Furniture | forum `council_or_assembly` (the Moderation Council votes the request at its December sitting), forcing event `vote_or_meeting`, organisation family `software_or_platform`, role family `operations_director`, context artifact `monitoring_export`, calibration `none`, opening `question-first`, question form `how-many` (all unchanged from the draw) |
| Spine | the review platform's reviewer roster (23,148 access spells: grant date, first and last review on the platform, status, lapse date) beside its daily inbox export, January 2024 to September 2026 (36,144 rows, one per site, UTC entry day and item type); constructed |
| Deliverables | `moderation_pool_2027.xlsx` (the request, the site needs, the reviewer pools and their stop rates by tenure, the ask tables, notes) and `council_pool_request_2027.pptx` (the request slide and the monthly hours chart) |
| People | drawn with `guard.py names --geo Canada --seed 156` at the draw: Duane Zamora (head of moderation operations, the operations handbook), Natalie Maxwell (finance business partner, the envelope letter), Claudia Spence (council chair, the charter and the 2027 standards); the requester is in no file and not in the prompt |

**Guard.** Re-registered at loop 3 with the decisive step's own identity (driver, stump, strategy, Gate G, Layer 2
family); the loop 1 to 2 identity sits in `lineage` with its fate, so the similarity rules screen against the solved
driver. Results in `## Surface screen`.

**Domain tag.** `product-analytics/retention-cohort-lifetime-value-modeling` fits better now than at the draw: the
decisive quantity is a retained-user cohort's survival by tenure, the cell's own rigor pattern (heterogeneous churn,
censored and truncated cohorts), set against the queue the cohort must clear.

**Same-puzzle and same-driver tests.** Gap population and time, G6, decision `quantity_figure`, Gate G `forecasting`:
the guard's structural tests run on the re-registered card (`## Surface screen`).

**Abstraction test.** Stripped of nouns: a pool's members leave at their own steady rates, which differ widely, so the
fast leavers go first and the pool's overall leaving rate falls as its members age; while new members kept arriving the
overall rate stayed high, and once arrivals stop the closed pool sheds its newest members and then slows, so carrying
the open pool's rate overstates the losses; the record opens part-way through most members' lives, so the rate by tenure
must count each member from when the record first sees them. The nearest by mechanism, read for latent structure:
- task179 lets a member's chance of leaving fall once it meets the same peers in several groups, a forward process the
  new members no longer pass through; here nobody's chance changes, the overall rate falls only through who is left.
- task170 has a per-attempt failure probability falling with each operator's own count of attempts (learning); here a
  reviewer's stop chance is constant for life and the fall is selection, not learning.
- task176 ends units when the youngest dependant reaches a fixed age, a clock other than tenure; here tenure is the
  clock and the curve is read from the record, left-truncated.
- task134 turns a conversion hazard near zero for a member's first months into a forward inflow; here the hazard is
  highest in the first months and the forecast is the survival of a closed pool, not an inflow.
- task265 (this lane) reads a survival share from a record that began after many units had started: the left edge is
  its decisive step; here it is the second layer (R3b), under the closed pool's composition.
- task174's paused screen found that a survival curve by tenure absorbs a subscription book's stationary structure, so a
  stump needs a condition the record has not shown; here the record never showed a closed pool (grants ran at about 320
  a month to August 2026), and the default route (measured on the portal) carried the open pool's rate.
None shares the latent structure, the default path and the correction.

**Data-native sentence.** Most of Millrind's new reviewers review casually and stop within months (about 9 per cent a
month in their first year of access), while reviewers past their third year stop at well under one per cent, so while
grants ran at about 320 a month the pool's overall lapse rate held near 3 per cent; since 1 September 2026 review access
is by invitation only, so the 10,607 reviewers active in September 2026 are the 2027 pool, shedding their 2,066
first-year reviewers fast and then slowing, which the open pool's lapse rate overstates by about half; and the roster
opens in January 2024, so a tenure curve that counts every reviewer from the day access was granted reads the
survivors of older cohorts as whole cohorts and understates the losses.

**Sources read, one line each.**
- The portal's two responses (2026-10-27): both 35 FTE, the capacity built against the inbox at the saturated pace, the
  pool carried at its own lapse rate; that route is the default path.
- `guard.py mechanisms --objective forecasting` and `slots` on the candidate driver: the retention and hazard drivers on
  file (task170, task176, task179, task134, task177) and task174's paused finding, each read above.
- `layer2-rigor-patterns.md`, product analytics: heterogeneous churn and censored or truncated cohorts are the cell's
  own patterns; this build's version is a closed cohort's survival read from a left-truncated roster, with the open
  pool's rate as the easy route.

## Default path

Built figures (`generator/calc.py` on the shipped files, asserted in `generator/checks.py` and reproduced by
`generator/verify.py`). Each request is the nine site needs, each rounded to a whole FTE, added up (the charter).

1. Read the charter's need definition, the 2027 standards, the 2027 question plan and finance's 26-FTE envelope.
2. See that items reach the paid team only when the volunteers fall short, and build each site's monthly capacity
   against its inbox: the reviews a reviewer completes when the inbox outruns the pool, about 40 a month over the 402
   site-months since 2021 in which more than 5 per cent of entering items were routed.
3. Carry each site's September 2026 pool forward at its own monthly lapse rate over September 2024 to August 2026 (2.61
   to 4.35 per cent, 3.1 across the network), with no new reviewers since access became invitation-only.
4. Route each 2027 month's inbox beyond that capacity, price it and the handled flags at the 2027 standards, round each
   site to a whole FTE and add them up.

Ends on: 41 FTE (Frontend & Web 5, Mobile Apps 2, Data & ML 9, Databases 6, Infrastructure & DevOps 6, Game Development
3, Security 5, Embedded & Hardware 3, Scientific Computing 2), 15 above the envelope.

Golden: 32 FTE (Frontend & Web 5, Mobile Apps 2, Data & ML 6, Databases 4, Infrastructure & DevOps 4, Game Development
2, Security 4, Embedded & Hardware 3, Scientific Computing 2), 6 above the envelope: each reviewer active in September
2026 carried on the monthly stop rate the roster shows at their own tenure (months since access was granted, each
reviewer counted from the first month the platform shows them active, January 2024 to August 2026: 9.07 per cent a
month in the first year, 5.19 in the second, 2.23 in the third, 0.92 in the fourth, 0.53 after), no new reviewers but
invitations (none in September); the 10,607 reviewers average about 8,800 a month in 2027; the same capacity, routing
and pricing. The world's own realised 2027 gives the same nine site needs (31.69 FTE against the forecast's 32.69).

## Stump sentence

Carrying each site's reviewer pool from September 2026 at its own lapse rate of the last two years, with no new
reviewers since access became invitation-only, files 41 FTE (40 on the last twelve months' rate, 38 on the last three);
the step that lands it there is reading one stop rate off a pool that was still taking in newcomers, when reviewers stop
at about 9 per cent a month in their first year and under one per cent from their fourth, so the closed pool sheds its
newest reviewers and then slows: carried on the stop rate of each reviewer's own tenure, counted from when the roster
first sees them, the 10,607 active reviewers average about 8,800 a month in 2027 and the request is 32 FTE (27 with the
tenure curve read from each grant date, which takes the roster's survivors of older cohorts for whole cohorts).

## Three rules

- **Task type:** product-analytics, retention-cohort-lifetime-value-modeling (serves Forecasting): the deciding quantity
  is a closed volunteer cohort's survival through 2027, carried on its stop rate by tenure, times the reviews a retained
  reviewer delivers when work is plentiful, set against the inbox the 2027 plan implies.
- **Domain test:** the deciding quantity is each site's 2027 volunteer review capacity, which product analytics forecasts
  as a cohort's retained activity: survival by tenure read from a truncated, censored roster, applied to the members who
  are left, rather than a pooled churn rate; with another field's nouns the quantity stops making sense.
- **Swap:** "how many agency nurses each of nine wards needs in 2027 to cover what its permanent staff cannot" keeps a
  two-tier cover, but permanent nurses are rostered to fixed hours and replaced by hiring, so there is no self-selecting
  volunteer cohort whose members drift away at rates that differ by tenure and that stopped admitting members.
- **Layer 1:** a review-platform change in January 2024 (a monthly per-queue workbook for 2021 to 2023 beside a daily
  inbox export by item type from 2024), old site names against new codes with Graphics folded into Game Development in
  2023 (the site register), UTC days on the platform against Toronto time in the WFM records, the September 2026 export
  pulled twice (a preliminary pull with the last days still open, the full pull of 8 October), the moderator tool's flag
  export in two parts that both carry 15 August, a WFM week re-sent with its original lines kept as superseded, and the
  roster's 952 reviewers whose access lapsed in January or February 2024 without a review on the platform (first review
  blank). Each is what these systems write; none carries the stump (`checks.py` R2a to R2e, the access-holder reading).
- **Layer 2:** `estimation_fit`: the 2027 pool is survival by tenure from a left-truncated, right-censored roster with
  heterogeneous stop rates; the open pool's rate, the pool's trend and a curve read from the grant dates are the easy
  routes, each refuted out of sample by a back-test on the closed cohort of September 2025.
- **Decisive step:** carry each reviewer active in September 2026 on the monthly stop rate at their own tenure, the rate
  read from the roster with each reviewer at risk from the first month the platform shows them active to their last
  review, instead of one lapse rate for the pool.
- **Not semantics:** every field (grant date, first and last review, status, lapse date) is read the same way by the easy
  routes; the access-holder reading and the lapse-date stops file the same nine; no field, code or definition states a
  stop rate, a tenure effect or how many reviewers 2027 will have, and the routes that read every field correctly file
  41, 40, 38, 27, 24 or 23.
- **Not rule application:** the shipped sentences that bear on the pool (the charter's need, the 72-hour hand-off, the
  handbook's invitation-only clause) fix who can review in 2027, never how fast they stop; no filed sentence names a
  tenure, a stop rate, a lapse rate or a method (asserted: no tenure, stop-rate or retention wording anywhere in the pack).
- **Analyst test:** a strong analyst who builds the capacity right (the saturated pace, the inbox from the plan) and reads
  the invitation-only clause carries each pool at its own lapse rate of the last two years and files 41 FTE (executed on
  the generator's clean truth in `checks.py` R3a: 41, five sites off; the decisive step alone, R3b: the golden's nine).
- **Estimand:** the prompt and the Moderation Council charter (section on need): the pool, in FTE of 1,600 hours, that
  covers the hours the paid moderators will spend in calendar 2027 (UTC, each item in the year it entered the inbox and
  each flag in the year it was raised) on every moderator flag they handle and every community item that reaches them,
  including items from posts and accounts that do not yet exist, each at the 2027 handle-time standard, for each of the
  nine sites and in total, compared with finance's 26-FTE envelope; the population, outcome, window, unit and comparison
  are filed, and who can review in 2027 is filed (the handbook), the method is not.
- **No decoy:** no consultant study, prior need table, staff draft or stakeholder figure states or argues a 2027 need, a
  lapse rate, a stop rate or a pool size (asserted, R3c and HOW: the only FTE figures in the pack are the envelope and the
  2026 pool); the handbook's clause states the access rule and nothing about how fast reviewers stop.
- **No certified replay:** no certified or published need figure ships and nothing graded is reproduced from one; the
  roster is the raw record every carrying method is scored on, and the back-test on the September 2025 cohort is the
  analyst's own.
- **Lesson:** a closed cohort's losses follow its members' own stop rates, which fall with tenure when members differ, so
  the rate a pool showed while it was still admitting members overstates what it will lose once it stops, and a record
  that opens part-way through members' lives has to count each from when it first sees them.

## Readability screen

Six tests per rung (1 a filed sentence names it or sends the solver looking, 2 a column, key or marker makes it a
predicate or a header join, 3 an opponent reflex, 4 a control or corpus scores it, 5 the hygiene battery finds it, 6 one
subtraction, ratio or half of a figure). Built figures (`generator/calc.py`; the back-test is `checks.py` BACKTEST).

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 each site's paid queue hours per question over the last twelve months carried onto the plan (24) | the charter prices items and the plan gives the questions | routed items and flags by site and day | yes, the shallow default | the routed history: the B sites routed almost nothing | no | yes, one ratio | readable |
| R1 each site's routed share or paid hours trended (23) | no | the same columns | yes, the trend reflex | the same | no | yes, a fitted line | readable |
| R2 the pool trended, or carried with the last year's new reviewers (22 to 24) | the handbook's invitation-only clause rules out new reviewers | grants by date in the roster | a forecaster's reflex on a pool | the back-test and the clause | no | no | readable |
| R2b the pace read from 2026 throughput (47) | no | reviews and reviewers by site and month | the capacity-modeller's reflex | the saturated months show the pace | no | no | readable |
| R3 the closed pool at its own lapse rate of the last two years (41; 40 on twelve months, 38 on three) | no | the roster's status and lapse dates | yes: the portal's measured route | the back-test on the September 2025 cohort: 5.5 per cent short of its reviewer-months | no | yes, one rate | readable |
| R3b the tenure curve read from each grant date (27) | no | the grant date | a cohort analyst's reflex | the same back-test: 11.2 per cent over | no | no | readable |
| R4 (decisive) each reviewer carried on the stop rate at their own tenure, counted from when the roster first sees them (32) | no sentence names a tenure, a stop rate or a method; the handbook says who may review | no column carries a tenure, a type or a rate: the roster lists spells | no: the reflex is one lapse rate (the portal) | none ships: the back-test is the analyst's own | no: nothing duplicated, missing or mis-keyed on the call's rows | no: a product over each reviewer's tenure path | silent |

## Semantic fork table

Every term in the main ask and every convention the main computation needs. Every id is asserted in `generator/checks.py`.

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "FTE" | 1,600 hours of need at the standards (the charter) | 1,950 or 2,080 paid hours a year | a smaller request | the charter's FTE sentence |
| SF2 | "need" | the hours the paid moderators will spend on the items that reach them, each at the year's standard (the charter) | the hours the paid team worked in 2026 (the WFM export, 30.6 FTE a year) | 31 | the charter's need sentence |
| SF3 | "2027" | calendar 2027, each item in the month it entered the inbox and each flag in the month it was raised, UTC (the charter) | the month an item reaches the paid team; Toronto time | same call (asserted) | the charter; same call, asserted |
| SF4 | the items counted | every moderator flag a paid moderator handles and every community item routed to the paid team (the charter) | flags the platform closes because the post was deleted | a larger request | the charter's flag sentence |
| SF5 | "each of our nine sites" | the nine sites on the register, Graphics & Shaders inside Game Development since July 2023 | Graphics as a tenth site | same call (no records after June 2023) | the site register |
| SF6 | "the 2027 handle-time standards" | the council's 2027 standards (close 2.0 minutes) | the 2026 standards | a larger request | the prompt and the standards' effective dates |
| SF7 | "question plan" | the planning team's 2027 questions by site and month | a trend of each site's questions | a different request | the prompt names the plan |
| SF8 | the rounding path | each site's need to the nearest whole FTE, the request their sum (the charter) | the network's hours over 1,600 rounded once | 33 | the charter's request sentence |
| SF9 | "how far it sits from finance's envelope" | the request less the envelope, in FTE | a percentage | same call | the prompt's rounding sentence |
| SF10 | items from posts and accounts not yet written | in: the plan's questions carry them | only items on existing posts | a much smaller request | the charter |
| SF11 | the chart's history | each month's paid review hours at the standards in force then, 2027 at the 2027 standards | history restated at the 2027 standards | the chart only | the standards' effective dates |
| SF12 | the September 2026 inbox records | the full pull of 8 October | the preliminary pull of 2 October (the last days still open) | same call (asserted, R2d) | every row's pull stamp; same call, asserted |
| SF13 | the pool and its stops | reviewers active in a month (a review in the month), a stop at the last review | access holders (until the lapse date), a stop at the lapse month, the 952 pre-platform lapses among them | same call (asserted) | same call, asserted |
| SF14 | who reviews in 2027 | the reviewers active in September 2026 and anyone invited (the handbook: access by invitation only from 1 September 2026) | the last year's new reviewers carried on | 24 | the handbook's clause |

## Ladder

Built figures (`generator/calc.py` on the shipped files; every row asserted in `generator/checks.py`). Each request is
the sum of the nine site needs rounded to whole FTE (web, mobile, data, databases, devops, gamedev, security, embedded,
scicomp).

| Rung | Construction | Request | Dies to |
|---|---|---|---|
| R0 | each site's flags and routed items over the last twelve months at the 2027 standards, per question, carried onto the plan | 24 (5, 2, 4, 3, 3, 1, 3, 2, 1) | the routed history is the residue of a capacity, not a share |
| R1 | each site's routed share or paid hours trended | 23 | the same |
| R2 | the pool trended over the record or the last year (23, 22), or carried at its lapse rate with the last year's new reviewers (24) | 22 to 24 | the handbook's invitation-only clause; the back-test |
| R2b | capacity from 2026 throughput | 47 | the saturated months: throughput where work ran out is the work |
| R3 default | the closed pool at each site's own lapse rate of September 2024 to August 2026 (40 on twelve months, 38 on three) | 41 (5, 2, 9, 6, 6, 3, 5, 3, 2) | the back-test: on the September 2025 cohort it misses its reviewer-months by 5.5 per cent; the stop rate falls with tenure |
| R3b | the tenure curve read from each grant date | 27 (5, 2, 5, 3, 3, 2, 3, 2, 2) | the roster opens in January 2024: older cohorts appear only as survivors; the back-test 11.2 per cent over |
| R4 decisive | each reviewer on the stop rate at their own tenure, counted from when the roster first sees them | 32 (5, 2, 6, 4, 4, 2, 4, 3, 2) | golden |

**Position and margins.** The golden is bracketed: every share, trend, open-pool and whole-cohort route below it (22 to
27), the closed pool at its own lapse rate and the censored pace above it (38 to 47). The nearest wrong request is 27,
five FTE away; every rung's nine site needs differ from the golden's at three sites or more (asserted).

**Convergence (C1, asserted on the shipped files).** Every defensible construction of the golden files the same nine site
needs (22 constructions plus the access-holder reading and a day-by-day simulation of the 72-hour hand-off): the curve in
bands of 3, 6 or 12 months, each site's own curve, stops at the lapse month, the curve read over the last 24 or 18
months, its tail over 6 or 24 tenure months, plus or minus one standard error, a two-kind mixture fitted by maximum
likelihood (it recovers 85 per cent of reviewers stopping at 11.8 per cent a month and the rest at 0.51), invitations
dropped, annual netting, the pace at any saturation cut from 1 to 15 per cent or from either era, ratios from 2025, no
floor. The network's unrounded need runs 31.88 to 32.97 across them, and every site stays 0.16 FTE or more inside its
bin (Data & ML and Frontend & Web the closest).

**Out of sample.** A back-test on a closed cohort the roster shows month by month (the reviewers active in September
2025, followed to September 2026; `checks.py` BACKTEST): the tenure curve read on January 2024 to August 2025 misses
their reviewer-months by 0.3 per cent network-wide (worst site 3.2 per cent); the pool's own lapse rate by 5.5 per cent
short; the curve read from the grant dates by 11.2 per cent over. The test is the analyst's own, on records no document
summarises.

**Strength.** P(one strong solver lands) about 0.25: it must see that the pool's lapse rate belongs to an open pool and
that stop rates fall with tenure (the portal's two responses did neither), then read the curve with the record's left
edge. P(both land) about 0.08 if independent. The seed was fixed by rule (1561009) before any data was generated; the
covers were calibrated to centre each site in its bin with common random numbers, recorded in `## Tried and rejected`.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | every flag a paid moderator handles and every community item routed to the paid team in 2027 at the nine sites, posts and accounts not yet written included | filed (the charter's need sentence); SF4, SF10 |
| 2 | Unit of account | FTE of 1,600 hours of need at the standards, whole FTE per site | filed (charter); SF1, SF8 |
| 3 | Attribution window | calendar 2027, items by entry month and flags by raise month, UTC | filed (charter); SF3 same call asserted |
| 4 | As-of dating | data through 30 September 2026, pulled 8 October | every export's pull stamp; SF12 |
| 5 | Version basis | the full September pull | SF12 same call asserted |
| 6 | Denominator | reviewer-months at each tenure | C1: bands, own-site curves and the access-holder reading the same needs (asserted) |
| 7 | Weighting | none | n/a |
| 8 | Window length | the months the curve and the pace are read from | C1: the curve over 18, 24 or 32 months, every saturation cut, the same needs (asserted) |
| 9 | Boundary inclusivity | the 72-hour hand-off | the charter states it once; a day-by-day simulation files the same nine (asserted) |
| 10 | Rounding path | each site to the nearest whole FTE, the request their sum | filed (charter); SF8 |
| 11 | Tie-break | none | n/a |
| 12 | Maturity and censoring | reviewers still active are censored at August 2026; the roster opens in January 2024 (left truncation) | the decisive step; C1 over the curve's readings; R3b is the curve without the left edge |
| 13 | Order of operations | arrivals against capacity month by month, then priced | C1: monthly, annual and daily netting the same needs (asserted) |
| 14 | Row order | sums | C1 |
| 15 | Duplicate resolution | none on the call's rows | asserted: no duplicate key in the inbox export, the roster or the flag summary |
| 16 | Identity normalisation | old site names to codes through the register | C1: no mapping moves the pace (asserted) |
| 17 | Netting against gross | none | n/a |
| 18 | Dimensional units | minutes per item, hours, FTE | filed (standards, charter) |
| 19 | Code and status semantics | the roster's access status and lapse date | SF13: active or access holder, last review or lapse month, the same nine (asserted) |
| 20 | Integerisation | whole FTE per site | each site 0.16 FTE or more inside its bin across every construction (asserted) |
| 21 | Clause scope | the 2027 standards apply to items in 2027 | filed (standards' effective date) |
| 22 | Forward window contents | the 2027 questions and who may review | the plan (SF7) and the handbook's invitation-only clause (SF14) |

## Literal reader

Executing the prompt, the charter, the 2027 standards and the handbook word for word gives, for each site, the hours the
paid moderators will spend in calendar 2027 on every moderator flag they handle and every community item no volunteer
has reviewed 72 hours after it entered the inbox, at the 2027 standards, over 1,600 and rounded to a whole FTE, the
request their sum, with nobody reviewing in 2027 but the reviewers of September 2026 and the invited; no shipped sentence
says how many reviewers will stop, so a literal reader must forecast it, and the fork table leaves no reading under
which 41, 27 or 24 is the golden.

## Oracles

- The roster itself: on the wrong path it offers one lapse rate to carry; followed month by month, the September 2025
  cohort refutes that rate and the grant-date curve and confirms the tenure curve read from the record's left edge.
- The 2026 pool (27 FTE) and finance's envelope (26 FTE): figures the request is compared with, consistent with every
  method; neither states a need.
- The old workbook's routed history (2021 to 2023): raw records showing the pace volunteers kept when work outran them.
- No control ties only under the golden.

## Ask sheet

**Main call's declared row population:** the review platform's daily inbox export (January 2024 to September 2026,
both September pulls), the old monthly queue workbook's item, review, routed and reviewer columns (2021 to 2023), the
reviewer roster, the moderator tool's daily flag summary, the posts warehouse's monthly question counts for 2024 to
2026, the 2027 question plan, the charter, the 2027 standards, the operations handbook's review-access clause, the
site register and the envelope letter. Device and
hazard rows in it: 0 (asserted: the call reads no per-flag export, decision review, WFM line, assignment,
migration or 2022 question count). The asks read files the call never reads and share no primary device or path.

**Ask A. Each site's 24-hour flag response (the flag service standard's measure: the share of the flags raised in each of July, August and September 2026 that a
paid moderator first acted on within 24 hours** (27 figures, per cent to one decimal).
- H18 home: a component of the request's case: the service the 2026 pool held, a measure every site carries that the
  call never turns on.
- Use: the council's December paper reports it beside the request.
- Basis (filed in the moderation team's flag service standard, the owner's voice): every flag raised in the month
  (UTC), less the flags the platform closed because the post was deleted before a moderator acted; a flag counts when
  a paid moderator's first action on it came within 24 hours of the raise.
- Primary A1 (D8, an anchor on the current record, not the first): the moderator tool's flag export carries the time a
  flag was last marked handled; a flag whose decision was taken to a decision review (about 4 per cent, one to six days
  after the first action) is marked handled again when the review closes, so its export time is the review's. Fair: the
  decision-review log carries each reviewed flag's first action time and outcome. Silent: the export's time column is
  the only handling time it carries, every value follows its raise, and the reviewed flags look like slow flags.
- Hazards: HA1 the flags the platform closed (post deleted before a moderator acted; about 6 per cent, outcome
  `closed_post_deleted`, left out by the basis; kept, every share rises by about 3 points); HA2 the export pulled in two
  parts that both carry 15 August (exact duplicate rows, removed by the battery).
- Stops (built, asserted): S1 every exported row, the closed flags in (27 miss); S2 the battery's work (duplicates
  out, closed flags out, the export time as the first action; 27 miss, the nearest 2.9 points low); S3 the reviewed
  flags dropped from both counts (14 of 27 miss, the over-correction); S4 the golden. HA1 kept raises all 27; HA2
  counted twice moves 4 of the 9 August figures. No share sits on a half step, and no first action falls exactly 24
  hours after its raise.
- Span: the two export parts, the decision-review log, the flag service standard, the site register (5 files); flag id,
  site, raised at, handled at, outcome, handler, review's first action at, first outcome, review closed at (9 columns).
- Realism: a ticketing tool overwrites its resolved time when a ticket reopens and resolves again, and a quality
  programme keeps its own log of what it reviewed.

**Ask B. The hours each site's paid moderators worked in each of the first three quarters of 2026** (27 figures,
hours to the nearest hour).
- H18 home: an audit trail of the 2026 pool, where its hours went site by site, reconciled against the WFM system's own
  totals; the call prices need, never hours worked.
- Use: the council's paper shows where the 2026 pool was spent.
- Basis (filed in the operations handbook): a shift's hours count for the site the moderator was assigned
  to on the day the shift started, in the quarter it started, both on Toronto time.
- Primary B1 (D7, a field overwritten later): the WFM system's shift export joins each moderator's site from the
  moderator's current record, so the six moderators moved in July and August 2026 (from Frontend & Web, Mobile Apps,
  Data & ML, Databases, Infrastructure & DevOps and Game Development to Security, Embedded & Hardware and Scientific
  Computing) carry their new site on every 2026 shift. Fair: the assignment history gives each moderator's site with
  its effective dates. Silent: the export's site column is complete and every value is a real site.
- Hazards: HB1 the WFM system still names Infrastructure & DevOps "Ops & Cloud" (the register maps it); HB2 a corrected
  week (4 to 10 May) whose lines were re-sent, the originals marked superseded (dropped by the battery); HB3 night
  shifts starting on the last evening of a quarter (by the start day, filed).
- Stops (built, asserted): S1 by the export's site, superseded lines kept (27 miss); S2 by the export's site,
  superseded dropped (27 miss, the nearest 16 hours off); S3 by the assignment on the shift's end day (15 of 27 miss);
  S4 the golden. HB1 unmapped drops Infrastructure & DevOps' three quarters; HB2 kept moves the second quarter at seven
  sites. Every shift line is whole hours, so no total sits on a rounding edge.
- Span: the WFM export, the assignment history, the operations handbook, the site register, the moderator list (5 files);
  moderator id, shift start, shift end, hours, site, line status, effective from, effective to (8 columns).
- Realism: workforce systems export the current record's attributes onto historical lines; moderators were moved to
  the three sites whose queues grew.

**Ask C. Each site's January to September 2026 questions as a percentage of the same months of 2022** (9 figures, per
cent to one decimal).
- H18 home: a component of the case: how much each site's volume has fallen, the context the request opens with; the
  call reads no 2022 question count.
- Use: the first table of the council's paper.
- Basis (filed in the data platform team's question count standard): each question counts once, on the site it lives on now, in the month it
  was first asked (UTC); comparisons with 2021 to 2023 are made on that basis.
- Primary C1 (D1, the same records under two sources): the old monthly workbook counted a question moved between sites
  twice, on the site it was asked on and again on the site it moved to, in the month of the move; the 2026 counts come
  from the posts warehouse, which counts each question once. Fair: the moderators' migration log (2021 to 2023) lists
  every move with both question ids, both sites and both dates. Round 1 (the judge's FIX_NOW): the old job's counting is
  now filed in the question count standard in the data team's voice ("The old statistics job counted a question on every site
  it was posted to ..."), with the comparison basis, so C1 is seen and repaired from the migration log. The two readings
  the judge licensed are asserted out: the old job read as counting each question once on its posting site misses all
  nine (nearest 0.22 points), and no restatement (S2) misses all nine.
- Primary C2 (round 2; D2, a superseded cut that looks final): the tag-sync fault of 9 May to 22 August 2022 left
  questions posted through the API out of the statistics job's counts, so the 2022 sheet's May to August questions as
  first reported understate every old site, by 1.4 to 3.1 per cent of its questions in those months (the API's share
  differs by site). The job was rerun on 14 March 2023 and its restated questions sit below the sheet's notes, sites
  down and months across, labelled as replacing the counts above, on the same basis. Fair: the restated counts with the
  moves undone are the world's questions to the question (asserted). Silent: the block sits below the notes in another
  layout, so a parse of the sheet's table drops it; the sheet's subtitle still says final for the year, and its totals
  row ties to the rows as first reported. Honest: a statistics job's rerun appended to the year's report. It touches no
  review item, reviewer or flag (the call's columns).
- Hazards: HC1 Graphics & Shaders folded into Game Development in July 2023 (the register); HC2 the 2022 sheet's
  layout (a title block, old site names, a totals row).
- Stops (built, asserted): S1 the workbook as it stands, Graphics left out of Game Development (9 miss); S2 the merger
  applied, no restatement on the warehouse's basis (9 miss, the nearest 0.14 points off); S3 the copies taken off, each
  question once but on the site it was asked on (7 of 9 miss); S4 the careful-but-literal path, every filed rule and the
  migration log applied but the 2022 questions as first reported (9 miss, the nearest 0.27 points off); S5 the golden.
  Applying each move in the month it moved instead of the month asked files the same nine (a convergence, asserted).
- Span: the 2022 workbook sheet, the posts warehouse export, the migration log, the register, the count standard (5
  files); site, month, questions, question id, asked, moved, from, to (8 columns).
- Realism: a Q&A platform migrates a question by creating it on the new site and closing the original, and a monthly
  report counts posts created per site.

**The chart and slide** (`council_pool_request_2027.pptx`): the request slide and the network's monthly paid review
hours from January 2024 to December 2027, each site stacked, the envelope (26 FTE, 3,467 hours a month) drawn across,
graded on its content. Round 1 (the judge's FIX_NOW): the series is filed once in the operations handbook (each moderator
flag a paid moderator handled and each community item routed to the team, at the standard in force for its year, by
the month raised or entered, UTC; not WFM hours; months to come on the plan and its outlook), and the 33 actual months
are exact counts on it (asserted against the workbook's Monthly hours sheet, where the plotted months sit). Round 2: the
three yearly totals round 1 graded are out of the prompt and the deliverable answers; they were construction figures
every top response lands.

**Hazard table.**

| Hazard | Asks moved | Per-ask delta (design) |
|---|---|---|
| Clocks stated per source (UTC on the platform and the moderator tool, Toronto time in the WFM system) | A, B | A: a share moves where flags raised in the last Toronto evening of a month fall in the next; B: quarter-end night shifts |
| Re-sent records (15 August in both flag export parts; the re-sent May week) | A, B | A: 4 of the 9 August figures (asserted); B: the second quarter at the seven sites of the eight corrected moderators (asserted) |
| Site identity (Graphics folded into Game Development; DevOps under its old name in the WFM system) | B, C | B: DevOps's three quarters left unmapped; C: Game Development's 2022 base |

**Referee.** The flag summary's daily counts (Ask A, raised and closed by day, byte-clean, no handling time) and the
WFM system's own monthly totals by moderator (Ask B, no site); neither hands over a level.

**Cracker sheet** (the cracker landed the call, ran the hygiene battery, executed every filed rule and matched every
control):

| Ask figures | The cracker's route | Device that holds | Verdict |
|---|---|---|---|
| A, July to September by site (27) | duplicates and closed flags out, export time as the first action | A1 the reviewed flags' export time is the review's | miss |
| B, Q1 to Q3 by site (27) | superseded lines out, old name mapped, by start day on Toronto time, by the export's site | B1 the six moves overwrite the site on every 2026 shift | miss |
| C, nine sites (9) | the merger applied, the old job's double count undone from the migration log on the warehouse's basis, the 2022 sheet's questions as first reported | C2 the March 2023 rerun's restatement below the 2022 sheet's notes (C1 is filed since round 1) | miss |

**Mirror sheet.** The mirror stops at R3 (41, the closed pool at its overall lapse rate) or R1 (23 to 24) and meets the
same devices; it keeps the chart's parts and stacking, the site needs R3 shares with the golden (web, mobile, embedded,
scicomp), and nothing in A, B or C unless it cracks a device.

Mirror leakage: 4.5 per cent of ask weight (the chart's parts, about 3 of 66 ask criteria; no A, B or C figure).

Pair ceiling: 31.4 (the cracker at 38 + 7 + about 3.3 of 55 ask points, the chart's parts and the request slide; the
mirror at about 5 + 7 + 2.5). If the cracker finds the March 2023 restatement it keeps Ask C too, and the pair rises to
about 35.2. Round 1 had moved it to 41.0 (Ask C's counting filed and the chart's totals graded); round 2's restatement
device and the totals' removal bring it back. The asks are unchanged by the loop 3 redesign (their files, devices and
figures are byte-for-byte the same; `checks.py` EXPECT).
Measured by: generator/checks.py (every ask stop S1 to S5 run on the cut pack and asserted to miss, with the devices'
fairness rows)
## Leak sweep

`leak.py task156 --asof 2026-10-09` on the loop 3 cut (f17b387d): REVIEW, no LEAK; sweep 1 clean (no file describes
the data: no dictionary, file list, notes, readme or manifest ships; `checks.py` NO DESCRIPTION). Each REVIEW line:
- Sweep 3, the member survey carries 14 of 20 distinctive words of the call: they are the nine site names, which every
  file carries; the survey states no need, lapse rate, stop rate or FTE figure (asserted, R3c).
- Sweep 4, the charter (members, reviewers, reviewer, platform): the domain's nouns in its sections on members and how
  work reaches the paid team; it names no tenure, stop rate or method.
- Sweep 4, the operations handbook (roster, members, reviewers, reviewer, handbook, routed): the review-access clause
  says who may review from 1 September 2026 and that invited reviewers appear on the roster like any other; it states no
  stop rate, lapse rate, tenure effect or method (asserted, HOW). Single-use test: the handbook also carries the shift
  patterns, the holidays, the WFM approval and re-send practice and the paid-review-hours definition; deleting the
  clause opens the 2027 population (the open-pool route files 24), so it is the estimand's population, filed as WHAT.
- Sweep 6, the question plan and the WFM export name every site beside planned questions and shift lines: no ranking
  of the sites on their 2027 need.
- Sweep 8, `flag_id` in the flag exports and the review log: the moderator tool's own record key.

**Leak reader, loop 3** (isolated, on f17b387d after the dictionary and notes were removed): nothing quoted for questions
1 to 4; question 5 gives the charter's need sentence as the estimand, fixing what is counted and not how 2027's routed
items are projected; question 6 analytical (the projection against reviewer capacity under invitation-only access); every
REVIEW line harmless; realism notes mild (the 2021 sheet's missing edit columns read as a schema change, the finance
letter a little stylised).

## Surface screen

`guard.py surface task156` on the loop 3 cut: 298 builds screened, no hard tell (no shared file name, schema, same-seed
table or invented name), personas the drawn three; two pairs promoted on the cards alone, each differentiated on the
card; the adjudicated `/clone-check` is left to the author:
- task156 vs task157 (consecutive numbers, drawn by another author on 2026-10-27): the decisive gap (population) and the
  decision type (`quantity_figure`) match; task157's driver expands a sample in which one defect class is a property of
  record pairs (inclusion at the square of the sampling fraction), nothing like a closed cohort's survival by tenure;
  surface 0.077.
- task156 vs task452: the gap, the decisive generator (G9) and the decision type match; task452 weights reference
  observations by their design inclusion probabilities after a reclassification; nothing is sampled here; surface 0.084.
`guard.py heart task156`: WARN (people.first, Natalie also in task281, an older build; the persona was drawn at the
original draw and is kept), no BLOCK.

## Gates at ship

GATES_PENDING

## Pre-ship check

- The 10/10 rules re-read against the built pack: the decisive step is how the closed pool is carried, survival by
  tenure read from a left-truncated, censored roster, which product analytics recognises as its own method for a
  retained cohort and which the open pool's lapse rate gets wrong out of sample; no planted defect, withheld rule, field
  reading or executed procedure decides it (the invitation-only clause files who may review, never how fast reviewers
  stop); the mess (the platform change, old site names, UTC against Toronto, the two September pulls, the flag export's
  overlap, the re-sent WFM week, the pre-platform lapses) is Layer 1 and moves no site (R2a to R2e, SF13); the analyst
  test holds on the clean truth (R3a 41 FTE five sites off, R3b the golden's nine).
- No shipped file describes the data (asserted, NO DESCRIPTION): no dictionary, file list, notes, readme or manifest.
- Gate G: no shipped artifact ranks the sites on their 2027 need; the two distractors (page views, the member survey)
  rank nothing and are named in metadata.json.
- The card is current: the answer (32 FTE, the nine site needs, 6 above the envelope), the spine's 23,148 roster rows,
  the deliverables, the loop 3 identity with the solved one in lineage, task157 and task452 differentiated.
- target.zip is the final rebuild's cut (f17b387d), equal to the second build's; metadata.json regenerated for the
  subdomain text only (the pack untouched).

## Tried and rejected

- A mix shift by author tenure (new accounts' posts carry most review items, and AI took the newcomers): rejected at the
  draw, because the account-age column makes the segmentation a reflex the opponent runs on every visible attribute.
- Spam and flags scaling with page views rather than questions: rejected at the draw, because a per-queue trend of the
  flags already follows views, so the reflex lands, and the swap test reads it as generic demand forecasting.
- A volunteer pool with two retention types (veterans and casual reviewers) as a rung: dropped at the prototype, because
  the defensible retention estimators (tenure bands, pooled recent churn, a heterogeneity fit) split the per-site
  figures by up to 0.8 FTE; every site's pool now leaves at one steady rate since the pipeline dried up.
- Item and flag rates per question stepping up in 2023: dropped at the prototype, because a pooled ratio (over the
  step) and a reviewer trend over 2024 carry errors of opposite sign that cancel near the golden; both rates hold steady.
- Sizing the pool on the busiest 2027 month (shape 02): dropped at the prototype, because each late-2027 month's network
  hours carry about 300 hours of one-sigma spread, too wide for a monthly grid at any natural rounding.
- A volunteer pace with a wide spread across reviewers (KAPPA_SIG 0.60): the 2021 to 2023 and 2024 to 2026 saturated
  paces differed by 3.6 per cent, which moved Data & ML across its bin between eras; reviewers' own paces now spread at
  0.15.
- A Poisson trickle of new reviewers after the pipeline dried up: carried or dropped, it moved two sites by 0.4 FTE; the
  trickle is now a floor share (0.004) of the old inflow, and no construction moves a site.
- Pre-platform reviewers' grant dates drawn freely: they piled up at January 2013; tenure is now bounded by each site's
  launch on the register.
- Cover targets calibrated against random-walk inflows and exits: the calibration moved the wrong way; exits and inflow
  are now constructed (zero-sum swings within each quarter), and the January to September 2026 cover targets of
  Databases and Embedded & Hardware were set at 1.137 and 0.76 to centre their needs in their bins.
- Question moves drawn by source site: they ran the wrong way and reached 90,000 rows; moves are drawn into each
  destination at 0.55 of the first shares (49,530 rows).
- October to December 2026 on the chart with no question driver: a trend of each site's questions would be an open
  fork; the plan workbook carries the planning team's outlook sheet for those months, used only for the chart.
- WFM shifts of 7.5 paid hours: half the quarter totals ended on a half hour, a rounding fork at the nearest hour;
  shifts are now 8 paid hours, short days, overtime and corrections in whole hours.
- First actions on flags with an unbounded lognormal tail: some ran past the moderator tool's export run, dating rows
  after the as-of; a flag left past 90 hours is now escalated and taken within the next week of hours (no Ask A figure
  moves), and a review still open at the export keeps its first action as the handled time.
- The network first named Quernstone: a UK accounting firm carries that exact name (Companies House 04197485); the
  network is now Millrind (no company, network or software of that name found).
- Ask C's stop "each move applied in the month it moved": it files the golden's nine (no move straddles the window's
  edges enough to cross a rounding step), so it is recorded as a convergence, not a stop; Ask A's over-correction stop
  (reviewed flags dropped) misses 14 of 27, not 27.
- target.zip cut with a `target/` folder inside: the archive now carries the files at its root (house fix H4).
- Round 1, Ask C's device left silent (no file said how the old statistics job counted a moved question): the judge
  licensed three readings one decimal apart at every site (FIX_NOW). The warehouse notes now file the old job's counting
  and the comparison basis in the data team's voice; both other readings are asserted out. The device is no longer
  silent, so the cracker and the mirror both land Ask C (cracker sheet `hit`).
- Round 1, slide 2's series undefined (hours worked or need hours, flags in or out, which close standard, how October
  to December 2026 is counted): the operations notes now define paid review hours once, the prompt asks each year's
  actual hours totalled, and the three actual totals are graded and asserted (36,419, 36,233 and 29,626 hours); being
  construction figures, both top responses land them (cracker sheet `hit`). With Ask C, the pair ceiling moves from
  31.0 to about 41.0, over the 40 build target and under the 50 bar; precut fails its pair-ceiling and cracker rows on
  this alone, reported to the coordinator.
- Round 1, the roster missed the reviewers whose access lapsed in January or February 2024 without a platform review
  (its dictionary scope said every reviewer with access since 1 January 2024): a lapse rate read by lapse date then
  counted zero lapses in those months (1.92 per cent, 33). The 689 rows are now in the roster (first review blank), the
  dictionary's scope and lapse rule carry a worked example, and the lapse-date reading files the same nine.
- Round 1, the items no volunteer ever picks up drawn at one share for every item type: routed shares were identical
  across types in slack months, which read synthetic. Each type now has its own (close votes 0.91, low quality 0.72,
  edits 0.40, first posts 0.35 per cent); no graded figure moved. In saturated months the shares stay close across types
  because the 72-hour hand-off takes the oldest items first whatever their type; a per-type volunteer preference would
  change the routed mix that prices the frozen call, so it was not added.
- Round 1, the 24-hour share's denominator and the envelope's sign: the flag service standard now defines flag
  response as a share with the post-deleted closures out of both counts, the prompt names the measure (24-hour flag
  response), and the prompt asks how far above or below the envelope the request sits.
- Round 1, the question plan's 2026 actuals sheet stamped as pulled 8 October inside a workbook issued 18 September:
  the sheet now carries January to August 2026 as pulled on 14 September (no figure reads it).
- Round 2, Ask C held only less careful solvers once round 1 filed the old job's counting (the cracker landed it, precut
  failed): the 2022 sheet now carries the tag-sync undercount of May to August 2022 as first reported, with the
  statistics job's March 2023 restatement below its notes (sites down, months across); the careful-but-literal path
  misses all nine (nearest 0.27 points) and the golden's nine figures are unchanged.
- Round 2, the chart's three actual yearly totals (round 1): construction figures both top responses land; out of the
  prompt and the deliverable answers. The chart is graded on its content, its series filed in the operations notes and
  its months on the workbook's Monthly hours sheet. The pair ceiling is back to 31.4.
- Loop 3 (2026-10-27), the portal landed the call: both responses filed 35 FTE (the then golden) by building capacity
  against the inbox at the saturated pace and carrying each pool at its own lapse rate; the capacity framing was every
  strong solver's default, so it is now the default path and the decisive step moved to how the pool is carried.
- Two retention types with the pipeline drying in late 2024 or summer 2025: a trend of the network's lapse rate,
  extrapolated, landed the golden by coincidence (the closed pool's decline was already plain in the record); review
  access now closes on 1 September 2026, so the record shows only an open pool's flat rate.
- Grants following the question level squared (older pools at the sites AI hit hardest): the separations shrank and the
  trended-rate routes still tracked the golden; grants now follow the question level.
- Grants drying in January 2026 with the last twelve months' grants carried on: the two errors cancelled on the golden;
  with invitation-only access filed, no window of past grants is a reading of 2027.
- Invitations at 2 per cent of the old flow: carrying or dropping them moved a site by 0.44 FTE in all; invitations
  are now a handful a year and none fell in September.
- Covers calibrated by re-drawing the whole pool at each step: a site's need jumped by up to a whole FTE between
  iterations; each reviewer now draws from their own stream and each month's grants from a fixed quantile, so a cover
  change only adds or removes reviewers at the margin.
- The data dictionary, the file list, the operations notes and the warehouse notes (markdown): a file that describes the
  data is a leak (`dataset-generation` section 3); the conventions the asks and the chart need now sit in the operations
  handbook and the question count standard, and every export names its own columns.
- Annual netting at Databases and Infrastructure & DevOps 0.07 and 0.12 FTE from their bin edges, and the world's
  realised 2027 one bin lower at Data & ML (the 72-hour queue carries a short month's backlog into the next month's
  spare capacity): the three sites were re-centred slightly above their integers, and a day-by-day simulation of the
  hand-off on the forecast pool is asserted to file the same nine.

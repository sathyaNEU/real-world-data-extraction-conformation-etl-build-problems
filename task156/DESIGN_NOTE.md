# task156: Millrind's 2027 paid moderation pool, nine sites behind a shrinking volunteer review community (architecture 1)

Private, never ships. A new build (wave 5), numbered from seed FC27. The seed (a developer Q&A network's 2027 paid
moderation pool across nine topic sites after generative AI cut question volume, under a finance cap, voted at the
council's December sitting) was read at its header and Situation only. Its world, decision and quantity are kept. Its two
banned features are not shipped: the charter clause that a need method may be used only if it reproduces every
certified figure (no certified need table ships at all, so there is nothing to replay), and the revised close-queue
standard (5.0 to 2.0 minutes) ships only as a filed standard every response applies to the items it prices, never as the
decisive step. The committed quantity moves from the seed's split of a fixed pool in proportion to need to the pool
itself: how many FTE the council should ask finance for, with each site's need as its component. The pitfall is
re-found from how the network's review records come to exist: every community review item goes first to the volunteer
reviewers, and reaches the paid moderators only when no volunteer has reviewed it 72 hours after it entered the inbox.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task156.json`, architecture v1; `guard.py check` PASS (one WARN, `domain.house`, answered by naming the client domain on the card); nearest driver 0.09 (task181 v2) |
| Domain / task type | `product-analytics`, task type `retention-cohort-lifetime-value-modeling` (serves Forecasting): the deciding quantity is each site's 2027 volunteer review capacity, forecast as product analytics forecasts a user segment's retained activity, the reviewer pool projected from its own monthly exits and near-zero arrivals, times the activity each retained reviewer delivers when work is plentiful |
| Objective | Forecasting & Predictive Modeling: each site's paid review hours in calendar 2027, a year not begun at the as-of date (Friday 9 October 2026), built from the network's own inbox, reviewer and flag history and its 2027 question plan |
| Shape | `other`: the pool to request with its nine site needs, the gap to finance's envelope, a council slide charting the network's monthly paid hours with 2027 forecast, and row-set asks on rows the call never reads; criteria counted in `## Ask sheet` |
| Decision | `quantity_figure`, answer unit `count` (FTE: each site to the nearest whole FTE, the request their sum) |
| Mechanism | gap time (decisive: the history at four sites shows almost nothing reaching the paid team, and the year the request funds is the one their volunteers fall short in) with population (the items the paid team prices are not a share of arrivals but what the volunteers leave); pattern none; generators G5 (provision elsewhere: the volunteers meet the need up to their capacity), G13, G16; Gate G `binding_constraint`; strategy `binding_constraint` |
| Layer 2 family / pattern | `allocation_constraints` (capacity and queueing: the work a capacity-limited first tier leaves); `own:volunteer-review-capacity-projected-from-reviewer-retention-against-inbox-arrivals` |
| Furniture | forum `council_or_assembly` (the Moderation Council, elected by the sites' moderators, votes the request at its December sitting), forcing event `vote_or_meeting` (that sitting), organisation family `software_or_platform`, role family `operations_director` (the head of moderation operations, who takes the request to the council and then to finance), context artifact `monitoring_export` (the review platform's daily inbox export), calibration `none`, opening `question-first`, question form `how-many` |
| Spine | the review platform's daily inbox export, January 2024 to September 2026 (36,144 rows, one per site, UTC entry day and item type: entered, reviewed by a volunteer, routed to the paid team), beside its reviewer roster (19,391 access spells: first and last review, status, lapse date); constructed |
| Deliverables | `moderation_pool_2027.xlsx` (the request, the site needs, the ask tables, notes) and `council_pool_request_2027.pptx` (two slides for the December sitting: the request, and the network's monthly paid hours January 2024 to December 2027 with each site stacked and the envelope drawn across); the format set (xlsx and pptx) is in none of the last twelve builds |
| People | drawn with `guard.py names --geo Canada --seed 156` (checked clean by `guard.py check`): Duane Zamora (head of moderation operations, the operations notes and the file list), Natalie Maxwell (finance business partner, the envelope letter), Claudia Spence (council chair, signatory on the charter and the 2027 standards); the requester is in no file and not in the prompt |

**Guard.** `guard.py check` at the draw: PASS after the client domain was named (the one WARN, `domain.house`). The ban
window was read twice: at the first check it held task235 (software platform), task465 and task236; by the second it
held task465, task236 and task264, whose budget round (`budget_or_appropriation`), filed standard and finance role are
banned now. The forcing event is the seed's own December sitting (`vote_or_meeting`), the honest key for a request the
council votes; the finance envelope is the comparison the request is read against, not the event that forces it. The
context artifact is the platform's daily inbox export (`monitoring_export`); the charter and the standards are filed
documents the call reads but not the stakeholder's working file.

**Domain tag (round 1).** The rule 3 audit called the product-analytics retention tag thin for a capacity-censored
queue forecast and suggested a trust-and-safety or community-moderation workforce task type; `vocab.json` carries none
(the only workforce task type is healthcare's patient flow, which would make the domain a backdrop), so the tag stays
`product-analytics/retention-cohort-lifetime-value-modeling`, honestly the closest: the deciding quantity is the
volunteer reviewer cohort's retained activity. The tag line now names the reviewers as the retained-user cohort.

**Same-puzzle and same-driver tests.** Gap time, decisive G-code G5, decision `quantity_figure`, Gate G
`binding_constraint`: no build in the last twelve and no older build carries either triple (the guard reports none).

**Abstraction test.** Stripped of nouns: work reaches a paid tier only when a volunteer tier falls short, the volunteer
tier's capacity shows only in the periods it fell short, and with almost no new volunteers arriving each pool shrinks at
a steady exit rate, so units whose records show almost nothing reaching the paid tier cross below their arrivals inside
the forward window. The nearest by mechanism, read for latent structure rather than score:
- task153 caps what a yard island hands a vehicle at the smaller of the fuel burned between yard visits and a tankful;
  the cap there is a known physical constant applied per segment, the decisive move is the grain (the segment), and no
  capacity is forecast. Here the capacity is a quantity the history hides wherever it was not binding, it shrinks on
  the volunteers' own retention, and the decisive move is that it crosses below arrivals in the year the request funds.
- task150 carries pupils at rates on their own base and arrivals at steady counts; here nothing arrives at a steady count,
  and the decisive split is a capacity limit, not a component carried at the wrong rate.
- task148 drains a queue by abandonment; here no item leaves on its own, the 72-hour hand-off is a routing rule, and the
  forecast is how many items the volunteers will not reach, not how long anyone waits.
- task140 strikes a residual after higher reservations that include a dependent load; here the volunteers are not a
  reservation and their capacity does not depend on the paid tier.
- task111 and task128 read overflow onto a workforce late in the day and a contact's effect where the queue outran the
  team: both are past-window attributions, neither forecasts a capacity crossing.
- task146 releases a pool at a calendar turn and task134 a hazard-driven inflow: both are flows into the measured
  population; here the measured flow is the residue of a capacity.
None shares the latent structure, the default path and the correction.

**Data-native sentence.** Millrind's review platform hands every community item (a close vote, a new account's first
post, a low-quality answer, a suggested edit) to the volunteer reviewers first and routes it to the paid moderators only
if no volunteer has reviewed it 72 hours after it entered the inbox; volunteers review at their own pace when the inbox
is full and below it when it runs dry, so their capacity shows only in the months items were routed (most sites in
2022, Security, Embedded & Hardware and Scientific Computing since 2025); since almost no member has been granted review
access after the autumn of 2024, every site's reviewer pool shrinks by about two per cent a month, and the four sites
generative AI hurt in the middle (Data & ML, Databases, Infrastructure & DevOps, Game Development), whose routed items
have been near zero since January 2024, cross below their 2027 inbox arrivals.

**Sources read, one line each.**
- Seed FC27 header and Situation (`status.py task156`): the world, the cap, the December sitting and the revised close
  standard; nothing else of the seed is read or kept.
- `guard.py mechanisms --objective forecasting` (66 builds): capacity and overflow ground on file is a tankful cap per
  segment (task153), runs through full units (task147), abandonment (task148), a residual after reservations (task140)
  and past-window overflow attributions (task111, task128); none forecasts a hidden capacity crossing its arrivals.
- The kin cards the brief names (task150, task153, task152, task149): the shape moves from placing a fixed count across
  sites to sizing the pool itself; the decisive quantity is a retained-activity forecast of a volunteer user pool, not a
  cohort-component projection, a segment cap, a wear decomposition or a pace hazard.
- No trust-and-safety card in the corpus carries a moderation-capacity driver (task13 and task48 are a fraud ruleset and
  a claims monitor).
- `two-layer-task-design.md`: "the data's real structure" (capacity observed only where it binds) and "validating a
  forecast properly" (a rolling-origin test on the closed months rejects the share and trend routes) are the frames.
- `layer2-rigor-patterns.md`, product analytics: the retention patterns (censored young cohorts, heterogeneous churn,
  user-level resampling) are learned, not copied; this build's own version is a pool whose retained activity is the
  capacity a queue runs against, observed only when the queue outruns it.
- task150 and task153 design notes (the lane's allocation shapes): the call here is the pool, its site needs the
  components, and no fixed total is split.

## Default path

Built figures (`generator/calc.py` on the shipped files, asserted in `generator/checks.py` and reproduced by
`generator/verify.py`). Each request is the nine site needs, each rounded to a whole FTE, added up (the charter).

1. Read the charter's need definition (every moderator flag a paid moderator handles, and every community item no
   volunteer has reviewed 72 hours after it entered the inbox, each at the year's handle-time standard; an FTE is 1,600
   such hours; each site's need in whole FTE, the request their sum), the 2027 standards (the close item down from 5.0
   to 2.0 minutes), the 2027 question plan by site and month, and finance's 26-FTE envelope.
2. Stack the old monthly queue workbook (2021 to 2023) and the daily inbox export (2024 to September 2026, the revised
   pull), map the old site names to the platform's codes through the site register, and take each site's last twelve
   months (October 2025 to September 2026).
3. Price each site's handled flags and routed items over those twelve months at the 2027 standards, divide by its
   questions, and carry that rate onto the 2027 plan's questions.
4. Round each site to a whole FTE and add them up.

Ends on: 23 FTE, inside the envelope (Data & ML 4, Databases 3, Infrastructure & DevOps 3 and Game Development 1, at
little more than their flag hours).

Golden: 35 FTE (Frontend & Web 5, Mobile Apps 2, Data & ML 7, Databases 5, Infrastructure & DevOps 5, Game Development
2, Security 4, Embedded & Hardware 3, Scientific Computing 2), 9 above the envelope: each site's 2027 routed items are
each month's inbox arrivals (the plan's questions times the site's items per question) less what its reviewer pool can
review, the pool projected from September 2026 at its own monthly lapse rate (2.03 to 2.09 per cent, 2.05 across the
network) with almost no new reviewers, each retained reviewer at the pace reviewers keep when the inbox is full (40.0
reviews a month, read from the 89 site-months since 2021 in which more than 5 per cent of entering items were routed);
the handled flags at the plan's questions times the site's flag rate. The generator's own realised 2027 hours give the
same nine site needs (34.44 FTE against the forecast's 34.97; `checks.py` CALL).

## Stump sentence

Carrying each site's paid queue hours per question over the last twelve months onto the 2027 question plan files a
request of 23 FTE, inside finance's 26-FTE envelope, and trending each site's routed share or its monthly paid hours
forward still files 25 to 28; the step that lands each there is treating the items that reach the paid team as a share
of what arrives, when they are what arrives beyond what each site's shrinking reviewer pool can review at the pace
reviewers keep when the inbox is full, so Data & ML, Databases, Infrastructure & DevOps and Game Development, which have
routed almost nothing since January 2024, fall short of their 2027 inbox and the request needed is 35 FTE (31 with the
pool trended over the platform's whole record, 53 with the pace read from 2026 throughput).

## Three rules

- **Task type:** product-analytics, retention-cohort-lifetime-value-modeling (serves Forecasting): the deciding quantity
  is a volunteer user segment's retained activity in 2027, each site's reviewer pool carried forward from its own monthly
  exits and arrivals, times the reviews a retained reviewer delivers when work is plentiful, set against the inbox the
  2027 plan implies.
- **Domain test:** the deciding quantity is each site's 2027 volunteer review capacity, which product analytics
  forecasts as a cohort's retained activity (survivors of the current pool at the pool's own exit rate, plus the cohorts
  still arriving, times activity per active member) and trust and safety sets against the review queue it must clear.
- **Swap:** "how many agency nurses each of nine wards needs in 2027 to cover what its permanent staff cannot" keeps a
  two-tier cover, but permanent nurses are rostered to fixed hours, so their capacity is known from the roster rather
  than hidden whenever the work runs out, and there is no user cohort whose engagement decays on its own retention
  curve after a reputation pipeline dries up; the quantity that decides the call stops making sense.
- **Layer 1:** a review-platform change in January 2024 (a monthly per-queue workbook for 2021 to 2023, one sheet a
  year, the edit queue added in 2022, beside a daily inbox export by item type from 2024), old site names against new
  codes with Graphics folded into Game Development in 2023 (the site register), UTC day boundaries in the platform
  exports against Toronto time in the moderation team's records, the September 2026 export pulled twice (a preliminary
  pull with the last days' routing still open, a revised pull a week later), the moderator tool's flag export pulled in
  two parts that both carry 15 August, a WFM week re-sent after a payroll query with its original lines kept as
  superseded, and the roster's 689 reviewers whose access lapsed in January or February 2024 without a review on the
  platform (first review blank). Each is what these systems write; none carries the stump (`checks.py` R2a to R2e and
  the lapse-date reading: each mishandled, the same nine site needs).
- **Layer 2:** `allocation_constraints`: the paid team's work is what a capacity-limited first tier leaves, so it is
  forecast as arrivals less the first tier's capacity, month by month, the capacity projected from the volunteer pool's
  own retention and read at the pace volunteers keep when work outruns them; validated out of sample on the closed months.
- **Decisive step:** project each site's reviewer pool from September 2026 at its own monthly exit rate with the few
  reviewers still arriving, multiply by the reviews a reviewer completes in a month when the inbox is full (read from
  the months items were routed, never from months the inbox ran dry), and route each 2027 month's inbox arrivals beyond
  that capacity to the paid team.
- **Not semantics:** every field (entered, reviewed by a volunteer, routed to moderation; a reviewer's monthly reviews;
  the plan's questions; the standards' minutes) and every filed term (the charter's need, the 72-hour hand-off, the
  FTE's 1,600 hours) is read the same way by the easy routes; no field, code or definition states a capacity, a pace or
  an exit rate, and the routes that read them all file 23 to 28.
- **Not rule application:** the shipped sentences that bear on how the need is computed (the charter's need and FTE, the
  72-hour hand-off, the 2027 standards, the plan) executed word for word on the history give each year's past hours, and
  on 2027 they fix what is counted and what it costs, not how many items will be left unreviewed; no filed sentence says
  how many reviewers a site will have, how fast they review when work is plentiful, or that routed items are the
  arrivals beyond them (asserted: no capacity, pace, exit-rate or pipeline wording anywhere in the pack).
- **Analyst test:** a strong analyst who stacks the old workbook and the daily export, maps the sites, and reads the
  charter, the standards and the plan correctly carries each site's paid queue hours per question onto the plan and files
  23 FTE, or 25 to 28 with the routed share or the monthly paid hours trended forward (executed on the generator's
  clean truth in `checks.py` R3a: 23; the decisive step alone, R3b: the golden's nine).
- **Estimand:** the prompt and the Moderation Council charter (section on need): the pool, in FTE of 1,600 hours, that
  covers the hours the paid moderators will spend in calendar 2027 (UTC, each item in the year it entered the inbox and
  each flag in the year it was raised) on every moderator flag they handle and every community item that reaches them,
  including items from posts and accounts that do not
  yet exist, each at the 2027 handle-time standard, for each of the nine sites and in total, compared with finance's
  26-FTE envelope; the population, outcome, window, unit and comparison are filed, the method is not.
- **No decoy:** no consultant study, prior need table, staff draft or stakeholder figure states or argues a 2027 need, a
  routed share or a capacity for any site (asserted, R3c: the only FTE figures in the pack are the envelope and the
  2026 pool); finance's letter states its envelope and nothing about need.
- **No certified replay:** no certified or published need figure ships and nothing graded is reproduced from one; the
  closed months are raw records every candidate method is scored on, and the rolling-origin test that rejects the share
  and trend routes is the analyst's own, run on records no document summarises.
- **Lesson:** a second tier's workload is the residue of the first tier's capacity, and when the first tier is a
  volunteer community its capacity is a retention forecast, visible only when work outruns it; a share of arrivals, a
  trend in the residue or a capacity read from slack months all miss the year a pool crosses below its work. No build on
  file teaches it.

## Readability screen

Six tests per rung (1 a filed sentence names it or sends the solver looking, 2 a column, key or marker makes it a
predicate or a header join, 3 an opponent reflex, 4 a control or corpus scores it, 5 the hygiene battery finds it, 6 one
subtraction, ratio or half of a figure). Built figures (`generator/calc.py`; the back-test is `checks.py` BACKTEST).

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 each site's paid queue hours per question over the last twelve months carried onto the plan (23) | the charter prices items at the standard and the plan gives the questions, which invites a rate per question | the inbox export and the flag summary carry routed items and flags by site and day | yes, the default | the analyst's own back-test refutes it (from September 2025 it misses the next twelve months' routed items by 73 per cent) | no | yes, one ratio | readable |
| R1 each site's routed share or monthly paid hours trended forward (25, 28) | no | the same columns | yes, the trend reflex | the same back-test: the trended share misses by 68 per cent, the hours trend at Security, Embedded and Scientific Computing only | no | yes, a fitted line | readable |
| R2a volunteer capacity against arrivals, the reviewer pool trended over the platform's whole record from January 2024 (31) | no | the roster carries each reviewer's first and last review | a careful forecaster's reflex once capacity is seen | the back-test from September 2025 under-predicts routed items by 31 per cent (the record's first nine months, before the pipeline dried up, flatten the trend) | no | no | readable |
| R2b volunteer capacity read from each site's own reviews per reviewer in January to September 2026 (53) | no | reviews and reviewers by site and month | the capacity-modeller's reflex (current throughput as capacity) | the back-test over-predicts routed items by 597 per cent: at every site with spare volunteers the throughput is held down by the work that arrived | no | no | readable |
| R3 (decisive) each site's reviewer pool projected from September 2026 at the exit rate its records show since the pipeline dried up, each reviewer at the pace reviewers keep when the inbox is full, each 2027 month's arrivals beyond that capacity routed (35) | no sentence states a capacity, a pace, an exit rate or a pipeline; the charter defines what reaches the paid team, not how many items will | no column carries capacity, pace or exits: the roster lists access spells, the inbox export counts items, nothing names a site as short | no: the reflexes are a rate per question, a trend, a share, current throughput | none ships: the closed months are raw records every candidate is scored on, no document scores the methods | no: nothing is duplicated, missing or mis-keyed on the call's rows | no: a capacity built from a projected pool and a pace read only where work outran it, set month by month against arrivals | silent |

## Semantic fork table

Every term in the main ask and every convention the main computation needs. Every id is asserted in `generator/checks.py`.

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "FTE" | 1,600 hours of need at the standards (the charter) | 1,950 or 2,080 paid hours a year | a smaller request | the charter's FTE sentence |
| SF2 | "need" | the hours the paid moderators will spend on the items that reach them, each at the year's standard (the charter) | the hours the paid team is scheduled or works (the WFM export) | the 2026 pool's hours carried | the charter's need sentence |
| SF3 | "2027" | calendar 2027, each item in the month it entered the inbox and each flag in the month it was raised, UTC (the charter) | the month an item reaches the paid team; Toronto time | same call (asserted: a tenth of each month's routed items moved into the next month, the same nine) | the charter; same call, asserted |
| SF4 | the items counted | every moderator flag a paid moderator handles and every community item routed to the paid team, the items no volunteer ever picks up included (the charter) | flags the platform closes because the post was deleted before a moderator acted | a larger flag count | the charter: flags the platform closes cost no moderator time and are left out |
| SF5 | "each of our nine sites" | the nine sites on the register, Graphics & Shaders inside Game Development since July 2023 | Graphics as a tenth site | same call (Graphics has no records after June 2023) | the site register |
| SF6 | "the 2027 handle-time standards" | the council's 2027 standards (close 2.0 minutes, every other item as in 2026) | the 2026 standards | a larger request | the prompt and the standards' effective dates |
| SF7 | "question plan" | the planning team's 2027 questions by site and month, counted as the posts warehouse counts them | a trend of each site's questions | same call (asserted: each site's own questions trended log-linearly from January 2025 file the same nine) | the prompt names the plan |
| SF8 | the rounding path | each site's need to the nearest whole FTE, the request their sum (the charter) | the network's hours over 1,600 rounded once | same call (55,959 hours is 34.97 FTE, 35; asserted) | the charter's request sentence |
| SF9 | "how far it sits from finance's envelope" | the request less the envelope, in FTE | a percentage | same call | the prompt's rounding sentence (FTE in whole numbers) |
| SF10 | items from posts and accounts not yet written | in: the plan's questions carry them | only items on existing posts | a much smaller request | the charter: every item entering the inbox in the year |
| SF11 | the chart's history | each month's paid review hours at the standards in force then (unchanged from 2023 to 2026), 2027 at the 2027 standards | history restated at the 2027 standards | the chart's history months, not the call | the standards' effective dates; the request is unaffected |
| SF12 | the September 2026 inbox records | the revised pull of 8 October | the preliminary pull of 2 October (items entering 28 to 30 September still open) | same call (asserted, R2d) | the file list; same call, asserted |

## Ladder

Built figures (`generator/calc.py` on the shipped files; every row asserted in `generator/checks.py`). Each request is
the sum of the nine site needs rounded to whole FTE (web, mobile, data, databases, devops, gamedev, security, embedded,
scicomp).

| Rung | Construction | Request | Dies to |
|---|---|---|---|
| R0 default | each site's flags and routed items over the last twelve months at the 2027 standards, per question, carried onto the 2027 plan (nine months gives the same) | 23 (5, 2, 4, 3, 3, 1, 2, 2, 1) | the back-test: carrying the routed share from September 2025 misses the next twelve months' routed items by 73 per cent |
| R1a | each site's routed share trended (the last twelve months against the twelve before) | 25 (5, 2, 4, 3, 3, 1, 3, 3, 1) | the same back-test, 68 per cent low |
| R1b | each site's monthly paid hours, seasonally adjusted, trended log-linearly from January 2025 | 28 (5, 2, 4, 3, 3, 1, 4, 4, 2) | a trend of the residue cannot see a crossing: Data & ML, Databases, Infrastructure & DevOps and Game Development move by less than a whole FTE from R0 |
| R2a | capacity against arrivals, the reviewer pool trended log-linearly over January 2024 to September 2026 | 31 (5, 2, 6, 4, 4, 2, 3, 3, 2) | the back-test from September 2025, 31 per cent low: the pools held until new reviewers stopped arriving in the autumn of 2024 |
| R2b | capacity against arrivals, the pace read from each site's own reviews per reviewer in January to September 2026 | 53 (13, 5, 9, 7, 7, 3, 4, 3, 2) | the back-test, 597 per cent high: where volunteers had spare capacity their throughput was the work that arrived |
| R3 decisive | each pool projected from September 2026 at its own lapse rate (2.03 to 2.09 per cent a month), each reviewer at the pace kept when the inbox is full (40.0 reviews a month over the 89 saturated site-months since 2021), each 2027 month's arrivals beyond that capacity routed | 35 (5, 2, 7, 5, 5, 2, 4, 3, 2) | golden |

**Position and margins.** The golden is bracketed: R0 to R2a below (23 to 31), R2b above (53). Every correction short
of the decisive one walks up from 23 and stops at or under 31; only the pace read where work outran the volunteers,
with the pool projected on its own lapses, reaches 35, and reading the pace from slack months overshoots to 53. The
nearest principled wrong request is 31, four FTE away; every rung's nine site needs differ from the golden's at two
sites or more (asserted).

**Convergence (C1, asserted on the shipped files).** Every defensible construction of the golden files the same nine
site needs (18 constructions): the lapse rate read over the last 12, 18 or 24 months or at either end of its one-sigma
band, or the pool trended log-linearly over the last 12 to 21 months; the trickle of new reviewers carried or dropped;
the pace read from 2021 to 2023, from 2024 to 2026 or pooled, at any saturation cut from 1 to 15 per cent of items
routed (39.7 to 40.2 reviews a month across every cut and era), or each site's own pace with the pooled pace where a
site never ran short; monthly or annual netting; item ratios from 2025; no floor. The network's unrounded need runs
34.44 to 35.51 FTE across them (the one-sigma lapse rates at the ends), and every site stays 0.17 FTE or more inside
its bin (Frontend & Web the closest).

**Worth on the graded quantity.** Seeing the volunteers' capacity is worth 8 FTE (R0 23 to R2a 31), and projecting the
pool on its own lapses and reading the pace where work outran it another 4 (to 35); the censoring error alone costs 18
the other way. Without the capacity no trend or share moves Data & ML, Databases, Infrastructure & DevOps or Game
Development by a whole FTE (asserted).

**Out of sample.** A rolling-origin test on the closed months (fit through September 2025, score the routed items of
October 2025 to September 2026; `checks.py` BACKTEST): the capacity method misses by 4.9 per cent network-wide (worst
site 16 per cent); the carried share by 73, the trended share by 68, the full-record pool trend by 31, the censored pace
by 597 (over). The test is the analyst's own, run on records no document summarises.

**Strength.** P(one strong solver lands) about 0.12: it must see that routed items are the arrivals beyond a capacity
rather than a share (the dictionary defines the column, nothing else points there), read the volunteers' capacity
where work outran them rather than from current throughput, and project the pool from its exits since the pipeline
dried up rather than over the platform's whole record. P(both land) about 0.02 if independent, under 0.1 with any
plausible correlation. The seed was fixed by rule (task number, then the as-of month and day: 1561009) before any data
was generated and is never searched; every later move is a design parameter recorded in `## Leak sweep

`leak.py task156 --asof 2026-10-09`: REVIEW, no LEAK. Each REVIEW line, harmless:
- Sweep 3, the member survey carries 14 of 20 distinctive words of the call: they are the nine site names, which every
  file carries; the survey states no need, routed share or FTE figure (asserted, R3c).
- Sweep 4, the charter, the ops notes, the file list and the data dictionary carry 4 to 6 stump-paragraph terms
  (reviewer, volunteer, platform, routed, export, reviews): the domain's own nouns; none states a capacity, a pace, a
  lapse rate or how many items volunteers will leave (asserted, HOW).
- Sweep 6, the question plan and the WFM export name every site beside numbers: planned questions and shift lines, no
  ranking of the sites on their 2027 need.
- Sweep 8, `flag_id` in the flag exports and the review log: the moderator tool's own record key (a flag is the
  domain's noun), no marker column.

## Surface screen

`guard.py surface task156` promotes two pairs for adjudication; neither carries a hard tell (no shared file name,
schema, same-seed table or invented name), and `guard.py heart` passes (nearest driver 0.09, task181 v2). For the
author, who alone runs the adjudicated `/clone-check`:
- task154 vs task156 (two apart): the coarse card axes match (decisive gap time, `quantity_figure`, context artifact
  `monitoring_export`), each the honest key here; the drivers share nothing (task154 revalues a holder's stock over its
  own holding period to separate volume from price in a GDP nowcast; task156 forecasts a volunteer pool's capacity
  crossing below its arrivals). task154 was registered before this draw and `guard.py check` passed then; the keys are
  not relabelled.
- task103 vs task156 (surface 0.102, corpus top 1 per cent): the whole score is the flat layout and the same four
  formats (csv, xlsx, pdf, md) with one shared prompt shingle (prompt Jaccard 0.0095); no file name, column set, value
  or name is shared. Nothing to rename.

## Tried and rejected`.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | every flag a paid moderator handles and every community item routed to the paid team in 2027 at the nine sites, posts and accounts not yet written included | filed (the charter's need sentence); SF4, SF10 |
| 2 | Unit of account | FTE of 1,600 hours of need at the standards, whole FTE per site | filed (charter); SF1, SF8 |
| 3 | Attribution window | calendar 2027, items by entry month and flags by raise month, UTC | filed (charter); SF3 same call asserted |
| 4 | As-of dating | data through 30 September 2026, pulled 8 October | filed (the file list, every export's pull date) |
| 5 | Version basis | the revised September pull | SF12 same call asserted |
| 6 | Denominator | none on the golden path (items and hours are counts); R0's per-question rate is a wrong rung | named in the ladder |
| 7 | Weighting | none | n/a |
| 8 | Window length | the months the exit rate and the pace are read from | C1: 12 to 24 months, every saturation cut, the same needs (asserted) |
| 9 | Boundary inclusivity | the 72-hour hand-off | the charter states it once; the inbox export records the outcome, no reading turns on the boundary |
| 10 | Rounding path | each site to the nearest whole FTE, the request their sum | filed (charter); SF8 |
| 11 | Tie-break | none | n/a |
| 12 | Maturity and censoring | items entering 28 to 30 September still open in the preliminary pull | C1: the revised pull is complete (asserted) |
| 13 | Order of operations | arrivals against capacity month by month, then priced | C1: monthly and annual netting the same needs (asserted) |
| 14 | Row order | sums | C1 |
| 15 | Duplicate resolution | none on the call's rows | asserted: no duplicate key in the inbox export, the roster or the flag summary |
| 16 | Identity normalisation | old site names to codes through the register | C1: the pace is pooled over sites, no mapping moves it (asserted: Graphics' old rows left out, the same nine) |
| 17 | Netting against gross | none | n/a |
| 18 | Dimensional units | minutes per item, hours, FTE | filed (standards, charter) |
| 19 | Code and status semantics | item types; the roster's access status | the dictionary; C1: status and last review agree on every row (asserted) |
| 20 | Integerisation | whole FTE per site | each site's unrounded need 0.17 FTE or more inside its bin across every construction and one sigma (asserted) |
| 21 | Clause scope | the 2027 standards apply to items in 2027 | filed (standards' effective date) |
| 22 | Forward window contents | the 2027 questions | a shipped driver file: the planning team's 2027 plan by site and month (SF7) |

## Literal reader

Executing the prompt, the charter and the 2027 standards word for word gives, for each site, the hours the paid
moderators will spend in calendar 2027 on every moderator flag they handle and every community item no volunteer has
reviewed 72 hours after it entered the inbox, at the 2027 standards, over 1,600 and rounded to a whole FTE, the request
their sum; no shipped sentence says how many items the volunteers will leave, so a literal reader must forecast it; the
easy method on the same literal estimand (each site's routed share or paid hours per question carried onto the plan)
files 23, and the fork table leaves no reading under which 23, 25, 28 or 31 is the golden.

## Oracles

- The closed months themselves (2021 to September 2026): on the wrong path they suggest a share or a trend to carry,
  and a rolling-origin test on them rejects both; no document scores any method, and no closed month carries a 2027
  figure.
- The 2026 pool (27 FTE) and finance's envelope (26 FTE): figures the request is compared with, consistent with every
  method; neither states a need.
- The old workbook's routed history (2021 to 2023): raw records, every site's items, reviews, routed items and active
  reviewers; it shows the pace volunteers kept when work outran them and states nothing about 2027.
- No control ties only under the golden.

## Ask sheet

**Main call's declared row population:** the review platform's daily inbox export (January 2024 to September 2026,
both September pulls), the old monthly queue workbook's item, review, routed and reviewer columns (2021 to 2023), the
reviewer roster, the moderator tool's daily flag summary, the posts warehouse's monthly question counts for 2024 to
2026, the 2027 question plan, the charter, the 2027 standards, the site register and the envelope letter. Device and
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
- Basis (filed in the moderation team's timesheet note): a shift's hours count for the site the moderator was assigned
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
- Span: the WFM export, the assignment history, the timesheet note, the site register, the moderator list (5 files);
  moderator id, shift start, shift end, hours, site, line status, effective from, effective to (8 columns).
- Realism: workforce systems export the current record's attributes onto historical lines; moderators were moved to
  the three sites whose queues grew.

**Ask C. Each site's January to September 2026 questions as a percentage of the same months of 2022** (9 figures, per
cent to one decimal).
- H18 home: a component of the case: how much each site's volume has fallen, the context the request opens with; the
  call reads no 2022 question count.
- Use: the first table of the council's paper.
- Basis (filed in the posts warehouse notes): each question counts once, on the site it lives on now, in the month it
  was first asked (UTC); comparisons with 2021 to 2023 are made on that basis.
- Primary C1 (D1, the same records under two sources): the old monthly workbook counted a question moved between sites
  twice, on the site it was asked on and again on the site it moved to, in the month of the move; the 2026 counts come
  from the posts warehouse, which counts each question once. Fair: the moderators' migration log (2021 to 2023) lists
  every move with both question ids, both sites and both dates. Round 1 (the judge's FIX_NOW): the old job's counting is
  now filed in the warehouse notes in the data team's voice ("The old statistics job counted a question on every site
  it was posted to ..."), with the comparison basis, so the device is no longer silent: it is seen and repaired from the
  migration log. The two readings the judge licensed are asserted out: the old job read as counting each question once
  on its posting site misses all nine (nearest 0.22 points), and no restatement (S2) misses all nine.
- Hazards: HC1 Graphics & Shaders folded into Game Development in July 2023 (the register); HC2 the 2022 sheet's
  layout (a title block, old site names, a totals row).
- Stops (built, asserted): S1 the workbook as it stands, Graphics left out of Game Development (9 miss); S2 the merger
  applied (9 miss, the device, the nearest 0.14 points off); S3 the copies taken off, each question once but on the
  site it was asked on (7 of 9 miss); S4 the golden. Applying each move in the month it moved instead of the month asked
  files the same nine (a convergence, asserted).
- Span: the 2022 workbook sheet, the posts warehouse export, the migration log, the register, the warehouse notes (5
  files); site, month, questions, question id, asked, moved, from, to (8 columns).
- Realism: a Q&A platform migrates a question by creating it on the new site and closing the original, and a monthly
  report counts posts created per site.

**The chart and slide** (`council_pool_request_2027.pptx`): the request slide and the network's monthly paid review
hours from January 2024 to December 2027, each site stacked, each year's actual hours totalled, the envelope (26 FTE,
3,467 hours a month) drawn across. Round 1 (the judge's FIX_NOW): the series is filed once in the operations notes
(each moderator flag a paid moderator handled and each community item routed to the team, at the standard in force for
its year, by the month raised or entered, UTC; not WFM hours; months to come on the plan and its outlook), and its
graded figures are the three actual totals (2024 36,419 hours, 2025 36,233, January to September 2026 29,626), exact
counts asserted and reproduced by the verifier; the 2027 months sum to the call's own need.

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
| C, nine sites (9) | the merger applied, the old job's double count undone from the migration log on the warehouse's basis, as the warehouse notes now file it | none since round 1: the old job's counting is filed | hit |
| Chart, three actual totals (3) | paid review hours as the operations notes define them, from the inbox export and the flag summary | none: a construction figure | hit |

**Mirror sheet.** The mirror stops at R2a (31) or R1 (25 to 28) and meets the same devices; it keeps the chart's
history parts and stacking, the chart's three actual totals and, since round 1, Ask C's nine figures, the site needs R2a
shares with the golden (web, mobile, gamedev, embedded, scicomp), and nothing in A or B unless it cracks a device.

Mirror leakage: 22 per cent of ask weight (the chart's parts and three actual totals and Ask C's nine figures, about 15
of 69 ask criteria; no A or B figure).

Pair ceiling: 41.0 (round 1: the cracker at 38 + 7 + about 13 of 55 ask points, Ask C, the chart's totals and parts and
the request slide; the mirror at about 5 + 7 + 12). Before round 1 it was 31.0; the two FIX_NOW repairs (Ask C's
counting filed, the chart's totals graded) cost about ten points of pair score, all of it on rows both top responses
now land. Asks A and B still hold both whole. Rerun from the generated rubric at stage 4.

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

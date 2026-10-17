# task156: Quernstone's 2027 paid moderation pool, nine sites behind a shrinking volunteer review community (architecture 1)

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
| Decision | `quantity_figure`, answer unit `count` (FTE: the pool to the nearest five, each site to the nearest whole) |
| Mechanism | gap time (decisive: the history at four sites shows almost nothing reaching the paid team, and the year the request funds is the one their volunteers fall short in) with population (the items the paid team prices are not a share of arrivals but what the volunteers leave); pattern none; generators G5 (provision elsewhere: the volunteers meet the need up to their capacity), G13, G16; Gate G `binding_constraint`; strategy `binding_constraint` |
| Layer 2 family / pattern | `allocation_constraints` (capacity and queueing: the work a capacity-limited first tier leaves); `own:volunteer-review-capacity-projected-from-reviewer-retention-against-inbox-arrivals` |
| Furniture | forum `council_or_assembly` (the Moderation Council, elected by the sites' moderators, votes the request at its December sitting), forcing event `vote_or_meeting` (that sitting), organisation family `software_or_platform`, role family `operations_director` (the head of moderation operations, who takes the request to the council and then to finance), context artifact `monitoring_export` (the review platform's daily inbox export), calibration `none`, opening `question-first`, question form `how-many` |
| Spine | the review platform's reviewer-month activity export, January 2024 to September 2026 (one row per volunteer reviewer per site per month: reviews completed by item type, days with a review), beside the platform's daily inbox export by site and item type; constructed |
| Deliverables | `moderation_pool_2027.xlsx` (the request, the site needs, the ask tables, notes) and `council_pool_request_2027.pptx` (two slides for the December sitting: the request, and the network's monthly paid hours January 2024 to December 2027 with each site stacked and the envelope drawn across); the format set (xlsx and pptx) is in none of the last twelve builds |
| People | drawn with `guard.py names --geo Canada --seed 156` (checked clean by `guard.py check`): Duane Zamora (head of moderation operations, the operations notes and the file list), Natalie Maxwell (finance business partner, the envelope letter), Claudia Spence (council chair, signatory on the charter and the 2027 standards); the requester is in no file and not in the prompt |

**Guard.** `guard.py check` at the draw: PASS after the client domain was named (the one WARN, `domain.house`). The ban
window was read twice: at the first check it held task235 (software platform), task465 and task236; by the second it
held task465, task236 and task264, whose budget round (`budget_or_appropriation`), filed standard and finance role are
banned now. The forcing event is the seed's own December sitting (`vote_or_meeting`), the honest key for a request the
council votes; the finance envelope is the comparison the request is read against, not the event that forces it. The
context artifact is the platform's daily inbox export (`monitoring_export`); the charter and the standards are filed
documents the call reads but not the stakeholder's working file.

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

**Data-native sentence.** Quernstone's review platform hands every community item (a close vote, a new account's first
post, a low-quality answer, a suggested edit) to the volunteer reviewers first and routes it to the paid moderators only
if no volunteer has reviewed it 72 hours after it entered the inbox; volunteers review at their own pace when the inbox
is full and below it when it runs dry, so their capacity shows only in the months items were routed (every site in 2021
and 2022, Security, Embedded and Scientific Computing since late 2025); since almost no members have reached the review
privilege after the autumn of 2024, every site's reviewer pool shrinks by about two per cent a month, and the four sites
generative AI hurt in the middle (Data & ML, Databases, DevOps, Game Development), whose routed items have been near
zero since 2023, cross below their 2027 inbox arrivals.

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

Figures from the design prototype (`proto5`, to be replaced by `generator/calc.py` on the shipped files and asserted in
`generator/checks.py`).

1. Read the charter's need definition (every moderator flag, and every community item no volunteer has reviewed 72
   hours after it entered the inbox, each at the year's handle-time standard; an FTE is 1,600 such hours), the 2027
   standards (the close item down from 5.0 to 2.0 minutes), the 2027 question plan by site and month, and finance's
   110-FTE envelope.
2. Stack the old monthly queue workbook (2021 to 2023) and the daily inbox export (2024 to September 2026, the revised
   pull), map the old site names to the platform's codes through the site register, and take each site's last twelve
   months (October 2025 to September 2026).
3. Price each site's flags and routed items over those twelve months at the 2027 standards, divide by its questions,
   and carry that rate onto the 2027 plan's questions.
4. Sum the sites and divide by 1,600.

Ends on: about 105 FTE, inside the envelope (Data & ML, Databases, DevOps and Game Development at their flag hours alone).

Golden: about 130 FTE, 20 above the envelope: each site's 2027 routed items are each month's inbox arrivals (the plan's
questions times the site's items per question) less what its reviewer pool can review, the pool projected from
September 2026 at its own monthly exit rate with almost no new reviewers, each retained reviewer at the pace reviewers
keep when the inbox is full (about 150 reviews a month, read from the months items were routed); the flags at the plan's
questions times the site's flag rate.

## Stump sentence

Carrying each site's paid queue hours per question over the last twelve months onto the 2027 question plan files a pool
of about 105 FTE, inside finance's 110-FTE envelope, and trending each site's routed share, its monthly paid hours or its
reviewer count forward still files 110 to 114; the step that lands each there is treating the items that reach the paid
team as a share of what arrives, when they are what arrives beyond what each site's shrinking reviewer pool can review at
the pace reviewers keep when the inbox is full, so Data & ML, Databases, DevOps and Game Development, routed almost
nothing since 2023, fall short of their 2027 arrivals and the pool needed is about 130 FTE.

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
  pull with the last days' routing still open, a revised pull a week later), reviewer accounts re-keyed at the platform
  change (old site-local numbers to network account ids). Each is what these systems write; none carries the stump.
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
  an exit rate, and the routes that read them all file about 105 to 114.
- **Not rule application:** the shipped sentences that bear on how the need is computed (the charter's need and FTE, the
  72-hour hand-off, the 2027 standards, the plan) executed word for word on the history give each year's past hours, and
  on 2027 they fix what is counted and what it costs, not how many items will be left unreviewed; no filed sentence says
  how many reviewers a site will have, how fast they review when work is plentiful, or that routed items are the
  arrivals beyond them (asserted: no capacity, pace, exit-rate or pipeline wording anywhere in the pack).
- **Analyst test:** a strong analyst who stacks the old workbook and the daily export, maps the sites, and reads the
  charter, the standards and the plan correctly carries each site's paid queue hours per question onto the plan and files
  about 105 FTE, or 110 to 114 with the routed share, the monthly paid hours or the reviewer count trended forward (to be
  executed on the generator's clean truth in `checks.py`).
- **Estimand:** the prompt and the Moderation Council charter (section on need): the pool, in FTE of 1,600 hours, that
  covers the hours the paid moderators will spend in calendar 2027 (UTC, by the time an item reaches them) on every
  moderator flag raised and every community item that reaches them, including items from posts and accounts that do not
  yet exist, each at the 2027 handle-time standard, for each of the nine sites and in total, compared with finance's
  110-FTE envelope; the population, outcome, window, unit and comparison are filed, the method is not.
- **No decoy:** no consultant study, prior need table, staff draft or stakeholder figure states or argues a 2027 need, a
  routed share or a capacity for any site (to be asserted: no document states a 2027 FTE figure other than the
  envelope); finance's letter states its envelope and nothing about need.
- **No certified replay:** no certified or published need figure ships and nothing graded is reproduced from one; the
  closed months are raw records every candidate method is scored on, and the rolling-origin test that rejects the share
  and trend routes is the analyst's own, run on records no document summarises.
- **Lesson:** a second tier's workload is the residue of the first tier's capacity, and when the first tier is a
  volunteer community its capacity is a retention forecast, visible only when work outruns it; a share of arrivals, a
  trend in the residue or a capacity read from slack months all miss the year a pool crosses below its work. No build on
  file teaches it.

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

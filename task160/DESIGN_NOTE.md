# task160 design note

Architecture 1, wave 6 (new), Forecasting lane (sathya8571), numbered from seed FC31. The seed (a state hospital
association block-booking its January agency nurse shifts for a 24-hospital winter pool with two staffing agencies, the
pool funding agency shifts worked while a member hospital's surge plan is active, the block set at the forecast pool
draw) was read at its header and Situation only. Its world, decision and quantity are kept; the world moved from one
state to a three-region cooperative at the rule-3 recheck, so the lags between regions are the sizes multi-state
seasons show. The seed's mechanism (the agencies' surge booking code only mostly agreeing with the activation days the
pool funds) is not the decisive step: reading the code against the contract's definition is data semantics, so the code
survives only as Layer 1 mess and as an ask device. The pitfall is re-found from how a winter respiratory wave reaches
a cooperative's regions: one after another, each at a lag behind the region it follows that has held in every winter
on file, while the wave's calendar timing, and its lag behind the region it reaches first, move by weeks.

The Tri-Region Hospital Cooperative (fictional) is a member-owned cooperative of hospitals in the Southeast (Georgia and
South Carolina), Central (Tennessee, Kentucky and West Virginia) and the North (northern Michigan), every member in
Eastern time. It runs a winter surge staffing pool: it block-books agency RN shifts with two staffing agencies
(Crestfield Medical Staffing and Inland Seas Nursing, both fictional) and funds the agency shifts its members work while
their surge plans are active. For 2026-27 the pool grows from the sixteen Southeast and Central hospitals it has covered
since 2021-22 to 24: the eight North hospitals join it on 1 November 2026. Every member has filed a daily capacity
report (midnight census, staffed beds, declared surge level) since July 2021. The block for the four weeks from Monday
4 January 2027 is filed with the agencies on Tuesday 22 December 2026, set at the forecast pool draw, to the nearest 50
shifts.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task160.json`, architecture v1, registered 2026-10-18T00:47:12Z; `guard.py
   check` WARN, answered below. Nearest driver 0.10 (task157).
2. Pairing: Healthcare Delivery & Health Economics (client domain) / `patient-flow-beds-workforce-optimization` /
   Forecasting & Predictive Modeling. The task type serves Forecasting in the taxonomy (OS, F). The deciding analysis is
   a health system's surge workforce forecast: where each region's respiratory wave falls in the block window, timed
   from the region it follows, turned into agency RN shifts through each hospital's surge unit staffing. Not banned
   against the last three registrations (task194 healthcare-delivery x anomaly-detection, task470, task243); task142
   (the nearest world: a purchasing alliance's Hospital in the Home overflow block) sits in
   `utilization-access-demand-forecasting`, a different task type, and is differentiated on the card.
3. Niche: a hospital cooperative's January 2027 agency nurse block for its 24-hospital winter surge pool, when the
   respiratory wave reached its Southeast members (Georgia and South Carolina) in late November and its Central members
   (Tennessee, Kentucky and West Virginia) in mid-December, earlier than in any winter on the capacity census, and the
   eight northern Michigan hospitals new to the pool have met the wave about four weeks after Central in every winter
   on file, while their lag behind the Southeast moved by two weeks or more.
4. Call and shape: the agency RN shifts to block-book for the four weeks from Monday 4 January 2027 (`quantity_figure`,
   count, question form how-many), to the nearest 50 shifts (the agencies take the block in lots of 50). Shape
   `single-figure`: the call with its critical components, the asks' tables on rows the call never reads, and a chart;
   criteria counted in `## Ask sheet`.
5. Mechanism keys: gap time (the evidence is what past January blocks held; the decision bets on a block whose content
   moves with the wave's timing), then population (the North's eight hospitals have no pool history); decisive generator
   G16 (the forecasting method the closed winters select out of sample: the North's wave timed by its lag behind
   Central, against the calendar, the pool's own post-peak weeks, the Southeast's lag and the regressions that lean on
   the Southeast's timing), then G13 (the window holds a different part of each region's wave this winter) and G6 (the
   window's mix of regions in their waves differs from every January on file); Gate G `forecasting`; strategy
   `forecast_method_backtest` (F6: the January draw is stationary only in each region's own wave time, and the calendar
   fit, the Southeast-anchored lag and the regressions on the Southeast's timing fail out of sample on closed winters).
6. Layer 2: `forecast_uncertainty` (model choice on out-of-sample error), pattern
   `own:regional-surge-waves-timed-by-propagation-lag-not-calendar`. Library neighbours:
   epidemiology-public-health/infectious-disease-transmission-modeling (spatial spread, not an Rt or eigenvalue read) and
   healthcare-delivery-health-economics/patient-flow-beds-workforce-optimization/2 (staff to the arrival curve, not the
   daily average); this build's version times each region's surge by the lag of an epidemic's spread across a
   cooperative's regions, read from the closed winters, choosing the upstream region whose lag held, and carries no
   queueing or percentile construction.
7. Furniture: forum `operations_desk` (the pool manager files the block; no committee approves it); forcing event
   `purchase_order_or_contract` (the block order goes to the two agencies on 22 December); organisation family
   `cooperative_or_member_body` (a hospital cooperative is its members' body); role family `procurement_lead` (the
   winter pool manager buys the block); context artifact `capacity_report` (the cooperative's daily capacity census);
   calibration `prior_period_close_out` (the closed winters' capacity census and declarations, which the out-of-sample
   check reads). Each is free against task194, task470 and task243.
8. Spine: the cooperative's daily capacity census (hospital x day, midnight census, staffed beds and declared surge
   level), 1 July 2021 to 20 December 2026, two layouts across the July 2024 system change; constructed in the layout of
   a hospital cooperative's daily capacity reporting system.
9. Deliverables: `winter_pool_block_jan2027.xlsx` (the block, its components and the ask table) and
   `pool_shifts_winter_2025-26.png` (a chart on an ask's quantity, never on the block). The format set (xlsx and png) is
   in none of the last three builds.
10. People, drawn again for the multi-state world with `guard.py names --geo "United States" --seed 160` (the locale's
    pool, every name the check would block skipped): Brandon Williams (the winter pool manager and the requester, named
    in the agreement, the register and the block book, not in the prompt), Linda Ashley (the cooperative's surveillance
    lead, the admissions outlook) and Shawn Whitaker (its finance manager, the rate schedule), the draw's third to fifth
    names. David Cooper and Judith Harrison, ahead of them, were passed over (David Cooper's first name stands in
    task104's people; Judith Harrison was replaced at the first draw); Greg Matthews and Andrew Harvey left with the
    one-state world. Invented names checked on the web against real organisations: Tri-Region Hospital Cooperative (no
    organisation of the name; Corridor Hospital Cooperative, tried first, sat beside WVU Medicine's Elkins Corridor
    Medical Center), Crestfield Medical Staffing and Inland Seas Nursing (no match). The southern hospitals new to this
    world were checked one by one: Pettigrew (a Georgia physician of the name), Ashcraft Memorial (within two letters of
    Ashraff Memorial and inside Schoolcraft Memorial) and Marcum (Mercy Health Marcum and Wallace Hospital, Kentucky)
    were replaced by Satterfield, Lattimore Memorial and Spurlock Memorial; Kinard, Crumley Memorial, Satterfield,
    Lattimore and Spurlock returned no hospital of the name. The other names carry over from the first cut's check, where
    14 of 24 were renamed for a real name within reach (`reduce-house-fixes` H21) and the ten kept were place names with
    no institution of the name.

**Data-native sentence.** The cooperative's capacity census records every member's surge spells day by day, and in
every winter on file the respiratory wave has reached the eight North hospitals about four weeks after Central's (26 to
34 days between the regions' centres), while Central's own gap behind the Southeast ran from three days to two weeks
and the wave's calendar timing moved by four weeks; this winter the Southeast's surge spells began 18 to 25 November and
Central's 9 to 17 December, earlier than ever on file, so the four weeks from 4 January hold the North's whole wave,
which no January block on file ever held, and none of the south's, which every January block on file held.

**Guard and similarity.** `guard.py check` WARN at registration, re-pulled before the check and before register (the ban
window held task194, task470 and task243 after task470 and task243 registered at the second pull; task196, which carried
`cooperative_or_member_body`, had moved out). WARN answered: `repeat.question_form` (how-many, task470): the call is a
count of shifts and a count asks how many. NOTES: `test.same_puzzle_older` and `test.same_driver_older` (gap time,
decisive G16, quantity_figure, Gate G forecasting) against task127 v3, task138 v1 round 1, task145 and task446 v2, each
differentiated on the card (a reserve developed at closed shares; a store replayed from the forecast date; a count above a
line at forward conversion factors; a yield carried onto a moved base rate). A first draw with G13 decisive met the same
two tests against task102, task130 v4, task134 v2 and task501 v3; G16 names the decisive move more exactly (the method the
closed winters select) and is kept.

**Abstraction test.** Stripped of nouns: a recurring wave reaches each group of units at a stable lag behind the group it
follows, while its calendar timing and its lag behind the first group it reaches move from cycle to cycle, so a fixed
forward window holds whichever groups' waves fall inside it this cycle; carrying what the same window held in past
cycles, or timing a group from the first group the wave reaches, misses a group whose wave has always come after the
window and this cycle falls wholly inside it. Nearest by mechanism, read for latent structure:
- task157 reads a returning cohort's size off its own leading edge at a timing ratio every earlier wave kept on the
  calendar; here the calendar timing is what moves, the North's wave has not begun at the as-of, and its timing comes
  from another region's wave by a stable lag while its size is each hospital's own per-wave draw.
- task142 builds a quarter's upper visit percentile from admissions and lengths of stay; here the call is an expected
  draw, and no percentile, length of stay or queue decides it.
- task151 and task157's threshold payoffs need a distribution; here every surge spell lies wholly inside or wholly
  outside the window, so the expected draw is a sum of whole spells and no distribution of a trigger decides it.
- task181 nowcasts specimens by laboratory route; here nothing is incomplete at the as-of, and the forecast is of a wave
  that has not started where it is coming.
- task190 and task501 read surveillance and an eigenvalue of a who-passes-to-whom matrix; here no transmission
  parameter is estimated: the lag is read from where the wave was in each closed winter, and the upstream region is the
  one whose lag held.
None shares the latent structure, the default path and the correction.

**Sources, one line each.**
- Seed FC31 header and Situation (`status.py task160`): the world, the decision (the January block with two agencies),
  the quantity (agency shifts worked while a member's surge plan is active); nothing else of the seed is read or kept.
- `guard.py mechanisms --objective forecasting` (71 builds): wave and timing ground on file is a returning cohort's
  leading edge (task157), a fixed-anniversary step (task107 v4), a business-day release (task102) and an announced
  threshold step (task134 v2); none times a window's content by a wave's spread from one region to the next.
- `stumping/references/client/layer2-rigor-patterns.md`: healthcare-delivery patient-flow pattern 2 (staff to the
  time-varying curve, not the average) and utilization pattern 1 (capped demand); this build's surge curve moves in
  time by region, and the method that holds is read off where each region's wave fell in the closed winters.
- `stumping/references/strategies.md` F6 (method selection: the fit is wrong out of sample because the quantity is
  stationary only in a constructed clock) and F1 (a clock the closed window never exercised): the clock here is each
  region's own wave time, built from the lag behind the region it follows.
- `two-layer-task-design.md`: the client's example of validating a forecast on data it was not built on; the calendar
  carry, the Southeast-anchored lag and the regressions on the Southeast's timing all fail on closed winters.
- The CDC's regional influenza surveillance (FluView, by HHS region): seasons often reach the South first and the upper
  Midwest weeks later, with the gaps moving from season to season; the lags here (Central 3.5 to 14.5 days behind the
  Southeast, the North about four weeks behind Central, moving about four days either way) are sized to that pattern.
- task142 (the nearest world, three waves back) and task157 (the nearest driver): differentiated on the card.

## Default path

1. Read the 2026-27 pool agreement: the pool funds the agency RN shifts that staff a member's surge unit and start
   while its surge plan is active (from the declared activation to the declared stand-down in the capacity system);
   the January block covers every member's surge unit for the four weeks from Monday 4 January to Sunday 31 January
   2027 and is set at the pool's expected draw over those weeks, to the nearest 50 shifts; Schedule A lists 24
   members, the eight North hospitals from 1 November 2026.
2. Stitch the capacity census's two layouts (member numbers and report dates to 30 June 2024, facility ids and census
   dates after) through the roster, and price each member's surge nights at its surge plan's agency staffing per
   level (the surge plan register).
3. Take the pool's draw in each closed winter's block weeks (the four weeks from the first Monday in January,
   2022 to 2026): 2,944, 1,730, 3,050, 1,606 and 2,900 shifts, every one of them the sixteen southern members' (the
   North's surge nights fell in none of those weeks).
4. Average the five Januaries: 2,446 shifts; round to the nearest 50.

Ends on: 2,450 (built: 2,446.0, 2,439.4 shift by shift at the declared times; last January alone 2,900, the five
Januaries trended 2,382).
Golden: 600 (built: 595.6, the eight North members' mean per-wave draw; the sixteen southern members' expected
draw in the block weeks is none).

## Stump sentence

Averaging the closed winters' January block draws, the sixteen southern members' surge nights in those four weeks at
their surge plans' agency staffing with the North's none, files 2,450 shifts; the step that lands it there is reading
January by the calendar when the respiratory wave's timing moves by weeks from winter to winter, and the analyst who
times the North from the Southeast instead, whose lead over the North moved by two weeks or more, puts its wave partly
before the block; the North follows Central by about four weeks, and Central's spells began 9 to 17 December, so this
January holds the North's whole wave and none of the south's: 600 shifts.

## Three rules

Task type: patient-flow-beds-workforce-optimization (Healthcare Delivery & Health Economics), which serves Forecasting & Predictive Modeling in the taxonomy; the forecast is a health system's surge workforce demand for a window not yet open.
Domain test: the deciding quantity is the January surge staffing demand of each region's hospitals, forecast the way a health-system capacity planner forecasts a winter surge: by where each region's respiratory wave will fall in the window, timed from the region it follows by the lag the closed winters show, and turned into agency RN shifts through each hospital's surge unit staffing at each surge level.
Swap: "how many megawatt-hours should the cooperative block-buy for the four weeks from 4 January" keeps a block and a window but loses the respiratory wave travelling north from region to region, four weeks from Central to the North, the surge plans that open agency-staffed units when a hospital's census crosses its triggers, and the hospitals that join a pool with their own wave still to come, so nothing places one region's whole demand inside a window it has never reached.
Layer 1: the capacity system replaced on 1 July 2024 (member numbers, report dates the morning after each census night and S1/S2 codes in the old export; state-prefixed facility ids, census dates and 1/2 in the new, its last seven nights provisional); the roster carrying every key; Crestfield's member shift report with UTC times, its own site codes, a night on two lines and a late cancellation billed at four hours; Inland Seas' weekly workbooks with payroll dates (the dictionary's convention) and facility short names; two staffed-bed changes on file; wastewater results posted preliminary and revised, weekly in the North; the cooperative's July-to-June fiscal year against the November-to-March pool season; the surge plan register as a PDF table with each plan's own revision history; the block book split by agency slots. Each is how those systems write their files and none carries the call (asserted neutral, R2).
Layer 2: forecast_uncertainty, model choice on out-of-sample error: the closed winters' January draws are stationary only in each region's own wave time, and the North's wave time is fixed by its lag behind Central, which, left out one winter at a time, missed by 2.5 days on average by centres and 3.1 by first surge nights, not by its lag behind the Southeast (5.5 and 6.8) or a regression on both southern regions' timing (15.6 and 6.6); the choice that flips the call is timing the North from the region whose lag held rather than reading January by the calendar or timing the North from the region the wave reaches first.
Decisive step: forecast the block weeks' draw region by region: the sixteen southern members' waves have run their course in December, and the North's, which every closed winter brought about four weeks after Central's, falls wholly inside the block weeks from Central's spells this winter, so the draw is the North's own per-wave surge draw at its surge plans' staffing.
Not semantics: every field is read correctly on the default path and on the Southeast-timed path (each member's surge nights and levels, both layouts, the staffing per level, the block weeks, the members and their join dates, each member's region); reading every one of them right still leaves the analyst choosing how to forecast the window and which region to time the North from, and the calendar files 2,450 while the Southeast files 450 or less.
Not rule application: the agreement files the estimand (the members, the funded shifts, the four weeks, the expected draw, the rounding) and the register files each hospital's staffing per level; no filed rule or procedure says when a region's wave arrives, which region the North follows or how to forecast the draw, and executing every filed rule on the closed Januaries files 2,450.
Analyst test: a strong analyst who stitches both capacity layouts, reads the agreement and the register correctly and averages the closed winters' January block draws at the register's staffing files 2,450 shifts against the golden 600 (executed in checks.py on the generator's clean truth); the analyst who sees the early season and times the North from the Southeast, the region the wave reaches first, files 450 or less (400 aligning the whole census on the Southeast), and only timing the North's wave by its lag behind Central files 600.
Estimand: the 2026-27 pool agreement (clauses 1.2, 3.1, 5.1 and 5.2 and Schedule A) files the population (every Member's surge unit, the 24 members of Schedule A, the eight North hospitals included from 1 November 2026, members not yet drawn on in the pool's history counted), the outcome (agency RN shifts that staff a member's surge unit and start while its surge plan is active, one per nurse per scheduled shift), the window (00:00 Monday 4 January to 23:59 Sunday 31 January 2027, Eastern time), the unit (the expected number of shifts over the block weeks) and the rounding (the nearest 50); there is no comparison.
No decoy: no memo, draft, forecast, stakeholder figure or earlier block order argues a figure for the 2027 block; the surveillance outlook forecasts two weeks of admissions correctly and ranks nothing; the block book states what was filed in past winters (the first block from the members' surge plans, each later one the last January's draw carried, missing the outturn by two-fifths or more in both directions), not what January holds, and its 2026-27 row is blank.
No certified replay: no shipped figure is reproduced to recover a method; the closed winters are the analyst's own out-of-sample record, every one of them read alike by every method.
Lesson: a model learns that a seasonal window's content is set by where each region's wave falls this season, timed from the region it follows by a lag the record holds, that the region a wave reaches first is not the clock for every region after it, that a regression leaning on the first region's timing extrapolates a record this season has left, that a calendar window which never held a region's wave can hold all of it in an early season, and that a pool's own history validates nothing for members whose clock it never saw; no build on file times a window's content by a wave's spread from one region to the next.

## Readability screen

Six tests per rung (1 a filed sentence names it or sends the solver looking, 2 a column, key or marker makes it a
row predicate or a header join, 3 an opponent reflex, 4 a control or corpus scores it, 5 the hygiene battery finds
it, 6 one subtraction, ratio or half of a figure). Figures built in `generator/calc.py` and `generator/pack_read.py`,
asserted in `generator/checks.py` (LADDER, REFLEX, R3a, R3b).

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the closed Januaries' block draws averaged, the North at its own January surge nights (2,450) | the agreement's block clause names the four weeks from the first Monday in January | the census's dates and levels | yes, the default | the analyst's own back-test: each closed January carried to the next missed it by 43 to 90 per cent | no | yes, a mean | readable |
| R0b last January alone (2,900) | no | the census | yes | the same back-test; the block book's own carried blocks missed by two-fifths or more | no | yes | readable |
| R1 the pool's own post-peak weeks: the sixteen southern members aligned on each winter's Southeast centre, the North at the same draw per bed (none) | no | the census | yes, the early-season correction | the North's own capacity reports: their spells never sat in the south's post-peak weeks | no | yes | readable |
| R1c the North timed from the Southeast, its centre or first surge night plus the closed winters' mean lag (400 or 450) | no | the census and the roster's regions | yes, the wave reaches the Southeast first | the out-of-sample lag: the Southeast's lead over the North, carried from the other four winters, misses 2023-24 by 10 days by centres and 2024-25 by 16 by first surge nights | no | yes, one addition | readable |
| R1d every member's census aligned on this winter's Southeast centre (400) | no | the census | yes, the analog | the same: Central's gap behind the Southeast ran from 3.5 to 14.5 days, and is 17.5 this winter | no | yes | readable |
| R1e the North's first surge night regressed on both southern regions' first nights (50) | no | the census | yes, the multivariate fit | the out-of-sample record: left out one winter at a time it misses by 6.6 days against Central's lag's 3.1, and it carries the Southeast 33 days before its earliest closed winter | no | no, a three-parameter fit | readable |
| R2c the closest closed winter by the Southeast's timing, 2022-23, taken whole (1,750) | no | the census | yes, the analog | 2022-23's Southeast centre fell a month later than this winter's | no | yes | readable |
| R2d one month later: the four weeks from the first Monday in February averaged (650) | no | the census | a half step | the shift is a month, not each region's lag | no | yes | readable |
| R2f the season's usual total less what this winter has drawn by 31 December (550) | no | the census | a budget reflex | the North's draw does not move with the south's season total | no | yes, one subtraction | readable |
| R3 (decisive) the North timed by its lag behind Central: the south's waves over by 31 December, the North's whole wave inside the block weeks at its own per-wave draw (600) | no sentence names a wave, a lag, a region's timing, which region leads which or a forecasting method; the agreement files what is funded and when the block runs | no column marks a wave, a lag, a phase or an upstream region: the census carries nights, levels and staffed beds, the roster a region, a city and a join date | no: the reflexes are the calendar, the analog, the trend, the pool's own post-peak profile, the Southeast's lead and the regressions on its timing | none ships: no document scores a method, the closed winters are read alike by every method | no: nothing is duplicated, missing or mis-keyed on the call's rows | no: two candidate lags read from five winters' timing, the one that held chosen, the North's wave placed, its per-wave draw built from its own nights and staffing | silent |

## Semantic fork table

Every term in the main ask and every convention the main computation needs. Every id is asserted in
`generator/checks.py`.

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "block-book for the four weeks from Monday 4 January" | the block clause: the four weeks from the first Monday in January, 00:00 Monday 4 January to 23:59 Sunday 31 January 2027, Eastern time | calendar January | same call (asserted: under every pooled lag the North's typical wave falls 8 to 27 January, and the south's last surge night is in December) | the agreement, clause 5.1; same call, asserted |
| SF2 | "how many agency RN shifts" | the pool's expected draw over the block weeks (clause 5.2) | a cover figure at a high percentile | a larger block | the agreement, clause 5.2 ("set at the Pool's expected draw over the Block weeks") |
| SF3 | the pool's draw | agency RN shifts that staff a member's surge unit and start while its surge plan is active (clause 3.1) | every agency shift at a member during the weeks | a far larger block | the agreement, clause 3.1 |
| SF4 | the members | the 24 hospitals of Schedule A, the eight North hospitals from 1 November 2026 | the sixteen members of the pool's history | none (asserted) | Schedule A |
| SF5 | a shift | one nurse for one scheduled shift, 07:00 to 19:00 or 19:00 to 07:00 (clause 1.4) | an agency billing line | same call (the call reads staffing per level, not billing lines) | the agreement, clause 1.4; same call, asserted |
| SF6 | the surge plan's activity | from the declared activation to the declared stand-down (the declaration log); the census night's level is the level in force at its midnight census | the census night's level for the whole day | same call (asserted: shift by shift 594.0, per night 595.6) | clause 1.5; same call, asserted |
| SF7 | the staffing a surge level draws | the register's agency RN shifts a day at each level, unchanged for 2026-27 | the closed winters' worked shifts per surge night for the south | same call (the North has no worked pool shifts; last winter the south's funded shifts ran 0.6 per cent under the register's staffing at the declared times, asserted, and the golden is the same bin at either: 589.7 and 590.7 scaled) | the register; same call, asserted |
| SF8 | the as-of | the census to the night of Sunday 20 December 2026, every file pulled on Monday 21 December | data to 30 November | same call | the export manifest |
| SF9 | the rounding path | the expected draw unrounded, then to the nearest 50 | each member or region rounded first | same call (asserted) | clause 5.2; same call, asserted |
| SF10 | the closed winters | the five winters on the capacity system, 2021-22 to 2025-26 | the winters the pool has history for (the same five) | same call | the census covers 1 July 2021 onward |
| SF11 | whose surge units the block covers | every Member's surge unit (clause 5.1), a Member being a hospital of Schedule A from its Pool start date (clause 1.2): the eight North hospitals from 1 November 2026 | only the sixteen members the pool's history covers | none (asserted: the sixteen draw none of the block weeks) | the agreement, clauses 5.1 and 1.2 with Schedule A; asserted |

## Ladder

Built figures from `generator/calc.py` on the clean truth, every row asserted in `generator/checks.py` (LADDER, R3a,
R3b; R1e in REFLEX) and recomputed from the bundle by `generator/verify.py`. Each block is the expected draw over the block weeks,
to the nearest 50 shifts.

| Rung | Construction | Block | Dies to |
|---|---|---|---|
| R0 default | the closed Januaries' block draws averaged (2,944, 1,730, 3,050, 1,606, 2,900) | 2,450 (2,446.0) | its own back-test: each closed January carried to the next missed it by 43 to 90 per cent; the January draw moves with the wave's timing |
| R0b | last January alone | 2,900 (2,900) | the same |
| R0c | the five Januaries trended | 2,400 (2,382.4) | the same |
| R1 | the pool's own post-peak weeks: the south aligned on each winter's Southeast centre, the North at the same draw per bed | none (0) | the North's own capacity reports: its spells never sat in the south's post-peak weeks |
| R1b | the south's post-peak weeks, the North at its own calendar January | none (0) | the same |
| R1c | the North timed from the Southeast: its centre at the pull plus the closed winters' mean lag (37.7 days), or its first surge night plus the mean first-night lag (42.2) | 400 (417.2), 450 (465.2) by first surge nights | the lag behind the Southeast ran from 29.5 to 44.25 days by centres and 32 to 55 by first nights; left out one winter at a time it misses by 5.5 and 6.8 days on average |
| R1d | every member's census aligned on this winter's Southeast centre | 400 (384.0) | Central's gap behind the Southeast ran from 3.5 to 14.5 days, and is 17.5 this winter |
| R1e | the North's first surge night regressed on both southern regions' first nights (on the cut pack, asserted in REFLEX) | 50 (53.6) | three parameters on five winters, the Southeast's coefficient negative: left out one winter at a time it misses by 6.6 days against Central's lag's 3.1, and it carries the Southeast 33 days before its earliest closed winter |
| R2c | 2022-23, the closest closed winter by the Southeast's timing, taken whole | 1,750 (1,730) | 2022-23's Southeast centre fell a month later than this winter's |
| R2d | the four weeks from the first Monday in February averaged | 650 (657.2) | one month is not each region's lag; it reads the North's closed waves where they fell |
| R2e | a line through the January draw against the Southeast's timing | 2,850 (2,830.4) | the relation is not linear in timing; the line runs off the record |
| R2f | the season's usual total less this winter's draw to 31 December | 550 (540.4; 750 to the pull, 734.4) | the North's per-wave draw does not move with the south's season |
| R3 decisive | the North timed by its lag behind Central (26.0 to 34.25 days in the closed winters, mean 30.4): the south's waves over by 31 December, the North's whole wave inside the block weeks at its own mean per-wave draw (592, 578, 604, 608, 596) | 600 (595.6) | golden |

**Position and margins.** The golden is bracketed: the rungs above it file 650 to 2,900 (the calendar's 2,400 to 2,900,
one month later 650), the rungs below it none to 550 (the Southeast-timed 400 and 450, the regression on the
Southeast's timing 50, the season's remainder 550, the post-peak weeks none). The nearest rungs sit one bin either side, R2d at 657.2 (32.2 past the golden cell's 625 edge)
and R2f at 540.4 (34.6 under its 575 edge); every other rung is two bins or more away.

**Reflex sweep (asserted, REFLEX in `checks.py`, on the cut pack).** Thirty-four routes that skip the North's relation to
Central, each measured before the ladder was frozen. Nineteen cheap routes: the pool's season draw spread flat over the
season (four weeks of 151 days, of 22 weeks and of the chart's 21 weeks, the lowest closed season, last winter's funded
shifts) files 504 to 551; all 24 members' seasons spread flat files 647; the south's season draw or last winter's funded
shifts per staffed bed carried to the North's beds files 530 and 529; the Januaries by mean, median, last three, last,
smallest and per bed file 1,606 to 2,900; the season times its January share 2,429; the order book 1,600 and 2,320; the
season's remainder at the pull 734; the peak four weeks of each closed season 2,792. Fifteen timing routes, each
asserted to miss the golden's cell by a full bin or more: the whole census aligned on this winter's Southeast centre 384,
on its first Southeast surge night 408, on its first surge night anywhere 408 and on the southern median centre 443; on
the season's draw-weighted centre 242 (118 and 391 with the anchor three days either side), the route the rule-3
recheck found at 598.8 in the one-state world; the North eyeballed from the Southeast at its centre plus the mean lag
417, plus the median lag 513, its first night at the Southeast's first plus the mean lag 465 and plus the median lag
417; the wastewater alone, the North's peak from the Southeast's, 367; the North's first night regressed on both
southern regions' first nights 54, on the Southeast's first night alone 0, and its centre on the Southeast's centre
alone 1. Every route sits a quarter bin or more outside the golden's cell; the nearest, all 24 members' seasons spread
flat, sits at 647, 22 past the 625 edge, and the chart's 21 weeks at 551, 24 under 575. The transfers by bed are rivals,
not constructions of the golden: the North's own census gives its per-wave draw directly.

**Convergence (C1, asserted).** Nine constructions of the golden on the clean truth file 600 (594.0 to 607.0): the mean
of the five waves priced per night (595.6) and shift by shift at the declared times (594.0), the median wave (596), the
last three (602.7), the middle three (597.3), the hospital-by-hospital medians (606), the mean scaled by this winter's
southern draw against the closed winters' (607.0), every member's census aligned on Central's centre (595.6) and the
North placed by Central's first surge night (595.6). On the cut pack every Central route files 600: the census aligned
on Central's centre or its first surge night, the North at Central's centre plus the mean or the median lag, its first
night plus the mean lag, the North's wastewater peak from Central's, the North's first night regressed on Central's,
and its centre regressed on both southern regions' centres, each 595.6; its centre regressed on Central's alone 594.4;
the nearest analog winter by Central's gap (2024-25), aligned on either region, 608; and the mean scaled by last winter's
funded shifts against the register's staffing draw, 589.7 per night and 590.7 shift by shift. Every one sits at least a
quarter bin inside the cell (the nearest, 589.7, 14.7 from the 575 edge, and 608, 17 from 625). The golden sits 20.6
shifts from the 575 edge and 29.4 from 625; one sigma of the mean wave (11.7 / sqrt 5 = 5.2) leaves it in the bin.

**Timing margins (asserted, TIMING).** The North's typical closed wave (its first and last surge nights at the median
offsets of the five closed waves from their own anchor) falls 8 to 23 January from Central's centre at the pull plus the
closed winters' mean lag (30.4 days) and 9 to 23 January at the median lag (30.5); from Central's first surge night plus
the mean first-night lag (32.6) it falls 11 to 26 January, and 12 to 27 January at the median (34): at least four days
inside both edges under every pooled estimator (asserted three days clear), and the regressions on Central or on both
regions' centres place it the same way. Carried at any one closed winter's own lag (26.0 to 34.25 days by centres, 27 to
35 by first nights) the typical wave stays inside, from 4 to 19 January at the shortest lag to 13 to 28 January at the
longest (asserted), and every such route files 600 (589.6 to 595.6); only the most spread closed wave, carried at the
shortest lag, puts four of its nights before the block. A 16-night wave carried across an eight-day range of lags spans
25 of the block's 28 nights, so a single winter's lag cannot hold margin at both edges at once; narrowing the North's
spells by two days, with the lags re-centred by a day, would give each edge about two days, and is the smallest change
that would; it is not made, since every pooled estimator already holds four. The North's spells this
winter run 9 to 26 January in the generator's realised winter (never shipped), five days inside each edge; the sixteen
southern members' last surge night falls on 26 December, and at each member's longest closed-winter spell every one
stands down by 31 December.

**Worth on the graded quantity.** Reading the window by the calendar costs about 1,850 shifts; timing the North from
the Southeast leaves 450 or less in the block (400 aligning the whole census on it); only the North's lag behind Central
puts its 600 shifts inside the block.

**Out of sample.** Carrying each closed January to the next missed it by 43 to 90 per cent; the North's lag behind
Central, carried from the other four closed winters, came within 5.5 days of each winter's own by centres (2.5 on
average) and within 7 by first surge nights (3.1 on average), and its per-wave draw within 3.8 per cent of each winter's
outturn (-2.5 to +3.8); the lag behind the Southeast, carried the same way, missed by 5.5 days on average by centres
(10.25 in 2023-24) and 6.8 by first nights (16 in 2024-25); a regression of the North's timing on both southern regions'
missed by 15.6 days by centres and 6.6 by first nights, one on Central alone by 4.2 and 4.7, one on the Southeast alone
by 7.6 and 12.2. So the closed winters themselves select Central's lag as the North's clock (asserted, OOS), and the
regressions that lean on the Southeast's timing also carry it 33 days before its earliest closed winter.

**Strength.** P(one strong solver lands) about 0.16: it must see that the window's content moves with the wave's timing
(about 0.4 of strong solvers get past the calendar), include the eight North members, time the North region by region,
and then choose Central over the Southeast as the North's clock (about 0.4 of those who time regions: the Southeast is
where the wave starts and where most solvers anchor, and the two clocks separate in the record by their spread, not by
any single winter). P(both land) about 0.03 if independent and under 0.07 with any plausible correlation. The rule-3
audits' bypasses (the aligned analog, the eyeballed Southeast lag, the draw-weighted centre) are closed: every
Southeast-anchored, statewide or draw-weighted route misses by a full bin or more. The seed was fixed by rule (task
number, then the as-of month and day: 1601221) before any data was generated and is never searched; this winter's
southern amplitudes, the North's amplitudes and lags and the timing constants are design parameters that put the golden
mid-bin and keep the closed winters' record free of a chance fit to the Southeast's timing.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | every Member's surge unit, the 24 members of Schedule A, the North from 1 November 2026 | filed (clauses 1.2 and 5.1, Schedule A); SF4, SF11 |
| 2 | Unit of account | one nurse for one scheduled shift; the expected draw over the block weeks | filed (clauses 1.4, 5.2); SF2, SF5 |
| 3 | Attribution window | 4 to 31 January 2027, Eastern time, by shift start | filed (clause 5.1); SF1 same call asserted |
| 4 | As-of dating | the census to the night of 20 December 2026, pulled 21 December | filed (the export manifest); SF8 |
| 5 | Version basis | the register's 2026-27 staffing per level | filed (the register); SF7 |
| 6 | Denominator | none (a count) | n/a |
| 7 | Weighting | none | n/a |
| 8 | Window length | the closed winters the lag and the per-wave draw are read from | C1: five, three or the middle three winters the same block (asserted) |
| 9 | Boundary inclusivity | a shift starting at 00:00 on 4 January is in, one at 00:00 on 1 February out | C1: no surge shift near either edge in the realised winter, and every pooled estimator three days clear (asserted) |
| 10 | Rounding path | the unrounded expected draw to the nearest 50 | filed (clause 5.2); SF9 |
| 11 | Tie-break | none | n/a |
| 12 | Maturity and censoring | Central's spells open at the as-of (six of its seven members) | C1: every one ends before the block weeks under any closed winter's spell length (asserted) |
| 13 | Order of operations | each hospital's nights priced, summed, then rounded | C1 (asserted) |
| 14 | Row order | sums | C1 |
| 15 | Duplicate resolution | none on the call's rows (one capacity report per member and census night) | C1 (asserted) |
| 16 | Identity normalisation | member numbers to facility ids through the roster | C1: one facility id per member number (asserted) |
| 17 | Netting against gross | none | n/a |
| 18 | Dimensional units | shifts a day at each level against shifts | filed (the register) |
| 19 | Code and status semantics | S1/S2 in the old export, 1/2 in the new | the data dictionary's field notes; C1 (asserted) |
| 20 | Integerisation | none before the total | the golden mid-bin with one sigma (asserted) |
| 21 | Clause scope | the 2026-27 agreement governs the 2027 block | filed |
| 22 | Forward window contents | the members' surge nights in the block weeks | forecast from the records (the decisive step); no file covers the window |

## Literal reader

Executing the prompt and the 2026-27 agreement word for word gives the expected number of agency RN shifts, one per
nurse per scheduled shift, that staff a Schedule A member's surge unit and start while its surge plan is active
between 00:00 on Monday 4 January and 23:59 on Sunday 31 January 2027, Eastern time, the eight North members
included, to the nearest 50; no shipped sentence says when any region's surge will come, which region the North
follows or how to forecast it, so a literal reader must forecast it from the records; the easy method on the same
literal estimand (the closed Januaries averaged) files 2,450, timing the North from the Southeast files 450 or less,
and the fork table leaves no reading under which any rung is the golden.

## Oracles

- The closed winters' capacity reports: every method reads them alike; on the wrong paths they supply the January
  averages and the Southeast's lead, and the analyst's own back-test on them rejects both. No closed window holds a
  2027 figure.
- The block book: what was filed in each closed winter, at the time (the first block from the members' surge plans,
  each later one the last January's draw carried); it states no 2027 figure and ranks nothing.
- The surveillance outlook: two weeks of regional admissions to 1 January, correct for its horizon; it holds no January
  figure.
- No control ties only under the golden.

## Ask sheet

**Main call's declared row population:** the capacity census in both layouts (every member, every census night), the
declaration log, the surge plan register's staffing per level, the agreement's clauses 1.2, 1.4, 3.1, 5.1 and 5.2 with
Schedule A, and the roster's keys. Device and hazard rows in it: 0 (asserted, DEVICE: the block computed with both
agency reports, the wastewater, the outlook and the block book deleted is unchanged to the shift; the call reads no
agency line).

**Ask A. For each of the 16 hospitals in last winter's pool, the agency RN shifts the pool funded between 1 November
2025 and 31 March 2026** (16 figures, whole shifts).
- H18 home: the audit trail of the pool's last settlement, member by member; the block prices the coming draw and
  never reads last winter's billing lines.
- Use: the workbook's member table, which the pool manager sends each member's finance office with its winter
  statement.
- Basis (filed, the agreement): clause 3.1 (the pool funds the agency RN shifts that staff a member's surge unit and
  start while its surge plan is active, from the declared activation to the declared stand-down) and clause 1.4 (a
  shift is one nurse for one scheduled shift, 07:00 to 19:00 or 19:00 to 07:00, Eastern time); clause 7.1 records that
  the 2025-26 agreement held the same terms.
- Primary A2 (D6, one shift on several ledger lines): Crestfield's member shift report bills each night shift on two
  lines, one for each calendar day it covers (19:00 to 24:00 and 00:00 to 07:00 local), both under the night's
  timesheet number; counted line by line, every Crestfield night on a surge unit counts twice, at every one of the 16
  hospitals (Crestfield fills every second slot on every surge shift). Fair: the timesheet number and the 5.0 and 7.0
  hours that make one 12-hour shift, with clause 1.4 counting one per nurse per scheduled shift. Silent: line ids are
  unique, no line repeats another, every site code joins, and no shipped sentence says how Crestfield bills a night.
- Second silent device D3 (a billing line with no worked shift behind it): Crestfield bills a booking the member cancels
  inside the six-hour cut-off as one line of 4.00 hours under its own timesheet number, its start and end times the
  booked shift's twelve hours, on the same unit and bill-to as the booking; 85 such lines last winter at all 16 members,
  57 of them on surge units. Counted as shifts they move every Ask A figure (48 in all), Ask B at 14 members (37 in
  all) and both chart figures. Fair: clause 4.2 files the four-hour term as a plain rate term (a booked shift the Member
  cancels less than six hours before it starts is billed at four hours of the Agency's rate), the rate schedule states
  the same term, clause 1.4 counts nurses on scheduled shifts, and every worked line bills the hours it spans (12, or 5
  and 7 for a night, 11 or 13 across a clock change) while a cancellation bills 4.00 against a 12-hour span. Silent: no
  column, code or status marks a cancellation, no sentence names a cancellation line or says where clause 4.2 shows in
  the report, and the line's unit, times and bill-to read like a worked shift's. Independent of A2 (one line, not a
  split night) and of the payroll-date convention (Crestfield's report, not Inland Seas' workbooks).
- Hazard B1 (documented): Inland Seas dates every shift by its payroll date, the day the shift ends, as the pool
  office's data dictionary records for both workbooks; read as the night's start, each spell's last Inland Seas night
  reads as starting after the stand-down, at every one of the 16 hospitals. The dictionary files the convention; the
  solver still applies it to the night rows to recover each shift's start.
- Stops (built and asserted): S1 the cracker (lines counted, cancellation lines among them, the dictionary's payroll
  convention applied): all 16 miss; S1a A2 cracked alone: all 16 still miss on D3; S1b D3 cracked alone: all 16 still
  miss on A2; S2 lines counted and payroll dates read as start dates: all 16 miss; S3 both cracked: the golden.
- Span: the agreement, the register (surge units), the declaration log, the roster, Crestfield's report, Inland Seas'
  workbook, the dictionary (7 files).
- Realism: agency timekeeping splits a night shift at midnight so each calendar day's hours are paid at that day's
  rate, and bills a late cancellation at its guaranteed minimum against the booked shift; Inland Seas invoices its late
  cancellations on its monthly statement, outside the weekly workbooks; the export keeps what the billing system holds.

**Ask B. For each of the same hospitals, how many of the agency shifts worked there in that time were billed to the
pool though the pool did not fund them** (16 figures, whole shifts).
- H18 home: the reconciliation of the agencies' billing to the pool's funding, the shifts returned to each member's
  account at settlement (clause 6.2).
- Use: the same member table, the column the members' finance offices settle.
- Basis (filed): clause 3.1 as above; clause 6.2 (an agency shift billed to the pool that the pool does not fund is
  returned to the member's account); the ask's own word "worked" (a cancelled booking staffed no shift).
- Primary A2 through HA7 and HA4: every Crestfield night among the surge-request bookings on other units and the teams
  that report after a stand-down is on two lines (asserted, DEVICE lines counted moves Ask B at 12 members).
- D3 through the surge-request bookings cancelled late: billed to the pool and staffing nothing, each reads as a worked
  shift the pool did not fund (asserted, DEVICE late-cancellation lines counted moves Ask B at 14 members).
- Hazards: B1 as above (each spell's last Inland Seas night moves from funded to billed and not funded when read as a
  start date); HA1 Crestfield's times in UTC (its column names say so); HA2 declarations at the 14:45 bed meeting (the
  day shift of an afternoon activation is not funded, of an afternoon stand-down is); HA3 the skeleton opening the night
  before a morning declaration (not funded, billed to the member); HA4 the team that reports for the shift after a
  stand-down (billed to the pool, not funded); HA5 the activation day's day shift booked as staffing (funded, billed to
  the member); HA6 Inland Seas' facility short names and Crestfield's site codes against the roster; HA7 the nurses a
  member's staffing office books on the open surge request for its other units, mostly the emergency department's
  holds (booked against the surge request and billed to the pool like the surge unit's own, worked on another unit, so
  not funded; the bulk of every member's Ask B figure).
- Stops: S0 the census night's level for the whole day (moves Ask A and Ask B only at the members with an afternoon
  stand-down last winter, asserted); S1 the cracker: all 16 miss; S1a A2 cracked alone: 14 still miss; S1b D3 cracked
  alone: 12 still miss; S2 both cracked: the golden. Last winter's golden figures run from 2 to 19 a member, none nil.
- Span: the agreement, the declaration log, the roster, both agency reports, the dictionary (6 files).
- Realism: payroll systems pay a night shift on the day it ends; the date on the line is the payroll date.

**Ask C. The chart** (`pool_shifts_winter_2025-26.png`): the shifts the pool funded in each of the 21
Monday-to-Sunday weeks from 3 November 2025 to 29 March 2026, by the week each shift started in, labelled with the
busiest week's funded total and the agency shifts starting that week billed to the pool. Graded on those two figures
(1,359 funded and 1,415 billed to the pool in the week of 19 to 25 January 2026, the busiest week 536 shifts clear of the
next); the chart file itself is an instruction-following point, so no chart part is free. A2 moves both figures (1,705
and 1,778 counted line by line), D3 moves both (1,382 and 1,452 with the cancellations counted), the payroll date read
as a start date moves the billed figure (1,422), and the cracker's route moves both (1,728 and 1,815; the mirror, at the
census night's level for the day as well, 1,723 and 1,822).

**Hazard table.**

| Hazard | Asks moved | Per-ask delta read the easy way |
|---|---|---|
| A2 Crestfield's nights on two lines | A, B, C | A: every member's Crestfield surge nights twice (728 in all); B: every Crestfield night among the other-unit bookings and post-stand-down teams twice (12 members); C: both figures |
| D3 Crestfield's late cancellations on one four-hour line | A, B, C | A: each cancelled surge-unit booking during an active plan counted funded (48 in all, every member); B: each cancelled surge-request booking counted as a returned shift (14 members); C: both figures |
| B1 Inland Seas' nights by payroll day (documented) | A, B, C | A and B: each spell's last Inland Seas night moves from funded to billed and not funded (27 shifts, every member); C: the billed figure |
| HA1 UTC in Crestfield's report | A, B, C | evening starts a day late if read unconverted |
| HA2 to HA5 the declared times and bookings | A, B, C | read off the census night's level: the funded and returned shifts at each afternoon stand-down |
| HA7 surge-request bookings on other units | B, and A for the mirror | counted funded when the bill-to is read as the funding test; each Crestfield night among them twice when lines are counted |

**Referee.** None: the agreement's clauses file the basis and nothing shipped totals the funded or returned shifts.

**Cracker sheet** (the cracker landed the call, ran the hygiene battery, executed every filed rule and documented
convention, Inland Seas' payroll date included, converted every documented time zone, and counted Crestfield's billing
lines as shifts):

| Ask figures | The cracker's route | Device that holds | Verdict |
|---|---|---|---|
| A, funded shifts at each of the 16 hospitals (16) | clause 3.1 with the declared times, every billing line counted, cancellation lines among them, payroll dates read as the day each shift ends | A2 Crestfield's two-line nights and D3 its late-cancellation lines, each alone at all 16 | miss |
| B, returned shifts at each of the 16 hospitals (16) | clauses 3.1 and 6.2, the same reading | A2 through HA7 and HA4, D3 through the late-cancelled surge-request bookings | miss |
| C, the busiest week's funded total and the shifts billed to the pool that week (2) | Ask A's construction by week | A2 and D3, each alone | miss |

**Single cracks.** With A2 cracked alone the cracker keeps 2 of 34 (two Ask B figures); with D3 cracked alone, 4 of 34
(four Ask B figures). Each is asserted at 40 or under (ASK, each silent device cracked alone).

**Mirror sheet.** The mirror stops at the census night's level for the whole day, the payroll date read as the date
worked and every billing line counted; it keeps no Ask A, B or C figure.

Measured by: `generator/cracker.py` (run on the cut pack by `checks.py` on every build).

Mirror leakage: 0.0 per cent of ask weight (no chart part is free; 34 ask criteria).

Pair ceiling: 28.5 (the cracker at 38 + 7 + 55 x 0/34 = 45.0, the mirror at 5 + 7 + 0 = 12.0); both top responses on
the call: 45.0. With A2 cracked alone the pair is 30.1 and with D3 cracked alone 31.7, so each silent device holds the
asks on its own; with both cracked it is 56.0. All asserted in `checks.py` on the cut pack (ASK pair lines). Rerun from
the generated rubric at stage 4. Criteria supplied: the call and its three components, 16 funded figures, 16 returned
figures and the chart's two figures, plus instruction-following.

## Surface screen

`guard.py surface task160` exits 0 and promotes five pairs, none with a hard tell (no shared file name, schema, invented
name or same-seed table): task145 and task446 on the card-level same-driver signature (gap time, G16, Gate G
forecasting), each differentiated on the card at the draw; task231 on corpus surface similarity alone (a
survey-research data-quality build: another domain, objective and decision; the shared features are the house idioms of
a dictionary, a manifest and a how-many opening); task161 and task162, registered after this card (01:20 and 01:37
against 00:47) in other domains (supply chain, product analytics), on the decisive gap (time) and the decision type
(quantity_figure) they share with it as consecutive draws: their decisive generators (G7 and G13) are not this build's
G16, and the two axes they repeat were this card's first. A first cut also paired task460 on one identical table, the
dictionary's `file, field, definition` sheet; the dictionary now carries a title row and a format column in the pool
office's own layout. Schedule A lists each member's city with its state, and the persona sweep (`guard.py people`)
finds Brandon Williams alone. `guard.py heart task160` WARN, exit 0: `repeat.question_form` (how-many, task470),
answered at the draw; nearest driver 0.10 (task157); the two NOTEs are the differentiated older builds above.

## Leak sweep

`leak.py task160 --asof 2026-12-21` returns REVIEW, no LEAK; every line answered:
- Sweep 3, the agreement carries the call's words (block, agency RN shifts, Monday 4 January to Sunday 31 January
  2027): it files the estimand (clauses 5.1 and 5.2, the four weeks and the expected draw to the nearest 50) and
  carries no block figure and no forecast; the 2026-27 row of the block book is blank (asserted, R3c). The rate
  schedule's 112.00 is Crestfield's spot rate in dollars an hour, not a count of shifts, and sits beside no member.
- Sweep 4, stump-paragraph terms in the agreement, the register and the rate schedule (region, Southeast, Central,
  member, hospital, cooperative, staffing, census): each document's own subject (who the members are and where; each
  surge unit's staffing per level; the season's rates); none names a wave, a lag, a region's timing, which region
  follows which or how to forecast the draw (a sweep of every shipped document's text, cells and headers for lag, lead,
  follow, wave, timing, behind, ahead, upstream and spread finds none).
- Sweep 6, files naming the members beside numbers (the roster's beds, the register's staffing, Schedule A's start
  dates, the workforce survey's vacancy returns): records per member, none ranking members on the block or on either
  ask's quantity.
- Sweep 9, dates after the pull: the block book's 2026-27 block weeks (4 to 31 January 2027, the agreement's clause
  5.1) and the admissions outlook's fourteen forecast days to 1 January 2027, forward-looking records allowed by file
  (`reduce-house-fixes` H16).
- Sweep 10: no writer signature and no stamp outside 2021-07-01 to 2026-12-21 in the pack or the goldens
  (`scrub_producer_metadata.py` audit, both directories).

## Build record

Stage 3 rework, 2026-10-18 (the multi-state world, the second silent device on Ask A, the North's lags re-drawn so the
closed winters carry no chance fit to the Southeast's timing, and the rule-3 recheck's routes asserted, in one rebuild).
`build.py`: `checks.py` 181 run, 0 failed (the three-rules block R1 to R3c on the clean truth and the pack, every SF row
SF1 to SF11, the ladder's rungs and the golden's bracket, thirty-four REFLEX routes each a quarter bin or more outside
the golden's cell and the fifteen timing routes a full bin or more, the out-of-sample record against the Southeast's
lag and every regression, nine constructions of the golden and fourteen more on the pack, the one-sigma corridor, the
timing margins under every pooled and single-winter lag, both asks equal to the truth with every device and hazard
moving its stated figures, D3's lines, terms and reach, the chart's two figures, the cracker pair on the cut pack at
28.5, each single crack at 30.1 and 31.7, both on the call 45.0, mirror leakage 0.0 per cent, the separation line by
deletion, the input gates, the realism sweep and the dates); `verify.py` (csv, openpyxl, pypdf and numpy, no generator
import) 0 failed, every format read back with a positive control, the North timed from Central and from the Southeast
on its own code path, the regression back-test, the chart's two figures, and the goldens and write-up checked against
its own recomputation; two consecutive builds byte-identical (target, golden, figures.json, submission);
`figures_check.py` 0 absent (31 figures); `voice-check.py` PASS (807 characters); `precut.py` exit 0; `leak.py` REVIEW,
no LEAK, every line answered; the H1 audit clean on the pack and the goldens; `guard.py validate` clean, `surface` exit 0
(five pairs, above), `heart` WARN (answered). 16 files in 4 formats (csv, xlsx, pdf, json), the largest the legacy
capacity export at 26,406 rows; distractors `rn_workforce_survey_2025q1_2026q3.xlsx` and
`agency_rate_schedule_2026-27.pdf` in `metadata.json`, each deletion leaving the call and every ask unchanged.
`target.zip` cut from the final rebuild, 16 entries equal to `target/` byte for byte. The seed was fixed by rule
(1601221) before any data was generated and never searched. Every file in the pack carries the pull's modification
time, 21 December 2026 09:30 Eastern (`dataset-generation` section 9).

## Tried and rejected
- Ask B as first built (only the teams that report after a stand-down): 8 of 16 members nil and every figure 0 or one
  team's size, so an all-nil response took half the column and cracking B1 alone kept all 16 (pair 47.3); the nurses a
  staffing office books on the open surge request for its other units (HA7) now give every member 6 to 20, and A2
  reaches Ask B at 15 of 16 (pair with B1 cracked 36.5).
- The first cut's hospital names: 14 sat within reach of a real hospital or institution (Calhoun Memorial, Little
  Traverse, Clinton Valley, Fairlane, Lakeshore Macomb, Saginaw General and others, `## Draw` item 10); renamed, every
  figure unchanged (figures.json byte-identical).
- The first cut's southern staffing: the pool's season draw spread flat over the season (617) and the south's draw per
  staffed bed carried to the North (612) both fell in the golden's cell by coincidence, without timing any wave; every
  southern member's Level 2 staffing was raised by two shifts a day (the North's untouched, the golden unchanged), and
  this winter's southern amplitude was set at 1.012 and 1.006 so the season's remainder (668) stays a bin off while the
  scaled construction (591.7) stays in the cell; one quantity, the south's December deficit, finances both, and the
  window that clears both runs from 48 to 91 shifts (66 built).
- The rival clause at 2,850: the five Januaries' mean (2,872.8 per night, 2,873 shift by shift) sits two shifts from
  the 2,875 edge, so the write-up states it as nearly 2,900, which both constructions share.
- The dictionary's `file, field, definition` sheet, identical to task460's; the persona sweep's place pairs off
  Schedule A (`## Surface screen`).
- The chart graded on five parts (21 weekly bars, the agency split, the block weeks marked, the axis, a title) with only
  the busiest week's total carrying a device: the mirror kept the free parts and both top responses on the call stood
  at 52.2; the chart is now graded on two labelled figures, the busiest week's funded total and the agency shifts
  starting that week billed to the pool, both moved by A2 and by the payroll date, and no chart part is free (both on
  the call 45.0).
- The uniform-lag world: the North followed the Southeast by 37 to 40 days in every closed winter, so the rule-3
  audit's aligned analog (the whole census moved onto this winter's Southeast centre or first surge night) and an
  eyeballed Southeast-to-North lag both filed 602 without reading any region's relation (P(both) about 0.12); West and
  Central now trails the Southeast by 4 to 32 days across the closed winters and the North follows West and Central by
  30 to 33, with the North's wastewater tied to West and Central's, so every Southeast-anchored route misses by a full
  bin or more (aligned 1,094 to 1,282, eyeballed 0 to 90, wastewater 14) and every West and Central route files 602.
- Inland Seas' payroll date left undocumented (B1 silent, backing A2 at all 16): the judge read it as an ask-side fork,
  a convention no shipped sentence filed; the dictionary now files it in the pool office's voice for both workbooks, B1
  is a convention the cracker executes, and the ask layer rests on A2 alone (pair with A2 cracked 56.0, against 35.7
  when B1 was silent).
- The block book's even halves, the register's uniform plan-revision dates, the query labels in Inland Seas' timesheet
  detail ("Billed to pool after stand-down") and typed block totals that, in the regional-lag world, sat above every
  January's draw: each read as made by hand; the splits follow the season's Schedule A slots with an agency confirming
  short in some seasons, each member's plan carries its own revision history on working days (the North's dated when
  each joined), the detail tab carries the agency's order numbers and request references, and each later block is the
  last January's draw carried, the pool manager's practice.
- The write-up's basis at 602.4 and the rival clause "not none, the pool's own draw in the same weeks after each closed
  winter's peak": the judge's own North waves averaged 604.4 and read the clause as garbled; blocks 1 to 3 state the
  basis as about 600, the precision every defensible construction shares, with one plain clause per rival and the
  Southeast-timed rival named without a figure, its constructions running from none to 1,282.
- Ask A resting on A2 alone: with A2 cracked the asks fell whole (the pair 56.0 against the bar of 40); Crestfield's
  late-cancellation lines (D3: four hours billed on one line against a booked shift no nurse worked, clause 4.2 filed
  as a rate term) now reach all 16 members in both columns, and each device cracked alone keeps the pair at 30.1 and
  31.7.
- D3's first build billed every worked night at twelve hours, so a night across the November clock change, thirteen
  hours long, billed fewer hours than it spanned, as a cancellation does; worked lines now bill the hours as worked (11
  or 13 across a change), and only a cancellation bills fewer hours than it spans (asserted).
- The one-state world (the Two Peninsulas Hospital Association, Michigan): the North a month behind West and Central
  and West and Central four days to a month behind Metro Detroit are lags no single state's season shows, where a wave
  crosses the state in days, and the rule-3 recheck read them as implausible; the pool moved to a three-region
  cooperative (Georgia and South Carolina, Tennessee, Kentucky and West Virginia, northern Michigan), Central 3.5 to
  14.5 days behind the Southeast and the North 26 to 34 behind Central, that lag moving about four days either way.
- Lockstep onsets and copied shapes: 8 of 9 Southeast members first surged on the same night this winter, tighter than
  in any closed winter, and every member's wave had nearly the same width and height (amplitudes within about four per
  cent); each member now carries its own stable offset, its own winter jitter, its own size and its own rise and fall (a
  wave rising faster than it falls), and this winter's southern onsets spread over a week like the closed winters' (at
  most five members of a region share a first night in any winter, asserted).
- The first multi-state tuning: Central's spells this winter ran past 31 December at their longest closed length and
  the North's typical wave touched both block edges; Central's spells were narrowed, its gap this winter set at two and
  a half weeks, the North's spells narrowed and its surge staffing raised so each wave stays whole at about 600.
- The draw-weighted centre left open: aligning the whole census on the season's draw-weighted centre filed 598.8 on the
  fcb08fab cut without reading any region's relation; in the multi-state world it files 242 (118 and 391 with the anchor
  three days either side), asserted a full bin off.
- The first season's even block split, back in the multi-state block book: each member's Crestfield skeleton slot now
  enters the season's Schedule A slots, so no season splits evenly.
- The first multi-state lags: across the five closed winters the North's lag behind Central fell, by chance, with the
  Southeast's timing and rose with Central's gap, so a regression of the North's centre on both southern regions'
  centres beat Central's lag out of sample (1.8 days against 3.5 left out one winter at a time) and, carried to this
  winter's early Southeast, put the North in February and filed none; the North's lags were re-drawn (26.0 to 34.25
  days, the same spread) so the record carries no such fit: that regression now misses by 15.6 days out of sample and
  files 600, and its first-night twin misses by 6.6 against Central's 3.1 and files 54 (asserted, OOS and REFLEX).

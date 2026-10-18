# task160 design note

Architecture 1, wave 6 (new), Forecasting lane (sathya8571), numbered from seed FC31. The seed (a state hospital
association block-booking its January agency nurse shifts for a 24-hospital winter pool with two staffing agencies, the
pool funding agency shifts worked while a member hospital's surge plan is active, the block set at the forecast pool
draw) was read at its header and Situation only. Its world, decision and quantity are kept. Its mechanism (the agencies'
surge booking code only mostly agreeing with the activation days the pool funds) is not the decisive step: reading the
code against the contract's definition is data semantics, so the code survives only as Layer 1 mess and as an ask
device. The pitfall is re-found from how a winter respiratory wave reaches a state's hospitals: region by region, each
region at a lag behind the region it follows that has held in every winter on file, while the wave's calendar timing,
and its lag behind the region it reaches first, move by weeks.

The Two Peninsulas Hospital Association (fictional, Michigan) runs a winter surge staffing pool: it block-books agency
RN shifts with two staffing agencies (Crestfield Medical Staffing and Inland Seas Nursing, both fictional) and funds the
agency shifts its member hospitals work while their surge plans are active. For 2026-27 the pool grows from the sixteen
Southeast and West and Central hospitals it has covered since 2021-22 to 24: the eight North hospitals (the northern
Lower Peninsula and the Upper Peninsula) join it in November 2026, after the regional contract they bought agency nurses
through ended. Every member has filed a daily capacity report (midnight census, staffed beds, declared surge level) since
July 2021. The block for the four weeks from Monday 4 January 2027 is filed with the agencies on Tuesday 22 December
2026, set at the forecast pool draw, to the nearest 50 shifts.

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
3. Niche: a hospital association's January 2027 agency nurse block for its 24-hospital winter surge pool, when the
   respiratory wave reached Metro Detroit and West and Central Michigan in the first days of December, earlier than in
   any winter on the capacity census, and the eight North hospitals new to the pool have met the wave about a month
   after West and Central Michigan in every winter on file, while their lag behind Metro Detroit moved by four weeks.
4. Call and shape: the agency RN shifts to block-book for the four weeks from Monday 4 January 2027 (`quantity_figure`,
   count, question form how-many), to the nearest 50 shifts (the agencies take the block in lots of 50). Shape
   `single-figure`: the call with its critical components, the asks' tables on rows the call never reads, and a chart;
   criteria counted in `## Ask sheet`.
5. Mechanism keys: gap time (the evidence is what past January blocks held; the decision bets on a block whose content
   moves with the wave's timing), then population (the North's eight hospitals have no pool history); decisive generator
   G16 (the forecasting method the closed winters select out of sample: the North's wave timed by its lag behind West and
   Central, against the calendar, the pool's own post-peak weeks and the Southeast's lag), then G13 (the window holds a
   different part of each region's wave this winter) and G6 (the window's mix of regions in their waves differs from
   every January on file); Gate G `forecasting`; strategy `forecast_method_backtest` (F6: the January draw is stationary
   only in each region's own wave time, and the calendar fit and the Southeast-anchored lag fail out of sample on closed
   winters).
6. Layer 2: `forecast_uncertainty` (model choice on out-of-sample error), pattern
   `own:regional-surge-waves-timed-by-propagation-lag-not-calendar`. Library neighbours:
   epidemiology-public-health/infectious-disease-transmission-modeling (spatial spread, not an Rt or eigenvalue read) and
   healthcare-delivery-health-economics/patient-flow-beds-workforce-optimization/2 (staff to the arrival curve, not the
   daily average); this build's version times each region's surge by the lag of an epidemic's spread across the
   state's regions, read from the closed winters, choosing the upstream region whose lag held, and carries no queueing
   or percentile construction.
7. Furniture: forum `operations_desk` (the pool manager files the block; no committee approves it); forcing event
   `purchase_order_or_contract` (the block order goes to the two agencies on 22 December); organisation family
   `cooperative_or_member_body` (a hospital association is its members' body); role family `procurement_lead` (the
   winter pool manager buys the block); context artifact `capacity_report` (the association's daily capacity census);
   calibration `prior_period_close_out` (the closed winters' capacity census and declarations, which the out-of-sample
   check reads). Each is free against task194, task470 and task243.
8. Spine: the association's daily capacity census (hospital x day, midnight census, staffed beds and declared surge
   level), 1 July 2021 to 20 December 2026, two layouts across the July 2024 system change; constructed in the layout of
   a hospital association's daily capacity reporting system.
9. Deliverables: `winter_pool_block_jan2027.xlsx` (the block, its components and the ask table) and
   `pool_shifts_winter_2025-26.png` (a chart on an ask's quantity, never on the block). The format set (xlsx and png) is
   in none of the last three builds.
10. People, drawn with `guard.py names --geo "United States" --seed 160`: Greg Matthews (the winter pool manager, the
    requester, in no file the prompt names and not in the prompt), Andrew Harvey (the association's surveillance lead,
    the admissions outlook), Shawn Whitaker (the association's finance manager, the workforce survey and the rate
    schedule). Judith Harrison and Sheila Frazier were drawn first and replaced (each first name in an older build);
    Linda Ashley, drawn for Crestfield's account manager, carries no file and was dropped at the cut. Invented names
    checked on the web against real organisations: Two Peninsulas Hospital Association, Crestfield Medical Staffing,
    Inland Seas Nursing (no match). The 24 hospitals were checked when the pack was cut and 14 renamed for a real name
    within reach (`reduce-house-fixes` H21): Calhoun Memorial (a closed Georgia hospital), Little Traverse (Petoskey's
    historic hospital), Clinton Valley (the Pontiac state hospital), Fairlane (Henry Ford's Dearborn centre), Lakeshore
    Macomb (McLaren Macomb-Lakeshore), Saginaw General, Huron (Bad Axe), Capitol (Capitol Medical Center), Riverside
    (Trenton's closed osteopathic hospital), Franklin Ridge (an Ohio care centre), Grand Valley (the region's brand),
    St. Florian (Hamtramck's parish), Whitcomb (a Michigan senior residence) and St. Marys River; the replacements
    (Zielinski Memorial, Talcott, Gilmartin, Haldane Community, Tolliver General, Kastner, Haverkamp, Ellery, Brennan
    Memorial, Ruddock, Brinkerhoff Memorial, Lindell, Callister Memorial, Ashmun Bay) each returned no hospital of the
    name, after Weisel, Sturdevant, Riegler, Pelton, Lundquist, Kerwin, Fennell and Merriwether fell within two letters
    of, or inside, a real hospital or institute's name. The ten kept are place names with no institution of the name.

**Data-native sentence.** The association's capacity census records every member's surge spells day by day, and in
every winter on file the respiratory wave has reached the North's hospitals about a month after West and Central
Michigan's, while West and Central's own gap behind Metro Detroit ran from four days to a month and the wave's calendar
timing moved by five weeks; this winter both southern regions' surge spells began 2 to 9 December, earlier than ever on
file, so the four weeks from 4 January hold the North's whole wave, which no January block on file ever held, and none
of the south's, which every January block on file held.

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
  carry and the Southeast-anchored lag both fail on closed winters.
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
   2022 to 2026): 2,156, 1,566, 2,090, 1,416 and 2,084 shifts, every one of them the sixteen southern members'
   (the North's surge nights fell in none of those weeks).
4. Average the five Januaries: 1,862 shifts; round to the nearest 50.

Ends on: 1,850 (built: 1,862.4, the same shift by shift at the declared times; last January alone 2,084, the five
Januaries trended 1,774).
Golden: 600 (built: 602.0, the eight North members' mean per-wave draw; the sixteen southern members' expected
draw in the block weeks is none).

## Stump sentence

Averaging the closed winters' January block draws, the sixteen southern members' surge nights in those four weeks at
their surge plans' agency staffing with the North's none, files 1,850 shifts; the step that lands it there is reading
January by the calendar when the respiratory wave's timing moves by weeks from winter to winter, and the analyst who
times the North from the Southeast instead, whose lead over the North moved by four weeks, puts its wave past the block;
the North follows West and Central by a steady month, and West and Central's spells began 3 to 9 December, so this
January holds the North's whole wave and none of the south's: 600 shifts.

## Three rules

Task type: patient-flow-beds-workforce-optimization (Healthcare Delivery & Health Economics), which serves Forecasting & Predictive Modeling in the taxonomy; the forecast is a health system's surge workforce demand for a window not yet open.
Domain test: the deciding quantity is the January surge staffing demand of each region's hospitals, forecast the way a health-system capacity planner forecasts a winter surge: by where each region's respiratory wave will fall in the window, timed from the region it follows by the lag the closed winters show, and turned into agency RN shifts through each hospital's surge unit staffing at each surge level.
Swap: "how many megawatt-hours should the cooperative block-buy for the four weeks from 4 January" keeps a block and a window but loses the respiratory wave travelling region to region, a month from one region to the next, the surge plans that open agency-staffed units when a hospital's census crosses its triggers, and the hospitals that join a pool with their own wave still to come, so nothing places one region's whole demand inside a window it has never reached.
Layer 1: the capacity system replaced on 1 July 2024 (member numbers, report dates the morning after each census night and S1/S2 codes in the old export; facility ids, census dates and 1/2 in the new); the roster carrying every key; Crestfield's member shift report with UTC times and its own site codes; Inland Seas' weekly workbook with payroll dates (the dictionary's convention) and facility short names; two staffed-bed changes on file; wastewater results posted preliminary and revised, weekly in the North; the association's July-to-June fiscal year against the November-to-March pool season; the surge plan register as a PDF table with each plan's own revision history; the block book split by agency slots. Each is how those systems write their files and none carries the call (asserted neutral, R2).
Layer 2: forecast_uncertainty, model choice on out-of-sample error: the closed winters' January draws are stationary only in each region's own wave time, and the North's wave time is fixed by its lag behind West and Central, which held to within two days out of sample, not by its lag behind the Southeast, which missed a winter by nearly four weeks; the choice that flips the call is timing the North from the region whose lag held rather than reading January by the calendar or timing the North from the region the wave reaches first.
Decisive step: forecast the block weeks' draw region by region: the sixteen southern members' waves have run their course in December, and the North's, which every closed winter brought about a month after West and Central's, falls wholly inside the block weeks from West and Central's spells this winter, so the draw is the North's own per-wave surge draw at its surge plans' staffing.
Not semantics: every field is read correctly on the default path and on the Southeast-timed path (each member's surge nights and levels, both layouts, the staffing per level, the block weeks, the members and their join dates, each member's region); reading every one of them right still leaves the analyst choosing how to forecast the window and which region to time the North from, and the calendar files 1,850 while the Southeast files 100 or none.
Not rule application: the agreement files the estimand (the members, the funded shifts, the four weeks, the expected draw, the rounding) and the register files each hospital's staffing per level; no filed rule or procedure says when a region's wave arrives, which region the North follows or how to forecast the draw, and executing every filed rule on the closed Januaries files 1,850.
Analyst test: a strong analyst who stitches both capacity layouts, reads the agreement and the register correctly and averages the closed winters' January block draws at the register's staffing files 1,850 shifts against the golden 600 (executed in checks.py on the generator's clean truth); the analyst who sees the early season and times the North from the Southeast, the region the wave reaches first, files 100 or none (1,150 aligning the whole census on the Southeast), and only timing the North's wave by its lag behind West and Central files 600.
Estimand: the 2026-27 pool agreement (clauses 1.2, 3.1, 5.1 and 5.2 and Schedule A) files the population (every Member's surge unit, the 24 members of Schedule A, the eight North hospitals included from 1 November 2026, members not yet drawn on in the pool's history counted), the outcome (agency RN shifts that staff a member's surge unit and start while its surge plan is active, one per nurse per scheduled shift), the window (00:00 Monday 4 January to 23:59 Sunday 31 January 2027, Eastern time), the unit (the expected number of shifts over the block weeks) and the rounding (the nearest 50); there is no comparison.
No decoy: no memo, draft, forecast, stakeholder figure or earlier block order argues a figure for the 2027 block; the surveillance outlook forecasts two weeks of admissions correctly and ranks nothing; the block book states what was filed in past winters (the first block from the members' surge plans, each later one the last January's draw carried, missing the outturn by a quarter or more in both directions), not what January holds, and its 2026-27 row is blank.
No certified replay: no shipped figure is reproduced to recover a method; the closed winters are the analyst's own out-of-sample record, every one of them read alike by every method.
Lesson: a model learns that a seasonal window's content is set by where each region's wave falls this season, timed from the region it follows by a lag the record holds, that the region a wave reaches first is not the clock for every region after it, that a calendar window which never held a region's wave can hold all of it in an early season, and that a pool's own history validates nothing for members whose clock it never saw; no build on file times a window's content by a wave's spread from one region to the next.

## Readability screen

Six tests per rung (1 a filed sentence names it or sends the solver looking, 2 a column, key or marker makes it a
row predicate or a header join, 3 an opponent reflex, 4 a control or corpus scores it, 5 the hygiene battery finds
it, 6 one subtraction, ratio or half of a figure). Figures built in `generator/calc.py`, asserted in
`generator/checks.py` (LADDER, REFLEX, R3a, R3b).

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the closed Januaries' block draws averaged, the North at its own January surge nights (1,850) | the agreement's block clause names the four weeks from the first Monday in January | the census's dates and levels | yes, the default | the analyst's own back-test: each closed January carried to the next missed it by 25 to 48 per cent | no | yes, a mean | readable |
| R0b last January alone (2,100) | no | the census | yes | the same back-test; the block book's own carried blocks missed by a quarter or more | no | yes | readable |
| R1 the pool's own post-peak weeks: the sixteen southern members aligned on each winter's Southeast centre, the North at the same draw per bed (1,250) | no | the census | yes, the early-season correction | the North's own capacity reports: their spells never sat in the south's post-peak weeks | no | yes | readable |
| R1c the North timed from the Southeast, its centre or first surge night plus the closed winters' mean lag (100, or none by first nights) | no | the census and the roster's regions | yes, the wave reaches the Southeast first | the out-of-sample lag: the Southeast's lead over the North, carried from the other four winters, misses 2024-25 by 27 days | no | yes, one addition | readable |
| R1d every member's census aligned on this winter's Southeast centre (1,150) | no | the census | yes, the analog | the same: West and Central's gap behind the Southeast ran from 4 to 32 days | no | yes | readable |
| R2c the closest closed winter by the Southeast's timing, 2022-23, taken whole (1,550) | no | the census | yes, the analog | 2022-23's Southeast centre fell 21 days later than this winter's | no | yes | readable |
| R2d one month later: the four weeks from the first Monday in February averaged (1,300) | no | the census | a half step | the shift is a month, not each region's lag | no | yes | readable |
| R2f the season's usual total less what this winter has drawn by 31 December (650) | no | the census | a budget reflex | the North's draw does not move with the south's season total | no | yes, one subtraction | readable |
| R3 (decisive) the North timed by its lag behind West and Central: the south's waves over by 29 December, the North's whole wave inside the block weeks at its own per-wave draw (600) | no sentence names a wave, a lag, a region's timing, which region leads which or a forecasting method; the agreement files what is funded and when the block runs | no column marks a wave, a lag, a phase or an upstream region: the census carries nights, levels and staffed beds, the roster a region, a city and a join date | no: the reflexes are the calendar, the analog, the trend, the pool's own post-peak profile and the Southeast's lead | none ships: no document scores a method, the closed winters are read alike by every method | no: nothing is duplicated, missing or mis-keyed on the call's rows | no: two candidate lags read from five winters' timing, the one that held chosen, the North's wave placed, its per-wave draw built from its own nights and staffing | silent |

## Semantic fork table

Every term in the main ask and every convention the main computation needs. Every id is asserted in
`generator/checks.py`.

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "block-book for the four weeks from Monday 4 January" | the block clause: the four weeks from the first Monday in January, 00:00 Monday 4 January to 23:59 Sunday 31 January 2027, Eastern time | calendar January | same call (asserted: the North's surge nights lie 10 to 23 January, the south's none after 26 December) | the agreement, clause 5.1; same call, asserted |
| SF2 | "how many agency RN shifts" | the pool's expected draw over the block weeks (clause 5.2) | a cover figure at a high percentile | a larger block | the agreement, clause 5.2 ("set at the Pool's expected draw over the Block weeks") |
| SF3 | the pool's draw | agency RN shifts that staff a member's surge unit and start while its surge plan is active (clause 3.1) | every agency shift at a member during the weeks | a far larger block | the agreement, clause 3.1 |
| SF4 | the members | the 24 hospitals of Schedule A, the eight North hospitals from 1 November 2026 | the sixteen members of the pool's history | none (asserted) | Schedule A |
| SF5 | a shift | one nurse for one scheduled shift, 07:00 to 19:00 or 19:00 to 07:00 (clause 1.4) | an agency billing line | same call (the call reads staffing per level, not billing lines) | the agreement, clause 1.4; same call, asserted |
| SF6 | the surge plan's activity | from the declared activation to the declared stand-down (the declaration log); the census night's level is the level in force at its midnight census | the census night's level for the whole day | same call (asserted: shift by shift 605.4, per night 602.0) | clause 3.1; same call, asserted |
| SF7 | the staffing a surge level draws | the register's agency RN shifts a day at each level, unchanged for 2026-27 | the closed winters' worked shifts per surge night for the south | same call (the North has no worked pool shifts; last winter the south's funded shifts ran 0.5 per cent under the register's staffing at the declared times, asserted, and the golden is the same bin at either: 597.4 and 602.4 scaled) | the register; same call, asserted |
| SF8 | the as-of | the census to the night of Sunday 20 December 2026, every file pulled on Monday 21 December | data to 30 November | same call | the export manifest |
| SF9 | the rounding path | the expected draw unrounded, then to the nearest 50 | each member or region rounded first | same call (asserted) | clause 5.2; same call, asserted |
| SF10 | the closed winters | the five winters on the capacity system, 2021-22 to 2025-26 | the winters the pool has history for (the same five) | same call | the census covers 1 July 2021 onward |
| SF11 | whose surge units the block covers | every Member's surge unit (clause 5.1), a Member being a hospital of Schedule A from its Pool start date (clause 1.2): the eight North hospitals from 1 November 2026 | only the sixteen members the pool's history covers | none (asserted: the sixteen draw none of the block weeks) | the agreement, clauses 5.1 and 1.2 with Schedule A; asserted |

## Ladder

Built figures from `generator/calc.py` on the clean truth, every row asserted in `generator/checks.py` (LADDER, R3a,
R3b) and recomputed from the bundle by `generator/verify.py`. Each block is the expected draw over the block weeks,
to the nearest 50 shifts.

| Rung | Construction | Block | Dies to |
|---|---|---|---|
| R0 default | the closed Januaries' block draws averaged (2,156, 1,566, 2,090, 1,416, 2,084) | 1,850 (1,862.4) | its own back-test: each closed January carried to the next missed it by 25 to 48 per cent; the January draw moves with the wave's timing |
| R0b | last January alone | 2,100 (2,084) | the same |
| R0c | the five Januaries trended | 1,750 (1,774.2) | the same |
| R1 | the pool's own post-peak weeks: the south aligned on each winter's Southeast centre, the North at the same draw per bed | 1,250 (1,243.4) | the North's own capacity reports: its spells never sat in the south's post-peak weeks; the window aligned on the Southeast carries West and Central's closed-winter waves, which trailed the Southeast by a month in four winters of five |
| R1b | the south's post-peak weeks, the North at its own calendar January | 1,050 (1,050.4) | the same |
| R1c | the North timed from the Southeast: its centre at the pull plus the closed winters' mean lag (56 days) | 100 (90), none by first surge nights (4) | the lag behind the Southeast ran from 35 to 63 days; left out one winter at a time it misses 2024-25 by 27 days |
| R1d | every member's census aligned on this winter's Southeast centre | 1,150 (1,128.8) | the same: West and Central's gap behind the Southeast ran from 4 to 32 days |
| R2c | 2022-23, the closest closed winter by the Southeast's timing, taken whole | 1,550 (1,566) | 2022-23's Southeast centre fell 21 days later than this winter's |
| R2d | the four weeks from the first Monday in February averaged | 1,300 (1,322.4) | one month is not each region's lag; it carries West and Central's closed-winter waves |
| R2e | a line through the January draw against the Southeast's timing | 2,200 (2,206.2) | the relation is not linear in timing; the line runs off the record |
| R2f | the season's usual total less this winter's draw to 31 December | 650 (654.4; 950 to the pull, 962.4) | the North's per-wave draw does not move with the south's season |
| R3 decisive | the North timed by its lag behind West and Central (30.0 to 33.0 days in the closed winters, mean 31.5): the south's waves over by 29 December, the North's whole wave inside the block weeks at its own mean per-wave draw (618, 608, 624, 586, 574) | 600 (602.0) | golden |

**Position and margins.** The golden is bracketed: the rungs above it file 650 to 2,200 (the calendar's 1,750 to
2,200, the Southeast-aligned 1,050 to 1,250, the season's remainder 650), the Southeast-timed rung 100 or none below
it. The nearest rung, R2f, is one bin above (654.4, 29.4 shifts past the golden cell's 625 edge); every other rung is
nine bins or more away.

**Reflex sweep (asserted, REFLEX in `checks.py`, on the cut pack).** Twenty-eight cheap routes that skip the North's own
relation, each measured before the ladder was frozen: the pool's season draw spread flat over the season (four weeks of
151 days, of 22 weeks and of the chart's 21 weeks, the lowest closed season, last winter's funded shifts) files 664 to
705; all 24 members' seasons spread flat files 797; the south's season draw or last winter's funded shifts per staffed
bed carried to the North's beds files 678 and 673; the Januaries by mean, median, last three, last, smallest and per
bed file 1,416 to 2,204; the season times its January share 1,858; the order book 1,400 and 1,890; the season's
remainder at the pull 962; the peak four weeks of each closed season 2,444. The timing bypasses the rule-3 audit named,
each asserted to miss the golden's cell by a full bin or more: the whole census aligned on this winter's Southeast centre
1,129, on its first Southeast surge night 1,282, on its first surge night anywhere 1,282 and on the southern median centre
1,094; the North eyeballed from the Southeast at its centre plus the mean lag 90, plus the median lag 0, its first night
at the Southeast's first plus the mean lag 4 and plus the median lag 0; the wastewater alone, the North's peak from the
Southeast's, 14. None is within a quarter bin of the golden's cell; the nearest, the lowest closed season spread flat,
sits at 664, 39 past the 625 edge. The transfers by bed are rivals, not constructions of the golden: the North's own
census gives its per-wave draw directly, 0.67 shifts a staffed bed against the south's 0.76 in the closed winters.

**Convergence (C1, asserted).** Nine constructions of the golden file 600 (593.5 to 608.0): the mean of the five waves
priced per night (602.0) and shift by shift at the declared times (605.4), the median wave (608), the last three (594.7),
the middle three (604), the hospital-by-hospital medians (600), the mean scaled by this winter's southern draw against
the closed winters' (593.5), every member's census aligned on West and Central's centre (602) and the North placed by
West and Central's first surge night (602). On the cut pack every West and Central route files 602: the census aligned
on its centre or its first surge night, the North at its centre plus the mean or the median lag, its first night plus
the mean lag, and the North's wastewater peak from West and Central's; the mean scaled by last winter's funded shifts
against the register's staffing draw files 597.4 per night and 602.4 shift by shift. Every one sits at least a quarter
bin inside the cell (the nearest, 608.0, 17 shifts from the 625 edge). The golden sits 23.0 shifts from the 625 edge and
27.0 from 575; one sigma of the mean wave (21.3 / sqrt 5 = 9.5) leaves it in the bin. The North's spells this winter
run 10 to 23 January in the generator's realised winter (never shipped), six days inside the first edge and eight
inside the last; the lag behind West and Central (30.0 to 33.0 days) puts a spell across an edge only by moving six
days or more, and every closed winter's lag carried from West and Central's centre at the pull keeps every North spell
inside (asserted). The sixteen southern members' last surge night falls on 26 December.

**Worth on the graded quantity.** Reading the window by the calendar costs about 1,250 shifts; timing the North from
the Southeast leaves 100 or none in the block (or 1,150 aligning the whole census on it); only the North's lag behind
West and Central puts its 600 shifts inside the block.

**Out of sample.** Carrying each closed January to the next missed it by 25 to 48 per cent; the North's lag behind
West and Central, carried from the other four closed winters, came within two days of each winter's own (at most
1.94), and its
per-wave draw within 6.1 per cent of each winter's outturn (-4.4 to +6.1); the lag behind the Southeast, carried the
same way, missed 2024-25 by 26.6 days and the other winters by 4.1 to 8.8, so the closed winters themselves select West
and Central as the North's clock (asserted, OOS).

**Strength.** P(one strong solver lands) about 0.17: it must see that the window's content moves with the wave's timing
(about 0.4 of strong solvers get past the calendar), include the eight North members, time the North region by region,
and then choose West and Central over the Southeast as the North's clock (about 0.45 of those who time regions: the
Southeast is where the wave starts and where most solvers anchor, and only the 2024-25 winter separates the two clocks
in the record). P(both land) about 0.03 if independent and under 0.07 with any plausible correlation. The rule-3 audit's
bypass (the aligned analog and the eyeballed Southeast lag filing the golden without reading the North's relation) is
closed: every Southeast-anchored or statewide route misses by a full bin or more. The seed was fixed by rule (task
number, then the as-of month and day: 1601221) before any data was generated and is never searched; this winter's
southern amplitudes, the North's amplitude and the timing constants are design parameters that put the golden mid-bin.

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
| 9 | Boundary inclusivity | a shift starting at 00:00 on 4 January is in, one at 00:00 on 1 February out | C1: no surge shift near either edge (asserted) |
| 10 | Rounding path | the unrounded expected draw to the nearest 50 | filed (clause 5.2); SF9 |
| 11 | Tie-break | none | n/a |
| 12 | Maturity and censoring | the West and Central spells open at the as-of | C1: every one ends before the block weeks under any closed winter's spell length (asserted) |
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
literal estimand (the closed Januaries averaged) files 1,850, timing the North from the Southeast files 100 or none,
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
  shift is one nurse for one scheduled shift, 07:00 to 19:00 or 19:00 to 07:00, Eastern time).
- Primary A2 (D6, one shift on several ledger lines): Crestfield's member shift report bills each night shift on two
  lines, one for each calendar day it covers (19:00 to 24:00 and 00:00 to 07:00), both under the night's timesheet
  number; counted line by line, every Crestfield night on a surge unit counts twice, at every one of the 16 hospitals
  (Crestfield fills every second slot on every surge shift). Fair: the timesheet number and the 5.0 and 7.0 hours that
  make one 12-hour shift, with clause 1.4 counting one per nurse per scheduled shift. Silent: line ids are unique, no
  line repeats another, every site code joins, and no shipped sentence says how Crestfield bills a night.
- Hazard B1 (documented): Inland Seas dates every shift by its payroll date, the day the shift ends, as the pool
  office's data dictionary records for both workbooks; read as the night's start, each spell's last Inland Seas night
  reads as starting after the stand-down, at every one of the 16 hospitals. The dictionary files the convention; the
  solver still applies it to the night rows to recover each shift's start.
- Stops (built and asserted): S1 the cracker (lines counted, the dictionary's payroll convention applied): all 16 miss
  on A2; S2 lines counted and payroll dates read as start dates: all 16 miss; S3 A2 cracked: the golden.
- Span: the agreement, the register (surge units), the declaration log, the roster, Crestfield's report, Inland Seas'
  workbook, the dictionary (7 files).
- Realism: agency timekeeping splits a night shift at midnight so each calendar day's hours are paid at that day's
  rate; the export keeps the split.

**Ask B. For each of the same hospitals, how many of the agency shifts worked there in that time were billed to the
pool though the pool did not fund them** (16 figures, whole shifts).
- H18 home: the reconciliation of the agencies' billing to the pool's funding, the shifts returned to each member's
  account at settlement (clause 6.2).
- Use: the same member table, the column the members' finance offices settle.
- Basis (filed): clause 3.1 as above; clause 6.2 (an agency shift billed to the pool that the pool does not fund is
  returned to the member's account).
- Primary A2 through HA7 and HA4: every Crestfield night among the surge-request bookings on other units and the teams
  that report after a stand-down is on two lines, at all 16 members (asserted, DEVICE lines counted moves Ask B at every
  member).
- Hazards: B1 as above (each spell's last Inland Seas night moves from funded to billed and not funded when read as a
  start date); HA1 Crestfield's times in UTC (its column names say so); HA2 declarations at the 14:45 bed meeting (the
  day shift of an afternoon activation is not funded, of an afternoon stand-down is); HA3 the skeleton opening the night
  before a morning declaration (not funded, billed to the member); HA4 the team that reports for the shift after a
  stand-down (billed to the pool, not funded); HA5 the activation day's day shift booked as staffing (funded, billed to
  the member); HA6 Inland Seas' facility short names and Crestfield's site codes against the roster; HA7 the nurses a
  member's staffing office books on the open surge request for its other units, mostly the emergency department's
  holds (booked SURGE and billed to the pool like the surge unit's own, worked on another unit, so not funded; the bulk
  of every member's Ask B figure).
- Stops: S0 the census night's level for the whole day (moves Ask A and Ask B only at the members with an afternoon
  stand-down last winter, asserted); S1 the cracker: all 16 miss on A2; S2 A2 cracked: the golden. Last winter's golden
  figures run from 7 to 20 a member, none nil.
- Span: the agreement, the declaration log, the roster, both agency reports, the dictionary (6 files).
- Realism: payroll systems pay a night shift on the day it ends; the date on the line is the payroll date.

**Ask C. The chart** (`pool_shifts_winter_2025-26.png`): the shifts the pool funded in each of the 21
Monday-to-Sunday weeks from 3 November 2025 to 29 March 2026, by the week each shift started in, labelled with the
busiest week's funded total and the agency shifts starting that week billed to the pool. Graded on those two figures
(902 funded and 928 billed to the pool in the week of 12 to 18 January 2026, the busiest week 42 shifts clear of the
next); the chart file itself is an instruction-following point, so no chart part is free. A2 moves both figures (1,109
and 1,142 counted line by line), the payroll date read as a start date moves both (asserted), and lines counted with
payroll dates read as start dates move the week too (1,117 and 1,177 in the week after; the mirror, at the census
night's level for the day as well, 1,113 and 1,177).

**Hazard table.**

| Hazard | Asks moved | Per-ask delta read the easy way |
|---|---|---|
| A2 Crestfield's nights on two lines | A, B, C | A: every member's Crestfield surge nights twice; B: every Crestfield night among the other-unit bookings and post-stand-down teams twice; C: both figures |
| B1 Inland Seas' nights by payroll day (documented) | A, B, C | A and B: each spell's last Inland Seas night moves from funded to billed and not funded; C: Sunday nights a week late, both figures and the week |
| HA1 UTC in Crestfield's report | A, B, C | evening starts a day late if read unconverted |
| HA2 to HA5 the declared times and bookings | A, B, C | read off the census night's level: the funded and returned shifts at each afternoon stand-down |
| HA7 surge-request bookings on other units | B, and A for the mirror | counted funded when the bill-to is read as the funding test; each Crestfield night among them twice when lines are counted |

**Referee.** None: the agreement's clauses file the basis and nothing shipped totals the funded or returned shifts.

**Cracker sheet** (the cracker landed the call, ran the hygiene battery, executed every filed rule and documented
convention, Inland Seas' payroll date included, and converted every documented time zone):

| Ask figures | The cracker's route | Device that holds | Verdict |
|---|---|---|---|
| A, funded shifts at each of the 16 hospitals (16) | clause 3.1 with the declared times, every billing line counted, payroll dates read as the day each shift ends | A2 Crestfield's two-line nights | miss |
| B, returned shifts at each of the 16 hospitals (16) | clauses 3.1 and 6.2, the same reading | A2 through HA7 and HA4 at all 16 | miss |
| C, the busiest week's funded total and the shifts billed to the pool that week (2) | Ask A's construction by week | A2 | miss |

**Mirror sheet.** The mirror stops at the census night's level for the whole day, the payroll date read as the date
worked and the billing lines counted; it keeps no Ask A, B or C figure.

Measured by: `generator/cracker.py` (run on the cut pack by `checks.py` on every build).

Mirror leakage: 0.0 per cent of ask weight (no chart part is free; 34 ask criteria).

Pair ceiling: 28.5 (the cracker at 38 + 7 + 55 x 0/34 = 45.0, the mirror at 5 + 7 + 0 = 12.0); both top responses on
the call: 45.0. With A2 cracked the asks fall whole (the cracker 100, the pair 56.0): B1, which backed A2 when it was
silent, is now the documented convention the judge asked for, so the ask layer rests on A2 alone. All asserted in
`checks.py` on the cut pack (ASK pair lines). Rerun from the generated rubric at stage 4. Criteria supplied: the call
and its three components, 16 funded figures, 16 returned figures and the chart's two figures, plus instruction-following.

## Surface screen

`guard.py surface task160` exits 0 and promotes three pairs, none with a hard tell (no shared file name, schema,
invented name or same-seed table): task145 and task446 on the card-level same-driver signature (gap time, G16, Gate G
forecasting), each differentiated on the card at the draw; task231 on corpus surface similarity alone (a survey-research
data-quality build: another domain, objective and decision; the shared features are the house idioms of a dictionary,
a manifest and a how-many opening). A first cut also paired task460 on one identical table, the dictionary's
`file, field, definition` sheet; the dictionary now carries a title row and a format column in the pool office's own
layout. The first cut's persona sweep read four place pairs off Schedule A's city and region cells (Mount Clemens
Southeast, Flint West and Central, Gaylord North, Sault Ste. Marie North) and blocked on two sharing "North"; Schedule A
now lists the region before the city and the sweep finds Greg Matthews alone. `guard.py heart task160` WARN, exit 0:
`repeat.question_form` (how-many, task470), answered at the draw; nearest driver 0.10 (task157); the two NOTEs are the
differentiated older builds above.

## Leak sweep

`leak.py task160 --asof 2026-12-21` returns REVIEW, no LEAK; every line answered:
- Sweep 3, the agreement carries the call's words (block, agency RN shifts, Monday 4 January to Sunday 31 January
  2027): it files the estimand (clauses 5.1 and 5.2, the four weeks and the expected draw to the nearest 50) and
  carries no block figure and no forecast; the 2026-27 row of the block book is blank (asserted, R3c).
- Sweep 4, stump-paragraph terms in the agreement, the register and the rate schedule (region, Southeast, Central,
  hospital, census, capacity, staffing, member, association, schedule): each document's own subject (who the members are and where; each
  surge unit's staffing per level; the season's rates); none names a wave, a lag, a region's timing, which region
  follows which or how to forecast the draw (a sweep of every shipped document for lag, lead, follow, wave, timing,
  behind and ahead finds only the rate schedule's travel allowance).
- Sweep 6, files naming the members beside numbers (the roster's beds, the register's staffing, Schedule A's start
  dates, the workforce survey's vacancy returns): records per member, none ranking members on the block or on either
  ask's quantity.
- Sweep 9, dates after the pull: the block book's 2026-27 block weeks (4 to 31 January 2027, the agreement's clause
  5.1) and the admissions outlook's fourteen forecast days to 1 January 2027, forward-looking records allowed by file
  (`reduce-house-fixes` H16).
- Sweep 10: no writer signature and no stamp outside 2021-07-01 to 2026-12-21 in the pack or the goldens
  (`scrub_producer_metadata.py` audit, both directories).

## Build record

Stage 3 rework, 2026-10-18 (the reader's, the rule-3 audit's and the judge's findings and the chart hardening folded
into one rebuild). `build.py`: `checks.py` 151 run, 0 failed (the three-rules block R1 to R3c on the clean truth and the
pack, every SF row SF1 to SF11, the ladder's rungs and the golden's bracket, twenty-eight REFLEX routes each a quarter
bin or more outside the golden's cell and the nine timing bypasses a full bin or more, the out-of-sample record, nine
constructions of the golden and eight more on the pack, the one-sigma corridor, the timing margins, both asks equal to
the truth with every device and hazard moving its stated figures, the chart's two figures, the cracker pair on the cut
pack at 28.5, both on the call 45.0, mirror leakage 0.0 per cent, the separation line by deletion, the input gates, the
realism sweep and the dates); `verify.py` (csv, openpyxl and pypdf, no generator import) 0 failed, every format read
back with a positive control, the North timed from West and Central and from the Southeast on its own code path, the
chart's two figures, and the goldens and write-up checked against its own recomputation; two consecutive builds
byte-identical (target, golden, figures.json, submission); `figures_check.py` 0 absent (31 figures); `voice-check.py`
PASS (794 characters); `precut.py` exit 0; `leak.py` REVIEW, no LEAK, every line answered; the H1 audit clean on the
pack and the goldens; `guard.py validate` clean, `surface` exit 0 (three card-level pairs, above), `heart` WARN
(answered). 16 files in 4 formats (csv, xlsx, pdf, json), the largest the legacy capacity export at 26,406 rows;
distractors `rn_workforce_survey_2025q1_2026q3.xlsx` and `agency_rate_schedule_2026-27.pdf` in `metadata.json`, each
deletion leaving the call and every ask unchanged. `target.zip` cut from the final rebuild, 16 entries equal to
`target/` byte for byte. The seed was fixed by rule (1601221) before any data was generated and never searched. Every
file in the pack carries the pull's modification time, 21 December 2026 09:30 Eastern (`dataset-generation` section 9).

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

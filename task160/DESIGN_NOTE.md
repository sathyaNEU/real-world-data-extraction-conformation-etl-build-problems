# task160 design note

Architecture 1, wave 6 (new), Forecasting lane (sathya8571), numbered from seed FC31. The seed (a state hospital
association block-booking its January agency nurse shifts for a 24-hospital winter pool with two staffing agencies, the
pool funding agency shifts worked while a member hospital's surge plan is active, the block set at the forecast pool
draw) was read at its header and Situation only. Its world, decision and quantity are kept. Its mechanism (the agencies'
surge booking code only mostly agreeing with the activation days the pool funds) is not the decisive step: reading the
code against the contract's definition is data semantics, so the code survives only as Layer 1 mess and as an ask
device. The pitfall is re-found from how a winter respiratory wave reaches a state's hospitals: region by region, at a
lag behind the region it spreads from that has held in every winter on file, while its calendar timing moves by weeks.

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
   from the region it spreads from, turned into agency RN shifts through each hospital's surge unit staffing. Not banned
   against the last three registrations (task194 healthcare-delivery x anomaly-detection, task470, task243); task142
   (the nearest world: a purchasing alliance's Hospital in the Home overflow block) sits in
   `utilization-access-demand-forecasting`, a different task type, and is differentiated on the card.
3. Niche: a hospital association's January 2027 agency nurse block for its 24-hospital winter surge pool, when the
   respiratory wave peaked in Metro Detroit and West and Central Michigan in mid-December, earlier than in any winter on
   the capacity census, and the eight North hospitals new to the pool have met the wave five to six weeks after Metro
   Detroit in every winter on file.
4. Call and shape: the agency RN shifts to block-book for the four weeks from Monday 4 January 2027 (`quantity_figure`,
   count, question form how-many), to the nearest 50 shifts (the agencies take the block in lots of 50). Shape
   `single-figure`: the call with its critical components, the asks' tables on rows the call never reads, and a chart;
   criteria counted in `## Ask sheet`.
5. Mechanism keys: gap time (the evidence is what past January blocks held; the decision bets on a block whose content
   moves with the wave's timing), then population (the North's eight hospitals have no pool history); decisive generator
   G16 (the forecasting method the closed winters select out of sample: each region's wave timed by its lag behind
   Metro Detroit, against the calendar and the pool's own post-peak profile), then G13 (the window holds a different
   part of each region's wave this winter) and G6 (the window's mix of regions in their waves differs from every January
   on file); Gate G `forecasting`; strategy `forecast_method_backtest` (F6: the January draw is stationary only in each
   region's own wave time, and the calendar fit and the pool's own aligned history fail out of sample on closed winters).
6. Layer 2: `forecast_uncertainty` (model choice on out-of-sample error), pattern
   `own:regional-surge-waves-timed-by-propagation-lag-not-calendar`. Library neighbours:
   epidemiology-public-health/infectious-disease-transmission-modeling (spatial spread, not an Rt or eigenvalue read) and
   healthcare-delivery-health-economics/patient-flow-beds-workforce-optimization/2 (staff to the arrival curve, not the
   daily average); this build's version times each region's surge by the lag of an epidemic's spread across the
   state's regions, read from the closed winters, and carries no queueing or percentile construction.
7. Furniture: forum `operations_desk` (the pool manager files the block; no committee approves it); forcing event
   `purchase_order_or_contract` (the block order goes to the two agencies on 22 December); organisation family
   `cooperative_or_member_body` (a hospital association is its members' body); role family `procurement_lead` (the
   winter pool manager buys the block); context artifact `capacity_report` (the association's daily capacity census);
   calibration `prior_period_close_out` (the closed winters' capacity census and declarations, which the out-of-sample
   check reads). Each is free against task194, task470 and task243.
8. Spine: the association's daily capacity census (hospital x day, midnight census, staffed beds and declared surge
   level), 1 July 2021 to 20 December 2026, two layouts across the July 2024 system change; constructed in the layout of
   a hospital association's daily capacity reporting system.
9. Deliverables: `winter_pool_block_jan2027.xlsx` (the block, its components and the ask tables) and
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
every winter on file the respiratory wave has reached the North's hospitals five to six weeks after Metro Detroit's while
its calendar timing moved by weeks; this winter Metro Detroit and West and Central Michigan peaked in mid-December,
earlier than ever on file, so the four weeks from 4 January hold the North's whole wave, which no January block on file
ever held, and none of the south's, which every January block on file held.

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
spreads from while its calendar timing moves from cycle to cycle, so a fixed forward window holds whichever groups' waves
fall inside it this cycle; carrying what the same window held in past cycles, or the pool's own history aligned on this
cycle's peak, misses a group whose wave has always come after the window and this cycle falls wholly inside it. Nearest
by mechanism, read for latent structure:
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
  parameter is estimated: the lag is read from where the wave was in each closed winter.
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
  region's own wave time, built from the lag.
- `two-layer-task-design.md`: the client's example of validating a forecast on data it was not built on; the calendar
  fit and the pool's own aligned history both fail on closed winters.
- task142 (the nearest world, three waves back) and task157 (the nearest driver): differentiated on the card.

## Default path

1. Read the 2026-27 pool agreement: the pool funds the agency RN shifts that staff a member's surge unit and start
   while its surge plan is active (from the declared activation to the declared stand-down in the capacity system);
   the January block covers the four weeks from Monday 4 January to Sunday 31 January 2027 and is set at the pool's
   expected draw over those weeks, to the nearest 50 shifts; Schedule A lists 24 members, the eight North hospitals
   from 1 November 2026.
2. Stitch the capacity census's two layouts (member numbers and report dates to 30 June 2024, facility ids and census
   dates after) through the roster, and price each member's surge nights at its surge plan's agency staffing per
   level (the surge plan register).
3. Take the pool's draw in each closed winter's block weeks (the four weeks from the first Monday in January,
   2022 to 2026): 3,698, 2,230, 3,596, 1,148 and 3,692 shifts, every one of them the sixteen southern members'
   (the North's surge nights fell in none of those weeks).
4. Average the five Januaries: 2,873 shifts; round to the nearest 50.

Ends on: 2,850 (built: 2,872.8, 2,873 shift by shift at the declared times; last January alone 3,692, the five
Januaries trended 2,545).
Golden: 600 (built: 602.4, the eight North members' mean per-wave draw; the sixteen southern members' expected
draw in the block weeks is none).

## Stump sentence

Averaging the closed winters' January block draws, the sixteen southern members' surge nights in those four weeks at
their surge plans' agency staffing with the North's none, files 2,850 shifts; the step that lands it there is reading
January by the calendar when the respiratory wave's timing moves by weeks from winter to winter and reaches the North
about five and a half weeks after the Southeast, so this January, after the south peaked on 10 and 17 December, holds
the North's whole wave and none of the south's: 600 shifts.

## Three rules

Task type: patient-flow-beds-workforce-optimization (Healthcare Delivery & Health Economics), which serves Forecasting & Predictive Modeling in the taxonomy; the forecast is a health system's surge workforce demand for a window not yet open.
Domain test: the deciding quantity is the January surge staffing demand of each region's hospitals, forecast the way a health-system capacity planner forecasts a winter surge: by where each region's respiratory wave will fall in the window, timed from the region it spreads from by the lag the closed winters show, and turned into agency RN shifts through each hospital's surge unit staffing at each surge level.
Swap: "how many megawatt-hours should the cooperative block-buy for the four weeks from 4 January" keeps a block and a window but loses the respiratory wave travelling region to region over five weeks, the surge plans that open agency-staffed units when a hospital's census crosses its triggers, and the hospitals that join a pool with their own wave still to come, so nothing places one region's whole demand inside a window it has never reached.
Layer 1: the capacity system replaced on 1 July 2024 (member numbers, report dates the morning after each census night and S1/S2 codes in the old export; facility ids, census dates and 1/2 in the new); the roster carrying every key; Crestfield's member shift report with UTC times and its own site codes; Inland Seas' weekly workbook with payroll dates and facility short names; two staffed-bed changes on file; wastewater results posted preliminary and revised, weekly in the North; the association's July-to-June fiscal year against the November-to-March pool season; the surge plan register as a PDF table. Each is how those systems write their files and none carries the call (asserted neutral, R2).
Layer 2: forecast_uncertainty, model choice on out-of-sample error: the closed winters' January draws are stationary only in each region's own wave time, so the choice that flips the call is timing each region's wave from the Southeast's by the lag the closed winters show rather than reading January by the calendar or by the pool's own post-peak weeks.
Decisive step: forecast the block weeks' draw region by region: the sixteen southern members' waves have run their course in December, and the North's, which every closed winter brought about five and a half weeks after the Southeast's, falls wholly inside the block weeks, so the draw is the North's own per-wave surge draw at its surge plans' staffing.
Not semantics: every field is read correctly on the default path (each member's surge nights and levels, both layouts, the staffing per level, the block weeks, the members and their join dates); reading every one of them right still leaves the analyst choosing how to forecast the window, and the calendar files 2,850.
Not rule application: the agreement files the estimand (the members, the funded shifts, the four weeks, the expected draw, the rounding) and the register files each hospital's staffing per level; no filed rule or procedure says when a region's wave arrives or how to forecast the draw, and executing every filed rule on the closed Januaries files 2,850 (or, on the pool's own post-peak weeks, none).
Analyst test: a strong analyst who stitches both capacity layouts, reads the agreement and the register correctly and averages the closed winters' January block draws at the register's staffing files 2,850 shifts against the golden 600 (executed in checks.py on the generator's clean truth); the analyst who sees the early peak and carries the pool's own post-peak weeks files none, and only timing the North's wave by its lag behind the Southeast files 600.
Estimand: the 2026-27 pool agreement (clauses 3.1, 5.1 and 5.2 and Schedule A) files the population (the 24 members of Schedule A, the eight North hospitals included from 1 November 2026, members not yet drawn on in the pool's history counted), the outcome (agency RN shifts that staff a member's surge unit and start while its surge plan is active, one per nurse per scheduled shift), the window (00:00 Monday 4 January to 23:59 Sunday 31 January 2027, Eastern time), the unit (the expected number of shifts over the block weeks) and the rounding (the nearest 50); there is no comparison.
No decoy: no memo, draft, forecast, stakeholder figure or earlier block order argues a figure for the 2027 block; the surveillance outlook forecasts two weeks of admissions correctly and ranks nothing; the block order register states what was filed in past winters, not what January holds.
No certified replay: no shipped figure is reproduced to recover a method; the closed winters are the analyst's own out-of-sample record, every one of them read alike by every method.
Lesson: a model learns that a seasonal window's content is set by where each region's wave falls this season, timed from the region it spreads from by a lag the record holds, that a calendar window which never held a region's wave can hold all of it in an early season, and that a pool's own history validates nothing for members whose clock it never saw; no build on file times a window's content by a wave's spread from one region to the next.

## Readability screen

Six tests per rung (1 a filed sentence names it or sends the solver looking, 2 a column, key or marker makes it a
row predicate or a header join, 3 an opponent reflex, 4 a control or corpus scores it, 5 the hygiene battery finds
it, 6 one subtraction, ratio or half of a figure). Figures built in `generator/calc.py`, asserted in
`generator/checks.py` (LADDER, R3a, R3b).

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the closed Januaries' block draws averaged, the North at its own January surge nights (2,850) | the agreement's block clause names the four weeks from the first Monday in January | the census's dates and levels | yes, the default | the analyst's own back-test: each closed January carried to the next missed it by 38 to 213 per cent | no | yes, a mean | readable |
| R0b last January alone (3,700) | no | the census | yes | the same back-test | no | yes | readable |
| R1 the pool's own post-peak weeks: the sixteen southern members aligned on each winter's Southeast centre, the North at the same draw per bed (none) | no | the census | yes, the early-season correction | the North's own capacity reports: their spells never sat in the south's post-peak weeks | no | yes | readable |
| R1b the same with the North at its calendar January (none) | no | the census | yes | the same | no | yes | readable |
| R2a the surveillance outlook at face value, its two weeks carried flat into January (none) | no | the outlook's regional columns | yes | the outlook ends on 1 January | no | yes | readable |
| R2c the closest closed winter by the Southeast's timing, 2022-23, taken whole (2,250) | no | the census | yes, the analog | 2022-23's Southeast centre fell 21 days later than this winter's | no | yes | readable |
| R2d one month later: the four weeks from the first Monday in February averaged (950) | no | the census | a half step | the shift is a month, not each region's lag | no | yes | readable |
| R2f the season's usual total less what this winter has drawn by 31 December (650) | no | the census | a budget reflex | the North's draw does not move with the south's season total | no | yes, one subtraction | readable |
| R3 (decisive) each region timed by its lag behind the Southeast: the south's waves over by 27 December, the North's whole wave inside the block weeks at its own per-wave draw (600) | no sentence names a wave, a lag, a region's timing or a forecasting method; the agreement files what is funded and when the block runs | no column marks a wave, a lag or a phase: the census carries nights, levels and staffed beds, the roster a county and a join date | no: the reflexes are the calendar, the analog, the trend and the pool's own post-peak profile | none ships: no document scores a method, the closed winters are read alike by every method | no: nothing is duplicated, missing or mis-keyed on the call's rows | no: a lag read from five winters' timing, each region's wave placed, the North's per-wave draw built from its own nights and staffing | silent |

## Semantic fork table

Every term in the main ask and every convention the main computation needs. Every id is asserted in
`generator/checks.py`.

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "block-book for the four weeks from Monday 4 January" | the block clause: the four weeks from the first Monday in January, 00:00 Monday 4 January to 23:59 Sunday 31 January 2027, Eastern time | calendar January | same call (asserted: the North's surge nights lie 11 to 24 January, the south's none after 27 December) | the agreement, clause 5.1; same call, asserted |
| SF2 | "how many agency RN shifts" | the pool's expected draw over the block weeks (clause 5.2) | a cover figure at a high percentile | a larger block | the agreement, clause 5.2 ("set at the Pool's expected draw over the Block weeks") |
| SF3 | the pool's draw | agency RN shifts that staff a member's surge unit and start while its surge plan is active (clause 3.1) | every agency shift at a member during the weeks | a far larger block | the agreement, clause 3.1 |
| SF4 | the members | the 24 hospitals of Schedule A, the eight North hospitals from 1 November 2026 | the sixteen members of the pool's history | none (asserted) | Schedule A |
| SF5 | a shift | one nurse for one scheduled shift, 07:00 to 19:00 or 19:00 to 07:00 (clause 1.4) | an agency billing line | same call (the call reads staffing per level, not billing lines) | the agreement, clause 1.4; same call, asserted |
| SF6 | the surge plan's activity | from the declared activation to the declared stand-down (the declaration log); the census night's level is the level in force at its midnight census | the census night's level for the whole day | same call (asserted: shift by shift 604.4, per night 602.4) | clause 3.1; same call, asserted |
| SF7 | the staffing a surge level draws | the register's agency RN shifts a day at each level, unchanged for 2026-27 | the closed winters' worked shifts per surge night for the south | same call (the North has no worked pool shifts; last winter the south's funded shifts ran 0.3 per cent under the register's staffing at the declared times, asserted, and the golden is the same bin at either) | the register; same call, asserted |
| SF8 | the as-of | the census to the night of Sunday 20 December 2026, every file pulled on Monday 21 December | data to 30 November | same call | the export manifest |
| SF9 | the rounding path | the expected draw unrounded, then to the nearest 50 | each member or region rounded first | same call (asserted) | clause 5.2; same call, asserted |
| SF10 | the closed winters | the five winters on the capacity system, 2021-22 to 2025-26 | the winters the pool has history for (the same five) | same call | the census covers 1 July 2021 onward |

## Ladder

Built figures from `generator/calc.py` on the clean truth, every row asserted in `generator/checks.py` (LADDER, R3a,
R3b) and recomputed from the bundle by `generator/verify.py`. Each block is the expected draw over the block weeks,
to the nearest 50 shifts.

| Rung | Construction | Block | Dies to |
|---|---|---|---|
| R0 default | the closed Januaries' block draws averaged (3,698, 2,230, 3,596, 1,148, 3,692) | 2,850 (2,872.8) | its own back-test: each closed January carried to the next missed it by 38 to 213 per cent; the January draw moves with the wave's timing |
| R0b | last January alone | 3,700 (3,692) | the same |
| R0c | the five Januaries trended | 2,550 (2,544.6) | the same |
| R1 | the pool's own post-peak weeks: the south aligned on each winter's Southeast centre, the North at the same draw per bed | none (0) | the North's own capacity reports: each closed winter's North spells sit 37 to 40 days after the Southeast's centre, never in the south's post-peak weeks |
| R1b | the south's post-peak weeks, the North at its own calendar January | none (0) | the same |
| R2a | the surveillance outlook (to 1 January) carried flat | none | the outlook's horizon; the North's wave has not begun in any series at the as-of |
| R2c | 2022-23, the closest closed winter by the Southeast's timing, taken whole | 2,250 (2,230) | 2022-23's Southeast centre fell 21 days later than this winter's |
| R2d | the four weeks from the first Monday in February averaged | 950 (928.4) | one month is not each region's lag; it carries 2025's late southern wave |
| R2e | a line through the January draw against the Southeast's timing | 4,450 (4,472.2) | the relation is not linear in timing; the line runs off the record |
| R2f | the season's usual total less this winter's draw to 31 December | 650 (668.0; 1,050 to the pull) | the North's per-wave draw does not move with the south's season; this winter's southern waves draw 66 shifts under their mean |
| R3 decisive | each region timed by its lag behind the Southeast: the south's waves over by 27 December, the North's whole wave inside the block weeks at its own mean per-wave draw (620, 596, 630, 572, 594) | 600 (602.4) | golden |

**Position and margins.** The golden is bracketed: the calendar rungs file 2,250 to 3,700 above it, the pool's own
post-peak rungs none below it. The nearest rung, R2f, is one bin above (668.0, 43 shifts past the golden cell's 625
edge); every other rung is six bins or more away.

**Reflex sweep (asserted, REFLEX in `checks.py`, on the cut pack).** Nineteen cheap routes that skip the regions'
timing, each measured before the ladder was frozen: the pool's season draw spread flat over the season (four weeks of
151 days, of 22 weeks and of the chart's 21 weeks, the lowest closed season, last winter's funded shifts) files 670 to
704; all 24 members' seasons spread flat files 797; the south's season draw or last winter's funded shifts per staffed
bed carried to the North's beds files 678 and 680; the Januaries by mean, median, last three, last, smallest and per
bed file 1,148 to 3,692; the season times its January share 2,855; the order book 2,500 and 2,710; the season's
remainder at the pull 1,058; the peak four weeks of each closed season 3,618. None is within a quarter bin of the
golden's cell; the nearest, the lowest closed season spread flat, sits at 670, 45 past the 625 edge.
A first build had the flat rate at 617 and the bed transfer at 612, both in the golden's cell by coincidence (the
south's season draw times 28/151 fell on the North's wave); every southern member's Level 2 staffing was raised by two
agency RN shifts a day, which moves the south's draws and none of the North's, and this winter's southern amplitude
was set so the season's remainder stays a bin off while the family's scaled construction stays inside the cell
(`## Tried and rejected`). The transfers by bed are rivals, not constructions of the golden: the North's own census
gives its per-wave draw directly, 0.67 shifts a staffed bed against the south's 0.76 in the closed winters.

**Convergence (C1, asserted).** Eight constructions of the golden file 600 (591.7 to 610.0): the mean of the five
waves priced per night (602.4) and shift by shift at the declared times (604.4), the median wave (596), the last three
(598.7), the last wave (594), the February waves only (610.0), the hospital-by-hospital medians (600), and the mean
scaled by this winter's southern draw against the closed winters' (591.7). Two more land with them: the mean scaled by
last winter's funded shifts against the register's staffing draw, per night (598.8) and shift by shift (602.3). The
golden sits 22.6 shifts from the 625
edge and 27.4 from 575; one sigma of the mean wave (23.0 / sqrt 5 = 10.3) leaves it in the bin. The North's spells
this winter run 11 to 24 January in the generator's realised winter (never shipped), seven days inside each edge; the
lag (37.2 to 39.8 days, mean 38.6) would have to move by a week to put a spell across an edge. The sixteen southern
members' last surge night falls on 27 December.

**Worth on the graded quantity.** Reading the window by the calendar costs about 2,250 shifts; correcting for the early
season with the pool's own history overshoots to none; only the North's lag puts its 600 shifts inside the block.

**Out of sample.** Carrying each closed January to the next missed it by 38 to 213 per cent; the regional-lag
forecast, made from the other closed winters (the lag within 1.7 days of each winter's own, the North's per-wave draw
within 7 per cent of each winter's outturn, -5.5 to +6.6), put every North spell in the right weeks.

**Strength.** P(one strong solver lands) about 0.2: it must see that the window's content moves with the wave's timing,
that the pool's own history holds none of the North's waves, that the North's waves follow the Southeast's by a lag
every closed winter kept, and that this winter places the North's whole wave in the block weeks. P(both land) about
0.04 if independent, under 0.1 with any plausible correlation. The seed was fixed by rule (task number, then the as-of
month and day: 1601221) before any data was generated and is never searched; this winter's southern amplitude and
Ostrander's staffing are design parameters that put the golden mid-bin.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the 24 members of Schedule A, the North from 1 November 2026 | filed (Schedule A); SF4 |
| 2 | Unit of account | one nurse for one scheduled shift; the expected draw over the block weeks | filed (clauses 1.4, 5.2); SF2, SF5 |
| 3 | Attribution window | 4 to 31 January 2027, Eastern time, by shift start | filed (clause 5.1); SF1 same call asserted |
| 4 | As-of dating | the census to the night of 20 December 2026, pulled 21 December | filed (the export manifest); SF8 |
| 5 | Version basis | the register's 2026-27 staffing per level | filed (the register); SF7 |
| 6 | Denominator | none (a count) | n/a |
| 7 | Weighting | none | n/a |
| 8 | Window length | the closed winters the lag and the per-wave draw are read from | C1: five, three or one winter the same block (asserted) |
| 9 | Boundary inclusivity | a shift starting at 00:00 on 4 January is in, one at 00:00 on 1 February out | C1: no surge shift near either edge (asserted) |
| 10 | Rounding path | the unrounded expected draw to the nearest 50 | filed (clause 5.2); SF9 |
| 11 | Tie-break | none | n/a |
| 12 | Maturity and censoring | the West and Central spells open at the as-of | C1: every one ends by 27 December under any closed winter's spell length (asserted) |
| 13 | Order of operations | each hospital's nights priced, summed, then rounded | C1 (asserted) |
| 14 | Row order | sums | C1 |
| 15 | Duplicate resolution | none on the call's rows (one capacity report per member and census night) | C1 (asserted) |
| 16 | Identity normalisation | member numbers to facility ids through the roster | C1: one facility id per member number (asserted) |
| 17 | Netting against gross | none | n/a |
| 18 | Dimensional units | shifts a day at each level against shifts | filed (the register) |
| 19 | Code and status semantics | S1/S2 in the old export, 1/2 in the new | the export manifest's field notes; C1 (asserted) |
| 20 | Integerisation | none before the total | the golden mid-bin with one sigma (asserted) |
| 21 | Clause scope | the 2026-27 agreement governs the 2027 block | filed |
| 22 | Forward window contents | the members' surge nights in the block weeks | forecast from the records (the decisive step); no file covers the window |

## Literal reader

Executing the prompt and the 2026-27 agreement word for word gives the expected number of agency RN shifts, one per
nurse per scheduled shift, that staff a Schedule A member's surge unit and start while its surge plan is active
between 00:00 on Monday 4 January and 23:59 on Sunday 31 January 2027, Eastern time, the eight North members
included, to the nearest 50; no shipped sentence says when any region's surge will come or how to forecast it, so a
literal reader must forecast it from the records; the easy method on the same literal estimand (the closed Januaries
averaged) files 2,850, and the fork table leaves no reading under which any rung is the golden.

## Oracles

- The closed winters' capacity reports: every method reads them alike; on the wrong path they supply the January
  averages, and the analyst's own back-test on them rejects the calendar. No closed window holds a 2027 figure.
- The block order register: what was filed in each closed winter, at the time; it states no outcome and ranks nothing.
- The surveillance outlook: two weeks of regional admissions to 1 January, correct for its horizon; it holds no January
  figure.
- No control ties only under the golden.

## Ask sheet

**Main call's declared row population:** the capacity census in both layouts (every member, every census night), the
declaration log, the surge plan register's staffing per level, the agreement's clauses 1.4, 3.1, 5.1 and 5.2 with
Schedule A, and the roster's keys. Device and hazard rows in it: 0 (asserted, DEVICE: the block computed with both
agency reports, the wastewater, the outlook and the block order register deleted is unchanged to the shift; the call
reads no agency line).

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
- Hazard B1 (below) moves every figure too: each spell's last night, read a day late, falls after the stand-down.
- Stops (built and asserted): S0 the census nights at the register's staffing, no agency line read (misses all 16:
  unfilled slots and the 14:45 declarations); S1 the cracker (lines counted, payroll dates read as start dates): all
  16 miss; S2 A2 cracked (timesheets counted): all 16 miss on B1; S3 B1 cracked alone: all 16 miss on A2; S4 the
  golden.
- Span: the agreement, the register (surge units), the declaration log, the roster, Crestfield's report, Inland Seas'
  workbook (6 files, 15 columns on the path).
- Realism: agency timekeeping splits a night shift at midnight so each calendar day's hours are paid at that day's
  rate; the export keeps the split.

**Ask B. For each of the same hospitals, how many of the agency shifts worked there in that time were billed to the
pool though the pool did not fund them** (16 figures, whole shifts).
- H18 home: the reconciliation of the agencies' billing to the pool's funding, the shifts returned to each member's
  account at settlement (clause 6.2).
- Use: the same member table, the column the members' finance offices settle.
- Basis (filed): clause 3.1 as above; clause 6.2 (an agency shift billed to the pool that the pool does not fund is
  returned to the member's account).
- Primary B1 (D8, a date set per source): Inland Seas' member shift workbook dates every shift by its payroll day, and
  a night shift is paid on the day it ends; read as the night's start, each spell's last night (started before the
  stand-down, billed to the pool) reads as starting after it, at every one of the 16 hospitals (Inland Seas fills every
  second slot on every surge shift, or the first where it is the member's primary agency). Fair: the workbook's
  timesheet detail sheet gives clock-in and clock-out times with payroll dates for the shifts queried last winter, and
  every night among them is paid on the day it ended. Silent: a payroll date reads as the date worked, and no shipped
  sentence says otherwise.
- Hazards: HA1 Crestfield's times in UTC (its column names say so); HA2 declarations at the 14:45 bed meeting (the day
  shift of an afternoon activation is not funded, of an afternoon stand-down is); HA3 the skeleton opening the night
  before a morning declaration (not funded, billed to the member); HA4 the team that reports for the shift after a
  stand-down (billed to the pool, not funded); HA5 the activation day's day shift booked as staffing (funded, billed to
  the member); HA6 Inland Seas' facility short names and Crestfield's site codes against the roster; HA7 the nurses a
  member's staffing office books on the open surge request for its other units, mostly the emergency department's
  holds (booked SURGE and billed to the pool like the surge unit's own, worked on another unit, so not funded; 4 to 17
  a member last winter, the bulk of every member's Ask B figure). A2 reaches Ask B through HA7 and HA4: every
  Crestfield night among those shifts is on two lines, at 15 of the 16 members.
- Stops: S0 the census night's level for the whole day (moves Ask A and Ask B only at the one member with an afternoon
  stand-down last winter, MI-0446); S1 the cracker: all 16 miss on B1; S2 A2 cracked: all 16 miss on B1; S3 B1
  cracked: 15 of 16 miss on A2; S4 the golden. Last winter's golden figures run from 6 to 20 a member, none nil.
- Span: the agreement, the declaration log, the roster, both agency reports (5 files, 12 columns).
- Realism: payroll systems pay a night shift on the day it ends; the date on the line is the payroll date.

**Ask C. The chart** (`pool_shifts_winter_2025-26.png`): the shifts the pool funded in each Monday-to-Sunday week
from 3 November 2025 to 29 March 2026, one bar per week split by agency, the four January block weeks marked and the
busiest week's total labelled. Graded on its parts (21 weekly bars, split by agency, the block weeks marked, the axis
in shifts, a title naming the winter) and on the busiest week's total, which A2, B1 and HA1 move.

**Hazard table.**

| Hazard | Asks moved | Per-ask delta read the easy way |
|---|---|---|
| A2 Crestfield's nights on two lines | A, C | A: every member's Crestfield surge nights twice; C: every surge week |
| B1 Inland Seas' nights by payroll day | A, B, C | A and B: each spell's last Inland Seas night moves from funded to billed and not funded; C: Sunday nights a week late |
| HA1 UTC in Crestfield's report | C | Sunday-night shifts a week late if read unconverted |
| HA2 to HA5 the declared times and bookings | A, B | read off the census night's level: the funded and returned shifts at each afternoon stand-down (MI-0446 last winter) |
| HA7 surge-request bookings on other units | B, and A for the mirror | counted funded when the bill-to is read as the funding test; each Crestfield night among them twice when lines are counted |

**Referee.** None: the agreement's clauses file the basis and nothing shipped totals the funded or returned shifts.

**Cracker sheet** (the cracker landed the call, ran the hygiene battery, executed every filed rule and converted
every documented time zone):

| Ask figures | The cracker's route | Device that holds | Verdict |
|---|---|---|---|
| A, funded shifts at each of the 16 hospitals (16) | clause 3.1 with the declared times, every billing line counted, payroll dates read as dates worked | A2 Crestfield's two-line nights (and B1) | miss |
| B, returned shifts at each of the 16 hospitals (16) | clause 3.1 and 6.2, the same reading | B1 Inland Seas' payroll-dated nights (and A2 at 15 of 16 through HA7 and HA4) | miss |
| C, the busiest week's total (1) | Ask A's construction by week | A2 and B1 | miss |

**Mirror sheet.** The mirror stops at the census night's level for the whole day and the agencies' bill-to as the
funding test; it keeps the chart's five parts and no Ask A, B or C figure.

Measured by: `generator/cracker.py` (run on the cut pack by `checks.py` on every build; `--truth` scores the
generator's clean truth with the agency layouts simulated).

Mirror leakage: 13.2 per cent of ask weight (the chart's five parts of 38 ask criteria).

Pair ceiling: 35.7 (the cracker at 38 + 7 + 55 x 5/38 = 52.2, the mirror at 5 + 7 + 7.2 = 19.2); with the most
obvious device, A2, cracked: 35.7 (B1 holds both columns); with B1 cracked instead: 36.5 (Ask A holds on A2 at all 16,
Ask B at 15 of 16). Both top responses on the call: 52.2 on this sheet, 49.6 if the rubric grades only the three chart
parts the prompt names; the ladder keeps the second response off the call. All four asserted in `checks.py` on the cut
pack (ASK pair lines). Rerun from the generated rubric at stage 4.

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
- Sweep 4, stump-paragraph terms in the agreement, the register and the rate schedule (region, Southeast, hospital,
  census, capacity, staffing, member, association): each document's own subject (who the members are and where; each
  surge unit's staffing per level; the season's rates); none names a wave, a lag, a region's timing or how to forecast
  the draw (asserted, R3c and the readability screen).
- Sweep 6, files naming the members beside numbers (the roster's beds, the register's staffing, Schedule A's start
  dates, the workforce survey's vacancy returns): records per member, none ranking members on the block or on either
  ask's quantity.
- Sweep 9, dates after the pull: the block book's 2026-27 block weeks (4 to 31 January 2027, the agreement's clause
  5.1) and the admissions outlook's fourteen forecast days to 1 January 2027, forward-looking records allowed by file
  (`reduce-house-fixes` H16).
- Sweep 10: no writer signature and no stamp outside 2021-07-01 to 2026-12-21 in the pack or the goldens
  (`scrub_producer_metadata.py` audit, both directories).

## Build record

Stage 3, 2026-10-18. `build.py`: `checks.py` 113 run, 0 failed (the three-rules block R1 to R3c on the clean truth
and the pack, every SF row SF1 to SF10, the ladder's rungs and the golden's bracket, nineteen REFLEX routes each a
quarter bin or more outside the golden's cell, the out-of-sample record, ten constructions of the golden, the one-sigma
corridor, the timing margins, both asks equal to the truth with every device and hazard moving its stated figures, the
cracker pair on the cut pack at 35.7, 35.7 with A2 cracked and 36.5 with B1 cracked, mirror leakage 13.2 per cent,
the separation line by deletion, the input gates, the realism sweep and the dates); `verify.py` (csv, openpyxl and
pypdf, no generator import) 42 passed, 0 failed, every format read back with a positive control and the goldens and
write-up checked against its own recomputation; two consecutive builds byte-identical (target, golden, figures.json,
submission); `figures_check.py` 0 absent (30 figures); `voice-check.py` PASS (764 characters); `precut.py` exit 0;
`leak.py` REVIEW, no LEAK, every line answered; the H1 audit clean on the pack and the goldens; `guard.py validate`
clean, `surface` exit 0 (three card-level pairs, above), `heart` WARN (answered). 16 files in 4 formats (csv, xlsx,
pdf, json), the largest the legacy capacity export at 26,406 rows; distractors
`rn_workforce_survey_2025q1_2026q3.xlsx` and `agency_rate_schedule_2026-27.pdf` in `metadata.json`, each deletion
leaving the call and every ask unchanged. `target.zip` cut from the final rebuild, 16 entries equal to `target/` byte
for byte. The seed was fixed by rule (1601221) before any data was generated and never searched. Every file in the
pack carries the pull's modification time, 21 December 2026 09:30 Eastern (`dataset-generation` section 9).

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

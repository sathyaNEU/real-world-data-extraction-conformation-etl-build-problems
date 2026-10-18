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
   the capacity census, and the eight North hospitals new to the pool have met the wave about five weeks after Metro
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
   calibration `prior_period_close_out` (the closed winters' settlements and capacity reports the out-of-sample check
   reads). Each is free against task194, task470 and task243.
8. Spine: the association's daily capacity census (hospital x day, midnight census, staffed beds and declared surge
   level), 1 July 2021 to 20 December 2026, two layouts across the July 2024 system change; constructed in the layout of
   a hospital association's daily capacity reporting system.
9. Deliverables: `winter_pool_block_jan2027.xlsx` (the block, its components and the ask tables) and
   `pool_spend_winter_2025-26.png` (a chart on an ask's quantity, never on the block). The format set (xlsx and png) is
   in none of the last three builds.
10. People, drawn with `guard.py names --geo "United States" --seed 160`: Greg Matthews (the winter pool manager, the
    requester, in no file the prompt names and not in the prompt), Andrew Harvey (the association's surveillance lead,
    the wastewater and admissions reports), Linda Ashley (Crestfield's account manager), Shawn Whitaker (the
    association's finance manager, the settlement statements). Judith Harrison and Sheila Frazier were drawn first and
    replaced (each first name in an older build). Invented names checked on the web against real organisations: Two
    Peninsulas Hospital Association, Crestfield Medical Staffing, Inland Seas Nursing (no match); the hospitals are named
    and checked when the pack is cut.

**Data-native sentence.** The association's capacity census records every member's surge spells day by day, and in
every winter on file the respiratory wave has reached the North's hospitals about five weeks after Metro Detroit's while
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

## Tried and rejected


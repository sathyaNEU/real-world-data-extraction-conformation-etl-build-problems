# task176 design note

**Status: PAUSED at stage 1, no card ever registered, nothing cut.** Wave 8, new, Forecasting, seed FC47: a
broadband satellite operator with 360 satellites ready for 2027 and six rideshare launches (February, April,
June, August, October, December) of at most 60 each; satellites released at 210 km raise themselves to their
shell, and until they pass 350 km a geomagnetic storm's drag can bring them down; the mission assurance memo
lets a launch carry only as many satellites as keep its expected storm loss at two or fewer, the rest waiting
for 2028. The world, the decision and the quantity were kept; the seed's own mechanism (onsets against storm
days) was set aside as a unit reading to be filed as a WHAT. Two decisive steps were screened on code, the
brief's two ideas, and neither held on measurement. No architecture is live. This note holds the screen
record only; it carries none of the `precut.py` sections, because no design exists. The prototypes stay in
the session scratchpad (b176/proto).

**The structural sentence, and the first thing to read.** Every factor of a 2027 launch's expected storm
loss is either barely forecastable beyond climatology or barely moved by the solar cycle. The storm onset
rate for one phase of one cycle varies from cycle to cycle by a coefficient of variation of 0.40 at the 2027
phase, far more than the phase itself moves it, so the field's standard conditioning forms (phase with the
cycle's amplitude as sunspot number, as F10.7, or as the cycle's own storm level) spread wider than any cheap
route misses by, and none beats the all-years climatology out of sample by a visible margin. The time below
350 km, the factor the operator's own records measure precisely, is set by thrust and not by drag for any
satellite with the thrust margin to survive solar maximum, so the solar cycle moves it by 25 per cent from
F10.7 70 to 240 and by about 5 per cent between 2026 and 2027; it becomes steep only where the drag-to-thrust
ratio nears one at 210 km, which is where a batch is lost anyway. The loss per onset rests on the few dozen
batch-storm encounters an operator's history holds. A draw on this quantity needs a difference between 2027
and the record that is large, measured in full in the record, and estimated from many events; none was found
in this world.

**The taxonomy finding.** A storm-frequency step sits honestly in physical-environmental-sciences
`climate-weather-extremes` (F, never drawn), the frequency of an extreme in a coming window. The exposure step
is at that task type's edge (the thermosphere's solar-cycle climate, not an extreme). `hydrology-flood-frequency`
is a different field, and actuarial `claims-frequency-severity` (DD, F) fits only an insurer's world, which the
seed is not. The seed's Supply Chain line has no forecasting home for a hazard rate.

**The data finding.** GFZ's own file since 1932 (kp.gfz-potsdam.de, datapub.gfz-potsdam.de) and every NOAA,
NASA and SILSO host returned 403 at this session's proxy; PyPI and raw GitHub were reachable. The screen ran on
CelesTrak's `SW-All.txt` (updated 21 July 2025, bundled in the `spaceweather` 0.4.2 wheel on PyPI, CelesTrak's
note: no licensing requirement, cite the URL), which compiles GFZ's definitive Kp and Ap (CC BY 4.0, Matzka et
al. 2021, doi 10.5880/Kp.0001) and NRCan's F10.7 from 1 October 1957 to 20 July 2025 (24,765 days, 2,231 storm
onsets at Kp 5o or more with a 24-hour gap), plus the July 2025 monthly predicted F10.7 to 2041. So the record
holds cycles 19 to 24 in full and cycle 25 to 0.7 years after its October 2024 maximum, not the eight cycles
the seed names; the two missing cycles would narrow a mean's sampling error and close none of the family
spread below, which comes from how the cycle's strength is measured. SILSO's sunspot number (CC BY-NC 4.0) was
used only as a screen covariate. A pack set at a late-2026 as-of would need Kp from August 2025 onward by
another route, since a constructed Kp may not carry GFZ's or NOAA's name.

**Redraw in a new world, 2026-10-19 (actuarial-science-insurance / reserving-development-triangles,
Forecasting), screened at stage 1 and failed; no card registered, nothing cut.** The coordinator allocated the
cell; the client's reserving cards (`actuarial-science-insurance/loss-reserving-claims-development/1` to `/3`:
Berquist-Sherman on disposal rates, a fitted tail, a Mack or bootstrap range) and Bornhuetter-Ferguson against the
chain ladder are the careful reader's routes, so a stump had to be a judgment those take for granted that the data
settle. The structural sentence for the cell: every maturity shift (exposure attaching later in its period, reports
arriving sooner, settlement speeding up) moves the chain ladder by 15 to 170 per cent but moves
Bornhuetter-Ferguson materially only where the unpaid share is mid-range, and the disposal-rate card restates it
away whenever closed counts track the shift; the rest of the cell's triangle judgments are spent on file (case
adequacy, settlement speed, completion of immature periods, a cap that binds more often), banned this round (every
mix shift, `composition_mix`), need a filed future rate (calendar-year inflation, which is rule application or a
fork), or are a variance (ranges, tails). Prototypes are in the session scratchpad (r176/proto).

**Second redraw, 2026-10-19 (sociology-demography / population-estimation-demographic-projection, Forecasting),
screened at stage 1 and failed; no card registered, nothing cut.** The coordinator allocated the cell and lifted the
round's extra bans. The cell's cards (`sociology-demography/population-estimation-demographic-projection/1` to `/5`:
cohort-component ageing, gross migration flows, stated-coverage intervals, the control total, shrinking small-area
rates) are the careful demographer's routes. The structural sentence for the cell: the judgments those cards take
for granted that the records settle are each spent on file, closed by the guard's window, or a textbook route of
their own:
- who is at risk of a flow (duration since arrival, parity, a pool outside the area by age) is a hazard on a pool
  whose composition shifted (task134 v2, task468);
- a fixed stock's turnover is task132's renewal;
- a housing capacity is the housing-unit method;
- special populations are `population_selection` (task270's window) and census practice;
- a back-test of projection methods is `forecast_method_backtest` (task177's window);
- on population levels the structural levers run under 10 per cent, because flows are small against stocks.

Prototypes are in the session scratchpad (r176/demog).

## Tried and rejected

- **The solar cycle's phase, with or without the cycle's amplitude, as the decisive step** (the brief's first
  idea; prototypes `load.py`, `phase1.py` to `phase3.py`, `backtest1.py`, `season1.py`, and `screen_c1.py`,
  whose output `screen_c1.out` is byte-identical over two runs). Killed at stage 1 on measurement, on the real
  record: the right family spreads wider than the rivals miss by, and the data does not reject the rival out
  of sample.
  - The 2027 windows sit 2.3 to 3.2 years after the October 2024 maximum; the screen reads the half-year bins
    from 2.0 to 3.5 years after each earlier maximum. At Kp 5o or more with a 24-hour gap, in onsets a year:
    - all years 32.9, cycle 25's last 2.7 years 28.8, cycle 24's same phase 24.7;
    - the same phase of cycles 19 to 24 alone (phase-only) 42.4, by cycle 56.7, 30.7, 62.0, 54.0, 26.7 and 24.7;
    - a Poisson model on phase bins with log amplitude 34.3 (sunspot amplitude) and 40.6 (F10.7 amplitude),
      and cycle 25's own level times the earlier cycles' declining-to-maximum ratio 34.8 (mean ratio) and
      32.6 (median).
  - The amplitude-conditioned family runs 32.6 to 40.6 (25 per cent wide) and contains the all-years rate;
    phase-only sits 4 per cent above its top and the last 2.7 years 12 per cent below its floor. The Poisson
    model's dispersion is 2.51 per degree of freedom: the cycles differ by far more than counting noise.
  - The pattern holds at every threshold and gap tried. The family is 28.2 to 32.4 at a 48-hour gap
    (all years 27.3, phase-only 33.4) and 23.0 to 28.0 at 72 hours (all years 23.7, last 2.7 years 24.8). At
    Kp 6- it is 20.4 to 27.2 (all years 19.6, phase-only 28.7), at Kp 7- 5.2 to 11.2 (all years 7.3, phase-only
    11.3), at Kp 5- 43.8 to 50.3 (all years 41.6, phase-only 52.1), and at Kp 4o 55.8 to 61.4, where every route lands (all years 56.8, last 2.7 years 58.4).
    The lever and the spread grow together with the threshold: one dial.
  - The leave-forward back-test forecasts each of cycles 20 to 24 from the record before its window, in RMS log
    error over the five cycles: the sunspot-amplitude model 0.297, the F10.7-amplitude model 0.337, the last 2.7
    years carried 0.346, all years 0.363, level times shape 0.365 (four cycles), phase-only 0.512 and the previous
    cycle's same phase 0.528. Phase-only is worse than climatology, and the best form beats persistence by 0.05
    in log error with five cycles behind it, so no rival is rejected by a visible margin; a year-ahead forecast
    at this phase misses by about a third whatever the method.
  - The eda6c8c screens, as code: dispersion does not apply (a level), though the cross-cycle coefficient of
    variation at the phase is 0.40; variance-only passes (phase-only moves the point estimate to 1.29 times
    climatology); the common-exposure subset fires, since the same-phase years of past cycles, filtered and
    divided, are the phase-only route itself (42.4) and land above the family, while the family holds the
    all-years rate; truncation direction does not apply.
  - Determinism fails before strength. With six whole-satellite launch counts, or loading in 12-satellite
    trays, a bin holding a 25 per cent family spread plus one sigma (about 16 per cent, a six-cycle mean at CV
    0.40) leaves no room for the all-years route, which sits inside the family, or for the last two years,
    which sit 12 per cent from its floor.
  - Seasonality is not a separate stump. The record's equinoctial modulation of onsets (monthly factors 0.70
    in December to 1.24 in October at Kp 5o) is what a careful analyst gets by default when counting onsets in
    each window's calendar days across every year.
- **Exposure below 350 km set by the thermosphere's solar-cycle state as the decisive step** (the brief's
  second idea; prototypes `expo1.py`, `expo_run.py`, and `screen_c2.py`, whose output `screen_c2.out` is
  byte-identical over two runs). The revision log's overrun ("raising has run longer than planned") would be
  the solar maximum's thicker thermosphere, which the declining phase removes. Killed at stage 1 on lever:
  every cheap route lands inside the right family's own spread.
  - The truth, as built:
    - each batch climbs from 210 km under electric thrust (1.6e-4 m/s2, a 1.5 to 3 day checkout at 0.8 duty)
      against drag on an exponential thermosphere tuned to MSIS-like magnitudes, with density at 200 km of
      2.0e-10 kg/m3 times (F10.7/70)^0.72, a scale height of 33 + 0.055 (F10.7 - 70) km, an Ap term and a
      30 per cent semiannual oscillation;
    - real daily F10.7 and Ap drive it to 20 July 2025, then the July 2025 predicted F10.7 plus AR(1) and
      27-day noise;
    - 47 to 48 launches run from March 2020 to October 2026, each with a plan computed at a reference
      atmosphere (F10.7 150, Ap 12);
    - the 2027 windows run on the predicted F10.7 of 102 to 122; seeds 1, 2 and 3 were fixed before outcomes.
  - The lever is the climb's flux elasticity. With the thrust margin to survive solar maximum (ballistic
    coefficient 0.008 m2/kg) the climb takes 6.80 days at a constant F10.7 of 70, 7.25 at 130, 8.00 at 200 and
    8.55 at 240. Near stall (0.0095) it takes 6.95, 7.50, 8.60 and 9.70, steepening only past 240 (12.05 at
    280), where storms stall batches (1 to 2 of the history's launches never climbed).
  - The golden comes out at 7.05 to 7.64 days below 350 km. The right family (a physical replay on the
    planning flux, linear, log-log and quadratic regressions on the 81-day F10.7, and the launches flown
    within 15 of each window's planning flux) spreads 0.93 to 1.06 of its median.
  - The cheap routes, over three seeds, six windows and both regimes, as a share of the golden: the plan 1.01
    to 1.08, the all-history mean 1.01 to 1.06, the last four launches 0.97 to 1.05, the latest launch 0.97 to
    1.11, the plan scaled by the mean or recent overrun 0.97 to 1.06, launches in the same months 0.98 to
    1.14, and the straight-line trend 1.08 to 1.19. Only the trend clears the family's top, and at its nearest by
    0.04, under half the family's own width.
  - The eda6c8c screens, as code: the common-exposure subset fires, since the launches flown at the 2027 flux,
    filtered and divided, sit at 0.93 to 1.02 of the golden; variance-only passes; dispersion and truncation
    direction do not apply.
  - The overrun's other two causes give no stump either:
    - a procedural lengthening (a longer checkout) persists, so carrying the latest launches is the right
      forecast;
    - a heavier bus is a register column, so reading it hands the step over.
- **Paper screens, not coded.**
  - Storm-attributable loss net of background deployment failures (the excess over a baseline hazard): an
    operator flying about 2,500 satellites in 2020 to 2026 holds 50 to 70 batch-storm encounters. With a
    per-encounter loss fraction spread at a coefficient of variation near 1.5, the mean loss per encounter
    carries about 20 per cent at one sigma, against the under 10 per cent a 12-satellite tray bin can absorb.
  - Loss per onset by the batch's altitude at onset, or by the storm's intensity: the pooled rate carried onto
    a different mix is `composition_mix` (held for task165 and task173 in the queue), and it rests on the same
    encounter count.
  - The stragglers' long tail of time below 350 km (satellites with raising anomalies carry most of the storm
    exposure): the per-satellite mean from the orbit table is the careful route by default, a coin flip
    between a batch figure and a per-satellite one.
  - A loss per onset that rises with storm duration, since declining-phase recurrent storms last longer:
    unscreened; it needs a duration response fitted on the same few dozen encounters.
- **Redraw P1, 2026-10-19: an underwriting-year (risks-attaching) triangle whose recent periods' contracts attach
  late in the period, read on each period's own exposure clock** (prototype `p1_ev.py`, expected values). With 52
  per cent of a period's contracts moved from mostly 1 January to a 1 October inception, the period chain ladder
  files 0.55 to 0.93 of the true ultimate at ages 12 to 48 months (gamma payment patterns with means of 20, 30 and 45
  months), but Bornhuetter-Ferguson on the true prior files 0.79 to 0.99 of the true unpaid (0.88 to 0.94 at 36 to
  48 months on the 30-month pattern) and about 0.95 on the 2024 to 2026 total, so the textbook route for immature
  periods lands inside any bin the 30 per cent bar allows. A whole-period shift of inception is fixed exactly by the
  age-shift reflex (the old pattern read at the age less the shift). The re-based clock is also task468's live
  driver (development by months in the current episode, not since first activity) by the abstraction test, and
  `guard.py slots` on the driver hit task468's draw lines. Died at stage 1 on the BF reflex and the driver repeat.
- **Redraw P2, 2026-10-19: reports arrive sooner for recent accident years while settlement from report is
  unchanged, projected from reports and the payment delay from report** (prototypes `p2_ev.py`, `p2_sim.py`). On
  expected values, cutting the mean report lag from 12 to 4 months puts the chain ladder at 1.10 to 2.67 times the
  true ultimate and Bornhuetter-Ferguson at 1.05 to 2.20 times the true unpaid at ages 12 to 60. On a claim-level
  simulation (15 accident years, about 4,000 claims a year, larger claims settling later; seeds 1 and 2), the
  unpaid for accident years 2023 to 2026 over the truth is: paid chain ladder 2.01 to 2.17, Bornhuetter-Ferguson with
  the exact expected ultimate 1.19 to 1.20, Berquist-Sherman on all-years count ultimates 1.42 to 1.46, and
  Berquist-Sherman on latest-three count factors 1.05 to 1.08. The disposal-rate card is the careful reader's route
  once the reported-count factors visibly drop, and it lands within a bin. Died on the library test (stumping 1.3).
- **Redraw paper screens, 2026-10-19, each dead before code:**
  - a per-claim benefit cap that binds more as treatment intensity drifts up: task172's driver by the abstraction
    test (a per-unit cap that cut only the record's tail now binds most forward units), close to task168;
  - settlement speed through Berquist-Sherman or operational time: task127 architecture 3's mechanism (judge
    SEND_BACK, frequency-severity $350M against the restatement's $400M); case-reserve adequacy: task228's kill;
  - a calendar-year step (a fee schedule or benefit revision): a dated cause an event study finds, and rule
    application once filed; chronic calendar-year inflation: the forward rate is an assumption (a fork) or a filed
    index (rule application), with a lever of 5 to 15 per cent;
  - a tail from claimant-level annuities: a mortality-longevity task, a filed table is rule application, and the
    claimants' own deaths give about 6 per cent at one sigma; a fitted tail where the factor curve bends: the
    decay rate of late increments is too poorly determined (a 1 against 2 per cent decay halves the tail);
  - a reserve range or 75th percentile with diagonal dependence: the variance-only screen, and a spread estimated
    from 10 to 40 diagonals carries 20 per cent or more relative error;
  - chain-ladder leverage on immature years, additive against proportional development: the BF reflex lands;
  - every mix shift (channel, litigation share, claim type, deductible mix, closure order): `composition_mix`;
  - reopened claims by time since closure after closures accelerate: a lever of a few per cent (reopenings are a
    small share of the reserve), and returns by time since leaving read as task157's driver;
  - the split of development into new reports and growth on reported claims under a filed notification cut-off:
    once the window is filed as the WHAT, the report-year triangle and a reported-count projection are the careful
    reader's routes;
  - settlement timed by a litigation calendar's trial dates: task172's per-unit scheduled date ending the wait, and
    a timing-only lever on a reserve; claims-unit closure capacity: the swap test fails (any queue);
  - excess-layer, large-deductible and per-policy aggregate development: too few claims for a sigma near 1 per
    cent and an open per-claim family; retro-rating and corridor treaties: the contract formula is rule
    application; a large-loss transfer between claims systems: a filed threshold plus a join;
  - a closed exposed pool depleting as members claim (latent and mass claims): the hazard's shape on the remaining
    pool is a fork (constant against heterogeneous), the forcing rosters sit in epidemiology, and the natural
    instances are sensitive.
- **Second redraw D1, 2026-10-19: returners drawn from the area's diaspora (people born there living elsewhere), a
  wave that left at 20 to 30 in 1995 to 2010 now ageing into the return ages** (prototype `d1_diaspora.py`, expected
  values, return hazard 0.5 per cent a year at 25 to 49 and 2.0 at 55 to 69). On the 2027 to 2031 return flow the
  card-2 route (origin-destination rates by age on the origin population, struck over 2016 to 2025) files 0.62 of the
  truth, a linear trend 0.81 and the latest year carried about 0.75; at 55 to 74 the card-2 route files 0.08 of the
  flow. But on the 55 to 74 population level the returns move the figure about 4 per cent, and the abstraction is
  task134 v2 round 1's driver (an inflow that a pool held outside the decision's record sends at a hazard on that
  pool, whose composition shifted). The birthplace column on the in-migration records also makes the split a row
  predicate. Died on the driver repeat and the level lever.
- **Second redraw paper screens, 2026-10-19, each dead before code:**
  - duration-dependent out-migration after an influx (mover-stayer): task134's slot measured it at about 1 per cent
    (its `sim1.py`), and it is task468's and task134 v2's driver (a hazard by time since entry after a surge);
  - gross against net migration (card 2): task150 shipped it on school attendance areas, and task134's slot found
    the gross variants split unless every origin is static;
  - second births echoing a surge of first births (parity and interval): the same time-since-entry family;
  - housing-constrained growth: the housing-unit method (dwellings, occupancy, persons per household) or a
    headship-rate household projection is the field's textbook for a capped small area, and task79 carries the
    capacity insight;
  - turnover in a fixed stock as its occupants age in place (vacancy chains): task132's renewal driver;
  - special populations (students, prisons, barracks, care homes) that do not age in place: `population_selection`
    sits in the window (task270), and projecting group quarters apart is census practice;
  - the control-total gap allocated by the component that makes it up (card 4's judgment): the regional model's
    closed-system note reads it out, and each area's own external migration, the careful route, lands;
  - a births-based base for young children against a census undercount: a lever of about 5 per cent;
  - stated-coverage intervals with cross-area correlation (card 3's judgment): the variance-only screen, and a
    correlation estimated from 30 years carries about 15 per cent;
  - shrinkage choices (card 5): the shrinkage family (stumping 1.2);
  - fertility postponement and recuperation: a future-rate assumption, a fork;
  - cohort mortality improvement at 85 and over: the mortality-longevity card;
  - a group returning in a wave: task157;
  - two-sex births (partner availability): the marriage function's form is open (harmonic, geometric, minimum)
    and the real effect is weak;
  - simple trend methods beating cohort-component out of sample: `forecast_method_backtest` sits in the window
    (task177);
  - a caseload ageing out at a fixed age: task172's cap;
  - education-specific rates: a mix on a visible column;
  - an error-of-closure correction of the base: one past event per area and a back-test organ.

## Retired

**RETIRED 2026-10-19 under the author's rule that a number which dies in its second new cell this round is
retired.** Three worlds were screened at stage 1 and none held:
- the seed's satellite storm-loss world, two architectures on code;
- actuarial reserving triangles, P1 and P2 on code and 17 on paper;
- sociology population projection, D1 on code and 18 on paper.

No card was ever registered, so no guard axis is held. The screens above are the number's record for `guard.py
slots`.

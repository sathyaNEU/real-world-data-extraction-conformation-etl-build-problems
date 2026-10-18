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

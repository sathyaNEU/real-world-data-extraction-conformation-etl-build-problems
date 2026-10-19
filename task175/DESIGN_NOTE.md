# task175 design note

**Status: PAUSED at stage 1. No card has been written or registered, which is deliberate.** Two screens
have run on this number and neither produced a design that meets the bar (every reflex route a full bin
from the golden, the right family inside a quarter-bin of the bin centre with one sigma, a lever of 30
per cent or more of the graded figure with sigma near 1 per cent). The first (2026-10-18) took the seed
FC46's world, decision and quantity and measured two capped-cost candidates dead over three seeds each.
The second (2026-10-19) redrew the number in the cell the coordinator allocated,
human-factors-ergonomics / human-reliability-assessment for Forecasting, set nine candidates aside on
paper against the deaths already on file in this cell and measured the two survivors dead on code
(`## Redraw screen` below). Nothing was cut, `architecture` stays 0, and no axis of the guard's window was
spent.

## What was screened

- **Seed** FC46, header and Situation only (`status.py task175`). Kept: an online music retailer gives
  its 25,000 best customers a free two-day shipping membership for 52 weeks; the programme pays at most
  $150 of any member's shipping; the catalogue sits across three fulfilment centres, standard orders
  wait for the consolidation shuttle and ship in one parcel, two-day orders cannot wait and ship one
  parcel per centre the basket spans. The call: the shipping the programme pays for the 25,000 over the
  first 52 weeks, one budget figure. The seed's own mechanisms (a parcel count read off the SKU location
  table, the cost report's per-item shipping as an official decoy) were never candidates.
- **Pairing tried:** `product-analytics` / `retention-cohort-lifetime-value-modeling` (serves F),
  objective forecasting, decision a quantity figure. `churn-propensity-uplift-modeling` was the fallback
  for a response-heterogeneity step; the measurements below close both.
- **Corpus reads** before any design: `guard.py recent`, `coverage`, `mechanisms --objective
  forecasting` (81 builds) and `slots` on three term sets (membership, subscription, free shipping,
  capped, limited expected, Jensen; BG/NBD, Pareto, P(alive), dropout, lapsed, regression to the mean,
  heterogeneity, negative binomial; cart, session, batching, basket, consolidated). The hits that bear:
  task151 rejected the step payout alone at its draw ("one enumerable insight (Jensen) is the coin-flip
  signature"); task147 rejected a Jensen gap on capacity as too small to move its pick; task130 v3 died
  on the analog cohort (a group chosen on a noisy outcome, forecast by the next-period experience of a
  group chosen the same way, landed in four minutes); task153's driver is a per-segment cap at a
  tankful; task142 and task143 spend "the distribution, not the point" on a percentile and a joint
  chance. No screen on file touches cart sessions or order batching.

## The harness

`scratchpad/b175/proto/` in this session (session-scoped; rebuild from this section). `proto2.py` is
candidate 1, `proto3.py` candidate 2, `pilot52.py` the subset arithmetic, `proto1.py` and `sweep1.py`
the first parameter sweep. Shared world: 420,000 customers; weeks from Monday 2 January 2023 to Sunday
29 November 2026 with a December-heavy seasonal profile; registration dates spread with growth (55 to
60 per cent before the window); standard order rates gamma across customers (shape 0.8 or 0.9); the
25,000 chosen as the top trailing-52-week spenders to 29 November 2026; a 26-week randomised pilot from
28 April 2025 (15,000 treated of the then top 40,000 by trailing spend, the rest the holdout); per-order
two-day cost gamma with a member-level mean (zone and centre mix, lognormal SD 0.18) and CV 0.45, so a
year's cost given its order count is gamma and every capped expectation is computed exactly, summed over
the count's predictive distribution, never simulated. The golden in each candidate is what a correct
analyst computes from the pack: a negative binomial fitted by maximum likelihood on every customer's
counts and exposure, each member's posterior predictive for the membership year, the pilot's estimates,
and the cap applied to each member's predictive cost distribution.

## The structural finding: a member-level capped forecast is a continuum, and the cap cancels

The truncation-direction screen passes (the cap hides the top, and the latent quantity is the upper tail
of each member's coming year), and the variance-only screen passes (every spread moves the point figure
through the cap). What kills the family is three regularities, each measured:

1. **The right family is a continuum, not a point.** Every source of a member's predictive variance
   lowers the capped total by its own fraction: the estimation uncertainty of the member's own rate
   (posterior mean with chance on top, against the negative binomial predictive) **+1.26% to +1.54%**,
   the response's form at fixed moments (gamma against lognormal) **+0.41% to +0.51%**, the parcel-cost
   spread mis-set by a third **-0.41% to +0.30%**, and the pilot's own sampling (estimated against true
   response parameters) **-0.70% to +0.51%** at 15,000 treated (one sigma about 0.6 per cent; at 6,000
   treated +1.07% on one seed). The rate-uncertainty term is structural: its share of the predictive's
   chance variance is the membership multiplier over the years of history, about 0.47 to 0.52 at three
   years, so no realistic history removes it. The family therefore spans 1.5 to 2.5 per cent, which
   needs bins of 6 to 10 per cent for a quarter-bin margin.
2. **Under a per-member cap a misallocated factor is half absorbed, so errors cancel.** A member pushed
   above the cap loses its error and a member pulled below keeps it, so a common factor applied in place
   of each member's own errs downward, while capping a point forecast errs upward. The route that does
   both lands near the golden: orders times the pilot's average uplift, point-capped, **+1.77% to
   +2.60%** (candidate 2); the analog cohort times the average uplift **+2.15% to +3.06%**
   (candidate 1).
3. **The pilot is either too short or it hands the answer over.** A 26-week pilot leaves the annual cap
   to a model (the continuum above). A 52-week pilot answers by filter and divide: capping each of a
   random 6,000 like members' realised years and scaling to 25,000 lands **-0.86%** from the golden with
   a sampling SD of **0.58%**, within $50,000 of the golden in 194 of 200 draws. There is no pilot
   length between.

So at bins narrow enough for the far partial routes to miss (about 4 per cent, $100,000 on a $2.4M to
$2.7M figure), the right family alone breaks the quarter-bin and the cancelling routes of law 2 sit
inside one bin; at bins wide enough to hold the family (6 to 10 per cent), the plug-in, shrunk-response
and analog routes land in the golden's bin or the next. This is the same dial at both ends
that `stumping` 1.6a and `determinism-check` section 1 record for task194, met here on a capped sum.

## Redraw screen: human-reliability-assessment (2026-10-19)

- **Cell and fences.** human-factors-ergonomics / human-reliability-assessment (serves Forecasting), a
  pairing never built. The round's bans: pattern G14, `composition_mix`, `local_government`,
  `committee_or_panel` and `executive_team`, `programme_officer` and `capacity_planner`,
  `monitoring_export` and `filed_standard`. The guard's window after task249, task269 and task468 adds
  patterns G16, G2 and G13, strategies `causal_design`, `decomposition_attribution` and `composition_mix`,
  and shapes 04 and 05. The library refresh (b7a54be) leaves Human Factors with no cards, so the seeds
  were the five families in `two-layer-task-design.md` and the nearest domains' cards (healthcare
  delivery's patient-flow and provider-quality cards, general statistics' calibration, robustness and
  measurement-error cards, banking's reviewer-capacity and labels-above-the-line cards).
- **Deaths read first, all binding on this cell.** task171 (screeners' detection under short stints and a
  new-hire cohort; dispensing errors under longer shifts, task149's within-person driver); task230 v2
  (the low-prevalence effect at a shared verification pool, shipped in this task type and retired);
  task194 architecture 8 (signal detection's discriminability against criterion, accident-proneness, an
  own rate behind a load-dependent downstream catch); task202's six human-factors drivers (an unpublished
  opportunity count a forward change multiplies, which is task181 v4; within-period clustering; two
  checks' joint miss; a practice curve; a classification lag; a marginal contribution to a set); task181
  (losses of separation follow level crossings); task182 (composition and observability screens).
- **The structural finding.** In its own form, human reliability forecasting carries an error
  probability conditioned on performance-shaping factors onto the forward mix of those factors, which an
  honest card labels G14 or `composition_mix`, both out this round. The structures in this field that
  are not a mix (dependence between checks, prevalence and detection criteria, thinned counts, time on
  task, learning, shift length, unpublished opportunity counts, co-presence pairs, classification lags,
  bursts, proneness, load-dependent catch, latency waves, caps, calendar locks) are each spent on file.
  The residue was two candidates, a time-reliability race read at each demand's own window and a
  performance-shaping factor's slope flattened by a noisy record, and both died on measurement.
- **The harness.** `scratchpad/r175/proto/c11.py` (the race, five seeds, a `vol` multiplier) and
  `c10.py` (the flattened slope, three seeds, settings `b` and `lam`), session-scoped; each was run twice
  with byte-identical output, and the settings and figures are in the Tried and rejected lines so the
  harness rebuilds from this note. `guard.py slots` on both driver sentences returned lexical overlaps
  only (task182, task194, task117, task132, task201), no screen of either mechanism.

## Tried and rejected

- **Candidate 1, the cap priced on each member's predictive year, with the spread of individual
  responses the pilot measures** (2026-10-18, stage 1, measured on seeds 1, 2, 3). Driver as drafted: a
  per-member cap is worth the limited expected value of each member's coming year, whose spread comes
  from chance, from how far the member's own record pins its rate (the members were chosen for a good
  year), and from how differently members answer free shipping, which the pilot's treated arm shows as
  spread beyond its holdout's. Golden $2,449,197 to $2,478,491 (response mean 1.55, SD 0.70, gamma).
  Routes against the golden: posterior mean with chance and the response spread +1.52% to +1.54%
  (family, breaks the quarter-bin); lognormal response +0.41% to +0.51%; the three-year rate plugged in
  with the response spread +5.86% to +5.87%; individual responses shrunk toward the mean +5.01% to
  +5.35%; the analog cohort (last year's top 25,000 and their next year) times the average uplift
  +2.15% to +3.06%; the analog cohort with drawn responses -4.57% to -5.04%; posterior predictive with a
  common uplift +7.30% to +8.21%; the pilot's average cost seasonally scaled, uncapped, times 25,000
  +8.78% to +10.35% (and +0.85% in a configuration with shape 1.1 and response 1.40/0.65, so its position is
  a coincidence of parameters); point posterior capped +13.71% to +14.64%; the default path
  (trailing-year orders times the uplift times the two-day cost, capped) +28.47% to +29.58%; raw
  individual ratios as the response spread -12.39% to -13.13%; the pilot seasonally scaled and capped
  -15.52% to -16.47%; uncapped +30.95% to +32.41%. Sensitivity: +1% on the mean response moves the
  golden +0.67% to +0.69%, +5% on the response SD moves it -0.64% to -0.71%. The first sweep (true
  response parameters, response CV 0.30 to 0.60, cost $9 to $12 an order, shape 0.45 to 0.80) put the
  plug-in-rate route at +2.40% to +5.67% and the common-uplift route at +3.23% to +14.03%. Dead on the
  continuum (law 1) and the analog cancellation (law 2), and the response spread is a dispersion whose
  estimator family is open in form, which is the dispersion screen's warning met exactly.
- **Candidate 2, membership orders are the member's purchase sessions, which its paid-shipping orders
  batched** (2026-10-18, stage 1, measured on seeds 1, 2, 3). Driver as drafted: once shipping is free a
  member places an order at each visit whose items it buys (the cart log's sessions), so the coming
  year's orders are its sessions, not its past orders times the pilot's uplift, and heavy buyers, who
  batched most, take the cap fastest. Built to remove candidate 1's latent response form (each member's
  response is its own sessions per order, observable, correlation of log sessions with log batching
  0.55 to 0.57 among the 25,000). Golden $2,691,823 to $2,709,498 (the pilot's session-to-order
  conversion 0.879 to 0.881 and session uplift 0.076 to 0.083). Routes: posterior mean with chance
  +1.26% to +1.27% (family, breaks the quarter-bin); orders times the average uplift, point-capped
  +1.77% to +2.60%; the same with chance +2.36% to +3.20%; the pilot's average cost seasonally scaled,
  uncapped +3.37% to +3.73%; the three-year session rate plugged in +4.37% to +4.43%; items over the
  pilot's basket +4.97% to +5.45%; orders times the uplift with the predictive -4.53% to -5.28%; the
  analog cohort's orders times the uplift -4.69% to -5.76%; point posterior sessions capped +6.38% to
  +6.40%; every session taken as an order +6.92% to +7.08%; trailing-year sessions +10.07% to +10.19%;
  the default path +10.94% to +12.08%; the pilot capped and scaled -17.25% to -17.60%; uncapped +23.56%
  to +23.89%. The analog cohort's own sessions, the empirical member of the right family, sat -2.05% to
  -2.56% (the harness dropped the pilot's treated members from the analog, whose second year carries
  membership months; a careful analog strips those months instead). Dead on laws 1 and 2: the
  point-capped uplift route and the pilot average sit inside one bin, and the family spans more than a
  quarter-bin. The order-to-session unit is also `grain_or_unit` beside task153's segment-by-segment
  cap, which the brief named as a driver to stay clear of.
- **Also set aside at the draw, on paper, before either prototype:** the cap's Jensen gap alone (task151's
  measured coin-flip signature, and enumerable); regression to the mean of the chosen 25,000 alone
  (task130 v3's analog-cohort death, and the analog is free here); the pilot's mean response as the
  decider (the common-exposure subset screen, law 3); the split count off the SKU table (a stated
  construction, the seed's banned mechanism); a novelty burst in the pilot's response (the midpoint of
  the pilot's average uplift and its latest month is exactly the 52-week answer, since the burst falls
  once in both windows); the response conditioned on batching or on the delivery time two-day saves
  (`composition_mix`, which task165 and task173 carry in the ban window, and a stratification reflex on
  a column the history builds); a capped trial's stopping rule (Wald's identity makes events over
  exposure on the offer weeks consistent, so the on-offer weeks answer by filter and divide); free
  shipping weeks as the response (a promotion measures stockpiling, not the unbatching a membership
  causes); uptake of the invitation (a censored activation clock on the lightest members, a lever of a
  few per cent); members going quiet in the year (the analog cohort hands it over by recency band).
- **Redraw candidate 11, a time-reliability race read at each demand's own window** (2026-10-19, stage 1,
  human-reliability-assessment, `c11.py`, five seeds). World: a bulk liquids terminal whose operators stop
  each transfer between the high-level alarm and the automatic overfill trip; the time each alarm leaves
  is the tank's headspace between the two levels over the transfer's fill rate; the operator's response
  is a two-component lognormal (attentive, median 4.0 minutes; lapses, 12 per cent, median 16) independent
  of the rate; 2027 raises the pipeline receipt rate into the gasoline tanks from 700 to 1,000 to 1,600 to
  2,000 cubic metres an hour. Graded figure: expected automatic trips in 2027. Driver as drafted: the
  chance a demand fails is the response-time survival read at that demand's own window, so shorter
  windows raise trips by the curve's bend across demands rather than at their average window. At a
  typical terminal (about 10,800 transfers and 480 alarm demands a year, 23 to 41 trips in four years,
  2027 truth 11.2 to 12.8 trips) the golden family (Kaplan-Meier on response times censored at each
  trip's window, and the two-component mixture) agrees within 2.4 points but sits -11.0 to +14.5 per
  cent from the truth, sigma about 9 per cent. At the largest realistic terminal (three times the volume,
  88 to 108 trips in four years, truth 33.3 to 38.3) the golden sits -2.6 to +8.7 (sigma about 4) while
  the trip share by window band, a filter and a divide once each demand's window is built, lands -12.3
  to +5.7 (mean -1.8); trips per demand by stream with the changed stream rate-scaled -13.1 to -30.7;
  persistence -18.9 to -41.3; the field's textbook time-reliability curve (one lognormal fitted to the
  operators' stop times, read at the nominal window) -77.3 to -85.3, and with the trips taken as
  censored -67.0 to -76.2; single-component censored Weibull and log-logistic fits 25 to 50 per cent
  under. Only at ten times a terminal's volume (about 20,000 demands, 350 trips) does the golden reach
  +0.1 to +5.8, and there the window-band share lands -7.0 to +7.9. Dead three ways: sigma 4 to 9 per
  cent at any real volume, because trips are rare and the lapse tail that decides them is read from
  those few; the subset screen (the window-band share lands inside the golden's own seed range); and
  the library test (the golden is the censored survival curve applied demand by demand, the
  probabilistic-analysis card's "not at the mean" with the forcing fact, faster receipts, cueing the
  window). An honest card also reads it as a trip rate conditioned on each demand's window carried to the
  forward window mix, G14.
- **Redraw candidate 10, a performance-shaping factor's slope flattened by a noisy record** (2026-10-19,
  stage 1, `c10.py`, three seeds). World: medication administration errors per ward-shift Poisson in
  administrations, log rate rising by `b` per patient per nurse actually on the floor; the staffing
  system records the ratio with classical error (reliability `lam`); a badge-swipe audit on four wards for
  six months (2,160 ward-shifts) carries the true ratio; 2027 mandates at most 5 patients per nurse
  against a recorded mean of 6.3. Graded figure: expected 2027 administration errors (truth about 11,700).
  At a realistic effect and record (`b` 0.15, `lam` 0.6, 43,000 errors in three years) the naive slope
  misses by only +7.0 to +9.3 per cent (fitted 0.089 to 0.091 against 0.15), against the 30 per cent
  that held; the golden (regression calibration, moments) sits -1.6 to +1.3, SIMEX with a quadratic
  extrapolant +3.3 to +4.0, and the slope fitted on the audited ward-shifts alone -5.7 to +2.2. The lever
  is exp(-b(1-lam)D) for a forward shift D, so 30 per cent needs `b` 0.30 with `lam` 0.4 at once; there
  the naive slope misses by +27.5 to +31.1, but the golden's own seed range widens to -7.1 to +7.0
  (reliability estimated 0.36 to 0.40 from the audit), SIMEX splits the family at +15.0 to +21.9, and
  the audited rows alone land -0.6 to +2.4, nearer the truth than the designed correction. Dead on the
  lever at any plausible setting, on the subset screen (the card's own validation rows are a filter that
  beats the correction), on an open method family (the extrapolant), on the library test (general
  statistics' measurement-error card 2 applied as stated, its pin the audit file), on the swap test
  (staffing and errors swap for any load proxy and failure count) and on the label (an error rate
  conditioned on staffing carried to the mandated ratio is G14), beside task149's workload driver.
- **Also set aside in the human-reliability cell, on paper, before either prototype:** the low-prevalence
  effect at a final check after an upstream improvement (task230 v2, and G14 by its honest label;
  inside the observed range a filter and a divide, outside it a 15 per cent family spread on paper);
  confusable items or addresses grouped together (task181's co-presence); red-signal approaches as the
  exposure for a new timetable (task202 C1, task181 v4, and the forecast of red approaches is an
  operations simulation); errors at the first execution after a change (C1 again, and G14); adding or
  removing a redundant check (task202 C3, and a read-across); latent maintenance errors found at
  scheduled inspections (a dose-response conditioned yield, task77 v1's pipeline and task157's wave);
  time-reliability tails for a single action (the empirical share is a filter and a divide,
  extrapolated tails spread by form, and samples per action are sparse); a reminder or re-alarm moved
  inside a response duration (task172's driver in other nouns); fatigue states under a new roster
  (task171's shift death, G14, and the fatigue models' own spread).

## Resume

Neither screen left a live design, so the next move is the coordinator's or the author's: move the
number to another Forecasting cell, or come back to human reliability when the round's G14 and
`composition_mix` bans lapse. Do not re-screen, in either world, anything in `## Tried and rejected`:

1. **The seed's world (FC46).** The three laws close the per-member capped forecast for any decisive step
   that refines a member's predictive year, because the refinements form a continuum wider than a
   quarter-bin and the cap makes the common-factor and point-forecast errors cancel.
2. **Human reliability under this round's bans.** The cell's own form is a conditioned error probability,
   which is G14 by an honest label, and its non-mix structures are spent on file (the redraw screen's list).
   A time-reliability race dies on rare trips and the window-band filter and divide; a flattened factor
   slope dies on its lever and on the audited rows. A further draw here would start from a file the
   organisation keeps whose forcing input no stratification of the error log reproduces, and would price
   the four unscreened card seeds first, with their predicted deaths: labels that exist only above a
   review line (a verified subsample, spent, and a filter and a divide on it); reviewer-capacity yield (a
   binding constraint on a filed integer of hours); an error-risk score's calibration against its ranking
   (the card applied as stated, the library test); blocking probability against occupancy for a staffed
   desk (queueing, the swap test).

Window facts on 2026-10-19 after task468: patterns G16, G2 and G13, strategies `causal_design`,
`decomposition_attribution` and `composition_mix`, and shapes 04 and 05 sit in the ban window, and this
round's six serial registrations will move it again.

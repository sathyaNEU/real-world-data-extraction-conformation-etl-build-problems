# task175 design note

**Status: PAUSED at stage 1. No card has been written or registered, which is deliberate.** The wave
brief for this number says to screen by measurement before any card and to stop after two candidates
that do not hold. Two candidate designs on the seed's world, decision and quantity were prototyped and
measured over three seeds each; neither meets the bar (every reflex route a full bin from the golden,
the right family inside a quarter-bin of the bin centre with one sigma, P(both) clearly under 0.08).
Nothing was cut, `architecture` stays 0, and no axis of the guard's window was spent.

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

## Resume

Do not re-screen the per-member capped forecast in this world: the three laws above close it for any
decisive step that refines a member's predictive year (rate uncertainty, response spread, batching,
severity), because the refinements form a continuum wider than a quarter-bin and the cap makes the
common-factor and point-forecast errors cancel. Two routes for the next pass, priced before drawing:

1. **Keep the world and move the decisive step off the member's predictive year**, to a level that
   neither the pilot (law 3) nor the analog cohort (task130 v3) hands over and that is not a filed
   forward condition. On paper the candidates for that are few, because the record measures standard
   behaviour (the analog) and membership behaviour (the pilot) for like members, and what neither
   measures is mostly a filed 2027 change, which is rule application. Price any such candidate on the
   harness against laws 1 and 2 before writing a sentence.
2. **Re-number to another seed in the lane** if the author prefers: the seed's quantity, a per-member
   capped benefit over a year, is the structure that fails, not the domain.

Window facts for whoever draws next: `single-figure` is likely blocked by `ban.shape` once task165
registers, and `composition_mix` by `ban.strategy` until three builds register after task173.

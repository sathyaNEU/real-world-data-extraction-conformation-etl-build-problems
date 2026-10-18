# task177 design note

**Status: PAUSED at stage 1, no card ever registered, nothing cut.** Wave 8, new, Forecasting, seed FC48:
thirty unstaffed recycling drop-off points opened in December and January with 15 bins of 1,100 litres each
(ten on the coast, twenty in town, five of them in the Larchmere enclave round the lake), a July standard
(a point gets enough bins that its forecast July average weekly fill is at most 80 per cent of its bins),
weekly emptying logs carrying each bin's fill and any side waste, and a bin order due at the manufacturer by
15 March. The world, the decision and the quantity were kept; the seed's own mechanisms (the standard's "of
like demand" read as a filed method, the dashboard's district indices deciding as a decoy, a holiday-home
flag read off the property register) were set aside. Two decisive steps were screened on code, both forms of
the brief's comparison-group idea, and neither held. No architecture is live. This note holds the screen
record only; it carries none of the `precut.py` sections, because no design exists. The prototypes stay in
the session scratchpad (b177/proto).

**The structural sentence, and the first thing to read.** The graded object is a small sum of ceilings: at
each point the bins to add are the July fill over 0.8, rounded up, less 15, floored at nil, so a point that
will need 20 to 30 bins in July carries 5 to 15 of them in the answer and every per cent of error in its
July forecast moves its share of the answer two to three per cent. Each new point's forecast rests on its
own 10 to 13 winter weeks (about 2.5 per cent at a weekly noise of 8 per cent) and on its peers'
July-to-winter ratio, which runs 2 to 6 per cent apart from peer to peer within one kind of catchment. So
the right family's own members disagree by a median of 2.4 to 3.2 bins at a holiday point, which rules out
grading any point's bins, and the total moves 2.7 to 3.9 per cent under a redraw of the weekly noise. A bin
wide enough to hold the family with one sigma and a quarter-bin margin is a fifth to a third of the answer,
and at that width a flat summer uplift near the golden's own implied factor lands, along with the partly right
readings (the size or nearest-point peers, the half-term alone, the holiday points pooled). Thirty points
are too few for the lever this decision has against that noise.

**The registration finding.** The comparison-group step is honestly `composition_mix` (a district rate that
does not fit a point whose kind no column names, the kind rebuilt from the point's own winter history:
strategies F5, and task124 labelled a kind read from records the same way). task165 registered
`composition_mix` at 14:10 and task173 carries it in the queue, so the step could not be registered beside
either; `forecast_method_backtest` would have passed the guard and was not used. The window after task165's
registration (task201, task247, task165) also banned every honest forcing event, organisation and role this
world offers: the forcing event `season_or_peak` (task201, task247) and `purchase_order_or_contract`
(task165), the organisation `utility_or_infrastructure` (task201; a waste contractor running the network,
SIC 2007 section E) and `local_government` (task165), and the role `field_unit_lead` (task201, task247) and
`operations_director` (task165).

**The taxonomy finding.** The deciding quantity, each catchment's July population present against its
winter population, sits honestly in sociology-demography `population-estimation-demographic-projection` (F):
a seasonal population read from a symptomatic series, the waste itself, against catchments of like mix. The
literal home, urban-regional-science `municipal-service-demand-resource-allocation` (F), is task165's pairing
in the window.

**The repeat screen.** `guard.py recent`, `mechanisms --objective forecasting` and `slots` ran before any
card. `slots` on both candidate drivers, and on peers, analogs, summer, holiday, half-term, seasonality,
second homes, lets, owners, occupancy, cold start, like demand, comparable sites, seasonal index district,
summer uplift and drop-off bins, found no slot that spent a peer-seasonality or holiday-response mechanism;
the hits were words in unrelated notes. The closest card by mechanism is task124 (a unit's kind read from
its group's surviving records), the same family by its label.

## Tried and rejected

- **Candidate 1: peers read from each point's winter response to Christmas and the February half-term,
  three kinds of catchment** (residents, coastal villages with some lets, holiday cottages; the Larchmere
  enclave holiday cottages inside the Town district, the coast's villages and cottages mixed along the
  shore; prototypes `world4.py`, `p6.py`, `screen177.py`, whose output `screen177.out` is byte-identical over
  two runs; seeds 1 to 3 fixed before outcomes). Killed at stage 1 on measurement: the right family will not
  hold whole bins at any point, and at the width the total needs, a flat uplift and the partly right readings
  land.
  - The world: 140 mature points with two years of weekly emptyings (the Coast district 26 villages with
    some lets, 16 cottage sites and 12 residential estates; the Town district 76 residential villages and
    estates, 6 forest-lodge sites and 4 villages with some lets) and 30 new points opened 7 to 21 December
    (on the coast 5 villages, 3 cottage sites and 2 estates; in town 15 residential points and the five at
    Larchmere), the cottage points at 70 to 80 per cent of their 15 bins in an ordinary January week, the
    coastal villages at 60 to 73 and the residential points at 57 to 63. Weekly fill is the point's
    catchment (residents on a resident calendar with the Christmas packaging peak, holiday occupants on a
    school-holiday occupancy calendar) times a weekly noise of 8 per cent, with a 4 per cent summer factor of
    the point's own.
  - The golden (each new point's mean over its own weeks times the mean July-to-same-weeks ratio of its 8
    nearest mature points on the two winter responses): 153, 146 and 156 bins to add (truth 146, 144, 144).
    The right family (4 to 12 nearest, median, log and raw features, a silhouette-chosen k-means, local and
    quadratic regressions, the Christmas response alone, the whole weekly profile, a two-calendar
    decomposition, the true kind's mean) runs 135 to 157, 124 to 148 and 144 to 160, so -12 to +3 per cent,
    -15 to +1 and -8 to +3 of the golden; the k-means and the quadratic fit are the low members. One sigma
    over 12 redraws of the weekly noise is 4.4, 4.9 and 4.3 bins (2.8 to 3.3 per cent).
  - Per point the family spreads a median of 3.1 bins needed (3.11, 3.06, 3.15) and up to 5.8 to 6.3 at the
    non-residential points, against a whole bin, so no point's bins can be graded.
  - The reflexes, as shares of the golden: the district's own ratio -56 to -62 per cent, the dashboard's
    monthly index -56 to -62, every mature point's ratio -67 to -71, the 1, 3, 5 or 8 nearest points -55 to
    -69, a fit on distance to the coast -58 to -65, the Coast district's ratio borrowed for every
    holiday-looking point -36 to -44, the last July at the nearest point -78 to -83, a flat 1.25 -31 to -37, a
    flat 1.5 +33 to +34, a flat 2.0 +173 to +182, peers of like size -24, -30 and -4. The behavioural readings
    sit inside the family: the holiday-looking points pooled -12, -8 and -3, the top-ratio peers -1, +3 and +9,
    the half-term alone -5, -10 and -3. The decisive split is one obvious split (holiday or not), so it
    reads off the new points' own winter weeks once anyone looks.
  - The flat factor's total climbs about 40 to 46 bins per 0.1 and crosses the golden at 1.37 to 1.38
    (T(1.35) 145, 132 and 145; T(1.40) 166, 153 and 163), so 1.35 and 1.40 sit within 7 to 14 bins of it.
  - The back-test (each mature point forecast from its own winter 2025-26 against its July 2026, every other
    point as the pool) rejects the rivals by a visible margin: RMS log error 0.056 to 0.066 for the nearest
    peers on the two responses against 0.21 to 0.23 for the district, 0.26 to 0.27 for all points and 0.21 to
    0.22 for the three nearest points, and on the points whose kind is unlike their district 0.047 to 0.071
    against 0.43 to 0.46. Separation was never the problem.
  - Determinism at the total: rounding to 10, 20 or 25 bins, the family leaves the golden's bin in every
    seed but one (seed 3 at 25), and there one sigma breaks the quarter-bin margin; rounding to 50 holds the
    family and the margin in seeds 1 and 3 (in seed 2 the k-means leaves the bin), and puts the flat 1.35
    and 1.40, the pooled holiday points, the top-ratio peers and the half-term alone inside the golden's bin
    in every seed (and the size peers in seed 3).
  - The eda6c8c screens, as code on the clean truth: dispersion does not apply (a level; the July ratio's
    coefficient of variation within a kind is 0.031 to 0.036 for the cottages and 0.028 to 0.029 for the
    villages); variance-only passes (the golden is 2.28, 2.61 and 2.36 times the district route); the
    common-exposure subset, every filter and divide on a visible attribute (district, all points, nearest
    points, distance to the coast, size, the Coast district for the holiday-looking), misses by 24 to 71 per
    cent except the size peers in seed 3 (-4); truncation direction does not apply (overflow is logged as
    side waste and counted).
- **Candidate 2: the same reading with lets told from second homes** (the Larchmere enclave holiday lets;
  owner-used second-home villages on the coast and inland, emptier in winter and so steeper into July, as
  the lure a holiday-peer reading takes; the coast's new points lets and estates; same prototypes and seeds,
  the same output file). Killed at stage 1 on measurement for the same reason; the bracket it builds does
  not survive the width the noise needs.
  - The world: 148 mature points (the Coast district 30 villages, 14 let sites, 8 second-home hamlets and 12
    estates; the Town district 70 villages and estates, 10 second-home villages and 4 lodge sites) and the
    same 30 new points, the 13 holiday points lets. Lets fill at the half-term nearly as much as at Christmas;
    second homes fill at Christmas and hardly at the half-term (a winter response of about 3.3 to 3.9 at
    Christmas and 1.3 at the half-term, against about 2.3 to 2.5 and 1.9 to 2.1 for lets), so only the two
    responses together tell them apart.
  - The golden 236, 233 and 238 bins (truth 238, 231, 223); the family -5 to +2, -6 to +2 and -2 to +2 per
    cent of it; one sigma 8.9, 6.2 and 9.3 bins (2.7 to 3.9 per cent); per point a median spread of 2.4, 3.2
    and 3.1 bins needed and up to 4.6 to 7.9.
  - The bracket held in shape: the holiday-looking points pooled +28 to +39 per cent and the top-ratio peers
    +32 to +42 over the golden, the district -44 and the Coast district's ratio borrowed for the lake -31 to
    -33 under it. The rest: every mature point -48 to -52, the nearest 3 points -36 to -49, the distance fit
    -43 to -48, a flat 1.25 -41 to -43, a flat 1.5 +4 to +8, a flat 2.0 +100 to +103, the nearest point -53,
    -15 and -1, the size peers +3, -15 and -33, the half-term alone -1 to +1 (the back-test rejects it at RMS
    0.24 to 0.28, yet it lands on these new points, because none of them is a village or a hamlet).
  - The flat factor crosses the golden at 1.46 to 1.47, so 1.5 sits 4 to 8 per cent over it, inside any bin
    the noise allows.
  - The back-test: 0.057 to 0.065 for the nearest peers on the two responses against 0.35 to 0.36 for the
    district and 0.13 to 0.15 for the pooled holiday points, and on the off-district kinds 0.060 to 0.068
    against 0.62 to 0.64.
  - Determinism at the total: no rounding of 10, 20, 25 or 50 bins holds the family with one sigma inside a
    quarter-bin margin in any seed; inside the golden's bin sit a flat 1.45 to 1.55 at every rounding in
    some seed, the half-term alone at 10, 20 and 50 in every seed, the size peers in seed 1 and the nearest
    point in seed 3.
  - The eda6c8c screens: dispersion does not apply (the within-kind coefficient of variation is 0.022 to 0.040
    for lets and 0.044 to 0.063 for second homes); variance-only passes (1.77 to 1.79 times the district
    route); the common-exposure subset misses by 15 to 53 per cent except the nearest point in seed 3 (-1) and
    the size peers in seed 1 (+3); truncation direction does not apply.
- **The per-point requirement, measured on both.** Whole bins at each point need every defensible member of
  the family within a quarter-bin of the golden at 20 to 30 bins needed, about 1 per cent of the July
  forecast, which would take a within-kind ratio spread near 1 per cent and a weekly noise near 3 per cent:
  lockstep series. At the realistic 2 to 6 per cent and 8 per cent the members spread 2.4 to 3.2 bins.
- **The prototypes before the screen** (`p1.py` to `p11.py`) moved the parameters the same way and found
  the same wall: with the holiday points at 35 to 50 per cent of their bins in winter the totals were 30 to
  100 bins and one sigma 7 to 21 per cent; a beach-car-park kind made the two-response family split 62 to
  165 on one seed because a village's and a beach's winter responses coincide; a lets enclave among
  second-home lures with a mixed coast let the district route land by cancellation (the coast's villages
  over, the lake under).
- **Paper screens, not coded.**
  - The new points' ramp as households find them: FC04's station-maturity driver, task133's seed.
  - Each mature peer's July completed past its capacity from the peers that never overflowed: task168's
    driver.
  - The two Julys normalised for weather: a lever of 8 to 12 per cent on July fill, inside the bin the noise
    needs.
  - The school summer holiday's start: it falls within the same few days of late July in England in 2025,
    2026 and 2027, so no lever.
  - Deposits diverted from nearby mature points: the winter split carries into July, so no lever.
  - Dwellings times a kind's yield per dwelling: determinate per point only if every point captures the same
    share of its catchment, which is lockstep; with capture varying, the point's own winter level beats it
    out of sample.
  - The total July weekly fill in place of bins to add: a flat uplift lands, because the sum runs over the
    residential points too.

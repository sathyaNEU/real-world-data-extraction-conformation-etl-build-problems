# task177 design note

**Status: stage 1, drawn 2026-10-19, architecture 1 in a new world.** The seed FC48 world (drop-off recycling
bins) died at stage 1 on measurement before any card was filed (its record is kept below under `## Seed world`
and in `## Tried and rejected`). The redraw was handed the cell psychology-behavioral-science /
decision-making-computational-behavioral-modeling and searched it by prototype on 2026-10-19: goals as
reference points (A) and drift-diffusion speed-accuracy adaptation (E) died on measurement and on the library
test, a dozen more on paper, and the imposed-contact learning discount (F) held. The prototypes are in the
session scratchpad (r177/proto).

## Draw

| Item | The draw |
|---|---|
| Card | `cards/task177.json`, registered at the DRAWN commit through the round's serial lock |
| Pairing | `psychology-behavioral-science` (client domain), task type `decision-making-computational-behavioral-modeling` (serves Forecasting), objective Forecasting |
| World | Prairie Works Manitoba (fictional), a provincial employment and income assistance service; jobseekers contact it by phone or through its digital assistant, Ask Prairie Works, in the app and on the web |
| Decision | the March and April 2027 usage tier for Ask Prairie Works, ordered from the assistant's vendor by 12 February 2027 (`purchase_order_or_contract`); the head of contact services signs it (`line_manager_or_team`); the forecast comes from the behavioural insights adviser in the digital channels team (`policy_adviser`) |
| Call | the share of the contacts jobseekers start themselves in the eight weeks from 1 March 2027 that they start in the assistant, after the assistant-first weeks of 4 January to 28 February in which the upgraded assistant answers every call first |
| Shape | `02`, a forecast across the eight weeks (the headline share with each week's figures); the 25-criterion arithmetic is written at stage 2 |
| Decision type / unit | `quantity_figure` / `rate_or_share` |
| Mechanism | gap population then time; pattern none, decisive G16 (the learning model the record selects), G7 (the assistant-first window) and G17 (its profile interval) supporting; Gate G `method_or_model_selection`; strategy `forecast_method_backtest`; Layer 2 `forecast_uncertainty`, pattern `psychology-behavioral-science/decision-making-computational-behavioral-modeling/3` |
| Calibration / context artifact | none / other (the vendor's usage-tier order form for March and April; the assistant-first rollout plan is the governing document that files the dates and the routing) |
| Deliverables | `assistant_share_forecast_mar_apr_2027.xlsx`, `assistant_first_aftermath_note.docx` |
| People | Loretta Rodgers (head of contact services), Sabrina Ward (digital channels), drawn with `guard.py names --geo "Manitoba, Canada" --seed 177` |

**Data-native sentence.** Queue overflow sends phone-minded claimants to the assistant only in scattered
peak-hour episodes, so the record holds thousands of contacts a claimant did not choose but almost never a
run of them, and a learner fitted to the whole record, where they are about one assistant experience in ten,
back-tests well while weighing them like chosen ones.

**The library test.** The cell's cards are the textbook route: a reinforcement-learning model of each
claimant's contact-by-contact channel choices, compared on held-out choices (card 1), its parameters
recoverable (card 2), simulated to check it reproduces the behaviour (card 3). Applied as the cards state it,
with one learning rate, that route misses the share by about +49 per cent. The judgment beyond the cards,
which the data settle, is which experiences teach: a contact the claimant was sent to by overflow moves their
later choices about a fifth as much as one they chose (the record's split model beats one learning rate by
about 1,460 log-likelihood units and beats "redirected contacts teach nothing" by about 100; the outcome of a
redirected contact moves the next choice 0.112 against 0.075, a chosen one 0.631 against 0.263), and the
assistant-first weeks redirect every call. The judgment alone, without the learning model (next-contact
transitions after redirected contacts), misses by about -22 per cent; the two together give the golden.

**Measured on the prototype** (`f_forced5.py`, 20,000 claimants, twelve months, two contacts a month, overflow
on 2 per cent of calls, imposed contacts at a fifth of chosen ones, assistant resolution 0.50 now and 0.85 on
the acceptance test, the phone 0.88; seeds 1 to 4): truth 22.3, 22.3, 22.3 and 22.4 per cent (sigma of the
window's own draw 0.19 to 0.25 points); one learning rate +48.6, +49.5, +50.0, +48.5 per cent; redirected
contacts treated as chosen +54; as teaching nothing -30 to -31; no learning -42 to -44; a waiting cost on
redirected contacts +51 to +52 (and 1,224 to 1,882 log-likelihood units worse); a pooled last-four logistic
+10.4 to +12.4; a pooled first-order Markov chain +23 to +26; the same two split by route -32 and -22; the
split model (with or without perseveration) -0.8 to +2.0. Profile of the imposed learning rate: one standard
error moves the share about 0.37 points, the two-unit interval about 0.8. Individual heterogeneity in learning
rates or in channel preference (sd 0.25 to 0.5) moves the pooled split fit under 1 per cent. Claimants who
already met three or more redirects inside one eight-week span: 24 of 20,000.

**Guard (2026-10-19).** WARN only. `overuse.org_family`: a public employment service is honestly a
government agency, and no government-agency build on file turns on a learning model of its clients' choices.
`repeat.gate_g` and `overuse.gate_g` (method_or_model_selection, task269 among the last two): the decisive step
is honestly the selection of a learning model the record settles; task269's is a reliability decision study,
another pairing, gap and generator. `test.same_puzzle_older` and `test.same_driver_older` are answered by the
card's differentiation lines (task70, task104, task134, task168, task463, task501). The window's bans this
draw clears: shape 04 and 05, G6, G2 and G13, population_selection, decomposition_attribution and
composition_mix, research_desk, programme_officer and operations_director, and the round's own list.

**Sources, one line each.** Cards 1 to 3 of the task type give the family and the default path's route, never
the stump (stumping 1.3). task501's current driver pools two regimes and rebuilds a static matrix from the
season's own days; here that static rebuild is a wrong rung, and the imposed rate has to sit inside a jointly
fitted learning model. task148 censors a latent patience; no latent limit is censored here. task137 is a
contact-centre world on a repricing share; the decision, organisation, country and driver here differ.

## Seed world (FC48), set aside on 2026-10-18

**The seed world, as it stood.** Wave 8, new, Forecasting, seed FC48:
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

- **Redraw screen, 2026-10-19, candidate A: goals as reference points.** An activity-rewards programme raises
  its daily step goal (7,500 to 10,000) and pays a weekly reward for three goal-days (prototype `a_goal.py`,
  seeds 1 to 3, 3,000 members, 26 weeks, 13 forecast weeks). Killed on the library test and the round's G14
  ban. Truth 15,409, 15,150 and 15,762 weekly rewards (sigma 0.33 to 0.35 per cent); the share of weeks with
  three days at the new goal (default) -36.2, -36.3, -35.4 per cent; the current reward rate carried +78, +82,
  +76; the pile at the old goal read over every day (the card-literate route) -12.5, -12.3, -11.3 (stretch 0.44
  to 0.45 against 0.63 to 0.65 on days the reward was still in play, 32 per cent of days dead); the pile read on
  live days -2.4, -1.4, -0.8. The live-day rule leaves the forecast itself unchanged and fixes only the estimate
  of the stretch, an absolute split no column names (pattern E, G14); the band's carriage between two goal
  levels moves about 9 per cent on paper; the pile itself is what a card-literate reader looks for.
- **Candidate E: drift-diffusion speed-accuracy adaptation.** A selection test tightens its per-item limit
  from 10 to 6 seconds, an older 6-second version on another item bank in the record (prototype `e_ddm.py`,
  seeds 1 to 3, 2,000 candidates by 40 items, the 6-second boundary 0.75 of the unhurried one). Killed: at a
  70 per cent cut the truth passes 94.8, 95.4 and 93.8 per cent and truncating the current response times at
  6 seconds lands within 1.3, 0.8 and 1.4 per cent (mean accuracy 0.817 against 0.822: the slow responses
  truncation drops are the low-drift ones, so the totals coincide); only at a cut near the top does truncation
  miss (+26 to +29 per cent at a 0.75 boundary, +105 to +112 at 0.60), and there the lever is the DDM transport
  itself, the field's textbook route, on a tail share carrying 5 per cent relative noise; the old version timed
  out 1.9 to 2.2 per cent, so the censoring a careful fit adds is a negligible lever that card 3 catches.
- **Killed on paper the same day.** Hot-stove learning after an improvement (the card's learning model already
  updates only the chosen option, so the card lands; a lag-1 outcome logit sits near the golden over one
  quarter). Pooling titration answers whose offers followed the respondent's own earlier answers (the field
  scores each respondent's indifference point, which is the golden). Reference-dependent income targeting
  across a gig day (labour economics by taxonomy, as task157 found; a reduced form on own earnings lands;
  under 20 per cent on hours). A screener's criterion moving with prevalence (needs a gold-standard subsample;
  in range a regression on prevalence lands, out of range a fork). Every rate-by-state design carried to a new
  state mix (reference prices, the disposition effect, forgetting by gap, returns after a deferral, projection
  bias, streak breaks: honestly G14 or composition_mix). Notification habituation (task83's driver, rejected in
  task122's note). Peak-end follow-up (recognisable; lever about 24 per cent). Goal-gradient loyalty cards
  (lever about 4 per cent). Compromise and decoy menus (famous; past introductions land). The magnitude effect
  (amount as a covariate lands). Partition dependence in fund menus (the default fund dilutes it;
  identification only across employers). The description-experience gap in fare enforcement (past changes
  land). Bold against timid play under a stake cap (the pile at break-even plus a session simulation is the
  card-literate route, and players' time budgets reopen task148's censored-patience driver). A delivery promise
  as the reference point of learning (under 10 per cent on totals, a product-analytics home). A learner-share
  recruitment forecast (the analysis file's selection is a WHAT; a fatigue bend is G13).
- **F's own dead settings** (`f_forced.py`, `f_forced3.py`). With 1.4 imposed contacts per customer (six weeks
  at a contact a month) no learning lands within 1.4 per cent. With overflow on 6 per cent of contacts,
  redirects are 30 per cent of assistant experiences and the pooled reduced forms (a last-four logistic and a
  first-order Markov chain) cross the truth for imposed-to-chosen ratios of 0.25 to 0.40 (seed 1: -3 and -3 per
  cent at 0.35, -7 and -7 at 0.40); the draw keeps overflow at 2 per cent of calls (redirects about a tenth of
  assistant experiences) and the ratio near a fifth, where every pooled route misses by 10 per cent or more.

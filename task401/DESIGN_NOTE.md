# task401 design note

Architecture 5, drawn 2026-11-04. The number was handed out against seed RC07 (a supplier's January imbalance bill).
The seed's world could not carry an honest unbanned draw; architecture 1 (a frailty virtual ward against care home
closures, Epidemiology and Public Health) and architecture 2 (a canola hybrid against July heat, Economics and
Econometrics) died at stage 2, architecture 3 (a GB energy supplier's satisfaction fall, Marketing and Consumer
Research) was spent at stage 4, round 2, on an ask's unfiled re-attribution, and architecture 4 (a river's winter
ammonia failures below a water recycling centre, Physical and Environmental Sciences) was spent at stage 4, round 1,
when the judge's blind derivation reached the call and every ask figure (`## Tried and rejected`, the card's
`lineage`). One architecture per world: architecture 5 moves to Psychology and Behavioural Science, an English leisure
trust's membership base, a new dataset and a new shell.

The world: Wrenford Leisure Trust, an invented charity that runs Wrenford Borough Council's nine leisure centres under
an operating contract, with about 25,000 members paying monthly by Direct Debit. Members who joined before the January
2023 tariff migration sit on legacy tariffs (about three in ten by 2026); everyone since is on the 2023 tariffs, which came
with the Rewards scheme (points for visits, spent on guest passes, cafe credit and class bookings). To close a budget
gap the trust made five changes between January and February 2026: a daytime class timetable consolidated at the
centres older members use most (12 January), the Rewards scheme closed (1 February), every legacy member written to
with the current terms at an unchanged price (letters posted from 2 February), a member care team calling members with
no visit in three weeks (from 16 February), and shorter evening and weekend hours at two centres (from 23 February).
Cancellations jumped in February. The council's contract review in April asks the trust which change its 2026-27 plan
reverses, and the head of membership has the trust's extract of 16 March 2026 to answer from.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task401.json`, architecture v5, registered after `guard.py check` at WARN.
  `overuse.objective`: the slot's objective is fixed by its number. `repeat.gate_g` and `overuse.gate_g`
  (`decomposition_attribution` repeats task402 and task403): the call assigns the year's cancellations among five
  changes made inside six weeks, and the stump is that the count to date assigns them the wrong way round, so the
  mechanism is honestly an attribution; `forecasting` would name the projection, which is the decisive step, not the
  call. `test.same_driver_older` against task122's lineage is answered by the card's differentiation line (nothing here
  is re-attributed), and so is task274, the nearest family member on file (below).
- **Pairing:** Psychology and Behavioural Science (client domain), task type `mediation-moderation-process-modeling`,
  which serves Root-Cause Analysis in the taxonomy; objective Root-Cause Analysis; shape 18 (the five filed changes are
  the hypotheses, each with its own in-place date and reach).
- **Strategy:** `maturity_censoring`, gap time first (the twelve months from 2 February 2026 are six weeks observed at
  the extract, and one change's cancellations sit almost wholly in the unobserved part), objective second (the count to
  date answers a different question from the year's count). Pattern none; generators G13 horizon mismatch (decisive),
  G3 record versus operation (the register lists as active a member who has stopped coming), G12 absence of record
  versus record of absence (no cancellation yet is not no cancellation caused). Layer 2 family `estimation_fit`. The
  window's three live cards hold `causal_design`, `time_semantics` and `composition_mix`.
- **Data-native sentence:** a member who stops coming keeps paying by Direct Debit for about three months before
  cancelling, so the members the Rewards closure lost in February sit in the visits record as members with no recent
  visit while the register still lists them as active, and reach the cancellations only from April; the legacy terms
  letters prompted members who had stopped coming long before to cancel within days, so their cancellations sit inside
  the extract's six weeks, and some of them would have cancelled later in the year anyway.
- **Abstraction sentence:** two changes made in the same week reach their outcome on opposite clocks, one at once and
  partly brought forward from later in the year, the other only after its units have sat idle for months, so the count
  to date ranks them the wrong way round and the idle stock, set against the same date a year earlier and converted at
  the earlier year's rate, puts them right. It is not writable against the nearest builds: task274 (shipped 11-02)
  completes units inside a recorded programme stage through that stage's hazard to size one randomised offer, with no
  rival and no unmarked pending state; task133 converts a dormant residue whose young units only look dormant (a stock
  forecast, no attribution); task402's architectures pair a unit's consecutive events or lose cases when an actor's
  assignment lapses; this slot's architecture 3 standardised a mix behind a satisfaction fall.
- **Same-puzzle and library tests:** gap, pattern and decision type repeat no build in the last twelve; gap, pattern
  and Gate G repeat only task122's lineage, differentiated. The golden is no named correction: the field's methods for
  the deciding quantity, a before-and-after or difference-in-differences on each change's cancellations and a mediation
  model read on the outcomes observed so far, sit at rungs 0 and 1 and both name the letters; no textbook names "count
  the members who stopped coming and still pay, against the same date a year earlier, and convert them at last year's
  rate".
- **Layers:** Layer 1 is the trust's own record-keeping: access-control entries in local time across the March 2025
  clock change with gate re-entries minutes apart and a turnstile outage week at one centre; a membership register whose
  tariff codes were renamed at the January 2023 migration; cancellation requests from three channels (online form,
  front desk, telephone) with request, notice and effective dates and duplicate requests; letters posted in batches over
  a week with returned mail; a care-call log keyed by membership number as text with its leading zeros dropped; a 2025
  and a 2026 extract of the register with different column names. Layer 2 is the cancellations still to come from
  members who have stopped coming, timed by the lag from last visit to cancellation.
- **People** (`guard.py names --geo "United Kingdom, England" --seed 401 --n 30`, taking the first three names in draw
  order that fire no people rule and that no earlier architecture of this slot used): Aimee Williams (the trust's head
  of membership, who owns the answer to the council), Marilyn Patel (membership systems manager, who keeps the register
  and the extracts), Abdul Norman (the council's leisure contract manager). The prompt names no one.
- **Furniture drawn against the live window** (read off `guard.py check`): forum `customer_or_counterparty` (the
  council is the trust's contracting client; `committee_or_panel`, `trustees_or_governors` and `executive_team` are held
  by task400, task402 and task403), forcing event `period_close` (the 2025-26 year end sets the 2026-27 plan;
  `vote_or_meeting` and `season_or_peak` are held), organisation family `nonprofit_or_charity`, role family
  `operations_director` (`product_manager` is held by task403), context artifact `filed_standard` (the contract's
  performance schedule).
- **Sources:** synthetic throughout, built to the structure of the records it imitates; every file's source, date and
  licence goes into `metadata.json` at stage 3. Invented names checked: no place or organisation named Wrenford was
  found (the nearest is Wrenbury, a Cheshire village).

### Documented levels

- **The lag from last visit to cancellation.** DellaVigna and Malmendier (2006, "Paying Not to Go to the Gym",
  American Economic Review 96(3)) put the average at 2.31 months over every canceller. The prototype splits cancellers
  into members who quit while still coming (cancelling within days of a visit) and members who drift away, whose lag
  runs about three months (gamma, shape 6, mean 13 weeks). All cancellers together then show a median of 2.5 months, 38
  per cent within a month of their last visit, and a mean of about 4 months that the legacy members' long tail raises;
  drifters cancel within a month of their last visit 0.5 per cent of the time. The spread of the drift lag is a
  modelling choice the source does not publish, and the design was moved until it held at this width (Tried and
  rejected, 2026-11-04).
- **Attrition.** About 3.1 per cent of members a month on the 2025 run, a modelling level; no single published UK
  figure is cited.
- **The closure's effect.** About one 2023-tariff member in fourteen stops coming, most within a fortnight of the
  closure (1,208 to 1,329 more members with no visit in four weeks at the extract than without it, seeds 1 to 3),
  cutting that group's visits by 4 to 6 per cent against the same weeks of 2025. Loyalty programme termination lowering
  patronage is documented (Melnyk and Bijmolt 2015, European Journal of Marketing 49(3/4)); the size is a modelling
  choice. The letters prompt about a quarter of legacy members who had not been in for a month or more to cancel within
  a fortnight; the size is a modelling choice.

### The four go/no-go screens

Measured on the clean truth over 20 redraws (seeds 1 to 20) at the screened setting, `scratchpad/t401/a5/screens2.py`
on `proto5.py` (the prototype with weekly visit totals by reach; its random streams match `proto3.py`), extract 16
March 2026, drift lag mean 13 weeks at shape 6. Truth: the Rewards closure's twelve-month cancellations 712 to 844,
the letters' 91 to 158, the care calls -312 to -252, the timetable -39 to 54, the opening hours 18 to 106; the closure
first in 20 of 20.

1. **The lever against the rivals' estimates:** the golden (members with no visit in the 28 days to the extract on the
   2023 tariffs, in excess of the same date of 2025, times the share of last year's such members who cancelled in the
   following ten months, plus the closure's excess so far) beats the largest rival estimate a careful solver computes
   from the pack (each change's difference-in-differences or year-on-year count, and the linear year-scaling of the
   small changes) by 1.34x at the lowest and 2.77x at the median, 1.5x or more in 19 of 20.
2. **The golden's own method holds the call:** all 24 specifications (no visit in 3, 4 or 5 weeks; last year's
   conversion from the reach or from every member; over ten or twelve months; against last year or against the legacy
   members) name the closure in 19 of 20 redraws; the exception (seed 3, 0.89x on the 3-week, every-member, ten-month
   variant) is not a shippable seed.
3. **No easy completion and the first look lands wrong:** the first-look reader (cancellations in each change's own
   reach, after against before at 2, 4 and 6 weeks and lags of 0 to 8) names the letters in 20 of 20, and the same
   reader net of the same weeks of 2025 in 20 of 20; read on visits instead, the step is 4 to 6 per cent and shared with
   the timetable's and the opening hours' reaches, naming the closure in 4 of 20 and naming no cancellations at all.
   The flexible crackers (every change scaled to the year; the closure scaled and the letters kept as a one-off, on
   year-on-year or difference-in-differences counts) land wrong in 20 of 20 each.
4. **Literal execution:** the filed WHAT (a change's cancellations are the requests in the twelve months from its
   in-place date that would not otherwise have been made, against the same weeks of the year before) executed on the
   cancellations to the extract, by difference-in-differences and by year-on-year counts, names the letters in 20 of 20;
   the golden needs the cancellations still to come, which no filed sentence asks for.

## Tried and rejected

- 2026-11-03, the seed's world (RC07, a supplier's January imbalance bill against plant trips and low wind), every
  candidate screened before the card. The trips' effect on the supplier's own imbalance volume at the system price is
  settlement accounting: each unit's metered shortfall against its notified output in the window before the desk can
  re-trade, priced per settlement period, reconciles exactly to the bill, so nothing is left to decide (rule
  application). The price the supplier would have faced without its own units' trips re-runs the system's price
  formation on the changed path, task398's spent insight in other nouns. Netting the desk's replacement trades out of a
  trip's cost is the same insight again (the cause owns the response it triggered). Which settlement periods a trip owns
  (gate closure, the share of an interval) is a market rule or a time-semantics read, banned as decisive. The cost
  spike's drivers identified from interval data need a driver the settlement data does not meter, and in this market
  every driver is metered. Dual imbalance pricing makes the portfolio's net position matter, but executing the price
  rule on the with-and-without positions is rule application. The honest strategy, `decomposition_attribution`, and the
  seed's forum (the board) are both held by task398 in the window. Moved, per `CLAUDE.md`.
- 2026-11-03, other moves screened and set aside before this draw: gas turbine inlet icing in freezing fog read against
  temperature (the winter measures on the table name the mechanism, so a reader checks each one's conditions and lands
  it; two cheap routes); a groundwater nitrate rise read against travel time through the unsaturated zone (task202's
  reach-the-receptor insight in other nouns, and the field's first move); a bathing water's sources separated by marker
  decay in transit (task202's reach and task248's transit loss); selective in-migration behind a widening mortality gap
  (task68's entrants and task134 v2's newcomers, and the prior-diagnosis read lands the decision without it); depletion
  of the frail by a winter's deaths before an intervention's evaluation (dead on lever at realistic excess mortality, as
  task173's screens found for mortality displacement, and its frailty proxy forks the expectation); the Will Rogers
  stage migration (the field's stage-specific comparison collapses into which stage field to read, data semantics);
  attenuation by a mediator's or a predictor's unreliability (task262's insight); regression dilution of a risk factor
  in a disparity decomposition (task262 again); a funnel's downstream rate falling when an upstream filter loosened (the
  end-to-end funnel is the field's reflex); a two-stage complaint escalation's selection (the per-complaint view lands it);
  a mode or non-response shift in a satisfaction tracker (task121 v4's linkage and halo).
- 2026-11-03, prototypes before the card (`scratchpad/t401/proto1.py` to `proto3.py`, expected values with Poisson draws):
  winter-only counts in a city of 600,000 left the default and the golden overlapping across draws (default 5th to 95th
  percentile 23 to 179, golden -38 to 119), so the build runs at integrated-care-system scale over October-to-September
  years with the closures in the year between the baseline and the pilot; there the default's expectation is 912 (spread
  208) against a golden of 392 (spread 215, truth 389), and the trend-adjusted golden forms agree within a median of 6.4
  admissions once the framework files the comparison; without the comparison filed, the no-trend form differs from them
  by a median of 77 (a fork the framework's comparison sentence closes, a WHAT naming no method).
- 2026-11-03, architecture 1 dies at stage 2 on the coordinator's realism check, before any data was cut. Set to published
  English levels (a care home resident aged 80 and over about 0.70 to 0.75 emergency admissions a year, community
  residents by band 0.24 to 0.58, a same-age ratio near two, not the prototype's five), the composition lever is about
  113 admissions for the 440 Core20 residents the closures moved (sd 26), against draw-to-draw spreads of 202 in the
  default and 214 in the golden on a one-year baseline and about 160 on three years (`scratchpad/t401/proto4.py`, 400
  draws). A bar at the midpoint separates default above from golden below in 22 per cent of draws (27 on three years);
  900 residents moved gives 41 to 51 per cent and 1,400 gives 58 to 72, and 1,400 is two fifths of Core20's care home
  places in one system closing in a year, which no honest care group failure produces. A larger 80 and over population
  scales the spread with the lever, and a bar nearer the truth only moves the coin flip. The stump was the noise. Re-rooted.
- 2026-11-03, the redraw's other candidates, set aside before the card: regression to the mean of units chosen on a
  noisy outcome (task130 v3 landed it; task149 and task174 rejected it on that lineage); a satisfaction fall read against
  the conditions each respondent met, or a tracker's mode or response shift (task121 v4); a storable good's purchases
  pulled forward before an announced price rise and paid back after (the pre-rise spike is the pack's largest movement
  and announces the step); a distributor's orders falling as channel stock is drawn down (sell-through is the field's
  reflex and lands it); a local policy confounded by a common shock loading on each unit's exposure (the council
  furniture is banned in the window and the exposure needs data no operator holds); transformer insulation ageing under
  new loads (electricity is spent, task129, task196, task201, task303, and F6's 46 already holds a rate stationary in a
  constructed exposure); in the crop world itself, a hybrid placed on clubroot or hail-struck fields (a lab result or an
  adjuster's claim names the field, readable), and a hybrid whose own later flowering met the heat (`crop2.py`: a three-day
  shift moves the season-long panel only 3 to 5 per cent, and the forward step then needs a climatology fork).
- 2026-11-03, prototypes for architecture 2 (`scratchpad/t401/crop1.py`, `crop3.py`, ten weather draws each, the
  hybrid's own effect nil and equal phenology): with most of the hybrid's seed late by 8 to 14 days, the season-long
  panel files minus 9.1 per cent (sd 9.8 across weather draws), farm-by-year effects minus 9.3, a linear seeding-date term
  minus 7.0, raw 2026 means minus 11.6, the flowering-window exposure minus 0.1 (sd 0.9), its variants (thresholds 28 and
  31 C, windows 14 and 22 days, 490 and 550 heat units to flower) minus 3.5 to plus 0.5, and fields seeded on the same
  days on the same farm minus 0.6 (the same insight by matching). The spread across draws is the weather's: the pack's
  July heat wave and seed delay are set by design, never picked from draws.
- 2026-11-03, architecture 2 dies at stage 2 on its own ladder (`generator/ladder.py`, seed 4012026, measured at commit
  7d3a3cd), before any data was cut. First, the golden's own method forks the main call: the flowering-window variants
  land +2.1 (28 C), -2.5 (31 C), -12.0 (a 14-day window), +3.4 (a 22-day window), -8.2 (490 heat units to flower) and
  +4.9 (550 units) against the 5 per cent bar, so two agronomically defensible variants drop the hybrid and four keep
  it; filing the window or the heat metric would name the decisive step, and the generator cannot close the spread under
  realistic catch-up (a 17-day seeding gap became a 6-day flowering gap). Second, the stump rests on a functional-form
  choice: the default path's own rung 4 already rebuilds seeding dates from the seeder's logs, and every flexible form of
  that variable then lands the golden (seeding-week bins +3.6, a cubic +4.4, same-day matching +9.3); only a linear term
  stays wrong (-10.1 in the season panel, -8.3 with farm-by-year effects), so Gate F would rest on the solver choosing a
  straight line. Spent; one architecture per world, so the crop and weather world is closed to this slot. Re-rooted at
  architecture 3 in another client domain, world and dataset.
- 2026-11-03, architecture 3's draw, candidates set aside before the card. In the never-built satisfaction cell, the
  client card's moves (Shapley shares, a Net Promoter change's multinomial error, penalty against reward, loyalty read
  on later behaviour) are reflexes, and reading a fall on the conditions each response was made under is task121 v4's.
  A broadband provider's speed promise against delivered speed died on the regulator's own reflex (the share of plan
  speed delivered is the standard metric). The energy quote mechanism in the supplier's base-wide relationship tracker
  carried 0.54 points (1.35 with 2025's joiners using a fifth more) against a fall whose draw-to-draw spread is 0.66
  (`scratchpad/t401/a3/proto_e2.py`), architecture 1's death in other nouns, so the build runs on the six-month
  new-customer tracker. In the concentrated form a first harness with the platform's own effect at 1.3 points left the
  golden's 10 and 20 per cent flags (0.98, 1.78) under the residual (`proto_e3.py`); at the platform's realistic small
  effect the standing forms clear it (`proto_e4.py`). Other cells screened: education multilevel (the client's three
  cards are reflexes; teacher reassignment and special-needs assessment waits fail screen 1 or repeat the actor family),
  health equity (an inhaler switch run practice by practice is task400's staggered rollout; discharge after a missed
  appointment repeats task402's broken-off cases), pollution source attribution (every wind, tide and capture-zone route
  is task202's reach), water network reliability (the isolation extent per burst is one group-by; transients read
  through topology sit beside task303), the human factors cells (the pairing is barred against task400), and
  interpretability (ruled a backdrop at task129 v1).
- 2026-11-03, stage 2 on architecture 3, three cuts. (a) The first world set the first Direct Debit from the quote, so
  the review rise was a near-copy of the gap and a solver asking why payments rose walked to the quote; the payment is
  now set from the meter point's industry quantity at registration, and the Direct Debit change books 0.35 points and
  names the platform (`## Ladder`, R2b). (b) A Direct Debit policy document stating that rule was drafted and dropped:
  its sentence on industry quantities would send a reader to set quotes against quantities, and the golden never needs
  it. (c) The contact centre ask and its two call logs were cut for budget; the contact rival stays on the tracker's own
  contact question. The asks' first devices as drafted (stale legacy status, re-runs keyed on the legacy reference,
  withdrawals) were each executable from the cutover plan's and the asking sentences' own pins, so they were re-sited
  onto an erroneous-transfer return, a reload chain with a pilot twin, and a gas registration raised under its own
  reference.
- 2026-11-03, stage 2 on architecture 3, the full includer (precut FAIL: one primary per ask). The coordinator's candidates
  were screened against the full includer: (a) Ask B, an account whose gas was removed between its first load and its
  reload: the full includer that walks the chain takes the last load's row, fuels with its week, and keeps the block, and
  the sentence that closes the fork (the fuels that load carried) makes it a work order; (b) Ask C, broker switches
  registered on the broker's lead reference: noticing the unmatched reference and joining on the prospect is one act, and
  every quote under a broker's lead is a broker quote, so nothing goes wrong after the notice; re-sited onto a broker sale
  re-quoted by the phone team after the registration; (c) Ask A, two-rate registers alone: a work order once the plan
  files day and night together; the device is the register set changing at an exchange, and gas has no register. Also set
  aside: split-fuel legacy accounts merged on load (one platform number on two rows, and the filed unit, the account the
  platform holds, makes it a work order); a requested supply start on legacy sales (the industry registration date in the
  quantities fixes it in one act); fuel add-ons across the migration renumbering (the solver who landed the call already
  built the crosswalk).
- 2026-11-03, stage 2, the full includer at 36 of 58 (62 per cent of the ask weight, 79.1 on the call): one second device
  per ask on its own block left a full includer and an on-call cracker pairing near 62. Widened: Ask A gained a change of
  occupier on the same meter points (the primary's own repair keeps the leaving account), Ask B's returned accounts take
  both fuels, Ask C's re-quotes reach every channel; the full includer keeps none of the 58.
- 2026-11-03, stage 4 round 1 (judge NOT_DETERMINISTIC and SOLUTION_WRONG, SEND_BACK light on the workbook asks alone, main
  call forced, Gates G and H passing; reader clean on the main call): Ask B's second device, the 410 accounts loaded and
  returned to the legacy platform, died to its own WHAT. Filing what counts as moved (the new platform billing the account
  at the end of 2 November 2025) closed the judge's fork 1 and made the returns a work order: with the sentence filed and
  nothing else changed, the full includer keeps 16 of 18 Ask B figures (`scratchpad/t401/fix/remeasure_b.py`). The returns
  stay as a hazard; the second device is re-sited onto 389 accounts the legacy platform took back during 2026 on a change
  to prepayment, where the repair the sentence invites is right before the close and wrong after it (the full includer
  keeps 0 of 18).
- 2026-11-03, stage 4 round 1, the Gate A anomaly: the change-of-occupier branch drew the leaving account's supply start
  without reference to its closure, so two Closed accounts began after they closed and took their meter points from the
  live occupiers (Eastern and London one account short under the golden's own rule). The leaving account's start now
  precedes its closure, asserted over every account. Fork 3 was closed by "no withdrawn registration counted" rather than
  by dating the boundary in the asking sentence (shorter, and true whatever the date), with every withdrawal now dated
  before the start it requested, as switching allows.
- 2026-11-03, stage 4 round 2, architecture 3 spent. The round-2 judge returned NOT_DETERMINISTIC, SEND_BACK (narrow), on
  the switches table: "credited to the sale it was registered on", read word for word, takes each registration's
  quote_ref, and 596 Phone registrations name a quote dated 2 to 10 days after the registration; the golden moves each to
  the prospect's latest quote on or before it, a rule no file states, and for 94 of those prospects latest against
  earliest moves about 20 cells. The literal ask executor in checks.py had carried the re-attribution as though it were
  the field's own value, so it never saw the fork. Every round-1 finding closed, and the main call held in both rounds
  (forced and reproduced; Gate F good; Gate G analytical_non_defect; Gate H analytical), but the judge noted that
  Critical Component 2's "more than half" depends on the cut (a binary covered split puts 14 per cent of the fall on the
  quote mix, five bands 60, eight bands 85, the kinked model 75). A second round without APPROVE spends the architecture
  under the round-1 ruling; the slot re-roots at architecture 4 in another domain, world, dataset and shell. Lessons: a
  literal executor takes every field at its face value, so a golden that overrides a field's own link (a reference, a
  date, a status) carries a filed WHAT or the data are regenerated so the face value is the golden; and every quantity
  the write-up states for the main call holds at every natural granularity of the comparison, or is stated so it does.
- 2026-11-03, architecture 4's draw, candidates set aside before the card (four go/no-go screens, `scratchpad/t401/a4/`).
  The strategy window (binding_constraint, causal_design and decomposition_attribution held by task399, task400 and
  task402) bars the natural attribution labels, so each candidate's decisive move was labelled before it was priced.
  (a) An online retailer's checkout conversion fall booked to a checkout release, caused by a collection partner
  withdrawing urban points while adding as many in suburbs (`proto1.py`, `proto2.py`, 20 redraws): it fails screens 2
  and 3, since the access effect acts only on latent collection-preferring shoppers through a continuous distance, so its
  share runs 0.84 to 2.50 points across defensible exposure forms and the release's residual -0.62 to 2.67, and it fails
  the swap test (collection points read the same as clinics); it also sits beside task129's surroundings exposure and
  task399 v3's supply behind a journey, and task177 had called a nearest-locker reading a replay. (b) Opportunity to
  learn in a primary trust's mid-year maths tests, a new scheme's sequence placing tested topics after the test date:
  an intrinsic fork, because the scheme's sequencing is itself a counterfactual cause of the measured spring fall, so
  the default's "the scheme" and the golden's "the sequence against the test date" name one candidate. (c) A school
  trust's illness absence driven by classroom ventilation cut to save energy: at published levels (about 0.5 to 0.9
  points of absence per 1,000 ppm) the lever is a fifth to a half of the rise. (d) Deploy-spanning journeys breaking
  in-flight checkouts: task129 v1 spent the first-use-after-a-version-change shape. (e) Split shipments across
  fulfilment centres: task175's seed and task277's reflex. (f) Tampered HGVs read from roadside remote sensing: task202
  screened it. (g) Storm overflows against the load apportionment model: the overflow record is the zeitgeist's first
  check, and the move is attribution. (h) A charity upgrade appeal's anchored figure, a norm boomerang and a goal
  difficulty gap: the levels are not documented, or the gap is architecture 3's family. (i) Composition designs in
  every cell: this slot has spent two (architecture 1's closures, architecture 3's mix standardisation).
- 2026-11-03, architecture 4, stage 2: the caustic clean-in-place excursion drawn at the card (pH above 11 for twenty
  to forty minutes) breaches the consent's "pH of any sample ... not more than 11" in the dairy's own record, so a
  careful reader catches a breach by reading a condition (rule 3, a field reading deciding). Redrawn to acid whey run
  to the drain on evenings after a missed collection: an oxygen-demand shock at pH 6.1 to 6.4, inside the consent.
- 2026-11-03, stage 2: whey evenings on Thursday to Sunday only put every exceedance day on Friday to Tuesday, a weekly
  hole one tabulation finds. Spread to every evening but Wednesday's (the composite's night); no weekday now holds
  above three tenths of the days.
- 2026-11-03, stage 2: the morning-after oxygen sag alone in the historian (0.05 to 0.35 mg/l with the blowers flat
  out) marked the shock days at the works in one query. Given twins of the same shape (the control's night-load sags
  after go-live, storm flushes before), so under half of the days in any of four sag queries are exceedance days.
- 2026-11-03, stage 2: the dairy's pH drawn as a clipped normal piled readings at the clip (6.60) and its gamma
  replacement reached 11.9, a visible breach. Replaced by a smooth distribution held under 10.3.
- 2026-11-03, stage 2, asks: homes connected per quarter (flats behind one lateral) is a device whose discovery is its
  remedy (the addressing register lists the homes), and no second device of another family stood on it without a filed
  sentence naming it, so the full includer kept 12 of 12. Dropped with the inspection record and the addressing
  register. The first trade effluent set handed the cracker both devices (a meter register listing each exchange with
  its final and initial reads beside the multiplier it opens the file for; the scheme's "dated by its collection"), and
  suspended solids moved under one bin for three dischargers. The multiplier moved to the consent's metering columns,
  the exchange reads into the reads file, the dating left to the WHAT ("collected in the charging year"), solids
  ungraded. The first energy set named TB1 on MCC 7 in the meters sheet, handing the new blower to the cracker; the
  board is now listed without its load and the shutdown works record names it.
- 2026-11-03, stage 2, the coordinator's ruling on the first rebuilt ask layer: the blowers' transformer change shared
  its file and its question with the new blower's board (a reader opening the shutdown record for MCC 7 reads both rows),
  was marked on the reads sheet (a site read and an "as at" note), was fixed by one swapped multiplier, and sat in D2
  with the trade effluent exchange; the full includer kept 18 of 18. The report date against the collection date was
  caught too (the scheme's emptying sentence pointed at the round sheets, the laboratory column is honestly named and the
  label is the join): 15 of 15. The blowers' electricity was dropped: every fact its golden needed had to be stated, and
  once stated its fix was a swap. The ask now carries one primary per family, P1 the exchanges (D2) and P2 the
  two-bottle composites weighted by the samplers' logged volumes (D6); charges came out because they sit in both blocks.
- 2026-11-03, stage 2: two-bottle composites at one week in ten moved three strengths under one bin (the laundry's and
  the bottler's suspended solids under a plain mean, three under the second bottle dropped). Raised to about a third of
  weeks with the night bottle at 45 to 65 per cent of the day's strength; every wrong reading now moves every strength by
  3 bins or more.
- 2026-11-04, architecture 4 spent at stage 4, round 1: the judge's blind derivation reached the call and every ask
  figure. Every free gate had passed, precut was clean, the leak reader found no decisive-step sentence, and the judge
  returned DETERMINISTIC with a wording FIX_NOW and Gate F "moderate to good"; but its derivation, written before it
  opened the graded blocks, landed the call and all 15 ask figures in 26 tool calls. The works' hourly final-effluent
  ammonia jumped to 10 to 17 mg/l from midnight on every failure day (against 0.7 to 1.0), the spikes aligned one to one
  with the discharger's evening pH dips in its own fifteen-minute monitor file (a file the pack carried for that
  discharger alone; 38 of 38 such evenings were followed by a failure day), and the prompt's chart sentence ("tracing the
  winter's exceedance days from the river down through the works to whatever sets them off") announced the trace. The ask
  fell the same way: the scheme's filed WHAT ("the strength of a composite sample is the strength of the effluent it
  holds") beside the sampler log's volume column made volume-weighting the bottles the obvious move. The deeper cause: a
  graded count that holds under every operationalisation needed a clean, short, visible alignment, which is exactly what
  one look finds, so the stump sat in finding the signal and determinism and difficulty pulled against each other.
  Lessons carried to architecture 5: the first-look reader (the outcome at its finest grain beside every candidate's own
  record, aligned by date and lag, plus a before-and-after on each dated change) is coded and must land the wrong call;
  every candidate's evidence sits in records all candidates share at one grain; the prompt names the WHAT, never the
  route; a filed WHAT never names the property its ask's remedy needs while the column that supplies it ships.
- 2026-11-04, architecture 5's draw, cells and candidates set aside before the card (screens in `scratchpad/t401/a5/`).
  Cells: workload-fatigue-shift-analysis is barred by `ban.pairing` against task400 (human factors on root-cause);
  funnel-journey-analysis registered to task403 at 01:15Z the same day (shape 09, `executive_team`, `product_manager`, a
  price change booked for a subscription conversion fall), so it, those axes and any price-change rival are kept clear
  of; interpretability (directly or through the nonprofit and audit house domains) reads as a backdrop on every world
  tried. Mechanisms screened on paper, each with its reason: an age-matched comparison against units' life-cycle curves
  (the pre-trend check and unit trends are reflexes); a remedy targeted at members already lapsing (confounding by
  indication is a reflex once the targeting is read); a change's harm reaching the comparison units through shared
  demand (task500 v2's spillover through a link); a timetable change breaking members' habitual slots (architecture 2's
  dated shock meeting each unit's own phase); a detector's precision falling with prevalence (the swap test fails);
  separating two same-day changes by a dose rebuilt from records (task129 v1 and task129's surroundings); an
  instructor's departure breaking classes (task402 v1's lapsed actor); a consumable's stock running out unit by unit
  (task50's rotation); members leaving at a contract's end (a column); a reward's withdrawal read on the dose alone (the
  dose test lands it whenever its cancellations fall inside the window).
- 2026-11-04, architecture 5's prototypes (`proto1.py` to `proto4.py`, `screens.py`, 20 redraws each): a permanent visit
  loss after the Rewards closure kept producing lapses after the cut, which no snapshot can count (the golden reached a
  third of the truth); with the closure in January its lapsed members were harvested by the February letter, so its
  in-window effect was 550 of 870 and the two causes tangled; with disjoint reaches and a 1 March cut the golden's figure
  moved with the inactivity rule (an eight-week rule cannot see five-week-old lapses), closed by the contract's 28-day
  active-member definition; a Direct Debit notification to every member put part of the letter's spike inside the
  closure's own reach, so the mixed extrapolation landed on the closure in 15 of 20; the legacy terms letter (legacy
  members only, price unchanged) restored every screen. The price rise first used for the letter was dropped for task403's
  price-change rival in the same wave.
- 2026-11-04, architecture 5's screens re-run before the card (`screens2.py`, 20 redraws per setting): the prototype's
  drift lag (mean ten weeks, the published 2.31-month average, at gamma shape 14, a spread of a quarter of the mean)
  held the mixed-extrapolation cracker (the closure's count so far scaled to the year, the letters kept as a one-off) in
  19 of 20 only by its tightness: at shape 10 that cracker named the closure in 10 of 20 and at shape 6 in 19 of 20,
  and the published average is taken over every canceller, members who quit while still coming included, so the drift
  path's own lag runs longer and wider than the prototype had it. At the 23 March extract a three-month drift lag at
  shape 6 still let the cracker in 3 of 20 (7 of 20 at 13.7 weeks and shape 5). Moved the extract to 16 March with the
  three-month drift lag at shape 6, which holds every screen (`## Draw`); at the 16 March extract the 23 March
  setting's tight ten-week lag left the golden's own variants on the call in only 18 of 20.
- 2026-11-04, architecture 5's personas: the drafted card's three people were not in the seed-401 draw; redrawn from
  `guard.py names --seed 401 --n 30` in draw order, skipping the names that fire a people rule (Harry, Patricia, Hayley,
  Raymond and five more first names on older builds) and every name this slot's architectures 3 and 4 used.

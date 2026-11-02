# task183 design note

Architecture 2, a re-root (2026-11-02). Architecture 1 (Tamsin Valley Electric's underground cable program) is spent on
measurement and stays delivered on the portal as it shipped; its identity sits in the card's lineage. The objective and
the number are kept; the world, the dataset, the generator, the shell and the decisive step are new.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task183.json`, architecture v2, registered 2026-11-02T08:25:18Z after
  `guard.py check` on the filed card (no BLOCK). v1 moved into `lineage` with its fate and its shell into
  `lineage_shells`.
- **Pairing:** Energy Systems & Utilities, task type grid reliability and outage analysis (serves RC and AD),
  objective Anomaly Detection & Diagnostics. Shape `other` (criteria arithmetic in `## Ladder`); decision
  `pick_one_of_n`, answer a named main-line section. Question form `where`.
- **World:** the City of Pawnee Ridge Electric Department (Nebraska, a fictional city-owned distribution utility).
  Feeder 14 leaves Westside Substation at 12.47 kV and runs a three-phase main line 15.8 miles into farmland: 336.4
  ACSR (Linnet) through town and the Elk Creek woods to mile 3.6, 1/0 ACSR (Raven) beyond. Line recloser R1407 at
  mile 1.9 tripped through 2026, mostly two-phase trips on windy days, and members on the far laterals complain of
  blinks; the department's January 2027 patrol walks one main-line section before the spring wind season.
- **Mechanism:** gap rule (no filed sentence says how a fault is located), pattern none, generators G2 decisive (the
  recloser's locator works at the line grain with one conductor's impedance; the location needs the segment grain), G16
  (the method the line's own structure entitles), G3 (the recorded location against where the fault is). Gate G
  `method_or_model_selection`; strategy `grain_or_unit`; calibration `gold_standard_subsample` (the crews' found
  locations, every one on the 336.4 stretch, where the locator's setting is exact).
- **Furniture:** forum `operations_desk` (the department's operations desk issues the patrol order), forcing event
  `season_or_peak` (the patrol before the spring wind season), organisation `local_government`, role
  `capacity_planner` (system engineering writes the order), context artifact `filed_model` (the protection
  coordination study), opening `question-first`. Personas drawn with `guard.py names --geo "United States" --seed
  183`: Debbie Kline, Lisa Lawson (neither a v1 persona); the prompt carries none.
- **Guard result on the filed card:** no BLOCK. WARNs answered:
  - `three_rules.strategy_risk` (grain_or_unit): the analyst test below reads every field correctly and still files
    section 8, because the field read correctly (the locator's distance) is the device's own estimate, and only
    recomputing it from the trip's current through the line's segments shows it overshoots; no field or rule decides.
  - `repeat.gate_g` and `overuse.gate_g` (method_or_model_selection against task266 v2, five of twelve): the honest
    label, two locating methods, the right one entitled by the line's physical make-up; the alternatives
    (`decomposition_attribution`, `forecasting`) do not describe a location.
  - `test.same_puzzle_older` against task186 is differentiated on the card (a noise model for a change against a
    per-trip relocation through segment impedances).
  - Nearest driver on file 0.05 (task1); no driver within the 0.12 warn band.
- **Data-native sentence:** Feeder 14's main line is 336.4 ACSR through town and the woods to mile 3.6 and 1/0 ACSR
  for twelve miles of farmland beyond; R1407's fault locator was set with the 336.4 impedance for the whole line, every
  fault the crews have pinned down since the control was fitted sat in the woods where that setting is exact, and the
  wind-driven two-phase trips of 2026 came from the farmland, where it places every fault too far out.
- **Abstraction sentence (the one a reviewer would say is the same, written to test it):** "a device's recorded
  position for each event assumes the line is uniform, is validated only where it is, and is re-derived event by event
  through the line's actual make-up." No approved build carries it: the nearest delivered drivers, task185's
  instrument conversion sized at the reading and task192's audit frame, correct a value or a label, never a position
  through a structure; neither is approved.
- **Sources read, one line each:**
  - `stumping/references/client/two-layer-task-design.md`: the three rules and the two layers; the mess here is clocks,
    units, codes and a PDF table, and none of it moves a trip's location.
  - `stumping/references/evidence.md` Part 3 (step three, the benchmark screen, the multiplicative floor) and 1.6a: the
    correcting quantity is one per trip, forced by the GIS segments, with no free parameter; the cluster's correcting
    factor is not 1; the easy route sits outside the licensed family because the physics refutes it.
  - `stumping/references/strategies.md` F2 and F6: a correct monitor blind at its configured grain (48 v2's form, here
    a locator configured for one conductor), the bridge a geometry, never a key column.
  - `layer2-rigor-patterns.md`: Energy Systems & Utilities has no card; the family is `field_method` (the field's own
    method done right), pattern `own:fault location on a non-uniform line`.
  - `guide-to-prompt/references/examples.md`: the forcing fact once (the January patrol, one section), the question
    first, the method never named.

## Default path

The pipeline a competent analyst builds from the prompt's words and the files' grain:

1. Read the question: where on Feeder 14's main line the January patrol should look for what kept tripping R1407 in
   2026.
2. Load R1407's 2026 event report; keep the trips (operations that saw fault current), each with its fault type,
   phase currents and the control's own fault-locator distance.
3. Map each trip's locator distance onto the GIS main-line sections: the two-phase trips on windy days cluster at
   8.6 to 8.8 miles, in section 8 (8.4 to 9.3 miles).
4. Validate the locator, the field's method for where a fault is: for every 2026 trip the crews pinned to a pole
   (the tree faults in the woods), the locator's distance agrees with the pole's mileage within 0.1 mile.
5. Corroborate: section 8 carries the long span over State Highway 92, the kind of span where conductors slap in wind.

Ends on: section 8
Golden: section 6

## Stump sentence

A competent solver takes R1407's own fault-locator distances, which agree with every crew-found fault on file within a
tenth of a mile, maps the 2026 two-phase wind-day trips onto the main-line sections and sends the January patrol to
section 8 (8.4 to 9.3 miles, the State Highway 92 crossing); the step that lands it there is trusting a locator set
with one conductor's impedance on a main line whose conductor changes at mile 3.6, when each trip's own fault current,
carried through the line's segment impedances, puts the cluster at mile 7.0, in section 6.

## Tried and rejected

- Portal determinism review (2026-10-12), `competing_defensible_answer`: Sutter Park 5 under its 2025 count, two- and
  three-year averages and a recent cohort Poisson model, because the Kessler Avenue loop's overload (scheduled 2024 to
  2026) had no end anywhere in the pack and its SCADA peaks still reached 119 per cent in July 2026; the write-up's
  clause that Sutter Park 5 leads only on insulation and age was also wrong against the record. A filed back-test
  criterion was measured and rejected: on the shipped record a three-year cohort rate predicts each closed year 2019
  to 2025 best (absolute error 302 against the failure-count model's 418), so it would select Sutter Park 5. Closed
  instead by filing the overload's end (the loop's second feed, energised 15 September 2026, after its last failure on
  4 September) in the 2025 report (6.3) and the extract notes, with the write-up's clause corrected (SF9); no record
  any graded figure reads moved.

- Seed AD06 as written (a surge trigger rebuilt from a settled activation ledger): the decisive step is a rule left out of the method note and recovered from settled figures, which the guard blocks and the client caps, and under literal determinism the undefined term is a fork, not a stump.
- Drinking-water non-detects (left-censored lab results; substitution against a censored-data estimator for the 95th percentile): the decisive move is method selection (G16, banned against the last three builds), and a laboratory reporting full values is a better instrument that dissolves it.
- Heaping of cash deposits under a reporting threshold: the decisive move is a statistical test (G16 or G17), and the swap test fails because any threshold-gaming setting reads the same.
- An ICU 96-hour readmission rhythm: comparisons in 24-hour bands cancel the rhythm, so the naive read lands on the right unit by accident.
- A Farrington-type seasonal baseline behind an outbreak trigger: method selection on a seasonal baseline, and too near the background-rate driver drawn for task181 at the time.
- Capture-recapture for under-ascertained incidents: fails the instrument repair (complete ascertainment dissolves it) and sits next to task181's surveillance build.
- Funnel limits with overdispersion for an outlier hospital: the choice of overdispersion model (multiplicative or additive) flips the flag, a fork, and the decisive step is statistical rigour (G17).
- An empirical null for many hospitals' z-scores: G17 decisive, and a reflex correction for a strong solver.
- Technical against non-technical distribution losses: decomposition_attribution is banned against the last three, and it is task180's first world.
- Card cohort seasoning behind an early-default alarm: adjacent to task133 and to a task181 architecture.
- A post-campaign immunity rebound behind a measles trigger: needs a back-tested forecast method, a banned strategy for this slot.
- Service-time inflation behind an emergency department boarding alarm: a queueing decomposition, a banned strategy for this slot.
- Interviewer interpenetration behind a survey anomaly: causal_design, banned for this slot.
- Constant-risk standardisation, retrospective (emergency laparotomy; a community hospital good on the low-risk cases its catchment brings and poor on the high-risk ones; card drafted, guard PASS with no WARN, never registered): once the estimand is filed literally (the death rate the system's patients would have had at each hospital) the careful first move is direct standardisation and it lands right; the only deeper variant, risk bands too coarse, is a fork (in the sketch three bands named another hospital, five bands gave 1.14x, six bands 1.20x, per-hospital logistic curves 1.19x).
- Frailty as the unmeasured modifier in the same world: the target hospital was not worst under the frailty strata across seeds, and the strata were fragile.
- Left truncation in a joint-replacement registry (a hospital that joined late loaded its earlier primaries from its surveillance list, alive and unrevised, so the time before loading is immortal; delayed-entry Kaplan-Meier names it, Kaplan-Meier from the operation names another): it survives the literal test but fails the clean-data and instrument repair, because a registry that captured every primary at its operation makes the naive estimate right; also every partial correction (drop the loaded records, a rate from loading, a clock from loading) lands right, and a late-rising hazard put the target first on counts and crude shares.
- Constant-risk forecast (a closing hospital's emergency laparotomies moved to a neighbour in 2027; each hospital's 2027 ratio of observed to predicted deaths): it passes Gate G (a different population at a different date, both limbs filed), but the method stays open between a carried ratio and each hospital's own curve, and every filed criterion that separates them either names the step (calibration at each level of risk) or needs a back-test across a mix change (a dated event, and a banned strategy here); the per-hospital 2027 ratios also differ by estimator in the second decimal, so they cannot be graded.
- Composition designs in general (standardisation to a common population, each unit's own curve applied to a known forward mix): applying stratum-specific rates to a mix is the "reweight" reflex on the readability screen, so the decisive rung is readable however the bands are drawn.
- Device records against faults on an outage export (one fault opens several protective devices, the default counts rows): the client's Layer 1 library lists collapsing staged restorations into events as mess, so the stump would rest on Layer 1.
- Wastewater signal per person contributing to the sewer (students and visitors against census residents): the literal estimand has to name the denominator, and the fecal-strength ratio is one ratio a solver reads off a column (tests 2 and 6).
- Locus effect with masking variants in a genome-wide scan: filing the estimand literally ("the locus's variants together") names the joint model, and any selection rule for the joint set is a fork.
- Tuberculosis contacts progressing to disease in 2027: the same "a quiet unit about to surge" insight as task181's nowcast, a clone risk in the same task type.
- Learning curve of new structural heart programs: the rate-in-cumulative-experience family of task46 and task132.
- Intensive care blocking by queueing scale: no anomaly-detection task type hosts it, and the empirical past blocking is the right forecast while the load is stationary.
- This draw's first card (gap population, pattern E, gate method_or_model_selection): guard BLOCK on same_puzzle_older and same_driver_older (task28, 30, 31, 32, 53, 57, 69, 76, 228); redrawn as gap time with G14 decisive and gate forecasting before registration.
- Cable recurrence world, first tuning: with recurrence only from the third failure, the trailing in-service average already named the target (it never replaced, so its repeat failures sat in the default window); fixed by moving the recurrence threshold to the second failure, flattening the target's yearly counts, and giving the other feeders replacement at the second failure since 2019.
- Builder's first tuning (WIP before the restart): the section-year split credited the rest of each piece after a failure to the count before it, which inflated the rates after two and three failures; fixed in `models.py`, and on correct exposures the WIP world's R3 lead fell to 1.24x and the Poisson model with attributes to 1.03x.
- The WIP world itself (paper cable spliced in place, episodes on every count, Mill Lane 7 still at three times baseline in 2026): a pooled rate after one failure of 6 to 7 per cent (paper cable and the State Route 443 run) lifted every feeder's forecast, a feeder-effect Poisson model named Mill Lane 7 (1.13x) and passing history to replacements named Harrow Road 12 (1.85x), a fork on SF7; replaced by paper cable replaced at its first fault, first-failure episodes, and Mill Lane 7's episode easing out.
- A fourth rung above the failure count, 2026-10-15 (the author asked for a second decisive layer). Two were
  built and measured, and both died on this world's own structure:
  - the repeat hazard as a function of time since the last failure, with a second spliced-in-place run (a duct
    bank under a rail viaduct) carrying a recent cohort of second failures: the process self-regulates, because a
    section with a high hazard fails often and its time since the last failure stays short, so the built cohorts
    came out with the same time since (medians 1.2 and 1.8 years) and the layer had nothing to separate;
  - the repeat hazard conditioned on the water the section's structures stand in, with the viaduct run drying out
    when the deck was relaid: the water is the cause of the failure count here, so the two are collinear by
    construction and the conditioning added nothing the count had not already given; worse, the inspection
    file's Water Level column makes it a header-found join, which fails the readability screen's schema test, and
    a readable decisive rung is dead.
  The deeper reason is that in this world any model conditioned on the section's failure count already ranks
  Quarry Hill 21 first by a wide margin (its stock is 14 sections at three failures or more), so a decoy cannot
  outrank it on a count-conditioned basis without a failure volume that would also make it lead the default
  five-year average, which collapses the ladder. A fourth rung therefore needs a re-rooted world with different
  volumes, not a hardening of this one, and the shipped build was left exactly as it is (rebuilt byte-identical
  after the experiment).

- Removing the filed adjudication, the cheap repair the rework was opened on, 2026-10-22: dead on measurement,
  and it was priced clause by clause before anything was edited (harness
  `scratchpad/t183rw/s4.py`, run twice byte-identical). Two of the four clauses the wave 8 reader quoted are
  redundant and could go (report 6.2 on Harrow Road 12's paper replacement, because the register's own status,
  retired_date, insulation and install_date columns already refute a per-feeder rate there, 21.79 expected
  against the attribute model's 2.08, a ratio of 10.5; report 6.4 on Harrow Road 14's elbow batch, because no
  standing member of the estimator family names Harrow Road 14 at all, 0 of 9). One cannot go: the prompt's
  "sections in service at the end of September 2026" is the estimand's population, one of the five parts
  `determinism-check` section 1 requires filed. And one is load-bearing: SF9, the Kessler Avenue loop's
  overload and its relief in report 6.3 and the extract notes, is the clause the portal's own determinism
  return of 2026-10-12 required, and removing it reinstates `competing_defensible_answer` exactly, Sutter Park
  5 under the last twelve months (1.083x), a two-year average (1.043x), a three-year average (1.088x), a
  straight line on the yearly counts (1.076x) and an exponentially weighted count (1.025x), with Quarry Hill 21
  second in all five. So the dial has both ends on the same end: the convergence Gate C rests on here is the
  reach Gate F pays, which is the condition `stumping` 1.1 names, and it holds because the easy route (a
  trailing average) is itself a member of the family the portal licenses.

- Resuming this architecture at all, 2026-10-22: dead, because the stump does not need the clauses. The
  decisive content of the call is 17 in-service sections at two or more failures on Quarry Hill 21 against 0 on
  every other feeder, and five one-group-by routes on `section_id`, a key the default path already holds, reach
  the call from the files alone with no filed sentence: sections at two or more failures (infinite lead),
  sections at three or more (infinite), most failures on any one in-service section (9.000x), repeat-failure
  events inside the default path's own five-year window (4.000x) and sections spliced in place twice or more off
  `repair_code` (1.889x). The designed forecast is exactly linear in the stock counts and a regression on the
  twice-failed count alone reproduces it at R-squared 0.8180 with the same top bar, maximum difference 2.222
  expected failures. Screens failed, by name: `stumping` Part 3 step three (the correcting quantity is one per
  CLASS, four pooled rates, not one per case, and it is forced from the same file at the same grain as the main
  file rather than by a second file at a finer grain); the proxy screen in its structural form (the forcing file
  is the work order history and its plainest column, the per-section failure count, IS the correction); the
  monotone-functional screen (the graded object is a sum over a per-class rate vector, which a one-pass count
  reaches); and the designation determinacy screen (the standing family returns 2 distinct names, Quarry Hill 21
  in 12 of 16 and Harrow Road 12 in 4, and only one of those four groupings is asserted refuted in
  `checks.py`). The recorded resume line of 2026-10-20 was necessary and not sufficient: inferring the retired
  causes from the data's own structure rather than from a filing leaves every one of those five routes standing.

- Retuning this world's dial, 2026-10-22: dead, and the cells were counted jointly rather than marginally
  (harness `scratchpad/t183rw/s3.py` against a copy of the generator with the replacement year parameterised,
  run twice byte-identical). 300 settings swept over four dials, the highway run at 12, 20, 33, 48 and 70
  sections, the rate after two failures at 0.12, 0.20, 0.33 and 0.50, the rate after three or more at 0.33,
  0.50, 0.70 and 0.90, and the replacement-at-the-second-failure policy starting 2014, 2019, 2023 or never.
  The requirements were listed before the sweep: the licensed family unanimous on one printed call, the golden's
  lead at or above 1.15x, each of the three wrong rungs naming another feeder and clearing its own second place
  by 1.15x, no cheap count form naming the golden, and the golden in another printed cell. Marginally the dial
  looks open (the golden's separation holds in 181 of 300, rung 0's floor in 288, the golden in another cell in
  228). Jointly it is shut: **0 of 300**. The family is unanimous in only 32 settings, and a cheap count form
  lands the call in all 32 of them; the count of twice-failed in-service sections lands it in **300 of 300**,
  the count at three or more in 300 of 300, the most failures on any one section in 300 of 300 and the
  repeat-failure events in 288 of 300. The reason is algebra and not tuning: the decisive construction is
  `n2 + rho n3` with `rho = r3 / r2`, so `rho = 1` IS the twice-or-more count and `rho` large IS the
  three-or-more count, and the designed forecast sits between the two cheap routes by construction. Searching
  integer stocks to 60 sections and `rho` from 1.05 to 12, the largest lead an intermediate `rho` can take while
  both cheap routes name someone else is 1.2732x, so a cell exists in the geometry and no realistic replacement
  policy reaches it, which is why the sweep found none. Also measured at the shipped setting: the licensed
  family is NOT unanimous (Harrow Road 12 under the per-feeder and per-substation groupings), and rung 2's own
  lead is 1.165x on the built pack but 1.122x when the lateral is read off the register rather than moved, so
  the rung floor sits on the attribution of one lateral.
- **(2026-10-25, measured) A blind reader landed the call and took 97.7 per cent of the ask figures.** One isolated Sonnet reader at medium effort, holding only the pack, the prompt and the emitted key list, filed **Quarry Hill 21** against the golden QH21 and hit **43 of 44 ask figures**, every feeder's SAIFI, SAIDI, four-plus count and customers served among them, both major event days and the 13.72 minute beta threshold. It reached the call by the section-level reasoning this architecture rests on: it counted only insulation, splice and termination failures on sections still in service at 30 September 2026, found the 17 twice-failed sections at the State Route 443 duct bank with the crew note about standing water, set aside HR12's 322 failures because only 5 are on cable still in service, and named Sutter Park 5 as the answer a raw or trailing-twelve-month ranking gives, which is the default path. Readability test 3 and test 6 together: retiring out-of-service plant before projecting failures is what a reliability engineer does first.

- **Architecture 1 (2026-10-11 to 2026-11-02), spent on measurement and re-rooted, not on a portal result.** Tamsin
  Valley Electric's underground cable program (which of eight feeders fails most in 2027) stays delivered on the portal
  as it shipped on 2026-10-12. Its decisive quantity, the in-service sections at two or more failures, was a count of
  work-order rows by section_id, forced from the same file at the same grain as the main record, so one group-by named
  the call in 300 of 300 swept settings. Architecture 2 moves to a new world, dataset and shell (one architecture per
  world) and puts the decisive step on a per-trip quantity forced by a second file at a finer grain.
- 2026-11-02, the re-root draw, candidates screened on paper and set aside before the card was filed:
  - a cooperative's own direct load control releases blowing tap fuses minutes after each event, read as line faults
    until each outage is timed against the release log: the correcting factor is 1 for the feeder the call would
    designate (dropping the loud feeder and ranking the rest lands it, `evidence.md` Part 3 benchmark screen), the
    rebound after a control window is task131's driver, and the abstraction (an external process's events traced case
    by case and removed) is task303's and task181 v6's;
  - a feeder's insulation judged against the induced voltage of each nearby lightning stroke (IEEE 1410): the count
    form (flashovers per nearby stroke) equals the per-stroke physics in expectation whenever the stroke mix is
    stationary, so it bites only through a contrived quiet period; filed, the physics is rule application or, beside a
    density procedure, an official decoy; estimated from the feeders' own record, it is indirect standardisation by
    stress, the reweight reflex;
  - members with four or more interruptions in 2027 replayed through each member's protection path: under stationarity
    the trailing per-member count and the path replay estimate one quantity, so the gap is noise, and a protection
    change that makes it systematic is a dated step an event study finds or a forward condition (validated decoy);
  - a failing primary connection read off AMI voltages against a load flow: the calculated-against-measured voltage
    drop is the field's own method (golden at the top), and a degrading connection shows as a per-meter voltage trend at
    matched load, a cheaper route;
  - a cooperative's or a gas utility's balance separation (a loss proportional to throughput against one proportional
    to time): task180 v5 drew it on retail fuel tanks the same morning, and a gas or water balance has no
    anomaly-detection task type in this domain;
  - card-scheme dispute ratios carried into Q1 2027 through each dispute's lag: the maturity family, spent on this
    objective (task191, task194, task201).
  - The guard then moved under this draw: task180 v5 (filed 07:51 UTC) took shape 01, `line_manager_or_team`,
    `cooperative_or_member_body` and G3 into the window, and the gap population with G2 or G3 is a spent structural
    signature (same_puzzle and same_driver in the last twelve). The organisation was redrawn to a city-owned electric
    department (local government, the honest family for a municipal utility), the forum to the department's operations
    desk, the decisive generator to G2 under gap rule (no filed sentence says how a fault is located).

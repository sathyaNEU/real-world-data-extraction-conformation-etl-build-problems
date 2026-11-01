# task157 design note: Thornsby Bridge closure relief routes (architecture 3)

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first. Architecture 1
(the January 2027 winter guarantee qualifier forecast) was spent on its second portal return when its graded bin
proved finer than its estimator; architecture 2 (an Arizona elections division's projection of a filed initiative
petition from the statutory sample) shipped 10-27 and came back from the portal with the call landed and a
determinism finding. One architecture per world, so architecture 3 is drawn afresh in another client domain, world,
dataset and prompt shell under the same objective and number. Every figure in the live sections below is measured
on the cut pack by the generator and asserted in `generator/checks.py`.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task157.json`, architecture v3, registered 2026-11-01 with
  architectures v1 and v2 in `lineage`, each with its fate. `guard.py check` on the registered card: WARN only, no
  BLOCK (repeat.gate_g and overuse.gate_g, the forecasting mechanism every forecasting build carries;
  repeat.decision and repeat.question_form against task273, answered below); `validate` clean on 306 cards.
  Personas drawn with `guard.py names --geo "England" --seed 157`: Molly Hughes (the Combined Authority's head of
  bus network performance), Shaun Brown (Pellbridge Buses' operations director), Damien Ward (the city council's
  bridges engineer).
- **Pairing:** `urban-regional-science` / `forecasting`, objective **Forecasting & Predictive Modeling**, shape
  **10** (a scorecard: each route's forecast punctuality checked against the 80 per cent floor), decision type
  `designation_set` (the routes the relief notice names), answer unit `set_of_items`.
- **Niche:** a combined authority that franchised its buses forecasting each route's departure punctuality during an
  emergency closure of the Thornsby Bridge, because its performance regime relieves every route the notified
  disruption takes below the 80 per cent punctuality floor and the notice naming them is due before the closure
  starts.
- **As-of and window:** Friday **11 December 2026**. The bridge's principal inspection on 2 November 2026 found
  bearing corrosion; the council announced on 20 November that the bridge closes to all traffic from Monday
  **11 January to Sunday 28 March 2027**. Route 41 diverts over the Ring Road crossing. The franchise agreement's
  performance schedule wants the relief notice 21 days before a notified disruption, so by 21 December. The AVL
  extract runs from the September timetable change (31 August 2026) to Sunday 6 December 2026. The window the call
  is about has not opened, so the call faces forward.
- **Why Forecasting.** The call is each route's share of on-time departures over eleven weeks that have not yet run,
  predicted from the operating record of the timetable and duty schedule that will run them. It is not Descriptive
  (nothing in the window is observed) and not Anomaly Detection (no event in the record is being diagnosed).
- **Strategy:** gap `population` then `time`, generators **G7** (operating window: a departure inherits lateness
  only where the gap in the driver's duty is shorter than the delay) and **G4** (attribution at transition: the
  lateness belongs to the inbound route at the relief point), Gate G `forecasting`, strategy `causal_design`
  (interference between routes carried by shared crews), Layer 2 family `estimand_identification`, pattern
  `own:relief-point-lateness-carried-through-crew-duties`, calibration `prior_period_close_out` (the 2025 Marsh
  Lane diversion close-out, read only for the diversion's realised running time), context artifact
  `operations_log`, `stump_class: analytical`, no official decoy, no validated decoy, decisive rule not filed.
- **Data-native sentence.** A franchised bus network's punctuality record is kept route by route, while the people
  who drive it are scheduled duty by duty, and a duty that ends a piece of work on route 41 at Merchant Row
  Interchange often starts its next piece on another route's departure a few minutes later; so a late route 41
  arrival is recorded as a late departure on a different route, whose own path and timetable never changed.
- **The abstraction sentence**, the one a reviewer holding this build beside its nearest approved build would say
  about both: "a unit's start inherits another unit's late finish through a shared worker who passes from one to
  the other inside a short gap, so a delay imposed on the other unit reaches this one only where the gap is
  shorter than the delay." It is not writable against any approved build. task303 (the nearest in spirit) reads a
  shared upstream supply as simultaneity across sibling feeders; task162 rebuilds a device's benefit hour by hour
  from a third party's draw; task117 replays per-unit draw caps reached through a dated join; task141 and task175
  carry a rate across a covariate; task179 adds another agency's record. None links two units by a worker who
  passes between them.
- **Same-puzzle and library tests.** `guard.py check` clears `test.same_puzzle` and `test.same_driver` on
  (population, G7, designation_set) and (population, G7, forecasting). The library test: the stump sentence does
  not read "use X on Y"; there is no named correction for crew-carried lateness, and the field's named method
  (the route-level disruption assessment: the diverted route's added running time, the corridor's added traffic
  delay, every other route at its own record) is rung 0.
- **Shell, drawn with the world.** Question form `which` (a designation set asks which); corpus quota for `which`
  is over 30 per cent and task273 used it, so the other roles are drawn away: the second sentence does not open
  "Put", the deliverable set is an xlsx with an svg chart (task273 shipped docx and xlsx; architecture 2 shipped
  xlsx and png), and the rounding sentence does not open "Give". The lineage shells (v1 how-much, v2 how-many with
  xlsx and png) are not kept.
- **Fiction.** England, an invented city region (Grainford), the Grainford City Region Combined Authority as the
  franchising authority, Pellbridge Buses as the franchise operator at Saltmeadow depot, the Thornsby Bridge over
  the river between Ravensholme and the city centre. Forum `customer_or_counterparty` (the notice goes to the
  operator under the franchise agreement), forcing event `incident_or_complaint` (the inspection's defect and the
  emergency closure), org family `local_government`, role family `operations_director`.
- **Deliverables:** `closure_punctuality_forecast_2027.xlsx` (each route's forecast punctuality, the floor check
  and the notice's route list, with the asks' tables) and `closure_punctuality_by_route.svg` (each route's autumn
  2026 punctuality and its closure forecast against the 80 per cent line).
- **Spine:** `avl_timing_point_events.csv`, one AVL departure or arrival event at a registered timing point, grain
  journey by timing point by operating day, stamped in UTC. Beside it the operator's duty schedule workbook (each
  duty's pieces of work, their routes, times and relief points), the registered timetable as an XML export, the
  bridge's traffic management plan and the franchise agreement's performance schedule.
- **Sources, one line each.** `guard.py recent`, `coverage` and `mechanisms --objective forecasting` (92 builds)
  read before drawing; `guard.py slots` run on the mechanism nouns (relief, duty, driver, interchange, crew,
  roster, handover, lateness, interlining, layover, propagation) and on the setting nouns (bus, punctuality,
  diversion, roadworks, timing point, vehicle working, stand time): no slot note screens a delay carried between
  routes by crew reliefs. task469's note set aside delay propagation through aircraft rotations on the WHAT screen;
  task159, task254 and task269 are transit worlds with other drivers (a platform backlog, segment delays, excess
  wait on a common corridor). The nearest driver on file is 0.11 (task469).

## Default path

The pipeline a competent analyst builds from the prompt's words and the files' grain, with the field's own method
for a disruption's punctuality impact in it.

1. Convert the AVL events from UTC to local time across the 25 October clock change, map vehicle registrations to
   fleet numbers, drop duplicate pings and match each departure event to its registered journey and timing point
   in the timetable export.
2. Apply the performance schedule's on-time window (departure from a timing point between one minute early and five
   minutes fifty-nine seconds late, final timing points excluded, a scheduled departure lost in the lost mileage
   log counted as not on time) and compute each route's punctuality over the autumn 2026 record: every route sits
   between about 82 and 90 per cent.
3. Back-test the persistence of that record on the authority's published monthly punctuality for 2025 and 2026: each
   route's autumn level reproduces its own previous autumn within two points, so the record is a sound basis.
4. Apply the traffic management plan: route 41's journeys run the Ring Road diversion, adding the plan's nine minutes
   in the weekday peaks and six minutes at other times to every timing point after the diversion, in both
   directions; route 41 falls far below the floor.
5. Apply the plan's corridor delay for general traffic to the routes that use the Ring Road (routes 6 and 12): two
   minutes in the peaks on the timing points beyond the Ring Road; both dip and stay above 80 per cent.
6. Check for knock-on effects through the vehicles: the AVL shows route 41's buses cycling on route 41 all day, so no
   other route takes a bus off route 41.

Ends on: **route 41 alone**, every other route above the floor (route 27 at about 87 per cent, route 58 at about
88, route 33 at about 85), so the relief notice names route 41 only.

Golden: **routes 41, 27 and 58.** The duty schedule puts route 41's inbound drivers onto route 27 and route 58
departures at Merchant Row Interchange four and five minutes after their scheduled arrival, so during the closure
those departures inherit the diversion's minutes and the two routes fall to about 64 and 69 per cent; route 33's
relieving drivers have a fourteen-minute gap that absorbs most of the delay and route 33 stays near 85. The exact
figures are measured on the cut pack and asserted in `generator/checks.py`.

## Stump sentence

A competent solver who converts the AVL to local time, matches every departure to its registered timing point,
applies the performance schedule's window, backs the autumn record against the published monthly series and adds
the traffic management plan's diversion minutes to route 41 and its corridor minutes to the Ring Road routes names
**route 41 alone** for relief; the step that lands them there is treating every other route's departures as
independent of route 41, when the duty schedule hands route 41's inbound drivers onto route 27 and route 58
departures at Merchant Row Interchange within a few minutes, so those departures inherit the diversion and both
routes fall below the 80 per cent floor.

## Tried and rejected

- The blind-reader evidence this screen first recorded as owed at stage 4 is withdrawn, not deferred.
  CLAUDE.md gained a STOP block on 2026-10-27 retiring the solver flow under every name (no scored reader, no
  cold or blind reader, no call-only or draw probe, no isolated thread that answers the task), leaving stump
  power to the paper argument and the portal. The nine-route sweep computed on the clean truth stands as that
  argument. The isolated leak reader and the determinism judge are unaffected and remain stage 4.

- Architecture 1, the January 2027 qualifier forecast from the seasonal return wave (spent 2026-10-27 on its
  second portal return): the graded bin is finer than the estimator. Measured above in `## Architecture 1 is
  spent`. The decisive step was worth 0.58 of a 50,000 bin, the smallest gap in the ladder; the choice between
  two measurable subgroups for the un-returned remainder is worth 0.90 bins and the sampling error on the right
  one another 0.31, so no pin, world parameter or rounding choice forces one bucket. Three repairs were built and
  measured: a later return profile (0.58 to 2.08 bins, still open), positioning the golden by the campaign size
  (about 8,500 of slack a side), and a coarser bin (kills the stump). Re-rooted, not retired.

- Market dilution (riders' January demand is fixed, so returning drivers split a fixed pool of trips and fewer clear 40), worked at the draw: the qualification count needs the hours distribution and a demand forecast stacked on the supply forecast, and the defensible constructions spread wider than any graded bin; dropped before registration.
- A moved threshold with bunching at the old and new lines (the notch response estimated from past windows), worked at the draw: the deciding analysis is a labour-supply response to a notch, honestly economics-econometrics, whose pairing with forecasting task155 holds in the ban window; dropped rather than relabelled.
- The trips-per-driver distribution against the threshold as the decisive step: task151's driver (a stepped payout as the sum of chances from a resampled distribution); kept only as last year's observed rates, never decisive.
- The campaign recruits' type read from when each stopped (an exit-timing reference class): task146's lesson, and the campaign's bonus drivers stopped in April with its seasonal workers; kept only as a rival that misses.
- Holiday drivers (December-only drivers) inside the wave, prototyped: they separate the aggregate KPI route but their share inside each December band changes year to year, which moved every band-priced construction of the golden by up to $140,000 in the prototype; left out of the world.
- A wave timed by each driver's own anniversary, or by weather: neither is what seasonal trades do, and either would make the timing ratio a property of the group; the timing is the trades' common calendar.
- Each seasonal driver's return week fixed once for life (dealt from a profile at entry), built at stage 3: each winter's returners then kept their own mix of weeks, and the January-to-December ratio ran 1.11, 1.01 and 0.97 across the three winters, wider than the fund's bin; replaced by the trades' calendar dealt afresh each winter (which driver returns which week changes, the calendar does not), after which the winters read 1.098, 1.093 and 1.074.
- New drivers priced from the onboarding app's approvals at the as-of, built at stage 3, while drivers approved during the window could still reach 40 trips: the pool-only and every-new-qualifier constructions differed by about $25,000; closed by the terms' eligibility clause (accounts approved by the Sunday before the window, as in 2025 and 2026; 73 drivers who completed 40 trips in the 2026 window on later accounts were not paid), with "every eligible driver" in the prompt.
- Ask A as twelve figures (main run, later runs, returns, recoveries, net, drivers, both years): the main runs and later runs carry no device and hand the strongest response free points; cut to the six device-bearing figures, the chart keeping the full bridge.
- HB3 (an approved applicant whose account was opened under a second email): the applications export carries the driver id an approval opened, so the hazard had no record to live in; dropped.
- Occasional drivers coming back on at 6 per cent a week: they sat in last winter's drivers often enough to swing the June-to-October-blank construction by $13,000; raised to 15 per cent a week (shorter breaks, fewer in the winter group), the construction now within $4,000.
- Approvals stamped at any hour, and Sunday decisions moved back to the Saturday: 24 decisions fell before their own resubmission; decisions are now taken on working days in office hours, a Sunday's on the Monday.

- 2026-10-26, the portal's determinism block, both judges `competing_defensible_answer` on the main call,
  fix location `input_files`. Two forks, both closed without moving a graded figure (`freeze.py check
  --mode determinism` PASS). SF14, the shipped rider demand plan: it carried 316,650 completed trips for the
  guarantee's window, 72.5 per cent of the 436,733 the window actually takes, because it assumed 11.8 per
  cent growth where the autumn ran 19 to 38 per cent ahead and the window itself grew 53.7 per cent. Read as
  a trip ceiling it gave 3,500 drivers and $1,250,000 against the golden's 4,700, and nothing shipped ruled
  that reading out, so a declared distractor was doing the work of an official decoy. Closed by C1 rather
  than by a pin: the generator now sets the plan's growth off the autumn's own year-on-year rate, the window
  carries 447,500 trips, and three assertions hold that no demand-constrained reading binds. SF15, the
  out-of-sample line: "within 2 per cent" did not say what it was 2 per cent of, and the second judge read
  it as the fund's own precision, about plus or minus 94 drivers on 4,700. The write-up now names the counts,
  308 against 306 and 413 against 405, which are returns in the hundreds. The stump is untouched: the
  default path still files $1,450,000 against the golden's $1,650,000, four bins apart.

- **Architecture 2 draw hunt, 2026-10-27 (screens run on paper before any card was registered, under the bin law now filed in `determinism-check`).** Four directions screened against the brief's test, that the decisive step's worth in bins must exceed the defensible-subgroup spread plus the golden estimator's own sampling interval, and that it must not be the smallest rung gap.
  - **Pharmacology, population pharmacokinetics and exposure response (a weight-banded concentrate's forward vial commitment, the requirement built from each patient's own measured elimination rather than the per-kg label dose): dead before measurement.** `guard.py slots` put it on `task170/DESIGN_NOTE.md` line 667, where the same cell was screened with twenty in-cell candidates before any card and every one fell into one of four graves, "effective half-life on sparse troughs" among them as a fit whose estimator family forks the graded figure, with the note's own verdict "the cell is spent for this slot". Bins never reached: the candidate dies on determinacy, which is the (b) term.
  - **Media reach and frequency (a 2027 schedule's net reach from a single-source panel's pairwise duplication against a random-duplication product of marginals): bins pass and Gate F does not.** Measured on paper at a target of 4.21 million with the bin at 100,000 people: decisive step 490,000 people or 4.9 bins, panel sampling interval about 48,000 or 0.48 bins, subgroup spread about 0.2 bins. It dies on readability test 7 instead, because the panel that makes the golden computable makes it a one-group-by (count the distinct respondents the schedule's vehicles reach), and the escape of carrying the joint across a longer window is already recorded dead in `task270/DESIGN_NOTE.md` line 155, a radio schedule's four-week reach from one-week diaries.
  - **A council's already-born cohort (a forward intake read off births and the dwellings completing rather than off each area's own birth-to-intake ratio): dead on the corpus.** task150 is a school-by-school cohort-component projection with a kindergarten-to-births ratio in its own stump sentence and task153 already differentiates against it; the direction is occupied rather than fresh.
  - **A regional waste authority's permitted void (the exhaustion quarter built from the settlement consecutive surveys of one lift measure, against the latest survey's filled volume over a lifetime density): bins pass, the guard blocks.** Measured with the bin at one quarter: decisive step about 3 quarters or 3 bins, survey volume error about 0.4 bins, subgroup spread about 0.2 bins, and the decisive gap is the largest rung gap. `guard.py check` returns BLOCK `test.same_driver` inside the batch against task304 on (time, G3, forecasting), which differentiation does not clear, and BLOCK `test.same_driver_older` against task169 v2; the abstraction test also maps its driver onto task89 v9 and v10, time to exhaustion as a stock over the right net change rather than the published stock over a gross outflow (`guard.py nearest` 0.05). Available only on a redrawn gap or decisive pattern.
  - **Carried forward as the hunt's recommendation:** a pairwise defect's inclusion probability under a sampling design (a filed petition's duplicate signatures seen only when the sample draws both members of a pair, so the duplicate burden expands at the square of the sampling fraction while every single-signature ground expands at the fraction). `guard.py check` WARN, no BLOCK, nearest driver 0.09; measured at 11.4 bins for the decisive step against 2.30 for the sampling interval and at most 0.12 for the subgroup spread. Its two risks are named for whoever takes it: the abstraction adjacency to task264 (an inclusion probability the record's own design sets) and the measured Gate F death of task190's architecture 3, where a design-based projection had to ship the manual that then handed the route back.

- **Stage 2 of architecture 2, 2026-10-27. Four things died or were re-specified under measurement, each with
  the number that killed it (`generator/cracker.py`, six seeds, byte-identical over two runs).**
  - **The draw's own figures.** 1,043,000 filed, a three per cent sample, a 623,212 threshold and 95 and 110
    per cent bands are California's statute on an Arizona card. Rebuilt on Arizona's: 540,000 lines, five per
    cent of the signatures filed, 384,924 required, bands at 95 and 105. The decisive step is unmoved and in
    fact only exact under the new world, because Arizona samples signature lines, so a pair's inclusion is the
    square of the fraction; a three per cent sample of whole sections would have made a same-section pair's
    inclusion the fraction itself and the registered driver wrong as written.
  - **The merged disposition code as neutral Layer 1: rejected.** At a 9.2 per cent share of the sampled
    duplicate strikes, unfolding it moved the golden 0.61 bins while four of six seeds sat 0.03 to 0.19 bins
    from a cell edge, so it was load-bearing on the graded figure and therefore a fork. Closed by C1 in the
    world (SF4): the old-code county's sampled lines carry no duplicate strike at all.
  - **The calibration organ as drawn: rejected in both of its only two directions.** A prior measure projected
    from its own sample and then fully counted either reproduces its full count under the linear expansion,
    which blesses the naive method and is the validated decoy the guard blocks, or fails to, which refutes the
    naive read and is readability test 4 on the decisive rung. Replaced by a prior measure that fell under the
    sampling threshold and was verified by full count only, carrying no projection and no duplicate figure.
  - **A world with a five per cent triple-signer share: rejected.** The all-doubles expansion is then biased
    0.59 bins and the multiplicity mix is not identified from the sample at all, which is a Gate B failure
    rather than a tuning problem. The world draws multiplicity near binary (150 triple signers against 60,000
    double signers) and the bias is measured at 117 signatures, 0.0233 bins, and asserted under 0.05.
  - **Chao1 on the sample's singletons and doubletons, screened as the rival a solver reaches for:** it returns
    minus 3,482,881 valid signatures, so it refutes itself rather than standing as a competing defensible
    answer, and it is recorded in `## Convergence` rather than used as a rung.

- **Stage 3 of architecture 2, 2026-10-27. What the build measured and what it moved.**
  - **Architecture 1's `generator/checks.py`, `verify.py`, `calc.py` and `ops.py`: replaced or deleted.**
    The old checks asserted SF1 to SF15 for forks this architecture does not have, which is the FAIL
    `precut.py` was fixed to catch. The new `checks.py` asserts this build's own eight rows and runs 134
    checks; `ops.py` and the old `calc.py` were architecture 1's fund arithmetic and are gone (138 checks
    after the house-fix pass added a second PDF extractor, the citation resolution and the denominator
    refusal).
  - **The design-stage figures: superseded by the pin.** The note carried a golden of 388,460 against a
    default path of 431,420 at a slip of 400 and a duplicate count of 92. The stage 3 pin (the
    double-signer count, the single-ground rates and the share of the March cancellations falling after
    their signers' dates) moves them to 390,200 against 420,520, which is what the band and cell targets
    cost: the decisive step's full worth falls from 6.99 bins to 4.64 and its worth at the last rung from
    4.33 to 2.96, against (b) plus (c) of at most 1.44.
  - **Rung 2 outside the statutory band at all six seeds: not reachable, and recorded rather than
    smoothed.** Sixty parameter sets were measured over the six seeds against the author's two position
    targets and the rung-2 band together, and none met both, because rung 2 is the golden plus 0.62 of the
    duplicate burden while the golden must sit 2.5 bins clear of both boundaries. The shipped seed keeps
    rung 2 outside the band by 850 signatures and the other five put it inside with its figure three cells
    from the golden's.
  - **SF4's duplicate fold: re-rooted into two single-signature grounds.** The design stage had Navajo's
    merged code covering duplicates and the general class, closed by that county carrying no duplicate
    strike. A wrong split of 34 lines would then have moved the call by 12,920 signatures, 2.6 bins, so the
    fold was a live fork on the main call. The merged code now covers two grounds that both carry at the
    sample's factor (not registered, and registration cancelled), the split is forced by the registration
    the recorder matched, and `checks.py` asserts the projection identical under either reading.
  - **The ask layer: rebuilt on three primaries after the first one measured 0.495 of the ask weight.**
    The design-stage sheet's four devices were a code fold, a correction file, a sheet key and a
    determined-by filter, every one of them documented in a shipped file or found by the hygiene battery,
    so the cracker kept 45 of 91 ask figures and a single response scored 72.0. Rebuilt on three
    reconstructions over dated records (the registration state at the day signed, the firm as at the day
    signed, the day-first dates), with the free per-code ask cut, the cracker keeps 16 of 90 and the worst
    honest reading is 66.4 for a single response and 44.1 for the pair.
  - **SF5 closed by a filed sentence rather than by convergence.** The firms' manifests claim 543,380
    lines against the office's 540,000, which at the design stage was asserted convergent. Measured, the
    manifest basis projects 392,488, which does print the golden's own cell, but the margin is a draw, so
    the filing record now states flatly that the 240 sheets presented in duplicate were struck at receipt
    and are not part of the filing, and the row is closed by that sentence with the convergence reported
    beside it.
  - **Every sheet exactly full: dropped.** 540,000 lines on 36,000 sheets of fifteen makes the sheet
    register a constant column, which the realism sweep reads as a generator's arithmetic. The office now
    receipts 38,080 sheets carrying 5 to 15 lines each and summing to the statutory 540,000, asserted.
  - **The circulator register without the firm on the sheet index: the only way ask B's primary is not a
    fork.** With a firm column on the sheet index or the receipt log there are two defensible firm
    attributions and the ask is forked rather than deviced; both columns are gone and the circulator
    registration extract is the single source, so the as-of join is the work and not a choice.
  - **Floating point in the two expansion factors: removed.** The sample's factor and the pair's
    denominator are computed as integers (twenty and four hundred) because `61 / (0.05 * 0.05)` is
    24,399.999999999996 and cost a signature to rounding in the first write-up.
  - **The global sheet sequence: dead, and the assertion that passed over it with it.** The instruction and
    the filing record both file that a sheet number is the circulator's own series running from one, which
    is what makes the line key need the circulator's registration number as well. The generator numbered
    sheets 1 to 15,044 in one global sequence across all 329 circulators, so no circulator had a series of
    its own and the key claim was false in the data while `checks.py` passed on it: the assertion tested
    that some number repeated across circulators, which a global sequence satisfies by coincidence because
    the returns carry the same number under different circulators only by accident of the draw. Each
    circulator is now numbered from one over its own sheets in receipt order, 412 distinct numbers over
    44,120 sheets, and the assertion tests the claim instead: every circulator's own series is one to n and
    contiguous, and a number is shared by two circulators under different serials.
  - **Ask A's count of each recorder's own determinations: cut, measured.** It was 15 of the sheet's 90
    figures and the cracker kept all 15, because the verification instruction tells a reader how to filter
    the division's lines. Cutting it took the cracker's keep from 0.178 of the ask weight to 0.040 and the
    worst honest single response from 66.4 to 58.2, under the build target of 60, with the main call and
    the projection untouched. The population it supplied now lives inside ask A's own asking sentence,
    where it is not separately graded.
  - **The per-code ask kept in the prompt after its table was cut: a prompt that asked for a deliverable
    the pack's goldens did not carry.** The asks were restructured at stage 3 and `prompt.txt` was not
    rewritten with them, so the shipped prompt asked for a per-disposition-code figure with no table behind
    it and gave the per-month ask the sheet serials instead of the figure the workbook holds. The prompt is
    now written from the three asks the goldens carry, and the month range is pinned in the asking sentence
    (January to June 2028) rather than left to the data.
  - **Two ask-side forks closed by the filing record's own sentences rather than by a convention in the
    code.** A circulator who moves firm is withdrawn on the day its new registration takes effect, so 17
    sampled lines sit on a handover day and the firm they belong to was a convention; and one firm's two
    trading names on one registration number split 141 lines into a fifth firm against an asking sentence
    that names four. Clearing the handover days in the generator was tried first and cannot work: the
    circulators who move are the busiest, so there is no day inside the window on which they gathered
    nothing. The filing record now carries a `Circulator registrations` section stating both conventions,
    which is legitimate on this side of the build because rule 3 binds the main call's decisive step and
    the asks are free of it, and `checks.py` asserts both against the extract's own rows.
  - **The primary-cost assertion rewritten to test its claim.** It asserted that each primary solved on its
    own lifts the cracker's total, which is false once two primaries compose: solving the firm as at the day
    signed while still reading dates month first scores two figures below the cracker's baseline, because
    the right firm with the wrong month moves cells that had matched by accident. It now asserts what is
    actually claimed, that every primary is load-bearing (a response solving the other two without it keeps
    16, 29 and 55 of 75) and that no primary solved alone reaches a third of the ask weight.
  - **Seventy-three per cent of sheets at exactly fifteen lines, consecutive bundle ids and round-robin
    receiver ids: all three dropped as procedural shapes.** The weighted draw over 4 to 15 lines now leaves
    a 27.6 per cent mode at the pad's full fifteen, bundle ids step by one to four, and the six receiving
    staff ids carry an uneven load (274, 228, 174, 94, 82, 53) instead of cycling. The two statewide
    snapshots no longer carry the same row count or a monotonic identifier column, status_changed_utc
    equals the registration date only for the quarter of rows never touched since registration, the query
    notices are spread over ten dates after each line's own return rather than all on one day, and the
    instruction PDF's creation and modification stamps differ.
  - **The 2024 close-out as a pointer: re-subjected rather than cut.** It read as a file placed to be
    compared with this filing. Its county table is now subjected on the examination itself (lines examined,
    examiner days, examination closed) and its header states that every signature line filed was examined
    and no sample was drawn, so it carries its own subject and still ties under every expansion basis.  - **Ask 2's and ask 4's three live forks: closed in the asking sentence, at the cost of the ask's biggest
    device.** The stage 4 re-judge returned NOT_DETERMINISTIC on ask 2 and one boundary line in ask 4 with
    the main call, the projection, ask 1 and ask 3 forced. Which lines count (487 against 484 and 489),
    whose record establishes the registration state on the day signed (the snapshot's own dates, 487,
    against the recorder's finding, 506 to 515 and differing in 11 of 15 counties) and the same-day
    cancellation (487 and 488 against 488 and 489) are now named in the sentence, with the lapsed test
    stated once for both asks. Naming the record and the boundary files the reconstruction as a rule, so
    the registration state at the day signed stopped being a device: it moved into `cracker.py`'s
    `DOCUMENTED` set, the cracker's keep went from 0.040 of the ask weight to 0.240, the single response on
    the call from 58.2 to 66.3 and the pair ceiling from 36.2 to 45.7. Left where it landed: this pass was
    not licensed to chase the ceiling, and 45.7 is what the bar measures.
  - **Closing the same-day boundary by moving the data: not attempted, and would have broken the freeze.**
    The alternative to wording was to move the one Pima signer's cancellation off the day it signed, which
    changes a snapshot row the main call's own registration step reads, so `freeze.py check --mode rubric`
    would have failed on a frozen figure. The wording closure moves nothing graded, which is why ask 2's
    and ask 4's figures are unchanged at 487 and 488.
  - **The primary-lift assertion rewritten again, for the same reason as the first time.** With the
    registration state documented, the assertion that no primary solved alone lifts a response to a third
    of the ask weight was measuring the cracker's whole total rather than the primary's lift, and the total
    is already gated at two fifths. It now measures the lift itself (the day-first dates plus 0.147, the
    firm as at the day signed minus 0.027) and leaves the total to the gate that owns it.
  - **The reconstruction-moves-the-counties assertion re-based.** It compared ask 2's figures with the
    cracker's, which collapsed to one county once the lapsed test was filed. It now compares them with the
    easy route that counts every signer the snapshot shows cancelled (14 of 15 counties move) and asserts
    separately that the day-first dates still move exactly one county's figure, Mohave's.


- **Architecture 2, the Arizona petition sample projection (shipped 10-27), spent 2026-11-01.** The author's Batch 5
  sheet reports the portal's return as "determinism, landed": the call landed. The decisive step (a duplicate
  strike is a property of a pair of lines, so its inclusion probability is the square of the sampling fraction) is
  the field's own design-based expansion for duplicates, the random-sample duplicate formula an elections reader
  reaches for from memory, which the shipped note had named as its standing risk. It was the field's method at the
  top of the ladder, which `stumping` 1.1b says lands. One architecture per world: re-rooted into another client
  domain, world, dataset and shell; nothing of the petition world is carried.
- **Architecture 3 draw screens, 2026-11-01, each set aside on paper before any harness, with what killed it.**
  - The election-polling cell as a whole: task171's slot note screens it across poll averages, house effects,
    turnout after a surge, swing scales, tactical switching, late count streams, mail returns by time since
    mailing, notional boundaries, ranked-choice caps and signature duplicates; with architecture 2 spent there is no
    unscreened driver left in the one Forecasting task type the domain carries, so the domain moves.
  - An amendment that needs a majority of all ballots, roll-off driven by which card of a multi-card ballot the
    question sits on: the card is a column of the ballot layout, so the decisive property is a row predicate
    (readability test 2), and laying the card out in its place is rule application.
  - A new primary school's first reception intake, families with an older child at another school staying there:
    the new school's take-up among children with no sibling tie has no history to measure it, a free parameter
    that forks the golden; the sibling echo of a bulge class at an existing school spreads over four intakes and a
    trend in sibling offers catches it.
  - Landfill void exhaustion with settlement of capped cells counted as void: the survey's cut-and-fill
    conventions fork the consumption, and the regional planning cell is a thin home for an engineering quantity.
  - A teachers' pension plan's retirement wave at first eligibility for an unreduced pension (age plus credited
    service of 85): the eligibility rule is filed, so dating it is rule application, and a step at a service
    milestone is task107's driver.
  - A second-homes council tax premium base eroding as holiday lets cross the business rates letting threshold:
    the flip is a behaviour with no measured response, and the variable is the one the change names.
  - A housing trajectory whose back-test passes because optimistic large sites offset unplanned windfalls: the
    history blesses the naive method until the window breaks it (the validated decoy), as task485's note records.
  - Bus punctuality carried through vehicle workings (a route's departures made by buses arriving late off another
    route): the vehicle chain sits in the AVL the solver already opens, so it is the careful reader's next rung, and
    task469's note set aside delay propagation through aircraft rotations. Kept as rung 2 of this architecture
    (route 41's buses do not interwork), with the crew link as the decisive rung.
  - Reserving, mortality and longevity, deposit runoff, stress testing, event-driven trials, cemetery capacity and
    scaling laws: screened dead in task170, task171, task173 and task174's notes (caps, scheduled dates, persistence
    landing at one year, families that fork), not re-screened.

# task276 design note

Architecture 3, re-rooted on 2026-11-03 after architecture 2 (Urban & Regional Science, network-analysis, the
level crossing world) was spent at stage 4. Nothing of architecture 2's world, survey or replay is carried over; its
death is the A2.7 line in `## Tried and rejected`.

## Draw

- **Pairing.** Human Factors & Ergonomics (`human-factors-ergonomics`), task type `anthropometric-design-fit`, which
  serves Descriptive & Distribution Analysis in the taxonomy. The call is how a measured population of drivers is
  composed against each candidate cab's package: how many of them each cab cannot accommodate.
- **World.** Hallowfen Ambulance Service, an invented regional ambulance service formed in April 2023 from two
  predecessor services (Brackmoor in the north, which measured in millimetres and kilograms, and Vennerley in the
  south, whose occupational health forms were kept in feet, inches, stones and pounds). Its Fleet and Estates
  Committee specifies one cab for the 2027 front-line ambulance order: a base chassis (FD35 or RD43) with one
  converter's cab conversion (Pennick Coachbuild, Wrenfold Bodies, Ostrel Vehicle Conversions), five combinations
  on the tender shortlist.
- **Niche.** The converter that buys a longer patient saloon by moving the cab bulkhead forward, and fits a longer
  seat slide so that its stated seat travel is the longest on the shortlist.
- **The decision and its filing.** The service's cab fit standard files the criterion: the committee specifies the
  shortlisted cab that the fewest rostered drivers fail to fit, a driver failing a cab when they cannot be seated in
  the posture the service's driver posture model predicts for them in that cab with their eye point inside the
  standard's vision zone. Prices are tendered and shipped (a distractor); the criterion does not read them.
- **Forward facing.** The cab is specified for vehicles delivered in 2027; the population is the roster published on
  1 October 2026, filed as the population the order is bought for.
- **Shape 01**, each shortlisted cab with two figures (drivers it fails to fit, of whom women): 10 criteria; the call,
  the runner-up and the gap: 3; the chart's named parts (one bar per cab, the values, the recommended cab marked, the
  axis in drivers): 4; the two files: 2; the asks, each station with musculoskeletal absence episodes, rostered
  shifts lost and mean weekly driving hours per rostered driver: three figures for each station. With the stations
  the pack holds the sum is well over 25 before the asks are widened at stage 2.
- **Deliverables.** `cab_fit_2027.xlsx` (the committee workbook) and `cab_fit_2027.pdf` (the chart printed for the
  committee pack).
- **Shell.** Question form how-many, second-sentence opener "set", rounding opener "keep", deliverable set pdf+xlsx.
  Architecture 2's shell was what, build, give and docx+xlsx, so every element moves (shell.lineage).
- **Card.** `guard.py register` filed it at WARN: `repeat.deliverables` (pdf+xlsx against task241 v2 and task194
  v17), answered here: the pair is what a fleet team sends a committee (a workbook and the chart printed as a PDF),
  and neither build shares a world, a driver or a shell element beyond the format pair. `test.same_puzzle_older`
  differentiated against task258 (v1) and task303 (v2) on the card. Nearest driver 0.06 (task230's lineage).
- **The one other build in this cell.** task256 (shipped, pending) is the only Human Factors build on Descriptive &
  Distribution: a transit authority's bus workstation share inside a box of ranges, its operators known only by
  stature and weight and the box filled from a reference survey carried through them. Here every driver is measured,
  every stated range is already met on paper by the default path, and the miss is physical: the structure behind the
  seat stops the backrest short of the posture. The card carries the line; the shell, the decision rule (no price
  line, no share threshold), the population's data and every file differ.
- **Data-native sentence.** Ambulance converters buy saloon length by moving the cab bulkhead forward and quote seat
  travel as the slide's own length, so the drivers who need the rear of the slide are the drivers whose backrests,
  reclined to their own torso angle, meet the bulkhead first; a seat-travel count cannot see it because the stop
  moves with each driver's posture.

## Default path

1. Build the population from the front-line driving roster published on 1 October 2026, joined to the cab fit
   measurements through the staff-number crosswalk (Vennerley's legacy numbers), the latest measurement standing
   where a driver was measured twice, Vennerley's imperial entries converted.
2. Place every driver in every shortlisted cab with the service's driver posture model: hip point aft of the
   accelerator heel point from stature, body mass index and the cab's seat height; torso angle from stature and body
   mass index; eye point from the hip point and sitting height.
3. Fail the driver in a cab when the predicted hip point lies outside the cab's stated hip-point travel (each
   converter's package drawing, Wrenfold's converted from its seating reference point to the heel point) or the eye
   point misses the standard's up-vision or down-vision angle at the chassis's windscreen header and bonnet points.
   This is the field's seat-position accommodation method (the SAE J1517 and J4004 way of placing a hip point in a
   travel range) with the vision check, executed on the stated ranges.
4. Count the drivers each cab fails, and specify the cab that fails the fewest.

Ends on: Wrenfold Bodies on the FD35 chassis, failing 115 drivers on the prototype (Pennick Coachbuild on the FD35
chassis next at 184).

Golden: Pennick Coachbuild on the FD35 chassis, failing 184 drivers on the prototype, with Ostrel on the FD35 the
runner-up at 296 and Wrenfold on the FD35 at 483 once each driver's backrest is placed against its bulkhead.

## Stump sentence

A competent analyst places every rostered driver with the service's posture model, checks the hip point against each
cab's stated seat travel and the eye point against the vision standard, and specifies Wrenfold Bodies on the FD35
chassis, failing 115 drivers against Pennick FD35's 184; the step that lands it there is treating Wrenfold's stated
travel as travel its drivers can use, when its forward bulkhead stops the backrest, set at each tall driver's
predicted torso angle, before the seat reaches that driver's hip point, which fails 368 more drivers and leaves
Pennick Coachbuild on the FD35 chassis failing the fewest.

## Three rules

Task type: `anthropometric-design-fit` in Human Factors & Ergonomics, which serves Descriptive & Distribution
Analysis: the call is the composition of the service's measured driver population against each cab's package.

Domain test: the deciding quantity is the number of rostered drivers each cab fails to accommodate, which
anthropometric design fit estimates by placing each person's predicted driving posture (hip point, torso angle, eye
point) from a posture-prediction model into the vehicle package and testing it against the package's constraints.

Swap: "how many of our patients would each ward bed fail to fit" keeps the count and loses the work: a bed has no
hip point placed by a posture model, no torso angle that sets a backrest against a bulkhead, no eye point against a
windscreen header, so the question stops making sense.

Layer 1: Vennerley's occupational health forms keyed in feet, inches, stones and pounds beside Brackmoor's metric
entries (the merged OH system keeps a units column); Vennerley's legacy staff numbers in the OH system and the
telematics until the 2025 driver card reissue (HR's crosswalk); drivers re-measured on query (the protocol's latest
stands); Wrenfold's drawings dimensioned from its seating reference point while Pennick and Ostrel use the heel
point; the seat maker's dimension sheet in inches; telematics card events in UTC against a rota in UK local time
across both clock changes; telematics batches re-sent after modem outages; absence episodes that the Vennerley
legacy system split at month ends. Every item comes from the system named, none is placed to be caught, and none
moves the call (asserted in `checks.py`).

Layer 2: the data's real structure is physical: the seat is an object whose backrest occupies space set by its
occupant's own posture, and the cab's structure behind the seat bounds where that object can go; the methodological
choice that flips the call is placing the whole seated posture against the package rather than the hip point
against the seat's stated travel.

Decisive step: setting each driver's backrest to the torso angle the posture model predicts for them and placing its
top rear corner, at the driver's predicted hip point, against the bulkhead line, so the travel a driver can use ends
where the backrest meets the bulkhead rather than at the slide's stated rear stop.

Not semantics: the default path reads every field correctly (the travel is the converter's stated travel, the
bulkhead dimension is the bulkhead's trim face, the inches and the datum are converted) and still files Wrenfold
FD35; no field, code, unit or definition carries the clearance, which is a geometric relation across the seat
sheet, the package drawing and each driver's predicted posture.

Not rule application: the standard files the WHAT (who must fit, what failing means, the vision zone) and the
posture model files the posture; no filed rule or procedure performs the clearance test. Enumerated family (the 5th
to 95th percentile check, hip point in travel, hip point in travel with vision, the same with the seat's recline
range, the whole posture against the package): Wrenfold FD35's count spreads from 110 to 483 drivers (the
percentile check finds no shortfall at all) and the call splits between Wrenfold FD35 and Pennick FD35. Standing family under the filed text alone (the three hip-point
constructions and the whole posture): spread 368 drivers on Wrenfold FD35 and the same split call. What rules the
easy members out is the geometry itself (a backrest set through the bulkhead line is not a seat setting), silent: no
sentence, column or flag states it, and only the constructed corner position shows it.

Analyst test: a strong analyst who places each rostered driver with the posture model, checks the hip point against
each cab's stated travel and the eye point against the vision standard (the service's fit method executed on the
stated ranges) specifies Wrenfold Bodies on the FD35 chassis, when Wrenfold's forward bulkhead stops the reclined
backrest of its tall drivers before the seat reaches their hip points and Pennick Coachbuild on the FD35 chassis
fails the fewest.

Estimand: the cab fit standard (`policy/cab_fit_standard.docx`) files the population (every member of staff on the
front-line driving roster published on 1 October 2026), the outcome (a driver fails a cab when they cannot be seated
in the posture the service's driver posture model predicts for them in that cab with their eye point inside the
vision zone the standard defines), the unit (drivers, each counted once), the comparison (every cab on the 2027
shortlist) and the decision (the cab the fewest fail).

No decoy: nothing is planted to be caught; each converter's sheet describes its own product as converters do, no
memo, draft, briefing or stakeholder figure argues for any cab, and no fit count ships anywhere in the pack.

No certified replay: no certified or published fit figure exists to reproduce; the posture model's validation is of
the posture predictions against seat positions observed in the current fleet, honest, and it ranks no 2027 cab.

Lesson: a seat's stated travel is not the travel its occupants can use, because the structure behind the seat, met
by the backrest at each occupant's own torso angle, ends the usable travel early for exactly the occupants who need
the rear of the slide; no build on file teaches that an adjustment range is tested by placing the whole posture
against the surrounding structure (task256 teaches a multivariate share carried from a reference survey).

## Survivor anatomy

Actor: the deciding property, whether a driver's backrest at their torso angle clears the bulkhead at their hip
point, has no column in any file; it is a relation between each driver's predicted posture, the seat's backrest
geometry and the cab's bulkhead line.

Link: the comparison runs through a construction no key offers: the backrest's top rear corner (seat sheet, inches,
measured along and behind the torso line) set at the driver's torso angle and hip point (measurements through the
posture model) against the bulkhead line at the corner's height (package drawing, Wrenfold's in another datum), a
comparison the field's seat-position method never asks for.

Reflex: the field's seat-position accommodation method with the vision check is the default path's rung and files
Wrenfold FD35, the cab with the longest stated travel and the most forgiving front stop.

Back-test: the posture model validates honestly: the 2025 seat trial's observed seat positions in the current fleet
match its predictions, and the fit method applied to the current fleet reproduces the trial's observed fits, because
no current cab has a forward bulkhead, so the clearance never binds where the record was made.

Second use: every file the decisive step reads is on the default path anyway: the seat sheet for its travel and
recline, the package drawings for travel, seat height and vision points (the bulkhead is one dimension among the
package's), the measurements and the posture model.

Shock: Wrenfold's forward bulkhead reads as its selling point (the longer saloon) and its longer slide as an
advantage; Pennick FD35 is first on no single shipped statistic (Pennick RD43 has the rearmost bulkhead, Wrenfold
RD43 the longest and rearmost travel, Wrenfold FD35 the lowest seat and the most forward front stop).

Pins: the WHAT is filed in the service's cab fit standard in its own genre, and no filed sentence names the
backrest, the bulkhead, clearance or recline as a test; deleting any filed sentence leaves the clearance exactly as
silent as before.

## Readability screen

Stage 2.

## Semantic fork table

Stage 2.

## Ladder

Stage 2. Prototype on 2,640 drivers (`proto_final.py`, `proto_tune.py` in the session scratchpad, rebuilt in the
generator): the 5th to 95th percentile check, hip point in travel and hip point in travel with vision all name
Wrenfold FD35 (110 and 115 drivers against Pennick FD35's 179 and 184, margins 1.63 and 1.60); the whole posture
names Pennick FD35 (184 against Ostrel FD35's 296, margin 1.61), Wrenfold FD35 rising to 483.

## Closure table

Stage 2.

## Literal reader

Stage 2.

## Oracles

Stage 2.

## Ask sheet

Stage 2.

## Tried and rejected

- Overlap and saturation alone (`binding_constraint`, G8): the first-order correction a careful analyst makes by reflex (collaborators already seeded cannot be invited) lands the call, and overlap among invitees is a second-order effect at launch densities that stay plausible.
- Acceptance delay completed community by community (`maturity_censoring`): the nowcast by unit-specific delay is task181's and task451's driver.
- A dated platform campaign inflating some pilots (`decomposition_attribution`): a cause with a cutover date is adjusted by reflex (the strategy record, F8).
- The pilots' evidence judged at the pilot rather than the invitation (`uncertainty_hold`): the client's record has interval stumps landing on the natural computation.
- Exposure-response at launch density (`composition_mix`, pattern E, 2026-10-24): a developer's chance of accepting rises steeply with how many seeded collaborators invite, read at each member's own invitation count at launch density, is task175's driver (a unit's chance of being taken rises steeply with how many units on its own run are already taken, read at its own run's fill and carried run by run) with the count created by the seeding instead of found on the street; `guard.py check` scored it 0.06 against task175 and passed it with WARNs only, so the repeat was found by the abstraction test, not the guard.
- A1.1 Year-one retention by market against the month's sign-ups, when members who leave erase their accounts (in-app deletion under App Store guideline 5.1.1(v) and GDPR Article 17) and the accounts table and the analytics export hold only accounts not erased (Product Analytics, metric-definition-measurement-science, `population_selection`, G9): the strongest; honest, prototyped, and the routes separate, but `guard.py check` BLOCKs `test.same_driver` inside the twelve-build window (population, G9, method_or_model_selection against task270's v1 and v6 lineage), the G12 reading of the same step BLOCKs against task268 v2 and task273 v1 lineage, and no honest redraw of the gap or the pattern keeps the mechanism, so it cannot register. Written in full below.
- A1.2 The share of checkout requests over a latency line from traces weighted by their recorded sample rate, when the collector's rate limit drops traces at peak minutes without changing the recorded rate (Product Analytics, metric-definition-measurement-science): the swap fails (a laboratory audit desk with a daily cap reads the same; inclusion probabilities under a capacity cap are generic survey sampling), so the domain is a backdrop. Written in full below.
- A1.3 Block parking occupancy for a demand-responsive rate change, from paid space-hours that miss free placard parkers, completed from enforcement licence-plate sweeps matched to pay-by-plate sessions (General Statistics, missing-data-censoring-measurement-error): all seven anatomy lines hold on paper, but the abstraction sentence (the part a measuring channel misses is completed from a second channel's sample cell by cell and added) is task275's, approved. Written in full below.
- A1.4 A release's store rating read from reviews posted during a phased release (Product Analytics): regressing each day's ratings on the day's version mix from the analytics is task263's driver (each source's own level measured only in mixtures whose proportions change), spent. Written in full below.
- A1.5 A free plan's monthly limit set from a usage distribution held down by the current rolling-window cap (Product Analytics, metric-definition): the capped rows hand over the signal (stumping Part 3, step 7), and the uncensored demand above the cap needs a fitted model with a free parameter (Gate C).
- A1.6 Checkout funnel losses at a payment step that hands the buyer to a bank app and returns them under a new browser identity (Product Analytics, funnel-journey-analysis): identity resolution carried by Layer 1; once the join is cleaned the call is easy.
- A1.7 Multi-visit web funnels fragmented by WebKit's seven-day cap on script-set cookies (Product Analytics, funnel-journey-analysis): a reflex for web analysts and a reading of a platform behaviour (data semantics).
- A1.8 A candidate primary metric scored for sensitivity on an experiment corpus whose experiments were stopped early on the old primary metric (Product Analytics, metric-definition): the swap fails (a hospital's trials stopped on the old endpoint read the same) and each experiment's planned horizon is a registry column (the schema test).
- A1.9 Push deliveries under APNs store-and-forward coalescing once the 2027 schedule sends more alerts (Product Analytics, metric-definition): devices' offline spells are unobservable at the new schedule's resolution, a free-parameter model (Gate C), and the effect is small outside a few segments.
- A1.10 New items' first-week views held down until the next recommendation-model retrain, carried to a daily cadence (Product Analytics, feature-adoption-diffusion-modeling): task258's abstraction (an effect that reaches only the units a step's condition lets it reach), and the step rides on an as-of time join (time semantics risk).
- A1.11 A legacy feature's distinct users over 2027 read from an event log retained for six months (Product Analytics, feature-adoption): the off-window seasonal users are absent (Gate B) and any projection is a fitted reach model, the field's method as the golden or a fork.
- A1.12 Email-verification losses from deliveries deferred at corporate mail gateways (Product Analytics, funnel-journey-analysis): a root-cause question; the losses are real losses at the step, so the descriptive answer does not move.
- A1.13 A new version's crash rate during a phased release with self-selected manual updaters mixed into the random slice (Product Analytics, metric-definition): a comparison-group question, `causal_design` (banned against task157) and Experiment and Causal Analysis ground.
- A1.14 Durable usage inflated by in-product prompts (Product Analytics, feature-adoption): already dead in this slot (a dated campaign adjusted by reflex).
- A1.15 Search requests' tail latency once the index is split across more shards and every request waits for its slowest shard (Product Analytics, metric-definition): the swap fails (a discharge that waits on every laboratory result reads the same).
- A1.16 Life expectancy of a group under-recorded on death certificates, corrected locally through a linkage to an enrolment register (Sociology, fertility-mortality-life-table-estimation): misclassification among decedents outside the register is absent (Gate B), and carrying the linked rate within a place is task124's abstraction.
- A1.17 Ward peak occupancy against the midnight census (Healthcare, provider-quality-risk-adjustment): the estimand's clock (midnight against hourly) is the step, a WHAT fork (stumping 1.2).
- A1.18 Claims-based disease prevalence by area with practice-dependent coding intensity (Healthcare, provider-quality-risk-adjustment): task271 v1's driver (a risk property recorded at other units), and the honest label `composition_mix` is banned against task166.
- A1.19 Small-area support for a ballot measure by MRP with engagement-driven nonresponse corrected through voter-file turnout (Political Science, small-area-public-opinion-estimation-mrp): several defensible model specifications split the districts near the line (Gate C).
- A1.20 Brand duplication inflated by shared store access (Marketing, segmentation-market-structure): the honest label `composition_mix` is banned against task166 and partitioning by distribution is a known correction in the duplication-of-purchase literature (reflex).
- A1.21 A port passenger survey whose interviewers fall behind at peak hours, so realised sampling rates fall under the designed interval (Survey Research, sample-design-allocation-weighting): post-stratifying by hour is a grouping (stumping 1.1c), which the data separate by reflex.
- A1.22 Plan-limit and pricing replays (seat licences, AI token costs under a new cache rule, per-organisation rate limits) over the 2026 history (Product Analytics, metric-definition): executing a filed plan rule over the history is rule application.
- The four strongest written in full, as the orchestrating session asked. A1.1: default path, each matured monthly cohort (November 2024 to October 2025) built from the accounts table's sign-up date and country, a member retained when the analytics export shows a session in the twelfth month after the sign-up month, pooled by market (or cohort rates averaged, or a Kaplan-Meier on the last active month), the market with the highest rate named; the analytics vendor's own retention dashboard agrees because the vendor honours the same erasures; ends on the market whose leavers erase most (the prototype: Germany, 0.268, against Spain 0.210). Golden: retention over the month's sign-ups, the erased members placed in their cohorts by the account id's order among surviving ids and their country from the request register's residence field, counted not retained unless the erasure came after their twelfth month, those few bounded both ways: Spain, 0.192, bounds 0.190 to 0.195, Portugal next at 0.181. Swap: holds (a hospital cannot erase a patient's record under records-retention law and a utility keeps a leaver's account for years, so the route that removes leavers does not exist there). Anatomy: Actor holds (whether a sign-up later erased their account has no column; the erased are absent), Link holds (the register keys requests by an account id the accounts table no longer holds; the cohort comes from the id order), Reflex holds (the cohort retention table files the wrong market), Back-test holds (the vendor dashboard agrees with the survivors), Second use holds (the register sits for a GDPR one-month completion ask), Shock open (the high-erasure markets lead the survivors' ranking by a visible margin), Pins hold (the plan files retention over the month's sign-ups and no sentence names erasure). Bin: margins 1.08 on the survivors and 1.06 on the sign-ups, both under the 1.15 floor, with erasure shares of 9 to 37 per cent of sign-ups; realistic shares of 10 to 25 per cent bound the swing. Prototype: a seeded replay of ten markets' sign-ups, monthly activity and erasure behaviour (leavers erase at a market-specific rate, stayers rarely, a delay after the last session), run in the session scratchpad and not kept in the pack. Guard: BLOCK as A1.1 states. A1.2: default path, each request's latency weighted by its trace's recorded sample rate, the share over one second, which reconciles with the load balancer's per-minute counts within 2 per cent on monthly volume and understates the peak-minute tail; swap fails; Actor, Link (kept traces per second against the load balancer's counts), Reflex, Back-test, Second use, Shock and Pins hold on paper; bin not reached; dead on the swap. A1.3: default path, paid space-hours over available space-hours by block and rate period, validated on the 2019 sensor pilot's low-placard blocks; golden adds the unpaid occupancy the sweeps read cell by cell; swap holds; all seven anatomy lines hold; bin a ratio estimator with a corridor; dead on task275's abstraction. A1.4: default path, the rating before and after the release date; golden the daily rating regressed on the day's version mix; swap holds; Link holds (the store's reviews carry no version, the mix comes from the analytics); Shock open; dead on task263's driver.
- A2.0 (2026-11-03, architecture 2's draw): the count of vehicles held over five minutes as the deciding quantity. Died
  on the prototype: with the bridge near its capacity the count above five minutes moved by a factor of four between
  neighbouring storage settings, so the graded figure had no stable bin; the deciding quantity moved to the closures'
  vehicle-hours, whose spread across every reasonable convention is about three per cent.
- A2.1: the first card check BLOCKed on `ban.pattern` (C against task241) and on the older same-puzzle and same-driver
  tests against task147 and task159 with G7 decisive; G7 with pick_one_of_n hard-blocks against task307 inside the
  twelve. Redrawn to pattern none with G8 decisive and differentiation lines against task147 and task159.
- A2.2: a downstream signal 400 metres beyond the crossing. Rejected: the estimand's section would have to reach it at
  every crossing, and a far count site that counts departures records the slow discharge directly, a back-test that
  refutes the closure model at the stump crossing in plain sight.
- A2.3: approach counters that count both directions. Rejected for the same reason: the departure lane is a Newell
  input-output measurement of the paced discharge, a second route to the golden that needs no network walk.
- A2.4: vehicle-actuated bridge signals with logged greens. Rejected: the greens on a morning without closures are
  unknowable, so the comparison the brief files has two readings (Gate C); fixed-time shuttle working in the
  morning plan closes it.
- A2.5: a signal lost-time convention left open. Rejected after measuring it: two seconds of lost time a green moved
  Mill Lane's figure by 31 per cent, far outside any bin; the timing register's own note files effective green as the
  displayed green.
- A2.6: crossing, county and bridge names drawn as invented place names (Sallowby, Tewsley, Hawsby). Renamed to
  descriptive road names under H21: two of them sat within two letters of real villages.
- A2.7 (2026-11-03, architecture 2 spent at stage 4 after four determinism judge rounds): the queue survey, the
  default path's validation organ, agreed with the no-blocking replay and contradicted the world, and an honest
  survey names Mill Lane at a glance (a mean queue at the barriers' rise of 37.7 vehicles against 28.6, westbound
  rows to 113 against at most 53 elsewhere), so no honest survey both agrees with the world and keeps the stump; the
  finite-storage rule the golden needs could only be filed by stating most of the decisive step. The general lesson:
  a validation record of the default path that is true only under the wrong mechanism is a certified record blessing
  the wrong method, and when the honest record reveals the answer, the stump is a surface read. The level crossing
  world, its survey and its closure replay stay dead.
- A3.1 (2026-11-03, architecture 3 search, each dead at the screens before any data was cut): part-load NOx from
  dry low-NOx combustors (Jensen at the period mean is task229's and task187's driver, part-load factors task450's);
  tidal speed through the water (task482); out-of-home loop and dwell audiences (task281); adherence variants
  (task281, and task270 v8's supplier-filled supply); historian deadband and compression (task486, and the swap
  fails); aliasing of sampled series (task241, task249, task251); radio day-after recall, retransmission blackouts and
  panel reporting weeks (dead in task271's and task281's notes); the dissimilarity index's small-unit bias,
  tempo-adjusted fertility, emigration in old-age death rates, capture-recapture, interval-censored onsets and
  testlets (spent, task262, task265, task123, task236 and the notes that list them); care-home falls with held beds,
  FX last-look re-trades and infusion pump dosing (each step settles the population or the outcome, the WHAT pincer,
  or is a field reading); not-reached items (the golden is the field's own method and the scoring rule forks);
  bonus hunger in claim reporting (a free behavioural model); analyser carryover (linear and small); a steering
  column's rake arc against a converter's adjustment box (a field reading or one cheap comparison, prototyped as
  `proto_cab`); survey multiplicity and respondent-driven sampling, legislative cohesion, multilevel regression and
  poststratification, segregation indices (spent or forked across the field's estimators); retest lift, intensive
  sampling RMS moves, reporting-cost claims, slot landing and subscores (task270's lineage); pooled testing,
  age-length keys and glycolysis in delayed specimens (screened dead in task307's, task482's and task274's notes).
- A3.2 (2026-11-03): the first cut of this world put one vision angle per cab in the standard; one standard angle for
  every cab replaced it (a per-cab angle is a rule the reader executes), and the FD35 header was raised so the
  shortlist reads as a real shortlist (the first tuning failed a quarter of all drivers on the RD43 cabs).

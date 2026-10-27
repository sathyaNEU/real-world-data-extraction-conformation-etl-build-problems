# task308: which 2027 capacity offer the cooperative should contract, and what it is worth

Architecture 3, drawn 2026-10-27 (wave 7, Opportunity Sizing & Decision Support, perssathya). Re-root after
architecture 2 (a catastrophe layer for one of four regional home books) was spent at stage 4. Moved to another client
domain and dataset under the rule that a stuck build is redrawn rather than parked (`CLAUDE.md`). Nothing of the
insurance world is carried.

## Draw

- **Pairing:** energy-systems-utilities x Opportunity Sizing & Decision Support, task type
  generation-capacity-planning (OS). Decision: pick one of four offers. Sized quantity: each offer's 2027 expected
  unserved energy removed (pool: the offered megawatts; realisable: the shortfall they would have covered in the
  recorded weather years), valued at the planning standard's value of lost load less the offer's annual capacity
  payment.
- **World:** Prairie Hollow Power Cooperative, a generation and transmission cooperative in a fictional US Upper Midwest
  territory serving eight member distribution cooperatives, winter peaking since its members' heat pump programmes. Its
  2027 fleet: a nuclear share, a hydro plant, one coal unit (its sister unit retires at the end of 2026), two combined
  cycles on firm pipeline transport, ten simple-cycle combustion turbines on Northgate Interstate Gas Transmission's
  interruptible service, six reciprocating engines, 800 MW of wind and 400 MW of solar under contract, 200 MW of firm
  imports from Red Willow Hydro Authority over the 345 kV tie. The resource planning committee awards one 2027 capacity
  contract from the request for offers: the Ketchum Ridge peaker (300 MW, interruptible transport on Northgate), a 300 MW
  firm import from Red Willow over the existing tie, Sandhill Draw Wind (450 MW), Coulee Flats Solar (500 MW).
- **Forum and forcing event:** the resource planning committee (committee_or_panel); the offers are firm to the award
  meeting and the contract is signed for delivery from 1 January 2027 (purchase_order_or_contract). Organisation:
  cooperative_or_member_body. Role: the resource planning engineer (capacity_planner).
- **Data-native sentence:** the outage event log records each unit's forced outages with a cause code, and the ten
  peakers on Northgate's interruptible service carry lack-of-fuel outages that begin and end together in the coldest
  hours, the same hours that carry nearly all of the 2027 fleet's replayed shortfall; a new peaker on that service has no
  record of its own, so what it would have done in those hours is read from its class's record in those hours, not from
  its rating.
- **Four candidates, each with a default path and a screen** (the author file's rule):
  1. *Correlated fuel outages (chosen).* Default: replay the fleet, credit the new peaker its rated or class-average
     forced outage rate in every hour, award the peaker. Screen: the decisive step is a dependence between a unit with
     no record and its class, read only by setting the class's outages against the shortfall hours; no filed sentence
     names fuel, curtailment, cold or the class's hours.
  2. *Risk hours moved by the solar already contracted.* Default: credit solar its output in last decade's top gross
     load hours. Screen: on a winter-peaking system every competent replay already removes it; a lower rung, not the stump.
  3. *Energy-limited demand response against long cold spells.* Default: credit a capped number of four-hour calls at
     nameplate. Screen: the call schedule is a dispatch rule (a method fork on the main call); dropped.
  4. *Imports curtailed when the neighbour is short.* Default: firm import at full availability. Screen: the neighbour's
     shortage would have to be planted in a document; a hydro exporter with its own record carries no such hidden
     condition. Dropped; the import is the honest winner instead.
- **Guard (filed card, 2026-10-27):** WARN only. The gap, generator and Gate G axes were redrawn from the first draft
  (gap population with G14 repeated nine older builds' signature; objective with G14 and method_or_model_selection
  carries one differentiation line against this slot's architecture 2). `repeat.question_form` (which, against task271)
  is answered by the decision: a pick of one offer asks which. Deliverables moved to xlsx and docx after the pdf and xlsx
  set repeated task271.

## Tried and rejected

- 2026-10-25, before the pack: the seed's own step (cannibalisation measured on flat streets carried to a hilly
  district) is a visible-state stratification on elevation, which the probes on this lane land by reflex; a
  station-level pilot comparison missing members who switched stations is a contaminated comparison, found by both
  probes on task304; battery swaps capping a hilly district's rides are handed over by battery columns. Set aside on paper.
- 2026-10-25, stage 2: twenty small University stations; per-station cells by day of week within month overshot the
  turned-away requests by 13 per cent (a station's stocked seconds and empty seconds move together when a few bikes
  drain), so the family forked; five large hubs (two residence halls, three class hubs) cut it to 3 per cent.
- 2026-10-25, stage 2: the graded figure to the nearest USD 10,000; the standing family on University spans about USD
  8,000 (induced riders on the rides served, day-of-week cells, the simulated e-bike world), so no seed holds it in one
  10,000 bin; 25,000 holds every network with USD 5,000 to spare.
- 2026-10-25, stage 2: per-station 2024 trips as a distractor; it licenses a difference-in-differences reading of the
  pilot that moves the uplift by a point and University's figure by USD 6,000. Dropped for the vendor's quotation.
- 2026-10-25, stage 2: the operations director's line that the e-bikes should go where the riders are, in the board
  paper; a stakeholder view pointing at the wrong answer reads as a planted decoy. Cut.
- 2026-10-25, stage 2: billing ZIP codes with a lookup for ask A; any real ZIP ties the invented city to a real one. The
  register carries the rider's home area from sign-up instead.
- 2026-10-26, stage 2: road-test retests reopened within 90 minutes only; a one-day window repair then lands the golden.
  Retests now reopen up to 39 hours later and intermittent faults come back within a ride or two, so no window separates
  them from genuine repeats.
- 2026-10-26, stage 3: the e-bike crew's moves on a 15-second grid, every charging session taking the lowest free point and
  192 sessions plugged in at local midnight on 1 January read as generated; the crew's pace, the point a rider picks and
  the New Year's Eve plug-ins now come from their own stream, and no call figure moved.
- 2026-10-26, stage 3: the 03:00 audit showed each station at its par on 92 per cent of mornings, a constant stream; the
  night crew now leaves a station a bike or two off par when the van runs short, and the call's figures moved by under
  USD 200 (University USD 127,946 to 127,804).
- 2026-10-26, stage 3: the first controller replacement in April; with the points re-drawn, a register-must-rise filter
  landed two of the three months before it. Moved to January, the filter misses every month.
- 2026-10-26, stage 4: architecture 1 spent. Both isolated scored readers (sonnet and opus at medium, prompt and pack
  only) rebuilt each station's classic stock from the 03:00 audit, the trips and the van moves, imputed the requests the
  empty seconds turned away and named University (USD 100,000 on station x day x hour-by-weekend cells; USD 125,000, the
  golden, on station x hour x day type x term cells): demand censored at empty stations is the field's textbook estimate,
  and a pack holding the audit and the dispatch log makes it executable. Both landed ask B (the re-sent sessions by their
  repeated registers) and neither ask A (one person a card) nor ask C (every job card). The judge thread returned
  NOT_DETERMINISTIC, SEND_BACK on Gate C (the estimation grain and the e-bikes' new riders unfiled in the measure; the
  person and job definitions in asks A and C), Gate G analytical_non_defect and Gate H pass. Realism tells the readers
  named: the inventory closing to zero on every station-day, one par per network at the 03:00 audit, Harbour's flat
  per-station rides, trip durations and the e-bike share flat across networks, hours and distances, the pilot note issued
  in January in the past tense, the pilot stations' capacities against the 5 per cent match. Re-root at stage 1.
- 2026-10-26, re-root screen (scratch t308v2): the pilot's comparison stations ran dry too, so the ride-based uplift
  double counts the relief; call-only probe B (opus) found the comparison stations' empty hours and measured the uplift
  on demand (University at USD 125,000). Any stump that runs through censoring or stock in this world is spent.
- 2026-10-26, re-root concept readers (opus, medium, scenario text only): household interference in an
  account-randomised retention trial, appraisal-smoothed private-fund returns, first-round against repeat screening
  yield. Each reader took the named textbook move at once (household-level contrasts, Geltner desmoothing, first kits
  split from repeats). Dropped before a pack.
- 2026-10-26, re-root, the journey unit (scratch t308v3): members re-dock at 45 minutes and day-pass holders at 30 to
  restart their included minutes, and the pilot's riders choose an e-bike once per journey, so take-up read per ride
  undervalues Central's day-pass tours. Both concept readers and both call-only probes on the first pack missed it
  (Riverside at USD 125,000 against the golden Central at USD 200,000). On the second pack (tourists riding two or
  three journeys a pass-day), probe D (opus) read the pile-up of classic rides just under the included minutes and
  the cliff after them as riders re-docking, chained same-station restarts within five minutes and filed the golden
  exactly (Central USD 225,000), and probe C (sonnet) reached Central through the day-pass e-bike rides' uncapped
  lengths. The allowance's cliff in the ride-length distribution announces the re-dock. Dead.
- 2026-10-26, re-root screen (plan-only Opus readers, text only, no figures): county procurement savings that budget-bound
  departments re-spend, a growth grant's induced jobs where the workforce commutes in, a Medicaid plan's savings past its
  members' churn, bus journeys from housing sites that build out slower than the developers' survey says, and contingent
  business interruption carried by suppliers' locations. Each reader named the step itself as the decisive one, unprompted.
  An economic mechanism that the filed estimand's own wording invites ("the fall in expenditure", "regional jobs", "the
  plan's spending") is a reflex, whatever the world.
- 2026-10-26, re-root probe pack (job-search app, a cancellation-flow save offer tested in two markets, carried to five):
  subscribers who cancel because an employer on the platform has just hired them cannot be saved by a price, and one
  market's employer side hires half its cancellers. The plan-only reader missed it; on the pack the Sonnet probe filed
  Mexico (USD 510,000) and the Opus probe linked the employer placement invoices to the cancellers and filed Colombia
  (USD 420,000, the golden). A hire record in its own file is read as churn by the first reader who opens it. Dead.
- 2026-10-26, plan-only screen of six general mechanisms (Opus readers, text only): a list-price rise judged on promotion-week elasticities (stockpiling), an adherence programme sized on the adherent against non-adherent admission gap (healthy adherer), a heat programme sized on same-day excess deaths (harvesting), threshold clinics sized on the last reading (regression to the mean), fare-free days sized on the trial days' lift (trips moved between days), and a ward sized on average occupancy (queueing at the peaks). Every reader named its mechanism unprompted, five of them as a numbered step. A general statistical mechanism is a reflex whatever world it is dressed in; only a world-specific structure is worth a pack.
- 2026-10-26, plan-only screen of four world-specific candidates (Opus readers, text only): a road reconstruction sized on patching avoided (the reader weighted traffic by standard axles unprompted), a station car park sized on new rail journeys (the reader named railheading and the full car park's hidden demand), and a cancellation-screen save offer carried to five markets (the reader named app-store billing as the first thing that could move the winner). All three dead on paper. The fourth, a bus priority corridor whose late running carries into the vehicles' next journeys, passed: the reader worked the corridor's own journeys only.
- 2026-10-26, probe pack (bus priority on one of four corridors, sized by the passenger lateness removed in 2027; Mill Lane's buses go straight on to the busy cross-town 22 and 30 on a short layover, so the lateness the scheme removes there stops passing into those journeys; the corridor-journeys replay files Harbour Road at 62,000 against the golden Mill Lane at 96,000): the plan-only reader missed it, but on the pack the Opus probe rebuilt the 2025 operation from the AVL, found that holding at timing points and a two-minute stand on each running board reproduced every recorded arrival to the second, replayed every board-day with the scheme and filed Mill Lane at 96,000 in eight tool calls; the Sonnet probe read the same two-minute stand off the running boards and filed Mill Lane at 96,000 too. A record that a replay of its own rules reproduces exactly invites the replay, and a replay of the whole operation carries every knock-on with it. Dead.
- 2026-10-26, plan-only screen of eight more (Opus readers, text only): an express lane whose toll would pass the statutory cap (the reader solved the toll under the cap and the speed standard), a security programme on a layered defence (marginal effect after the controls in place), a card limit increase whose defaulters draw the new limit (the pilot's own charge-off gap carried by score and utilisation band), a lender's product line whose losses sit with brokers since removed from the panel, an unlit artificial pitch (floodlight conditions applied slot by slot), courier-delayed potassium samples, a price rise that rivals follow, and a GP surgery sited by floating catchments. Each mechanism was a numbered step in the reader's plan. Dead on paper.
- 2026-10-26, plan-only screen of two more (Opus readers, text only): a motor rate cut sized by underwriting profit with one segment's case reserves strengthened by a claims-handling change (step 1 of the reader's plan checked case-reserve adequacy against the reserve history and fell back to paid), and a recycling service sized by tonnes diverted with contaminated loads rejected at the sorting plant (step 2 netted each area's reject rate). Both mechanisms were numbered steps. Dead on paper.
- 2026-10-26, plan-only screen of four more (Opus readers, text only): an extra ambulance crew sized by category 2 calls reached in time (step 4 split each late call into an availability miss and a geography miss, step 5 replayed the dispatch with the extra vehicle), e-bikes sized by ride revenue with flat batteries waiting for the swap van (step 6 capped usable e-bike-days by the 2027 swap rota), a home renewal increase sized by the underwriting result with multi-line households cancelling their car policy (step 6 priced the car-line spillover), and four nurse posts sized by agency spending avoided with the bank nurses the posts free covering agency shifts on other wards (missed: the reader netted bank-filled gaps as no saving, but the freed pool is a workforce mechanism any staffing field shares, so the swap test fails). Dead.
- 2026-10-26, plan-only screen of four more (Opus readers, text only): a survey boost sized by the cut in the regional standard error (step 4 rebuilt the design effect of the added sample by PSU take and interviewer workload), a regional catastrophe cover sized by expected recoveries less premium (step 4 rebuilt events from uncoded claims under the hours clause), a bus priority scheme sized by passenger time riding and waiting (step 5 priced waiting from each stop's headway spread, E[H squared] over 2E[H]), and a seven-day discharge team sized by bed-days released (steps 2 and 3 kept only the delay the team can remove and counted midnights, weekends first). All named. Dead on paper. The bus reader used the smartcard taps only to sense-check the counters and never followed a passenger from one bus to the next.
- 2026-10-26, the bus corridors with an hourly country connection at Grove Road (passengers set down late by the corridor bus wait for the next hour's country bus): two plan-only readers passed it on paper (one priced the country buses' waits against the timetable and used the smartcard taps only to reconcile loads; the other chained taps only to find alighting stops), but the estimand cannot carry it. Counting the connection wait needs either a sentence naming the change of bus (which hands the step over) or an arrival convention for passengers who walk to a stop, whose scope is then the decisive step (a definition reading under rule 3). Dropped before any data was cut.
- 2026-10-26, stage 2: the first ask layer (the unit's figures over the platform's, cases that left the report open;
  the scheme rebuilt by effective dates). On pack t5 the opus probe kept 16 of 16, finding the open cases and the
  effective dates, and the sonnet probe 4 of 16 by the effective dates: every device sat on a path a careful reader
  takes. Re-sited onto the unit's re-dated losses and reopened cases and the scheme's reinstatements and rewrites; on
  t7 both fresh probes kept 0 of 16.
- 2026-10-26, stage 2: taking the usual day's claims off each period moves Severn Vale to the bin edge (-0.150 against
  -0.084); the event definitions now say every claim of the peril dated in the period belongs to the occurrence.
- 2026-10-26, stage 2: the unit's re-dating capped at 120 days for a leak and 210 for subsidence reached 9 or 10 of 12
  cells on every stream, Fenland having no leak or subsidence case near a year start; widened to 200 and 300 days it
  reaches 11 (Fenland 2025 stays out of reach).
- 2026-10-26, stage 4 round 1: event claims notified late without the code at 8 per cent across every peril let the
  codes-only route at the index alone name Pennine (-0.771 against Severn Vale -0.992): the dropped claims pull Severn
  Vale's floods under the retention while Pennine's large freezes stay over it, a cheap route onto the golden region.
  Freeze claims now come in late more often (16 per cent, frozen pipes found after the thaw) and storm and flood claims
  less (3 per cent); the codes-only route names Fenland with Pennine third (asserted).
- 2026-10-26, stage 4 round 1: ask B's devices B0 to B3 fell whole to reader J (opus), who read a cancellation followed by
  later In force rows as a reinstatement. Re-sited with B4 and B5 (notice given ahead of the day cover ends, so a term
  is listed for the month its cancellation takes effect); the golden figures did not move, the heuristic now misses by
  GBP 0.89 million or more in every region.
- 2026-10-26, stage 4 round 2: four catastrophes that reach the layer (Severn Vale's floods of April 2012, June and
  November 2019; Coastal North's windstorm of January 2015) carried no event code, so the coded storms read as the
  occurrences named Pennine at its default -0.428 (reader K, sonnet). Coded on their own stream as declared late; every
  graded figure unchanged; the coded-storms route now names Severn Vale (asserted in checks.py).
- 2026-10-26, stage 4 re-judge (pass 3): NOT_DETERMINISTIC, SEND_BACK on ask B, the main call forced (Pennine +0.087
  on every route the judge built, Gate H analytical). Ask B's population was open: 17 terms given notice in September for
  a day in October or November were listed for October and never again, their Cancelled rows before the window, and
  nothing filed said what a listing means (GBP 0.5 to 1.8 million a region). Read as an ask-layer and fork repair, not a
  re-root, because both findings sit outside the decisive step and the judge found the call forced. A notice for a day
  inside the bordereaux is now keyed inside them (no term leaves the bordereaux without its end or a Cancelled row,
  asserted), the claims operations report files what a bordereau lists (SF21) and step 7 states the golden's rule.
  Filing the rule made B2 and B4 readable, and a December-listing snapshot then filed the golden in every region (gaps
  0.00 to 0.07), so the old B5 (the terms listed once) went and ask B's primary became the listing's sum insured moving
  when an endorsement is keyed, carried by the society's further advances. The judge's Fenland fork (the 2025 panel
  counted on weather claims only, 131 firms against 137, Fenland -0.727 against -0.775) was closed in the data (SF20),
  and the claims parquet lost its pandas schema block.
- 2026-10-26, stage 4 pass 4 (8851863d): NOT_DETERMINISTIC, SEND_BACK on the main-call estimand. RC-07's "at what
  repairing them would cost in the cover year", beside the plan's 2027 index, executed literally to the recorded cost
  carried by the index alone (Severn Vale -0.1), and nothing filed said the 2027 cost of repairing a catastrophe's
  claims is anything else; both round-3 readers took that reading for question 5. Ask A's step 6 did not reproduce the
  twelve figures (the judge's reconstruction differed by 0.05 to 1.5 pounds a policy). Repaired rather than re-rooted,
  because the judge found the effect in the data and the decisive step analytical (Gate H), and its own fix is a
  filing of what is valued, not of how: RC-07 s.3 now says the plan's index follows the price of rebuilding a standard
  home in ordinary times and does not carry what else made a catastrophe's repairs cost what they did, naming no
  driver, panel or method. Filing it makes a surge readable, so the surge the field reads on a catastrophe's size
  became a rung: on the old quote 3 of its 16 forms filed Pennine (the catastrophe's loss, pooled: linear, quadratic
  and hinge), a cheap route onto the golden. Severn Vale's quote was re-priced from GBP 4.42 to 4.34 million (rate on
  line 29.47 to 28.93 per cent), which moves no other region and puts all 16 size readings on Severn Vale (SF22, with
  the claims-per-firm fit far ahead of every size reading); the default now ends on Severn Vale at GBP 0.0 million.
  Step 6 states the unit's case handling word for word and the rival clause in block 1 was rewritten for a runner-up
  at nil. Round 3's realism tells were fixed in the same pass (repair lags by peril, one claim a policy for a peril on
  a day, each catastrophe's own span); no graded figure but Severn Vale's value moved.
- 2026-10-26, stage 4 round 4 and judge pass 5 (eb9d2db9): architecture 2 spent. Reader O (sonnet) landed the call: it
  read RC-07 s.3's new sentence (the index does not carry what else made a catastrophe's repairs cost what they did)
  as demand surge, fitted the cost of a claim on claims per panel contractor (flat to about 17.5, then 3.9 per cent a
  claim a firm), re-priced each event at its 2027 load and filed Pennine at GBP 0.9 million, quoting the s.3 sentence
  and the contractor column as what decided it. Reader P (opus) read the same sentence as leaving the recorded surge
  in the costs and filed Severn Vale at the index alone (0 of 1 call, 4 of 20). The pass-5 judge returned
  DETERMINISTIC, FIX_NOW: the main call forced by the s.3 sentence and the claims, with the 2027 panel unfiled (a
  panel grown with the book, or a fit not carried past the 35 claims a firm on record, gives no uplift) and ask B's
  term identity read by policy number (10 to 30 million high, the rewrites' old terms kept). The dial is the
  architecture's own: filing that the index leaves out what a catastrophe's own repair load adds (Gate C, the pass-4
  SEND_BACK) hands a reader holding the panel-firm column the step (Gate F), and without the sentence the pass-4 judge
  read the index alone as the literal estimand. A call any reader lands is spent; re-root at stage 1, architecture 3
  (the last before the number is retired, which needs the author).
- 2026-10-27, re-root: architecture 3 moved to energy-systems-utilities (generation-capacity-planning) under the
  no-idle-pause rule; the insurance world and its panel-firm surge are not carried.

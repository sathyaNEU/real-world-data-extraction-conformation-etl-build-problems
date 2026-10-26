# task308: which region's home book takes the 2027 catastrophe layer, and what the layer is worth there

Architecture 2, drawn 2026-10-26 (wave 7, Opportunity Sizing & Decision Support, perssathya). Re-root after
architecture 1 (300 e-bikes for one of five bike-share networks, the rides on record censored by empty stations) was
spent at stage 4. The number's seed (OS10, the bike-share world) is not carried: the world, the decision and the quantity
are new, and about sixty candidates were screened on paper and by call-only probes before this one (`## Tried and
rejected`).

## Draw

| Field | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task308.json`, architecture v2 (v1 in lineage) |
| Pairing | Actuarial Science & Insurance / catastrophe-exposure-accumulation / Opportunity Sizing & Decision Support |
| Niche | which of a UK mutual home insurer's four regional home books takes a 2027 catastrophe excess of loss layer (GBP 15 million excess of 10 million each loss occurrence, one reinstatement at 100 per cent), valued as the expected 2027 recoveries on the region's own 2010 to 2025 storm, flood and freeze events brought to the 2027 book, less the quoted premium and the expected reinstatement premium, when what a claim costs rises with the claims each repair panel firm has to take on at once and one region's book doubled in 2021 while its panel did not grow |
| Call | the region whose book takes the layer, and the layer's 2027 value on each of the four regions, GBP million to one decimal |
| Decision | `pick_one_of_n`, answer unit `named_option` (with its GBP figure) |
| Mechanism | gap objective then time; pattern none (G14 carries the decisive rung); generators G14 (decisive: the cost of a claim conditioned on its event's claims per repair panel firm, read across every event and carried to the event's 2027 scale), G13 (each historical year's events carried forward to the 2027 book and the 2027 panel) |
| Gate G | `binding_constraint`: the repair panel's capacity binds at the 2027 scale and moves the pick off the region the on-levelled losses name |
| Strategy | `binding_constraint`; layer 2 family `field_method`, own pattern: post-event demand surge at the cover year's scale |
| Calibration | none |
| Furniture | forum `board_of_directors` (the mutual's board approves the 2027 business plan and its reinsurance budget), forcing event `budget_or_appropriation` (the budget buys one regional layer; the brokers' quotations are firm until 15 December 2026), organisation `financial_institution` (a mutual home insurer), role `portfolio_manager` (the head of reinsurance writing the placement paper), context artifact `filed_standard` (the committee's valuation basis and the company's catastrophe event definitions) |
| People | Donna Phillips, Anne Shah, Nicholas Hardy, drawn with `guard.py names --geo uk --seed 308` (Amanda replaced on a persona WARN) |

**Data-native sentence.** A catastrophe's claims are repaired by the region's panel of contractors, and when one event
hands each panel firm several dozen jobs at once the firms subcontract, materials run short and every repair costs more,
so a claim's cost in the record is the cost at its own event's claims per firm; Pennine's book doubled with the 2021
Calder and Colne transfer while its panel stayed at about 34 firms, so each of its pre-2021 events would put about twice
as many claims on each firm in 2027, and only its post-2021 events, the record's largest claims per firm, show what that
does to the cost of a claim.

**Guard.** `guard.py check` on the card: PASS, no WARN. The draft's three BLOCKs were cleared on the furniture, not the
design: `test.same_puzzle_older` on (time, G14, pick_one_of_n), where three priors sit, by the honest gap pair (the
reported, on-levelled loss is right and is not what the layer pays at the 2027 scale: objective first); the forum
`committee_or_panel` (barred against task121) by the board, which approves the reinsurance budget; and the forcing event
`purchase_order_or_contract` (barred against task137) by the budget round, which is what forces the choice of one
layer. Nearest driver 0.10 (task120 v1, lineage), next 0.08.

**Abstraction test.** Stripped of nouns: a past loss carried to a larger book is scaled claim by claim at the cost each
claim carried, when the cost of a claim rises with the claims per unit of a capacity that did not grow with the book;
only cost per claim read against claims per unit of capacity across every past event shows the uplift. Against task303
v2 (a renewal increase priced on claims whose storm days a model must hold out): there the record holds the frequency
the decision needs once the storms are set aside; here every claim's cost is right for its own event and wrong for the
same event at the 2027 scale. Against task130 v4 (a cover paying only events first reported inside a short window):
there the count of past events is the quantity; here the count and the date of every event are given, and the cost of
each claim at a scale no past event of that region reached is the quantity.

**Call-only probes (2026-10-26, the probe pack at scratchpad `s308/probes`, an earlier set of quotations).** Both
isolated probes (sonnet and opus at medium, prompt and pack only) named Severn Vale, at GBP +1.2 and +1.9 million on
that pack's quotations. Both built each year's occurrences with a window dynamic programme over the dates of loss and
on-levelled every claim by its district's policies and the rebuild cost index; neither read the cost of a claim
against its event's size. The probes' window programme split long floods into two occurrences on that pack; storm and
flood claims are now front-loaded on their first days, and the window programme and one period per event agree on
every region and year.

**Sources, one line each.**
- `layer2-rigor-patterns.md`, catastrophe-accumulation-risk #1 (occurrence against aggregate): the layer pays each
  loss occurrence over the retention and the reinstatement caps the year at two limits, so annual totals cannot stand
  in for occurrences; this build's step is not that one, it is the cost of each occurrence at the 2027 scale.
- The catastrophe-modelling literature's post-event loss amplification (demand surge): claim costs rise with an
  event's demands on local repair capacity, modelled as a function of the event's size against that capacity; run here
  on the company's own events, with the capacity the panel firms on record.
- Burning-cost (as-if) pricing of a catastrophe layer: past events re-stated at current exposure and costs, then the
  layer's terms applied; the field's own method, which this build's default path executes faithfully.

## Default path

1. Read the committee's valuation basis, the quotations, the event definitions, the business plan and the claims and
   exposure files; build each region's windstorm, flood and freeze claims into loss occurrences under the hours clause
   (72 hours for a windstorm, 168 for a flood or a freeze), the company choosing each period's start.
2. Bring every claim to 2027: its district's 2027 policies (the plan's region total spread by the 2025 district mix)
   over the year's, and the plan's 2027 rebuild cost index over the index in its month of loss.
3. Apply the layer to each occurrence, cap each year at two limits, average over 2010 to 2025, and take off the premium
   and the expected reinstatement premium.
Ends on: Severn Vale, about GBP -0.4 million (every region negative; Pennine about GBP -1.0 million).
Golden: Pennine, about GBP +0.2 million (figures fixed at stage 2).

## Stump sentence

A competent analyst brings every claim to 2027 by its district's policies and the rebuild cost index, applies the layer
to the occurrences the hours clause allows and names Severn Vale at about GBP -0.4 million, because the record prices
each claim at its own event's claims per repair panel firm: Pennine's book doubled with the 2021 transfer while its panel
stayed at about 34 firms, so each pre-2021 freeze and storm would put about twice as many claims on each firm in 2027,
and the cost of a claim read against claims per firm across every event (the post-2021 Pennine events the record's
steepest) re-prices those events into the layer and puts Pennine first at about GBP +0.2 million.

## Three rules

Task type: catastrophe-exposure-accumulation (actuarial-science-insurance), which serves Opportunity Sizing: the call sizes what a catastrophe layer is worth on each of four books (expected recoveries less premium and reinstatement premium) and places the one layer the budget buys where it is worth most.
Domain test: the deciding quantity is a catastrophe layer's expected recoveries at the cover year's exposure and costs, which a reinsurance actuary prices by burning cost from the company's own events, and the field's catastrophe models carry post-event demand surge: an event's claim costs rise with its demands on local repair capacity, so an event striking a larger book costs more than in proportion where the capacity has not grown.
Swap: "Pennine takes the layer because its old freezes, struck on its 2027 book, would swamp its 34 repair firms and cost more per claim" with a hospital's admissions in place of claims and wards in place of repair firms reads as a capacity question with nothing to price: no retention, no limit, no reinstatement, no hours clause, no premium to set against recoveries; with a utility's outage repairs it loses the layer's terms, which are what turn a cost per claim into recoveries.
Layer 1: event codes only for declared events and missing on late-notified claims (the claims system); occurrences built from dates of loss under the hours clause (the company's event definitions); incurred as paid plus outstanding on 31 October 2026, the 2025 claims still part-reserved (the claims ledger); cash settlements with no panel firm or sign-off date (the settlement route); the 1 January 2021 Calder and Colne book transfer into eight Pennine districts (the policy administration system's district counts); two storms two days apart in February 2022 that one 72-hour period can hold; ordinary windstorm, flood and freeze claims on quiet days among the event claims; nothing placed to be caught.
Layer 2: field_method, post-event demand surge: the cost of a claim rises with its event's claims per panel firm, read from every event's indexed cost per claim against its claims per firm, and each past event is re-priced at its own 2027 claims per firm before the layer's terms apply.
Decisive step: price each historical event at the repair cost its 2027 scale implies (the cost of a claim read against claims per panel firm across every event, each event carried from its own claims per firm to its 2027 claims per firm on the 2025 panel) instead of carrying each claim's recorded cost forward by the index alone.
Not semantics: every field can be read correctly (what incurred is, what a panel firm is, what the transfer added, what the index measures) and the analyst still carries each claim's cost forward by the index, because no field, flag or document says the cost of a claim depends on how many claims its event put on each firm; only the cost per claim against claims per firm across the events shows it.
Not rule application: the valuation basis files the estimand (each year's events had they struck the 2027 book, at what repairing them would cost in 2027, under the layer's terms) and the hours clause files the occurrence; nothing names demand surge, panel capacity or the cost of a claim against an event's size. Enumerated family on the draw pack (four surge forms, pooled and Pennine-only fits, district and region scaling, index at loss and at sign-off, period starts on the spike or up to two days earlier): 56 of 64 surge-aware routes name Pennine, its value GBP -0.43 to +0.25 million; the standing family (district scaling, which the basis files): 32 of 32 name Pennine, its value GBP -0.20 to +0.25 million, five bins of the printed unit; the eight routes without the surge name Severn Vale. Stage 2 retunes the world until every standing route files Pennine's value in one bin (its pre-2021 freezes exhausting the layer under every surge form), with the spread asserted in `checks.py`. The ruling-out is quiet: no column or clause separates the routes; the cost per claim against claims per firm does.
Analyst test: the easy route, every claim carried to 2027 by its district's policies and the rebuild cost index with the layer applied to the hours clause's occurrences, names Severn Vale at about GBP -0.4 million (the default path's Ends on), against Pennine at about GBP +0.2 million.
Estimand: `committee_pricing_basis.pdf`: expected 2027 recoveries are the average over 2010 to 2025 of what the layer would have recovered had each year's windstorm, flood and freeze events struck the region's 2027 home book, each event's claims at the 2027 policies in force in each postcode district, at what repairing them would cost in 2027, under the layer's retention, limit, reinstatement and loss occurrence definitions, less the quoted premium and the expected reinstatement premium, in GBP million to one decimal.
No decoy: nothing is planted; no document argues for a region, carries a value for one or ranks them; the brokers' quotations price the layer in each region (an input the value nets, not a ranking on it), the group's 2026 catastrophe programme and the 2024 flood resilience survey are declared distractors.
No certified replay: no certified or published loss figure is shipped for a method to be recovered from; the golden is built from the claims, the exposure, the index and the plan.
Lesson: an as-if loss carried to a larger book is not the old loss scaled up when the cost of a claim depends on the load each event puts on a fixed repair capacity; a model learns to read cost per claim against load per unit of capacity across every event and to re-price each event at its forward load, which no build on file teaches for catastrophe pricing.

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

# task315 design note

Architecture 1, drawn 2026-11-07. Opportunity Sizing & Decision Support, Urban & Regional Science, optimization.
An inland Norwegian county council chooses which fast-charging site package its 2027 budget funds on its mountain
roads, each package sized as the long-distance electric car trips of 2027 it makes completable that today's network
cannot.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task315.json`, architecture v1, registered 2026-11-07 and re-checked
  as filed: WARN only (repeat.decision, pick_one_of_n against task286). The older same-puzzle note (gap time,
  pattern C, pick_one_of_n) is differentiated on the card against task258 v1 (slow page loads rebuilt part by part,
  a different quantity, record and decision). Nearest driver 0.06 (task122 v3).
- **WARN answered.** The call is one package of three funded from one budget line, so `pick_one_of_n` is the
  decision's honest type; task286 picks a pilot area by a household-use count, a different decision.
- **Axes redrawn at the draw, and why the new label is the honest one.** The first probe carried the state charging
  fund (`government_agency`), the fund's call for proposals (`filed_standard`) and the fund's board; task286 filed
  `government_agency` and task314 `filed_standard` into the window. Norwegian county councils fund charging on
  their own county roads, and the roads here are county roads, so the county council (`local_government`, its
  council adopting the 2027 budget, `council_or_assembly`, `budget_or_appropriation`) is the owner a reviewer would
  name; the stakeholder's own file is the county's 2026 fast-charging coverage report (`capacity_report`). Gap
  objective with pattern C repeats ten older builds on both structural tests; the decisive gap is time (the stretch
  that fails is fine from April to October and fails in the cold months the 2027 window holds), objective second.
- **Seed and why its world was left.** OS17 (ten grant-funded child-care centres placing children in their first
  year), read through `status.py task315` only. Its pairing (policy-education with Opportunity Sizing) has no task
  type serving the objective, so the world needed a client domain; re-homed to Urban & Regional Science /
  municipal-service-demand-resource-allocation, every honest driver the child-care world offers was priced and is
  spent on file or executes as rule application (`## Tried and rejected`). The number moved to a county's
  charging-site choice in the same client domain, keeping the seed's decision shape: one figure a public plan
  commits, sized from a pool of places to what is really realised.
- **Pairing:** Urban & Regional Science (client domain) / optimization (serves Opportunity Sizing only) /
  Opportunity Sizing & Decision Support. The pool is the travel survey's 2027 projection of long-distance trips by
  electric car over the county's mountain and valley routes; the realisable is the part each package makes
  completable that today's network cannot; the call is the package that makes the most.
- **Shape 07 (a grid):** each package's trips made completable by month of 2027 (three packages by twelve months,
  each cell graded), the call, the runner-up and the gap; the asks add their own grids (Ask sheet); the chart's
  named parts and the files. About 50 criteria before the asks are cut down.
- **Mechanism:** stump strategy `binding_constraint` (reachability is the limit the coverage figure never checks: a
  route counts only if every stretch is within what the car can drive there in that month); gap time (the cold
  months) then objective; pattern C with G8 decisive (reachability, binary per stretch, car and month), G13 (the
  2027 window holds the cold months the measuring summer does not) and G14 (the network's pooled energy per
  kilometre does not apply to the exposed stretch); Gate G `binding_constraint`; Layer 2 family
  `allocation_constraints`, own pattern `stretch-energy-as-driven`.
- **World:** Fjellmark County (Fjellmark fylkeskommune, invented), an inland Norwegian county of valleys and two
  mountain crossings on county roads: the Ramnfjell plateau crossing on Fv 40 (exposed above the treeline) and the
  Tverrlia pass on Fv 52 (higher and longer, forested and sheltered), plus the long lowland Saudalen road on Fv 33.
  Fast chargers stand in the valley towns either side of each crossing. Package A infills the Saudalen gap with two
  sites, package B puts one site at the Ramnfjell summit lodge, package C one at the Tverrlia ski centre. Two
  invented operators run the existing sites and send the county their session exports. Furniture: forum
  `council_or_assembly` (the county council's 2027 budget meeting in December 2026), forcing event
  `budget_or_appropriation`, organisation `local_government`, role `programme_officer` (the county's charging
  programme manager), context artifact `capacity_report` (the county's 2026 coverage report).
- **People** (`guard.py names --geo Norway --seed 315`): Ann Henriksen (the county's charging programme manager)
  and Kjersti Rasmussen (an operator's data contact); Anders was dropped for a first-name WARN. More are drawn from
  the same seed when the documents are written.
- **Data-native sentence.** Cars use about the same energy per kilometre on every stretch of the county's roads
  that a valley weather station describes, except where Fv 40 runs exposed above the treeline over Ramnfjell, where
  the winter wind and drifting snow cost what no valley station, rated figure or climb records; the only trace of
  it is the energy the same cars used between the chargers either side, which only their consecutive fast-charging
  sessions bracket.
- **Abstraction sentence** (the one a reviewer holding this build beside its nearest approved build would say is
  shared): a route counts only if every stretch is within what the vehicle can cover on it in that month, and one
  stretch's cold-month cost is recorded only as the energy the same vehicles used between the refills either side
  of it, so coverage at a rated, derated or pooled figure credits the option that fixes a longer or higher stretch
  and misses the one that fixes the exposed one. It cannot be written against an approved build: task309 conditions
  an effect on an intensity class built from an event's field; task162 gates a device's effect by the hours its
  inlet runs above a setting; task106 shares a pool of return legs; task120 is a storage mass balance; task303 a
  shared upstream event in the same minute; task105 a nearest-open-branch catchment; task128 a capacity natural
  experiment; task135 prices carried from another close. None is a stretch-level reachability recovered from
  consecutive refills.
- **Mechanisms on file** (`guard.py mechanisms --objective opportunity-sizing-decision`, one line each): task105
  nearest-open-branch catchment; task106 a shared pool of spare legs; task116 a contract keyed to one member;
  task118 a welfare wedge on the quantity reached; task120 production less storage gain; task127 a fused wait;
  task128 a call's effect where the queue outran the team; task301 attrition carried from recent lists to old;
  task302 substitution inside a group; task303 a shared upstream loss in the same minute; task304 a forward yield
  that is not the pilot's; task305 a forced choice read from members already forced; task306 old units still to
  arrive; task307 wear inside one duty band; task308 a common-mode outage; task309 an effect by intensity class;
  task310 output held at a send-out limit; task311 variance components; task313 an intervention acting only after a
  variable hand-off; task314 the price a customer answers; task464 quadratic branch losses. None is a reachability
  read stretch by stretch from consecutive refills.
- **`slots` screens** (mechanism and setting nouns, before the first harness): fast charging, charging session,
  charger, kWh per km, state of charge, consumption, range, mountain pass, plateau, corridor, winter, and the driver
  sentence itself (`guard.py slots --driver`). The only charging hits are task117 (a depot's contracted demand set
  by each car's onboard charger limit, a draw cap reached through a dated join) and task164 (a shared asset's
  seasonal peak from an added intermittent load); neither reads a stretch's energy. No slot screened stretch-level
  reachability.
- **Sources, one line each.** The client's rigor cards for the task type (the stated objective decides the sites;
  greedy siting misses the best set; busy units leave coverage gaps when coverage assumes every unit is always
  there) supply the family: coverage that assumes ideal reach overstates. The field supplies the rung models:
  flow-capturing location (Hodgson 1990) and flow-refuelling location with a range limit (Kuby and Lim 2005), the
  standard corridor-planning practice of checking each leg against a rated or derated range. The pack's own session
  exports decide between them.
- **Clean-truth price at the draw** (`scratchpad proto_ev2.py`, no Layer 1): rated range, a uniform winter derate,
  climb with valley temperature, climb with a lapse-rate temperature and the network's pooled energy per kilometre
  by month all fund A (167 to 270 trips against at most 4 for B); a derate on the high stretches funds A with C
  second (119); only each stretch's energy read by month funds B (201 against A's 167, a 1.20x margin that the
  design widens). The twin crossing is the organ that stops a mountain derate from landing B: Tverrlia looks harder
  on every visible attribute and is the one a derate punishes.

## Default path

1. Read the county's 2027 grant rules: a package is scored on the 2027 long-distance trips by registered electric
   cars that it makes completable, charging only at public fast chargers, leaving home at 90 per cent, charging to
   80 per cent and arriving nowhere below 10 per cent; trips today's network already makes completable do not
   count.
2. Build each projected route's stretches between chargers from the road stretch table and the site register, for
   today's network and with each package's sites added.
3. Take each car model's usable battery from the registry extract and its energy per kilometre from its WLTP
   figure, raised for the cold months as corridor planners do (the field's method), or read as the network's pooled
   energy per kilometre by month from the session exports, adding each stretch's climb.
4. A route is completable for a model if every stretch needs no more than 70 per cent of the usable battery (80
   down to 10), 80 per cent on the first stretch from home.
5. Share each month's projected trips over the models by the registered fleet and sum the trips each package makes
   completable that today's network does not.
6. Fund the package with the most.

Ends on: package A, the Saudalen lowland infill, as the most trips made completable in 2027 (figure measured on
the generator's clean truth at design).
Golden: package B, the Ramnfjell summit site, as the most trips made completable in 2027 (figure measured at
design).

## Stump sentence

The default path funds package A, the Saudalen lowland infill, because every rated, derated, pooled or
climb-adjusted energy it applies to the Ramnfjell plateau crossing keeps that crossing within range for most of
the fleet; only the same cars' consecutive sessions at the chargers either side of the plateau, read month by
month, show a winter crossing costing far more per kilometre than any of those figures, which strands most models
there from December to March and makes the summit site the package that completes the most 2027 trips.

## Three rules

- **Task type:** urban-regional-science / optimization, which serves Opportunity Sizing: the stated objective (2027
  trips made completable) decides which site package the county funds.
- **Domain test:** the deciding quantity is each package's 2027 long-distance trips made completable, computed the
  way corridor charging location analysis computes flow-refuelling coverage, route by route and stretch by stretch
  against what each car can drive there.
- **Swap:** "which clinic package makes the most 2027 patient trips completable" leaves no stretches between refill
  points and no range to cover them, so the coverage the call turns on stops meaning anything.
- **Layer 1:** two operators' session exports (one stamped in UTC with energy in Wh, one in local time with kWh),
  station identifiers that differ between each export and the county's site register, car models named differently
  in the registry extract and the exports, records one operator re-sent after correction overlapping its monthly
  file, and the travel survey contractor's projection workbook with merged headers, footnotes and suppressed cells.
  Each is produced by an operator's back office, the vehicle register or the survey contractor; nothing is placed
  to be caught.
- **Layer 2:** `allocation_constraints`: coverage under the real limit, which is what each stretch costs a car in
  each month; the methodological choice that flips the call is reading each stretch's energy as driven from
  consecutive sessions rather than a rated, derated, climb-modelled or pooled figure.
- **Decisive step:** the energy a crossing of each mountain stretch costs in each month, measured as the energy the
  same cars used between the fast chargers either side of it, read from their consecutive sessions, and the
  reachability that follows for every model in the cold months.
- **Not semantics:** every field (state of charge at start and end, energy delivered, timestamps, station
  identifiers, battery capacity, WLTP consumption) and every definition in the grant rules read correctly still
  leaves the easy route applying a rated, derated, climb-modelled or pooled energy to the plateau and funding A; no
  field, code or unit carries the plateau's winter cost.
- **Not rule application:** the grant rules fix the trips, the charge levels, the arrival reserve and the baseline;
  no rule or procedure says what a stretch costs, and executing every rule with the WLTP figure, a uniform or
  high-stretch winter derate, a climb model or the pooled energy per kilometre files A (or C); the enumerated
  family's spread and the standing family's spread on the graded trips are measured on the generator at design.
- **Analyst test:** a strong analyst checks every 2027 route's stretches against each model's WLTP energy, a winter
  derate, a climb-and-valley-temperature model or the network's pooled energy per kilometre and funds package A,
  the Saudalen lowland infill (the default path's `Ends on:`), or the Tverrlia summit site once the high stretches
  are derated.
- **Estimand:** the county's 2027 grant rules (to ship as `ladeplan_2027_tildelingsregler.pdf`, the county's own
  genre): population, the travel survey's 2027 long-distance trips by registered electric car on the county's
  routes; outcome, completable charging only at public fast chargers under the stated charge levels and reserve;
  window, calendar 2027; unit, trips; comparison, today's network.
- **No decoy:** nothing is planted to be caught: no memo, draft, briefing or stakeholder figure argues for A; the
  coverage report ranks gaps by length, never by trips, and is declared a wrong-basis distractor in
  `metadata.json` with the grant rules' scoring sentence that rules it out.
- **No certified replay:** no certified, published or closed trips figure ships, so the method is not recovered by
  reproducing one; the session exports are an operator's raw record.
- **Lesson:** a car's range is a property of the stretch and the month as much as of the car, and the only honest
  record of it is the energy cars used between consecutive charges; no build on file teaches stretch-level
  reachability recovered from consecutive refills.

## Tried and rejected

- 2026-11-07, at the draw: seed OS17's own pairing, policy-education with Opportunity Sizing: no task type serves
  it (`guard.py coverage` lists the pairing as undrawable), so the child-care world was re-homed to Urban &
  Regional Science / municipal-service-demand-resource-allocation before its drivers were priced.
- 2026-11-07, the seed's family-placement idea (a family enrols only if every young child is placed): filed, the
  forward count is an allocation simulation under the admissions order (rule application); unfiled, it is a hidden
  rule; and the family number is a shipped key that makes the sibling relation one group-by (`Link:` fails).
- 2026-11-07, waitlist take-up conditioned on whether a registered child is already in subsidised care elsewhere,
  rebuilt by linking the register to the payment history: task83's driver (an effect conditioned on each unit's
  own prior treatment history, rebuilt from a log, because the target pool's mix differs) told in other nouns.
- 2026-11-07, the other child-care drivers, each priced before any harness and each spent: a shared regional pool
  of educators or of families (task106's shared pool); comparables' fill held down by their own places (task308
  v1, task310); a ramp read on centres that opened in another season (task105 v1); waitlist staleness carried from
  fresh lists to old (task301); first-year places net of children switching from other providers (task118 v2,
  task302); places packed by weekday (task128 v2); turnover from a length-biased snapshot (task182 v4); ratios,
  age bands, school entry and licensing (stated rules, so rule application); comparables' survivorship (a count
  mismatch between the grant ledger and the close-out announces it).
- 2026-11-07, worlds screened after the child-care world, each before code: theatre lists where saved changeover
  minutes add a case only where they complete one inside a list (task472's driver: a saving realises only where it
  crosses a discrete boundary); district heating capacity limited by flow rather than heat (once the rating's basis
  is filed it is a unit reading, and a filed design cooling would be an official decoy); a municipal pilot's
  comparison streets contaminated by spillover (task500 v2's and task144's spillover through links); a diesel
  plant's fuel saved at the marginal rather than the average rate (task460's marginal responders); a hospital day
  removed at its own cost rather than the average (the valuation is part of the estimand, so the WHAT screen kills
  it); an immunisation campaign's start week against waning protection (the step is stratifying effectiveness by
  time since the dose, a grouping 1.1c rules out, and the start-week question prompts it); single-track rail
  capacity at the crossing loops (a timetable construction under stated constraints, read as rule application);
  regional input-output multipliers (formulaic and fork-heavy, every refinement a textbook card); capture-recapture
  of reported defects (24 slot notes); trip chaining for a new express route (task228, task159 and task308's
  corridor screen record it as a reflex); a call centre's redial fixed point (task148's queue with reneging).

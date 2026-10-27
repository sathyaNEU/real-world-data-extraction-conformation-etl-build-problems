# task307 design note

## Draw

- **Number and objective.** task307, Opportunity Sizing & Decision Support, architecture 1. The seed (OS09, a
  mini-split rebate programme's net savings) was left at the draw: every honest label for its decisive step
  (a comparison-group design, a population read, a decomposition of gross into net) was held by the guard
  window, and its furniture (a utility's filing with its regulator) was barred. Under the author's rule that a
  stuck build is unblocked rather than parked, the build moved to another client domain and dataset.
- **Pairing.** Urban & Regional Science, task type `optimization` (OS): which road project in a metropolitan
  planning organisation's 2028 Transportation Improvement Program takes its one congestion-relief slot, sized
  by the vehicle-hours a year it saves across the whole network.
- **World.** Merrimont, a fictional river metro in the United States, split by the Ashkettle River; the
  west bank's suburbs reach the east bank's downtown over three crossings (the Route 9 freeway bridge, the
  Center Street Bridge and the Southport Bridge). The Merrimont Area Metropolitan Planning Organization
  (MAMPO) runs the regional travel demand model. Personas drawn with `guard.py names --geo US --seed 307`:
  Krystal Cooke (travel demand modelling lead), Charles Cummings (executive director).
- **Decision and quantity.** Four candidate projects (the Route 9 widening on the west bank, the Ferry Street
  exit ramp, a lane each way on the Center Street Bridge, the Southport Avenue signal and turn-lane package);
  the call is the project that saves the most vehicle-hours in 2028's AM and PM peak hours across the
  network, with the annual hours each saves and the hours saved per million dollars.
- **Default path (written first).** Take the regional model's 2028 no-build loaded network, apply each
  project's capacity change to its own links, price the time saved on those links at the no-build volumes
  through the documented volume-delay functions, annualise and fund the largest: the Route 9 widening, whose
  segment carries the most vehicles at the worst volume to capacity ratio. Ends on: the Route 9 widening.
  Once trips re-route, the widened segment feeds the Route 9 bridge downstream, which binds, and the Center
  Street Bridge lane pulls trips off Route 9: the prototype keeps about four fifths of the widening's
  link-level saving and puts the Center Street lane about a third ahead.
- **Stump sentence.** A competent solver prices each project on its own links at the no-build volumes and
  funds the Route 9 widening; the step that lands it there is holding every trip on its no-build route, when
  trips re-route once a project opens and the widened freeway feeds the downstream crossing that binds.
- **Data-native sentence.** The trip table and the volume-delay functions are the network's own record, and
  re-assigning the 2028 trip table to equilibrium on each build network is the only way the record says where
  the traffic goes once a project opens.
- **Candidates written before this one (each with its default path and screen):**
  1. OS09 spillover by installers against their pre-registration baseline: the default (registered
     installers' unrebated sales as spillover) ends wrong, but the honest label is a comparison-group design,
     held by the window (task271).
  2. OS09 claims-lag completion of this year's rebated volume: a reflex chain-ladder completion; dead on the
     readability screen.
  3. Resource adequacy for a generation cooperative, forced outages conditioned on the cold that sets the
     heating peak: prototyped (the plan near the criterion on all-hours rates, near 190 MW short on
     temperature-conditioned rates, the tolling unit credited at about 60 MW not 97); task308's architecture
     3 registered the same world and driver first, so it is task308's.
  4. Screening yield by time since the last screen (a mobile screening unit across four districts): the
     decision frame and the yield-by-elapsed-time driver echo task301; dropped.
  5. Network equilibrium (this draw): no build on file assigns a trip table; `guard.py slots` on the
     mechanism (wardrop, equilibrium, assignment, rerouting, braess) and on the setting (traffic, congestion,
     route, link) returned no screen of it.

- **Guard at registration (2026-10-27, WARN).** `overuse.org_family` (government_agency in 40 builds): an
  MPO is a government agency, and the honest label stays. `repeat.decision` and `repeat.question_form`
  against task308 v3: the call is a pick among four projects, so it asks which. Differentiation filed
  against task158 (`test.same_puzzle_older`).

## Tried and rejected

- 2026-10-27: OS09 (a mini-split rebate programme's net first-year savings) left at the draw: its honest
  stump labels were all held by the guard window and its furniture barred; moved to another domain.
- 2026-10-27: a resource adequacy design (cold-correlated forced outages, four capacity offers) prototyped
  and dropped before registration: task308's architecture 3 registered the same world and driver first.
- 2026-10-27: screening yield by time since the last screen dropped on paper as an echo of task301's
  yield-by-record-age driver.

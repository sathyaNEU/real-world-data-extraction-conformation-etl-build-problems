# task478 design note: the Calderwick Turnpike's 2027 virtual weigh station sections, by the share of tractor-semitrailers over the gross limit

Status lives in `pipeline.json`; this note holds the design. Read the Tried and rejected section first. Architecture 5
(re-rooted 2026-10-22); the records of architectures 1 to 4 are at the end.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task478.json` (architecture v5), registered 2026-10-22 after a pull, the
  architecture 1 to 4 identities in its lineage. `check` on the registered card: WARN only, answered here.
  `people.first` (Anthony, one older build, task130): kept at the guard's warning level. `test.same_puzzle_older`
  against task228 v2 (gap objective, method selection, a ranked slate): differentiated on the card, task228 ranks the
  instruments by their own random error from three series' covariances, while here the instruments are never ranked and
  the units they weigh are counted against a legal limit after each instrument's systematic bias is removed. Nearest
  drivers on file at 0.08 (task464 v2, task244, task251 v3).
- **Redrawn at the draw, and why the replacements are the honester labels.** The live window (task249, task273, task169)
  bans the government agency, the budget cycle, the council, the regulator, the committee and the policy adviser, and
  G3 as the decisive generator. A turnpike authority is a toll-funded public authority that owns its road, so
  `utility_or_infrastructure` is its family; the decision is the site schedule of a let contract
  (`purchase_order_or_contract`), recommended by the director of freight operations (`operations_director`) to the
  authority's executive team (`executive_team`). G16 leads because the decisive step is the construction that puts
  twelve instruments on one weight basis; G19 follows because the conformed weights are judged against a contract's
  limit. Context artifact `monitoring_export`: the director works from the WIM program's export.
- **Pairing:** Supply Chain & Logistics (house domain; transportation network) sitting in General Statistics & Data
  Science, task type `data-integration-record-linkage-entity-resolution`, the ETL task type the house domain maps to.
  The ETL work conforms twelve weigh-in-motion stations of two sensor technologies (the piezoelectric stations' fixed
  width export in hundreds of pounds, the bending-plate stations' CSV in kilograms), their controllers' local standard
  time, one station's renumbered lanes and the milepost list that ties stations to sections, onto one gross-weight basis
  for the five-axle tractor-semitrailers each station weighed in 2026. Objective: Data Extraction & Conformation (ETL).
- **The decision and the quantity:** the Calderwick Turnpike Authority (fictional) lets its virtual weigh station
  contract in 2027 and must fix the five sections that receive the screening sites by 1 March 2027. Its Freight
  Compliance Program 2027 places them at the five of its twelve sections with the highest share of five-axle
  tractor-semitrailers (FHWA class 9) whose gross vehicle weight exceeded the 80,000-lb limit, among the class 9 trucks
  the section's weigh-in-motion station weighed in calendar 2026. A retrospective quantity with its reason: the program
  sites the screening on the last closed year's trucks, and the contract runs from 2027.
- **Shape:** 01, a ranked list under a cap of five: twelve sections' share over the limit to one decimal (12) and their
  trucks over the limit (12), the five sections (1), a chart's named parts (the twelve bars, the five marked, the cut
  between fifth and sixth: 3), the files (3), and the asks (designed at stage 2): 31 before the asks.
- **Strategy:** `other`, named on the card: an instrument's multiplicative bias read on a component whose true size
  depends only on load state, matched by that state to a static reference, before readings are counted against a limit.
  Gate G `etl_conformance`: the conformed weights are the object and no shipped artifact ranks the sections. Gap
  objective (the quantity counted against the limit), pattern none, generators G16 (decisive) and G19. Layer 2 family
  `field_method`, pattern `own:an instrument's multiplicative bias measured on a load-independent component, matched by
  load state to a static reference, before readings are counted against a limit`.
- **World:** United States, an unnamed state's 284-mile Calderwick Turnpike in twelve sections between its system
  interchanges, one weigh-in-motion station per section (seven piezoelectric, five bending plate), two static scale
  houses at the mainline barrier plazas where the turnpike's enforcement unit weighs the trucks it pulls in. Personas
  from `guard.py names --geo us --seed 478`: Anthony Hale (director of freight operations), Anna Haynes (WIM program
  engineer).
- **Forcing fact:** the screening sites are fixed by 1 March 2027 for the contract's notice to proceed; the pack is as
  of 12 February 2027 (exports pulled 4 to 9 February).
- **Data-native sentence:** every station weighs a tractor's steer axle with the rest of the truck, and a steer axle
  carries the cab, engine and fuel, about 10,000 lb under an empty trailer and about 11,500 lb under a loaded one
  whatever the cargo, so a station whose loaded tractors' steer axles read several per cent above the scale houses'
  loaded tickets reads every axle that much heavy, and at the 80,000-lb line that carries a large part of a section's
  heavily loaded tractor-semitrailers across it; the sections also differ in how many of their tractors run empty.
- **The WHAT screen.** Population: the class 9 trucks the section's station weighed in 2026 (program 3.2). Outcome:
  gross vehicle weight over 80,000 lb (3.1). Window: calendar 2026 at the section's station (3.2). Unit: the share of
  those trucks, to one decimal of a per cent (3.3). Comparison: the five highest of twelve (3.1). The decisive step
  settles none of them: it is how each station's readings are put on the weight basis the limit tests, which nothing
  files.
- **Sources, one line each:**
  - The client's data-integration rigor patterns: here the sources disagree by an instrument bias, removed before the
    records are counted, not by linkage error.
  - The traffic monitoring field's weigh-in-motion quality control on class 9 steer axles and gross-weight peaks: the
    field's own check, here matched by load state and pinned to static tickets.
  - This slot's architecture 4 (a per-unit latency calibrated on surveyed covers): the instrument bias family, here on a
    weight basis with no surveyed control and a load-state confound.
- **Same-puzzle and same-driver tests:** (objective, G16, ranked_slate_under_cap) and (objective, G16, etl_conformance)
  against the last twelve builds, lineage included: task228 v2 only, differentiated on the card.
- **Abstraction test:** the nearest drivers stripped of nouns (task464 v2, units below a cut on a new instrument's scale
  linked by regression; task244, a share of moves in a two-period record; task251 v3, each unit's systematic error from
  paired checks) carry no instrument bias read on a component of every measured unit whose size depends only on a coarse
  state, matched by that state to a static reference before counting against a limit.

## Architecture 4 record (spent 2026-10-22)

Architecture 4 resolved Kerbline's detections into potholes after moving each one back along its pass by its unit's
GPS latency, fitted on the surveyed utility covers, times the pass's speed. Over four stage 4 rounds seven of eight
readers missed the call, and reader F (round 3) landed it by fitting each unit's lag from the detections' offsets
inside rough clusters on the pass's signed speed; the judge's last pass (r4e) was DETERMINISTIC and APPROVE. A call any
reader lands is spent (leak-check), so the architecture is spent.

## Architecture 3 record (spent 2026-10-21)

Architecture 3 completed the unrecorded potholes with the fleet groups that drove a segment as the capture occasions
(units of one kind seeing the same potholes); three readers and the judge missed or confirmed it, the fourth landed the
call by estimating each group's visibility by maximum likelihood.

## Architecture 1 record (spent 2026-10-21)

Architecture 1 completed the unrecorded potholes over the distinct units that drove each segment (each unit either
always or never seeing a given pothole); eight readers and the judge missed or confirmed it, the ninth landed the call
by fitting each unit as an independent list. In architecture 3 that route is the careful wrong one.

## Architecture 2 record (spent 2026-10-21)

Architecture 2 resolved Kerbline's raw detections into potholes with a linkage tolerance set by each unit's positional
error, measured on surveyed utility covers; two readers missed it, two landed it by folding the sweepers' visibly
scattered reports into the precise units' potholes. Judge APPROVE (v2).

## Tried and rejected

- Architecture 5 draw (2026-10-22): re-rooted on the author's standing rule (no retirement) with a fresh world.
  Screened before it and dead: competing exits read as censoring (task134's main call); landfill first-order decay
  (set aside at task486's draw against task480); the inspection paradox on headways (task135); unconstrained demand
  behind a capacity (task147, task168); triple collocation of three series (task228, landed); startup emissions by
  thermal state (task273's screen); risk pooling of a health trust's reserve (the careful route sums the members' claims
  and lands it); coincident peaks (task117); a register's overcoverage by signs of life (the register count reads as a
  surface figure overturned, Gate G); coding completeness from switchers (a data defect corrected); GPS chord length
  from sparse pings (a known pitfall, and the swap test reads it as geometry); departmental against hospital-wide
  cost-to-charge ratios (the cost-centre organ hands it over); an inventory trend's correlated factor errors (the
  variance-only screen in mirror image: the point estimate lands the golden); seasonal shares of the calendar year
  against detrended factors (classical decomposition is the reflex and the shares route can beat it); generic erosion
  after loss of exclusivity (task484 v1's ramp curve); a one-time service depleting its pool (task83's lesson).
- Architecture 4, potholes resolved after a per-unit GPS latency fitted on surveyed covers (2026-10-22, spent at stage
  4): reader F fitted each unit's lag from the offsets of its detections inside rough clusters, regressed on the pass's
  signed speed, and landed the call exactly (1,441 potholes, 1,427 on the roadway); seven other readers and the judges'
  first derivations missed. A displacement proportional to speed is identifiable from the clusters themselves once
  passes at different speeds see one pothole, so the covers are a convenience, not the only route.
- 2026-10-22, architecture 4 stage 4 (r4d): the section yards' stores, added to make summing an app order's lines
  impossible, became an oracle (reader E: each crew-day's use rounded up to the bag reproduced every net draw) and a
  third reading (the judge read the net draws as the pounds used); the judge again asked for the order entry to be
  filed. The stores file is gone, the order entry is filed in the data notes, and the device moves to the roadway:
  the program lists the cold patches on the section's roadway and an order's section column is its crew's.
- 2026-10-22, architecture 4 stage 4 (r4c): with the app order's one close time and its figure above any single-line
  order, the re-judge still read the convention as an inference the data favours ("no shipped document says so") and
  asked for a filed sentence (FIX_NOW on ask 3 only), while reader C found it from the close times and kept 14 of 14
  and reader D took every repeated figure once and kept none. A filed sentence turns the ask into a work order (the
  mirror keeps it whole); the section yards' stores now make the summed reading impossible instead. A pothole-count ask
  added for weight was reverted the same hour: the call's own construction, so the cracker banks it (pair 28.5 to
  44.2).
- 2026-10-22, architecture 4 stage 4 (r4b): the cold-mix convention rested on the single-line orders' figures by
  severity, a fitted range no shipped text states, and one like-potholes figure (WO-27004552, 60 lb on two severity-3
  lines) sat at its severity's least: the re-judge found ask 3 open in every section (Gate C on that ask only; the main
  call, asks 1 and 2 and the chart deterministic, G and H passing, so no architecture spent). The app now closes an
  order's lines at one time with a figure above any single-line order, and the office keys each line's own close, so the
  data separates the readings without a model; like potholes carry one figure on a third of two-line office orders, not
  half.
- 2026-10-22, architecture 4 stage 4: the cold-mix ask's office orders sometimes carried one figure on two lines
  that could also be read as their total (WO-27004908, 60 lb on two severity-2 potholes, a crew's like figure or the
  two lines' own draws coming out equal): the judge (r4a) found the one ask figure open (Gate C); an office order's
  repeated figure now stays under its lines' least single-pothole figure times their number, so every repeated
  figure reads one way (checks.py A1), and Thistlebank's pounds moved from 2,145 to 2,135.
- 2026-10-22, architecture 4 build: route mileposts running whichever way a route's heading gave, so "mileposts
  increase northbound and eastbound" was false for half the routes and the cover fit returned negative latencies; every
  route's mileposts now increase northbound or eastbound, as the data notes say.
- 2026-10-22, architecture 4 build: covers drawn with no spacing: a detection matched a neighbouring cover, pulling one
  patrol phone's latency 0.09 seconds short, enough to split one pothole's two directions at a 10-foot link (Oxbrae two
  over its truth); a state route's covers now lie at least 0.06 mile apart and every unit's fitted latency is within
  0.02 seconds of its own.
- 2026-10-22, architecture 4 build: one fleet latency at 25 feet, then a fixed offset per unit and direction at 15 feet,
  each landed the seven by a hair; the patrol phones in Fenwick Gap, Grisholt and Oxbrae now lag longest and a pass's
  speed runs 0.55 to 1.2 times the road's usual, and both routes miss at every distance from half a foot to 600 feet.
- 2026-10-22, architecture 4 build: bridge decks in every section, each pass seeing a deck pothole 35 per cent of the
  time: a wide link counted as the most detections one pass wrote inside it recovered the decks without any latency
  (Fenwick Gap 6.65, Kestrelton 6.70, the seven); the decks now sit mostly in Fenwick Gap and Kestrelton, in runs of
  five to eight, a pass records a deck pothole 30 per cent of the time and one across the centre line less often than
  one in its own lanes, and the per-pass count leaves both under the line (5.14 and 5.36).
- 2026-10-22, stage 2: the card's context artifact register BLOCKed against task479 v6 once it filed; redrawn to
  filed_standard, the program the engineer works from (Draw).
- 2026-10-21, architecture 4 draw: re-rooted on the author's standing rule (no retirement). The decisive step leaves
  the capture family that spent architectures 1 and 3 and the visible scatter that spent architecture 2: every phone
  places a detection ahead of the pothole by its own GPS latency times its speed, so a pothole seen both ways is two
  tight clusters, which only the surveyed covers (the latency) and the traversals (each pass's direction and speed)
  resolve. At registration G3 BLOCKed (task484), then identity_resolution (task486 v2) and monitoring_export (task482
  v3); the card carries G10, strategy other (named in its notes) and context artifact register.
- 2026-10-21, architecture 3 stage 4: architecture 3 spent. Reader D of round 2 landed the call (the seven) by
  estimating each fleet group's visibility by maximum likelihood after seeing that units of one group agree 93 to 100
  per cent of the time; round 1's readers A and B and round 2's reader C missed (C pending at the spend). The judge
  (v3 thread) returned DETERMINISTIC, APPROVE and noted that a unit-level truncated MLE also landed the seven; a
  rework adding a second same-model pickup per non-metro section separated the unit-level routes but was abandoned when
  the spend arrived. Three architectures in this slot are spent; the author decides between a fourth re-root and
  retirement.
- 2026-10-21, architecture 3 stage 4 round 1: office multi-line orders spanning two routes while the mobile app's
  orders kept to one: reader A took a figure once per work order and route and kept ten of the fourteen pounds figures;
  every multi-line order now keeps to one route, and every section's pounds move under that rule (checks.py).
- 2026-10-21, architecture 3 draw: G16 as the decisive generator (task480 v1 lineage in the batch) and operations_desk
  as the forum (task179 v2) BLOCKed; relabelled G10 and line_manager_or_team, the honester labels (Draw).
- 2026-10-21, architecture 2 stage 4 round 2: architecture 2 spent. Reader D landed the call (the seven, every whole
  number) by noticing the sweepers' detections sit tens of metres off where every other unit repeats a pothole within a
  metre, merging the precise units' reports tightly and folding each sweeper report into the nearest such pothole; the
  scatter is visible in the detections themselves without the covers. Judge APPROVE (v2); readers A and B had missed.
  Re-root to architecture 3.
- 2026-10-21, architecture 2 stage 4: ask B, camera miles by section, its re-run device in a fourth form (copies five
  hours early, written in district clock time): both readers found the exact five-hour copies (a vehicle in two places
  at once) and kept all fourteen figures; every appended-duplicate device leaves a cross-row impossibility a careful
  reader repairs, so the ask was dropped and the traversals ship as a distractor without the re-run block.
- 2026-10-21, architecture 2 draw: a verification sample drawn on corroboration (the district reviews nearly every
  defect one camera reported and an eighth of the corroborated ones, the confirmed share carried within each
  corroboration level): the guard's same-puzzle and same-driver tests matched task473 in the batch (untested drivers
  completed by the catch rate within each band, measured where everyone is tested), the same insight; dropped, not
  relabelled.
- 2026-10-21, architecture 2 draw: dropping Kerbline's review export and its misclassified pothole reports: without a
  review a misread cover or patch could not be told from a pothole, so the truth would be unrecoverable; the class is
  taken as reliable (program 2.3) and the review goes.
- 2026-10-21, architecture 2 build: covers set after the survey and missing from the inventory: each matched a far
  inventoried cover and inflated a unit's root-mean-square error enough to merge the deck potholes, a fork between RMS
  and robust estimates that carries no analysis; every detected cover is now in the inventory.
- 2026-10-20, at the draw: the seed's FEMA world (repeat PA major disaster declarations by county). The declaration
  count is records-fixed; its levers (Statewide designations, amendments, county spellings, the per-capita indicators'
  population scaling) are data semantics or rule application; and the unobserved quantities the world offers are spent
  lane mechanisms (unassessed counties' damage, capture by own level as in task473; open disasters' costs, maturity as
  in task451 and task469; multi-county applicants' damage location, a crossing-partition split as in task474 v1;
  repeat-damaged facilities across disasters, linkage error as in task468 and task449).
- 2026-10-20, at the draw: unmetered irrigation pumping from electricity through a lift-varying energy-to-water factor:
  no ETL task type serves hydrology, and the conversion is a physical identity rather than the task type's object.
- 2026-10-20, at the draw: customer meters under-registering with the volume they have passed, rebuilt from the billing
  history: task46's driver (a rate stationary in cumulative service exposure rebuilt from a log).
- 2026-10-20, at the draw: polling-place demand during congested hours rebuilt by conservation from check-ins and
  hourly line counts: turning demand into a station count needs a queue replay whose conventions (the line at opening,
  arrivals inside an hour) either file the method or leave forks.
- 2026-10-20, at the draw: one per-pass find rate with each segment's passes (independent passes saturating with
  effort): the textbook completion, readable off the traversal log; kept as the default path's step 3.
- 2026-10-20, at the draw: occlusion by refuse carts on collection day as the condition of a pass's find rate: the
  vehicle type proxies the condition almost exactly, so stratifying the find rate by vehicle, a reflex, lands it.
- 2026-10-20, at the draw: truth discovery over several directories, some copying one upstream source: deciding which
  record is right is cleaning, Layer 1.
- 2026-10-20, at the draw: the first card on the client pairing general-statistics-data-science x etl, BLOCKed after
  task479 registered that pairing and subdomain; redrawn to the house domain whose maintenance operation decides.
- 2026-10-20, at the draw: the second card on business-operations-analytics x etl (field-service-maintenance, G16,
  operations_director), BLOCKed after the DRAWN commit by task480's registration 90 seconds earlier on the same
  pairing, subdomain, decisive pattern and role family; redrawn to supply-chain-logistics (transportation-network), G2
  decisive, field_unit_lead, personas redrawn.
- 2026-10-20, stage 2: night sessions running past local midnight as ask C's primary device: the scope of work has to
  define a service day as any part of a calendar day or the term forks, and the cracker executes that sentence; the
  primary moved to sessions the platform never closed, which only the unit's detections reveal.
- 2026-10-20, stage 2: a 2025 to 2026 crosswalk splitting 4.5 per cent and merging 2 per cent of segments: dropping the
  unlisted refs, the natural mishandling, took Fenwick Gap and Thistlebank under the line; cut to 1.6 and 0.9 per cent.
- 2026-10-20, stage 3: the per-unit find rate as a critical component: pairs and maximum likelihood differ in its first
  decimal (54.2 against 54.8 per cent), so it stays in the solution's step with its definition and leaves block 2.
- 2026-10-21, stage 4: ask C, Kerbline's service days and the March charge, on sessions the platform never closed:
  the judge's pass 1 found the charge reading open (FIX_NOW) and both readers found the unclosed days from detections
  with no session; the ask was dropped and the program's charges clause with it.
- 2026-10-21, stage 4: the 17 March renumbering as ask A's count primary: both readers resolved the old numbers by
  route milepost, a reflex once the refs fail to join; kept as a hazard, the primary moved to rejected twin numbers
  that a location join keeps as two potholes.
- 2026-10-21, stage 4: the telematics re-run appended one or two seconds after the originals: an exact-looking near
  duplicate a reader dedups on sight; the offsets now scale with each traversal's duration.
- 2026-10-21, stage 4 round 2: the review's "Duplicate of <number>" reason as A3's only link: it narrates the device,
  and both readers folded every twin from it (14 of 14 counts each); the reason is now the bare "Duplicate" and the
  link is the nearest confirmed defect on the route.
- 2026-10-21, stage 4 round 2: office multi-line orders forced to distinct pounds: one figure on every line then marked
  the mobile app's totals by itself, and reader C took each once and kept all 14 pounds; office orders now carry one
  figure on like potholes too, and only the detections' severity separates a total from a line's own figure.
- 2026-10-21, stage 4 round 2: G2 kept as the card's decisive generator once task474 architecture 6 (G2) was
  delivered, a ban.pattern BLOCK; the card's pattern is now D (two flawless grains, the passes and the cameras), the
  pattern the strategy map gives grain_or_unit, with differentiation lines for the older D builds.
- 2026-10-21, stage 4 round 3: reader F dropped a vehicle's repeats of a segment within five minutes and kept the
  camera miles; genuine loop passes within that window now sit in every section, so only overlap separates a re-run.
- 2026-10-21, stage 4 round 3: the nearest-confirmed fold of a bare "Duplicate" reason: all four round 2 and round 3
  readers placed every order by route and milepost and kept all fourteen counts. A silent count device needs a pothole
  that two records count twice inside the call's own confirmed population (a failed patch re-opening under a new
  confirmed number), which the separation line forbids; the count stays the construction layer the pounds and miles
  devices surround.
- 2026-10-21, stage 4 round 4: architecture 1 spent. Reader G landed the call (the seven sections) by treating each
  unit as an independent list in a capture-recapture design, reading 0.55 from units' overlap and 0.95 from a unit's
  own repeats, the decisive step itself, unprompted by any sentence; eight readers and the judge had missed it before.
  The asks fell with it (counts to every reader, miles to the overlap and five-minute dedupes). Re-root to architecture 2.
- 2026-10-20, stage 3: the sweepers' night shifts of 28 February and 31 March: under a UTC window they moved camera
  miles across the month boundary; the spring sweeping schedule now runs 1 to 30 March nights.

# task400 design note

Architecture 1, drawn 2026-11-03 (wave 7, Root-Cause lane), numbered from seed RC06 (an area control centre's summer
of tripled en-route delay). The seed's world could not carry an honest unbanned draw (`## Tried and rejected`, first
line), so the build moves to another client domain, world and dataset under the same objective and number (CLAUDE.md,
a stuck build is unblocked). Kept from the seed: the decision kind (a body adopts one account of a tripled operational
outcome and corrective action follows from it) and the kernel (part of the shortfall is self-inflicted upstream by a
setting changed with good intentions, while every recorded code is correct).

Corella Iron Ore runs the Mount Bracken open-pit iron ore mine in the Pilbara region of Western Australia. Its haul
trucks and light vehicles carry a collision avoidance system that sounds an in-cab alarm when another tagged vehicle
comes within a zone around the truck. Vehicle interaction incidents (collisions and significant potential incidents
between vehicles) roughly tripled in 2026. In the same spring the mine widened the system's warning zones (March), a
contractor, Westray Haulage, put a haul fleet and new operators on the North pit waste circuit (April) and production
rose (May). After a light vehicle was struck at the North ramp junction in August, the state regulator's improvement
notice requires the mine to identify the cause and put a control in place; the site safety steering committee picks
the one 2027 vehicle interaction programme from five in November 2026.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task400.json`, architecture v1, drawn and registered 2026-11-03.
  `guard.py check` on the registered card: WARN only (repeat.gate_g against task398, repeat.question_form against
  task398; a pick asks which, and the data give no other honest Gate G, see Strategy). The window was read with the
  sibling build task399's architecture 4 card in place (branch batch4-task399, commit 11e8631, not yet merged into
  this tree): it moved task399's decisive generator from G3 to G5, so G3 is free here; with task399's architecture 3
  card the draft hit ban.pattern on G3, and the honest decisive generator was kept rather than relabelled. NOTE
  test.same_driver_older against task107 v2 and task121 v4 (lineage), differentiated on the card.
- **Pairing:** Human Factors & Ergonomics (client domain) / `safety-incident-error-analysis` / Root-Cause Analysis. The
  task type serves Root-Cause and Anomaly Detection; no live Root-Cause card sits on it (task190 is its Anomaly
  Detection build; task191 architecture 3, a bus operator's collision warnings, died at stage 4 before shipping).
- **Objective and call:** which one of five programmes the committee funds for 2027 against vehicle interaction
  incidents, decided by finding what drove 2026's rise; the programme runs in 2027, so the call faces forward, and it
  is judged on the closed record of January 2025 to October 2026 because the regulator's notice asks for the cause of
  the rise. The tag stays Root-Cause: the work names the cause with the rivals ruled out; nothing is forecast.
- **Candidates (the committee's list):** A Westray operator retraining and supervision; B a separated light vehicle
  road at the North ramp junction; C a collision avoidance zone and alarm redesign; D fatigue monitoring cameras for
  night shift; E a traffic controller and queuing lanes at the run-of-mine crusher.
- **Shape:** 18, hypotheses against evidence: each candidate's cause read against the evidence cells it predicts,
  plus the call, the runner-up and the asks (arithmetic in `## Ask sheet` at stage 2).
- **Strategy and Gate G:** `causal_design` (the comparison that separates the cause: the same operators, the same
  circuits and the same exposure to real interactions before and after the zone change, with the contractor's
  arrival and the production rise landing the same spring); Gate G `decomposition_attribution` (a correctly reported
  rise assigned to the right driver; binding_constraint, signal_vs_noise_or_hold and forecasting are not honest here,
  so the WARN is answered rather than relabelled). Gap objective (every count in the pack is correct, and the
  incidents per hour, the system's interaction count and its acknowledgement rate are not what the call turns on),
  then time (the zone change, the contractor's arrival and the production rise fall within ten weeks); pattern none;
  generators G3 (the alarm record against what the operator did), G12 (an acknowledgement press logged, the absence of
  any slowdown logged nowhere), G6 (the contractor's operators and circuit shifting the employer mix).
- **Furniture:** forum `committee_or_panel` (the site safety steering committee), forcing event `incident_or_complaint`
  (the August collision and the regulator's improvement notice), org family `other` (a mining company; the
  vocabulary has no mining key), role family `compliance_or_audit` (the site health and safety superintendent),
  context artifact `monitoring_export` (the collision avoidance vendor's monthly dashboard), calibration none. None is
  held by the last three live cards (task277, task398, task399 architecture 4).
- **People** (`guard.py names --geo "Australia" --seed 400`): Shari Jefferson (health and safety superintendent, the
  requester), Kerri Smith (mine production manager), Ana Cuevas (Westray Haulage's project manager). Corey Nguyen and
  Christine Carney were drawn first and set aside on people.first WARNs. None appears in the prompt.
- **Data-native sentence:** the collision avoidance system logs every alarm and the operator's acknowledgement press,
  and nothing in any record says whether the operator then slowed; the truck's own speed in the dispatch system's
  event snapshots, logged on Western Australian time while the alarm log runs on UTC, is the only record of what each
  operator did after each alarm, so how far the warnings were still believed after the March widening exists only as
  speed traces read against alarm onsets across two systems.
- **The abstraction sentence** (what a reviewer holding this build beside its nearest approved build would call the
  same): "a setting change made most of a warning system's activations false, the people it warns stopped acting on
  any activation, and incidents rose behind more warnings while the activation and acknowledgement counts read as
  more hazard caught." Written against every approved and delivered Root-Cause driver and the warning, alert and
  exposure drivers on file: task122 v4 reads a decision aid's effect at like traffic count and mix (confounding by the
  conditions of use, no warning's credibility); task129 places a rise outside a provider's zone by each unit's
  surroundings; task303 removes a shared supply loss logged under each feeder in the same minute; task111 asks which
  cause still operates forward; task202 routes an input to a lake layer by physics; task398 re-runs a rule keyed to
  the whole's own path; task190 reads errors found only where a second record exists. None is a warning whose false
  share drove the response to it. It cannot be written against any of them.
- **Semantic screen** (`guard.py mechanisms --objective root-cause`, one line per build on the insight it spends):
  task13 re-attributes outcomes from an exceptions-only log where absence means success; task11 a threshold rebate
  seen only on a rebuilt ledger; task36 a filed rule excluding the largest candidate; task50 exposure inside a funded
  window by a filed issue order; task72 the owner whose agreement covered each piece; task84 identical live units
  competing on a key nothing is keyed on; task111 which cause still operates in the forward window; task500 a
  matched-reference method pinned by certified statements; task129 a rise scaling with each unit's surroundings
  outside a provider's zone; task121 the rest before a shift rebuilt from consecutive records (and its lineage: a
  self-healing state, a second-party identity link, the same hours on other days, journey conditions, feeder
  schools); task202 the share of an input reaching the layer the response draws on; task398 a path-dependent
  counterfactual re-run on a rule keyed to the whole's own price; task399 (architecture 3, as briefed) unmet demand
  behind an empty capacity stock rebuilt from its own events, and (architecture 4) an advocate's presence in the room
  when each case was called. **Is the decisive step any of them in other nouns?** No. It rebuilds no stock, re-runs
  no system on a changed path, rebuilds no worker's state from his own consecutive records and places no exposure in
  surroundings or layers: it reads each warning against what the warned operator did in the next seconds and finds
  that the response collapsed for every operator once most warnings became false. The nearest in theme is task191
  architecture 3 (never shipped: depots' failure-to-act rates on genuine warnings once planted fixed structures were
  caught); there the false warnings were furniture inflating a count, here they are the cause.
- **The seed's own mechanism, screened explicitly against task398 and task399:** the area control centre's queue
  replay attributes delay by re-running each regulated sector's queue with a short hour restored, because a short
  hour's backlog outlives it. That is task398's insight in other nouns (an attribution holding the recorded state is
  wrong and the system has to be re-run on the changed path) and its queue is a stock of unmet demand rebuilt from its
  own arrivals and service, task399's architecture 3 insight. Every honest route to the seed's quantity (each
  mechanism's share of the summer's regulated delay) runs through that replay, so no different decisive step exists in
  the seed's data for that quantity, and the world was left.
- **Slots, run twice before any harness:** mechanism nouns (alarm, warning, acknowledge, nuisance, detection zone,
  response; three or more terms) return no slot note; setting nouns (mine, haul, haul road, light vehicle, pit,
  shovel, crusher; two or more terms) return no slot note; the candidate driver returns lexical overlaps only (task182,
  task230, task229, task270), none this insight.
- **Library test:** the golden is not a named correction. The field's measure for vehicle interaction risk (incidents
  per million hours worked by employer, circuit and shift, the hotspot read, and the system's interaction count as the
  exposure) sits at rungs 0 to 2; the decisive step is recognising that the warning stopped working as a warning, read
  from the operators' behaviour after each warning, which no report in the pack measures.
- **Sources** (every file synthetic, generated by `generator/` from seed 400, invented world, no real organisation,
  mine, vendor or person; licence CC BY 4.0, recorded in `metadata.json` at stage 3): the collision avoidance alarm log
  (the spine, UTC), the dispatch system's event snapshots (speed traces, Western Australian time), the dated tag
  register, the incident register, the two employers' hours worked, the dispatch production summary, the vendor's
  monthly dashboard, the zone configuration history, the regulator's improvement notice and the committee's programme
  terms, and distractors named in `metadata.json`.

## Default path

1. Read the committee's programme terms and the improvement notice: fund the programme that removes the cause of
   2026's rise in vehicle interaction incidents.
2. Count the incident register's vehicle interaction incidents by month and rate them per million hours worked from the
   two employers' hours: the site rate roughly triples from the second quarter of 2026.
3. Split by employer: Westray's operators, on site from April 2026, run at about two and a half times the mine's own
   rate (the field's measure, incidents per million hours by group).
4. Split by location and shift: the incidents gather at the North ramp junction and the waste circuit Westray hauls,
   with no extra night-shift share.
5. Read the vendor dashboard: interactions up more than four times as production rose, acknowledgement near 97 per
   cent, so the system is catching more hazards and operators are answering it.
6. Fund A, Westray operator retraining and supervision.

Ends on: A, Westray operator retraining (provisional figures at stage 2).

Golden: C, the collision avoidance zone and alarm redesign: read against each truck's speed after each alarm, the
share of alarms followed by a slowdown fell from about three in four to about one in five after the March widening,
for the mine's own operators as much as Westray's, and most 2026 incidents followed an alarm nobody acted on
(provisional).

## Stump sentence

A competent solver rates vehicle interaction incidents per million hours by employer, finds Westray's operators (on
site from April 2026) at about two and a half times the mine's, sees the incidents gather at the North ramp junction
and the system's interactions up more than four times as production rose, and funds A, Westray operator retraining
(Ends on: A); the step that lands it there is reading the alarms as hazards detected and the acknowledgements as
responses, when each truck's speed after each alarm shows that operators of both employers stopped slowing for alarms
once the warning zone was widened in March, so the rise belongs to the zone setting and the programme is C.

## Tried and rejected

- 2026-11-03, the seed's own world (RC06: an area control centre's summer of tripled en-route ATFM delay, the
  performance plan's characterisation of each mechanism's share), refused at the draw before any harness: (1) its
  honest decisive step, a queue replay in which a short hour's backlog outlives it, is task398's path-dependent re-run
  counterfactual and task399's capacity stock against demand in other nouns, and every honest route to the seed's
  quantity (shares of the summer's regulated delay) runs through that replay; (2) its honest strategy,
  decomposition_attribution, is held by task398 in the ban window (BLOCK ban.strategy), and so is its forcing event, a
  statutory filing; (3) Supply Chain & Logistics' only Root-Cause task type is general statistics' interpretability,
  which the author ruled a backdrop for an operations world at task129 v1, and under Human Factors the same queue is
  the decisive step again. Other ATC decisive steps were screened and each either needed the replay to price a share
  (traffic grain at the binding hour, the most penalising regulation's overlap, censored sector capacity) or read a
  field (reason codes, planned against actual demand). Moved world, dataset and domain.
- 2026-11-03, draw screens set aside before the card (each one line): an electricity network's evening-peak fuse
  operations from synchronised EV charging or load-control release (a transformer's coincident peak is task196's
  driver; the diversity factor died at task201; cold load pickup is in task398's screens); a hospital's medication
  incidents on outlier patients (task122 v4's confounding by conditions of use, and the swap to a school reads the
  same); a dispensing robot's mis-filled canisters producing runs of errors (a state rebuilt from the canister's own
  events, task121's and task399's abstraction); workers' compensation claims by mechanism developed for report lag
  (report lags spent at task130, task149 and task196); a bathing beach's source markers tested only after rain
  (selection settles the population the estimand files, the WHAT screen); children's blood lead read through
  first-draw compliance samples that miss the service line (task202's layer abstraction, and a Flint reflex); an
  ambulance service's manual handling injuries per heavy carry without a powered stretcher (an exposure construction,
  task129's family); aircraft noise complaints against event counts above 65 dB (a free dose-response form and a
  route-concentration reflex).

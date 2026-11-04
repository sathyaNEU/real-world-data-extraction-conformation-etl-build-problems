# task399 design note

Architecture 1, drawn 2026-11-04. Root-Cause Analysis, Human Factors & Ergonomics, safety-incident-error-analysis.
A rail infrastructure manager's regional operating centre (Fenmoor Rail Operating Centre, the Wyvern route,
England), whose 2027 improvement plan funds one programme against the cause that produced the most of the
operating centre's own delay minutes in the twelve months to 30 September 2026.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task399.json`, registered 2026-11-04 and re-checked as filed: WARN
  only (`driver.near` 0.13 against two task307 lineage entries that were never drawn, `repeat.question_form`), the
  older same-puzzle and same-driver notes differentiated against task107 v2 and task121 v4. Nearest drawn driver
  0.06 (task137 v3).
- **Seed:** RC05 (an electricity distributor's one reliability programme, when the costliest cause leaves no fault
  record), read through `status.py task399` only. Kept: the decision (one programme from a catalogue of five) and
  the quantity (the outcome units the funded programme's cause accounted for over the last twelve months). Its world
  was set aside at the draw: `grid-reliability-outage-analysis` holds seven cards, and its slot notes spend every
  distribution-reliability mechanism this pass could find (Tried and rejected), so the number moved to another
  client domain under the same objective.
- **Pairing:** Human Factors & Ergonomics / `safety-incident-error-analysis` (RC, AD in the taxonomy) /
  Root-Cause Analysis. The call names the cause behind the operating centre's signaller-error delay minutes, so
  that the programme placed against it removes them.
- **Shape:** 12 (drill-down to one leaf): the operating centre's delay minutes taken apart by the cause that
  produced each incident, the funded cause's minutes taken down by workstation and quarter, with the asks' tables
  (route requests by workstation and month, delay by incident type and quarter, signaller hours by competence band
  and workstation) supplying the rest of the criteria. Sized in `## Ask sheet` once the world is fixed.
- **Decision:** root_cause_named: which of the five catalogue programmes the 2027 plan funds (A signaller competence
  training, B workstation display renewal, C eight-hour shifts, D ARS timetable data rebuild, E a seventh
  workstation splitting the busiest one), and the delay minutes its cause produced in the window. The plan is
  forward facing (the 2027 programme); the quantity is retrospective by the decision's nature (a cause is read off
  the incidents it produced), the reason recorded here.
- **Strategy:** classification_error: each incident's cause is observed only through the local investigation's
  finding, which is right for decisions, omissions and late route setting and wrong for slips (booked to the
  signaller), so the observed composition of causes is a biased image the analysis rebuilds from evidence. Gap
  objective (the investigations' findings are correct records of what the investigators concluded and are not what
  the panel's but-for counterfactual scores), population second; pattern none; G3 decisive (record against
  operation: who, or what, actually produced the wrong route), G6 second (the peak hours' request mix). Gate G
  decomposition_attribution. Calibration organ none.
- **Data-native sentence:** Fenmoor's screens draw each junction's exits where the screen had room, so at a few
  dozen routes scattered across all six workstations the exit a signaller wants sits eight to twelve pixels from
  another exit of the same entrance, and every signaller who sets those routes sometimes lands on the neighbour; the
  control system logs each slip that is caught as a route cancelled within seconds and reset from the same
  entrance, and each one that is not as a train routed the wrong way, which the local investigation books to the
  signaller.
- **Abstraction sentence** (what a reviewer holding this build and its nearest approved build would say is the
  same): none can be written. The approved Root-Cause build (111) asks which cause still operates in the forward
  window; the approved physical attributions (303's sibling feeders opening in the same minute, 275's unobserved
  trips, 193's piezometer gradient) re-attribute through a shared upstream supply, an observer's coverage or a flow
  direction. None re-attributes an operator's errors to a fixed geometry of two controls, read through the
  operators' own corrected reversals.
- **Clean-truth prototype** (scratchpad `t399/proto2.py`, 20 seeds, no Layer 1 mess, every key and code correct):
  the display renewal's but-for minutes beat every rival's upper bound by 1.80 to 5.29 times; the investigations'
  findings mapped to the catalogue file competence (A) on 20 of 20 seeds, and the workload split (E) on 18 of 20
  when "distraction" is read as workload; the display's natural claim (display equipment faults) is the smallest
  figure on every seed; wrong routes per thousand requests run higher for first-year signallers on 15 of 20 seeds
  and higher in the peaks on 18 of 20.
- **WARN answers:** `driver.near` (0.13, task307 "seed OS09" and "resource adequacy draft"): both entries are
  draws dropped before any driver was written, so the similarity is lexical; task307's drawn architectures (a wear
  limit crossed inside one operating band; system equilibrium; a two-pool side-room resource) share nothing with this
  driver. `repeat.question_form` (which, against task489 and task314): the decision is a pick among five filed
  programmes, which asks which; the shell is redrawn at the role level instead (the second sentence opens on the
  panel's use of the slides, not on "Put"), and the deliverable set (pptx and xlsx) is new to the last twelve builds.
- **Furniture:** forum committee_or_panel (the route's safety review panel commits the improvement plan), forcing
  event statutory_or_regulatory_filing (the plan goes to the safety regulator by 15 December 2026, answering its July
  2026 letter on operating-centre incidents), org family utility_or_infrastructure, stakeholder the operating
  centre's safety and assurance manager (compliance_or_audit), context artifact register (the operating incident
  register). None is banned against the last three builds (task285, task489, task314).
- **People** (drawn with `guard.py names --geo England --seed 399`, the three whose first and last names no card
  carries): Helen Douglas (safety and assurance manager, keeps the incident register), Alan Pope (operating centre
  manager, signs the local investigations), Zoe Hayward (route performance analyst, keeps the delay attribution
  extracts). Invented names: Fenmoor Rail Operating Centre, the Wyvern route.
- **Sources** (all synthetic, generated by `generator/`, CC0 1.0, dated within the fiction):
  - the control system's event log for the twelve months (every route request, set and cancel, signaller and ARS),
    the spine;
  - the operating incident register with each local investigation's coded findings and narrative;
  - the delay attribution extract (every train's delay records against each incident number) and the review log of
    minutes moved between incidents;
  - the workstation display data (every signal and exit button by workstation, screen and position);
  - the four-weekly rosters and the swaps and overtime log;
  - the signaller competence register;
  - the working timetable extract (each train's booked route through each junction);
  - the improvement catalogue (the five programmes, scope and cost) and the panel's terms of reference;
  - distractors (named in `metadata.json` only): the 2025 workload assessment of the six workstations and the
    railhead adhesion log.

## Default path

1. Read the panel's terms of reference (the programme whose cause produced the most of the operating centre's
   delay minutes in the twelve months to 30 September 2026, an incident counting for a cause when it would not have
   happened without it) and the improvement catalogue (programmes A to E and the cause each addresses).
2. Join the incident register to the delay attribution extract on the incident number and total each incident's
   primary and reactionary minutes inside the window, after the review log's moves.
3. Book each incident to the programme its local investigation's underlying-cause finding names: competence to A,
   fatigue to C, ARS data to D, workload to E, display equipment to B.
4. Check the finding with the field's own measure, the error probability per opportunity: wrong routes per manual
   route request, by the performance shaping factors the records carry (signaller experience from the competence
   register, workload from requests per hour per workstation, time into shift from the rosters). First-year
   signallers' rate runs above the experienced rate, which confirms competence; the peak rate runs above the
   off-peak rate, which a reader who books "distraction" to workload takes as the workload split's case.
5. Fund the largest.

Ends on: A, signaller competence training, at the minutes the investigations book to competence (or E, the
workload split, for a reader who books distraction and the peak-hour rate to workload).

Golden: B, the workstation display renewal, at the delay minutes of the wrong routes that were slips onto the exit
drawn beside the one the train's route required.

## Stump sentence

A competent solver books the operating centre's delay minutes by each local investigation's underlying cause and
funds signaller competence training (A), confirmed by the higher wrong-route rate per request among first-year
signallers, because no column marks a slip and the investigations book every wrong route to the signaller; the wrong
routes at the routes whose exit buttons sit eight to twelve pixels from another exit of the same entrance are slips
every signaller makes in quiet and busy hours alike, and the display renewal (B) accounts for the most minutes.

## Tried and rejected

- 2026-11-04, draw, seed RC05's own pitfall (planned interruptions done de-energised, which leave no fault
  record): the costliest cause appears once the reliability standard's definition of an interruption is read
  correctly, so the decisive step is a definition (data semantics), banned.
- 2026-11-04, draw, electricity distribution: recloser lockouts turning transient faults into sustained ones
  (task198 H4 spent the completion route, and fast-trip conversion died as semantics in task188's fourth pass);
  lateral fuses switched from fuse saving to fuse blowing (task129, a dated cause an event study finds); shared
  substation supply losses (task303, approved); same-phase repeats at one point (task192); crew queueing on storm
  days (task198's queue screens); abnormal back-feeds during planned work extending outages (task194's tie flows
  are the same structure on water). The cell's drivers are spent and the world was moved.
- 2026-11-04, draw, Human Factors candidates set aside before this one: the interval since a worker last did a
  rare task, acclimatisation from the previous fortnight's shifts, and a handover splitting a task across two
  technicians (each is an exposure built from the worker's own consecutive records, task121's driver); interception
  by a later check (task275's approved driver); forklift impacts under tall loads and heat strain by the weather
  (a time join to a shipped key, readable); maintenance-induced failures after intrusive exams (a dated regime
  change an event study finds, and the post-exam window is one as-of join).
- 2026-11-04, draw, other Root-Cause cells: an airline's satisfaction against journeys broken by missed
  connections (the linkage is the step, task121 v4's death); a custody-rate rise read through the conviction
  offence (set aside in task121's architecture 4 screen); dispensing-cabinet selections onto look-alike drug names
  (tall-man lettering is the field's reflex for wrong-drug errors); coastal recirculation of a stack plume and a
  lake's internal phosphorus load (the receptor-routing abstraction task398 holds); the multilevel classroom cell
  (closed by task397's record).

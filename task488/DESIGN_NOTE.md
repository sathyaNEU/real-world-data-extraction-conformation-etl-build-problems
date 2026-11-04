# task488 design note

Architecture 2, drawn 2026-11-04: a re-root of the number into a new world, dataset, generator and prompt shell.
Architecture 1 (commissioning new items below the Approaching cut from a consortium's adaptive item bank) was found
spent at the 2026-11-02 re-check; its line is in `## Tried and rejected`, its build files are cleared from the folder
and kept in history, and its shipped pack (target.zip bfca5a21) stays at the portal, pending. This build replaces it
at ship. No seed: the world, the decision and the quantity are new.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task488.json`, architecture v2, registered 2026-11-04T07:59:59Z, v1 in
  its lineage with its fate and its prompt shell (how-many, put, csv+docx+xlsx) in `lineage_shells`. `guard.py check`
  on the filed card: WARN only. `repeat.gate_g` (etl_conformance repeats task476 v3 and task461 v3) is answered here:
  the label is the honest one, the stump sitting in a conformed recall list and section drain plan judged against the
  operator's quality procedure, on another driver in another world. `test.same_puzzle_older` against task270's ninth
  architecture (objective, G13, designation set) is a NOTE, differentiated on the card: that build read a variability
  standard at one interval from readings at others; nothing here is an interval or a variability. Nearest drivers on
  file 0.07 (task307's lineage) and 0.05 (task201 v2, task98 v1); none is a displacement front in a pipe network.
- **Window at the draw:** task192 v4, task476 v3 and task461 v3, so the strategies grain_or_unit,
  decomposition_attribution and other, the forums operations_desk, executive_team and customer_or_counterparty, the
  forcing events shift_or_daily_cycle, statutory_or_regulatory_filing and audit_or_inspection, the organisation
  families local_government, agriculture_or_food_producer and other, the roles other, compliance_or_audit and
  portfolio_manager, the artifacts filed_standard, register and operations_log, and the shapes 15 and other are off
  the table; record linkage and emissions-inventory BLOCK on pairing and subdomain.
- **Pairing:** Supply Chain & Logistics (house domain) / transportation-network / Data Extraction & Conformation (ETL),
  in its client domain General Statistics & Data Science, task type data-integration-record-linkage-entity-resolution,
  which serves ETL. The call is read from a conformed set: the fuel farm's tank line-ups, the hydrant network register,
  two into-plane agents' fuel tickets in two layouts, the truck rack's loading log and the refuellers' records
  integrated into the recall's notification list and the operator's drain plan.
- **Why this cell:** the 2026-11-04 map of the six ETL task types (task476's `## Tried and rejected`, S3.1 to S3.60)
  closes payment claims, census and register quality, official time series and test equating on mechanism, and its one
  survivor was a physical mechanism in a data-integration world; record linkage and emissions-inventory sit in the
  window, so the number moves to a house world that inherits data integration, as task472 did. Twenty-five screens of
  this draw, each one line below, died before this one was priced.
- **Shape:** 07, a grid of cells: the hydrant's sections and the refuellers, each with the fuel from the batch standing
  in it at the suspension, beside the airlines, each with its uplifts to notify and the batch litres they took, hydrant
  and refueller apart.
- **Strategy:** population_selection (exposure): which sections and uplifts the recalled batch reached is set by the
  volume each segment of the hydrant passed downstream after the batch entered it, not by the window the tank line-up
  records. Decisive generator G13 (each pit's own exposure window against the tank's line-up window), with G3 (the
  line-up record against the physical delivery) and G19 (the conformed list against the procedure). Gate G
  etl_conformance.
- **World:** Canada, Pacific time. Windrell International Airport's fuel farm, truck loading rack and hydrant system
  belong to the Windrell Fuel Facilities Corporation, which its member airlines own, and are run under contract by
  Pellacre Aviation Services, the Operator; two into-plane agents fuel aircraft from hydrant dispensers at the pits and
  from refuellers loaded at the rack. Jet A-1 arrives by products pipeline in batches; each batch is received into one
  tank, settled, recertified and released. Names are provisional until the near-name check at stage 3.
- **Forum, forcing event, organisation, role:** committee_or_panel (the corporation's fuel quality committee approves
  resumption after a quality incident), incident_or_complaint (the supplier's recall of a released batch),
  cooperative_or_member_body (an airline-owned fuel facility corporation), field_unit_lead (the Operator's fuel quality
  manager at the site, Natalie Daugherty; William Hopkins chairs the committee). Personas from `guard.py names --geo
  Canada --seed 488`; the other names it drew warn on first names held by older builds, so the logs carry initials.
- **Forcing fact:** batch J-26-1187 was released from Tank 3 and lined up to the hydrant and the truck rack at 06:00 on
  Tuesday 13 October 2026; the rack moved to Tank 1 at 12:20 and the hydrant at 15:40. At 05:12 on Wednesday 14
  October the supplier recalled the batch (FAME far above the specification), and the duty supervisor suspended
  hydrant and refueller fuelling at 05:30. The committee meets at 08:00 to approve what is drained before fuelling
  resumes and which aircraft operators are told. The call faces forward (the drain and the notices are still to do);
  its quantity is the state at the 05:30 suspension. As of 14 October 2026, 07:30 (the `--asof` for `leak.py`).
- **Data-native sentence:** the hydrant is always full and its branches end at their last pit, so fuel moves in a
  segment only while a pit downstream of it draws; the busy piers took the batch within minutes of the main line
  turning over and were flushed clean by early evening, while the cargo apron, the remote stands and the maintenance
  base drew a few uplifts a day, took the batch hours after it reached their junctions and still held it when fuelling
  stopped, and every aircraft that fuelled there overnight took it.
- **Abstraction sentence:** "a substance entering an always-full branched network reaches and leaves each outlet as the
  draws downstream of each conduit displace it, so the outlets that drew little received it late and still hold it."
  No build on file carries a displacement front through a network; the nearest drivers sit at 0.07.
- **The WHAT screen.** Population: every uplift that delivered fuel from the batch, in any quantity, and every hydrant
  section and refueller holding fuel from it at the suspension. Outcome: the batch litres standing in each and taken in
  each uplift. Window: from the batch's release to the 05:30 suspension. Unit: litres. Comparison: none beyond any
  against none. The decisive step settles none of them: it is how the records show where the batch went.
- **Deliverables:** `j26-1187_recall_uplifts.csv` (the airlines' notification list, one row per uplift that delivered
  batch fuel) and `hydrant_resumption_plan.pdf` (the committee's plan: what is drained, a schematic of the hydrant
  marking where the batch stands, the notices by airline).
- **Sources, one line each:**
  - Airport hydrant practice: an always-full pressurised network from the fuel farm's pump station to pits on the
    apron, its line fill held by section in the operator's register, fuel delivered by into-plane agents through
    hydrant dispensers whose tickets name the pit; product changes are reckoned in line fills.
  - The quality-control practice of the jet fuel industry: a released batch later found off specification is traced
    to every aircraft that may have received it and removed from every part of the system holding it before that
    part is used again.
  - `dataset-generation/references/layer1-messiness.md`: two agents' exports in two layouts (gross litres at fuel
    temperature and local time against net litres at 15 C and UTC), pit identifiers in two schemes, a re-issued
    ticket, a meter register reset at a proving, tank line-ups in the farm's own shift log.
  - The lane's spent drivers (`guard.py mechanisms --objective etl`, read in full at the draw) and the slot notes
    (`guard.py slots` on hydrant, line fill, plug flow, displaced, dead leg, branch): no build moves a substance
    through a network by volume displaced.

## Tried and rejected

- Precision of an attribute matcher carried from a small-block pilot to the full build, rebuilt from the
  per-comparison false-acceptance rate times the comparisons each block makes: the lesson is task192's
  (an instrument's error rates carry, its predictive values do not when the base rate moves) and task446
  v2's, in record-linkage nouns, so it is a repeated driver whatever the guard's lexical score (0.07).
- Resolving pairwise links into entities under a one-record-per-source constraint, chains cut at the
  weakest link: task486 architecture 2's driver, landed by its scored reader A.
- Correcting a noisy disagreement flag for its own error rates measured on known true and false links to
  estimate a barcode join's false-match share: task468's heart (linker misses and false links measured on
  control groups) and close to task456's latent class.
- Self-null coincidence rate (how often FDC's own distinct products agree on brand, serving and panel)
  applied to label-snap stubs: a paper simulation on seeds 488, 7 and 11 showed pair-level precision
  dominated by visible ties, so the tie rung lands the golden, and the per-link form needs the
  counterpart share, which no file pins.
- Clustered audit errors read with a design effect at the company prefix: task228's and task261's lesson
  (variance built at the unit the errors cluster within).
- The ET45 world's two live record-linkage candidates (value-specific agreement weights; a matcher's overconfidence carried to the auto-link band) were left unbuilt at the 2026-10-28 redraw into education at the user's request; the first had no determinate form inside the seed's world and the second's miscalibration shows to anyone who bins the review band.
- Ask layer, first form: the import's population left to the export's operational status with nothing filed on a
  revised item's keys, and enemy groups read from every version's row; the judge's pass 1 loaded both keys of the 98
  re-keyed revisions and called the one-per-item golden wrong, a fork sold as a device. Replaced by the section 1 pin
  and a version-history catalog whose 2025 accessibility versions carry the silent primary.
- Architecture 1, at the 2026-11-02 re-check: the golden is the field's own fixed-anchor calibration by marginal maximum likelihood with the launch items held at their 2021 values, applied as the textbook states it, with nothing in the data violating its precondition and a standing spread of 0. The field's method is therefore the top rung, not rung 0 or 1 (stumping 1.1b), and the honest anatomy fails Link, Reflex and Back-test. The easy routes do file wrong commissions on the clean truth (138, 116, 93), but the portal's models run this method by reflex. Spent, not re-rooted; the next step is the orchestrator's.
- 2026-11-04, architecture 2 draw, screens before the hydrant (each dead on paper, read against task476's S3.1 to
  S3.60, task274's and task486's lists and the cards):
  - Test equating, another world: anchors drifting together (the drift screen's masking) needs an outside link the
    records do not hold, and a drifted anchor dropped is cleaning (task479 v4's Gate G); testlet dependence is a model
    fork; anchors seen again by repeaters is the first-time-taker rule; mode and accommodation effects are DIF, the
    field's reflex; items calibrated in another position is task482 architecture 6; the item-family mean for new
    clones adds a term to a fitted specification (determinism-check, the identity).
  - Census and register quality: oldest-old and emigrant over-coverage by signs of life (task471 architecture 4,
    task173, task274); stock against flow sampling (task182); usual residence by duration (task485); households from a
    shared address (grain, banned in the window); an enterprise group from ownership chains (a filed SME rule);
    unrecorded cattle deaths against fallen-stock collections (task476 S3.41, an inner join); a care home capped at its
    licensed beds (S3.38).
  - Official time series: closed seasonal establishments imputed as open (S3.44, dead twice); degree-day adjustment
    (task486's screen, the textbook route); ISO week 53 in a weekly series (time semantics); the error of closure
    spread over an intercensal decade (an estimator family); first-release revision bias with a HAC test (the field's
    method, a variance step); journey factors for season tickets (S3.48, and the yield conversion task476 v3 spent).
  - Payment claims: the facility fee beside a hospital clinic's professional claim (the health economist's reflex);
    therapy units under the 8-minute rule, anaesthesia concurrency, a benefit period across facilities (filed rules);
    GLP-1 fills by the member's diagnoses (the population, the WHAT screen).
  - House worlds: a weighbridge's stored tare drifting with fuel (a model of the measurement); wood chips by moisture,
    fuel by temperature, cylinders by pressure (task476 v3's conversion at a state); a raw milk silo's dilution of a
    contaminated tanker (the field's mass balance is the golden); FIFO and FEFO lots in drive-in racking (task56 v12's
    batch running balance, and a record against an operation alone); a whisky warehouse's evaporation by cask size (a
    rate by condition); a network's device outages implying its topology (task461 v3's hierarchy from series); a
    pipeline's batch tracked by volume (the field's own method, the golden); a weight-or-cube freight driver (an
    allocation basis fork).
- 2026-11-04, the hydrant's first prototype (proto.py, session scratchpad, three seeds) put each pit on a 160-litre
  riser: every pit used during the batch then held batch fuel in its riser, so its next uplift after the trailing front
  took a sub-one-per-cent dose and the notified set grew by twenty for a reason no reader would weigh; the register's
  pits sit on the branch pipe (proto2.py, six seeds), where the routes' notified sets differ by 6 to 24 and the time
  window, one line fill and the path volume against the pump station's meter all file the hydrant clear while the
  per-segment front leaves batch fuel in the low-use branches on five seeds of six.

# task285 design note (architecture 1: the flood that closes the valley's roads a day apart)

## Draw

- **Slot.** Wave 10, oviya1301 backlog, Descriptive & Distribution Analysis lane. Seed DA35 (a research council
  funding universities on the share of 2016-2020 papers in the top 10 per cent of field and year) was read only
  through `status.py task285` and set aside at the draw: every decisive move its world offers is either Layer 1
  (collapsing preprint and journal versions into one paper) or a filed counting rule (ties at the threshold,
  fractional credit, the field-year reference set), and no client task type that serves this objective carries
  bibliometrics. The number keeps its objective and moves to Urban & Regional Science.
- **Pairing.** Client domain `urban-regional-science`, task type `network-analysis` (serves Descriptive &
  Distribution only). Objective: Descriptive & Distribution Analysis: how the valley's parishes divide between
  those a flood would cut off from the hospital by road and those it would not.
- **World.** The Leddon Valley Community Foundation (an invented community foundation in an invented English
  river valley) runs the Flood Ready Fund. For 2027 its trustees fund a community flood store, a satellite phone
  and a volunteer first-responder kit in every parish whose main village the 1 in 100 design flood (the 2025
  river model with the 2080s climate allowance) would cut off from Hawkesbridge General Hospital by road. The
  Fund's guidance files the WHAT: a village is cut off when no road route between it and the hospital is
  passable to an emergency ambulance, and the ambulance service treats a carriageway as impassable where water
  stands deeper than 0.25 m. The evidence is the model's output (hourly stage hydrographs for each floodplain
  storage area), the highways authority's surveyed road levels, the road network, the council's address
  register and the documents around them.
- **Call.** Which parishes the 2027 Flood Ready grants go to, and the households in each. Forward facing: the
  grants equip the parishes for the next flood of that size, whenever it comes; the design event is the
  planning scenario the county's flood plan already uses.
- **Shape.** 10, a scorecard against one threshold: every parish in the valley checked (cut off or not), the
  households in each one cut off, and two asks with a figure per parish and per road. About 20 parishes plus 6
  household figures plus the call, then about 20 ask figures: over 25 criteria from the structure.
- **Card.** `cards/task285.json`, registered 2026-11-04. Gate G `method_or_model_selection`, strategy
  `time_semantics` (point in time), gap objective, generators G2 (the event's envelope against the hour) and
  G16, decision `designation_set`, forum `trustees_or_governors`, forcing event `budget_or_appropriation`,
  organisation `foundation_or_funder`, role `research_desk`, artifact `filed_model`. People from `guard.py names
  --geo uk --seed 285`: Gareth Johnston (the Fund's grants manager), Lindsey Mistry (research and evaluation
  lead), Julian Woodward (the ambulance service's resilience officer).
- **Guard at registration.** WARN only. `three_rules.strategy_risk` (time_semantics) is answered in `## Three
  rules`: every field and rule read correctly still leaves the envelope route on nine parishes. `repeat.question_form`
  (which, against task398) is the decision's own form, a designation, answered at the role level in the prompt's
  wording. `repeat.deliverables` (xlsx and png, against task313): a workbook and one chart are what a funder's
  analyst sends trustees. NOTE lines `test.same_puzzle_older` (task84) and `test.same_driver_older` (task257,
  task269 v2) are differentiated on the card. Nearest drivers 0.06 (task488 v2) and below.
- **Abstraction tests.** Against task254 (approved cell neighbour, pending): task254 composes one path's travel
  time through segment delays read at the moment the vehicle reaches each segment; this build asks whether any
  path exists at each moment while links close and reopen in different windows, and its wrong route is the
  union of all closures over the event. Against task114 (approved, co-presence): task114 counts demand created
  when two parties share a site after a merger; here closures that never share an hour create no isolation, and
  their union over the event creates isolation that never happens.
- **Data-native sentence.** The valley's tributary becks fill their storage areas and drain them while the
  Leddon is still rising, so the ridge road's dips are under water a day before the river road's are, and a
  village with a road each way always keeps one of them open, which a map of the deepest water the flood ever
  reaches cannot show.

## Default path

1. Read the Fund's guidance (cut off: no route to the hospital passable to an ambulance; impassable where water
   on the carriageway is deeper than 0.25 m) and the model report (the 2025 model supersedes the 2023 run).
2. From `storage_area_stages_2025.csv` take each storage area's peak stage over the design event.
3. Join each surveyed road point (`road_levels_survey.csv`, re-keyed to the 2025 link identifiers through the
   asset upload's crosswalk) to its storage area; a point's depth is the peak stage less its surveyed level.
4. Close every link with any point deeper than 0.25 m: the field's map of the deepest water the event reaches,
   laid over the network, which is how a flood plan lists communities at risk of being cut off.
5. Search the remaining network from the hospital and list every main village it cannot reach.
6. Count each such parish's dwellings on the address register.

Ends on: nine parishes, Hollinside, Sawley Bridge, Marrowby, Kelderby, Ellingthorpe, Brantwell, Netherhay,
Wendle and Wyke End.
Golden: six parishes, Hollinside, Sawley Bridge, Marrowby, Netherhay, Wendle and Wyke End.

## Stump sentence

A competent analyst closes every link whose surveyed points would stand under more than 0.25 m of water at its
storage area's peak and files nine parishes (Hollinside, Sawley Bridge, Marrowby, Kelderby, Ellingthorpe,
Brantwell, Netherhay, Wendle and Wyke End); the step that lands it there is closing at once links that are
never closed in the same hour, because the becks' storage areas have drained before the Leddon's fill, so
Kelderby, Ellingthorpe and Brantwell keep the ridge road or a river bridge open at every hour and six parishes
qualify.

## Tried and rejected

- Seed DA35, citation normalisation (2026-11-04, at the draw): the version-family collapse is Layer 1, ties at
  the field-year threshold and fractional credit are filed counting rules, and no client task type serving
  Descriptive carries bibliometrics; the number moved domain.
- Trap saturation in single-catch kill traps checked weekly or monthly (GSDS censoring, 2026-11-04, a probe
  card only): the latent rate recovered by inverting a saturating observation map is task184 v8's spent driver
  (the reader reached the inversion unaided, and the grouping it is fitted over forked the figure, stumping
  1.1j), and the estimator is a model of the measurement (1.2c).
- Coordinated omission in a closed-loop load test (product analytics): task273 architecture 1, spent at stage
  4; task280 holds the same abstraction.
- Testlet reliability and decision consistency at a cut (education psychometrics): spent in task262, task265,
  task123 and task236's notes; task269 v2's G-study died at stage 4.
- Flood isolation read off the envelope against per moment, first framed with "at some time" in the estimand:
  the clause names the clock the step rides on (readability test 1); the guidance files cut off as a state of
  the network and nothing names the hour.
- A capacitated dialysis catchment solved as a maximum flow: task106's shared-pool double-booking device
  re-skinned (task177 records the same), so it was not drawn.
- Network criticality under congestion (user equilibrium after each link removal): task253's lineage and
  task307's note, where the equilibrium on the coded network was the golden and the analyst test failed.
- A wheelchair's swept turning circle by drive type and fitted accessories against a turning space (human
  factors design fit): the configured length adds to the stated diameter almost linearly (readability test 6)
  and the abstraction sits beside task276's stated range against the user's own posture.
- Ventilation per pupil from classroom CO2 decay against the steady-state method: physical, exact and unspent,
  but no client task type serving Descriptive holds it (indoor air sits in environmental monitoring, Anomaly
  Detection and Data Quality only).
- Library visits displaced by a branch closure: diversion is spent ("a line's absence is the category's loss
  only net of diversion") and the counterfactual share is a model.
- Household-specific inflation from diary weights: the per-household computation is the natural reading of the
  estimand, and two-week diaries make the weights noisy (task262's transitory-variance lesson).
- An EPC register carried to today by later retrofit measures: re-dating records to a reference date is ETL
  (task259's carry), and the recommendation uplifts are sequential and not additive.
- FX last-look rejections, care-home falls with held beds, aliasing, segregation indices, MRP, legislative
  cohesion, survey multiplicity, adherence variants and out-of-home loop audiences: each already dead in
  task276's and task281's screen lists for the reason recorded there.

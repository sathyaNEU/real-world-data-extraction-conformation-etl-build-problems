# task249 design note

## Draw

Card `cards/task249.json` (architecture 1, registered 2026-10-18). Guard verdict WARN, no BLOCK. test.same_puzzle_older
and test.same_driver_older are NOTEs, differentiated on the card against task104, task134 (v1 lineage), task236,
task453 (v1 lineage), task463, task501 (v4 lineage) and task70 (v2): none of them reads a unit's gain against
references elsewhere. Each WARN, answered: overuse.objective (Data Quality Monitoring in 4 of the last 12): the lane is
Data Quality Monitoring & Alerting; repeat.gate_g and overuse.gate_g (method_or_model_selection after task268): the
decisive step is the choice of estimator for a filed quantity, and no other key is true of it. Nearest driver 0.06
(task253 v3 lineage).

- **Pairing.** Physical & Environmental Sciences / sensor-calibration-measurement, a task type serving Data Quality
  Monitoring; not banned against the last three builds (task165 urban forecasting, task268 survey descriptive, task248
  epidemiology data quality). The object is the health of a low-cost ozone network's data, how far each node's span has
  drifted from true ozone since the heads were set at installation, and the call is a monitoring decision: which nodes
  go on the pull list for recalibration at the June 2028 round, before the summer ozone season.
- **The seed, re-found.** DQ22 gave the world (a low-cost sensor network serviced in rounds), the decision (the pull
  list for the next maintenance round) and the quantity (each sensor's drift against a tolerance). Its pitfall (the
  direction of the calibration regression at a collocation) belongs to a sensor sitting beside its reference; here no
  node sits beside one, and the decisive step is how a node's span is read against analysers kilometres away.
- **Niche.** A public research foundation in the Spanish interior runs 36 low-cost ozone nodes (gas-sensitive
  semiconductor heads) on school and municipal roofs across a comarca, beside the regional government's four reference
  analysers (UV photometry). The heads were set against a reference at installation in autumn 2027; their span (the
  change in the reading per unit change in true ozone) drifts over months. At each maintenance round the contractor
  pulls the nodes on the list, takes them to a reference station for a week, and resets them.
- **The call.** Which nodes go on the pull list for the June 2028 round, judged on each node's span over the eight
  weeks to 31 May 2028 against the quality plan's band of 0.85 to 1.15.
- **Shape.** 10, a scorecard: each of the 36 nodes against the band, the list, the count, each listed node's direction,
  and the asks; over 25 criteria. Decision designation_set, answer set_of_items, question form which.
- **Strategy.** other, named in the card's notes: an errors-in-variables attenuation from a remote reference. G16
  decisive (which estimator of a filed span), G5 beside it; gap population (the analyser's hourly series is not the air
  at the node's inlet); Gate G method_or_model_selection; calibration none (no corpus of settled outcomes ships; the
  analysers' own record shows the shared regional distribution); context artifact filed_standard (the network's quality
  plan); Layer 2 family estimation_fit, pattern own:span-from-distributions-against-a-regional-reference-not-paired-slope.
- **Forum, event, organisation.** operations_desk (the network coordinator sends the list to the maintenance
  contractor), season_or_peak (the June round is the last before the summer ozone season), research_or_statistics_office
  (a public research foundation). Role field_unit_lead (the network coordinator).
- **People** (`guard.py names --geo Spain --seed 249`, locale es_ES): Matilde Criado, the network coordinator, who
  asks; Adán Ruano, the contractor's field technician; Edelmira Urrutia, the regional network's data officer; Paulino
  Cardona, the centre's sensor scientist. None appears in the prompt.
- **Data-native sentence.** Ozone is a regional pollutant, so the background sites of a comarca share one distribution
  of hourly ozone over weeks, but two sites kilometres apart agree only partly hour by hour (a shower, a sea of cloud, a
  plume reaching one and not the other), and a slope fitted on paired hours is pulled toward zero by exactly that
  partial agreement: a healthy node far from every analyser looks as if it has lost span, and a node whose span has
  risen looks healthy.
- **As-of.** Thursday 1 June 2028, after the export of 31 May and before the round of 12 June.
- **Sources.** The client's two-layer standard (estimation_fit); the low-cost sensor literature's proxy methods for
  network calibration (a node's distribution over a window matched to a nearby regulatory station's, used for drift
  detection in dense ozone networks) and the regression-dilution result for a slope whose regressor carries error. No
  build on file reads a sensor's gain against a reference elsewhere through the spread of their distributions (task241
  compares a float with a reference on a conserved coordinate; task246 removes measurer offsets from single readings;
  task262 carries a reliability ratio from a selected subsample).

## Tried and rejected

- Drift forecast from the cumulative particle load through an optical PM sensor (drift accrues with dose, not calendar
  time): the lesson is task46's (a rate law stationary only in cumulative service exposure), so the driver is spent.
- Seasonal confounding of a PM sensor's gain by humidity growth or aerosol type: the shape of task248's driver (a
  covariate moving over the year against a level comparison), one build earlier.

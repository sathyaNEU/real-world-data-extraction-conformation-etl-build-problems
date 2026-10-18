# task247 design note

## Draw

Card `cards/task247.json` (architecture 1, registered 2026-10-18). Guard verdict WARN, no BLOCK. The one WARN,
repeat.gate_g (method_or_model_selection after task172), is answered here: task172 selects a forecast method by
back-testing renewals, while here the choice is between correcting a provisional record by its average past error and
refilling its cloud gaps from the observations on both sides once the season has closed, and nothing is back-tested on
a filed criterion. Nearest driver 0.06 (task138 v1 lineage, task458 v1 lineage, task245, task70 v1, task123 v2).

- **Pairing.** Physical & Environmental Sciences / environmental-monitoring-exceedance, a task type serving Anomaly
  Detection and Data Quality Monitoring; drawn for Data Quality Monitoring & Alerting. Not banned against the last three
  builds (task170 healthcare forecasting, task244 survey research data quality, task172 general statistics
  forecasting). The object is the health of the provisional sea surface temperature record the station's bleaching
  alerts were declared on (how far its cloud-filled days moved each reef's heat stress), the call a monitoring
  decision: which reefs' declared alert levels stand on the reprocessed record, and so which reefs the post-bleaching
  survey visits.
- **The seed, re-found.** DQ20 gave the world (alerts raised on provisional monitoring data and scored once the record
  is reprocessed), the decision (each alert kept, changed or withdrawn) and the quantity (the alert scored against the
  reprocessed record on the event it claimed). Its air quality network was left: a rule replayed on its own archive is
  a direct count, the drift and calibration stumps that network could carry belong to the lane's own seeds task249 to
  task252, and the forward versions it allows (analysers ageing, a calibration interval lengthened) teach the
  exposure-clock lesson task46, task132 and task134 v2 already teach. A reef heat-stress watch keeps every element:
  weekly alert levels declared on a near-real-time satellite analysis, a reprocessed record months later, and the alert
  scored on the heat it claimed.
- **Niche.** A public university's reef station on the Caribbean coast of Quintana Roo runs a coral bleaching watch for
  16 reef sites: each week it declares each site's alert level from the degree heating weeks of the near-real-time
  satellite sea surface temperature analysis (HotSpots of a degree or more above the site's maximum monthly mean,
  summed over twelve weeks); the reprocessed analysis, built later with every satellite pass and the in situ records
  that arrive afterwards, is the record of reference and is released the following May. The station's post-bleaching
  survey, sent in November, visits the sites the reference record will put at Alert Level 2.
- **The call.** Which of the 16 sites go on the November 2027 survey list: a site goes when its 2027 season maximum
  degree heating weeks on the reprocessed record reach Alert Level 2 (8 degree-weeks); each site's level declared on the
  near-real-time record is confirmed, raised, lowered or withdrawn accordingly.
- **Shape.** 01, a ranked list under a line: per site the estimated maximum degree heating weeks on the reprocessed
  record, its level and its verdict against the declared level (16 sites by three), the survey list and its count, the
  site nearest the line below it, a chart of each site's declared and estimated heat stress against the alert levels,
  and the asks, well over 25 criteria. Decision renew_replace_lapse, answer set_of_items, question form which.
- **Strategy.** maturity_censoring: the provisional record is not the record the decision is scored on, and its
  unfinished part is the cloud-filled days. G13 decisive (a filled day carries only what was known that day, while the
  reference record fills it with the observations after it as well), G12 (a filled value is the analysis's absence of an
  observation written as a temperature), G16 (the provisional record corrected by its mean error, by flag, by site, or
  refilled from both sides); gap population (a filled day is not an observation of the sea) then time; Gate G
  method_or_model_selection; calibration parallel_run_overlap (nine seasons with both records); context artifact
  operations_log (the weekly alert bulletins); Layer 2 family estimation_fit, pattern
  own:hindsight-refill-of-gaps-a-real-time-analysis-relaxed-to-climatology.
- **Forum, event, organisation.** line_manager_or_team (the station's head of reef monitoring signs the survey list),
  season_or_peak (the close of the June to October heat-stress season and the November survey window),
  university_or_school (a public university's marine station). Role field_unit_lead (the survey's coordinator, who
  asks). None of the three is used by task170, task244 or task172.
- **People** (`guard.py names --geo Mexico --seed 247`, locale es_MX): Fabiola Mireles, the survey coordinator, who
  asks; Alfredo Montero, the station's head of reef monitoring; Rocío Muñiz, the remote sensing analyst who issues the
  bulletins; Hernán Pichardo, the dive team leader. None appears in the prompt.
- **Data-native sentence.** The near-real-time analysis has to say something every day, so on a day cloud hides a reef
  it keeps the last clear-sky anomaly and lets it decay toward climatology; that costs nothing in ordinary weeks and a
  great deal when the cloud is a stalled trough over a hot sea, because then the filled days slide back toward normal
  exactly while the HotSpots should be accumulating, and the reprocessed record, which fills the same days with the
  observations that come after them, will not.
- **As-of.** Wednesday 3 November 2027, before the survey's field trip; the 2027 reprocessed record is due in May 2028.
- **Sources.** The client's two-layer standard (estimation_fit: an estimate that ignores how the data were made) and
  the real coral bleaching heat-stress method (HotSpots above the maximum monthly mean, degree heating weeks over
  twelve weeks, Alert Levels 1 and 2 at 4 and 8 degree-weeks). No build on file uses a satellite analysis, a sea
  surface temperature record or a reef (`guard.py slots` finds no screen on them).

## Tried and rejected

- 2026-10-18, the seed's own air quality network, the alert rule replayed on the archived provisional data against the
  ratified data: a direct count with no analytical step; with the provisional data overwritten, rebuilding them from
  the calibration log executes the network's ratification procedure (rule application).
- 2026-10-18, the alert log as the only record of provisional readings, its over-readings selected by the alarm itself:
  any treatment of the hours that did not alert lands the golden (a coin flip on one insight), the share over all
  hours at the level is read off the filed population (a semantics risk), and the observed misses refute the naive
  error model at once.
- 2026-10-18, verification by reference filters weighed for every alert day and a third of the others: the weighing
  design has to be filed, which makes the weights the obvious move, and a design-weighted estimate is task452's lesson.
- 2026-10-18, analysers' span drift growing with their age (or with the pollutant dose they have measured) and next
  season's analysers older: the exposure-clock lesson of task46, task132 and task134 v2; analyser drift by age swaps
  into any field's instruments unchanged; and the forward allowance reads as a forecast.
- 2026-10-18, a season's calibration-function change as one draw, the rule judged over the draws on record: which
  seasons stand for the coming one is the estimand's population, so filing it hands the step over and leaving it open
  is not determinate.

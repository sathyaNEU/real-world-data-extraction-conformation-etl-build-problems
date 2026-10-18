# task245 design note

Architecture 1, wave 4, seed DQ18 (which monitoring sites' annual compliance statistic is reportable): the seed's
world (a monitoring network's annual statistics), decision (which sites' statistic goes out as it stands and which
carries a data-capture flag) and quantity (each site's annual count of days above a daily limit) only. The seed's
pitfall is a data-capture rule (counting exceedances over whatever readings arrived), which executed is rule
application, so the pitfall is re-found in the data: the analysers that fault under heavy loading lose exactly the days
a bulk terminal's dust plume blows onto them, so a station's lost days are not like its reported days and have to be
rebuilt from the day's wind and the rest of the network.

Thornmouth (a fictional coastal borough in north-east England): the council's air quality team runs seven automatic
monitoring stations; the operator of the Thornmouth Bulk Terminal runs five PM10 stations around the terminal under its
environmental permit and shares their data with the council; the council's QA/QC contractor audits the network's 2027
data before the council's Annual Status Report. The UK air quality objective for PM10 is real: a 24-hour mean of 50
micrograms per cubic metre, not to be exceeded more than 35 times a calendar year.

## Draw

Card `cards/task245.json` (architecture 1, registered 2026-10-18). Guard verdict PASS; the one NOTE
(test.same_puzzle_older against task265 v1) is differentiated on the card: task265 corrects a survival curve's risk set
for units the record saw only after their start, while here every day of the year is in the population and the record
loses the heaviest days as they happen. Nearest driver task229 v3 at 0.06.

- **Pairing.** Physical & Environmental Sciences / environmental-monitoring-exceedance, a task type serving Anomaly
  Detection and Data Quality Monitoring; drawn for Data Quality Monitoring & Alerting. Not banned against the last three
  builds (task164 energy load forecasting, task162 product feature adoption, task163 economics forecast evaluation).
  The object is the health of each station's 2027 record (whether the days its analyser lost change its standing
  against the objective), the call a monitoring decision: which stations' 2027 PM10 results go to the audit and into
  the Annual Status Report with the data-capture note.
- **Niche.** A borough network's data-capture review before its annual report: the PM10 objective counts days above
  50 over a calendar year, the stations around a bulk terminal see its dust only on their own wind bearing, and the
  terminal operator's older analysers fault on the heaviest hours and stay down until the next working-day visit.
- **The call.** Which of the 12 stations have a 2027 count of days above 50 over their valid days of 35 or fewer while
  their count over the whole year, every day counted (the days without a valid daily mean included), is more than 35;
  those stations cannot be reported as meeting the objective and carry the data-capture note.
- **Shape.** 10, a scorecard of metric-threshold checks: per station the count over valid days, the whole-year count
  with its accepted range and the note (12 stations), the noted set, the chart (each station's two counts against the
  35-day line) and the asks' per-station figures, well over 25 criteria before the rubric folds them. Decision
  designation_set, answer set_of_items, question form which.
- **Strategy.** population_selection: the reported days are a selected population, the year is the estimand. G9
  decisive (the reported days are the days the analyser survived, and it does not survive the heaviest hours), G12 (a
  lost day is the absence of a record, not a record of a clean day), G16 (a station's lost days filled from its own
  reported days, from the network alone, or from the network plus the station's own response to the wind); gap
  population; Gate G decomposition_attribution (each station's level split into the network's background and the
  terminal's plume by the hour's wind); calibration none; context artifact monitoring_export (the council's and the
  operator's hourly exports); Layer 2 family estimation_fit, pattern own:informative-outage-plume-sector-infill.
- **Forum, event, organisation.** auditor (the council's QA/QC contractor, whose annual audit signs off the network's
  2027 statistics before the report), audit_or_inspection (the audit closes on the 2027 data year), local_government
  (Thornmouth Borough Council). All clear the last three (task162, task163, task164: committee_or_panel,
  executive_team, regulator_or_inspector; cutover_or_migration, budget_or_appropriation, statutory_or_regulatory_filing;
  software_or_platform, professional_services, utility_or_infrastructure). Role compliance_or_audit (the council's air
  quality officer, who answers to the auditor), clear of field_unit_lead, finance_controller and programme_officer.
- **People** (`guard.py names --geo "United Kingdom" --seed 245`): Harriet Hopkins, the council's air quality officer,
  who asks; Marc Bevan, the QA/QC contractor's auditor; Jemma Holloway, the terminal operator's environmental manager,
  who sends the operator's export. None appears in the prompt.
- **Data-native sentence.** The terminal lies on a fixed bearing from each station, so its dust reaches a station only
  on the hours the wind blows from that bearing, and the operator's older analysers fault under exactly that loading
  and stay down until the next working-day visit; each such station's lost days are its plume days, not a random part
  of its year, while the rest of the network, off that bearing, reads an ordinary day.
- **Sources.** The client's two-layer standard (estimation_fit: an estimate that ignores the data's structure; here
  the structure is informative loss, the losses falling on the outcome's high values). layer2-rigor-patterns.md has no
  patterns for this domain, so the pitfall comes from the family, not a listed pattern. The seed DQ18 gave the world,
  the decision and the quantity only. UK local air quality management practice gave the reflexes the ladder is built
  against (data capture, the 90.4th percentile of daily means reported where capture is short, the expected-exceedance
  scaling a US reader brings), each of which treats the lost days as like the reported ones. The field's own tool for a
  station against the wind (the bivariate polar plot of concentration by wind direction and speed) is the decisive
  step's instrument; nothing in the pack names it.
- **Mechanisms on file** (`guard.py mechanisms --objective data-quality-monitoring`, 16 builds), the insight each
  spends: 229 a convex conversion of a daily mean (and, in lineage, a shared-parent standard error, checks seen just
  before reset, gated arrivals); 231 exits reaching the record late; 232 a transmission rate from delayed closed
  episodes; 230 a late channel moving items to default categories; 228 events clustered within randomised units; 233 a
  gold-standard follow-up carried across base rates; 234 a share in a source's output that transit loss cannot move;
  235 an item lost only once its device had its next chance; 236 a capture change changing which cases are reached; 237
  the share of a composite's variance due to its attribute; 238 a channel effect through a randomised nudge; 239 a
  group-level factor; 240 the error of a post-stratified total; 241 a sensor's error against a reference at a
  displaced position; 242 a detector whose sensitivity fades with time since the event; 243 a growth balance carrying
  movement. None spends losses that fall on the outcome's own high values, rebuilt from a driver the record does not
  lose.

## Tried and rejected

- A regional-dust design in a Spanish network (every station sees the same Saharan intrusions, the golden filling each
  station's lost days from the other stations that day): rejected at the draw; filling lost days from correlated
  stations is the generic imputation reflex and would land the call, and the pack's working documents would be in
  Spanish.
- TEOM stops driven by cumulative filter loading since the last filter change: rejected in prototype; the stops fell on
  ordinary days as often as on plume days, so the losses carried little information and interpolation in time
  recovered most of the lost exceedances.
- A daily plume with a narrow, speed-sensitive kernel: rejected in prototype; a station's valid days on its bearing were
  too weak to predict its lost plume days, so the wind-aware rebuild itself fell under 36 for two stations.

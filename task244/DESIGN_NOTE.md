# task244 design note

## Draw

Card `cards/task244.json` (architecture 1, registered 2026-10-18). Guard verdict WARN, no BLOCK. The one WARN left,
repeat.decision (designation_set after task246), is answered here: the candidates are a grid of 24 published rates
(twelve survey districts, a job-finding and a job-loss rate each), not a list of sites or offices, and the question is a
whether (can the release go out without the warning, and if not on which rates), so the prompt does not take the
"which of the twelve carry the note" carrier of task243, task245 and task246. The people WARN (a recycled first name)
and the overuse WARNs (government_agency, method_or_model_selection) were cleared by redrawing those axes. Nearest
driver 0.05 (task229 v2 lineage, task465, task266, task246, task267 v0).

- **Pairing.** Survey Research & Official Statistics / nonresponse-calibration-measurement-error-adjustment, a task type
  serving Descriptive & Distribution Analysis and Data Quality Monitoring; drawn for Data Quality Monitoring & Alerting.
  Not banned against the last three builds (task168 supply chain transportation network, task167 grant-making other,
  task246 general statistics measurement error). The object is the health of the flows the bureau publishes (how much
  of each published labour market flow is classification error rather than people moving), the call a monitoring
  decision: which published rates go out under the classification-error warning in the 2027 annual flows release.
- **Niche.** A state bureau of statistics' quarterly labour force survey interviews each household in four consecutive
  quarters, so each matched pair of quarters gives a person's labour force status twice and the bureau publishes, per
  survey district, the job-finding rate (unemployed to employed) and the job-loss rate (employed to unemployed). A
  supervisor reinterviews a random subsample of each quarter's respondents and reconciles every difference with the
  respondent; the reconciled status is the bureau's measure of a person's true status.
- **The call.** Whether the 2027 annual flows release can go out without the classification-error warning, and if not,
  which of the 24 district rates carry it: a rate carries the warning when a third or more of the moves it counts are
  not real moves (persons counted as moving between the two statuses whose true statuses in the two quarters were not
  that pair).
- **Shape.** 07, grid of cells: 12 districts by 2 flows, per cell the published rate, the share of its counted moves
  that are not real moves and the warning (24 cells, 72 figures), the warned set and its count, plus the asks (per
  district figures), well over 25 criteria. Decision designation_set, answer set_of_items, question form whether.
- **Strategy.** other: the decisive move inverts the reinterview's misclassification matrix at both quarters of every
  matched pair (the true flows), which no strategy key names; it is regression to the mean from classification error
  (a counted move is far likelier than a random record to be a misreading of someone who stayed put). G2 decisive (what
  one counted move is: a recorded pair of statuses, not a move), G16 (the share of real moves taken as the product of
  the two ends' predictive values, as the product of their correct-reading rates, or from the inverted matrix); gap
  time (two readings of a persistent status manufacture change between them) with population second; Gate G
  signal_vs_noise_or_hold (the warning marks rates whose counted moves are largely misreading); calibration
  gold_standard_subsample (the reconciled reinterview, a random subsample re-read and reconciled with the respondent);
  context artifact published_series (the bureau's flows tables); Layer 2 family estimand_identification, pattern
  own:true-flows-by-inverting-misclassification-at-both-ends.
- **Forum, event, organisation.** committee_or_panel (the bureau's release clearance committee, which clears each
  release and its quality notes), period_close (the 2027 annual flows tables, released in February 2028 once the
  year's four quarter pairs are closed), research_or_statistics_office (the state bureau of statistics). Role
  statistical_office_head (the Director of Labour and Social Statistics, who signs each release's quality note). Every
  axis clears the last three builds (forums executive_team, board_of_directors, operations_desk; events season_or_peak,
  vote_or_meeting, other; organisations other, foundation_or_funder, local_government; roles capacity_planner,
  compliance_or_audit, programme_officer; artifacts filed_standard, close_out_summary, monitoring_export; strategies
  population_selection, forecast_method_backtest, decomposition_attribution; calibration forms prior_period_close_out,
  none, other; shapes other and 14).
- **People** (`guard.py names --geo Nigeria --locale yo_NG --seed 244`; `--geo Nigeria` alone falls back to en_US):
  Atinuke Adebisi, the Director of Labour and Social Statistics, who asks; Babasola Oginni, the head of field
  operations, whose supervisors run the reinterview; Comfort Olawale (en_NG draw), the survey methodologist; Ronke
  Shekoni, the release clearance committee's secretary. None appears in the prompt.
- **Data-native sentence.** Each household's members are read four times a quarter apart, most adults stay employed or
  outside the labour force from one quarter to the next, and an employed adult is now and then recorded as unemployed
  (a lost day's work read as a search, a job between contracts); because the employed stock is many times the
  unemployed stock and the true job-loss rate is a percent or two a quarter, those single misreadings make up a large
  part of every counted move into and out of unemployment, and only the reinterview, which re-reads a random
  subsample and reconciles it with the respondent, measures the misreading.
- **Sources.** The client's two-layer standard (estimand_identification: regression to the mean; a measured change that
  is partly the measurement's own noise) and the task type's pattern 3 in layer2-rigor-patterns.md (prevalence
  corrected for sensitivity and specificity from a record check; shortcut: the observed share, or divide by the
  sensitivity alone); here the correction is of a transition between two readings, not of one prevalence, and the
  shortcut that bites is multiplying the two ends' predictive values. Labour statistics practice gave the method (the
  true flows recovered by inverting the reinterview's misclassification matrix at both ends of the matched pair, as in
  the gross-flows adjustments of Abowd and Zellner and of Poterba and Summers). The seed DQ17 gave the world, the
  decision and the quantity only.
- **Mechanisms on file** (`guard.py mechanisms --objective data-quality-monitoring`, 18 builds), the insight each
  spends: 229 a convex conversion of a daily mean; 231 exits reaching the record late; 232 a transmission rate from
  delayed closed episodes; 230 a late channel moving items to default categories; 228 events clustered within
  randomised units; 233 a gold-standard follow-up carried across base rates; 234 a share in a source's output that
  transit loss cannot move; 235 an item lost only once its device had its next chance; 236 a capture change changing
  which cases are reached; 237 the share of a composite's variance due to its attribute; 238 a channel effect through a
  randomised nudge; 239 a group-level factor; 240 the error of a post-stratified total; 241 a sensor's error against a
  reference at a displaced position; 242 a detector whose sensitivity fades with time since the event; 243 a growth
  balance carrying movement; 245 losses falling on the outcome's own high values; 246 a measurer's offset and field
  error out of a tail share. None spends a change between two readings manufactured by misreading either of them.

The call is retrospective by design: the four quarter pairs of 2027 are closed and the warning is a monitoring decision
on their published flows; what faces forward is the release (the annual flows tables go out in February 2028 and stand
until the 2028 tables replace them).

## Tried and rejected

- 2026-10-18, architecture 0 (the seed's own world, coded write-ins and a recode): the net against gross difference
  rate decides only by reading a definition (data semantics); correlated coder variance through interpenetrated
  workloads repeats task228's lesson (variance built at the unit that carries many records); a fallible expert recode
  repeats task246; error rates carried route by route repeat task230 and task242; a fixed take per coder or batch is
  one reweighting (an opponent reflex); acceptance-sampling outgoing quality reads the same with factory lots (fails the
  swap). World moved to the labour force survey's panel flows, keeping the reinterview, the published categories and
  the classification error.
- 2026-10-18, laboratory proficiency testing with results below each laboratory's reporting limit: dropping or
  substituting the censored results moves the consensus by about 3 per cent at realistic censoring, too little to move
  a laboratory across the action line with margin; and censored results are listed as Layer 1 mess for this domain.

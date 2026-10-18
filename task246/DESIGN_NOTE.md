# task246 design note

Architecture 1, wave 4, seed DQ19 (how many public alerts a monitoring network should have issued, and the alert
configuration that follows): the seed's world (a surveillance network whose figures feed public alerts), decision (the
configuration each site's alert figure is published on) and quantity (each site's alert figure) only. The seed's
pitfall is an averaging-period reading (data semantics), so the pitfall is re-found in the readings: every figure the
network publishes is a measurer's reading of a child, and the readings carry each survey team's tape offset and field
error as well as the child's arm, so the share below the wasting cut-off has to be read from the children's own
distribution, net of the measurers.

A fictional arid county in northern Kenya: the county government's Department of Health runs a long-rains nutrition
surveillance round each year in twelve survey zones (its sub-counties split by livelihood zone), with two partner
NGOs' survey teams measuring children aged 6 to 59 months in sampled clusters; each zone's wasting prevalence by
mid-upper arm circumference (MUAC under 125 mm, or bilateral oedema) goes into the county's monthly early warning
bulletin, where it sets the zone's public nutrition alert. Every measurer and the survey supervisor take a
standardisation test before the round and a refresher mid-round, reading the same children twice. The MUAC cut-offs
and the standardisation test are real practice; the county, its zones, the partners and every person are invented.

## Draw

Card `cards/task246.json` (architecture 1, registered 2026-10-18). Guard verdict PASS; the two NOTEs
(test.same_puzzle_older and test.same_driver_older against task266 v1) are differentiated on the card: task266 builds a
completion share from competing endings' hazards among students still enrolled, while here each child is measured once
and the share comes from splitting each reading into the child's own arm and the measurer's offset and field error.
task198's spent v2 (interviewer effects inferred from the survey data through measurers who crossed regions) is
differentiated too: here the measurers' offsets and errors are measured directly against a supervisor on the same
children. Nearest driver task198 v2 (lineage) at 0.09.

- **Pairing.** General Statistics & Data Science / missing-data-censoring-measurement-error, a task type serving
  Descriptive & Distribution Analysis and Data Quality Monitoring; drawn for Data Quality Monitoring & Alerting. Not
  banned against the last three builds (task471 survey register quality, task166 banking stress testing, task198 survey
  anomaly detection). The object is the health of each zone's MUAC readings (how far the measurers' error moves the
  zone's published wasting figure), the call a monitoring decision: which zones' figures carry the measurement note and
  go into the bulletin at their error-free value.
- **Niche.** A county surveillance round's measurement note: each zone's MUAC readings were taken by one to three
  teams, each team's anthropometrist has a tape offset (a tight or loose pull, a misread window) and a field error
  against the supervisor, both found in the standardisation test, and the note is carried where the measurers' error
  raises the zone's wasting prevalence by two points or more.
- **The call.** How many of the twelve zones' 2027 long-rains wasting figures carry the measurement note, and which:
  a zone carries it when the wasting prevalence read from the normal distribution of its readings exceeds the
  prevalence read from the normal distribution of its children's own MUAC by two percentage points or more.
- **Shape.** 14, cuts of a distribution per segment: per zone the readings' prevalence, the children's own prevalence
  with its accepted range, the measurement points and the note (12 zones), the noted set, a chart of the two
  prevalences per zone against the alert bands, and the asks' per-zone figures, well over 25 criteria. Decision
  designation_set, answer set_of_items, question form how-many.
- **Strategy.** decomposition_attribution: each zone's readings split into the children's own arm and each team's
  offset and field error. G17 decisive (the error-free distribution needs the measurement error estimated and taken
  out, not assumed away), G16 (the error taken as the repeat readings' technical error, as the error against the
  supervisor, with or without the offsets); gap population (the readings are not the children); Gate G
  decomposition_attribution; calibration other (the standardisation test, each measurer and the supervisor reading the
  same children twice); context artifact filed_standard (the county's surveillance protocol); Layer 2 family
  estimation_fit, pattern own:measurer-offset-and-field-error-out-of-the-spread.
- **Forum, event, organisation.** operations_desk (the county's early warning bulletin desk, which publishes each
  zone's alert from the round's figures), season_or_peak (the long-rains round closes before the short-rains season's
  response is set), local_government (the county government's Department of Health). All clear the last three
  (task471, task166, task198: customer_or_counterparty and committee_or_panel; vote_or_meeting,
  purchase_order_or_contract and period_close; government_agency, financial_institution and
  research_or_statistics_office). Role field_unit_lead (the county's nutrition information officer, who runs the round
  and signs off its figures), clear of programme_officer, portfolio_manager and research_desk.
- **People** (`guard.py names --locale en_KE --seed 246`; the geography's own locale, `--geo "Kenya"` falls back to
  en_US): Winny Karisa, the county's nutrition information officer, who asks; Purity Maina, the round's survey
  supervisor, who reads the standardisation children as the reference; Barasa Kahindi and Caroline Nthenya, the two
  partner NGOs' survey coordinators; Kelvin Omollo, the early warning bulletin's drought information officer. None
  appears in the prompt.
- **Data-native sentence.** Each zone's readings were taken by one to three teams and each team's anthropometrist pulls
  the tape a little tighter or looser than the supervisor and places it a little differently child to child, so a
  zone's spread and mean of readings are its children's plus its measurers', and a cut-off in the tail turns a small
  offset into several points of wasting; the standardisation test is the only place the measurers are separated from
  the children, because each team works its own clusters.
- **Sources.** The client's two-layer standard (estimation_fit: an estimate that ignores the data's measurement
  structure) and the task type's pattern 2 in layer2-rigor-patterns.md (error carried from replicate measurements,
  shortcut: treat the readings as exact); here the error is in the outcome and moves a tail share, and the replicate
  organ has two parts, repeat readings and readings against a supervisor. The seed DQ19 gave the world, the decision
  and the quantity only. Anthropometric survey practice gave the reflexes the ladder is built against: the
  standardisation test's technical error of measurement as the measurer's error, and the readings' own share as the
  prevalence.
- **Mechanisms on file** (`guard.py mechanisms --objective data-quality-monitoring`, 17 builds), the insight each
  spends: 229 a convex conversion of a daily mean; 231 exits reaching the record late; 232 a transmission rate from
  delayed closed episodes; 230 a late channel moving items to default categories; 228 events clustered within
  randomised units; 233 a gold-standard follow-up carried across base rates; 234 a share in a source's output that
  transit loss cannot move; 235 an item lost only once its device had its next chance; 236 a capture change changing
  which cases are reached; 237 the share of a composite's variance due to its attribute; 238 a channel effect through a
  randomised nudge; 239 a group-level factor; 240 the error of a post-stratified total; 241 a sensor's error against a
  reference at a displaced position; 242 a detector whose sensitivity fades with time since the event; 243 a growth
  balance carrying movement; 245 losses falling on the outcome's own high values. None spends a reading's offset and
  field error, measured on reference children, taken out of a tail share.

## Tried and rejected

- The seed's own pairing in air quality (public PM10 or ozone alerts): set aside at the draw; task245 shipped the same
  pairing and world type the same day, and the seed's averaging-period pitfall is a reading of the standard.
- Wastewater alert lines from off-season baselines with non-detects (a censored fit with each sample's own detection
  limit): rejected at the draw; task189 spends censored results with per-instrument limits, and the field's own
  convention (half the limit) would stand as a competing defensible answer.
- West Nile virus risk alerts from pooled mosquito tests (the pooled maximum-likelihood rate against the minimum
  infection rate): rejected at the draw; task188 spends it, and the alerts are about the world, not the data.
- Next season's alerts after a sampling or replicate cut (the noise decomposed at the new design): rejected at the
  draw; the honest strategy is signal against noise (uncertainty_hold, banned against task198) and a strong solver
  decomposes the noise by reflex once the cut is filed.
- Beach advisories caught by weekly sampling (a two-state process fitted to irregular samples): rejected at the draw;
  task182 spends length-biased observation, the monitoring rates from a few dozen routine samples a season are too
  noisy to force one answer, and a rainfall model would stand as a competing one.
- Inflation measured as the counted share less the error-free share: rejected in prototype; the counted share's
  binomial noise (about 1.5 points at 550 children) is the size of the two-point line, so the note is filed on two
  normal-frame prevalences, the readings' and the children's.

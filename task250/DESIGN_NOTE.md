# task250 design note

## Draw

Card `cards/task250.json` (architecture 2, re-rooted 2026-10-20 from architecture 1, spent at stage 4; see Tried and
rejected). Guard verdict WARN, no BLOCK. test.same_driver_older is a NOTE, differentiated on the card against task157
(members still away returning on a calendar earlier waves kept) and task231 (exits reaching the record a year late);
the card also carries lines against task469 (a duration censored by its own allowance, read where allowances were
already short), task190 v4 (a setting valued by each episode's remaining volume at its firing), task229 v2 (unit states
seen through checks that set them right), task101 and this slot's architecture 1. The one WARN, answered:
repeat.question_form (which, after task249 v5, spent and never shipped): the decision is a pick from the filed menu of
settings, so the question asks which. Nearest driver 0.13 (this slot's architecture 1, differentiated); next 0.07
(task189).

- **Pairing.** Physical & Environmental Sciences / sensor-calibration-measurement, a task type serving Data Quality
  Monitoring & Alerting; drawn for Data Quality Monitoring & Alerting. The object is the health of the network's
  temperature record, watched by the daily quality control, and the call is a monitoring decision: the drift-alert
  setting the quality control runs in 2028.
- **The seed, re-found.** DQ23 gave the world (a station network with per-station drift alerts), the decision (the
  setting, against a budget) and the quantity (alerts a year). Its pitfall (the multiplicity of a per-station rule) is
  the reflex every competent analyst applies, so replaying the filed rule over the record is the default path; the
  decisive step is re-found in the record's own structure.
- **Niche.** The Consorcio Agroclimático del Ebro Medio, a consortium of irrigation communities in Aragón, runs 148
  automatic weather stations feeding its irrigation advice. Each morning its quality control reads every station's
  daily air-temperature anomaly against the inverse-distance estimate from its three nearest reporting stations,
  keeps the 14-day mean of the departure as the drift statistic and raises a drift alert past a setting times the
  station's configured spread; each alert sends a technician who checks the sensor against the transfer standard and
  adjusts or replaces it. On 31 December 2027 the rural development programme that paid for 34 stations ends: the
  irrigation communities take over 17 and the other 17 close, and the second technician's post goes with the funding.
- **The call.** Which setting the quality control runs from its January 2028 configuration, the most sensitive whose
  drift alerts in 2028 fit the visits the field plan leaves for them (QC-02 section 7), and how many drift alerts a
  year it will raise, planned on the 2025 to 2027 record.
- **Shape.** 04, one dial: each of the four settings' drift alerts a year (4), the setting and its count (2), a chart
  of the settings against the plan's visits (5 to 6 named parts), the asks by district (24) and the two files: about
  36 criteria. Decision dial_setting, answer named_option, question form which.
- **Strategy.** maturity_censoring: the record was produced by the policy the call replaces, and every drift that
  policy caught was repaired within days, so the record holds the drifts cut short below the wider limits they would
  otherwise have reached. G12 decisive (no alert at 3.5 in the record is not a record of no alert at 3.5: the 3.0
  alert's repair removed the drift first), G3 (the record's residuals and policy are 2025 to 2027's, not 2028's: the
  network re-run is the first rung), G17; gap time (the drifts' course after the repair is censored), then
  population (the 2028 network); Gate G forecasting (the correctly read past does not pin 2028's alerts); calibration
  none; context artifact monitoring_export; Layer 2 family estimand_identification, pattern
  own:alert-policy-censoring-of-a-drift-record.
- **The two keys.** Each alone leaves 3.5 inside the plan's visits; only both put it over. The network re-run (the
  stated change, landed by architecture 1's reader) is a rung; the decisive move is the second, data-native one.
- **Forum, event, organisation.** line_manager_or_team (the network manager signs the January configuration),
  cutover_or_migration (the 2028 configuration goes live on 15 January 2028 with the programme's stations gone),
  cooperative_or_member_body. Role capacity_planner (the network quality coordinator).
- **People** (`guard.py names --geo Spain --seed 250`, locale es_ES): Celia Hernando, the network quality coordinator,
  who asks; Teodoro Falcó, the field team's lead; Inés Dávila, who runs the quality-control software. None appears in
  the prompt.
- **Data-native sentence.** A temperature sensor's drift is a persistent offset that accumulates until a technician
  recalibrates it against the transfer standard, while the weather's spatial residual reverts by itself; every drift
  in the 2025 to 2027 record was repaired within days of the 3.0 alert that found it, so a setting of 3.5 or 4.0
  replayed on that record misses drifts that, left running in 2028, would have grown until they crossed it, one alert
  each; and the estimate of a station whose near neighbour closes is drawn from farther stations in 2028, so its
  residual spreads wider than the limit set from the record.
- **As-of.** Wednesday 5 January 2028, before the configuration goes live on 15 January.
- **Sources.** The client's two-layer standard; calibration-interval analysis (as-found and as-left records read as
  renewals the adjustments impose: NCSL RP-1); spatial-consistency checks of surface station networks (the spatial
  regression and inverse-distance tests used by state mesonets and national services). `guard.py slots` for the
  driver's terms: no slot holds the mechanism.

## Default path

(architecture 2: written at stage 2)

## Tried and rejected

- The seed's own pitfall (a per-station two-sigma rule against a network budget): the multiplicity reflex; it is the
  default path, not a stump.
- Limits estimated from short baselines (the parameter-estimation effect on false alarms): an honest replay of the
  filed limit-setting over the record lands it, and executing the filed limit rule is close to rule application.
- A burn-in of new sensors in a 2028 replacement programme: a composition shift (composition_mix banned against
  task473) announced by the replacement plan.
- Closures clustered in one province: the continuing stations keep their near neighbours on their own side and the
  alerts barely move (prototype, 0 of 97 continuing stations' spread up by 5 per cent); the programme's stations are
  interspersed, as gap-filling stations are.
- validated_decoy true on the first card (the replay reproduces the alert log and only the closures break it):
  guard BLOCK; the April 2026 additions put the refutation inside the record.
- Seed 252: the per-setting figures at 3.0 and 3.5 sat 0.17 from their rounding edges (65.67, 26.67 a year) and a
  literal reading of the record's first fortnight moved 3.0; a scan of 1,000 seeds found one (1141) with all four
  three-year counts divisible by three and unchanged under the start, limit-rounding and strict-limit readings.
- A statistic defined on every day with 10 residuals: the export carries read days only, and a reader of the export
  moved 4.0 from 11 to 10; the statistic and its alerts are now on read days (section 5).
- The hold read per calendar year: lifting it each January moved 3.0 and 3.5 by a whole alert; section 8 now says a
  new year's configuration does not lift it.
- One out-of-sample year: a single fresh year on the 2028 network raised exactly 18 at 3.5; three fresh years are the
  section 7 horizon (24.7 at 3.5, 10.3 at 4.0).
- The asks with one campaign device drawn at random: the readings-first path kept 10 of 24 and the order-first path
  12; the campaign visits, the cancellations after the visit and the remote resets are now aimed at every district,
  and the standard's absence reaches the winter visits no campaign touches.
- Architecture 1 (the record re-run with the 34 closing programme stations out of the neighbour pool, as the decisive
  step on its own): spent 10-20 at stage 4. Reader 1 re-ran the quality control with the 2028 network and filed 4.0 at
  9 a year, every setting within one of the golden (63, 26, 9 and 3 against 61, 25, 9 and 3); reader 2 replayed the
  record and filed 3.5 at 9; judge DETERMINISTIC APPROVE. A stated change with an obvious mechanism is landed by a
  careful reader: the network re-run is now the first rung, and the decisive step is the drifts the record's own 3.0
  alerts cut short.
- One key, the censoring alone (no closures): a single unprompted insight decides it, and a reader who thinks of the
  repairs lands the call; two keys, each alone leaving 3.5 inside the visits, are needed.
- Drifts anywhere in the network: a drift left to grow carries a close neighbour's statistic over that neighbour's
  limit before its own alert (prototype, 5 to 12 stations per seed whose counterfactual count departed from the
  re-run plus the cut-short drifts); drifts now sit only where the weight a neighbour gives them times their spread
  stays under 0.7 of the neighbour's own, at stations that keep their usual neighbours.
- Censored drifts the spring round would have found first: a drift cut short in January or February at a setting of
  3.0 would at 4.5 have met the station's spring round before its alert (prototype, 1 to 2 a year); a drift whose
  station's next round falls before it could have crossed 4.5 is redrawn.
- An autumn calibration round in 2027 and 2028: 2028's rounds would then differ from 2025's and 2026's, and the
  record's drifts of June to August would have been found by a round rather than an alert, a forecasting fork on
  the window; every year now has the spring round only.
- The six stations added in April 2026: their 21 months against the record's three years opened an annualisation
  fork on each setting's count; the six infill stations now report from 2025.
- Old sensors with standing offsets up to 0.4 degrees: a false alert's visit at such a station adjusts a sensor
  that never drifted, and the history's drift-alert adjustments stop meaning drifts; standing offsets are now under
  0.12 degrees and no check without a drift passes the 0.2 adjustment threshold.

# task250 design note

## Draw

Card `cards/task250.json` (architecture 1, registered 2026-10-20). Guard verdict WARN, no BLOCK. test.same_puzzle_older
and test.same_driver_older are NOTEs, differentiated on the card: against task101 (a payout threshold cut from a
distribution the decision's own payments entered), task469 (overruns of a shorter allowance seen through censored
tasks) and task138 (a forward requirement replayed from each unit's rebuilt store). The one WARN, answered:
repeat.question_form (which, after task249 v5, spent and never shipped): the decision is a pick from the filed menu of
settings, so the question asks which. A first draft carried validated_decoy, which the guard blocked; the record now
holds the network's own earlier change (six stations added in April 2026 narrowed their neighbours' residuals and
cut those stations' alerts), so a replay of the record as it ran is refuted inside the record and the flag is false.
Nearest driver 0.07 (task240).

- **Pairing.** Physical & Environmental Sciences / sensor-calibration-measurement, a task type serving Data Quality
  Monitoring & Alerting; drawn for Data Quality Monitoring & Alerting. Not banned against the last three live builds
  (task474 survey research ETL, task473 general statistics ETL, task472 supply chain ETL; task249 v5 is spent and
  holds no axis). The object is the health of the network's temperature record, watched by the daily quality control,
  and the call is a monitoring decision: the drift-alert setting the quality control runs in 2028.
- **The seed, re-found.** DQ23 gave the world (a station network with per-station drift alerts), the decision (the
  setting, against a network budget) and the quantity (expected alerts a month). Its pitfall (two sigma at every
  station fires several alerts a week; set the threshold for the network) is the multiplicity reflex every competent
  analyst already applies, so it is the default path here, executed by replaying the filed rule over the record. The
  decisive step is re-found in the network's own structure.
- **Niche.** The Consorcio Agroclimático del Ebro Medio, a consortium of irrigation communities in Aragón, runs 148
  automatic weather stations that feed its irrigation advice. Each morning its quality control reads every station's
  daily mean air-temperature anomaly against the inverse-distance estimate from the three nearest stations reporting
  that day, keeps the 14-day mean of the departure as the drift statistic, and raises a drift alert when it passes a
  setting times the station's configured spread; each alert is a field visit. On 31 December 2027 the rural
  development programme that paid for 34 of the stations ends; they close, and with them the second technician.
- **The call.** Which setting the quality control runs from its January 2028 configuration so that drift-alert visits
  stay within the field team's 2.5 a month, the most sensitive setting that does, and how many alerts a month it will
  raise, planned on the 2025 to 2027 record.
- **Shape.** 04, one dial: each allowed setting's expected alerts a month, the call, the runner-up and the gap, a chart
  of the settings against the budget, and the asks by district; over 25 criteria. Decision dial_setting, answer
  named_option, question form which.
- **Strategy.** forecast_method_backtest: the network's structure changes at the year's turn, so the natural fit to the
  record (the rule replayed over the residuals as they ran) is wrong out of sample. G3 decisive (the record's
  residuals were produced by the network's old configuration, not by the one that will run), G13 (the record's window
  against the 2028 window), G17; gap population (the neighbour pool the residuals were measured with is not the 2028
  pool), then time; Gate G forecasting (the correctly read past does not pin 2028's alerts); calibration none;
  context artifact monitoring_export (the quality control's daily export); Layer 2 family field_method, pattern
  own:spatial-consistency-residual-under-network-thinning.
- **Forum, event, organisation.** line_manager_or_team (the network manager signs the January configuration),
  cutover_or_migration (the 2028 configuration goes live on 15 January 2028), cooperative_or_member_body (a consortium
  of irrigation communities). Role capacity_planner (the network quality coordinator, who fits the alerts to the field
  team's visits and asks).
- **People** (`guard.py names --geo Spain --seed 250`, locale es_ES): Celia Hernando, the network quality coordinator,
  who asks; Teodoro Falcó, the field team's lead; Inés Dávila, who runs the quality-control software. None appears in
  the prompt.
- **Data-native sentence.** The quality control judges each station against an estimate from its three nearest
  reporting neighbours, and that estimate's error grows with the neighbours' distance because the day's mesoscale
  temperature anomalies decorrelate over tens of kilometres; the 34 closing stations were sited to fill gaps, so many
  continuing stations lose a near neighbour and will be read against farther ones in 2028, while the January
  configuration sets every limit from the spread of the statistic as it ran with the old neighbours, so their
  alerts rise even as the network shrinks.
- **As-of.** Wednesday 5 January 2028, before the configuration goes live on 15 January.
- **Sources.** The client's two-layer standard (field_method); spatial-consistency checks of surface station networks
  (the spatial regression and inverse-distance tests used by state mesonets and national services); agro-climatic
  station networks for irrigation advice in Spain. No build on file reads an alert count through the estimate's
  dependence on the neighbour pool (`guard.py slots` for neighbour, spatial, closure: no hit on the mechanism).

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

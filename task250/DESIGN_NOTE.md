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

The path a competent analyst takes after reading every file and filed rule correctly, the pack cleaned (the daily
export's repeats dropped, the register read for the 2028 network, the export's statistic and limits checked against
section 8).

1. Read QC-02 (sections 4 to 8), the field plan (28 visits for drift alerts in 2028), the register (17 stations with a
   baja_prevista of 31/12/2027) and the quality-control export.
2. Set each kept station's 2028 limit by section 6: the setting times the standard deviation (n - 1) of its
   estadistico_14d over 2025 to 2027.
3. Re-run sections 4, 5 and 8 on the export's anomalies with the 131 kept stations as the network (the careful step;
   the record replayed as it ran gives 12 at 3.5) and count the kept stations' alerts: 66, 23, 7 and 3 a year at 3.0,
   3.5, 4.0 and 4.5.
4. Choose the most sensitive setting within the 28 visits.

Ends on: 3.5 at 23 drift alerts a year
Golden: 4.0 at 18 drift alerts a year

## Stump sentence

A competent solver re-runs the filed quality control on the 2025 to 2027 export with the 131 stations the network
keeps, counts 23 drift alerts a year at 3.5 against the field plan's 28 visits and files 3.5; every drift in the record
was repaired within days of the 3.0 alert that found it, so 30 of the 35 drifts the sensor history shows repaired at
kept stations never reached the 3.5 limit before their repair and would in 2028 have kept growing until they did, one
alert each, which puts 3.5 at 33 a year, over the visits, and files 4.0 at 18.

## Three rules

Task type: sensor-calibration-measurement (Physical & Environmental Sciences), a task type the taxonomy tags for Data
Quality Monitoring & Alerting; the call is the network's drift-alert setting, a monitoring decision on the health of
the temperature record.

Domain test: the deciding quantities are measurement-network ones: a temperature sensor's drift is a persistent offset
that accumulates until a technician sets it right against the transfer standard (calibration-interval analysis reads
an instrument's as-found record as renewals the adjustments impose), while the weather's spatial residual reverts by
itself; and a station's spatial-consistency residual widens when the nearest stations its estimate draws on close.

Swap: in a hospital's or a call centre's nouns there is no transfer standard, no recalibration that resets a monotone
drift to zero and no interpolated neighbour estimate whose error grows as the network thins, so neither key, nor the
count they decide, carries over.

Layer 1: the daily export in Spanish headers with decimal commas and re-sent rows repeated; clock-change days short or
long and five-minute loggers after a firmware upgrade; the maintenance contractor changed in July 2027 and the work
orders' sheet, language and statuses with it; the new contractor checks a spare sensor at the workshop under the
station's order before going out; the tablets carried a station's last order forward onto some visits' readings; drift
orders closed from the office with the system's closing date in the visit column; route orders carrying two
stations; breakdowns reset remotely closed with a visit date; the register's sensor history mixing adjustments,
replacements and shield cleanings.

Layer 2: two keys. The first is the stated change: the 17 closing stations leave the quality control's neighbour pool,
so the record is re-run with the 2028 network (architecture 1's decisive step, landed by a reader, now a rung). The
second is the decisive one: the record was produced by the policy being replaced, and every drift in it was cut
short by the visit that policy's 3.0 alert sent, so at a wider setting each would have grown until it crossed, one
alert each.

Decisive step: adding, at each setting, one alert for every drift the sensor history shows adjusted or replaced at a
drift-alert visit to a kept station that the re-run's alerts at that setting never reached before the repair (30 of 35
at 3.5); with the re-run alone 3.5 stays inside the 28 visits, and with the cut-short drifts alone (no network
re-run) it stays inside too.

Not semantics: every field reads plainly (the history's motivo and as-found error, the register's baja_prevista, the
export's statistic and alert); a reader who reads them all correctly, and executes every filed rule, still files 3.5,
because no field or definition says the record's drifts were cut short: section 9 says only that a drift grows until a
check sets it right, a property of sensors that neither the replay nor the re-run has any use for.

Not rule application: no filed rule adds the cut-short drifts or says how a setting's alerts are to be estimated;
section 7 names the three years the plan rests on, section 8 how an alert is raised and section 9 that a drift grows
until a check sets it right, and executing all three on the record, with or without the 2028 network, files 3.5; the
step is the analyst's reading of the record as censored by its own policy.

Analyst test: a strong analyst who cleans the pack and reads every rule re-runs the quality control with the 2028
network against the section 6 limits, counts 23 alerts a year at 3.5 inside the 28 visits and files 3.5 at 23 (or 22
with the cut-short drifts added to the record as it ran); only both keys put 3.5 at 33 and file 4.0 at 18.

Estimand: each setting's drift alerts in 2028 at the 131 stations the network keeps, against the January 2028
configuration's limits (section 6), planned on the 2025 to 2027 record (section 7), a year; the setting is the most
sensitive whose count fits the plan's 28 visits.

No decoy: no document argues for the replay or the re-run, nothing certifies a count at any setting but 3.0 (the 2027
alert summary counts the alerts raised at 3.0, which every route reproduces), and no sentence says how a setting's
alerts are estimated beyond section 7's three years.

No certified replay: the replay reproduces the export's own 3.0 alerts, as any route does; the record itself refutes
it at 3.5, where the history shows 30 drifts repaired at kept stations that the 3.5 limit never reached (validated_decoy
false).

Lesson: task249 v1 to v5 and this slot's architecture 1 were landed by careful readers on a single stated change or a
named reflex; here the stated change is a rung and the decisive move is a second, data-native one, each key alone
leaving 3.5 inside the visits by five.

## Readability screen

| Rung | Where a reader meets it | Verdict |
|---|---|---|
| 1. The record replayed as it ran (3.5 at 12) | the export's statistic and alert column, sections 6 and 8 | readable |
| 2. The 2028 network re-run (3.5 at 23) | the register's baja_prevista, the plan's 131 stations, section 4's nearest stations | readable |
| 3. (decisive) The drifts the record cut short (3.5 at 33) | nothing names it: the history lists adjustments by date, motivo and as-found error, the export lists alerts, and only the analyst's reading of the two together, with what a drift does if left alone, shows the record censored by its own policy | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | drift alert | a section 8 alert, the hold applied | every day beyond the limit | alert-days file 4.5 | section 8's hold; the export's alert column replays exactly |
| SF2 | planned on | the three calendar years 2025 to 2027 | 2027 alone | not computed | section 7, the three previous calendar years |
| SF3 | the 2028 network | the 131 stations with no baja_prevista | the 148 | the re-run's pool | the plan: the network runs 131 stations in 2028 |
| SF4 | the limit | setting times SD (n - 1) of the recorded statistic, 2025 to 2027 | 2027's statistic alone | same call | section 6 |
| SF5 | most sensitive | the lowest setting | the highest | not a reading | section 7: a lower setting catches a drift sooner |
| SF6 | fit | at or under 28 | under 28 | same call | no setting sits at 28 |
| SF7 | the hold | 14 days | 13 days | same call | section 8, any of the 14 days before |
| SF8 | read day | the statistic on read days only | every day with 10 residuals | not a reading | section 5 |
| SF9 | the estimate's stations | the three nearest with an anomaly that day within 75 km | the nearest three regardless | not a reading | section 4 |
| SF10 | distance | straight line between the register's UTM coordinates | great circle | same call | section 4; no two stations share a position |
| SF11 | anomaly | the export's anomalia | recomputed from normals | not computable | no normals ship |
| SF13 | the year's turn | the hold carries across | lifted each January | not a reading | section 8: a new year's configuration does not lift it |
| SF14 | a year | the three years' count divided by three | a fraction | same figures | every three-year count divides by three |
| SF15 | the record's first fortnight | the statistic from 10 residuals, version 4 in force from 1 January 2025 | a full 14-day window | same call, 3.0 at 68 | section 5's at least 10 |
| SF16 | rounding of the limit | unrounded | k times the spread to three decimals | same figures | asserted |
| SF17 | district | the register's comarca | the order's own field | not a field | every order's station is in the register |
| SF18 | n - 1 | sample standard deviation | population | same figures at 3.5 to 4.5, 3.0 at 69 | section 6 |
| SF19 | radius and ties | the 75 km radius never binds, no ties | not a reading | same call | asserted |
| SF20 | either side | two-sided | one side | 3.5 | section 8: either side |
| SF21 | beyond | strictly beyond | at or beyond | same figures | the export's alert column replays strictly |
| SF22 | set right | an adjustment or a replacement both end a drift | the replacement starts a new sensor | not a reading | section 9: one beyond 0.2 is adjusted, one more than 1.0 out is replaced |
| SF23 | the drifts cut short | every drift-alert row of the history with an as-found error | adjustments only | 4.0 | section 9; asserted |
| SF24 | the alert a repair answered | the station's latest alert within 10 days before | an earlier one | not a reading | one alert within 30 days, asserted |
| SF25 | never reached before its repair | from a fortnight before the alert to the repair | 30, 60 or 90 days before | same figures | asserted |
| SF26 | one alert per drift | the cut-short drifts added to the re-run's count | every drift once, the re-run's drift alerts dropped | same figures | asserted |
| SF27 | a drift after its repair | set right by the check; left alone it goes on growing at its own rate | stops at the size the history records | 3.5 | section 9: a sensor's drift does not stop on its own and grows until a check sets it right |
| SF28 | the spring round before a cut-short drift's crossing | none comes first: each drift crosses the 3.5, 4.0 and 4.5 limits 62 days or more before its station's next round | a round sets one right first | 4.5 at 13 | asserted (the audit redraws any drift whose next round could come first) |

## Ladder

| Route | 3.0 | 3.5 | 4.0 | 4.5 | Files |
|---|---|---|---|---|---|
| The record replayed as it ran, kept stations | 49.0 | 12.3 | 2.7 | 1.0 | 3.5 at 12 |
| The whole network replayed | 54.3 | 14.3 | 3.3 | 1.3 | 3.5 at 14 |
| Key 1: the 2028 network re-run | 65.7 | 23.0 | 7.0 | 2.7 | 3.5 at 23 |
| Key 2 alone: the cut-short drifts added to the record as it ran | 52.3 | 22.3 | 13.7 | 12.3 | 3.5 at 22 |
| Both keys, the closing stations' drifts counted too | 70.0 | 34.0 | 19.0 | 15.0 | 4.0 at 19 |
| Both keys, every adjustment in the history counted | 71.7 | 35.7 | 20.7 | 16.7 | 4.0 at 21 |
| Golden: both keys | 69 | 33 | 18 | 14 | 4.0 at 18 |

The record re-lived at each setting with the 2028 network, every drift left to grow until that setting's alert sent its
visit or the spring round found it, raises exactly the golden's count (207, 99, 54 and 42 over the three years,
asserted). Three fresh years on the same stations, the record's drifts again, give the same direction out of sample
(asserted in checks.py).

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | the 131 kept stations; drifts at closing stations out | filed (baja_prevista, the plan); C1 |
| 2 | Unit of account | an alert (section 8), a visit (a technician at the station) | filed |
| 3 | Attribution window | 2025 to 2027, alerts and limits | filed (sections 6, 7); C1 at the edges (no drift open at the end) |
| 4 | As-of dating | 5 January 2028 | filed |
| 5 | Version basis | QC-02 version 4 from 1 January 2025 | filed |
| 6 | Denominator | three years | filed (section 7) |
| 7 | Weighting | none | not applicable |
| 8 | Window length | 14 days, 10 residuals | filed (section 5) |
| 9 | Boundary inclusivity | strictly beyond; the hold of 14 days | filed; SF21, SF7 |
| 10 | Rounding path | whole numbers a year from three-year counts divisible by three | C1 by construction |
| 11 | Tie-break | none open | asserted (no tied distances) |
| 12 | Maturity and censoring | the record's drifts cut short by its own repairs (the decisive step, forced by the design: each drift persists until set right and the history dates every repair) | C1 over windows and formulations (SF25, SF26); the counterfactual equality |
| 13 | Order of operations | re-run, then limits from the recorded statistic | filed (section 6) |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | the daily export's repeats are exact | C1 |
| 16 | Identity normalisation | station codes one scheme | C1 |
| 17 | Netting against gross | either side counted once | filed (section 8) |
| 18 | Dimensional units | degrees C throughout | data |
| 19 | Code and status semantics | motivo, Estado, status | dictionary; never the stump |
| 20 | Integerisation | whole alerts | C1 |
| 21 | Clause scope | section 8's hold across the year's turn | filed |
| 22 | Forward window contents | 2028 planned on 2025 to 2027 (the spring round each year, the 2028 plan the same) | filed (section 7, the plan) |

## Literal reader

Executing the prompt and every filed sentence word for word (sections 4 to 9, the register's baja_prevista and sensor
history, the plan's 28 visits), with the record read for what a wider setting would have met, gives the golden: section
9 files that a drift grows until a check sets it right, so a drift the record's 3.0 alert sent a check to would have
gone on to a wider setting's limit; the only open move, counting the drifts the record cut short, converges over every
window from a fortnight to 90 days and over counting every drift once (SF25, SF26), and the record re-lived with each
drift left to grow raises exactly the golden's count at every setting (C1, asserted).

## Oracles

- The 2027 alert summary counts the alerts raised at 3.0 by district and month; every route reproduces it.
- The export's alert column replays exactly under section 8 on its own statistic and limits; every route passes it.
- The history's as-found errors tie to the calibration database's readings; every route passes it.
- No document carries a count at any setting but 3.0, and none ranks the settings.

## Ask sheet

Ask A: by district, the drift-alert visits made in 2027 and the days their alerts waited (16 figures). Ask B: by
district, the breakdown visits made in 2027 at the kept stations (8 figures). Neither reads the call's rows: the call
reads the quality control's export and the register; the asks read the work orders, the calibration database and the
loggers' daily export, none of which moves the call (separation and deletion tests asserted).

What a visit is, filed once each: the plan counts visits by station, a visit being a day a technician is at a
station; section 9 puts a check of the sensor against the transfer standard at every visit a drift alert calls, and
the plan at every visit since July 2027; the dictionary gives the old contractor's Visita as the day the technician
visited (blank on a cancelled order and on one closed without a visit) and the new contractor's visit_date as the date
the order was closed on its app. So the old sheet's visits are its closed orders with a Visita, and the new
contractor's are the days a technician read a station's sensor there while an order was open. No cancelled order has a
reading under it, every reading sits under an order the two sheets hold, and every reading a technician took at a
station lies inside the range the station's logger recorded that day (all asserted): the pass 3 judge's
Visita-against-readings conflict and the lost orders are gone.

The device, silent. The new contractor checks a spare sensor at the workshop before a technician goes out (three
paired readings at the ice point, three at 40 degrees in the dry block), and the calibration database enters them
under the station's order like a visit's: on the false alert the desk then closed in six districts, on a breakdown
then reset remotely at a kept station in every district, and before two drift-alert visits (Cinco Villas, Monegros).
Nothing marks them: no flag, note, technician, count or order type, and the dictionary describes the database as every
paired reading of a temperature sensor against the transfer standard. Only a cut nothing invites finds them: the
readings against the range the station's logger recorded that day, both points 3 degrees or more outside it, on
weekdays the logger delivered in full and on no day a technician read the station there. Fair: that one test, on the
order-led route and on the alert-led route alike, reproduces the field truth exactly (both asserted), and block 3
steps 6 and 7 name it for the grader. Hazards on the same rows: the desk's closures and remote resets with nothing
under them, readings under the station's previous order (never as many in a district as the orders holding only a
workshop check, so the two never net out on the order-key path), route orders carrying two stations, weekend alerts,
the new contractor's visit_date after the visit, and drift alerts answered at the spring round.

| Path (no test of a reading against the logged range) | Visits | Days | Breakdowns | Keeps |
| --- | --- | --- | --- | --- |
| readings at the station while the order was open | 2 of 8 | 1 of 8 | 0 of 8 | 3 of 24 |
| the same, the order's notice as the alert | 2 | 0 | 0 | 2 |
| the same, the old orders by their readings | 2 | 1 | 0 | 3 |
| readings under the order only | 1 | 1 | 0 | 2 |
| readings under the order, else the visit_date | 2 | 1 | 0 | 3 |
| every closed order on its visit_date | 2 | 1 | 0 | 3 |
| alert-led (first reading day within 9, 14 or 21 days) | 2 | 1 | 0 | 3 |

The figures every path keeps are the two districts with no drift alert the desk closed since July 2027 (Cinco Villas
and Somontano de Barbastro, whose visit counts no device can reach) and Somontano's days (no drift alert there since
July 2027).

| Ask | Cracker (the best of the paths above) | Verdict |
| --- | --- | --- |
| A visits | 2 of 8 (Cinco Villas and Somontano de Barbastro) | miss |
| A days | 0 to 1 of 8 (Somontano de Barbastro) | miss |
| B breakdowns | 0 of 8 on every path | miss |

Pair ceiling: 35.4 ((51.9 + 18.9) / 2), the cracker keeping 3 of 24 ask figures on the call and the mirror the same.
Mirror leakage: 12 per cent of ask weight.
Measured by: generator/pair.py on the cut pack (target.zip 19727806). The device's resolution (the temperature test)
lands all 24 on both routes; a reader who finds it keeps the ask layer, and the stage 4 readers are the measurement.

## Pre-ship check

- Free gates (stage 3, round 3): generator checks 514 passed (the counterfactual equality at every setting, the
  ladder, R1 to R3 with three fresh years, SF1 to SF26, the separation line and deletion tests, the asks against the
  field truth with every reading inside its station's logged range and every workshop reading outside it, the link
  window from 2 to 14 days, the alert-led route with the range test landing the same 24 figures, every natural path
  at 6 of 24 or fewer, the documents read back, the realism sweep with no negative zero, the dates); verify.py 0
  failures; two builds byte-identical (target.zip 19727806); figures_check 79 of 79; precut 51 of 51; voice-check
  PASS.
- leak.py REVIEW, no LEAK, every line answered harmless as in the earlier rounds: the procedure lists the four
  settings (the filed menu, which section 7 needs); the 2027 summary names the setting in force (3.0, the record's
  own); the call's vocabulary in the procedure and the plan is the field's ordinary wording; the stump-paragraph terms
  are the network's ordinary nouns; the ET0 bulletin and the register carry the candidates only as numbers of other
  meaning. No filed document names a workshop, bench, spare, ice point or dry block (asserted).
- guard heart WARN (question form which, after task476 v2 and task477: the decision is a pick from a filed menu);
  surface PASS on people (Red Agroclimática is the network's name, not a person).
- Containers clean (no producer signature, no out-of-band timestamp) in target/ and golden/.
- Golden realism: the workbook leads with the finding as its title, carries the per-setting split, the district sheet
  with a network total and a note on what a visit is (the workshop's spare checks named there, for the grader), and a
  notes sheet; the chart splits each bar into the re-run's alerts and the drifts the 3.0 alerts' visits set right
  first, the 4.0 bar marked, the plan's 28 visits as a labelled line.
- Open risk, stated: a reader who tests the readings against the logged range lands both asks; a reader who turns both
  keys lands the call. The stage 4 readers are the measurement.

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
- The visit asks on orders and readings alone (round 2): drift orders cancelled after the visit with the readings under
  the cancelled order, orders the handover export lost, and a closed order with nothing under it counted a visit when
  the station had a reading under another order while it was open. The pass 3 judge sent it back (52 cancelled orders
  with readings against the dictionary's Visita, the lost orders' window unrecoverable; Gate C on asks 3 and 4), and
  with the visit filed reader D built the visits from the readings station by station and took 24 of 24. Filing a
  visit closes the fork and hands the ask to every reader; the devices that held were all readings a careful reader
  joins. The cancellations after a visit and the lost orders are gone; the device is now readings no visit made (a
  spare checked at the workshop under the station's order), found only against the range the station's logger
  recorded that day.
- The growth of a drift left to the reader (rounds 1 to 3): the pass 4 judge read section 7 literally as the record
  re-run and found nothing filed that a drift the 3.0 alert's check set right would have gone on growing; the as-found
  errors at repair (0.6 to 0.9 of the 4.0 limit) then read as the drifts' full size, and 3.5 stood as at least as
  defensible (SEND_BACK, Gates A to C on the main call). Section 9 now files the property of sensors the counterfactual
  rests on (a drift does not stop on its own and grows at the sensor's own rate until a check sets it right); the
  censoring remains the analyst's, and the cut-short drifts alone, without the network re-run, still file 3.5.

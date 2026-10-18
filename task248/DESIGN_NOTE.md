# task248 design note

## Draw

Card `cards/task248.json` (architecture 1, registered 2026-10-18). Guard verdict WARN, no BLOCK. test.same_puzzle_older
is a NOTE, differentiated on the card against task133's v1 lineage: there a filed outcome curve is conditioned on each
unit's own survival to date; here a measurement loses part of what it carries in transit at a rate that moves with
the season, read against each unit's own baseline. Each WARN, answered: overuse.org_family (government_agency): a
regional public health service is a government agency and no other key is true of it; repeat.decision
(quantity_figure after task165): the desk plans on a count of episodes; repeat.deliverables (docx and xlsx after
task165): a planning note to the surveillance manager and the workbook behind it are what a coordinator sends. Nearest
driver 0.06 (task170, task99 lineage, task234 v1 lineage).

- **Pairing.** Epidemiology & Public Health / disease-surveillance-outbreak-anomaly-detection, a task type serving
  Anomaly Detection and Data Quality Monitoring; drawn for Data Quality Monitoring & Alerting. Not banned against the
  last three builds (task201 energy anomaly detection, task247 physical and environmental sciences data quality,
  task165 urban forecasting). The object is the health of the wastewater dashboard's levels, how much of each plant's
  winter rise is the sewer destroying less of the virus's RNA in cold water rather than more virus, and the call is a
  monitoring decision: how many alert episodes the verification desk plans for once the dashboard reads every sample
  on the shed load.
- **The seed, re-found.** DQ21 gave the world (a duty desk that checks every alert episode a monitoring system
  raises), the decision (the desk sized for the coming season on episodes) and the quantity (alert episodes). Its
  air quality network is left, its pairing banned against task247, and its pitfall (consecutive exceedances counted as
  one episode under the policy's gap rule) is rule application: here the episode rule is filed and executed by every
  route, and the decisive step is the reconstruction of the record the episodes are read on.
- **Niche.** A regional public health service in New Zealand runs wastewater surveillance of SARS-CoV-2 at 24
  treatment plants: two 24-hour composite samples a week, the laboratory's concentrations of the N1 gene and of PMMoV,
  the plants' flows and inlet temperatures from the water services company. The dashboard gives each plant a weekly
  level against its own baseline and the verification desk checks every alert episode (a run of weeks at High or
  above) before the public health team acts on it. From 1 May 2028 the dashboard reads every sample on the shed load:
  the plant's concentration with the RNA the sewer destroyed on the way from the town to the plant restored.
- **The call.** How many alert episodes the desk plans for over winter 2028, on the planning basis the service uses:
  last winter's samples (May to September 2027) read as the dashboard will read them, with every plant's episode
  count on the published basis and on the shed load.
- **Shape.** 03, a bridge from the published total to the shed-load total, plant by plant (24 plants by two counts),
  the total, the plants whose count moves, a chart of each plant's winter levels or counts on both bases, and the asks;
  well over 25 criteria. Decision quantity_figure, answer count, question form how many.
- **Strategy.** other, named in the card's notes: a measurement's in-transit loss whose rate moves with the season,
  read against each unit's own baseline (neither censoring nor a composition shift). G9 decisive (what reaches the
  plant is what survived the sewer, not what the town shed), G16 (one decay rate, PMMoV normalization, a temperature
  term beside travel time, or the rate as a function of temperature over travel time), G4; gap time then population;
  Gate G decomposition_attribution (each plant's winter rise assigned to its two drivers, more virus and less decay);
  calibration physical_verification (the paired study's upstream composites, taken where the town's sewage enters the
  trunk sewer); context artifact monitoring_export (the dashboard's level and episode export); Layer 2 family
  field_method, pattern own:temperature-dependent-in-sewer-decay-over-travel-time-against-own-baseline.
- **Forum, event, organisation.** line_manager_or_team (the service's surveillance manager signs the desk's winter
  rota), cutover_or_migration (the dashboard moves to the shed load on 1 May 2028), government_agency (a regional
  public health service). Role capacity_planner (the wastewater surveillance coordinator rosters the desk and asks).
- **People** (`guard.py names --geo "New Zealand" --seed 248`, locale en_NZ): Fiona Chandler, the wastewater
  surveillance coordinator, who asks; Luke Jefferies, the molecular laboratory's scientist; Craig Stuart, the water
  services company's network modeller (travel times); Alana Costello, who ran the paired upstream study. None appears
  in the prompt.
- **Data-native sentence.** The virus's RNA decays on its way down the sewer at a rate that rises with the water's
  temperature, so a plant at the end of a long trunk sewer loses far more of it in summer than in winter; its baseline
  is set by the summer lull, when the losses are largest, and its winter samples arrive with much more of their RNA,
  so on the plant's concentration the cold months look higher against the baseline than the town's shedding was, and
  only a loss that moves with the temperature can take that out, since anything constant over the year scales the
  winter samples and the baseline alike.
- **As-of.** Wednesday 12 April 2028, before the cutover on 1 May.
- **Sources.** The client's two-layer standard (field_method: the field's own method done right); published wastewater
  studies of SARS-CoV-2 RNA decay in sewage (first order, faster in warm water) and the use of population-weighted
  travel times from network models. No build on file takes wastewater surveillance as its object (task160 lists
  wastewater results as one input to a hospital surge plan; task121 names a wastewater plant as an odour source);
  task189 and task190 spent detection-limit censoring, which this build does not use.

## Default path

1. Read the laboratory's export: the accepted run of each sample and target (the export notes); each sample's N1 load
   per person is the concentration times the composite's flow on the chain-of-custody form times 1,000 over the
   register's population served (methods note section 3).
2. Weekly values by the week of the day the composite ended, each plant's baseline the 10th percentile (PERCENTILE.INC)
   of its weekly values of the weeks starting 6 April 2026 to 29 March 2027, the levels, the episodes (open at 1.0 or
   more, close below 0.5), winter 2027's those opening in the weeks starting 3 May to 27 September (sections 4 and 5):
   30, the dashboard's export.
3. The shed load (section 6.1) restores the RNA the sewer destroyed, resting on the paired study and the travel times:
   fit one first-order decay rate to the study's ratios of plant to upstream N1 against the travel time (0.0408 an
   hour) and multiply every sample's load by exp(that rate times the plant's travel time in hours).
4. Recompute the weekly values, baselines, levels and episodes on the shed load per person, as section 6.1 says.

Ends on: 30 alert episodes on the shed load, every plant's count as published, no plant moving.

Golden: 26 alert episodes: Ardenmouth South, Ardenmouth East, Tarnbrook, Cleaveland Flat and Saltmarsh Point one fewer
each and Ardenmouth West one more, with each sample's RNA restored at the paired study's decay rate for the composite's
own inlet temperature (0.050 an hour at 20 degrees, rising about 9 per cent a degree) over the plant's travel time.

## Stump sentence

A competent analyst restores each sample's shed load with the paired study's single decay rate over the plant's travel
time (or reads the samples on PMMoV-normalised concentrations) and ends on 30 alert episodes, every plant as published;
the step that lands it there is treating the sewer's loss as a constant, when the RNA's decay rate rises with the
water's temperature, so at the long trunk sewers the summer samples that set each plant's baseline lost far more than
the winter samples (at Cleaveland Flat the study's composites lost 0.69 log10 in December to February and 0.31 in June
to August), and a correction constant over the year lifts a plant's baseline and its winter samples alike; only the rate
at each composite's own temperature over the travel time lifts the baselines at the long sewers more than their winter
samples (by 0.52 to 0.68 log10 against winter peaks that fall from 1.06 to 1.14 to under 0.81), removes the five
episodes the colder water alone raised and splits Ardenmouth West's merged one in two, 26.

## Three rules

- **Task type:** epidemiology-public-health / disease-surveillance-outbreak-anomaly-detection, which serves Data
  Quality Monitoring & Alerting (the dashboard's levels and alert episodes are the monitored data product, and the call
  is the monitoring decision taken on them: how many episodes the verification desk checks once the levels are read on
  the shed load).
- **Domain test:** the quantity that decides is each plant's weekly level on the shed load, which wastewater-based
  epidemiology recovers from the plant's concentration by treating the RNA's in-sewer decay as first order over the
  population-weighted travel time at a rate that rises with the water's temperature, the rate measured by paired
  composites at the trunk sewer's head and at the plant.
- **Swap:** "how many alerts should our hospital desk plan for, reading last winter's admissions on the corrected
  count" keeps the sentence and loses the task: there is no sewer, no travel time over which a virus's RNA decays
  faster in warm water, no paired upstream composite and no faecal marker riding along, so a temperature-dependent
  restoration has nothing to act on.
- **Layer 1:** the laboratory's export by analysis run (rejected and check runs beside the accepted), the composite's
  flow from the operator's form, the paired study's copies per millilitre in triplicate with probe readings and missed
  visits, the travel times in the network modeller's memo table, the historian's local time across both daylight saving
  changes; each written by the laboratory's system, the operator, the field team, the modeller or the historian, none
  placed, and the call is the same under every handling (SF2, SF5, SF11, the R2 block). The contract report, the second
  inlet channels and the historian's faults since October 2027 lie outside the call's rows (S1).
- **Layer 2:** field_method, the field's own method done right: the in-sewer decay of SARS-CoV-2 RNA as first order at a
  rate depending on the water's temperature, applied at each composite's own temperature over the travel time, where
  the easy routes take the loss as a constant or divide by the faecal marker.
- **Decisive step:** fitting the paired study's loss as a temperature-dependent first-order rate, k(T) = k20 times
  theta^(T - 20), and restoring each composite at its own inlet temperature over the plant's travel time, rather than
  with one rate, a PMMoV ratio or a temperature term beside the travel time.
- **Not semantics:** reading every field, code, unit and definition right (the accepted run, the form's flow, copies per
  millilitre, the memo's minutes, the weeks, PERCENTILE.INC, the episode rule, the shed load's definition) still leaves
  the single-rate route on 30: the methods note defines the shed load as the load with the destroyed RNA restored and
  points to the study and the travel times, and nothing says how the destruction varies.
- **Not rule application:** the methods note files the estimand (the shed load, the levels, baselines and episodes
  computed on it exactly as on the load per person, the winter's weeks) and no model of the decay; executing every
  stated rule with the study's average decay gives back the published 30, and no filed rule ties the decay to the
  temperature.
- **Analyst test:** a strong analyst who reads every file right fits one decay rate to the study's ratios against the
  travel time, restores every sample with it, recomputes the baselines and levels and ends on 30 alert episodes, every
  plant as published; on the simulator's clean truth the same route files 30 and the temperature-dependent rate alone
  files 26, the towns' true shedding also 26 (R3a, R3b in checks.py).
- **Estimand:** the methods note (`wastewater_dashboard_methods_v4.pdf`, sections 3 to 6.1) with the prompt: the alert
  episodes of the 24 plants that open in the weeks starting 3 May to 27 September 2027, each plant's weekly value the
  mean log10 shed load per person of the week's samples, its baseline the 10th percentile of its weekly values of the
  weeks starting 6 April 2026 to 29 March 2027, an episode opening at 1.0 and closing below 0.5; the count against the
  published count.
- **No decoy:** nothing is planted: no memo, draft or stakeholder figure argues a count; the request names none; the
  dashboard's export is its published levels and episodes, correct on their basis and the bridge's starting total the
  prompt asks for; the study's field report gives its design and no result; the two distractors (rain gauges, the
  laboratory's quality assessment returns) give no plant a level.
- **No certified replay:** no certified or published shed-load figure exists for a method to reproduce; the method is
  found from the study's own pairs (the loss at the long trunk sewers more than doubling from winter to summer) and the
  field's first-order model.
- **Lesson:** a measurement's in-transit loss whose rate moves with a seasonal covariate does not cancel against a
  unit's own baseline the way a constant loss does; restoring it at the covariate's value for each measurement is what
  moves the levels, and the units with the longest transits move most. No build on file spends it (task247 refilled
  cloud gaps from both sides; task133 conditioned a curve on survival; no build takes wastewater as its object).

## Readability screen

Six tests per rung (stumping 2.1): 1 a filed sentence names the decisive quantity or sends the solver to it; 2 a
column, key or marker makes it a row predicate or a header-found join; 3 an opponent reflex reaches it; 4 a control or
corpus scores the rules or refutes the naive read; 5 the hygiene battery finds it; 6 one subtraction, ratio or half of
a reported figure.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 the published levels: 30 | the dashboard's export | the episodes sheet | yes, the operational record | none | no | read off | readable |
| 1 (default) one decay rate over each travel time: 30 | the methods note's shed load and the study | the study's ratios, the memo's travel times | yes, a decay constant from the study | the study's pairs fit one rate on average | no | one factor per plant | readable |
| 2 the samples divided by their PMMoV: 30 | none | the PMMoV rows | yes, the field's habit of normalising by the faecal marker | none | no | a ratio | readable |
| 3 a temperature term beside the travel time: 22 | none | the study's water_temperature_c | partly, a regression on the study's columns | the study's pairs | no | one regression | readable |
| 4 the temperature-dependent rate at the four study plants only: 28 | none | the study's plant codes | partly | the study | no | a fit | readable |
| 5 (decisive) the rate as a function of temperature at each composite's inlet temperature over every plant's travel time: 26 | no sentence names a temperature dependence; the methods note says the restoration rests on the study and the travel times | the study's water_temperature_c sits beside pH and conductivity, the historian's inlet_temperature_c beside the flow | no: the reflex is a constant rate or the marker | the study refutes the constant rate only when its ratios are read against the water's temperature or the season (0.69 against 0.31 log10 at Cleaveland Flat) | no | not linear: a rate per composite, then each plant's baseline, levels and episodes | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | winter 2027's episodes | those opening in the weeks starting 3 May to 27 September 2027 | those open at any time in the winter | same call | no plant is open on 26 April 2027 (SF9); methods section 5 |
| SF2 | a sample's week | the week of the day its composite ended | the week of the day it started | same call | same counts at every plant on both bases (asserted); methods section 4 |
| SF3 | the baseline | PERCENTILE.INC, the 10th percentile | PERCENTILE.EXC | same call | same counts (asserted); methods section 4 |
| SF4 | the reference weeks | the weeks starting 6 April 2026 to 29 March 2027 | none differs | converge | 52 weeks (asserted); methods section 4 |
| SF5 | the composite's flow | the form's (the published basis) | the historian's 24-hour inflow | same call | same counts on both bases (asserted); methods sections 3 and 6.2 |
| SF6 | the temperature | each composite's mean inlet temperature over its 24 hours | the month's or the season's mean; the study's plant, upstream or mean reading for the fit | same call | same counts at every plant (asserted, the variants) |
| SF7 | the travel time | the memo's population-weighted minutes | the shortest or longest sub-catchment | ruled out | methods section 6.1 "each plant's population-weighted travel time" (SF7 asserted on the memo) |
| SF8 | an episode's close | the first week back at Low (below 0.5) | the first week below High | ruled out | methods section 5 "back at Low" |
| SF9 | where episodes are followed from | the record's first week | the reference year's or the winter's first week | same call | every plant below 0.45 in the week of 26 April 2027 on both bases (asserted) |
| SF10 | the shed load's baseline | recomputed on the shed load | the published baseline kept | 28, ruled out | methods section 6.1 "exactly as sections 4 and 5 compute them" (asserted) |
| SF11 | a sample's result | the accepted run | the latest, the first or the mean run | same call | same counts (asserted); methods section 2 and the export notes |
| SF12 | the faecal-strength check on last winter's samples | no composite of April 2026 to September 2027 fails it | none differs | converge | asserted |
| SF13 | the decay's units | the study's natural-log ratios per hour, levels in log10 | the rate fitted on log10 ratios | same call | one rate in either unit (the fit's form) |
| SF14 | the population | the register's population served | none differs | converge | methods section 3 |
| SF15 | the published total | the dashboard's export | recomputed from the laboratory | converge | the same 30 and the same plants (asserted) |
| SF16 | counts and hours | whole numbers | none | converge | the prompt |
| SF17 | Ask A's window | local days, 1 April 2027 to 31 March 2028 | UTC days | same figures | no fault within a day of either edge (asserted) |
| SF18 | Ask B's composites | by the day the composite ended | by the day it started | same figures | no failing composite among the window's first or last two (asserted) |
| SF19 | Ask B's inflow where an hour lacks a reading | the mean of the valid readings times 24 | the raw sum, the valid sum, interpolation | same figures | every fill gives the same failures (asserted) |
| SF20 | Ask B's failure | more than 0.5 log10 above or below the median | below only | same figures | methods section 6.3; same failures (asserted) |
| SF21 | Ask B's 365 days before the composite's day | the 365 days before it | including the day 365 or 366 days before | same figures | no composite falls 365 or 366 days before another (asserted) |
| SF22 | Ask A's hour | an hour of the clock as it ran (8,784 in the year, two at 02:00 on 4 April 2027, none at 02:00 on 26 September 2027) | each wall-clock label of the year once | +1 at every plant, ruled out | the export note's span, "23:00 on 9 April 2028, 19,825 hours", one more than its 826 days of 24 labels (asserted) |

## Ladder

Five wrong rungs and the golden, each a defensible way to restore the shed load, each dying to one fact of the study
(per-plant counts on the cut pack, printed by `generator/pair.py --ladder`, asserted in `checks.py`).

| Rung | Construction | Answer | Dies to |
|---|---|---|---|
| 0 | the published levels (the dashboard's export) | 30, every plant as published | the dashboard moves to the shed load on 1 May (methods 6.1) |
| 1 (default) | one first-order rate fitted to the study (0.0408 an hour) over each travel time | 30, every plant as published | the study's own loss at the long sewers more than doubles from winter to summer, so a rate constant over the year is not the sewer's |
| 2 | the samples divided by their PMMoV | 30, every plant as published | PMMoV barely decays, so the ratio keeps the N1's own loss in, as constant over the year as the marker |
| 3 | a temperature term beside the travel time, ln(plant/upstream) = c0 + c1 tt + c2 T | 22: CRF, FNK, GLO and INB also lose their episode | the loss does not move with temperature at the short sewers (Dunkerley's 0.06 against 0.04 log10), so the term corrects them as much as the long |
| 4 | the temperature-dependent rate at the four study plants only | 28: ADS and CLF move | every plant's sewer decays by the same law over its own travel time (methods 6.1 names every plant's) |
| 5 (golden) | the temperature-dependent rate at each composite's inlet temperature over every plant's travel time | 26: ADS, ADE, TRN, CLF, SLT -1, ADW +1 | |

- **Margins.** The smallest uniform shift of a plant's weekly levels that moves its winter count is 0.10 at Ardenmouth
  West and 0.16 or more everywhere else on the shed load, 0.06 (Ardenmouth South) on the published basis. Every
  temperature-dependent route (linear in temperature, plant by plant, the upstream or plant reading, the composite's,
  the month's or the season's temperature, the historian's flow, the marker-normalised ratio in the study) gives every
  plant's count (asserted).
- **Position.** No wrong rung reaches 26; the four plants of the study reach two of the six moves.
- **Dominance.** The decisive step lifts the long sewers' baselines by 0.52 to 0.68 log10 (Ardenmouth West 0.37) while
  their winter peaks fall from 1.06 to 1.14 to 0.78 to 0.80; at the short sewers it moves nothing.
- **Grid.** Published, constant rate, PMMoV, additive term, study plants only, the rate at temperature: 30, 30, 30, 22,
  28, 26; the flows (form, historian) and runs (accepted, latest, first, mean) cross every cell with the same counts.
- **Worth.** Four episodes on the total and six plants' counts; the clean truth's towns shed 26 with the same six moves.

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | the register's 24 plants, every one in the count |
| 2 | Unit of account | one alert episode (methods 5) |
| 3 | Attribution window | episodes opening in the weeks starting 3 May to 27 September 2027 (methods 5, SF1) |
| 4 | As-of dating | Wednesday 12 April 2028: the laboratory to the composites of 6 April, the historian to 9 April; the cutover 1 May |
| 5 | Version basis | methods note v4 (section 6 from 1 May 2028); the study's 2026 pairs; the memo of November 2025 |
| 6 | Denominator | the register's population served (SF14) |
| 7 | Weighting | each week the plain mean of its samples' log10 loads (methods 4) |
| 8 | Window length | the 52 reference weeks (SF4); the composite's 24 hours |
| 9 | Boundary inclusivity | High at 1.0 or more, Low below 0.5 (methods 5); the winter's first and last weeks included |
| 10 | Rounding path | none before the count; whole numbers (SF16) |
| 11 | Tie-break | none needed |
| 12 | Maturity and censoring | every composite of the window analysed and accepted; no result is pending for winter 2027 |
| 13 | Order of operations | accepted runs, loads, the restoration, weekly values, baseline, levels, episodes |
| 14 | Row order | no step depends on file order |
| 15 | Duplicate resolution | the accepted run (SF11) |
| 16 | Identity normalisation | plant codes across the export, register and historian; the memo's codes |
| 17 | Netting against gross | none |
| 18 | Dimensional units | gene copies a litre; the study's per millilitre (ratios unit-free, SF13); minutes to hours; cubic metres |
| 19 | Code and status semantics | accepted, rejected, check (SF11); the bands (methods 5) |
| 20 | Integerisation | counts whole (SF16) |
| 21 | Clause scope | section 6.1 applies to every plant (rung 4); sections 4 and 5 on both bases (SF10) |
| 22 | Forward window contents | winter 2028 is planned on winter 2027's samples read on the shed load (the prompt, the request) |

## Literal reader

Executing the prompt and the methods note word for word: the episodes of the 24 plants opening in the weeks starting 3
May to 27 September 2027, on the shed load per person, its baselines and levels computed exactly as on the load. The
shed load needs the RNA the sewer destroyed restored, which no sentence quantifies; every restoration that takes the
study's decay as a first-order rate depending on the water's temperature at each composite's own temperature, over
each plant's travel time, files 26 with the same six moves (linear or exponential in temperature, pooled or plant by
plant, the plant's, upstream or mean probe reading, the composite's, the month's or the season's temperature, either
flow), and every convention row of the fork table files 26. The easy answer, 30, comes from an easy method (a constant
rate or the marker) on the same literal estimand, never from another reading.

## Oracles

None for the call: no shed-load figure, earlier restoration or ranking on it ships. The dashboard's export ties the
published basis under every handling; a constant restoration reproduces its levels by algebra, which is the stump's own
identity and holds whether or not the export ships. The paired study confirms the temperature dependence only when its
ratios are read against the water's temperature or the season. For the asks, the historian's export note (the
definition of a valid reading) and the year's own clock referee Ask A, and the contract report's method line referees
Ask B; neither names a row or a plant.

## Ask sheet

**Ask A, each plant's hours from 1 April 2027 to 31 March 2028 with no valid inlet flow reading in the historian (24
figures, whole hours).** H18: the historian becomes the dashboard's flow source at the cutover (methods 6.2), so its
hours without a valid reading are the input audit of the new basis; the call reads the historian only for each
composite's temperature over its 24 hours from April 2026 to September 2027, which no fault reaches. Use: the desk fills
by hand every composite whose flow the historian cannot give. Primary devices: D8 (a clock against the window): the
historian keeps New Zealand local time, so the year has 8,784 real hours, 02:00 on 26 September 2027 never happens and
02:00 on 4 April 2027 happens twice with a row each; a grid of every wall-clock hour counts the skipped hour as a gap at
every plant (+1), and removing duplicate plant-and-timestamp rows, the reflex repair for the 165 rows the historian
re-sent after outages, deletes one of the two real 02:00 readings at every plant (+1). D4 (absence as the signal): an
hour the historian received nothing for has no row, so counting the invalid rows the export holds misses every
drop-out (-12 to -47 at every plant). The export note gives its span as 19,825 hours, one more than its days of 24
wall-clock labels, so the clock's hours are the record's (SF22), with no sentence naming the clocks. Hazards: held readings (every reading after the first of four or more identical
consecutive readings; counting the whole run adds 1 to 3 at 17 plants), blank flows, zero and negative readings, the
re-sent exact duplicates. Path: the historian, its export note, the dictionary, the request (4 files, 4 columns).
Realism: the outstations moved to a new cellular network in October 2027; hourly historians export local time and skip
or repeat the changing hour.

**Ask B, each plant's composites from 4 October 2027 to 30 March 2028 that fail the faecal-strength check (24 figures,
whole counts).** H18: the check starts with the cutover (methods 6.3) and every failing composite comes to the desk
before its result enters the level, the desk's second stream of work; the call reads no PMMoV row and no composite after
September 2027. Primary device: D3 (units set per source): the contract laboratory that analysed the closure's
composites (23 December 2027 to 6 January 2028, five at every plant) reports gene copies per microlitre of extract, its
method line giving the volumes (100 mL concentrated, the pellet resuspended in 2 mL, 200 microlitres extracted, eluted in
100), so a copy per microlitre of extract is 10,000 a litre; read as copies a litre, scaled to the litre without the
aliquot (x1,000) or as microlitres to litres (x1,000,000), every closure composite fails at every plant (+3 to +5 at all
24). Hazards: the form's flow at the three plants with a second inlet channel since 18 October 2027 (the sampler's
controller sees one channel: +31 to +43 at KSB, PLH and UWD); the first analysis run of a re-extracted sample (+1 to +3
at 20 plants); the report left out (-1 to -2 at 5 plants, the closure's own failures missed); the historian's faults
inside composite windows (every fill gives the same failures, SF19); the report's abbreviated site names. Path: the
results export, its notes, the contract report, the register, the historian, its note, the methods note, the dictionary
(8 files, 12 columns: plant_code, composite_end, target, status, result_gc_per_l, composite_flow_m3, client site,
sampled, analyte, result, population_served, inlet_flow_m3h). Realism: contract laboratories report per microlitre of
extract with their method's volumes, and a second inlet channel's flow reaches the historian before the sampler's
controller.

Main population zero-counts: the call reads the laboratory's N1 accepted runs of the composites of January 2026 to
September 2027 and the historian's temperatures over their 24 hours; no fault, spoiled composite, contract composite or
second channel sits in those rows, and the call computes the same without the contract report and the distractors (S1).

| Hazard | Asks moved | Per-ask deltas (largest) |
|---|---|---|
| the skipped and repeated clock hours (D8, primary) | A | +1 at every plant |
| drop-outs without a row (D4, primary) | A | -47 |
| held readings counted whole | A | +3 |
| the contract report's units (D3, primary) | B | +5 at every plant |
| the form's flow at the two-channel plants | B | +43 |
| the first analysis run | B | +3 |
| the contract report left out | B | -2 |

| Ask row | The cracker (landed the call, hygiene battery, every filed rule executed) | Verdict |
|---|---|---|
| Ask A, hours, all 24 plants | the historian with duplicate plant-and-timestamp rows removed, on the year's local clock hours (or every wall-clock hour) | miss |
| Ask B, failing composites, all 24 plants | the historian's inflow, the accepted runs, the contract report's copies per microlitre of extract scaled to the litre through the concentrate (x1,000) | miss |

Measured by: generator/pair.py on the cut pack: the cracker keeps 0 of the 48 ask figures; the lazier paths keep 0 to
4 (the form's flow with first runs keeps 4); a response meeting every device keeps all 48 (58.1 with it on the call).

Pair ceiling: 30.6 ((38 + 7 + 55 x 0) and (4.6 + 7 + 55 x 0.083), averaged)

Mirror leakage: 8.3 per cent of ask weight

## Pre-ship check

1. Domain: the call stands on each plant's weekly level on the shed load, recovered from the plant's concentration by
   the field's first-order model of the RNA's in-sewer decay at a rate that rises with the water's temperature, over
   the population-weighted travel time, the rate measured by paired composites at the trunk's head and at the plant;
   with another field's nouns (a hospital's admissions, a utility's meter reads) there is no sewer, no travel time over
   which a virus's RNA decays faster in warm water and no paired upstream composite, so the task stops making sense.
2. Two layers: Layer 1 (the export by analysis run, the form's flow, the study's copies per millilitre in triplicate
   and its missed visits, the memo's minutes, the historian's local time across both clock changes) is neutral on the
   call (SF2, SF5, SF11, the R2 block, S1). Layer 2 is the temperature-dependent restoration, asserted alone to move the
   easy route (30) to the golden (26) on the simulator's clean truth, where the towns' true shedding also gives 26 (R3).
3. No banned stump decides: nothing is planted (the dashboard's export is its published basis, correct and asked for
   as the bridge's start; the field report gives no result); not semantics (every field read right, the single-rate
   route still files 30); not rule application (the methods note files the estimand and no model of the decay).
4. Gate G: no shipped artifact counts episodes on the shed load; the dashboard's export is the context artifact
   (correct on its own basis, declared in metadata.json); the two distractors (rain gauges, the laboratory's quality
   assessment returns) give no plant a level.
5. Determinism: thirteen temperature-dependent routes (linear, exponential or plant-by-plant in temperature, the
   plant's, upstream or mean reading, the composite's, month's or season's temperature, either flow, the N1 over
   PMMoV ratio in the study) give every plant's count; 20 fork rows asserted; the verifier recomputes every graded
   figure by its own code (the IANA zone, a non-linear fit; 242 checks); two builds byte-identical.
6. Fingerprint: heart WARN (overuse.org_family, repeat.deliverables, answered in the Draw; same_puzzle_older NOTE
   differentiated against task133); the surface screen promotes no pair and reads the four card personas only.
7. Judge (one isolated thread, Sonnet, medium, the bundle and the graded blocks only, on target.zip 4733488b):
   DETERMINISTIC, APPROVE; every graded figure reproduced (30 published, 26 on the shed load with the same six moves,
   the decay fit, the seasonal losses, all 48 ask figures); Gate G method_or_model_selection, analytical_non_defect;
   Gate H domain, layers and decisive step pass; spec gates pass. It varied theta from 1.07 to 1.10, scaled the rate
   0.5 to 2 times and tried linear, plant-only, upstream-only and monthly temperatures and the historian's flow: 26
   every time; the temperature term cuts the study's residual sum of squares from 7.57 to 1.02 (F = 637). Taken from
   it: its fit gave theta 1.0875, on the 1.087/1.088 edge, so the write-up states 0.050 an hour, about 9 per cent a
   degree and theta 1.09, the figures every fitting route prints (asserted); and its finding 1, the hour at the clock
   changes in Ask A, closed by stating the export's span in hours in the historian note (19,825, one more than its
   days of 24 labels, SF22), the fact the reader then used to settle the hour without any sentence naming the clocks.
   The shipped bundle differs from the judged one by that sentence only; no graded figure moved.

## Leak check

leak.py (as-of 2028-04-12): REVIEW, no LEAK; author vocabulary, column names, announcements, hidden content, dates
and the prompt gate clean. Each REVIEW line, answered:

- The field report names Ardenmouth South and Cleaveland Flat beside "travel times": they are two of the study's four
  plants, named as its design; harmless.
- The dictionary, the folder's contents and the methods note carry the words of the call (verification desk, alert
  episodes, winter): the fiction's own vocabulary; none states a count; harmless.
- Design-note vocabulary in the documents (wastewater, episode, baseline, composite, travel, temperature): the
  domain's own words; no document says how the decay varies or names a restoration (R1 asserts no "decay rate", "per
  degree", "warm water" or temperature dependence in any document, through a control sentence found first); harmless.
- The prompt's second sentence carries plant, level and shed load: the asks' own nouns; harmless.
- The travel-time memo names plants beside numbers: a lookup of travel times, not a ranking on the decision; harmless.

Reader (isolated, Sonnet, medium, the prompt and a fresh pack only), three reads: the first on 4733488b, the second
after the span sentence, the third after its rewording. Q1 to Q4 none in every read; Q6 analytical; each read the
decisive step as a decay-per-travel-time fit from the study and none named the water's temperature. Taken from them:
the clock-change hour (closed as above), the span sentence first worded as if every plant held 19,825 rows (reworded
as the export's span, with a row for each hour the historian holds), and two ask readings answered by assertions
already in place (the median window's boundary, SF21; the closure's composites as the plant's composites, methods
6.3). Left as they are: the main wave's episodes opening within three weeks of each other at most plants (a regional
wave), the register's tidy populations.

## Tried and rejected

- 2026-10-18, the seed's own air quality network and any environmental-monitoring pairing: banned against task247
  (domain plus objective), and a fourth environmental build in the wave reads as a monoculture.
- 2026-10-18, wastewater levels with non-detects below the detection limit: the substitution-against-censored-estimator
  driver is task189's (left-censoring at limits that differ by laboratory).
- 2026-10-18, two-source capture-recapture of notified cases before electronic laboratory reporting: the estimate
  moves with every defensible stratification (Chapman against Lincoln-Petersen, setting against setting by district
  by age), so the count is not determinate; capture-recapture is spent in task199 and named in task243.
- 2026-10-18, coders' drift against a master coder on a stratified double-coded sample: the rater analysis reads the
  same with any field's raters (the noun swap fails), and measurers against a reference repeats task246's world.
- 2026-10-18, the episode count read on weekly levels without a way out of High: with no exit rule each plant's count
  chatters with the noise around the threshold, so the count moved with the fitted decay model; the filed episode rule
  needs an entry level and a lower exit level.

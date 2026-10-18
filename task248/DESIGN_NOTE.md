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

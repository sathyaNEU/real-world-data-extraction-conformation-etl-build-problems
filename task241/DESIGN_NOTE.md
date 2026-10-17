# task241 design note

Architecture 1, wave 3, seed DQ14 (which domain estimates fail the calibration margin check and are reissued): the
seed's decision (a release's reissue list) and quantity (each estimate against its calibration margin) only. The
seed's own pairing (survey research, nonresponse and calibration) is banned against task240, three builds back, so
the release moves to an ocean data centre: the Instituto Oceânico do Atlântico runs a regional array of 24 profiling
floats in the Iberian Basin, each surfacing every ten days with a temperature and salinity profile from 2,000 dbar,
and once a year its data centre runs delayed-mode quality control on the year's salinity before the delayed-mode
files go to the international data assembly centre. A float whose conductivity sensor has drifted or was off from
deployment has its salinity adjusted in the release; the rest are released as measured.

## Draw

Card `cards/task241.json` (architecture 1, registered 2026-10-17). Guard verdict WARN, each answered here:
repeat.gate_g (decomposition_attribution against task194 v2, a provider-quality risk adjustment: the shared key is the
generic mechanism, the builds share no quantity or file); repeat.deliverables (xlsx and png against task159, a
forecast's table and chart: here a calibration scorecard and a figure of each float's offset); repeat.question_form
(which, against task194: the decision designates floats, so the form follows it). test.same_puzzle_older against
task148 v2 is differentiated on the card (queue patience from censored waits; nothing shared).

- **Pairing.** Physical & Environmental Sciences / sensor-calibration-measurement, serving Data Quality Monitoring &
  Alerting. Not banned against the last three builds (task240, task194, task159). The object is the health of the
  float array's salinity record (whether each float's conductivity sensor still reads the ocean's salinity), the call
  a monitoring decision on the delayed-mode release.
- **Niche.** Delayed-mode calibration of profiling-float salinity against ship reference data: the float's
  temperature sensor is stable and its conductivity cell drifts, so the water's temperature identifies the water
  mass, and the reference gives that water's salinity at that place.
- **The call.** Which of the 24 floats have their 2027 salinity adjusted in the delayed-mode release.
- **Shape.** 10, scorecard against thresholds: each float's checks (its salinity offset against the 0.010 tolerance,
  and the asks' delivery checks). Decision designation_set, answer set_of_items, question form which.
- **Strategy.** population_selection (the reference water a float's reading is compared with: the same water mass, at
  the same place), G16 decisive (the comparison the estimand entitles), G6 (the water at a fixed pressure changed
  under the comparison), G14 (the basin's pooled relation does not apply at the float's position); gap time first
  (the reference years' water column against 2027's) then population; Gate G decomposition_attribution (a float's
  apparent offset split into the ocean's change and the sensor's error); calibration other (the ship reference casts,
  an independent calibrated measurement of the water); context artifact planning_thread (the data management lead's
  release thread carries the tolerance, layer and period); layer 2 family field_method, pattern
  own:float-salinity-offset-on-isotherms-against-local-reference.
- **Forum, event, organisation.** line_manager_or_team (the data centre's head signs the release), period_close (the
  2027 delayed-mode release closing the year's record), research_or_statistics_office. All clear the last three.
- **People** (`guard.py names --geo Portugal --seed 241`, locale pt_PT): Naiara Nogueira, the array's delayed-mode
  quality-control operator; Tiago Tavares, the data centre's data management lead, who wrote the release thread;
  Patrícia Araújo, the float programme's engineer, who keeps the float register.
- **Deliverables.** `ioa_dmqc_salinity_2027.xlsx` (each float's offset and decision, and the asks' figures) and
  `ioa_dmqc_offsets_2027.png` (each float's offset against the tolerance band).
- **As-of.** Friday 7 January 2028: the year's last profiles came in before 1 January, the reference database was
  frozen on 15 December 2027, and the delayed-mode files are due at the assembly centre on 21 January.
- **Data-native sentence.** Below the Mediterranean outflow the deep water's temperature fixes its salinity, but the
  layer heaves with eddies and sat deeper in 2027 than in the reference years, and the salinity on a given isotherm
  falls westward as the outflow thins; a float's salinity error therefore shows only against reference water of the
  same temperature at the float's own position, while at fixed pressure the heave reads as sensor error.

Sources, one line each (what it teaches; how this build differs):
- Owens and Wong (2009) and the delayed-mode practice of profiling-float arrays: salinity calibrated against
  reference data on potential-temperature levels, mapped to the float's position; here the comparison and the mapping
  are the analyst's to choose, never named in the pack.
- Böhme and Send (2005) on regional reference data: water-mass gradients across a basin bias a pooled reference;
  here the gradient is the Mediterranean outflow thinning westward.
- The physical oceanography of the Iberian Basin (Mediterranean water at 1,000 to 1,200 m, the deep layer's tight
  temperature-salinity relation below it): the world's structure, generated, never a real dataset.

## Default path

1. Read the release thread: a float's salinity is adjusted when its offset, averaged over its 2027 ascending profiles
   in the 1,400 to 1,900 dbar layer, exceeds 0.010 in magnitude; values the real-time checks flagged bad are left out.
2. Build each float's 2027 ascending profiles (one copy of a resent profile, no descending or test profiles, good
   values only).
3. Interpolate each profile's salinity onto standard pressure levels across the layer, and take the reference casts'
   mean salinity at the same levels.
4. Each profile's offset is the mean difference across the levels; each float's offset the mean over its profiles;
   adjust where it exceeds 0.010.

Ends on: 17 of the 24 floats adjusted, one of the four drifting floats among those missed (prototype figures, to be
replaced by the tuned simulator's).

Golden: 6 floats adjusted (four drifting fresh, two salty from deployment), from each profile's salinity on
temperature levels against the reference water at the profile's own position.

## Stump sentence

A competent analyst interpolates each float's 2027 salinity and the reference casts' mean salinity onto common
pressure levels across the 1,400 to 1,900 dbar layer and files 17 of the 24 floats adjusted, one of the four drifting
floats among those missed; the step that lands it there is comparing at fixed pressure, when the layer heaved deeper
in 2027 than in the reference years and the salinity of water at a given temperature falls westward across the basin,
so only the offset on temperature levels against reference water at the float's own position gives the six.

## Three rules

- **Task type:** physical-environmental-sciences / sensor-calibration-measurement, which serves Data Quality
  Monitoring & Alerting (the calibration of an observing array's sensors and the health of the record they produce).
- **Domain test:** the quantity that decides is each float's conductivity-sensor offset, estimated the way delayed-mode
  quality control of profiling floats estimates it: against ship CTD reference data on temperature levels, where the
  deep water masses' temperature-salinity relation is conserved, mapped to the float's position.
- **Swap:** "which floats have their 2027 salinity adjusted" rewritten as "which ward thermometers have their 2027
  readings adjusted" with patients for water: there is no water column that heaves, no water mass whose temperature
  fixes its salinity and no basin-scale property gradient, so the task stops making sense.
- **Layer 1:** profiles at two grains (the profile index with times as days since 1950 in UTC, the level file);
  real-time quality flags on every value; profiles received twice when a transmission was resent; descending profiles
  beside ascending ones; each float's cycle 0 test profile; reference casts from several cruises, the older ones in
  the IPTS-68 temperature scale; the data centre's receipt log in Lisbon local time. Each is how the float, the
  satellite link or the data centre writes the record; none is placed to be caught.
- **Layer 2:** field_method: a sensor's error read against the true value of the medium it sampled, which here means
  comparing salinity on temperature levels (the water mass) against reference water at the float's position (the
  basin's gradient), not at fixed pressure against the basin's average.
- **Decisive step:** reading each float's salinity against the reference on potential-temperature levels mapped to
  the profile's position, the way delayed-mode calibration of float salinity is done, rather than at fixed pressure
  against the reference casts' mean.
- **Not semantics:** reading every flag, code, unit and time right (resent profiles once, descending and test profiles
  out, bad values out, IPTS-68 converted) still leaves the default path on 17 floats: the false flags come from the
  comparison, not from any value read.
- **Not rule application:** the release thread files the estimand (each float's salinity error against the true
  salinity of the water it sampled, averaged over its 2027 profiles in the layer), the tolerance and the period; no
  rule says how to know the water's true salinity, so executing every stated rule at fixed pressure still files 17.
- **Analyst test:** a strong analyst who reads every flag and file right and differences each float's salinity against
  the reference casts' salinity at the same pressures adjusts 17 floats (Ends on: 17 of the 24 floats adjusted, one of
  the four drifting floats among those missed); one who compares on temperature levels against the whole basin's
  reference adjusts another 10, and one who measures drift from each float's first profiles finds only the four
  drifting floats; only temperature levels against reference water at each profile's position give the six.
- **Estimand:** the release thread (`ioa_dmqc_2027_release_thread.eml`) fixes the population (the 24
  floats' 2027 ascending profiles, good values in the 1,400 to 1,900 dbar layer), the quantity (the salinity the float
  reported less the true salinity of the water it sampled, averaged over the float's profiles), the tolerance (more
  than 0.010 in magnitude) and the decision (adjusted in the release).
- **No decoy:** nothing is planted: no earlier calibration result, draft list or stakeholder figure ships; the 2027
  heave and the basin's gradient are how the ocean is, not errors in a file.
- **No certified replay:** no certified or published 2027 offset exists for a method to reproduce.
- **Lesson:** a sensor's error is measured against what the medium really held at that moment and place; when the
  medium moves under a fixed coordinate, the comparison has to follow the property that identifies the medium, which
  no build on file teaches (task229 converts a daily mean through a convex rating curve; task239 separates two levels
  of a factor structure).

## Tried and rejected

- The seed's pitfall (one raking pass against raking to convergence): executing a filed procedure, rule application;
  dropped at the draw.
- The seed's survey world: the pairing is banned against task240; dropped at the draw.
- A surveillance completeness check by capture-recapture with dependent sources (epidemiology): task236 already reads
  a capture rate against an independent sample; too close; dropped at the draw.
- A laboratory calibration curve's weighting (weighted against unweighted least squares): either the weighting is
  filed (rule application) or two least-squares readings stay open (a fork); dropped at the draw.

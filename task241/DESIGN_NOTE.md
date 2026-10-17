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
- **Shape.** 10, scorecard against a threshold: each of the 24 floats' 2027 offset against the 0.010 tolerance and its
  decision (24 offsets, 24 decisions), the call, the reference coverage by year (11 counts), the delivery record by
  month (12 counts), the chart (bars, the band, the marked floats) and the two files: about 75 criteria before the
  rubric folds them. Decision designation_set, answer set_of_items, question form which.
- **Strategy.** population_selection (the reference water a float's reading is compared with: the same water mass, at
  the same place), G16 decisive (the comparison the estimand entitles), G6 (the water at a fixed pressure changed
  under the comparison), G14 (the basin's pooled relation does not apply at the float's position); gap time first
  (the reference years' water column against 2027's) then population; Gate G decomposition_attribution (a float's
  apparent offset split into the ocean's change and the sensor's error); calibration other (the ship reference casts,
  an independent calibrated measurement of the water); context artifact planning_thread (the data management lead's
  release thread carries the tolerance, layer and period); layer 2 family field_method, pattern
  own:float-salinity-offset-on-isotherms-against-local-reference.
- **Forum, event, organisation.** line_manager_or_team (the data management lead signs the release off), period_close
  (the 2027 delayed-mode release closing the year's record), research_or_statistics_office. All clear the last three.
- **People** (`guard.py names --geo Portugal --seed 241`, locale pt_PT): Naiara Nogueira, the array's delayed-mode
  quality-control operator; Tiago Tavares, the data centre's data management lead, who wrote the release thread;
  Patrícia Araújo, the float programme's engineer, who keeps the float register and wrote the float models summary.
- **Deliverables.** `ioa_dmqc_salinity_2027.xlsx` (each float's offset and decision, the reference coverage and the
  delivery record) and `ioa_dmqc_offsets_2027.png` (each float's offset against the tolerance band).
- **As-of.** Friday 7 January 2028: the year's last profiles came in before 1 January, the reference data were frozen
  on 15 December 2027, and the delayed-mode files are due at the assembly centre on 21 January. The call is
  retrospective on 2027's record by design: a delayed-mode release corrects a closed year's data; what it settles is
  what goes out on 21 January.
- **Data-native sentence.** Below the Mediterranean outflow the deep water's temperature fixes its salinity, but the
  layer heaves with eddies and sat about 17 dbar deeper in 2027 than in the reference years, and the salinity on a
  given isotherm falls westward as the outflow thins; a float's salinity error therefore shows only against reference
  water of the same temperature at the float's own position, while at fixed pressure the heave reads as sensor error.

Sources, one line each (what it teaches; how this build differs):
- Owens and Wong (2009) and the delayed-mode practice of profiling-float arrays: salinity calibrated against
  reference data on potential-temperature levels, mapped to the float's position; here the comparison and the mapping
  are the analyst's to choose, never named in the pack.
- Böhme and Send (2005) on regional reference data: water-mass gradients across a basin bias a pooled reference;
  here the gradient is the Mediterranean outflow thinning westward.
- The physical oceanography of the Iberian Basin (Mediterranean water at 1,000 to 1,200 m, the deep layer's tight
  temperature-salinity relation below it): the world's structure, generated, never a real dataset.

## Default path

1. Read the release thread: a float's offset is the salinity it reported less the true salinity of the water it
   sampled, the mean difference over each profile's good values between 1,400 and 1,900 dbar averaged over the
   float's 2027 ascending profiles; more than 0.010 in magnitude is adjusted; good values are flags 1 or 2.
2. Build each float's 2027 ascending profiles from the register and the profile index (the complete file of a resent
   profile, no descending profiles, the partner float out) and their good values in the layer.
3. Put both reference sources on pressure (the archive is in dbar; the RHD extract's depths taken to pressure, its
   temperatures already ITS-90), interpolate every reference cast to a 10 dbar grid, and take the casts' mean
   salinity at each pressure.
4. Each good float value less the reference mean at its pressure; each profile's offset the mean over its values;
   each float's the mean over its profiles; adjust where it exceeds 0.010.

Ends on: 14 of the 24 floats adjusted, the six whose sensors are off and eight whose sensors read true.

Golden: 6 floats adjusted (1990001, 1990004, 1990005 and 1990008 reading fresh, 1990007 and 1990012 reading salty),
from each profile's salinity on potential-temperature levels against the reference water at the profile's own
position.

## Stump sentence

A competent analyst differences each float's good 2027 salinity values between 1,400 and 1,900 dbar against the
reference casts' mean salinity at the same pressure and files 14 of the 24 floats adjusted, the six whose sensors are
off and eight whose sensors read true; the step that lands it there is comparing at fixed pressure, when the deep layer
sat deeper in 2027 than in the reference years and heaved with eddies, and the salinity of water at a given
temperature falls westward across the basin, so only the offset on potential-temperature levels against reference
water at each profile's own position gives the six.

## Three rules

- **Task type:** physical-environmental-sciences / sensor-calibration-measurement, which serves Data Quality
  Monitoring & Alerting (the calibration of an observing array's sensors and the health of the record they produce).
- **Domain test:** the quantity that decides is each float's conductivity-sensor offset, estimated the way delayed-mode
  quality control of profiling floats estimates it: against ship CTD reference data on potential-temperature levels,
  where the deep water's temperature-salinity relation is conserved, mapped to the float's position.
- **Swap:** "which floats have their 2027 salinity adjusted" rewritten as "which ward thermometers have their 2027
  readings adjusted" with patients for water: there is no water column that heaves, no water mass whose temperature
  fixes its salinity and no basin-scale property gradient, so the task stops making sense.
- **Layer 1:** profiles at two grains (the profile index with times as days since 1950 in UTC, the level file); real-
  time quality flags on every value; profiles received twice when a transmission broke off; descending profiles beside
  ascending ones; a partner institute's float decoded beside the array; the model K floats' firmware stamping each
  profile at the start of its ascent; reference casts from two sources, the institute's archive (the 2015 and 2016
  cruises in IPTS-68) and an international extract (depth in metres, positions to 0.01 degree, decimal-hour times,
  the institute's own casts again under the database's ids); stations worked twice a few hours apart; casts stopping
  short of 2,000 dbar; the data centre's receipt log on the server's Lisbon clock. Each is how the float, the
  satellite link, the ship's processing or the data centre writes the record; none is placed to be caught.
- **Layer 2:** field_method: a sensor's error read against the true value of the medium it sampled, which here means
  comparing salinity on potential-temperature levels (the water mass) against reference water at the float's position
  (the basin's gradient), not at fixed pressure against the casts' mean.
- **Decisive step:** reading each float's salinity against the reference on potential-temperature levels mapped to
  the profile's position, the way delayed-mode calibration of float salinity is done, rather than at fixed pressure
  against the reference casts' mean.
- **Not semantics:** reading every flag, code, unit and time right (resent profiles once, descending profiles and the
  partner float out, bad values out, IPTS-68 converted, depths taken to pressure) still leaves the default path on 14
  floats: the false adjustments come from the comparison, not from any value read (R3a on the clean truth: 15).
- **Not rule application:** the release thread files the estimand (each float's salinity error against the true
  salinity of the water it sampled, averaged over its 2027 profiles in the layer), the tolerance and the period, and
  no rule says how to know the water's true salinity, so executing every stated rule at fixed pressure still files 14.
- **Analyst test:** a strong analyst who reads every flag and file right and differences each float's salinity against
  the reference casts' salinity at the same pressures adjusts 14 floats (Ends on: 14 of the 24 floats adjusted, the
  six whose sensors are off and eight whose sensors read true); one who compares on potential-temperature levels against
  the basin's pooled reference adjusts 10 to 14 depending on the pooled fit (13 for a quadratic), and one who measures drift from each float's first profiles finds only the
  four drifting floats; only potential-temperature levels against reference water at each profile's position give the
  six.
- **Estimand:** the release thread (`ioa_dmqc_2027_release_thread.eml`) fixes the population (the 24 floats' 2027
  ascending profiles, good values in the 1,400 to 1,900 dbar layer), the quantity (the salinity the float reported
  less the true salinity of the water it sampled, the mean over the profile's good layer values averaged over the
  float's profiles), the tolerance (more than 0.010 in magnitude) and the decision (adjusted in the release).
- **No decoy:** nothing is planted: no earlier calibration result, draft list or stakeholder figure ships; the 2027
  heave and the basin's gradient are how the ocean is, not errors in a file; the recovered-sensor checks are other
  floats' laboratory results and rank nothing in this array.
- **No certified replay:** no certified or published 2027 offset exists for a method to reproduce.
- **Lesson:** a sensor's error is measured against what the medium really held at that moment and place; when the
  medium moves under a fixed coordinate, the comparison has to follow the property that identifies the medium, which
  no build on file teaches (task229 converts a daily mean through a convex rating curve; task239 separates two levels
  of a factor structure).

## Readability screen

Six tests per rung (stumping 2.1): 1 a filed sentence names the decisive quantity or sends the solver to it; 2 a
column, key or marker makes it a row predicate or a header-found join; 3 an opponent reflex reaches it; 4 a control
or corpus scores the rules or refutes the naive read; 5 the hygiene battery finds it; 6 one subtraction, ratio or
half of a reported figure.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 (default) every good value at fixed pressure against the reference casts' mean: 14 | the thread names the layer in dbar | pres on both sides | yes, the natural comparison of two profiles | none | no | one subtraction | readable |
| 1 at fixed pressure against the nearest twelve casts: 13 | none | positions on both sides | yes, an analyst who knows the basin is not uniform | none | no | one subtraction | readable |
| 2 drift from each float's own first profiles: 4 | none | juld | yes, the drift-detection reflex | none | no | one subtraction | readable |
| 3 potential-temperature levels against the basin's pooled reference: 13 (10 to 14 across pooled fits) | none | temp, psal, pres | partly, an analyst who knows the water mass is the comparison | none | no | a fit and a subtraction | readable |
| 4 (decisive) potential-temperature levels against the reference water at the profile's position: 6 | no sentence names temperature levels, position or the mapping; the thread says only "the true salinity of the water it sampled" | no potential temperature, reference salinity or offset ships; positions and in-situ temperature are ordinary columns | no: the reflex compares at fixed pressure or pools the reference | no earlier offset, calibration result or control ships | no | not linear: potential temperature, a reference field in temperature and position, per-level differences | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | 2027 profiles | the profiles the floats surfaced with in 2027 | juld's year | same call (no profile's juld falls in another year than its surfacing) | the thread; same call (asserted) |
| SF2 | good values | flag 1 or 2 in pressure, temperature and salinity | salinity's flag alone | same call (no pressure or temperature value in the layer is flagged) | the thread; same call (asserted) |
| SF3 | a profile received twice | the file carrying every level | both files kept | same call | the thread ("the file that carried every level"); same call (asserted) |
| SF4 | the array's floats | the register's 24 | the partner float too | same call (the partner reads true) | the thread; same call (asserted) |
| SF5 | more than 0.010 | strictly greater in magnitude | 0.010 or more | same call (no offset within 0.006 of the tolerance) | the thread; same call (asserted) |
| SF6 | the float's offset | the mean of its profiles' means | the mean of all its layer values | same call (offsets within 0.0005) | the thread ("averaged over the float's 2027 ascending profiles"); same call (asserted) |
| SF7 | salinity | practical salinity | absolute salinity | same call (offsets scale by 1.005) | the dictionary; same call (asserted) |
| SF8 | temperature levels | potential temperature | in-situ temperature | same call | same call (asserted) |
| SF9 | the reference data | the archive and the RHD extract | either alone | same call | the thread and the reference note; same call (asserted) |
| SF10 | between 1,400 and 1,900 dbar | the ends inclusive | exclusive | same call | same call (asserted) |
| SF11 | the offset's sign | the float less the water | the water less the float | same set (magnitude) | the thread ("the salinity the float reported less the true salinity") |
| SF12 | more than 0.010 in magnitude | either sign | fresh only | another set | the thread ("in magnitude") |

## Ladder

Four wrong rungs and the golden, each a defensible way to read a float's salinity error, each dying to one fact of
the record (figures on the cut pack, asserted in `checks.py`).

| Rung | Construction | Answer | Dies to |
|---|---|---|---|
| 0 (default) | each good value at fixed pressure against the reference casts' mean | 14: the six and 1990002, 1990003, 1990010, 1990015, 1990016, 1990022, 1990023, 1990024 | the 5.5 degree isotherm sat 17 dbar deeper in the 2027 float profiles than in the casts, and eddies move it further; water at a fixed pressure in 2027 is not the water the casts sampled there |
| 1 | at fixed pressure against the nearest twelve casts | 13: the six and 1990002, 1990003, 1990010, 1990015, 1990016, 1990021, 1990024 | the same heave; position does not undo it |
| 2 | drift measured from each float's own first 2027 profiles | 4: the drifting four | 1990007 and 1990012 were off from deployment, so their first profiles carry the same error |
| 3 | potential-temperature levels against the basin's pooled reference | 13: the six and 1990009, 1990014, 1990016, 1990020, 1990021, 1990022, 1990023 (10 to 14 across pooled fits, every one keeping the six) | the reference water freshens westward on every temperature level (0.0036 per degree of longitude at 5.5 degrees) |
| 4 (golden) | potential-temperature levels against the reference water at the profile's position | 6 | |

- **Margins.** The adjusted six read 0.020 to 0.030 from the water; the largest of the other 18 reads 0.003. Every
  position-mapped implementation checked (nearest 5 to 100 casts, casts within 1 to 5 degrees, Gaussian weights of 2 to
  4 degrees, a fit in position, in-situ temperature, either source alone) files the same six, and the local ones
  reproduce every offset within 0.003.
- **Position.** The six are reached by no other rung: fixed-pressure variants file 13 to 17 (seven to eleven clean
  floats among them), pooled references 10 to 14 (four to eight clean), the drift reading 4.
- **Dominance.** The decisive move takes the eight clean floats of the default path from over 0.010 down to 0.003 or
  less, and leaves the six over the tolerance.
- **Grid.** Fixed pressure by mean, median, nearest 5, 12, 20 or 40 casts, standard levels every 10 or 50 dbar, depths
  as pressure, archive alone (13 to 17); temperature levels pooled by quadratic, cubic or binned means, either source
  alone or the layer alone (10 to 14); drift (4); temperature levels at position (6). On the simulator's clean truth the
  same rungs file 15, 13, 12, 4 and the golden six (R3).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | the register's 24 floats, their 2027 ascending profiles (the thread); the partner float and descending profiles out (SF4) |
| 2 | Unit of account | one float's 2027 offset: the mean of its profiles' mean differences (the thread, SF6) |
| 3 | Attribution window | profiles the floats surfaced with in 2027 (SF1) |
| 4 | As-of dating | the pack drawn on 7 January 2028; every 2027 profile's complete file received by then |
| 5 | Version basis | the file carrying every level of a resent profile (SF3); the reference data as frozen on 15 December 2027 |
| 6 | Denominator | the true salinity of the water sampled; estimated from the reference data, the method open and forced by the record (C1 across implementations) |
| 7 | Weighting | each profile equally within a float; each value equally within a profile (the thread) |
| 8 | Window length | one year of profiles; the reference 2015 to 2025 |
| 9 | Boundary inclusivity | more than 0.010 (SF5); no offset within 0.006 of it |
| 10 | Rounding path | offsets from unrounded values, three decimals at the close; the call never depends on rounding |
| 11 | Tie-break | none needed |
| 12 | Maturity and censoring | every 2027 profile's complete file arrived before the as-of morning (asserted) |
| 13 | Order of operations | profiles, good layer values, potential temperature, reference water at the value's temperature and the profile's position, differences, profile means, float means, tolerance |
| 14 | Row order | no step depends on file order |
| 15 | Duplicate resolution | profile files by version (SF3); the RHD copies of the institute's casts change no offset by more than 0.001 (asserted) |
| 16 | Identity normalisation | WMO numbers and cycles join exactly across the profile, technical and receipt files |
| 17 | Netting against gross | not applicable |
| 18 | Dimensional units | practical salinity; pressure in dbar, RHD depth in metres taken to pressure; IPTS-68 taken to ITS-90 |
| 19 | Code and status semantics | flags 1 and 2 good (SF2); file_version 2 the complete file; direction A ascending |
| 20 | Integerisation | none for the offsets; the asks' counts are whole casts and profiles |
| 21 | Clause scope | the thread's tolerance and layer apply to every float of the array |
| 22 | Forward window contents | the release covers 2027's closed record; nothing is forecast |

## Literal reader

Executing the prompt and the release thread word for word: the 24 floats are the register's, their 2027 ascending
profiles the profile index's, one file per profile (the one carrying every level), and each float's offset is the
salinity it reported less the true salinity of the water it sampled, the mean over each profile's good values (flags 1
or 2) between 1,400 and 1,900 dbar, averaged over its profiles; more than 0.010 in magnitude is adjusted. The literal
estimand is the true salinity of the water sampled, which the reference casts give on the water's own identity (its
potential temperature) at its place; that reading files the six under every position-mapped implementation, and the
easy answer, 14, comes from an easy method on the same literal estimand (the casts' salinity at the same pressure),
never from another reading: every row of the fork table files the six.

## Oracles

None for the call: no earlier offset, calibration result or adjusted file ships; the recovered-sensor checks (a
distractor) are other floats' laboratory results and tie to nothing in the array; the oxygen profiles (a distractor)
carry no salinity. For the asks, the archive's own station list is the referee for which RHD stations are the
institute's casts, and the technical file's end of ascent for surfacing; neither ties to any count by itself.

## Ask sheet

**Ask A, reference casts reaching 2,000 dbar by year, 2015 to 2025** (11 counts). H18: the reference coverage the
release report carries beside the offsets, an audit trail of the reference the offsets rest on; the call does not
count casts. Use: the data management lead reports how much deep reference water each year supplies. Primary device D1
(the same records under two key schemes or sources: 119 of the RHD extract's 190 stations are the institute's own
casts as the institute submitted them, under RHD ids, positions to 0.01 degree, times as decimal hours shifted by up to
three minutes, depth not pressure; nothing marks them, and the archive does not name its ship); hazards: the RHD's depth
in metres (23 stations end between 1,981 and 1,999 m, past 2,000 dbar under any conversion, short of 2,000 m), stations
worked twice a few hours apart (24 repeat casts: two casts, which a same-day, same-position dedup collapses), casts
stopping where the plan or the bottom stopped them. Path: the archive's station and level files, the RHD's station and
level files, the reference note, the thread, the dictionary (6 files, 13 columns: cast_id, cruise, station, time_utc,
latitude, longitude, max_pres, station_id, date, time, lat, lon, max_depth_m). Stops: every row counted with depth as
pressure +5 to +13 a year; every row counted with depth taken to pressure +7 to +14; copies matched but depth read as
pressure -1 to -3 in ten years; same day and position collapsed -1 to -3 in eight years. Realism: a national archive
submits its cruises to the international database every year, and the database serves them under its own ids and
conventions; a station worked twice is two casts.

**Ask B, the array's ascending profiles that reached the data centre in full within 24 hours of the float surfacing,
by month of 2027** (12 counts). H18: the delivery record the assembly centre asks for, in the release report beside
the offsets; the call does not read delivery times. Use: the assembly centre's real-time delivery target. Primary
device D8 (an anchor on the wrong event: the model K floats' firmware stamps juld at the start of the ascent, about six
hours before the float surfaces, while model A stamps it at the surface; surfacing is the end of the ascent in the
cycle technical file; nothing in the profile index says which); hazards: the receipt log on the server's Lisbon clock
(summer time from 28 March to 31 October), profiles whose first file broke off and came again (the complete file
counts; an Iridium float sends it with its next profile), descending profiles sent with the next ascending one, the
partner float. Path: the register, the profile index, the technical file, the receipt log, the thread, the float
models summary, the dictionary (7 files, 11 columns: wmo, model, cycle, direction, juld, file_version, ascent_end,
received, n_levels, file_name, profiles). Stops: juld as surfacing -6 to -13 in every month; the first file +2 to +5 in
eleven months; the Lisbon clock read as UTC -1 to -2 in eight months; the partner float +2 to +3 in every month;
descending profiles +9 to +13 in every month. Realism: firmware time-stamps differ between float models, and a server
logs local time.

Main population zero-counts: the call's rows are the array's 2027 ascending profiles and their good layer values; no
receipt-log row, technical row, partner profile or descending profile is among them (asserted), and the call reads the
reference data, where the RHD copies move no offset by more than 0.001 (asserted); every Layer 1 slip keeps the six
(R2 in `checks.py`).

| Hazard | Asks moved | Per-ask deltas (largest) |
|---|---|---|
| the RHD copies of the institute's casts (D1) | A | +14 (2015) |
| the RHD depth in metres (D3) | A | -3 (2017, 2018, 2019, 2024, 2025) |
| stations worked twice (D1, over-cleaning) | A | -3 (2015, 2024) |
| juld at the start of the ascent (D8) | B | -13 (December) |
| the Lisbon clock (D8) | B | -2 (March, June, August) |
| the first file of a resent profile (D2) | B | +5 (September) |
| the partner float (D5) | B | +3 |
| descending profiles (D5) | B | +13 (January, May) |

Referee: the archive's station list for the copies; the technical file's ascent_end for surfacing.

| Ask row | The cracker (landed the call, hygiene battery, every filed rule executed) | Verdict |
|---|---|---|
| Ask A, 2015 to 2019 | no exact duplicate or repeated key in either source; the RHD copies counted again | miss |
| Ask A, 2020 to 2025 | the same | miss |
| Ask B, January to June | the delivery record executed as filed (complete file, the array, the Lisbon clock), juld as surfacing | miss |
| Ask B, July to December | the same | miss |

Measured by: generator/pair.py on the cut pack: the cracker keeps 0 of the 23 ask figures, Lc 0; the mirror (stopped
at the fixed-pressure comparison) keeps 0 of 23 whether careful or careless on the asks, Ls 0, and about 8 of the
recommendation weight from the critical components it shares.

Pair ceiling: 30.0 ((38 + 7 + 55 x 0) and (8 + 7 + 55 x 0), averaged)

Mirror leakage: 0.0 per cent of ask weight

## Pre-ship check

1. Domain: the call stands on each float's conductivity-sensor offset read the way delayed-mode quality control of
   profiling floats reads it, the float's salinity against ship reference water of the same potential temperature at
   the float's position; with ward thermometers or warehouse scanners in place of floats there is no water column that
   heaves, no water mass whose temperature fixes its salinity and no basin gradient, and the task stops making sense.
2. Two layers: Layer 1 (profiles at two grains, real-time flags on all three variables, files received twice, descending
   profiles and a partner float, model K's profile time at the start of the ascent, an archive in IPTS-68 for two
   cruises, an extract in metres that holds the institute's casts again under its own ids, stations worked twice, a
   receipt log on the server's Lisbon clock) is neutral on the call: every slip in R2 keeps the six. Layer 2 is the
   comparison on potential-temperature levels against reference water at the profile's position, asserted alone to
   move the default path to the golden on the simulator's clean truth (R3b).
3. No banned stump decides: nothing is planted (no earlier offset, calibration result or draft list ships); not
   semantics (the default path reads every field and unit right and files 14, 15 on the clean truth, R3a); not rule
   application (the thread files the estimand, the layer, the flags and the tolerance and names no comparison, asserted
   on its text).
4. Gate G: no shipped artifact ranks the floats; the recovered-sensor checks are other floats' laboratory results and the
   oxygen file carries no salinity.
5. Determinism: the six hold under every position-mapped implementation checked (nearest 5 to 100 casts, radii of 1 to
   5 degrees, Gaussian scales of 2 to 4 degrees, either source, in-situ temperature); the adjusted floats read 0.020 or
   more and the others 0.003 or less; offsets are graded within 0.003, the spread of those implementations; the asks'
   counts are integers with no RHD cast between 1,962 and 1,981 m and no delivery within 30 seconds of the 24 hour
   line; the 12 fork rows are asserted in `checks.py` and the verifier recomputes every figure by its own route.
6. Fingerprint: heart WARN (repeat.gate_g, repeat.deliverables, repeat.question_form, answered under Draw); the
   question opens as whether-and-which since four of the lane's last six prompts open "Which"; surface promotes task148
   (gap, pattern and decision family collide, surface 0.079), differentiated on the card; personas clean.
7. Judge (one isolated thread at a time, Sonnet, medium, the bundle and the graded blocks only). Pass 1: DETERMINISTIC,
   FIX_NOW on the write-up alone (carry the 0.003 acceptance into the grading; quote the easy routes as measured
   ranges, its own runs giving 14 and 12; name the fit's theta range), all three taken. Pass 2: DETERMINISTIC,
   APPROVE: the six, every offset within 0.001 bar 1990005 (-0.026 against -0.027, inside the 0.003), both tables
   exactly; fixed pressure 15, pooled 11, drift 4; Gate G method_or_model_selection, analytical_non_defect; Gate H
   domain, layers and decisive step pass.

## Leak check

`leak.py --asof 2028-01-07`: REVIEW, no LEAK. The REVIEW lines: data and document vocabulary shared with the stump
paragraph (temperature, position, pressure, levels: the field's own words in a data dictionary and a reference note,
none naming the comparison, asserted); Argo-style column names (temp, temp_qc, temp_scale). The float WMO numbers and
the extract's stated precision are listed as stated inputs.

Solver's-eye reads (two isolated reads, Sonnet, medium, the prompt and the bundle only; the second after the fix pass):
- Question 1: none, both times: the thread files what the offset is and not how to know the water's true salinity;
  both reads listed choosing the matching (pressure, nearest casts, temperature) as theirs to make.
- Questions 2 to 4: none, both times.
- Question 5: the thread's estimand, flags, layer, averaging and tolerance, each executing to the golden's population
  and quantity.
- Question 6: an analytical choice, both times (how the reference water of the sampled water is estimated).
- Realism, fixed: RHD casts ending at 1,980 m (a rule-of-thumb conversion would have read them short of 2,000 dbar);
  three deepest values across the archive; one 10 m grid for every RHD institute; resends exactly ten days later; no
  temperature or pressure flag; the year's first descent exactly ten days before the next; no battery ageing; cruises
  starting on the hour; one section on an exact latitude step; two receipts in the repeated October hour read a pass
  early by the estimator. Kept: the overlap of the two reference sources (the first ask's device, how the database
  serves submitted cruises), juld by model (the second ask's device), sequential WMO numbers (one programme's block),
  cruise codes by the institute's running number, "as last year" in the thread.

## Tried and rejected

- The seed's pitfall (one raking pass against raking to convergence): executing a filed procedure, rule application;
  dropped at the draw.
- The seed's survey world: the pairing is banned against task240; dropped at the draw.
- A surveillance completeness check by capture-recapture with dependent sources (epidemiology): task236 already reads
  a capture rate against an independent sample; too close; dropped at the draw.
- A laboratory calibration curve's weighting (weighted against unweighted least squares): either the weighting is
  filed (rule application) or two least-squares readings stay open (a fork); dropped at the draw.
- A westward gradient of 0.0042 per degree at 6.8 degrees: the pooled-reference rung sat within 0.0002 of the
  tolerance on two floats and could collapse onto the golden; raised to 0.0060.
- Floats free to reach the box's edges, casts only inside it: nearest-cast mappings for edge floats were one-sided and
  the corridor ended at a 4 degree radius; floats now turn back inside the recirculation and the casts extend past
  them, so the corridor reaches 5 degrees.
- A pressure-level default on 50 dbar standard levels with profiles dropped unless they spanned the layer: a third of
  the profiles fell out on the levels' jitter; the default now differences each good value at its own pressure.
- Three partner floats: their on-time profiles cancelled the profile-time anchor in three months for a solver making
  both mistakes; one partner float, and the Argos latency drawn from 8 to 26 hours.
- A drifting sensor free to start drifting late in 2027: one drifting float's 2027 mean fell under the tolerance;
  drift now starts between July and November 2026 in a float in the water for a year or more.
- RHD casts ending at 1,980 m: 2,005 dbar by Saunders (1981) but 1,999.8 by the 1.01 rule of thumb, so the conversion
  chose the count (leak reader); the extract's deepest levels now sit clear of 1,962 to 1,981 m and the reference note
  names the database's conversion.
- One 10 m grid for every RHD institute and three deepest values across the archive read as generated (leak reader);
  each institute now submits on its own grid, and archive casts stop where the plan or the bottom stopped them.
- Resent Iridium files exactly ten days after the first, the year's first descent exactly ten days before the next,
  engineering values with no ageing, and no temperature or pressure value ever flagged (leak reader): the resend now
  comes with the float's next profile, the battery ages, and spikes are flagged in all three variables.
- The fixed-pressure and pooled-reference rungs quoted as single counts (15 and 13): the judge measured 14 and 12 with
  its own implementations (finding 2); the write-up now quotes the measured ranges over each family (13 to 17, 10 to
  14), asserted in `checks.py`.
- A second read found the institute's cruises all starting on the hour and one section on an exact latitude step; both
  now come from a separate random stream (station keeping and the first station's time), so nothing else moved, and
  the estimator reads a receipt in the repeated October hour in the pass that keeps it after its own surfacing (the
  counts were the same either way).

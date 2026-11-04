# task210 design note

Architecture 1, drawn 2026-11-04. Wave 8 of the sathay3012 backlog, Anomaly Detection and Diagnostics, seed AD33.

## Draw

**Why the world moved.** Seed AD33 is a data-centre battery's January FCR-D offer. Its only legal home on this
objective is `energy-systems-utilities/grid-reliability-outage-analysis` (the one energy task type that serves
Anomaly Detection), and task402 holds that domain and subdomain inside the live window: a probe card returned
`BLOCK ban.subdomain` against task402. No other client domain hosts a frequency-reserve task honestly (General
Statistics would be a relabel), so the draw moved to another client domain, world and dataset under the same
objective and number (CLAUDE.md, A stuck build is unblocked). What the seed's decision did is kept: one figure
committed by 10 December for January, a cap the per-unit consumption divides into, and a per-unit consumption
that concentrates in a handful of moments the averages hide.

**Card.** `cards/task210.json`. Pairing `physical-environmental-sciences` / `environmental-monitoring-exceedance`
(serves AD and DQ; tagged AD). Shape 04 (setting one dial: the predicted haulage level at every fleet size).
Decision `dial_setting`, unit count (articulated dump trucks). Gap objective then population; pattern none;
generators G14 (conditioned yield), G3 (record against operation), G13 (horizon); Gate G
`decomposition_attribution`; strategy `decomposition_attribution`; calibration `pilot_log`; context artifact
`filed_standard`; role `operations_director` (the quarry manager); forum `regulator_or_inspector` (the mineral
planning authority receives the working scheme); forcing event `statutory_or_regulatory_filing` (the January
working scheme, due 10 December under the planning permission); org family `manufacturer` (an aggregates
producer). People from `guard.py names --geo England --seed 210`: Harriet Kirk, Maurice Russell, Hollie Brown.

**The world.** Calderwick Stone works Ravensby Quarry, a limestone quarry in the north of England whose
processing plant and haul roads sit about 450 m south-west of the village of Ulverthorpe. A Class 1 sound level
meter at monitoring location MP1 (Ulverthorpe Lane, free field, 1.5 m) has logged 15-minute levels since April
2026 under the planning permission's noise condition. Five to seven of the haulage contractor's articulated dump
trucks (ADTs; the contractor can field up to twelve) haul from whichever face is worked that day: the south and west faces by the in-pit ramp, screened from the village by the
pit face; the north face by the north crest road, which runs along the original ground in line of sight of MP1;
the west crest road runs behind the west screening bund. In January the first bench of the eastern extension
opens, and its haul road runs along the extension's crest, in view of MP1, at the north crest road's distance.
The January working scheme must state how many ADTs haul from the extension; the noise management plan holds
haulage to its share of the 45 dB LAeq,1h limit at MP1.

**The decision.** How many ADTs can haul from the eastern extension in January (a whole number, the scheme's
cycle of loaded movements per ADT per hour converting a movement rate into trucks).

**The quantity.** The sound exposure one haul movement on the extension road delivers at MP1 (one loaded trip
to the plant and its empty return), which the haulage share divides into.

**The anomaly and its diagnosis.** MP1's loudest hours of May to October, and the complaints logged on them,
fall on a handful of days whose haul counts are ordinary. What drives them is the route: on those days the trucks
loaded at the north face and ran the north crest road in view of the village; on every other day the same
movements ran screened in the pit or behind the bund. No ticket records the face or the route; only each truck's
GPS track read against the site survey shows it. The January road runs in view, so its per-movement exposure is
the in-view movements' one.

**Data-native sentence.** Which face the trucks load at changes day to day with the quarry's blasting and
stocking, and that alone decides whether a haul movement passes in view of Ulverthorpe or behind the pit face,
so the monitoring record is mostly screened movements and the loud days are a minority no record labels.

**Abstraction sentence (written to be tested, not to be shipped).** The per-unit effect at a receptor depends
on a configuration state no file records, the forward plan runs wholly in one state while the record is mostly
the other, and the effect has to be estimated on the record's units in the forward state, identified from their
own position tracks against a survey of the ground. Against the approved builds: task182 (each bore's own lagged
response to a shared driver), task196 (two capture channels, one produced by the firm's own follow-up), task120
(a day's use as production less storage gain) and task187-style matched comparisons (turbulence is a recorded
ten-minute statistic there) are not this sentence. It is not writable against any approved build on file.

**Semantic screen against the nearest drivers** (`guard.py mechanisms --objective anomaly-detection`, one line
each on the insight it spends, then whether this decisive step is it in other nouns):
- task125: events from a steady part plus scheduled occasions that the coming schedule moves to another site. Not
  this: nothing here is scheduled or moved; the January road's state is read from geometry, not a calendar.
- task156 (forecasting): a response that scales with a fluctuating level read from a separate record. Not this:
  there is no exogenous level; the state is each movement's own route, read from its own track.
- task181: a shared upstream resource added risk to the cases it handled. Not this: no shared resource and no
  stretch of time; every movement is classified on its own.
- task182 v1: each unit's own lagged response to a shared driver. Not this: no driver series and no lag.
- task182 v3: one continuously running source's share of a measured total, with the nuisance measured outside the
  window. Not this: the sources are discrete movements, the nuisance (residual and plant) is measured inside it.
- task184 v8: inverting a saturating observation map per record. Not this: energy adds linearly; nothing saturates.
- task185: a conversion between two instruments sized at the value converted. Not this: one instrument throughout.
- task187: a shortfall read at matched spread of inputs. Nearest in spirit (condition on a state before reading a
  per-unit effect); the difference is that task187's state (turbulence) is a recorded ten-minute statistic and a
  matched comparison of units, while here the state has no column and is built per movement from a second file.
- task192 v1: distinct processes behind overlapping bursts. Not this: no repetition structure is used.
- task197: a unit's response measured over seconds while its output follows a scheduled trajectory. Not this:
  no response gain, no trajectory.
- task204: a transport rate from an unsteady balance across short windows. Not this: no balance or response time.
- task139 (forecasting): events accrue on the scale wear runs on. Not this: no accumulated use.
- task400 (root cause, in the window): a mine's collision warnings after a firmware change. Shares the setting's
  nouns (haul trucks, ramps) and nothing else; the pack's vocabulary is a small English quarry's, not a mine's.
- task182 arch 2 (archived): ranking noise monitoring positions by specific level after background subtraction.
  Shares the genre; its decisive step (the statistical background) is not used here, where the residual is netted
  as an ordinary covariate and the decision is a fleet size.
The decisive step is none of these in other nouns.

**WARN answers.** `repeat.gate_g` and `overuse.gate_g` (decomposition_attribution in 6 of the last 12): the label
is the honest one, since the decisive step apportions MP1's sound energy among movements by route state;
`method_or_model_selection` collides with task483 inside the batch (`test.same_driver`), so the label stays and
the strategy differs from all three window builds. `test.same_driver_older` against task122 v4 and
`test.same_puzzle_older` against task488 carry differentiation lines on the card.

**Slot screen before any harness.** `guard.py slots` on the setting nouns (quarry noise, decibel, sound power,
minerals planning, screening bund, map matching, dump truck, declared sound) returned nothing in this sense; haul
road returned task400 (setting only, above) and noise monitor returned task182 arch 2 (above). On the seed's own
setting nouns, deterministic frequency returned task197 and hour boundary returned task111, task117 and task119.

**The five go/no-go screens** (prototype on the clean truth, `screens_quarry.py`, 20 redraws, seeds 1 to 20;
every figure is ADTs, the call):
1. *Realistic levels and the lever against the rivals' estimates.* The golden (the in-view movements' exposure
   apportioned by route) separates from every rival estimate in 20 of 20 redraws: the BS 5228 prediction from
   the declared sound power by +2 to +4 ADTs, the BS 5228 prediction calibrated to the pooled record with every
   movement taken in the pit by -2 to -4, the first look by +4 to +7, the crest movements pooled by elevation by
   +5 to +18, every pooled energy calibration by +54 or more. Levels follow the sources below; the pack is about
   12 MB at one fix per truck-minute.
2. *The golden's own method holds the call.* Five specifications (15-minute energy split by route; with wind;
   hourly; day-level face classification; BS 5228 calibrated per route) land the same ADTs in 13 of 20 redraws
   and in all 10 redraws whose estimates sit mid-bin; the shipped seed is chosen among those, every variant
   between 0.15 and 0.85 of a bin.
3. *The first look lands wrong.* Tabulating MP1 beside every driver's dated record (haul tickets, wind, village
   traffic, plant hours, blasts), the busiest hour inside the limit allocates 10 or 11 ADTs: wrong in 20 of 20.
4. *The careful reader lands wrong.* Decomposing by every recorded field and netting wind, traffic, plant,
   weekday, month and hour, then projecting: pooled energy calibration (+54 or more), the same with calendar
   dummies (+54 or more), a decibel regression on log movements (no finite fleet), crest days pooled by the
   trucks' elevation (+5 to +18), BS 5228 declared (+2 to +4), BS 5228 calibrated to the pooled record (-2 to
   -4): every route wrong in 20 of 20, none reaching the golden.
5. *Literal execution.* The filed WHAT (below) executed with every natural operationalisation of "the haulage's
   specific level at MP1 at the scheme's rate": the standard method from declared sound power (+2 to +4), the
   pooled record's exposure per movement (+54 or more), the pilot's busiest compliant hour (+4 to +7). All wrong;
   the golden needs a step no filed sentence asks for: which pilot movements carry the extension road's state.

**The filed WHAT, written before the screens** (the organisation's own voice; no method):
- Planning permission condition 17: except for temporary operations under condition 18, the specific sound level
  from operations at the site shall not exceed 45 dB LAeq,1h (free field) at MP1 between 07:00 and 19:00, Monday
  to Friday.
- Noise management plan 5.2: of the 45 dB at MP1, 37.5 dB LAeq,1h is the processing plant's (the plant-only
  survey of March 2026); haulage on the site's roads is held to 44.0 dB LAeq,1h at MP1.
- Noise management plan 4.1: MP1 logs LAeq, LA90 and LAmax over 15-minute periods, free field, at 1.5 m; the
  specific sound level of an activity is the level at MP1 attributable to that activity over the reference
  period.
- Noise management plan 6.1: each working scheme states the ADTs allocated to the scheme's haul road, and is set so
  that the haulage's specific level at MP1 at the scheme's haul rate is within its share; a haul movement is one
  loaded trip from the face to the plant and the truck's empty return.
- January working scheme (draft): the extension haul road's alignment and levels; each ADT completes 3.6 loaded
  movements an hour on the extension road; haulage 07:00 to 17:00, Monday to Friday; ADTs allocated left blank.

**Sources for the levels** (each rate the generator uses sits inside these):
- Declared sound power of 35 to 45 tonne ADTs under Directive 2000/14/EC: manufacturers' declarations of about
  107 to 110 dB LWA; BS 5228-1:2009+A1:2014 Annex C gives articulated dump trucks at about 107 to 111 dB LWA.
- Operating level above the declared one when climbing loaded: BS 5228-1 Annex C notes that measured levels vary
  with operating mode; the generator sets the loaded-uphill excess at 2.6 to 3.6 dB.
- Noise limits at quiet rural properties: Planning Practice Guidance, Minerals, paragraph 021 (55 dB(A) LAeq,1h
  free field ceiling, background plus 10 dB where that is lower), so 45 dB at a quiet village edge is ordinary.
- Screening: BS 5228-1 Annex F (10 dB for a source completely screened); ISO 9613-2:1996 barrier attenuation;
  the generator uses 11.5 to 13 dB for the pit face and 8 to 9.5 dB for the bund.
- Ground and air: ISO 9613-2 ground attenuation of about 3 to 4 dB over soft ground at 450 m; ISO 9613-1 air
  absorption near 2 dB/km at mid frequencies.
- Cycle: 3 to 4 loaded movements an hour per ADT on a 1 to 1.5 km haul (operator practice).
- Instrument: Class 1 sound level meter to BS EN 61672-1, free field measurement to BS 7445-1.

## Tried and rejected

- 2026-11-04, seed AD33's world itself (a data-centre battery's January FCR-D offer): undrawable on this objective
  while task402 holds energy-systems-utilities/grid-reliability-outage-analysis in the window (`ban.subdomain`); its
  mechanism also sat near task197 (a unit's frequency response during scheduled ramps) and task125 (occasions a
  forward schedule moves).
- 2026-11-04, a nuclear site's fence-line gamma monitors at go-live, the alarm level set against rain-induced
  radon-progeny washout (prototype `proto_gamma.py`, `screens_gamma.py`, seeds 1 to 5, two climates): the golden
  needs a fitted dynamic washout model with call-out merging; event regressions with an antecedent dry-time term
  land 6 to 12 nSv/h off it and the first look sometimes lands near it, so screens 1 and 2 fail.
- 2026-11-04, occupational blood lead at a secondary lead smelter (January furnace shifts under the action level):
  its decisive state is a shared upstream resource (task181) or each unit's lagged response (task182), and a
  monthly AR(1) careful route sits close to the kinetic golden.
- 2026-11-04, a data centre's UPS battery strings on thermal age and a device fleet failing on uptime since the last
  reset: both are task139's wear-clock insight and task132's renewal, in other nouns.
- 2026-11-04, hydropeaking under a filed rating curve (downstream stage ramps at winter base flow): task156's
  response scaled by a level read from a separate record.
- 2026-11-04, darkness-relative crime hours, susceptible depletion, backlog draining, road salt, build-up and
  wash-off, immortal time, an extremal index and tide aliasing: each already screened dead in another slot's note
  (`guard.py slots`: task182 arch 8, task178 and task202, task174, task165, task121, task122, task178 and task194,
  task249).

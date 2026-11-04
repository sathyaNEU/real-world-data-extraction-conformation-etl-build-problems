# task210 design note

Architecture 1, drawn 2026-11-04. Whether any of Wendle Water's sewage pumping station storm overflows
discharged in 2026 before its station was passing forward the flow its permit sets, and if so which one the
company self-reports to the Environment Agency with its 2026 event duration monitoring return. The number is
fixed in Anomaly Detection & Diagnostics by `START_HERE.md`; its seed (AD33, a data-centre battery's January
FCR-D offer) supplied the objective only, for the reasons in `## Tried and rejected`.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task210.json`, architecture v1, registered 2026-11-04 |
| Client domain / task type | Physical & Environmental Sciences (`physical-environmental-sciences`), `environmental-monitoring-exceedance` (serves AD and DQ): whether a permitted discharge operated outside its permit's conditions, read from the discharge's own monitoring, is the field's exceedance determination |
| Objective | Anomaly Detection & Diagnostics: a real breach (an overflow that spilled before its station reached its permitted pass forward flow) separated from artifacts that look like breaches (dry-day spills at a station whose sewer fills with groundwater, the most frequent spiller, whose permit sets a small pass forward flow) and from a station that looks compliant because its pump runs |
| Decision | whether any pumping station storm overflow discharged in breach of its permit's pass forward condition in 2026, and if so which one is self-reported (`pick_one_of_n` with none licensed). Retrospective by necessity: a permit self-report concerns discharges that have happened; the forward action is the report itself, filed with the 2026 return, and the station's repair before more spills |
| Shape | 10, a scorecard: every station's overflow against its permit's pass forward flow, with each station's delivered pass forward flow, its 2026 spills and its dry-day spills, the call, the chart's named parts and the return's per-overflow figures |
| Gap / pattern / generators | `population` (the file is not the thing: the register's rated duty is not what the running pump delivers); pattern `none`; `G3` record against operation decisive (the telemetry and register say a pump of a given duty is running, the operation is a part-blocked rising main passing forward three fifths of it), `G7` (when a spill is lawful: only once the station is at its permitted capacity) |
| Gate G | `binding_constraint`: the permit's capacity condition decides which spills are lawful, and whether the station had reached it is the whole question |
| Strategy | `binding_constraint`; Layer 2 family `field_method` (the field's own capacity test done on the capacity the station delivers); pattern `own:delivered-pump-rate-from-wet-well-fill-and-draw-against-rated-duty` |
| Forum, forcing event, org family | `regulator_or_inspector` (the self-report goes to the Environment Agency with the return), `statutory_or_regulatory_filing` (the 2026 event duration monitoring annual return, due 31 March 2027), `utility_or_infrastructure` (a water and sewerage company) |
| Role | the company's wastewater environmental compliance manager, who signs the return and the self-report (`compliance_or_audit`) |
| Context artifact | `register`: the wastewater asset register (station, wet well, pump and setpoint records) and the consents register |
| Calibration | none |
| Personas | Harriet Kirk, Maurice Russell (`guard.py names --geo "England" --seed 210`; Amy Howarth from the same draw was dropped on `people.first` against task130) |
| Fiction as-of date | 2027-01-15 (the compliance team's export for the return; every record ends 31 December 2026) |
| Guard | `guard.py check` on the draft: WARN `overuse.objective` (the number fixes the objective), WARN `repeat.geography` against task313 (England is where the pass forward permit condition and the event duration monitoring return exist as written; the world, a water and sewerage company, shares nothing else with task313's integrated care board). Redrawn before registration: the generators (G8 first repeated task398 and task276's lineage on the structural tests, and G8 was the wrong key: the pass forward condition is attained or not, read from what the pump did against what the register says, which is G3); the question form from which to whether (which is 36 per cent of prompts on file, over the 30 per cent quota; the decision is first a gate, whether any overflow breached, then a pick); the deliverable set from docx+png+xlsx (task398's) to csv+docx+svg; a persona. `test.same_puzzle_older` and `test.same_driver_older` stand as NOTEs, answered by differentiation lines on the card (task121, task310, task464, and task192's screen A4.5) |

**Why the world moved.** AD33's battery sits in energy-systems-utilities, whose only anomaly-detection task
type is grid-reliability-outage-analysis, the most crowded anomaly-detection cell on file (six cards, two of
them in the last twelve builds); and the seed's mechanism, activations bunched at a handful of hour boundaries
where deterministic frequency deviations fall, is task197's confounder (a unit's response read through the
settlement-period boundaries). The decision and quantity cannot leave that cell, so the number moved to
another client domain under the same objective.

**Data-native sentence.** A small sewage pumping station has no flow meter, so the flow it passes forward is
read everywhere as the duty of the pump its telemetry shows running; Gallowfen's rising main is part-blocked,
so each of its pumps runs at its full control state and moves only about three fifths of its duty, which no
field records and which shows only in how long its wet well takes to draw down between the duty pump's stop
and start levels against how long it takes to fill.

**Abstraction sentence (written to be refused).** "A permit lets a unit release only once it is working at a
set capacity; the record of what the unit is doing is its running state and its rated output, a unit
throttled downstream of its rating keeps its running state while delivering less, and only a volume balance
on the unit's own storage between its control levels, timed from its own starts and stops, shows the
delivered output." No approved or delivered build carries it. task194 (shipped) nets a unit's metered inflow
against a neighbour's supply through an open boundary; task193 (shipped) conditions background wells on the
gradient at each sampling date; task187 reads turbine shortfall through the turbulence inside a ten-minute
average; task182 v1 (approved) fits each bore's lagged response to a shared driver. None measures a unit's
delivered rate from its own storage cycles against a rated value. Nearest driver on file 0.07 (task276's
lineage, a queue that drains only as fast as the next control lets it through).

**Not task192's screen A4.5.** task192's architecture 4 pass prototyped a storm overflow whose throttle
part-blocked and died on the dial: its golden (the rain before each spill's onset) was a member of the
rainfall family the easy route belongs to, so confounds that moved the easy route moved the golden with it.
Here no rainfall quantity enters the decisive step at all: the station's delivered pumping rate is read from
its own pump start and stop times and its wet well's area and control levels, and rainfall enters only the
rungs below it (dry-day spills, spill counts) and one ask.

**Sources.** Fully constructed for a fictional company and catchment in eastern England (a coastal marsh
drained by small pumping stations and a chalk wold whose sewers take groundwater in late winter): the
telemetry outstations' pump event log and fifteen-minute wet well levels, the event duration monitors' spill
records, the radar rainfall by catchment, the wastewater asset register, the consents register, the flow
meter records at the stations that have one, the company's event duration monitoring reporting procedure,
and distractors. Provenance in `metadata.json`.

## Stump sentence

A competent analyst checks each 2026 spill against its permit's pass forward flow using the rated duty of the
pump the telemetry shows running, finds every station at or above its permitted flow and self-reports no
overflow (or, screening dry-day spills, reports the groundwater-fed Wold station), because Gallowfen's
pumps, on a part-blocked rising main, keep running while delivering about three fifths of their duty, which
shows only in Gallowfen's own wet well fill and draw times between the duty pump's control levels.

## Tried and rejected

- 2026-11-04, the seed's own world (AD33: a data-centre battery's January FCR-D offer against a warranty
  throughput cap, activations at hour boundaries): grid-reliability-outage-analysis is the only
  anomaly-detection task type the battery can sit in (energy-systems-utilities), the most crowded cell on file,
  and the hour-boundary deterministic frequency deviations are task197's confounder; an offer in MW is also a
  forecasting quantity, so the call would retag. Moved.
- 2026-11-04, a hospital's duodenoscope carrying CPE from each patient to the next, polyclonal on the scope so
  the clonality test dismisses it (epidemiology-public-health / disease-surveillance): the honest org family
  (hospital_or_health_provider, task313) and strategy (causal_design: interference between consecutive users)
  are both in the current ban window, and the predecessor check is the investigator's own reflex for scope
  transmission; a carriage-reconstruction variant reduces to "predecessor ever positive", one line. Not carded.
- 2026-11-04, a vaccine or drug signal read from time to onset against how long patients stay on treatment
  (pharmacology / safety-signal-detection): the null of a temporal pattern set by the exposure's own timing is
  the family task193's architecture 2 (sequence symmetry) spent on the clean truth. Not carded.
- 2026-11-04, an estuary input read against the conservative mixing line between river and sea end-members,
  then against end-members lagged by the freshwater transit time: the mixing diagram is the estuarine
  chemist's first move (rung 0 is the golden), the lagged version is a fitted transit time from a box model no
  file carries (external dependency), and task398's lake-layer inflow mechanism had just registered in the
  same domain. Not carded.
- 2026-11-04, a thermal discharge's temperature rise read against the upstream sonde lagged by the reach's
  travel time: the lagged comparison is task182 v1's family (approved), and the lag is a fitted parameter.
  Not carded.
- 2026-11-04, airport departure noise read against each type's noise-power-distance level at its own slant
  distance: the interpolation, lateral attenuation and atmospheric conventions each move the graded residual
  by more than its bin. Not carded.
- 2026-11-04, the draft card with gap objective and generators G8, G3: BLOCK on ban.pattern (G8 against
  task398) and the structural tests against task276's lineage; G8 (reachability) was the wrong key, so the
  generators were redrawn to G3, G7 and the gap to population (the register's duty is not the thing).

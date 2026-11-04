# task210 design note

Architecture 1, drawn 2026-11-04. Whether any of Lindmarsh Water's sewage pumping station storm overflows
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
| Gap / pattern / generators | `population` (the file is not the thing: the register's rated duty is not what the running pump delivers); pattern `none`; `G3` record against operation decisive (the telemetry and register say a pump of a given duty is running, the operation is a part-blocked rising main passing forward a little over half of it), `G7` (when a spill is lawful: only once the station is at its permitted capacity) |
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
so each of its pumps runs at its full control state and moves only a little over half of its duty, which no
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
overflow (or, timing each station's drawdown without the inflow or screening dry-day spills, reports the
groundwater-fed Wold station), because Gallowfen's pumps, on a part-blocked rising main, keep running while
delivering a little over half of their duty, which shows only in Gallowfen's own wet well fill and draw times
between the duty pump's control levels, the fill timing the inflow that the drawdown alone leaves in.

## Survivor anatomy

Actor: The deciding property, the rate each station's running pump actually moves into its rising main, has no
column in any file: the register holds the pump's rated duty, the telemetry holds pump starts and stops with the
wet well level, the meters exist at three other stations, and the delivered rate is a relation between consecutive
start and stop rows of one station (the off-time that filled the wet well and the on-time that drew it down)
against the register's wet well area and control levels.

Link: The signal is read through a comparison the compliance check never asks for: the telemetry's pump cycle
timings against the asset register's wet well geometry, two systems with no shared quantity (the RTU number links
the rows, but nothing joins a cycle to a flow until the analyst builds the volume between the duty pump's stop and
start levels and divides it by the times).

Reflex: The field's desk test for a pass forward condition at an unmetered station is the duty of the pump the
telemetry shows running, cross-checked against a rising main meter where one is fitted; it sits at rung 0 and files
none, every running pump rated at 1.17 to 1.24 times its permitted flow, Gallowfen's at 85.3 against 72.

Back-test: The textbook route validates: at the three metered stations the meters read 118, 84 and 67 l/s while
their overflows spilled, within 0.4 to 2.7 per cent of the rated duties of 118.5, 86.3 and 67.1, so a solver who
checks the rated duty against the only measured flows in the pack finds it confirmed.

Second use: Every file the decisive step reads is in the pack for its own reason: the telemetry historian carries
the overflow alarms, the high level alarms, the comms failures and the kiosk door alarms the operations team works
from and is read by rung 0 to see which pump ran; the asset register's Pumping stations sheet carries the
monitor serials, the control and alarm levels, the weir and the rising main for every station; nothing ships only
for the decisive step.

Shock: Gallowfen is at neither end of any shipped statistic a solver can sort: 12 spills (tenth of fourteen), 20.4
hours, no dry-day spill, 14 high level alarms (tenth), run hours per day fourth, starts per day fifth, spills per
100 mm of rain eleventh, rated duty against permitted flow fourth of fourteen at 1.185, its permitted flow and rated
duty third largest; on the drawdown timed without the inflow (rung 0b) Hagworth Wold, not Gallowfen, is the
outlier; only the delivered rate, which no file holds, puts Gallowfen apart.

Pins: The WHAT is filed in the organisation's own genre: condition 2.3.1 of each permit in the consents register
(the flow, passed forward to the rising main, before the overflow may discharge), WW-ENV-PR-014 (the reporting
year in UK local time, the 12/24 count per overflow with a block counted when any part of a discharge falls in it,
duration with a period counted once, the operational hours of the year, one overflow per self-report); no filed
sentence says how a station's pass forward flow is
established, names a pump's delivered rate, a drawdown, a wet well volume or a meter, and deleting any one of them
leaves the call forced by the records.

## Default path

1. Read condition 2.3.1 of each of the fourteen permits in `registers/wastewater_discharge_consents_2026.csv`: the
   overflow may discharge only when its station is passing forward to the rising main a set flow, 16 to 101 l/s.
2. Read WW-ENV-PR-014: the reporting year in UK local time, the 12/24 count, a breach of a permit condition
   self-reported with the return.
3. Take each overflow's 2026 discharges from `edm/edm_discharge_log_2026.csv` on the monitor the asset register
   lists, converted from UK local time, and count them by the 12/24 method.
4. For each discharge, find the pump `pump_event` shows running and take its duty from the register's Pumps sheet,
   converting the four stations held in m3/h; at the three metered stations read the rising main meter over the
   discharge.
5. Every running pump is rated at 1.17 to 1.24 times its station's permitted flow (Gallowfen 85.3 against 72) and
   the meters read 118, 84 and 67 l/s against 101, 73 and 56 while their overflows spilled; no overflow
   breached condition 2.3.1. A solver who distrusts that and screens the discharges for an operating fault instead
   times each station's drawdown from `pump_event` and the register's levels, which files Hagworth Wold lowest by
   far (12 l/s against 31), or takes the procedure's dry-day annex and finds dry-day spills at Hagworth Wold alone
   (110 of them).

Ends on: none, no overflow self-reported (or Hagworth Wold on the dry-day screen)

Golden: Gallowfen PS storm overflow, permit EPRWW4412BK, passing forward 48 l/s against 72

## Three rules

Task type: physical-environmental-sciences, environmental-monitoring-exceedance: whether a permitted discharge
operated outside its permit's conditions, read from the discharge's own monitoring and the works' operating
records; it serves Anomaly Detection & Diagnostics, a real breach told apart from the overflows that only look like
breaches (dry-day spills fed by groundwater, the most frequent spiller).

Domain test: The quantity that decides is the flow each pumping station was passing forward to its rising main
while its storm overflow discharged, tested against the permit's pass forward condition the way a water company
and the regulator test a storm overflow permit; the field's own desk test for it at an unmetered station is the
running pump's duty, checked against a rising main meter where one is fitted, and that sits at rung 0.

Swap: Rewrite the call with a hospital's or a retailer's nouns and it stops making sense: no permit lets a ward or a
store discharge only once it is passing forward a set flow, no event duration monitor counts 12/24 spills, and no
wet well holds a fixed volume between a duty pump's stop and start levels from which a delivered rate can be timed.

Layer 1: The telemetry historian in UTC beside the monitoring platform in UK local time; outstations re-sending
their last pump events after a comms loss (exact duplicates in `pump_event`); the same comms losses dropping the
fifteen-minute level polls; duties held in l/s at ten stations and m3/h at four; control levels in mAOD in the
register against levels above the wet well floor in the telemetry; three identifiers for one station (permit and
site id, RTU number, station code); monitor outages splitting a discharge into several records; the meter
historian's quality codes (no value through a comms loss, the historian's estimate while a transmitter was faulted,
the verification window, the empty-pipe detector's suspect spells). Each is written by
the system that produces the file and none moves the call (the R2 assertions).

Layer 2: The family is `field_method`: the flow a pumped station passes forward is measured where it is not metered,
from the wet well's fixed volume between the duty pump's stop and start levels timed over each cycle (the pump-off
time fills it at the inflow, the pump-on time draws it down at the pump's rate less the inflow), and that measured
rate, not the nameplate, is what the permit's condition is tested on.

Decisive step: Timing every 2026 pump cycle at every station from the outstation's own starts and stops and
converting each into a delivered rate through the wet well's volume between the control levels: both Gallowfen
pumps run normally and move 48 l/s, 56 per cent of their 85.3 l/s duty and 67 per cent of the 72 l/s the permit
sets, while every other station delivers 1.14 to 1.26 times its permitted flow.

Not semantics: No field, code, unit or definition flips the call: the m3/h duties only scale duties that clear the
permit either way, the platform's local time and the historian's UTC both show Gallowfen discharging in 2026, the
condition's text and its pass forward column agree on every permit, and no column holds a delivered rate, a
restriction or a fault, so a solver who reads every field correctly still has the rated duty in hand.

Not rule application: No filed rule establishes the flow a station passes forward: the consents register states
the flow to reach, the procedure counts spills, defines dry days and names the self-report, and executing every one
of them gives the default path's none or Hagworth Wold. The estimator family the method leaves open (median, mean or
trimmed mean of the cycles; the off-time before each run or the mean of the two either side; all cycles or night
cycles; the register's control levels or the levels the outstation logs at each start and stop: 24 members) spreads
Gallowfen's rate over 47.88 to 48.29 l/s and any station's over 0.58 l/s at most, every member on the golden's
whole figure.

Analyst test: Yes: a strong analyst who drops the re-sent events, converts every duty and clock, reads every
condition and clause correctly and checks each spill against the duty of the pump the telemetry shows running (the
meter where fitted) files none, no overflow self-reported; timing the drawdown without the inflow, or on the dry-day
screen, it files Hagworth Wold; all are wrong, and the step that lands Gallowfen is a measurement the data support
and no sentence asks for.

Estimand: Population, the fourteen pumping station storm overflows on the consents register, every one under
event duration monitoring; outcome, whether the overflow discharged in 2026 while its station was passing forward
less than the flow condition 2.3.1 of its permit sets; window, the 2026 reporting year in UK local time; unit,
litres per second, whole; comparison, each station's flow passed forward against its own permit's condition. The
prompt carries the population, outcome and comparison; the consents register files the flows; WW-ENV-PR-014 files
the reporting year.

No decoy: Nothing is planted to be caught: no memo, draft, briefing or prior review ranks the stations or argues
for none; the register's rated duty is the true datasheet duty, the meters are correct at the stations they
measure, Hagworth Wold's dry-day spills are real groundwater-fed discharges the annex rightly lists, and no block
of records is copied, backfilled or altered (R3c).

No certified replay: The method is not recovered by reproducing a certified or published figure: no file states
any station's pass forward flow for 2026, the meter verification work orders verify three meters at three other
stations, and the pump service work orders record servicing, not a performance test.

Lesson: A model that gets it right learns to test a capacity condition on the capacity the unit delivers, measured
from the unit's own storage cycles, rather than on its rating when the rating has been confirmed everywhere it could
be checked; no build on file teaches it (the nearest drivers are a queue drained at the next control's rate at 0.07
and a unit's metered inflow netted against a neighbour's supply), and task192's storm overflow screen read rain
before onset, which this build keeps out of the decisive step.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0 rated duty of the running pump (meter where fitted): none | the register's duty column | `Duty flow` | the field's desk test | the three meters confirm it | none | duty against the permit, one comparison | no | readable |
| 0b drawdown from the pump-on time alone (no inflow): Hagworth Wold lowest, three short | no sentence names it | `pump_event` and the register's levels | the drawdown test as it is done on site, read off the telemetry | the three meters refute it | none | a volume over one time | no | readable |
| 1 dry-day screen: Hagworth Wold | section 6 of the procedure defines it | rain by radar zone | a screen for operating faults | none | none | a filter | no | readable |
| 2 most 12/24 spills: Marram End | section 3 counts them | none | the frequent-spiller reflex | none | none | a sort | no | readable |
| 3 (decisive) delivered rate from each station's wet well cycles: Gallowfen | no sentence names a delivered rate, a cycle or a volume | no column holds a rate; the step joins cycle timings to wet well geometry | rung 0's duty is the reflex and it files none | the meters agree with the duty and with the cycles at their own stations, so they rank nothing | dropping the re-sent events and converting units leaves the duty in place | a volume over two times per cycle, then a median over thousands of cycles per station | the telemetry and the register carry alarms, serials and levels for their own uses | silent |

## Ladder

| Rung | Route (in `generator/routes.py`) | Files | Refused by |
|---|---|---|---|
| 0 | `rated_check` (`R1` in the code): the running pump's duty, the meter at the three metered stations | none: duties 1.17 to 1.24 times the permits, meters 117.8, 83.8, 66.6 against 101, 73, 56 | the cycles: Gallowfen's pumps move 48 l/s, not 85.3 |
| 0b | `naive_drawdown`: the volume between the duty pump's control levels over the pump-on time alone; the median of every run, of the runs starting between midnight and 05:00, or the 90th percentile | Hagworth Wold, far the lowest: 12.2 l/s against 31 (0.39 of its permit; 0.44 on the midnight-to-05:00 runs, 0.48 at the 90th percentile), then Gallowfen 39.5 against 72 (0.55; 0.59, 0.59) and Marram End 15.0 against 16 (0.94 on the median of every run); the other eleven clear their permits at 1.02 to 1.10 | Hagworth Wold's groundwater runs into the well through every cycle (its fill-and-draw rate is 36 l/s against 31); the meters read 9 to 14 per cent above the pump-on route at their own stations; adding back the inflow timed from the fill before each run gives the golden |
| 1 | `dry_day_spills` (`R0`): the procedure's dry-day annex | Hagworth Wold, 110 dry-day spills, every other overflow none | the station was pumping 36 l/s against a permitted 31 through them: groundwater, not a pass forward failure |
| 2 | the high spiller (`R2`): the most 12/24 spills and hours | Marram End, 57 spills and 198.2 hours | Marram End delivers 19 l/s against 16 |
| 3 (decisive) | `delivered` in `generator/golden.py`: each station's median cycle rate against its permit | Gallowfen, 48 l/s against 72 (0.666 of the permit); the next lowest Sallowholme 57 against 50 (1.139) | |

Why rung 0b is the measurement a strong solver reaches for first: the drawdown test is how a station's pumping
rate is checked on site, where the crew stops the inflow or reads it as negligible and times the well down between
two levels, so a solver who distrusts the nameplate and turns to `pump_event` and the register's levels times the
pump-on spells and divides the volume by them. On this network the route is credible: eleven stations clear their
permits on it, and the three it flags include the station with the slowest drawdowns by far, Hagworth Wold, whose
chalk groundwater runs into the sewer all year and into its wet well through every cycle (the observation borehole
and its dry-day spills say why). A solver who keeps the route and names its outlier self-reports Hagworth Wold, the
dry-day screen's answer too; one who reports every station it flags names three overflows. What refutes it is the
fill before each run: timing it gives the inflow the drawdown leaves in, and adding it back puts Hagworth Wold at 36
l/s against 31 and Gallowfen alone below its permit. The meters, 9 to 14 per cent above the pump-on route at their
own stations, are the other way out (asserted in `checks.py`, `rung0b.` labels, on every build).

Separation: Gallowfen sits fourth of fourteen on rung 0's headroom (rated duty over permitted flow 1.185, against
1.173 to 1.235), is second to Hagworth Wold on rung 0b by 0.16 of a permit (0.15 on the runs starting between
midnight and 05:00, 0.10 at the 90th percentile), has no dry-day spill on rung 1 and is tenth on rung 2's spill count; the final margin is 1.139
against 0.666, a factor of 1.71. The reflex routes priced in `routes.py` (run hours, starts per day, run per start,
hours per spill, rain before onset, spills per 100 mm, high level alarms and their hours and their rate per spill,
call-outs, work orders) never put Gallowfen alone at either end (asserted).

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "discharging in 2026" | any discharge the overflow's monitors recorded in 2026 | the 12/24 spills, or the telemetry's overflow alarms | Gallowfen discharged on every source | same call |
| SF2 | "passing forward" | the flow the station sends into its rising main | the station's inflow | the inflow exceeds the pump whenever it spills | condition 2.3.1: "passing forward to the rising main" |
| SF3 | "less than the flow its permit sets" | strictly below | at or below | no station within 1 l/s of its permit | same call |
| SF4 | "while it spilled" | the station's rate around its 2026 discharges | its rate over the whole year | Gallowfen's 12,939 cycles have a 95th percentile of 48.6 l/s, the cycles within six hours of its spills a median below 72 | same call |
| SF5 | "the station" with two pumps | either pump, as they alternate | both, or the duty pump | Gallowfen's pumps move 47.97 and 47.93 l/s | same call |
| SF6 | "any of our overflows" | one or more | exactly one | exactly one breaches | same call |
| SF7 | "in 2026" | the reporting year in UK local time | the UTC year | no discharge within hours of either year end | same call |
| SF8 | the self-report "names the overflow" | one overflow and its permit | a list of overflows | one breach | WW-ENV-PR-014 section 7: "A self-report names one storm overflow and its permit." |
| SF9 | "whole litres per second" | the rate rounded once, compared unrounded | rounded before comparing | whole l/s separates every station from its permit | same call |
| SF10 | "the flow its permit sets" | `pass_forward_ls` | the condition's text | identical on all fourteen permits | same call |
| SF11 | "spills counted as our reporting procedure counts them" | the 12/24 count on the overflow's discharges, every monitor pooled | 12/24 per monitor serial, summed | moves the asks at nine or more overflows, never the call | WW-ENV-PR-014 section 3: "Spills are counted for each storm overflow" |
| SF12 | "hours of discharge" | the union of the overflow's records | the records summed; one unit kept through a handover | summed adds 1.5 hours or more at every replaced overflow | WW-ENV-PR-014 section 4: "any period of discharge counted once" |
| SF13 | "the percentage of the year its discharges were monitored" | each local day's most hours any of its monitors reported, over 8,760 | the hours summed across monitors; each day capped at 24; the mean of its monitors' hours | the capped sum equals the golden; a 24-hour cap rounds the same at every overflow; the mean moves the eleven replaced overflows by 0.1 or 0.2 (an hour two monitors watched was monitored, not half monitored) | WW-ENV-PR-014 section 5: "the percentage of the hours in the reporting year during which its discharges were being monitored" |
| SF14 | the volume between control levels | the register's duty start and stop levels | the levels the outstation logs at each start and stop | same whole l/s at every station | same call |
| SF15 | the cycle estimator | median of each cycle's volume over on-time plus volume over the off-time before it | mean, trimmed mean; mean of the two off-times; night cycles | 24 members, Gallowfen 47.88 to 48.29 | same call |
| SF16 | the metered stations | the cycles, as everywhere | the meter | same whole l/s at all three | same call |
| SF17 | the grain of the rate | the station | each pump | same whole l/s | same call |
| SF18 | which overflow a retired serial watched | the station whose overflow alarms its discharges match most closely, among those whose register monitor went in the nine days before it retired (six to eight days in every batch) | the handover week's discharges against the new units' | every serial placed the same way, the runner-up at 0.58 of the best or less | same call (asks only) |
| SF19 | the candidate set for a retired serial | the batch whose register installs fall in the nine days before its retirement | every station | each retirement follows exactly one batch, its stations in distinct radar zones | same call (asks only) |
| SF20 | "each storm overflow" in the return | every serial the platform holds for the overflow | the serial the register lists today | the register serial alone misses spills, hours and operational time at all eleven replaced overflows | WW-ENV-PR-014 sections 3 to 5 count, time and monitor "each storm overflow" |
| SF21 | the discharge log's clock (the chart's months, the count, the hours, the serial mapping) | UK local time, converted | the log read as UTC | no graded figure moves: every count, every hours figure and every chart cell is the same at one decimal, and every retired serial still lands on its overflow (the batch carries it); only the summer discharges stop meeting the alarms, 0 of 101 within five minutes of one against 99 of 101 on local time | the data: the log's starts sit about a minute after the UTC overflow alarms in winter and about an hour after them in summer |
| SF22 | a 24-hour block "contains discharge" | any part of a discharge falls within it | only a discharge that starts in it | Marram End 54 spills against 57 and Hagworth Wold 29 against 30, every other overflow unchanged, the call untouched | WW-ENV-PR-014 section 3: "A block contains discharge when any part of a discharge falls within it." |

## Closure table

| # | Axis | Reading in this build | Move |
|---|---|---|---|
| 1 | Population | the fourteen overflows on the consents register, every one monitored | C1: the prompt's "our Marsh and Wolds pumping station storm overflows" and the register's fourteen rows agree |
| 2 | Unit of account | the overflow and its station | the question names the overflow; one permit per station |
| 3 | Attribution window | 2026, a discharge in the year it starts | filed in WW-ENV-PR-014 section 2; C1, no discharge near either year end |
| 4 | As-of dating | the register and monitor list as exported on 15 January 2027 | filed by the export dates; the 2026 records are complete |
| 5 | Version basis | the permits as issued and last varied before 2026 | C1: one condition text per permit, varied 2021 to 2023 |
| 6 | Denominator | operational time over the year's 8,760 hours | filed in section 5 (the hours in the reporting year) |
| 7 | Weighting | the median over a station's cycles | C1: the 24-member estimator family gives the same whole figure |
| 8 | Window length | every 2026 cycle | C1: night-only and all-cycle windows agree |
| 9 | Boundary inclusivity | strictly less than the permit's flow; a 24-hour block counts when any part of a discharge falls in it | C1: no station within 1 l/s; the block filed in section 3 (SF22) |
| 10 | Rounding path | rates rounded once to whole l/s, hours and percentages once to a decimal | asserted: delivered rates 0.17 l/s or more inside their bins across the family; every hours figure, the year's in the return and each month's on the chart, a minute or more from its rounding line (settled in `settle.py`, 66 seconds at the closest); operational time 0.015 of a point or more above one |
| 11 | Tie-break | none needed | C1: no tie at any step |
| 12 | Maturity and censoring | a complete year | C1: every record closes inside 2026 |
| 13 | Order of operations | pool the overflow's serials, merge, then count and time | filed per overflow in sections 3 and 4; the per-serial order differs (SF11, SF12) |
| 14 | Row order | the telemetry's re-sent events out of order | C1: the cycles are taken on the sorted, de-duplicated events |
| 15 | Duplicate resolution | exact re-sent events dropped; two units' records of one discharge merged | C1 for the call (asserted neutral); filed for the asks in section 4 |
| 16 | Identity normalisation | permit, site id, RTU number and station code | the register's own crosswalk columns; C4 |
| 17 | Netting against gross | none | not an axis this call has |
| 18 | Dimensional units | m3/h duties at four stations | units in the register's own column; C1 for the call |
| 19 | Code and status semantics | the monitor list's ACTIVE and RETIRED, the alarm names | the platform's and the outstation's own codes; never the stump |
| 20 | Integerisation | spills as whole counts | C1 by construction |
| 21 | Clause scope | condition 2.3.1 governs every discharge of the overflow | filed in each permit's own text |
| 22 | Forward window contents | none: the call is a filing on a closed year | retrospective by necessity (the `## Draw` table) |

## Literal reader

Executed word for word, the prompt asks whether any overflow discharged in 2026 while its station was passing
forward less than the flow its permit sets; condition 2.3.1 sets that flow as the flow passed forward to the rising
main, the procedure fixes the reporting year and the self-report, and nothing in any file says how the flow passed
forward is established. Every reading of the terms (SF1 to SF10) gives the same call, and the open method is forced
by the data: the records time every pump cycle, the register gives every wet well's volume between its control
levels, and the 24 reasonable cycle estimators all print Gallowfen at 48 l/s against 72 and every other station
above its permit, while the rated duty is a nameplate, not a flow passed forward. The asks' terms (SF11 to SF13,
SF20, SF22) are each fixed by a sentence of WW-ENV-PR-014 executed literally on the overflow, the log's clock (SF21)
by the data with no graded figure moving either way, and the mapping of the retired serials (SF18, SF19) converges
on two routes.

## Oracles

- The three rising main meters: they confirm the rated duty at their own stations and agree with the cycle rate
  there too (SF16), so they tie on both paths and rank nothing; Gallowfen has none.
- The overflow and high level alarms: they confirm that Gallowfen spilled (as every overflow did) and carry no
  rate; Gallowfen's 14 high level alarms sit tenth of fourteen.
- The work orders: routine visits, pump services, meter verifications and high level call-outs at every station,
  none at Gallowfen naming a fault, a flow or a test.
- The dry-day annex and the observation borehole: they explain Hagworth Wold's dry-day spills as groundwater, a
  second source agreeing with the wrong rung's facts, not arbitrating the call.
- The improvement plan: schemes by overflow for 2025 to 2030 with costs and drivers; it states no 2026 flow and
  ranks nothing on the pass forward condition.
- No control ties only under the golden: deleting the meters, the alarms, the work orders, the borehole and the
  plan leaves the call forced by the cycles and the register.

## Ask sheet

Asks, all on `overflow_return_lines_2026.csv` and `spill_hours_by_month_2026.svg`: per overflow its 12/24 spills
(A1, 14 figures), its hours of discharge (A2, 14), its monitored percentage of the year (A3, 14) and its hours in
each month (A4, 14 rows of 12 cells); beside them the scorecard's construction (the permit's flow, the flow passed
forward and whether it met the permit, 42 figures), which the call-lander has and the mirror misses. H18 home:
the return's lines are the audit trail of the call, the same overflows on the same return the self-report goes in
with, and the chart is that return's hours by month; no ask names, orders or titles anything on the pass forward
flow.

- Primary device, D7 (the true key elsewhere): eleven of fourteen monitors were replaced in three crew batches
  (Scarrow Leas, Kettlewade, Sedgefleet and Brackenings in March; Cressfleet, Sallowholme and Saltwade in
  September; Northwade Bank, Reedhaven, Thornmarsh and Swathe Drove in November) and the old units' 2026 history
  stays in the platform under serials the register no longer lists, retired with no site. The remedy is a
  reconstruction across two systems: each retired serial placed by its discharges against the telemetry's overflow
  alarms within the batch its retirement date follows (runner-up 0.58 of the best or less).
- Hazard, D1 (an inexact copy under two keys): through each handover week both units record the same discharges
  with their own thresholds, debounce and clocks; summed, they add 1.74 to 8.25 hours, one to three spills and 1.65
  to 2.22 points of operational time per replaced overflow.
- Texture, D8: the platform writes UK local time and the telemetry UTC. Read as UTC, the log's summer discharges
  stop meeting the overflow alarms, but the batch still places every retired serial and no count, hours figure or
  chart cell moves (SF21, asserted), so the clock is texture here and not a device.
- Stops per replaced overflow (Cressfleet as the example): the register's serial alone 5 spills, 10.6 hours,
  29.5 per cent; every serial pooled without merging 17, 27.1, 99.3; the golden 15, 24.1, 97.4. Every figure of
  A1 to A4 moves at all eleven (asserted, SF20).
- Pin test: the asking sentence pins the unit, the rounding, "counted as our reporting procedure counts them" and
  "the percentage of the year", and the procedure files per overflow, a period counted once and the year's hours;
  the device sits in which serials are the overflow's, which no sentence names. Zero device rows in the call's
  population: Gallowfen's monitor was never replaced (asserted). Realism: a fleet upgrade replaced in batches, old
  units left running until the crew came back, a platform that keeps a retired unit's history under its own serial.
- Span: the discharge log, the daily status, the monitor list, the asset register (serials, install dates, RTU),
  the telemetry's alarm table and the procedure: six files, seventeen columns of the five data files on the asks'
  causal path.

| Ask | Figures | Cracker (lands the call, hygiene battery, every filed rule, the register's serial) | Mirror (rated duty, same ask route) | Cracker |
|---|---|---|---|---|
| A1 12/24 spills | 14 | 3 of 14 (the three overflows never replaced) | 3 of 14 | miss |
| A2 hours of discharge | 14 | 3 of 14 | 3 of 14 | miss |
| A3 monitored percentage | 14 | 3 of 14 | 3 of 14 | miss |
| A4 monthly hours, by overflow | 14 | 3 of 14 | 3 of 14 | miss |
| C permit flow, flow passed forward, met | 42 | 42 of 42 | 30 of 42 | miss |

Cracker keep: 55.1 per cent of the 98 ask figures, 12 of the 56 device figures; the full includer (every serial
mapped through the alarms, the handover counted once) keeps 98 of 98.

Pair ceiling: 55.4 (cracker 75.3 on the call, mirror 35.6 off it, on 38, 7 and 55 L)

Mirror leakage: 42.9 per cent of ask weight

Measured by: generator/ceiling.py, run on the cut pack by build.py at every build, pack digest c6e59728678c48a4

## Leak sweep answered

`leak.py task210 --asof 2027-01-15`: REVIEW, no LEAK. Fixed in the generator on the way: sweep 13's LEAK on
"device" in `metadata.json`'s line for the monitor list, then its REVIEW lines on provenance lines that described a
file's contents or shared the note's vocabulary (each provenance line now names the source system only); the
procedure's "Telemetry and Monitoring team" renamed the Instrumentation team, so the procedure no longer carries
the word telemetry.

- Sweep 3, the procedure carries 9 of the call's 13 distinctive words: they are the procedure's own subject (self-
  report, storm overflow, permit, condition, discharged, station); it names no overflow, figure or station.
  Harmless.
- Sweep 4, 4 of 25 stump-paragraph terms in the procedure (register, dry-day, condition, company): institutional
  words and the dry-day annex the wrong rung uses; the procedure is silent on pumps, rates, wet wells, cycles,
  volumes, meters, serials and alarms (asserted in `checks.py`). Harmless.
- Sweep 12, four column names in the procedure (Investigation, Permit, issued, station): ordinary words of a
  procedure that happen to be headers elsewhere; it describes no file. Harmless.
- Sweep 6 (INFO), the consents register and the improvement plan name the overflows: the register lists permits
  in permit order and the plan schemes by overflow; neither ranks them on the pass forward condition.
- Files a reader may be told the sweeps flagged: `procedures/WW-ENV-PR-014_storm_overflow_EDM_reporting.pdf`
  (sweeps 3 and 12).

## Build record

- Generator: `python3 build.py` from `task210/generator` (sim, pack, documents, golden, deliverables,
  figures.json, metadata.json, submission.md, then 527 assertions in `checks.py`, 155 in `verify.py`, the ceiling
  sheet, target.zip). Two rebuilds byte-identical (target.zip, goldens, submission, metadata, figures.json).
- Stage 4, pass 1: the leak reader found no leak and the judge returned DETERMINISTIC, APPROVE. Closed after it with
  nothing graded moving (figures.json, the goldens, submission.md and metadata.json byte-identical): the 12/24 block
  defined in section 3 (SF22), SF13's averaging reading recorded, SF21 rewritten to what the data show, the meter
  historian's quality codes, the work orders' closure codes and technicians' notes, the planned visit round, and
  rung 0b written into the ladder.
- Stage 4, rung 0b hardened: Hagworth Wold's sewer takes chalk groundwater all year (`gw_base` in `world.py`, with
  the late-winter rise on top and its impervious area cut to 1.0 ha), and the other stations' dry weather flows are
  set so their drawdown without the inflow clears their permits; the pump rates are untouched, so every delivered
  rate, permitted flow and met verdict and Gallowfen's whole line are as they were, while the spills, hours and
  monitored percentages of eleven overflows moved (25 cells) and the golden, figures.json and submission.md were
  regenerated. The monitors' draw stays 35, which clears every margin on the new hydraulics.
- Stage 4, pass 2 (judge DETERMINISTIC, FIX_NOW; reader no leak), closed with nothing graded moving: solution step 5,
  SF18 and SF19 now give the same true span (a retired serial's batch went in six to eight days before it retired,
  and the mapping looks nine days back); `settle.py` moves the end (or, where another unit's record of the same
  discharge holds the end, the start) of a few discharges by the seconds that put every hours figure, the year's and
  each month's, a minute clear of its rounding line on the side it already rounds to, 47 stretches across the
  fourteen overflows, every spill count and rounded figure held (asserted); a technician's closing remark no longer
  restates the note. The return lines, figures.json and every rounded chart label are byte-for-byte as they were;
  the chart's fill shades moved a step at eight cells and three rows of the self-report's discharge table (the three
  Gallowfen discharges whose months were settled) show their new ends.
- The monitors' own draw (`MON_VARIANT` 35 in `world.py`) was chosen from 260 by a search that kept every hours
  figure 7 seconds or more from its rounding edge, every operational percentage 0.013 of a point or more above
  one (a 24-hour cap on 25 October lowers it 0.011), no month cell on an exact half, no day with two part-reporting
  units, 1.5 hours or more of handover duplication at every replaced overflow and the register serial alone off the
  golden on every figure. The delivered fractions are set so each station's 24-member estimator family sits 0.17
  l/s or more inside one whole litre per second.
- `figures_check.py` PASS (73 figures), `leak.py` REVIEW answered above, `guard.py heart` WARN (nearest 0.05),
  `guard.py surface` clean on personas, container audit clean on the pack and the goldens.

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
- 2026-11-04, eight replaced monitors in two crew batches: with the scorecard's construction columns kept by the
  call-lander, the paper pair ceiling came to 62.4 per figure; the replacements were widened to eleven overflows
  in three batches (the three ladder stations kept clear), which measures 55.4 on the cut pack.
- 2026-11-04, a November batch holding Northwade Bank and Sedgefleet: the two R3 stations spill within minutes of
  each other and Sedgefleet's old serial scored 0.90 of its best against Northwade Bank's alarms; every batch was
  redrawn with one station per radar zone (runner-up 0.55 of the best or less).
- 2026-11-04, the discharge log to the minute with a duration column: end less start disagreed with the duration by
  a minute and month cells fell on exact halves; the platform now writes start and end to the second.
- 2026-11-04, the handover's two records left open: the union against keeping one unit moved one-decimal hours at
  four overflows; WW-ENV-PR-014 section 4 now files the WHAT ("any period of discharge counted once").
- 2026-11-04, an alarm table holding only OVERFLOW OPERATING, and work orders drawn at random: one-use telemetry and
  dates no alarm or register backed; the outstation's high level, comms and kiosk door alarms were added, every work
  order now follows a crew visit, and the register's pump service and meter verification dates are those visits.
- 2026-11-04, Gallowfen rated at 82.4 l/s: it put Gallowfen alone at the bottom of rated duty over permitted flow
  (1.144, a sortable shipped statistic); rated at 85.3 l/s it sits fourth of fourteen (1.185).
- 2026-11-04, the names Wendle Water, Holmfleet WRC and Ashby Leas: the Wendle, Holm and Ashby stems repeat task127
  and task464, and the people screen read Ashby as a first name; renamed Lindmarsh Water, Fleetmouth WRC and
  Scarrow Leas.
- 2026-11-04, the 12/24 block's membership left to the reading (stage 4, pass 1): a block counting only where a
  discharge starts gives Marram End 54 spills against the golden's 57; section 3 now says a block contains discharge
  when any part of a discharge falls within it (SF22), nothing graded moved.
- 2026-11-04, SF21 as first written compared UTC months on the converted log; the judge read that the log taken as
  UTC shifts month-boundary cells and breaks the serial matching. Measured on the pack, neither reproduces (every cell
  the same at one decimal, every serial placed by its batch); SF21 now asserts the log read as UTC moves no graded
  figure and that the data force local time (a minute after the UTC alarms in winter, an hour in summer).
- 2026-11-04, a meter historian writing G on all 105,120 rows and work orders closed with a handful of verbatim
  outcome strings, on a routine round drawn by random kind (three electrical inspections a year at one station):
  quality codes as a historian writes them, closure codes with each technician's own note, and a planned round.
- 2026-11-04, rung 0b as first built (stage 4): the drawdown timed without the inflow flagged 13 of 14 stations
  with Gallowfen alone at 0.55 of its permit against 0.92 or more, so a solver either distrusted it and corrected to
  fill-and-draw or named its one outlier, and both landed the call. Hagworth Wold's year-round groundwater now makes
  it the route's outlier (0.39 against Gallowfen's 0.55) and the other stations' dry weather flows were set so the
  route flags three overflows, not thirteen.
- 2026-11-04, hours figures exact to the second left where they fell (stage 4, pass 2): 47 of the year's and the
  months' hours sat under a minute from a rounding line, seven of them within seconds, where a reader working to the
  minute would round them the other way; settled in the generator, a minute clear on the side each rounded to.

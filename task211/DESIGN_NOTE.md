# task211 design note

Architecture 1, drawn 2026-11-04. Whether any station of a regional ambient gamma dose-rate network recorded
radioactivity of artificial origin between 1 July and 30 September 2026, and if so which stations and on which
nights, for the quarter's notification. The number is fixed in Anomaly Detection & Diagnostics by
`START_HERE.md`; its seed (AD34, an offshore contractor's winter jack-up) supplied the objective only, for the
reasons in `## Tried and rejected`.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task211.json`, architecture v1, registered 2026-11-04 |
| Client domain / task type | Physical & Environmental Sciences (`physical-environmental-sciences`), `environmental-monitoring-exceedance` (serves AD and DQ): telling an increase of artificial origin in a monitored environmental quantity from the natural ones, read from the monitor's own record, is the field's exceedance determination |
| Objective | Anomaly Detection & Diagnostics: a real event (artificial radiation at a station) separated from artifacts that look like one (radon-progeny washout in showers that no rain gauge records, at the upland granite and coastal stations) and from an artificial source the field's natural-cause test clears (weld radiography that carries on through rain) |
| Decision | whether any station recorded radioactivity of artificial origin in the quarter, and if so which stations and which nights go into the notification (`designation_set`, none licensed on equal footing). Retrospective by necessity: a notification concerns detections that have happened; the forward action is the notification itself and the regulator's follow-up of the source before more exposures |
| Shape | `other`: a designation over every station (each station's verdict), the dates and highest ten-minute value at each designated station, with the chart's named parts, and the quarter's network workbook (each station's source check with its result, each station's timeliness, every weekly filter's gross beta concentration): 2 stations, 11 dates and 2 peaks, then 24, 24 and 39 figures; arithmetic in `## Ask sheet` |
| Gap / pattern / generators | `objective` decisive (the measure the screening runs on, an exceedance cleared by coincident rain, is not the quantity the notification is about, an excursion's origin), with `time` (the origin is read on the decay clock of each excursion's fall); pattern `none`; `G7` decisive (when can a natural excess physically vanish: no faster than lead-214 and bismuth-214 decay), `G12` (a dry record at a rain gauge is not a dry station) |
| Gate G | `decomposition_attribution`: each correctly reported excursion is assigned to its driver, natural washout or an artificial source |
| Strategy | `decomposition_attribution`; Layer 2 family `estimation_fit` (each excursion decomposed by the data's own physical structure); pattern `own:decay-bound-excursion-origin` |
| Forum, forcing event, org family | `operations_desk` (the network's duty desk decides what the notification carries), `period_close` (the quarter's close: the data freeze and the quarterly report the notification goes with), `university_or_school` (a university environmental radioactivity laboratory runs the network under contract to a joint committee of three county councils) |
| Role | the network's duty radiation scientist preparing the quarter's notification (`operations_director`) |
| Context artifact | `monitoring_export`: the network's ten-minute ambient dose equivalent rate export |
| Calibration | none |
| Personas | Cameron Brown (network manager), Hazel Lambert (duty radiation scientist), Julia French and Antony Connolly (field engineers), Frances Stevens (radiochemistry analyst), Katie Clarke (clerk to the joint committee), Rosemary Wood (radiation protection supervisor), and on the documents' signature blocks Kim Simpson, Brian Smith and Gerard Buckley, from `guard.py names --geo uk --seed 211` (`--n 20` for the last five); Marian Ward and Wayne Sanderson were dropped on `people.first` against task200 and task120, Shirley Collins against task123, Carole Davies against task105 and Lynne Rees against task305 |
| Fiction as-of date | 2026-10-09 (the duty scientist's quarter-end export; every record ends 30 September 2026 23:50 UTC) |
| Guard | `guard.py check` on the draft: BLOCK `ban.forcing_event` (statutory filing, task399) redrawn to `period_close`, the honest key (the quarter's close forces the report the notification travels with); BLOCK `ban.org_family` (`local_government`, task314) redrawn to `university_or_school` (a university laboratory runs the network under contract, as several regional networks are run); WARN `overuse.org_family` on `government_agency` cleared by the same redraw; the deliverable set from docx+png+xlsx (task314's) to docx+svg+xlsx; the question form from which to whether (the decision is a gate first, whether any station, then a designation, and `which` repeats task314 and task399); two personas. Standing at registration: WARN `overuse.domain` (answered below), WARN `repeat.gate_g` against task399 (task399 attributes delay minutes to a signalling display's button geometry; nothing shared but the label), NOTEs `test.same_puzzle_older` and `test.same_driver_older` answered by differentiation lines on the card (task249 v6, task111 v1) |

**Why the world moved.** AD34 asks which offshore site gets a scarce jack-up for a winter campaign: an
allocation sized by downtime avoided, an Opportunity Sizing call, not an anomaly one, whatever its header
says. Its mechanism, storm sequences whose calms are shorter than a floating vessel's round trip, is the
weather-window persistence replay that task170's seventh cell measured on code (`t170/proto/g1.py`) as "the
metocean field's own weather-window method", the careful reader's move; and the decision cannot leave the
offshore world. So the number moved to another client domain and world under the same objective.

**Why this cell, against `overuse.domain`.** The domain's four builds in the last twelve are two
emissions-inventory conformations (task461, task489), a pollution-source root cause (task398) and a sewage
overflow anomaly (task210); none monitors radioactivity or reads a decay chain. The cell's anomaly cards
(task180 seismicity, task189 herbicide limits, task193 groundwater gradients, task204 classroom ventilation,
task210 pump delivery) share no world, file or mechanism with this one, and no card or slot note on file
mentions radon, dose rate, radioactivity or radiography (`guard.py slots` on mechanism and setting nouns,
2026-11-04). The anomaly-detection task types outside this domain and energy were screened first, on paper and
on two prototypes, and every candidate died on a recorded measurement or a standing screen (`## Tried and
rejected`); energy's one anomaly task type is the most occupied anomaly cell on file. A physical record whose
physics bounds the natural cause is what the recent survivors on this objective share (task192, task193,
task210), and only this domain and energy carry one.

**Against task210 (same client domain and objective, drawn back to back).** task210 decides which sewage pumping station's storm overflow is self-reported, from the delivered rate a wet well's fill and draw cycles give against a permit's pass-forward flow; task211 decides which dose-rate stations notify artificial radioactivity, from the decay bound on each excursion's own ten-minute fall. They share no world, file, quantity, decision or decisive step. What they share is Layer 1 furniture any telemetered network carries: a platform clock against UTC, re-sent telemetry, a replaced unit. That furniture decides neither call, and the adjudicated clone read is the author's.

**Data-native sentence.** The network's probes count gamma rays every ten minutes and nothing else; rain
brings down radon's short-lived decay products and raises the count at whatever station the shower crosses, and
the excess that rain leaves can only fade as lead-214 and bismuth-214 decay, losing at most about a quarter of
itself in ten minutes; the network reads rain from six telemetered gauges in the valleys, which upland
convective showers and coastal night showers miss, while a pipeline contractor's weld radiography crew works
nights within a few hundred metres of two lowland stations in turn, through dry nights and wet ones alike, and
its excess appears and vanishes inside one ten-minute interval.

**Abstraction sentence (written to be refused).** "An excursion is cleared as natural when it coincides with
the trigger the natural cause needs, but the trigger is recorded at a few points while it falls everywhere,
and an artificial source runs through it; only the physical limit on how fast the natural cause's excess can
fade, read from each excursion's own fall, separates the artificial ones." No approved or delivered build
carries it. task210 (shipped) reads a station's delivered pump rate from its wet well's fill and draw against
its rated duty; task204 recovers a ventilation rate from a room's unsteady carbon dioxide balance; task180 v4
corrects detection for a daily noise cycle; task192 (shipped) locates repeated faults by a current signature;
task193 (shipped) conditions reference wells on the gradient. None classifies events by a decay bound on their
own record. Nearest driver on file 0.05 (task257, latent dimensions of categorical responses).

**Priced on a clean-truth prototype before carding** (`scratchpad/t211proto/rad2.py`, four seeds, no Layer 1
at all: 24 stations, five upland granite, five coastal, fourteen lowland, a 90 by 60 km region, six gauges,
Q3 at ten minutes, Bateman decay of deposited progeny, counting noise). The investigation-level count and the
largest excess land on upland stations on every seed; the nearest-gauge rain check, the any-gauge check, the
neighbour check and the dry-and-lonely combination each file a set of uplands and coastal stations that
includes or misses the two radiography stations; mean duration and mean peak point at uplands. Only the
decay-bound fall test (an excess above 30 nSv/h losing more than 55 per cent in one interval and staying down)
and the thirty-minute tail ratio land both radiography stations, at 5 to 8 events against at most 2 anywhere
else. Night share grazed the truth on one seed of four, so the build gives the coastal stations their
nocturnal showers and spreads the radiography into evenings and dawns; measured again at the generator.

**Sources.** Fully constructed for a fictional university laboratory, a fictional joint committee of three county councils and a fictional region of England (granite uplands, a coastal strip, a lowland vale), every file generated by `generator/` from a fixed seed: the platform's ten-minute dose-rate export (317,592 rows), the station register, the 2025 code migration table, the alarm configuration, a water company's rain gauge telemetry and site list, the operating procedure (MVGN-OP-04), the service agreement's Schedule 2, the source check visit sheets, the check source certificates, the field kit register, the sealed source register, the platform's ingest log, the air sampler field sheets, the pump controllers' logs and the laboratory's gross beta results, with two declared distractors (the 2025 annual report, the quarter's gamma spectrometry). Provenance in `metadata.json`.

**Invented names (H21).** The station, site and organisation names were redrawn after a check against real places and bodies: the first draw's university ("Hallcross", against Hall Cross Academy, Doncaster), its water company (against Dales Water Services) and a dozen station names that are real English villages or hills (Thorlby, Scarth Nab, Greygarth, Marrick, Stainby, Wansford, Saltholme and others) gave way to descriptive site names (Headland Lookout, Old Brickworks, Upper Reservoir), a region name (Northvale) with no university, water company or council of that name found, and three councils named for their ground (North Moors, Mid Vale, Saltmarsh Coast). Figures unchanged.

## Default path

The pipeline a competent analyst builds from the prompt's words, the operating procedure and the files' grain,
with the field's own screen for the deciding quantity in it (a counting network without spectrometry clears an
increase as radon washout when rain coincides with it):

1. Read `mvgn_dose_rate_10min_2026Q3.csv`, exact duplicate rows once, the three old-firmware outstations'
   microsieverts converted, test-mode (T) and fault (F) records set aside, as procedure section 2 defines them.
2. Take each station's reference level from `mvgn_alarm_config_2026Q3.json`; every value 30 nSv/h or more above
   it is investigation-level (procedure section 3); consecutive ones make a period.
3. Find each station's nearest rain gauge from the register's and the gauge site list's grid references, and
   put the gauges' fifteen-minute totals (`Time (GMT/BST)`) onto UTC.
4. Clear every period with rain at that gauge within an hour either side as washout; notify the rest, by
   station and date, with each station's highest value.
5. The careful analyst's refinements: clear a dry period too when a neighbour within 18 km was elevated at the
   same time, then keep only the dry, lonely periods that begin at night.

Ends on: 16 stations notified (MV129, MV142, MV158, MV166, MV176, MV184, MV207, MV214, MV226, MV231, MV243,
MV305, MV311, MV318, MV327, MV334), with MV334's 17/07, 20/07 and 07/08 and MV129's 24/08 and 17/09 cleared as
rain; the refinements still file 16 and then 12.

Golden: 2 stations, MV334 Headland Lookout on 6 dates (highest ten-minute value 155 nSv/h) and MV129 Old Brickworks
on 5 dates (164 nSv/h).

## Stump sentence

A rain screen, the analyst's own reflex and no filed rule (every period of the procedure's investigation-level
values cleared as washout when the nearest valley gauge recorded rain within an hour), files 16 stations (15 if
only periods with no rain at all are kept, 16 at a 1 mm tolerance: upland and coastal stations whose showers the
six valley gauges missed, beside the two radiography stations) and clears five of the eleven radiography
evenings that ran through rain; only reading each excursion's own end against the decay of the natural excess (radon decay
products cannot lose more than about a quarter of themselves in ten minutes, and every artificial increase
lost 85 per cent or more in one step) files the two stations and their eleven dates.

## Three rules

**Task type:** `environmental-monitoring-exceedance` in Physical & Environmental Sciences, which serves Anomaly
Detection & Diagnostics in the taxonomy: a real increase of artificial origin separated, in a monitor's own
record, from the natural increases that look like it.

**Domain test:** the quantity that decides is each dose-rate excursion's origin, natural washout or artificial,
which the field reads for a counting network without spectrometric probes by its coincidence with rainfall,
clearing increases that rain explains (the washout screen against precipitation records, which no document in
this pack files: the analyst brings it to the procedure's investigation level and the water company's gauges);
the deciding physics is the radon decay chain the washout excess comes from.

**Swap:** "Two hospital wards recorded infections of external origin on eleven dates" does not survive: the
deciding quantity is how fast a natural signal can end, set here by lead-214 (26.8 minutes) and bismuth-214
(19.9 minutes) decaying on the ground, and with another field's nouns there is no decay chain to bound the
natural cause, so nothing separates the two origins.

**Layer 1:** the platform re-read four station-days of a delayed backfill (exact duplicate rows); three
old-firmware outstations send microsieverts; source checks leave test-mode records; the 2025 batch of cable
glands at eleven stations lets water in after heavy rain and the outstation sends fault records with no dose
rate; power cuts leave no record; MV157's exchanged probe ran on the old probe's factor for eight days; the
water company's gauges keep UK clock time in 0.2 mm tips; one engineer records against the outstation codes in
microsieverts; the LoRa gateway stamps UK clock time; the gateway re-sends unacknowledged hours; a pump
controller was replaced and another's totaliser rolled over; the laboratory re-issued two results. Each is the
named system's own behaviour; none is placed to be caught, and none decides the call.

**Layer 2:** `estimation_fit`, each excursion decomposed by the data's own physical structure; the choice that
flips the call is whether an excursion's origin is judged by its trigger (rain recorded at a gauge) or by its
own end, against the rate at which a washout excess can physically fade.

**Decisive step:** recognising that clearing an increase on coincident rain presumes the gauges stand for every
station and that only natural increases coincide with rain, both false here, and judging each excursion by its
last step instead: an excess that falls by more than half in one ten-minute step and stays down cannot be
lead-214 and bismuth-214 decaying, whatever the gauges recorded.

**Not semantics:** reading every field, code, unit and definition correctly (the V, T and F statuses, UTC
interval starts, the microsieverts, the duplicates, the gauges' UK clock, the alarm configuration's levels)
leaves the rain screen on 15 or 16 stations; the difference between them and 2 is the physics of each
excursion's fall, not a reading of any file.

**Not rule application:** no filed rule or procedure performs the step: procedure section 3 files the
investigation level and its review, the agreement files what is notified, and neither says how origin is told;
the rain screen a strong analyst adds to them gives 15 or 16 stations. The enumerated family (the nearest-gauge, any-gauge, neighbour and night screens, the
investigation-level count, the decay-bound fall test at any reasonable setting) spreads from 2 to 16 stations;
the standing family, what the filed rules and the data leave defensible, spreads the same 2 to 16, because no
sentence and no column rules a rain screen out; what rules them out is silent physics no document states (a
natural excess fell 41 per cent in a step at most, every artificial increase 85 per cent or more), and inside
the decay-bound family the standing spread is zero (72 of 72 settings file the golden).

**Analyst test:** a strong analyst who cleans the export, reads every status and unit, applies the procedure's
investigation level and, by the field's reflex, clears every period the nearest gauge saw rain in files 16 stations (the default
path's `Ends on:`), and with the neighbour and night refinements 16 and then 12, all wrong: yes, the easy
route lands wrong with every field read and every rule applied.

**Estimand:** agreement Schedule 2, paragraph 2.2 (`MVJC_service_agreement_schedule2.pdf`): every increase in
the ambient dose equivalent rate recorded at a network station that is of artificial origin, giving the station,
the date of the increase and the highest ten-minute value recorded during it, the Contractor's own source checks
excluded; the window is the prompt's 1 July to 30 September 2026, the record the procedure's (section 2).

**No decoy:** nothing is planted to be caught: no copied block, hidden rule, memo, draft, briefing or stakeholder
figure carries an answer; the rain screen is the analyst's own reflex, written nowhere in the pack, and
the two distractors (the 2025 annual report, the quarter's gamma spectrometry) rank nothing on origin.

**No certified replay:** the method is not hidden and recovered by reproducing certified figures: no file holds a
past notification, a classified excursion or a validated detection, and the 2025 annual report records only that
nothing was notified that year.

**Lesson:** a coincidence screen fails both ways when its trigger is measured at points while it falls
everywhere and the artificial source runs through it, and a natural cause's own physics, here the decay of the
products rain brings down, bounds how its signal can end; no build on file classifies events by a physical
decay bound on their own record (nearest driver 0.05).

## Survivor anatomy

**Actor:** the deciding property, an excursion's last step against the decay bound, has no column in any file:
it is a relation between consecutive ten-minute rows of one station's record, measured against physics no file
states; the export's columns are station, interval, dose rate, unit, status and probe serial.

**Link:** the signal is read through a comparison the field's screen never asks for, each excursion's end
against the rate a washout excess can fade, instead of the join to the rain record the procedure invites; no key
offers it, and no sentence names radon, decay or a fall (asserted, R3b); the spectrometry report's nuclide library
lists lead-214's and bismuth-214's half-lives among eleven nuclides as plain nuclide data, and says nothing of
dose rates, rain or increases (asserted).

**Reflex:** the field's method for a counting network without spectrometry, clearing an increase on coincident
rain, sits at rung 0 (the analyst's addition to the procedure's investigation-level review) and files 16
stations; its refinements, the neighbour and night
checks, sit at rungs 1 and 2 and file 16 and 12.

**Back-test:** the textbook route validates on its own terms: every period it clears has rain at the gauge and
every period it notifies is dry there, the 2025 annual report records no notification under the same procedure,
and the quarter's gamma spectrometry finds no artificial nuclide in air, which a solver reads as consistent with
whatever the screen files because radiography leaves nothing airborne.

**Second use:** the decisive step reads only the dose-rate export, which every rung, the rain screen, the
telemetry ask and the quarterly report read for their own reasons; delete the step and the pack carries every
file it carries now.

**Shock:** the two stations are not the top or bottom two on any shipped per-station statistic (investigation-level
values rank them seventh and ninth, the screen's dry days first and joint fourth, the highest value, the mean, the
timeliness and the source check elsewhere), asserted as SHOCK in `generator/checks.py`; the radiography increases
peak at 155 and 164 nSv/h, under the upland washouts' maxima.

**Pins:** the WHAT is filed in the organisation's own genre, the agreement's notification clause (2.2) and the
procedure's record and review sections (2, 3); no filed sentence names the fall, the decay, the baseline, the
threshold or the clock the step rides on.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 the rain screen | fires: procedure section 3 files the investigation level and its review (the rain clearing is the analyst's) | fires: the gauges and the alarm levels are shipped columns | fires: the field's washout screen | no | no | no | no | readable |
| R1 the neighbour check | no | fires: the register's grid references | fires: a careful analyst's regional check | no | no | no | no | readable |
| R2 the night check | no | fires: the interval start's hour | fires: radiography is a night trade | no | no | no | no | readable |
| R3 the decay-bound fall (decisive) | no: no document names radon, decay or a fall | no: the fall is a relation between consecutive rows, no column | no: the field's reflex is the rain screen, and the bound is no named correction | no: no control scores a route | no: the battery computes no step ratio | no: the ratio is of the excess over a running median, recovered per excursion, not of a reported figure | no: the export is the network's record, read by every rung | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | station | the platform code the export carries | the outstation code | same call | same call (the export carries platform codes only) |
| SF2 | of artificial origin, against the network's own source checks | test-mode (T) records left out | T records read as monitoring data | adds five or more checked stations | agreement 2.2, "the Contractor's own source checks, are not notified"; procedure section 2, T "is not monitoring data" |
| SF3 | between 1 July and 30 September 2026 | UTC interval starts | BST bounds | same call | same call (every increase two days clear of either edge) |
| SF4 | on which dates | the date the increase starts, UTC | the BST date | same call | same call (every increase starts on the same date in both) |
| SF5 | the highest ten-minute dose rate | the highest value recorded | the highest excess above background | 155 and 164 against 89 and 94 | agreement 2.2, "the highest ten-minute value recorded during it" |
| SF6 | during its detections | one highest value per station over all its increases | one per increase | same per-station figure (the notification gives both) | the prompt's "each recorded during its detections" |
| SF7 | re-read station-days | exact duplicates read once | read twice | same call | same call |
| SF8 | microsieverts at three outstations | converted to nSv/h | read as nSv/h | same call | same call (none of the three is detected either way) |
| SF9 | fault (F) records | no value | blank read as zero | same call when set aside | procedure section 2, F records carry "no dose rate"; same call |
| SF10 | test mode | outside the record of monitoring data | inside it | see SF2 | procedure section 2 |
| SF11 | MV157's eight days on the old probe's factor | as recorded | corrected by the factor ratio | same call | same call (a 3 per cent step, MV157 detected under neither) |
| SF12 | consecutive values across a gap | adjacent intervals only | consecutive valid values across a power cut or fault | same call | same call |
| SF13 | the baseline the excess is read over | a centred 48-hour running median | a trailing 24-hour median, a seven-day 30th percentile | same call | same call over the family |
| SF14 | the fall test's settings | more than half, from 30 nSv/h, the next value staying down | more than half to 70 per cent, from 30 or 35, zero to two values staying down | same call, 72 of 72 | same call (the corners at 45 and 80 per cent, floors 25 and 40, at least half exact) |
| SF15 | an increase spanning midnight | dated by its start | both dates | same call | same call (no increase spans a BST midnight) |
| SF16 | the LoRa gateway's receipt stamps (the timeliness ask) | UK clock time, every other receipt UTC | the LoRa stamps read as UTC | same call (19 timeliness figures would move, asserted) | OP-04 section 2, "Receipts logged by the LoRa gateway are stamped in UK clock time; all other receipts are in UTC."; same call |
| SF17 | an F record against "the station's value" (the timeliness ask) | not a received value | counted as received | same call (the eleven gland-batch figures would move, asserted) | OP-04 section 2, "A record with the status F carries no value, so the platform has not received the station's value for that interval."; same call |

## Ladder

| Rung | Route | Ends on | Dies to |
|---|---|---|---|
| R0 (default path) | investigation-level periods cleared by rain at the nearest gauge within an hour | 16 stations, MV334 and MV129 among them, five of their eleven dates cleared as rain and three wrong ones added | upland and coastal showers the valley gauges miss; radiography that runs through rain |
| R1 | R0, a dry period also cleared when a neighbour within 18 km was elevated | 16 stations | local showers have no elevated neighbour; coastal night showers are single-station |
| R2 | R1, keeping the dry, lonely periods that begin at night | 12 stations | the coastal stations' night showers |
| R3 (decisive) | an excess of 30 nSv/h or more falling by more than half in one step and staying down | 2 stations, 11 dates | (the golden) |

Winners and margins: on the decisive rung the smallest fall that ended an artificial increase is 85 per cent and
the largest natural fall anywhere in the quarter 41 per cent, so the two populations sit 44 points apart against
a counting noise of about 10 points on the fall fraction at an excess of 30 nSv/h; no other station carries a
qualifying fall. Position: the truth is not the top or bottom two on any rung's statistic (investigation-level
values rank the stations seventh and ninth; the screen's dry days rank MV334 first and MV129 joint fourth). The
investigation-level count's top five are the upland granite stations (MV231 302 values, MV207 255, MV214 248,
MV226 247, MV243 193). Grid: three baselines, four fall settings, two floors and three persistence settings, 72
members, all the golden. Worth: the whole call, a designation of 2 stations with 11 dates and 2 highest values.
The pricing sequence: the residue the filed WHAT leaves is a method (which excursions are artificial), not a
knob; R0 files 14 wrong stations and clears 5 of the 11 true dates; no shipped column is affine to the decisive
quantity, which is a ratio of consecutive rows; the counting noise is the standard error of the fall, and the
two populations sit four noise widths apart.

## Closure table

| Axis | Name | Reading here | Closure |
|---|---|---|---|
| 1 | Population | every network station's record for the quarter | C1: every station's record ships and is read |
| 2 | Unit of account | the station, the date of an increase, the highest value | filed: agreement 2.2 |
| 3 | Attribution window | the quarter's UTC intervals | C1: every increase two days clear of an edge (SF3) |
| 4 | As-of dating | the export of 09/10/2026, every record ending 30/09 23:50 UTC | static: the quarter closed before the export |
| 5 | Version basis | the re-read station-days | C1: exact duplicates (SF7) |
| 6 | Denominator | none for the call; the asks' denominators filed | filed: agreement 2.3, procedure sections 4 and 5 |
| 7 | Weighting | none | none needed: a designation |
| 8 | Window length | the baseline's window | C1 over 48 hours centred, 24 trailing, 7 days (SF13) |
| 9 | Boundary inclusivity | more than half | C1: falls of 85 per cent or more against 41 at most |
| 10 | Rounding path | the record is in whole nSv/h; the highest value is a recorded value | C1: nothing is rounded |
| 11 | Tie-break | none arises | none needed |
| 12 | Maturity and censoring | the quarter complete at the export | static |
| 13 | Order of operations | units and duplicates before the fall test | C1 (SF7, SF8) |
| 14 | Row order | the export's row order | C1: every route sorts by interval |
| 15 | Duplicate resolution | exact duplicates | C1 (SF7) |
| 16 | Identity normalisation | platform against outstation codes | the migration table; the call reads platform codes (SF1) |
| 17 | Netting against gross | the recorded value is gross | filed: agreement 2.2 (SF5) |
| 18 | Dimensional units | nSv/h against microsieverts | units in the data (SF8) |
| 19 | Code and status semantics | V, T and F | filed: procedure section 2 (SF2, SF9, SF10) |
| 20 | Integerisation | none | none needed |
| 21 | Clause scope | the notification clause covers network stations | filed: agreement 2.2 |
| 22 | Forward window contents | none: the quarter is closed | none needed (retrospective, the reason under `## Draw`) |

## Literal reader

Executing the prompt, agreement 2.2 and procedure sections 2 and 3 word for word fixes the estimand (every
network station, increases of artificial origin between 1 July and 30 September 2026, each dated, each station's
highest ten-minute value recorded); every term and convention has a row above, closed by a sentence or `same
call`, each asserted in `generator/checks.py`; the method is open and forced by the data, the decay-bound family
filing the golden 72 of 72 while the rain screens file 16, 16 and 12 stations, so a literal reader who reads the
excursions lands on the golden and one who executes the screen lands on a different estimator of the same
estimand, never on a different reading.

## Oracles

None. No shipped control scores a route or arbitrates between them: the 2025 annual report's means and data
capture and the quarter's gamma spectrometry rank nothing on origin and are declared distractors, and nothing in
the pack validates or refutes the rain screen.

## Ask sheet

Three asks, all in `network_quarter_2026Q3.xlsx`, each the quarterly report's own content under agreement 2.4 (each
station's source check and its result, each station's timeliness, the gross beta results of the quarter's
filters): 24 source-check figures (per cent of expected, with the result), 24 timeliness figures and 39 filter
concentrations. None reads the call's population: the call reads the export's V records only, and the asks read
the visit sheets, the certificates, the kit and source registers, the ingest log, the field sheets, the pump
controllers' logs and the laboratory's results (asserted, SEP).

- Ask A, primary device D2 and D7 (a state the register does not show, rebuilt from a record no question
  invites): CS-0583 was out at the Radiation Metrology Unit from 5 August to 4 September; the sealed source
  register's transfer out and back and its 21 August stock check place the spare CS-0417 in KIT-2 meanwhile,
  while the kit register still names CS-0583 and the visit sheets record kits, not sources; the register records
  CS-0583's return into KIT-2 on 4 September (the stage 4 judge's fork on the 8, 10 and 17 September checks,
  closed), and CS-0417's August place rests on the stock check and elimination. Seven KIT-2 checks
  (MV166, MV157, MV135, MV327, MV207, MV158, MV334) move by about 5 per cent; no result flips (asserted).
  Hazards: the certificate in force by its date of issue (CS-0583's recalibration, issued 27 August, for its five
  checks after 4 September), the jig (KIT-3's J2 sleeve from the kit register, for the sheet with no jig
  column), the outstation codes and microsieverts on that sheet, and the three repeats.
- Ask B, primary device D4 (absence evidenced in the series itself): each sampler's flow transmitter drops out for
  three to ten hours in most weeks while the pump runs, so the controller logs RUN rows with a blank measured flow;
  the air drawn through the filter (procedure section 5) is the measured flow integrated over the filter's rows
  with every dropout filled from the measured flow either side, and the five ways of filling it (linear, the mean
  of the values either side, the value before, the value after, the filter's mean flow) give the same figure on
  every filter (asserted). Summing the logged flow as it stands leaves the dropouts out and moves 34 of 39
  filters. The producing systems name their counters in their own field names (the pump controller export's
  `measured_flow_m3_h` and `run_totaliser_at_set_flow_m3`, AS2's field sheet's `Volume at set flow (m3)`), so the
  set-flow volumes are not readings of the air drawn (the stage 4 judge's fork, closed). Hazards: AS1's
  controller replaced on 20 August (its totaliser restarts at zero), AS3's totaliser rolling over at 100,000, two
  results re-issued as version 2.
- Ask C, primary device D4 and D6 (absence evidenced in a file no habitual join reaches): at the eleven gland-batch
  stations the outstation's fault records arrive on time but carry no dose rate (procedure section 2), so the
  platform did not receive the station's value for those intervals (agreement 2.3); the ingest log counts them
  among its records, and only the export shows which carry none. OP-04 section 2 files what an F record is ("A
  record with the status F carries no value, so the platform has not received the station's value for that
  interval.") and the receipt clocks ("Receipts logged by the LoRa gateway are stamped in UK clock time; all other
  receipts are in UTC."), both at revision 6 with the platform migration (the pass-2 judge's two forks, closed,
  SF16 and SF17); the device's work stays the cross-file cut, since the ingest log alone shows no F. Agreement 2.3
  now says in its own voice that a
  value recorded in test mode for a source check counts (the stage 4 judge's fork, closed), and every figure is
  an interval clear of its rounding line with test-mode values counted or left out (asserted). Hazards: the LoRa
  gateway's UK clock, re-sent hours (the earliest receipt counts), the quarter's 13,248 intervals as the
  denominator, and a few watchdog resets inside batch ranges.
- Pin test: the asking sentence pins each quantity's name, unit and rounding; the procedure files the source
  check (section 4) and the concentration (section 5), the agreement timeliness (2.3); the devices sit in which
  source a kit held, which record measures the air drawn and which records carry a value, and no sentence names
  any of them. Realism: a source away for recalibration with the spare in its place, time-based totalisers on
  cheap samplers, a bad batch of glands.
- Span: the visit sheets, the kit register, the source register, the certificates and the migration table for A;
  the field sheets, the pump logs and the laboratory's results for B; the ingest log, the export and the
  register for C: eleven files on the asks' causal paths.

| Ask | Figures | Cracker (lands the call, hygiene battery, every filed rule, the kit register's source, the measured flow as logged, the ingest log's records) | Mirror (the rain screen's call, same ask route) | Cracker |
|---|---|---|---|---|
| A source checks | 24 | 17 of 24 (the seven KIT-2 checks while CS-0583 was away) | 17 of 24 | miss |
| B gross beta concentrations | 39 | 5 of 39 (the filters whose dropouts move nothing past a line, or have none) | 5 of 39 | miss |
| C timeliness | 24 | 9 of 24 (the eleven gland-batch stations and the watchdog resets) | 9 of 24 | miss |

Cracker keep: 35.6 per cent of the 87 ask figures; the naive route (the LoRa clock read as UTC, a source's first
certificate, the set-flow volumes) keeps 16.1 per cent; the full includer keeps 87 of 87.

Pair ceiling: 48.1 (cracker 64.6 on the call, mirror 31.6 off it, on 38, 7 and 55 L)

Mirror leakage: 35.6 per cent of ask weight

Measured by: generator/ceiling.py, run on the cut pack by build.py at every build, pack digest 82da52791b7d2981

## Leak sweep answered

`leak.py task211 --asof 2026-10-09` on the pass-2 cut: verdict REVIEW, no LEAK; every REVIEW answered here.

- Sweep 3, six golden figures in `mvgn_annual_report_2025.pdf` (99.5, 99.3, 98.6, 97.8, 99.4, 97.5): each is another
  station's 2025 annual mean or data capture, coinciding at one decimal with a Q3 2026 timeliness or source-check
  figure in the same narrow band; no station's 2025 figure equals its own Q3 figure (asserted in `checks.py`),
  and the report is a declared distractor that ranks nothing on origin.
- Sweep 3, 97.6 in `air_filter_gamma_spectrometry_2026Q3.pdf`: the emission probability of Cs-134's 604.7 keV line
  in the nuclide library, which coincides with MV103's source check; it is nuclide data, not a station figure.
- Sweep 3, `MVJC_service_agreement_schedule2.pdf` carries 8 of 12 distinctive words of the call: they are the words
  of the notification clause itself (2.2, the filed estimand), which the call repeats; the clause names no station,
  date or figure.
- Sweep 4, the procedure (6 of 25 stump-paragraph terms), the agreement (6), the spectrometry report (3) and the
  annual report (4): the shared words are the documents' own subject (stations, natural, report, increase,
  radiation, university, analyst, annual); none names radon, decay, a fall, a half or a step, and the spectrometry
  report's nuclide library gives half-lives and gamma lines only (asserted), so none names the move.
- Sweep 12, the annual report names four data values that the register's first rows carry (Beck Side, Carr Lane
  Allotments, MV166, MV176): it is the network's own annual record listing its stations, not a note written for
  the analyst, and it names no column of any file.
- Sweep 10, INFO: no writer signature in any container.

## Tried and rejected

- AD34's world (an offshore contractor's winter jack-up, storm sequences against a floating vessel's round
  trip): an allocation call, not an anomaly one, and its mechanism is the weather-window persistence replay
  task170's seventh cell measured as the metocean field's own method; the decision cannot leave the world, so
  the number moved (2026-11-04, before any design).
- Procurement bid rigging under Accounting, Audit & Forensic (a county highways framework's cover-pricing
  ring, the field's dispersion and cover screens at rung 0, a losing-bid cost-ordering test as the decisive
  step), prototype 1 (`scratchpad/t211proto/proto1.py`): the pooled price-level residual landed all four ring
  members on seed 0 and the losing-bids-far-above-the-winner screen landed them too; the per-firm
  within-tender slope was confounded by the ring's block of bids moving with the designated winner's cost.
  Dead (2026-11-04).
- The same, hardened (`proto2.py`: spread ring depots, covers drawn from the competitive losers' own margin
  distribution, a 6 per cent ring markup, firm efficiency spread and two premium firms): an efficient ring
  (its cheapest member is the designated winner) orders its own bids by cost at the top, so the losing-bid
  cost ordering separated weakly (ring slopes 0.0011 to 0.0040 against outsiders 0.0037 to 0.0058) and the
  reasonable test family forked, while the residual level still put the ring first on seed 0. Dead on Gate C
  and Gate F together (2026-11-04).
- Paper screens in the anomaly cells outside this domain and energy, each dead before code: a hospital ward
  where infections are acquired, credited through bed moves (task119 v1's origin-credited paths, which repeated
  task109 and task120); stage migration under differential staging (task271 architecture 1's coding-depth
  insight, the unit that measures risk more completely looks better); faults masked by a controller holding
  its setpoint (no anomaly task type outside the two physical cells hosts a control loop); a waterborne
  outbreak read by water supply zone (the question would name the zone, readability test 1); a Legionnaires'
  plume (root cause, and task188's note records practice disinfecting every tower); cash-in-transit shortages
  attributed to crews (task198 v2's measurer and place collinearity); warehouse shrink netted of offsetting
  mis-picks (the matching rule forks); vaccine failure by birth cohort (the grouping dichotomy); channel
  stuffing by sell-in against sell-through (the field's own test, the golden as the opponent's first move);
  fabricated trial data as inliers (a planted copy, rule 3); dialysis adequacy and urea rebound (a
  measurement-condition normalisation, the lane's fourth after task180 and task187); a pharmacovigilance dose
  gradient (the family forks); electric vehicle chargers reporting available while broken (task210's insight,
  a reported state overstating delivery).
- The radiation world's first prototype (`scratchpad/t211proto/rad1.py`): radiography and a density-gauge van
  too loud and too frequent, so the plain investigation-level count landed both artificial stations as the top
  two on all three seeds. Rebalanced in `rad2.py` (above) before the card was filed.
- The set-flow counters as ask B's device (the totaliser and AS2's hour-meter volume read as the air drawn): the stage 4 judge found it the weakest ask fork, closed by the producing systems' own field names; the device moved to the flow transmitter's dropouts, filled the same way by every reasonable fill (2026-11-07).
- Crediting the rain screen to the procedure (the submission's and this note's first wording): OP-04 files the investigation level and its review, never a rain test; the screen is the analyst's reflex, 15 or 16 stations by its tolerance, and the submission no longer states its count (2026-11-07).
- Leaving the LoRa receipt clock to the delay distribution and the F record to a reading of "value" (the pass-2 judge's two open ask forks, 19 and 11 graded figures): both filed in OP-04 section 2 as WHAT sentences, no graded figure moved (2026-11-07).

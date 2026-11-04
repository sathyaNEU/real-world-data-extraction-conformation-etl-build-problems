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
| Shape | `other`: a designation over every station (each station's verdict), the nights and peak dose rates at each designated station, and the network's quarter workbook (each station's monthly mean and data capture), with the chart's named parts; arithmetic in `## Ask sheet` |
| Gap / pattern / generators | `objective` decisive (the measure the screening runs on, an exceedance cleared by coincident rain, is not the quantity the notification is about, an excursion's origin), with `time` (the origin is read on the decay clock of each excursion's fall); pattern `none`; `G7` decisive (when can a natural excess physically vanish: no faster than lead-214 and bismuth-214 decay), `G12` (a dry record at a rain gauge is not a dry station) |
| Gate G | `decomposition_attribution`: each correctly reported excursion is assigned to its driver, natural washout or an artificial source |
| Strategy | `decomposition_attribution`; Layer 2 family `estimation_fit` (each excursion decomposed by the data's own physical structure); pattern `own:decay-bound-excursion-origin` |
| Forum, forcing event, org family | `operations_desk` (the network's duty desk decides what the notification carries), `period_close` (the quarter's close: the data freeze and the quarterly report the notification goes with), `university_or_school` (a university environmental radioactivity laboratory runs the network under contract to a joint committee of three county councils) |
| Role | the network's duty radiation scientist preparing the quarter's notification (`operations_director`) |
| Context artifact | `monitoring_export`: the network's ten-minute ambient dose equivalent rate export |
| Calibration | none |
| Personas | Cameron Brown, Julia French, Hazel Lambert, Antony Connolly (`guard.py names --geo uk --seed 211`; Marian Ward and Wayne Sanderson from the same draw were dropped on `people.first` against task200 and task120) |
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

**Sources.** Fully constructed for a fictional university laboratory, a fictional joint committee of three
county councils and a fictional region of England (granite uplands, a coastal strip, a lowland vale): the
network's ten-minute dose-rate export, the station register, the probe calibration certificates, the
maintenance visit log, the rain gauge telemetry, the network's operating procedure and the councils' service
agreement, and distractors. Provenance in `metadata.json`.

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

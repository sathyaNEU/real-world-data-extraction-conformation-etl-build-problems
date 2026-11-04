# task398 design note

Architecture 1, drawn 2026-11-04. The number is in Root-Cause Analysis (START_HERE.md). Its seed, RC04 (which of five
delay causes on a commuter line gets the winter's one fix, when the cause losing the most time is mostly recovered
before the terminal), gives the decision and the quantity only. The world, the dataset, the mechanism and the prompt
shell are new, and the seed's mechanism is not used (Tried and rejected, first line).

## Draw

| Field | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task398.json`, architecture v1, registered 2026-11-04T10:46:47Z at WARN (repeat.gate_g against task313) |
| Client domain / task type | Physical & Environmental Sciences (`physical-environmental-sciences`), `pollution-source-attribution` (serves RC): attributing the atrazine in a supply reservoir's raw water to the tributary sub-watersheds it came from is source attribution at a receptor |
| Objective | Root-Cause Analysis: the cause behind the raw water's days above the plant's carbon-feed trigger, rivals ruled out on evidence, named so that fixing it (the cost-share program in that sub-watershed) recovers the outcome |
| Decision | which sub-watershed above Lake Merrin gets Brennick Water's one 2027 atrazine cost-share program (`root_cause_named`), forward facing: the program must sign its farms before the April 2027 applications, and it is judged on the 2026 season, the last one closed |
| Shape | 12, drill-down to one leaf: the 2026 days above the trigger, by sub-watershed (each sub-watershed's days caused), with each sampled sub-watershed's atrazine past its station by month (April to July) and the plant's carbon by month (May to August) as the asks |
| Gap / pattern / generators | `objective` (each sub-watershed's load is correct and is not what the intake drew); pattern `none`; `G8` decisive (reachability: whether a tributary's water reached the intake's layer at all), `G7` second (the operating window: only while the lake is stratified) |
| Gate G | `decomposition_attribution`: the raw water's correctly recorded days above the trigger attributed among the sources |
| Strategy | `decomposition_attribution`; Layer 2 family `field_method`; pattern `own:inflow-entry-depth-against-the-intake-layer` |
| Forum, forcing event, org family | `board_of_directors` (the Board of Water Commissioners approves the program's placement), `season_or_peak` (the 2027 application season), `local_government` (a city department) |
| Role | the water production superintendent, whose treatment budget pays for the carbon and funds the program (`operations_director`; `programme_officer` was the first label and task313 holds it in the window) |
| Context artifact | `filed_standard`: the Source Water Protection Plan's cost-share section, and the plant's carbon-feed procedure |
| Calibration | none |
| Personas | Brandi Dougherty, Carl Newman, Rhonda Dixon (`guard.py names --geo us --seed 398`) |
| Deliverables | `cost_share_placement_2027.docx`, `atrazine_sources_2026.xlsx`, `raw_water_atrazine_2026.png` |
| WARN answered | `repeat.gate_g` against task313: decomposition_attribution is the FINE-numbers shape here (the plant's record is correct and the step attributes its days among the sources), on another objective (OS there), domain (healthcare there) and decisive mechanism (G7 there, G8 here) |

**Data-native sentence.** A reservoir stratified for the summer takes each tributary's water in at the depth where
the lake is as cold as that water, so the city's intake at its fixed elevation, 34 feet below full pool, draws only
the tributaries cool enough to enter its layer: Fennick Creek, fed by springs and running near the lake's
mid-depth temperature, slides in at the intake, while the warm Tessel River and Oxley Creek, carrying most of the
season's atrazine, spread across the surface layer and leave over the spillway, and Ladd Branch, colder than the
whole lake, runs to the bottom and out through the outlet.

**Abstraction sentence (written to be refused).** "The decisive quantity is which sources a receptor actually drew
from in each period, when the receiving body is layered and each source's inflow enters at the layer matching its own
temperature, so a receptor drawing one layer takes only the sources entering there, while a mixed budget books the
receptor's excess to the largest source." No approved or delivered build carries it: task263 separates wells
measured only in pumped blends by a mass balance across mixtures (sources mixed at the receptor in varying
proportions, every source present); task193 conditions background wells on a reversing gradient (a reference set
that sometimes samples the source); task245 rebuilds a PM10 station's lost days from the plume's bearing; task182
nets a continuous source's share against a background observable outside the window. Here no source is in a mixed
blend at the intake at all: the layering decides which sources the receptor draws, and the receptor draws one.
Nearest driver on file 0.07 (task182 v3 lineage).

**Same-puzzle and library tests.** Gap, pattern and decision type (objective, G8, root_cause_named) match no build
in the last twelve; gap, pattern and Gate G (objective, G8, decomposition_attribution) neither. The library has no
rigor card for this task type (Physical & Environmental Sciences carries none); the golden is not a card's method.

**Sources.** Fully constructed operating layer for a fictional city in northeast Iowa (Brennick) and its supply
reservoir (Lake Merrin on the Tessel River): three hydrometric exports (15-minute discharge and water
temperature), the department's two level loggers on the smaller creeks with their ratings and field visits, the
source water program's bottle log, autosampler run logs and tributary atrazine results from two laboratories, the
plant's raw-water log across its LIMS replacement, the carbon feeder's SCADA setpoints and alarm history and the
plant's daily operating report, the dam-site buoy's thermistor string, the dam's daily operations log,
the reservoir's area and capacity table and the intake tower's record drawing, the county extension's 2026
atrazine use survey, daily rainfall, the Source Water Protection Plan and the carbon-feed procedure. Provenance in
`metadata.json`.

## Default path

The pipeline a competent source-water analyst builds from the prompt's words and the files' grain, with the field's
own apportionment of a receptor's excess in it.

1. Take each day's raw-water result as SOP-WQ-07 2.3 sets it, from the legacy log and the LIMS export (the overlap
   20 to 26 May carries the same samples), and count the 15 April to 31 October days above 3.0 ug/L: 47.
2. Estimate each sampled sub-watershed's atrazine past its station from the bottles and the 15-minute flows (DC-04
   from its logger through the rating in force): the Tessel River carries the most in every month from April to
   July, 373 kg over the four months against Oxley Creek's 235, Dunmore Creek's 153 and Fennick Creek's 88.
3. Check the route against the record: the raw water rises after the storms that carry those loads (29 May after
   the 27 May storm, 9 and 10 June after the 7 June storm), so the loads
   explain the timing.
4. Apportion each day above the trigger by each sub-watershed's share of the atrazine that passed the stations in
   the 30 days before it, the receptor treated as one mixed volume, and count the day for a sub-watershed when the
   raw water less its share would have stayed at or below 3.0 ug/L (plan 5.1's counterfactual): the Tessel River 39
   days, Oxley Creek 22, Dunmore Creek 16, Fennick Creek 10, Ladd Branch none (14 and 45-day windows: 40 and 38 for
   the Tessel).

Ends on: Tessel River (39 of the 47 days by the 30-day load share)

Golden: Fennick Creek (all 47 days; every other sub-watershed none)

## Stump sentence

A competent analyst who estimates each sub-watershed's atrazine past its station from the samples and the 15-minute
flows, sees the raw water rise on the storms that carry those loads and books each day above the trigger by the
trailing 30-day load share names the Tessel River (39 of 47 days), when the lake was stratified on every one of those
days, the Tessel's warm water spread over the surface layer above the intake, and Fennick Creek's cool spring-fed
water entered at the intake's own depth and was behind all 47.

## Three rules

Task type: pollution-source-attribution (Physical & Environmental Sciences), serving Root-Cause Analysis: the cause of the raw water's days above the trigger, attributed among the tributary sources at the receptor and named so that the program placed on it removes the excess.

Domain test: The quantity that decides the call is how much of each sub-watershed's atrazine reached the water the intake drew on each day above the trigger, a receptor-attribution quantity the source-water field estimates by apportioning tributary loads in a mass balance (rungs 0 and 1 here) and a limnologist works out for a layered reservoir by routing each inflow to its density level.

Swap: "Place the infection-control program in the ward whose patients caused the most days above the hospital's alert" reads only as a load share; nothing in a ward enters a building at the depth of matching temperature, so the reservoir's layering and the intake's fixed elevation, which decide here, have no counterpart and the call stops making sense.

Layer 1: the plant's LIMS replacement (legacy log to 26 May, LIMS from 20 May, overlap) and its ELISA screens against State laboratory confirmations; the buoy logger kept on CST and its string re-hung on 10 June half a metre lower, sensor 9 dead 21 July to 1 August; the intake drawing in NAVD88 against the dam log in NGVD29; the DC-04 and LB-05 loggers on UTC, DC-04's rating replaced after the May flood and its logger sliding in its pipe on 3 July; storm bottles logged when the carousel came off, with positions that drew nothing; the State laboratory's bottle numbers without hyphens; the SCADA setpoints and alarms in UTC and the feeder's trips and empty hopper; OC-03's October equipment gap and the January ice-affected flows. Each is what its system writes; nothing is placed to be caught.

Layer 2: field method family; the choice that flips the call is to treat the reservoir as the stratified lake its buoy records and attribute the intake's water by where each tributary entered it, against the field's reflex of apportioning the excess by load share as if the lake were mixed.

Decisive step: Recognising that the lake was layered on every day above the trigger, so the intake drew one layer, and placing each tributary's water at the depth where that day's temperature profile was as warm as the tributary, which leaves Fennick Creek's water the only water entering the intake's layer from late April to the end of July.

Not semantics: Reading every field, code, unit and definition correctly (the confirmation over the screen, strictly above 3.0, the 15 April to 31 October season, the datum conversion, the buoy's CST clock and re-hang, the loggers' UTC) still leaves the load-share route on the Tessel River, because no file holds an entry depth, a layer or a source share and the call turns on a computation across the buoy's profiles and the stations' temperatures, not on the meaning of any column.

Not rule application: No filed rule places an inflow in the lake: plan 5.1 files the counterfactual and nothing says how to know what the intake drew; the enumerated family (season load, trailing load share over 14, 30 and 45 days, flow-weighted concentration, lagged correlation, regression on 14-day means, the nearest entry, presence in the intake's layer over half-widths 1.0 to 3.5 m and look-backs 0 to 120 days) spreads from the Tessel River at 38 to 40 days to Fennick Creek at 47; the standing family (the members consistent with the layering the buoy records on all 47 days) gives Fennick Creek 47 and every other sub-watershed none in every member, and the ruling out is quiet: it lives in the buoy table and the station temperatures read together, in no sentence.

Analyst test: Yes. A strong analyst who cleans every file and reads every rule, estimates the station loads (the Tessel River largest in every month), sees them line up with the raw water's storm rises and apportions each day by the 30-day load share files the Tessel River (39 of 47 days), because the lake is treated as one mixed volume.

Estimand: Plan SWP-01 5.1 and 5.2 (program/source_water_protection_plan_rev2.pdf) with SOP-WQ-07 2.3: the program goes to the sub-watershed of Table 2 whose atrazine was behind the most days of the last completed season, 15 April to 31 October 2026, on which the day's raw-water result was above 3.0 ug/L, a day counting for a sub-watershed when the raw water would have stayed at or below the trigger that day without that sub-watershed's atrazine.

No decoy: Nothing is planted: no memo, draft, briefing, prior placement or stakeholder figure argues for the Tessel River; the loads are correct and the solver computes them; no block of readings is copied; every rule the call needs is filed and nothing decisive is withheld.

No certified replay: No certified or published figure carries the method: the pack holds no earlier season's attribution, no consultant's study and no validation record to reproduce, and every entry depth is computed from the raw profile and the raw temperatures.

Lesson: A receptor in a layered water body draws the layer it sits in, so apportioning what it received by the sources' loads is wrong when the sources enter at different depths; no build on file teaches an inflow's entry level against a fixed withdrawal depth (the nearest, task263, separates wells measured only in pumped mixtures where every source is present at the receptor).

## Survivor anatomy

Actor: The deciding property, the depth at which each tributary's water entered the lake on a day, has no column in any file: it is a relation between a station's daily temperature and that day's buoy profile, and the intake's depth is a second relation, the dam log's pool elevation against the S-4 drawing's centreline.

Link: The signal is read across files no key joins and the load method never opens for it: the buoy's CST hourly table with its service log, the stations' temperature columns (two loggers on UTC), the dam log and the record drawing; no shipped key, code or clause names a tributary and a depth together.

Reflex: The field's method for a receptor's sources, apportioning the excess by each tributary's trailing load share in a mixed-receptor mass balance, sits at rung 1 and files the Tessel River (39 days), and the season load at rung 0 puts Fennick Creek last of the four sampled.

Back-test: The textbook route validates: the raw water's rises follow the storms that carry the loads, and a lagged correlation of the raw water on each tributary's sampled concentration peaks between 0.688 and 0.705 for all four at 15 to 16 days, so the timing confirms the loads and separates no source.

Second use: Every file the decisive step reads is in the pack for its own reason: the buoy table and service log are the dam's water-quality record, the station temperatures are columns of the flow exports the load ask needs, the dam log carries the releases and storage, and the drawing is the intake's record; deleting the decisive step drops no file.

Shock: Fennick Creek tops no sort of a shipped statistic: not the load (last of four), the load per square mile, the peak, median or mean sample, the samples above 3 ug/L, the flow, the area, the flow-weighted concentration, the coldest summer water (Ladd Branch), the atrazine applied or the share of it exported (asserted in checks.py).

Pins: The WHAT is filed in the plan's own genre (SWP-01 5.1 and 5.2) and the procedure's (SOP-WQ-07 2.3 and 3.1); no filed sentence names stratification, a depth, a temperature, an entry level, a withdrawal layer or a look-back, and deleting any filed sentence leaves the call forced by the data.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Second use | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 season load ranking | plan 5.1 points at each sub-watershed's atrazine | loads from shipped columns | the field's first move | none | none | one sum per station | the station files | readable |
| R1 trailing load share, lake mixed | 5.1's counterfactual invites a share | shipped columns | the field's apportionment | none | none | one ratio per day | the station files | readable |
| R2 lagged correlation or regression on the tributary samples | none | shipped columns | a common check | none | none | one fit | the station files | readable |
| R3 entry depth against the intake's layer (decisive) | no sentence names layering, depth or temperature | no column holds a depth, a layer or a source | the reflex for a receptor's sources is the load mass balance; the entry level is the correction it skips | no control scores it | no battery step reaches it | a profile interpolation per tributary per day across three files | every file has its own use | silent |

The reflex row is enumerated from the field's vocabulary for a receptor's sources (load apportionment, mass balance,
flow-weighted concentration, correlation, regression, source fingerprinting), not from the rungs: fingerprinting needs
a tracer the pack does not carry (every tributary's atrazine is the same compound), and each of the others is a rung
above.

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the season | 15 April to 31 October (plan 5.2) | calendar 2026; April to September | Fennick Creek, 47 days in each | same call (no result above 3.0 outside 29 May to 27 July) |
| SF2 | above the trigger | strictly above 3.0 ug/L (SOP 3.1) | at or above | no result at 3.00 or in (3.00, 3.05] | same call |
| SF3 | a day's result | the confirmation where run, else the screen (SOP 2.3) | the ELISA screen alone | 52 days, Fennick Creek still first | SOP-WQ-07 2.3 |
| SF4 | caused | plan 5.1's counterfactual | the largest share; any contribution | Fennick Creek on every day | same call (Fennick's water the only water in the intake's layer) |
| SF5 | sub-watershed | the area above its station (plan 2.1, Table 2) | with the lake's direct drainage | no station, no candidate | plan 2.1 |
| SF6 | the intake's depth | drawing NAVD88 less 0.24 ft, against the NGVD29 pool | no datum conversion | 0.07 m, same sources | same call |
| SF7 | a tributary's temperature | its daily mean | the 08:00 reading; the noon buoy profile; the nearest entry | same sources every day | same call |
| SF8 | the intake's layer and look-back | 2 m either side, 30 days | 1.0 to 3.5 m; 0 to 120 days | same counts | same call (C3 corridor, asserted) |
| SF9 | the season judged | 2026, the last completed (plan 5.1) | a forecast of 2027 | not the filed season | plan 5.1 |
| SF10 | stayed at or below the trigger without it | against the residue the intake's layer held before Fennick's water reached it (0.21 ug/L) | against zero | same call | same call |
| SF11 | ask conventions | left 15-minute sum, mean offset per hang, local months | trapezoid; closing stamp in; median offset per hang; DC-04 months on UTC | the same 16 cells | same figures (asserted) |
| SF12 | the samples a month's flows take | the samples either side of each flow, whatever their month | samples inside the month only | cells move | the prompt: interpolating its samples linearly in time against the 15-minute flows |
| SF13 | the look-back into the mixed spring | stops where the lake was mixed | the presence test carried into April | days left unattributed | plan 5.1: the spring residue (at most 0.21 ug/L) cannot hold a day above the trigger |

## Ladder

| Rung | Construction | Tessel River | Oxley Creek | Dunmore Creek | Fennick Creek | Ladd Branch | Names |
|---|---|---|---|---|---|---|---|
| R0 | atrazine past the station, April to July (kg) | 373 | 235 | 153 | 88 | not sampled | Tessel, 1.59x Oxley; Fennick last |
| R1 | days by the 30-day load share, lake mixed | 39 | 22 | 16 | 10 | 0 | Tessel, 1.77x Oxley |
| R1' | 14 and 45-day load share | 40, 38 | 22, 22 | 17, 16 | 10, 9 | 0 | Tessel |
| R2 | lagged correlation (best lag), regression on 14-day means | r 0.701 | r 0.688 | r 0.697 | r 0.705 | not sampled | no source by a margin |
| R3 (decisive) | water entering within the intake's layer since the lake stratified | 0 | 0 | 0 | 47 | 0 | Fennick Creek |

Fennick Creek is fourth of four at rung 0, fourth at rung 1 and named only at rung 3. Margins: rung 0 1.59x, rung 1
1.77x; at rung 3 Fennick's entry is within 0.63 m of the intake on every day above the trigger and every other
tributary at least 4.5 m away from the lake's stratifying on 27 April to 27 July.

## Closure table

| Axis | Name | Reading | Move |
|---|---|---|---|
| 1 | Population | every sub-watershed of Table 2; Ladd Branch not sampled for the asks | filed (plan 2.1, 3.1) |
| 2 | Unit of account | the day | filed (5.1) |
| 3 | Attribution window | 15 April to 31 October 2026 | filed (5.2); C1, no day near the edges |
| 4 | As-of dating | the season closed 31 October; memo 3 November | filed |
| 5 | Version basis | legacy log and LIMS carry the same overlap samples | C1 (asserted equal) |
| 6 | Denominator | none: a count of days | n/a, C1 |
| 7 | Weighting | none: each day counts once for each sub-watershed it counts for | filed (5.1) |
| 8 | Window length | the look-back 0 to 120 days | C3 corridor (SF8) |
| 9 | Boundary inclusivity | strictly above 3.0; nothing in (3.00, 3.05] | C1 (SF2) |
| 10 | Rounding path | counts are integers; ask cells rounded once, each on its own | filed by the prompt; bins asserted |
| 11 | Tie-break | none needed: 47 against 0 | C1 |
| 12 | Maturity and censoring | the season is closed | C1 |
| 13 | Order of operations | the day's result before the count; offsets before the rating | C1 |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | the overlap days, the split bottles (State laboratory first, plan 3.2) | filed and C1 |
| 16 | Identity normalisation | hyphenless bottle numbers; site codes to stations by Table 2 | the systems' own keys, C4 |
| 17 | Netting against gross | none | n/a |
| 18 | Dimensional units | ug/L and ppb the same; cfs to litres; MGD and 8.34 (SOP 3.2) | units in the data and the SOP |
| 19 | Code and status semantics | NO LIQUID, U, < not detected as zero (plan 3.2) | filed and the records' own codes |
| 20 | Integerisation | whole days, whole kilograms and pounds | the prompt |
| 21 | Clause scope | 5.1's counterfactual per day | filed |
| 22 | Forward window contents | the call is judged on the closed 2026 season | filed (5.1); no forward driver needed |

## Literal reader

Executed the prompt, plan SWP-01 5.1 and 5.2 and SOP-WQ-07 2.3 and 3.1 word for word on the finished pack: the
days are the 47 season results above 3.0 ug/L; "caused" is 5.1's counterfactual; the only open HOW is how to know
what the intake drew without a sub-watershed's atrazine, and every member of the family that respects the layering
the buoy records gives Fennick Creek 47 and the others none, while the load-share members are ruled out by that
layering, which the buoy records on every one of the 47 days. The asks are pinned by the prompt (months, units,
rounding, linear interpolation in time against the 15-minute flows) and the records' own headers (the bottle log's
"Time logged", the autosampler log's "Sample time", the ratings' "Effective from ... CDT", the operating report's
"Plant day (06:00 to 06:00 next day)", SOP 3.2's pounds formula); the conventions left converge (SF11, asserted).

## Oracles

None. Nothing ties only under the golden: the raw water's storm timing fits every source, the dam log's storage,
releases and the area-capacity table balance whatever the attribution, and the extension survey ranks the Tessel
River first by application. For the asks, no total, control or second source confirms a load cell or a carbon month:
the operating report carries no carbon column, the State laboratory runs a quarter of the storm bottles at most, and
no file states a bottle's position or a feeder outage's length.

## Ask sheet

- **Ask A, each sampled sub-watershed's atrazine past its station in each month from April to July (16 figures,
  Ladd Branch not sampled).** Home: the program's load table the coordinator reports each November (plan 6.1). Files:
  the three station exports, the DC-04 logger, the ratings and field visits, the bottle log, the autosampler run
  logs, both laboratories' results. Primary D8 (a recorded time for the event time): a storm bottle's time is the
  autosampler's sample time for its position, while the bottle log and both laboratories carry the morning the
  carousel came off; the reconstruction left after noticing is which logged bottle filled at which position, the
  carousel's bottles in number order against the positions that drew a sample (NO LIQUID positions hold none). The
  logged-time route moves all 16 cells; the k-th bottle at the k-th position moves 8. Second primary D3 on a disjoint
  block (Dunmore Creek): gage height is the logger's level plus the staff-gage offset, and the logger slid 0.25 ft in
  its pipe on a dry afternoon between two visits; one mean offset moves May, June and July, offsets stepping at the
  visits or prorated between them move July. Hazards: the loggers' UTC clock, DC-04's rating change, the
  hyphenless State laboratory numbers, the split bottles (plan 3.2).
- **Ask B, the powdered carbon fed in each month from May to August (4 figures).** Home: the treatment budget's
  carbon line. Files: the setpoint historian, the alarm and event history, the operating report, SOP-WQ-07. Primary
  D4 (absence evidenced in a file no habitual join reaches): the feeder fed nothing while it was stopped by a motor
  overload until it was started again (the trip's return-to-normal comes hours before the restart) and while the
  hopper stood at low-low; the setpoints alone move all four months, run status alone moves three, a trip until its
  return-to-normal moves three. Hazard: the historian's UTC clock moves all four.
- **Chart:** the daily result against the trigger; it carries no ask figure and no decision quantity in its title.
- Separation: the asks read the stations' discharge columns, the bottles, the laboratories, the ratings, the run
  logs and the plant's SCADA and operating report; the call reads none of them but the stations' temperature columns,
  and no ask device row sits in a file or column the call reads (the DC-04 slip moves its level, not its
  temperature).

| Ask | Figures | Cracker (lands the call; battery and filed rules; bottle-log times, one mean offset, setpoints alone) | Verdict |
|---|---|---|---|
| A Tessel River, April to July | 4 | storm bottles at the logged morning | miss |
| A Fennick Creek, April to July | 4 | storm bottles at the logged morning | miss |
| A Oxley Creek, April to July | 4 | storm bottles at the logged morning | miss |
| A Dunmore Creek, April to July | 4 | logged morning and one mean offset across the slip | miss |
| B May to August | 4 | setpoints with no outage taken out | miss |

Measured on the cut pack by every route in generator/asks.py: the cracker keeps 0 of the 20 ask figures (2 of 22
criteria with the chart's two); the full includer (autosampler join, offsets stepping at the visits, outages taken
out) keeps 19 of 20 and misses Dunmore Creek's July; the join with one mean offset keeps 17; the join by
position keeps 11. If both top responses took the full join the pair would reach 81.0: that is the layer's exposure,
and the portal measures it.

Pair ceiling: 33.5 (cracker 50.0 and mirror 17.0 on the cracker's ask route, weights 38, 7 and 55)

Mirror leakage: 9.1 per cent of ask weight (the chart's two criteria)

Measured by: generator/ceiling.py

## Leak review (leak.py --asof 2026-11-03)

Verdict REVIEW, no LEAK; each REVIEW line ruled here.

- Sweep 1, `lake/merrin_dam_precip_daily_2026.txt`: the dam's cooperative-observer precipitation record, a station
  header and one value a day; it describes no other file. Harmless.
- Sweep 3, the plan carries the call's words: the words are the plan's own (program, sub-watershed, atrazine,
  cost-share) and Fennick Creek is one row of Table 2's five; no sentence places the program anywhere. Harmless.
- Sweep 4, the plan carries nine stump-paragraph terms: they are a source water plan's own nouns (intake, source,
  tributary, sampled, the sub-watersheds' names); the plan says nothing of layering, depth, temperature or an entry
  level, and deleting it leaves the call forced by the data. Harmless; not handed to a reader.
- Sweep 6, the extension survey names the candidates beside numbers: it ranks by atrazine applied, a different
  question, correctly (the Tessel River first); the plan's Table 2 gives areas. Neither ranks on days caused.
  Harmless.
- Sweep 8, the department laboratory's `Flag` column: the qualifier column its LIMS export carries (`<` below the
  reporting limit), not a generator flag. Harmless.
- Sweep 9, the buoy service log's 2026-11-09: a planned recovery date written on 31 October, forward-looking by
  nature. Harmless.

## Tried and rejected

- The seed's own world and mechanism (2026-11-04, before any draw): commuter rail punctuality has no root-cause task
  type in the client taxonomy (supply-chain-logistics inherits only general-statistics `interpretability` for RC, so
  rail would be a backdrop), and the seed's mechanism, delay absorbed by timetable slack before a deadline, is dead
  twice on file: task134 architecture 3 (missed connections against transfer buffers, "a generic scheduling tail, the
  swap reads the same with appointment slots") and task281 (a timetable replay whose hold reflex lands the golden and
  whose honest home is municipal service planning). The number moves world and client domain under its objective.
- A PM10 dust design at a village school monitor, two permitted sites on one bearing separated by the periods one
  stood idle (2026-11-04, paper): the separation by on/off combinations is task263's driver (each source's level
  measured only in mixtures of the sources running), and the PM10-plume-on-a-bearing setting is task245's and
  task121 architecture 3's (odour sources against the valley wind). Dropped before a card.
- Bathing-water bacteria from storm overflows judged by die-off in transit (2026-11-04, paper): task198's notes
  record the seasonal-percentile rebuild forking at 2.85 distinct answers per draw, and the decay rate is a free
  parameter no shipped record pins.
- Shape 07 (a grid of sub-watersheds by figures) at registration: `ban.shape` against task488 in the last two
  builds; redrawn to 12, which is the honest shape of a drill-down from the year's days to the sub-watershed behind
  them.
- `programme_officer` as the role at registration: `ban.role` against task313 (registered 10:22 the same morning);
  redrawn to the water production superintendent, the honester owner of a call whose purpose is the plant's carbon.
- The first lake prototype (scratchpad, 2026-11-04): an Eulerian layer model advected storm inflows through 0.5 m
  bins faster than one bin a day and created mass (the intake reached 2,000 ug/L); replaced by a Lagrangian stack of
  parcels that conserves mass by construction. A modelling defect, not a design death; recorded so the generator
  keeps the parcel form.
- An intake at 821.5 ft (41.5 ft below full pool) in the prototype: it sat in the hypolimnion's weak gradient (0.05 to
  0.2 C per metre in June), where a tenth of a degree moves an inflow's entry depth by metres, so no reading of entry
  depth could be determinate there; the intake moved to 829.0 ft, in the lower metalimnion's 0.4 to 1.1 C per metre
  from mid-June to September.
- A same-side condition on the boundary-day closure (both the screen and the confirmation clear of 3.0 on the same
  side) in the plant's results (2026-11-04, build): it piled results up just above the trigger; the closure keeps
  only that no reported result sits in (3.00, 3.05].
- Each sub-watershed's season load as the ask, with plan 3.2 filing that a sample's time is when its bottle was
  filled and 3.3 and 3.4 saying how logger discharge is taken and that storm bottles come off the carousel after the
  run (2026-11-04, design): every device on the ask was adjudicated by a sentence the work reads anyway, so the
  cracker kept the whole ask; the sentences are cut, the sample time is filed in the records' own headers (the bottle
  log's "Time logged", the run log's "Sample time") and the ask moves to monthly cells.
- The season's days above the trigger by month as an ask (2026-11-04, design): it is the call's own population, so
  it can carry no device and both top responses keep it; it stays in the memo as context and is not asked.
- Load cells for August and September (2026-11-04, measured): baseflow carries them, so no device moves them by a
  bin and the cracker kept three; the ask runs April to July.
- Ladd Branch in the load ask (2026-11-04, measured): about one kilogram a season, which no handling moves; LB-05 is
  a flow and temperature station and Ladd Branch is not sampled (plan 3.1).
- A 15-minute flow, temperature and atrazine series normalised day by day to the world's daily values (2026-11-04,
  build): it stepped at every midnight during recessions, which any hydrograph shows and the logger-step search
  found first; the series is built continuous, each storm a hydrograph from its start hour.
- The 30 June storm (2026-11-04, measured): its peak sat on the July boundary, where the left 15-minute sum and the
  trapezoid differ by a third of a kilogram on Oxley Creek, a fork on two cells; the storm moved to 27 June.
- A look-back carried into the mixed spring in the attribution (2026-11-04, measured): a presence test then leaves
  days unattributed at 45 and 60 days; the look-back stops where the lake was mixed (the spring residue, SF13).
- A 0.15 ft DC-04 logger slip on 8 July (2026-11-04, measured): one mean offset moved May and June only and the
  prorated reading moved nothing; the slip is 0.25 ft on 3 July.
- Whole-minute feeder events and setpoints beside seconds on every other alarm, an operator stamp only on the
  feeder's restarts, and dust-collector alarms in January with the feed idle (2026-11-04, realism): each marked the
  device's rows; the historian exports to the minute, operators stamp starts and stops on the feeder and the pumps,
  and the dust collector alarms on feeding and delivery days.
- Allamore County for the extension office (2026-11-04, house fix H21): three letters from Allamakee County, a real
  county in the same corner of Iowa; renamed Haldane County.
- A prompt opening "Where should" (2026-11-04, guard check): `repeat.question_form` against task488 v2, delivered;
  the decision is a pick, so the prompt asks which sub-watershed.

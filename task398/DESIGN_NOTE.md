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
| Shape | 12, drill-down to one leaf: the 2026 days above the trigger, by month, by sub-watershed (each sub-watershed's days caused), plus each sub-watershed's season load and the plant's carbon by month as the asks |
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
reservoir (Lake Merrin on the Tessel River): three USGS-style gauge records (15-minute discharge and water
temperature, RDB format), the city's two stage transducers on the ungauged creeks with their rating tables, the
source water program's tributary atrazine results from two laboratories, the plant's raw-water log across its LIMS
replacement, the carbon feeder's records, the dam-site buoy's thermistor string, the dam's daily operations log,
the reservoir's area and capacity table and the intake tower's record drawing, the county extension's 2026
atrazine use survey, daily rainfall, the Source Water Protection Plan and the carbon-feed procedure. Provenance in
`metadata.json`.

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

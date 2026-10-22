# task478 design note: the Calderwick Turnpike's 2027 virtual weigh station sections, by the share of tractor-semitrailers over the gross limit

Status lives in `pipeline.json`; this note holds the design. Read the Tried and rejected section first. Architecture 5
(re-rooted 2026-10-22); the records of architectures 1 to 4 are at the end.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task478.json` (architecture v5), registered 2026-10-22 after a pull, the
  architecture 1 to 4 identities in its lineage. `check` on the registered card: WARN only, answered here.
  `people.first` (Anthony, one older build, task130): kept at the guard's warning level. `test.same_puzzle_older`
  against task228 v2 (gap objective, method selection, a ranked slate): differentiated on the card, task228 ranks the
  instruments by their own random error from three series' covariances, while here the instruments are never ranked and
  the units they weigh are counted against a legal limit after each instrument's systematic bias is removed. Nearest
  drivers on file at 0.08 (task464 v2, task244, task251 v3).
- **Redrawn at the draw, and why the replacements are the honester labels.** The live window (task249, task273, task169)
  bans the government agency, the budget cycle, the council, the regulator, the committee and the policy adviser, and
  G3 as the decisive generator. A turnpike authority is a toll-funded public authority that owns its road, so
  `utility_or_infrastructure` is its family; the decision is the site schedule of a let contract
  (`purchase_order_or_contract`), recommended by the director of freight operations (`operations_director`) to the
  authority's executive team (`executive_team`). G16 leads because the decisive step is the construction that puts
  twelve instruments on one weight basis; G19 follows because the conformed weights are judged against a contract's
  limit. Context artifact `monitoring_export`: the director works from the WIM program's export.
- **Pairing:** Supply Chain & Logistics (house domain; transportation network) sitting in General Statistics & Data
  Science, task type `data-integration-record-linkage-entity-resolution`, the ETL task type the house domain maps to.
  The ETL work conforms twelve weigh-in-motion stations of two sensor technologies (the piezoelectric stations' fixed
  width export in tens of pounds, the bending-plate stations' CSV in kilograms), their controllers' local standard
  time, one station's renumbered lanes and the milepost list that ties stations to sections, onto one gross-weight basis
  for the five-axle tractor-semitrailers each station weighed in 2026. Objective: Data Extraction & Conformation (ETL).
- **The decision and the quantity:** the Calderwick Turnpike Authority (fictional) lets its virtual weigh station
  contract in 2027 and must fix the five sections that receive the screening sites by 1 March 2027. Its Freight
  Compliance Program 2027 places them at the five of its twelve sections with the highest share of five-axle
  tractor-semitrailers (FHWA class 9) whose gross vehicle weight exceeded the 80,000-lb limit, among the class 9 trucks
  the section's weigh-in-motion station weighed in calendar 2026. A retrospective quantity with its reason: the program
  sites the screening on the last closed year's trucks, and the contract runs from 2027.
- **Shape:** 01, a ranked list under a cap of five: twelve sections' shares over the limit at the whole per cent (12),
  the five sections (1), a chart's named parts (the twelve bars, the five marked, the labels: 3), the files (3), and the
  asks' twenty-four figures (each section's weekday entries and gross citations): 43.
- **Strategy:** `other`, named on the card: an instrument's multiplicative bias read on a component whose true size
  depends only on load state, matched by that state to a static reference, before readings are counted against a limit.
  Gate G `etl_conformance`: the conformed weights are the object and no shipped artifact ranks the sections. Gap
  objective (the quantity counted against the limit), pattern none, generators G16 (decisive) and G19. Layer 2 family
  `field_method`, pattern `own:an instrument's multiplicative bias measured on a load-independent component, matched by
  load state to a static reference, before readings are counted against a limit`.
- **World:** United States, an unnamed state's 284-mile Calderwick Turnpike in twelve sections between its system
  interchanges, one weigh-in-motion station per section (seven piezoelectric, five bending plate), two static scale
  houses at the mainline barrier plazas where the turnpike's enforcement unit weighs the trucks it pulls in. Personas
  from `guard.py names --geo us --seed 478`: Anthony Hale (director of freight operations), Anna Haynes (WIM program
  engineer).
- **Forcing fact:** the screening sites are fixed by 1 March 2027 for the contract's notice to proceed; the pack is as
  of 12 February 2027 (exports pulled 4 to 9 February).
- **Data-native sentence:** every station weighs a tractor's steer axle with the rest of the truck, and a steer axle
  carries the cab, engine and fuel, about 10,000 lb under an empty trailer and about 11,400 lb under a loaded one
  whatever the cargo, so a station whose loaded tractors' steer axles read several per cent above the scale houses'
  loaded tickets reads every axle that much heavy, and at the 80,000-lb line that carries a large part of a section's
  heavily loaded tractor-semitrailers across it; the sections also differ in how many of their tractors run empty.
- **The WHAT screen.** Population: the class 9 trucks the section's station weighed in 2026 (program 3.2). Outcome:
  gross vehicle weight over 80,000 lb (3.1). Window: calendar 2026 at the section's station (3.2). Unit: the share of
  those trucks, to one decimal of a per cent (3.3). Comparison: the five highest of twelve (3.1). The decisive step
  settles none of them: it is how each station's readings are put on the weight basis the limit tests, which nothing
  files.
- **Sources, one line each:**
  - The client's data-integration rigor patterns: here the sources disagree by an instrument bias, removed before the
    records are counted, not by linkage error.
  - The traffic monitoring field's weigh-in-motion quality control on class 9 steer axles and gross-weight peaks: the
    field's own check, here matched by load state and pinned to static tickets.
  - This slot's architecture 4 (a per-unit latency calibrated on surveyed covers): the instrument bias family, here on a
    weight basis with no surveyed control and a load-state confound.
- **Same-puzzle and same-driver tests:** (objective, G16, ranked_slate_under_cap) and (objective, G16, etl_conformance)
  against the last twelve builds, lineage included: task228 v2 only, differentiated on the card.
- **Abstraction test:** the nearest drivers stripped of nouns (task464 v2, units below a cut on a new instrument's scale
  linked by regression; task244, a share of moves in a two-period record; task251 v3, each unit's systematic error from
  paired checks) carry no instrument bias read on a component of every measured unit whose size depends only on a coarse
  state, matched by that state to a static reference before counting against a limit.

## Default path

1. Read the Freight Compliance Program 2027: the virtual weigh station sites go to the five sections with the highest
   share of five-axle tractor-semitrailers (FHWA class 9) whose gross vehicle weight exceeded 80,000 lb, among the
   class 9 trucks the section's weigh-in-motion station weighed in 2026 (section 3).
2. Parsed both exports: the piezoelectric stations' fixed-width records (weights in tens of pounds) and the
   bending-plate stations' CSV (kilograms), kept class 9 and the weighings the controllers did not reject, and joined
   the stations to their sections by milepost.
3. Counted each section's class 9 trucks over 80,000 lb on the gross as recorded and divided by its class 9 trucks
   weighed.

Ends on: Brannock, Cole Hollow, Garnet Ridge, Ingram Mill and Jessup Fork.

Golden: Cole Hollow, Elk Ferry, Garnet Ridge, Jessup Fork and Kettle Run.

## Stump sentence

The default path counts each section's class 9 trucks over 80,000 lb on the weights its station recorded and equips
Brannock, Cole Hollow, Garnet Ridge, Ingram Mill and Jessup Fork, because each weigh-in-motion station reads every
axle with its own calibration: Brannock's, Foxbriar's and Ingram Mill's read 5 to 7 per cent heavy and Elk Ferry's and
Kettle Run's 4 to 5 per cent light, which carries hundreds of loaded tractor-semitrailers across the 80,000-lb line;
a tractor's steer axle carries its cab and engine and moves only with whether its trailer is loaded, so each station's
loaded tractors' steer-axle median against the scale houses' loaded static tickets measures its calibration, and the
weights put on the static basis that way equip Cole Hollow, Elk Ferry, Garnet Ridge, Jessup Fork and Kettle Run
(11, 16, 21, 11 and 11 per cent against Dunmere's 7).

## Three rules

Task type: data-integration-record-linkage-entity-resolution (General Statistics & Data Science), through the house
domain Supply Chain & Logistics (transportation network): twelve weigh-in-motion stations of two sensor technologies
conformed onto one gross-weight basis and counted against a contract's limit, a task type serving Data Extraction &
Conformation (ETL).

Domain test: traffic monitoring's own weigh-in-motion quality control: the deciding quantity is each section's share of
class 9 trucks over the gross limit, which needs every station's readings on the static scale's basis; the field reads
a station's calibration off the class 9 steer axle, whose load depends on the tractor and on whether the trailer is
loaded, not on the cargo, and checks it against static weighings; with another field's nouns there is no steer axle,
no load state and no static scale, so nothing is left to decide.

Swap: put "hospital" for "section" or "megawatt-hours" for "pounds" and nothing reads: there is no axle carrying a
fixed part of every unit, no empty and loaded state to match and no static reference read on the same component; the
abstract move (an instrument's bias read on a component of every measured unit) needs the field's own axle physics.

Layer 1: the piezoelectric stations' fixed-width export in tens of pounds against the bending-plate stations' CSV
in kilograms; the controllers' local standard time all year; one station's lanes renumbered at a controller
replacement; the station list's mileposts with one station re-sited in 2025; weighings the controllers rejected left in
the export; the scale houses' tickets keyed by hand, the gross typed beside the axles; the toll system's UTC
timestamps and a plaza code reissued in 2026. Each is written by the system named, none is placed to be caught, and
each read the natural wrong way leaves the call where it is (checks.py R2a to R2f).

Layer 2: field_method, a weigh-in-motion station's calibration read on its loaded class 9 steer axles against the
static scales' loaded tickets, the axle load matched by load state because an empty tractor's steer axle is lighter and
moves with its trailer type.

Decisive step: dividing each station's weights by its loaded tractors' steer-axle median over the scale houses' loaded
tickets' (factors 0.951 to 1.066) before counting the class 9 trucks over 80,000 lb, which moves the five from Brannock,
Cole Hollow, Garnet Ridge, Ingram Mill and Jessup Fork to Cole Hollow, Elk Ferry, Garnet Ridge, Jessup Fork and Kettle
Run.

No decoy: nothing is planted: the exports, the station list, the tickets, the toll and citation records and the
documents are what each system writes; no report ranks the sections, states a station's calibration or says the
stations were calibrated; every station's bias is the kind every weigh-in-motion network carries.

Not semantics: every field, unit, code and clock read correctly (tens of pounds, kilograms, the rejected weighings,
local standard time, the renumbered lanes) still leaves the careful route counting the gross as recorded; no column
holds a calibration factor or a static-basis weight and nothing says one is needed; the step is an estimate (each
station's bias) and the correction it sets, not a reading.

Not rule application: the program files the population, the limit, the window and the cap (the WHAT); no filed rule
or procedure says how a weighing is put on the static basis or that the stations differ.

Analyst test: a strong analyst who conforms both exports, keeps the class 9 weighings the controllers accepted and
reads the program correctly counts the gross as recorded and equips Brannock, Cole Hollow, Garnet Ridge, Ingram Mill and
Jessup Fork; only the weights put on the static basis through each station's loaded steer axles equip Cole Hollow, Elk
Ferry, Garnet Ridge, Jessup Fork and Kettle Run (checks.py R3a on the generator's clean truth: the true gross gives the
same five).

Estimand: the Freight Compliance Program 2027 section 3: the five sections with the highest share of class 9 trucks
whose gross vehicle weight exceeded 80,000 lb among the class 9 trucks the section's station weighed in 2026 (a valid
weighing, local dates), the gross vehicle weight being the truck's weight as the law measures it, on a static scale
(section 2).

No certified replay: no ranking, share or calibration of any station ships; the scale houses' tickets are static
weighings of trucks pulled in at the barrier plazas, matched to no station, so no published figure ties under either
route.

Lesson: a weigh-in-motion station reads every axle through its own calibration, so shares over a fixed limit are
compared only after each station is put on one basis; the class 9 steer axle carries a load set by the tractor and the
load state, not the cargo, so its level at a station against static weighings of loaded tractors measures the
station, and pooling empty and loaded tractors or reading the gross peaks confounds the calibration with the traffic.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, the gross as recorded, the default path (Brannock, Cole Hollow, Garnet Ridge, Ingram Mill, Jessup Fork) | program s.3 the estimand: fires | gross: fires | count over the limit: fires | none | rejected weighings dropped | one count | readable |
| R1, every station's weights scaled to the tickets' gross (median, mean, loaded or empty median, a percentile: Ashford Gap, Elk Ferry, Garnet Ridge, Halbrook, Jessup Fork and kin) | none | gross: fires | match a sensor to the scale: fires | none | none | one divide | readable |
| R2, each station's steer axles pooled, empty and loaded, against the tickets' (Cole Hollow, Dunmere, Elk Ferry, Garnet Ridge, Kettle Run) | none | axle 1: fires | weigh-in-motion QC on the steer axle: fires | none | none | one divide | readable |
| R3, the empty tractors' steer axles or the empty gross peak (Dunmere, Elk Ferry, Garnet Ridge, Jessup Fork, Kettle Run; Brannock, Cole Hollow, Dunmere, Jessup Fork, Kettle Run) | none | axle 1, gross: fires | the empty peak: fires | none | none | one divide | readable |
| R4, every station scaled to the network's median station on its loaded gross (Ashford Gap, Cole Hollow, Halbrook, Jessup Fork, Kettle Run) | none | gross: fires | normalise to the network: fires | none | none | one divide | readable |
| G (decisive), each station's loaded tractors' steer-axle median against the tickets' loaded steer axles | no sentence says the stations differ or how a weighing is put on the static basis | no column holds a calibration | no reflex matches the steer axle by load state | none | none | none | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | gross vehicle weight | the truck's weight on a static scale (the law's) | the weight a station recorded | Brannock, Cole Hollow, Garnet Ridge, Ingram Mill, Jessup Fork: not the program's | program s.2 |
| SF2 | over the limit | above 80,000 lb | at or above | same call (asserted) | program s.2 ("exceeded") |
| SF3 | class 9 | the controller's class 9 | every five-axle vehicle | same call (asserted) | program s.3 |
| SF4 | weighed | a weighing the controller accepted | every record | same call (asserted) | the data dictionary (a rejected weighing carries no valid weights) |
| SF5 | 2026 | local dates, the controllers' standard time | UTC dates | same call (asserted) | the dictionary |
| SF6 | the section's station | the station inside the section's mileposts | the station list's 2024 milepost | same call (asserted) | the station list's re-siting date |
| SF7 | lanes and directions | every lane, both directions | the truck lane only | same call (asserted) | program s.3 (every class 9 truck weighed) |
| SF8 | the static reference | the scale houses' loaded class 9 tickets | every ticket | same call and figures (asserted: 17 empty tickets) | the data |
| SF9 | loaded | gross over 50,000 lb as recorded | over any line from 45,000 to 72,000 lb | same call and figures (asserted) | the data (the empty and loaded peaks sit 40,000 lb apart) |
| SF10 | a station's steer level | the median | the mean | same call and figures (asserted) | the data |
| SF11 | rounding | half up to the whole per cent from the unrounded share | none | none | the prompt's rounding |
| SF12 | ties for fifth | none (4.1 points clear) | none | none | the data |
| SF13 | a weekday (ask B) | Monday to Friday, holidays included, 261 in 2026 | business days | figures differ: not the program's | program s.5 |
| SF14 | an entry's date (ask B) | the local date of the entry, the old host's stamps already local | every stamp as UTC | figures differ: not the program's | program s.5 (local) and the stamps' own hours (A1) |
| SF15 | a section's interchanges (asks) | the plazas the plaza list places in the section, on the entry's date | the plaza list as it stands | figures differ: not the program's | the plaza list's effective dates and the 2025 toll schedule |
| SF16 | a citation for gross overweight (ask A) | a citation the enforcement unit issued for a gross over 80,000 lb | a ticket whose gross exceeds it | figures differ: not the program's | program s.6 |
| SF17 | where a cited truck entered (ask A) | the entry of the trip on which it was weighed, its tag's last entry before the stop on the hosts' own clocks | the citation log's entry plaza | figures differ: not the program's | program s.6 (the trip weighed) |
| SF18 | the files the call reads | both WIM exports, the station list, the tickets, the program | the toll entries, citations, plaza list, schedule | same call (asserted, X1) | the estimand |

## Ladder

Built figures, read from the cut pack by `generator/bundle.py` (each section's share over the limit, then the five).

- **R0, the gross as recorded, the default path: Brannock, Cole Hollow, Garnet Ridge, Ingram Mill and Jessup Fork.**
  Dies to the steer axles: Brannock's and Ingram Mill's loaded tractors' steer axles read 6 and 5 per cent above the
  scale houses' loaded tickets, Elk Ferry's and Kettle Run's 5 and 4 per cent below.
- **R1, every station scaled to the tickets' gross: Ashford Gap, Elk Ferry, Garnet Ridge, Halbrook and Jessup Fork**
  (the median, the mean or the loaded median; the other statistics file their kin). Dies to the tickets: the scale
  houses pull in heavy trucks, so their gross is no station's traffic, and the share over a fixed fraction of a
  station's own gross ranks the sections by how many of their tractors run loaded.
- **R2, each station's steer axles pooled, empty and loaded: Cole Hollow, Dunmere, Elk Ferry, Garnet Ridge and Kettle
  Run.** Dies to the empties: an empty tractor's steer axle runs about 1,300 lb lighter, and Dunmere's tractors run
  empty 48 per cent of the time against Halbrook's 14.
- **R3, the empty tractors' steer axles or the empty gross peak: Dunmere, Elk Ferry, Garnet Ridge, Jessup Fork and
  Kettle Run; Brannock, Cole Hollow, Dunmere, Jessup Fork and Kettle Run.** Dies to the trailers: an empty trailer's
  kingpin load and an empty truck's gross move with the trailer type, and the sections haul different trailers.
- **R4, every station scaled to the network's median station on its loaded gross: Ashford Gap, Cole Hollow, Halbrook,
  Jessup Fork and Kettle Run.** Dies to the freight: the bulk haulers on Elk Ferry and Garnet Ridge load to the limit,
  so their loaded gross sits high for a reason in the traffic, and scaling it down erases genuine overweights.
- **G: Cole Hollow, Elk Ferry, Garnet Ridge, Jessup Fork and Kettle Run (11, 16, 21, 11 and 11 per cent).** Each
  station's weights divided by its loaded tractors' steer-axle median over the scale houses' loaded tickets' (11,420
  lb; the stations read 10,856 to 12,170 lb).
- **Margins:** every licensed member (median or mean on either side, the loaded line anywhere from 45,000 to 72,000 lb:
  28 members) files the same five and every share inside its whole-per-cent bin, 0.17 points or more from its edge
  (checks.py G2, G3); fifth place clears sixth by 3.9 points under every member (G4). The loaded steer axles against
  the network's median station, a weaker anchor, still file the five (L5).
- **Position, separation and dominance:** a cap on a ranking, five of twelve; there is no decoy to dominate.
- **Worth:** the call and the twelve shares; the default path keeps three of the twelve shares and none at the
  sections that move.

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | the class 9 trucks the section's station weighed in 2026, weighings the controller accepted (SF3, SF4) |
| 2 | Unit of account | the truck weighed; the share of them over the limit; for the asks the entry and the citation |
| 3 | Attribution window | calendar 2026, local dates (SF5, SF14) |
| 4 | As-of dating | the exports of 4 to 9 February 2027 |
| 5 | Version basis | the station list and plaza list as of February 2027 with their effective dates; the 2025 toll schedule for retired codes |
| 6 | Denominator | the class 9 trucks weighed; for ask B the 261 weekdays |
| 7 | Weighting | none: every weighing counts once |
| 8 | Window length | one calendar year |
| 9 | Boundary inclusivity | over 80,000 lb, strictly (SF2) |
| 10 | Rounding path | half up to the whole per cent from the unrounded share; whole trucks and citations |
| 11 | Tie-break | none needed (SF12) |
| 12 | Maturity and censoring | 2026 closed; the exports run to 31 December |
| 13 | Order of operations | conform the exports, keep class 9 accepted weighings, put each station on the static basis, count, rank |
| 14 | Row order | none |
| 15 | Duplicate resolution | none in the WIM exports; the asks' entries once per entry, the new host's backfill twin dropped |
| 16 | Identity normalisation | stations to sections by milepost; plazas to sections by code and date |
| 17 | Netting | none |
| 18 | Dimensional units | tens of pounds and kilograms to pounds |
| 19 | Code and status semantics | the controllers' class and rejection flags; the citation codes; never the stump |
| 20 | Integerisation | whole per cent; whole trucks and citations |
| 21 | Clause scope | program s.3 governs the sites; s.5 and s.6 the asks |
| 22 | Forward window contents | the 2027 contract's five sites |

## Literal reader

Executed word for word, the program fixes the estimand: the five sections whose class 9 trucks weighed by the
section's station in 2026 most often had a gross vehicle weight over 80,000 lb, the gross vehicle weight being the
weight the law measures on a static scale. The candidates are the gross as each station recorded it and the gross put
on the static basis, and the data separate them: the scale houses' loaded tickets put a loaded tractor's steer axle at
11,420 lb, the stations' loaded tractors read 10,856 to 12,170 lb, and the stations' empty tractors and gross peaks
move with the trailers they haul; every member of the loaded-steer family files the golden five, while the gross as
recorded and the pooled and empty references file others (checks.py G1, R3b).

WHAT screen (stumping 1.2): population, program s.3; outcome, s.2; window, s.3; unit, the share; comparison, s.3. The
decisive step settles none of them.

## Oracles

None. No control, published figure or ranking ties only under the golden: no station's calibration, share or count
ships, and the tickets weigh trucks pulled in at the barrier plazas, matched to no station. The asks' files carry no
total that ties under one handling.

## Ask sheet

The director's recommendation carries, beside the five sites, each section's 2026 five-axle traffic entering at its
interchanges and the gross-overweight citations issued to trucks that entered there, the contract's screening volume
and enforcement baseline (H18: components of the call's case, read from the toll and enforcement systems, rows the call
never reads). The asks read no row the call reads (checks.py X1 to X3). Both ride on the toll back office's move to a
new host, a system switch the call never touches.

- **Ask B, each section's average five-axle entries a weekday in 2026: 12 figures, whole trucks.** Path: the toll
  entries, the plaza list, the 2025 toll schedule and the program (four files). Primary device: D1 with a staged
  switch. The back office moved to its new host plaza by plaza, on nineteen days from 18 May to 30 June, and the new
  host backfilled each plaza's last 18 days from the lanes' own logs (local time to the second) while the old host's
  rows carry its receipt stamp (local, to the minute, up to 15 minutes after the entry). Every backfilled entry is in
  the export twice, under two key schemes, up to 16 minutes apart. Reflexes and what they file (checks.py A2): every
  row kept, exact duplicates dropped, pairs within 60 seconds dropped, one cut at the new host's first row, one cut at
  the old host's last row, one entry a tag, plaza and day: each moves all twelve figures. Only a cut at each plaza's
  own last old-host stamp, or a pairing wide enough to catch the receipt delay, files the golden (asserted equal).
  Hazards: the old host's stamps local and the new host's own UTC (a one-clock reading moves one figure); the reissued
  plaza code P23. Round 1's readers took one global cut (reader A) and 60-second pairs (reader B) on the earlier device.
- **Ask A, each section's citations for gross overweight issued in 2026 to five-axle trucks that had entered there:
  12 figures, whole citations.** Path: the citation log, the scale houses' tickets, the toll entries, the plaza list,
  the 2025 toll schedule and the program (six files). Primary device: D8, a clock on the rows the old host wrote. The
  new host stamps its own entries in UTC (the dictionary says so of its stamps) and the old host's rows keep their local
  stamps in the same column; a truck cited for gross weight usually leaves through the barrier, offloads and comes back
  onto the turnpike at that barrier a few hours later (839 of them did). Read as UTC, an old-host return entry falls
  before the stop and the tag's last entry before the stop becomes the barrier: every section's figure moves (the
  barrier sections gain 100 or more), and the citation log's entry plaza, the tag's latest entry when a paper citation
  was keyed, agrees with that wrong reading on many rows, so checking one against the other confirms it. Only the old
  host's stamps read as local time file the golden; the evidence is the old host's stamps peaking at 07:00 against the
  new host's own at 12:00 and, read as UTC, 150 or more trucks entering at the barrier where they are weighed on the way
  out (checks.py A1). Hazards: the staged switch's twins; the reissued plaza code.
- **The construction layer:** the call and the twelve shares; the cracker has them.
- **Main population zero-counts (asserted):** the call reads no toll entry, citation or plaza row (X1, X2).
- **Referee:** none. **Sensitivity:** a reader who handles the switch right but reads every stamp as UTC keeps 11 of
  the 24 (pair 41.0 alone, 53.5 if the mirror does too); one with the clock right and exact duplicates dropped keeps 4.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, each section's gross-overweight citations | each citation at its tag's last entry before the stop (6.2), every stamp read as UTC, exact duplicates dropped: 0 of 12 | miss |
| B, each section's weekday entries | local weekdays from the stamps read as UTC, the plaza list by date with the 2025 schedule, exact duplicates dropped: 0 of 12 | miss |

Pair ceiling: 28.5 (weights 38 / 7 / 55, r 5: the cracker keeps the call and the instructions, 45.0; the mirror at the
default path keeps r and the instructions, 12.0; the asks read alike under both, 0 of 24)

Mirror leakage: 0.0 per cent of ask weight

Measured by: generator/ceiling.py

## Layer 1 inventory

| Item | System that writes it | File | Natural mishandling | Effect (asserted) |
|---|---|---|---|---|
| two export formats, tens of pounds and kilograms | the two sensor vendors' controllers | both WIM exports | kilograms read as pounds | every bending-plate station at zero over the limit, a loud failure every careful route repairs (R2a) |
| local standard time all year | the WIM controllers | both WIM exports | read as daylight time | none: the year's ends are in standard time (R2b) |
| Foxbriar's lanes renumbered 1 to 4 at its controller's replacement on 14 April | the replacement controller | the piezoelectric export | lanes 3 and 4 dropped | the call holds (R2c) |
| a re-sited station | the station list | the station list | the previous milepost | the same section (R2d) |
| rejected weighings | the controllers | both WIM exports | kept | the call holds (R2e) |
| hand-keyed tickets, the gross typed beside the axles (14 transposed) | the scale houses | the tickets | the typed gross trusted over the axles | the call and the twelve shares hold (R2f) |
| the toll back office's staged move to a new host: the old host's local receipt stamps, the new host's UTC, each plaza's backfill | the toll system | the toll entries | one clock or one cut for the year | moves the asks only (R2g, A1, A2) |
| plaza code P23 reissued to Halbrook East | the toll system | the toll entries, the plaza list | the list as it stands | moves Brannock's and Halbrook's ask figures only (R2h) |

## Architecture 4 record (spent 2026-10-22)

Architecture 4 resolved Kerbline's detections into potholes after moving each one back along its pass by its unit's
GPS latency, fitted on the surveyed utility covers, times the pass's speed. Over four stage 4 rounds seven of eight
readers missed the call, and reader F (round 3) landed it by fitting each unit's lag from the detections' offsets
inside rough clusters on the pass's signed speed; the judge's last pass (r4e) was DETERMINISTIC and APPROVE. A call any
reader lands is spent (leak-check), so the architecture is spent.

## Architecture 3 record (spent 2026-10-21)

Architecture 3 completed the unrecorded potholes with the fleet groups that drove a segment as the capture occasions
(units of one kind seeing the same potholes); three readers and the judge missed or confirmed it, the fourth landed the
call by estimating each group's visibility by maximum likelihood.

## Architecture 1 record (spent 2026-10-21)

Architecture 1 completed the unrecorded potholes over the distinct units that drove each segment (each unit either
always or never seeing a given pothole); eight readers and the judge missed or confirmed it, the ninth landed the call
by fitting each unit as an independent list. In architecture 3 that route is the careful wrong one.

## Architecture 2 record (spent 2026-10-21)

Architecture 2 resolved Kerbline's raw detections into potholes with a linkage tolerance set by each unit's positional
error, measured on surveyed utility covers; two readers missed it, two landed it by folding the sweepers' visibly
scattered reports into the precise units' potholes. Judge APPROVE (v2).

## Tried and rejected

- 2026-10-22, architecture 5 spent at stage 4 round 2 (zip md5 98e0e301): reader C landed the call without the
  tickets. It measured each station's gain on the vehicle classes other than 9 (two-axle, three-axle and six-axle trucks
  weigh alike at every station), referenced it to the four stations that agree within half a per cent, divided class 9
  by it and filed the golden five (Elk Ferry 20 and Garnet Ridge 23 against 16 and 21, the set unmoved), and it kept all
  24 ask figures (the backfill paired within 15 minutes, the other new-host rows read as UTC, each trip rebuilt from the
  tags). A multiplicative bias every class carries is measured by comparing across stations any population that should
  weigh the same everywhere, and an instrument calibrated before counting is the field's own standard method, so a
  golden that is that calibration is a strong reader's reflex: the next architecture's golden has to go past the
  field's standard method, with that method the default path. Judge r5b DETERMINISTIC with a FIX_NOW on step 5's
  one-sided backfill window (determinism_check_report_v5.md); reader D stopped at the spend.
- 2026-10-22, architecture 5 stage 4 round 1 (zip md5 feba8739): both readers missed the call on the default path and
  the judge (r5a) returned DETERMINISTIC and APPROVE, but both kept all 24 ask figures: the new host's re-import showed
  as two id schemes overlapping from 15 June (reader A cut once at the new host's first row, reader B paired within 60
  seconds, both right on that pack), and program 6.2 sent both to rebuild each trip from the toll tags, where the paper
  citations' overwritten entry plaza showed. The switch is now staged by plaza with a backfill and late receipt stamps
  (every global cut and tight pairing misses), and the old host's rows keep local stamps under the new host's UTC
  column while cited trucks come back through the barrier after offloading, so the tag rebuild read on one clock files
  the barrier (checks.py A1, A2).
- 2026-10-22, architecture 5 build: with the golden five also the five sections running the most loaded tractors,
  every station scaled to the tickets' gross (median, mean, loaded median) landed the five, because the share over a
  fixed fraction of a station's own gross ranks the sections by loaded share. Ashford Gap and Halbrook now run 84 and
  86 per cent loaded with light loads, Cole Hollow and Kettle Run 62 and 66 per cent with heavier ones, and every gross
  scaling files another five (checks.py L1).
- 2026-10-22, architecture 5 build: the network-relative loaded gross scaling landed the five while Elk Ferry and Garnet
  Ridge carried ordinary freight; their bulk haulers now load to the limit (a tight loaded gross near 77,000 lb), so
  scaling them to the network erases genuine overweights (L4).
- 2026-10-22, architecture 5 build: a loaded line of 70,000 lb moved Elk Ferry's share across a bin edge (a steer
  axle's own random error correlates with a gross cut through the loaded peak); a steer axle's random error is now half
  the other axles' (its single tires bounce less) and the bulk sections sit mid-bin, so every line from 45,000 to 72,000
  lb prints the same twelve figures (G2).
- 2026-10-22, architecture 5 build: with 3.5 per cent of the tickets empty, the stations' loaded steer axles against
  every ticket printed 15 and 20 for Elk Ferry and Garnet Ridge (a 20-lb shift in the reference); the scale houses'
  pull-ins are now loaded trucks bar 17, and the all-ticket reference prints the golden's figures (SF8).
- 2026-10-22, architecture 5 build: a ticketed truck's tag could enter again between its trip and its stop, so the
  tag's last entry before the stop missed the trip weighed on a handful of citations; a weighed trip is now an entry its
  tag does not follow for eight hours.
- Architecture 5 draw (2026-10-22): re-rooted on the author's standing rule (no retirement) with a fresh world.
  Screened before it and dead: competing exits read as censoring (task134's main call); landfill first-order decay
  (set aside at task486's draw against task480); the inspection paradox on headways (task135); unconstrained demand
  behind a capacity (task147, task168); triple collocation of three series (task228, landed); startup emissions by
  thermal state (task273's screen); risk pooling of a health trust's reserve (the careful route sums the members' claims
  and lands it); coincident peaks (task117); a register's overcoverage by signs of life (the register count reads as a
  surface figure overturned, Gate G); coding completeness from switchers (a data defect corrected); GPS chord length
  from sparse pings (a known pitfall, and the swap test reads it as geometry); departmental against hospital-wide
  cost-to-charge ratios (the cost-centre organ hands it over); an inventory trend's correlated factor errors (the
  variance-only screen in mirror image: the point estimate lands the golden); seasonal shares of the calendar year
  against detrended factors (classical decomposition is the reflex and the shares route can beat it); generic erosion
  after loss of exclusivity (task484 v1's ramp curve); a one-time service depleting its pool (task83's lesson).
- Architecture 4, potholes resolved after a per-unit GPS latency fitted on surveyed covers (2026-10-22, spent at stage
  4): reader F fitted each unit's lag from the offsets of its detections inside rough clusters, regressed on the pass's
  signed speed, and landed the call exactly (1,441 potholes, 1,427 on the roadway); seven other readers and the judges'
  first derivations missed. A displacement proportional to speed is identifiable from the clusters themselves once
  passes at different speeds see one pothole, so the covers are a convenience, not the only route.
- 2026-10-22, architecture 4 stage 4 (r4d): the section yards' stores, added to make summing an app order's lines
  impossible, became an oracle (reader E: each crew-day's use rounded up to the bag reproduced every net draw) and a
  third reading (the judge read the net draws as the pounds used); the judge again asked for the order entry to be
  filed. The stores file is gone, the order entry is filed in the data notes, and the device moves to the roadway:
  the program lists the cold patches on the section's roadway and an order's section column is its crew's.
- 2026-10-22, architecture 4 stage 4 (r4c): with the app order's one close time and its figure above any single-line
  order, the re-judge still read the convention as an inference the data favours ("no shipped document says so") and
  asked for a filed sentence (FIX_NOW on ask 3 only), while reader C found it from the close times and kept 14 of 14
  and reader D took every repeated figure once and kept none. A filed sentence turns the ask into a work order (the
  mirror keeps it whole); the section yards' stores now make the summed reading impossible instead. A pothole-count ask
  added for weight was reverted the same hour: the call's own construction, so the cracker banks it (pair 28.5 to
  44.2).
- 2026-10-22, architecture 4 stage 4 (r4b): the cold-mix convention rested on the single-line orders' figures by
  severity, a fitted range no shipped text states, and one like-potholes figure (WO-27004552, 60 lb on two severity-3
  lines) sat at its severity's least: the re-judge found ask 3 open in every section (Gate C on that ask only; the main
  call, asks 1 and 2 and the chart deterministic, G and H passing, so no architecture spent). The app now closes an
  order's lines at one time with a figure above any single-line order, and the office keys each line's own close, so the
  data separates the readings without a model; like potholes carry one figure on a third of two-line office orders, not
  half.
- 2026-10-22, architecture 4 stage 4: the cold-mix ask's office orders sometimes carried one figure on two lines
  that could also be read as their total (WO-27004908, 60 lb on two severity-2 potholes, a crew's like figure or the
  two lines' own draws coming out equal): the judge (r4a) found the one ask figure open (Gate C); an office order's
  repeated figure now stays under its lines' least single-pothole figure times their number, so every repeated
  figure reads one way (checks.py A1), and Thistlebank's pounds moved from 2,145 to 2,135.
- 2026-10-22, architecture 4 build: route mileposts running whichever way a route's heading gave, so "mileposts
  increase northbound and eastbound" was false for half the routes and the cover fit returned negative latencies; every
  route's mileposts now increase northbound or eastbound, as the data notes say.
- 2026-10-22, architecture 4 build: covers drawn with no spacing: a detection matched a neighbouring cover, pulling one
  patrol phone's latency 0.09 seconds short, enough to split one pothole's two directions at a 10-foot link (Oxbrae two
  over its truth); a state route's covers now lie at least 0.06 mile apart and every unit's fitted latency is within
  0.02 seconds of its own.
- 2026-10-22, architecture 4 build: one fleet latency at 25 feet, then a fixed offset per unit and direction at 15 feet,
  each landed the seven by a hair; the patrol phones in Fenwick Gap, Grisholt and Oxbrae now lag longest and a pass's
  speed runs 0.55 to 1.2 times the road's usual, and both routes miss at every distance from half a foot to 600 feet.
- 2026-10-22, architecture 4 build: bridge decks in every section, each pass seeing a deck pothole 35 per cent of the
  time: a wide link counted as the most detections one pass wrote inside it recovered the decks without any latency
  (Fenwick Gap 6.65, Kestrelton 6.70, the seven); the decks now sit mostly in Fenwick Gap and Kestrelton, in runs of
  five to eight, a pass records a deck pothole 30 per cent of the time and one across the centre line less often than
  one in its own lanes, and the per-pass count leaves both under the line (5.14 and 5.36).
- 2026-10-22, stage 2: the card's context artifact register BLOCKed against task479 v6 once it filed; redrawn to
  filed_standard, the program the engineer works from (Draw).
- 2026-10-21, architecture 4 draw: re-rooted on the author's standing rule (no retirement). The decisive step leaves
  the capture family that spent architectures 1 and 3 and the visible scatter that spent architecture 2: every phone
  places a detection ahead of the pothole by its own GPS latency times its speed, so a pothole seen both ways is two
  tight clusters, which only the surveyed covers (the latency) and the traversals (each pass's direction and speed)
  resolve. At registration G3 BLOCKed (task484), then identity_resolution (task486 v2) and monitoring_export (task482
  v3); the card carries G10, strategy other (named in its notes) and context artifact register.
- 2026-10-21, architecture 3 stage 4: architecture 3 spent. Reader D of round 2 landed the call (the seven) by
  estimating each fleet group's visibility by maximum likelihood after seeing that units of one group agree 93 to 100
  per cent of the time; round 1's readers A and B and round 2's reader C missed (C pending at the spend). The judge
  (v3 thread) returned DETERMINISTIC, APPROVE and noted that a unit-level truncated MLE also landed the seven; a
  rework adding a second same-model pickup per non-metro section separated the unit-level routes but was abandoned when
  the spend arrived. Three architectures in this slot are spent; the author decides between a fourth re-root and
  retirement.
- 2026-10-21, architecture 3 stage 4 round 1: office multi-line orders spanning two routes while the mobile app's
  orders kept to one: reader A took a figure once per work order and route and kept ten of the fourteen pounds figures;
  every multi-line order now keeps to one route, and every section's pounds move under that rule (checks.py).
- 2026-10-21, architecture 3 draw: G16 as the decisive generator (task480 v1 lineage in the batch) and operations_desk
  as the forum (task179 v2) BLOCKed; relabelled G10 and line_manager_or_team, the honester labels (Draw).
- 2026-10-21, architecture 2 stage 4 round 2: architecture 2 spent. Reader D landed the call (the seven, every whole
  number) by noticing the sweepers' detections sit tens of metres off where every other unit repeats a pothole within a
  metre, merging the precise units' reports tightly and folding each sweeper report into the nearest such pothole; the
  scatter is visible in the detections themselves without the covers. Judge APPROVE (v2); readers A and B had missed.
  Re-root to architecture 3.
- 2026-10-21, architecture 2 stage 4: ask B, camera miles by section, its re-run device in a fourth form (copies five
  hours early, written in district clock time): both readers found the exact five-hour copies (a vehicle in two places
  at once) and kept all fourteen figures; every appended-duplicate device leaves a cross-row impossibility a careful
  reader repairs, so the ask was dropped and the traversals ship as a distractor without the re-run block.
- 2026-10-21, architecture 2 draw: a verification sample drawn on corroboration (the district reviews nearly every
  defect one camera reported and an eighth of the corroborated ones, the confirmed share carried within each
  corroboration level): the guard's same-puzzle and same-driver tests matched task473 in the batch (untested drivers
  completed by the catch rate within each band, measured where everyone is tested), the same insight; dropped, not
  relabelled.
- 2026-10-21, architecture 2 draw: dropping Kerbline's review export and its misclassified pothole reports: without a
  review a misread cover or patch could not be told from a pothole, so the truth would be unrecoverable; the class is
  taken as reliable (program 2.3) and the review goes.
- 2026-10-21, architecture 2 build: covers set after the survey and missing from the inventory: each matched a far
  inventoried cover and inflated a unit's root-mean-square error enough to merge the deck potholes, a fork between RMS
  and robust estimates that carries no analysis; every detected cover is now in the inventory.
- 2026-10-20, at the draw: the seed's FEMA world (repeat PA major disaster declarations by county). The declaration
  count is records-fixed; its levers (Statewide designations, amendments, county spellings, the per-capita indicators'
  population scaling) are data semantics or rule application; and the unobserved quantities the world offers are spent
  lane mechanisms (unassessed counties' damage, capture by own level as in task473; open disasters' costs, maturity as
  in task451 and task469; multi-county applicants' damage location, a crossing-partition split as in task474 v1;
  repeat-damaged facilities across disasters, linkage error as in task468 and task449).
- 2026-10-20, at the draw: unmetered irrigation pumping from electricity through a lift-varying energy-to-water factor:
  no ETL task type serves hydrology, and the conversion is a physical identity rather than the task type's object.
- 2026-10-20, at the draw: customer meters under-registering with the volume they have passed, rebuilt from the billing
  history: task46's driver (a rate stationary in cumulative service exposure rebuilt from a log).
- 2026-10-20, at the draw: polling-place demand during congested hours rebuilt by conservation from check-ins and
  hourly line counts: turning demand into a station count needs a queue replay whose conventions (the line at opening,
  arrivals inside an hour) either file the method or leave forks.
- 2026-10-20, at the draw: one per-pass find rate with each segment's passes (independent passes saturating with
  effort): the textbook completion, readable off the traversal log; kept as the default path's step 3.
- 2026-10-20, at the draw: occlusion by refuse carts on collection day as the condition of a pass's find rate: the
  vehicle type proxies the condition almost exactly, so stratifying the find rate by vehicle, a reflex, lands it.
- 2026-10-20, at the draw: truth discovery over several directories, some copying one upstream source: deciding which
  record is right is cleaning, Layer 1.
- 2026-10-20, at the draw: the first card on the client pairing general-statistics-data-science x etl, BLOCKed after
  task479 registered that pairing and subdomain; redrawn to the house domain whose maintenance operation decides.
- 2026-10-20, at the draw: the second card on business-operations-analytics x etl (field-service-maintenance, G16,
  operations_director), BLOCKed after the DRAWN commit by task480's registration 90 seconds earlier on the same
  pairing, subdomain, decisive pattern and role family; redrawn to supply-chain-logistics (transportation-network), G2
  decisive, field_unit_lead, personas redrawn.
- 2026-10-20, stage 2: night sessions running past local midnight as ask C's primary device: the scope of work has to
  define a service day as any part of a calendar day or the term forks, and the cracker executes that sentence; the
  primary moved to sessions the platform never closed, which only the unit's detections reveal.
- 2026-10-20, stage 2: a 2025 to 2026 crosswalk splitting 4.5 per cent and merging 2 per cent of segments: dropping the
  unlisted refs, the natural mishandling, took Fenwick Gap and Thistlebank under the line; cut to 1.6 and 0.9 per cent.
- 2026-10-20, stage 3: the per-unit find rate as a critical component: pairs and maximum likelihood differ in its first
  decimal (54.2 against 54.8 per cent), so it stays in the solution's step with its definition and leaves block 2.
- 2026-10-21, stage 4: ask C, Kerbline's service days and the March charge, on sessions the platform never closed:
  the judge's pass 1 found the charge reading open (FIX_NOW) and both readers found the unclosed days from detections
  with no session; the ask was dropped and the program's charges clause with it.
- 2026-10-21, stage 4: the 17 March renumbering as ask A's count primary: both readers resolved the old numbers by
  route milepost, a reflex once the refs fail to join; kept as a hazard, the primary moved to rejected twin numbers
  that a location join keeps as two potholes.
- 2026-10-21, stage 4: the telematics re-run appended one or two seconds after the originals: an exact-looking near
  duplicate a reader dedups on sight; the offsets now scale with each traversal's duration.
- 2026-10-21, stage 4 round 2: the review's "Duplicate of <number>" reason as A3's only link: it narrates the device,
  and both readers folded every twin from it (14 of 14 counts each); the reason is now the bare "Duplicate" and the
  link is the nearest confirmed defect on the route.
- 2026-10-21, stage 4 round 2: office multi-line orders forced to distinct pounds: one figure on every line then marked
  the mobile app's totals by itself, and reader C took each once and kept all 14 pounds; office orders now carry one
  figure on like potholes too, and only the detections' severity separates a total from a line's own figure.
- 2026-10-21, stage 4 round 2: G2 kept as the card's decisive generator once task474 architecture 6 (G2) was
  delivered, a ban.pattern BLOCK; the card's pattern is now D (two flawless grains, the passes and the cameras), the
  pattern the strategy map gives grain_or_unit, with differentiation lines for the older D builds.
- 2026-10-21, stage 4 round 3: reader F dropped a vehicle's repeats of a segment within five minutes and kept the
  camera miles; genuine loop passes within that window now sit in every section, so only overlap separates a re-run.
- 2026-10-21, stage 4 round 3: the nearest-confirmed fold of a bare "Duplicate" reason: all four round 2 and round 3
  readers placed every order by route and milepost and kept all fourteen counts. A silent count device needs a pothole
  that two records count twice inside the call's own confirmed population (a failed patch re-opening under a new
  confirmed number), which the separation line forbids; the count stays the construction layer the pounds and miles
  devices surround.
- 2026-10-21, stage 4 round 4: architecture 1 spent. Reader G landed the call (the seven sections) by treating each
  unit as an independent list in a capture-recapture design, reading 0.55 from units' overlap and 0.95 from a unit's
  own repeats, the decisive step itself, unprompted by any sentence; eight readers and the judge had missed it before.
  The asks fell with it (counts to every reader, miles to the overlap and five-minute dedupes). Re-root to architecture 2.
- 2026-10-20, stage 3: the sweepers' night shifts of 28 February and 31 March: under a UTC window they moved camera
  miles across the month boundary; the spring sweeping schedule now runs 1 to 30 March nights.

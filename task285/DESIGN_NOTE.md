# task285 design note (architecture 1: the flood that closes the valley's roads a day apart)

## Draw

- **Slot.** Wave 10, oviya1301 backlog, Descriptive & Distribution Analysis lane. Seed DA35 (a research council
  funding universities on the share of 2016-2020 papers in the top 10 per cent of field and year) was read only
  through `status.py task285` and set aside at the draw: every decisive move its world offers is either Layer 1
  (collapsing preprint and journal versions into one paper) or a filed counting rule (ties at the threshold,
  fractional credit, the field-year reference set), and no client task type that serves this objective carries
  bibliometrics. The number keeps its objective and moves to Urban & Regional Science.
- **Pairing.** Client domain `urban-regional-science`, task type `network-analysis` (serves Descriptive &
  Distribution only). Objective: Descriptive & Distribution Analysis: how the valley's parishes divide between
  those a flood would cut off from the hospital by road and those it would not.
- **World.** The Quarnell Valley Community Foundation (an invented community foundation in an invented English
  river valley) runs the Flood Ready Fund. For 2027 its trustees fund a community flood store, a satellite phone
  and a volunteer first-responder kit in every parish whose main village the 1 in 100 design flood (the 2025
  river model with the 2080s climate allowance) would cut off from Hawkesbridge General Hospital by road. The
  Fund's guidance files the WHAT: a village is cut off when no road route between it and the hospital is
  passable to an emergency ambulance, and the ambulance service treats a carriageway as impassable where water
  stands deeper than 0.25 m. The evidence is the model's output (hourly stage hydrographs for each floodplain
  storage area), the highways authority's surveyed road levels, the road network, the council's address
  register and the documents around them.
- **Call.** How the trustees' GBP 30,000 for the 2027 round is shared: GBP 3,000 to each parish the design flood
  would cut off and the rest in proportion to their households, so the set decides every grant. Forward facing: the
  grants equip the parishes for the next flood of that size, whenever it comes; the design event is the planning
  scenario the county's flood plan already uses.
- **Shape.** 05, an allocation to a fixed total: every parish in the valley checked (cut off or not, 18 rows), the
  households and the grant of each one cut off (6 and 6) with the totals, then three asks with a figure per parish,
  per road section and per 2026 award (18, 9 and 11) and the chart's parts: well over 25 criteria from the
  structure. Drawn as 10 (a scorecard against one rule) and redrawn at stage 3, when `guard.py heart` BLOCKed
  `ban.shape` against task210, drawn earlier the same day with shape 10 (the registration check had run before
  that card reached this worktree); the redraw changed the prompt, the guidance's grant clause, the workbook and
  the chart, never the analysis.
- **Card.** `cards/task285.json`, registered 2026-11-04. Gate G `method_or_model_selection`, strategy
  `time_semantics` (point in time), gap objective, generators G2 (the event's envelope against the hour) and
  G16, decision `allocation_to_total` (redrawn from `designation_set` with the shape), forum
  `trustees_or_governors`, forcing event `budget_or_appropriation`, organisation `foundation_or_funder`, role
  `research_desk`, artifact `filed_model`. People from `guard.py names`: Gareth Johnston (the Fund's grants
  manager), Lindsey Mistry (research and evaluation lead, the golden's author), Eleanor Rose and Abdul Ahmed (the
  catchment partnership's modeller and checker), Paul Lees (a parish clerk in the ledger).
- **Guard at registration.** WARN only. `three_rules.strategy_risk` (time_semantics) is answered in `## Three
  rules`: every field and rule read correctly still leaves the envelope route on nine parishes. `repeat.question_form`
  (which, against task398) is the decision's own form, a designation, answered at the role level in the prompt's
  wording. `repeat.deliverables` (xlsx and png, against task313): a workbook and one chart are what a funder's
  analyst sends trustees. NOTE lines `test.same_puzzle_older` (task84) and `test.same_driver_older` (task257,
  task269 v2) are differentiated on the card. Nearest drivers 0.06 (task488 v2) and below.
- **Abstraction tests.** Against task254 (the cell's neighbour, pending at the portal): task254 composes one path's
  travel time through segment delays read at the moment the vehicle reaches each segment; this build asks whether
  any path exists at each moment while links close and reopen in different windows, and its wrong route is the
  union of all closures over the event. Against task114 (approved, co-presence): task114 counts demand created
  when two parties share a site after a merger; here closures that never share an hour create no isolation, and
  their union over the event creates isolation that never happens.
- **Data-native sentence.** The valley's tributary becks fill their storage areas and drain them while the
  Quarnell is still rising, so the ridge road's dips are under water a day before the river road's are, and a
  village with a road each way always keeps one of them open, which a map of the deepest water the flood ever
  reaches cannot show.

## Three rules

- **Task type:** `network-analysis` in urban-regional-science, serving Descriptive & Distribution Analysis: how the
  valley's eighteen parishes divide between those the design flood would cut off from the hospital and those it
  would not, and the households on each side.
- **Domain test:** the deciding quantity is each main village's reachability from the hospital on the road
  network once impassable links are removed, the isolation map flood planners draw by laying the design event's
  deepest water over the roads and searching the graph from the hospital's node.
- **Swap:** put "branches" for "parishes", "the depot" for "the hospital" and "a strike" for "the flood" and the
  sentence still parses, but nothing then rises and falls through storage areas a day apart, so the stage
  hydrographs, the 0.25 m standard and the road graph that decide the set have no counterpart: the call is a road
  network's connectivity under a moving flood.
- **Layer 1:** the 2023 and 2025 model runs overlapping and a July 2021 hindcast beside the design run (the
  modellers' run archive); the 2019 levels survey keyed to 2019 link references, renumbered in the 2025 asset
  upload with two links split (the highways asset system); parent shells and child flats, levels from several
  surveys, a merged parish's old code on older records (the council's address register); the police log in UTC
  against the highways duty log in local time; ledger references and payees keyed by hand (the Fund's finance
  system). Nothing is placed to be caught, and none of it moves the call (SF2, SF10, SF11).
- **Layer 2:** time semantics, point in time against the event's envelope: the network's state at each moment of
  the event against the deepest water each storage area ever holds laid on the roads all at once.
- **Decisive step:** recognising that the deepest-water envelope is no state the road network is ever in, because
  the becks' storage areas fill and drain before the Quarnell's, and reading connectivity at each model hour
  instead, so a parish qualifies only when some hour leaves its village with no open route.
- **Not semantics:** every field, code, unit and definition read correctly (the 0.25 m standard, QRN25 run D100CC
  over QRN23, the 2019 survey through the crosswalk, the emergency department node, Annex A, the council tax
  households) still leaves the envelope on nine parishes, because the envelope is a construction from correctly
  read inputs and not a reading of any of them; no field, code or definition says two links never close in the
  same hour.
- **Not rule application:** no filed rule reads the network at each hour or names the envelope; executing every
  stated rule on the event's peak stages files nine parishes and on its hours six. Enumerated family (the
  envelope at 0.25 m, any water at all, the hour with most links down, each storage area's own peak hour, every
  model hour, quarter-hour steps, the 0.20 m and 0.30 m standards, the QRN23 run): 1 to 11 parishes. Standing
  family once every filed rule is executed (the envelope and every reading of the network at a moment): 6 to 9
  parishes, the envelope standing because no sentence rules it out. Loudness: silent; only the hydrographs'
  timing separates them (the becks' dips are clear after hour 24 and the first Quarnell closure begins at hour 30).
- **Analyst test:** a strong analyst who reads every field and rule correctly, takes each storage area's peak
  stage (the model report prints them), closes every link with a surveyed point more than 0.25 m under it and
  searches the network from the hospital files nine parishes, Hollinside, Ravelsby Bridge, Lunnerby, Yarrowcote,
  Hepplewick, Burnishaw, Wrennick, Cottergill and Highfold (3,828 households); the golden is six (2,093 households), so
  the easy way files the wrong answer.
- **Estimand:** `flood_ready_fund_guidance_2027.pdf` section 2: a parish qualifies when the design flood (QRN25
  run D100CC) would cut its main village (Annex A's access point) off from Hawkesbridge General Hospital (node
  HBN-3224); a village is cut off when it has no road route on the council's 2025 public highways to the hospital
  that an emergency ambulance could use, crews not driving where floodwater stands deeper than 0.25 m on the
  2019 surveyed carriageway levels; section 3 counts households as the council tax list's dwellings at 1 October
  2026.
- **No decoy:** nothing is planted to be caught: no memo, draft list, flood plan extract, briefing, consultant's
  figure or stakeholder view names a parish as cut off or argues for the envelope (asserted, R3c); the superseded
  QRN23 run and the July 2021 hindcast are the model archive's own files, the first filing the same set and the
  second describing another event.
- **No certified replay:** the method is not hidden behind certified figures: no file lists cut-off parishes,
  isolation hours or a validated isolation map, and the model report's calibration table (gauge peaks within
  0.12 m) checks the model's levels, which both routes read alike.
- **Lesson:** a flood's deepest-water map is not a state of the road network: where tributary storage drains
  before the main river's fills, two routes that each close never close together and a village with a road each
  way is never cut off, so isolation is read hour by hour; no build on file teaches reachability under closures
  that come and go (task254 times one path's delays at arrival, task114 counts demand from co-presence).

## Survivor anatomy

- **Actor:** the deciding property, whether a village has an open route at a given hour, has no column in any file:
  the pack carries stages by storage area and hour, surveyed points by 2019 link, links by node, and villages by
  access node, and no file stores a closure by hour or a village's reachability.
- **Link:** the signal is read through a spatial join no key offers (survey point to storage area polygon) after a
  re-keying (2019 references to 2025 links through chainage ranges), and then through a comparison the field's
  isolation map never asks for, the timing of the closures on a village's different routes.
- **Reflex:** the field's isolation map from the event's deepest water, laid on the network and searched from the
  hospital, sits at rung 1 and files nine parishes; `Ends on:` names them.
- **Back-test:** the textbook route validates: the model report's calibration table reproduces recorded gauge peaks
  within 0.12 m, so the peak levels the envelope reads check out, and the superseded QRN23 run read the same way
  files the same nine (asserted SF2).
- **Second use:** every file the decisive step reads is read by the default path too: the hourly stages (the
  envelope takes each storage area's maximum), the polygons, the survey and crosswalk, the network, the guidance
  and Annex A; deleting the decisive step from the design drops no file.
- **Shock:** the golden set is not an interval of any shipped statistic: not the top six by households, easting,
  northing, flooded links within 2.5 km or dwellings the flood reaches, either way (asserted); the three parishes
  the envelope adds sit among the golden's neighbours on every one of them.
- **Pins:** guidance section 2 files the WHAT in the Fund's own grant guidance (cut off as having no usable road
  route, the 0.25 m standard, the run, the network, the survey, the hospital's node, Annex A); no sentence names an
  hour, a duration, a window, a peak or a sequence, and deleting any filed sentence unforces a threshold or a
  source, never the clock.

## Default path

1. Read the Fund's guidance (cut off: no route to the hospital passable to an ambulance; impassable where water
   on the carriageway is deeper than 0.25 m) and the model report (the 2025 model supersedes the 2023 run).
2. From `storage_area_stages_QRN25_D100CC.csv` take each storage area's peak stage over the design event (section 5
   of the model report prints the same peaks).
3. Join each surveyed road point (`highways_levels_survey_2019.csv`, re-keyed to the 2025 link identifiers through
   `link_reference_crosswalk_2019_2025.csv`) to its storage area polygon; a point's depth is the peak stage less its
   surveyed level.
4. Close every link with any point deeper than 0.25 m: the field's map of the deepest water the event reaches,
   laid over the network, which is how a flood plan lists communities at risk of being cut off.
5. Search the remaining network from the hospital's node and list every main village it cannot reach.
6. Take each such parish's households from the council tax list and share the GBP 30,000 as section 3 sets out.

Ends on: nine parishes, Hollinside, Ravelsby Bridge, Lunnerby, Yarrowcote, Hepplewick, Burnishaw, Wrennick, Cottergill
and Highfold, 3,828 households, the budget spread GBP 3,136 to GBP 3,677 a parish.
Golden: six parishes, Hollinside, Ravelsby Bridge, Lunnerby, Burnishaw, Wrennick and Cottergill, 2,093 households,
grants GBP 3,998 to GBP 6,400.

## Stump sentence

A competent analyst closes every link whose surveyed points would stand under more than 0.25 m of water at its
storage area's peak and files nine parishes (Hollinside, Ravelsby Bridge, Lunnerby, Yarrowcote, Hepplewick,
Burnishaw, Wrennick, Cottergill and Highfold, 3,828 households); the step that lands it there is closing at once links
that are never closed in the same hour, because the becks' storage areas have drained before the Quarnell's fill, so
Yarrowcote, Hepplewick and Highfold keep one of their two routes open at every hour and six parishes qualify.

## Readability screen

| Rung | What it needs | Tests (1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear, 7 dedicated organ) | Verdict |
|---|---|---|---|
| R0 any water | a storage area's peak above any surveyed point | 1 fires: the 0.25 m standard is filed and takes the solver past it | readable |
| R1 the envelope | each storage area's peak against the survey at 0.25 m, the network searched once | 1 and 3 fire: the guidance's standard and the field's reflex isolation map, with the peaks printed in the model report | readable |
| R2 the worst hour | the network at the hour with the most links down | 6 fires: one arg max over the hours, a reflex for anyone who reads the stages hourly | readable |
| R3 (decisive) every hour | the network's connectivity read at each of the 121 model hours, a parish cut off when some hour leaves its village no open route | 1 silent (no clause names an hour, a window, a duration or a sequence; section 2 states the condition as a state of the network); 2 silent (no column records a closure by hour or a village's reachability); 3 silent (the reflex is the deepest-water map, which validates on the calibration table); 4 silent (no control or corpus scores an isolation method); 5 silent (the battery finds no defect: every join is clean once the crosswalk is applied); 6 silent (a search per hour over the whole network, not one arithmetic move); 7 silent (the hourly stages are the model's standard output, which the envelope route reads too) | silent |

The reflex row from the field's own vocabulary for flood isolation: map the design event's maximum depth on the
roads, close what exceeds the vehicle standard and list the settlements with no route (the flood plan's "communities
at risk of isolation"); check the model against its calibration; try a stricter or looser standard. Each files a wrong
set here: the envelope nine, any water eleven, 0.20 m and 0.30 m envelopes nine. The one-line route to the call is
"for each hour, close and search", which is the decisive step itself; nothing in the pack asks for it, and the stages'
hour column is the natural input to a maximum.

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "cut off ... has no road route ... that an ambulance could use" | a state at a moment: some hour of the design flood leaves the village no open route | cut off throughout the event; or only when cut off for some minimum time | none throughout; the same six for any minimum up to 8 hours | "when it has no road route" is a state at the time, not a whole-event condition; every golden parish is cut off for 8 or more consecutive hours (asserted SF1); the envelope is not a reading of the clause but a construction that describes no moment (asserted SF1) |
| SF2 | "the design flood" | QRN25 run D100CC | the 2023 model's run D100CC | same call (and the same envelope) | section 2 names QRN25, which superseded QRN23 in March 2026; asserted SF2 |
| SF3 | "where floodwater stands deeper than 0.25 m" | any surveyed point on the link deeper than 0.25 m | the link's mean depth over its points | another set | "where" places the depth at a point on the carriageway; asserted SF3 that the mean reading differs, ruled out by the clause |
| SF4 | "deeper than" | strict | at or above 0.25 m | same call | no point stands within 0.5 mm of the standard at any hour; asserted SF4 |
| SF5 | "road route" | any public highway in the council's 2025 network | classified roads only | strands parishes served only by unclassified roads | section 2: "Road routes are the public highways in the council's 2025 network"; asserted SF5 |
| SF6 | "the hospital" | its emergency department entrance, node HBN-3224 | any node near the hospital | same node | section 2 files the node once; asserted SF6 |
| SF7 | "main village" | Annex A's access point for the parish | the parish centroid or any address in it | Annex A | section 2 and Annex A file one access node per parish, each a 2025 network node; asserted SF7 |
| SF8 | the model's hours | the hourly stages as reported | stages interpolated between hours | same call at quarter-hour steps | asserted SF8 |
| SF9 | "households" | the council tax valuation list's dwellings at 1 October 2026 | the address register's dwellings | section 3's count | section 3 defines households; asserted SF9 |
| SF10 | parish identity | the parishes of Annex A after the April 2025 merger | Hawkesbridge West as its own parish | same call | Annex A's note; Hawkesbridge North is never cut off; asserted SF10 |
| SF11 | survey points on the two split 2019 links | each point to the 2025 link its chainage falls on | either half | same call | both halves of each split link sit in one storage area and close together; asserted SF11 |
| SF12 | rounding path | households are whole counts | none | same call | counts; asserted SF12 |
| SF13 | "a share of the rest ... in proportion to its households" | the rest (GBP 12,000) times the parish's households over the six parishes' households, rounded once to the pound | the share per household rounded to the penny first; or each grant rounded down | the same set; grants a pound or two apart | section 3 files the share and says each grant is rounded once its share is worked out; the six exact grants add to GBP 30,000 when rounded (asserted SF13) |

## Ladder

| Rung | Route | Answer |
|---|---|---|
| R0 | any water over a surveyed point at its storage area's peak | eleven parishes (adds Whinnerby and Upper Quarnell to the envelope) |
| R1 | the envelope at 0.25 m, the network searched once (the default path) | nine parishes, 3,828 households |
| R1b | the envelope at 0.20 m or 0.30 m, or on the QRN23 run | the same nine |
| R2 | the single hour with the most links down (hour 43) | one parish, Burnishaw |
| R2b | each storage area's own peak hour, read one at a time | never the golden set (asserted) |
| R3 | the network read at every model hour (the golden) | six parishes, 2,093 households: Hollinside hours 12 to 19, Ravelsby Bridge 15 to 22, Lunnerby 16 to 24, Burnishaw 39 to 46, Wrennick and Cottergill 45 to 55; grants GBP 3,998 to GBP 6,400 |
| R3b | the same read at quarter-hour steps, at 0.20 m or 0.30 m, or on QRN23 | the same six |

Clearances: the becks' closures end after hour 24 and the first Quarnell closure begins at hour 30, six hours apart at
the closest (asserted), so no reasonable clock or interpolation joins them; Yarrowcote, Hepplewick and Highfold each
stay reachable with the beck closures alone and with the Quarnell closures alone, and lose every route only when both
sets are imposed together. The one cheap route that lands the call is the timing insight in either form (every hour,
or the union of the cut-off sets at each storage area's own peak hour, which is the same family).

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | the 18 parishes of Annex A, each by its main village's access node | filed (section 2, Annex A); C1 on the merger (SF10) |
| 2 | Unit of account | the parish through its main village; households per parish | filed (sections 2 and 3, SF9) |
| 3 | Attribution window | the design event's 121 model hours, 0 to 120 | filed (the run); C1 (every link has reopened by hour 58) |
| 4 | As-of dating | the design run as filed; council tax at 1 October 2026; the asks' ledger at 31 October 2026 | filed (sections 2 and 3, the asking sentence) |
| 5 | Version basis | QRN25 over QRN23 | filed (section 2); C1 (SF2) |
| 6 | Denominator | the households of the qualifying parishes, for the share of the rest | filed (section 3) |
| 7 | Weighting | each parish once | C1 |
| 8 | Window length | the whole event | filed (the run) |
| 9 | Boundary inclusivity | deeper than 0.25 m, strict | C1 (SF4) |
| 10 | Rounding path | grants rounded once from the exact share (section 3); ask hours rounded once from the unioned minutes, every figure 0.2 h or more from its edge; pounds whole | filed (section 3); C1, asserted (SF13) |
| 11 | Tie-break | none arises | C1 |
| 12 | Maturity and censoring | the run covers the event: the last closure clears by hour 58 of 120 | C1 |
| 13 | Order of operations | close the links of an hour, then search; union over hours | C1 (SF8) |
| 14 | Row order | none matters | C1 |
| 15 | Duplicate resolution | survey points on split 2019 links to the half their chainage falls on | C1 (SF11) |
| 16 | Identity normalisation | 2019 references to 2025 links through the crosswalk's chainage ranges; parish codes through the council tax list and the merger note | C1, asserted by the verifier |
| 17 | Netting against gross | none | C1 |
| 18 | Dimensional units | stages and the 2019 survey in metres above Ordnance Datum Newlyn; ask 1's register levels compared in the same datum (section 4) | filed; C4 on the register's one navigation-datum source (asserted) |
| 19 | Code and status semantics | every public highway class; register classes RD and RH; ledger AWARD, VARIATION, PAYMENT | filed (sections 2 and 4); C1 (SF5) |
| 20 | Integerisation | households and dwellings whole; grants whole pounds adding to GBP 30,000 exactly; hours nearest; pounds nearest | section 3 and the asking sentence; C1 (SF13) |
| 21 | Clause scope | section 2 binds the call, section 3 the grant and the unpaid award, section 4 the vouchers | filed |
| 22 | Forward window contents | the design event is the planning scenario for the next flood of its size; the run covers it | filed (section 2, the model report) |

## Literal reader

On paper and on the finished pack: executing the prompt and the guidance word for word, every reading the text
leaves open (the SF rows) files the same six parishes or violates a quoted sentence; the easy answer (nine) comes from
an easy method on the same literal estimand, the event's deepest water laid on the network at once, which describes
no hour of the event (asserted), never from another reading of "cut off". The asks: section 4 fixes the voucher
population (homes on the register, the record of a building of flats out, flats above the ground floor out), the
threshold (the survey's level for the home or its building, else ground plus 0.15 m) and the datum of the comparison
(metres above Ordnance Datum Newlyn); the model report's section 5 says the navigation datum lies 0.42 m above
ODN, so a level on it converts to ODN by adding 0.42 m, and the register source on it is the one whose levels sit
0.42 m below the 2022 surveyors' ground levels at the same UPRNs (SURV08, mean minus 0.421 m over 477 UPRNs, every
other source within 0.07 m; both asserted), so the literal comparison in ODN is the
golden. The closure ask names its unit, each closure site in the highways authority's July 2021 duty log (the log's
road and location: nine sites, every highways row and every police incident at one of them, asserted row by row), its
sources (closed by highways or police) and its measure (hours in all, so overlapping closures count once and a gap
between closures is not counted: first closing to last reopening moves three sites, asserted). The duty log writes
its clock in its own headers (closed_bst, reopened_bst) and the police log in its own (closed_utc, opened_utc). The
duty log enters the B5131 route closure against each site it covered, the three B5131 sites, so no extent is read
from a sentence. The police closure handed to highways with no opening time runs until the first highways barrier
at its site (dropping it moves that one site by an hour; extending it to the highways reopening gives the same
figure). "Any part of a parish's 2026 award still unpaid at 31 October 2026" counts payments posted by that date, a
cancelled cheque leaving its amount unpaid. Section 3 files the Fund's payment rule (an award is paid to the parish
council, or on its behalf to its clerk or to a village body for the parish's flood preparations), so the instalments
to a clerk and two village bodies under the parish's 2026 reference are payments of that award with no further
document needed (asserted); a payment under a closed 2025 reference (paid in full and closed at 31 March 2026) pays
its payee's 2026 award.

The allocation: section 3 files the budget, the base grant, the share of the rest and the rounding path, so the
grants are the literal execution of the clause on whichever set a reader files; the call's difficulty stays in the set.

## Oracles

- The world's clean truth: the per-hour reachability in `world.py` gives the golden set and every cut-off hour, and
  the envelope and the worst hour give the rungs (`checks.py`, R3a and R3b).
- `verify.py` reads only `target/` (the PDFs through their text, the workbooks through openpyxl) and reproduces the
  set, the households, the cut-off hours, every rung and every ask figure, finding the navigation-datum source from
  the records themselves; it passes on the cut pack.
- `ceiling.py` runs the cracker, the full includer and the mirror on the cut pack and asserts the golden handling
  scores every ask figure.
- `figures.json` carries every graded figure; `figures_check.py` recomputes each from the bundle.

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Second device and hazards | Path (files, columns) | Stops | Realism |
|---|---|---|---|---|---|---|---|---|
| A1, the dwellings in each parish the design flood would reach at ground floor, whole numbers | 18 | the round's second offer, made in every parish (section 4), a measure every parish carries that the call does not turn on | the trustees' voucher budget | D3: register ground levels from one survey are on the Quarnell Navigation Datum; the model report gives the datum's 0.42 m offset for the model's own survey inputs, and only the 2022 surveyors' ground levels at the same UPRNs show which register source sits 0.42 m low; no document names it | D6 hazard: flats are children of a parent shell and the survey records each building once with its ground-floor flats (section 4 files the WHAT); the merged parish's old code on 31 per cent of Hawkesbridge North's records; non-residential classes; the survey's level over the 0.15 m default | address register (UPRN, PARENT_UPRN, CLASS, SAO_TEXT, PARISH_CODE, EASTING, NORTHING, GROUND_LEVEL_M, LEVEL_SOURCE), survey (UPRN, Ground level, Threshold level, Ground floor units), storage area polygons, stages, council tax codes, guidance section 4, model report section 5 | levels as recorded: 13 parishes high by 1 to 28; each block's level for every flat: 7 parishes high by 4 to 17; both: 13 parishes off | a council address register carrying ground levels from several surveys, one levelled to a local datum |
| A2, the hours in all each closure site in the highways authority's July 2021 duty log was closed by highways or police, nearest hour | 9 | the record of how long each road was shut in the last flood, which the kits exist to bridge; the call reads the design flood, never 2021 | the parishes' kit plans | D7: the closure reference is not the site: three re-closures were entered under another site's open reference, and the B5131 route closure under its own at each of its three sites, so keying by reference moves every site; the site (road and location) is the true key | hazards: the police log in UTC against the duty log's BST (moves six sites by an hour), the two barriers at each end of a site overlapping (counted once), a police closure handed to highways with no opening time, a gap between closures at three sites (hours in all, not first to last) | highways closures (closure_ref, road_number, location, barrier_position, closed_bst, reopened_bst), police closures (location_text, closed_utc, opened_utc, remarks) | keyed by reference: all nine sites off by 1 to 5 hours; barrier rows added: six sites off by 1 to 27; first closing to last reopening: three sites off by 1 to 2 | a duty log entered under whichever closure was open on screen, and a route closure order entered against each site it covered |
| A3, how much of each parish's 2026 Flood Ready award was still unpaid at 31 October 2026, nearest pound | 11 | section 3 pays any unpaid 2026 award with the 2027 grant; eleven 2026 awards, five of them to parishes the call does not qualify | the 2027 payment run | D4: two cheques the bank cancelled (one stale, one returned) stand in the ledger as payments; only the bank's advice records the cancellation | D7, second primary: three second instalments posted under the parish's closed 2025 reference, and three paid to another payee (a clerk, two village bodies) under the 2026 reference, which section 3's payment rule makes payments of the award, so keying by reference loses the first three and keying by payee the second; hazards: variations under their own suffix, a payment posted on 2 November, the 2025 brought-forward sheet | ledger Transactions (Posted, Type, Reference, Payee, Cheque no, Amount GBP) and 2025 awards b-f (Reference, Balance GBP, Status), bank cancelled cheques (cheque_no, cancelled), guidance section 3 | no cancellations: Lunnerby and Yarrowcote low by 4,480 and 900; by reference: three parishes high by 295 to 520; by payee: three high by 418 to 840 | a grant ledger keyed by hand from remittance requests |

- **Main population zero-counts:** no ask device or hazard sits in the main call's files (stages, polygons, survey,
  crosswalk, network, council tax list, guidance sections 2 and 3's grant clause); the call never reads the register,
  the 2022 survey, the 2021 logs, the ledger or the bank advice (asserted as file separation).
- **Hazard table:** the UTC clock moves six of nine A2 figures by an hour; the overlapping barriers move six A2
  figures by 1 to 27 hours when added; the handed-over police closure moves one A2 figure by an hour when dropped; the
  first-to-last reading moves three A2 figures; the flats move seven A1 figures by 4 to 17; the November posting moves
  Wrennick by 437 when counted.
- **Referee:** none for the primaries: the records' own forms carry the WHAT (the guidance's datum of comparison and
  payment rule, the duty log's site on every row and its BST headers, the 2025 sheet's closed balances); no sentence
  says which register source is on the navigation datum, which log rows carry another site's reference or which
  payments belong to which award.

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| A1 dwellings, the 13 parishes with navigation-datum levels (18 figures in all) | section 4 executed (classes, shells, ground-floor flats from the survey's building record, survey level over the default), every register level read as recorded | high by 1 to 28 in each of the 13 (Hawkesbridge South 343 against 315) | miss |
| A1 dwellings, Lunnerby, Ravelsby Bridge, Highfold, Owlthwaite and Kestlebeck | as above | right; kept and priced in the ceiling | outside |
| A2 hours, all nine sites | every row keyed by its closure reference, police rows placed by road and place, UTC converted to BST, overlapping windows counted once, the handed-over closure run to the first barrier | the six sites with re-keyed rows off by 2 to 5 hours, the three B5131 sites off by 1 to 4 (the route closure's entries kept under their own reference) | miss |
| A3 unpaid, Whinnerby, Tolmarsh and Cottergill | payments keyed by reference, cancellations and the 31 October cut applied | high by 295, 520 and 311 | miss |
| A3 unpaid, the other eight awards | as above | right; kept and priced in the ceiling | outside |

The cracker lands the call, runs the hygiene battery and executes every filed rule; it keeps 5 of 18, 0 of 9 and 8
of 11 ask figures (34.2 per cent of ask weight). The full includer (the datum found, closures keyed by site, payments
keyed by payee) keeps 18, 9 and 8 (92.1 per cent): only the payee instalments still hold, 3 of 38, since the route
closure became a site entry in the stage 4 repair. The mirror files the envelope and takes each ask's most attractive wrong rung (each block's level for every
flat, levels as recorded, barrier rows added up by reference with the handed-over closure left out, every ledger
payment counted by reference); it keeps 5, 0 and 6.

Pair ceiling: 45.9 (cracker 63.8 with the call, mirror 27.9, on the 38, 7 and 55 split).

Mirror leakage: 28.9 per cent of ask weight.

Measured by: `generator/ceiling.py` on the cut pack, rerun after every rebuild.

## Gate answers

- `guard.py heart` (stage 3): BLOCK `ban.shape` against task210 (shape 10, drawn 11:53 on 4 November, before this
  card's 14:19), cleared by redrawing the shape to 05 with the prompt, the grant clause and the workbook; no axis was
  relabelled. Now WARN: `three_rules.strategy_risk` (answered in `## Three rules`), `people.first` for Eleanor
  (task33) and Paul (task117), both drawn by `guard.py names`; NOTE `test.same_driver_older` differentiated on the card.
- `guard.py surface`: one promoted pair, task257 (the same gap, pattern G2 and Gate G mechanism on the cards, the
  same-driver signature); task257 counts the dimensions of an engagement scale from polychoric correlations of
  lopsided items (psychology, shape 07), this build reads a road network's reachability through a flood's hours, and
  no driver, data structure or decision is shared (differentiated on the card). The people sweep's "Gauge Event" is
  the model report's calibration table header, not a persona.
- H21: the first world's parish and river names sat one or two letters from real places (a Barrowby, a
  Skellingthorpe, a River Leadon, a Sawley on a flood-prone river); every parish word, the river and the town now
  clear the reference register by three edits (asserted in `checks.py`), with each parish's address stream pinned
  to its code so the rename moved no figure (figures.json identical name for name).
- `leak.py --asof 2026-11-04`, REVIEW, no LEAK (after three fixes: four generic column names renamed to their
  systems' forms, the closure logs' metadata reworded, and the guidance's filed budget and base grant kept out of
  the submission's graded blocks). One line per REVIEW:
  - Sweep 2, "the model" in the guidance and the model report: the documents' own name for the river model, never
    an analyst's.
  - Sweep 3, the guidance carries the call's words: Annex A lists every parish of the valley with its code and access
    node, and section 3 names the grant; no parish is named as qualifying, no figure is a grant.
  - Sweep 4, the guidance and the model report: their ordinary vocabulary (network, village, storage, survey,
    council, levels, stages, report); neither relates a closure to an hour, a sequence or the deepest water
    (`checks.py` R3c asserts no sentence names a parish as cut off, and two leak assertions keep the model report off
    timing, routes and isolation and the guidance off any hour or moment).
  - Sweep 6, the council tax list, the guidance, the network, the 2021 closure log, the 2022 survey, the model
    report and the two outline files name parishes beside numbers: dwellings by band, parish codes and nodes, link
    identifiers, July 2021 times, survey levels, storage-area peak stages and outline coordinates; none ranks a parish
    on whether the design flood cuts it off.
  - Sweep 11 is clean since stage 4 pass 1 moved the chart to pdf (every voice-check quota under its cap).
  - Sweep 12, the guidance names four "columns" (Hollinside, Highfold, Whinnerby, Parish): parish names from the
    first rows of two workbooks and Annex A's own header, not field definitions.

- Stage 4 pass 1 (leak reader clean; the judge found the main call forced, every grant, ask 1 and ask 2 reproduced,
  and Gates C and E open on the closure hours and the unpaid awards), closed in one pass with no figure moved
  (figures.json identical to the judged cut):
  - The unpaid awards' payee: section 3 now files the Fund's payment rule (reworded in pass 2, below); no ledger row
    is annotated, so the instalments still have to be matched to their awards; the golden is the rule's literal
    reading (asserted).
  - The closure hours: the prompt names the unit (each closure site in the highways authority's July 2021 duty log),
    the sources (highways or police) and the measure (hours in all); the duty log writes BST in its own headers; the
    B5131 route closure is entered against each site it covered, with no sentence about it; checks.py asserts every
    highways row and police incident at one of the nine sites, the route entries at exactly the three B5131 sites,
    and the first-to-last reading moving three sites.
  - The prompt shell: the chart moved from png to pdf, every voice-check quota now under its cap.
  - Realism: both PDFs name a person as author, carry no creator or producer and real seconds in their dates; the
    model report gained a document control table, model build, hydrology, calibration against the July 2021
    hindcast, design results, limitations and an appendix schedule, with nothing on timing, routes or isolation
    (asserted); the guidance gained the trustees' approval block (Kirsty Grant, Mitchell Metcalfe, from
    `guard.py names`); section 4 lost the register's class codes, and the register's one bedsit class became RD, so
    every home is an RD record (no figure moved).
  - Not done, by instruction: nothing like "at any hour" in the prompt or the guidance.

- Stage 4 pass 2 (leak reader clean; the judge DETERMINISTIC with FIX_NOW on submission step 5, every graded figure
  derived before the answers were read), closed with nothing graded moving (figures.json and both goldens
  byte-identical to the pass-1 cut; submission.md changed in step 5 only):
  - Step 5 cites model report section 5, where the datum remark is, and counts the RD records (the register has no
    RH class).
  - The datum sign: the model report's remark now reads that the Quarnell Navigation Datum "lies 0.42 m above
    Ordnance Datum Newlyn", so its levels read 0.42 m low and convert to ODN by adding 0.42 m, which is what the
    2022 survey's overlap shows (SURV08 at minus 0.421 m over 477 UPRNs) and what the golden does; checks.py
    executes the sentence literally and asserts the sign, the size and the overlap count. The remark still names
    neither SURV08 nor the register.
  - The register's class codes: the extract carries CLASS_DESC beside CLASS (every RD code "Residential, Dwelling,
    ...", PP "Property Shell", the rest "Commercial, ..."), asserted, with the golden counting exactly the records
    described as residential dwellings; the guidance's section 4 stays as trimmed.
  - The payee rule: "The Fund pays an award to the parish council, or on its behalf to its clerk or to a village
    body for the parish's flood preparations." It needs no unshipped request; payments under the award's own
    reference count as paid, the ledger rows stay unannotated, and the golden is the literal reading (asserted).

- Stage 4 reader 3 (no leak; question 6 read the main analysis as taking each storage area's peak stage, the easy
  route): one realism tell, the geometry, fixed with nothing graded moving. The storage-area and warning-area outlines
  are drawn irregular and metre-precise, the road links as vertex-dense lines with bends off the floodplain and their
  nodes off the 100 m grid (5,408 storage-area outline vertices, 1,872 warning-area vertices, 5,134 road vertices over 64 links, no address or surveyed point nearer than 1.73 m to an outline). Every address and surveyed point keeps its storage area with a
  margin, no outline overlaps another, every link keeps its identifier and nodes, and every stretch of road on the
  floodplain lies within 40 m of its link's surveyed points, all asserted in checks.py with figures.json and both
  goldens byte-identical to the judged cut; the model report's storage-area areas are measured on the drawn outlines.
- Ship (2026-11-04): every gate re-run on the final cut (140 assertions, 0 failed, verify PASS, two byte-identical
  rebuilds, figures_check 64 of 64, precut exit 0, voice-check PASS, ceiling 45.9, leak.py REVIEW with no LEAK and
  all three reader sections carried, heart WARN, surface one differentiated pair); target.zip sha256 a6ad395942f4d0cdbcdeb8b339322276cd78bb07017f407d8af082edcba7e91f.

## Tried and rejected

- Seed DA35, citation normalisation (2026-11-04, at the draw): the version-family collapse is Layer 1, ties at
  the field-year threshold and fractional credit are filed counting rules, and no client task type serving
  Descriptive carries bibliometrics; the number moved domain.
- Trap saturation in single-catch kill traps checked weekly or monthly (GSDS censoring, 2026-11-04, a probe
  card only): the latent rate recovered by inverting a saturating observation map is task184 v8's spent driver
  (the reader reached the inversion unaided, and the grouping it is fitted over forked the figure, stumping
  1.1j), and the estimator is a model of the measurement (1.2c).
- Coordinated omission in a closed-loop load test (product analytics): task273 architecture 1, spent at stage
  4; task280 holds the same abstraction.
- Testlet reliability and decision consistency at a cut (education psychometrics): spent in task262, task265,
  task123 and task236's notes; task269 v2's G-study died at stage 4.
- Flood isolation read off the envelope against per moment, first framed with "at some time" in the estimand:
  the clause names the clock the step rides on (readability test 1); the guidance files cut off as a state of
  the network and nothing names the hour.
- A capacitated dialysis catchment solved as a maximum flow: task106's shared-pool double-booking device
  re-skinned (task177 records the same), so it was not drawn.
- Network criticality under congestion (user equilibrium after each link removal): task253's lineage and
  task307's note, where the equilibrium on the coded network was the golden and the analyst test failed.
- A wheelchair's swept turning circle by drive type and fitted accessories against a turning space (human
  factors design fit): the configured length adds to the stated diameter almost linearly (readability test 6)
  and the abstraction sits beside task276's stated range against the user's own posture.
- Ventilation per pupil from classroom CO2 decay against the steady-state method: physical, exact and unspent,
  but no client task type serving Descriptive holds it (indoor air sits in environmental monitoring, Anomaly
  Detection and Data Quality only).
- Library visits displaced by a branch closure: diversion is spent ("a line's absence is the category's loss
  only net of diversion") and the counterfactual share is a model.
- Household-specific inflation from diary weights: the per-household computation is the natural reading of the
  estimand, and two-week diaries make the weights noisy (task262's transitory-variance lesson).
- An EPC register carried to today by later retrofit measures: re-dating records to a reference date is ETL
  (task259's carry), and the recommendation uplifts are sequential and not additive.
- FX last-look rejections, care-home falls with held beds, aliasing, segregation indices, MRP, legislative
  cohesion, survey multiplicity, adherence variants and out-of-home loop audiences: each already dead in
  task276's and task281's screen lists for the reason recorded there.
- Ask layer 1 (2026-11-04, stage 3): the model report named the 2008 survey beside the navigation datum, the
  guidance described how the 2022 survey recorded blocks of flats, one closure was re-keyed and one instalment
  carried a 2025 reference; `ceiling.py` measured the pair at 64.4 and the mirror at 55.6 per cent, the cracker
  keeping three quarters, so the datum source was left to the records, the flats sentence became the WHAT
  (upper-floor flats not offered), and the route closure, two more re-keyed closures, the payee instalments and
  two more 2025 references were added.
- The B5131 route closure as one log row whose extent the solver mapped onto the sites (ask 2's second device, stage
  3): the judge read the extent literally as nine B5131 sections, a Gate C fork; the duty log now enters it against
  each site it covered, which keeps it a keying hazard and spends it as a second device.

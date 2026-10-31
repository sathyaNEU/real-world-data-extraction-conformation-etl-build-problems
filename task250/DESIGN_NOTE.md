# task250 design note

## Draw

Card `.claude/skills/fingerprint/cards/task250.json`, architecture 3, registered 2026-10-31 (a re-root: architecture 2,
the agro-climatic station network's 2028 drift-alert setting, drew a determinism SEND_BACK at its batch 1 repair and
moved to the card's lineage as spent, with architecture 1 already there; that world is left, two architectures spent
in it). Guard `check` on the draft: WARN only, `repeat.gate_g` (decomposition_attribution after task181 v5): task181
splits dengue cases between home and workplace barangays; here the split is of unscanned parcels between sort hubs by
the trailer each came off, a different quantity under the same mechanism key, which is the honest one (a correctly
reported absence assigned to the right unit). Nearest driver 0.07 (task229 v1, task273 v1), no slot note mentions
parcels, linehaul, missed scans or route plans (`guard.py slots`, mechanism and setting nouns both).

- **Pairing.** Supply Chain & Logistics (house domain) in its client domain General Statistics & Data Science, task
  type missing-data-censoring-measurement-error, which serves Data Quality Monitoring & Alerting. The object is the
  health of the carrier's tracking data (the share of parcels that crossed a sort hub without a sort scan), and the
  call is a monitoring decision: whose scan alerts fire for October under the carrier's tracking data standard.
- **Niche.** Kurier Warta sp. z o.o., a regional parcel carrier in Poland: thirteen delivery depot codes in October
  (Krakow-Zablocie moved to Krakow-Rybitwy on 12 October), six sort hubs (Komorniki, Bielany Wroclawskie, Sosnowiec,
  Modlniczka, Strykow, Pruszkow), a destination-hub network in which every parcel is sorted once, at the hub that serves
  its delivery depot, by the sort plan. On the heaviest October nights Pruszkow's sorter is at capacity and linehaul
  control moves whole roll cages of the Warsaw-bound flow to Strykow, which sorts them on its manual line and trucks
  them to the two Warsaw depots on a trailer of its own. Each depot unloads an inbound trailer at one door, every parcel
  read off it by that door's fixed reader in one run.
- **The call.** Whether the standard's scan alert fires at any hub for October, and at what hubs: a hub's alert fires
  when its missed sort scans exceed 1.00 per cent of the parcels it sorted among the parcels its delivery depots
  unloaded on the mornings of 1 to 31 October (TDS-4, the carrier's tracking data standard). A monitoring call on the
  closed month's record; the alert sends a scan audit to the hub in the first two weeks of the peak (crews from 9
  November), which is why the window is the closed month and the call is retrospective by construction.
- **Shape.** 10, a scorecard of six hubs against one tolerance: each hub's parcels handled, missed sort scans, rate and
  verdict (24), the call (1), the chart's named parts (3), the two files (2); the asks add, for each of the thirteen
  depot codes, its courier events sent twice (13) and its pre-advised October parcels never picked up (13): 56
  criteria. Decision designation_set, answer set_of_items, question form whether.
- **Strategy.** population_selection: the rate's denominator is the parcels each hub sorted, and which hub an unscanned
  parcel passed is unrecorded; the plan of record names one hub, the night's routing another. Gap time (decisive: the
  route of record is standing, the routing changed night by night on the overflow nights) then population; generators
  G17 (statistical rigor: a missingness that depends on the stratum it hides, so the stratum is imputed from the
  auxiliary grouping and never split as if missing at random) decisive, G3 (record versus operation, the default
  path's plan of record), G12 (absence of record against record of absence: a parcel with no sort scan at its plan's
  hub never reached that hub); Gate G decomposition_attribution; calibration none; context artifact operations_log
  (the sorters' availability by hub night, a distractor); Layer 2 family estimand_identification, pattern
  own:latent-route-denominator.
- **Forum, event, organisation.** committee_or_panel (the operations board takes the scorecard), season_or_peak (the
  peak crews from 9 November), logistics_or_3pl. Role operations_director (the director of network operations, who
  rosters the scan audits a fired alert sends to a hub in the first two weeks of the peak).
- **People** (`guard.py names --geo Poland --seed 250`, locale pl_PL): Krzysztof Konieczek, director of network
  operations, who asks; Inga Blaut, head of tracking data quality, who owns TDS-4 and took the extract; Aurelia
  Pieczyrak, shipper integration, who takes the depot lines to the shippers' integration teams. None appears in the
  prompt.
- **Deliverables.** The scorecard workbook (the hubs and the depots) and one slide for the operations board (the chart
  of the six rates against the line, beside the hub table): xlsx and pptx.
- **Data-native sentence.** A sort scan is the only record of a hub on a parcel's history and the sort plan is the
  only record of its route, but on the overflow nights Pruszkow's sorter ran full while Strykow sorted the overflow by
  hand and trucked it to the Warsaw depots itself, so an unscanned parcel unloaded at a Warsaw depot on those mornings
  may have missed either hub, and only the unloading it came off, whose sorted parcels all carry one hub's sort scan,
  says which; the same nights are the nights Pruszkow's own sorter missed most (1.55 per cent against 0.86 on its
  other mornings), so the nights' excess over Pruszkow's usual rate is not Strykow's.
- **Abstraction sentence** (the one a reviewer holding this build beside its nearest approved build would say is the
  same, without domain nouns): none writable. Against task229 (units' states seen through checks), task235 (an item
  lost only once its device had its next chance to send), task236 (capture read against an independent protocol) and
  task242 (detection fading with time since the event) the quantity here is not a detection probability or a state
  but the route of each unrecorded unit, read from the batch it was unloaded in.
- **Same-puzzle and library tests.** Gap time, pattern G3 and designation_set repeat no build in the last twelve and
  no older one (`check`); the stump is not a named correction applied as a card states it: no rigor card carries a
  denominator rebuilt from the unload a unit belongs to.
- **Sources.** Carriers' scan-compliance practice (missed scans counted against the expected scan events of a parcel's
  route); the client's two-layer standard; at-least-once delivery in event integrations (re-sent events); EDI
  pre-advice matching against collection scans; trailer collections at large shippers without a per-parcel pickup scan.

## Default path

1. Read TDS-4 (sections 2 to 4), the sort plan (each delivery depot's hub, with the revision moving Opole to Sosnowiec
   from the night of 19 October) and the platform's feeds: the parcels unloaded at a delivery depot on the mornings of
   1 to 31 October (the re-sent arrival rows of 21 October dropped as the same rows), each parcel's sort event.
2. Give each parcel its hub: the hub of its sort event, and for a parcel with none the hub the plan in force on its
   night names for its delivery depot (the carriers' scan-compliance count against the route of record; the parcels
   Strykow sorted for the Warsaw depots show where the sorted overflow went).
3. Count per hub the parcels, the parcels without a sort event and the rate; fire the alert above 1.00 per cent.

Ends on: alerts at Sosnowiec and Pruszkow, Strykow under the line (its overflow misses charged to Pruszkow).

Golden: alerts at Sosnowiec, Pruszkow and Strykow, each unscanned parcel charged to the hub whose trailer it came off
at its delivery depot, read from its unloading.

## Stump sentence

A competent solver takes each parcel's hub from its sort scan or, where it has none, from the sort plan of its night,
and ends on alerts at Sosnowiec and Pruszkow with Strykow under the line; Strykow sorted Pruszkow's overflow by hand on
the heavy nights and sent it to the Warsaw depots on its own trailers, so the unscanned overflow parcels that route
charges to Pruszkow came off Strykow's trailers, and only the unloading each unscanned parcel came off at its delivery
depot fires Strykow as well.

## Three rules

Task type: missing-data-censoring-measurement-error (General Statistics & Data Science), the client domain the house
domain supply-chain-logistics sits in, a task type the taxonomy tags for Data Quality Monitoring & Alerting.
Domain test: the deciding quantity is each hub's missed-scan rate, the parcel network's scan-compliance measure, worked the way the field works missing data whose missingness hides its own stratum: the denominator is the parcels a hub sorted, and for a parcel with no sort scan the hub it passed is itself missing, so it is imputed from the auxiliary record that carries it.
Swap: "which wards' October handover logs miss more than 1 per cent of the patients who passed through them" keeps a completeness rate but loses the overnight trailer unloaded at one door in one run, the overflow trailer between sort hubs and the sort plan as the route of record, so nothing ties an unrecorded patient to a ward and the call stops reading the same.
Layer 1: the carrier's systems produce it: three feeds each written its own way (hub sort events in UTC with a second read when a parcel goes round the sorter loop, depot arrival scans in local time across the end of summer time, courier events in local time); one morning's arrival rows re-sent by two depot servers on 21 October as the same rows; the Krakow depot's code changed on its move; the sort plan revised for Opole; contract shippers' piece labels (consignment number and piece number) and marketplace order numbers kept to 20 characters by the handheld; pre-advice messages superseded by later versions; each is neutral on the call (asserted) and none is placed to be caught.
Layer 2: estimand_identification: the missed-scan rate's population is the parcels each hub sorted, a latent stratum for exactly the parcels that went unscanned; the methodological choice is how to impute it, from the plan of record, from the depot morning's sorted split (missing at random), from the mornings with one hub only (complete cases), from the nights' excess over a hub's usual rate, or from the unloading each parcel belongs to.
Decisive step: imputing each unscanned parcel's stratum from the auxiliary grouping it travelled in, the run of arrival reads at its delivery depot's door whose sorted members all carry one hub's sort scan, because here the missingness depends on the stratum itself (Strykow's manual line missed 9.03 per cent, Pruszkow's sorter 1.55 on the same mornings).
Not semantics: every field read right (the plan's hub per night with its revision, the event types, the three clocks, the depot codes, the number formats) still leaves the solver charging an unscanned parcel to its plan's hub or to the morning's sorted split: no field of an unscanned parcel names the hub it passed, and the plan is an accurate statement of the route of record.
Not rule application: TDS-4 files the estimand (a missed sort scan is one of a hub's parcels with no sort event; the rate is over the parcels it sorted among those unloaded in the month; the alert above 1.00 per cent) and nothing filed says how an unscanned parcel's hub is known; the enumerated family (route of record, the morning's sorted split, the month's split, the one-hub mornings only, the nights' excess charged to Strykow, the unloading) spreads Strykow's rate from 0.49 to 2.30 per cent and Pruszkow's from 0.86 to 1.76 and names four alert sets; the standing family on a careful read without the unloadings keeps the first five, because only the unloadings refute them, and nothing points at the unloadings.
Analyst test: a strong analyst who cleans the feeds and reads TDS-4 and the plan correctly takes each parcel's hub from its sort scan or its plan and ends on alerts at Sosnowiec and Pruszkow, Strykow under the line at 0.49; on the generator's clean truth the same route files the same pair and only the unloading fires Strykow (checks.py R-block).
Estimand: TDS-4 sections 2.1 to 2.3 (TDS-4_tracking_data_standard.pdf): a hub's parcels for the month are the parcels it sorted among those the delivery depots unloaded on the mornings of the month, a missed sort scan is one of them with no sort event on the platform, the rate is the missed over the parcels, and the alert fires above 1.00 per cent.
No decoy: nothing is planted: the sort plan is the carrier's ordinary route of record and correct as a plan, the overflow is linehaul control's ordinary capacity practice with nothing announcing it beyond the reads it leaves, no memo, draft, earlier scorecard or stakeholder figure ranks the hubs, and no file is shipped to carry the wrong answer.
No certified replay: the method is not recovered by reproducing a published figure: no file states a hub's October rate, parcels or misses, and nothing filed is reproduced to recover the imputation.
Lesson: a completeness rate whose denominator is a latent stratum for exactly the missing records is imputed from the auxiliary record that carries the stratum (here the unloading a parcel belongs to), never from the plan of record, a missing-at-random split or an excess the same overload produced; no build on file rebuilds a missing record's stratum from the batch it travelled in.

## Survivor anatomy

Actor: which hub an unscanned parcel passed has no column in any file; it is a relation between the parcel's arrival read and the other arrival reads at the same depot door that morning, whose sort events name one hub.
Link: each unscanned parcel is tied to the unloading it belongs to, a grouping of arrival reads by depot door and pause in time that no key offers (no event carries a trailer, a trip or a route) and no sentence invites.
Reflex: the field's own scan-compliance count, each parcel's expected sort read from its route of record (the sort plan of its night), and the field's missing-data reflexes (a missing-at-random split within the depot morning, complete cases) sit at rungs 0 to 2 and file alerts at Sosnowiec and Pruszkow (`Ends on:`) or at Sosnowiec alone, not the golden three.
Back-test: every check the record offers passes on the plan route: every sorted parcel was sorted at its plan's hub on every night without overflow, the sorted overflow parcels sit on the nights Strykow sorted for the Warsaw depots, each hub's parcels reconcile to its sort events and the depots' arrivals, so the plan reads as the complete route of record.
Second use: every file the step reads sits in the pack for its own reason: the depot arrival scans are the month's population every rate is over, the hub sort events are the numerators, the register gives the hubs, depots and door readers every grouping needs, and TDS-4 is the standard the call runs on; the courier events, the pre-advices and the handheld register carry the asks.
Shock: the movement the step recovers reads as ordinary: Pruszkow's high rate on its heavy nights is its own sorter running full, Strykow's overflow is 1,440 parcels of a month's 24,425 at Pruszkow, and sorted on any shipped statistic (rate on the route of record, volume, nights) the golden set is not an interval.
Pins: TDS-4 files the WHAT (the population, the window, the rate and the tolerance) in the carrier's own standard; no filed sentence names the plan, the overflow, a trailer, a door, an unloading or how an unscanned parcel's hub is known.

## Readability screen

Seven tests per rung (stumping 2.1): 1 a filed sentence names the decisive quantity or sends the solver to it; 2 a
column, key or marker makes it a row predicate or a header-found join; 3 an opponent reflex reaches it; 4 a control
or corpus scores the rules or refutes the naive read; 5 the hygiene battery finds it; 6 one subtraction, ratio or
half of a reported figure; 7 a file the step alone reads.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Bench | 5 Hygiene | 6 Linear | 7 Second use | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0 (default) the plan's hub for a parcel without a sort event: Sosnowiec and Pruszkow, Strykow 0.49 | TDS-4 2.1 says the hub that sorted it and the plan names one per depot and night | the plan's delivery depot and nights join to every arrival | yes, the route of record | none refutes it | no | a lookup | the plan sits in the pack for this | readable |
| 1 the depot morning's unscanned split by its sorted parcels' hubs: Sosnowiec and Pruszkow, Strykow 0.77 | none | the sort events by depot and day | yes, missing at random within the cell | none | no | a share | none | readable |
| 2 the mornings with two hubs left out: Sosnowiec alone, Pruszkow 0.86 | none | the same grouping | yes, complete cases | none | no | a filter | none | readable |
| 2 the two-hub mornings' excess over Pruszkow's rate on its other mornings charged to Strykow: Sosnowiec and Strykow, Pruszkow 0.86 | none | the same grouping | yes, an excess over a baseline | none | no | one subtraction | none | readable |
| 3 (decisive) each unscanned parcel's hub from its unloading at the delivery depot, because the missingness depends on the hub | no sentence names an unloading, a door, a trailer or how an unscanned parcel's hub is known | no column holds a trailer, a trip or a hub for an arrival; the reader id and the second are the only keys | no: the reflexes are the plan, the split and the complete cases | nothing scores it | no | not linear: a per-parcel grouping by door and pause | the arrivals are the population file | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | October | parcels unloaded on the mornings of 1 to 31 October, the 30 September night's sorts in | parcels sorted on October nights | same call | TDS-4 2.1; same call (asserted) |
| SF2 | parcels handled | the distinct parcels the hub sorted among the month's, unscanned included | the hub's sort-event rows (loop re-reads counted) over the sorted only | same call | TDS-4 2.1 and 2.2; same call |
| SF3 | missed sort scan | no sort event on the platform at the extract | a sort event that reached the platform after it | same call | every record received before 07:40 on 6 November (asserted) |
| SF4 | missed-scan rate | per cent of the hub's parcels | per cent of its sorted parcels | same call | TDS-4 2.2; same call |
| SF5 | above 1.00 per cent | strictly above | at or above | same call | no hub within 0.2 points of the line |
| SF6 | rounding | the verdict on the unrounded rate, the rate shown to two decimals | the verdict on the two-decimal rate | same call | same call |
| SF7 | the re-sent arrival rows | one parcel once | each row a parcel | same call | the rows are the same rows; same call |
| SF8 | Krakow's two depot codes | two depots | one depot | same call | the call is per hub; same call |
| SF9 | the arrival clock | local, as the depot server writes it | UTC | same call | every unloading between 03:00 and 09:00, the same morning either way |
| SF10 | the sort clock | UTC, as the column is named | local | same call | the call never reads the sort time |
| SF11 | the hub of a parcel without a sort event | the hub that sorted it | the hub the plan names for its depot and night | Sosnowiec and Pruszkow | TDS-4 2.1 (a hub handles a parcel when it sorts it; a plan is not a sort), the unloadings each holding one hub's sorted parcels |
| SF12 | our sort hubs | the six hubs of the network register | none | same call | TDS-4 1 (every hub in the register) |
| SF13 | the as-of | the extract of 6 November, 07:40 | records arriving later | same call | TDS-4 5.1; none arrives later (asserted) |
| SF14 | a parcel in the call | each piece label | a consignment once | same call | TDS-4 4.1 (each piece is one parcel); same call |
| SF15 | whether its alert fires | one verdict per hub | none | same call | TDS-4 2.3 |
| SF16 | an unloading | a door's run of arrival reads | the depot's run whatever the door | same call | the same unloadings either way (asserted) |
| SF17 | sent twice | an event counted once however many further records arrive | each further record | same figures | TDS-4 3.1; no scan sent three times |
| SF18 | the depot of a courier event | the depot the event names | the register's depot for the handheld | moves Krakow's two rows | TDS-4 3.2 |
| SF19 | pre-advised for October collection | the latest version's collection date in October | any version's date | moves ask B | TDS-4 4.1 and 4.2 |
| SF20 | the depot of a pre-advice | the replacing depot for a replaced code from the day it opened | the code as the shipper sent it | moves Krakow's two rows | TDS-4 4.3 and the register's Depots sheet |
| SF21 | parcels in ask B | pieces | consignments | moves every contract depot | TDS-4 4.1 |
| SF22 | never picked up | never collected from the shipper | no pickup scan | moves every depot | TDS-4 4.4; a parcel sorted, unloaded or delivered was collected |

## Ladder

Four routes past the default, each a defensible way of giving an unscanned parcel a hub, each dying to one shipped
fact (rates per cent of the hub's parcels; the line at 1.00; figures measured on the shipped pack, asserted in
`checks.py`).

| Rung | Construction | Answer | Dies to |
|---|---|---|---|
| 0 (default) | the plan's hub (Q4-2 in force) for a parcel without a sort event | Sosnowiec 1.34 and Pruszkow 1.76 fire; Strykow 0.49 | the unloadings: on 24 depot mornings the Warsaw depots unloaded a second trailer whose sorted parcels all carry Strykow's sort event |
| 0b (hazard) | the first plan issue all month | adds Bielany Wroclawskie at 1.05; Strykow 0.49 | the plan's Issues sheet (Q4-2, Opole at Sosnowiec from the night of 19 October) |
| 1 | each depot morning's unscanned parcels split by its sorted parcels' hubs; or by the depot's month | Sosnowiec and Pruszkow (1.62; 1.67); Strykow 0.77; 0.67 | the unloadings: Strykow's trailers carry 9.1 per cent of the two-trailer mornings' sorted parcels and 38.8 per cent of their missing sort scans |
| 2 | the two-trailer mornings left out | Sosnowiec alone; Pruszkow 0.86, Strykow 0.55 | TDS-4 2.1: the month's parcels are every parcel unloaded, and the cut drops the mornings Pruszkow ran full |
| 2 | the two-trailer mornings' excess over Pruszkow's rate on its other mornings (0.86) charged to Strykow | Sosnowiec and Strykow 2.30; Pruszkow 0.86 | the unloadings: Pruszkow's own trailers missed 205 of 13,223 (1.55 per cent) on those mornings |
| 3 (golden) | each unscanned parcel's hub from its unloading | Sosnowiec 1.34, Strykow 1.55 and Pruszkow 1.23 fire | |

- **Margins.** The golden's nearest hubs are Pruszkow at 1.23 (1.23x) and Bielany Wroclawskie at 0.79 (1.27x); every
  verdict on rungs 0, 1 and 2 stands 1.15x or more from the line (Bielany at 0.85 on the month's split, 1.18x); the
  hazard rung is wrong at Strykow by 2.04x whichever side Bielany falls (asserted).
- **Purity.** All 300 unloadings hold one hub's sorted parcels and at least one sorted parcel; any pause from one to 29
  minutes, with or without the door, gives the same unloadings (the longest pause inside an unloading is under a
  minute, the shortest between two at a door over 30 minutes).
- **Position.** The default path's one wrong verdict (Strykow under the line) sits 2.04x from it; no rung reaches the
  golden; the rungs name four different wrong sets.
- **Worth.** The decisive step moves 130 parcels from Pruszkow to Strykow and decides one verdict.

## Closure table

| Axis | Reading here | Move |
|---|---|---|
| 1 Population | the parcels unloaded on the mornings of 1 to 31 October, unscanned included | filed, TDS-4 2.1; C1 under the sort-night reading (SF1) |
| 2 Unit of account | a parcel (a piece label), per hub | the question and TDS-4 4.1; C1 (SF14) |
| 3 Attribution window | the unloading morning | filed, TDS-4 2.1; C1, every unloading 03:00 to 09:00 (SF9) |
| 4 As-of dating | the extract of 6 November 07:40 | filed, TDS-4 5.1; every record received before it (SF13) |
| 5 Version basis | pre-advices at their latest version; the plan in force on the night | filed, TDS-4 4.1 (asks); the golden never reads the plan |
| 6 Denominator | the hub's parcels | filed, TDS-4 2.2; C1 (SF4) |
| 7 Weighting | none: counts | n/a, asserted on the figures |
| 8 Window length | one month | filed, TDS-4 2.1 |
| 9 Boundary inclusivity | above 1.00, strict | C1, no hub within 0.2 points (SF5) |
| 10 Rounding path | the verdict on the unrounded rate, rates shown to two decimals once | C1 (SF6) |
| 11 Tie-break | none | no two hubs or depots share a count (asserted) |
| 12 Maturity and censoring | the month closed six days before the extract | C1, nothing received after the extract |
| 13 Order of operations | the same rows collapsed, then grouped | C1, the re-sent rows are the same rows (SF7) |
| 14 Row order | the unloadings sort by door and time | C1, the grouping sorts its input |
| 15 Duplicate resolution | the re-sent arrival rows once; a scan sent twice counted once | C1 (SF7); filed for the asks, TDS-4 3.1 (SF17) |
| 16 Identity normalisation | full tracking numbers in the call; piece labels and cut references in ask B | C4: every sort event matches an arrival (asserted); the asks' keys are their devices |
| 17 Netting against gross | none | n/a |
| 18 Dimensional units | parcels only | n/a |
| 19 Code and status semantics | ARRIVED and sort events in the call; a failed pickup is not a collection in ask B | the call reads two codes; filed for the ask, TDS-4 4.4 (SF22) |
| 20 Integerisation | counts whole; rates two decimals | C1 by construction |
| 21 Clause scope | TDS-4 2 for the call, 3 and 4 for the asks | filed |
| 22 Forward window contents | none: a closed month | the call is retrospective by construction (Draw) |

## Literal reader

Executed word for word, TDS-4 2.1 to 2.3 make each hub's parcels the month's parcels it sorted and its missed sort
scans those with no sort event; the one step the text leaves open is which hub sorted a parcel the platform holds no
sort event for, and every route that identifies the hub that sorted it gives the golden (the unloadings are pure and
threshold-free, asserted) while the plan, the morning's split, the complete cases and the excess each name the hub
planned or an estimate, not the hub that sorted it; SF1 to SF22 close every term and convention.

## Oracles

None. No file states a hub's October rate, misses or parcels, or any depot's re-sends or uncollected pre-advices; the
sorters' availability file (a distractor) records scheduled and down minutes per hub night and ranks nothing on the
decision basis; the claims file (a distractor) holds claims by tracking number; the request names no hub.

## Ask sheet

Two asks, 26 figures, decoupled from the call: the call reads the depot arrival scans, the hub sort events, the
register's hubs and TDS-4 section 2; the asks read the courier events, the handheld register, the pre-advices and TDS-4
sections 3 and 4, files and sections the call never reads.

**Main population (zero device rows, asserted):** the depot arrivals and the sort events. Deleting the courier events,
the pre-advices, the accounts, the claims, the sorters' availability and the request leaves the call unchanged
(asserted).

| Ask | Figures | H18 home | Use | Primary devices (family) | Hazards | Path (files, columns) | Stops |
|---|---|---|---|---|---|---|---|
| A: each depot's courier events its handhelds sent twice | 13 | an audit of the platform's intake from the depots' handhelds | the shipper-integration lead's call with the integration teams | D8, a clock on a subset: a re-send carries the first record's time as the handheld queued it, cut to the minute, in local time from a TC52 and in UTC from a TC51 (two hours behind until 25 October, one after); every depot runs both models; D1 over-cleaning: a parcel taken off the first loop and loaded on the second, and a failed attempt taken out on the afternoon wave, are new scans the same day on the same handheld | the Krakow move (the event names its depot, TDS-4 3.2) | courier events (tracking number, depot, courier, handheld, event, time, received), register Handhelds (model), TDS-4 3: 3 files, 8 columns | exact duplicates (0 to 27 per depot); the battery's near-exact duplicate, same minute (the TC52 re-sends only: 42 to 662 against 97 to 942); same parcel, event and handheld on the day (the second loops and waves counted: 166 to 1,335); within 5 minutes; within 3 hours; the TC51 shift fixed at two hours all month (keeps D-KRK1 only, closed before 25 October); the answer |
| B: each depot's parcels pre-advised for October collection it never picked up | 13 | a reconciliation of the shippers' pre-advices against the network's own records | the same call: the uncollected pre-advices each shipper's system keeps sending | D4, absence evidenced in a file the habitual join never reaches: the largest label-printing shippers at every depot load trailers on some days, so their parcels carry no pickup scan yet are sorted, unloaded and delivered; and a courier who found nothing ready records a failed pickup against the pre-advised number; D7, the true key elsewhere: a contract shipper's parcels carry the consignment number plus a three-digit piece number, some consignments short of their pre-advised pieces, and marketplace order numbers kept to 20 characters by the handheld, orders of a seller's day sharing their first 20 | versions superseded (the latest stands, TDS-4 4.1); the replaced Krakow code (4.3); September and November collection dates; re-sent pickup events | pre-advices (consignment, version, depot, date, number, pieces, reference), courier events (number, event, reference, depot), hub sort events and depot arrivals (number), register Depots (replaced code, opened), TDS-4 4: 5 files, 14 columns | every line on exact keys (334 to 5,161 per depot); latest versions on exact keys (240 to 4,717); labels and references matched by prefix, any match (240 to 1,233); pieces and references counted against the pickup events (the cracker: 240 to 1,245 against 43 to 346); every courier event as a collection (the failed pickups counted collected: 30 to 274); the answer |

- **Span:** seven files and 22 column uses across the asks; no shared primary or path (A reads clocks and handhelds,
  B numbers, pieces and references).
- **Shared hazards:** the courier re-sends repeat pickup events, so counting pickup rows against a marketplace order
  understates its uncollected orders; the Krakow move moves both asks' Krakow rows.
- **Realism:** an older handheld's app writing its retry queue in UTC, a second loop and an afternoon wave, trailer
  collections at large shippers, failed collections keyed from the pickup list, piece labels under a consignment
  number and a handheld field of 20 characters are records these systems make with no task in mind.
- **Referee:** none.

| Ask figure | Where the cracker's path goes | Mirror (stops at rung 0) | Cracker (lands the call, runs the battery) |
|---|---|---|---|
| A courier events sent twice, every depot (13) | drops the near-exact duplicates (same parcel, event, courier, handheld and minute), which finds the TC52 re-sends and none of the TC51's | counts the same parcel, event and handheld on the day, second loops and waves included | miss |
| B pre-advised parcels never picked up, every depot (13) | applies the latest version and the replaced code, matches piece labels and cut references and counts them, against the pickup events the ask names; every trailer-collected parcel counts as never picked up | matches labels and references by prefix, any match | miss |

- **Cracker keeps:** 0 of 26 ask figures (every depot's figure in both asks is moved by a device off the battery).
- Mirror leakage: 34.0 per cent of ask weight, counting the hub rows the plan route gets right inside the ask weight (17 of 24); 0 of the 26 depot figures.
- Pair ceiling: 51.1 (the hub rows counted as asks: C = 38 + 7 + 55 x 0.48 = 71.4, S = 5 + 7 + 55 x 0.34 = 30.7; with the hub rows inside the call's components, C = 45.0, S = 12.0 and the pair 28.5).
- Measured by: generator/ceiling.py on the cut pack (pack digest printed with the sheet).

## Pre-ship check

1. Domain: the call stands on each hub's missed-scan rate with the hub of every unscanned parcel imputed from the
   auxiliary record that carries it (the unloading), because the missingness depends on the hub (9.03 per cent on
   Strykow's manual line against 1.55 on Pruszkow's sorter the same mornings); with wards for hubs there is no trailer
   unloaded in one run and nothing to impute from.
2. Two layers: Layer 1 (three clocks, the re-sent arrival rows, the Krakow move, the Opole revision, loop re-reads,
   piece labels, cut references, superseded pre-advices) is neutral on the call, each item asserted (R2, SF rows);
   Layer 2 is the imputation of a missing stratum from its auxiliary grouping, asserted alone to move the default path
   to the golden (R3b).
3. No banned stump decides: nothing is planted (the overflow is recorded only as the reads it leaves); not semantics
   (the default path reads every field right and files Sosnowiec and Pruszkow, asserted on the clean truth, R3a); not
   rule application (TDS-4 files the population, the rate and the line and names no way of knowing an unscanned
   parcel's hub).
4. Gate G: no shipped artifact rates, flags or ranks a hub; the two distractors carry no rate.
5. Determinism: every route that identifies the hub that sorted each parcel gives the golden counts exactly (pure,
   threshold-free unloadings); SF1 to SF22 closed; every rate at least 0.2 points from the line; counts are integers.
6. Asks: A (13) and B (13) are moved in every figure by a device the battery does not repair (the TC51 clock at every
   depot; trailer collections and failed pickups at every depot), the call reading neither file (asserted).
7. Input gates: 11 files in five formats, the courier events at 280,378 rows, two distractors named in metadata.json;
   the generator's checks with the realism sweep; the verifier (nearest neighbours at the door, a hand-written clock,
   merges) green; two builds byte-identical.

## Leak review

`leak.py task250 --asof 2026-11-06`: REVIEW, no LEAK; each line ruled here.

- Answer figures: TDS-4 carries 1.00, the filed tolerance (TDS-4 2.3), which the chart draws as its line; harmless.
- Design-note vocabulary: TDS-4's matching words (record, parcel, sorted, network, nights, mornings) are the filed
  population's own (2.1: every parcel sorted by one hub on the night before, the parcels unloaded on the mornings of
  the month); it names no unloading, door, trailer, overflow or plan; harmless.
- Dates after the setting: the sort plan's Q4 rows run to 31 December, the plan's validity; harmless.

## Tried and rejected

- 2026-10-31, architecture 2 (the agro-climatic network's 2028 drift-alert setting, the drifts cut short by the 3.0
  alerts' repairs): spent at the batch 1 repair; the determinism judge returned NOT_DETERMINISTIC, SEND_BACK: the 4.0
  call counted every repaired drift the re-run never reached as exactly one later alert, which no shipped file
  forces; a rate model built from the sensor history (onset at the previous clean check) puts slow drifts hundreds of
  days from the wider limits and gives 14 to 16 a year at 4.0, not 18; and the new contractor's visit day rested on
  an inference. Filing the counting rule would make the decisive step rule application, so the world is left after
  two architectures.
- 2026-10-31, the draw's first card (gap population, G3 decisive): `test.same_puzzle` and `test.same_driver` BLOCK
  against task270 v8, task464 and four older builds; the decisive gap is time (the route of record is standing and the
  routing changed night by night), the honest reading, which clears both.
- 2026-10-31, a bypass mechanism (depot-to-depot direct trailers skipping every hub): on the route of record each
  direct-loaded parcel is a miss at its plan's hub, a loud rate a solver investigates, and the lane-night correction
  that follows lands that hub's verdict; dropped before any data, the overflow alone carries the step.
- 2026-10-31, overflow nights on which Pruszkow's own scanning is unaffected: the overflow nights' excess of unscanned
  parcels at the Warsaw depots over Pruszkow's usual rate is then Strykow's unscanned overflow, a one-subtraction route
  to the call; Pruszkow's own misses now rise with its sorter's load on the same nights, so the excess route charges
  Strykow with Pruszkow's own misses and clears Pruszkow.
- 2026-10-31, a linehaul trip log in the pack: it is a second, timed route to each trailer and nothing else reads it,
  so its presence would announce the step (readability test 7); the unload bursts carry the trailer on their own.
- 2026-10-31, the first ask A (each hub's sort events its interface sent twice): a re-sent batch of sort events is the
  battery's near-exact duplicate and sits on the call's own file; the ask moved to the courier events per depot.
- 2026-10-31, one handheld model per depot (TC51 at the contract depots only): the battery's near-exact duplicate then
  lands every TC52 depot's re-sends exactly; every depot now runs both models.
- 2026-10-31, ask B matched against every courier event: with trailer collections as the only absence, any courier
  event is evidence of collection and that shortcut lands all 13 depots; couriers now record a failed pickup against the
  pre-advised number, which is no collection.
- 2026-10-31, marketplace order numbers drawn per seller for every marketplace: two sellers on one marketplace then
  share an order number and a pickup is counted against the wrong order; the marketplaces that number orders globally
  now do so.
- 2026-10-31, Strykow's own sorter at 0.61 per cent: the morning's sorted split left Strykow at 0.87, 1.148x from the
  line; at 0.56 per cent it sits at 0.77.
- 2026-10-31, the card as drawn at the heart screen (G3 decisive, the head of tracking data quality asking, a PDF note
  beside the workbook): `guard.py heart` BLOCKed ban.pattern and ban.role against task470's later re-draw, and warned
  the shell (whether, each, pdf and xlsx) repeated task245; the measured ladder puts the decisive step past the
  missing-at-random split (rung 1), so the decisive generator is G17 and G3 is the default path's; the requester is
  redrawn to the director of network operations and the chart goes to the board on a slide.
- 2026-10-31, the claims file opened claims up to five days after the extract (`leak.py`, dates after the setting): a
  claim not yet opened on 6 November is not in a 6 November extract, and a claim opened in its last five days is open.

Architecture 2 and earlier, carried from the agro-climatic note:


- The seed's own pitfall (a per-station two-sigma rule against a network budget): the multiplicity reflex; it is the
  default path, not a stump.
- Limits estimated from short baselines (the parameter-estimation effect on false alarms): an honest replay of the
  filed limit-setting over the record lands it, and executing the filed limit rule is close to rule application.
- A burn-in of new sensors in a 2028 replacement programme: a composition shift (composition_mix banned against
  task473) announced by the replacement plan.
- Closures clustered in one province: the continuing stations keep their near neighbours on their own side and the
  alerts barely move (prototype, 0 of 97 continuing stations' spread up by 5 per cent); the programme's stations are
  interspersed, as gap-filling stations are.
- validated_decoy true on the first card (the replay reproduces the alert log and only the closures break it):
  guard BLOCK; the April 2026 additions put the refutation inside the record.
- Seed 252: the per-setting figures at 3.0 and 3.5 sat 0.17 from their rounding edges (65.67, 26.67 a year) and a
  literal reading of the record's first fortnight moved 3.0; a scan of 1,000 seeds found one (1141) with all four
  three-year counts divisible by three and unchanged under the start, limit-rounding and strict-limit readings.
- A statistic defined on every day with 10 residuals: the export carries read days only, and a reader of the export
  moved 4.0 from 11 to 10; the statistic and its alerts are now on read days (section 5).
- The hold read per calendar year: lifting it each January moved 3.0 and 3.5 by a whole alert; section 8 now says a
  new year's configuration does not lift it.
- One out-of-sample year: a single fresh year on the 2028 network raised exactly 18 at 3.5; three fresh years are the
  section 7 horizon (24.7 at 3.5, 10.3 at 4.0).
- The asks with one campaign device drawn at random: the readings-first path kept 10 of 24 and the order-first path
  12; the campaign visits, the cancellations after the visit and the remote resets are now aimed at every district,
  and the standard's absence reaches the winter visits no campaign touches.
- Architecture 1 (the record re-run with the 34 closing programme stations out of the neighbour pool, as the decisive
  step on its own): spent 10-20 at stage 4. Reader 1 re-ran the quality control with the 2028 network and filed 4.0 at
  9 a year, every setting within one of the golden (63, 26, 9 and 3 against 61, 25, 9 and 3); reader 2 replayed the
  record and filed 3.5 at 9; judge DETERMINISTIC APPROVE. A stated change with an obvious mechanism is landed by a
  careful reader: the network re-run is now the first rung, and the decisive step is the drifts the record's own 3.0
  alerts cut short.
- One key, the censoring alone (no closures): a single unprompted insight decides it, and a reader who thinks of the
  repairs lands the call; two keys, each alone leaving 3.5 inside the visits, are needed.
- Drifts anywhere in the network: a drift left to grow carries a close neighbour's statistic over that neighbour's
  limit before its own alert (prototype, 5 to 12 stations per seed whose counterfactual count departed from the
  re-run plus the cut-short drifts); drifts now sit only where the weight a neighbour gives them times their spread
  stays under 0.7 of the neighbour's own, at stations that keep their usual neighbours.
- Censored drifts the spring round would have found first: a drift cut short in January or February at a setting of
  3.0 would at 4.5 have met the station's spring round before its alert (prototype, 1 to 2 a year); a drift whose
  station's next round falls before it could have crossed 4.5 is redrawn.
- An autumn calibration round in 2027 and 2028: 2028's rounds would then differ from 2025's and 2026's, and the
  record's drifts of June to August would have been found by a round rather than an alert, a forecasting fork on
  the window; every year now has the spring round only.
- The six stations added in April 2026: their 21 months against the record's three years opened an annualisation
  fork on each setting's count; the six infill stations now report from 2025.
- Old sensors with standing offsets up to 0.4 degrees: a false alert's visit at such a station adjusts a sensor
  that never drifted, and the history's drift-alert adjustments stop meaning drifts; standing offsets are now under
  0.12 degrees and no check without a drift passes the 0.2 adjustment threshold.
- The visit asks on orders and readings alone (round 2): drift orders cancelled after the visit with the readings under
  the cancelled order, orders the handover export lost, and a closed order with nothing under it counted a visit when
  the station had a reading under another order while it was open. The pass 3 judge sent it back (52 cancelled orders
  with readings against the dictionary's Visita, the lost orders' window unrecoverable; Gate C on asks 3 and 4), and
  with the visit filed reader D built the visits from the readings station by station and took 24 of 24. Filing a
  visit closes the fork and hands the ask to every reader; the devices that held were all readings a careful reader
  joins. The cancellations after a visit and the lost orders are gone; the device is now readings no visit made (a
  spare checked at the workshop under the station's order), found only against the range the station's logger
  recorded that day.
- The growth of a drift left to the reader (rounds 1 to 3): the pass 4 judge read section 7 literally as the record
  re-run and found nothing filed that a drift the 3.0 alert's check set right would have gone on growing; the as-found
  errors at repair (0.6 to 0.9 of the 4.0 limit) then read as the drifts' full size, and 3.5 stood as at least as
  defensible (SEND_BACK, Gates A to C on the main call). Section 9 now files the property of sensors the counterfactual
  rests on (a drift does not stop on its own and grows at the sensor's own rate until a check sets it right); the
  censoring remains the analyst's, and the cut-short drifts alone, without the network re-run, still file 3.5.

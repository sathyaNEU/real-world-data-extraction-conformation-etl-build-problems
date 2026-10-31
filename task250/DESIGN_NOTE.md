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
- **Niche.** Kurier Warta sp. z o.o., a regional parcel carrier in Poland: twelve delivery depots, six sort hubs
  (Komorniki, Bielany, Sosnowiec, Modlniczka, Strykow, Pruszkow), a destination-hub network in which every parcel is
  sorted once, at the hub that serves its delivery depot, by the sort plan. On the heaviest October nights Pruszkow's
  sorter is at capacity and linehaul control sends the overflow of the Warsaw-bound trailers to Strykow, which sorts it
  on its manual line and trucks it to the two Warsaw depots on a trailer of its own. Each depot unloads an inbound
  trailer at one door, scanning every parcel off it in one burst on that door's fixed scanner.
- **The call.** Whether the standard's scan alert fires at any hub for October, and at what hubs: a hub's alert fires
  when its missed sort scans exceed 1.00 per cent of the parcels that passed through it, counting the parcels unloaded
  at a delivery depot on the mornings of 1 to 31 October (TDS-4, the carrier's tracking data standard). A monitoring
  call on the closed month's record; the alert decides where the peak scanning crews go from 9 November, which is why
  the window is the closed month and the call is retrospective by construction.
- **Shape.** 10, a scorecard of six hubs against one tolerance: each hub's parcels handled, missed sort scans and rate
  with its verdict (18), the call (1), the chart's named parts (5), the two files (2); the asks add each hub's twice-sent
  sort events (6) and each origin depot's pre-advised parcels never picked up (12): 44 criteria. Decision
  designation_set, answer set_of_items, question form whether.
- **Strategy.** population_selection: the rate's denominator is the parcels that passed through a hub, and which hub
  an unscanned parcel passed is unrecorded; the plan of record names one hub, the night's routing another. Gap time
  (decisive: the route of record is standing, the routing changed night by night on the overflow nights) then
  population; generators G3 (record versus operation) decisive, G12 (absence of record against record of absence: a
  parcel with no sort scan at its plan's hub never reached that hub), G6 (the overflow nights' composition); Gate G
  decomposition_attribution; calibration none; context artifact operations_log; Layer 2 family
  estimand_identification, pattern own:latent-route-denominator.
- **Forum, event, organisation.** committee_or_panel (the network quality review takes the alerts), season_or_peak
  (the peak crews from 9 November), logistics_or_3pl. Role statistical_office_head (the head of network data quality).
- **People** (`guard.py names --geo Poland --seed 250`, locale pl_PL): Inga Blaut, head of network data quality, who
  asks; Krzysztof Konieczek, linehaul control; Aurelia Pieczyrak, owner of TDS-4. None appears in the prompt.
- **Data-native sentence.** A sort scan is the only record of a hub on a parcel's history and the sort plan is the
  only record of its route, but on the overflow nights Pruszkow's sorter ran full while Strykow sorted the overflow by
  hand and trucked it to the Warsaw depots itself, so an unscanned parcel unloaded at a Warsaw depot on those mornings
  may have missed either hub, and only the trailer it came off, whose scanned parcels all carry one hub's sort scan,
  says which; the same nights are the nights Pruszkow's own tunnel missed most, so the nights' excess over Pruszkow's
  usual rate is not Strykow's.
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
  pre-advice matching against collection scans.

## Default path

1. Read TDS-4 (sections 2 to 4), the sort plan (each origin and delivery depot's hub, with the revision moving Opole to
   Sosnowiec from the night of 19 October) and the tracking events: the parcels unloaded at a delivery depot on the
   mornings of 1 to 31 October, the re-sent arrival batch dropped, the Krakow depot's two codes merged.
2. Give each parcel its hub: the hub of its sort scan, and for a parcel with none the hub the plan in force on its
   night routes its origin and delivery depot through (the carriers' scan-compliance count against the route of
   record; the overflow parcels Strykow scanned show where the scanned overflow went).
3. Count per hub the parcels, the parcels without a sort scan and the rate; fire the alert above 1.00 per cent.

Ends on: alerts at Sosnowiec and Pruszkow, Strykow under the line (its overflow misses charged to Pruszkow).

Golden: alerts at Sosnowiec, Pruszkow and Strykow, each unscanned parcel charged to the hub of the trailer it came
off at its delivery depot.

## Stump sentence

A competent solver takes each parcel's hub from its sort scan or, where it has none, from the sort plan of its night,
and ends on alerts at Sosnowiec and Pruszkow with Strykow under the line; Strykow sorted Pruszkow's overflow by hand on
the heavy nights and sent it to the Warsaw depots on its own trailers, so the unscanned overflow parcels that route
charges to Pruszkow came off Strykow's trailers, and only the trailer each unscanned parcel came off at its delivery
depot fires Strykow as well.

## Three rules

Task type: missing-data-censoring-measurement-error (General Statistics & Data Science), the client domain the house
domain supply-chain-logistics sits in, a task type the taxonomy tags for Data Quality Monitoring & Alerting.
Domain test: the deciding quantity is each hub's missed-scan rate, the parcel network's scan-compliance measure, worked
the way the field works missing data whose missingness hides its own stratum: the denominator is the parcels that
passed the hub, and for a parcel with no sort scan the hub it passed is itself missing, so it is imputed from the
auxiliary record that carries it, the depot unload the parcel belongs to.
Swap: "which wards' October handover logs miss more than 1 per cent of the patients who passed through them" keeps a
completeness rate but loses the overnight trailer unloaded at one door in one burst, the overflow trailer between sort
hubs and the sort plan as the route of record, so nothing ties an unrecorded patient to a ward and the call stops
reading the same.
Layer 1: the carrier's systems produce it: depot handhelds and hub interfaces writing one event stream with local event
times and UTC receipt times across the end of summer time; a batch of depot arrival events re-sent with their own event
ids; the Krakow depot's code changed on its move to Rybitwy; two tracking-number formats (a legacy contract range);
the sort plan revised mid-month for Opole; pre-advice messages superseded by later versions; each is neutral on the
call (asserted) and none is placed to be caught.
Layer 2: estimand_identification: the missed-scan rate's population is the parcels that passed each hub, a latent
stratum for exactly the parcels that went unscanned; the methodological choice is how to impute it, from the plan of
record, from the night's scanned parcels on the lane, from the nights' excess over a hub's usual rate, or from the
unload each parcel belongs to.
Decisive step: imputing each unscanned parcel's hub from its unload, the door-scanner burst it came off at its
delivery depot, whose scanned parcels all carry one hub's sort scan, rather than from the route of record, the lane's
scanned split or the overflow nights' excess.
Not semantics: every field read right (the plan's hub per night with its revision, the event types, the two clocks,
the depot codes, the number formats) still leaves the solver charging an unscanned parcel to its plan's hub: no field
of an unscanned parcel names the hub it passed, and the plan is an accurate statement of the route of record.
Not rule application: TDS-4 files the estimand (a missed sort scan is a parcel that passed a hub without a sort event
there; the rate is over the parcels that passed it; the alert above 1.00 per cent), and nothing filed says how an
unscanned parcel's hub is known; the enumerated family (route of record, lane-night majority, lane-night proportional
split, overflow nights left out, the nights' excess charged to Strykow, the unload) spreads Strykow's rate from about
0.6 to about 2.0 per cent and names four different alert sets; the standing family on a careful read without the
unload keeps the first five, because nothing but the unload bursts refutes them, and that refutation is silent.
Analyst test: a strong analyst who cleans the events and reads TDS-4 and the plan correctly takes each parcel's hub
from its sort scan or its plan and ends on alerts at Sosnowiec and Pruszkow, Strykow under the line; on the
generator's clean truth the same route files the same pair and only the unload fires Strykow (checks.py R-block).
Estimand: TDS-4 sections 2 to 4 (tds4_tracking_data_standard.pdf): a hub's missed-scan rate for a month is its missed
sort scans over the parcels that passed through it among the parcels unloaded at a delivery depot on the mornings of
the month, and its scan alert fires when the rate exceeds 1.00 per cent.
No decoy: nothing is planted: the sort plan is the carrier's ordinary route of record and correct as a plan, the
overflow is linehaul control's ordinary capacity practice with nothing announcing it beyond the scans it leaves, no
memo, draft, earlier scorecard or stakeholder figure ranks the hubs, and no file is shipped to carry the wrong answer.
No certified replay: the method is not recovered by reproducing a published figure: no file states a hub's October
rate, passages or misses.
Lesson: a completeness rate whose denominator is a latent stratum for exactly the missing records is imputed from the
auxiliary record that carries the stratum (here the unload a unit belongs to), never from the plan of record or from
an excess the same overload produced; no build on file rebuilds a missing record's stratum from the batch it travelled
in.

## Survivor anatomy

Actor: which hub an unscanned parcel passed has no column in any file; it is a relation between the parcel's arrival
scan and the other arrival scans on the same door scanner that morning, whose sort scans name one hub.
Link: each unscanned parcel is tied to the unload burst it belongs to, a grouping of arrival events by depot door and
gap in time that no key offers (no event carries a trailer, a trip or a route) and no sentence invites.
Reflex: the field's own scan-compliance count, each parcel's expected sort scan read from its route of record (the
sort plan of its night), with the observed hub where it was scanned, sits at rung 0 and files alerts at Sosnowiec and
Pruszkow (`Ends on:`), not the golden three.
Back-test: every check the record offers passes on that route: every scanned parcel was sorted at its plan's hub on
every night without overflow, the scanned overflow parcels sit on the nights the scans show Strykow sorting for the
Warsaw depots, each hub's parcels reconcile to its sort events and the depots' arrivals, so the plan reads as the
complete route of record.
Second use: every file the step reads sits in the pack for its own reason: the tracking events are the platform's
record every figure comes from (the call, the twice-sent events, the pickups the pre-advices are matched to), the
register gives the depots, codes and doors every grouping needs, and TDS-4 is the standard the call runs on.
Shock: the movement the step recovers reads as ordinary: Pruszkow's high rate on the heavy nights is its own sorter
running full, Strykow's overflow volume is a share of a single month's Warsaw flow, and sorted on any shipped
statistic (rate on the route of record, volume, nights) the golden set is not an interval.
Pins: TDS-4 files the WHAT (the population, the window, the rate and the tolerance) in the carrier's own standard; no
filed sentence names the plan, the overflow, a trailer, a door, a burst or how an unscanned parcel's hub is known.

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

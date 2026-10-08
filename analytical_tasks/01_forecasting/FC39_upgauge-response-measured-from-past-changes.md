# FC39 — How many more passengers this summer's nine upgauges will carry, when the routes run full and the only honest measure of their response is the airline's own past upgauges

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Supply Chain & Logistics · airline network and capacity planning |
| Mirrors | Forecasting what added capacity carries on constrained routes (airline upgauges, air-cargo lift added to sold-out lanes, cloud capacity added to throttled tiers), where the full routes' load factor measures seats rather than demand and recorded denials understate what was turned away |
| Decision shape | One figure committed at a date: the incremental summer passenger forecast that sets the ground-handling contract and the revenue plan |
| Committed call | Additional passengers the nine upgauged routes will carry this summer over last summer, to the nearest thousand |
| Gap · Pattern | Gap 1 (time) over Gap 4 (rule) · change-log natural experiments (measured #25), with a saturated measure broken by the standard's floor (measured #19) at rung 2 |
| Gate G mechanism | forecasting, with method_or_model_selection |
| Measured traps engaged | #25 assumes an effect the log could measure · #19 breaks a big tie instead of questioning it · #7 uses the ready-made measure |
| Calibration form | Prior-period close-out: the summer close-outs from 2023 to 2026 (route passengers, seats, load factor and denied bookings), read against the schedule change log's nine past upgauges |
| Driving force | On a route that runs at 98–100%, the load factor is a measure of the seats, not of demand, so carrying it onto bigger aircraft fills every new seat. The planning standard's floor (carried passengers plus denied bookings) breaks that saturation but counts only travellers who tried and failed to book. Nine past upgauges, each logged with the summer before and the summer after, show the first summer carrying 41% of the added seats, between 40.8% and 41.2% every time, while the same first summers ran anywhere from 1.6 to 3.1 times their recorded denials. |

## 1. Situation

An airline's summer schedule upgauges nine routes, adding 620,000 summer seats. The ground-handling contract and the revenue plan both
need one figure: how many more passengers those routes will carry than last summer. Every summer the nine routes have flown at 98–100%
load factor. The network planning standard measures demand on a constrained route as carried passengers plus the bookings the
reservation system denied. The pack holds the summer close-outs since 2023, the reservation system's denial records, the schedule change
log, the segment-group capacity plan and the planning standard. The forecast goes to the revenue committee on the 20th.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: close-out passengers, seats, load factors and denials, the change log and the capacity plan. Network
  planning is right that the routes run full. No reported number is overturned; the difficulty is how much of the new capacity the routes
  will use, which no figure about the past states.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete network planning's view and every voice. Carrying each route's load factor is still the natural build, and the
  standard's floor still gives a defensible lower figure; neither touches the change log.
* **Instrument repair.** Imagine a reservation system recording every traveller who looked and walked away. Spill would be measured
  better, but the response to larger aircraft also includes travel the bigger schedule creates, which only a past upgauge shows.
* **Lens swap.** The naive read and the answer are different moments: these routes' carried traffic at last summer's gauge, against their
  traffic at the new gauge, which only the nine past before-and-after pairs describe.

## 3. The driving force

A strong solver takes last summer's close-out, carries each upgauged route's load factor onto its new seats, then sees the routes sat at
98–100% and recognises a saturated measure: the load factor tells it how many seats there were. It reaches for the planning standard's
floor, carried passengers plus denied bookings, which is the lowest demand every record supports, and forecasts the routes to carry that
demand. Every step is defensible. But denials count only travellers who tried to book a sold-out flight; many never try, and bigger aircraft
also bring fares down and add frequencies' worth of choice. The schedule change log records nine past upgauges with the summer before and
the first summer after in the close-outs. In every one, the first summer carried 41% of the added seats, while its multiple of recorded denials
wandered from 1.6 to 3.1. Measured, not assumed, the nine upgauges carry 254,000 more passengers.

## 4. The ladder

| Rung | Construction | Lands on (additional passengers) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Each route's last-summer load factor carried onto its new seats | 600,000 (+136%) | The planning tool's default, and these routes have filled every summer | The capacity plan's segment groups: an upgauged route moves into the long-haul leisure group, whose seat-weighted load factor is 88%, not 99% |
| 1 | Segment-group load factor (ratio of sums) carried onto the new seats | 540,000 (+113%) | Seat-weighted by group, the textbook treatment of a mix shift | The close-outs: the nine routes run at 98–100%, so their load factor saturates at the seats and no carried ratio measures demand |
| 2 | The standard's floor: forecast traffic = last summer's carried passengers plus recorded denials | 70,000 (−72%) | The lowest demand every file of record supports, exactly as the standard defines constrained demand | The change log's nine past upgauges: every first summer carried more than its denials, from 1.6 to 3.1 times them |
| 3 | **Decisive:** the first-summer response measured on the nine past upgauges, 41% of added seats, applied to this summer's 620,000 | **254,000** | — | — |

* **Figure shape.** The corrections walk the figure down (600,000, 540,000, 70,000) and the decisive rung reverses the walk. No other cell
  lands within 36% of the answer.
* **Partial correction priced (L3).** A solver who distrusts the floor but assumes the planners' rule of thumb, denials times one and a half,
  lands at 105,000 (−59%). One who uses the past upgauges but measures their response as a multiple of denials (2.3 on average) lands at
  161,000 (−37%): this summer's routes recorded few denials, because revenue management closed their low fares early last summer, and the
  multiple has a flat loss curve across the nine instances.
* **Grid.** Response basis (route load factor, group load factor, denial floor, denials × 1.5, denials × measured multiple, measured share
  of added seats) × base (last summer, two-summer average) = 12 cells. Every cell without the measured share sits at least 36% from 254,000,
  and the two-summer base moves the measured cell by under 1%, because the routes were full in both summers.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard defines constrained demand and says nothing about the response to added capacity; no document states a
   share of added seats or refers to the change log as evidence.
2. **Reproduction across the natural experiments.** The share-of-added-seats rule reproduces all nine past first summers within 2%; the
   denial floor misses all nine low, by 37–69%; the planners' 1.5 multiple misses eight of nine low; the average multiple of denials misses
   six of nine by more than 15% in both directions, so it reconciles in aggregate and fails row by row. The rule is recovered, not chosen:
   each instance pairs a change-log entry with two close-outs, and nothing labels them as experiments.
3. **No arithmetic symptom.** Seats reconcile to the schedule, passengers to the close-out, denials to the reservation system; every rung's
   figure is internally consistent.
4. **Not a row predicate.** The response comes from before-and-after differences on nine routes, matched to their change-log entries and
   divided by each route's added seats.
5. **The enumeration is arithmetic.** No column says how a route will respond; the share is computed from closed pairs.
6. **No cutover date in any outcome series the forecast reads.** The past upgauges are dated, and each is used as an experiment; this
   summer's are in the future and step nothing in the pack.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The summer close-outs for 2023–2026 (passengers, seats, load factor and denied bookings for every route), with the change log
  marking nine upgauges between them.
* **What it certifies.** The saturation (the nine routes at 98–100% in every summer) and the denial floor as a measure of past constrained
  demand.
* **What it pins.** The first-summer response: 40.8–41.2% of added seats in all nine instances.
* **Twin pair.** Past upgauges on routes 412 and 437 had identical close-outs the summer before: seats, passengers, 99% load factor and
  9,000 recorded denials. Their first summers added 33,000 and 66,000 passengers (2.0× apart), because route 412 added 80,000 seats and route
  437 added 161,000. Every denial rule predicts the two responses equal; only the share of added seats reproduces both.
* **Resemblance points at the decoy.** This summer's routes most resemble the past upgauges in their pre-upgauge close-outs, where load
  factor carried forward would have looked right for exactly one summer.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The planning standard: demand on a constrained route is the lowest figure consistent with every record, carried
  passengers plus denied bookings. The capacity plan gives each route's summer seats and segment group. The summer runs from 1 June to
  31 August, as the close-outs define it.
* **Empirical pins.** The first-summer response share, from the nine past upgauges.
* **Voices.** The head of network planning: "Those routes are full every summer; the new seats will fill." The revenue manager: "Denials
  are the only hard evidence of demand we have." A senior scheduler: "The old hands always took one and a half times denials for spill."
* **Licensed wrong basis.** The planning standard records that the ground-handling contractor sizes its summer contract on the plan's
  carried load factors and will quote against them.

## 8. Determinism by construction

* **Response share.** Nine instances between 40.8% and 41.2%, with mean and median both 41.0%, so the averaging choice moves the figure by
  under 2,500 passengers, inside the committed rounding.
* **First summer.** Every past instance is measured on its first full summer after the change, the same horizon as this summer's.
* **Season.** The close-outs define the summer as June to August; this summer's schedule changes all take effect before 1 June.
* **Route identity.** Each upgauge keeps its route number and city pair, so before-and-after matching has one reading.
* **Rounding.** 0.41 × 620,000 = 254,200, which rounds to 254,000 clear of the bin's edges.

## 9. Prompt sketch and deliverables

> The summer schedule upgauges nine routes, adding 620,000 seats, and the ground-handling contract and the revenue plan both hang on how many
> extra passengers that brings. Network planning says those routes are full every summer, so the new seats will fill. Give me the additional
> passengers over last summer, to the nearest thousand, in one sentence for the plan, and send `upgauge_forecast.xlsx` with the build and the
> sheets below, a chart `upgauge_response.png`, and a one-page `forecast_note.pdf`.

* `upgauge_forecast.xlsx` — the per-route forecast, the punctuality sheet (ask A) and the connections sheet (ask B).
* `upgauge_response.png` — a scatter of the nine past upgauges, added seats against first-summer added passengers, with the fitted 41% line,
  the denial-floor predictions as hollow markers, the twin routes labelled, and this summer's nine routes plotted on the line.
* `forecast_note.pdf` — the committed figure and why carried load factors and denials both miss it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the nine routes and each summer month last year, the on-time departure rate.
  *Device:* a flight that pushed back, returned to the gate and departed again keeps its first pushback time in the departure table, with the
  return recorded in the gate-event table, as the operations data guide documents; timing from the first pushback overstates punctuality on
  five routes. Punctuality enters no part of the passenger forecast.
* **Ask B (device-carried).** For each route, last summer's share of passengers connecting rather than local. *Device:* a passenger on a
  two-segment through flight appears once per segment in the segment table and once in the itinerary table, as the revenue accounting guide
  documents; classifying from segments counts every through passenger as two locals. Segment passenger totals are unchanged.
* **Ask C (validity).** The additional passengers under each of the four rung constructions, and how many of the nine past upgauges each
  construction reproduces within 5%.
* **Decoupling.** Clearing the measured response changes no figure in asks A or B.

## 11. Rubric arithmetic

9 routes × 3 months (ask A) + 9 routes (ask B) + 4 constructions × 2 (ask C) + the committed figure and the nine per-route increments + 5
named chart parts + 3 files ≈ 62 criteria.

## 12. World-building constraints

* Nine routes, 1.24M summer seats last summer at 98–100% load factor; 620,000 seats added; recorded denials total 70,000.
* Additional passengers by rung: 600,000 / 540,000 / 70,000 / 254,000; denials × 1.5 gives 105,000; denials × 2.3 gives 161,000.
* Nine past upgauges: first-summer response 40.8–41.2% of added seats, 1.6–3.1 times recorded denials.
* This summer's routes recorded denials at 11% of added seats, against 13–26% in the past instances.
* The twin routes are identical on every pre-upgauge close-out column.
* Gate returns and through-flight segments touch no seat, passenger or denial count used in the forecast.

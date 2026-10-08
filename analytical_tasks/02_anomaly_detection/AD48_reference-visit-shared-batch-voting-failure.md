# AD48 — Which weather station gets the quarter's reference visit, when two of a station's three sensors can come from the same bad shipment

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Economics · weather-index insurance data |
| Mirrors | Redundant-sensor management where two of three channels can share a defect and outvote the good one (angle-of-attack sensors on aircraft, data-centre temperature probes from one supplier lot, triple-modular redundancy in industrial control), traced through how parts were issued rather than through the readings alone |
| Decision shape | Which of N gets one scarce thing: the quarter's single reference visit (a technician with a reference thermometer, three verified sensors and a new fan) goes to one of five shortlisted stations |
| Committed call | The station visited, and the absolute error removed from its published temperatures over the next policy year, in °C-days |
| Gap · Pattern | Gap 2 (population: which sensors share a batch) over Gap 4 (rule recovered at zero tolerance) · a mixture, not a constant (each station's error mixes its sensors' shipments, so a two-of-three vote can convict the good sensor), with a quiet common-mode trap (aspiration fan failures) below it |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #11 beats the headline trap, misses the quiet one · #17 guesses an attribution the data can settle · #3 stops at a close but inexact match |
| Calibration form | Existing-book actuals: the book of 260 sensors checked against a reference thermometer on past visits, with each sensor's measured error |
| Driving force | Two-of-three voting assumes faults are independent. Sensors reach stations through the depot, which issues stock oldest first, so the sensors fitted on one visit come from the same shipment, and shipment B7 drifts by −0.55°C after its first year. At a station with two B7 sensors the pair agrees, the good sensor disagrees, the vote convicts the good one, and the published mean is off by twice what the vote implies. Which sensors are B7 is the unique assignment, an oldest-first issue run over the depot's deliveries and the swap log, under which all 260 reference checks agree. |

## 1. Situation

An agricultural insurer settles frost and heat-index policies on the published daily temperatures of its 40-station network. Each station
carries three aspirated sensors and publishes their mean. The maintenance plan has one reference visit this quarter: a technician replaces all
three sensors and the fan at one station and removes whatever error the station carries, and the visit goes where it removes the most
absolute error from published temperatures over the next policy year. Five stations are shortlisted. The insurer holds the five-minute data
(three sensor channels and the fan-speed channel), the swap log, the depot's delivery records, neighbouring public stations and the book of
past reference checks. The maintenance contractor trusts its checks on the published value.

## 2. Gate G: why this is legal

* **Litmus.** Every reading is correct for its sensor, every pairwise difference is right, the vote is computed correctly, and the reference
  checks are exact. The network scientist is right that voting finds a single bad sensor. Nothing reported is overturned; the difficulty is
  that faults are not independent, which the readings cannot show on their own.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the contractor's flags. Pairwise voting plus the fan channel, the natural careful build, still
  names C.
* **Instrument repair.** Add a fourth sensor of the same make from the same depot and the vote still fails wherever two of four share B7. The
  difficulty is in where the parts came from.
* **Lens swap.** The naive population is the sensor a vote flags at each station; the answer's is the sensors that share a shipment, a
  different set at two of the five stations, and a different station.

## 3. The driving force

A strong solver sets aside the contractor's anomaly checks against neighbours (a frost hollow is not a fault), takes daily medians of
pairwise differences, convicts the sensor that disagrees with an agreeing pair, and then notices the quiet trap: when a station's fan fails,
all three sensors read high together in sunshine, which no pairwise test can see but the fan-speed channel records. That names C. Every step
is correct, and voting assumes one fault at a time. The reference book disagrees at a handful of stations: there the sensor the vote
convicted was within 0.05°C of the reference and the agreeing pair was 0.55°C low. The depot issues stock oldest first, so one shipment
supplies every sensor fitted on a visit and the visits after it until the shipment runs out. Running that issue order over the depot's
deliveries and the swap log assigns every sensor in the network to a shipment, and B7's sensors are exactly the drifting ones. At E two of
three are B7: the vote calls E's error 0.18°C, and it is 0.37°C.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Contractor's check: published value against neighbouring stations, °C-days beyond its 1.5°C line: A 290, C 230, B 180, D 150, E 120 | A | The contractor's long-standing check on what the insurer actually settles on | The pairwise differences: A's three sensors agree to 0.03°C; A sits in a frost hollow its neighbours do not share |
| 1 | Two-of-three voting on daily median pair differences; error = convicted offset ÷ 3 × 365: B 91, D 67, E 67, A 0, C 0 | B | The textbook fault isolation for triple redundancy | The fan-speed channel: C's fan runs under 1,500 rpm on 40% of afternoons, when all three sensors read high together |
| 2 | Voting plus common-mode fan bias from the fan channel: C 110, B 91, D 67, E 67, A 0 | C | Beats the loud trap and the quiet one | The reference book: at stations like E the convicted sensor matched the reference and the agreeing pair was 0.55°C low |
| 3 | **Decisive:** assign every sensor to a shipment by running the depot's oldest-first issue over deliveries and the swap log, apply each shipment's drift from the book, add fan bias: E 134, C 110, B 91, D 67, A 0 | **E** (5th of 5 on rung 0) | — | — |

* **Position table.** E ranks 5th on rung 0, joint 2nd on rung 1 (B leads it by 1.36×) and joint 3rd on rung 2, and leads only rung 3. Rung
  leaders beat their runners-up by 1.26×, 1.36×, 1.21× and 1.22×.
* **Discriminator dominance.** C carries a 1.64× advantage over E into rung 3 (110 against 67). E's true error is 2.0× what the vote implies
  (two B7 sensors, not one convicted good one) while C's is unchanged, so the net is 2.0 / 1.64 = 1.22×.
* **Partial correction priced (L3).** A solver who finds the B7 drift in the book but assigns batches by install-date window instead of issue
  order puts E's second B7 sensor in a later shipment, keeps E at 67 and names C. A solver who issues newest first names B.
* **Grid.** Check (published value or voting) × fan bias (ignored or measured) × batch assignment (none, date window, oldest first) = 12 cells.
  Published-value cells name A; voting cells name B without fan bias and C with it under no or window assignment; only oldest-first with fan
  bias names E.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The swap log records positions replaced and dates; the delivery records record shipments and batches; no document
   says how stock is issued or connects a batch to drift.
2. **The corpus pins a construction, not a menu (Pattern B).** The oldest-first assignment reproduces all 260 reference checks at zero
   tolerance (every B7 sensor in service over a year reads −0.52 to −0.58°C; every other within ±0.05). Single-fault voting reproduces 241,
   convicting the good sensor at three two-B7 stations; a date-window assignment 223; newest-first 211. The assignment is an inventory run
   over two files, not a parameter.
3. **No arithmetic symptom.** Pair differences, votes, fan readings and the published mean all reconcile; a two-B7 station looks exactly
   like a one-fault station.
4. **Not a row predicate.** Each sensor's shipment depends on every issue before it at its depot, so the assignment is an ordered run over
   deliveries and swaps.
5. **The enumeration is arithmetic.** B7 membership is computed for all 120 sensors; no column holds it.
6. **No cutover date.** B7 sensors went out over seven months and each drifts on its own clock after its first year; no network series
   steps.
7. **Survives deletion.** Remove both voices and the contractor's flags, and voting with fan bias is still the natural build.

## 6. The calibration corpus

* **Form.** The book of 260 sensors checked against a reference thermometer on past visits: station, position, months in service and measured
  error.
* **What it pins.** Shipment drift (B7 −0.55°C after a year, all others negligible) and the oldest-first assignment (above). It also holds one
  past fan failure, confirming the common-mode bias of +1.2°C in sunshine.
* **Every rule exercised.** The book includes one-B7 stations (where voting is right), two-B7 stations (where it convicts the good sensor) and
  a three-B7 station (where it sees no fault at all).
* **Twin pair.** D and E are identical on every voting column: one convicted sensor 0.55°C from an agreeing pair, the same fan record, the
  same neighbours. D's convicted sensor is its single B7 and E's convicted sensor is its single good one, so their true errors are 67 and 134
  °C-days, 2.0× apart, separated only by the shipment assignment.
* **Resemblance points at the decoy.** On every reading-based column E resembles the book's one-fault stations, where voting was right.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The maintenance plan: the reference visit goes where it removes the most absolute error from published temperatures over
  the next policy year. The publication rule (the mean of three sensors). The station readme's channel list, including fan speed. One sentence
  each.
* **Empirical pins.** Shipment drifts and the issue order, from the book; fan bias, from the book's fan case.
* **Voices.** The contractor: "Our checks on the published value have caught every bad station for years." The network scientist: "Two of
  three always finds the bad sensor."
* **Licensed wrong basis.** The plan records that the reinsurer's data auditor reviews stations by anomalies against neighbours and will
  review the visit choice on that basis.

## 8. Determinism by construction

* **Issue order.** Every depot delivery is a single shipment with one batch, and no two shipments arrive on one day, so oldest-first is
  unambiguous.
* **Drift.** B7's drift is flat after twelve months in service (−0.52 to −0.58°C), so next year's error equals today's for every B7 sensor
  already past a year, which includes both of E's.
* **Fan bias.** C's fan-failure afternoons are taken from the fan channel; the bias per failed afternoon comes from the book's fan case.
* **Rounding.** The committed figure is given to the nearest 5°C-days; E's 134 sits clear of C's 110 at either end of the drift range.

## 9. Prompt sketch and deliverables

> We can send the reference technician to one station this quarter, and the contractor has five on its list. The contractor tells me its
> checks on the published value have never missed a bad station. Tell me which station gets the visit and how much error it takes out of the
> published temperatures over the next policy year, in °C-days to the nearest five, in a line for the settlement committee. Send
> `visit_case.xlsx`, a chart `shipment_drift.png`, and a one-page `visit_memo.pdf`.

* `visit_case.xlsx` — the five stations under each rung's basis (ask C), the travel sheet (ask A) and the portal sheet (ask B).
* `shipment_drift.png` — reference-check error against months in service for the 260 checked sensors, coloured by assigned shipment with B7's
  plateau labelled, and a side panel of each shortlisted station's three sensors with the vote's conviction and the true faults marked.
* `visit_memo.pdf` — the committed station and figure, and why each other station falls away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 40 stations, technician travel hours last year from the visit log. *Device:* a trip
  covering two stations logs its travel once against the first station, as the visit log guide says; charging travel per log row loads all of
  it on the first station of each pair. The visit choice never uses the visit log.
* **Ask B (device-carried).** For each of the six agencies that download the network's data, downloads per month last year. *Device:* the
  portal guide lists the user agents of automated harvesters, which are excluded from downloads; counting them inflates four agencies by more
  than half.
* **Ask C (validity).** Each station's figure under each of the four rung bases.
* **Decoupling.** Clearing the shipment assignment and the fan bias changes no figure in asks A or B.

## 11. Rubric arithmetic

40 stations × 1 (ask A) + 6 agencies × 2 (ask B) + 5 stations × 4 bases (ask C) + the committed station, its error removed, the runner-up and
the margin + 5 named chart parts + 3 files ≈ 84 criteria.

## 12. World-building constraints

* Rung figures as in the ladder; E is 5th, joint 2nd (1.36× behind B), joint 3rd and 1st.
* E carries two B7 sensors past a year in service and D one; B has one non-batch sensor at +0.75°C; C's fan fails on 40% of afternoons.
* Oldest-first issue reproduces all 260 checks; the book includes three two-B7 stations and one three-B7 station.
* D and E are identical on every voting and fan column.
* The visit log and the portal log never touch sensor data, the swap log or the depot deliveries.

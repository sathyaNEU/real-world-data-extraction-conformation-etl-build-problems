# RC34 — Which delay cause the airline's reliability programme funds, when a twelve-minute inbound costs connecting customers hours

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Supply Chain & Logistics · airline network operations |
| Mirrors | End-to-end latency triage where a small delay upstream of a fan-out point is multiplied downstream (Amazon fulfilment hub cut-offs, request fan-out in Google and Meta service meshes, parcel-network sort windows), so per-hop delay and customer-felt delay rank causes differently |
| Decision shape | Which of N root causes gets the fix: next season's reliability programme funds one of five delay causes |
| Committed call | The one cause the programme funds, named in a sentence, with each cause's minutes of delay to customers' final destinations last summer |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · Pattern D (two grains, flight and passenger journey, differing in shape because misconnects amplify inbound-to-bank delays), with Pattern B (the published index pins the grain) |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #1 reports a failed back-test, ships anyway · #5 takes the population a flag or filter suggests · #3 stops at a close but inexact match |
| Calibration form | Published control set with a reproduction clause: eight quarters of the customer-delay index for four hubs, which the programme charter requires a ranking basis to reproduce |
| Driving force | A flight delay and a customer's delay to their final destination rank causes differently. An inbound twelve minutes late into Brennan Field's morning connection bank strands its connecting customers for hours, while a Brennan departure twelve minutes late costs its customers twelve minutes. Outstation maintenance sign-offs make the first-wave inbounds that feed the 10:00 and 11:30 banks late. That cause is small in every flight table and the largest at the journey grain. Only the journey construction reproduces the 32 published index cells. |

## 1. Situation

Corvane Air's published on-time rate rose from 76% to 83% after its spring schedule change lengthened block times, yet its customer-delay
index, published quarterly for each of its four hubs, did not improve. Next season's reliability programme funds one fix: Westmarch airspace
de-peaking, spare aircraft for late-aircraft knock-on, a Brennan Field turnaround programme, crew reserves, or night maintenance cover at
the outstations. The programme charter says a ranking of causes may be used only if its delay basis reproduces every published
customer-delay figure of the last eight quarters. The operations vice-president is sure Westmarch's airspace is the problem.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct: flight records, station delay codes, the traffic-management log, rotation chains, booking
  itineraries, re-accommodation records and the published index. The padded schedule really did lift on-time. No one's reading of their
  own figures is overturned. The difficulty is which grain of delay ranks the causes.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete every voice. The natural flight-grain pipeline still ranks Westmarch or Brennan turnarounds first.
* **Instrument repair.** Time every flight to the second and code every delay correctly. A twelve-minute inbound still strands its
  connectors, and the hours they lose exist only at the journey grain.
* **Lens swap.** The naive grain is flights, and the answer's is customer journeys across connections. These are different units, and the
  answer counts customers whose own flight was on time but who missed their connection.

## 3. The driving force

A strong solver starts from the flight records, as every on-time study does. It re-derives the station delay codes under the operations
manual's rule, which counts a delay as airspace only when a traffic-management initiative covered the flight. That turns most of
Westmarch's "airspace" delays into late-aircraft knock-on. It traces knock-on down each aircraft's rotation to its root, and the root
analysis names Brennan Field turnarounds. Every step is correct for flights. The charter, though, ranks on the basis that reproduces the
customer-delay index, and the index counts each customer to their final destination. Brennan's morning banks connect thousands of customers
inside the minimum connection time. A first-wave inbound held twelve minutes at an outstation for a maintenance sign-off misses the bank for
every tight connector aboard, and they arrive hours later on re-accommodation flights. Built per journey, outstation sign-offs cost 22
customer-minutes per flight-minute, and Brennan's own departures cost 4.1.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Flight delay minutes by station delay code | Westmarch airspace (64k minutes, 1.23×) | The regulator's statistics and the station codes, as filed | The manual's coding rule and the traffic-management log: 38k of the coded minutes had no initiative in force |
| 1 | Flight minutes with codes re-derived against the traffic-management log, the population the flag only suggests | Late-aircraft knock-on (90k, 2.37×) | Each code now matches its rule | The rotation chains: knock-on is a symptom, and each late aircraft traces to an earlier root |
| 2 | Knock-on traced down each rotation to its root cause | Brennan turnarounds (93k flight minutes, 2.66×) | Root-caused, exhaustive, and every minute assigned | The charter's reproduction clause: flight minutes, even weighted by passengers aboard, reproduce 19 of the 32 index cells |
| 3 | **Decisive:** delay to final destination per journey, with segments ordered, misconnects tested against minimum connection times and re-accommodated arrivals joined | **Outstation sign-offs (660k customer-minutes, 1.73× Brennan)**, 5th on rung 0 | — | — |

* **Position table.** Outstation sign-offs rank 5th, 5th and 3rd on rungs 0 to 2, and lead only rung 3.
* **Discriminator dominance.** Brennan turnarounds carry a 3.10× flight-minute lead into rung 3. The sign-offs' journey amplification is
  22 against Brennan's 4.1, an edge of 5.37×, above 1.2 × 3.10 = 3.72.
* **Partial correction priced (L3).** A solver who weights flight delay by passengers aboard ranks Brennan first. One who counts a
  misconnected customer's delay only to the missed flight's scheduled departure, not to the re-accommodated arrival, leaves the sign-offs
  at 210k against Brennan's 381k and names Brennan. Neither half names the sign-offs.
* **Grid.** Codes (station or rule) × knock-on (as coded or traced) × grain (flight, passengers aboard, journey) = 12 cells. Only rule codes,
  traced roots and the journey grain name the outstation sign-offs. With station codes, the journey grain names Westmarch at 1.65×.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The charter requires reproduction and names no grain. The index's method is undocumented, and no document says that
   inbound delays into a bank are multiplied.
2. **The control set pins a construction, not a menu.** The journey construction reproduces all 32 published cells exactly. The best rival,
   flight delay × passengers aboard, reproduces 19 of 32 and misses every Brennan bank cell by 18% to 41%, all on the low side, so it fails on
   the total too. The reproducing rule orders each itinerary's segments, tests each connection against the published minimum connection
   time, and joins the re-accommodation record's arrival. It has no parameter to sweep.
3. **No arithmetic symptom.** Flights, codes, rotations, bookings and re-accommodations reconcile under every rung, and flight-grain
   on-time ties to the regulator's figures.
4. **Not a row predicate.** A misconnect is a property of an ordered pair of segments in one itinerary, compared with a connection time for
   that terminal pair, and its cost comes from a third record.
5. **The enumeration is arithmetic.** No flight carries a "stranded connectors" field. The figure is built from journeys.
6. **No cutover date.** The schedule change is dated, and it is the decoy behind the on-time rise. Sign-off delays recur daily.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The published customer-delay index: minutes of delay to final destination per customer, by hub of first connection, for eight
  quarters at four hubs (32 cells).
* **What it pins.** The journey grain, 32 of 32 against the best rival's 19 of 32. The rival's misses run one way, so it also fails on the
  index total, by 23%.
* **Twin pair.** Inbounds CV 1418 and CV 1442 are identical on arrival delay (12 minutes), aircraft, load, connecting-customer count and
  arrival bank. They cost 41k and 19k customer-minutes (2.16×). CV 1418's connectors were booked onto departures inside the minimum
  connection time and CV 1442's onto later ones, so only the journey construction reproduces both.
* **Every rule exercised.** Two quarters include held departures, where Corvane held an outbound for late connectors, and the index counts
  the held flight's own delay. Only the journey construction reproduces them.
* **Resemblance points at the decoy.** The Brennan index cells move quarter to quarter in step with Brennan's turnaround delay minutes, so
  by resemblance Brennan turnarounds drive the index.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The programme charter: "A ranking of causes may be used only if its delay basis reproduces every published customer-delay
  figure for the last eight quarters." The operations manual's coding rule: "A delay is coded to airspace only when a traffic-management
  initiative covered the flight's scheduled time." Airports publish their minimum connection times.
* **Empirical pins.** The journey construction comes from the 32 index cells. Root tracing follows the rotation chain's tail numbers.
* **Voices.** Operations VP: "Westmarch's airspace wrecks every summer; fix that and we fix the network." Brennan hub director: "Our turns
  are the bottleneck." Fleet planning head: "We don't have enough spares. One late aircraft ruins the evening."
* **Licensed wrong basis.** The charter records that the board's operations committee reads reliability from the regulator's flight-level
  on-time statistics and will see the programme proposal on that basis.

## 8. Determinism by construction

* **Connection test.** Every tight connection misses or makes by at least four minutes against the published minimum connection time, so
  second-level timing cannot move a misconnect.
* **Overnights.** Customers re-accommodated next day count to their actual arrival, the convention the index reproduces under. No
  re-accommodation record lacks an arrival.
* **Root tracing.** Late-aircraft delay is attributed to the inbound's root up the tail-number chain. Each knock-on chain resolves within
  three legs to a coded root.
* **Hub of first connection.** Each itinerary's first connecting airport is unambiguous, and no itinerary connects twice at one hub.
* **Maturity.** The summer is complete, and every re-accommodated customer had arrived before the extract.

## 9. Prompt sketch and deliverables

> Next season's reliability money goes to one fix, and I owe the board the cause it should go after by the end of the month. Our operations
> VP is sure Westmarch's airspace is the problem. Name the cause the programme should fund, in a sentence the board can vote on, with each
> cause's delay to customers last summer in thousands of customer-minutes. Send `reliability_case.xlsx`, a chart `cause_delay_grains.png`, and
> a one-page `programme_choice.pdf`.

* `reliability_case.xlsx` — the five causes on every basis, the baggage sheet (ask A), the fuel sheet (ask B) and the index reproduction
  (ask C).
* `cause_delay_grains.png` — paired bars per cause of flight-delay minutes and customer-delay minutes. Brennan's 10:00 bank misconnects are
  annotated with their count, the funded cause is marked, and the title names it.
* `programme_choice.pdf` — the named cause and why each other fix buys less.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each hub and quarter, mishandled bags per 1,000 customers. *Device:* the baggage system writes
  a delayed bag and its later delivery as two records under one tag number, as its dictionary states. Counting records doubles the rate at
  the two hubs with courier delivery. No baggage record enters the delay construction.
* **Ask B (device-carried).** For each of the five fleet types and each quarter, fuel burned per block hour. *Device:* stations record
  uplift in kilograms or litres with a density field, as the fuel manual documents. Mixing units without converting overstates burn for
  the two fleets fuelled mostly at litre stations.
* **Ask C (validity).** For each of the 32 index cells, the published figure beside your construction's.
* **Decoupling.** Clearing the journey construction or the code rule changes no figure in asks A or B.

## 11. Rubric arithmetic

4 hubs × 4 quarters (ask A) + 5 fleets × 4 quarters (ask B) + 32 index cells (ask C) + the named cause, the five journey-grain sizes and the
winning margin + 5 named chart parts + 3 files ≈ 83 criteria.

## 12. World-building constraints

* Flight minutes by rung (thousands): Westmarch 64 / 26 / 26, knock-on 52 / 90 / 0, Brennan 38 / 38 / 93, crew 21 / 21 / 35, sign-offs
  9 / 9 / 30.
* Journey amplification is sign-offs 22, Westmarch 12, knock-on 8, crew 5 and Brennan 4.1 customer-minutes per flight-minute. Under
  station codes the journey grain names Westmarch.
* The index has 32 cells, reproduced 32 / 32 by journeys and 19 / 32 by passengers aboard, with misses all low.
* CV 1418 and CV 1442 are identical on every flight-level column.
* Bag records and fuel units never touch flights, itineraries or re-accommodations.

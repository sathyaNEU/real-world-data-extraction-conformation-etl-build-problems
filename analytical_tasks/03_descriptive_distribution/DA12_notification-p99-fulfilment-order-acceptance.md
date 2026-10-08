# DA12 — The order-notification P99 a commerce platform writes into its merchant agreement, when fulfilment-service merchants acknowledge an order through a second log keyed to fulfilment orders

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Product Analytics · commerce-platform reliability and merchant SLAs |
| Mirrors | Committing an end-to-end latency figure for an order whose completion is recorded in a second system keyed to a sub-unit (fulfilment-service apps accepting split orders on storefront platforms, vendor purchase-order acknowledgements per shipment at Amazon, marketplace orders split across fulfilment centres at Amazon and Walmart), where the delivery log's 2xx looks like the end of every order |
| Decision shape | One figure committed at a date: the notification P99 in the merchant agreement sent to legal on 3 March 2027 |
| Committed call | The 99th-percentile time from a shopper's payment submission to the merchant's acknowledgement of the order, in whole seconds |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · E20, each fulfilment-service order's acknowledgement reached through the Accept log's fulfilment-order IDs and the fulfilment-order table, never through the event key, with E02 (the checkout, which no file stores) below it and a counterparty file blind to fulfilment-service apps (L1) |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #18 joins only on the visible key · #2 counts file rows instead of the real unit · #13 validates on one population, applies to another · #7 uses the ready-made measure |
| Calibration form | Counterparty acknowledgement file: the enterprise merchants' nightly files, each order notification with the merchant's own receipt time |
| Driving force | 2,300 merchants run their orders through fulfilment-service apps. Their endpoints answer 202 Accepted the moment a notification reaches the app's queue, and the app then accepts each of the order's fulfilment orders, one per fulfilment location, through the Accept API. Each acceptance is logged against its fulfilment-order ID, which only the fulfilment-order table ties to an order. Every order still has a 2xx response under its event ID, so the event-keyed join looks complete. The 18% of orders on these apps are taken whole 15 seconds to 12 minutes after submission, and the split ones hold the 99th percentile. The enterprise merchants' files certify the event join exactly, because every enterprise integration is synchronous. |

## 1. Situation

A storefront platform is renewing its merchant agreement, and legal needs the order-notification figure by 3 March. The SLA document
measures each order from the shopper's payment submission to the merchant's acknowledgement of the order, over the last complete
quarter, and the platform commits to the 99th percentile. The pack holds the distributed traces of the checkout API, the order event log,
the notification delivery log (each attempt with its delivery ID, event ID, endpoint, response status and time), the fulfilment-order
table, the platform's API access log, the merchant integration register, the merchant terms, the integration guide, the API reference,
and the nightly acknowledgement files that 210 enterprise merchants send back. The SRE dashboard shows the checkout API's P99 at 0.8
seconds.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the traces, the events, every delivery attempt and its response, every acceptance and the
  enterprise merchants' receipt times. The SRE dashboard's P99 is a true statement about API requests, and a 202 is a true statement that
  a queue received the notification. Nobody's reading of their own numbers is overturned. The difficulty is where an order's
  acknowledgement is recorded and what unit it is recorded against.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the SRE lead's view and the payments partner's licensed basis. The event-keyed join still gives every order a
  2xx response, and the enterprise files still confirm it to the millisecond.
* **Instrument repair.** Clean-data test. No file is suspect. The delivery log records every attempt's HTTP response, complete, and the
  integration guide says a fulfilment-service endpoint answers 202 on receipt, so the 202 is a correct record of a different event, not a
  narrower record of acceptance. The Accept log records every acceptance, complete, against its fulfilment-order ID, and the
  fulfilment-order table maps every fulfilment order to its order. No key is blank, no file is stale, and the instrument that records the
  end event directly already ships, keyed to the fulfilment order. Nothing is left to fill, correct or replace: rung 0 returns 0.8 s,
  rung 1 3.1 s and rung 2 5.9 s, the answer stays 412 s, and building each order's acknowledgement as the last acceptance over its
  fulfilment orders is still needed.
* **Lens swap.** The two reads end on different events. For 18% of orders the event-keyed join ends at a 202 queue receipt 2 to 4 seconds
  after submission, and the SLA ends when the last of the order's fulfilment orders is accepted, 15 seconds to 12 minutes later, in
  another log.

## 3. The driving force

A strong solver moves from requests to checkouts: it links each submission trace to its order's confirmed event and then to the
notification delivery carrying that event ID, taking the first 2xx response as the integration guide's webhook chapter says. Checked
against the enterprise merchants' own receipt times, the construction matches all 1.7 million of their orders, and the P99 comes out at
5.9 seconds. But the guide has a second chapter. 2,300 merchants run their orders through fulfilment-service apps, whose endpoints answer
202 Accepted as soon as a notification reaches the app's queue. The platform has already split each order into one fulfilment order per
fulfilment location, and the app accepts each one through the Accept API when that location's system takes it. A second warehouse that works in batches accepts minutes later. The Accept log carries only the fulfilment-order ID. Joined on event
ID, every order has its 2xx and nothing looks missing. Built through the fulfilment-order table, the merchant terms' acknowledgement (the
whole order taken) arrives 15 seconds to 12 minutes after submission for 18% of orders, and the split orders hold the 99th percentile.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | P99 of the checkout API's request spans (the SRE dashboard's figure) | 0.8 s (−99.8%) | The platform's own latency instrument, clean and complete | The SLA measures each order to the merchant's acknowledgement, and a submission returns before payment completes |
| 1 | Checkouts: submission trace linked to the order's confirmed event by order ID (E02) | 3.1 s (−99.2%) | The order as the unit, timed by the platform's own record | The SLA ends at the merchant, and the notification is dispatched after the confirmed event |
| 2 | Checkouts to the first 2xx response of the notification delivery carrying the event ID | 5.9 s (−98.6%) | Reproduces every enterprise merchant's receipt time exactly | The integration register: 2,300 merchants are on fulfilment-service apps, whose endpoints answer 202 on queue receipt |
| 3 | **Decisive:** for fulfilment-service merchants, checkouts to the last Accept call over the order's fulfilment orders (Accept log, then the fulfilment-order table); for the rest, the webhook's 2xx | **412 s** | — | — |

* **Figure shape.** Every correction lengthens the figure, and the answer is the maximum cell. A merchant agreement written at any lower
  rung commits to a P99 the platform misses every quarter.
* **Partial correction priced (L3).** A solver who finds the Accept log but takes each order's first acceptance, as if one location's
  acceptance acknowledged the order, lands at 104 s (−74.8%). One who joins the Accept log only where an order has a single fulfilment
  order, and keeps the 202 for the split ones, lands at 97 s (−76.5%). One who drops the fulfilment-service orders as unmeasured lands at
  6.2 s. Only the last acceptance over every fulfilment order reaches the split orders' tail, where the 99th percentile falls.
* **Grid.** End event (API response, confirmed event, webhook 2xx, first acceptance, single-location acceptance, last acceptance) × the
  fulfilment-service orders (kept or dropped) gives 8 distinct cells. The nearest wrong cell is 104 s (−74.8%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The SLA says "the merchant's acknowledgement of the order". The merchant terms say an order is acknowledged when
   the merchant's systems have taken the whole order. The integration guide's second chapter says a fulfilment-service app accepts each
   fulfilment order through the Accept API, and the API reference says Accept takes a fulfilment-order ID. No document joins them, or says
   where an order's acknowledgement is found.
2. **Corpus blind for a computable reason.** *In every order in the enterprise merchants' files the webhook's 2xx was the acknowledgement,
   because all 210 enterprise merchants run synchronous integrations behind their own order systems, and none uses a fulfilment-service
   app.* On all 1.7 million of their orders, rungs 2 and 3 coincide.
3. **No arithmetic symptom.** Every order has exactly one notification with a 2xx under its event ID, every event joins, every fulfilment
   order is accepted, and no key repeats. The Accept log appears only to a solver who opens the API access log.
4. **Not a row predicate.** An order's acknowledgement is the latest acceptance over its fulfilment orders, reached through two joins
   (Accept log to fulfilment order, fulfilment order to order). No row carries both the order and its acknowledgement.
5. **The enumeration is arithmetic.** 756,000 fulfilment-service orders and their 1,020,000 fulfilment orders are resolved by the join
   alone.
6. **No cutover date.** Fulfilment-service merchants have run on the platform for years, warehouse batch cycles recur every day, and no
   latency series steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, the event key still looks like the whole join.

## 6. The calibration corpus

* **Form.** The enterprise merchants' nightly acknowledgement files: 1.7 million order notifications, each with the event ID and the
  merchant's receipt timestamp, sent back for reconciliation.
* **What it certifies.** The checkout unit and the event join. Submission to the event-keyed delivery's first 2xx reproduces every
  enterprise receipt within the files' 10 ms timestamp resolution. Ending at the confirmed event misses all of them by the dispatch delay.
* **What it is blind to.** Fulfilment-service acceptance (above).
* **Twin pair.** Orders O-41806 and O-63355 are identical on every column the event-keyed join shows: merchant, submission hour, confirmed
  event at 2.9 seconds, webhook 202 at 3.4 seconds. O-41806 has one fulfilment order, accepted at 198 seconds. O-63355 has two, accepted
  at 198 and 401 seconds (2.0×). Only the fulfilment-order table and the Accept log separate them.
* **Resemblance points at the decoy.** The quarter's latency profile up to the 94th percentile most resembles the enterprise merchants',
  the population in which the webhook's 2xx is the acknowledgement.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The SLA document: "Notification latency is measured for each order from the shopper's payment submission to the
  merchant's acknowledgement of the order, over the last complete quarter, and the platform commits to its 99th percentile in whole
  seconds." The merchant terms: "A merchant has acknowledged an order when its systems have taken the whole order." The integration
  guide, webhook chapter: "Respond with a 2xx to acknowledge." Its fulfilment-service chapter: "Answer 202 Accepted at once, and accept
  each fulfilment order through the Accept API when your location has taken it."
* **Empirical pins.** The checkout construction, from the enterprise files.
* **Voices.** The SRE lead: "The tracing dashboard already shows checkout latency; it's been under a second all quarter." The partnerships
  director: "Merchants judge us on how fast the order reaches them. Our enterprise feeds prove we're quick."
* **Licensed wrong basis.** The SLA document records that the payments partner measures notification latency to the first delivery
  response and will publish its own figure.

## 8. Determinism by construction

* **Clock.** The traces, the delivery log and the API access log share one platform clock. Enterprise receipt times match the platform's
  response times within 10 ms, so no clock offset is needed.
* **Percentile.** The 99th percentile sits at 412.3 seconds under nearest-rank and interpolated conventions alike, inside a dense band of
  split orders' last acceptances, and no convention moves it across a whole second.
* **Completion.** Every fulfilment order in the quarter was accepted within 12 minutes, no order was cancelled or edited before
  acceptance, and no acceptance falls outside the quarter of its order's submission.
* **Retries.** A failed delivery is retried under the same event ID, so the first 2xx on the event key is the webhook's acknowledgement.
  Every fulfilment-service endpoint answered 202 on its first attempt.

## 9. Prompt sketch and deliverables

> What notification P99 can we put in the merchant agreement? Legal needs the figure by 3 March, and our SRE lead's view is that the
> tracing dashboard already shows it. Give me the P99 in whole seconds, as the sentence that goes into the agreement, and send
> `sla_measurement.xlsx` with the build and the sheets below, plus `notification_latency.png`.

* `sla_measurement.xlsx` — the order build, the four rung constructions with their match counts against the enterprise files (ask C),
  the authorisation sheet (ask A) and the plan sheet (ask B).
* `notification_latency.png` — the latency distribution's upper tail on a log axis under the event-keyed and the acceptance-built
  constructions, the 99th-percentile line labelled for each, synchronous, single-location and split fulfilment-service orders in separate
  colours, and the twin orders marked.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Authorisation approval rate for each of six payment methods in each month of the quarter.
  *Device:* a soft decline retried by the platform's smart retry is logged as a second authorisation on the same payment intent, as the
  payments guide documents. Counting attempts, not intents, understates approval by 2 to 8 points in 14 of the 18 cells.
* **Ask B (device-carried).** Active merchants on each of the four plans at the end of each month of the quarter. *Device:* a merchant
  changing plan mid-month keeps a row under each plan for that month, with an effective date, as the billing data dictionary documents.
  Counting both rows overstates 9 of the 12 cells.
* **Ask C (validity).** The P99 under each of the four rung constructions, the share of orders on fulfilment-service apps, each
  construction's match count against the enterprise files, and the twin orders' acknowledgement times.
* **Decoupling.** The authorisation log and the billing records share no row with the delivery log, the Accept log or the
  fulfilment-order table. Clearing the acceptance build changes no figure in asks A or B.

## 11. Rubric arithmetic

6 payment methods × 3 months (ask A) + 4 plans × 3 months (ask B) + 4 constructions × 2, the fulfilment-service share and the twin
orders' times (ask C) + the committed P99 + 4 named chart parts + 2 files ≈ 48 criteria.

## 12. World-building constraints

* 4.2 million orders in the quarter: 82% to synchronous webhooks, 18% (756,000) to fulfilment-service apps from 2,300 merchants. Of the
  latter, 70% have one fulfilment order and 30% two or three, 1,020,000 fulfilment orders in all.
* Acceptance times: single fulfilment orders 15 to 120 seconds after submission; split orders' first acceptance 15 to 120 seconds and
  last acceptance 60 seconds to 12 minutes.
* P99 by rung is 0.8 / 3.1 / 5.9 / 412 seconds. The partial cells are 104 s (first acceptance), 97 s (single-location joins only) and 6.2
  s (fulfilment-service orders dropped).
* The 210 enterprise merchants carry 1.7 million orders, all on synchronous integrations. Their files match rungs 2 and 3 exactly.
* O-41806 and O-63355 are identical on every event-keyed column; their acknowledgements fall at 198 and 401 seconds.
* The authorisation log and the billing records touch no delivery, acceptance or fulfilment-order row.

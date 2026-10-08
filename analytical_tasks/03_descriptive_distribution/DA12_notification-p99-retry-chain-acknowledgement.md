# DA12 — The order-notification P99 a commerce platform writes into its merchant agreement, when the slow acknowledgements sit behind retries the event key never reaches

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Product Analytics · commerce-platform reliability and merchant SLAs |
| Mirrors | Committing an end-to-end latency figure for an event that completes across asynchronous hops linked by a second identifier (webhook delivery SLAs at large payment and storefront platforms, order-event delivery to sellers through marketplace APIs at Amazon, push-notification delivery at Apple and Google) |
| Decision shape | One figure committed at a date: the notification P99 in the merchant agreement sent to legal on 3 March 2027 |
| Committed call | The 99th-percentile time from a shopper's payment submission to the merchant's successful acknowledgement of the order notification, in whole seconds |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · E20, the successful acknowledgement reached through the retry chain's parent-delivery IDs, with E02 (the checkout, which no file stores) below it and a counterparty file blind to retries (L1) |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #18 joins only on the visible key · #2 counts file rows instead of the real unit · #13 validates on one population, applies to another · #7 uses the ready-made measure |
| Calibration form | Counterparty acknowledgement file: the enterprise merchants' nightly files, each order notification with the merchant's own receipt time |
| Driving force | A first delivery that a merchant endpoint rejects is retried under a new delivery ID carrying only its parent's delivery ID, not the event ID. Every order still has a first delivery with a response time under its event ID, so the event-keyed join looks complete. The 3.0% of checkouts whose first delivery failed are acknowledged 30 to 240 seconds later, through a chain the explicit key never reaches, and they hold the 99th percentile. The enterprise merchants' files certify the event join exactly, because their dedicated endpoints never failed a first delivery. |

## 1. Situation

A storefront platform is renewing its merchant agreement, and legal needs the order-notification figure by 3 March. The SLA document
measures each order from the shopper's payment submission to the merchant's acknowledgement of the order notification, over the last
complete quarter, and the platform commits to the 99th percentile. The pack holds the distributed traces of the checkout API, the order
event log, the notification delivery log (each attempt with its delivery ID, event ID, parent delivery ID, endpoint, response status and
time), the merchant integration guide, the webhook service runbook, and the nightly acknowledgement files that 210 enterprise merchants
send back. The SRE dashboard shows the checkout API's P99 at 0.8 seconds.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the traces, the events, every delivery attempt and its response, and the enterprise merchants'
  receipt times. The SRE dashboard's P99 is a true statement about API requests, and nobody's reading of their own numbers is overturned.
  The difficulty is the unit the SLA measures and where its end event sits.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the SRE lead's view and the payments partner's licensed basis. The event-keyed join still gives every order a
  delivery with a response time, and the enterprise files still confirm it to the millisecond.
* **Instrument repair.** Make every log complete; each one already is. A retry is a real new delivery, logged as the runbook describes.
  The order's acknowledgement lives on a different row from its event, two or more hops away, and no better delivery log puts them on one
  row.
* **Lens swap.** The two reads end on different events. For 3.0% of checkouts the event-keyed join ends at a rejection 1 to 6 seconds
  after submission, and the SLA ends at an acceptance 30 to 240 seconds later, on another delivery.

## 3. The driving force

A strong solver moves from requests to checkouts: it links each submission trace to its order's confirmed event and then to the
notification delivery carrying that event ID. Checked against the enterprise merchants' own receipt times, the construction matches all
1.7 million of their orders. The P99 comes out at a few seconds. But the integration guide counts only a 2xx response as an acknowledgement,
and a merchant endpoint that answers 503 or times out is retried by the webhook service at 30, 60, 120 and 240 seconds. Each retry is a new
delivery whose only link back is its parent delivery ID. The event ID sits on the first attempt alone. Joined on event ID, every order still
has a first attempt and a response, so nothing looks missing. The 3.0% whose first attempt failed are acknowledged on the first or a later
retry, reached only by walking the parent chain. They are the slowest 3% of checkouts, so they hold the 99th percentile.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | P99 of the checkout API's request spans (the SRE dashboard's figure) | 0.8 s (−98.7%) | The platform's own latency instrument, clean and complete | The SLA measures each order to the merchant's acknowledgement, and a submission returns before payment completes |
| 1 | Checkouts: submission trace linked to the order's confirmed event by order ID (E02) | 3.1 s (−95.1%) | The order as the unit, timed by the platform's own record | The SLA ends at the merchant, and the notification is dispatched after the confirmed event |
| 2 | Checkouts to the response of the notification delivery carrying the event ID | 5.9 s (−90.6%) | Reproduces every enterprise merchant's receipt time exactly | The integration guide counts only a 2xx response as an acknowledgement, and 3.0% of first attempts answered 5xx |
| 3 | **Decisive:** checkouts to the first 2xx response, following retries through parent delivery IDs | **63 s** | — | — |

* **Figure shape.** Every correction lengthens the figure, and the answer is the maximum cell. A merchant agreement written at any lower
  rung commits to a P99 the platform misses every quarter.
* **Partial correction priced (L3).** A solver who sees the 5xx responses and drops those orders as unacknowledged lands at 5.6 s. One who
  follows a single retry hop and drops the rest lands at 33 s (−48%), because the 99th percentile sits among second retries. Two hops
  lands at 34 s. Only the full chain reaches the second-retry group, where the 99th percentile falls.
* **Grid.** End event (API response, confirmed event, first response, first 2xx on the event key, first 2xx through the chain) × retry
  depth gives 7 distinct cells. The nearest non-answer cell is 34 s (−46%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The SLA says "the merchant's acknowledgement". The integration guide defines acknowledgement as a 2xx response.
   The runbook says a retry points at its parent. No document joins the three or says where an order's acknowledgement is found.
2. **Corpus blind for a computable reason.** *In every order in the enterprise merchants' files the first delivery was acknowledged with
   a 2xx, because enterprise integrations run on dedicated endpoints with no failed first attempt in the quarter.* On all 1.7 million of
   their orders, rungs 2 and 3 coincide.
3. **No arithmetic symptom.** Every order has exactly one first attempt under its event ID, every event joins, and no key repeats. The
   retries' null event IDs appear only to a solver who starts from the delivery log rather than from the orders.
4. **Not a row predicate.** An order's acknowledgement is found by walking parent delivery IDs from its first attempt to the first 2xx, a
   recursive chain of variable depth. No row carries both the order and its acknowledgement.
5. **The enumeration is arithmetic.** 126,000 retried orders and their chains of one to five attempts are resolved by the walk alone.
6. **No cutover date.** Merchant endpoint failures are scattered through the quarter, and no latency series steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, the event key still looks like the whole join.

## 6. The calibration corpus

* **Form.** The enterprise merchants' nightly acknowledgement files: 1.7 million order notifications, each with the event ID and the
  merchant's receipt timestamp, sent back for reconciliation.
* **What it certifies.** The checkout unit and the event join. Submission to the event-keyed delivery's response reproduces every
  enterprise receipt within the files' 10 ms timestamp resolution. Ending at the confirmed event misses all of them by the dispatch delay.
* **What it is blind to.** Retries (above).
* **Twin pair.** Orders C-118 and C-406 are identical on every column the event-keyed join shows: merchant, submission time, confirmed
  event, first delivery answered 503 at 1.8 seconds. One was acknowledged on the first retry at 31.8 seconds and the other on the second
  retry at 61.8 seconds (1.9×). Only the parent chain separates them.
* **Resemblance points at the decoy.** The quarter's latency profile up to the 97th percentile most resembles the enterprise merchants',
  the population in which the first response is the acknowledgement.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The SLA document: "Notification latency is measured for each order from the shopper's payment submission to the
  merchant's acknowledgement of the order notification, over the last complete quarter, and the platform commits to its 99th percentile
  in whole seconds." The integration guide: "An acknowledgement is a 2xx response." The runbook: "A retry is a new delivery whose parent
  delivery ID points at the attempt it repeats."
* **Empirical pins.** The checkout construction, from the enterprise files.
* **Voices.** The SRE lead: "The tracing dashboard already shows checkout latency; it's been under a second all quarter." The partnerships
  director: "Merchants judge us on how fast the order reaches them. Our enterprise feeds prove we're quick."
* **Licensed wrong basis.** The SLA document records that the payments partner measures notification latency to the first delivery
  response and will publish its own figure.

## 8. Determinism by construction

* **Clock.** All platform logs share one clock. Enterprise receipt times are taken at the merchant, and they match the platform's
  response times within 10 ms, so no clock offset is needed.
* **Percentile.** Nearest-rank and interpolated 99th percentiles fall within the second-retry group (61 to 67 seconds) and round to 63.
* **Abandoned chains.** No order in the quarter exhausted the retry schedule unacknowledged, so the full chain always ends in a 2xx.
* **Quarter.** Orders are assigned by submission time. No chain crosses the quarter boundary.

## 9. Prompt sketch and deliverables

> What notification P99 can we put in the merchant agreement? Legal needs the figure by 3 March, and our SRE lead's view is that the
> tracing dashboard already shows it. Give me the P99 in whole seconds, as the sentence that goes into the agreement, and send
> `sla_measurement.xlsx` with the build and the sheets below, plus `notification_latency.png`.

* `sla_measurement.xlsx` — the order build, the four rung constructions with their match counts against the enterprise files (ask C),
  the authorisation sheet (ask A) and the plan sheet (ask B).
* `notification_latency.png` — the latency distribution's upper tail on a log axis under the event-keyed and chain-followed
  constructions, the 99th-percentile line labelled for each, the retry groups shaded at 30, 60, 120 and 240 seconds, and the twin orders
  marked.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Authorisation approval rate for each of six payment methods in each month of the quarter.
  *Device:* a soft decline retried by the platform's smart retry is logged as a second authorisation on the same payment intent, as the
  payments guide documents. Counting attempts, not intents, understates approval by 2 to 8 points in 14 of the 18 cells.
* **Ask B (device-carried).** Active merchants on each of the four plans at the end of each month of the quarter. *Device:* a merchant
  changing plan mid-month keeps a row under each plan for that month, with an effective date, as the billing data dictionary documents.
  Counting both rows overstates 9 of the 12 cells.
* **Ask C (validity).** The P99 under each of the four rung constructions, the share of orders whose notification was retried, and each
  construction's match count against the enterprise files.
* **Decoupling.** The authorisation log and the billing records share no row with the delivery log. Clearing the retry-chain walk
  changes no figure in asks A or B.

## 11. Rubric arithmetic

6 payment methods × 3 months (ask A) + 4 plans × 3 months (ask B) + 4 constructions × 2 and the retried share (ask C) + the committed P99
and the twin orders' times + 4 named chart parts + 2 files ≈ 47 criteria.

## 12. World-building constraints

* 4.2 million orders in the quarter. First attempts answered 2xx for 97.0%. Retries succeeded on the first retry for 1.65% of orders, the
  second for 0.90%, the third for 0.30% and the fourth or later for 0.15%.
* P99 by rung is 0.8 / 3.1 / 5.9 / 63 seconds. The partial cells are 5.6, 33 and 34 seconds.
* The 210 enterprise merchants carry 1.7 million orders, all first attempts answered 2xx. Their files match rungs 2 and 3 exactly.
* C-118 and C-406 are identical on every event-keyed column.
* The authorisation log and the billing records touch no delivery row.

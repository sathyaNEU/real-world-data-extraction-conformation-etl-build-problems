# FC32 — How many of six overflow warehouse blocks to take up for January to June after the tariff rush, when the honest error band leaves none of them clearing the leasing test

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Supply Chain & Logistics · port-adjacent warehousing |
| Mirrors | Committing to optional capacity after a demand pull-forward (retailers' overflow warehousing after tariff-driven front-loading, cloud capacity reservations after a usage spike, airline wet-leases ahead of a demand pulse), where the forecast's own residuals make the commitment look safe and the record of past pull-forwards does not |
| Decision shape | An allocation under a cap: up to six 4,000-position blocks at the industrial park, or none |
| Committed call | The number of blocks to take up by 15 December (zero to six), with the lower edge of the January overflow interval that decides it |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · hold forced by a computed blocking quantity (Part 6.4), with two grains both flawless (Pattern D) at rung 2 |
| Gate G mechanism | signal_vs_noise_or_hold, with forecasting support |
| Measured traps engaged | #1 reports a failed back-test, ships anyway · #13 validates on one population, applies to another · #2 counts file rows instead of the real unit |
| Calibration form | Existing-book actuals: three years of monthly TEU and pallet-position actuals for the 31 existing customers, including both earlier tariff rushes |
| Driving force | The leasing policy takes a block only if January's overflow, at the lower edge of its 80% interval, would fill three quarters of it. A model's own residuals come from calm months and give a band of ±17%. The existing book's actuals one month after each earlier rush ended show how far the drawdown of front-loaded stock can run either way: ±87% at that horizon. On that band the lower edge of January's overflow is 1,600 pallets against the 3,000 the first block needs, so every block fails the test on the same number. |

## 1. Situation

A third-party logistics operator near the San Pedro Bay ports runs 40,000 pallet positions across its own buildings. It holds an option
on six overflow blocks of 4,000 positions each at a nearby industrial park for January to June, at $1.1 million a block, exercisable until
15 December. For three months customers have front-loaded imports ahead of a tariff increase, and the buildings are nearly full. The
leasing policy takes a block only if the peak-month overflow, at the lower edge of its 80% forecast interval, would fill at least three
quarters of it. The landlord re-offers any unexercised blocks at a premium in April. The pack holds port TEU statistics, the existing
book's monthly TEU and pallet-position actuals, customers' December booking notices and the leasing policy.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the TEU counts, the pallet positions, the bookings and the policy's thresholds. Operations is right
  that the rush stock is real and that the buildings are full. No reported number is overturned. The difficulty is how wide January's
  forecast band honestly is one month after a rush, which only the existing book's past rushes can say.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete operations' view and every voice. The pallet-grain payback forecast still produces a confident January figure,
  its residual band is still narrow, and the policy's test on that band still takes two blocks.
* **Instrument repair.** Imagine perfect daily stock records for every customer. January has not happened, and the spread of drawdowns
  after past rushes is a property of how customers unwind front-loaded stock, not of how well stock is measured.
* **Lens swap.** The naive read and the answer differ in moment: forecast errors drawn from calm months, against the errors the book
  actually showed one month after a rush ended, the moment the decision sits in.

## 3. The driving force

A strong solver separates the rush from the trend, conserves the front-loaded volume so it is paid back over the following months, converts
TEU to pallet positions customer by customer because the policy counts positions, and finds January's overflow peaking at 12,400 pallets.
It then runs the policy's test with the band its model's residuals give, about ±17%, and takes two blocks. Each step is correct. The band
is not. The model's residuals are drawn from 33 months in which nothing was being unwound. The existing book went through two earlier
rushes, and one month after each ended the realised overflow ran from 13% to 187% of what the same model forecast at the time, because
customers draw down front-loaded stock at different speeds and the speed is not visible a month in. At the horizon the decision sits at,
the 80% band is ±87%. Its lower edge is 1,600 pallets of overflow, and the first block needs 3,000.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | TEU trend fitted through the rush, at the network-average 4.1 pallets per TEU, with the model's residual band | 4 blocks (lower edge 18,500) | The port series the industry plans on, and the policy's test applied as written | The existing book: in both earlier rushes every front-loaded TEU was paid back within four months, so the rush is not growth |
| 1 | Baseline plus pull-forward and an equal payback, in TEU, at 4.1 pallets per TEU | 1 block (lower edge 6,100) | Conserves volume, as the earlier rushes did | The policy counts pallet positions, and the existing book shows furniture and appliance customers, who led this rush, at 1.6 times the average pallets per TEU |
| 2 | The same payback built in pallet positions customer by customer, with the model's residual band (±17%) | 2 blocks (lower edge 10,300) | Right volume, right unit, right timing, and the policy's test run on the model's own band | The existing book one month after each earlier rush ended: realised overflow ran from 13% to 187% of the forecast made at the time |
| 3 | **Decisive:** the policy's test run on the band the existing book's post-rush errors give at a one-month horizon (±87%), which no block clears | **Hold: no block now** (lower edge 1,600 against 3,000) | — | — |

* **The blocking quantity.** January's overflow point forecast is 12,400 pallets. The 80% band from the 24 customer-episodes of post-rush
  error at a one-month horizon runs from 1,600 to 23,200. The first block needs 3,000 at the lower edge; the second 7,000. Every block
  fails on the same number, so the answer is a hold, not a smaller pick.
* **Falsifiability.** The hold would have been one block if the post-rush band's lower half-width had been under 76% of the point (lower
  edge at least 3,000), and two blocks under 44%. A fitted normal on the same errors gives a lower edge of 2,100, also short.
* **Partial correction priced (L3).** A solver who uses post-rush errors but from all horizons pooled gets ±52% and takes one block. One
  who back-tests the earlier rushes in TEU rather than pallets gets ±61% and also takes one block. Neither half lands on
  the hold.
* **Grid.** Volume model (trend, payback) × unit (TEU at the average ratio, pallets by customer) × band (model residuals, pooled
  post-rush, one-month post-rush) = 12 cells. The cells name between one and five blocks; only the payback in pallets with the one-month
  post-rush band holds. The nearest wrong cell is one block, and reaching it takes pooling the post-rush errors across horizons.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy names an 80% interval and its lower edge; it says nothing about which errors build it. No document
   relates forecast error to the months after a rush.
2. **Corpus blind for the model, decisive for the band.** The existing book certifies the payback and the unit: *in every closed month
   outside the two post-rush windows the payback model's error was within ±17%, because nothing was being unwound;* only the 24 post-rush
   customer-episodes carry the error the decision faces, and nothing labels them.
3. **No arithmetic symptom.** TEU, pallets and bookings reconcile on every rung, and the residual band is computed correctly from the model
   it belongs to.
4. **Not a row predicate.** The band needs a rolling-origin back-test of the payback model on the existing book, its errors grouped by
   months since a rush ended, and quantiles taken at the decision's horizon.
5. **The enumeration is arithmetic.** Which months are post-rush is computed from each episode's end; no column marks them.
6. **No cutover date in the decisive cause.** The rushes are dated and loud, and they sit at rungs 0 and 1. The blocking quantity is a
   spread of drawdown speeds, which steps no series.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** Monthly TEU and pallet-position actuals for the 31 existing customers over three years, spanning two earlier tariff rushes
  (24 customer-episodes, each with the months after the rush ended).
* **What it certifies.** Volume conservation (every front-loaded TEU paid back within four months in both rushes) and the unit
  conversion (each customer's pallets per TEU, from 2.2 for electronics to 6.6 for furniture), so rungs 1 and 2 are confirmed.
* **What it pins.** The one-month post-rush error distribution of the payback model: 10th percentile 13% of forecast, 90th percentile
  187%.
* **Twin pair.** Customers Brightwater Home and Kessler Furnishings each front-loaded 2,900 TEU in the second rush, with identical December
  bookings and identical pallets per TEU. One month after that rush ended, their stock above contracted positions was 600 and 1,400 pallets (2.3× apart), because one
  drew its stock down in six weeks and the other held it for four months. Nothing visible a month in separates them, which is the hold's
  reason in miniature.
* **Resemblance points at the decoy.** This rush's size and customer mix most resemble the second earlier rush, whose mean outcome the
  pallet-grain payback forecast matched to within 4%.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The leasing policy: a block is taken only if the peak-month overflow, at the lower edge of its 80% forecast interval,
  would fill at least three quarters of it. Warehouse capacity is planned and leased in pallet positions. The option: six blocks of 4,000
  positions, $1.1 million each for January to June, exercisable until 15 December.
* **Empirical pins.** Pallets per TEU by customer, and the payback, from the existing book. The post-rush error distribution, from the
  existing book's rolling-origin back-test.
* **Voices.** The operations director: "The rush stock will keep us full into spring; we'll need every block." The network planner: "The
  port numbers are the only forecast the industry trusts." The CFO: "If the model says two blocks, take two and stop guessing."
* **Licensed wrong basis.** The leasing policy records that the park's landlord sizes its re-offer premium from port TEU forecasts and will
  present them in the April negotiation.

## 8. Determinism by construction

* **Peak month.** January is the peak overflow month under every payback timing the existing book shows, so the test month is unambiguous.
* **Band method.** Empirical quantiles and a fitted normal on the 24 one-month post-rush errors give lower edges of 1,600 and 2,100, both
  under 3,000.
* **Horizon.** The decision on 15 December forecasts January's month-end stock, a one-month horizon under either a month-end or a
  mid-month reading of "January", because the existing book's errors are tabulated at month-ends and January's peak falls at month-end.
* **Conversion.** Each customer's pallets per TEU is flat across all 36 months, so averaging windows do not move it.
* **Maturity.** November's pallet positions are a closed month-end count; December bookings are confirmed notices, not forecasts.

## 9. Prompt sketch and deliverables

> We have until the 15th to take up any of the six overflow blocks at the park for January to June, at $1.1 million a block. Operations is
> sure the rush stock will keep us full into spring. Tell me how many blocks to take up, if any, in one line I can send the landlord, and
> send `overflow_case.xlsx` with the build and the sheets below, a chart `peak_overflow_band.png`, and a one-page `option_note.pdf`.

* `overflow_case.xlsx` — the forecast and the policy test under each band, the dock-time sheet (ask A) and the put-away sheet (ask B).
* `peak_overflow_band.png` — monthly pallet stock from August to June against the 40,000-position capacity line, the payback forecast
  with both the residual band and the post-rush band shaded, the first block's 3,000-pallet threshold drawn above capacity, and the
  January lower edge annotated with the decision.
* `option_note.pdf` — the committed call, the blocking quantity and what would have made it a pick.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the eight largest existing customers and each month of last quarter, the share of
  inbound containers received at the dock within 48 hours of leaving the terminal gate. *Device:* terminal gate-out events arrive from the
  terminals' feed stamped in UTC, while dock receipts are stamped in Pacific local time, as the integration guide documents; differencing
  the raw stamps drops seven or eight hours and moves containers across the 48-hour line for five customers. No receipt, pallet or TEU
  count changes.
* **Ask B (device-carried).** For each of the eight and each month of last quarter, the pallets put away into storage. *Device:* a
  cross-docked pallet is written to the receiving table like any receipt and leaves the same day, with its cross-dock status held in the
  dock-appointment table, as the warehouse system guide documents; counting every receipt as a put-away overstates storage receipts for
  three customers. A cross-docked pallet never holds a position at a month-end, so the stock counts the forecast uses are unchanged.
* **Ask C (validity).** The block count each rung's construction takes, its lower edge, and the coverage of each band method on the 24
  post-rush customer-episodes.
* **Decoupling.** Clearing the post-rush band changes no figure in asks A or B.

## 11. Rubric arithmetic

8 customers × 3 months (ask A) + 8 × 3 months (ask B) + 4 constructions × 3 (ask C) + the committed hold, the lower edge, the point
forecast and the falsifying threshold + 5 named chart parts + 3 files ≈ 72 criteria.

## 12. World-building constraints

* Owned capacity 40,000 positions; January point overflow 12,400 (pallet grain, payback). Lower edges: 18,500 (rung 0), 6,100 (rung 1),
  10,300 (rung 2), 1,600 (one-month post-rush band), 2,100 (fitted normal), pooled-horizon band one block, TEU-grain post-rush band one
  block.
* Post-rush errors at one month: 24 customer-episodes, 10th to 90th percentile 13% to 187% of forecast; outside post-rush windows the
  model's errors stay within ±17%.
* The rush is led by furniture and appliance customers at 1.6 times the book's average pallets per TEU.
* The twin customers are identical on rush TEU, bookings and pallets per TEU.
* Timestamp zones and cross-docked pallets touch no month-end pallet count, TEU or booking used in the forecast.

# RC19 — Which scheme the retail fleet's peak-season fund buys, or none, when the dock queues it would clear are worst exactly when the yard has nowhere to put a trailer

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Supply Chain & Logistics · retail distribution fleet operations |
| Mirrors | Capacity funding where the measured bottleneck is real but the fix can only reach part of it (drop-trailer pools at Walmart and Amazon distribution centres that free a driver only when the yard has an empty slot, cloud platforms releasing on-call engineers blocked on a degraded dependency, chat agents added while the queue waits on a back-office team) |
| Decision shape | Hold, forced by a blocking quantity: fund one peak-season scheme, or hold the money |
| Committed call | Hold the fund, with the blocking figure: the largest lateness cut any scheme can deliver this peak is 3.1 minutes (the CC1 drop yard) against the fund's 4.0-minute floor |
| Gap · Pattern | Gap 3 (objective) into Gap 2 (population) · Pattern C (serviceable share behind a join: drop-yard slots free in the hours tractors queue), with E16 (finer controls separate constructions) at rung 2 |
| Gate G mechanism | signal_vs_noise_or_hold, with binding_constraint |
| Measured traps engaged | #10 notes a binding limit as a risk · #12 stops at the first control that passes · #9 picks from the offered options when none passes |
| Calibration form | Existing-book actuals: the fleet's eleven past peak-season schemes, each with tractor-hours released and the lateness change that followed |
| Driving force | Tractors held in dock queues at the consolidation centres are lost capacity, and a drop yard takes a trailer off a driver only when it has an empty slot. A drop yard's slots fill in the same evening hours the queues peak, because every dock door at the centre beside it is busy then and dropped trailers wait to be unloaded. Free slots come from the centre's hourly door and yard census, another organisation's file from the fleet's gate times, and they cut the worst centre's releasable hours to 31% of its excess. No scheme then reaches the floor. |

## 1. Situation

A home-improvement retailer's dedicated fleet saw mean store-delivery lateness rise from 32 to 51 minutes this peak season on 4% more deliveries.
Fleet management wants more tractors; the logistics provider that runs the three supplier consolidation centres says the fleet's drivers are lost
queueing at its doors. The fleet has one peak-season fund. It will buy additional tractors and drivers (A), an order-consolidation programme that
cuts store trips (B), or a drop-trailer yard at one of the three centres, CC1 (C), CC2 (D) or CC3 (E). The fund rule buys the scheme that cuts mean
lateness the most at this season's volumes, and only if the cut is at least four minutes; otherwise the money is held. The fleet keeps the actual
results of every past peak-season scheme.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: deliveries and their booked slots, gate-in and gate-out times by centre and hour, the centres' hourly door
  and yard census, the scheme proposals and the book of past schemes. The provider is right that drivers are queueing, and fleet management is
  right that tractors are short. Nothing is overturned; the fund's floor binds once each scheme's reach is computed.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete management's request, the provider's view and the licensed basis. The gate times and the book's queueing conversion
  still commit the fund to the CC2 drop yard.
* **Instrument repair.** None suspect: deliveries and booked slots, gate times by centre and hour, each centre's hourly door and yard census, the
  proposals and the book are complete; the gates time every truck and the census counts every busy door and occupied slot each hour. Every rung
  reads complete files, so rung 0 still commits A (6.2 minutes), rung 1 C (9.4) and rung 2 D (6.6); none holds. What a drop yard can release is
  the smaller of tractors queueing and slots free in each hour, a quantity built across two organisations' files that no record holds.
* **Lens swap.** The naive build counts tractor-hours lost at each centre; the answer counts the tractor-hours a drop yard could take back in the
  hours they are lost, a different set of hours.

## 3. The driving force

A strong solver knows lateness is a symptom of utilisation, so it does the Little's-law accounting: tractor-hours consumed by trips plus
tractor-hours held in dock queues. Queueing dominates, CC1 has the largest excess, and converted at the fleet's average minutes per tractor-hour it
clears the floor by a wide margin. It then checks the conversion against the book of past schemes. Every conversion reproduces the book's total
(the salient control), and only a queueing curve, in which an hour released at high utilisation is worth far more, reproduces the book's weekly
results. CC2's queues sit in the evening peak, so on the curve CC2's drop yard wins at 6.6 minutes, and the solver commits. A drop yard, though,
takes a trailer off a driver only when it has an empty slot. CC2's dock doors are all busy in exactly those evening hours, so dropped trailers sit
unloaded and fill its yard, and only 31% of CC2's evening excess is releasable; CC1's is 60%. The share comes from the centre's hourly door and
yard census set against each scheme's slots. Carried through the curve, no scheme reaches four minutes; the best is the CC1 drop yard at 3.1.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Deliveries against lateness; minutes bought per tractor-hour at the fleet's average | A, extra tractors (6.2 min) | Volume rose 4% and lateness 60%, so capacity, priced the obvious way | The gate times: 38% of tractor-hours this season were spent queueing at the consolidation centres |
| 1 | Little's-law tractor-hours: trip time plus queueing excess by centre, converted at the average | C, CC1 drop yard (9.4 min) | Where capacity went, accounted exactly, with the worst centre first | The book's weekly results: an average conversion matches the book's total but misses 8 of 11 schemes' weekly changes |
| 2 | Conversion on the queueing curve the book's weekly results reproduce, applied hour by hour | D, CC2 drop yard (6.6 min) | Both the book's total and its finer weekly controls reproduce; CC2's queues sit in the hours worth most | The centres' hourly census: CC2's yard slots would be full in the evening hours its queues occupy |
| 3 | **Decisive:** each drop yard's releasable hours, the smaller of tractors queueing and slots free in each hour, then the curve | **Hold: best is C at 3.1 minutes** | — | — |

* **Why every candidate fails.** On the rung-3 basis: CC1 3.1 minutes, tractors 2.4, CC2 2.0, CC3 1.1, order consolidation 0.9. One standard,
  the fund's four-minute floor at this season's volumes, refuses all five.
* **Blocking quantity and its distance.** The best improvement, 3.1 minutes, is 0.9 short of the floor (23%). The decision would turn if CC1's
  yard could take 77% of its excess instead of 60%, or CC2's 61% of its evening excess instead of 31%.
* **Position table.** Rungs 0–2 commit to A, C and D, each above the floor, leading their runners-up by 4.13×, 1.34× and 1.27×.
* **Discriminator dominance.** CC2's yard carries a 1.65× margin over the floor into rung 3 (6.6 against 4.0 minutes). The hourly slot limit
  cuts its figure to 2.0, an edge of 3.30×, 1.67 times the required 1.2 × 1.65 = 1.98, and the best survivor, CC1 at 3.1, sits 1.29× under the
  floor.
* **Partial correction priced (L3).** A solver who caps releasable hours by each yard's slot count over the whole day, rather than by the slots
  free in each hour, releases 74% of CC2's excess and commits D at 4.9 minutes against CC1's 4.2 (1.17×). One who applies the census but converts
  at the average rather than on the curve commits C at 5.6 minutes against the extra tractors' 4.7 (1.19×). Both commit; neither holds.
* **Grid.** Accounting (deliveries, tractor-hours) × conversion (average, curve) × reach (gross, daily slot cap, hourly free slots) gives seven
  feasible builds, because the curve is fitted on tractor-hours released and reach applies only to queueing hours. Six commit to A, C or D, and
  only the decisive build holds.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The scheme proposals give slot counts; the census is the provider's file. No document says a drop yard can take a trailer
   only when a slot is free, or relates the census to the fleet's dock queues.
2. **Corpus blind for a computable reason.** *Every past drop yard in the book ran at a site whose yard was rebuilt with spare slots, so its yard
   never filled and its released hours equal its gross queueing excess in every closed season.* The book certifies the curve and cannot see the
   slot limit.
3. **No arithmetic symptom.** Tractor-hours, deliveries, gate times and lateness reconcile under every rung; CC2's queues and its census are both
   correct and agree.
4. **Not a row predicate.** Releasable hours are a minimum, hour by hour, of a quantity from the fleet's gate times and a quantity from another
   organisation's census, summed before conversion.
5. **The enumeration is arithmetic.** No column carries "releasable"; it is built per centre-hour.
6. **No cutover date.** Queues and full yards run all season; the dated event (the pre-holiday promotion week) raises every scheme alike and is
   the decoy.
7. **Survives deletion.** With every voice gone, the curve still commits the fund to CC2.

## 6. The calibration corpus

* **Form.** The book: eleven past peak-season schemes (tractor additions, order-consolidation programmes, drop yards at four other sites), each
  with the tractor-hours it released by week and the mean lateness by week before and during it.
* **What it certifies.** The queueing curve (rung 2). The salient control, the book's total change against total hours released, is matched by
  the average, Little's-law and curve conversions alike; only the curve matches the finer controls, the weekly changes, in all eleven schemes.
* **What it is blind to.** The slot limit (above).
* **Twin pair.** Schemes W-17 and W-22 released the same tractor-hours (2,400) over the same eight weeks at the same kind of site. Mean lateness
  fell 5.8 and 2.7 minutes (2.15×): W-17's hours fell in weeks running above 90% fleet utilisation, W-22's below 80%. Only the curve reproduces
  both.
* **Resemblance points at the decoy.** CC2's proposal matches W-19, a drop yard that released its whole gross excess, on slots, queue length and
  evening share.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The fund rule: the fund buys the scheme that reduces the fleet's mean store-delivery lateness the most at this season's
  volumes, and only if the reduction is at least 4.0 minutes; otherwise it is held. The scheme proposals (tractor-hours, slots, hours of
  operation).
* **Empirical pins.** The queueing curve, from the book; free slots by hour, from each centre's census.
* **Voices.** The fleet's general manager: "We can't make the store slots; we need more tractors on the road." The provider's operations
  director: "CC2's dock queues are the worst in the network; start there."
* **Licensed wrong basis.** The fund rule records that the network planning team sizes queueing schemes on gross tractor-hours lost and will
  present that sizing.

## 8. Determinism by construction

* **Releasable hours.** In each hour, the smaller of tractors queueing beyond 30 minutes and slots free in the proposed drop yard; the census and
  the gate times share hourly timestamps.
* **Curve.** One curve for the fleet, fitted on the book; every scheme's released hours are applied hour by hour at that hour's utilisation.
* **Demand.** This season's deliveries and booked slots, as the rule specifies; no forecast enters.
* **Tractors.** The fund buys 9,800 tractor-hours at the lease contract's rate, spread over the rota's hours.
* **Rounding.** Minutes to one decimal; no scheme sits within 0.4 minutes of the floor.

## 9. Prompt sketch and deliverables

> Mean lateness on our store deliveries has gone from 32 to 51 minutes this peak and the fleet has one peak-season fund. Fleet management is sure
> the answer is more tractors. Tell me which scheme the fund buys, or tell me we hold it, with the figure that decides it, in a sentence for the
> logistics board. Send `peak_fund_case.xlsx`, a chart `releasable_hours.png` and a one-page `fund_decision.pdf`.

* `peak_fund_case.xlsx` — the five schemes under each construction, the change-request sheet (ask A), the depot sheet (ask B) and the book
  reproduction (ask C).
* `releasable_hours.png` — for each centre, tractors queueing and drop-yard slots free by hour of day as two lines with the releasable hours
  shaded between them, a side bar of each scheme's minutes against the 4.0-minute floor, and the blocking figure labelled.
* `fund_decision.pdf` — the hold, the blocking figure and what would change it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six transport planning desks and each peak week, the 90th-percentile time to confirm a
  store's delivery-change request. *Device:* requests forwarded from the store-support line carry both that line's receipt time and the desk's
  receipt time, and the standard measures from the desk's receipt, as the request-data guide documents; using the first time overstates two
  desks.
* **Ask B (device-carried).** For each of the nine depots, tractor availability over the peak season. *Device:* tractors off the road for
  planned servicing carry a planned code that the availability measure excludes from the denominator, as the fleet guide documents; counting
  them as unavailable understates availability at the four depots with workshop days.
* **Ask C (validity).** For each of the eleven past schemes, the actual weekly changes and those predicted by the average, Little's-law and
  curve conversions; and each scheme's minutes under each rung construction.
* **Decoupling.** Clearing the slot limit changes no figure in asks A or B; neither touches a gate time, a census row or a scheme.

## 11. Rubric arithmetic

6 desks × 13 weeks (ask A) + 9 depots (ask B) + 11 schemes × 4 figures + 5 schemes × 4 constructions (ask C) + the hold, the blocking figure
and the two turning points + 5 named chart parts + 3 files ≈ 165 criteria.

## 12. World-building constraints

* Minutes by rung (A / B / C / D / E): 6.2 / 1.5 / 1.1 / 0.9 / 0.6; 4.7 / 1.5 / 9.4 / 7.0 / 4.1; 2.4 / 0.9 / 5.2 / 6.6 / 2.6; 2.4 / 0.9 / 3.1 /
  2.0 / 1.1.
* Releasable shares of gross excess: CC1 0.60, CC2 0.31, CC3 0.44; daily slot caps would give CC1 0.80 and CC2 0.74.
* 38% of tractor-hours spent queueing at the centres; deliveries +4%.
* W-17 and W-22 identical on hours released, weeks and site type.
* Forwarded-request stamps and planned-servicing codes touch no gate time, census row or scheme row.

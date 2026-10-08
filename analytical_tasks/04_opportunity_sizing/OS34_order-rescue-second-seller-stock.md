# OS34 — How many orders the rescue service saves in its eight new categories next quarter, when a cancelled item usually has no other seller with stock

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Product Analytics · marketplace order reliability |
| Mirrors | Rescuing orders a seller cannot fill by re-sourcing them from another seller (re-sourcing of seller-cancelled orders on Amazon's and Walmart's marketplaces, ticket guarantees at StubHub that replace cancelled seats, grocery substitutions at Instacart), sized on cancellations when only an item someone else holds in stock can be rescued |
| Decision shape | One figure committed at a date: the orders the rescue service saves next quarter in its eight new categories, written into the quarterly operating plan that locks on the 15th |
| Committed call | Orders rescued next quarter across the eight categories, to the nearest 1,000 |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · Pattern C (serviceable share behind a join: a cancelled order can be rescued only if another seller held the same item in stock at the hour of cancellation and could reach the buyer by the original date), with E33 below it (the cancellation flag against the ship-by rule) |
| Gate G mechanism | binding_constraint, with forecasting |
| Measured traps engaged | #13 validates on one population, applies to another · #5 takes the population a flag or filter suggests · #7 uses the ready-made measure |
| Calibration form | Retry or revision log: the pilot's re-routing log, 26 weeks of every order a seller failed to fill in phone accessories and household consumables, with each re-route attempt to another offer, the buyer's response, the outcome and its reason code |
| Driving force | A rescue offers the buyer the same item from another seller, so it exists only where another seller holds that catalogue item in stock at the hour of the cancellation and ships to the buyer's region by the original date. The pilot's phone accessories and household goods had six or more such sellers for every order outside one hurricane week, so its rescue rate looks like a property of buyers. The categories with the most cancellations, collectible cards, refurbished phones and vintage goods, sell items that are usually the only one of their kind. The rescuable share is built per order by an as-of join through order → catalogue item → other offers to the hourly offer snapshots and the sellers' shipping templates. |

## 1. Situation

A large online marketplace built a rescue service for orders its third-party sellers fail to fill: instead of refunding the buyer, it
offers the same item from another seller at the original price and delivery date. A 26-week pilot ran the service in phone accessories
and household consumables in two regions. Next quarter it switches on in eight new categories, and the quarterly operating plan, which
locks on the 15th, needs one figure for it: the orders it will save. The head of marketplace's view is that a cancelled order is a buyer
who still wants the item, so most of them can be saved.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the order file, the shipment events, the pilot log, the offer snapshots and the shipping templates.
  The pilot really does rescue more than half its cancellations, and the head of marketplace is right that those buyers still want what
  they ordered. Nothing is overturned. The difficulty is that a rescue needs someone else with the item, which the pilot's categories
  always had.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the head of marketplace's view and every voice. The pilot log still certifies value-band rates that reproduce
  25 of 26 weeks, and nothing says a new category lacks second sellers.
* **Instrument repair.** Suspect file: the order file's `cancelled_by` field, which records who executed a cancellation and files the
  marketplace's own cancellations of orders a seller failed to ship under "system", with unpaid and fraud cancellations. Repaired at
  three depths (the cause filled in for every system cancellation from the shipment events; the field recoded to the cause; a
  cancellation-cause record kept at the moment of cancelling), rung 0 becomes rung 1 (132,200), and rung 2 stays at 163,400. The offer
  snapshots are complete for the question, because every alternative held stock all day around a cancellation or not at all, and no
  instrument records whether another seller could have filled a cancelled order. The availability construction is still needed, and
  the answer stays at 70,000.
* **Lens swap.** The answer runs on a different population: the cancelled orders whose item another seller held in stock in time. In
  the pilot that population was every order; in the new categories it is 44% of them.

## 3. The driving force

A strong solver scopes the forecast to the policy's population, every order a seller failed to fill, including the marketplace's own
cancellations of orders that passed their ship-by date unshipped. It then applies the pilot's acceptance by order value to each
category's mix. That is the textbook transfer of a measured rate, it reproduces 25 of the pilot's 26 weeks, and it lands at 163,400. But a
rescue offers the same item from another seller, and the pilot's phone accessories and household goods are listed by six or more
sellers who ship from both regions. The eight new categories sell collectible cards in a given grade, refurbished phones in a given
condition and colour, fitment-specific parts and vintage pieces. When their seller cancels, there is usually no one else with the item
in stock. The rescuable share is an as-of join from each cancellation to every other offer of the same catalogue item, that offer's
stock in the hourly snapshot and its shipping template against the buyer's region and date. The categories with the most cancellations
are the ones where this join comes back empty.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Last quarter's orders flagged as seller-cancelled × the pilot's headline rescue rate (56.7%) | 115,300, +64.8% | The pilot report's own headline, on the marketplace's own cancellation flag | The service policy: orders the marketplace cancels when the ship-by date passes unshipped are rescued too, and they carry the system flag with unpaid and fraud cancellations |
| 1 | Orders sellers failed to fill (seller cancellations plus system cancellations after the ship-by date with no shipment event) × the pilot's rate per such order (0.54) | 132,200, +88.9% | The policy's population, built through the shipment events | The pilot log: buyers accepted re-routes on 0.78 of orders of $25 or more and 0.46 below |
| 2 | Acceptance by value band applied to each category's value mix | 163,400, +133.5% | Reproduces 25 of the pilot's 26 weeks within 2%; the 26th is the hurricane week | The offer snapshots: most cancelled collectible, refurbished and vintage items had no other seller with stock when their seller cancelled |
| 3 | **Decisive:** only orders for which another seller held the same item in stock at the hour of cancellation and could reach the buyer by the original date, at the value-band rates | **69,991, committed 70,000** | — | — |

* **Figure shape.** Both corrections walk the figure up (+14.6% and +23.6%), and the decisive move reverses them (−57.2%).
* **The deciding comparison.** Collectible cards and refurbished phones carry 31,500 and 31,400 rescues under rung 2 and 3,150 and 9,400
  under rung 3. Vintage and handmade falls from 15,300 to 300. Home and kitchen keeps most of its figure, 15,500 to 13,900.
* **Partial correction priced (L3).** Counting any other active listing of the item, stocked or not, lands at 130,800 (+86.9%). Checking
  stock at the hour the order was placed rather than when the seller cancelled lands at 101,400 (+44.8%), because by then the other
  sellers of fast-moving cards and phones had sold out too. Checking stock anywhere, without the buyer's region and date, lands at 87,900
  (+25.5%).
* **Grid.** Population (flag, fail-to-fill rule) × rates (pilot headline or pooled, by value band) × alternatives (ignored, in stock in
  time) = 8 cells. The nearest wrong cell is the pooled rate with the availability construction, 57,900 (−17.3%). Every cell without the
  construction lands at least 64% above the answer.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The service policy defines a rescue, and the plan template fixes the base. No document says how often another
   seller has a cancelled item in stock, and the pilot report never mentions it.
2. **Corpus blind for a computable reason.** *In every one of the pilot's 126,000 orders outside week 20, another seller held the item in
   stock and could reach the buyer by the original date, because the pilot's phone accessories and household goods are listed by at
   least six sellers who ship from both regions; the only exceptions, week 20's Southeast orders during a hurricane embargo on the
   carrier's hubs, are coded as a weather event.* The value-band model and the availability model return identical rescues for every
   other pilot order.
3. **No arithmetic symptom.** Cancellations, re-routes, acceptances and refunds reconcile on every rung, and the offer snapshots tie to the
   sellers' inventory feeds hour by hour.
4. **Not a row predicate.** Availability needs an as-of join from each cancellation to every other offer of the same catalogue item, that
   offer's stock in the snapshot at that hour, and its shipping template against the buyer's region and the original date.
5. **The enumeration is arithmetic.** No column marks an order as rescuable. The category shares come out of the join over 244,840 orders.
6. **No cutover date.** Availability is a property of what each category sells and is the same every quarter; no series steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The pilot's re-routing log: for each of 126,000 orders sellers failed to fill over 26 weeks in the Northeast and Southeast,
  each re-route attempt to another offer, the buyer's response, the outcome and the reason code (buyer declined, new seller declined,
  shipped, carrier embargo).
* **What it certifies.** Acceptance by value band (0.78 at $25 or more, 0.46 below), the 10% price cover, and on-time delivery of every
  rescued order. The rung-2 model reproduces 25 of 26 weeks within 2%.
* **What it is blind to.** Orders with no other seller holding the item in stock (above).
* **The absolute split (O2).** In the pilot, every order with an alternative was rescued at its value band's rate and none without one
  was rescued. In last quarter's eight categories, every cancellation either had a qualifying alternative for the whole day around it or
  had none, with no order in between.
* **Twin pair (free training instance).** Pilot weeks 18 and 20 are identical on every column of the cancellation report: 4,850 orders
  each, the same value-band mix and the same even split between regions. In week 20 a hurricane closed the carrier's Southeast hubs, so
  no alternative could reach a Southeast buyer by the original date, and the week rescued 1,310 orders against week 18's 2,620, 2.0×
  apart. The log codes those orders "carrier embargo", and the pilot report sets the week aside as a weather event, so the gap changed
  nothing the value-band model reports. In collectible cards, refurbished phones and vintage goods, alternatives are missing in fine
  weather, and there the same rule decides.
* **Resemblance points at the decoy.** The new categories' buyers match the pilot's within each value band on membership, device and
  repeat purchase, so transferring the pilot's value-band rates by resemblance files rung 2.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The plan template takes last quarter's volumes by category as next quarter's base and asks for a feature's figure in
  orders. The service policy rescues an order a seller fails to fill, whether the seller cancels it or the marketplace cancels it when the
  ship-by date passes unshipped, by offering the buyer the same item from another seller at the original price and delivery date, with
  the marketplace covering up to 10% of any price difference.
* **Empirical pins.** Acceptance by value band comes from the pilot log. Alternatives come from last quarter's hourly offer snapshots and
  the sellers' shipping templates.
* **Voices.** The head of marketplace: "A cancelled order is a buyer who still wants the item; most of them can be saved." The pilot's
  product manager: "The pilot saved more than half of every week's cancellations except the hurricane week." That is true.
* **Licensed wrong basis.** The plan template records that the finance partner forecasts a launched feature at its pilot's headline rate
  on each new category's volumes, and will review the figure on that basis.

## 8. Determinism by construction

* **Availability window.** Around every cancellation, each alternative held stock for all 24 hours or for none of them, so hourly or
  daily snapshots and any window inside ±12 hours return the same orders.
* **Fail-to-fill rule.** The marketplace's cancellations of unshipped orders fall at least 24 hours after the ship-by date, and unpaid and
  fraud cancellations fall before it, so any rule anchored on the ship-by date returns the same orders.
* **Value band.** No order is priced within 50 cents of $25.
* **Price cover.** No in-stock alternative is priced more than 10% above the cancelled offer, so the cover never binds.
* **Pilot weeks.** The pilot report's rates exclude week 20. Including it lowers the pooled rate by 1.9% and leaves the rates on orders
  with an alternative unchanged, so the answer does not move.
* **Rounding.** The answer (69,991) sits 491 orders from the nearest rounding boundary.

## 9. Prompt sketch and deliverables

> Our quarterly plan locks on the 15th, and it needs one number from your team: how many orders the rescue service will save in its eight
> new categories next quarter, to the nearest thousand. Our head of marketplace believes a cancelled order is a buyer who still wants the
> item, so most of them can be saved. Send `rescue_forecast.xlsx`, a chart `rescue_by_category.png`, and a one-page `plan_note.pdf`.

* `rescue_forecast.xlsx`: the order-level construction by category, the figure under the four rung bases, the returns sheet (ask A) and
  the handling-time sheet (ask B).
* `rescue_by_category.png`: for each category, three nested bars (orders sellers failed to fill, the part with an alternative in stock in
  time, the part rescued), categories sorted by cancellations, the alternative share printed on each bar and the pilot's rate drawn as a
  reference line.
* `plan_note.pdf`: the committed figure, the category split, and the basis the finance partner will bring.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the eight categories, last quarter's returns and the return rate on delivered orders.
  *Device:* a return authorisation covers everything a buyer sends back from one order, and each parcel gets its own label row under it,
  as the returns guide documents. Counting label rows as returns overstates returns by 14% in the categories where buyers send
  multi-item orders back in several boxes.
* **Ask B (device-carried).** For each category, the median handling time from order to dispatch last quarter. *Device:* an order shipped
  in several parcels records a dispatch event per parcel, and the fulfilment guide defines dispatch as the last parcel's event. Using the
  first event understates handling time by 1.4 days in home and kitchen and in auto parts, where split shipments are common.
* **Ask C (validity).** The figure under each of the four rung bases, and the pilot reproduction under the value-band model and the
  availability model: 25 of 26 weeks for the first, which predicts twice week 20's rescues, and 26 of 26 for the second.
* **Decoupling.** Clearing the availability construction changes no figure in asks A or B, and neither device touches a cancelled order.

## 11. Rubric arithmetic

8 categories × 2 (ask A) + 8 (ask B) + 4 bases + 2 reproduction counts (ask C) + the committed figure and the eight categories'
alternative shares + 5 named chart parts + 3 files ≈ 47 criteria.

## 12. World-building constraints

* Last quarter's orders flagged as seller-cancelled (thousands): Collectible cards 46.0, Refurbished phones 38.0, Auto parts 30.0, Used
  books 26.0, Vintage and handmade 22.0, Home and kitchen 16.0, Toys and games 13.4, Beauty 12.0 (203.4 in all). System cancellations
  after the ship-by date per flagged order 0.05 / 0.08 / 0.35 / 0.30 / 0.02 / 0.45 / 0.40 / 0.40, so sellers failed to fill 244,840
  orders. Shares at $25 or more 0.60 / 0.95 / 0.85 / 0.20 / 0.70 / 0.65 / 0.60 / 0.45. Shares with an alternative in stock in time 0.10 /
  0.30 / 0.45 / 0.55 / 0.02 / 0.90 / 0.88 / 0.92.
* Partial bases: shares with any other active listing 0.70 / 0.85 / 0.80 / 0.90 / 0.35 / 0.98 / 0.97 / 0.99; in stock at the order hour
  0.40 / 0.55 / 0.70 / 0.75 / 0.10 / 0.95 / 0.94 / 0.96; in stock anywhere at the cancellation hour 0.18 / 0.45 / 0.62 / 0.72 / 0.04 /
  0.96 / 0.95 / 0.97.
* Pilot: 120,000 flagged orders and 6,000 system cancellations after the ship-by date over 26 weeks, 25% at $25 or more, acceptance 0.78
  and 0.46 (0.54 pooled, 0.567 per flagged order), and an alternative for every order outside week 20.
* Rung figures are 115,300 / 132,200 / 163,400 / 69,991, no other grid cell is within 17% of the answer, and every partial lands at
  least 25% above it.
* Weeks 18 and 20 are identical on every cancellation-report column; only week 20's Southeast orders lack an alternative (2,620 against
  1,310 rescued).
* Return labels and dispatch events never touch cancelled orders (no cancelled order carries either), the offer snapshots or the pilot
  log.

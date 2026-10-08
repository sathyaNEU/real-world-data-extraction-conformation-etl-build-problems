# FC46 — What the two-day free-shipping membership will cost in its first year, when the cost report's shipping per item is a share of a parcel charge and the membership splits each order across centres

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Product Analytics · e-commerce membership programmes |
| Mirrors | Costing a fast free-shipping membership from per-item shipping costs (Amazon Prime, Walmart+, retailer memberships with two-day promises), where the per-item cost embeds the consolidated parcel that standard shipping waits to build and the faster promise no longer waits for |
| Decision shape | One figure committed at a date: the membership's first-year shipping subsidy in the marketing budget |
| Committed call | The shipping the programme will pay for its 25,000 invited members over the first 52 weeks, to the nearest $10,000 |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · S6 (a correct share carried onto a different book: the parcel's fixed charge shared over a consolidated 3.0-item parcel, carried onto members' orders that ship from every centre holding an item), with a binding limit applied in the figure (measured #10) at rung 2 |
| Gate G mechanism | forecasting, with decomposition_attribution |
| Measured traps engaged | #7 uses the ready-made measure · #13 validates on one population, applies to another · #10 notes a binding limit as a risk |
| Calibration form | Pilot log: last year's 26-week two-day free-shipping pilot for 1,000 top customers, every order with its items and its carrier charge, run on the one fulfilment centre then on the two-day network |
| Driving force | The carrier charges $4.40 a parcel plus $0.53 an item and invoices one total per parcel. Standard shipping waits for the consolidation shuttle and sends each order complete, so the cost report's $2.00 an item is exact for the three-item parcels that produced it. The membership promises two-day delivery, so each of the three fulfilment centres ships what it holds at once, and the SKU location table puts a member's three-item basket in 2.2 centres: every item carries more than twice the parcel charge. The pilot confirmed $2.00 an item because it ran from one centre. Nothing labels the fixed part; it appears only when parcel charges are set against the items in each parcel. |

## 1. Situation

An online music retailer is launching a two-day free-shipping membership for its 25,000 best customers: every order ships free for a
year, and the programme pays at most $150 of any member's shipping. Its catalogue is stocked across three fulfilment centres by
distribution agreement. Standard orders wait for the inter-centre consolidation shuttle and ship complete in one parcel within eight days.
The marketing budget carries the membership's shipping as one line, and finance needs it before launch. The pack holds three years of
transactions, the carrier's parcel invoices, the monthly cost report, the pilot's order log, the SKU location table, the membership terms
and the analytics team's customer-model library. The budget is locked on 1 December.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: transactions, carrier invoices, the cost report's $2.00 per item, the pilot log, the SKU locations
  and the terms. No stakeholder's reading of their own numbers is overturned; $2.00 an item really has been the retailer's shipping cost
  for three years, and the pilot really did cost $2.00 an item. The difficulty is that the cost belongs to the consolidated parcel, and the
  membership ships a different one.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the head of e-commerce's view and every voice. The cost report's per-item figure is still the natural price
  for every forecast item, the pilot still confirms it, and it still reproduces every past invoice total.
* **Instrument repair.** Clean-data test. No file the ladder reads is incomplete, stale or narrower than it claims: the invoices carry
  every parcel's full charge, the cost report divides them exactly, the pilot log carries every pilot order with its charge, and the SKU
  location table places every title. The deepest repair available, invoices that itemise each parcel into its $4.40 and its $0.53 an
  item, leaves rung 0 at $1,200,000, rung 1 at $964,000 and rung 2 at $869,000, because each still ships one parcel per order; the split
  construction is still needed, since no file records how members' orders will ship under a promise that has not run across centres.
* **Lens swap.** The naive read and the answer price different books: consolidated three-item parcels, against members' orders broken
  into one parcel per centre that holds an item.

## 3. The driving force

A strong solver prices the members' purchases at the cost report's $2.00 an item, then improves the purchases: it replaces each member's
past rate with the customer model's expected purchases, which allows for customers who have quietly stopped, applies the pilot's 15% rise
in items bought under free shipping, and caps each member's subsidy at the programme's $150. The pilot's own charges confirm $2.00 an item.
It lands at $869,000. Every step is correct. But the carrier does not charge by the item: set against the items in each parcel, its
invoices show $4.40 a parcel plus $0.53 an item, so $2.00 is the parcel charge shared over the three items standard shipping waits to
consolidate. The pilot never split an order, because it ran from the one centre then on the two-day network. Under the membership's
promise each centre ships its own items at once, and joined to the SKU location table the members' own baskets span 2.2 centres an order.
Rebuilt as parcels per centre, an item costs $3.76, the cap binds for every heavy member, and the year's shipping is $1,500,000.

## 4. The ladder

| Rung | Construction | Lands on ($ thousands) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Each member's past purchase rate × 52 weeks × the cost report's $2.00 an item | 1,200 (−20.3%) | Finance's own shipping rate on the members' own history | The transactions: a fifth of the members have bought nothing in 26 weeks, and the analytics library's customer model prices the chance each is still buying |
| 1 | The customer model's expected purchases, raised by the pilot's 15% under free shipping, × $2.00 | 964 (−35.8%) | Allows for lapsed customers and for what free shipping does to buying, and the pilot's own charges confirm $2.00 | The membership terms: the programme pays at most $150 of a member's shipping in the year |
| 2 | The same, with each member's subsidy capped at $150 | 869 (−42.2%) | The binding limit applied member by member, not noted as a risk | The membership terms' two-day promise: each centre ships the items it holds without waiting for the shuttle, and the SKU location table spreads the members' baskets over 2.2 centres an order |
| 3 | **Decisive:** members' parcels counted as the centres their baskets span, each charged $4.40 + $0.53 an item as the invoices fit, capped at $150 a member | **1,500** | — | — |

* **Figure shape.** Rungs 0 to 2 walk the subsidy down (−20.3%, −35.8%, −42.2%) and the decisive rung reverses past rung 0, so a solver
  who stops anywhere short under-budgets by at least $300,000.
* **Partial correction priced (L3).** A solver who counts the extra parcels but prices each at the book's average parcel ($6.00, built on
  three items) lands at $1,730,000 (+15.2%). One who rebuilds by parcel but forgets the cap lands at $1,810,000 (+20.8%). One who counts
  the splits but keeps $2.00 an item is rung 2.
* **Grid.** Purchases (past rate, customer model) × cap (off, on) × shipping (per item, per parcel per centre) = 8 cells: 1,198, 1,043,
  2,254, 1,830; 964, 869, 1,815, 1,502. The nearest wrong cells are 1,198 (−20.3%) and 1,815 (+20.8%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The cost report gives shipping per item; the invoices give one charge per parcel; the terms promise two days and
   say nothing about parcels. No document says the charge is mostly per parcel or that the promise splits orders.
2. **Corpus blind to the split.** *In every closed quarter every order shipped complete in one parcel, because standard shipping waits
   for the consolidation shuttle; so items per parcel held between 2.9 and 3.1, $2.00 an item reproduced every quarter's invoices within
   1%, and the single-centre pilot reproduced it too.* The cost report is validated exactly where it cannot fail.
3. **No arithmetic symptom.** Invoices reconcile to parcels, parcels to orders, the cost report to the invoices, and every rung's figure
   is internally consistent.
4. **Not a row predicate.** The fixed part comes from setting every parcel's charge against its items across the invoices; the members'
   parcels come from joining each basket's titles to the centres that stock them and counting distinct centres per order.
5. **The enumeration is arithmetic.** No column says "per parcel" or "split"; both the charge split and the members' parcels are computed.
6. **No cutover date.** The pilot and the launch are dated but step no series the forecast reads.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The pilot's order log: 1,000 top customers for 26 weeks, every order with its items and its carrier charge, and the same
  customers' orders in the year before, alongside the main book's carrier invoices.
* **What it certifies.** The customer model (pilot customers' purchases follow its expectations within 2%), the 15% rise in items bought
  under free shipping (14–16% in every customer tier), unchanged basket size (3.0 items an order), and $2.00 an item for one-centre parcels.
* **What it is blind to.** Splitting: every pilot order shipped from one centre.
* **Twin pair.** Two weeks in last year's invoices shipped identical items (11,200) to the same number of customers. Their carrier charges
  were $22,360 and $42,080 (1.88× apart), because in the second the consolidation shuttle was off the road and mixed orders shipped from
  each centre, 1.36 items a parcel against 3.0. Per-item costing predicts them equal; only $4.40 a parcel plus $0.53 an item reproduces
  both.
* **Resemblance points at the decoy.** By spend, frequency and tenure, the members most resemble the pilot's customers, whose shipping
  cost exactly $2.00 an item.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The membership terms: every member's order ships free with two-day delivery for 52 weeks, and the programme pays at most
  $150 of a member's shipping. The fulfilment guide: under a two-day promise each centre ships the items it holds on the day ordered. The
  25,000 invitations.
* **Empirical pins.** The parcel charge and the item charge, from the invoices. Centres per order, from members' baskets joined to the SKU
  location table. The 15% rise, from the pilot. Expected purchases, from the customer model.
* **Voices.** The head of e-commerce: "Shipping is two dollars an item; it has been for three years, and the pilot proved it." The loyalty
  manager: "Members will buy more, not differently." The finance business partner: "The cap keeps this small whatever happens."
* **Licensed wrong basis.** The terms record that the carrier's account team quotes volume discounts on the retailer's shipping per item
  and will benchmark the membership against it.

## 8. Determinism by construction

* **Charge split.** Every invoiced parcel under 5 kg fits $4.40 + $0.53 × items to the cent, and no member's order weighs more.
* **Centres per order.** Members' last six and last twelve months of baskets give 2.18–2.22 centres an order, so the cost per item moves by
  under 1%.
* **Customer model.** The library's model and its fitted parameters are pinned; expected purchases per member agree within 0.5% under
  either of its two documented fitting routines.
* **Cap.** Applied member by member over the 52 weeks; no member's uncapped subsidy sits within $5 of $150.
* **Rounding.** The forecast is $1,502,400, inside the $1,500,000 bin and clear of its edges.

## 9. Prompt sketch and deliverables

> We launch the two-day free-shipping membership for our 25,000 best customers in January, and the shipping it pays for is one line in
> the marketing budget. Our head of e-commerce says shipping is two dollars an item and the pilot proved it. Give me the programme's
> first-year shipping cost, to the nearest $10,000, in one sentence for the budget, and send `membership_cost.xlsx` with the build and the
> sheets below, a chart `parcel_split.png`, and a one-page `budget_note.pdf`.

* `membership_cost.xlsx` — expected purchases, parcels and capped subsidy by member tier, the returns sheet (ask A) and the gift-card sheet
  (ask B).
* `parcel_split.png` — parcel charge against items per parcel from the invoices with the $4.40 + $0.53 line, the consolidated 3.0 and the
  members' 1.36 marked on the axis, the per-item cost at each shown as labelled points, and the twin weeks highlighted.
* `budget_note.pdf` — the committed figure, why $2.00 an item does not hold for members, and where the cap binds.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the four product lines (CD, vinyl, cassette, merchandise) and each quarter of last
  year, the share of items returned. *Device:* an exchange is written as a return and a new sale under one exchange ID, with the link in
  the exchanges table, as the order-system guide documents; reading the returns table alone counts exchanges as returns for two lines.
  Returns enter no part of the shipping forecast.
* **Ask B (device-carried).** For each quarter of last year, gift-card value issued and redeemed. *Device:* a gift card reissued after a
  lost-card claim keeps its balance under a new card number, with the old number voided in the card-events table, as the payments guide
  documents; summing issuances counts reissued balances twice. Gift cards enter no part of the shipping forecast.
* **Ask C (validity).** The subsidy under each of the four rung constructions, and the cost per item each implies.
* **Decoupling.** Clearing the parcel rebuild changes no figure in asks A or B.

## 11. Rubric arithmetic

4 product lines × 4 quarters (ask A) + 4 quarters × 2 (ask B) + 4 constructions × 2 (ask C) + the committed figure, the members' parcels
per order and the members capped + 5 named chart parts + 3 files ≈ 43 criteria.

## 12. World-building constraints

* Carrier: $4.40 a parcel plus $0.53 an item; consolidated parcels carry 2.9–3.1 items, so $2.00 an item; members' baskets of 3.0 items
  span 2.2 centres, so 1.36 items a parcel and $3.76 an item.
* Members: 25,000; expected items over 52 weeks with the 15% rise 483,000 (16,000 at 7.5, 8,000 at 30, 1,000 at 123); past rate × 52 gives
  600,000.
* Subsidy by rung: 1,198 / 964 / 869 / 1,502 ($ thousands); uncapped parcel build 1,815; book-average parcel 1,731.
* Pilot: every order single-centre, 3.0 items, $2.00 an item; the twin weeks identical in items and customers, charges $22,360 and $42,080.
* Exchanges and reissued gift cards touch no order, parcel or charge used in the forecast.

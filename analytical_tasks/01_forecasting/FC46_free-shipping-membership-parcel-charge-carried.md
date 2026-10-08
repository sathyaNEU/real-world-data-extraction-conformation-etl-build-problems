# FC46 — What the free-shipping membership will cost in its first year, when the cost report's shipping per item is a share of a parcel charge that free shipping splits into smaller parcels

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Product Analytics · e-commerce membership programmes |
| Mirrors | Costing a free-shipping membership from per-item shipping costs (Amazon Prime, Walmart+, marketplace and retailer memberships), where the per-item cost embeds a basket size that free shipping itself shrinks |
| Decision shape | One figure committed at a date: the membership's first-year shipping subsidy in the marketing budget |
| Committed call | The shipping the programme will pay for its 25,000 invited members over the first 52 weeks, to the nearest $10,000 |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · S6 (a correct share carried onto a different book: the parcel's fixed charge shared over 3.0 items, carried onto members' 1.4-item orders), with a binding limit applied in the figure (measured #10) at rung 2 |
| Gate G mechanism | forecasting, with decomposition_attribution |
| Measured traps engaged | #7 uses the ready-made measure · #13 validates on one population, applies to another · #10 notes a binding limit as a risk |
| Calibration form | Pilot log: last year's 26-week free-shipping pilot for 1,000 top customers, every order with its items; the pilot's parcels went through a bulk postage account, so the log carries no charges |
| Driving force | The carrier charges $4.80 a parcel plus $0.40 an item, and invoices one total per parcel. Customers who pay for shipping batch three items into a parcel, so the cost report's $2.00 per item is exact for the book that produced it. Under free shipping the pilot's members ordered 1.4 items at a time, so every item carries more than twice the parcel charge. Nothing labels the fixed part: it appears only when parcel charges are set against the items in each parcel, and the pilot that shows the smaller orders shows no costs. |

## 1. Situation

An online music retailer is launching a free-shipping membership for its 25,000 best customers: every order ships free for a year, and
the programme pays at most $150 of any member's shipping. The marketing budget carries the programme's shipping as one line, and finance
needs it before the launch. The pack holds three years of transactions, the carrier's parcel invoices, the monthly cost report, the
pilot's order log, the programme terms and the analytics team's customer-model library. The budget is locked on 1 December.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: transactions, carrier invoices, the cost report's $2.00 per item, the pilot log and the terms. No
  stakeholder's reading of their own numbers is overturned; $2.00 an item really has been the retailer's shipping cost for three years. The
  difficulty is that the cost belongs to the basket the paying customer built, and members build a different one.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the head of e-commerce's view and every voice. The cost report's per-item figure is still the natural price for
  every forecast item, and it still reproduces every past invoice total.
* **Instrument repair.** Imagine invoices that itemised the parcel charge. The split would be plain, but members' orders have not happened
  yet; their size comes only from the pilot, and the cost only from combining the two.
* **Lens swap.** The naive read and the answer price different books: paying customers' three-item parcels against members' 1.4-item ones,
  where every item carries more than twice the parcel charge.

## 3. The driving force

A strong solver prices the members' purchases at the cost report's $2.00 an item, then improves the purchases: it replaces each member's
past rate with the customer model's expected purchases, which allows for customers who have quietly stopped, applies the pilot's 15% rise
in items bought under free shipping, and caps each member's subsidy at the programme's $150. It lands at $870,000. Every step is correct.
But the carrier does not charge by the item. Set against the items in each parcel, its invoices show a charge of $4.80 a parcel plus $0.40
an item, so $2.00 an item is the parcel charge shared over the 3.0 items a paying customer packs. The pilot's members, with nothing to
save by waiting, ordered 1.4 items at a time, and the pilot's bulk postage left no per-parcel cost to warn anyone. Rebuilt as parcels at
the members' order size, an item costs $3.83, the cap now binds for every heavy member, and the year's shipping is $1,530,000.

## 4. The ladder

| Rung | Construction | Lands on ($ thousands) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Each member's past purchase rate × 52 weeks × the cost report's $2.00 an item | 1,200 (−21.5%) | Finance's own shipping rate on the members' own history | The transactions: a fifth of the members have bought nothing in 26 weeks, and the analytics library's customer model prices the chance each is still buying |
| 1 | The customer model's expected purchases, raised by the pilot's 15% under free shipping, × $2.00 | 966 (−36.8%) | Allows for lapsed customers and for what free shipping does to buying, both measured | The programme terms: the programme pays at most $150 of a member's shipping in the year |
| 2 | The same, with each member's subsidy capped at $150 | 870 (−43.1%) | The binding limit applied member by member, not noted as a risk | The carrier invoices: a parcel's charge is $4.80 plus $0.40 an item, and the pilot's members ordered 1.4 items at a time against the book's 3.0 |
| 3 | **Decisive:** members' parcels at the pilot's order size, each charged $4.80 + $0.40 an item, capped at $150 a member | **1,530** | — | — |

* **Figure shape.** Rungs 0 to 2 walk the subsidy down (−21.5%, −36.8%, −43.1%) and the decisive rung reverses past rung 0, so a solver
  who stops anywhere short under-budgets by at least $330,000.
* **Partial correction priced (L3).** A solver who sees the smaller orders but prices each at the book's average parcel ($6.00, built on
  three items) lands at $1,690,000 (+10.8%). One who rebuilds by parcel but forgets the cap lands at $1,850,000 (+21.0%). One who uses the
  pilot's rise in items but keeps $2.00 an item is rung 2.
* **Grid.** Purchases (past rate, customer model) × cap (off, on) × shipping (per item, per parcel at the members' order size) = 8 cells:
  1,200, 1,044, 2,297, 1,862; 966, 870, 1,849, 1,528. The nearest wrong cells are 1,200 (−21.5%) and 1,849 (+21.0%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The cost report gives shipping per item; the carrier invoices give one charge per parcel; no document says the
   charge is mostly per parcel or that members will order differently from paying customers.
2. **Corpus blind to the density.** *In every closed quarter the book's items per parcel held between 2.9 and 3.1, because every customer
   paid for shipping and batched to the same basket; so $2.00 an item reproduced every quarter's carrier invoices within 1%.* The cost
   report is validated exactly where it cannot fail.
3. **No arithmetic symptom.** Invoices reconcile to parcels, parcels to orders, the cost report to the invoices, and every rung's figure is
   internally consistent.
4. **Not a row predicate.** The fixed part comes from setting every parcel's charge against its items across the invoices, and the members'
   cost from combining that split with an order size measured in a different file.
5. **The enumeration is arithmetic.** No column says "per parcel"; the split and the members' order size are both computed.
6. **No cutover date.** The pilot is dated but steps no series the forecast reads; the membership starts in the future.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The pilot's order log: 1,000 top customers for 26 weeks, every order with its items and the same customers' orders in the year
  before, alongside the main book's carrier invoices.
* **What it certifies.** The customer model (the pilot customers' purchases follow its expectations within 2%) and the 15% rise in items
  bought under free shipping, steady at 14–16% in every customer tier.
* **What it pins.** The members' order size: 1.4 items an order in every week of the pilot and every tier (1.38–1.42), against 3.0 for the
  same customers the year before.
* **Twin pair.** Two weeks in last year's invoices shipped identical items (11,200) to the same number of customers. Their carrier charges
  were $22,400 and $45,800 (2.05× apart), because the second held the spring free-shipping weekend and its parcels carried 1.3 items
  against 3.0. Per-item costing predicts them equal; only $4.80 a parcel plus $0.40 an item reproduces both.
* **Resemblance points at the decoy.** By spend, frequency and tenure, the members most resemble the book's top-tier customers, whose
  shipping the cost report's $2.00 an item reproduced within 1% every quarter.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The programme terms: every member's order ships free for 52 weeks and the programme pays at most $150 of a member's
  shipping. The forecasting convention: members' ordering follows the pilot's pattern all year. The 25,000 invitations.
* **Empirical pins.** The parcel charge and the item charge, from the carrier invoices. The members' order size and the 15% rise, from the
  pilot. Expected purchases, from the customer model.
* **Voices.** The head of e-commerce: "Shipping is two dollars an item; it has been for three years." The loyalty manager: "Members will
  buy more, not differently." The finance business partner: "The cap keeps this small whatever happens."
* **Licensed wrong basis.** The programme terms record that the carrier's account team quotes volume discounts on the retailer's
  shipping per item and will benchmark the membership against it.

## 8. Determinism by construction

* **Charge split.** Every invoiced parcel under 5 kg fits $4.80 + $0.40 × items to the cent, and no member's order weighs more.
* **Order size.** 1.4 items an order in every pilot week and tier, so pooled and tier-level sizes give the same parcels.
* **Customer model.** The library's model and its fitted parameters are pinned; expected purchases per member agree within 0.5% under
  either of its two documented fitting routines.
* **Cap.** Applied member by member over the 52 weeks; no member's uncapped subsidy sits within $5 of $150.
* **Rounding.** The forecast is $1,528,300, inside the $1,530,000 bin and clear of its edges.

## 9. Prompt sketch and deliverables

> We launch the free-shipping membership for our 25,000 best customers in January, and the shipping it pays for is one line in the
> marketing budget. Our head of e-commerce says shipping is two dollars an item and has been for three years. Give me the programme's
> first-year shipping cost, to the nearest $10,000, in one sentence for the budget, and send `membership_cost.xlsx` with the build and the
> sheets below, a chart `parcel_split.png`, and a one-page `budget_note.pdf`.

* `membership_cost.xlsx` — expected purchases, parcels and capped subsidy by member tier, the returns sheet (ask A) and the gift-card sheet
  (ask B).
* `parcel_split.png` — parcel charge against items per parcel from the invoices with the $4.80 + $0.40 line, the book's 3.0 and the pilot's
  1.4 marked on the axis, the per-item cost at each shown as labelled points, and the twin weeks highlighted.
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
and the members capped + 5 named chart parts + 3 files ≈ 43 criteria.

## 12. World-building constraints

* Carrier: $4.80 a parcel plus $0.40 an item; the book packs 2.9–3.1 items a parcel, so $2.00 an item; members order 1.4 items, so $3.83.
* Members: 25,000; expected items over 52 weeks with the 15% rise 483,000 (16,000 at 7.5, 8,000 at 30, 1,000 at 123); past rate × 52 gives
  600,000.
* Subsidy by rung: 1,200 / 966 / 870 / 1,528 ($ thousands); uncapped parcel build 1,849; book-average parcel 1,693.
* The twin weeks are identical in items and customers; charges $22,400 and $45,800.
* Exchanges and reissued gift cards touch no order, parcel or charge used in the forecast.

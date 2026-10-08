# OS19 — How to split a $600,000 e-book grant across five collections, when the readers waiting longest can already borrow no more

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Nonprofit & Grant-making · library grant programmes |
| Mirrors | Allocating a content-licensing budget by genre when the heaviest users already consume at a plan limit (Kindle Unlimited's 20-title borrowing limit, Audible credits, Netflix's DVD-queue slots, Libby lending limits), so more supply in their favourite genres changes what they consume, not how much |
| Decision shape | An allocation under a cap: a $600,000 licence grant split across five collections in $10,000 blocks |
| Committed call | Each collection's share of the grant, and the added checkouts it buys next year, to the nearest 1,000 |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · S5, a ceiling on a grouping orthogonal to the build's partition (every card's six-loan limit, which cuts across collections), with finer published controls (#12) separating turn and substitution constructions below it |
| Gate G mechanism | binding_constraint, with decomposition_attribution |
| Measured traps engaged | #6 treats a mixed segment all one way · #12 stops at the first control that passes · #7 uses the ready-made measure |
| Calibration form | Settled-transaction ledger: the licence aggregator's settled ledger for last year, every licence lot bought and every loan settled against a licence, with card, start, return and hold-delivery times |
| Driving force | A new licence adds a checkout only when its borrower had room to borrow. Each card may hold six digital loans, and the heavy readers who fill the longest holds lists sit at six all year, so a licence that reaches them changes which book they read next, not how many they read. Summed over the system the limit never binds; card by card it binds for 80% of Romance's hold-driven loans and 3% of Non-fiction's. That share exists only by replaying each card's loans in the settled ledger, and the lot back-test cannot see it because a displaced loan settles against another lot. |

## 1. Situation

A county library system has a one-off $600,000 state grant for e-book and audiobook licences next year. The grant terms split it across
its five digital collections, Adult fiction, Mystery & thriller, Romance, Non-fiction and Young readers, in proportion to the added
checkouts per dollar each collection's licences are expected to deliver, in $10,000 blocks. The aggregator's holds report gives holds by
collection, and its price list the average licence price. The state library publishes annual circulation statistics by collection and
format. The lending policy allows six digital loans per card at a time. The aggregator's settled ledger holds last year's 48 licence lots
and every loan. The collections manager wants the money to follow the holds lists.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the holds report, the prices, the state statistics, the ledger's turns and the lending policy. Every
  Romance licence really does circulate 20 times a year. No stakeholder read is overturned. The difficulty is which of those checkouts
  would not otherwise happen, and that is decided card by card.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the manager's view and the holds report. The ledger's turns and the state's series still certify rung 2 and
  send 43% of the grant to Romance.
* **Instrument repair.** Time every loan and hold to the second, as the ledger already does. Every lot still settles its full turns, and
  a card holding six loans still reads no more books.
* **Lens swap.** The naive read counts checkouts on new licences. The answer counts checkouts by cards with a free slot, a different
  population of borrowers.

## 3. The driving force

A strong solver drops the holds split for the grant's own rule, prices each collection's licences, and replaces the vendor's pooled 14
turns and the system's 30% print substitution with each collection's own, because only those reproduce the state's by-collection series.
Romance, at $22 a licence, 20 turns and almost no print substitution, then takes 43% of the grant. But the lending policy lets a card hold
six digital loans, and a delivered hold waits until one is returned. Romance's holds lists are filled by readers who are always at six:
replaying each card's loans through the ledger, 80% of Romance's hold-driven loans began only when the card returned another book. For
those readers a new licence changes which book comes next, not how many. In Non-fiction 3% of loans are slot-bound. Summed over the
system the limit looks irrelevant, with about 10,000 loans out against 186,000 slots on an average day.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Grant split by each collection's share of holds, sized at the vendor's 14 checkouts a licence | Adult fiction leads ($200k, 1.33× over Mystery); 305,665 checkouts (+85%) | The aggregator's own demand report on the vendor's own figure | The grant terms: the split follows added checkouts per dollar, and licences cost from $9 to $58 |
| 1 | Shares by the vendor's 14 turns net of the system's 30% print substitution, per dollar | Young readers leads ($280k, 2.33× over Romance); 416,794 (+152%) | The grant's rule on the system rates, which reproduce last year's state totals | The state statistics' by-collection series: digital loans run from 6 to 20 a licence and print substitution from 10% to 50% |
| 2 | Each collection's own turns from the ledger and its own substitution from the state series, per dollar | Romance leads ($260k, 2.17× over Non-fiction); 316,947 (+92%) | Reproduces all ten by-collection series and all 48 settled lots | The lending policy with the ledger's loans: 80% of Romance's hold-driven loans waited for a free slot |
| 3 | **Decisive:** rung 2 × the share of each collection's hold-driven loans taken by cards with a free slot, from replaying every card's loans against the six-loan limit | **Adult fiction $70k · Mystery & thriller $60k · Romance $90k · Non-fiction $210k · Young readers $170k; 165,000 added checkouts** | — | — |

* **Shape.** The graded objects are the five-way split and the added-checkouts figure. The largest share changes at every rung (Adult
  fiction, Young readers, Romance, Non-fiction), and every rung's figure sits at least 85% above the answer.
* **Position table.** Non-fiction's share ranks 4th on rung 0, 3rd on rung 1 and 2nd on rung 2 (2.17× behind Romance), and leads only
  rung 3 (1.24× over Young readers).
* **Discriminator dominance.** Romance carries 2.09× more net checkouts per dollar into rung 3 (0.82 against Non-fiction's 0.39). The loan
  limit keeps 0.97 of Non-fiction's and 0.20 of Romance's, an edge of 4.85×, 1.94 times the 2.50× floor. Product: 4.85 / 2.09 = 2.33.
* **Partial correction priced (L3).** No half-applied construction reaches the split. A solver who applies the slot-bound shares to the
  vendor's 14 turns and the system substitution puts Young readers first ($360k against Non-fiction's $130k, 2.77×) and claims 440,645.
  One who applies them without print substitution, or with the system's 30%, ships 70 / 60 / 70 / 160 / 240 with Young readers first
  (1.50×) and claims 263,350 or 184,345. One who checks the limit in aggregate finds it never binds and stays on Romance (2.17×), and one
  who applies the system-wide slot-bound share to every collection keeps rung 2's split and claims 136,720.
* **Grid.** Turns (vendor, collection) × substitution (system, collection) × loan limit (ignored or checked in aggregate, per card) gives
  8 cells. Ignoring the limit names Young readers (2.33×, 1.31×) or Romance (1.40×, 2.17×); applying it per card with either pooled rate
  names Young readers (1.50× to 2.77×). Only the answer cell names Non-fiction, and the nearest wrong figure is 184,345 (+11.7%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The lending policy sets the six-loan limit and says a delivered hold waits for a free slot. No document says a
   slot-bound loan adds nothing, or connects the limit to the grant.
2. **Corpus blind for a computable reason.** *In every settled lot the lot's loans equal its licences × its collection's turns whoever
   borrows, because a slot-bound card's displaced loan settles against another lot, never this one.* Collection turns reproduce 48 of 48
   lots, and no lot shows a shortfall.
3. **No arithmetic symptom.** Lots tie to the ledger's totals, the ledger's collection totals to the state series, and every rung's split
   sums to $600,000.
4. **Not a row predicate.** Each loan's status needs its card's loans replayed in time order against six slots, the hold's delivery time
   compared with the card's state, and then a share per collection.
5. **The enumeration is arithmetic.** No column marks a loan as slot-bound; 252,000 loans across 31,000 cards are replayed.
6. **No cutover date.** The limit and the readers' habits ran unchanged all year, and no series steps.
7. **Survives deletion.** Removing the holds report and the manager's view leaves the ledger and the state series certifying rung 2.

## 6. The calibration corpus

* **Form.** The aggregator's settled ledger: last year's 48 licence lots and every loan settled against any licence, with card, start,
  return and, for hold-driven loans, the delivery time.
* **What it certifies.** Each collection's turns (15, 13, 20, 12, 6), 48 of 48 lots. The vendor's pooled 14 matches the ledger's total and
  no single lot within 5%.
* **The state statistics' finer controls.** Four constructions reproduce last year's state totals (252,000 digital loans, 75,600 print
  loans replaced). The by-collection digital series rejects pooled turns and the by-collection print series rejects the pooled
  substitution; only collection turns with collection substitution pass both.
* **What it is blind to.** Slot-binding (above).
* **Twin pair.** Romance lots R07 and R19 are identical on every lot column: 400 licences at $22, nine holds a licence at purchase, 20
  turns, 8,000 settled loans. R07's borrowers were 80% slot-bound and R19's 60%, so they added 1,440 and 2,880 checkouts net of print, 2.0×
  apart. Only the card replay separates them.
* **Resemblance points at the decoy.** Romance's cart most resembles the ledger's best-settling lots, the only ones at 20 turns.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The grant terms: the $600,000 is split across the five collections in proportion to the added checkouts per dollar
  each collection's licences are expected to deliver next year, in $10,000 blocks by largest remainder; added checkouts are loans next
  year that would not otherwise occur, net of the print loans they replace. The lending policy: six digital loans per card at a time,
  21-day loans, and a delivered hold waits until the card has a free slot. The aggregator's price list.
* **Empirical pins.** Turns, from the ledger. Print substitution by collection, from the state series. Slot-bound shares, from the card
  replay.
* **Voices.** The collections manager: "The money should follow the holds lists. That's where readers are waiting." The digital services
  lead: "Romance turns twenty times a year. Nothing in the catalogue works harder."
* **Licensed wrong basis.** The grant terms record that the state library's grant review compares each collection's share with its share
  of holds and will present that comparison.

## 8. Determinism by construction

* **Replay.** Every loan's start and return and every hold's delivery are timed to the second, and no delivery falls in the same second as
  a return on the same card, so each delivery's slot state is unambiguous.
* **Stability.** Each collection's slot-bound share is the same in every quarter of the ledger within one point, so any twelve-month
  window gives the same share.
* **Independence.** Within each collection, slot-bound and free-slot loans show the same print substitution, so the two factors multiply.
* **Turns.** Every lot settled exactly its collection's turns.
* **Rounding.** The last three blocks go to Romance, Adult fiction and Non-fiction on remainders of 0.89, 0.85 and 0.68, 0.11 above Young
  readers' 0.57. The figure is 165,072, which rounds to 165,000.

## 9. Prompt sketch and deliverables

> The state's digital collections grant gives us $600,000 for e-book and audiobook licences next year, and the trustees want to see how
> it splits across our five collections, in $10,000 blocks, and how many added checkouts it buys, to the nearest thousand. Our collections
> manager says the money should follow the holds lists. Give me the split and the figure in two sentences I can read out, with
> `grant_split.csv`, a chart `value_per_dollar.svg`, and a one-page `trustees_note.docx`.

* `grant_split.csv` — each collection's share and added checkouts on the four bases, with the turns, substitution and slot-bound share
  behind each.
* `value_per_dollar.svg` — a script-rendered grouped bar chart: per collection, checkouts per $1,000 at the vendor's rate, on its own
  turns net of print, and net of slot-bound loans, the slot-bound part hatched, each collection's grant share printed above its group, and
  Romance's 80% annotated.
* `trustees_note.docx` — the split, the figure, why Romance's share falls, and the branch tables for asks A and B.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the nine branches, last year's median days from print hold placement to pickup and
  the share over 30 days. *Device:* a hold filled from another branch's copy is logged as a new hold record carrying `transferred_from`
  with its own placement time, and the circulation guide measures waits from the original placement. Measuring from the transferred
  record understates waits at the three branches that borrow most from others.
* **Ask B (device-carried).** For each branch, the share of last year's new cardholders who borrowed anything within 90 days. *Device:* a
  card replaced after loss gets a new number carrying `replaces`, and the registration guide dates a cardholder from the original
  registration. Counting replacements as new cardholders lowers the rate at the two branches with the most replacements.
* **Ask C (validity).** Each collection's share and added checkouts under each of the four rung bases; the state's ten by-collection series
  reproduced by system and by collection rates; settled lots reproduced (of 48) by the vendor's turns and by collection turns.
* **Decoupling.** Treating every loan as added changes no figure in asks A or B. Hold transfers and card registrations touch neither the
  settled ledger's loans nor the grant formula.

## 11. Rubric arithmetic

9 branches × 2 (ask A) + 9 branches (ask B) + 5 collections × 4 bases × 2 and 4 reproduction counts (ask C) + the five shares and the
figure + 5 named chart parts + 3 files ≈ 85 criteria.

## 12. World-building constraints

* Collections (Adult fiction, Mystery & thriller, Romance, Non-fiction, Young readers): holds shares 33.6% / 24.4% / 19.8% / 12.2% /
  10.0%; licence prices $58 / $42 / $22 / $26 / $9; turns 15 / 13 / 20 / 12 / 6; print substitution 0.35 / 0.35 / 0.10 / 0.15 / 0.50;
  slot-bound shares 0.25 / 0.45 / 0.80 / 0.03 / 0.03.
* Last year: 18,000 licences (8,500 / 4,500 / 1,500 / 2,500 / 1,000) settled 252,000 loans, 14.0 a licence, replacing 75,600 print loans
  (30%).
* Splits ($k): rung 0 200 / 150 / 120 / 70 / 60; rung 1 40 / 60 / 120 / 100 / 280; rung 2 50 / 60 / 260 / 120 / 110; answer 70 / 60 /
  90 / 210 / 170.
* Lots R07 and R19 match on every lot column.
* Hold transfers and card registrations never touch loans, lots or the grant formula.

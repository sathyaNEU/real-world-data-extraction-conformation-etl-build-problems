# RC22 — Which cause of the retailer's margin squeeze gets the procurement programme, when suppliers raise prices by replacing the item

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Economics · retail pricing and procurement |
| Mirrors | Cost and margin diagnostics at retailers and marketplaces (vendor cost increases at Amazon, supplier terms at Walmart and Costco), where a supplier raises its price by replacing an item with a near-identical successor that every price monitor treats as a new product |
| Decision shape | Which of N root causes gets the fix: one procurement programme for next year |
| Committed call | The cause the programme targets, and the points of gross margin it took between the second and fourth quarters |
| Gap · Pattern | Gap 2 (population) · S7 (every screen is right and the answer is what nothing flags: predecessor–successor item pairs, linked through the planogram slot), with E15 (a loud decoy and a quiet contamination, each with its own control) at rungs 1 and 2 |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #11 beats the headline trap, misses the quiet one · #7 uses the ready-made measure · #18 joins only on the visible key |
| Calibration form | Pilot log: last year's cost-challenge desk in two categories, every flagged increase challenged, with outcomes and the filed decisions |
| Driving force | The cost monitor flags price increases on continuing items, freight surcharges, promotional funding changes and shrink, each correctly. A supplier that delists an item and lists a slightly smaller pack at a higher unit cost creates no increase on any continuing item. The monitor books the margin lost to "range and mix". Only pairing each delisted item with the new item that took its planogram slot, a pair the monitor cannot express, shows those pairs carrying 0.40 of the 1.60 points lost. |

## 1. Situation

A national grocery retailer's gross margin rate fell 1.60 points between the second and fourth quarters. Its cost monitor attributes the squeeze to
list-price increases on continuing items (A), freight and energy surcharges (B), promotional funding suppliers withdrew (C) and shrink (E), with the
rest booked to range and mix. The head of trading wants to renegotiate list prices; logistics blames surcharges; the CFO thinks suppliers pulled
promotional money. Procurement will run one programme next year, against one cause, a list that also includes a cost audit of new items replacing
old ones (D). Last year a cost-challenge desk piloted in two categories.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: invoices, the monitor's flags and categories, the supplier terms log, the rebate ledger, the item
  master and the planogram history. Every flag is right under its definition, and each stakeholder's cause is real. Nothing is overturned;
  the largest cause sits in a population the monitor's grain cannot express.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete every voice and the licensed basis. The monitor's categories still reconcile to the squeeze, range and mix still
  reads as customers buying new things, and no flag marks a succession.
* **Instrument repair.** A perfect price monitor still compares an item with its own history, and a successor has none; the pair is a relation
  between two items, which only the planogram history records.
* **Lens swap.** The monitor attributes margin item by item; the answer attributes it to pairs of items, a population of relations the
  item-level ledger does not contain.

## 3. The driving force

A strong solver treats the monitor as a starting point. Many "list-price" increases turn out to be suppliers moving to delivered pricing (freight
folded into the list price), and the supplier terms log says which, so 0.20 points move to freight. Freight's fourth quarter also carries the
logistics provider's annual volume rebate, accrued through the year and reversed in the fourth quarter when the volume target was missed; the
rebate ledger shows it as a timing item, not a cost change, and 0.26 points come out. Promotional funding then leads, and every check passes.
The range-and-mix bucket still holds 0.44 points, read as customers trading into new products at lower margins. In 61 cases a supplier delisted an
item and, the same week, a new item from the same supplier took its exact planogram slot: the same product in a pack 8–12% smaller at the old pack's
cost, a higher unit cost the monitor never compares because the successor has no history. Linked through the slot, those pairs took 0.40 points.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The monitor's categories, as booked | A, list prices (0.46 pts) | The retailer's own reconciled decomposition, the head of trading's story | The supplier terms log: 0.20 points of "list-price" increases are suppliers moving to delivered pricing |
| 1 | Delivered-pricing conversions moved to freight | B, freight and energy (0.46) | The loud decoy beaten with its own control; freight now carries what it really is | The rebate ledger: 0.26 points of the fourth quarter's freight are the annual rebate reversed, a timing item |
| 2 | The rebate reversal removed as a timing item | C, promotional funding (0.32) | The quiet contamination found with its own control, every category reconciled | The planogram history: 61 delisted items were replaced in their slots the same week by the same supplier's smaller packs |
| 3 | **Decisive:** delisted and new items paired through the planogram slot, the successor's unit cost compared with its predecessor's | **D, increases via successions (0.40)** (5th of 5 on rung 0) | — | — |

* **Position table.** D ranks 5th on rungs 0–2, where no category can hold it, and leads only rung 3. Rung leaders beat their runners-up by
  1.44×, 1.44×, 1.23× and 1.25×.
* **Discriminator dominance.** Promotional funding carries 0.32 points into rung 3 and D carries none. The pairing moves 0.40 points out of
  the range-and-mix bucket, 1.25× promotional funding's figure against the 1.2× floor; the bucket keeps 0.04 points of genuine mix.
* **Partial correction priced (L3).** A solver who suspects shrinkflation and pairs delisted and new items by brand and description finds 140
  candidate pairs, most of them range changes with no common slot, and books 0.71 points to D, 78% high. One who pairs only items sharing a
  product code prefix finds 9 pairs, books 0.06 and names C.
* **Grid.** Freight reassignment (off, on) × rebate timing (in, out) × pairing (none, by description, by prefix, by slot) gives sixteen builds.
  Without pairing they name A, B or C; prefix pairing names A, B or C; description pairing names D at an inflated figure; slot pairing names D
  at 0.40 only with both earlier corrections, and A or B otherwise, because list prices (0.46) or freight (0.46) then still lead.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The monitor's guide defines its categories and says new items enter the cost index after twelve months of history.
   No document says suppliers replace items or that the planogram links them.
2. **Corpus blind for a computable reason.** *Every pilot category sold loose produce and in-store bakery under fixed weight-based codes, so
   no supplier could replace an item with a smaller pack and no succession pair exists in any pilot case.* The pilot certifies the decomposition
   and the recoverability of flagged increases, and cannot see successions.
3. **No arithmetic symptom.** Every category reconciles to the 1.60-point squeeze before and after pairing; item counts, invoices and planograms
   tie.
4. **Not a row predicate.** A succession is a relation between two items, found by matching a delisting to a listing in the same slot in the
   same week and comparing unit costs across pack sizes.
5. **The enumeration is arithmetic.** No column marks a successor; 61 pairs are built from the planogram history.
6. **No cutover date.** Successions happened item by item through the half; the dated events (the delivered-pricing switch in August, the rebate
   reversal in the fourth quarter) are the traps the ladder beats first.
7. **Survives deletion.** With every voice gone, the monitor and both controls still name promotional funding.

## 6. The calibration corpus

* **Form.** The pilot log: last year's cost-challenge desk in two categories, every flagged increase challenged with the supplier, the outcome
  (rescinded, phased, upheld), the margin recovered and the desk's filed decision on extending the programme.
* **What it certifies.** That the monitor's categories reconcile to category margin (to the basis point in both pilot categories) and how much
  of a flagged increase a challenge recovers.
* **What it is blind to.** Successions (above).
* **Twin pair.** Breakfast cereal and pet food carried identical range-and-mix buckets (0.9 points of category margin), identical flag counts
  and identical new-item shares. Succession pairs took 0.62 points of cereal's margin and 0.30 of pet food's (2.07×). Only slot pairing separates
  them.
* **Resemblance points at the decoy.** This year's range-and-mix bucket matches last year's, when it was a genuine premium range launch with no
  delistings, on size, categories and new-item share.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The procurement policy: next year's programme targets the cause that took the most gross-margin points between the second
  and fourth quarters, costs measured as incurred in the quarter. The supplier terms log and the rebate terms, one entry each.
* **Empirical pins.** The decomposition, from the pilot; pairs from the planogram history.
* **Voices.** The head of trading: "Suppliers pushed list prices all year; renegotiate them." The logistics director: "The surcharges are killing
  us, and the monitor says so."
* **Licensed wrong basis.** The policy records that the suppliers' trade body attributes retail margin changes by the monitor's categories and
  will present that view.

## 8. Determinism by construction

* **Pairs.** A delisting and a listing from the same supplier in the same planogram slot within seven days; every slot change in the half is
  either such a pair or a slot handed to a different supplier.
* **Unit cost.** Cost per base unit (gram, millilitre, sheet), from the item master's pack size; every pair shares a base unit.
* **Margin points.** The pair's unit-cost increase times the successor's volume in the fourth quarter, over the quarter's sales.
* **Timing.** The rebate reversal is identified in the ledger by its accrual period; no other timing item exceeds 0.01 points.
* **Rounding.** Margin points to two decimals; the committed figure sits mid-bin.

## 9. Prompt sketch and deliverables

> Our margin rate is down 1.6 points since the second quarter, and procurement gets one programme next year against one cause. The CFO is sure
> suppliers pulled promotional money. Tell me which cause the programme should go after and how many margin points it took, to two decimals, in
> one sentence for the trading board. Send `margin_squeeze.xlsx` and a chart `margin_bridge.png`.

* `margin_squeeze.xlsx` — the five causes under each construction, the price-tier sheet (ask A), the distribution sheet (ask B) and the pilot
  reproduction (ask C).
* `margin_bridge.png` — a waterfall from the second quarter's margin to the fourth's by cause, with the range-and-mix bar split into genuine mix
  and succession pairs, the two timing and reassignment adjustments marked, and three example pairs annotated with their unit costs.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 14 categories, fourth-quarter sales by price tier. *Device:* multi-buy offers record
  the whole discount on the qualifying unit's line, as the till data guide documents; tiering units on line prices pushes the discounted units
  into the lowest tier in five categories.
* **Ask B (device-carried).** For each of the six distribution centres, cases shipped and cost per case in the fourth quarter. *Device:*
  cross-docked cases appear at the receiving and the shipping centre with a cross-dock flag, as the warehouse system documents; counting both
  overstates two centres' volumes and understates their unit cost.
* **Ask C (validity).** For each pilot category, the category margin change and the monitor's decomposition of it; and each cause's points under
  each rung construction.
* **Decoupling.** Clearing the slot pairing changes no figure in asks A or B.

## 11. Rubric arithmetic

14 categories × 3 tiers (ask A) + 6 centres × 2 figures (ask B) + 2 categories × 6 figures + 5 causes × 4 constructions (ask C) + the targeted
cause, its points, the pair count and the runner-up + 5 named chart parts + 2 files ≈ 105 criteria.

## 12. World-building constraints

* Squeeze 1.60 points: monitor categories A 0.46, B 0.26, C 0.32, E 0.12, range and mix 0.44; delivered pricing moves 0.20 from A to B; the
  rebate reversal is 0.26 of B; succession pairs 0.40 of range and mix.
* 61 slot pairs, packs 8–12% smaller at the predecessor's pack cost; description matching finds 140 candidates, prefix matching 9.
* Cereal and pet food identical on every monitor column.
* Multi-buy lines and cross-dock rows touch no invoice cost, planogram slot or item-master pack size.

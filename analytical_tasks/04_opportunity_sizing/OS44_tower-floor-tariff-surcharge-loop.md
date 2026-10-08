# OS44 — The lowest 2030 tower price floor a fabricator can accept, when the plate surcharge is part of the value it is charged on

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Supply Chain & Logistics · wind-component manufacturing and procurement |
| Mirrors | Pass-through charges that sit inside their own base, with a cap that binds only once the loop is solved (tariff surcharges declared inside the customs value of delivered-duty-paid shipments at hardware and electronics makers, platform fees charged on prices that include the fee, management fees on project totals that include the fee) |
| Decision shape | One figure committed at a date: the lowest 2030 floor the company can accept in the frame agreement the board approves on the 28th |
| Committed call | The lowest 2030 price floor per tonne of XL tower the company can accept, to the nearest $10 |
| Gap · Pattern | Gap 4 (rule) over Gap 1 (time) · E23 (a self-referencing surcharge: the mill declares its surcharge-inclusive price as the customs value, so the duty it passes on is levied on itself, and the contract's collar binds only after the loop is solved), with E18 below it (heavy offshore plate priced on its own mill index, not the steel-mill-products shorthand) |
| Gate G mechanism | binding_constraint, with forecasting |
| Measured traps engaged | #22 solves a self-referencing rule in one pass · #14 coarsens the segment it was asked about · #10 notes a binding limit as a risk |
| Calibration form | Revision log: the plate mill's invoice revision log for the last two years, every delivered-duty-paid invoice with its first issue and, once customs liquidated the entry, its final revision |
| Driving force | The mill clears plate delivered duty paid and declares its own invoice price, surcharge included, as the customs value, so the 60% tariff it passes on is charged on itself. The surcharge solves to 150% of ex-works plus freight, and the plate contract's collar caps it at 120% of ex-works. Every liquidated invoice entered at today's 25% rate, where the loop gives a third and the collar never binds, and the 60% rate starts on 1 January, so the record pins the loop and never shows the collar. One pass prices XL plate at $1,872 a tonne, and the solved, collared surcharge prices it at $2,514. |

## 1. Situation

A wind-tower fabricator is negotiating a 2027–2030 frame agreement with a turbine maker for XL towers, the 15 MW class. The turbine maker
proposes a 2030 floor of $3,200 a tonne, and the company's pricing policy accepts no floor below its full forecast cost plus 8%. Heavy plate
is 1.08 tonnes of every tonne of tower. It comes from one mill under a delivered-duty-paid contract. The national steel tariff on imported
plate has been 25% for two years, and the published schedule raises it to 60% on 1 January. The board approves the agreement on the
28th. The turbine maker's procurement lead points out that tower prices have fallen every year for a decade.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the cost sheet, the learning curve, the plate index, the tariff schedule, the mill's invoices and
  their revisions. The procurement lead is right that tower prices fell for a decade. Nothing reported is overturned. The difficulty is a
  clause that puts the surcharge inside its own base.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the procurement lead's view and every voice. The mill's first issues still compute the surcharge in one pass,
  and no document says what the new rate will do once entries are liquidated.
* **Instrument repair.** Suspect file: the 38 open invoices of the last nine months, first issues awaiting liquidation. Repair: their final
  revisions, a third of ex-works plus freight. Rung 0, which prices today's rate as the mill invoices it, moves to $2,290; rungs 1 and 2
  never read invoices and stay at $2,561 and $3,121. No invoice exists at 60%, so the loop at the new rate and the collar must still be
  solved, and the answer stays $3,870. The cost sheet, index, schedule and liquidated log are complete and current.
* **Lens swap.** The answer prices 2030 plate under a rate and a collar that no closed invoice has faced, a different moment from last
  year's invoices, not the same cost under another lens.

## 3. The driving force

A strong solver discards the standard cost sheet, which predates the tariff, and adds the duty. It then prices plate on the contract's own
class, offshore heavy plate from 60 to 150 mm, rather than the steel-mill-products index the cost sheet escalates. Its 2030 floor is $3,121
a tonne, comfortably under the turbine maker's $3,200. The plate contract says the mill passes on the duty it pays and declares its invoice
price as the customs value, and the invoice price includes that surcharge. So the duty is charged on itself: surcharge = rate × (ex-works +
freight + surcharge), which at 60% solves to 150% of ex-works plus freight. The contract's collar limits the surcharge to 120% of
ex-works, which the one-pass surcharge never reaches and the solved surcharge exceeds. The mill's first issues compute the surcharge in
one pass. Its liquidated invoices, all at 25%, were each revised from a quarter to a third of ex-works plus freight.

## 4. The ladder

| Rung | Construction (2030 cost per tonne of tower × 1.08) | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Standard cost sheet: fabrication on the learning curve ($868), plate on the steel-mill-products index ($820 ex-works in 2030), duty at today's 25% as the mill invoices it | $2,206, −43.0% | The company's own cost sheet, the method its finance team signs | The tariff schedule: the rate on imported plate rises to 60% on 1 January, and the plate contract passes duty through |
| 1 | Duty at the scheduled 60%, in one pass on ex-works plus freight | $2,561, −33.8% | The tariff the floor year will face, priced on the shipment the way the mill computes a first issue | The plate contract's schedule prices XL plate on the offshore heavy-plate index: $1,120 ex-works in 2030, not the general index's $820 |
| 2 | Plate on its own class (E18), duty in one pass | $3,121, −19.4% | The right segment, the right rate, the mill's own first-issue method | The revision log: every liquidated invoice was revised from 25% to a third of ex-works plus freight |
| 3 | **Decisive:** surcharge solved on a declared value that includes it, capped at the collar (120% of ex-works) | **$3,869.8, committed as $3,870** | — | — |

* **Figure shape.** Every correction walks the floor up (+16.1%, +21.9%, +24.0%), and the answer is the maximum cell of the grid. The
  company should refuse $3,200.
* **The answer.** 2030 plate costs $1,120 ex-works, $50 freight and a $1,344 surcharge (the collar), $2,514 a tonne. With $868 of
  fabrication, a tonne of tower costs $3,583, and the floor is $3,869.8.
* **Partial correction priced (L3).** Scaling the one-pass surcharge by the liquidated invoices' revision ratio (4/3) gives $3,394
  (−12.3%): the ratio fits every closed invoice and is wrong at the new rate. Solving the loop at 60% without the collar gives $4,349
  (+12.4%). Each half lands at least 12% from the answer.
* **Grid.** Rate (today's 25%, scheduled 60%) × plate index (general, contract class) × surcharge (one pass, solved with the collar) = 8
  cells. The nearest are one pass at 60% on the contract class, $3,121 (−19.4%), and the solved surcharge on the general index, $3,100
  (−19.9%). Every cell at today's rate sits at least 28% below the answer.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The plate contract says how value is declared and that the surcharge passes on duty. No document joins the two,
   and the mill's open invoices compute the surcharge in one pass.
2. **The corpus pins the loop and is blind to the collar.** *In every liquidated invoice the solved surcharge was a third of ex-works plus
   freight, far below the collar, because every entry so far came in at the 25% rate; the 60% rate starts on 1 January.* The loop
   reproduces 96 of 96 final revisions and so does the 4/3 ratio. They part only at the new rate, where the collar binds.
3. **No arithmetic symptom.** First issues tie to the shipments, revisions tie to the liquidation notices, and the cost sheet reconciles to
   the ledger on every rung.
4. **Not a row predicate.** The surcharge is a fixed point of the declared value and then a minimum against a second quantity, the collar,
   computed per tonne.
5. **The enumeration is arithmetic.** No column holds the solved surcharge or says the collar binds.
6. **No cutover date.** The 1 January rate change is the dated decoy. The loop runs under today's rate too, and the collar is a standing
   clause.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The mill's revision log: 96 liquidated invoices, each with its first issue (a quarter of ex-works plus freight) and final
  revision (a third), and 38 open invoices from the last nine months, first issues at 25% awaiting liquidation.
* **What it certifies.** Ex-works prices, freight and tonnages, and the revision rule for liquidated entries. A solver who back-tests the
  first issues' one-pass method on closed entries finds it fails all 96 and is pushed to a ratio or to the loop.
* **What it is blind to.** The collar (above).
* **Twin pair.** 2030 plate lots 07 and 11 are identical on every price and quantity column of the order file a lookup reaches: tonnes,
  plate class, ex-works price ($1,120) and freight ($50). Lot 07 comes from the contract mill, delivered duty paid; lot 11 from a spot mill cleared by the
  company's own broker at ex-works plus freight. Their surcharges are $1,344 and $702 a tonne, 1.91× apart, and no one-pass rule tells them
  apart.
* **Resemblance points at the decoy.** The 2030 floor looks like last year's settled tower contracts on tonnage, class and plate share, and
  a solver who carries their realised surcharge rate (a third) lands at the ratio partial.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The pricing policy accepts no floor below full forecast cost plus 8%. The plate contract makes the mill importer of
  record, declares the invoice price as the customs value, passes the duty paid to the company as a surcharge and caps the surcharge at 120%
  of the ex-works price per tonne. Freight is $50 a tonne, and 2030 ex-works follows the offshore heavy-plate index at $1,120.
* **Empirical pins.** Fabrication cost from the learning curve on cumulative tonnes; plate per tonne of tower from the bill of materials;
  the revision rule from the log.
* **Voices.** The turbine maker's procurement lead: "Tower prices have fallen every year for a decade." The company's finance director:
  "Our cost sheet has never been more than 2% out."
* **Licensed wrong basis.** The frame agreement records that the turbine maker's board approves floors on the all-in tower price trend and
  will see that basis.

## 8. Determinism by construction

* **The loop.** The surcharge has one fixed point, rate ÷ (1 − rate) of ex-works plus freight, and iteration from any start converges to
  it.
* **The collar.** It binds at the solved surcharge by $411 a tonne and does not bind at the one-pass surcharge by $642, so no rounding of
  rates moves it.
* **Learning curve.** Fits on cumulative tonnes with or without the steel control give 2030 fabrication within $5 of $868.
* **Plate yield.** The bill of materials fixes 1.08 tonnes of plate per tonne of tower for the XL class.
* **Rounding.** $3,869.8 sits $4.8 from the nearest $10 rounding boundary.
* **Maturity.** Liquidation takes nine to eleven months: 96 entries are final, 38 recent ones are first issues at 25%, and no entry exists
  at 60%.

## 9. Prompt sketch and deliverables

> The turbine maker wants a 2030 floor of $3,200 a tonne in the XL tower frame agreement, and its procurement lead says tower prices have
> fallen every year for a decade. Tell me the lowest 2030 floor per tonne we can accept, to the nearest $10, in a sentence for the board
> paper. Send `floor_case.xlsx`, a chart `floor_build.png`, and a one-page `board_paper_note.pdf`.

* `floor_case.xlsx`: the build under the four rung bases, the surcharge under one pass, the 4/3 ratio and the solved loop with and without
  the collar, the inspection sheet (ask A) and the delivery sheet (ask B).
* `floor_build.png`: 2030 cost per tonne of tower as stacked bars (fabrication, plate, surcharge) for each rung basis, the turbine maker's
  $3,200 as a horizontal line, the collar marked on the surcharge segment and the committed floor labelled.
* `board_paper_note.pdf`: the committed floor, the surcharge build and why $3,200 is refused.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each quarter of last year, the average welding hours per tower section and the share of
  sections re-welded after inspection. *Device:* a re-inspection adds a row with the same section ID and a higher sequence number, and a
  section's result is its last inspection, per the quality manual. Counting rows as sections doubles the rework share in the quarter with
  the new line.
* **Ask B (device-carried).** For each of the company's four plants, last year's on-time delivery share and median days late. *Device:* an
  agreed reschedule adds an amendment row with a new promised date, and on-time is measured against the latest promise, per the frame
  agreement's delivery schedule. Using the original promise overstates lateness at the two plants with reschedules.
* **Ask C (validity).** The floor under each of the four rung bases; the revision log reproduced under one pass, the 4/3 ratio and the loop
  (0, 96 and 96 of 96); and the 2030 surcharge under the same three rules and the collared loop.
* **Decoupling.** Clearing the loop changes no figure in asks A or B, and neither touches plate invoices, tariffs or the cost sheet.

## 11. Rubric arithmetic

4 quarters × 2 (ask A) + 4 plants × 2 (ask B) + 4 bases + 3 reproduction counts + 4 surcharges (ask C) + the committed floor, the 2030
surcharge, plate cost and fabrication cost + 5 named chart parts + 3 files ≈ 39 criteria.

## 12. World-building constraints

* 2030: fabrication $868 a tonne of tower; 1.08 tonnes of plate per tonne; ex-works $1,120 (contract class) or $820 (general index);
  freight $50; tariff 25% today and 60% from 1 January; collar 120% of ex-works; margin 8%.
* Surcharges at 60% on the contract class: one pass $702, 4/3 ratio $936, solved $1,755, collared $1,344.
* Rung floors $2,206 / $2,561 / $3,121 / $3,870; partials $3,394 and $4,349; the other grid cells $2,290, $2,643, $2,757 and $3,100.
* The revision log: 96 liquidated invoices at 25%, each revised from 25% to 33.3% of ex-works plus freight; 38 open first issues at 25%.
  Lots 07 and 11 are identical on every price and quantity column.
* Inspection sequences and delivery amendments never touch plate invoices, the tariff schedule or the cost sheet.

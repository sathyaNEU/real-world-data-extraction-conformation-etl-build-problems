# FC03 — The go-live stock value for a slow-moving parts tail, when the new engine forecasts each part on its whole supersession chain

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Supply Chain & Logistics · aftermarket service-parts planning |
| Mirrors | Accepting a replacement planning engine against a shadow run when item identities are revised over time (Apple and Cisco service-parts networks with engineering revisions, Amazon catalogue identifier merges, automotive OEM dealer-parts supersession) |
| Decision shape | One figure committed at a date: the target stock value of the tail at go-live, in the working-capital plan |
| Committed call | The go-live target stock value of the 2,410-part slow-mover tail, in dollars to the nearest $10,000, filed on 1 June |
| Gap · Pattern | Gap 4 (rule) over Gap 3 (objective) · Pattern B, the rule recovered from a closed corpus (the shadow run), with a binding limit applied in the figure |
| Gate G mechanism | method_or_model_selection, with forecasting and binding_constraint support |
| Measured traps engaged | #1 reports a failed back-test, ships anyway · #3 stops at a close but inexact match · #10 notes a binding limit as a risk |
| Calibration form | Parallel-run overlap: three months in which the new engine ran in shadow beside the legacy engine, both computing every in-scope part's order-up-to level from the same history |
| Driving force | The shadow run is the acceptance test, and the engine specification applied to each part number's own history reproduces 83% of it. Every miss is a part that superseded another. The engine forecasts a part on the demand of its whole supersession chain, walked hop by hop, converted by each link's quantity-per and cut at each effective date. The chain lives in the catalogue's supersession records, and no document says the engine reads them. |

## 1. Situation

An aftermarket parts distributor moves its 2,410-part slow-mover tail to a new replenishment engine on 1 July. Finance files the
working-capital plan on 1 June and needs the tail's target stock value at go-live. The vendor ran the engine in shadow for three months
beside the legacy engine. The contract's acceptance clause says a configuration may be used for planning only if it reproduces every
order-up-to level in the shadow run. The engine specification sets the methods, smoothing constants, review cycle and the stocking rule
for new parts.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the order history, the shadow-run outputs, the specification, the catalogue, the slotting register
  and standard costs. No one's claim about their own numbers is overturned. The difficulty is that the history a part is forecast on is
  not the history filed under its part number.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the finance analyst's view and the legacy engine's outputs. The specification run on per-part history still
  reproduces 83% of the shadow run and still files a figure 31% low.
* **Instrument repair.** Make every order line and every catalogue record perfect. The supersession records are already complete; what
  remains is a construction no record states.
* **Lens swap.** The naive read and the answer differ in population: the demand recorded against 412 successor part numbers since their
  introduction, against the demand of the chains they inherited.

## 3. The driving force

A strong solver implements the specification exactly, cleans the order history, applies the warehouse's bin limits, and back-tests on the
shadow run as the clause demands. It finds 1,236 of 7,230 cells wrong. Every miss is low and sits on a recently introduced part number,
which the specification's new-part rule stocks at one unit until it has twelve months of history. The misses look like start-up noise in
a vendor's black box. They are the engine's history construction. A successor part is forecast on its predecessors' demand: walk the
catalogue's supersession records back through every hop, multiply each link's demand by its quantity-per, and take each predecessor's
demand only up to its effective date. Recently revised parts are the tail's fastest movers, so their inherited history carries 45% of the
capped stock value.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The specification on each part number's own order history, uncapped, × standard cost | $4.37M, −10% | The engine exactly as specified, on the system of record | The EDI interface log: 12% of order lines are retransmissions of a dealer PO line already posted |
| 1 | Hygiene: retransmissions removed, same construction | $3.90M, −20% | Clean history, and the shadow run's cells on parts with retransmissions now match | The slotting register and the warehouse rule: a slow mover is held only in its assigned bin |
| 2 | **E14 (binding limit):** each target capped at its bin capacity in units | $3.35M, −31% | Specification, clean history, physical limits: every reconciliation passes, and 83% of the shadow run matches | The shadow run and the acceptance clause: 1,236 cells miss, all low, all on successor parts |
| 3 | **Decisive:** history built along each supersession chain (every hop, quantity-per, effective-date cut), then the specification and the bin caps | **$4.86M** | — | — |

* **Figure shape.** Three corrections walk the figure down (−10%, −20%, −31%) and the decisive rung reverses them (×1.45 on the capped
  figure), so a solver who stops short is low in a known direction.
* **Partial correction priced (L3).** Merging only direct supersessions lands at $4.31M (−11%). Merging chains without the quantity-per
  conversion lands at $4.35M (−10.5%). Carrying a predecessor's demand past its effective date lands at $5.41M (+11%).
* **Grid.** Retransmissions (kept, removed) × bin caps (off, on) × history construction (per part, one hop, no conversion, with residual,
  full chain) = 20 cells. The nearest wrong cells are rung 0 (−10%) and the unconverted chain (−10.5%), each one omission away. The full
  chain without de-duplication sits at +11% and the full chain uncapped at +16%.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The specification says forecasts use "the part's demand history". The supersession records ship as catalogue
   data for the parts lookup, and no document links them to forecasting.
2. **The reproduction numbers.** The full chain construction reproduces 7,230 of 7,230 shadow cells to the unit. The best rival (merge
   without conversion) reproduces 7,056, the one-hop merge 6,939, the residual-carrying merge 7,107, and per-part history 5,994. Per-part
   misses all fall low, and it sits 24% under the shadow run's total. The reproducing rule is a construction (a variable-length walk with
   a conversion and a date cut per hop), not a setting a solver sweeps.
3. **No arithmetic symptom.** Order lines tie to invoices, de-duplicated lines tie to dealer POs, and capped targets fit their bins.
   Nothing fails except the clause's test.
4. **Not a row predicate.** A successor's history is a sum over an unknown number of predecessors, each converted and date-cut, reached
   by repeated self-joins on the supersession records.
5. **The enumeration is arithmetic.** Which parts inherit what is computed by the walk; no column says "inherited demand".
6. **No cutover date.** Supersessions are spread over six years, and the engine change is in the future.
7. **Survives deletion.** No wrong number exists to delete. Without the voices and the legacy outputs, rung 2 is still where a careful
   build stops.

## 6. The calibration corpus

* **Form.** The shadow run: for each of the 2,410 parts and each of three months, the new engine's order-up-to level and the legacy
  engine's, computed from the same history (7,230 cells per engine).
* **What it pins (Pattern B).** The history construction, through 412 successors: 97 on chains of two or more hops, 58 with a
  quantity-per of 2 or 4, and 41 whose predecessor kept selling after the effective date. Each rival fails a distinct class of these.
* **Twin pair.** P-44817 and P-51230 are identical on every master column: lumpy segment, $212 standard cost, bin class, nine months of
  identical own demand, and a direct predecessor with 15 months of demand. Their shadow levels are 38 and 19 units (2.0×), because
  P-44817's predecessor itself superseded a part with 24 more months of demand. One-hop merging gives both 19, and per-part history gives
  both one unit.
* **Resemblance points at the decoy.** Successors resemble genuinely new parts on every master column (introduced within 18 months,
  short own history), and the legacy engine stocks them lean, as the new-part rule would.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The contract: a configuration is used for planning only if it reproduces every shadow-run level. The specification:
  SBA for intermittent and lumpy parts, SES for the rest, α = 0.1, monthly review, one-month lead time, and one unit for a part with fewer
  than twelve months of demand history. The warehouse rule: a slow mover is held only in its assigned bin. The costing standard: stock is
  valued at the go-live standard cost.
* **Empirical pins.** The history construction, from the shadow run. Bin capacities in units, from the slotting register.
* **Voices.** The planning manager: "The vendor's engine is a black box; the specification is what we configured." Finance's analyst:
  "New part numbers should be stocked lean until they prove themselves."
* **Licensed wrong basis.** The specification's cover note records that finance's working-capital model values the tail at the legacy
  engine's levels and will present that valuation at the budget review.

## 8. Determinism by construction

* **Chains.** Supersession records are acyclic, each part has at most one successor, and every effective date falls on a month
  boundary, so the date cut is unambiguous. Quantity-per is 1, 2 or 4.
* **Retransmissions.** Each retransmitted line repeats a dealer PO and line number and is flagged in the interface log; de-duplicating on
  either gives the same history.
* **Segments.** Segment classification on chain-built history is what the shadow run used, and no part sits within 0.02 of an ADI or
  CV² cut-off under either history.
* **Caps and costs.** Bin capacities are whole units, and no capped part's target sits within one unit of its cap under the answer
  construction. Standard costs are one row per part at the go-live date.
* **Rounding.** The unrounded answer is $4,862,300, far from a $10,000 boundary.

## 9. Prompt sketch and deliverables

> I file the working-capital plan on 1 June, and I need the target stock value for the slow-mover tail on the day the new engine goes
> live, to the nearest $10,000. Finance's analyst thinks new part numbers should be stocked lean until they prove themselves. Send me
> `tail_stock_value.xlsx`, a chart `shadow_run_match.png`, and a one-page `go_live_value_note.pdf` that commits to the figure.

* `tail_stock_value.xlsx` — the value build part by part, the returns sheet (ask A) and the lead-time sheet (ask B).
* `shadow_run_match.png` — shadow-run level against rebuilt level for all 2,410 parts in one panel per history construction, log axes,
  successors coloured by chain depth, the 45° line, and the twin parts annotated.
* `go_live_value_note.pdf` — the committed figure and the alternatives finance will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 14 dealer regions, slow-mover returns over the last twelve months in units and
  value, and the share returned within 30 days of shipment. *Device:* a credit memo that reverses a mis-shipment carries reason code MS and
  is not a return, as the returns manual documents. Counting every credit memo overstates returns in five regions. Returns never enter
  the engine's demand history.
* **Ask B (device-carried).** For each of the 12 supplier lead-time classes, the median and 90th-percentile purchase lead time over the
  last twelve months. *Device:* a PO line received in parts posts one receipt row per delivery, and the procurement manual measures lead
  time to the receipt that completes the line. Per-row lead times understate the 90th percentile in seven classes. The engine uses a
  filed one-month lead time.
* **Ask C (validity).** For each of the five history constructions, its shadow-run hits out of 7,230 and the go-live value it implies.
* **Decoupling.** Replacing chain-built history with per-part history changes no figure in asks A or B.

## 11. Rubric arithmetic

14 regions × 2 (ask A) + 12 classes × 2 (ask B) + 5 constructions × 2 (ask C) + the committed figure, the successor count and the
number of parts at their bin cap + 5 named chart parts + 3 files ≈ 73 criteria.

## 12. World-building constraints

* 2,410 parts; 412 successors (97 multi-hop, 58 with quantity-per 2 or 4, 41 with post-effective predecessor demand). Recently revised
  parts are the tail's fastest movers.
* Retransmissions inflate order lines by 12%. Bin caps bind on 186 parts under the answer.
* Rung figures $4.37M / $3.90M / $3.35M / $4.862M. Partial cells $4.31M, $4.35M, $5.41M. No non-answer cell of the 20-cell grid is
  within 10% of the answer.
* Shadow-run hits: 7,230 / 7,107 / 7,056 / 6,939 / 5,994. P-44817 and P-51230 are identical on every master column.
* Credit-memo reason codes and partial receipts never touch order history, supersession records or bins.

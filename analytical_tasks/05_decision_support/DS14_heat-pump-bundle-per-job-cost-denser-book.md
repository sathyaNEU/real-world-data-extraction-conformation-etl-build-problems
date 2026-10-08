# DS14 — Which heat-pump bundle wins the multi-family contract, when every installer's per-unit quote carries a per-job cost the new book spreads four ways

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Policy & Education · utility efficiency programmes |
| Mirrors | Choosing a supplier on per-unit prices quoted from one order profile and applied to another (Amazon and Apple supplier quotes that amortise set-up costs, cloud commitments priced on one usage shape and run on another, agency fees with fixed management components) |
| Decision shape | Which of N gets one scarce thing: next year's bulk contract, awarded to one model-and-installer bundle |
| Committed call | The bundle that gets the contract, and its verified lifetime savings per $1,000 of programme cost, in MWh to two decimals |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · S6, a correct per-unit share carried onto a denser book, with the climate segment coarsened (#14) at rung 1 and the evaluator's verification at rung 2 |
| Gate G mechanism | decomposition_attribution, with forecasting |
| Measured traps engaged | #14 coarsens the segment it was asked about · #7 uses the ready-made measure · #13 validates on one population, applies to another · #15 follows the requester's hunch over the rule |
| Calibration form | Gold-standard verification subsample: the programme evaluator's metered savings on a random 8% of last year's installs |
| Driving force | Each installer's quote per unit is correct for last year's book, where almost every job was one unit in one house. Part of every quote is per job (survey, permit, panel upgrade, commissioning), and next year's multi-family book averages 4.2 units per job. Carrying last year's per-unit price onto that book pays the per-job part once per unit. The split is written nowhere. It is recovered by fitting each installer's invoices on units per job, and it halves the cost of the Elm bundle while barely moving Dalton's. |

## 1. Situation

A utility's efficiency programme will award next year's bulk heat-pump contract to one bundle: one model, installed by one contractor. The
programme plan gives the contract to the bundle with the most verified lifetime savings per programme dollar on next year's book, which is
climate-zone-6 multi-family retrofits at 4.2 units per job. Six bundles have bid. The programme holds the technical reference manual's
deemed savings (with a convenience table for "cold zones 5–7"), each installer's quoted installed cost per unit, last year's invoices
(including a small multi-family pilot), and the evaluator's metered subsample. The programme manager wants the contract on the model that
tops the efficiency scorecard.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct and no stakeholder read is overturned. The scorecard, the deemed savings, the convenience
  table, the quotes, the invoices and the metered subsample are all right for what they cover. The difficulty is that a quote per unit is
  an average over last year's job sizes, and next year's job sizes are different.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the manager's view and the scorecard. Verified zone-6 savings over quoted cost still name the Dalton bundle, and
  every figure ties to its source.
* **Instrument repair.** Meter every install and audit every invoice. Last year's per-unit cost is still exact for last year, and a
  single-unit job still carries its whole per-job cost on one unit.
* **Lens swap.** The naive read prices each bundle on last year's jobs. The answer prices it on next year's jobs, a different book whose
  density changes what a unit costs.

## 3. The driving force

A strong solver ignores the efficiency scorecard because the plan counts savings per dollar. It takes zone-6 savings from the manual,
because the convenience table's zones 5–7 average is mostly mild zone-5 houses, and it swaps deemed for metered savings, because the
evaluator's subsample shows Dalton's variable-speed compressor beating its deemed figure by 15% while Birch loses 30% to defrost. Each step
is competent, and Dalton leads. But every installer quoted a single price per unit, and last year almost every job was one unit. The
invoices tell the rest. Including last year's pilot jobs of two to six units, each installer's invoices fit exactly a per-job amount plus
a per-unit amount. Elm's installer carries $9,200 per job (it does the panel upgrades itself) and $5,000 per unit. Dalton's carries $1,600
and $12,000. On 4.2-unit jobs Elm's cost per unit falls from $14,200 to $7,190, and Dalton's from $13,600 only to $12,380.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Deemed savings from the convenience table (cold zones 5–7) per $1,000 of quoted cost | A, Aster (4.92) | The programme's own table and the installers' own prices | The programme plan: next year's book is zone 6, and the manual's zone-6 savings for Aster are 41% below the 5–7 average |
| 1 | Deemed zone-6 savings per quoted dollar (#14) | C, Cedar (4.15) | The segment the plan names, from the manual | The evaluator's subsample: metered zone-6 savings run from 0.70× (Birch) to 1.38× (Elm) of deemed |
| 2 | Verified zone-6 savings per quoted dollar | D, Dalton (3.89) | Metered savings and the installers' own prices: what the plan asks for | Last year's invoices: every installer's job totals fit a per-job plus per-unit price, and next year's jobs hold 4.2 units |
| 3 | **Decisive:** verified zone-6 savings over the forward cost per unit (per-job amount ÷ 4.2 + per-unit amount, both fitted from each installer's invoices) | **E, Elm (5.76)** (4th of 6 on rung 0) | — | — |

* **Position table.** Elm is 4th on rung 0 (3.38), 6th on rung 1 (2.11, because its deemed curve uses the 47°F rating) and 3rd on rung 2
  (2.92). It leads only rung 3, 1.35× over Dalton (4.27). Rung margins: 1.21, 1.23, 1.30, 1.35.
* **Discriminator dominance.** Dalton carries a 1.33× advantage into rung 3 (3.89 against 2.92). The forward cost moves Elm by ×0.506 and
  Dalton by ×0.910, a relative swing of 1.80. Product: 1.80 / 1.33 = 1.35, Elm's final margin.
* **Partial correction priced (L3).** Re-costing with the programme-wide average per-job cost ($4,000 for every installer) names Dalton (5.01
  against Cedar's 4.03). The half-insight hands the contract back to rung 2's decoy. Re-costing without the evaluator's verification names
  Cedar, and re-costing on the convenience table names Aster.
* **Grid.** Segment (zones 5–7, zone 6) × savings (deemed, verified, which only exists at zone 6) × cost (quote, forward) gives 6 feasible
  cells, naming A, A, C, C, D and E. The nearest wrong cell is the forward cost on deemed zone-6 savings (Cedar, 1.06× over Elm), and it costs
  one omission: the subsample.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The quotes are single prices per unit, and the invoices are totals. No document separates a per-job cost or says
   next year's density changes the price.
2. **No sweepable corpus nominates it.** *Every metered install in the subsample sat in a single-unit job, because last year's programme
   served single-family homes and the pilot's multi-unit jobs were not metered.* So the subsample's cost per unit equals its job cost, and it
   certifies savings while saying nothing about how a quote splits.
3. **No arithmetic symptom.** Quotes reproduce last year's average cost per unit for every installer exactly. Shares sum to every invoice
   total under either reading.
4. **Not a row predicate.** It needs a fit within each installer of invoice totals on units per job, and then a re-cost at the forward book's
   density.
5. **The enumeration is arithmetic.** No column gives a per-job amount; each one is a fitted intercept.
6. **No cutover date.** The book changes because the programme's target changes, and no outcome series steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The evaluator's subsample: 8% of last year's installs, drawn at random, with metered heating and cooling energy against a
  metered baseline year, by model and zone.
* **What it certifies.** Verified-to-deemed ratios by model at zone 6 (Aster 0.85, Birch 0.70, Cedar 0.72, Dalton 1.15, Elm 1.38, Fenwood
  0.85). Rung 2 is exact, so a solver who checks its savings against the evaluator is confirmed.
* **What it is blind to.** Cost structure (above).
* **Twin pair.** Elm's installer and the installer of last year's Gable bundle (not bidding this year) both quoted $14,200 per unit, and
  their last-year books are identical on every column a lookup sees: 46 single-unit installs, zone 6, the same mean house size. On next year's 4.2-unit jobs their costs per unit
  are $7,190 and $13,450 (1.87×). Only the per-job fit separates them.
* **Every rule exercised.** Every installer did at least five pilot jobs of two to six units, so each intercept is identified. One installer's
  fit has a near-zero intercept, which tests that the construction does not impose a per-job cost.
* **Resemblance points at the decoy.** Elm's profile (a newer cold-climate model, a higher quote, no 5°F rating in the manual) resembles the
  bundles that ranked lowest in last year's award.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The programme plan: the contract goes to the bundle with the most verified lifetime savings per programme dollar on next
  year's book. It also states next year's book: zone-6 multi-family retrofits at 4.2 units per job. The evaluation plan: savings are counted
  as the evaluator verifies them. One sentence each.
* **Empirical pins.** The per-job and per-unit amounts, from the invoices. The verification ratios, from the subsample.
* **Voices.** The programme manager: "Aster tops the efficiency scorecard; give it to the best equipment." The procurement lead: "We pay
  installers per unit; the quote is the cost." The evaluation lead: "Deemed values are what the regulator accepts."
* **Licensed wrong basis.** The programme plan records that the utility commission's staff review procurement on deemed savings per quoted
  dollar from the manual's tables and will see that basis.

## 8. Determinism by construction

* **The fit.** Every installer's invoices are exactly a per-job plus a per-unit amount, so least squares, two-point and median fits all
  return the same intercept and slope.
* **Density.** The plan files 4.2 units per job, and a job never splits across installers.
* **Savings life.** The manual's measure life (18 years) applies to all six models, and verification ratios multiply lifetime deemed
  savings.
* **Rounding.** The figure is filed to two decimals, and Elm's 1.35× margin exceeds any rounding.

## 9. Prompt sketch and deliverables

> Next year's bulk heat-pump contract goes to one model-and-installer bundle, and the programme manager wants it on the model that tops the
> efficiency scorecard. Tell me which bundle gets it and its lifetime savings per thousand programme dollars, in MWh to two decimals, for the
> procurement paper. Send `bundle_case.xlsx`, a chart `cost_per_unit.png`, and a one-page `procurement_paper.pdf`.

* `bundle_case.xlsx` — the six bundles under each construction, the timeline sheet (ask A), the QA sheet (ask B) and the fit sheet (ask C).
* `cost_per_unit.png` — each installer's cost per unit against units per job as a fitted curve, last year's mean density and next year's
  4.2 as labelled reference lines, the six bundles' verified savings per $1,000 at 4.2 as a ranked inset, and Elm's and Dalton's
  quotes annotated.
* `procurement_paper.pdf` — the committed bundle and figure, and why the scorecard leader does not win.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each installer, the median days from contract to commissioning last year. *Device:* a job
  paused for a utility service upgrade carries a paused interval in the job log, and the programme's timeline standard excludes paused days.
  Raw dates overstate two installers by three weeks.
* **Ask B (device-carried).** For each bundle, the share of last year's installs needing a refrigerant-charge correction at the 30-day
  check. *Device:* the QA log records one row per refrigerant circuit, and multi-zone units have two. Counting rows instead of installs
  inflates the two multi-zone bundles by a half.
* **Ask C (validity).** Each installer's fitted per-job and per-unit amounts, each model's verification ratio, and each bundle's figure under
  the four rung constructions.
* **Decoupling.** Clearing the forward re-cost changes no figure in asks A or B. Paused intervals and QA circuits never enter a cost or a
  saving.

## 11. Rubric arithmetic

6 installers (ask A) + 6 bundles (ask B) + 6 × 2 fitted amounts + 6 ratios + 6 × 4 rung figures (ask C) + the committed bundle, its
figure and the runner-up + 6 named chart parts + 3 files ≈ 66 criteria.

## 12. World-building constraints

* Lifetime MWh per unit, zones 5–7 / zone 6 deemed / zone 6 verified: Aster 64 / 38 / 32.3, Birch 53 / 57 / 39.9, Cedar 48 / 49 / 35.3,
  Dalton 45 / 46 / 52.9, Elm 48 / 30 / 41.4, Fenwood 42 / 40 / 34.0.
* Quotes ($k per unit) and fitted per-job amounts: Aster 13.0 / 5.0, Birch 17.5 / 4.0, Cedar 11.8 / 1.0, Dalton 13.6 / 1.6, Elm 14.2 / 9.2,
  Fenwood 12.0 / 2.0. The per-unit amount is the quote less the per-job amount.
* Rung figures (MWh per $1,000): 4.92 / 4.15 / 3.89 / 5.76 for the four leaders. The average-per-job partial gives Dalton 5.01.
* The twin quotes are identical on every last-year column. Paused intervals and QA rows never touch invoices, savings or quotes.

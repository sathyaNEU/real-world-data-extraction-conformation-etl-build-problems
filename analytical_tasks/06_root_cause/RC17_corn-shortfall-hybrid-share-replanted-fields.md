# RC17 — How much of the state's corn shortfall the new hybrid family caused, filed before the seed company decides on a field review

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Economics · agricultural production and input markets |
| Mirrors | Attributing a KPI miss to a newly launched product when the launch roster is not the population that used it (a Google or Apple feature flag set on accounts that later opted out, a Meta ad product booked by advertisers who switched before launch, Amazon orders substituted at fulfilment) |
| Decision shape | One figure committed at a date (a component): the new family's share of the state shortfall, filed at the product meeting on the 20th |
| Committed call | The new hybrid family's contribution to the state's yield shortfall against trend, in bu/acre to one decimal |
| Gap · Pattern | Gap 2 (population) · E33 (the population a flag suggests: the seed-order flag against the fields actually planted, set by dated replant orders), with E19 (a latent attribution marker: field geometry identifies irrigation) at rung 2 |
| Gate G mechanism | decomposition_attribution, with confirm_surface_read support |
| Measured traps engaged | #5 takes the population a flag or filter suggests · #17 guesses an attribution the data can settle · #14 coarsens the segment it was asked about |
| Calibration form | Gold-standard verification subsample: 300 fields the agronomy team visited, with the hybrid planted, the practice and any replant verified |
| Driving force | The grower database flags a field with the hybrid on its seed order. After the June flood, 9% of fields ordered with the new family were replanted late with an older hybrid from a second, dated order, and the flag still names the new family. Those late fields yielded worst, so the flag hands the flood's damage to the new hybrid. Only joining the dated replant orders recovers the fields actually planted to it, and the company's verified subsample reproduces only that population. |

## 1. Situation

A seed company's regional team watched the state's corn yield come in 9 bu/acre below trend in a year of near-normal weather. Sales blames a new
hybrid family that took a large share of orders; the agronomists point to corn acres pushed onto dryland after a price rally. On the 20th product
management decides whether to fund a field-performance review of the new family, which its charter allows only if the family's contribution to the
shortfall is at least 2.0 bu/acre. The company's grower database covers 41% of the state's corn acres, field by field, and its agronomy team
verified a random subsample of 300 fields in person.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: county yields and trends, the grower database's order flags and yields, the replant orders, field
  boundaries and the verified subsample. Sales is right that the new family's flagged fields yielded less; the agronomists are right about the
  dryland shift. Nothing is overturned; the figure is the size of the component sales names.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices, the head of product's belief and the licensed basis. The order flag still defines the new family's
  fields and the shift-share still credits it with more than the review line.
* **Instrument repair.** A perfect seed-order system records the same two orders for a replanted field, each correct for its date; the flag
  is right about the order and silent about the replant by design.
* **Lens swap.** The naive build compares fields ordered with the new family; the answer compares fields planted with it, a different
  population that excludes the flood's late replants.

## 3. The driving force

A strong solver discounts the raw comparison, builds the shift-share against county trends so the dryland shift is booked as mix, and fills the
practice field (missing for 30% of fields) the right way: pivot-irrigated fields are circles and quarter-circles in the field boundary file, a
signal that reproduces every verified practice in the subsample. On that build the new family accounts for 2.3 bu/acre and the review is funded.
The family is identified, though, by the flag the seed order set. A June flood drowned low fields across three districts, and growers replanted
them in late June with whatever hybrid the dealer had left, under a second order dated after the first. The flag still names the new family on
those fields. Late-planted corn yields far below trend whatever the hybrid, so the flag charges the flood to the new family and credits the
older hybrids with fields they never had. With fields assigned to the hybrid actually planted (the latest dated order before harvest), the new
family's contribution is 1.2 bu/acre.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Flagged new-family fields' yield gap to other fields, scaled by its acreage share | 4.8 bu/acre (+300%) | Sales' comparison, made exactly on the company's own fields | County trends: the state shortfall is mostly corn moving onto dryland, which this comparison books to the hybrid |
| 1 | Shift-share against county trends by practice, with missing practice filled from each county's dominant practice | 3.1 (+158%) | Mix and within separated, at the grain the state reports | The verified subsample: county defaults mislabel 52 of 300 fields' practice |
| 2 | The same with practice from field geometry (pivot circles and quarter-circles are irrigated) | 2.3 (+92%) | Geometry reproduces all 300 verified practices; every input is now exact | The replant orders: 9% of order-flagged fields carry a second, dated order for an older hybrid after the June flood |
| 3 | **Decisive:** fields assigned to the hybrid on the latest dated order before harvest, then the same shift-share | **1.2 bu/acre** | — | — |

* **Figure shape.** Every correction walks the figure down (−35%, −26%, −48% per step), and the answer is the minimum cell, so every partial
  application funds the review the answer declines.
* **Partial correction priced (L3).** A solver who distrusts the order flag and switches to the hybrid label the combine operator keyed at
  harvest picks up labels operators left unchanged from field to field and lands at 3.6 (+200%), further than rung 2.
* **Grid.** Mix control (none, shift-share) × practice (county default, geometry) × population (order flag, latest dated order) gives eight
  cells from 1.2 to 4.8. The nearest wrong cell is 1.9 (+58%), which needs the replant join made with county-default practice.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The charter says "fields planted to the family"; the database's flag is documented as the hybrid ordered. No document
   mentions replants or says which order governs.
2. **The subsample pins a construction, not a menu.** The latest dated order before harvest matches the verified hybrid on 300 of 300 fields;
   the order flag on 273, the harvest label on 241. The flag's 27 misses are all flood replants, so it errs one way and overstates the new
   family's verified deficit by 61% on the subsample total. The rule is an ordering of each field's orders by date, then a join, not a setting.
3. **No arithmetic symptom.** Fields, acres and production reconcile to the database totals and to county statistics under every population.
4. **Not a row predicate.** A field's hybrid depends on every order attached to it and their dates relative to the planting window and the
   flood, read across two records.
5. **The enumeration is arithmetic.** No column marks a replant; 9% of flagged fields are rebuilt from the order history.
6. **No cutover date.** The flood is a dated event, and alignment to it shows a drop in the flooded districts that the decoy story absorbs;
   the decisive fact is which hybrid stood in each field, not when the water came.
7. **Survives deletion.** With every voice gone, the geometry build still files 2.3 and funds the review.

## 6. The calibration corpus

* **Form.** The verified subsample: 300 fields drawn at random from the database, each visited by an agronomist who recorded the hybrid in the
  ground, the practice and whether the field was replanted, with the field's database record and orders.
* **What it pins.** Practice from geometry (300 of 300 against 248 for county defaults) and the planted population (above).
* **Twin pair.** Fields F-2210 and F-2287 are in the same county, flagged with the new family, dryland, with the same soil productivity index
  and the same order date. They yielded 182 and 91 bu/acre (2.0×): F-2287 was flooded and replanted on 21 June with an older hybrid. Only the
  dated-order rule separates them.
* **Resemblance points at the decoy.** The new family's flagged fields resemble the launch year of the company's previous family, which did
  carry a real deficit, on share, districts and yield gap.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The product charter: a field-performance review is funded when a family's contribution to the state shortfall against
  trend, measured on the fields planted to it, is at least 2.0 bu/acre. County trend yields from the published series.
* **Empirical pins.** Practice from field geometry and the planted hybrid from the latest dated order, both from the subsample.
* **Voices.** The sales director: "The new family is underperforming everywhere we sold it." The district agronomist: "Corn went onto dryland
  after the price rally; that's your mix effect."
* **Licensed wrong basis.** The charter records that the seed trade association benchmarks hybrids on order-flagged fields and will present
  its comparison at the meeting.

## 8. Determinism by construction

* **Latest order.** A field's planted hybrid is on its latest order dated before 15 July; no order falls between 10 and 20 July.
* **Practice.** Boundaries whose area-to-circumscribed-circle ratio is above 0.75 for a full or quarter circle are irrigated; no field sits
  between 0.6 and 0.75.
* **Trend.** County trends are the published 15-year fits; the figure is the within component times the family's planted acre share.
* **Scope.** Database fields only, scaled to state acres by the database's coverage weights, as the charter specifies.
* **Rounding.** One decimal; the answer sits mid-bin, 0.8 below the review line.

## 9. Prompt sketch and deliverables

> The state's corn came in 9 bushels below trend and product management decides on the 20th whether the new hybrid family gets a field-
> performance review. Our head of product is sure the hybrid is the problem. Tell me how many bushels an acre of the shortfall the new family
> accounts for, to one decimal, as the figure I put to the meeting. Send `hybrid_shortfall.xlsx` and a chart `shortfall_bridge.png`.

* `hybrid_shortfall.xlsx` — the four constructions, the district sheet (ask A), the seed-treatment sheet (ask B) and the subsample
  reproduction (ask C).
* `shortfall_bridge.png` — a waterfall from the 9 bu/acre shortfall to the new family's contribution (mix, practice, other within, replant
  reassignment), with the 2.0 review line as a reference and the flooded districts' replanted acres as an inset map.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the nine crop reporting districts, harvested acres and production this year and last.
  *Device:* the published county series suppresses small counties and reports them as one combined row per district, as its notes document;
  summing named counties alone understates five districts.
* **Ask B (device-carried).** For each of the four seed-treatment packages, units sold this season. *Device:* orders are taken in bags or in
  80,000-kernel units with a unit field, as the order guide documents; summing quantities across the field overstates the two packages sold
  mostly in bags.
* **Ask C (validity).** For each of the 300 verified fields, the hybrid and practice under each assignment rule; and the figure under each of
  the four rung constructions.
* **Decoupling.** Clearing the replant join changes no figure in asks A or B.

## 11. Rubric arithmetic

9 districts × 2 years × 2 figures (ask A) + 4 packages (ask B) + 3 assignment rules × 2 accuracy counts + 4 constructions (ask C) + the
committed figure, the replanted share and the review decision + 5 named chart parts + 2 files ≈ 65 criteria.

## 12. World-building constraints

* Figures by construction (bu/acre): 4.8, 3.1, 2.3, 1.2; other cells 1.9, 2.7, 3.4, 4.1; harvest-label partial 3.6.
* 30% of fields lack practice; 9% of fields flagged with the new family were replanted with an older hybrid after the June flood, all in three
  districts, at yields 40–55% below trend.
* Subsample: latest-order rule 300/300, flag 273, harvest label 241; geometry 300/300, county default 248.
* F-2210 and F-2287 identical on every database column except the second order.
* District combined rows and order units touch no field record or replant order.

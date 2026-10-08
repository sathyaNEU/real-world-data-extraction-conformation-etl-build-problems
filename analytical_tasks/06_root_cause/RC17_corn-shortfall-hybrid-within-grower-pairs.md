# RC17 — How much of the state's corn shortfall the new hybrid family caused, filed before the seed company decides on a field review

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Economics · agricultural production and input markets |
| Mirrors | Attributing a KPI miss to a newly launched product that reached a different kind of customer (a Google or Apple feature promoted to new accounts, a Meta ad product taken up by advertisers entering new markets, an Amazon programme offered to new sellers), where the product's users differ from everyone else in ways no segment column records and only comparisons within one customer separate the product from the customer who chose it |
| Decision shape | One figure committed at a date (a component): the new family's share of the state shortfall, filed at the product meeting on the 20th |
| Committed call | The new hybrid family's contribution to the state's yield shortfall against trend, in bu/acre to one decimal |
| Gap · Pattern | Gap 2 (population) · E11 (every screen is right and the answer sits at a grain no screen expresses: pairs of fields within one grower, the new family against an older hybrid on the same farm, matched on practice and soil), with E19 (a latent attribution marker: field geometry identifies irrigation) at rung 2 and E33 (the population a flag suggests: the seed-order flag against dated replant orders) at rung 3 |
| Gate G mechanism | decomposition_attribution, with confirm_surface_read support |
| Measured traps engaged | #5 takes the population a flag or filter suggests · #11 beats the headline trap, misses the quiet one · #17 guesses an attribution the data can settle |
| Calibration form | Gold-standard verification subsample: 300 fields the agronomy team visited, with the hybrid planted, the practice and any replant verified |
| Driving force | With practice and the planted hybrid both exact, the new family's fields still yield 4.6 bu/acre below older hybrids in the same county and practice. The family launched with a dealer promotion to growers expanding corn after the price rally, much of it onto ground that had not carried corn in years, and those growers' fields yield below their neighbours' whatever the hybrid. Within every county and practice the new family's fields sit disproportionately on their farms, so the shift-share charges the growers' deficit to the hybrid. Only fields compared within one grower, matched on practice and soil, separate the hybrid from the grower who chose it, and they halve its contribution. |

## 1. Situation

A seed company's regional team watched the state's corn yield come in 9 bu/acre below trend in a year of near-normal weather. Sales blames a new
hybrid family that took a large share of orders; the agronomists point to corn acres pushed onto dryland after a price rally. On the 20th product
management decides whether to fund a field-performance review of the new family, which its charter allows only if the family's contribution to the
shortfall is at least 2.0 bu/acre. The company's grower database covers 41% of the state's corn acres, field by field, and its agronomy team
verified a random subsample of 300 fields in person. The family launched with a dealer promotion.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: county yields and trends, the grower database's order flags and yields, the replant orders, field
  boundaries, the promotion's grower list and the verified subsample. Sales is right that the new family's fields yielded less; the agronomists
  are right about the dryland shift. Nothing is overturned; the figure is the size of the component sales names.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices, the head of product's belief and the licensed basis. The clean shift-share still charges the family
  with the expanding growers' deficit, and nothing in the pack compares fields within a grower.
* **Instrument repair.** Suspect files: the order flag, which records the hybrid ordered rather than planted, and the practice field, blank for
  30% of fields. Repaired so that every field carries the hybrid in the ground and its practice, rung 0 returns 3.6 and rungs 1 to 3 all return
  1.2; none returns 0.6. The database's coverage is complete for its growers and weighted to the state by the charter's coverage weights, and
  filled to every field it moves no figure. The answer still needs fields compared within one grower: the family's fields sit disproportionately
  on expanding farms, and no field record, however complete, separates a hybrid from the grower who chose it.
* **Lens swap.** The naive build compares the family's fields with other fields in the same county and practice; the answer compares them with
  other fields of the same grower, a different comparison population that holds the grower fixed.

## 3. The driving force

A strong solver discounts the raw comparison, builds the shift-share against county trends so the dryland shift is booked as mix, fills the
practice field from field geometry (pivot circles and quarter-circles are irrigated), which reproduces every verified practice, and assigns each
field to the hybrid on its latest dated order, so the June flood's late replants, sown with older hybrids under a second order, leave the new
family. Every input is now exact and the subsample confirms each: the new family's planted fields yield 4.6 bu/acre below older hybrids in the
same county and practice, 1.2 bu/acre of the state shortfall. That gap still mixes two causes. The family launched with a dealer promotion aimed
at growers adding corn acres after the price rally, much of it on ground that had not carried corn in years, and those growers' fields yield
5.9 bu/acre below established farms' in the same county and practice whatever the hybrid. The promotion's growers hold 61% of the family's
planted acres against 22% of the older hybrids'. Compared within one grower, the new family against an older hybrid on the same farm matched on
practice and soil index, the family's own gap is 2.3 bu/acre and its contribution to the shortfall 0.6.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Flagged new-family fields' yield gap to other fields, scaled by its acreage share | 4.8 bu/acre (+700%) | Sales' comparison, made exactly on the company's own fields | County trends: the state shortfall is mostly corn moving onto dryland, which this comparison books to the hybrid |
| 1 | Shift-share against county trends by practice, with missing practice filled from each county's dominant practice | 3.1 (+417%) | Mix and within separated, at the grain the state reports | The verified subsample: county defaults mislabel 52 of 300 fields' practice |
| 2 | The same with practice from field geometry (pivot circles and quarter-circles are irrigated) | 2.3 (+283%) | Geometry reproduces all 300 verified practices | The replant orders: 9% of order-flagged fields carry a second, dated order for an older hybrid after the June flood |
| 3 | Fields assigned to the hybrid on the latest dated order before harvest, then the same shift-share | 1.2 (+100%) | Every input is exact, and the subsample confirms the planted hybrid on 300 of 300 fields | The promotion's grower list: 61% of the family's planted acres sit on farms that added corn this year, against 22% of older hybrids' |
| 4 | **Decisive:** the new family against older hybrids within one grower, matched on practice and soil index, the gap scaled by the family's planted acre share | **0.6 bu/acre** | — | — |

* **Figure shape.** Every correction walks the figure down (−35%, −26%, −48%, −50% per step), and the answer is the minimum cell, so every
  partial application overstates the family's contribution; rungs 0 to 2 fund the review the answer declines.
* **Partial correction priced (L3).** A solver who pairs fields within growers but on the order flag keeps the flood's replants on the new
  family's side of each pair and lands at 1.4 (+133%); one who pairs within growers without matching practice sets the expanding growers' new
  dryland ground against their irrigated fields and lands at 1.6 (+167%). Both are further from the answer than rung 3.
* **Grid.** Comparison (raw, county shift-share, within-grower pairs) × practice (county default, geometry) × population (order flag, latest
  dated order) gives ten feasible cells, the raw comparison using no practice, from 4.8 down to 0.6. The nearest wrong cell is 0.8 (+33%), the
  within-grower pairs on county-default practice, one fill away from the answer.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The charter says "fields planted to the family"; the promotion's terms name the growers it targeted. No document says
   those growers' fields yield less, or that a family's effect is read within a grower.
2. **Corpus blind for a computable reason.** *The subsample draws one field per grower, so in every verified case the within-grower contrast is
   zero by construction.* It confirms the planted population and the practice exactly (300 of 300 each) and holds no comparison that separates a
   hybrid from the grower who chose it.
3. **No arithmetic symptom.** Fields, acres and production reconcile to the database totals and to county statistics under every construction;
   the paired fields' acres sum to the paired growers' totals.
4. **Not a row predicate.** Each comparison sets a new-family field against an older-hybrid field of the same grower, matched on practice and
   soil index, so it needs fields grouped by grower and paired within the group.
5. **The enumeration is arithmetic.** No column marks a pair; 2,400 pairs are built from the field records.
6. **No cutover date.** The flood is a dated event and its replants sit at rung 3; the grower mix is set by who took the promotion, not by any
   date.
7. **Survives deletion.** With every voice gone, the replant-corrected shift-share still files 1.2.

## 6. The calibration corpus

* **Form.** The verified subsample: 300 fields drawn at random from the database, one per grower, each visited by an agronomist who recorded the
  hybrid in the ground, the practice and whether the field was replanted, with the field's database record and orders.
* **What it pins.** Practice from geometry (300 of 300 against 248 for county defaults) and the planted hybrid from the latest dated order (300
  of 300 against 273 for the flag and 241 for the combine operator's harvest label).
* **What it is blind to.** The grower contrast (above).
* **Twin pair.** Counties C-14 and C-31 carry identical shift-share inputs for the new family: planted acre share, practice mix, soil index and
  a 4.6 bu/acre gap to older hybrids on planted fields. Their within-grower pair gaps are 1.6 and 3.2 bu/acre (2.0×): in C-14 the promotion's
  growers took 70% of the family's acres, in C-31 established growers took most of them. Only the within-grower pairs separate the counties.
* **Resemblance points at the decoy.** The new family's fields resemble the launch year of the company's previous family, which did carry a real
  deficit, on share, districts and yield gap.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The product charter: a field-performance review is funded when a family's contribution to the state shortfall against
  trend, measured on the fields planted to it, is at least 2.0 bu/acre. County trend yields from the published series. The promotion's terms:
  dealers offered the new family at a discount to growers adding corn acres this season.
* **Empirical pins.** Practice from field geometry and the planted hybrid from the latest dated order, both from the subsample.
* **Voices.** The sales director: "The new family is underperforming everywhere we sold it." The district agronomist: "Corn went onto dryland
  after the price rally; that's your mix effect."
* **Licensed wrong basis.** The charter records that the seed trade association benchmarks hybrids on order-flagged fields and will present
  its comparison at the meeting.

## 8. Determinism by construction

* **Latest order.** A field's planted hybrid is on its latest order dated before 15 July; no order falls between 10 and 20 July.
* **Practice.** Boundaries whose area-to-circumscribed-circle ratio is above 0.75 for a full or quarter circle are irrigated; no field sits
  between 0.6 and 0.75.
* **Pairs.** A pair is a new-family field and an older-hybrid field of the same grower with the same practice and soil indices within five
  points, matched by nearest index, each field in at most one pair. The family's within effect is the acre-weighted mean pair gap, applied to
  all its planted acres; 70% of those acres sit with growers who planted both.
* **Trend.** County trends are the published 15-year fits; the figure is the within effect times the family's planted acre share (26%).
* **Scope.** Database fields only, scaled to state acres by the database's coverage weights, as the charter specifies.
* **Rounding.** One decimal; the answer sits mid-bin, 1.4 below the review line.

## 9. Prompt sketch and deliverables

> The state's corn came in 9 bushels below trend and product management decides on the 20th whether the new hybrid family gets a field-
> performance review. Our head of product is sure the hybrid is the problem. Tell me how many bushels an acre of the shortfall the new family
> accounts for, to one decimal, as the figure I put to the meeting. Send `hybrid_shortfall.xlsx` and a chart `shortfall_bridge.png`.

* `hybrid_shortfall.xlsx` — the five constructions, the district sheet (ask A), the seed-treatment sheet (ask B) and the subsample
  reproduction (ask C).
* `shortfall_bridge.png` — a waterfall from the 9 bu/acre shortfall to the new family's contribution (mix, practice, other within, replant
  reassignment, grower mix), with the 2.0 review line as a reference and an inset of pair gaps by county.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the nine crop reporting districts, harvested acres and production this year and last.
  *Device:* the published county series suppresses small counties and reports them as one combined row per district, as its notes document;
  summing named counties alone understates five districts.
* **Ask B (device-carried).** For each of the four seed-treatment packages, units sold this season. *Device:* orders are taken in bags or in
  80,000-kernel units with a unit field, as the order guide documents; summing quantities across the field overstates the two packages sold
  mostly in bags.
* **Ask C (validity).** For each of the 300 verified fields, the hybrid and practice under each assignment rule; and the figure under each of
  the five rung constructions.
* **Decoupling.** Clearing the within-grower pairs changes no figure in asks A or B.

## 11. Rubric arithmetic

9 districts × 2 years × 2 figures (ask A) + 4 packages (ask B) + 3 assignment rules × 2 accuracy counts + 5 constructions (ask C) + the
committed figure, the promotion growers' acre share, the replanted share and the review decision + 5 named chart parts + 2 files ≈ 60 criteria.

## 12. World-building constraints

* Figures by construction (bu/acre): 4.8, 3.1, 2.3, 1.2, 0.6; other cells 3.6, 1.9, 1.7, 1.4, 0.8; pairs without practice matching 1.6.
* The new family holds 26% of planted acres. Its planted fields yield 4.6 bu/acre below older hybrids in the same county and practice and 2.3
  below them within grower pairs. The promotion's growers hold 61% of its planted acres against 22% of older hybrids', and their fields yield
  5.9 bu/acre below established farms' in the same county and practice whatever the hybrid.
* 30% of fields lack practice; 9% of fields flagged with the new family were replanted with an older hybrid after the June flood, all in three
  districts, at yields 40–55% below trend.
* Subsample: one field per grower; latest-order rule 300/300, flag 273, harvest label 241; geometry 300/300, county default 248.
* C-14 and C-31 identical on every shift-share input for the new family.
* District combined rows and order units touch no field record, order or pair.

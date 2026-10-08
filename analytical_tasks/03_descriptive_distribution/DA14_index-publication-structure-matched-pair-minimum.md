# DA14 — Which categories a grocery price index publishes on their own, when a well-stocked week says nothing about whether two weeks compare like with like

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Economics · retail price statistics and index products |
| Mirrors | Publishing a sub-index or segment metric only where its matched sample holds across the whole window, not just in each period (online inflation trackers and retailer price indices with seasonal assortment rotation, marketplace like-for-like sales by category, A/B dashboards that compare cohorts only when every pair of periods shares a base) |
| Decision shape | A structure the body adopts: which of 18 candidate categories the 2027 index publishes as stand-alone sub-indices, the rest folding into "other food", scored on whether each category's index is reliable in every store format |
| Committed call | The list of categories published on their own |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · E30, a minimum over sub-units where the sub-unit is a pair of weeks within a format, with E18 (format cells against pooled stores) below it, pinned by Pattern B on the field audit |
| Gate G mechanism | method_or_model_selection, with signal_vs_noise_or_hold |
| Measured traps engaged | #14 coarsens the segment it was asked about · #3 stops at a close but inexact match · #12 stops at the first control that passes · #7 uses the ready-made measure |
| Calibration form | Gold-standard verification subsample: the 2025 field audit, 60 category-format cells re-priced by collectors every four weeks, each judged accurate or not against the scanner index |
| Driving force | A GEKS index compares every week with every other week in its window through the items the two share. A category that rotates its assortment (holiday cookies, summer and winter ice cream, seasonal confectionery) has plenty of items every week and almost none in common between July and December. Its index is assembled from a handful of matched items in hundreds of week pairs. The audit's accurate cells are exactly those whose smallest week-pair overlap, within each store format, is at least 12 items. Every per-week count, average or total the register offers is decorrelated from that minimum. |

## 1. Situation

A grocery analytics firm publishes a weekly price index built from store scanner data. Its methodology computes GEKS-Törnqvist indices
within each store format (superstore, neighbourhood, convenience, online) over a 52-week window and aggregates with format expenditure
weights. For 2027 the index committee will publish stand-alone sub-indices only for categories whose 2026 index is reliable in every store
format. The other categories fold into "other food". The pack holds the 2026 scanner movement file (store × item × week, with price,
quantity and sale codes), the item master, the store master with formats, the 2025 field audit and the methodology. The committee adopts
the structure on 9 December.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: scanner prices and quantities, item and store masters, and the audit's field prices and
  judgements. Each category really does have many items on the shelf every week, and nobody's reading of their own numbers is
  overturned. The difficulty is what an index's reliability depends on.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the head of methodology's view and the client panel's licensed basis. The register still shows healthy
  item counts in every format-week for eleven categories, and a per-week threshold still looks like the natural reliability screen.
* **Instrument repair.** Make the scanner feed perfect; it already records every sale. A rotating assortment is what the shops sold, and a
  perfect record of it still leaves January and July with few items in common.
* **Lens swap.** The two reads count different units: format-weeks (each with 20 or more items) against the 1,326 week pairs per format that
  GEKS uses, of which a rotating category leaves hundreds with fewer than 12 items in common.

## 3. The driving force

A strong solver reads the committee's rule ("reliable in every store format") and works within formats, as the methodology does. It
screens each format's index on the obvious reliability measure, the number of items priced each week, and finds most categories with at
least 12 in every week. It may also check that measure against the audit: per-week minima reproduce 49 of 60 judgements, so it stops at a
close but inexact match. But GEKS never compares a week with itself. Its index for week t is a geometric mean of comparisons through every
other week, and each comparison rests on the items the two weeks share. A category whose shelves turn over with the seasons has 30 items
in July and 30 in December and 7 in common. The audit's eleven misses are exactly such categories. Within each format, only the smallest
overlap across all week pairs separates the accurate cells from the inaccurate ones: 12 items or more accurate, 8 or fewer inaccurate, and
nothing in between.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Stores pooled, a category published when it averages 12 or more priced items a week | 15 categories | The firm's long-standing screen on the pooled panel | The committee's rule tests reliability in every store format, and the methodology's elementary cells are formats |
| 1 | Within each format, 12 or more priced items a week on average (E18) | 13 categories | The rule's segment, cleanly applied | The audit: format averages reproduce 41 of 60 judgements, because a format can average well and run thin for weeks |
| 2 | Within each format, 12 or more priced items in every week | 11 categories | A per-period minimum; reproduces 49 of 60 audit judgements | The audit's 11 misses: every one is a category whose weeks share few items, whatever each week holds |
| 3 | **Decisive:** within each format, every pair of weeks in the window sharing 12 or more priced items (the minimum over week pairs) | **8 categories** | — | — |

* **Structure shape.** Each rung adopts a smaller structure, and every earlier list contains the answer: Cereals, Soft drinks, Canned
  soup, Toothpaste, Laundry detergent, Cheese, Crackers and Bath soap. Rung 2's list adds Cookies, Ice cream and Seasonal confectionery,
  whose indices the audit judges inaccurate.
* **Partial correction priced (L3).** A solver who takes the week-pair minimum on pooled stores (skipping formats) passes 10 categories,
  keeping Ice cream and Beer, whose online and convenience cells fail. The half insight adds two wrong categories.
* **Grid.** Cell (pooled or format) × law (average, per-week minimum, week-pair minimum) gives 6 cells and 6 different lists, of 8 to 15
  categories. Only format cells with the week-pair minimum give the eight.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The rule says "reliable in every store format". The methodology defines GEKS. The audit protocol defines accurate
   as within 1% of field prices at every audit point. No document says what makes a GEKS index reliable, or names a week pair.
2. **Reproduction, and why it is a construction.** The week-pair minimum reproduces 60 of 60 audit judgements, the per-week minimum 49,
   the format average 41 and the pooled average 37. Rival laws have flat loss curves: no per-week threshold from 5 to 25 items exceeds 49
   of 60. The reproducing quantity is built by matching item sets across 1,326 week pairs per format. No register column carries it, and it
   is decorrelated from every per-week count (correlation 0.11 across the 60 cells).
3. **No arithmetic symptom.** Every index computes, every bilateral comparison has matched items, expenditure shares sum to one, and no
   week is empty.
4. **Not a row predicate.** The quantity is the minimum over pairs of weeks of the size of an intersection of item sets, a group property
   no row holds.
5. **The enumeration is arithmetic.** 18 categories × 4 formats × 1,326 pairs, computed rather than read.
6. **No cutover date.** Assortments rotate every season of every year, and no series steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, per-week counts are still the first screen anyone runs.

## 6. The calibration corpus

* **Form.** The 2025 field audit: 60 category-format cells drawn at random. In each, collectors re-priced a fixed basket every four weeks
  and the audit compared the field index with the scanner GEKS, judging the cell accurate (within 1% at every audit point) or not.
* **What it pins.** The week-pair minimum, by an absolute split: every audited cell whose smallest week-pair overlap is 12 or more was
  accurate, every cell at 8 or fewer was not, and no cell falls between 9 and 11. Any threshold from 9 to 12 gives the same structure.
* **Twin pair.** Cookies and Crackers in the superstore format are identical on every per-week column: items priced each week (minimum
  31, mean 36), UPC count, expenditure and promotion share. Their audit judgements are opposite, with maximum deviations of 3.1% and 0.6%.
  Cookies' holiday lines leave 7 items shared between July and December, against Crackers' 24. Only the week-pair minimum separates them.
* **Resemblance points at the decoy.** The 2026 Cookies cells most resemble the audited Crackers cell on every per-week statistic.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The methodology: "Elementary indices are GEKS-Törnqvist within each store format over the 52-week window, aggregated
  with format expenditure weights." The committee's rule: "A category is published as a stand-alone sub-index for 2027 only if its 2026
  index is reliable in every store format." The audit protocol defines accuracy against field prices.
* **Empirical pins.** The reliability law and its threshold, from the audit.
* **Voices.** The head of methodology: "Any category with plenty of items on the shelf every week will hold up." The client-services
  lead: "Clients want ice cream and cookies; they're the categories they ask about most."
* **Licensed wrong basis.** The rule records that the client panel judges reliability on the number of items priced each week and will
  comment on the structure.

## 8. Determinism by construction

* **Matched items.** An item is priced in a format-week when it has positive quantity there. Store pooling within a format is fixed by the
  methodology, so the match needs no convention.
* **Window.** The 52 weeks of 2026. Week pairs are unordered, giving 1,326 per format.
* **Threshold.** The audit's empty band from 9 to 11 makes any cut in it file the same eight categories. No 2026 category has a minimum
  between 9 and 11 in any format.
* **Bundle pricing.** Unit value is price divided by bundle quantity. Matching does not depend on price, so the bundle convention cannot
  move the structure.

## 9. Prompt sketch and deliverables

> Which categories should the 2027 grocery index publish as sub-indices of their own, and which fold into "other food"? The committee
> adopts the structure on 9 December, and our head of methodology thinks any category with plenty of items on the shelf every week will
> hold up. Give me the list of stand-alone categories, as the structure the committee adopts, and send `publication_structure.xlsx` with
> the sheets below, plus `matched_pairs_heatmap.png`.

* `publication_structure.xlsx` — the screen for 18 categories × 4 formats, each rung's list with its audit reproduction count (ask C),
  the field-visit sheet (ask A) and the store-change sheet (ask B).
* `matched_pairs_heatmap.png` — for Cookies and Crackers in the superstore format, 52 × 52 heatmaps of items shared between weeks with the
  12-item contour drawn, and a strip of the 18 categories' smallest week-pair overlap by format with the adopted list marked.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Field collectors' planned visits completed in each format in each month from July to December
  2026. *Device:* a visit moved after a store closure is logged as a new visit carrying the original visit's number in its rescheduled-from
  field, as the collection manual documents. Counting both as planned visits understates completion by 4 to 12 points in 19 of 24 cells.
* **Ask B (device-carried).** Stores opened and closed in each format in 2024, 2025 and 2026. *Device:* a store re-bannered to another
  format keeps its store number and gets a new format code with an effective date in the store master. Reading the change as a closure
  and an opening overstates both in 15 of the 24 cells.
* **Ask C (validity).** For each of the 18 categories, the smallest week-pair overlap in each format, and the audit reproduction count of
  each rung's law.
* **Decoupling.** The collection log and the store master's change history share no row with the movement file's item matching. Clearing
  the week-pair minimum changes no figure in asks A or B.

## 11. Rubric arithmetic

4 formats × 6 months (ask A) + 4 formats × 3 years × 2 (ask B) + 18 categories' smallest overlaps and 4 reproduction counts (ask C) + the
18 publication decisions + 4 named chart parts + 2 files ≈ 94 criteria.

## 12. World-building constraints

* Rung lists: 15 / 13 / 11 / 8 categories, each containing the next. Baking mixes, Pet treats and Fresh-cut flowers fail at rung 0;
  Beer and Snack bars at rung 1; Frozen entrées and Yogurt at rung 2; Cookies, Ice cream and Seasonal confectionery at rung 3.
* The audit holds 60 cells. Week-pair minimum 60/60, per-week minimum 49, format average 41, pooled average 37. No cell's week-pair
  minimum falls between 9 and 11.
* Cookies and Crackers (superstore) are identical on every per-week column. Their smallest week-pair overlaps are 7 and 24.
* Per-week counts and week-pair minima correlate at 0.11 across the audit.
* The collection log and the store master's changes touch no movement row.

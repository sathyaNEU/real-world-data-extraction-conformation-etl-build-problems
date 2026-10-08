# FC48 — How many bins to add at this winter's thirty new recycling drop-off points, when the summer curve they borrow must come from points of like demand and the haulage districts only mostly match it

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Demographic & Social Science · seasonal population and household recycling |
| Mirrors | Cold-start capacity for new sites that borrow seasonality from peers, where the operating grouping everyone plans by only mostly matches the population the new site will serve (the containers Waste Management and Republic Services set at new drop-off and commercial sites, and the cash that banks and cash-in-transit firms such as Brink's and Loomis load into new ATMs in resort towns, sized from comparable machines) |
| Decision shape | One figure committed at a date: the July bin order placed with the manufacturer |
| Committed call | Bins to add across the thirty winter-opened drop-off points before July, as a whole number |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · the population a field suggests (measured #5: peers by haulage district, where the standard's "like demand" is set by catchment occupancy through the property register), with finer controls separating constructions (measured #12) at rung 1 |
| Gate G mechanism | forecasting, with method_or_model_selection |
| Measured traps engaged | #5 takes the population a flag or filter suggests · #12 stops at the first control that passes · #14 coarsens the segment it was asked about |
| Calibration form | Published control set: the county's July returns for 2025 and 2026, average weekly fill at every drop-off point, the figures the state recycling grant funds bin additions against |
| Driving force | A new drop-off point borrows its summer rise from mature points of like demand. The dashboard's seasonal indices, and every plan the hauler makes, group points by haulage district, and the district index reproduces the returns district by district. But a point's summer follows who lives around it: where second homes and holiday lets make up most of the dwellings within a kilometre, July fill runs 4.5 times January; where year-round households dominate, 1.4 times. Five of this winter's points sit in the Larchmere holiday-cottage enclave inside the Town district, whose mature points are mostly year-round, and the district index gives them no summer at all. The class is reached only by intersecting each catchment with the county's property register. |

## 1. Situation

A coastal county's recycling service opened thirty unstaffed drop-off points between December and January, each with 15 bins of 1,100
litres: ten along the coast in the Coast haulage district and twenty in the Town district, five of them in the Larchmere holiday-cottage
enclave around the lake. The bin standard gives a point enough bins that its forecast July average weekly fill, in bins, is at most 80% of
its bins, with seasonality borrowed from mature points of like demand. The hauler empties every point on Mondays and logs each bin's fill
and any side waste, in bins. The bin order must be placed with the manufacturer by 15 March. The pack holds two years of emptying records,
the point register with each point's haulage district, the dashboard's seasonal indices by district, the county's property register, the
waste strategy, the sorting plant's load records, the transfer station's bulking table and the county's published July returns for the
last two years.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the emptying records, the point register, the district indices, the property register and the
  returns. No stakeholder's reading of their own numbers is overturned; the district indices really do reproduce the returns district by
  district. The difficulty is which mature points a new point is like, which the haulage district does not say.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the service manager's view and every voice. The dashboard's district indices are still the natural peers, they
  still pass the returns district by district, and they still give the Larchmere points no summer.
* **Instrument repair.** Clean-data test. No file the ladder reads is incomplete, stale or narrower than it claims: the emptying records
  hold every bin's fill and all side waste at every emptying, the returns every point's July fill, the property register every dwelling's
  occupancy (main residence, second home or holiday let), and the haulage district records which depot empties a point, a different
  attribute from demand, so using it as a peer group is an ordinary wrong rung. With nothing to repair, rung 0 returns 90 bins, rung 1 95
  and rung 2 120, and the catchment classing is still needed, because no file records a point's demand class.
* **Lens swap.** The naive read and the answer borrow from different populations: the mature points a depot empties, against the mature
  points whose catchments hold the same mix of year-round and seasonal households.

## 3. The driving force

A strong solver borrows seasonality from mature points, measures each new point's level from its first eight emptyings deseasonalized, and
scales it to July. It finds that a countywide index reproduces last year's cohort total in the returns but misses every district inside
it, so it moves to the dashboard's district indices, which pass the returns district by district. It drops each point's first, four-day
emptying, which the returns do not count. It orders 120 bins. Every step is correct. But the standard borrows from points of like demand,
and the waste strategy classes demand by who lives within a point's one-kilometre catchment: seasonal where second homes and holiday lets
exceed 40% of its dwellings, year-round otherwise. The Town district is mostly year-round points, so its index rises by about 70% from
January to July; the five Larchmere points follow the seasonal curve, which rises four and a half times, and on it each needs 7 more bins.
On the seasonal curve the coast points need 8 each rather than 3, and on the year-round curve the other Town points need 2 rather than 6.
The order is 145.

## 4. The ladder

| Rung | Construction | Lands on (bins) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Level per week over each point's first eight emptyings, deseasonalized and scaled by a countywide index from mature points | 90 (−37.9%) | The standard cold-start method, and it reproduces last year's cohort total in the returns within 3% | The returns' district totals: under the countywide index last year's Coast cohort ran 45% above forecast and its Town cohort 12% below |
| 1 | The dashboard's district indices, each new point scaled by its own haulage district's | 95 (−34.5%) | Passes the returns in total and district by district | The returns' notes: a point's first, partial week is not counted, and every new point opened on a Thursday, so its first Monday emptying covered four days |
| 2 | Hygiene: each point's first, four-day emptying dropped | 120 (−17.2%) | Full weeks, district peers that pass every district control, every fill reconciled to the emptying records | The returns' point rows: inside the Town district, last year's new points whose catchments are mostly second homes and holiday lets ran 2.1 times the district index's forecast, and those mostly year-round 0.9 times |
| 3 | **Decisive:** every mature and new point classed by catchment occupancy through the property register, each new point scaled by its class's index | **145** | — | — |

* **Figure shape.** Every correction walks the order up (90, 95, 120) and the decisive rung is the last step up, so the answer is the
  maximum cell and a solver who stops anywhere short leaves the Larchmere points overflowing by mid-July.
* **Partial correction priced (L3).** A solver who builds seasonal and year-round indices but takes each new point's class from its
  haulage district (Coast seasonal, Town year-round) lands at 110 (−24.1%): the Larchmere points stay on the year-round curve. One who
  classes by catchment but keeps the four-day emptyings lands at 115 (−20.7%).
* **Grid.** Peers (countywide, haulage district, class from the district, class from the catchment) × first emptying (kept, dropped) = 8
  cells: 90, 105; 95, 120; 85, 110; 115, 145. The nearest wrong cells are 120 (−17.2%) and 115 (−20.7%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard says "mature points of like demand"; the waste strategy defines catchment classes for siting new
   points, not for seasonality; no document says the district indices are the wrong peers.
2. **Reproduction (Pattern B).** Catchment-class peers reproduce the July returns of all 24 of last year's new points within 5%; district
   peers 19, every miss a lakeside or harbour-town point; the countywide index 11. The rule is a construction, not a menu: each point's
   one-kilometre catchment intersected with the property register, occupancy shares computed, the class drawn at 40%, and an index built
   for each class from its mature points.
3. **No arithmetic symptom.** Fill reconciles to the emptying records, district indices to the dashboard, the returns to the emptying
   records; every rung's order is internally consistent.
4. **Not a row predicate.** A point's class needs a spatial intersection with tens of thousands of dwellings and an occupancy share before
   any peer group exists, and the order then runs through each class's index.
5. **The enumeration is arithmetic.** No column holds a demand class; it is computed from geometry and occupancy.
6. **No cutover date.** Nothing steps; the Larchmere points were simply opened inside a district drawn for depots.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The county's July returns for 2025 and 2026: average weekly fill, in bins with side waste included, at every drop-off point,
  with last year's 24 new points inside it.
* **What it certifies.** The district indices at district level (they reproduce each district's total) and the full-week rule.
* **What it pins.** The peer rule: only catchment classes reproduce every one of last year's new points.
* **Twin pair.** Reedhaven Road and Ropewalk Street, two of last year's new points in the Town district, opened in the same April week
  with 15 bins each and had identical fill over their first eight weeks. Their July returns were 26 and 13 bins a week (2.0× apart),
  because Reedhaven Road's catchment is 70% second homes and holiday lets and Ropewalk Street's 5%. District, bins and early fill predict
  them equal; only the catchment class reproduces both.
* **Resemblance points at the decoy.** By district, bins and winter fill, the Larchmere points most resemble the quiet Town points of past
  winters, none of which needed bins in July.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The bin standard: a point gets enough bins that its forecast July average weekly fill is at most 80% of its bins, with
  seasonality from mature points of like demand. The returns count full weeks of operation only. Mature points are those open for 24
  months or more. The waste strategy's demand classes.
* **Empirical pins.** The class indices (seasonal January 0.40, July 1.80; year-round 0.80 and 1.10), from mature points' last two years.
  Each point's class, from the property register.
* **Voices.** The recycling service manager: "The coast points barely filled a bin all winter; they won't need anything." The hauler's
  depot manager: "We plan everything by district; the districts are how this service runs." The county's waste planner: "Seasonality is
  seasonality; one index for the county is plenty."
* **Licensed wrong basis.** The standard records that the state recycling grant office reviews bin requests against the dashboard's
  district indices and will check the order on that basis.

## 8. Determinism by construction

* **Class line.** No point's catchment holds between 30% and 50% second homes and holiday lets, so any line in that range classes every
  point the same way.
* **Catchment.** 750-metre, one-kilometre and 1.5-kilometre catchments give the same classes.
* **Indices.** One-year and two-year averages agree within 2%: countywide January 0.72 and July 1.30, Coast district 0.46 and 1.60, Town
  district 0.70 and 1.20.
* **Rounding.** Every point's bins needed sits at least 0.3 from a whole number under every construction (coast 22.6, Larchmere 21.7,
  other Town points 16.5 on the answer).
* **Maturity.** The eight emptyings are closed and every emptying is in the pack.

## 9. Prompt sketch and deliverables

> Thirty recycling drop-off points opened this winter, and the bin order for July goes to the manufacturer by 15 March. Our service
> manager says the coast points barely filled a bin all winter and won't need anything. Tell me how many bins to add across the new
> points, as a whole number, in one sentence for the purchase order, and send `bin_order.xlsx` with the build and the sheets below, a
> chart `new_point_curves.svg`, and a one-page `order_note.html`.

* `bin_order.xlsx` — each new point's level, class, July forecast and bins under each construction, the contamination sheet (ask A) and
  the glass sheet (ask B).
* `new_point_curves.svg` — the countywide, district and class indices by week as lines, the five Larchmere points' winter weeks plotted
  against them, the July forecast against 80% of 15 bins as a reference line, and the bins added labelled for each group of points.
* `order_note.html` — the committed order, the five Larchmere points behind it, and why the district indices understated them.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the thirty new points, the share of its first eight weeks' material rejected for
  contamination at the sorting plant. *Device:* the plant rejects whole truckloads, and a load collected from several points is
  apportioned to them by weighed share in the load-allocation table, as the plant's data guide documents; charging each rejected load to
  the first point on the truck's round overstates contamination at the twelve points that start a round. Rejections enter no part of the
  bin forecast, which counts fill.
* **Ask B (device-carried).** For each of the county's six haulage districts and each month of last quarter, the tonnes of glass sent for
  reprocessing. *Device:* glass the hauler bulks at the transfer station leaves on the reprocessor's ticket under the station's own
  district, with each district's share in the bulking table, as the transfer-station guide documents; reading the reprocessor's tickets
  alone assigns all bulked glass to one district. Glass tonnage enters no part of the bin forecast.
* **Ask C (validity).** The order under each of the four rung constructions, and how many of last year's 24 new points each set of peers
  reproduces within 5%.
* **Decoupling.** Clearing the catchment classing changes no figure in asks A or B.

## 11. Rubric arithmetic

30 new points (ask A) + 6 districts × 3 months (ask B) + 4 constructions × 2 (ask C) + the committed order and the bins per coast,
Larchmere and other Town point + 5 named chart parts + 3 files ≈ 68 criteria.

## 12. World-building constraints

* New points: 10 coast (seasonal), 5 Larchmere points in the Town district (seasonal), 15 other Town points (year-round), 15 bins each.
  Weekly fill per emptying with the four-day first emptying in: coast 3.80, Larchmere 3.65, other Town 9.10 bins; dropping it raises each
  level by 56/53.
* Orders by rung: 90 / 95 / 120 / 145 bins (coast 8 each, Larchmere 7, other Town 2 on the answer). Grid: countywide with the first
  emptying dropped 105; class from the district 85 and 110; catchment class with the first emptying kept 115.
* Returns: last year's 24 new points opened between March and November, 8 in the Coast district (two of them year-round harbour-town
  points) and 16 in the Town district (three of them seasonal lakeside points); under the countywide index the Coast cohort ran 45% above
  forecast and the Town cohort 12% below, netting within 3%. Catchment peers reproduce 24, district peers 19, countywide 11, all within
  5%.
* The twin points are identical on district, bins and first-eight-week fill; July 26 and 13.
* Rejected loads and bulked glass touch no fill, class or bin in the forecast.

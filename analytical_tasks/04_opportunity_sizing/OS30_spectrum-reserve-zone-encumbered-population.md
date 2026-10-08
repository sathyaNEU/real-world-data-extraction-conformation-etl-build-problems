# OS30 — The reserve price for a mid-band spectrum sale, when every comparable sold spectrum that nobody else was using

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · telecommunications asset valuation |
| Mirrors | Valuing an asset from comparables when it carries an encumbrance no comparable ever did (carrier spectrum valuations in bands shared with federal incumbents, real-estate comps for a parcel under an easement, cloud capacity reservations priced against spot when part of the reservation is region-locked) |
| Decision shape | One figure committed at a date: the reserve price written into the board resolution on the 9th |
| Committed call | The market-approach value of the 40 MHz holding, in dollars to the nearest million |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · E03 (the book of closed sales certifies every shallow rung and is blind to encumbrance, because every band ever traded was cleared), with E21 below it (a comparability score saturated at 100% for four auctions, broken by the standard's lowest-consistent rule) |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #19 breaks a big tie instead of questioning it · #12 stops at the first control that passes · #5 takes the population a flag or filter suggests |
| Calibration form | Existing-book actuals: the adviser's book of 14 closed secondary-market spectrum sales (2015–2025), with licence areas, MHz, population and actual price |
| Driving force | The book confirms a constant-dollar 2017-auction price per MHz-pop to within 3% on all 14 sales, because every band ever traded on the secondary market was cleared of federal users first. The holding's band is the first that was not: 22.7% of its population lies inside permanent protection zones around federal radar sites, where the seller has never lit the band. A licence's population is not the population it can serve, and only a spatial join of the zones to census blocks says how much is left. |

## 1. Situation

A regional carrier is selling a 40 MHz mid-band holding across six licence areas, assigned to it in a 2012 administrative licensing round,
never auctioned. Board policy sets the sale's reserve at the holding's market-approach value, rounded to the nearest million. The bank's
valuation manual benchmarks a holding on the most complete comparable auction and breaks ties by recency. The independent valuation
standard the board follows has its own tie rule. The banker's view is that the 2022 auction is today's market.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the auctions' results and closing notices, the licence register, the partition register, the
  federal site list and the book of closed sales. No stakeholder claim about their own numbers is overturned. The difficulty is which
  population the holding can sell to a buyer, which no comparable ever had to answer.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the banker's view and every voice. The book still certifies the 2017 benchmark on licensed MHz-pop 14 of 14,
  and no document says zones reduce value.
* **Instrument repair.** Make every record perfect. The licence populations, zone radii and book prices are already exact. A licence's
  population is still not the population it can serve, and no record of the licence states the second.
* **Lens swap.** The answer prices a different population, the people outside federal protection zones, which is a strict subset of the
  licensed population.

## 3. The driving force

A strong solver weights by MHz-pop, deflates and keeps to mid-band, which defeats the banker's deck before it opens. It then refuses the
manual's recency tie-break, nets out the counties the seller partitioned away in 2019, and back-tests against 14 closed sales: 14 of 14
within 3%. Nothing is left to doubt. But the book is blind to one thing by construction, because every band that has ever traded was
cleared of incumbents before its auction or sale. The holding's band was licensed administratively, with 11 federal radar sites inside its
footprint protected permanently. The seller's site register shows the band lit at 0 of 405 sites inside those radii and at 94% of sites
outside them. The holding's sellable population is the census-block population outside every zone, and getting it needs a spatial join
from the federal site list to blocks to licence areas.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Manual: the most complete mid-band auction, recency tie-break (2022 auction, $1.04 per MHz-pop) × licensed MHz-pop (168.0M) | $174.7M, +96.1% | MHz-pop weighted, constant dollars, the right band class, executed by the bank's own manual | The standard counts a comparable's completeness at the lowest figure consistent with every record. The closing notices cancel three 2022 winners in the holding's region, so only 2017 stays at 100% |
| 1 | The 2017 auction ($0.79) × licensed MHz-pop | $132.7M, +48.9% | The tie is broken by the standard, not the manual | The partition register: 0.55M people in two of licence area L5's counties were partitioned to a rural carrier in 2019 |
| 2 | Hygiene: MHz-pop net of partitions (146.0M) | $115.3M, +29.4% | Reproduces all 14 closed sales within 3% | The federal site list puts 0.83M of the held population inside permanent protection radii, where the band is lit at no site |
| 3 | **Decisive:** $0.79 × MHz-pop outside every protection zone (40 MHz × 2.82M) | **$89.1M, reserve $89M** | — | — |

* **Figure shape.** Every correction walks the value down (−24.0%, −13.1%, −22.7%), and the answer is the minimum cell of the grid.
* **Partial correction priced (L3).** A solver who writes off every licence area a zone touches lands at $42M (−52.8%), further from the
  answer than rung 2. A solver who halves the zone population on the view that protection may lift has no shipped basis (the site list
  marks every zone permanent) and lands at $102M (+14.7%).
* **Grid.** Benchmark (2022, 2017) × partitions (ignored, netted) × zones (ignored, removed) = 8 cells. The nearest wrong cell is zones
  removed with partitions ignored, $106.5M (+19.5%). Reaching it means pricing people the seller no longer holds a licence to serve. With
  the 2022 benchmark and both corrections the value is $117.3M (+31.6%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The federal site list carries sites, coordinates and protection radii. No document says what protection means for
   deployment or value, and the licence register lists each area's full population.
2. **Corpus blind for a computable reason.** *In every one of the 14 closed sales the zone population is zero, because every band sold so
   far was cleared of federal users before its auction.* The zone-netted method and the rung-2 method reproduce the book identically, 14
   of 14.
3. **No arithmetic symptom.** Licence populations sum to the census, MHz-pop ties to the licence register, and the book reconciles on every
   rung.
4. **Not a row predicate.** The deployable population is a spatial construction: protection radii around another entity's sites,
   intersected with census blocks, rolled up to licence areas net of partitions.
5. **The enumeration is arithmetic.** No column holds deployable population, and no licence carries a zone flag.
6. **No cutover date.** The zones are as old as the licences; nothing steps in any series.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The adviser's book of 14 closed secondary-market sales, 2015–2025: licence areas, MHz, population, partitions and actual price.
* **What it certifies.** The 2017 benchmark in constant dollars and the partition netting. The 2022 benchmark reproduces 0 of 14 (each
  sale overstated by 25–35%). The 2017 benchmark on licensed MHz-pop reproduces 10 of 14, missing the four partitioned sales by 12–25%,
  all on the high side. Net of partitions it reproduces 14 of 14.
* **What it is blind to.** Encumbrance (above).
* **The absolute split (O2).** In the seller's site register the band is lit at 0 of 405 sites inside a protection radius and 94% of the
  1,380 outside, with no site in between.
* **Twin pair.** Licence areas L3 and L6 are identical on population (0.62M each), MHz, region class and licensing history. L6 has 46% of
  its population inside one zone and L3 none, so their deployable values differ 1.85×. No licensed-MHz-pop rule separates them.
* **Resemblance points at the decoy.** The holding matches closed sale 9 on MHz, population class and region, and sale 9 closed exactly at
  the rung-2 basis.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** Board policy sets the reserve at the market-approach value, to the nearest $1M. The valuation standard prices spectrum
  per MHz-pop in constant dollars at the valuation quarter, counts a comparable's completeness at the lowest figure consistent with every
  record of its auction, and fixes population to the latest census.
* **Empirical pins.** Encumbered population is worth nothing to a buyer, per the site register's 0-of-405 split. The 2017 benchmark comes
  from the book.
* **Voices.** The banker: "The 2022 auction is the market today; nothing older is relevant." The CFO: "Spectrum is spectrum, and the market
  pays per MHz-pop."
* **Licensed wrong basis.** The standard records that the buyer's adviser values spectrum on licensed MHz-pop at the most recent auction's
  price and will present that at the negotiation.

## 8. Determinism by construction

* **Zone geometry.** Census-block centroids and area-weighted overlap give the same zone population to within 0.4%, and no block straddles
  a radius in a way that changes the rounded reserve.
* **Unit convergence.** The seller's sites inside zones are 22.7% of its sites in the footprint, equal to the population share, so a
  site-based or population-based discount returns the same deployable fraction.
* **Deflator.** Pinned by the standard to the valuation quarter, and applied identically to every auction and sale.
* **Defaults.** Each closing notice lists cancelled licences by area. No cancelled area was later regranted inside the 2017 auction.
* **Rounding.** The answer, $89.11M, sits 0.39M from the nearest rounding boundary.

## 9. Prompt sketch and deliverables

> The board sets the reserve for our mid-band sale on the 9th, and our banker is certain the 2022 auction is today's market. Give me the
> reserve as one number in dollars, to the nearest million, that I can put in the resolution. Send `reserve_build.xlsx`, a chart
> `value_bridge.png`, and a one-page `board_paper.pdf`.

* `reserve_build.xlsx`: the six licence areas' licensed, partitioned, zone and deployable population, the value build, the sublease sheet
  (ask A) and the traffic sheet (ask B).
* `value_bridge.png`: a waterfall from the 2022-benchmark value to the reserve with one bar per correction, each bar labelled with its
  dollar move, and the book's back-test count printed above each stage.
* `board_paper.pdf`: the committed reserve, the deployable population behind it, and the basis the buyer's adviser will bring.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the three subleases the seller grants on parts of the holding, the lease income in
  each of the last four years. *Device:* amendments re-issue a lease row under the same lease number with a higher amendment number, and
  the latest amendment governs from its effective date, per the lease register guide. Summing every row double-counts two years of one
  lease, and taking only the latest row back-dates a rent change.
* **Ask B (device-carried).** For each licence area, last quarter's traffic carried on the band and its share of all the seller's traffic
  there. *Device:* when a cell is re-parented to a new site its counters restart under the new site number, and the network inventory
  links old and new. Summing by site double-counts the quarter's re-parented cells in four areas.
* **Ask C (validity).** The value under each of the four rung bases, and the book's back-test count under each (0, 10, 14 and 14 of 14).
* **Decoupling.** Clearing the zone construction changes no figure in asks A or B.

## 11. Rubric arithmetic

3 leases × 4 years (ask A) + 6 areas × 2 (ask B) + 4 values + 4 back-test counts (ask C) + the committed reserve, deployable MHz-pop, zone
population and partitioned population + 5 named chart parts + 3 files ≈ 44 criteria.

## 12. World-building constraints

* Holding: 40 MHz, licensed population 4.20M, partitioned 0.55M (all in L5), zone population 0.83M (L2 0.21M, L4 0.17M, L5 0.165M, L6
  0.285M). Net areas: L1 0.71M, L2 0.48M, L3 0.62M, L4 0.55M, L5 0.67M, L6 0.62M.
* Constant-dollar benchmarks: 2022 auction $1.04, 2017 $0.79 per MHz-pop. Round-result completeness is 100% for the 2014, 2017, 2020 and
  2022 auctions. After closing-notice cancellations it is 0.93, 1.00, 0.97 and 0.88.
* Rung figures are $174.7M / $132.7M / $115.3M / $89.1M, and no other grid cell is within 19% of the answer.
* Every closed sale has zero zone population. Four have partitions. L3 and L6 are identical on every licence-register column.
* Lease amendments and re-parented cells never touch populations, zones, benchmarks or the book.

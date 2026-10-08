# DA37 — How many truck ton-miles a new grain transload terminal takes off the roads, when only unit-train lanes ever move to rail

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Supply Chain & Logistics · freight mode-shift planning |
| Mirrors | Sizing what a new channel captures when only a fine segment of the coarse category converts (sellers large enough for a fulfilment programme, accounts big enough for a dedicated tier, cloud workloads steady enough for reserved capacity) |
| Decision shape | One figure committed at a date: the net reduction stated in the federal rail-shift grant application, due 15 May |
| Committed call | Net truck ton-miles a year the Ashgrove transload terminal removes from the state's roads, in millions to the nearest 10 |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · the segment kept at its fine grain (measured #14), pinned by the terminal book, with the deciding net comparison at rung 2 |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #14 coarsens the segment it was asked about · #20 leaves the deciding comparison unstated · #13 validates on one population, applies to another |
| Calibration form | Existing-book actuals: six existing transload terminals, each with its catchment's pre-opening truck flows and the tons it actually shifted to rail in its first three years |
| Driving force | The programme targets "bulk farm movements", and the convenience table is farm products as a whole. Only the flows a shipper sends down one lane at unit-train scale ever shift: establishment-lane tonnage is either under 40,000 tons a year or over 150,000, and every existing terminal shifted 62% of the large flows and none of the rest. Aggregating the survey's shipments by establishment and lane is a construction nothing invites, and the pooled rate the book gives on the coarse group fits no terminal. |

## 1. Situation

A state freight office is applying for a federal grant to build a grain transload terminal at Ashgrove, and the application must state the
net truck ton-miles a year the terminal removes from the state's roads. The pack holds the freight survey's shipment microdata with weights
and masked establishment IDs, the survey's published tables, the programme notice and scoring guide, the terminal catchment definition,
county geography, and the book of six existing transload terminals in neighbouring states.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each sampled shipment and weight, each published table, each terminal's actual tons. No stakeholder
  computes the reduction and nothing reported is overturned. The difficulty is which flows a terminal can ever take.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the co-op's view and the commission's basis. The weighted, net, coarse-group build still files 760 million and
  reconciles with every published table.
* **Instrument repair.** Suspect: the survey microdata, a weighted sample with masked establishment IDs. Repaired to a census of every
  shipment with real IDs, rung 0 returns rung 1's 880M, rung 1 stays 880M and rung 2 760M. Establishment-lane flows at unit-train scale
  are a unit no row claims to record, so the answer stays 1,010M and still has to be built.
* **Lens swap.** The naive base is every long-haul farm-product truck flow; the answer's base is the establishment-lane flows at
  unit-train scale, a different set of shipments carrying a different rate.

## 3. The driving force

A strong solver weights the microdata, takes farm-product truck flows over 500 miles from the catchment, applies the terminal book's rate,
and subtracts the truck drayage the transload adds, as the scoring guide's net basis requires. That files 760 million ton-miles. But no
single rate on the coarse group fits the book: the six terminals shifted 11% to 38% of it. Shift happens shipper by shipper and lane by
lane. A grain shipper sending more than 150,000 tons a year down one lane can fill unit trains and moves to rail; one sending less than
40,000 never does, and no establishment-lane sits between. On those large flows every terminal shifted 62%. Ashgrove's catchment holds
1.8 billion such ton-miles, so the net reduction is 1,010 million.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Unweighted sample: farm-product truck ton-miles over 500 miles × the book's pooled rate (21%) | 1,300M, +29% | Every sampled long-haul farm truck counted at the observed rate | The survey guide: estimates use the shipment weights |
| 1 | Survey-weighted base × the pooled rate, gross | 880M, −13% | Correctly weighted and tied to the published tables | The scoring guide: the programme scores truck ton-miles removed net of the drayage the terminal adds |
| 2 | Weighted, coarse group, net of drayage to the terminal | 760M, −25% | The full net comparison on the official base | The terminal book: the pooled rate fits none of the six terminals (11% to 38%) |
| 3 | **Decisive:** establishment-lane flows at unit-train scale × 62%, net of their drayage | **1,010M** | — | — |

* **Figure shape.** Rungs 0 to 2 walk the figure down (−32%, then −14%), and the decisive move reverses them (+33%).
* **Partial correction priced (L3).** A solver who narrows to bulk commodity codes without aggregating by establishment and lane fits its
  own pooled rate (33%) to a 2.9-billion base and lands at 880M (−13%), back on rung 1's figure.
* **Grid.** Weights (off or on) × net (off or on) × segment (coarse group, bulk codes, unit-train lanes) = 12 cells. The nearest wrong
  cell is unit-train lanes gross of drayage, 1,120M (+10.9%), which needs the decisive construction with the scoring guide's net basis
  ignored; every cell missing the segment construction is at least 13% away.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The notice says the grant targets "bulk farm movements" and defines them as "farm products moving in volumes rail
   service can carry". No document names a tonnage, a lane or an establishment grain.
2. **Pattern B, a constant only one segment holds.** At unit-train scale, one rate (62%) reproduces all six terminals' shifted tons
   within 1%. On the coarse group the best constant misses four terminals by 30% or more, and on bulk codes it misses three. The segment
   is a construction: weighted shipments grouped by establishment and origin-destination lane, then the hole in annual tonnage.
3. **No arithmetic symptom.** Weighted totals tie to every published table, drayage ties to county distances, and the book's tons tie to
   its rail waybills.
4. **Not a row predicate.** Whether a shipment is in the segment depends on the annual weighted tonnage of every shipment its establishment
   sends on that lane.
5. **The enumeration is arithmetic.** No column flags a unit-train flow, and the published tables stop at commodity group.
6. **No cutover date.** Terminals opened in different years and the book is read terminal by terminal.
7. **Survives deletion.** With every voice removed, the coarse net build still files 760M.

## 6. The calibration corpus

* **Form.** The terminal book: six transloads opened between 2014 and 2020, each with its catchment's survey flows before opening and its
  rail tons in the first three years.
* **What it certifies.** That drayage must be netted and that shift is far from total, which the coarse build already honours.
* **The absolute split (O2).** Establishment-lane flows are under 40,000 or over 150,000 tons a year in every catchment, so any cut in the
  gap selects the same flows.
* **Twin pair.** Terminals Brockfield and Tamarack match on catchment farm-product ton-miles, distance mix and commodity mix. They shifted
  1.24 and 0.62 million tons (2.0×): two-thirds of Brockfield's flows run from three large elevators down single lanes, while Tamarack's
  spread across small shippers.
* **Resemblance points at the decoy.** On every published-table column, Ashgrove resembles Tamarack, the low shifter.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The scoring guide: the reduction is truck ton-miles removed per year, net of truck movements the project adds. The
  application guide: the catchment is every county within 75 miles of the terminal, and drayage is measured from the origin county's
  centroid.
* **Empirical pins.** The segment and its rate, from the terminal book.
* **Voices.** The grain co-op's director: "Every farm truck running past 500 miles is a rail candidate." The freight planner: "The
  published commodity tables are the standard base for any grant."
* **Licensed wrong basis.** The scoring guide records that the state transportation commission sizes rail projects on the published
  commodity-group tables and will review the application on that basis.

## 8. Determinism by construction

* **Distance.** Routed distance as the survey files it; no catchment flow sits within 25 miles of the 500-mile line.
* **Lanes.** A lane is an origin-destination pair of survey areas; establishment IDs are stable across the survey year.
* **Rate.** 62% reproduces each terminal within 1%; three-year means and final-year shares give the same rate.
* **Rounding.** The answer sits mid-bin at 1,010M.

## 9. Prompt sketch and deliverables

> The rail-shift application closes on 15 May and has to say how many truck ton-miles a year Ashgrove takes off the state's roads. The
> grain co-op is sure every long-haul farm truck is a rail candidate. Give me the figure in millions of ton-miles to the nearest 10, as
> the sentence for the application, with `ashgrove_reduction.xlsx`, a chart `lane_scale.png`, and a one-page `application_note.pdf`.

* `ashgrove_reduction.xlsx` — the reduction build, the elevator sheet (ask A), the haul-rate sheet (ask B) and the book table (ask C).
* `lane_scale.png` — establishment-lane flows by annual tonnage on a log axis for Ashgrove and the six terminals, with the empty band
  between 40,000 and 150,000 tons shaded, each terminal's shifted share annotated, and the twin terminals paired.
* `application_note.pdf` — the committed figure and the bases a reviewer will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 12 catchment counties, the number of grain elevators and their licensed storage.
  *Device:* the licence register lists licences, and one elevator complex can hold several under a shared site ID, as its note
  explains; counting licences overstates elevators in five counties. The reduction build never reads the register.
* **Ask B (device-carried).** The average spot truck rate per mile for grain hauls in each of the last 12 months. *Device:* the market
  report switched from loaded miles to total miles in month 7, as its methodology note states; a naive series shows a false 30% drop.
* **Ask C (validity).** The figure under each of the four rungs, and each terminal's predicted and actual shifted tons on the coarse and
  the unit-train segments.
* **Decoupling.** Clearing the segment construction changes no figure in asks A or B.

## 11. Rubric arithmetic

12 counties × 2 (ask A) + 12 months (ask B) + 4 rungs and 6 × 2 terminal predictions (ask C) + the committed figure, the eligible base and
the rate + 5 named chart parts + 3 files ≈ 63 criteria.

## 12. World-building constraints

* Ashgrove: coarse weighted base 4.2 billion ton-miles (6.2 unweighted), unit-train base 1.8 billion; drayage 120M coarse, 106M unit-train.
  Rungs 1,300 / 880 / 760 / 1,010.
* Book: unit-train shift 62% at every terminal; coarse shares 11% to 38%; establishment-lane flows never between 40,000 and 150,000 tons.
* Brockfield and Tamarack match on every published-table column.
* Elevator licences and rate quotations never touch a survey shipment.

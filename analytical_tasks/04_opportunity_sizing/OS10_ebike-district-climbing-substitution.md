# OS10 — Which district gets the next 600 e-bikes, when the pilot's cannibalisation rate was measured on flat streets and the best district is a hill

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Product Analytics · shared-mobility product launches |
| Mirrors | Rolling a product variant out to the market where its pilot's adoption and cannibalisation were measured on a different mix (Lime and Uber e-bike expansions, Google and Apple feature launches validated in one city's usage pattern, Amazon benefit expansions whose cannibalisation of the existing tier was measured on a different customer mix) |
| Decision shape | Which of N gets one scarce thing, with the sizing kept as the graded figure: 600 new e-bikes, five candidate districts |
| Committed call | The district that receives the e-bikes, and the net fare revenue a year they add, to the nearest $10k |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · validated on one population, applied to another (#13), with a suppressed rider count bounded from published totals (#24) below it |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #13 validates on one population, applies to another · #24 treats an unpublished figure as unknown · #6 treats a mixed segment all one way |
| Calibration form | Parallel-run overlap: twelve months in which 24 pilot docks offered e-bikes alongside classic bikes while 12 matched docks stayed classic-only, every trip logged |
| Driving force | An e-bike trip earns its fare less the classic fare it displaces, and what it displaces depends on the climb. On flat trips 0.92 classic trips are lost per e-bike trip; on trips that climb, none, because nobody pedals those hills on a classic bike. The pilot's pooled 0.75 fits every pilot day exactly, because the pilot docks' climbing share never changed. Hillcrest's trips are 80% climbing, a fact reached only by joining each trip's docks to the station elevation file. |

## 1. Situation

A city bike-share operator has 600 new e-bikes for one of five districts: Central, University, Riverside, Old Town and Hillcrest. Its
pilot ran e-bikes at 24 waterfront docks for twelve months while 12 matched docks stayed classic-only, and every trip at both was
logged. E-bikes cost $1 plus $0.25 a minute and classic bikes $1 plus $0.10 a minute. The operator's open-data portal publishes trips by
district, month and rider type, suppressing any cell under 10,000 trips. The station file gives every dock's elevation. The board judges
a deployment on the net fare revenue it adds a year. The operations director wants the e-bikes where the riders are.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the published trip tables, the pilot's uptake, its pooled displacement rate, the fares and the
  elevations. The pooled rate is right for the pilot. No stakeholder read is overturned. The difficulty is that the rate belongs to the
  pilot's mix of trips, and the districts carry a different one.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the director's view. The pilot's rates still fit every pilot day, transport cleanly in arithmetic, and name
  Riverside.
* **Instrument repair.** Log every trip with GPS and run the pilot twice as long. The pooled rate stays exact for the pilot, and the
  districts still differ in how many trips climb.
* **Lens swap.** The naive read applies the pilot docks' trips to every district. The answer weights each district's own trips by their
  climb, a different population.

## 3. The driving force

A strong solver drops gross fares at once: the parallel run shows e-bike trips displacing classic ones, 0.75 per e-bike trip across the
pilot. It splits uptake by rider type, members 6% and casual riders 30%. When it finds University's casual counts suppressed, it bounds
them from the published district totals less members: 108,000 a year, not the 40% citywide share. Everything reconciles, every pilot day
reproduces, and Riverside wins. But displacement is not a constant of the e-bike. On flat trips almost every e-bike ride replaces a
classic one; on a climb it replaces nothing. The pilot's waterfront docks climbed on 18% of trips every day of the year, so no daily check
could see the split. Hillcrest climbs on 80%. Its e-bikes earn mostly new fares, and it moves from third to first.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | District trips × the pilot's 14.4% uptake × the pilot's average e-bike fare ($3.50) | A, Central ($5.54M) | The pilot's own numbers on the published trip totals | The parallel run: each e-bike trip displaced 0.75 classic trips, and uptake was 6% for members against 30% for casual riders |
| 1 | Uptake by rider type, net of 0.75 displacement at each district's fares; University's suppressed casual cells filled at the citywide 40% | B, University ($3.04M, 1.65× over C) | Rider mix and displacement handled; the gap in the table filled with the published citywide share | The published district-month totals less members: University's casual trips are 108,000 a year (1.2%) |
| 2 | The same with University's casual trips recovered from the totals | C, Riverside ($1.85M, 1.25× over D) | Every cell exact, every pilot day reproduced | The station elevation file: joined to the pilot's trips, displacement is 0.92 on flat trips and 0 on climbing trips; Hillcrest climbs on 80% |
| 3 | **Decisive:** displacement by climb (flat 0.92, climbing 0), applied to each district's climbing share from its own trips joined to dock elevations | **E, Hillcrest** (5th of 5 on rung 0), **$2.21M a year** | — | — |

* **Position table.** Hillcrest ranks 5th on rung 0, 4th on rung 1 and 3rd on rung 2, and leads only rung 3 (1.36× over Riverside).
* **Discriminator dominance.** Riverside carries a 1.27× advantage into rung 3 ($1.85M against $1.45M). Calibrating by climb multiplies
  Hillcrest's revenue by 1.52 and Riverside's by 0.88, an edge of 1.73×, above the 1.53× floor. Product: 1.73 / 1.27 = 1.36.
* **Partial correction priced (L3).** A solver who calibrates displacement by climb but keeps University's suppressed cells at the citywide
  share names University ($2.72M against $2.21M). One who calibrates by climb but drops the rider-type uptake names Hillcrest at $3.09M
  (+39.5%), the right district at a figure the pilot's own uptake refutes.
* **Grid.** Uptake (pooled, by rider type) × University's casual trips (filled, recovered) × displacement (pooled, by climb) gives 6
  distinct cells, each with a leader at least 1.19× clear. Only the answer cell names Hillcrest at $2.21M. The nearest wrong figure for
  Hillcrest is $2.03M (−8.3%), in a cell that names University.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The pilot report gives one displacement rate. No document says displacement depends on the climb.
2. **Corpus blind for a computable reason.** *On every pilot day the climbing share of the pilot docks' trips was 18%, because the pilot
   ran at the same 24 waterfront docks all year.* The pooled rate reproduces every day's displaced classic trips exactly, and only a split
   of trips by climb, through dock elevations, shows two rates.
3. **No arithmetic symptom.** Pilot trips reconcile to the parallel-run totals, district cells sum to published totals, and every rung's
   revenue reconciles to its trips.
4. **Not a row predicate.** Each trip's climb comes from its two docks' elevations, displacement by climb from the pilot's treated and
   control docks compared within each band, and each district's climbing share from its own trip file.
5. **The enumeration is arithmetic.** No column marks a trip as climbing; the climb is computed for 39 million trips.
6. **No cutover date.** The pilot ran a full year at constant docks, and no series steps.
7. **Survives deletion.** Removing the director's view leaves the pilot certifying the pooled rate.

## 6. The calibration corpus

* **Form.** The parallel run: twelve months of trips at 24 e-bike docks and 12 matched classic-only docks, with the dock elevations.
* **What it certifies.** Uptake by rider type (6% members, 30% casual) and the pooled displacement of 0.75, which reproduces all 365 days
  within 1%.
* **What it pins only through the join.** Displacement of 0.92 on flat trips and 0 on climbing trips. The by-climb rates reproduce all 24
  docks; the pooled rate reproduces 9.
* **Twin pair.** Pilot docks Quay 7 and Quay 19 are identical on size, daily trips, rider mix and e-bike uptake. Quay 7's departures are
  all flat and displace 0.92 classic trips per e-bike trip; half of Quay 19's climb to the old town and it displaces 0.46, 2.0× fewer. Only
  the elevation join separates them.
* **Resemblance points at the decoy.** By rider mix and trip length, Riverside's trips most resemble the pilot docks', the population
  the pooled rate was fitted on.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The board's rule: a deployment is judged on the net fare revenue it adds a year, e-bike fares less the classic fares
  they displace. The fare schedule ($1 plus $0.25 a minute e-bike, $1 plus $0.10 classic). The portal's note: cells under 10,000 trips are
  suppressed. The planning convention: next year's trips are this year's published district totals.
* **Empirical pins.** Uptake and displacement, from the parallel run. Climbing shares, from each district's trips and dock elevations.
* **Voices.** The operations director: "Central has the riders. Put the bikes where the riders are." The marketing lead: "Students
  will take to e-bikes faster than anyone."
* **Licensed wrong basis.** The board pack records that the city's transport committee compares districts on gross e-bike fares at the
  pilot's uptake and will present that comparison.

## 8. Determinism by construction

* **Climb.** A trip climbs if its destination dock sits at least 20 m above its origin. No trip in any district or in the pilot climbs
  between 12 m and 28 m, so a threshold anywhere in that band gives the same split.
* **Fares.** District mean trip lengths are published (Central 7, University 11, Riverside 12, Old Town 12, Hillcrest 13 minutes), and
  per-minute fares are linear, so means and trip-by-trip sums agree.
* **Suppression.** Members are published in every cell, and each suppressed casual cell is fixed exactly by the district-month total.
* **Uptake.** Uptake does not vary by climb in the pilot (14.4% on flat and climbing trips alike), so only displacement needs splitting.
* **Rounding.** Hillcrest's figure is $2,212,000, mid-bin at the nearest $10k.

## 9. Prompt sketch and deliverables

> We have 600 new e-bikes and they go to one district. Our operations director wants them where the riders are. Tell me which district
> gets them and how much net fare revenue a year they will add, to the nearest $10k, as a line for the board pack. Send me
> `ebike_district_case.xlsx`, a chart `displacement_by_climb.png`, and a one-page `fleet_decision.pdf`.

* `ebike_district_case.xlsx` — the five districts on four bases, the climbing-share build, the dock sheet (ask A) and the pass sheet
  (ask B).
* `displacement_by_climb.png` — a script-rendered two-panel chart: left, displaced classic trips per e-bike trip at each pilot dock against
  its climbing share, with the flat and climbing rates as reference lines and Quay 7 and Quay 19 labelled; right, each district's
  climbing share with its net revenue per e-bike trip, the pilot's 18% marked.
* `fleet_decision.pdf` — the committed district, the revenue figure, and why the other four fall away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each district, the share of weekday peak minutes last quarter in which docks stood empty and
  the share in which they stood full. *Device:* the station status feed repeats the last reading during a communication outage and flags
  it `stale`, as the feed specification documents. Counting stale rows misstates availability in the two districts with radio dead zones.
* **Ask B (device-carried).** For each district, annual-pass renewals as a share of passes expiring in the last twelve months. *Device:* a
  pass renewed within 30 days of lapsing keeps the member number but gets a new pass number, and the membership guide counts it as a
  renewal. Matching on pass number counts those members as churned and halves University's renewal rate.
* **Ask C (validity).** Each district's net revenue under each of the four rung bases, and pilot docks reproduced (of 24) by pooled and
  by-climb displacement.
* **Decoupling.** Setting displacement back to the pooled rate changes no figure in asks A or B. The status feed and the pass ledger
  touch neither trips nor elevations.

## 11. Rubric arithmetic

5 districts × 2 (ask A) + 5 × 2 (ask B) + 5 districts × 4 bases and 2 dock counts (ask C) + the committed district, its revenue, the
runner-up and the margin + 5 named chart parts + 3 files ≈ 54 criteria.

## 12. World-building constraints

* Annual trips (M): Central 11.0, University 9.0, Riverside 7.0, Old Town 6.4, Hillcrest 5.6. Casual shares 3%, 1.2%, 22%, 16%, 18%.
  Climbing shares 4%, 6%, 4%, 12%, 80%. Pilot: 35% casual, 18% climbing.
* Uptake 6% members and 30% casual on every trip; displacement 0.92 flat and 0 climbing; pooled 0.75.
* Rung leaders A, B, C, E at 1.22×, 1.65×, 1.25×, 1.36×; Hillcrest 5th, 4th, 3rd, 1st.
* University's casual cells are under 10,000 in every month; the citywide casual share is 40% because of the waterfront pilot district.
* Quay 7 and Quay 19 match on every dock column outside their trips' elevations.
* Status-feed rows and pass records never touch trips, elevations or the parallel run.

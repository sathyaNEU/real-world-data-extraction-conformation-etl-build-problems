# OS11 — Which corridor gets the next express-lane conversion, when the busiest corridor's toll would have to pass the legal maximum and its peak hours go free

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · transport pricing |
| Mirrors | Pricing capacity whose price is set by the demand it induces under a cap (surge pricing at Uber and Lyft with emergency caps, cloud spot capacity with price ceilings, Google Ads reserve prices), where a one-pass projection at today's prices misses the hours the cap forces the product off the market |
| Decision shape | Which of N gets one scarce thing, with the sizing kept as the graded figure: one express-lane conversion, five candidate corridors |
| Committed call | The corridor converted next, and its annual toll revenue, to the nearest $0.1M |
| Gap · Pattern | Gap 3 (objective) over Gap 1 (time) · S5 (a ceiling that binds only after the fixed-point solve, #22), with a uniformly labelled commercial segment split through the vehicle registry (#6) below it |
| Gate G mechanism | binding_constraint, with method_or_model_selection |
| Measured traps engaged | #22 solves a self-referencing rule in one pass · #6 treats a mixed segment all one way · #19 breaks a big tie instead of questioning it |
| Calibration form | Change-log natural experiments: the nine logged toll-table changes on the authority's four existing express lanes, with hourly volumes before and after |
| Driving force | An express-lane toll is set by the demand it creates: it rises until the vehicles that choose the lane fit its capacity of 1,600 an hour. That steady-state toll is a fixed point, and where it would pass the $14 legal maximum the hour is degraded and runs HOV-only, earning nothing. A one-pass projection at today's volumes never meets the ceiling. Solved hour by hour with the change log's elasticity, Lakeshore's peak needs $14.80 and goes free, and Western, identical to Ridge Road on averages, loses its two concentrated peak hours. |

## 1. Situation

A regional transport authority will convert one lane of one corridor to a priced express lane next year. The five candidates are Port
Way, Northern, Lakeshore, Western and Ridge Road. Its feasibility study projected revenue from an indicative toll table by corridor
volume and a 25% diversion share. The detector file gives each corridor's counted volumes by hour and vehicle class, with commercial
vehicles in one class. The statute caps the toll at $14 and bars vehicles over 26,000 lb from express lanes; lighter commercial vehicles
pay the car toll. The authority already runs four express lanes, and every change to their toll tables is logged. The board judges a
conversion on its annual toll revenue.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the counts, the registry, the indicative table, the logged volumes and the statute. The
  feasibility study's table is right for the question it answers. No stakeholder read is overturned. The difficulty is that a toll set
  by its own demand has to be solved, and the ceiling binds only in the solution.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the feasibility study and every voice. Counts, the registry split and the logged elasticity still project
  Lakeshore first in one pass.
* **Instrument repair.** Count every vehicle perfectly and log every toll change for a decade. The elasticity sharpens, and Lakeshore's
  steady-state peak toll is still above $14.
* **Lens swap.** The naive read prices today's traffic. The answer prices the traffic that the steady-state toll leaves in the lane,
  hour by hour, a different population at a different moment.

## 3. The driving force

A strong solver drops the feasibility study's diversion share, removes the heavy trucks the statute bars (reached by joining counted
plates to the vehicle registry, because the counts lump all commercial vehicles together), and applies the change log's elasticity: each
extra dollar cuts lane volume by 8%. Applied once to the indicative toll at today's volumes, Lakeshore leads. But the toll is not an
input. It adjusts against lane volume until the vehicles that pay fit the lane. In Lakeshore's peak hours that price is $14.80. The statute
stops the toll at $14, demand stays above capacity, the hour is degraded, and the corridor agreement runs degraded hours HOV-only. Lakeshore
keeps only its shoulders. Western looks identical to Ridge Road on average volumes, but two of its peak hours carry half its peak traffic
and cross the ceiling. Ridge Road's peak never does.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Counted volume × 25% diversion × the indicative toll | A, Port Way ($46.8M) | The feasibility study's method on the authority's own counts | The registry joined to the counts: 60% of Port Way's vehicles are over 26,000 lb and barred from the lane |
| 1 | The same on eligible traffic (heavy trucks out, vans in) | B, Northern ($36.8M, 1.35× over C) | The statute applied record by record | The change log: lane volume falls 8% for each extra dollar of toll, 9 of 9 logged changes |
| 2 | Indicative toll at today's eligible volume, then the logged elasticity, once | C, Lakeshore ($40.7M, 1.28× over E) | Demand response from the authority's own natural experiments | The corridor agreement: an hour whose volume exceeds capacity is degraded and runs HOV-only, and Lakeshore's peak needs $14.80 |
| 3 | **Decisive:** each hour's steady-state toll (the price at which choosers fit 1,600 an hour), capped at $14, degraded hours earning nothing | **E, Ridge Road** (tied 4th of 5 on rung 0), **$33.7M a year** | — | — |

* **Position table.** Ridge Road ties 4th on rung 0, ties 3rd on rung 1 and is 2nd on rung 2 (1.28× behind Lakeshore), and leads only
  rung 3 (1.55× over Lakeshore).
* **Discriminator dominance.** Lakeshore carries a 1.28× advantage into rung 3 ($40.7M against $31.9M). Solving the steady state multiplies
  Ridge Road's revenue by 1.06 and Lakeshore's by 0.53, an edge of 1.99×, above the 1.53× floor. Product: 1.99 / 1.28 = 1.55.
* **Partial correction priced (L3).** A solver who solves the steady state on average peak hours ties Western and Ridge Road at $33.7M,
  and the board's tie-break (lower conversion cost) names Western, which really earns $16.7M. One who solves it hour by hour but removes
  every commercial vehicle names Ridge Road at $27.4M (−18.8%). One who keeps the heavy trucks in names Port Way.
* **Grid.** Commercial reading (all counted, all removed, registry split) × toll (indicative once, steady state) × grain (average hour,
  each hour) gives 12 cells. Indicative-toll cells name Port Way or Lakeshore (1.22× to 1.31× clear); steady-state cells name Port Way,
  the Western tie, or Ridge Road at −18.8%. Only the answer cell names Ridge Road at $33.7M.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The operations manual says the toll adjusts every five minutes against lane volume; the statute gives the
   maximum; the corridor agreement defines degraded hours. No document joins them or says a corridor can lose its peak.
2. **Corpus blind for a computable reason.** *In every logged toll change the steady-state toll stayed below $14, because no existing
   lane's eligible demand ever exceeded 4,500 vehicles an hour.* The change log certifies the elasticity, 9 of 9, and never shows a
   degraded hour.
3. **No arithmetic symptom.** Counts reconcile to detector totals, the registry join matches every plate, and the one-pass projection
   is internally consistent.
4. **Not a row predicate.** Each hour's toll solves an equation in which the toll sets its own volume, then is compared with the cap,
   then the hour is kept or zeroed, over 2,500 tolled hours per corridor.
5. **The enumeration is arithmetic.** No column marks an hour as degraded; the threshold (4,903 eligible vehicles an hour) exists only
   in the solution.
6. **No cutover date.** Volumes are a stable weekday profile, and no series steps.
7. **Survives deletion.** Removing the feasibility study and every voice leaves the change log certifying the one-pass rung.

## 6. The calibration corpus

* **Form.** The change log's nine toll-table changes on the four existing lanes, with hourly lane volumes for four weeks before and after.
* **What it certifies.** The elasticity: volume falls 8.0% per dollar in all nine changes (7.8–8.2%). Treating demand as fixed misses all
  nine.
* **What it is blind to.** The ceiling (above).
* **Twin pair.** Western and Ridge Road are identical on average peak volume (5,200 an hour counted), shoulder volume (3,000), heavy share
  (16%) and van share (10%). Western's peak runs two hours at 7,800 and two at 2,600. Solved hour by hour, Western earns $16.7M and Ridge
  Road $33.7M, 2.0× apart, separated only by the hour-by-hour solve against the ceiling.
* **Resemblance points at the decoy.** Lakeshore's volumes most resemble the busiest existing lane, where every logged toll increase
  raised revenue.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The statute: tolls may not exceed $14; vehicles over 26,000 lb may not use express lanes, and lighter commercial
  vehicles pay the car toll. The corridor agreement: an hour in which lane volume exceeds 1,600 is degraded, and degraded hours run
  HOV-only. The operations manual: the toll adjusts every five minutes against lane volume. The board's rule: a conversion is judged on
  annual toll revenue, and equal cases go to the lower conversion cost.
* **Empirical pins.** The elasticity, from the change log. The eligible share, from the registry join.
* **Voices.** The finance director: "Revenue goes where the traffic is, and Port Way carries the most vehicles in the region." The corridor
  manager: "Lakeshore is the most congested road we run. That is what express lanes are for."
* **Licensed wrong basis.** The board's rule records that the state transport department's feasibility study ranks corridors on
  indicative tolls at today's counts and will present that ranking.

## 8. Determinism by construction

* **Elasticity.** All nine logged changes give 8.0% ± 0.2% per dollar, and log-linear and linear fits agree to within 0.1 point.
* **Threshold clearance.** No corridor-hour's eligible volume lies within 3% of 4,903, so any elasticity in the logged range sorts every
  hour the same way.
* **Hours.** Tolling runs 4 peak and 6 shoulder hours on 250 weekdays; every tolled hour's eligible demand exceeds 1,600, so the minimum
  toll never applies.
* **Registry.** Every counted plate matches the registry, and every commercial plate carries a gross weight.
* **Rounding.** Ridge Road's figure is $33.71M, mid-bin at $0.1M.

## 9. Prompt sketch and deliverables

> The board picks the next express-lane conversion on the 4th and wants one corridor and its annual toll revenue, to the nearest $0.1M.
> Our finance director is clear that revenue goes where the traffic is. Give me the recommendation in a sentence, with
> `corridor_revenue.xlsx`, a chart `hourly_tolls.svg`, and a two-page `conversion_paper.pdf`.

* `corridor_revenue.xlsx` — the five corridors on four bases with each hour's steady-state toll, the violations sheet (ask A) and the
  incident sheet (ask B).
* `hourly_tolls.svg` — a script-rendered line chart per corridor: the steady-state toll by hour of day against the $14 ceiling line,
  degraded hours shaded, the indicative toll as a dashed comparison line, and Western's and Ridge Road's panels placed side by side.
* `conversion_paper.pdf` — the committed corridor, its revenue, and why the other four fall away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the four existing express lanes, last year's share of trips billed by plate and the
  share of those invoices paid. *Device:* a plate invoice returned undeliverable is reissued as a new invoice carrying the original trip in
  `orig_txn`, as the billing guide documents. Counting invoices as trips inflates plate billing on the two lanes with most rental cars.
* **Ask B (device-carried).** For each candidate corridor, last year's median minutes to clear a lane-blocking incident and the share
  taking over an hour. *Device:* the traffic centre logs each incident update as a row under one incident number, and its guide times
  clearance to the last `lanes_open` update. Using the first update understates clearance on three corridors.
* **Ask C (validity).** Each corridor's revenue under each of the four rung bases, and logged changes reproduced (of 9) by the elasticity
  and by fixed demand.
* **Decoupling.** Replacing the steady-state toll with the one-pass toll changes no figure in asks A or B. Plate invoices and incident logs
  touch neither the counts, the registry nor the change log.

## 11. Rubric arithmetic

4 lanes × 2 (ask A) + 5 corridors × 2 (ask B) + 5 corridors × 4 bases and 2 back-test counts (ask C) + the committed corridor, its revenue,
the runner-up, the margin and Lakeshore's degraded hours + 5 named chart parts + 3 files ≈ 52 criteria.

## 12. World-building constraints

* Counted volume an hour (peak, shoulder), heavy and van shares: Port Way 7,200 / 4,800, 60% / 5%; Northern 10,000 / 1,800, 3% / 4%;
  Lakeshore 5,400 / 3,400, 3% / 4%; Western peaks of 7,800 and 2,600 (average 5,200) / 3,000, 16% / 10%; Ridge Road 5,200 / 3,000, 16% /
  10%.
* Lane capacity 1,600 an hour; elasticity 8% per dollar; maximum $14; degraded threshold 4,903 eligible vehicles an hour.
* Rung figures ($M): rung 0 46.8 / 38.0 / 29.1 / 25.3 / 25.3; rung 1 8.6 / 36.8 / 27.3 / 17.9 / 17.9; rung 2 20.9 / 30.5 / 40.7 / 31.9 /
  31.9; rung 3 17.2 / 2.6 / 21.7 / 16.7 / 33.7 (Port Way, Northern, Lakeshore, Western, Ridge Road).
* No existing lane's eligible demand exceeds 4,500 an hour in any logged hour.
* Western and Ridge Road match on every average and class share; Western's conversion cost is lower.
* Plate invoices and incident logs never touch counts, registry or the change log.

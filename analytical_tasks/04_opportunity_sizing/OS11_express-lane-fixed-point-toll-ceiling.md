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
| Measured traps engaged | #22 solves a self-referencing rule in one pass · #6 treats a mixed segment all one way · #13 validates on one population, applies to another |
| Calibration form | Change-log natural experiments: the nine logged toll-table changes on the authority's four existing express lanes, with hourly volumes before and after |
| Driving force | An express-lane toll is set by the demand it creates: it rises until the vehicles that choose the lane fit its capacity of 1,600 an hour. That steady-state toll is a fixed point, and where it would pass the $14 legal maximum the hour is degraded and runs HOV-only, earning nothing. A one-pass projection at today's volumes never meets the ceiling, and neither does a solve on average hours. Solved hour by hour with the change log's elasticity, Lakeshore needs $14.59 to $14.82 in seven of its ten tolled hours and they go free, and Western, which outearns Ridge Road on average hours, loses its two sharpest peak hours and its busiest shoulder. |

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
* **Instrument repair.** The suspect file is the detector count, which records all commercial vehicles in one class rather than by the
  weight that decides eligibility. Replace it with weigh-in-motion counts by weight: rung 0 still returns Port Way, rung 1 Northern (the
  registry split was already exact) and rung 2 Lakeshore, and the hour-by-hour steady state is still needed.
* **Lens swap.** The naive read prices today's traffic. The answer prices the traffic that the steady-state toll leaves in the lane,
  hour by hour, a different population at a different moment.

## 3. The driving force

A strong solver drops the feasibility study's diversion share, removes the heavy trucks the statute bars (reached by joining counted plates
to the vehicle registry, because the counts lump all commercial vehicles together), and applies the change log's elasticity: each extra
dollar cuts lane volume by 8%. Applied once to the indicative toll at today's volumes, Lakeshore leads. But the toll is not an input. It
adjusts against lane volume until the vehicles that pay fit the lane. In Lakeshore's four peak hours that price is $14.59, and in three of
its shoulder hours $14.82. The statute stops the toll at $14, demand stays above capacity, the hour is degraded, and the corridor agreement
runs degraded hours HOV-only. Lakeshore keeps three hours of ten. A solve on average hours sees none of this for Western, whose averages
sit under the threshold and outearn Ridge Road's. Hour by hour, Western's two sharpest peak hours and its busiest shoulder cross the
ceiling. Ridge Road's busiest hour needs $13.48 and never does.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Counted volume × 25% diversion × the indicative toll | A, Port Way ($53.4M, 1.27× over B) | The feasibility study's method on the authority's own counts | The registry joined to the counts: 60% of Port Way's vehicles are over 26,000 lb and barred from the lane |
| 1 | The same on eligible traffic (heavy trucks out, vans in) | B, Northern ($40.7M, 1.26× over C) | The statute applied record by record | The change log: lane volume falls 8% for each extra dollar of toll, 9 of 9 logged changes |
| 2 | Indicative toll at today's eligible volume, then the logged elasticity, once | C, Lakeshore ($45.2M, 1.26× over D) | Demand response from the authority's own natural experiments | The corridor agreement: an hour whose volume exceeds capacity is degraded and runs HOV-only, and Lakeshore's peak needs $14.59 |
| 3 | **Decisive:** each hour's steady-state toll (the price at which choosers fit 1,600 an hour), capped at $14, degraded hours earning nothing | **E, Ridge Road** (5th of 5 on rung 0), **$30.9M a year** | — | — |

* **Position table.** Ridge Road ranks 5th on rung 0 (1.17× behind Western), 4th on rung 1 and 4th on rung 2, and leads only rung 3 (1.42×
  over Port Way). It is never 2nd.
* **Discriminator dominance.** Lakeshore carries a 1.49× advantage into rung 3 ($45.2M against $30.4M). Solving the steady state hour by
  hour multiplies Ridge Road's revenue by 1.02 and Lakeshore's by 0.20, an edge of 4.98×, 2.79 times the 1.78× floor. Product: 4.98 / 1.49 =
  3.35.
* **Partial correction priced (L3).** Every half-applied construction names a wrong corridor outright. A solver who solves the steady state
  on average hours names Western ($38.8M against Ridge Road's $30.9M, 1.26×), which really earns $19.6M. One who solves it hour by hour but
  removes every commercial vehicle, vans included, drops Lakeshore's busiest hours to 4,611 and 4,698 eligible vehicles, under the ceiling's
  threshold, and names Lakeshore ($44.9M against Western's $30.8M, 1.46×). One who keeps the heavy trucks in names Port Way ($31.7M against
  Ridge Road's $14.6M, 2.17×).
* **Grid.** Commercial reading (all counted, all removed, registry split) × toll (indicative once, steady state) × grain (average hour, each
  hour) gives 12 cells. Indicative-toll cells name Port Way or Lakeshore (1.07× to 1.28× over the runner-up, at least 1.33× over Ridge
  Road); steady-state cells name Port Way (1.09× to 2.18×), Lakeshore (1.42× to 1.46×) or Western (1.26×). Only the answer cell names Ridge
  Road, and the nearest wrong cell, the average-hour solve, is one toggle away.

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
* **Twin pair.** Western's and Ridge Road's morning peaks are identical on the count summary: 5,600 vehicles an hour counted over the two
  hours, 16% heavy, 10% vans. Western's runs one hour at 6,050 and one at 5,150; Ridge Road's runs two at 5,600. Solved hour by hour, Ridge
  Road's morning earns $43,140 a weekday and Western's $19,890, 2.2× apart. Averaged, they earn the same, so only the hour-by-hour solve
  against the ceiling separates them.
* **Resemblance points at the decoy.** Lakeshore's volumes most resemble the busiest existing lane, where every logged toll increase
  raised revenue.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The statute: tolls may not exceed $14; vehicles over 26,000 lb may not use express lanes, and lighter commercial
  vehicles pay the car toll. The corridor agreement: an hour in which lane volume exceeds 1,600 is degraded, and degraded hours run
  HOV-only. The operations manual: the toll adjusts every five minutes against lane volume. The board's rule: a conversion is judged on
  annual toll revenue.
* **Empirical pins.** The elasticity, from the change log. The eligible share, from the registry join.
* **Voices.** The finance director: "Revenue goes where the traffic is, and Port Way carries the most vehicles in the region." The corridor
  manager: "Lakeshore is the most congested road we run. That is what express lanes are for."
* **Licensed wrong basis.** The board's rule records that the state transport department's feasibility study ranks corridors on
  indicative tolls at today's counts and will present that ranking.

## 8. Determinism by construction

* **Elasticity.** All nine logged changes give 8.0% ± 0.2% per dollar, and log-linear and linear fits agree to within 0.1 point.
* **Threshold clearance.** No corridor-hour's eligible volume lies within 3% of 4,903. Across the logged elasticity range (7.8% to 8.2%)
  the threshold moves between 4,768 and 5,043, and Western's sharpest hours (5,082) and Ridge Road's peak (4,704) stay on their sides.
* **Hours.** Tolling runs 4 peak and 6 shoulder hours on 250 weekdays; every tolled hour's eligible demand exceeds 1,600, so the minimum
  toll never applies.
* **Registry.** Every counted plate matches the registry, and every commercial plate carries a gross weight.
* **Rounding.** Ridge Road's figure is $30.90M, mid-bin at $0.1M.

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

* Counted volume an hour, heavy and van shares: Port Way 9,600 peak and 4,600 shoulder, 60% / 5%; Northern 10,500 / 2,400, 3% / 4%;
  Lakeshore 5,300 peak, three shoulder hours at 5,400 and three at 3,050, 3% / 10%; Western peak hours of 6,050, 5,150, 6,050 and 5,150, one
  shoulder hour at 6,300 and five at 2,800, 16% / 10%; Ridge Road 5,600 / 2,600, 16% / 10%.
* Lane capacity 1,600 an hour; elasticity 8% per dollar; maximum $14; degraded threshold 4,903 eligible vehicles an hour.
* Rung figures ($M, Port Way, Northern, Lakeshore, Western, Ridge Road): rung 0 53.4 / 42.2 / 34.3 / 30.3 / 25.9; rung 1 12.4 / 40.7 / 32.3
  / 21.4 / 18.3; rung 2 24.2 / 35.2 / 45.2 / 35.9 / 30.4; rung 3 21.7 / 11.3 / 9.2 / 19.6 / 30.9; the average-hour steady state 21.7 / 11.3
  / 28.2 / 38.8 / 30.9.
* No existing lane's eligible demand exceeds 4,500 an hour in any logged hour.
* Western's and Ridge Road's morning peaks match on the two-hour average and both class shares.
* Plate invoices and incident logs never touch counts, registry or the change log.

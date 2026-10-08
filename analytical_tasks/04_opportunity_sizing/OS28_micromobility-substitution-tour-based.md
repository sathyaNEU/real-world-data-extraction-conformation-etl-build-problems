# OS28 — Which car trips could be e-bike trips? A short trip inside a car tour cannot switch on its own

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Substitution sizing at the journey level rather than the step level (moving parts of a user journey to a lighter product, replacing one leg of a multi-leg shipment) |
| Domain | Urban mobility |
| Task shape | 03 · Bridge between two totals (weighted short car trips → substitutable car trips after tour constraints; the subsidy programme's addressable trip volume) |
| Core method | Build home-based tours from the trip file (sequence of trips from home back to home per person-day); a car trip is substitutable only if every car trip in its tour is ≤ 3 miles, no trip in the tour carries passengers needing a car (memo's rule) and the tour has ≤ 3 stops; weighted trips with person/trip weights |
| Analytical stump | Counting every car trip under 3 miles as "e-bike-able" ignores that the car is needed for other legs of the same tour (a short coffee stop on the way home from a 15-mile commute). Trip-level sizing overstates substitution; tours define feasibility |
| Primary sources | FHWA 2017 National Household Travel Survey (NHTS) public-use trip, person and household files |

## 1. The real-world situation

A city plans an e-bike subsidy and sizes its potential impact as the number of car trips under 3 miles made by residents of large urban areas.
Transport planners pointed out that many short car trips are links in longer car tours and could not switch independently.

## 2. The decision (one deterministic recommendation)

**The annual number of substitutable car trips (millions, weighted, urban residents) and whether it exceeds the memo's threshold for
launching the subsidy (≥ 40% of short car trips).**

Rules (planning memo):

* Data: NHTS 2017 trip file; respondents in urbanised areas ≥ 1 million (memo's MSA filter); trips by private vehicle as driver (TRPTRANS codes
  per memo).
* Weights: trip weight `WTTRDFIN` (annualised trips).
* Tours: for each person-day, sequences starting and ending at home (WHYFROM/WHYTO home codes); trips not in closed home-based tours
  excluded from substitution (counted separately).
* Substitutable car trip: in a tour where all car-driver trips are ≤ 3 miles (TRPMILES), the tour has ≤ 3 stops, and no trip in the tour has
  passengers under 12 or purpose "pick up/drop off someone" (memo).
* Bridge: all short car trips → minus trips in tours with long legs → minus passenger/escort constraints → minus tours with > 3 stops →
  substitutable.
* Launch if substitutable ÷ short car trips ≥ 40%.

## 3. Why capable analysts get it wrong

* Trip-level filters are simple and match how trip tables are organised.
* Mode choice is made for the tour; the car leaves home and must return.
* Escort trips and passengers require a car.
* Weights must be the trip weights, annualised.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `trippub.csv` | CSV | ~924k trips | FHWA NHTS 2017 | U.S. Gov public domain | Trips with mode, distance, purposes, weights |
| 2 | `perpub.csv` | CSV | ~264k persons | FHWA NHTS 2017 | Public domain | Person attributes |
| 3 | `hhpub.csv` | CSV | ~130k households | FHWA NHTS 2017 | Public domain | Household location (MSA size) |
| 4 | `nhts_2017_codebook.xlsx` | XLSX | — | FHWA | Public domain | Codes |
| 5 | `planning_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `trip_level_sizing.xlsx` | XLSX | — | Task author | — | Naive sizing |
| 7 | `tour_construction_rules.json` | JSON | — | Task author | — | Tour algorithm |
| 8 | `tours.parquet` | Parquet | ~400k | Derived | Public domain | Constructed tours |

## 5. Deterministic solution path

1. Filter urban respondents; order trips per person-day; construct home-based tours.
2. Flag tours meeting the constraints; identify substitutable car trips.
3. Weighted totals; bridge; launch rule.
4. Contrast with trip-level sizing.

## 6. Wrong paths (method errors, not misreadings)

**A — trip-level ≤ 3 miles.** Overstated.

**B — unweighted counts.** Sample, not annual trips.

**C — ignoring escort trips.** Infeasible switches counted.

**D — person weights for trips.** Wrong annualisation.

## 7. Why the stump is analytical, not semantic

Tour rules and constraints are specified. The trap is the unit of decision (tour versus trip).

## 8. Draft task prompt (prose)

> How many car trips could our e-bike subsidy realistically replace? Size substitution at the tour level from NHTS as the planning memo specifies.
> Provide `substitution_bridge.csv` (step: weighted trips), `tour_examples.png` (diagrams of three tour types), and a one-page
> `subsidy_case.pdf`.

## 9. Deliverables

* `substitution_bridge.csv`, `tour_examples.png`, `subsidy_case.pdf`.

## 10. Where 25+ rubric criteria come from

* Bridge steps; totals; share; launch call; counts of tours by type; contrast.

## 11. Golden-output checklist

* Urban filter; tour construction; constraints; trip weights; bridge; rule.

## 12. Build notes (scope tuning)

* Confirm the substitutable share falls below 40% while trip-level sizing implies launch.

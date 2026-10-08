# DS30 — The haddock limit that keeps the fleet inside its 1,200-tonne cod cap, when half the small trawlers switch to day trips

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · fisheries quota management |
| Mirrors | Carrying a per-unit rate onto a forward operation whose batch structure changes (per-stop cost shares in delivery networks when routes densify, per-session ad-load or crash rates when sessions shorten, per-job cloud overhead when long batch jobs are split into many short runs) |
| Decision shape | An allocation under a cap: the fleet's haddock limit, set where projected cod catch at the filed sector keys uses the 1,200 t cod limit |
| Committed call | Next fishing year's haddock catch limit, in tonnes to the nearest 100 |
| Gap · Pattern | Gap 1 (time) into Gap 2 (population) · S6, a correct share carried onto a different book (each day's share of its trip's cod is right for six-day trips and wrong for day trips), with the population a flag suggests (E33) at rung 1 |
| Gate G mechanism | binding_constraint, with forecasting |
| Measured traps engaged | #13 validates on one population, applies to another · #7 uses the ready-made measure · #5 takes the population a flag or filter suggests |
| Calibration form | Retry or revision log: five closed fishing years of fish tickets, with each ticket's first submission and every later revision, and the published final catch by sector |
| Driving force | Small-trawl cod comes in two parts: about 0.59 t on the first set of every trip, made on the inshore grounds on the way out, and 0.20 t a day after that. The observer programme's per-day rate is each day's share of a six-day trip. Next year vessels holding half the sector's days move to 48-hour day-boat trips, which pay the first set four times as often. Every closed year reconciles under either rate, because trips never got shorter. |

## 1. Situation

A regional fishery council sets next year's haddock catch limit on the 3rd. Haddock is caught alongside cod, and its harvest rule sets the
haddock limit where the fleet's projected cod catch, at the filed sector keys, uses the 1,200-tonne cod limit. Five sectors share the
haddock limit (large trawl 33%, small trawl 29%, longline 14%, gillnet 10%, seine 14%). This year the council issued 48-hour day-boat
permits to 22 small-trawl vessels. The chair believes five years inside the cod limit prove the fleet's rates.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: tickets, revisions, observer hauls, the published per-day discard rates, the enrolment history and
  the permit register. No stakeholder read is overturned: the fleet did stay inside the cod limit, and the per-day rates do reproduce every
  closed year. The difficulty is that next year's small-trawl trips are a different book.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the chair's view and the industry panel's basis. Per-day rates by sector, carried onto next year's planned
  days, still set the limit at 45,800 t.
* **Instrument repair.** Put an observer on every trip. The per-day rate becomes exact for the six-day book and is still the wrong rate for
  day trips, which have not yet been fished.
* **Lens swap.** The naive read and the answer are different books at different moments: six-day trips in closed years against day trips
  next year.

## 3. The driving force

A strong solver builds cod catch as landings plus observer-estimated discards, assigns trips to sectors properly, takes each sector's cod
per tonne of haddock, and solves for the haddock limit that uses 1,200 t of cod. Every input is correct, and the per-day rates reproduce
every closed year to the tonne. But cod in the small-trawl sector does not accrue by the day. Observed hauls show the first set of each
trip, made while crossing the inshore grounds, carrying 0.55 to 0.62 t of cod, and every later day 0.20 t. A per-day rate is each day's
share of that trip, correct for six-day trips. Next year 22 vessels holding half the sector's fishing days work 48-hour trips averaging 1.5
days, and pay the first set four times as often per day. Their cod per tonne of haddock rises 1.98×. The haddock that 1,200 t of cod
allows falls with it.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Landed cod over landed haddock by sector, three closed years, at the filed keys | 54,500 t (+35.2%) | The fleet's own landings record, simple and stable | The catch-accounting rule: the cod limit counts catch, landings plus discards estimated from observer rates |
| 1 | Hygiene, then catch: each ticket at its latest revision, plus the observer programme's published per-day discard rates; sectors from the vessel roster's sector field | 49,800 t (+23.6%) | Clean, revision-corrected catch on the programme's published rates | The enrolment history: trips count to the sector a vessel was enrolled in on the trip date, and nine low-cod seiners joined small trawl mid-year |
| 2 | Sectors as enrolled on each trip date; per-day cod rates by sector carried onto next year's planned days | 45,800 t (+13.6%) | Every assignment right, every closed year reproduced exactly | The permit register: 22 small-trawl vessels, holding half the sector's days, fish 48-hour trips from 1 May |
| 3 | **Decisive:** small-trawl cod rebuilt as a first-set amount per trip plus a daily amount from observed hauls, applied to next year's trip structure | **40,300 t** | — | — |

* **Figure shape.** Every correction walks the limit down, and the answer is the minimum cell of the grid, so every partial build
  overstates the haddock the cod limit allows.
* **Partial correction priced (L3).** A solver who decomposes cod per trip but keeps last year's trip lengths lands back on 45,800 t
  (+13.6%). One who reads the permit change as "more trips" but keeps per-day rates lands there too. Partial applications that overshoot
  sit at least as far: treating all small-trawl cod as a per-trip amount gives 32,300 t (−19.9%), and moving every small-trawl vessel to
  day trips rather than the 22 permit holders gives 36,000 t (−10.7%), which the permit register refutes vessel by vessel.
* **Grid.** Cod basis (landings, catch) × sector assignment (roster field, trip-date enrolment) × daily model (per-day share, first set
  plus daily) = 8 cells. Only catch, trip-date enrolment and the first-set model give 40,300 t. The nearest other cell is 45,000 t (+11.7%),
  the first-set model with roster-field sectors, because the misfiled seiners dilute small trawl's rate before the first set multiplies it.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The observer programme publishes per-day rates. The permit register lists who may fish 48-hour trips. No document
   says cod has a per-trip part, or that the published rate belongs to a trip length.
2. **Corpus blind for a computable reason.** *In every closed year small-trawl trips averaged 5.8 to 6.2 days, because day-boat permits did
   not exist, so per-day and first-set-plus-daily rates reproduce every year's sector cod catch identically.* The revision log reproduces
   the published finals under both.
3. **No arithmetic symptom.** Tickets reconcile to the published finals, observer extrapolations to sector catch, and days fished to the
   effort records, under every rung.
4. **Not a row predicate.** It needs trips built from departure and return pairs, hauls ranked inside each trip, the first set separated
   from the daily rate, and the result carried onto a trip structure taken from the permit register.
5. **The enumeration is arithmetic.** Next year's small-trawl cod is computed from trips and days. No column holds a first-set amount.
6. **No cutover date.** The permits act on next year's book; nothing in any shipped series steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, the published per-day rate still looks like the rate.

## 6. The calibration corpus

* **Form.** The revision log: every fish ticket of five closed years, its first submission and each revision (weight corrections, species
  re-codes, late tickets), and the council's published final catch by sector and year.
* **What it certifies.** Rung 1's hygiene and rung 2's assignment. Latest revisions with trip-date enrolment reproduce all 25 published
  sector-year cod finals to the tonne; first submissions miss 19 of 25, all low, by 3% to 6%; roster-field sectors miss 10 of 25.
* **What it is blind to.** Trip length (above).
* **Twin pair.** Small-trawl vessel-years A-17 (2023) and B-04 (2024) are identical on every roster and ticket column: port, gear,
  length, 150 days fished and 1,800 t of haddock. Their cod catch was 45 t and 88 t (1.96×). B-04 was one of the few vessels that already
  fished short trips, 100 of them against A-17's 25, and only trips built from the departure and return records separate them.
* **Resemblance points at the decoy.** On every roster column next year's day-boat vessels resemble the small trawlers whose per-day cod
  was steady for five years.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The harvest rule: the haddock limit is set where the fleet's projected cod catch at the sector keys equals the cod limit.
  The catch-accounting rule: catch is landings plus discards estimated from observer rates. The enrolment rule: a trip counts to the sector
  the vessel was enrolled in on the trip date. The projection convention: next year's days fished equal the last closed year's. One
  sentence each.
* **Empirical pins.** First-set and daily cod, from observed hauls. Day-trip length (1.5 days), from the permit holders' short trips in the
  closed years.
* **Voices.** The council chair: "Five years inside the cod limit is our proof." The small-trawl sector manager: "Day boats fish the same
  grounds; a day is a day." The scientific adviser: "Discards are the whole story; landings undercount cod."
* **Licensed wrong basis.** The harvest rule records that the industry advisory panel will present a haddock limit set on landed-cod
  ratios.

## 8. Determinism by construction

* **First set.** Every observed small-trawl trip has at least two hauls. First-set cod runs 0.55 to 0.62 t and later days 0.18 to 0.22 t,
  so a first-haul average and an intercept fit give the same projection to 100 t.
* **Trips.** Departures and returns come from the vessel monitoring records; no trip crosses the fishing-year boundary, and no return falls
  within an hour of a departure.
* **Haddock per day.** Haddock per fishing day does not depend on trip length in any closed year, so the day-boat change moves cod alone.
* **Maturity.** All five closed years are final in the revision log, and no revision is dated after the extract.
* **Rounding.** The solve gives 40,295 t, inside the bin at the nearest 100 and clear of both edges.

## 9. Prompt sketch and deliverables

> The council sets next year's haddock limit on the 3rd, and under our harvest rule it sits where the fleet's cod comes to the
> 1,200-tonne cod limit. The chair's view is that five years inside that limit prove our rates. Give me the haddock limit in tonnes, to the
> nearest hundred, as the line the council will vote on. Send `haddock_limit.xlsx`, a chart `cod_per_tonne_by_sector.png`, and a one-page
> `council_paper.pdf`.

* `haddock_limit.xlsx` — the solve under each rung (ask C), the sector cod projections, the port sheet (ask A) and the lease sheet (ask B).
* `cod_per_tonne_by_sector.png` — cod per tonne of haddock for the five sectors under the published per-day rates and the first-set model,
  paired, with small trawl's day-boat and six-day vessels split, the fleet line that uses 1,200 t marked and the committed limit labelled.
* `council_paper.pdf` — the committed limit and why the published rate overstates it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 12 landing ports, last year's average first-sale price of haddock per tonne.
  *Device:* auction lots withdrawn unsold are re-offered the next day as new lots carrying the original lot's reference, as the auction
  file's guide documents. Counting both offers double-counts withdrawn tonnage and drags the average down in seven ports.
* **Ask B (device-carried).** For each month of the last fishing year, the haddock quota leased between sectors in tonnes and its average
  lease price. *Device:* the quota register books each lease as a debit and a credit under one transfer ID, and a cancelled lease as a
  reversing pair referencing it. Summing rows doubles the volume; ignoring reversals keeps four cancelled leases.
* **Ask C (validity).** The haddock limit under each of the four rung constructions, and each sector's projected cod under per-day rates
  and under the first-set model.
* **Decoupling.** Clearing the first-set model changes no figure in asks A or B. Auction lots and lease transfers touch no ticket, haul,
  trip or enrolment record.

## 11. Rubric arithmetic

12 ports (ask A) + 12 months × 2 (ask B) + 4 rung limits + 5 sectors × 2 (ask C) + the committed limit, small trawl's projected cod, its
first-set share and the margin to rung 2 + 5 named chart parts + 3 files ≈ 62 criteria.

## 12. World-building constraints

* Sector keys 0.33 / 0.29 / 0.14 / 0.10 / 0.14. Fleet cod per tonne of haddock by rung: 0.02200, 0.02411, 0.02620, 0.02978, giving
  54,500 / 49,800 / 45,800 / 40,300 t. Small trawl's own rate is 0.0180 with roster-field sectors and 0.0252 with trip-date enrolment.
* Small trawl: six-day trips at 0.30 t of cod a day (first set 0.59 t plus 0.20 t a day); day trips of 1.5 days at 0.59 t a day, 1.98×.
  The 22 permit holders fished half the sector's days last year; none of the nine seiners that joined mid-year holds a permit.
* Every closed year's small-trawl trips average 5.8–6.2 days; a few vessels, B-04 among them, fished short trips. A-17 and B-04 match on
  every roster and ticket column.
* Revision log: 25 sector-years, all reproduced by latest revisions with trip-date enrolment.
* Auction re-offers and lease reversals are independent of every main-call record.

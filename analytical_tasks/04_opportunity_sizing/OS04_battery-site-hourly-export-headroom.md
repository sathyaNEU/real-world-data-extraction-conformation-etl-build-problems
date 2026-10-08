# OS04 — Which site gets the 20 MW battery, when the best-priced node shares its substation with a wind farm that exports in the same evening hours

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · wholesale electricity markets |
| Mirrors | Siting capacity where the price signal is best, when what the asset can deliver is limited by a shared connection whose other users peak at the same hours (data-centre siting against shared grid ties at Google and Microsoft, storage on renewables-heavy nodes, edge caches behind an uplink that peaks with the same evening traffic) |
| Decision shape | Which of N gets one scarce thing, with the sizing kept as the graded figure: one battery, five candidate sites |
| Committed call | The site taken to the investment committee, and its 2026 energy-arbitrage revenue to the nearest $10k |
| Gap · Pattern | Gap 3 (objective) over Gap 2 (population) · S5 (an hourly export ceiling set by the coincidence of the battery's schedule with its neighbours' output), with the settlement node recovered through the interconnection agreement (#5) |
| Gate G mechanism | binding_constraint, with method_or_model_selection |
| Measured traps engaged | #10 notes a binding limit as a risk · #5 takes the population a flag suggests · #12 stops at the first control that passes |
| Calibration form | Published control set with a reproduction clause: the 24 monthly settled revenues of the company's two operating batteries in 2024, from the audited annual report |
| Driving force | A battery delivers only what its substation can take after the connections ahead of it. At Ridgeline a 35 MW wind farm and an 18 MW solar farm share a 60 MW substation, and the wind runs on most evenings when the battery would discharge. Headroom is an hourly quantity, firm capacity minus the neighbours' metered output, so it has to be built hour by hour and the schedule re-optimised under it. Neither operating battery has a neighbour, so the control set reproduces uncapped revenue exactly. |

## 1. Situation

A developer will take one site for a 20 MW / 80 MWh battery to its investment committee. The five candidates are Northfield, Harbor
Point, Ridgeline, Millbrook and Cedar Flats. The screening model ran a perfect-foresight optimisation on real-time zonal prices and
liked Northfield's spikes. The investment policy values a project on what it can deliver to the grid in its first full year, on 2024
prices and conditions. It admits a revenue method for siting only if the method reproduces each operating battery's settled revenue in
every month of 2024. Each candidate has a non-firm connection offer from the utility.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: zonal and nodal prices, the operating batteries' settlements, the utility's capacity map and
  the neighbours' metered output. No stakeholder read is overturned. The difficulty is that delivery at a shared substation is limited
  hour by hour, and the hours that bind are the hours the battery earns.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the screening model and every voice. The control set still certifies day-ahead scheduling at the nodal
  price, 24 of 24, and still names Ridgeline.
* **Instrument repair.** Meter every interval perfectly and publish every price. The neighbours' output is already metered exactly; the
  headroom binds whatever the instrument.
* **Lens swap.** The naive read is the revenue a 20 MW battery earns at a price. The answer is the revenue of the energy the substation
  can take from it in each hour, a different quantity at a different grain.

## 3. The driving force

A strong solver drops perfect foresight because no operator knows real-time prices in advance, and schedules day-ahead. It sees that
the site register gives a zone for each site, but the interconnection agreements name the bus each battery connects at, and the ISO
settles a resource at its bus. Day-ahead scheduling at the bus price reproduces all 24 control months to the dollar, so the clause is
satisfied and Ridgeline, whose bus carries an evening congestion premium, wins. But Ridgeline's offer is non-firm. Its 60 MW substation
already exports a 35 MW wind farm and an 18 MW solar farm, and the wind blows on the same winter and shoulder evenings that carry the
premium. Hour by hour, Ridgeline's battery can export a median of 7 MW when it wants 20, and re-optimised under those caps it keeps 40%
of its revenue. Cedar Flats has no neighbour and keeps all of it.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Perfect-foresight optimisation on real-time zonal prices | A, Northfield ($3.40M) | The screening model's own method, cleanly reproduced | The control set: perfect foresight reproduces 0 of 24 settled months |
| 1 | Day-ahead schedule, settled at the zone price the site register gives | B, Harbor Point ($1.50M, 1.25× over C) | Feasible dispatch on known prices; reproduces Lakeview's 12 months | The interconnection agreements name each battery's bus, and zone prices miss 8 of Oakridge's 12 months |
| 2 | Day-ahead schedule at each site's bus price | C, Ridgeline ($1.62M, 1.24× over B) | Reproduces all 24 control months to the dollar, as the clause demands | The capacity map and the neighbours' metered output: Ridgeline's evening headroom has a median of 7 MW |
| 3 | **Decisive:** day-ahead schedule re-optimised under hourly export caps (firm capacity minus the hourly metered output of every earlier connection at the substation), at the bus price | **E, Cedar Flats** (5th of 5 on rung 0), **$1.15M** | — | — |

* **Position table.** Cedar Flats ranks 5th on rung 0, 5th on rung 1 and 3rd on rung 2, and leads only rung 3 (1.28× over Northfield).
* **Discriminator dominance.** Ridgeline carries a 1.41× advantage into rung 3 ($1.62M against $1.15M). Cedar Flats keeps 1.00 of its
  revenue under the caps and Ridgeline 0.40, an edge of 2.50×, above the 1.69× floor. Product: 2.50 / 1.41 = 1.77.
* **Partial correction priced (L3).** A solver who checks 20 MW against Ridgeline's 60 MW firm capacity sees no conflict and stays at
  rung 2. One who nets the neighbours' annual average output (17 MW at their capacity factors) finds 43 MW of headroom, never binding,
  and stays at rung 2. Only the hourly coincidence binds.
* **Grid.** Foresight (perfect, day-ahead) × price (zone, bus) × export (uncapped, hourly caps) gives 8 cells. Perfect-foresight cells
  name Northfield (1.23× to 1.74× clear). Day-ahead at the zone price names Harbor Point uncapped and Northfield capped (1.16×). Only
  day-ahead at the bus price with hourly caps names Cedar Flats. Cedar Flats' own figure in any other cell is at least 17% from $1.15M.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The connection offers say export is non-firm and may be curtailed when the substation is at its firm capacity.
   Nothing says how often, in which hours, or that the curtailment should enter the valuation.
2. **Corpus blind for a computable reason.** *In every control month the battery's export headroom was the full 20 MW, because Lakeview
   and Oakridge are each the only connection at their substations.* Uncapped bus-price scheduling reproduces all 24 months.
3. **No arithmetic symptom.** Schedules respect energy and power limits, bus prices tie to the ISO archive, and the 24 settlements tie
   to the dollar.
4. **Not a row predicate.** Headroom needs the substation's connections grouped and summed per hour from metered output, subtracted from
   firm capacity, then a dispatch re-optimised under 8,784 hourly caps.
5. **The enumeration is arithmetic.** No column gives a site's deliverable export; the capacity map gives one firm figure per substation.
6. **No cutover date.** No connection at any candidate substation changes before 2026, and no series steps; the headroom is a property of
   coincident hours.
7. **Survives deletion.** Removing the screening model and every voice leaves the clause-certified rung 2 intact and wrong.

## 6. The calibration corpus

* **Form.** The published control set: Lakeview's and Oakridge's settled energy revenue for each month of 2024 (24 figures), with their
  schedules, bus prices and metered output.
* **What it certifies.** Day-ahead scheduling at the bus price, 24 of 24. Zone prices reproduce 16 of 24 (all eight misses at Oakridge
  run low, so the zonal total is 11% short). Perfect foresight reproduces none and overstates every month.
* **What it is blind to.** Hourly export caps (above).
* **Twin pair.** Lakeview and Oakridge are identical on power, energy, efficiency, zone, commissioning date and zone-price spreads. In
  the eight congested months Oakridge settles 2.1× Lakeview's revenue, because Oakridge's bus carries the evening premium. Only the
  bus-price rule separates them.
* **Resemblance points at the decoy.** Oakridge, the higher-earning control, most resembles Ridgeline: same zone, a congested bus,
  evening premiums.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The investment policy: a project is valued on the energy it can deliver to the grid in its first full year, on 2024
  prices and conditions. The policy's clause: a revenue method may be used for siting only if it reproduces each operating battery's
  settled revenue in every month of 2024. The connection offers: export is non-firm and may be curtailed when the substation is at its
  firm capacity, and earlier connections have priority.
* **Empirical pins.** The settlement node, from the interconnection agreements and certified by the control set. Hourly headroom, from
  the capacity map and the neighbours' metered output.
* **Voices.** The screening lead: "Northfield's spikes are the market telling us where storage is short." The origination director:
  "Ridgeline's congestion premium is the most bankable spread on the system."
* **Licensed wrong basis.** The investment policy records that the lender's engineer values storage on day-ahead revenue at the zone
  price and will present that valuation to the committee.

## 8. Determinism by construction

* **Valuation year.** The policy fixes 2024 prices and conditions, so the neighbours' 2024 metered output is the 2026 profile, and no
  connection at any candidate substation is under construction.
* **Dispatch.** One cycle a day, state of charge from 5% to 95%, returning to 50% at midnight, 85% round-trip efficiency on charge, as
  the battery specification files. A daily linear programme has a unique optimum on every day of the year (no flat price plateaus at the
  binding hours).
* **Charging.** Import never binds at any candidate: every substation's import headroom exceeds 20 MW in every hour.
* **Rounding.** Cedar Flats' figure is $1,151,400, mid-bin at the nearest $10k.

## 9. Prompt sketch and deliverables

> I'm taking one site for our 20 MW, four-hour battery to the investment committee and I need its revenue case. The screening team's view
> is that the zone with the wildest real-time prices is the obvious home. Tell me the site and its 2026 arbitrage revenue, to the nearest
> $10k, in one sentence for the committee paper. I'll need `site_case.xlsx`, the chart `site_revenue_ladder.png`, and a two-page
> `committee_paper.pdf`.

* `site_case.xlsx` — the five sites' revenue on each basis, the hourly headroom summary, the cycle sheet (ask A), the capacity-test sheet
  (ask B) and the control-set reproduction (ask C).
* `site_revenue_ladder.png` — a script-rendered dot plot: one row per site, a dot for each basis, connected left to right, the committed
  site highlighted, Ridgeline's retained share annotated, and the 24-of-24 control result noted under the bus-price dots.
* `committee_paper.pdf` — the committed site, its revenue, and why the other four fall away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each operating battery, equivalent full cycles in each month of 2024 and the months above
  the warranty's 30-cycle limit. *Device:* the battery management system logs throughput in DC MWh at the cells, and the warranty counts
  AC MWh at the meter. Dividing DC throughput by nameplate overstates cycles by about 9% and flags two months that do not breach.
* **Ask B (device-carried).** For each operating battery, usable energy at each quarterly capacity test and the fade per 100 cycles.
  *Device:* tests run at different ambient temperatures, and the test procedure corrects readings to 25°C with a filed coefficient.
  Uncorrected readings invent a winter fade at Oakridge.
* **Ask C (validity).** Each site's revenue under each of the four rung bases, and control months reproduced (of 24) by perfect
  foresight, zone-price and bus-price scheduling.
* **Decoupling.** Removing the hourly caps changes no figure in asks A or B. Cycle logs and capacity tests touch neither prices nor
  settlements nor the capacity map.

## 11. Rubric arithmetic

2 batteries × 12 months (ask A) + 2 × 4 tests and 2 fade rates (ask B) + 5 sites × 4 bases and 3 reproduction counts (ask C) + the
committed site, its revenue, the runner-up and the margin + 5 named chart parts + 3 files ≈ 69 criteria.

## 12. World-building constraints

* Revenue ($k): perfect foresight at zone price A 3,400, B 2,700, C 2,500, D 2,250, E 1,950; at bus price 3,200, 2,400, 2,600, 2,200,
  2,100. Day-ahead at zone price 1,180, 1,500, 1,200, 1,000, 950; at bus price 900, 1,310, 1,620, 1,000, 1,150.
* Retained share under hourly caps: Northfield 1.00, Harbor Point 0.68, Ridgeline 0.40, Millbrook 0.85, Cedar Flats 1.00.
* Ridgeline: 60 MW firm, wind 35 MW and solar 18 MW ahead, median evening headroom 7 MW. Annual-average netting leaves 43 MW.
* Rung leaders A, B, C, E at 1.26×, 1.25×, 1.24×, 1.28×; every grid cell's leader at least 1.16× clear.
* Lakeview and Oakridge are sole connections, identical on every specification column.
* Cycle logs and capacity tests never touch prices, settlements or substation data.

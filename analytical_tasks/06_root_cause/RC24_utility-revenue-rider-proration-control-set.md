# RC24 — Which driver of the utility's 9% revenue jump the advocate contests, when only a month-by-month rider bridge is admissible

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Economics · regulated utility finance |
| Mirrors | Revenue bridges at usage-priced platforms (cloud usage revenue with mid-year price changes, app-store fee changes at Apple and Google, marketplace take-rate changes at Amazon), where a price factor that moves with the season covaries with volume and an annual-average bridge books the covariance to the wrong driver |
| Decision shape | Which of N root causes gets the fix: the one driver the consumer advocate contests in the earnings review |
| Committed call | The driver contested, and its dollars of the year's retail revenue increase |
| Gap · Pattern | Gap 4 (rule) · Pattern B (a reproduction-gated control set: the commission staff's published revenue bridges), whose decisive component is the fuel rider prorated month by month through the billing calendar, with E25 (a suppressed cell, bounded) at rung 2 |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #1 reports a failed back-test, ships anyway · #3 stops at a close but inexact match · #24 treats an unpublished figure as unknown |
| Calibration form | Published control set with a reproduction clause: staff's revenue bridges for the four preceding years, each component to the dollar |
| Driving force | The fuel rider rose in November on a winter gas forecast and stayed up through the heaviest months of use; gas fell and the rider kept collecting until March. Priced at its annual average against annual sales, the rider looks $110M smaller than it was, and that $110M lands in "base rates" and weather-driven volume. Residential bills cover two months, so the winter peak is billed after the factor that priced it has gone: only the rider's factors applied to each schedule's sales day by day of service, with every bill that straddles a factor change split by days through the billing calendar, reproduce staff's four published bridges to the dollar. That construction makes the rider the largest driver. |

## 1. Situation

An investor-owned utility's retail electric revenue rose $412M (9%) in a year. Its investor deck credits "approved rate increases"; the consumer advocate
has resources to contest one driver in the commission's earnings review. The candidates are the approved base-rate increase (A), over-collection
through the fuel cost rider (B), weather-driven sales (C), a new data-centre load on a confidential special contract (E) and a true-up of unbilled
revenue (F). The commission admits a party's revenue analysis only if its method reproduces each of staff's published bridges for the four preceding
years to the dollar. Staff publish the special contract's figures as confidential, inside the industrial class total.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: sales and revenue by schedule and month, the rider's filed factors and effective dates, the billing
  calendar, the class totals and staff's published bridges. The deck's "rate increases" are real increases, the data-centre load is real, and
  the unbilled true-up is real. Nothing is overturned; the decision turns on which construction the published record admits.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the deck, both voices and the licensed basis. A schedule-level bridge with the rider at its annual average still
  reconciles to $412M, still puts the contract first and the rider fourth.
* **Instrument repair.** Suspect file: staff's industrial class table, which publishes the special contract only inside the class total.
  Published in full, the contract's row shows $110M on 2.4 TWh, as rung 2's bound already gives: rung 1 then names E with rung 2, rung 0 still
  names A, and none names B. Sales, revenue, the rider's filed factors and the billing calendar are complete. The answer still needs each day of
  service priced at the factor in force that day through the billing calendar: no billing record, however complete, prices a January day of
  service at January's factor when its bill falls in March.
* **Lens swap.** The annual-average bridge prices a year's sales at a year's rider; the answer prices each day of service at the rider in
  force that day, wherever its bill fell, so $110M of revenue moves between drivers.

## 3. The driving force

A strong solver discards the deck's two lines, builds the bridge by rate schedule with stable schedule ids, and splits each schedule's price
change into base rates and the fuel rider, the rider at its filed annual average. The industrial class has a confidential row; valuing its 2.4
TWh at the published industrial price makes volume the story, so the solver bounds the row from the published class total less the published
schedules and finds the data-centre contract's $110M, which then leads. It tests the build against staff's four published bridges, as the
commission requires, and reproduces 11 of 20 published components exactly; the misses are the rider, base and volume cells of the three years
whose rider changed in winter. The rider is not collected at its average. It changes on a filed date, each bill carries the factor in force on
each day of service it covers, and a bill straddling a change is split by days. Residential bills cover two months, so the January and February
peak, 31% of residential sales, reaches bills rendered in March and April, after the factor that priced it has fallen. Applied day by day
through the billing calendar, the construction reproduces all 20 published cells, and the rider's over-collection comes to $175M, the largest
driver.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The investor deck's class-level bridge: price, volume, accounting, new contracts | A, rate increases ($205M) | The utility's own published bridge, reconciled to the total | Staff's bridges: class-level price and volume reproduce 4 of 20 published components |
| 1 | Schedule-level bridge, rider split from base at its annual average, the confidential industrial row's kWh valued at the published industrial price | C, sales volume ($254M) | Price measured where prices are set, every schedule mapped, the unpublished row valued the standard way | The industrial class total less its published schedules leaves $110M of revenue on 2.4 TWh in one confidential row, a third below the published price |
| 2 | The same with the confidential row bounded and attributed to the special contract | E, data-centre contract ($110M) | Nothing left unknown; 11 of 20 published components reproduce | The misses are the rider, base and volume cells of the three years whose rider changed in winter |
| 3 | **Decisive:** the rider's factors applied to each schedule's sales by day of service, bills straddling a change split by days through the billing calendar | **B, rider over-collection ($175M)** (5th of 5 on rung 0) | — | — |

* **Position table.** B ranks 5th on rung 0, 2nd on rung 1 (3.91× behind volume) and 4th on rung 2, and leads only rung 3. Rung leaders beat
  their runners-up by 1.53×, 3.91×, 1.22× and 1.59×.
* **Discriminator dominance.** The contract carries a 1.69× lead over the rider into rung 3 ($110M against $65M). Cycle proration multiplies
  the rider's figure by 2.69 and leaves the contract's unchanged, an edge of 2.69×, 1.33 times the required 1.2 × 1.69 = 2.03; the net margin
  is 1.59×.
* **Partial correction priced (L3).** Each half-built proration leaves the contract in front. A solver who applies each month's factor to the
  kilowatt-hours billed that month, ignoring that a residential bill covers the two months of service before it, prices much of the peak at
  March's lower factor: 16 of 20 cells reproduce and the rider comes to $92M against the contract's $110M (1.20×), naming E as rung 2 does.
  One who weights the annual factor by billed monthly sales without splitting straddling bills reproduces 14 and puts the rider at $82M
  against $110M (1.34×), again naming E.
* **Grid.** Grain (class, schedule) × confidential row (valued at the published price, bounded) × rider (annual, sales-weighted,
  billing-month, cycle-prorated) gives nine builds. The class build names A. Every build that values the confidential row at the published
  price names C, even with cycle proration (C $204M against B's $175M, 1.17×), because 2.4 TWh at the published price is $166M of volume.
  Bounded builds name E unless the rider is cycle-prorated, and only that build reproduces all 20 published cells.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The commission's rule demands reproduction and says nothing of method; the rider's tariff sheet states factors and
   effective dates. No document says bills straddling a change are split by days or that the bridge must be monthly.
2. **The control set pins a construction, not a menu.** Cycle-prorated factors reproduce 20 of 20 published cells; billing-month factors
   16, sales-weighted annual 14, average-valued confidential rows 14, annual average 11, class level 4. Every rider rival understates the rider in
   the winter-change years, so none reproduces the four years' rider total either; the average-valued rows miss the confidential cells and
   their years' base and volume cells. The construction joins each schedule's billing cycles to
   the rider's effective dates; it has no parameter.
3. **No arithmetic symptom.** Every build closes to $412M; schedules, classes and the confidential row reconcile.
4. **Not a row predicate.** A bill's rider revenue depends on the days of its cycle on each side of a filed date, joined from the billing
   calendar.
5. **The enumeration is arithmetic.** No column holds rider revenue by schedule and month; it is built.
6. **No cutover date.** The November rider change moves revenue gradually through cycles; the dated events (the base-rate order in January,
   the contract's start in March) step the series and are the decoys.
7. **Survives deletion.** With every voice and the deck gone, the bounded schedule bridge still names the contract.

## 6. The calibration corpus

* **Form.** Staff's earnings-surveillance revenue bridges for the four preceding years, each splitting the year's change into base rates, the
  rider, sales volume, special contracts and accounting items, to the dollar, with the special-contract cells marked confidential; and the
  commission's admission rule.
* **What it pins.** The construction (above), including the bound on the confidential rows, which decides the two confidential cells and
  their years' base and volume cells.
* **Twin pair.** Years Y-2 and Y-4 are identical on every class-level column: revenue change, sales change, customers and the average rider
  factor. Staff's rider components are $34M and $17M (2.0×): in Y-2 the rider rose in November, in Y-4 in May. Only cycle proration reproduces
  both.
* **Resemblance points at the decoy.** This year's class-level profile matches Y-3, a year staff attributed mostly to base rates.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The advocate's charter: the advocate contests the driver contributing the most to the year's retail revenue increase, on a
  bridge the commission will admit. The commission's admission rule. The rider's tariff sheets and the billing calendar.
* **Empirical pins.** The bridge's construction, from staff's published bridges; the confidential row from the class totals.
* **Voices.** The utility's investor-relations head: "The growth is the rate increases the commission approved." The advocate's staff economist:
  "It's customers moving tariffs and an accounting true-up."
* **Licensed wrong basis.** The rule records that the utility presents its revenue variance at customer-class level and will present that
  bridge at the hearing.

## 8. Determinism by construction

* **Cycles.** Twenty-one read cycles; residential schedules are billed every two months and the others monthly; every bill's start and end
  dates are in the calendar, and no rider change falls on a read date.
* **Confidential row.** The class total less the published schedules equals the confidential row exactly in every year.
* **Schedules.** Stable ids from the tariff crosswalk; no schedule opened or closed during the year except the special contract.
* **Accounting.** The unbilled true-up is taken from the revenue accounts as booked; no build differs on it.
* **Rounding.** Dollars to the nearest million; the committed figure sits mid-bin.

## 9. Prompt sketch and deliverables

> The utility's retail revenue is up 9% and we can afford to contest one driver in the earnings review. Our director is sure the data-centre
> contract is the story. Tell me which driver we contest and how many dollars of the increase it accounts for, to the nearest million, in a
> sentence for the testimony outline. Send `revenue_bridge.xlsx` and a chart `driver_bridge.png`.

* `revenue_bridge.xlsx` — the five drivers under each construction, the residential-bills sheet (ask A), the net-metering sheet (ask B) and
  the control-set reproduction (ask C).
* `driver_bridge.png` — a waterfall of the $412M increase by driver under the annual-average and the prorated rider side by side, with an inset
  of monthly sales against the rider factor and the contested driver highlighted.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the nine residential schedules, year-end customers and the average monthly bill.
  *Device:* budget-billing customers pay a level amount monthly with an annual settlement bill, flagged in the billing records, as the billing
  guide documents; averaging billed amounts puts the settlement spikes into three schedules' averages.
* **Ask B (device-carried).** For each month, net-metering customers' exported kWh and credits. *Device:* older meters record exports as negative
  usage on the import channel and newer ones on a separate channel, by meter type, as the metering guide documents; reading only the export
  channel misses 40% of exports.
* **Ask C (validity).** Each of staff's 20 published components and the value each of the five constructions returns; and each driver under
  each rung construction.
* **Decoupling.** Clearing the cycle proration changes no figure in asks A or B.

## 11. Rubric arithmetic

9 schedules × 2 figures (ask A) + 12 months × 2 figures (ask B) + 20 cells × 5 constructions + 5 drivers × 4 constructions (ask C) + the
contested driver, its dollars and the runner-up's + 5 named chart parts + 2 files ≈ 175 criteria.

## 12. World-building constraints

* $412M increase: rider 175, contract 110, unbilled true-up 59, weather sales 38, base rates 30 (cycle-prorated); the annual-average rider
  moves $110M out of the rider, $60M into base rates and $50M into weather-driven volume.
* Deck lines: rate increases 205, volume 134, accounting 59, new contract minimum charges 14.
* Rung 1 values the confidential row's 2.4 TWh at the published industrial price, $166M of volume against its $110M of revenue (base
  −$56M): C 254, B 65, F 59, A 34. With cycle proration that build gives C 204 against B 175.
* Partial builds (B / E / A / C): billing-month factors 92 / 110 / 76 / 75; sales-weighted annual 82 / 110 / 80 / 81.
* The rider rose on 1 November and fell on 1 March; January and February carry 31% of residential sales.
* Reproduction: cycle-prorated 20/20, billing-month 16, sales-weighted 14, average-valued confidential rows 14, annual 11, class 4.
* Y-2 and Y-4 identical on every class-level column; rider changes in November and May.
* Budget-billing settlements and meter channels touch no revenue-by-usage cell.

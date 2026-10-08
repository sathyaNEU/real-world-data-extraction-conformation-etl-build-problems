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
| Driving force | The fuel rider rose in November on a winter gas forecast and stayed up through the heaviest months of use; gas fell and the rider kept collecting. Priced at its annual average against annual sales, the rider looks $80M smaller than it was, and that $80M lands in "base rates". Only the rider's monthly factors applied to each schedule's monthly sales, with bills that straddle a factor change split by days through the billing calendar, reproduce staff's four published bridges to the dollar. That construction makes the rider the largest driver. |

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
  reconciles to $412M and still puts the rider third.
* **Instrument repair.** Perfect metering and billing records change nothing: the rider's covariance with sales is in the correct monthly data
  already, and only a monthly construction reads it.
* **Lens swap.** The annual-average bridge prices a year's sales at a year's rider; the answer prices each month's sales at the rider that
  month's bills carried, so $80M of revenue moves between drivers.

## 3. The driving force

A strong solver discards the deck's two lines, builds the bridge by rate schedule with stable schedule ids, and splits each schedule's price
change into base rates and the fuel rider, the rider at its filed annual average. The industrial class has a confidential row; it bounds the
row from the published class total less the published schedules and so finds the data-centre contract's $128M, which then leads. It tests the
build against staff's four published bridges, as the commission requires, and reproduces 12 of 20 published components exactly; the misses are
the rider and base-rate cells of the years when the rider changed in winter. The rider is not collected at its average. It changes on a filed date,
each month's bills carry the factor in force for the days they cover, and a bill straddling a change is split by days. Winter months carry most of
the year's sales, and this year the rider was highest exactly then. Applied month by month through the billing calendar, the construction
reproduces all 20 published cells, and the rider's over-collection comes to $170M, the largest driver.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The investor deck's class-level bridge: price, volume, accounting, new contracts | A, rate increases ($196M) | The utility's own published bridge, reconciled to the total | Staff's bridges: class-level price and volume reproduce 4 of 20 published components |
| 1 | Schedule-level bridge, rider split from base at its annual average, the confidential industrial row left in industrial volume | C, sales volume ($157M) | Price measured where prices are set, every schedule mapped | The industrial class total less its published schedules leaves $128M in one confidential row |
| 2 | The same with the confidential row bounded and attributed to the special contract | E, data-centre contract ($128M) | Nothing left unknown; 12 of 20 published components reproduce | The misses are the rider and base cells of every year whose rider changed in winter |
| 3 | **Decisive:** the rider's monthly factors applied to each schedule's monthly sales, bills straddling a change split by days through the billing calendar | **B, rider over-collection ($170M)** (5th of 5 on rung 0) | — | — |

* **Position table.** B ranks 5th on rung 0 and 3rd on rungs 1 and 2, and leads only rung 3. Rung leaders beat their runners-up by 1.37×,
  1.48×, 1.21× and 1.33×.
* **Discriminator dominance.** The contract carries a 1.42× lead over the rider into rung 3 ($128M against $90M). Monthly proration
  multiplies the rider's figure by 1.89 and leaves the contract's unchanged, an edge of 1.89×, above the required 1.2 × 1.42 = 1.71; the net
  margin is 1.33×.
* **Partial correction priced (L3).** A solver who applies monthly factors to calendar-month sales, ignoring that bills cover read cycles,
  reproduces 17 of 20 cells and puts the rider at $112M, behind the contract's $128M, naming E as rung 2 does. One who weights the annual factor
  by monthly sales without splitting straddling bills reproduces 15 and puts the rider at $104M, again naming E.
* **Grid.** Grain (class, schedule) × confidential row (left in volume, bounded) × rider (annual, sales-weighted, calendar-monthly,
  cycle-prorated) gives ten feasible builds. Class builds name A, unbounded schedule builds C, bounded builds E unless the rider is cycle-
  prorated, and only that build reproduces all 20 published cells.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The commission's rule demands reproduction and says nothing of method; the rider's tariff sheet states factors and
   effective dates. No document says bills straddling a change are split by days or that the bridge must be monthly.
2. **The control set pins a construction, not a menu.** Cycle-prorated monthly factors reproduce 20 of 20 published cells; calendar-monthly
   17, sales-weighted annual 15, annual average 12, class level 4. Every rival understates the rider in the winter-change years, so none
   reproduces the four years' rider total either (the annual average misses it by 28%). The construction joins each schedule's billing cycles to
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
* **What it pins.** The construction (above), including the bound on the confidential cells, which decides two of the twenty.
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

* **Cycles.** Twenty-one read cycles; every bill's start and end dates are in the calendar, and no rider change falls on a read date.
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

* $412M increase: rider 170, contract 128, unbilled true-up 59, weather sales 29, base rates 26 (cycle-prorated); the annual-average rider
  moves $80M from rider to base.
* Deck lines: rate increases 196, volume 143, accounting 59, new contract minimum charges 14.
* Reproduction: cycle-prorated 20/20, calendar-monthly 17, sales-weighted 15, annual 12, class 4.
* Y-2 and Y-4 identical on every class-level column; rider changes in November and May.
* Budget-billing settlements and meter channels touch no revenue-by-usage cell.

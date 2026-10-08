# DA50 — The value per MWh of solar a developer commits for its solar-plus-storage project, when the pilot's battery gains came from connections the project will not have

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Economics · electricity markets and renewable investment |
| Mirrors | Carrying a pilot's average uplift to a site whose structural condition the pilot under-sampled (a caching tier piloted in regions with spare egress, a pricing feature tested where supply was elastic, warehouse robots piloted in buildings with wide aisles), where the uplift splits absolutely on a capacity property reached through a join |
| Decision shape | One figure committed at a date: the base-case value per MWh of solar output in the financial close model signed on 30 September |
| Committed call | The project's expected value per MWh of solar output, in A$ to one decimal |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · Pattern E (conditioned yield: a battery's uplift splits on export headroom reached through the connection register), with the deciding comparison (measured #20) at rung 1 |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #13 validates on one population, applies to another · #20 leaves the deciding comparison unstated · #7 uses the ready-made measure |
| Calibration form | Pilot log: the developer's two-year battery pilot at 14 of its 24 operating solar farms, each farm's five-minute output, battery flows and revenue, with the 10 farms without batteries as the same-year control |
| Driving force | A co-located battery earns most of its value in afternoon price spikes, and it can discharge into them only where the farm's connection lets it export above the solar rating while the panels still run at full output. In the pilot, the eleven farms with that export headroom gained 35 to 41 a MWh of solar and the three without gained 9 to 11, with nothing between. Headroom is the connection register's export limit against the farm's registered solar capacity, not a column of the pilot log. The pilot ran mostly where batteries pay; the project's connection offer gives it no headroom. |

## 1. Situation

A developer commits, in its financial close model, the expected value per MWh of solar output for a 200 MW solar farm with a co-located
100 MW / 400 MWh battery in one market region. The lenders' term sheet values each MWh at the region's generation-weighted solar price
plus the battery's uplift measured on the developer's own pilot. Two years ago the developer added batteries at 14 of its 24 operating
farms in the region. The pack holds two years of five-minute regional prices and solar output, the pilot log, the connection register
with each farm's export limit, the registration list, the project's connection offer and design basis, the screening model, and the term
sheet.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each price, each output, each pilot flow and revenue, each export limit. The screening model's
  time-weighted price answers a different, labelled question, and nothing reported is overturned. The difficulty is which pilot farms
  the project resembles.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the screening model and both voices. The generation-weighted price plus the pilot's same-year uplift, with
  commissioning months excluded, still commits 86.0.
* **Instrument repair.** No file is suspect: prices, outputs, pilot flows and the connection register are complete, and the register
  records each export limit as it claims. Commissioning months are real operation under hold points, present only at headroom farms. With
  every file perfect, rung 0 still commits 75.1, rung 1 83.6 and rung 2 86.0. The project's uplift is a forward quantity conditioned on a
  property joined from the register, so the answer stays 64.0 and the conditioning is still needed.
* **Lens swap.** The naive base carries the whole pilot's uplift; the answer carries only the uplift of farms that, like the project,
  cannot export above their solar rating, a different population of comparable batteries.

## 3. The driving force

A strong solver weights the region's prices by solar output, 54.0, not the screening model's time-weighted 88.0. It measures the battery's
uplift against each pilot farm's own revenue in the same year without its battery, since the ten farms without batteries show prices
falling 8.5 between the two years, and it drops the months new batteries ran under commissioning hold points. The pilot's uplift is 32.0
and the base case 86.0. But the uplift is not one number. Eleven pilot farms gained 35 to 41 a MWh of solar and three gained 9 to 11, with
nothing between. The difference is the connection. Where the export limit exceeds the solar rating, the battery discharges into the
afternoon spikes while the panels run flat out; where it equals the rating, the battery waits for the sun to drop and catches only the
evening. The pilot log has no such column; the connection register and the registration list give it. The project's offer sets its
export limit at its solar rating, so its battery adds 10.0 and the base case is 64.0.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Generation-weighted regional price + the pilot's uplift measured year on year, after the battery against before | 75.1, +17% | The textbook capture price plus the pilot's measured gain | The pilot log: the ten farms without batteries lost 8.5 a MWh between the same two years |
| 1 | The same price + uplift against each pilot farm's own same-year revenue without its battery (the deciding comparison) | 83.6, +31% | The year's price fall separated from the battery's effect | The pilot log: new batteries ran under commissioning hold points for two to four months |
| 2 | Hygiene: commissioning months excluded from the uplift | 86.0, +34% | Every pilot month on full operation | The pilot log and the connection register: farms with export headroom gained 35 to 41, farms without 9 to 11 |
| 3 | **Decisive:** generation-weighted price + the uplift of pilot farms whose export limit equals their solar rating, as the project's does | **64.0** | — | — |

* **Figure shape.** Rungs 0 to 2 walk the figure up, and the decisive rung reverses them below where they started: a solver who stops
  anywhere commits 17% to 34% too much to the lenders.
* **Partial correction priced (L3).** A solver who conditions on connection voltage, the visible proxy, puts the project with the 132 kV
  farms, four of them with headroom, and lands at 80.0 (+25%). One who conditions on headroom but measures the uplift year on year charges
  the price fall to the battery and lands at 55.5 (−13%).
* **Grid.** Comparison (year on year or same year) × commissioning (kept or excluded) × group (pooled, connection voltage, farm size,
  export headroom) = 16 cells. The nearest wrong cell is headroom with year-on-year uplift, 55.5 (−13%); every pooled cell sits 17% or
  more above the answer.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The term sheet asks for the pilot's measured uplift. The pilot log records flows and revenue, the register export
   limits, the registration list solar capacity. No document links headroom to a battery's gain.
2. **Pattern E, absolute in the pilot log.** The eleven farms with export headroom gained 35 to 41 and the three without 9 to 11, with
   nothing between; the pooled 32.0 fits no farm. Headroom is a construction: each farm's export limit from the register against its solar
   capacity from the registration list, joined through the connection point.
3. **No arithmetic symptom.** Pilot revenues tie to settlement, outputs to the market's records, and every farm's same-year counterfactual
   ties to its own output and prices.
4. **Not a row predicate.** The project's uplift is the conditioned mean of other farms' measured gains, each built from two years of
   five-minute flows; no row of any file carries it.
5. **The enumeration is arithmetic.** No column gives a farm's headroom or a battery's uplift.
6. **No cutover date.** Batteries entered at different dates across a year, and each uplift is measured against the farm's own same-year
   counterfactual, so no date steps the comparison.
7. **Survives deletion.** With every voice removed, the pooled same-year uplift still commits 86.0.

## 6. The calibration corpus

* **Form.** The pilot log: 14 farms with batteries added two years ago and 10 without, each with two years of five-minute output, battery
  flows, revenue and settlement.
* **What it certifies.** That batteries add value and that the year's price fall must be separated from it, which the ten farms without
  batteries show.
* **What it pins.** The split by export headroom, absolute across all fourteen farms.
* **Twin pair.** Farms P-04 and P-11 match on solar capacity (180 MW), battery size, tracking, DC/AC ratio and connection voltage. Their
  batteries earned A$210,000 and A$105,000 per MW over the measured year (2.0×): P-04 can export 40% above its solar rating and P-11
  cannot.
* **Resemblance points at the decoy.** On every pilot column, the project resembles the larger headroom farms.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The term sheet: the base case values each MWh of solar at the region's generation-weighted price plus the battery's
  uplift measured on the developer's pilot. The connection offer: the project's export limit is 200 MW.
* **Empirical pins.** The same-year comparison, from the ten farms without batteries; the conditioning, from the register.
* **Voices.** The investment director: "Our pilot proved what batteries add here; bank the pilot's number." The grid connections manager:
  "A connection is a connection; the battery doesn't care what the limit is."
* **Licensed wrong basis.** The term sheet records that the lenders' adviser screens regions on the time-weighted average price and will
  present that screen at credit committee.

## 8. Determinism by construction

* **Headroom.** Every pilot farm's export limit is either its solar rating or at least 40% above it, none in between.
* **Commissioning.** Only headroom farms' batteries were commissioned within the measured year; the three without headroom ran it whole.
* **Counterfactual.** Each farm's same-year revenue without its battery is its own solar output at the interval prices, with no
  curtailment either way.
* **Rounding.** The answer is 64.0, mid-bin.

## 9. Prompt sketch and deliverables

> The project reaches financial close on 30 September, and our investment director wants the pilot's number in the base case. Tell me the
> value per MWh of solar output we commit, in A$ to one decimal, as the line in the lenders' base case. Send `base_case_value.xlsx`, a
> chart `uplift_by_connection.png`, and a one-page `close_note.pdf`.

* `base_case_value.xlsx` — the value under each rung, the curtailment sheet (ask A), the availability sheet (ask B) and the pilot table
  (ask C).
* `uplift_by_connection.png` — each pilot farm's same-year uplift against its export headroom as points, the pooled uplift as a line, the
  year-on-year measures as hollow points, the project's headroom marked, and the committed value annotated.
* `close_note.pdf` — the committed value and why the pilot's pooled number does not carry to the project.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 24 farms, network curtailment as a share of potential output last year.
  *Device:* the market's unconstrained-output estimates are revised once after settlement, and the revision file supersedes the first
  estimate; using the first overstates curtailment at six farms.
* **Ask B (device-carried).** For each farm, inverter availability last year. *Device:* planned maintenance outages carry a planned flag
  and are excluded from availability under the maintenance contract; counting them understates availability at five farms.
* **Ask C (validity).** The value under each of the four rungs, and each pilot farm's same-year uplift with its export headroom.
* **Decoupling.** Clearing the headroom conditioning changes no figure in asks A or B.

## 11. Rubric arithmetic

24 farms (ask A) + 24 farms (ask B) + 4 rung values and 14 farm uplifts (ask C) + the committed value, the project's uplift and the solar
price + 5 named chart parts + 3 files ≈ 77 criteria.

## 12. World-building constraints

* Prices over the two years: generation-weighted 54.0, time-weighted 88.0; farms without batteries lost 8.5 a MWh between the years.
* Pilot uplift (same year): eleven headroom farms 35 to 41, mean 38.0 (35.0 with commissioning months); three without headroom 9 to 11,
  mean 10.0; pooled 32.0 (29.6 with commissioning months).
* Rung values 75.1 / 83.6 / 86.0 / 64.0; partial cells 80.0 (connection voltage) and 55.5 (headroom, year on year). P-04 and P-11 match
  on every pilot column.
* Revision files and planned-outage flags never touch a revenue, a battery flow or an export limit.

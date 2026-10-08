# DS20 — Which terminal gets the port's flood wall, when most hours lost with water on the quay would have been lost to the storm anyway

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Supply Chain & Logistics · port operations and resilience investment |
| Mirrors | Placing resilience spend where an outage is avoidable rather than merely recorded (Amazon fulfilment-centre flood protection, cloud region resilience upgrades where grid outages coincide with the storms that cause them, airline hub de-icing capacity) |
| Decision shape | Which of N gets one scarce thing: the single permanent flood wall in this capital cycle |
| Committed call | The terminal that gets the wall, and the revenue loss it avoids a year, in $ thousands to the nearest ten |
| Gap · Pattern | Gap 3 (objective) over Gap 2 (population) · S10, the governing verb is causal so the baseline is constructed from the harbour master's closures and each terminal's own wind stops, with a suppressed revenue cell bounded by the published total (#24) at rung 2 |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #24 treats an unpublished figure as unknown · #7 uses the ready-made measure · #2 counts file rows instead of the real unit · #15 follows the requester's hunch over the rule |
| Calibration form | Retry or revision log: the harbour master's berth-window revision log for five years, with every port closure's start and end, checked against the 14 surge days when the liquid-bulk terminal's demountable barrier held |
| Driving force | The capital plan funds the wall where it avoids the most lost revenue. The operations log and the quay sensors show every hour a terminal stood suspended with water on its quay, but on those days the harbour master also closes the port to vessel movements, and cranes and loading arms stop for wind, so much of that loss would have happened behind any wall. No record says why a terminal stood idle. Only the hours outside the union of port closures and the terminal's own wind stops are avoidable, and the union is a construction across two logs that the barrier days reproduce exactly. Container and reefer cranes stop on the same storms that flood them; the low ro-ro quay floods through whole tide cycles after the port reopens. |

## 1. Situation

A port authority can build one permanent flood wall this capital cycle, at one of six terminals: two container terminals (four and two
berths), a reefer terminal, a single-tenant dry-bulk terminal, a one-berth ro-ro terminal and a liquid-bulk terminal that already deploys a
demountable barrier. The capital plan funds the wall where it avoids the most lost revenue a year. The port holds five years of surge-day
operations logs (each berth's suspension intervals), each quay's water-sensor record, the harbour master's berth-window revision log, the
crane and loading-arm anemometer logs, and its annual statistical report, which publishes revenue and operating hours by terminal but
suppresses the dry-bulk tenant's revenue. The chief operating officer
wants the wall at the biggest container terminal.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct and no stakeholder read is overturned. That covers the operations log's suspensions, the quay
  sensors' wet intervals, the revision log, the anemometer logs and the statistical report. The difficulty is that the plan's verb is "avoids",
  and the records count hours lost, not hours a wall would have saved.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the chief operating officer's view. Wet-quay suspended hours valued at each terminal's revenue rate still put a
  container or reefer terminal first, and every figure ties to its log.
* **Instrument repair.** The suspect file is the statistical report, which suppresses dry bulk's revenue. Published, it moves rung 1 to
  reefer (rung 2's pick) and leaves rung 0 at Container North and rung 2 at reefer; no lower rung names the ro-ro. No other file is
  suspect: the operations log records suspensions and the quay sensors record water, both complete, and neither claims why a terminal
  stood idle. A perfect sensor on every quay and every berth leaves the closures and wind stops where they were, so the union is still
  needed for the ro-ro's $980k.
* **Lens swap.** The naive read values every wet-quay suspended hour. The answer values only the hours outside the closure and wind-stop union, a
  different population of hours that differs by terminal.

## 3. The driving force

A strong solver values each terminal's suspended hours with water on its quay at its revenue rate. It converts berth-hours to
terminal-hours, because the statistical report's rates are per terminal operating hour, and it bounds the dry-bulk tenant's suppressed revenue from the published total
and the other terminals' rounded cells, instead of taking the port average. Each step is competent, and the reefer terminal leads at
$2.10M a year. But the plan's verb is causal. On every surge day the harbour master closes the port to vessel movements for part of the
storm, and the container and reefer cranes stop at their wind limit. A terminal that cannot work a ship for those reasons loses those hours
behind any wall. The revision log gives each closure's start and end, and the anemometer logs give each terminal's wind stops. Avoidable
hours are the wet-quay suspended hours outside their union. Only a quarter of the reefer terminal's hours fall outside it. The ro-ro
quay is the port's lowest, floods through whole tide cycles after the port reopens, and its ramps never reach their wind limit on a surge day, so 87.5%
of its hours are avoidable.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Wet-quay suspended berth-hours a year × the terminal's revenue rate, the suppressed dry-bulk rate replaced by the port average ($15k) | A, Container North ($5.40M) | The operations log and the published rates, as the plan's verb seems to ask | The statistical report's rates are per terminal operating hour, and Container North's four berths log one suspension four times |
| 1 | Terminal-hours (union across berths), dry bulk still at the port average | D, Dry Bulk ($2.55M) | The right unit, every terminal valued | The statistical report: the published total less the other terminals' rounded cells bounds dry bulk's rate at $4.6–5.4k an hour (#24) |
| 2 | Terminal-hours at bounded rates | C, Reefer ($2.10M) | Every hour and rate now ties to a source | The revision log and the anemometer logs: most reefer hours fall inside a port closure or its own crane wind stops |
| 3 | **Decisive:** avoidable terminal-hours (wet-quay suspended hours outside the union of port closures and the terminal's own wind stops), at bounded rates | **E, Ro-ro ($980k)** (5th of 6 on rung 0) | — | — |

* **Position table.** Ro-ro is 5th on rung 0 ($1.12M), 5th on rung 1 and 4th on rung 2, and leads only rung 3, 1.36× over dry bulk
  ($722k). Rung margins: 1.38, 1.21, 1.31, 1.36.
* **Discriminator dominance.** Reefer carries a 1.88× advantage into rung 3 ($2.10M against $1.12M). On the decisive axis, the avoidable
  share, ro-ro sits at 0.875 and reefer at 0.25, an edge of 3.5. Product: 3.5 / 1.88 = 1.87, ro-ro's final margin over reefer ($980k
  against $525k). The edge is 1.56× the 2.25 it needs (1.2 × the carried 1.88).
* **Partial correction priced (L3).** Netting port closures only names reefer ($1.22M, 1.24× over ro-ro). Netting wind stops only names
  reefer ($1.37M, 1.22× over ro-ro's $1.12M). Applying the barrier terminal's measured share (0.5) to every terminal names reefer ($1.05M,
  1.88× over ro-ro). Doing the full netting with dry bulk at the port average names dry bulk ($2.17M, 2.21×), and doing it on berth-hours
  names Container North ($1.62M, 1.65×). No half lands on ro-ro.
* **Grid.** Hours (berth, terminal) × dry-bulk rate (port average, bounded) × netting (none, closures, wind stops, union) gives 16 cells.
  Container North, dry bulk and reefer take the other fifteen; only terminal-hours, the bounded rate and the union name ro-ro. Its nearest
  wrong cells are its one-toggle neighbours: wind stops only (reefer, 1.22×), closures only (reefer, 1.24×) and the port-average rate
  (dry bulk, 2.21×).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The plan says "avoids". The operations log records suspensions and the quay sensors record water; no record says why a terminal
   stood idle. No document says a closed port or a stopped crane loses the hour anyway.
2. **The reproducing rule is a construction, not a menu.** On the 14 surge days the liquid-bulk barrier held, its quay stayed dry and it
   still lost hours. The union of port closures and its own loading-arm wind stops reproduces those hours on 14 of 14 days. Closures
   alone reproduce 5, and wind stops alone 3, both short. The union is an interval construction across two logs joined by date and time,
   with no parameter to scan.
3. **No arithmetic symptom.** Coded hours reconcile to the operations log, revisions to the harbour master's record, and rates to the
   statistical report under every rung.
4. **Not a row predicate.** It needs each surge day's closure intervals, each terminal's wind-stop intervals, their union, and the wet-quay
   suspension intervals with that union removed, summed and valued.
5. **The enumeration is arithmetic.** No column marks an hour as avoidable; the ro-ro's 70 hours a year fall out of the interval arithmetic.
6. **No cutover date.** Surges, closures and wind stops recur every winter, and nothing steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The harbour master's revision log: every berth-window revision for five years, each with a timestamp and reason, including
  every port closure's start and end. It is read against the liquid-bulk terminal's 14 barrier days, when water stayed off its quay.
* **What it certifies.** Hours lost behind a dry quay equal the union of closures and the terminal's own wind stops (14 of 14 days).
* **What it is blind to.** The ro-ro's own counterfactual. *In every surge day on file the ro-ro quay flooded, because it is the lowest in
  the port*, so its avoidable share has to be built from the union, not read from its record.
* **Twin pair.** Barrier days 4 and 11 are identical on every visible column: a 1.9 m surge peak, a 27 m/s gust peak, the barrier up for
  nine hours. The terminal lost 8 and 4 hours (2.0×). Only the union separates them: on day 11 the port closure fell inside the
  loading-arm wind stop, and on day 4 it followed it.
* **Every rule exercised.** Closures longer than wind stops, wind stops longer than closures, and days with neither all occur, so both arms
  of the union are tested.
* **Resemblance points at the decoy.** On the operations log the ro-ro looks like the barrier terminal (one berth, short wet-quay
  suspensions), which every valuation of wet-quay hours ranks low.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The capital plan: the wall goes where it avoids the most lost revenue a year. The statistical report's revenue per
  terminal operating hour is the valuation rate. The five complete winters on file are the window. One sentence each.
* **Empirical pins.** The union rule, from the barrier days.
* **Voices.** The chief operating officer: "Container North moves the most boxes; protect it first." The reefer tenant: "Our power rooms
  flood every winter." The harbour master: "The port closes when it must; that is a safety call, not a flood call."
* **Licensed wrong basis.** The capital plan records that the board's audit committee compares terminals on wet-quay suspended hours from the
  operations log and will see that basis.

## 8. Determinism by construction

* **Intervals.** Closures, wind stops and suspensions are stamped to the minute, and no stamp falls within five minutes of another
  interval's edge, so open and closed interval conventions agree.
* **Unit.** A terminal hour is suspended when any of its berths is suspended, as the statistical report defines operating hours.
* **Bound.** Dry bulk's rate is bounded at $4.6–5.4k an hour, and every value in the bound leaves it second on rung 3 and fifth on rung 2.
* **Window.** Five complete winters, averaged per year, with no partial season.
* **Rounding.** Ro-ro's figure is exact (70 avoidable hours a year at $14k) and filed to the nearest ten thousand dollars.

## 9. Prompt sketch and deliverables

> We can build one permanent flood wall this cycle. Our chief operating officer wants it at Container North, since it moves the most boxes.
> Tell me which terminal gets the wall and how much lost revenue it saves us a year, in thousands of dollars to the nearest ten, in a line
> for the capital committee. Send `wall_case.xlsx`, a chart `surge_day_hours.png`, and a one-page `capital_note.pdf`.

* `wall_case.xlsx` — the six terminals under each rung, the turnaround sheet (ask A), the carrier sheet (ask B) and the reproduction sheet
  (ask C).
* `surge_day_hours.png` — for each terminal, a stacked bar of wet-quay suspended hours split into port closure, own wind stop and avoidable, with
  the chosen terminal marked, plus a timeline panel of barrier days 4 and 11 showing closure, wind stop and lost hours.
* `capital_note.pdf` — the committed terminal and figure, and why the reefer and container terminals lose.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each terminal, last year's mean hours at berth per vessel call. *Device:* a vessel that
  shifts berth mid-call gets a new call row under the same voyage number, as the port community system documents. Counting rows as calls
  understates turnaround at the three terminals that shift vessels.
* **Ask B (device-carried).** For each terminal and quarter, the number of distinct shipping lines with cargo on calling vessels.
  *Device:* in vessel-sharing alliances the call row carries the operating carrier, and the slot owners sit in a separate allocation
  table. Counting operating carriers undercounts the container terminals by a third.
* **Ask C (validity).** Each terminal's figure under the four netting rules on both hour grains, and each rule's hits on the 14 barrier
  days.
* **Decoupling.** Clearing the union and the bound changes no figure in asks A or B. Call rows and slot allocations never enter a
  suspension, a closure or a rate.

## 11. Rubric arithmetic

6 terminals × 4 rungs + 6 terminals × 4 netting rules (ask C) + 3 rules' barrier-day hits + 6 turnaround figures (ask A) + 6 × 4
quarterly carrier counts (ask B) + the committed terminal, its figure and the runner-up + 6 named chart parts + 3 files ≈ 96 criteria.

## 12. World-building constraints

* Wet-quay suspended hours a year, berth / terminal: Container North 300 / 80, Container South 170 / 100, Reefer 130 / 70, Dry Bulk 250 / 170,
  Ro-ro 80 / 80, Liquid Bulk 40 / 40. Rates ($k an hour): 18, 16, 30, 5 (suppressed; port average 15), 14, 12.
* Avoidable shares (union / closures only / wind only): 0.30 / 0.55 / 0.45, 0.32 / 0.58 / 0.47, 0.25 / 0.58 / 0.65, 0.85 / 0.85 / 1.0,
  0.875 / 0.875 / 1.0, 0.50 / 0.60 / 0.80.
* Rung leaders A, D, C, E at $5.40M, $2.55M, $2.10M and $980k. The union reproduces 14 of 14 barrier days, closures 5, wind stops 3.
  Barrier days 4 and 11 are identical on every visible column.
* Call rows and slot allocations never touch suspensions, closures, wind stops or rates.

# AD07 — Which airport gets the one mobile screening team for the summer, when the team can only open lanes where a lane position stands idle

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Supply Chain & Logistics · aviation passenger screening operations |
| Mirrors | Placing a scarce flexible crew where it can actually add capacity, when the bottleneck is fixed positions rather than staff (pop-up pick crews in Amazon fulfilment centres where stations are all occupied at peak, surge support agents at cloud providers limited by seat licences, extra checkout staff in big-box retail limited by open tills) |
| Decision shape | Which of N gets one scarce thing: the agency's single mobile screening team for the summer peak |
| Committed call | The one airport the team works from 15 June to 31 August 2027 |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · a binding limit applied in the figure (E14): the team's three lanes fit only into lane positions idle in each checkpoint-hour, so the passengers it moves are a sum of hourly minimums, never the excess; the deciding comparison (E22) at the rung below |
| Gate G mechanism | binding_constraint, with decomposition_attribution |
| Measured traps engaged | #10 notes a binding limit as a risk · #20 leaves the deciding comparison unstated · #7 uses the ready-made measure |
| Calibration form | Existing-book actuals: the after-action book of last summer's 15 deployment-weeks, each with the passengers moved within the standard |
| Driving force | The team brings twelve officers, enough for three lanes, but no lane positions: it can open a lane only where a position stands idle in that hour. C's excess sits 85% in hours when every position is already staffed, so the team could move little of it; E is short of officers, not positions, and its bank hours have room for all three lanes. The passengers moved are a sum over checkpoint-hours of the smaller of the excess and the lanes that fit, a limit the lane register and the roster plan define only hour by hour, and the after-action book reproduces nothing else. |

## 1. Situation

A national screening agency has one mobile team for the summer peak and places it at one of eight airports that its throughput detector
flagged this spring. The deployment policy judges the team by the passengers it moves through screening within the 20-minute standard who
would otherwise have waited longer. The pack carries the detector's flags, last summer's queue-sensor records (every passenger's queue
entry and lane exit, by checkpoint), the lane register (each checkpoint's lane positions, rated capacity and this spring's new lanes),
last summer's roster and this summer's roster plan (lanes staffed per checkpoint-hour), and the after-action book.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the detector's aligned growth, every passenger's wait, the lane register, both rosters and the
  after-action actuals. The detector is labelled as describing spring throughput. Nothing reported is overturned and no stakeholder read
  is corrected; the difficulty is that the team's help is limited hour by hour by positions no excess figure sees.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the detector export. Excess passengers net of the new lanes, the natural careful build from
  the queue sensors, still names C.
* **Instrument repair.** No file the ladder uses is suspect: the queue sensors record every passenger's entry and exit, the lane register
  every position and its rated capacity, last summer's roster every staffed lane, and this summer's roster plan is the plan of record for
  the hours the team would work. No field records where the team could open a lane, so perfect files leave rung 0 at A (+14.2%), rung 1 at B
  (24.1%) and rung 2 at C (61,000), and the hour-by-hour position limit is still needed for E. The after-action book records every
  deployment made; an airport-week without the team has no moves to fill.
* **Lens swap.** The naive population is every passenger who waited over 20 minutes; the answer's is the passengers in checkpoint-hours
  where a lane position stood idle, up to what three lanes can screen: a different population, under a sixth of C's excess.

## 3. The driving force

A strong solver sees that spring growth is not summer waiting, counts last summer's passengers who waited over 20 minutes from the queue
sensors, notices that one airport opened five lanes this spring, nets the passengers those lanes absorb, and names C with 61,000. Every
step is competent, and the deciding comparison, excess against new capacity, is stated. But the team brings officers, not lanes, and a
lane needs a position. C's checkpoints run every position in the morning bank and at midday, the hours that hold 85% of its excess; the
team could work only its quiet hours. E's airport cannot recruit, so its positions stand half empty through the 05:00–08:00 bank, where
81% of its excess sits. Each checkpoint-hour gives the team the smaller of its net excess and what three lanes, or as many as fit in the
idle positions, can screen at 150 an hour. Summed per airport, that limit leaves C 9,150 passengers and E 38,500. The register and the
roster plan define it only hour by hour; a daily total of idle positions shows plenty of room at C.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The detector: spring throughput growth against the holiday-aligned baseline | A (+14.2%) | The agency's own anomaly screen, calendar-aligned, and growth is what breaks a checkpoint | The after-action book: last summer's realised moves bear no relation to spring growth at the six airports deployed |
| 1 | Share of last summer's peak passengers who waited over 20 minutes | B (24.1%) | The direct measure of waiting, every passenger counted | The lane register: B commissioned five lanes this spring, enough to absorb 70% of its excess |
| 2 | The deciding comparison: last summer's excess passengers net of what this spring's new lanes absorb | C (61,000) | Demand against capacity as one comparison, every input on file | The roster plan against the lane register: every position at C is staffed in the bank and at midday, the hours holding 85% of its excess |
| 3 | **Decisive:** per checkpoint-hour, the smaller of the net excess and what the team's lanes screen in the positions left idle by the roster plan, summed per airport | **E (38,500)** (5th of 8 on rung 0) | — | — |

* **Position table.** E ranks 5th on rung 0 (+6.4%), 4th on rung 1 (14.0%) and 3rd on rung 2 (41,000), and leads only rung 3, 1.88× D
  (20,500). Intermediate leaders hold margins of 1.23×, 1.24× and 1.27×.
* **Discriminator dominance.** C carries a 1.49× advantage over E into rung 3 (61,000 against 41,000). The hourly position limit keeps
  0.94 of E's excess and 0.15 of C's, an edge of 6.26 against the 1.2 × 1.49 = 1.79 required, 3.51× headroom.
* **Partial correction priced (L3).** A solver who applies the position limit to the day's idle position-hours instead of hour by hour
  finds room at C in its quiet hours and names C (58,000 against E's 39,000, 1.49×). A solver who caps by the team's three lanes but
  ignores positions names C again (61,000, 1.56× E). A solver who takes idle positions from last summer's roster instead of this summer's
  plan names D (46,500 against E's 38,500, 1.21×), because D hired screeners this spring and fills its bank. No half lands on E.
* **Grid.** Limit (none, team lanes only, positions by day, positions by hour) × roster (last summer's or this summer's plan) gives eight
  cells. Every cell without the hourly position limit names C; hourly positions on last summer's roster name D. Only hourly positions on
  this summer's plan name E, and the nearest wrong cell (D) needs only the old roster.
* **The deciding comparison (#20).** E's 38,500 passengers moved against C's 9,150 is the comparison the deployment order has to state;
  neither the excess nor the idle positions compute it alone.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy counts passengers moved; the register lists positions and the plan lists staffed lanes. Nothing says
   the team needs an idle position or that the limit binds by the hour.
2. **The corpus pins a construction, not a menu.** The hourly position limit reproduces all 15 deployment-weeks within 3%; uncapped net
   excess reproduces 6 and the daily limit 9, and both over-predict every week at a position-bound checkpoint, so each also overstates the
   book's total (by 41% and 17%). The limit is a construction: idle positions per checkpoint-hour, a minimum per hour and a sum, and no
   column holds a move.
3. **No arithmetic symptom.** Waits tie to the sensors, lanes to the register, and every daily total reconciles under every reading.
4. **Not a row predicate.** It needs the roster plan subtracted from the register's positions per checkpoint-hour, a minimum against that
   hour's net excess, and a sum; the minimum does not commute with the daily totals.
5. **The enumeration is arithmetic.** Which passengers the team moves is computed hour by hour; no field carries it.
6. **No cutover date.** The bank's shape repeats daily all summer; the only dated items, the spring lane openings, sit in the rungs below.
7. **Survives deletion.** With every voice and the detector removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The after-action book: last summer's three mobile teams over 15 deployment-weeks at six of the eight airports, each week with
  the passengers moved within the standard as the agency's operations analysts recorded them, beside that week's roster.
* **What it pins.** The hourly position limit, 15 of 15 within 3%; uncapped net excess 6 of 15; the daily limit 9 of 15.
* **Twin pair.** Deployment-weeks W-07 and W-11 are identical on net excess (6,200 passengers), throughput, lanes staffed per day and team
  size. The book records 5,840 and 2,790 passengers moved (2.09×): W-07's bank hours had idle positions, and W-11's checkpoint was full
  through its bank.
* **Every rule exercised.** Two weeks include hours where the team's three lanes, not the positions, bound; one week straddles a new lane's
  commissioning, so the netting is tested.
* **Resemblance points at the decoy.** C's excess profile most resembles W-07, the book's best week.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The deployment policy: the team goes where it will move the most passengers through screening within the 20-minute
  standard who would otherwise have waited longer. The summer peak runs from 15 June to 31 August. Lanes commissioned before the peak are
  in service for it at the register's rated capacity.
* **Empirical pins.** The hourly position limit, from the after-action book.
* **Voices.** The regional director: "Growth is what breaks a checkpoint; follow the detector." The general manager at B: "Our queues have
  been the worst in the region two summers running."
* **Licensed wrong basis.** The policy records that the airports' joint operations council ranks airports on excess passengers net of new
  lanes and will present that ranking at the planning session.

## 8. Determinism by construction

* **Capacity.** Every lane screens 150 passengers an hour at the register's rating, the team's and the airport's alike.
* **Forecast.** Last summer's hourly excess, net of the new lanes, is the basis; the median of the last two summers gives the same order.
* **Positions.** Every position belongs to one checkpoint, and the roster plan staffs whole lanes by the hour.
* **Threshold.** 15- and 25-minute standards keep E first by at least 1.6×.

## 9. Prompt sketch and deliverables

> We have one mobile screening team for the summer peak, and it has to go to one airport. The regional director would follow the spring
> detector. Name the airport in one sentence for the deployment order, and send `summer_deployment.xlsx` with the sheets below, the chart
> `idle_positions.png`, and a one-page `deployment_order.pdf`.

* `summer_deployment.xlsx` — the airport build, the interceptions sheet (ask A), the overtime sheet (ask B) and the book reproduction (ask C).
* `idle_positions.png` — for each airport, net excess passengers by hour of day against the team's screenable capacity in idle positions,
  the morning bank shaded, the passengers moved filled, and the chosen airport highlighted.
* `deployment_order.pdf` — the committed airport and the deciding comparison against C.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each airport, last summer's prohibited-item interceptions per 10,000 passengers and the share
  found at PreCheck lanes. *Device:* the interception log writes one row per item, and a bag holding several items produces several rows
  under one bag-check ID, as the incident guide documents. Counting rows overstates interceptions at the three airports with the most
  multi-item bags. The deployment build never touches the interception log.
* **Ask B (device-carried).** For each airport, officer overtime hours in June, July and August. *Device:* overtime on a shift that crosses
  midnight is booked to the shift's start date, per the timekeeping guide. Assigning hours by their clock time moves month-end night shifts
  into the wrong month at the five airports with overnight checkpoints.
* **Ask C (validity).** For each of the four rung constructions, the deployment-weeks it reproduces within 5% out of 15.
* **Decoupling.** Clearing the hourly position limit changes no figure in asks A or B.

## 11. Rubric arithmetic

8 airports × 2 (ask A) + 8 airports × 3 months (ask B) + 4 constructions (ask C) + the committed airport, its passengers moved and the
deciding comparison against C + 5 named chart parts + 3 files ≈ 55 criteria.

## 12. World-building constraints

* Rung leaders are A, B, C, E. E is 5th / 4th / 3rd / 1st; intermediate margins are at least 1.23×; E leads rung 3 by 1.88×.
* Rung 2: C 61,000, D 48,000, E 41,000, B 30,000. Rung 3: E 38,500, D 20,500, F 17,000, C 9,150. Daily limit: C 58,000. Last summer's
  roster: D 46,500.
* C's positions are all staffed in the bank and 11:00–14:00, the hours holding 85% of its excess. E's bank runs with half its positions idle,
  and 81% of its excess sits in the bank. B's five spring lanes absorb 70% of its excess and fill its idle positions.
* The book holds 15 deployment-weeks at six airports; W-07 and W-11 are identical on every week-level column.
* Interception rows and overtime bookings never touch the queue sensors, the register or the rosters.

# RC07 — How much of January's tripled imbalance bill the plant trips caused, filed for the board's outage-cover decision

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Economics · electricity market risk |
| Mirrors | Cost-spike attribution in scarcity-priced markets settled per interval (EC2 spot interruptions billed per hour, ride-hail surge cost per pricing window, spot freight rate spikes per booking period), where an event's size is right and its share of each settlement interval is what decides which cause takes the interval |
| Decision shape | One figure committed at a date (a component): January's trip-attributable imbalance cost, filed at the board on the 10th |
| Committed call | The supplier's January imbalance cost attributable to unplanned generation trips, in pounds to the nearest £10,000 |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · E15 (the quiet second trap: past the loud wind decoy and the feed's own traps, each class's contribution is energy within the settlement period, so a trip that begins late in a period loses that period, its most expensive, to the wind error), pinned through the subsample, with E21 (a saturated measure broken by the lowest value consistent with every file) at rung 1 and derate continuations matched through each asset's message history at rung 2 |
| Gate G mechanism | decomposition_attribution, with confirm_surface_read support |
| Measured traps engaged | #11 beats the headline trap, misses the quiet one · #3 stops at a close but inexact match · #1 reports a failed back-test, ships anyway |
| Calibration form | Gold-standard verification subsample: 40 spike periods investigated by hand by the risk team, each labelled with its verified driver |
| Driving force | The risk policy gives each spike period's whole cost to the class with the largest contribution to the system imbalance in that period. Event-level builds credit a trip with its full MW in every period it touches. The imbalance is settled per half hour, as energy: a unit that trips in the last minutes of a period removes its MW for those minutes only, and in that period the half hour's wind forecast error is larger. That first period is the trip's most expensive, because reserves have not yet responded. Only each class's energy within the period, from each unit's metered output against its notified output minute by minute, reproduces the risk team's 40 verified labels. |

## 1. Situation

A mid-sized electricity supplier's January imbalance bill was £4.8M, three times a normal winter month, across 212 settlement periods priced at £300/MWh
or more. The trading desk blames low wind; operations points to a cluster of plant trips during the cold snap. On the 10th the board decides whether to
buy outage cover for next winter, a product that pays when large units trip, and the CFO must file January's trip-attributable cost as the reference
figure. The supplier's risk policy sets how a period's cost is attributed. The risk team investigated a random 40 of the spike periods by hand.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: system prices, the supplier's imbalance volumes, the wind and demand forecasts and outturns, the outage
  feed, metered unit output, notified output and the 40 verified labels. Operations is right that trips drove many spikes, and the desk's wind
  story fails on evidence the solver will find. Nothing reported is overturned; the figure is the size of the component operations named.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the desk's view, operations' view and the licensed basis. The policy's rule applied to a clean event list still
  credits every trip with its full MW in the period it began.
* **Instrument repair.** Suspect file: the outage feed, which carries superseded versions under one event id, files a derate overrun as a new
  unplanned event and declares full registered capacity for trips from part load. Repaired so that each event appears once, overruns as
  continuations and every trip at the MW it removed, rung 0 returns £1.94M, as rungs 1 and 2 then also do; none returns £1.40M. The answer
  still needs each class's energy within the settlement period: a trip's MW, however exact, is a rate, and the policy compares contributions
  to the half hour's imbalance, so a trip in a period's last minutes loses that period to the wind error.
* **Lens swap.** The naive figure credits each trip with its full MW in every period it touches; the answer credits it with the energy it
  removed within each half hour, a different set of periods won by trips.

## 3. The driving force

A strong solver aligns every spike period with the forecast errors and outage events active in it, beats the desk's wind story at once, and
attributes each period by the policy's largest-contribution rule, one version per event. It notices that most trip messages declare the unit's
whole registered capacity, a saturated value, and replaces it with the unit's metered output before the event. It finds that when a planned
derate overran in the cold snap the feed recorded a new unplanned event at the minute the planned one ended, under a trip's reason code, and
that such an event removed nothing. That build is clean, every event a genuine trip at the MW it removed, and it still misses four of the risk
team's 40 verified labels. Each miss is a period in which a trip began in its last minutes. The imbalance is settled per half hour, as energy:
a unit that trips at minute 25 removes its MW for five minutes of that period, and the half hour's wind forecast error is larger. That first
period is the trip's most expensive, because reserves have not yet responded and the price spikes. Measured as energy within each period, from
each unit's metered output against its notified output minute by minute, 23 spike periods move from trips to wind or demand, and the
trip-attributable cost is £1.40M.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The policy's rule (each spike period's cost to the class with the largest contribution), latest version per event, unplanned events active in the period at their declared MW | £3.05M (+118%) | Event-level attribution exactly as the policy states, every event counted once, and it overturns the desk's wind story | Metering: 31 of 44 trip messages declare full registered capacity, and 18 of those units were producing less before the event |
| 1 | MW removed = the lower of declared unavailability and metered output in the period before the event | £2.48M (+77%) | The saturation is broken by the only value consistent with both files | The asset message histories: 14 unplanned events start at the minute a planned derate on the same asset ended |
| 2 | Unplanned events that start at the minute a planned event for the same asset ends are continuations and contribute no MW | £1.94M (+39%) | Every event is now a genuine trip at the MW it removed | The subsample: 36 of 40 verified labels reproduce, and the four misses are periods in which a trip began in the last ten minutes, each verified as wind- or demand-driven |
| 3 | **Decisive:** each class's contribution as energy within the settlement period, trips from metered output against notified output minute by minute | **£1.40M** | — | — |

* **Figure shape.** Every correction walks the figure down (−19%, −22%, −28% per step), and the answer is the minimum cell of the grid, so every
  partial application overstates the trip cost the board will reference.
* **Partial correction priced (L3).** A solver who jumps from rung 0 straight to energy within the period, keeping declared MW and the overruns,
  lands at £2.20M (+57%), further from the answer than rung 2. One who sees that a trip's first period matters but hands every first period to
  the next class, whatever minute the trip began, lands at £0.80M (−43%).
* **Grid.** Versions (rows as filed, latest) × de-saturation × continuation × energy within the period gives sixteen cells, from £3.62M down to
  £1.40M. Every instantaneous-MW cell lies at £1.94M or above; the nearest wrong cell is £1.66M (+19%), the full build made on duplicated rows.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The market rules say an overrun is published as unplanned; the policy says a trip contributes the MW it removed and
   compares contributions "in that period". No document says a contribution is energy over the half hour, or that a trip's first period
   carries only its minutes.
2. **The corpus pins a construction, not a menu.** The energy build reproduces 40 of 40 verified labels; the best rival (rung 2) 36, rung 1 33,
   rung 0 30, rows as filed 27. Every rival over-labels trips, so each also overstates the subsample's verified trip cost. The build integrates
   each unit's metered output against its notified output within each half hour, a construction across two files, not a parameter.
3. **No arithmetic symptom.** Event ids are unique after de-duplication and periods tie to the bill. No build's contributions sum to the
   period's imbalance volume, because interconnector ramps, embedded generation and the system operator's own actions sit outside every class
   and leave a residual of up to 300 MWh in every spike period, so no reconciliation singles out a trip's first period.
4. **Not a row predicate.** A trip's contribution to a period is a sum over the minutes it overlapped the half hour, joining the unit's minute
   metering to its notified output, and the period's class follows only from comparing it with the half hour's forecast errors.
5. **The enumeration is arithmetic.** No column marks the periods a trip loses to the wind error; 23 spike periods change class.
6. **No cutover date.** Trips begin at every minute of the cold snap's periods; the dated event in the month (a wind lull on the 8th) is the
   desk's decoy.
7. **Survives deletion.** With every voice removed, rung 2's clean build still files £1.94M.

## 6. The calibration corpus

* **Form.** The risk team's gold-standard subsample: 40 spike periods drawn at random from the 212, each investigated against the system
  operator's incident reports and labelled with its verified driver (trip, wind, demand, interconnector), with the supplier's cost in each.
* **What it pins.** The energy build (above), and on the way the de-saturation and continuation rules. It also certifies the policy's
  largest-contribution rule against the desk's wind-first reading, which reproduces 19 of 40.
* **Twin pair.** 12 and 19 January carry identical spike counts, prices, wind and demand errors, and trips identical in units, MW and duration,
  none of them an overrun. The verified trip cost was £310,000 on the 12th and £150,000 on the 19th (2.07×): on the 12th the trips began in the
  first minutes of their periods, on the 19th in the last minutes, so each first period on the 19th went to the wind error. Only the energy
  build reproduces both days.
* **Every rule exercised.** The subsample holds a genuine trip at a station that also had a planned derate (so "any planned outage" fails), a
  full-capacity trip from part load (testing de-saturation), a trip that began in a period's last minutes (testing the energy rule) and a
  period whose largest contribution is demand.
* **Resemblance points at the decoy.** January's evening spikes match December's on price, wind error and time of day, and December's spikes
  were verified as wind-driven.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The risk policy: a spike period is one priced at £300/MWh or more; its whole cost goes to the class with the largest
  contribution to the system imbalance in that period; a trip contributes the MW it removed from the system. One sentence each.
* **Empirical pins.** De-saturation, the continuation rule and the energy build, all reproduced only through the subsample.
* **Voices.** The head of trading: "We were short wind all month; every spike lines up with a wind miss." The operations director: "Those
  were the coldest nights of the year, and plant fell over all week."
* **Licensed wrong basis.** The policy records that the outage-cover broker prices cover on the MW declared unavailable in the outage feed and
  will present January on that basis.

## 8. Determinism by construction

* **Window.** An event counts in a period if it is active in any minute of it; no event starts or ends within one minute of a period boundary.
* **Continuation match.** An overrun's start equals its planned predecessor's end to the minute; no genuine trip starts within 30 minutes of a
  planned end on the same asset.
* **MW removed.** Metered output in the settlement period before the event start; every trip has one. Within a period, a unit's shortfall is
  its notified output less its metered output, minute by minute.
* **Energy.** Wind and demand contributions are the half hour's forecast errors in MWh; a trip's is its minute shortfall summed over the half
  hour. No spike period has two contributions within 25 MWh under any build.
* **Rounding.** The figure is filed to the nearest £10,000 and sits mid-bin.

## 9. Prompt sketch and deliverables

> The board decides on the 10th whether we buy outage cover for next winter, and it wants to know how much of January's £4.8M imbalance bill the
> plant trips actually cost us. The desk is sure it was wind. Give me that figure to the nearest £10,000, as the line I file in the board paper.
> Send `trip_cost_case.xlsx`, a chart `spike_attribution.png` and a two-page `board_paper.pdf`.

* `trip_cost_case.xlsx` — the attribution build, the wind-farm sheet (ask A), the gas sheet (ask B) and the subsample reproduction (ask C).
* `spike_attribution.png` — January's spike periods as a timeline of daily cost bars split by attributed class, with the periods a trip loses
  to wind or demand marked, the 40 subsample periods ticked, 12 and 19 January annotated, and the committed figure as a labelled reference.
* `board_paper.pdf` — the committed figure, what it counts and what it excludes.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six contracted wind farms, January metered output, availability and curtailed MWh.
  *Device:* curtailment instructions are filed as accepted bids with negative volumes on the farm's balancing unit, as the balancing data's
  sign convention documents; reading the bid volumes as positive generation overstates output at the four farms behind the export constraint.
* **Ask B (device-carried).** For each January gas day, the supplier's shipper imbalance quantity and charge. *Device:* the gas day runs from
  05:00 to 05:00, as the network code documents; grouping by calendar day misplaces the overnight cold-snap swings and moves the worst day.
* **Ask C (validity).** For each of the four constructions and the rows as filed, verified labels reproduced out of 40 and the subsample's trip
  cost; and the twin days' trip cost under each.
* **Decoupling.** Clearing the energy build changes no figure in asks A or B; neither uses the outage feed, unit metering or notified output.

## 11. Rubric arithmetic

6 farms × 3 figures (ask A) + 31 gas days × 2 figures (ask B) + 5 constructions × 2 figures + 2 days × 5 constructions (ask C) + the committed
figure, the periods that change class and the runner-up construction's figure + 5 named chart parts + 3 files ≈ 120 criteria.

## 12. World-building constraints

* £4.8M across 212 spike periods; rung figures £3.05M / £2.48M / £1.94M / £1.40M, rows as filed £3.62M; energy cells £2.61M, £2.20M, £2.12M,
  £2.04M, £1.79M, £1.72M, £1.66M, £1.40M.
* 44 trip messages, 31 at full registered capacity, 18 of those from part load; 14 derate overruns, each starting at its planned predecessor's
  end to the minute.
* 23 spike periods in which a trip began change class under the energy build, carrying £540,000; first periods carry the month's highest prices.
* The subsample: 40 periods, 27 / 30 / 33 / 36 / 40 reproduced on rows as filed and rungs 0–3, wind-first 19.
* 12 and 19 January identical on every period-summary column and in their trips' units, MW and durations; the trips began in the first minutes
  of their periods on the 12th and in the last minutes on the 19th.
* Curtailment bids and gas-day boundaries touch no spike period's classification.

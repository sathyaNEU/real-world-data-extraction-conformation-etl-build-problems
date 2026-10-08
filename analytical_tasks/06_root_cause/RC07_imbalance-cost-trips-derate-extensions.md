# RC07 — How much of January's tripled imbalance bill the plant trips caused, filed for the board's outage-cover decision

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Economics · electricity market risk |
| Mirrors | Cost-spike attribution in scarcity-priced markets (EC2 spot interruptions, ride-hail surge cost, spot freight rate spikes in retail supply chains), where the event feed is correct and part of its "unplanned" events are continuations of known ones |
| Decision shape | One figure committed at a date (a component): January's trip-attributable imbalance cost, filed at the board on the 10th |
| Committed call | The supplier's January imbalance cost attributable to unplanned generation trips, in pounds to the nearest £10,000 |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · E15 (the quiet second trap: derate extensions filed as unplanned), with E21 (a saturated measure broken by the lowest value consistent with every file) at rung 2 and Pattern B pinning the classification |
| Gate G mechanism | decomposition_attribution, with confirm_surface_read support |
| Measured traps engaged | #11 beats the headline trap, misses the quiet one · #19 breaks a big tie instead of questioning it · #1 reports a failed back-test, ships anyway |
| Calibration form | Gold-standard verification subsample: 40 spike periods investigated by hand by the risk team, each labelled with its verified driver |
| Driving force | The outage feed files a planned derating that overruns as a new "unplanned" event, with a fresh start time, under the same structured reason code as a genuine trip. A rule that counts unplanned events starting in the prior two hours credits those overruns with MW they never removed, because the derate was already in force. Only the asset's message history (an unplanned message starting at the minute a planned message for the same asset ended) separates them, and the risk team's verified subsample is the only record that reproduces under that separation. |

## 1. Situation

A mid-sized electricity supplier's January imbalance bill was £4.8M, three times a normal winter month, across 212 settlement periods priced at £300/MWh
or more. The trading desk blames low wind; operations points to a cluster of plant trips during the cold snap. On the 10th the board decides whether to
buy outage cover for next winter, a product that pays when large units trip, and the CFO must file January's trip-attributable cost as the reference
figure. The supplier's risk policy sets how a period's cost is attributed. The risk team investigated a random 40 of the spike periods by hand.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: system prices, the supplier's imbalance volumes, the wind and demand forecasts and outturns, the outage
  feed, metered unit output and the 40 verified labels. Operations is right that trips drove the spikes, and the desk's wind story fails on
  evidence the solver will find. Nothing reported is overturned; the figure is the size of the component operations named.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the desk's view, operations' view and the licensed basis. The policy's rule applied to the outage feed still
  credits overrunning derates as trips.
* **Instrument repair.** A perfect outage feed files the same messages: the market rules require an overrun to be published as an unplanned
  event from the moment it begins. Perfect metering changes nothing either. The difficulty is reading a correct event history, not completing it.
* **Lens swap.** The naive figure counts every unplanned event as MW lost at its start; the answer counts the MW each event actually removed,
  a different set of events and periods.

## 3. The driving force

A strong solver aligns every spike period with the forecast errors and outage events active in it, beats the desk's wind story at once, and
attributes each period by the policy's largest-contribution rule. It de-duplicates message versions. It also notices that most trip messages
declare the unit's whole registered capacity unavailable, a saturated value, and replaces it with the lowest MW consistent with both the feed
and metering: the unit's metered output before the event. That build is clean and passes the desk test, and it is still wrong. During the cold
snap several stations were running on planned deratings (one gas turbine of two out for maintenance). When a derate overran, the feed recorded a
new unplanned event starting at the minute the planned one ended, with the same reason code a trip carries. Metered output before that "event"
is the derated output, so the saturation fix does not touch it. The overrun removed nothing; the derate was already in force. Only the asset's
message history exposes it, and only the classification that drops such continuations reproduces the risk team's 40 verified labels.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The policy's rule (each spike period's cost to the class with the largest MW contribution), unplanned events starting in the prior two hours, feed rows as filed | £3.62M (+87%) | Event-level attribution exactly as the policy states, and it overturns the desk's wind story | The feed carries several versions of one event under one event id, and the rows sum them |
| 1 | Hygiene: latest version per event id | £3.05M (+57%) | Every event counted once, every period reconciled to the bill | Metering: 31 of 44 trip messages declare full registered capacity, and 18 of those units were producing less before the event |
| 2 | MW lost = the lower of declared unavailability and metered output in the period before the event | £2.48M (+28%) | The saturation is broken by the only value consistent with both files | The subsample: 34 of 40 verified labels reproduce; the six misses are periods whose "trip" is a derate overrun |
| 3 | **Decisive:** unplanned events that start at the minute a planned event for the same asset ends are continuations and contribute no MW | **£1.94M** | — | — |

* **Figure shape.** Every correction walks the figure down (−16%, −19%, −22% per step), and the answer is the minimum cell, so every partial
  application overstates the trip cost the board will reference.
* **Partial correction priced (L3).** A solver who suspects overruns but drops every unplanned event on an asset that had any planned outage in
  January also drops genuine trips at those stations and lands at £1.30M, 33% low, further from the answer than rung 2. The feed's reason field
  is a structured code shared by trips and overruns, with no free text, so no wording shortcut exists.
* **Grid.** De-duplication × de-saturation × continuation (eight cells): £3.62M, £3.05M, £2.94M, £2.83M, £2.48M, £2.39M, £2.30M and £1.94M.
  The nearest wrong cell is £2.30M (+18.6%), which needs the decisive move made on duplicated rows.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The market rules say an overrun is published as unplanned; the policy says a trip contributes the MW it removed. No
   document connects the two or says that an overrun removes nothing.
2. **The corpus pins a construction, not a menu.** The continuation rule reproduces 40 of 40 verified labels; the best rival (rung 2) 34, rung
   1 30, rung 0 27. Every rival over-labels trips, so each also overstates the subsample's verified trip cost, by 22% to 61%. The rule is a match
   across an asset's message history (an unplanned start equal to a planned end, same asset), not a parameter.
3. **No arithmetic symptom.** Event ids are unique after de-duplication, periods tie to the bill, metered output and declared MW are both
   consistent with every overrun.
4. **Not a row predicate.** Whether a message is a continuation depends on another message for the same asset, so each asset's history has to
   be ordered and matched.
5. **The enumeration is arithmetic.** No column marks a continuation; 14 overrun events are found by the match.
6. **No cutover date.** Overruns sit inside the cold snap alongside genuine trips; the dated event in the month (a wind lull on the 8th) is the
   desk's decoy.
7. **Survives deletion.** With every voice removed, rung 2's clean build still files £2.48M.

## 6. The calibration corpus

* **Form.** The risk team's gold-standard subsample: 40 spike periods drawn at random from the 212, each investigated against the system
  operator's incident reports and labelled with its verified driver (trip, wind, demand, interconnector), with the supplier's cost in each.
* **What it pins.** The continuation rule (above). It also certifies the policy's largest-contribution rule against the desk's wind-first
  reading, which reproduces 19 of 40.
* **Twin pair.** 12 and 19 January carry identical spike counts, prices, wind and demand errors and unplanned MW starting within two hours. The
  verified trip cost was £310,000 on the 12th and £150,000 on the 19th (2.07×), because half the 19th's unplanned MW were derate overruns. No
  rule that reads the feed row by row reproduces both days.
* **Every rule exercised.** The subsample holds a genuine trip at a station that also had a planned derate (so "any planned outage" fails), a
  full-capacity trip from part load (so de-saturation is tested) and a period whose largest contribution is demand.
* **Resemblance points at the decoy.** January's evening spikes match December's on price, wind error and time of day, and December's spikes
  were verified as wind-driven.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The risk policy: a spike period is one priced at £300/MWh or more; its whole cost goes to the class with the largest MW
  contribution to the system imbalance in that period; a trip contributes the MW it removed from the system. One sentence each.
* **Empirical pins.** De-saturation and the continuation rule, both reproduced only through the subsample.
* **Voices.** The head of trading: "We were short wind all month; every spike lines up with a wind miss." The operations director: "Those
  were the coldest nights of the year, and plant fell over all week."
* **Licensed wrong basis.** The policy records that the outage-cover broker prices cover on the MW declared unavailable in the outage feed and
  will present January on that basis.

## 8. Determinism by construction

* **Window.** An event counts in a period if it starts in the two hours before the period and is still active; no event starts within ten
  minutes of a window edge.
* **Continuation match.** An overrun's start equals its planned predecessor's end to the minute; no genuine trip starts within 30 minutes of a
  planned end on the same asset.
* **MW removed.** Metered output in the settlement period before the event start; every trip has one.
* **Ties.** No spike period has two contributions within 50 MW.
* **Rounding.** The figure is filed to the nearest £10,000 and sits mid-bin.

## 9. Prompt sketch and deliverables

> The board decides on the 10th whether we buy outage cover for next winter, and it wants to know how much of January's £4.8M imbalance bill the
> plant trips actually cost us. The desk is sure it was wind. Give me that figure to the nearest £10,000, as the line I file in the board paper.
> Send `trip_cost_case.xlsx`, a chart `spike_attribution.png` and a two-page `board_paper.pdf`.

* `trip_cost_case.xlsx` — the attribution build, the wind-farm sheet (ask A), the gas sheet (ask B) and the subsample reproduction (ask C).
* `spike_attribution.png` — January's spike periods as a timeline of daily cost bars split by attributed class, with the overrun periods marked,
  the 40 subsample periods ticked, 12 and 19 January annotated, and the committed figure as a labelled reference.
* `board_paper.pdf` — the committed figure, what it counts and what it excludes.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six contracted wind farms, January metered output, availability and curtailed MWh.
  *Device:* curtailment instructions are filed as accepted bids with negative volumes on the farm's balancing unit, as the balancing data's
  sign convention documents; reading the bid volumes as positive generation overstates output at the four farms behind the export constraint.
* **Ask B (device-carried).** For each January gas day, the supplier's shipper imbalance quantity and charge. *Device:* the gas day runs from
  05:00 to 05:00, as the network code documents; grouping by calendar day misplaces the overnight cold-snap swings and moves the worst day.
* **Ask C (validity).** For each of the four constructions, verified labels reproduced out of 40 and the subsample's trip cost; and the twin
  days' trip cost under each.
* **Decoupling.** Clearing the continuation rule changes no figure in asks A or B; neither uses the outage feed.

## 11. Rubric arithmetic

6 farms × 3 figures (ask A) + 31 gas days × 2 figures (ask B) + 4 constructions × 2 figures + 2 days × 4 constructions (ask C) + the committed
figure, the overrun MW and the runner-up construction's figure + 5 named chart parts + 3 files ≈ 115 criteria.

## 12. World-building constraints

* £4.8M across 212 spike periods; rung figures £3.62M / £3.05M / £2.48M / £1.94M; grid as in section 4.
* 44 trip messages, 31 at full registered capacity, 18 of those from part load; 14 derate overruns, each starting at its planned
  predecessor's end to the minute.
* The subsample: 40 periods, 27 / 30 / 34 / 40 reproduced on rungs 0–3, wind-first 19.
* 12 and 19 January identical on every period-summary and feed-level column.
* Curtailment bids and gas-day boundaries touch no spike period's classification.

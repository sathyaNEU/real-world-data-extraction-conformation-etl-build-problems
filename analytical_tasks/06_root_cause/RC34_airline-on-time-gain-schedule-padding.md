# RC34 — On-time arrivals up from 76% to 83%: did the operation improve, or did the schedule get longer?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | SLA metrics that improve when the target moves (support "resolved within SLA" after SLA tiers were lengthened; delivery promises padded; build times "within budget" after budgets rose) |
| Domain | Airline operations |
| Task shape | 12 · Drill-down to one leaf (airline on-time change → schedule padding vs operational change vs route mix → hub → the route where padding contributed most) |
| Core method | Arrival delay = departure delay + (actual elapsed − scheduled elapsed); for flights in route × departure-hour cells present in both years, recompute this year's on-time status against last year's scheduled elapsed time for the cell (counterfactual); padding effect = actual − counterfactual on-time rate; operational effect = counterfactual − last year; route-mix effect from cells not matched; cancellation rates reported as a selection check |
| Analytical stump | On-time is measured against the published schedule, so lengthening scheduled block times raises on-time performance without any flight arriving earlier. A within-route comparison against a fixed schedule separates padding from operations. Ignoring cancellations is a second trap: cancelled flights drop out of the on-time denominator, so a rise in cancellations of delay-prone flights flatters the metric |
| Primary sources | U.S. DOT Bureau of Transportation Statistics — Reporting Carrier On-Time Performance (flight-level) |

## 1. The real-world situation

An airline's on-time arrival rate for July rose from 76% to 83% year over year, and the operations division requested its performance bonus for an
"operational excellence" programme. The finance committee noticed that published block times on many hub routes had been lengthened at the
schedule change. It asked for a decomposition before approving the bonus.

## 2. The decision (one deterministic recommendation)

**Whether the operational-excellence bonus is approved (approved only if the operational effect is ≥ 50% of the on-time improvement), with the
decomposition and the hub and route where padding contributed most.**

Rules (finance memo):

* Data: BTS Reporting Carrier On-Time Performance for the memo's carrier (operating carrier code), July of years Y1 and Y2.
* Flights: operated flights (not cancelled, not diverted) for on-time; cancellation rate reported separately.
* On-time: arrival delay < 15 minutes; arrival delay = departure delay + (actual elapsed − CRS elapsed), consistent with the BTS fields.
* Cells: origin × destination × departure-hour block (05–09, 10–13, 14–17, 18–23 local); matched if ≥ 20 operated flights in both years.
* Counterfactual for Y2 flights in matched cells: arrival delay′ = departure delay + actual elapsed − mean CRS elapsed of the cell in Y1.
* Effects (percentage points of the carrier's on-time rate): padding = (Y2 on-time − Y2 counterfactual on-time) × matched-flight share in Y2;
  operational = (Y2 counterfactual on-time in matched cells − Y1 on-time in matched cells) × matched-flight share in Y2; route mix = remainder.
* Drill-down: padding effect by hub (origin or destination in the memo's hub list), then by route within the top hub.

## 3. Why capable analysts get it wrong

* On-time percentage is treated as an operational outcome.
* Scheduled block times change quietly at schedule changes.
* Route and time-of-day mix shift between years.
* Cancellations remove delay-prone flights from the denominator.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `On_Time_Reporting_Carrier_On_Time_Performance_<Y1>_7.csv` | CSV | ~600k | BTS TranStats | U.S. Government work (public domain) | Y1 flights |
| 2 | `On_Time_Reporting_Carrier_On_Time_Performance_<Y2>_7.csv` | CSV | ~600k | BTS TranStats | Public domain | Y2 flights |
| 3 | `L_AIRPORT_ID.csv` / `L_UNIQUE_CARRIERS.csv` | CSV | ~7k | BTS lookup tables | Public domain | Codes |
| 4 | `airport_timezones.csv` | CSV | ~400 | Task author (from public airport data; cite) | Cite | Local hour blocks |
| 5 | `finance_memo.pdf` | PDF | — | Task author | — | Rules in §2, carrier, hubs |
| 6 | `operations_bonus_request.xlsx` | XLSX | — | Task author | — | The headline claim |

## 5. Deterministic solution path

1. Filter carrier and months; derive local hour blocks; separate cancelled and diverted flights.
2. Build cells; match; compute Y1 mean CRS elapsed per cell.
3. Counterfactual on-time for Y2 matched flights; effects; closure with the headline change.
4. Hub and route drill-down; cancellation check; decision.

## 6. Wrong paths (method errors, not misreadings)

**A — headline on-time change.** Padding credited as operational improvement.

**B — mean arrival delay comparison.** Also measured against the schedule; shares the bias.

**C — no route/time matching.** Mix changes contaminate the comparison.

**D — cancellations ignored.** A rise in cancellations of late-day flights inflates on-time.

## 7. Why the stump is analytical, not semantic

All fields are standard BTS columns; the counterfactual is specified. The trap is a relative metric whose reference (the schedule) moved.

## 8. Draft task prompt (prose)

> Operations wants its bonus for a 7-point on-time gain. Decompose the improvement with the finance memo's schedule-adjusted method and tell me
> whether the operation actually improved. Provide `on_time_decomposition.csv` (component: points; hub and route detail), `padding_by_hub.png`, and a
> one-page `bonus_decision.pdf`.

## 9. Deliverables

* `on_time_decomposition.csv` — padding, operational and mix effects; hub and route drill-down.
* `padding_by_hub.png` — padding vs operational effects by hub.
* `bonus_decision.pdf` — decision, decomposition, cancellation check and the leaf route.

## 10. Where 25+ rubric criteria come from

* Filtering counts (operated, cancelled, diverted by year): 6.
* Cell matching (cells, matched share): 3.
* Y1, Y2 and counterfactual on-time rates: 3.
* Three effects and closure: 4.
* Hub and route drill-down: 4.
* Cancellation check and decision: 3.
* Contrast with the request: 2+.

## 11. Golden-output checklist

* Local departure hour blocks; operated-flight base.
* Cell matching threshold; Y1 mean CRS elapsed per cell.
* Effects weighted by matched share; closure.

## 12. Build notes (scope tuning)

* Choose a carrier and year pair with a documented block-time increase at hubs; confirm that padding exceeds 50% of the gain.

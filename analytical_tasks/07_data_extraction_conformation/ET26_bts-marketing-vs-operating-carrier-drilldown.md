# ET26 — Why did the hub's on-time performance fall? Marketing brand vs operating carrier, mix vs rate

| Field | Value |
|---|---|
| Domain | Airline operations / airport performance / network planning |
| Objective family | Root-Cause Analysis |
| Task shape | 12 · Drill-down to one leaf (brand → operating carrier → route group) |
| Core technique | Carrier-identity conformance (marketing vs operating vs reporting carrier); shift-share decomposition separating traffic-mix change from rate change at each level; regulator-consistent on-time definition |
| Trap family (honest data) | Attributing regional-partner flights to the regional's own code; reading rate changes without separating mix; mis-defining on-time with cancellations/diversions |
| Primary sources | BTS Marketing Carrier On-Time Performance (2018+), BTS Reporting Carrier On-Time Performance, carrier/airport lookup tables |

## 1. The real-world project

An airport authority's performance team saw its hub's arrival on-time rate fall between two summers and must tell the
board **which carrier relationship and which part of the network** drove it. The dashboard used the familiar BTS
reporting-carrier table and listed regional airlines separately. The mainline brand looked fine; the regional carriers
looked bad; the board asked the wrong airline for an explanation.

## 2. The business decision (one deterministic recommendation)

**Which single leaf — brand → operating carrier → route-length group — explains the largest share of the decline in
hub arrival on-time rate from July–August 2023 to July–August 2024, and which team owns it?**

Rules (performance-analysis standard):

* Flights: arrivals at the hub (Dest = hub) in July–August of each year from the **Marketing Carrier On-Time Performance**
  table; brand = `Marketing_Airline_Network`; operating carrier = `Operating_Airline` (or the operating-carrier field in
  that table); route-length group by `Distance` (< 500, 500–999, ≥ 1000 miles).
* On-time = arrived < 15 minutes after schedule (`ArrDel15 = 0`); cancelled and diverted flights count as **not on time**
  and stay in the denominator (the standard's definition; note this differs from some public summaries).
* Decomposition at each level: Δrate = Σ (Δshare × base-period rate) [mix] + Σ (current share × Δrate) [rate]; drill into
  the child with the largest rate contribution (absolute, negative); stop at route-length group.
* Owner mapping (folder): brand network-operations team for mainline-operated leaves; partner-management team for
  regional-operated leaves.

## 3. Why this gets overlooked in real projects

* The long-standing "Reporting Carrier" table reports by the operating carrier; branded regional flights look like
  separate airlines, so brand-level questions get carrier-level answers.
* Regional partners often fly several brands; summing by operating carrier mixes brands.
* Rate declines and mix shifts (e.g. more long-haul or more regional flying) are conflated when ranking "who got worse".
* Cancellation treatment changes the denominator; with summer storms, it changes the answer.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1–4 | `mkt_ontime_2023_07.csv`, `…_2023_08.csv`, `…_2024_07.csv`, `…_2024_08.csv` | CSV | ~600k–700k each (all U.S.) | BTS TranStats, Marketing Carrier On-Time Performance | U.S. Gov public domain | Flights with brand + operator |
| 5–8 | `rep_ontime_2023_07.csv` … `rep_ontime_2024_08.csv` | CSV | ~600k each | BTS Reporting Carrier On-Time Performance | Public domain | Familiar but different carrier view |
| 9 | `L_CARRIER_HISTORY.csv`, `L_UNIQUE_CARRIERS.csv` | CSV | ~1.7k / ~1.7k | BTS lookup tables | Public domain | Carrier codes |
| 10 | `L_AIRPORT_ID.csv` | CSV | ~6.5k | BTS | Public domain | Airport IDs |
| 11 | `bts_ontime_field_definitions.pdf` | PDF | — | BTS | Public domain | Field meanings |
| 12 | `air_travel_consumer_report_excerpt.pdf` | PDF | — | U.S. DOT | Public domain | Context on published definitions |
| 13 | `analysis_standard.pdf` | PDF | — | Task author | — | Rules in §2 |
| 14 | `owner_mapping.json` | JSON | ~20 | Task author | — | Teams per leaf type |

## 5. Deterministic solution path

1. Filter hub arrivals in both periods from the marketing-carrier table.
2. Compute on-time rates and shares at brand level; decompose Δ into mix and rate; choose the brand with the largest
   negative rate contribution.
3. Within that brand, repeat by operating carrier; then by route-length group.
4. Report the leaf, its rate contribution, and owner; reconcile the hub total change exactly.
5. Show the reporting-carrier view and the cancellations-excluded definition for contrast.

## 6. The traps

**Trap A — reporting-carrier view.** Regional operators appear as independent airlines; the "worst airline" differs from
the brand-level leaf.

**Trap B — ranking raw rates.** A child whose share grew but whose rate held steady gets blamed (mix mistaken for rate).

**Trap C — cancellations excluded.** Storm-heavy days drop out; the leaf moves to a different operator.

**Trap D — departures instead of arrivals.** Different question, different leaf.

## 7. Why the data is honest

BTS publishes both views from airline-reported data; the marketing-carrier table exists precisely to show branded
regional operations. The decomposition rule and on-time definition are stated in the standard.

## 8. Draft task prompt (prose)

> The board wants to know what drove the fall in our hub's arrival on-time rate between summer 2023 and summer 2024, and
> who owns it. Following the analysis standard in the folder, decompose the change brand by brand, then operating carrier
> within the brand, then route-length group, separating mix from rate at each level, and tell me the leaf and the owning
> team. Produce `otp_drilldown.xlsx` with a sheet per level (shares, rates, mix and rate contributions) and
> `otp_drilldown.png`, a three-panel chart showing the contributions at each level with the chosen path highlighted. On
> the first sheet, state the leaf, its contribution in percentage points, the owner, and which carrier a reporting-carrier
> analysis would have blamed instead.

## 9. Deliverables

* `otp_drilldown.xlsx`, `otp_drilldown.png`.

## 10. Where 25+ rubric criteria come from

* Contributions at each level (brands ~5, operators ~4, route groups 3) split mix/rate; hub totals; leaf, owner,
  alternative blame.

## 11. Golden-output checklist

* Marketing-carrier table; cancellations/diversions in denominator; shift-share at each level; leaf and owner stated.

## 12. Build notes (scope tuning)

* Pick a hub dominated by one brand with two or more regional operators; confirm the reporting-carrier view and the
  cancellation-excluded definition each point to a different culprit.
* Copy exact column names from the downloaded marketing-carrier files (they differ from the reporting table).

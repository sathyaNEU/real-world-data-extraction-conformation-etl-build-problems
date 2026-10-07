# P18 — Battery cycling threshold from day-ahead prices: hour-ending 24:00, 25-hour days and the UTC trap

| Field | Value |
|---|---|
| Domain | Power markets / battery storage asset management |
| Objective family | Forecasting & Predictive Modeling (operational policy from history) |
| Task shape | 04 · Setting one dial (minimum daily spread that keeps cycles within warranty) |
| Core technique | Market-calendar conformance: operating day in local prevailing time, hour-ending labels, repeated/missing DST hours; constrained daily optimization; order statistic for the dial |
| Trap family (honest data) | Grouping by UTC date; parsing HE 24:00 as 00:00 of the same day; deduplicating the repeated fall-back hour |
| Primary sources | ERCOT Day-Ahead Market Settlement Point Prices (hourly); ERCOT market calendar/protocol documentation |

## 1. The real-world project

An owner of a 100 MW / 400 MWh battery at an ERCOT hub sets one parameter for the coming year: the **minimum daily
day-ahead spread** below which the battery sits idle. The warranty allows 300 full cycles per year. The analyst replayed
2023 prices to calibrate the threshold. Their data loader converted timestamps to UTC "to be safe" and grouped by date.
Their replay showed the battery charging at 1 a.m. and discharging at 6 p.m. on the *previous* evening.

## 2. The business decision (one deterministic recommendation)

**What daily spread threshold θ ($/MWh) should be set for next year, calibrated on 2023, and what 2023 revenue does it
imply?**

Rules (asset operating policy):

* Operating day = ERCOT operating day in Central Prevailing Time; prices are hour-ending (HE 01:00 … HE 24:00); the
  fall-back day has 25 hours (the repeated HE 02 is flagged), the spring-forward day has 23.
* Each operating day, choose 4 charge hours and 4 discharge hours (1 MWh per MW per hour, 100 MW) such that **every charge
  hour precedes every discharge hour** within the operating day; maximize daily value
  V = Σ discharge prices × 0.88 − Σ charge prices (round-trip efficiency 88%), in $/MW-day; spread S = V ÷ 4.
* Node: the hub in the policy; DAM settlement point prices.
* θ = the 300th-largest positive daily spread in 2023 (so exactly 300 days cycle; if fewer than 300 positive days, θ = 0).
* Implied revenue = Σ over cycled days of V × 100.

## 3. Why this gets overlooked in real projects

* "Convert to UTC first" is good practice for storage, but market products are defined on local operating days; grouping
  UTC dates moves the evening peak into the next day's bucket (CPT evening hours are after 00:00 UTC).
* Many datetime parsers reject `24:00` or map it to 00:00 of the same date, moving the last hour of every day to its start
  — changing which hours can precede which.
* Pivoting by (date, hour) fails or silently averages on the 25-hour day; the 23-hour day gets a phantom hour.
* The dial is an order statistic; small, systematic shifts in daily spreads move it.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1–12 | `DAM_SPP_2023_MM.csv` (monthly, all settlement points) | CSV | ~0.1–0.15M each | ERCOT Market Information System / Public API (NP4-190-CD) | ERCOT public data (terms of use; verify) | Hourly DAM prices with repeated-hour flag |
| 13 | `DAM_SPP_2023.xlsx` (annual historical workbook) | XLSX | ~1.5M | ERCOT historical DAM SPP | Same | Cross-check |
| 14 | `ercot_dst_and_hour_ending_conventions.pdf` (Protocols/market guide excerpt) | PDF | — | ERCOT Nodal Protocols | Public | Operating-day and DST rules |
| 15 | `settlement_points_list.csv` | CSV | ~1k | ERCOT | Public | Hub names |
| 16 | `asset_operating_policy.pdf` | PDF | — | Task author | — | Rules in §2 |
| 17 | `ercot_api_sample_response.json` | JSON | ~100 | ERCOT Public API | Public | Field names/format |

## 5. Deterministic solution path

1. Load the hub's DAM prices; build a local operating-day index from Delivery Date + Hour Ending + repeated-hour flag
   (25 hours on fall-back day, 23 on spring-forward day).
2. For each day, for each split point k, take the 4 cheapest hours before k and the 4 most expensive at/after k; keep the
   best V; compute S.
3. Sort positive S descending; θ = 300th value; revenue = Σ top-300 V × 100.
4. Reproduce the result under the UTC-date grouping and the 24:00→00:00 parse to show how θ and revenue move.

## 6. The traps

**Trap A — UTC dates.** Evening peaks fall into the next UTC day; daily optima become "charge at night, discharge
yesterday evening" artefacts; θ shifts materially.

**Trap B — HE 24 at the start of the day.** The cheap late-night hour becomes available for charging before the same
day's peak; spreads inflate; θ too high.

**Trap C — DST mishandling.** 25-hour day deduplicated or 23-hour day padded; small effect unless those days sit near the
300th rank — check and report.

**Trap D — ignoring the ordering constraint.** Unconstrained top-4/bottom-4 spreads overstate value on days with morning
peaks.

## 7. Why the data is honest

ERCOT prices are official settlement prices with documented hour-ending and DST conventions. The difficulty is time
semantics, not data quality.

## 8. Draft task prompt (prose)

> Set the battery's minimum daily spread for next year using our operating policy, calibrated on 2023 day-ahead prices at
> the hub in the folder, so the battery cycles exactly 300 days. Tell me the threshold and the 2023 revenue it implies.
> Produce `daily_spreads_2023.csv` with one row per operating day (hours in the day, chosen charge and discharge hours,
> daily value, spread, cycled flag) and `spread_duration_curve.png`, the daily spreads sorted from highest to lowest with
> the 300th day and θ marked. Add a one-page `threshold_memo.pdf` stating θ, the implied revenue, the spread of the 301st
> day, and how θ would change if the days had been grouped in UTC.

## 9. Deliverables

* `daily_spreads_2023.csv` (365 rows), `spread_duration_curve.png`, `threshold_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* θ, revenue, 301st spread; daily values for ~10 named days (incl. both DST days, a scarcity day); hours-per-day for DST
  days; UTC-variant θ; chart marking.

## 11. Golden-output checklist

* Local operating days; HE24 as last hour; 25/23-hour days; ordering constraint; θ and revenue stated.

## 12. Build notes (scope tuning)

* Verify that Traps A and B each move θ by more than $2/MWh on the chosen hub/year; if not, choose a year/hub with
  sharper evening peaks.
* Record the exact ERCOT report ID and download dates; ERCOT moved historical data to an API with key-based access.

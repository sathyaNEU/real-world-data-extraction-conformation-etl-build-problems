# OS04 — Battery arbitrage revenue: hindsight dispatch is not a business case

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Sizing value from timing decisions made under uncertainty: storage arbitrage, spot-instance bidding, inventory buying ahead of price changes |
| Domain | Electricity markets / energy storage |
| Task shape | 03 · Bridge between two totals (perfect-foresight real-time arbitrage revenue → revenue from a day-ahead-scheduled battery settled at real-time deviations; the zone selected for a 20 MW / 80 MWh project) |
| Core method | Daily linear-programme dispatch of a 4-hour battery (round-trip efficiency, state-of-charge limits, one cycle per day cap) — (a) on real-time prices with perfect foresight; (b) scheduled on day-ahead prices, settled day-ahead, with real-time imbalance = 0 (follows schedule); bridge: foresight premium, DA–RT spread, efficiency losses |
| Analytical stump | Optimising dispatch on realised real-time prices captures every spike that no operator could have known in advance; it overstates achievable revenue, often by a factor that changes the investment decision. A feasible strategy commits on information available at decision time |
| Primary sources | NYISO day-ahead and real-time zonal LBMP (public market data) |

## 1. The real-world situation

A developer compares New York zones for a 20 MW / 80 MWh battery. The screening model ran a perfect-foresight optimisation on real-time
prices and found one upstate zone most attractive because of a handful of extreme real-time spikes. The investment committee asked for a
revenue estimate that the battery could realistically earn with day-ahead scheduling.

## 2. The decision (one deterministic recommendation)

**The zone selected (highest day-ahead-scheduled annual arbitrage revenue for 2023 among the 5 candidate zones) and the bridge from
perfect-foresight RT revenue for that zone.**

Rules (investment memo):

* Prices: NYISO zonal LBMP, day-ahead hourly and real-time 5-minute (averaged to hourly), 2023, candidate zones in memo.
* Battery: 20 MW charge/discharge, 80 MWh energy, round-trip efficiency 85% (applied on charge), SoC between 5% and 95%, start/end each day at
  50%, ≤ 1 full equivalent cycle per day.
* Strategy A (benchmark): daily LP on real-time hourly prices (perfect foresight).
* Strategy B (feasible): daily LP on day-ahead prices; revenue settled at day-ahead prices; no real-time deviations.
* Annual revenue = Σ discharge × price − Σ charge × price.
* Bridge for the chosen zone: A → (remove foresight on RT) → B; report RT-vs-DA spread contribution.
* Choose the zone with the highest Strategy B revenue.

## 3. Why capable analysts get it wrong

* Perfect-foresight optimisation is the easiest benchmark to compute.
* Real-time spikes are short and unpredictable; most value in hindsight is unattainable.
* Day-ahead prices are known when scheduling; they are the right basis for a committed schedule.
* Efficiency and cycle limits reduce revenue materially.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–365 | `<yyyymmdd>damlbmp_zone.csv` | CSV | ~360 per day | NYISO public market data (MIS) | NYISO public data (terms: public use; verify) | Day-ahead LBMP |
| 366–730 | `<yyyymmdd>realtime_zone.csv` | CSV | ~4.3k per day | NYISO | Same | Real-time LBMP (5-minute) |
| 731 | `nyiso_zone_map.pdf` | PDF | — | NYISO | Public | Zones |
| 732 | `candidate_zones.json` | JSON | 5 | Task author | — | Zones |
| 733 | `battery_spec.json` | JSON | — | Task author | — | Parameters |
| 734 | `investment_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 735 | `screening_model_results.xlsx` | XLSX | 5 | Task author | — | Perfect-foresight revenue |
| 736 | `lp_check_day.json` | JSON | — | Task author | — | Hand-checked dispatch for one day |
| 737 | `hourly_prices_2023.parquet` | Parquet | ~88k | Derived | Same | Hourly DA and RT by zone |

## 5. Deterministic solution path

1. Load prices; average RT to hourly; align DST.
2. Daily LPs for Strategy A on RT and Strategy B on DA per zone.
3. Annual revenues; choose the zone; bridge.
4. Contrast with the screening results.

## 6. Wrong paths (method errors, not misreadings)

**A — perfect foresight.** Overstated revenue and wrong zone.

**B — DA schedule settled at RT prices without re-optimisation.** Not the memo's strategy.

**C — ignoring efficiency or SoC limits.** Inflated.

**D — DST hours mishandled.** 23/25-hour days misaligned.

## 7. Why the stump is analytical, not semantic

Parameters and strategies are specified. The trap is look-ahead in a dispatch optimisation used for sizing.

## 8. Draft task prompt (prose)

> Which zone should host our 4-hour battery? Compute annual arbitrage revenue for a day-ahead-scheduled battery in each candidate zone per the
> investment memo, and bridge the screening model's perfect-foresight number for the chosen zone. Provide `zone_revenue.csv` (zone: A and B
> revenue, cycles), `revenue_bridge.png`, and a one-page `zone_selection.pdf`.

## 9. Deliverables

* `zone_revenue.csv`, `revenue_bridge.png`, `zone_selection.pdf`.

## 10. Where 25+ rubric criteria come from

* 5 zones × (A, B, cycles) = 15; bridge items; monthly B revenue for the chosen zone (12); LP check day.

## 11. Golden-output checklist

* Price alignment; LP constraints; efficiency; strategy settlement; choice; bridge.

## 12. Build notes (scope tuning)

* Confirm the perfect-foresight leader differs from the Strategy B leader.

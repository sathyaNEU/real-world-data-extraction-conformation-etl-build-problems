# AD45 — Complaint storms: forty calls from one building, and a cold week that explains the rest

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Customer-support operations where one outage generates thousands of tickets (cloud providers, telcos, ride-hail apps), and city service desks |
| Domain | Housing enforcement / civic operations |
| Task shape | 12 · Drill-down to one leaf (citywide jump in heat complaints → borough → community district → the district whose excess distinct buildings is largest after weather adjustment) |
| Core method | Collapse complaints to distinct building-days (BBL × day); expected building counts from a weather model (negative binomial on heating degree days, day-of-week, district fixed effects) fitted on two prior heating seasons; drill-down of excess by level |
| Analytical stump | Raw complaint counts are dominated by large buildings where many tenants call about one boiler failure, and by cold snaps that raise complaints everywhere. The operational anomaly — more buildings without heat than the weather explains — needs de-duplication to the incident unit and a weather-adjusted expectation before drilling down |
| Primary sources | NYC 311 Service Requests (NYC Open Data); NOAA GHCN-Daily Central Park temperatures (for heating degree days) |

## 1. The real-world situation

During a January week, heat and hot-water complaints in New York City rose 70% over the prior week. The housing agency can send one extra
inspection team to one community district. The dashboard pointed to the district with the most complaints — home to several very large
complexes — while inspectors suspected a cluster of small buildings elsewhere.

## 2. The decision (one deterministic recommendation)

**The community district that receives the extra team, and its excess distinct buildings without heat over the target week.**

Rules (operations memo):

* Complaints: 311 records with complaint type HEAT/HOT WATER, created in heating seasons (1 Oct–31 May) 2021–22, 2022–23 and the target
  week in 2024; valid BBL required.
* Unit: distinct BBL × calendar day.
* Heating degree days: HDD = max(0, 65 − mean daily °F) at Central Park.
* Expectation model: negative binomial regression of daily distinct buildings per district on HDD, HDD², day-of-week and district fixed
  effects, fitted on the two prior seasons.
* Excess = observed − expected distinct building-days over the target week, by district; aggregate to borough and city.
* Drill: city → borough with largest excess → district within it with largest excess.

## 3. Why capable analysts get it wrong

* Call counts are the natural volume measure in service-desk dashboards.
* One incident generates many reports; incidents, not reports, consume inspection capacity.
* Weather drives heat complaints citywide; without adjustment, every cold week looks anomalous.
* Drilling down on counts follows the biggest buildings, not the biggest excess.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `311_Service_Requests_heat_2021_2024.csv` | CSV | ~600k | NYC Open Data (311 Service Requests) | NYC Open Data terms (open) | Complaints |
| 2 | `USW00094728.csv` | CSV | ~55k | NOAA GHCN-Daily (Central Park) | U.S. Gov public domain | Temperatures |
| 3 | `community_districts.geojson` | GeoJSON | 59 | NYC Department of City Planning | Open | District boundaries |
| 4 | `pluto_bbl_district_units.parquet` | Parquet | ~860k | NYC PLUTO | Open | BBL → district, units |
| 5 | `operations_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `dashboard_counts_target_week.xlsx` | XLSX | 59 | Task author | — | Dashboard view |
| 7 | `target_week.json` | JSON | 1 | Task author | — | Dates |
| 8 | `311_data_dictionary.xlsx` | XLSX | — | NYC Open Data | Open | Fields |
| 9 | `model_reference_coefficients.json` | JSON | ~10 | Task author | — | Check values |
| 10 | `hpd_heat_season_rules_citation.pdf` | PDF | — | NYC HPD (cite) | Public | Heat season context |

## 5. Deterministic solution path

1. Filter complaints; collapse to distinct BBL-days; attach districts.
2. Compute HDD; fit the expectation model on prior seasons.
3. Expected versus observed in the target week; excess by district, borough, city.
4. Drill-down; decision; contrast with the dashboard.

## 6. Wrong paths (method errors, not misreadings)

**A — complaint counts.** Large complexes dominate.

**B — no weather adjustment.** Cold-week effect taken as anomaly.

**C — expectation fitted including the target week.** Excess shrunk.

**D — ranking districts by percentage change.** Small bases dominate.

## 7. Why the stump is analytical, not semantic

The unit, model and drill rule are specified. The traps are report-versus-incident counting and confounding by weather.

## 8. Draft task prompt (prose)

> Where should the extra heat inspection team go this week? Follow the operations memo: count distinct buildings per day, compare with the
> weather-based expectation, and drill from the city to one district. Provide `excess_drill.csv` (level: observed, expected, excess),
> `district_excess_map.png`, and a one-page `team_deployment.pdf` explaining why the dashboard's top district is or is not chosen.

## 9. Deliverables

* `excess_drill.csv`, `district_excess_map.png`, `team_deployment.pdf`.

## 10. Where 25+ rubric criteria come from

* City and 5 borough excesses; district excesses within the chosen borough; model coefficients; de-duplication ratio; chosen district;
  dashboard contrast.

## 11. Golden-output checklist

* Complaint filter; BBL-day unit; HDD; model; target-week excess; drill path.

## 12. Build notes (scope tuning)

* Pick a target week where the top complaint district has large buildings with repeat callers and a different district leads on excess.

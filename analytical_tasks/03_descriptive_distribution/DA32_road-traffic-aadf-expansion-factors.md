# DA32 — Annual traffic from a one-day count: expand with the right seasonal and weekday factors

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Estimating monthly or annual usage from sampled days (panel measurement, sampled telemetry, store-traffic counters installed for a week) |
| Domain | Transport planning |
| Task shape | 02 · Forecast across many periods (annual average daily flow estimates for 30 count points from short counts; the road link prioritised for resurfacing on vehicle-km) |
| Core method | Expansion of 12-hour manual counts to 24-hour annual average daily flow (AADF) with factors from automatic traffic counters in the same factor group (road type × region): hour-of-day expansion (12h→24h), day-of-week and month factors; vehicle-type-specific factors |
| Analytical stump | A count taken on a June Tuesday is not an annual average: traffic varies by month, weekday and hour, differently on urban commuter roads and rural leisure routes. Using one national factor or none misranks links whose counts happened in peak or off-peak seasons |
| Primary sources | UK Department for Transport road traffic statistics — count-point raw counts and AADF data; automatic traffic counter (ATC) data |

## 1. The real-world situation

A highway authority prioritises resurfacing by vehicle-kilometres travelled on each link. It received single-day manual counts for 30 minor
road links and ranked them by the raw 12-hour counts multiplied by link length. Engineers noted that half the counts were taken in summer on
tourist routes and half in November on commuter roads.

## 2. The decision (one deterministic recommendation)

**The road link prioritised for resurfacing: the highest estimated annual vehicle-km (AADF × length × 365) among the 30, with AADF estimates for
all links.**

Rules (planning memo):

* Data: DfT raw count files for the 30 count points (12-hour counts 07:00–19:00 by vehicle type); ATC hourly data for the factor groups.
* Factor groups: road category (urban minor, rural minor) × region (as in `factor_groups.json`), assigned per count point.
* Factors from ATCs in the same group for the count year: E_h = 24-hour flow ÷ 07:00–19:00 flow (by day type); D_d = annual average daily flow ÷
  mean flow on weekday d; M_m = annual average ÷ mean flow in month m.
* AADF = 12-hour count × E_h × D_d × M_m, applied separately for cars/taxis, LGVs, HGVs, then summed (memo's vehicle-type factors).
* Vehicle-km = AADF × link length (km) × 365.
* Report the unexpanded ranking for contrast.

## 3. Why capable analysts get it wrong

* Raw counts look like measurements of traffic volume; they are samples of one day.
* Seasonal patterns differ by road type; national factors blur them.
* Factor application order and vehicle-type splits matter for HGV-heavy links.
* 12-hour counts miss evening and night traffic in different proportions.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `dft_traffic_counts_raw_counts.csv` | CSV | ~4.5M | DfT road traffic statistics | Open Government Licence v3 | Hourly manual counts by count point |
| 2 | `dft_traffic_counts_aadf.csv` | CSV | ~500k | DfT | OGL | Published AADF (validation where available) |
| 3 | `count_points.csv` | CSV | ~45k | DfT | OGL | Count point metadata, link length |
| 4 | `atc_hourly_<year>.csv` | CSV | ~3M | DfT / National Highways WebTRIS (OGL) | OGL | Automatic counter data |
| 5 | `factor_groups.json` | JSON | ~20 | Task author | — | Group definitions |
| 6 | `traffic_estimation_methodology.pdf` | PDF | — | DfT (cite) | OGL | Expansion methodology |
| 7 | `planning_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 8 | `raw_count_ranking.xlsx` | XLSX | 30 | Task author | — | Naive ranking |
| 9 | `links_in_scope.csv` | CSV | 30 | Task author | — | Count points, lengths |

## 5. Deterministic solution path

1. Extract 12-hour counts per link by vehicle type and date.
2. Build E_h, D_d, M_m per factor group from ATCs.
3. Expand per vehicle type; sum to AADF; compute vehicle-km.
4. Rank; validate against published AADF where the point was later counted; contrast with raw ranking.

## 6. Wrong paths (method errors, not misreadings)

**A — raw 12-hour counts.** Seasonal and weekday bias.

**B — one national factor.** Road-type differences ignored.

**C — total-vehicle factors only.** HGV-heavy links misestimated.

**D — 12h → 24h factor omitted.** Underestimates all links unequally.

## 7. Why the stump is analytical, not semantic

The factors and their application are specified. The trap is treating a sampled day as a population average.

## 8. Draft task prompt (prose)

> Which link should be resurfaced first? Expand the 30 short counts to annual average daily flows using the factor method in the planning memo
> and rank by annual vehicle-km. Provide `link_aadf.csv` (link: count date, 12-hour count, factors, AADF, vehicle-km, rank), `expansion_factors.png`
> (month and weekday factors by group), and a one-page `resurfacing_priority.pdf`.

## 9. Deliverables

* `link_aadf.csv`, `expansion_factors.png`, `resurfacing_priority.pdf`.

## 10. Where 25+ rubric criteria come from

* 30 AADF estimates (each a criterion); priority link; factors for 2 groups; contrast.

## 11. Golden-output checklist

* Group assignment; factor computation; vehicle-type application; length; ranking.

## 12. Build notes (scope tuning)

* Select links so that the raw-count ranking leader was counted in peak tourist season and falls below another link after expansion.

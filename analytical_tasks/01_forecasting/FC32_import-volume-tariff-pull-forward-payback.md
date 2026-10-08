# FC32 — Container imports after a tariff rush: front-loading moves volume in time, it doesn't create it

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Electronics and retail importers front-loading inventory ahead of tariff deadlines (2018–2019 and later tariff rounds) |
| Domain | Supply chain / port logistics / warehouse capacity |
| Task shape | 02 · Forecast across many periods (6 monthly import forecasts → one committed warehouse-lease level) |
| Core method | Baseline seasonal model estimated outside the surge window; intervention with a pull-forward pulse and an equal-volume payback spread over the following months |
| Analytical stump | A trend or seasonal model fed the surge months reads front-loading as growth and projects it forward; volume conservation (excess now = deficit later) is the key structural fact. Year-over-year comparisons during the payback look like a collapse in demand |
| Primary sources | Port of Los Angeles and Port of Long Beach monthly container statistics, U.S. Census import statistics |

## 1. The real-world situation

A third-party logistics firm leases overflow warehouse space near the San Pedro Bay ports. Ahead of a tariff increase, loaded
import containers surged for three months. The planner fitted a trend through the latest twelve months and committed to a large
six-month lease; after the deadline, volumes fell below normal for months and the space sat empty.

## 2. The decision (one deterministic recommendation)

**The committed lease level: the maximum monthly loaded-import TEU forecast for the six months after the forecast origin, and the
lease tier it implies.**

Rules (logistics memo):

* Series: monthly loaded import TEUs, Port of Los Angeles + Port of Long Beach combined, January 2010 onward.
* Surge window: the months between the tariff announcement and the effective date listed in `tariff_events.json`.
* Baseline: ln(TEU) = month effects + linear trend, OLS on the 60 months before the surge window.
* Excess = Σ over surge months (actual − baseline). Payback: the excess is subtracted equally over the 4 months after the
  effective date (documented shipper practice summarized in the memo).
* Forecast for each of the 6 months = baseline − payback share (if in the payback window).
* Lease tier: < 820k TEU/month → Tier A; 820–900k → Tier B; > 900k → Tier C (based on the maximum monthly forecast).

## 3. Why capable analysts get it wrong

* Recent months dominate trend fits; a three-month rush looks like acceleration.
* Seasonal models estimated with surge months distort seasonal factors for the same months next year.
* Without a conservation constraint, the payback is invisible to the model.
* Year-over-year growth comparisons in payback months mix two anomalies.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `pola_container_statistics_1995_2025.xlsx` | XLSX | ~370 months | Port of Los Angeles | Public statistics (verify terms) | TEUs by type |
| 2 | `polb_teu_archive_1995_2025.xlsx` | XLSX | ~370 | Port of Long Beach | Public statistics (verify terms) | TEUs by type |
| 3 | `census_imports_hs_district_monthly.csv` (Los Angeles customs district) | CSV | ~500k | U.S. Census International Trade API | Public domain | Import values by HS chapter |
| 4 | `census_api_query.json` | JSON | — | Task author | — | Query used |
| 5 | `tariff_events.json` | JSON | ~5 | Public USTR/Federal Register notices (dates) | Public domain | Announcement and effective dates |
| 6 | `federal_register_tariff_notice_excerpt.pdf` | PDF | — | Federal Register | Public domain | Event documentation |
| 7 | `shipper_survey_summary.pdf` (public trade-association survey, cited) | PDF | — | Cite | Cite | Front-loading behaviour |
| 8 | `logistics_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 9 | `planner_trend_forecast.xlsx` | XLSX | ~18 | Task author | — | Trend-based lease decision |
| 10 | `teu_monthly_combined.csv` | CSV | ~370 | Derived | — | Working series |

## 5. Deterministic solution path

1. Combine the two ports' loaded imports; fit the baseline on the pre-surge 60 months.
2. Compute excess over the surge window; distribute the payback.
3. Forecast six months; maximum; tier.
4. Contrast with the trend forecast; show cumulative volume conservation.

## 6. Wrong paths (method errors, not misreadings)

**A — trend through the surge.** Over-commits.

**B — seasonal model including surge months.** Distorted seasonality.

**C — no payback.** Baseline-only forecast too high in payback months.

**D — YoY reading of payback months.** Misread as demand collapse (if the decision were to cut).

## 7. Why the stump is analytical, not semantic

All series, dates and rules are specified. The trap is modelling a timing shift as a level change — a structural-modelling error.

## 8. Draft task prompt (prose)

> We need to commit to an overflow warehouse lease tier for the next six months. Using the port statistics and the logistics memo,
> forecast monthly loaded imports with the surge treated as front-loading — excess now, payback later — and tell me the tier.
> Provide `import_forecast.csv` (month: baseline, payback, forecast), `surge_and_payback.png` showing actuals, baseline and the
> forecast with cumulative excess and payback shaded, and a one-page `lease_decision.pdf` with the tier and what the trend forecast
> implied.

## 9. Deliverables

* `import_forecast.csv`, `surge_and_payback.png`, `lease_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* Baseline coefficients (12 month effects + trend); excess; 6 monthly forecasts; maximum; tier; trend contrast.

## 11. Golden-output checklist

* Combined loaded imports; pre-surge baseline; excess; equal payback; tiering.

## 12. Build notes (scope tuning)

* Use a historical tariff episode with a clear rush (e.g. late 2018) for a back-testable version; confirm trend and intervention
  forecasts fall in different tiers.
* Verify both ports' published definitions of loaded imports are comparable.

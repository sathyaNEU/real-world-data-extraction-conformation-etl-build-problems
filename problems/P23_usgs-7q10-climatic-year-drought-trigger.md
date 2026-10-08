# P23 — Drought-restriction trigger from streamflow: climatic years, provisional data and the 7Q10 you cannot compute by calendar

| Field | Value |
|---|---|
| Domain | Water utilities / drought contingency planning / hydrology data engineering |
| Objective family | Experiment & Causal Analysis (rule replayed on history) |
| Task shape | 08 · Rule replayed on history |
| Core technique | Hydrologic-year conformance (climatic year Apr 1–Mar 31 for low flows); qualifier-aware filtering (approved vs provisional, estimated, ice); moving-window statistics; log-Pearson III low-flow frequency |
| Trap family (honest data) | Calendar or water-year (Oct–Sep) minima; provisional data in frequency statistics; ice/missing as zero; centered vs trailing windows |
| Primary sources | USGS NWIS daily values (discharge, with qualification codes), USGS low-flow statistics documentation |

## 1. The real-world project

A municipal water utility withdraws from a river under a permit that requires **Stage 2 restrictions whenever the trailing
7-day mean flow falls below the 7Q10** (the lowest 7-day average flow expected once every 10 years). To size an
emergency interconnect contract, the utility replays the trigger over history. The engineer computed annual 7-day minima
on calendar years using all available data, fitted a distribution, and found restrictions would have been rare — too rare
for operators who remember three bad autumns.

## 2. The business decision (one deterministic recommendation)

**How many days of emergency-interconnect capacity should be reserved for 2025** = the 90th-percentile (nearest-rank)
of annual restriction days across the replay climatic years?

Rules (drought plan + statistics procedure):

* Flow: daily mean discharge (parameter 00060, statistic 00003) at the permit gage.
* 7Q10 statistic: climatic years (1 April – 31 March) from 1990-04-01 to 2023-03-31; only **approved** data (qualifier `A`,
  including `A:e` estimated); a climatic year with > 10 missing/unapproved days is excluded; annual statistic = minimum
  of 7-day moving means (window entirely within the climatic year); fit log-Pearson Type III by method of moments on
  log10 values with station skew; 7Q10 = flow at non-exceedance probability 0.10.
* Replay: for each included climatic year, count days whose **trailing** 7-day mean (days d−6…d, all present) is below
  7Q10; days with ice-affected or missing values break the window (no count).
* Reserve = nearest-rank 90th percentile of annual counts, in days.

## 3. Why this gets overlooked in real projects

* Low flows in many U.S. basins occur late summer through autumn — straddling both the calendar-year and water-year
  (October) boundaries. Calendar minima split one drought into two years and pick a less extreme minimum in each.
* NWIS serves provisional data (`P`) alongside approved data; it is revised, often materially for low flows.
* Ice-affected days (`Ice`) and equipment gaps show no value; filling with 0 creates artificial droughts.
* Centered moving averages (pandas default in some workflows) change which days are "below" the trigger.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1 | `dv_0xxxxxxx_00060_1990_2024.rdb` | RDB (tab-delimited) | ~12.5k days | USGS NWIS daily values service | U.S. Gov public domain | Primary gage |
| 2 | `dv_0xxxxxxx_00060_1990_2024.json` | JSON (WaterML-JSON) | ~12.5k | USGS | Public domain | Same with qualifiers |
| 3–4 | `dv_upstream_gage_*.rdb` (2 nearby gages) | RDB | ~12.5k each | USGS | Public domain | Context (not for statistics) |
| 5 | `site_info_0xxxxxxx.rdb` | RDB | 1 | USGS | Public domain | Drainage area, period of record |
| 6 | `nwis_qualification_codes.csv` | CSV | ~40 | USGS | Public domain | `A`, `P`, `e`, `Ice`, `Eqp` meanings |
| 7 | `usgs_lowflow_methods.pdf` (e.g. SIR on low-flow frequency, climatic year definition) | PDF | — | USGS publications | Public domain | Method basis |
| 8 | `streamstats_lowflow_report.pdf` (published 7Q10 for the gage, if available) | PDF | — | USGS StreamStats | Public domain | Sanity check |
| 9 | `drought_plan_and_procedure.pdf` | PDF | — | Task author (modelled on state drought plans) | — | Rules in §2 |
| 10 | `pearson3_frequency_factors.xlsx` | XLSX | ~300 | Standard statistical tables | Public domain | K-values (optional) |

## 5. Deterministic solution path

1. Parse values and qualifiers; classify days (approved, provisional, missing/ice).
2. Assign climatic years; compute 7-day moving means within each year; take annual minima for years passing completeness.
3. Fit LP3 (log10, method of moments, station skew); compute 7Q10.
4. Replay trailing 7-day means against 7Q10 for each included year; count restriction days.
5. Nearest-rank 90th percentile → reserve days. Contrast with calendar-year and provisional-inclusive variants.

## 6. The traps

**Trap A — calendar/water years.** Annual minima rise; 7Q10 rises or falls depending on basin timing; reserve changes.

**Trap B — provisional data.** Recent low-flow years enter the fit with values later revised.

**Trap C — gaps as zero.** Ice/equipment days produce zero-flow minima; LP3 on log10 breaks or 7Q10 collapses.

**Trap D — centered windows / windows across gaps.** Restriction-day counts shift.

**Trap E — percentile method.** Interpolated percentiles vs nearest rank change the integer answer.

## 7. Why the data is honest

NWIS daily values carry explicit approval and condition qualifiers; the climatic-year convention for low-flow statistics is
standard USGS practice. The data are what the gage measured and USGS reviewed.

## 8. Draft task prompt (prose)

> We need to size the emergency interconnect for 2025: reserve the number of days equal to the 90th-percentile year of
> Stage 2 restriction days, replaying the permit trigger over history as our drought plan and statistics procedure
> describe. Using the USGS files in the folder, compute the 7Q10 and replay every eligible climatic year. Provide
> `restriction_replay.csv` (one row per climatic year: completeness, annual 7-day minimum, included flag, restriction
> days), `lowflow_frequency.png` showing the annual minima on a probability plot with the fitted curve and the 7Q10
> marked, and a one-page `reserve_decision.pdf` stating the reserve, the 7Q10, the three worst years, and what the
> reserve would be if calendar years had been used.

## 9. Deliverables

* `restriction_replay.csv`, `lowflow_frequency.png`, `reserve_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* ~30 climatic-year minima / inclusion flags / restriction-day counts; LP3 moments; 7Q10; reserve; calendar-year variant.

## 11. Golden-output checklist

* Climatic years; approved data only for the fit; gaps break windows; trailing means; nearest rank; decision stated.

## 12. Build notes (scope tuning)

* Pick a perennial gage (no zero flows) in a basin with autumn droughts crossing 1 October, with recent provisional low
  flows and some ice days; confirm Trap A changes the reserve.
* Freeze the download (provisional values change); record the retrieval timestamp.

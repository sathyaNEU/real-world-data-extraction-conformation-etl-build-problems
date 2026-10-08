# AD03 — Which smart meters need a field visit? Judging each home against its own seasonal normal

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Domain | Electricity distribution / metering operations / revenue protection |
| Task shape | 01 · Ranked list under a cap (20 field inspections) |
| Core method | Per-household robust standardization (median/MAD) of weekly consumption after removing the population seasonal index; maximum robust z over the inspection window |
| Analytical stump | Global thresholds on kWh flag large homes; percentage changes flag tiny homes; unadjusted comparisons flag everyone in winter; non-robust SDs let a household's own past spikes hide a real fault. Anomaly must be relative to the unit's own normal, after the shared seasonal signal |
| Primary sources | UK Power Networks "SmartMeter Energy Consumption Data in London Households" (Low Carbon London) |

## 1. The real-world situation

A distribution network operator can send engineers to **20 homes** in the next inspection cycle to check for faulty meters
or tampering. The revenue-protection analyst flagged the homes with the largest drop in January–February consumption versus
the previous year. The list was dominated by homes with very small consumption (where a few kWh is a big percentage) and
missed several homes whose consumption had collapsed relative to their own history.

## 2. The decision (one deterministic recommendation)

**Which 20 households are inspected, and which is 21st?**

Rules (revenue-protection method):

* Households on the standard tariff (`stdorToU = Std`) with ≥ 90% half-hours present in both the baseline and inspection
  windows. Weekly kWh = Σ half-hourly kWh over ISO weeks (weeks with < 90% half-hours present are excluded).
* Baseline window: 2012-11-05 to 2013-12-29. Inspection window: 2014-01-06 to 2014-02-23 (7 weeks).
* Shared seasonal signal: population weekly index = median weekly kWh across all qualifying households in that week ÷ the
  median over the baseline window.
* For each household, adjusted weekly value = weekly kWh ÷ population index; household normal = median of adjusted baseline
  weeks; household scale = 1.4826 × MAD of adjusted baseline weeks.
* Score = max over inspection weeks of |adjusted kWh − normal| ÷ scale. Rank descending; ties by lower household ID.

## 3. Why capable analysts get it wrong

* "Biggest drop" lists are natural, but absolute changes scale with house size and percentage changes explode for small
  baselines.
* Winter weeks are high for everyone; a household-only baseline without the population index flags normal seasonality.
* A household's own holidays and spikes inflate a standard deviation; median/MAD resists them.
* Half-hourly data are noisy; weekly aggregation with completeness rules stabilizes the comparison.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–20 | `Power-Networks-LCL-June2015(withAcornGps)v2_<n>.csv` (block files) | CSV | ~1M each (167M total; ship the blocks covering the sample) | London Datastore / UK Power Networks | London Datastore licence (verify; dataset published openly) | Half-hourly kWh per household |
| 21 | `informations_households.csv` | CSV | 5,566 | UKPN (household metadata incl. tariff, Acorn) | Same | Tariff group, Acorn |
| 22 | `lcl_weekly_household_kwh.parquet` | Parquet | ~600k | Derived | Same | Weekly aggregates |
| 23 | `lcl_project_report_extract.pdf` | PDF | — | Low Carbon London reports (UKPN) | Same | Data collection notes |
| 24 | `uk_bank_holidays.json` | JSON | ~50 | GOV.UK | OGL v3.0 | Context |
| 25 | `revenue_protection_method.pdf` | PDF | — | Task author | — | Rules in §2 |
| 26 | `analyst_drop_list.xlsx` | XLSX | 20 | Task author | — | Percentage-drop list |

## 5. Deterministic solution path

1. Filter standard-tariff households; build weekly kWh with completeness rules.
2. Compute the population weekly index; adjust each household's weeks.
3. Household median and MAD on baseline; robust z in inspection weeks; max |z|.
4. Rank; top 20 + 21st.
5. Contrast: % drop list, raw-kWh global z list, SD-based z list.

## 6. Wrong paths (method errors, not misreadings)

**A — percentage drop.** Small-consumption homes dominate.

**B — global z on kWh.** Large homes dominate.

**C — no seasonal index.** Winter weeks flag normal homes.

**D — mean/SD instead of median/MAD.** Real faults masked in homes with spiky baselines.

## 7. Why the stump is analytical, not semantic

The data are kWh by half-hour with clear metadata; the method defines windows and scores. The traps are choices of
reference, scale and robustness — statistical design decisions.

## 8. Draft task prompt (prose)

> We can inspect twenty meters this cycle. Using the London smart-meter data and the revenue-protection method in the
> folder, score every qualifying household on how far its consumption in January–February 2014 departed from its own
> normal, after allowing for the citywide seasonal pattern, and give me the twenty homes and the one just behind. Produce
> `inspection_scores.csv` (household, normal, scale, worst week, score, rank), `top_households_weekly.png` showing the
> adjusted weekly series and normal band for the top six households, and a one-page `inspection_memo.pdf` listing the twenty,
> the score gap at the cut, and how many of the analyst's percentage-drop list remain.

## 9. Deliverables

* `inspection_scores.csv`, `top_households_weekly.png`, `inspection_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 20 households + 21st + gap; scores/worst weeks for ~8; population index for 7 inspection weeks; overlap with the analyst
  list.

## 11. Golden-output checklist

* Completeness filters; population index; median/MAD per household; max |z|; ranking and tie rule.

## 12. Build notes (scope tuning)

* Ship only the block files containing the sampled households (document which); confirm the percentage-drop list overlaps
  the correct top 20 by fewer than half.
* State the household-ID tie-break and missing-week rules exactly.

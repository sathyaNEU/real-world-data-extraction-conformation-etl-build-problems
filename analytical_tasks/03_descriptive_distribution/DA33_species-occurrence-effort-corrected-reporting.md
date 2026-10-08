# DA33 — Is the species spreading, or are more people looking? Occurrence counts track observers

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Any analysis of user-generated observations (reviews, check-ins, photo uploads, crowd-sourced outage reports) where counts reflect where and when users are active |
| Domain | Biodiversity / environmental consulting |
| Task shape | 07 · Grid of cells (8 regions × 3 periods → effort-corrected reporting rate; the region where the invasive-species response plan is activated) |
| Core method | Reporting rate = records of the target species ÷ total records of the reference taxon group by the same observation pool (region × period), with the memo's list-length restriction (checklists with ≥ 3 species); change relative to baseline period; comparison with raw occurrence counts |
| Analytical stump | Raw occurrence counts of a species explode wherever participation in citizen-science apps grows. Correcting by total recording effort in the same group, region and period distinguishes range expansion from observer growth |
| Primary sources | GBIF occurrence download (citizen-science datasets with CC0/CC BY licences) for a taxon group |

## 1. The real-world situation

A regional environment agency activates an invasive-species response plan where an invasive insect is expanding. A consultant's
dashboard showed records of the species rising tenfold in most regions over five years and recommended activation in five regions. An
ecologist noted that total records of all insects rose similarly after a popular identification app launched.

## 2. The decision (one deterministic recommendation)

**The region(s) where the plan is activated: those whose effort-corrected reporting rate in the latest period is ≥ 2× the baseline period
and ≥ 1% in absolute terms, with rates for all cells.**

Rules (agency memo):

* Data: GBIF occurrence download (DOI in memo) for the reference taxon group in the 8 regions, 2014–2023, licences CC0 or CC BY only;
  `basisOfRecord` = HUMAN_OBSERVATION.
* Periods: baseline 2014–2016, middle 2017–2019, latest 2021–2023 (2020 excluded per memo).
* Observation pool: records grouped into checklists by (recordedBy, eventDate, 1-km grid cell); keep checklists with ≥ 3 distinct species.
* Reporting rate = share of retained checklists containing the target species.
* Activation: latest ÷ baseline ≥ 2 and latest ≥ 1%; regions with < 200 checklists in any period are flagged "insufficient effort".
* Report raw record counts for contrast.

## 3. Why capable analysts get it wrong

* Counts are what occurrence portals display.
* Participation and app adoption vary strongly by place and year.
* Single-species incidental records are biased toward rare or striking species; list-length restriction approximates complete lists.
* The denominator must come from the same observers' effort, not area or population.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `gbif_download_<key>.zip` (Darwin Core Archive) | TSV inside ZIP | ~3–6M occurrences | GBIF.org occurrence download | CC0 / CC BY 4.0 (per-record, filtered) | Occurrences |
| 2 | `meta.xml`, `eml.xml` | XML | — | GBIF | Same | Archive metadata, dataset citations |
| 3 | `regions.geojson` | GeoJSON | 8 | Task author (administrative regions) | Open | Regions |
| 4 | `target_species.json` | JSON | 1 | Task author | — | Species key |
| 5 | `agency_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `consultant_dashboard_counts.xlsx` | XLSX | 24 | Task author | — | Raw counts |
| 7 | `reporting_rate_method_citation.pdf` | PDF | — | Szabo et al. / list-length analysis (cite) | Cite | Method |
| 8 | `checklists.parquet` | Parquet | ~600k | Derived | Same | Constructed checklists |
| 9 | `gbif_citation_list.txt` | Text | — | GBIF | — | Dataset citations (licence compliance) |

## 5. Deterministic solution path

1. Filter licences, basis of record, regions, years.
2. Construct checklists; list-length filter.
3. Reporting rates per cell; ratios; activation rule.
4. Contrast with raw counts.

## 6. Wrong paths (method errors, not misreadings)

**A — raw counts.** Observer growth mistaken for spread.

**B — rate per area or population.** Wrong denominator.

**C — no list-length filter.** Incidental records bias rates.

**D — including 2020.** Lockdown-specific effort patterns.

## 7. Why the stump is analytical, not semantic

Checklist construction and rates are specified. The trap is sampling effort in opportunistic data.

## 8. Draft task prompt (prose)

> Where should we activate the invasive-species response plan? Compute effort-corrected reporting rates from GBIF records as the agency memo
> specifies. Provide `reporting_rate_grid.csv` (region × period: checklists, target checklists, rate, raw records), `rate_vs_count.png`, and a
> one-page `activation_decision.pdf`.

## 9. Deliverables

* `reporting_rate_grid.csv`, `rate_vs_count.png`, `activation_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 8 regions × 3 periods rates = 24; ratios; activation list; insufficient-effort flags; contrast.

## 11. Golden-output checklist

* Licence filter; checklist key; list length; periods; ratio rule.

## 12. Build notes (scope tuning)

* Choose a species and regions where raw counts rise everywhere but rates rise in only one or two regions.

# P37 — EU cohesion region category: the right NUTS version, the right EU average and the right data vintage

| Field | Value |
|---|---|
| Domain | Public policy / EU structural funds / official statistics conformance |
| Objective family | Descriptive & Distribution Analysis (regulatory scorecard) |
| Task shape | 10 · Scorecard against thresholds (region × year × category test) |
| Core technique | Classification-version conformance (re-aggregating NUTS 3 to the regulation's NUTS 2 version via correspondence tables); denominator-population choice (EU-27 vs EU-28 average); point-in-time data vintage |
| Trap family (honest data) | Current-NUTS codes assumed equal to old-NUTS regions; EU-28 average used; latest revised GDP used instead of the regulation's vintage |
| Primary sources | Eurostat regional accounts (GDP and population by NUTS 2/NUTS 3), NUTS correspondence tables, Regulation (EU) 2021/1060 Art. 108 and Annex XXVI, Commission Implementing Decision (EU) 2021/1130 |

## 1. The real-world project

A regional development agency builds a model to rehearse cohesion-policy eligibility and must first **replicate the
2021–2027 categorization** of its member state's NUTS 2 regions: less developed (< 75% of EU-27 average GDP per head in
PPS), transition (75–100%), more developed (> 100%), on the 2015–2017 average. The model reproduced the official list
for every region except two — the two the agency cares about.

## 2. The business decision (one deterministic recommendation)

**Go / no-go: does the model reproduce the official category for every NUTS 2 region of the member state (and, if not,
which region and why)?** The deterministic replication itself is the deliverable; the go/no-go is whether the model can be
used for the next simulation.

Rules (replication protocol, mirroring the regulation's method):

* Geography: **NUTS 2016** NUTS 2 regions (the classification used for 2021–2027). Where current Eurostat tables are
  published on a later NUTS version, rebuild NUTS 2016 regions by aggregating NUTS 3 GDP and population using the
  official correspondence tables (including regions whose codes are unchanged but whose boundaries shifted).
* Metric: GDP (PPS) ÷ average population, per region and year; 2015, 2016, 2017 averaged (mean of the three annual ratios to
  the EU average, as specified in the protocol).
* Denominator: **EU-27 (2020 composition, i.e. excluding the UK)** average GDP per head in PPS.
* Vintage: the data snapshot labelled with the regulation's reference vintage in the folder (not the latest revised data).
* Thresholds and rounding exactly as written in Annex XXVI (protocol quotes the text).
* Go if all regions' computed categories match the official list in Implementing Decision 2021/1130.

## 3. Why this gets overlooked in real projects

* Eurostat tables carry only the current NUTS version; codes that persist across versions look comparable, but some
  regions changed boundaries without changing codes, and some codes were split or merged.
* EU-28 and EU-27 averages coexist in older extracts; units are named similarly (`PPS_HAB_EU28` vs `PPS_HAB_EU27_2020`).
* Regional accounts are revised (benchmark revisions); a region at 74.6% in the original vintage may be 75.3% today.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1 | `nama_10r_3gdp_snapshot_reference.tsv` | TSV | ~100k | Eurostat (archived vintage) | Eurostat free re-use with attribution | NUTS 3 GDP (PPS) |
| 2 | `nama_10r_3popgdp_snapshot_reference.tsv` | TSV | ~50k | Eurostat | Same | NUTS 3 average population |
| 3 | `nama_10r_2gdp_latest.tsv` | TSV | ~40k | Eurostat (current) | Same | Latest NUTS 2 GDP (vintage and version trap) |
| 4 | `nama_10r_2gdp_latest.json` (SDMX-JSON) | JSON | ~40k | Eurostat API | Same | Same data, API format |
| 5 | `NUTS2013-NUTS2016.xlsx`, `NUTS2016-NUTS2021.xlsx` | XLSX | ~2k each | Eurostat NUTS history | Same | Correspondence and change types |
| 6 | `NUTS_RG_01M_2016_4326.geojson` | GeoJSON | ~1.9k | Eurostat GISCO | GISCO terms (free with attribution; verify) | Boundaries |
| 7 | `CELEX_32021R1060_art108_annexXXVI.pdf` | PDF | — | EUR-Lex | EU law (reuse permitted) | Method and thresholds |
| 8 | `CELEX_32021D1130.pdf` | PDF | — | EUR-Lex | EU law | Official list (reconciliation target) |
| 9 | `eu_aggregates_gdp_pps_2015_2017.csv` | CSV | ~20 | Eurostat | Same | EU-27_2020 and EU-28 averages |
| 10 | `replication_protocol.pdf` | PDF | — | Task author | — | Rules in §2 |

## 5. Deterministic solution path

1. From the reference-vintage NUTS 3 files, map NUTS 3 units to NUTS 2016 NUTS 2 regions via the correspondence tables.
2. Aggregate GDP (PPS) and population; compute per-head values for 2015–2017.
3. Divide by EU-27_2020 per-head values; average per the protocol; round as specified; classify.
4. Compare with the official list; go if all match. Report the margin for regions within 2 points of a threshold.
5. Contrast: latest-vintage NUTS 2 table on current codes; EU-28 denominator.

## 6. The traps

**Trap A — current NUTS codes.** Regions with boundary changes use the wrong territory; categories flip near thresholds.

**Trap B — EU-28 average.** Ratios fall by a point or two; borderline regions drop a category.

**Trap C — latest revised data.** Revisions move borderline regions.

**Trap D — averaging GDP and population separately vs ratios.** If the protocol specifies mean of annual ratios, ratio of
means differs slightly — enough at the threshold.

## 7. Why the data is honest

All inputs are official Eurostat statistics and EU legal texts; version changes and revisions are documented. The
official list provides an exact target.

## 8. Draft task prompt (prose)

> Before we use our cohesion model for the next simulation, prove it reproduces the 2021–2027 category of every NUTS 2
> region in our member state, using the replication protocol in the folder. Compute each region's 2015–2017 GDP per head in
> PPS relative to the EU-27 average on the NUTS 2016 map with the reference-vintage data, assign categories, compare with
> the official decision, and give me a go or no-go. Deliver `category_replication.xlsx` (region × year values, average
> ratio, computed and official category, match flag, margin to threshold) and `category_margin_chart.png`, a dot chart of
> each region's ratio against the 75% and 100% lines, mismatches marked. On the first sheet, state the decision and, for any
> mismatch, its cause.

## 9. Deliverables

* `category_replication.xlsx`, `category_margin_chart.png`.

## 10. Where 25+ rubric criteria come from

* Regions (e.g. 16–17 for Poland, 8 for Hungary) × (3 annual ratios, average, category, match); go/no-go; margins.

## 11. Golden-output checklist

* NUTS 2016 rebuilt from NUTS 3; EU-27_2020 denominator; reference vintage; protocol rounding; decision stated.

## 12. Build notes (scope tuning)

* Choose a member state with NUTS changes between 2016 and the current version and at least one region near 75% or 100%;
  confirm the latest-vintage/current-NUTS path produces a mismatch.
* Archive the exact Eurostat files used as the "reference vintage"; if an original-vintage snapshot is unavailable, define
  the vintage as a dated download and adjust the protocol wording accordingly.

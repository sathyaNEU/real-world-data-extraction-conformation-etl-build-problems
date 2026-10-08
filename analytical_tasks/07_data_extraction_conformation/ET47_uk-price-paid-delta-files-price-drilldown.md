# ET47 — Which market drove the regional price fall? Land Registry deltas, Category B transfers and mix vs price

| Field | Value |
|---|---|
| Domain | Residential property / mortgage risk / housing market analytics |
| Objective family | Root-Cause Analysis |
| Task shape | 12 · Drill-down to one leaf (region → local authority district → property type) |
| Core technique | Applying change-data-capture records (add/change/delete) to rebuild a dataset as of a date; transaction-category filtering (standard vs additional price paid); shift-share decomposition of mean price (mix vs within-type price) |
| Trap family (honest data) | Monthly update files appended without applying C/D statuses; Category B (portfolio/company/repossession) transfers included; median-based "decomposition" that cannot separate mix |
| Primary sources | HM Land Registry Price Paid Data (yearly files and monthly update files) |

## 1. The real-world project

A mortgage lender's risk team monitors house-price movements in its book's regions. A dashboard showed the **mean price
in the region down 6.8%** from H1 2023 to H1 2024, and the team wanted the local market and property type responsible to
tighten loan-to-value limits there. The dashboard's table was built by appending each monthly Price Paid update file to the
yearly base file. A district with a large company portfolio transfer looked like a crash.

## 2. The business decision (one deterministic recommendation)

**Which single leaf — district × property type — explains the largest share of the region's mean-price change after
separating mix from price, and does the lender tighten LTV there (rule: tighten if the leaf's within-type price change is
below −5%)?**

Rules (risk analytics standard):

* Build the dataset **as of 2024-09-30**: start from the yearly files for 2023 and 2024 (as published at the snapshot), then
  apply monthly update files in order — record status `A` adds, `C` replaces the record with the same transaction ID, `D`
  deletes it.
* Standard price paid only: `PPD Category Type = A` (Category B — repossessions, buy-to-let and transfers to non-private
  individuals, including multi-property transfers — excluded).
* Periods: completions (Date of Transfer) in H1 2023 vs H1 2024; region = the set of districts listed in the folder.
* Decomposition on **mean** price: ΔP = Σ (Δshare_i × P_i,2023) [mix] + Σ (share_i,2024 × ΔP_i) [price]; at each level drill
  into the child with the largest negative **price** contribution.
* Leaf = district × property type (D, S, T, F; O excluded as non-residential/other).

## 3. Why this gets overlooked in real projects

* Monthly update files look like "new rows"; their record-status column (only present in monthly files) gets ignored, so
  corrections duplicate and deletions survive.
* Category B was added to capture more transactions; it includes transfers where one total price is repeated for every title
  in a portfolio, creating extreme values.
* Medians are robust and popular but do not decompose; teams compare median changes across groups and mistake mix for price.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1 | `pp-2023.csv` | CSV (no header) | ~0.8–0.9M | HM Land Registry Price Paid Data | OGL v3.0 (with HMLR attribution; address data notes) | Base 2023 |
| 2 | `pp-2024.csv` (as published at snapshot) | CSV | ~0.6–0.8M | HM Land Registry | OGL v3.0 | Base 2024 |
| 3–11 | `pp-monthly-update-2024-01.csv` … `-2024-09.csv` | CSV | 50k–150k each | HM Land Registry | OGL v3.0 | A/C/D deltas |
| 12 | `price_paid_data_explanations.pdf` | PDF | — | HM Land Registry guidance | OGL v3.0 | Columns, Category A/B, record status |
| 13 | `ONSPD_AUG_2024_UK.csv` (district lookup, optional) | CSV | ~2.7M | ONS Postcode Directory | OGL v3.0 (+ Royal Mail/OS notes) | Postcode → LAD (validation) |
| 14 | `uk_hpi_lad_2023_2024.csv` | CSV | ~10k | UK House Price Index (HMLR/ONS) | OGL v3.0 | Context sanity check |
| 15 | `region_districts.json`, `risk_analytics_standard.pdf` | JSON/PDF | — | Task author | — | Scope, rules |

## 5. Deterministic solution path

1. Load base files with the documented column order; apply monthly deltas in order by transaction ID.
2. Filter Category A, residential types, H1 periods, region districts.
3. Region level: decompose by district; choose the district with the largest negative price contribution.
4. Within it: decompose by property type; choose the leaf; apply the LTV rule.
5. Contrast: appended deltas; Category B included; median comparison.

## 6. The traps

**Trap A — appended deltas.** Duplicated corrected transactions and surviving deletions change means.

**Trap B — Category B included.** Portfolio transfers dominate a district's mean; wrong district.

**Trap C — mix read as price.** A district selling more flats looks like it fell.

**Trap D — 2024 base without updates.** Late-registered H1 2024 transactions missing.

## 7. Why the data is honest

Price Paid Data are HM Land Registry's official records; record statuses and categories are documented. The update
mechanism is designed for exactly this replay.

## 8. Draft task prompt (prose)

> The region's mean price fell between H1 2023 and H1 2024. Following our risk analytics standard, rebuild the Price Paid
> data as of 30 September 2024, separate mix from price at the district level and then by property type within the
> district, and tell me the leaf, its price contribution, and whether we tighten LTV there. Produce `price_drilldown.xlsx`
> with the delta-application log (adds, changes, deletes applied), the district-level and property-type-level
> decompositions, and `price_drilldown.png` showing contributions at both levels with the path highlighted. On the first sheet,
> give the leaf, the decision, and which district a dashboard that appended updates and kept Category B would have blamed.

## 9. Deliverables

* `price_drilldown.xlsx`, `price_drilldown.png`.

## 10. Where 25+ rubric criteria come from

* District contributions (mix + price) for ~8–12 districts; property-type contributions (4); delta counts; leaf; decision;
  alternative blame.

## 11. Golden-output checklist

* Deltas applied by status; Category A; residential types; mean decomposition; decision per rule.

## 12. Build notes (scope tuning)

* Choose a region where a Category B portfolio transfer and a mix shift toward flats both exist; confirm Traps A–C each point
  to a different leaf.
* Price Paid files are re-published; archive the exact files used and their download dates.

# ET34 — Explaining a county's wage jump with QCEW: hierarchy levels, ownership codes and suppressed children

| Field | Value |
|---|---|
| Domain | Economic development / labor-market analysis / official statistics |
| Objective family | Root-Cause Analysis |
| Task shape | 12 · Drill-down to one leaf (supersector → sector → 3-digit industry) |
| Core technique | Navigating a coded aggregation hierarchy (aggregation-level and ownership codes); residual "not disclosed" children from published parents; shift-share decomposition of an average (mix vs within-industry rate) |
| Trap family (honest data) | Summing across hierarchy levels; own_code 0 for a private-sector question; suppressed zeros taken as true; mean of average wages |
| Primary sources | BLS Quarterly Census of Employment and Wages (annual averages by area and industry), QCEW field layouts and code tables |

## 1. The real-world project

A county economic-development office must explain to its board why **private-sector average weekly wage** rose sharply
from 2022 to 2023 — real wage growth in some industry, or a shift in employment toward high-paying industries? The analyst
downloaded the county's QCEW file, summed every row with private ownership, and drilled into "the fastest-growing
industry". The story didn't survive the first board question.

## 2. The business decision (one deterministic recommendation)

**Which 3-digit NAICS industry is the leaf of the drill-down — the largest contributor to the change in county private
average weekly wage after separating mix from rate — and which industry desk owns it?**

Rules (analysis standard):

* County file, annual averages (`qtr = A`), `own_code = 5` (private), years 2022 and 2023.
* Levels: county private total (aggregation level 71) → supersectors (73) → NAICS sectors (74) → 3-digit (75). Only rows
  of the level being analysed are used at each step.
* Average weekly wage at any node = total annual wages ÷ (annual average employment × 52).
* Suppressed children (`disclosure_code = N`): form one residual child per parent = parent − Σ disclosed children (for both
  employment and wages); the residual can be chosen as a branch but cannot be drilled further.
* Decomposition at each level: ΔW = Σ (Δshare_i × W_i,2022) [mix] + Σ (share_i,2023 × ΔW_i) [rate]; drill into the child
  with the largest **rate** contribution; stop at 3-digit.
* Owner mapping (folder): supersector → industry desk.

## 3. Why this gets overlooked in real projects

* QCEW files contain every hierarchy level and ownership code in one table; `groupby(...).sum()` over all private rows counts
  each job several times.
* `own_code 0` ("total covered") is the default headline and includes government.
* Suppressed cells are stored as zeros with a flag; treating them as zeros makes children disagree with parents and pushes
  wage changes into the wrong branch.
* "Average of average weekly wages" is a mean of ratios.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1 | `2022.annual.by_area/<county>.csv` | CSV | ~2–6k | BLS QCEW | U.S. Gov public domain | 2022 county data, all levels |
| 2 | `2023.annual.by_area/<county>.csv` | CSV | ~2–6k | BLS QCEW | Public domain | 2023 county data |
| 3 | `2023.annual.singlefile.csv` (state filter) | CSV | ~0.5–2M | BLS QCEW | Public domain | Cross-check / context |
| 4 | `agglevel_titles.csv` | CSV | ~100 | BLS QCEW | Public domain | Aggregation codes |
| 5 | `ownership_titles.csv` | CSV | ~10 | BLS | Public domain | Ownership codes |
| 6 | `industry_titles.csv` | CSV | ~2.5k | BLS | Public domain | NAICS titles |
| 7 | `qcew_annual_layout.pdf` | PDF | — | BLS | Public domain | Field definitions, disclosure |
| 8 | `qcew_county_2022_2023.xlsx` (BLS county high-level tables) | XLSX | ~3k | BLS | Public domain | Published totals check |
| 9 | `naics2022_changes.pdf` | PDF | — | Census/BLS | Public domain | NAICS 2022 notes (context) |
| 10 | `analysis_standard.pdf`, `owner_mapping.json` | PDF/JSON | — | Task author | — | Rules, owners |

## 5. Deterministic solution path

1. Filter `own_code 5`, `qtr A`, county; separate rows by aggregation level.
2. At each level: build children of the chosen parent; add residual child for suppressed data; compute shares and wages
   per year; decompose; pick the largest rate contributor.
3. Repeat to 3-digit (or stop at a residual); map owner.
4. Verify that level totals reconcile exactly to the parent at each step.
5. Contrast: all-levels sum; own_code 0; suppressed-as-zero.

## 6. The traps

**Trap A — summing across levels.** Employment multiplied; wage levels distorted; wrong top branch.

**Trap B — own_code 0.** Government pay raises leak into the "private" story.

**Trap C — suppressed as zero.** Children don't reconcile; the drill goes to the wrong sector.

**Trap D — mix as rate.** Fast-growing high-wage industry blamed although within-industry wages barely moved.

## 7. Why the data is honest

QCEW is a near-census of covered employment; hierarchy and disclosure codes are documented; residual construction from
published parents is standard practice.

## 8. Draft task prompt (prose)

> The board wants to know what drove the county's private-sector average weekly wage from 2022 to 2023. Following our
> analysis standard, separate mix from rate at each level from supersector down to 3-digit industry, follow the largest
> rate contribution, and tell me the industry at the end of the path and the desk that owns it. Produce
> `wage_drilldown.xlsx` with one sheet per level (children incl. any not-disclosed residual, shares, wages, mix and rate
> contributions, reconciliation to the parent) and `wage_drilldown.png`, a three-panel contribution chart with the chosen
> path highlighted. On the first sheet, give the leaf, its rate contribution in dollars per week, the owner, and how much of
> the total change was mix.

## 9. Deliverables

* `wage_drilldown.xlsx`, `wage_drilldown.png`.

## 10. Where 25+ rubric criteria come from

* Contributions at each level (≈10 supersectors, ~5 sectors, ~5 3-digit) split mix/rate; county ΔW; leaf; owner; mix share.

## 11. Golden-output checklist

* Level-specific rows; private only; residual children; exact reconciliation; decision stated.

## 12. Build notes (scope tuning)

* Pick a county with a big mix shift (e.g. a new high-wage employer) and some suppressed children on the drill path; confirm
  Trap C or D changes the leaf.
* Verify aggregation-level codes for county files in the BLS code table you include.

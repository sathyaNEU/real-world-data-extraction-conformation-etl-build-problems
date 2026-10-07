# P22 — Pricing a parametric drought cover from GHCN-Daily: tenths of millimetres, quality flags and weekend totals

| Field | Value |
|---|---|
| Domain | Agricultural (re)insurance / parametric risk transfer / climate data engineering |
| Objective family | Experiment & Causal Analysis (rule replayed on labeled history) |
| Task shape | 08 · Rule replayed on history (burn cost → technical premium) |
| Core technique | Fixed-width climate record parsing; unit scaling; quality-flag and measurement-flag semantics; multi-day accumulation (MDPR/DAPR) handling; contractual fallback-station hierarchy |
| Trap family (honest data) | Values used without ÷10; -9999 used as a value or as zero; QC-flagged values kept; multi-day totals ignored |
| Primary sources | NOAA NCEI GHCN-Daily (.dly / by-station CSV), station metadata and inventory, GHCN-D readme |

## 1. The real-world project

A reinsurer prices a **parametric drought cover** for a farmers' cooperative: cumulative June–August rainfall at a named
station, with a daily cap of 40 mm (so a single storm cannot "fix" a drought). Payout starts when the season's index
falls below a trigger and reaches the limit at an exit. Pricing replays the contract over 1991–2023 ("burn analysis").
The first replay paid out in 17 of 33 seasons — an implausible frequency for the region.

## 2. The business decision (one deterministic recommendation)

**What technical premium should be quoted for the 2024 season** = (mean annual payout over 1991–2023) × 1.25 loading,
rounded to the nearest $100?

Contract and pricing rules (term sheet in the folder):

* Index = Σ over 1 Jun–31 Aug of min(daily PRCP, 40 mm) at the primary station.
* GHCN-D PRCP is in **tenths of mm**; `-9999` = missing; a non-blank **QFLAG** means the value failed QC and is treated as
  missing; MFLAG `T` (trace) counts as 0; MFLAG `P` ("missing presumed zero") counts as 0.
* Multi-day totals: where `MDPR` reports an accumulation over `DAPR` days with the corresponding PRCP days missing, the
  accumulation is spread evenly across those days before applying the daily cap.
* A missing day (after the rules above) is filled from the first available station in the fallback list (same day,
  same rules). If more than 10 days remain missing in a season, the season is void (no payout, excluded from the mean).
* Trigger 160 mm, exit 80 mm, limit $250,000; payout = limit × (trigger − index)/(trigger − exit), bounded [0, limit].

## 3. Why this gets overlooked in real projects

* Fixed-width `.dly` files look numeric; the ×0.1 scale is documented only in the readme.
* `-9999` survives `sum()`; or analysts `fillna(0)` and convert missing data into drought.
* QC flags are a single character per day in a 31-day row; they get dropped on reshape.
* Cooperative observers often report one accumulated total after a weekend (MDPR/DAPR); PRCP is missing for those days,
  so ignoring MDPR removes real rain and manufactures dry seasons.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1 | `USC00xxxxxx.dly` (primary) | Fixed-width text | ~1.5k month-rows (≈45k days) | NOAA NCEI GHCN-Daily | U.S. Gov public domain | Daily records |
| 2–4 | `USC00yyyyyy.dly`, … (3 fallback stations) | Fixed-width text | ~45k days each | NOAA NCEI | Public domain | Fallbacks |
| 5 | `USC00xxxxxx.csv` (by-station CSV) | CSV | ~100k+ rows (all elements) | NOAA NCEI GHCN-D by_station | Public domain | Same data, long format |
| 6 | `ghcnd-stations.txt` | Fixed-width | ~125k | NOAA NCEI | Public domain | Coordinates, names |
| 7 | `ghcnd-inventory.txt` | Fixed-width | ~750k | NOAA NCEI | Public domain | Element coverage |
| 8 | `ghcnd_readme.txt` | Text | — | NOAA NCEI | Public domain | Units, flags, MDPR/DAPR |
| 9 | `term_sheet.pdf` | PDF | — | Task author | — | Contract rules |
| 10 | `fallback_hierarchy.json` | JSON | 4 | Task author | — | Station order |
| 11 | `cooperative_loss_years.xlsx` | XLSX | ~33 | USDA NASS county yield (public) | Public domain | Basis-risk sanity check (not in pricing) |

## 5. Deterministic solution path

1. Parse `.dly` into long format with VALUE, MFLAG, QFLAG, SFLAG; scale PRCP by 0.1.
2. Apply missing/QC/trace/presumed-zero rules; distribute MDPR over DAPR days where PRCP is missing.
3. Fill remaining gaps from fallback stations by priority; count residual missing; void seasons as required.
4. Compute the capped index per season, payout per season, mean over non-void seasons, premium.
5. Contrast with naive replay (no scaling/flags/MDPR) to show payout frequency inflation.

## 6. The traps

**Trap A — no ÷10.** Index 10× too large; no payouts at all → premium near zero.

**Trap B — missing as zero.** Seasons with gaps become droughts; payouts inflate.

**Trap C — QC flags ignored.** Flagged outliers (e.g. spurious large values) kill payouts in genuinely dry seasons.

**Trap D — MDPR ignored.** Weekend accumulations vanish; many false payouts.

**Trap E — cap after distribution vs before.** Capping an un-distributed multi-day total at 40 mm understates rain.

## 7. Why the data is honest

GHCN-Daily values and flags are NOAA's quality-controlled archive with fully documented conventions; the multi-day
reporting is how cooperative observers actually work.

## 8. Draft task prompt (prose)

> Price the 2024 drought cover using the term sheet in the folder: replay the contract over every season from 1991 to
> 2023 at the primary station, applying the data rules and fallbacks exactly, and give me the technical premium. Produce
> `burn_analysis.csv` with one row per season (days observed, filled, missing, multi-day accumulations used, capped
> index, payout, void flag), and `index_history.png`, the seasonal index as bars with the trigger and exit lines and the
> paying seasons highlighted. Then a one-page `pricing_note.pdf` that leads with the premium, gives the mean payout and
> payout frequency, and shows how the premium would change if missing days had been treated as dry.

## 9. Deliverables

* `burn_analysis.csv` (33 rows), `index_history.png`, `pricing_note.pdf`.

## 10. Where 25+ rubric criteria come from

* 33 seasonal index/payout cells (spot-check ~15), mean payout, frequency, premium, void seasons, missing-as-dry variant.

## 11. Golden-output checklist

* Scaled values; flags honoured; MDPR distributed; fallbacks; voids; premium stated.

## 12. Build notes (scope tuning)

* Select a COOP station with regular MDPR use, a few QC-flagged summer values, and 1–3 seasons near the trigger; confirm
  the naive replay at least doubles payout frequency.
* Pick trigger/exit relative to the station's climatology (e.g. ~70% and ~35% of median season rainfall).

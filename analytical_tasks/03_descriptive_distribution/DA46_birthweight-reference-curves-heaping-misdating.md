# DA46 — Reference percentiles from heaped, misdated records: clean the implausible tail before you cut

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Building reference distributions (size curves, normal ranges, growth benchmarks) from operational records where some units are mis-recorded (wrong category or period) and values heap at round numbers |
| Domain | Maternal and child health |
| Task shape | 14 · Cuts of a distribution (10th and 90th percentiles of birthweight by completed gestational week 24–42 for singleton births; the small-for-gestational-age threshold adopted for a screening programme) |
| Core method | Exclusion of biologically implausible birthweight-for-gestational-age combinations (Alexander et al. criteria: outside ±4 SD of a provisional fit or the memo's published bounds), use of the obstetric estimate of gestation; smoothing of percentiles across weeks (the memo's LMS-free method: weighted quantile regression on week with natural splines) |
| Analytical stump | Misdated pregnancies place term-sized babies at 28–32 weeks, inflating the upper and lower percentiles at preterm weeks; heaping at 40 weeks and round grams creates steps. Raw week-by-week percentiles produce SGA thresholds that are too high at preterm weeks and erratic overall |
| Primary sources | CDC/NCHS natality public-use microdata (birth certificate data) |

## 1. The real-world situation

A state's newborn screening programme flags babies below the 10th percentile of birthweight for gestational age (SGA). Its analyst computed
raw percentiles by week from one year of national natality microdata. Neonatologists found the preterm thresholds implausibly high — many
healthy preterm babies were flagged — because misdated pregnancies contaminate the preterm weeks.

## 2. The decision (one deterministic recommendation)

**The SGA threshold table (10th percentile, grams, rounded to the nearest 10 g) for weeks 24–42, and the 90th percentile table, after cleaning
and smoothing as specified.**

Rules (screening memo):

* Data: natality public-use file for the year in the memo; singleton live births; US residents; plausible birthweights 500–6,000 g.
* Gestation: obstetric estimate (`OEGest_Comb`), completed weeks 24–42.
* Implausibility exclusion: within each sex and week, exclude records outside the bounds in `alexander_bounds.csv` (published bounds per week).
* Percentiles: weighted (equal weights) quantile regression of birthweight on natural cubic spline of week (knots in memo) for τ = 0.10, 0.90,
  separately by sex; thresholds read at integer weeks; table = average of sexes (memo) or by sex if requested.
* Report raw percentiles for contrast.

## 3. Why capable analysts get it wrong

* Raw percentiles per week are straightforward with millions of records.
* Gestational-age errors are concentrated in preterm weeks, where they dominate tails.
* LMP-based gestation was replaced by the obstetric estimate; the choice changes contamination.
* Heaping causes week-to-week jumps; smoothing is required.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `Nat<yyyy>PublicUS.c<date>.r<date>.txt` | Fixed-width text | ~3.6M births | CDC/NCHS Vital Statistics Online | U.S. Gov public domain | Birth records |
| 2 | `UserGuide<yyyy>.pdf` | PDF | — | CDC/NCHS | Public domain | Layout, variable definitions |
| 3 | `alexander_bounds.csv` | CSV | ~40 | From Alexander et al. 1996 (cite) | Cite | Plausibility bounds |
| 4 | `spline_knots.json` | JSON | — | Task author | — | Smoothing spec |
| 5 | `screening_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `analyst_raw_percentiles.xlsx` | XLSX | 19 | Task author | — | Raw thresholds |
| 7 | `fenton_or_intergrowth_reference_citation.pdf` | PDF | — | Cite | Cite | External reference curves (context) |
| 8 | `natality_extract.parquet` | Parquet | ~3.4M | Derived | Public domain | Relevant fields |

## 5. Deterministic solution path

1. Parse fixed-width fields; filters; obstetric gestation.
2. Apply plausibility bounds; counts excluded by week.
3. Quantile regression with splines by sex; thresholds at weeks; averaging.
4. Contrast with raw percentiles.

## 6. Wrong paths (method errors, not misreadings)

**A — raw weekly percentiles.** Contaminated preterm tails.

**B — LMP-based gestation.** More misdating.

**C — no plausibility exclusion but smoothing.** Smooths contaminated values.

**D — including multiples.** Lower weights shift percentiles.

## 7. Why the stump is analytical, not semantic

Fields, bounds and smoothing are specified. The trap is measurement error in the conditioning variable and heaping.

## 8. Draft task prompt (prose)

> Build the SGA threshold table for our screening programme from national natality data as the screening memo specifies: clean implausible
> combinations, use the obstetric estimate, and smooth percentiles across weeks. Provide `sga_thresholds.csv` (week: P10, P90 cleaned/smoothed and
> raw, exclusions), `percentile_curves.png`, and a one-page `threshold_table.pdf`.

## 9. Deliverables

* `sga_thresholds.csv`, `percentile_curves.png`, `threshold_table.pdf`.

## 10. Where 25+ rubric criteria come from

* 19 weeks × P10 = 19; P90 at 6 weeks; exclusion counts; contrast.

## 11. Golden-output checklist

* Filters; gestation field; bounds; quantile regression; reading thresholds; rounding.

## 12. Build notes (scope tuning)

* Confirm raw P10 at 30 weeks exceeds the cleaned value by ≥ 150 g.

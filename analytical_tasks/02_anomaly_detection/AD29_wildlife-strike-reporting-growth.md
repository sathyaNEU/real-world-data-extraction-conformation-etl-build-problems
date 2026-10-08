# AD29 — Bird-strike risk by airport: reporting got better, damage did not get worse everywhere

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Airline and airport safety analytics; any voluntary incident-reporting system (bug reports, near-miss reports, security tips) where reporting propensity changes over time |
| Domain | Aviation safety |
| Task shape | 01 · Ranked list under a cap (10 airports for wildlife-hazard reassessment funding) |
| Core method | Use damaging strikes (less sensitive to reporting propensity) per 100,000 aircraft movements; trend test of damaging-strike rate (Poisson regression with movements offset) 2014–2023 versus the national trend; rank airports by excess trend |
| Analytical stump | Total reported strikes rose several-fold nationally because reporting improved, not because hazards grew. Airports with active reporting programmes look worst on raw counts and raw trends. Damaging strikes are consistently reported and, normalised by movements and compared with the national trend, reveal the airports where hazard actually rose |
| Primary sources | FAA National Wildlife Strike Database; FAA Air Traffic Activity Data System (ATADS) airport operations |

## 1. The real-world situation

A safety office funds **10** airports per year to redo their wildlife hazard assessments. Last year's list ranked airports by growth in
reported strikes; several of the top airports had simply launched staff reporting campaigns. The office wants a ranking that reflects
increasing hazard.

## 2. The decision (one deterministic recommendation)

**The 10 airports funded for reassessment, ranked by excess trend in the damaging-strike rate, and the 11th.**

Rules (safety memo):

* Strikes: FAA database records 2014–2023 at U.S. airports with ≥ 50,000 annual movements in every year (ATADS); damaging strike =
  damage level M, M?, S or D (minor or worse) per the database dictionary.
* Rate model per airport: Poisson regression of yearly damaging strikes with log(movements) offset and a linear year term.
* National trend: same model pooled across all eligible airports (one intercept per airport, common year slope).
* Excess trend = airport slope − national slope; standard error from the airport model.
* Eligible: ≥ 20 damaging strikes over the ten years. Rank by the lower 80% bound of excess trend; top 10; report #11.

## 3. Why capable analysts get it wrong

* Total strikes and their growth are the headline numbers in public summaries.
* Reporting propensity varies by airport and time; minor no-damage strikes are the most sensitive to it.
* Movements changed (pandemic drop in 2020–2021); without an offset, rates and trends are distorted.
* Comparing to zero trend instead of the national trend misses the common drift in damaging reports.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `wildlife_strikes_2014_2023.xlsx` | XLSX | ~170k | FAA National Wildlife Strike Database (public download) | U.S. Gov public domain | Strike records |
| 2 | `wildlife_strike_data_dictionary.pdf` | PDF | — | FAA | Public domain | Damage codes, fields |
| 3 | `atads_airport_operations_2014_2023.csv` | CSV | ~5k airport-years | FAA ATADS | Public domain | Movements |
| 4 | `airport_identifier_map.csv` | CSV | ~600 | Task author (FAA LID ↔ ICAO) | — | Join key |
| 5 | `faa_annual_wildlife_report_citation.pdf` | PDF | — | FAA/USDA annual report (cite) | Public domain | Reporting-rate context |
| 6 | `safety_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `last_year_growth_ranking.xlsx` | XLSX | 10 | Task author | — | Previous list |
| 8 | `reporting_program_launch_dates.json` | JSON | ~15 | Task author (public airport announcements) | — | Context |
| 9 | `strike_summary_by_airport_year.parquet` | Parquet | ~3k | Derived | Public domain | Convenience table |
| 10 | `species_groups.csv` | CSV | ~800 | Derived | Public domain | Context |

## 5. Deterministic solution path

1. Filter airports by movements; classify damaging strikes.
2. Fit the national pooled model; fit per-airport models.
3. Excess trend, SE, lower 80% bound; eligibility; rank.
4. Compare with last year's list and with reporting-programme dates.

## 6. Wrong paths (method errors, not misreadings)

**A — all reported strikes.** Reporting campaigns dominate.

**B — no movements offset.** 2020–2021 artefacts.

**C — trend against zero.** National drift attributed to airports.

**D — ranking by point estimate.** Low-count airports dominate.

## 7. Why the stump is analytical, not semantic

Classes, models and ranking rules are specified. The trap is measurement propensity in voluntary reporting and exposure normalisation.

## 8. Draft task prompt (prose)

> Give me the 10 airports to fund for wildlife hazard reassessment using the damaging-strike trend method in the safety memo. Provide
> `airport_trends.csv` (airport: damaging strikes, movements, slope, excess, bound, rank), `trend_comparison.png` (all-strike growth vs
> damaging-strike excess trend per airport), and a one-page `funding_list.pdf` that explains which of last year's airports drop out and why.

## 9. Deliverables

* `airport_trends.csv`, `trend_comparison.png`, `funding_list.pdf`.

## 10. Where 25+ rubric criteria come from

* 10 airports + #11; national slope; slopes and bounds for 8 airports; overlap with last year; eligibility exclusions.

## 11. Golden-output checklist

* Damage classification; movement filter; offset models; excess trend; bound; ranking.

## 12. Build notes (scope tuning)

* Confirm at least four of last year's top-10 fall out under the damaging-strike method.
* Record the database download date; records are added retroactively.

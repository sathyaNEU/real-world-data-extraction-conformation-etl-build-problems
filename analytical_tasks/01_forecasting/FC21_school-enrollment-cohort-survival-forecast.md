# FC21 — Do we build another elementary school? Enrollment moves with birth cohorts, not with a trend line

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Capacity planning driven by cohort flows (school districts; analogous to seat/facility planning in large employers) |
| Domain | Public education / facilities planning |
| Task shape | 02 · Forecast across many periods (5 school years × grades → one committed K–5 capacity figure) |
| Core method | Cohort-survival (grade-progression ratio) projection with kindergarten from births five years earlier; ratio averaging over a stated window |
| Analytical stump | A linear trend on total enrollment ignores that the cohorts already in the pipeline (and the births that will become kindergarteners) are known; falling births five years ago guarantee smaller entering classes regardless of the recent trend |
| Primary sources | NCES Common Core of Data (membership by grade), CDC WONDER natality (births by county) |

## 1. The real-world situation

A growing suburban district must decide whether to build a new elementary school for 2028–29. A consultant fitted a linear trend
to ten years of total K–12 enrollment and projected 9% growth in elementary enrollment. The demographer on the board pointed out
that county births fell sharply after 2017 — those children enter kindergarten from 2022–23 onward.

## 2. The decision (one deterministic recommendation)

**Projected K–5 enrollment in 2028–29 and whether it exceeds current K–5 capacity (build / don't build).**

Rules (planning memo):

* District membership by grade (K–12) from CCD LEA files, fall of 2014 through 2023.
* Grade progression ratio GPR(g) = enrollment in grade g in year t ÷ enrollment in grade g−1 in year t−1; use the mean of the
  ratios for the three most recent transitions (2021→2022, 2022→2023, and 2020→2021 is excluded as pandemic-affected — use
  2019→2020 instead).
* Kindergarten in fall Y = county births in calendar year Y−5 × birth-to-K ratio, where the ratio = mean over falls 2019, 2022,
  2023 of K(Y) ÷ births(Y−5).
* Births for 2019–2023 come from CDC WONDER (final data).
* Project grades K–12 for falls 2024–2028; K–5 total in fall 2028; build if it exceeds capacity in the memo.

## 3. Why capable analysts get it wrong

* Trend lines are the default for "enrollment over time" and look reasonable in a growing district.
* The pipeline (children already enrolled and already born) determines most of the next five years; trends ignore it.
* Pandemic-year ratios (kindergarten deferrals and returns) distort averages unless the window is chosen deliberately.
* Using statewide births for a district in a fast-changing county mis-states kindergarten inflows.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–10 | `ccd_lea_052_YYYY_membership.csv` (falls 2014–2023) | CSV | 0.5–1M each (LEA × grade × race × sex) | NCES Common Core of Data | U.S. Gov public domain | Membership by grade |
| 11 | `ccd_lea_directory_2023.csv` | CSV | ~19k | NCES | Public domain | District identifiers |
| 12 | `wonder_natality_county_2007_2023.txt` | TSV | ~50k | CDC WONDER Natality | Public domain (WONDER terms) | Births by county and year |
| 13 | `ccd_documentation_membership.pdf` | PDF | — | NCES | Public domain | Field definitions |
| 14 | `district_capacity.json` | JSON | — | Task author (from public facilities plan) | — | K–5 capacity |
| 15 | `planning_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 16 | `consultant_trend_projection.xlsx` | XLSX | ~15 | Task author | — | The trend forecast |

## 5. Deterministic solution path

1. Extract district grade totals for 2014–2023; county births 2009–2023.
2. Compute GPRs for the specified transitions; average; compute the birth-to-K ratio.
3. Project K from births; age cohorts forward with GPRs to 2028.
4. Sum K–5 for fall 2028; compare with capacity; decide.
5. Contrast with the linear trend projection.

## 6. Wrong paths (method errors, not misreadings)

**A — linear trend on totals.** Build decision driven by past growth.

**B — pandemic-year ratios included.** Distorted progression and K ratios.

**C — state births.** Kindergarten inflows off.

**D — ratios averaged across grades.** Ignores grade-specific attrition (e.g. 8→9 transitions).

## 7. Why the stump is analytical, not semantic

Enrollment, births and the projection rules are specified. The trap is modelling time series without using the known cohort
structure — a forecasting-method error.

## 8. Draft task prompt (prose)

> The board needs a build or don't-build recommendation for a new elementary school in 2028–29. Project the district's enrollment
> by grade with the cohort method in the planning memo, using the CCD and natality files in the folder, and compare K–5 in fall 2028
> with current capacity. Provide `enrollment_projection.csv` (grade × fall 2024–2028), `cohort_flow.png` showing births, kindergarten
> and the K–5 total over time with the consultant's trend overlaid, and a one-page `build_decision.pdf` with the decision and the
> margin to capacity.

## 9. Deliverables

* `enrollment_projection.csv`, `cohort_flow.png`, `build_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 12 GPRs + birth-to-K ratio; K for 2024–2028 (5); K–5 totals for 5 years; decision; margin; trend contrast.

## 11. Golden-output checklist

* Correct transitions; pandemic exclusion; county births; projections; decision.

## 12. Build notes (scope tuning)

* Choose a district in a county whose births fell ≥ 10% after 2017 while enrollment grew through 2019; confirm the trend says build
  and the cohort method says don't (or vice versa).
* Verify the CCD file structure for each year (layouts changed around 2016).

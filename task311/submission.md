## Tags

**Domain:** Survey Research & Official Statistics (sample design, allocation and weighting).
**Analytical objective:** Opportunity Sizing & Decision Support.

## 1. Final Recommendation

**Place the Wexcombe Foundation's 1,200 interviews in the Central Valley.** Spread as 15 more completed interviews in each of its 80 sampled areas they remove 44% of the standard error of its 2027 estimate, against 29% in Lakeshore, the runner-up, which would need 27 more interviews per area (2,700 in all) to do better. Not the North, whose error is widest but 89% between areas the boost cannot add, so it gains 4%. Not Lakeshore on a design-effect projection that holds the 2025 weighting effect, which gives the Central Valley only 18%.

## 2. Critical Components

1. Table 2 of the 2025 technical report gives the Central Valley an intraclass correlation of **0.000**: its error sits within areas, where added interviews reach it.
2. The boost adds **15** completed interviews in every Central Valley area, so the supplement areas' take rises from **5** to **20** and the weighting effect falls from **3.4** to **1.6**.
3. The North's between-area variance is **89%** of its 2025 sampling variance, which no interview added inside its areas removes.
4. Projected area by area, the boost removes **44%** of the Central Valley's 2027 standard error and **29%** of Lakeshore's.

## 3. Step-by-Step Solution

1. Read wexcombe_boost_terms_2027.pdf sections 2 and 3: the boost of 1,200 completed interviews goes equally into a region's 2025 sampled areas, and the region is the one whose 2027 standard error (the kind technical report section 4 describes) loses the largest share, both errors reckoned the same way for the 2027 design on the 2025 wave.
2. Took the 2025 complete and proxy interviews with a usable prescription answer from northmark_phms_case_export_2023-2025.csv (North, Southern Uplands, Metro) and ostrander_phms2025_cases.json (Central Valley, Lakeshore), and weighted each by its area's design weight times occupied dwellings over completed interviews from phms_area_weights_2023-2025.csv, joined through moh_survey_area_concordance_2024.xlsx; this reproduces Table 2 of phms_2025_technical_report.pdf.
3. Took each region's intraclass correlation from Table 2 as the between-area part of a household's variance and one minus it as the within-area part.
4. Projected each region's 2027 variance as the sum over its areas of the squared weight share times the between-area part plus the within-area part over the take, with and without 1,200 divided equally among the areas, and took one minus the root of the ratio.
5. Ranked the regions: Central Valley first at 44%, Lakeshore second at 29%.
6. Raised Lakeshore's per-area boost one interview at a time until it removed a larger share than the Central Valley's, comparing unrounded shares: 27 more per area, 2,700 interviews.
7. For 2024, placed each Northmark case in its area by the numbering in force on its assignment date (pre-2024 numbers for cases assigned before 22 April 2024, when the first number the old series never had appears, the new numbers from then), mapped to the current regions through the concordance, and computed each region's completed interviews, weighted estimate and standard error as in step 2.
8. Recommended the Central Valley.

## 4. Deliverable Answers

### boost_region_2027.xlsx

1. Share of each region's 2027 standard error the 1,200 interviews would remove there, whole per cents:
   - Central Valley: 44%
   - Lakeshore: 29%
   - Southern Uplands: 14%
   - Metro: 8%
   - North: 4%
2. Region to fund: Central Valley.
3. Runner-up: Lakeshore.
4. Smallest boost that would remove a larger share of the runner-up's error: 27 more interviews per area (2,700 interviews in all).
5. 2024 on the current regions:
   - North: 702 completed interviews, estimate 24.4%, standard error 3.98 points
   - Central Valley: 2,506 completed interviews, estimate 8.6%, standard error 1.09 points
   - Lakeshore: 1,207 completed interviews, estimate 8.2%, standard error 0.84 points
   - Southern Uplands: 1,164 completed interviews, estimate 12.3%, standard error 1.70 points
   - Metro: 2,522 completed interviews, estimate 8.9%, standard error 0.75 points

### boost_memo_2027.pdf

1. Recommends the Central Valley, with the 44% share, Lakeshore's 29% and the 27 more interviews per area (2,700 in all) Lakeshore would need.
2. Bar chart of the share of the 2027 standard error removed in each region, the Central Valley's bar highlighted, on page 1.

# task118 · Headline squad placement for 2027

## Tags

**Domain:** Marketing & Consumer Research (media audience measurement: news publisher headline testing and click sourcing).
**Analytical objective:** Opportunity Sizing & Decision Support (the squad's realisable 2027 click gain, sized from each desk's planned clicks down to the clicks a new winning headline can still move).

## 1. Final Recommendation

**Place the headline squad with Culture·national for 2027, where it adds 1,250,000 extra article clicks.**

That is 450,000 ahead of the runner-up, Local·metro, at 800,000. Not Local·metro, whose own editors already test the headlines behind 71.1% of its own-surface clicks. Not Business·national, whose clicks mostly arrive on surfaces that show the stored headline. Not Politics·national, which leads on readers, planned clicks and the dashboard's Politics figure, but its own tests shrink to a modest lift. Not Sport·metro, whose raw lift comes from small tests that shrink to almost nothing. Not Sport·national, with a modest lift on a base its own tests already cover in large part. Not on readers, which do not change which headlines the squad can still move.

## 2. Critical Components

1. Culture·national's shrunk winning lift is **1.78%**
2. **50.2%** of Culture·national's 2027 clicks start on Bightline's own surfaces
3. Desk-run tests cover **8.6%** of Culture·national's own-surface clicks and **71.1%** of Local·metro's
4. Culture·national's 2027 own-surface clicks on headlines it does not test are **70,300,000**

## 3. Step-by-Step Solution

1. Took each variant's lift in `headline_tests_archive_2019-2026.csv` as its click-through ratio to the control minus one, with delta-method variance, shrank each test's shipped variant toward one normal prior fitted by maximum likelihood on every variant package of both engines (a kept control counts as zero) and averaged by desk: Culture·national's lift is 1.78%.
2. Back-tested on `headline_squad_change_log.xlsx`, each embedding's lift taken over the squad's tests at that desk in that year (its `tests_run` and observed lift reproduce from the archive): the shrunk lift is within 2% of the realised holdback lift, as a ratio, for 7 of 7 embeddings, against 0 of 7 for raw lift.
3. Classed source codes by where the tested headline renders (`audience_warehouse_field_reference.md`, `canonical_headline`) in `pageviews_by_source_age_2025-10_2026-09.parquet`, which ties to `audience_plan_2027.xlsx`: 50.2% of Culture·national's clicks start on Bightline's own surfaces (home pages, section fronts, the app feed and tabs, related-story links).
4. Joined each test's `owner_staff_id` to `newsroom_staff_list_2026-10-12.xlsx`: every shortlisted-desk test was run by that desk's own staff, on articles carrying 8.6% of Culture·national's own-surface clicks and 71.1% of Local·metro's, gains already inside the plan.
5. Multiplied each desk's shrunk lift by its own-surface clicks on the articles it did not test: Culture·national's 70,300,000 give 1,250,000, runner-up Local·metro 800,000, gap 450,000.
6. Averaged each desk's section in `panel_monthly_audience_2025-10_2026-09.csv` over the twelve months, reading R26-03 and earlier releases on the earlier section list and R26-04 onward, R26-04H included, on the 2026 list as the `panel_reference_workbook.xlsx` release log sets out, each month from its latest release, with the July file's April to June rows set aside as the R26-05 to R26-07 figures that R26-07B replaced, carried again: Culture·national has 1,412,000 monthly readers and 5,052,000 monthly visits.
7. Timed each article's first headline correction in `cms_revisions_web_desks_2025-10_2026-09.csv` (a new note on a published version that went up with a corrected headline, on the same save or a save within ten minutes either side, a live-blog entry's included, per `cms_revisions_export_fields.txt` and `editorial_standards_s7_corrections.pdf` 7.4 and 7.5; carried and put-back notes not new) from the article going live: its `publish_at`, the editor's Brisbane time (10 hours ahead of the UTC saves), when the CMS published a scheduled article before any live save, otherwise its first live save, over stories and live blogs first published October 2025 to September 2026 (live-blog posts, restored copies and documents carried across at the 1 October 2025 migration are not separate articles, a restored copy keeping its original's going live): Culture·national's median is 119 minutes.
8. Recommendation: the squad joins Culture·national for 2027.

## 4. Deliverable Answers

### squad_placement_2027.docx

1. Culture·national, 1,250,000 extra article clicks in 2027
2. Runner-up Local·metro at 800,000, 450,000 behind

### squad_placement_2027.xlsx

1. One row per shortlisted desk, October 2025 to September 2026:
   - Politics·national: 3,180,000 average monthly readers, 13,041,000 average monthly visits, 86 median minutes to first headline correction
   - Sport·metro: 470,000 average monthly readers, 1,550,000 average monthly visits, 55 median minutes to first headline correction
   - Business·national: 1,760,000 average monthly readers, 6,642,000 average monthly visits, 89 median minutes to first headline correction
   - Sport·national: 2,931,000 average monthly readers, 11,626,000 average monthly visits, 47 median minutes to first headline correction
   - Local·metro: 617,000 average monthly readers, 2,359,000 average monthly visits, 102 median minutes to first headline correction
   - Culture·national: 1,412,000 average monthly readers, 5,052,000 average monthly visits, 119 median minutes to first headline correction

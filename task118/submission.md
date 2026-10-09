# task118 · Headline squad placement for 2027

## Tags

**Domain:** Marketing & Consumer Research (media audience measurement: news publisher headline testing and click sourcing).
**Analytical objective:** Opportunity Sizing & Decision Support (the squad's realisable 2027 click gain, sized from each desk's planned clicks down to the clicks a new winning headline can still move).

## 1. Final Recommendation

**Place the headline squad with Culture·national for 2027, where it adds 1,250,000 extra article clicks.**

That is 450,000 ahead of the runner-up, Local·metro, at 800,000. Not Local·metro, whose own editors already test the headlines behind most of its platform clicks. Not Business·national, whose clicks mostly arrive on surfaces that show the stored headline. Not Politics·national, which leads only on the dashboard's vertical lift. Not Sport·metro, whose raw lift is small tests that shrink to almost nothing. Not Sport·national, with a modest lift on a base its own tests already cover in large part. Not on readers, which do not change which headlines the squad can still move.

## 2. Critical Components

1. Culture·national's shrunk winning lift is **1.78%**
2. **50.2%** of Culture·national's 2027 clicks start on Bightline's own surfaces
3. Desk-run tests cover **8.6%** of Culture·national's platform clicks and **71.1%** of Local·metro's
4. Culture·national's 2027 platform clicks on headlines it does not test are **70,300,000**

## 3. Step-by-Step Solution

1. Shrank each test's shipped variant in `headline_tests_archive_2019-2026.csv` toward one normal prior fitted by maximum likelihood on every package (kept control counts as zero) and averaged by desk: Culture·national's lift is 1.78%.
2. Back-tested shrunk lift x planned clicks on `headline_squad_change_log.xlsx`: 7 of 7 embeddings within 2%, against 0 of 7 for raw lift.
3. Classed source codes by where the tested headline renders (`audience_warehouse_field_reference.md`, `canonical_headline`) in `pageviews_by_source_age_2025-10_2026-09.parquet`, which ties to `audience_plan_2027.xlsx`: 50.2% of Culture·national's clicks are platform-drawn.
4. Joined each test's `owner_staff_id` to `newsroom_staff_list_2026-10-12.xlsx`: every shortlisted-desk test was run by that desk's own staff, on articles carrying 8.6% of Culture·national's platform clicks and 71.1% of Local·metro's, gains already inside the plan.
5. Dropped those articles: Culture·national keeps 70,300,000 platform clicks on untested headlines.
6. Multiplied by each desk's shrunk lift: Culture·national 1,250,000, runner-up Local·metro 800,000, gap 450,000.
7. Built readers from `panel_monthly_audience_2025-10_2026-09.csv`, each release read on the `panel_reference_workbook.xlsx` section list it was issued on, and headline corrections from `cms_revisions_web_desks_2025-10_2026-09.csv` as new notes published with a changed headline under `editorial_standards_s7_corrections.pdf` 7.4 and 7.5: Culture·national has 1,412,000 monthly readers and 14 headline corrections.
8. Recommendation: the squad joins Culture·national for 2027.

## 4. Deliverable Answers

### squad_placement_2027.docx

1. Culture·national, 1,250,000 extra article clicks in 2027
2. Runner-up Local·metro at 800,000, 450,000 behind
3. One chart walking each desk from its 2027 clicks through platform-drawn clicks and clicks on headlines the desk does not test to its extra clicks, desks in order of extra clicks, Culture·national marked recommended and Local·metro runner-up, the 450,000 gap labelled, titled with Culture·national

### squad_placement_2027.xlsx

1. One row per desk, October 2025 to September 2026 for readers, corrections and minutes:
   - Culture·national: 1,250,000 extra clicks, 1,412,000 average monthly readers, 0.9 extra clicks per reader, 14 headline corrections, 3.6 per 1,000 articles, 119 median minutes to first headline correction
   - Local·metro: 800,000 extra clicks, 617,000 average monthly readers, 1.3 extra clicks per reader, 34 headline corrections, 4.9 per 1,000 articles, 102 median minutes to first headline correction
   - Business·national: 700,000 extra clicks, 1,760,000 average monthly readers, 0.4 extra clicks per reader, 39 headline corrections, 4.9 per 1,000 articles, 89 median minutes to first headline correction
   - Sport·national: 650,000 extra clicks, 2,931,000 average monthly readers, 0.2 extra clicks per reader, 42 headline corrections, 3.8 per 1,000 articles, 47 median minutes to first headline correction
   - Politics·national: 550,000 extra clicks, 3,180,000 average monthly readers, 0.2 extra clicks per reader, 47 headline corrections, 5.2 per 1,000 articles, 86 median minutes to first headline correction
   - Sport·metro: 100,000 extra clicks, 470,000 average monthly readers, 0.2 extra clicks per reader, 18 headline corrections, 7.3 per 1,000 articles, 55 median minutes to first headline correction
2. 7 of the 7 finished embeddings within 2 per cent

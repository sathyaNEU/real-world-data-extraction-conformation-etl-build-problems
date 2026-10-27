# task118 · Headline squad placement for 2027

## Tags

**Domain:** Product analytics (churn, propensity and uplift modelling: the incremental article clicks a headline-testing squad adds to a news site).
**Analytical objective:** Opportunity Sizing & Decision Support (the squad's realisable 2027 gain, sized from each desk's clicks on Bightline's own pages down to the clicks that are new to the site).

## 1. Final Recommendation

**Place the headline squad with Business·national for 2027, where it adds 500,000 extra article clicks to Bightline.**

That is 100,000 ahead of the runner-up, Local·metro, at 400,000. Not Culture·national: its winning headlines would win the most clicks, 1,250,000, but on its own front and tab, where about four in five views already end in a click, so only 26.9% of them are new to Bightline and it adds 350,000. Not Sport·national or Politics·national, whose smaller lifts are not offset by their reach. Not Sport·metro, whose raw lift comes from very small tests and shrinks to almost nothing.

## 2. Critical Components

1. Business·national's shrunk winning lift is **2.00%**
2. Business·national's own-page clicks on headlines it does not test are **34,900,000**, which its winning headlines would turn into **700,000** won clicks
3. **71.1%** of Business·national's won clicks are new to Bightline, against **26.9%** of Culture·national's and **48.6%** of Local·metro's

## 3. Step-by-Step Solution

1. Took each variant's lift in `headline_tests_archive_2019-2026.csv` as its click-through over the control's minus one, with delta-method variance (the squared ratio of the two click-throughs times the sum of each one's binomial variance over its own click-through squared), shrank each shipped variant toward one normal prior fitted by maximum likelihood on all 10,111 variant packages (the prior's mean and variance those that maximise the normal marginal likelihood of every package's lift, each shipped variant moved toward the mean by the prior's variance over the prior's variance plus its own; a kept control counts as zero) and averaged by desk as the plain mean over its tests: Business·national's lift is 2.00%, and the same rule, averaged over each embedding desk's tests started in the calendar year its embedding began, comes within 2% of 7 of 7 realised holdback lifts in `headline_squad_change_log.xlsx` (raw lift 0 of 7), the lift half of the sign-off in `headline_squad_2027_placement_brief.pdf`.
2. Kept the clicks in `pageviews_by_source_age_2025-10_2026-09.parquet` that start on the pages the brief says a shipped headline replaces the old one on (home pages, section fronts, app feed and tabs, related-story links) and left out every article the archive shows under test: Business·national has 34,900,000.
3. Took each page's click-through in `page_performance_monthly_2025-10_2026-09.csv` as its twelve months of article click-throughs over its page views, and each desk's share of won clicks that is new to Bightline as one minus the click-through of the page each click starts on (its edition's home page, its own front and tab, the app feed, the related links): Business·national 71.1%, Culture·national 26.9%.
4. Back-tested that share on the change log, the click half of the brief's sign-off: planned clicks times the realised lift times the desk's share reproduces 7 of 7 embeddings' extra clicks against the 5 per cent holdback within 2%, where one average share of 57.0% for every desk does so for 2.
5. Multiplied each desk's shrunk lift by its untested own-page clicks and its share new to Bightline: Business·national 500,000, runner-up Local·metro 400,000, gap 100,000.
6. Timed each article's first headline correction in `cms_revisions_web_desks_2025-10_2026-09.csv` from the article going live (the time on its last scheduled save, `publish_at_aest`, when that save still stood when the time came and the CMS published it before any live save, so a time an editor moved later before it came never fired; otherwise its first live save, as for an article set back to draft before its scheduled time and published by hand later), counting a correction on the published version that went up with the corrected headline, the fix and the note on one save or saves up to ten minutes apart, an entry's headline included, a note put back not new, an autosave publishing nothing, live-blog entries and restored copies part of their articles (`editorial_standards_s7_corrections.pdf` 7.3 to 7.5 and 7.8): Business·national's median is 89 minutes, its total 4,109 minutes, 10 within an hour and 6 after more than three hours.
7. Recommendation: the squad joins Business·national for 2027.

## 4. Deliverable Answers

### squad_placement_2027.docx

1. Business·national, 500,000 extra article clicks in 2027
2. Runner-up Local·metro at 400,000, 100,000 behind

### squad_placement_2027.xlsx

1. One row per shortlisted desk, October 2025 to September 2026:
   - Politics·national: 86 median minutes to first headline correction, 5,231 total minutes, 14 first corrections within an hour, 7 after more than three hours
   - Sport·metro: 55 median minutes to first headline correction, 1,342 total minutes, 9 first corrections within an hour, 2 after more than three hours
   - Business·national: 89 median minutes to first headline correction, 4,109 total minutes, 10 first corrections within an hour, 6 after more than three hours
   - Sport·national: 47 median minutes to first headline correction, 2,799 total minutes, 23 first corrections within an hour, 2 after more than three hours
   - Local·metro: 102 median minutes to first headline correction, 21,693 total minutes, 12 first corrections within an hour, 6 after more than three hours
   - Culture·national: 119 median minutes to first headline correction, 2,057 total minutes, 1 first correction within an hour, 5 after more than three hours

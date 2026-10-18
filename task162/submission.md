## Tags

**Domain:** Product Analytics (feature adoption and diffusion modeling: a desktop browser's releases reaching its installs, each install taking the update at its next restart and most Windows installs restarting in the two days after Patch Tuesday).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Staff the triage team with 8 triagers for the first quarter of 2027: its busiest week, a release week, is forecast at about 900 triage items.**
All three of the quarter's releases (12 January, 9 February and 9 March) ship on Patch Tuesday, so the Windows restart wave of the Wednesday and Thursday after falls inside each release week and about 75 per cent of active installs reach the new version in it, against at most 48 per cent in any week of the record. Not last year's busiest first-quarter week scaled for install growth: that week's release shipped a week before Patch Tuesday and met the restart wave only in its second week. Not the record's release-week profile, which the two releases shipped two weeks before Patch Tuesday in autumn 2026 reject out of sample.

## 2. Critical Components

1. About **75 per cent** of active installs reach each first-quarter release in its release week, against at most **48 per cent** in any week of the record.
2. About **79 per cent** of the Windows installs not yet on the newest version update in the two days after Patch Tuesday, against about **12 per cent** a day on other weekdays.
3. The busiest week's forecast is about **900** triage items, 8 triagers at 120 items per triager-week.

## 3. Step-by-Step Solution

1. Counted triage items per tracker_cutover_runbook.docx from old_tracker_export_20251001_20261217.csv: every report in the Monday-to-Sunday Helsinki week of its opened time, duplicates included, the core-security group out; the record's busiest weeks fall in the first two weeks after each release.
2. Read each release's daily reach by platform from version_share_daily.csv as the rise in its major version's share over the share still on older versions: Windows installs update at about 12 per cent of those pending on an ordinary weekday and about 60 and 46 per cent on the Wednesday and Thursday after Patch Tuesday; macOS and Linux have no such days.
3. Fitted each platform's daily triage items on its active installs (active_installs_daily.csv) plus the installs reaching the newest version over the following days: about 1.1 first-use reports for every 10,000 installs reaching a version.
4. Out of sample, the release-week profile of the 13 releases shipped a week before Patch Tuesday missed the third weeks of the 2 releases shipped two weeks before it by more than half, while the restart model fitted on the same releases came within 15 per cent.
5. release_calendar_2025_2027.pdf puts the quarter's releases on 12 January, 9 February and 9 March 2027, each a Patch Tuesday, so the restart wave falls inside each release week and about 75 per cent of active installs reach the version in it.
6. Projected each platform's active installs from the same weeks a year earlier and the last eight weeks' growth of 3.9 per cent, and added the baseline and the first-use reports by week: the busiest week, a release week, comes to about 900 items.
7. Divided by 120 and rounded up per staffing_plan_q1_2027.eml: 8 triagers.

## 4. Deliverable Answers

### triage_staffing_q1_2027.xlsx

1. Triagers for the first quarter of 2027: 8.
2. Busiest week's forecast triage items, to the nearest 100: 900.
3. Parallel run, by the week the reports were filed (Monday to Sunday, Helsinki time), whole items:
   - 2 to 8 November 2026: 109 with no triage action within 24 hours of being filed, 319 closed by the end of the run
   - 9 to 15 November 2026: 101 with no triage action within 24 hours of being filed, 262 closed by the end of the run
   - 16 to 22 November 2026: 45 with no triage action within 24 hours of being filed, 119 closed by the end of the run
   - 23 to 29 November 2026: 85 with no triage action within 24 hours of being filed, 76 closed by the end of the run
4. The run's triage items by the component group they arrived in, whole items:
   - Rendering and Layout: 451
   - Graphics and Media: 136
   - Networking: 109
   - Script and Web APIs: 169
   - Browser Interface: 468
   - Extensions: 75
   - Developer Tools: 70
   - Platform and Updates: 55

### parallel_run_triage.svg

5. Grouped bar chart titled "Parallel run on the new tracker, 2 to 29 November 2026", one pair of labelled bars per week: the items with no triage action within 24 hours of filing and the items closed by the end of the run.

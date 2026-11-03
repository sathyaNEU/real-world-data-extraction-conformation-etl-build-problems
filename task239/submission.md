# task239 submission

## Tags

**Domain:** Psychology & Behavioral Science (psychometric measurement and scale validation: the annual structure check of a team climate index that a parcels company's staff survey reports per team, each item's loading on the factor the items share at team level).
**Analytical objective:** Data Quality Monitoring & Alerting (which items the index carries into the next survey after its yearly check on whether each item still measures the team property it reports).

## 1. Final Recommendation

**Keep ten of the twelve items, TC01 to TC10, in the Team Climate Index for the 2028 Staff Voice survey, and withdraw TC11 and TC12.**

TC11 and TC12 load under 0.25 on the factor the twelve items share at team level, far below the standard's 0.75 line, while every other item loads 0.80 or more. Not eight items, which one factor fitted to the team means gives: each team mean also carries the members' own covariance across the items, divided by the team's number of returns, so the two team-practice items, TC09 and TC10, on which whole teams differ while one member's answers barely move with the rest, fall below the line there and only there. Not ten items with TC09 and TC10 withdrawn, which dividing each correlation of the team means by the square root of the two items' team-mean reliabilities gives: that correction rescales each item's variance but leaves the members' covariance between items in the means, and lifts TC11 and TC12 instead.

## 2. Critical Components

1. TC09 and TC10, the two team-practice items, load **0.80 or more** at team level, as TC01 to TC08 do.
2. TC11 and TC12 load **under 0.25** at team level.

## 3. Step-by-Step Solution

1. Built the returns that count under section 3 of lfp_wi_sv03_measurement_standard_2027.pdf: sessions submitted by the close in lfp_sv27_platform_sessions.csv (a session a tablet re-sent with the same tablet_ref once), forms in lfp_sv27_paper_scans.csv scanned by 8 October with an answer, and each member once, at the return received last, the member found through the personal link's code, the code typed on a tablet and the pack each form was posted in (lfp_sv27_paper_packs.csv): 11,482 returns.
2. Placed each return in its team under section 3.4: personal links by their September code; tablet returns started before the tablets' second team list load on 13 September (lfp_sv27_site_tablet_log.csv) and paper packs by their printed code read through lfp_hr_reorganisation_map_2027-09-01.csv, a split team's code reaching no single team.
3. Kept the 1,016 teams with five or more returns that count (section 5.1) and their 8,323 returns that answer all twelve items on the scale, scored as section 2 sets out (TC04 and TC07 turned round).
4. Split the items' covariance into the pooled within-team covariance and the between-team covariance (the scaled between-team matrix less the pooled within-team matrix) and fitted one common factor to the between-team correlations by principal axis (section 4.2): TC01 to TC10 load 0.80 or more, 0.9 at one decimal, and TC11 and TC12 under 0.25 in size.
5. Applied the 0.75 line (section 4.3): ten items stay for 2028, TC11 and TC12 are withdrawn.
6. Took each team's development plan in lfp_sv27_dashboard_plans_2027-11-19.xlsx at its latest version (an earlier version is replaced, as lfp_staff_voice_2027_dashboard_methodology.docx sets out).
7. Read each target saved up to 5 November, which the export holds as a number, as the item at that row of the team's page (the team's items from its lowest percent favourable to its highest, over all the team's returns that count, ties in Table 1 order); a target saved from 8 November carries its item code.
8. Counted, for each item, the plans that target it and those whose status is Agreed (answer 2 for the workbook).

## 4. Deliverable Answers

### lfp_tci_structure_check_2027.xlsx

1. Each item's team-level loading, to one decimal place, and decision:
   - TC01 (It is safe to take a risk in this team): 0.9, stays
   - TC02 (I can raise a problem in this team without worrying how it will be received): 0.9, stays
   - TC03 (People in this team value the skills I bring): 0.9, stays
   - TC04 (In this team, people are sometimes blamed when something goes wrong): 0.9, stays
   - TC05 (I can ask colleagues in this team for help when I need it): 0.9, stays
   - TC06 (My views are listened to in this team): 0.9, stays
   - TC07 (It is difficult to disagree openly in this team): 0.9, stays
   - TC08 (I am treated with respect by the people I work with): 0.9, stays
   - TC09 (This team meets regularly to review how we are working): 0.9, stays
   - TC10 (New starters in this team are given time to learn how things are done): 0.9, stays
   - TC11 (I am able to do my job to a standard I am pleased with): 0.0, withdrawn (any value from -0.2 to 0.2, of either sign)
   - TC12 (Most days I go home feeling I have done a good job): 0.0, withdrawn (any value from -0.2 to 0.2, of either sign)
2. For each item, the team leaders' development plans that target it and how many of those plans their manager has agreed:
   - TC01: 162 plans, 99 agreed
   - TC02: 126 plans, 69 agreed
   - TC03: 77 plans, 40 agreed
   - TC04: 163 plans, 96 agreed
   - TC05: 45 plans, 24 agreed
   - TC06: 103 plans, 51 agreed
   - TC07: 149 plans, 82 agreed
   - TC08: 28 plans, 20 agreed
   - TC09: 132 plans, 77 agreed
   - TC10: 143 plans, 78 agreed
   - TC11: 87 plans, 42 agreed
   - TC12: 81 plans, 39 agreed

### lfp_tci_items_2028.pptx

3. One slide for the executive team: the ten items that stay and TC11 and TC12 withdrawn, with each item's team-level loading charted against the 0.75 line and TC11 and TC12 marked.

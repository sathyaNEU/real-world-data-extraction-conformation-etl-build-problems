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
3. Kept the 1,016 teams with five or more returns that count (section 5.1) and their 8,323 returns that answer all twelve items on the scale, scored as section 2 and lfp_staff_voice_2027_codebook.xlsx set out (TC04 and TC07 turned round).
4. Split the items' covariance into the pooled within-team covariance and the between-team covariance (the scaled between-team matrix less the pooled within-team matrix) and fitted one factor to the between-team correlations (section 4.2): TC01 to TC10 load 0.80 or more, TC11 and TC12 under 0.25.
5. Applied the 0.75 line (section 4.3): ten items stay for 2028, TC11 and TC12 are withdrawn.
6. Counted each channel's returns that count, those in no team the dashboard reports, those in a reported team leaving an item without an answer on the scale, and those the check used.
7. Counted each item's answers on the scale and its favourable answers over every return that counts, as lfp_staff_voice_2027_dashboard_methodology.docx sets out.
8. Placed each reported team in the division it belonged to on 1 September 2027 (lfp_hr_team_register_2027-11-15.csv, the previous division for a team that moved later) and counted the teams and the returns the check used.

## 4. Deliverable Answers

### lfp_tci_structure_check_2027.xlsx

1. Each item's team-level loading and decision:
   - TC01 (It is safe to take a risk in this team): 0.80 or more, stays
   - TC02 (I can raise a problem in this team without worrying how it will be received): 0.80 or more, stays
   - TC03 (People in this team value the skills I bring): 0.80 or more, stays
   - TC04 (In this team, people are sometimes blamed when something goes wrong): 0.80 or more, stays
   - TC05 (I can ask colleagues in this team for help when I need it): 0.80 or more, stays
   - TC06 (My views are listened to in this team): 0.80 or more, stays
   - TC07 (It is difficult to disagree openly in this team): 0.80 or more, stays
   - TC08 (I am treated with respect by the people I work with): 0.80 or more, stays
   - TC09 (This team meets regularly to review how we are working): 0.80 or more, stays
   - TC10 (New starters in this team are given time to learn how things are done): 0.80 or more, stays
   - TC11 (I am able to do my job to a standard I am pleased with): under 0.25, withdrawn
   - TC12 (Most days I go home feeling I have done a good job): under 0.25, withdrawn
2. The 2027 returns by channel:
   - Personal link: 7,793 count, 1,156 outside the teams the dashboard reports, 929 more leave an item without an answer on the scale, 5,708 used by the check
   - Site tablet: 1,975 count, 314 outside the teams the dashboard reports, 215 more leave an item without an answer on the scale, 1,446 used by the check
   - Paper form: 1,714 count, 290 outside the teams the dashboard reports, 255 more leave an item without an answer on the scale, 1,169 used by the check
3. For each item, the company-wide answers on the scale the dashboard counts and how many of them are favourable:
   - TC01: 11,329 answers, 6,824 favourable
   - TC02: 11,342 answers, 7,442 favourable
   - TC03: 11,387 answers, 8,404 favourable
   - TC04: 11,294 answers, 6,262 favourable
   - TC05: 11,419 answers, 8,923 favourable
   - TC06: 11,359 answers, 7,254 favourable
   - TC07: 11,273 answers, 6,070 favourable
   - TC08: 11,415 answers, 9,020 favourable
   - TC09: 11,162 answers, 6,072 favourable
   - TC10: 11,150 answers, 6,613 favourable
   - TC11: 11,374 answers, 7,533 favourable
   - TC12: 11,393 answers, 7,817 favourable
4. By division, the teams the dashboard reports and the returns the check used:
   - Hub Operations: 228 teams, 1,821 returns
   - Linehaul and Fleet: 149 teams, 1,309 returns
   - Customer Service: 103 teams, 781 returns
   - Engineering: 148 teams, 1,140 returns
   - Delivery Operations: 245 teams, 2,060 returns
   - Corporate Services: 143 teams, 1,212 returns

### lfp_tci_items_2028.pptx

5. One slide for the executive team: the ten items that stay and TC11 and TC12 withdrawn, with each item's team-level loading charted against the 0.75 line and TC11 and TC12 marked.

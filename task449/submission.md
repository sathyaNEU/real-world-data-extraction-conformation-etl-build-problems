# task449 submission

## Tags

**Domain:** General Statistics & Data Science, data integration and record linkage (the social care desk's name-and-city account links, corrected for the links that are wrong).
**Analytical objective:** Data Extraction & Conformation (ETL) (six channels' matters, the social care desk's search records and the processor's payment list conformed into the base the planning standard sizes the team on).

## 1. Final Recommendation

**Carry 35 dedicated analysts in Bellcroft's 2027 complaint desk statement of work.**

The sustained base is 950 new matters a week: the 1,450 a week opened from 3 August to 27 September 2026, less the 500 a week arising from Meridel's payment-posting failure, which over 27.5 matters per analyst-week is 34.5, rounded up to 35. Not 40: reading the social care desk's attached accounts as the posters' own puts 36 per cent of its name-and-city matters on the failure, when the matters whose search returned one cardholder show 80 per cent. Not 34: the verified social matters' share, 89 per cent, comes from the posters who chose to verify.

## 2. Critical Components

1. New matters a week in the eight weeks arising from the failure: **500**
2. Name-and-city matters under the four codes arising from the failure: **80 per cent** (**478** of the **597** whose search returned one cardholder)
3. Sustained new matters a week: **950**

## 3. Step-by-Step Solution

1. Took the matters in complaint_matters_2025_2026.csv first opened from Monday 3 August to Sunday 27 September 2026 (the last eight complete weeks before October, WPS-3 3.1), leaving out merged duplicates (WPS-3 2.2): 11,597, or 1,450 a week.
2. Marked the matters under Schedule 7's four codes (7.2) whose confirmed account is on meridel_affected_payments_20260508_10.csv with a posted date, the list's account number read as the BCF reference: 2,081.
3. Joined the social care desk's name-and-city matters under the four codes to social_care_posts_2025_2026.jsonl by matter number: 2,395 matters, each with the number of cardholders its search returned.
4. Of the 597 whose search returned one cardholder, so the attached account is the poster's, 478 carry an affected payment, 80 per cent; inverting the other matters' attachments against the portfolio's 4 per cent affected (bellcroft_card_portfolio_2025_2026.csv, 30 April) gives the same share.
5. Carried 80 per cent to the 2,395 matters (1,920), so 500 new matters a week arise from the failure and the sustained base is 950 a week, 34.5 analysts at 27.5 a week, rounded up to 35 (WPS-3 4.2).
6. Counted the matters open at the close of each month's last day from matter_status_history_2025_2026.csv, a matter open from OPENED or REOPENED until its next CLOSED or MERGED: 720 in January to 8,260 in May and 1,850 in September.
7. Added each month's Bellcroft-program overtime in fenwright_time_bellcroft_site_2026.csv, Marlowby's shifts with the re-sent week counted once, and Treadwell & Oake's shifts from their start and end times less the break (its Hours column is hours and minutes): 670 to 4,120 flex hours a month.
8. Recommendation: carry 35 dedicated analysts in 2027.

## 4. Deliverable Answers

### dedicated_analysts_2027.docx

1. Dedicated analysts for 2027: 35
2. Sustained new matters a week: 950
3. New matters a week in the eight weeks arising from Meridel's May payment-posting failure: 500
4. Matters open at the end of each month of 2026:
   - January: 720
   - February: 730
   - March: 710
   - April: 740
   - May: 8,260
   - June: 5,590
   - July: 3,230
   - August: 2,230
   - September: 1,850
5. Bar chart of the nine month-end counts, one labelled bar per month, after the table in the memo.

### flex_hours_2026.csv

6. Flex hours, overtime and agency together, worked on the desk in each month of 2026:
   - January: 790
   - February: 670
   - March: 760
   - April: 720
   - May: 3,430
   - June: 4,120
   - July: 3,440
   - August: 2,830
   - September: 2,170

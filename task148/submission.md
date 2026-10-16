## Tags

**Domain:** Urban & Regional Science (municipal service demand and resource allocation).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Fund a seasonal fifth call-taker on the Friday and Saturday late shift in July 2027, August 2027 and June 2028: with the four call-takers the FY2028 budget funds, those are the months of fiscal 2028 that fall short of the 90 per cent answering standard.**
July is expected at 88 per cent and August and June at 89, while May and September, the closest above, sit at 91. Not Erlang C, which has every caller wait until answered and puts May to September short; not a patience read off the hang-ups' own waits, which leaves no month short; not fiscal 2026's observed late-shift compliance, which ran with five call-takers and without Halvorsen Township's calls.

## 2. Critical Components

1. Busy time per answered 911 call, answer to Ready, January 2025 to September 2026: **227.0 seconds**.
2. Callers' patience, the total waiting time of every 911 call over the **7,651** calls abandoned: **161.4 seconds**.
3. Expected compliance in the months that fall short: July 2027 **88%**, August 2027 **89%**, June 2028 **89%**.

## 3. Step-by-Step Solution

1. Read acd_call_detail_legacy_2025-01-01_2025-05-16.csv (local time) and i3_call_log_2025-05-13_2026-09-30.jsonl (UTC) as one list of 417,086 911 calls, test calls left out as SOP 2.10 section 2 has it.
2. Busy time: the mean of ready less answered over the answered calls, a position being busy until the call-taker sets Ready (SOP 2.10 section 4.2): 227.0 seconds.
3. Patience: every call's wait (answer or hang-up less presentation) summed and divided by the 7,651 abandoned calls, an answered call's wait counting as time its caller held on: 161.4 seconds.
4. Checked out of sample: with January to June 2025's busy time and patience, each fiscal 2026 hour's calls and the call-takers on floor_roster_2025-01_2026-09.csv, a queue whose callers hang up gives 95.3 per cent against the observed 95.2; Erlang C gives 93.7 and the hang-ups' own waits 96.4.
5. Took the agency's FY2028 rows of tri_county_911_hourly_forecast_fy2027_fy2028.xlsx (SOP 2.10 section 5) for Friday and Saturday 22:00 and 23:00 and Saturday and Sunday 00:00 and 01:00, each night on the forecast of the month it starts (SOP 2.10 section 6).
6. Modelled each hour as a queue of four call-takers whose callers hang up (Erlang A, M/M/4+M) on those calls per hour with that busy time and patience, and took each month's compliance as SOP 2.10 section 3.3 defines it: expected calls answered within 15 seconds over expected calls less those abandoned within 5.
7. July 2027 (88%), August 2027 (89%) and June 2028 (89%) fall below 90 per cent; the other months are 91 to 95 per cent.

## 4. Deliverable Answers

### late_shift_staffing_fy2028.xlsx

1. Months below 90 per cent, for a seasonal fifth call-taker: July 2027, August 2027 and June 2028.
2. Expected answer-time compliance by month, whole per cent:
   - July 2027: 88%
   - August 2027: 89%
   - September 2027: 91%
   - October 2027: 93%
   - November 2027: 94%
   - December 2027: 93%
   - January 2028: 94%
   - February 2028: 95%
   - March 2028: 94%
   - April 2028: 93%
   - May 2028: 91%
   - June 2028: 89%
3. Wireless 911 calls placed from Halvorsen Township that reached the agency in fiscal 2026, answered or not, and of them transferred to Wexley County Emergency Communications:
   - Q1 (July to September 2025): 1,473 reached, 1,304 transferred
   - Q2 (October to December 2025): 1,249 reached, 1,126 transferred
   - Q3 (January to March 2026): 1,104 reached, 1,001 transferred
   - Q4 (April to June 2026): 1,265 reached, 1,154 transferred
4. Share of abandoned 911 calls dialled back within two minutes of the hang-up:
   - January 2026: 54.9%
   - February 2026: 55.3%
   - March 2026: 51.4%
   - April 2026: 53.6%
   - May 2026: 48.3%
   - June 2026: 51.6%

### late_shift_compliance_fy2028.png

1. Bar chart of the twelve months' expected compliance against a dashed 90 per cent line, July 2027, August 2027 and June 2028 in red below it.

## Tags

**Domain:** Urban & Regional Science (municipal service demand and resource allocation).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Fund a seasonal fifth call-taker on the Friday and Saturday late shift in July 2027, August 2027 and June 2028: with the four call-takers the FY2028 budget funds, those are the months of fiscal 2028 that fall short of the 90 per cent answering standard.**
July is expected at 88 per cent and August and June at 89, while May and September, the closest above, sit at 91. Not Erlang C, which has every caller wait until answered and puts May to September short; not one patience for every call, which brings the rest of the week's patient callers onto the late shift and puts May to September short as well; not a patience read off the hang-ups' own waits, which leaves no month short.

## 2. Critical Components

1. Expected compliance in the months that fall short: July 2027 **88%**, August 2027 **89%**, June 2028 **89%**; the closest months above the standard, September 2027 and May 2028, at **91%**.
2. The queue runs on the late shift's own callers' patience, about two minutes, estimated on the late shift's calls alone.

## 3. Step-by-Step Solution

1. Read acd_call_detail_legacy_2025-01-01_2025-05-16.csv (local time) and i3_call_log_2025-05-13_2026-09-30.jsonl (UTC) as one list of 416,621 911 calls, test calls left out as SOP 2.10 section 2.2 has it.
2. Busy time: the mean of ready less answered over the answered calls, a position being busy until the call-taker sets Ready (SOP 2.10 section 4.2): 226.9 seconds.
3. Patience, by segment: every call's wait (answer or hang-up less presentation) summed and divided by the calls that hung up, an answered call's wait counting as time its caller held on. On the late shift's own 15,814 calls (81 hung up) it is 123.2 seconds; at every other hour 587.7; over every call together 576.6.
4. Checked out of sample: with January to June 2025's parameters, the late shift's fiscal 2026 hours hung up on 0.46 per cent of calls; the late shift's own patience predicts 0.34, one patience for every call 0.14 and Erlang C none.
5. Took the agency's FY2028 rows of tri_county_911_hourly_forecast_fy2027_fy2028.xlsx (SOP 2.10 section 5.1) for Friday and Saturday 22:00 and 23:00 and Saturday and Sunday 00:00 and 01:00, each night on the forecast of the month it starts (SOP 2.10 section 6.1).
6. Modelled each hour as a queue of four call-takers whose callers hang up (Erlang A, M/M/4+M) on those calls per hour with the busy time and the late shift's patience, and took each month's compliance as SOP 2.10 section 3.3 defines it: expected calls answered within 15 seconds over expected calls less those abandoned within 5.
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
   - Q1 (July to September 2025): 1,475 reached, 1,326 transferred
   - Q2 (October to December 2025): 1,243 reached, 1,127 transferred
   - Q3 (January to March 2026): 1,104 reached, 1,003 transferred
   - Q4 (April to June 2026): 1,253 reached, 1,160 transferred
4. Share of abandoned 911 calls dialled back within two minutes of the hang-up:
   - January 2026: 55.2%
   - February 2026: 45.1%
   - March 2026: 56.8%
   - April 2026: 52.6%
   - May 2026: 50.3%
   - June 2026: 51.4%

### late_shift_compliance_fy2028.png

1. Bar chart of the twelve months' expected compliance against a dashed 90 per cent line, July 2027, August 2027 and June 2028 in red below it.

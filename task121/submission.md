## Tags

**Domain:** Human Factors & Ergonomics (workload, fatigue and shift analysis).
**Analytical objective:** Root-Cause Analysis.

## 1. Final Recommendation

**The rise in under-triaged medical calls came from the 2026 rotation's quick returns: shifts begun less than eleven hours after the call-taker's previous shift ended.**
From March 2026, 31.1 per cent of the critical or emergent calls taken on those shifts were sent cold, against 10.7 per cent on rested shifts, which ran at 10.2 per cent before March. Not protocol release 13.3, which the rested shifts ran on too while they held. Not the academy graduates, since the veterans' calls rose from 10.4 to 14.5 per cent. Not the call mix, since the March to August rate at the earlier mix is 14.7 per cent.

## 2. Critical Components

1. The under-triage rate was **10.5%** from September 2025 to February 2026 and **14.8%** from March to August 2026.
2. Shifts begun less than eleven hours after the call-taker's previous shift ended were **1.5%** of the shifts worked from September 2025 to February 2026 and **15.8%** of those worked from March to August 2026.
3. From March the under-triage rate was **31.1%** on those shifts and **10.7%** on rested shifts.
4. On rested shifts the rate was **10.2%** before March.

## 3. Step-by-Step Solution

1. Matched each call in cad_medical_calls_2025_2026.csv to its records in epcr_patient_records_2025_2026.csv by incident number (the tablets drop the dash), each call at its most acute patient (QA program 2.2): the under-triage rate was 10.5 per cent before March and 14.8 from March.
2. Placed each call on the shift worked in roster_shifts_worked_2025_2026.csv whose start and end hold its answer time, the CAD login joined to the employee number through call_takers.csv, and took each shift's rest from the end of the call-taker's previous shift worked (the extract starts on 18 August 2025): shifts begun under eleven hours after it were 1.5 per cent of those from September 2025 to February 2026 and 15.8 of those from March to August 2026.
3. Set the other changes against the rested shifts and the calls: on rested shifts, which ran on release 13.3 from 3 March, the rate was 10.2 per cent before March and 10.7 from March; the veterans' calls rose from 10.4 to 14.5 per cent, and at the earlier protocol mix the March to August rate is 14.7.
4. Ask A: took each medical call in cad_medical_calls_2025_2026.csv once (a split CAD incident repeats its call's che_call_id, answer second and call-taker), its processing time from the answer to the earliest assignment in cad_unit_history_2025_2026.csv among its incidents (unit_assigned holds the ambulance now on the incident), and each month's 90th percentile at rank 0.9 times the calls, rounded up (QA program 3).
5. Ask B: took each arrest's primary review in tcpr_arrest_reviews_2025_2026.csv where compressions were coached, reading reviewer QA7's times as minutes and seconds keyed without the colon (QA7's calibrated calls agree with the other reviewer only when so read), the first compression at recording_started plus those seconds, less the CAD's call_answered, and each month's median (QA program 5).
6. Ask C: took the calls in che_call_detail_2025_2026.csv on the 911 trunk groups of centre_reference.xlsx (TG01, TG02, TG03 and TG05, not the 10-digit lines on TG07), leaving out the record of a call passed from one position to another (it arrives the second an earlier record on the same trunk group from the same number was released), answered and not abandoned, and each month's share answered 15 seconds or less after arriving, by the month answered in local time (QA program 4).
7. Named the cause: from March the calls on quick-return shifts were sent cold at 31.1 per cent against 10.7 on rested shifts, so the rise came from the 2026 rotation's quick returns.

## 4. Deliverable Answers

### under_triage_cause_2026.xlsx

1. Cause: the 2026 rotation's quick returns, shifts begun less than eleven hours after the call-taker's previous shift ended (not protocol release 13.3).
2. Under-triage rate: September 2025 to February 2026 10.5%; March to August 2026 14.8%.
3. 90th percentile call processing time, medical calls, seconds:
   - September 2025: 121
   - October 2025: 121
   - November 2025: 122
   - December 2025: 123
   - January 2026: 122
   - February 2026: 122
   - March 2026: 128
   - April 2026: 129
   - May 2026: 129
   - June 2026: 128
   - July 2026: 130
   - August 2026: 130
4. Median time to first compression, cardiac arrest calls, seconds:
   - September 2025: 112
   - October 2025: 121
   - November 2025: 113
   - December 2025: 105
   - January 2026: 119
   - February 2026: 117
   - March 2026: 108
   - April 2026: 128
   - May 2026: 123
   - June 2026: 110
   - July 2026: 114
   - August 2026: 112
5. 911 calls answered within 15 seconds, per cent:
   - September 2025: 92.5
   - October 2025: 92.6
   - November 2025: 92.2
   - December 2025: 90.2
   - January 2026: 90.6
   - February 2026: 90.0
   - March 2026: 92.2
   - April 2026: 92.5
   - May 2026: 92.4
   - June 2026: 92.2
   - July 2026: 92.0
   - August 2026: 92.7

### under_triage_2025_26.png

1. Line chart of each month's under-triage rate, September 2025 to August 2026, the rate stepping up from March 2026.

# task241 submission

## Tags

**Domain:** General Statistics & Data Science (missing data, censoring and measurement error: each project's error rate of a dialer's answering machine detection, measured from what the people it hung up on did next).
**Analytical objective:** Data Quality Monitoring & Alerting (which recurring telephone projects have the dialer's answering machine detection switched off for 2027 because the answering-machine outcomes it records are not trustworthy, with each project's calling-hours exceptions, completed interviews and interviewer hours for the 2027 setup).

## 1. Final Recommendation

**Open six recurring projects in 2027 with answering machine detection switched off: KR-2607 Medicare Care Experience Survey, KR-2622 Farm Operator Survey, KR-2631 Alumni Outcomes Survey, KR-2638 Veterans Health Survey, KR-2644 Small Business Conditions Survey and KR-2651 Child Care Provider Survey; the other seven keep it on.**

On the six, 17 to 32% of the calls the dialer classed as answering machines in 2026 had been answered by a person, against the 2027 policy's one in ten; the other seven ran 2 to 6%. Not the maker's certified 2.1% or the 2025 listening audit's 9 of 400, which describe the pilot's short household greetings and keep every project on. Not the four projects with the highest machine-classed shares, which picks large employers and retired educators for ordinary voicemail.

## 2. Critical Components

1. Each project's share of machine-classed calls answered by a person, measured on its own calls: KR-2604 **3%**; KR-2607 **18%**; KR-2609 **2%**; KR-2615 **4%**; KR-2618 **3%**; KR-2622 **20%**; KR-2626 **4%**; KR-2631 **17%**; KR-2633 **6%**; KR-2638 **18%**; KR-2644 **32%**; KR-2647 **2%**; KR-2651 **29%**.
2. Nearest the limit: KR-2633 at **6%** stays on; KR-2631 at **17%** is the lowest switched off.
3. The pilot, KR-2604, reads **3%**, in line with the 2025 listening audit; people the message reached ring back within a minute of it and no other call from a dialed number reaches the line in the two and a half hours after the dialer's call, so every window from 2 to 120 minutes, counted from the call's start or from its end, gives the same counts and the same shares.

## 3. Step-by-Step Solution

1. Read the twelve exports in dialer_exports (letter codes and US dates to June, words and ISO dates from July) and dropped the day each export repeats from the month before by call id.
2. Collapsed inbound_switch_2026.csv to one call per switch_call_id (its first leg's time and caller), dropped the test calls from extension 6517 and tied each call from a dialed number to the latest outbound call to that number, numbers normalised to ten digits.
3. For each project in project_register_2027.xlsx, divided the share of its machine-classed calls rung back within 20 minutes by the share of its abandoned live answers rung back within 20 minutes.
4. Applied section 3 of dialer_policy_2027.docx: detection off where the share is one in ten or more, six projects; on for the other seven.
5. Calling hours: each answered call's household state from case_records_2026.csv, by the number dialed, else by the case number the dialer wrote from July, else (an appointment number the record lacks, before July) through the calls of the same job under the same case number to its recorded number, the pre-July case numbers restarting in every job; Central time converted with state_time_zones.csv, Arizona on standard time all year; counted calls before 8:00 or from 21:00 local.
6. Completed interviews: the dialer's COMPLETE rows and the inbound calls with COMPLETE on any leg completed in 2026 (an interview counts in 2026 when it was completed in 2026, so the switch log's completes dated 2027 fall outside), each case counted once across the July case-number change (matched to its case record), a supervisor's verification call adding none (policy section 5).
7. Interviewer hours: interviewer_hours_2026_h1.csv (decimal hours) and interviewer_hours_2026_h2.csv (hours.minutes, 4.30 being four and a half hours), each shift's hours shared by each project's talk and wrap time on the interviewer's calls inside the shift, shifts with no calls not charged (policy section 5).
8. Detection is switched off for 2027 on KR-2607, KR-2622, KR-2631, KR-2638, KR-2644 and KR-2651.

## 4. Deliverable Answers

### amd_review_2027.xlsx

1. Each project's 2026 share of machine-classed calls answered by a person (whole per cent) and its 2027 detection:
   - KR-2604 Minnesota Adult Health Survey (landline): 3%, detection on
   - KR-2607 Medicare Care Experience Survey: 18%, detection off
   - KR-2609 Large Employer Benefits Survey: 2%, detection on
   - KR-2615 Statewide Voter Attitudes Poll: 4%, detection on
   - KR-2618 School Parents Survey: 3%, detection on
   - KR-2622 Farm Operator Survey: 20%, detection off
   - KR-2626 Crime Victimization Survey: 4%, detection on
   - KR-2631 Alumni Outcomes Survey: 17%, detection off
   - KR-2633 Cooperative Member Survey: 6%, detection on
   - KR-2638 Veterans Health Survey: 18%, detection off
   - KR-2644 Small Business Conditions Survey: 32%, detection off
   - KR-2647 Retired Educators Survey: 2%, detection on
   - KR-2651 Child Care Provider Survey: 29%, detection off
2. Answered calls in 2026 that rang before 8 am or after 9 pm in the called household's own local time:
   - KR-2604: 181
   - KR-2607: 193
   - KR-2609: 76
   - KR-2615: 175
   - KR-2618: 110
   - KR-2622: 120
   - KR-2626: 147
   - KR-2631: 186
   - KR-2633: 125
   - KR-2638: 178
   - KR-2644: 85
   - KR-2647: 198
   - KR-2651: 124
3. Interviews completed in 2026:
   - KR-2604: 3,488
   - KR-2607: 2,311
   - KR-2609: 1,407
   - KR-2615: 2,745
   - KR-2618: 1,927
   - KR-2622: 1,982
   - KR-2626: 2,305
   - KR-2631: 1,877
   - KR-2633: 2,073
   - KR-2638: 2,034
   - KR-2644: 1,416
   - KR-2647: 1,868
   - KR-2651: 1,971
4. Interviewer hours used in 2026 (one decimal place):
   - KR-2604: 9,114.6
   - KR-2607: 6,666.6
   - KR-2609: 4,427.6
   - KR-2615: 7,496.1
   - KR-2618: 5,430.6
   - KR-2622: 5,475.9
   - KR-2626: 6,478.2
   - KR-2631: 5,502.8
   - KR-2633: 5,836.9
   - KR-2638: 6,118.9
   - KR-2644: 4,235.3
   - KR-2647: 5,623.2
   - KR-2651: 5,418.5

### amd_review_2027.pdf

5. One-page note: detection switched off for KR-2607, KR-2622, KR-2631, KR-2638, KR-2644 and KR-2651 because a tenth or more of their machine-classed calls were people, measured from the calls rung back within minutes against each project's abandoned answers; the certified rate and the listening audit hold only for short household greetings; a bar chart of the projects' shares against the one-in-ten limit.

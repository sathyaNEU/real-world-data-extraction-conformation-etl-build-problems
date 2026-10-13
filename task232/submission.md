# task232 submission

## Tags

**Domain:** Epidemiology & Public Health (disease surveillance and outbreak anomaly detection: attributing a childcare room's enteric cases to the index case's infectious attendance by the incubation range).
**Analytical objective:** Data Quality Monitoring & Alerting (the lateness at which each laboratory feed's SLA alert pages the on-call public health officer once release 4.2 switches on per-feed alerts).

## 1. Final Recommendation

**Set the SLA alert at 12 hours for Coast and Ranges Base Hospital Laboratory, 2 hours for Larkspur Pathology, 12 hours for Halden Pathology, 4 hours for Kestrel Pathology (Queensland), 12 hours for Highfield Pathology Services and 24 hours for the State Enteric Reference Laboratory.**

Each is the longest allowed setting at which the feed's expected secondary cases a year stay at or under 1.00 (0.61, 0.69, 0.81, 0.74, 0.61 and 0.15), and the next longer setting goes over it for every feed but the reference laboratory (1.33, 1.29, 3.54, 1.25 and 1.57), at 7.94 shigellosis, 3.07 STEC infection and 6.98 cryptosporidiosis secondary cases per 1,000 child-hours: the 141 cases in the closed investigations' rooms whose onset falls between the index's first infectious attendance plus the condition's shortest incubation and its last infectious attendance plus the longest. Not every case that fell ill after the index, which still counts the cases its secondary cases and later introductions brought while the follow-up ran two incubation periods past the exclusion, and sets Larkspur, Halden and Kestrel shorter. Not every case the rooms' follow-up records, which also counts the room's cases that fell ill no later than the index and community cases, and sets five of the six feeds shorter. Not only the cases ill before the exclusion, which drops the secondary cases that fall ill an incubation period after the exposure and sets every feed at 24 hours.

## 2. Critical Components

1. Child-hours of contact during the closed investigations' infectious attendance: shigellosis **9,442.03**, STEC infection **1,301.72**, cryptosporidiosis **8,881.78**
2. Secondary cases among room contacts in the closed investigations (onset within the condition's incubation range after the index's infectious attendance): shigellosis **75**, STEC infection **4**, cryptosporidiosis **62**
3. Secondary cases per 1,000 child-hours of contact: shigellosis **7.94**, STEC infection **3.07**, cryptosporidiosis **6.98**
4. Notifications that opened a childcare investigation with a result authorised from 1 October 2023 to 30 September 2026: **80** (base hospital 13, Larkspur 22, Halden 22, Kestrel 11, Highfield 10, reference laboratory 2)

## 3. Step-by-Step Solution

1. For the 140 closed investigations in cc_investigation_register_2021-2026.xlsx, summed the index case's hours at the centre on each day of its infectious attendance times the other children and educators who attended its room that day, from cc_attendance_signin_export.csv, cc_attendance_daily_roll.xlsx and cc_attendance_portal_export.json (CD-ST-07 section 3): 9,442.03 child-hours for shigellosis, 1,301.72 for STEC infection and 8,881.78 for cryptosporidiosis.
2. Kept as the index's secondary cases (GL-CD-11 section 2) the confirmed and probable cases in cc_contact_followup_2021-2026.csv whose onset falls no earlier than the index's first infectious attendance plus the condition's shortest incubation in GL-CD-11's condition table and no later than its last infectious attendance plus the longest: 141 of the 319 the closed investigations record (shigellosis 75, STEC infection 4, cryptosporidiosis 62).
3. Divided each condition's secondary cases by its child-hours (CD-ST-07 section 3): 7.94, 3.07 and 6.98 per 1,000 child-hours.
4. Took the register's investigations with a result authorised from 1 October 2023 to 30 September 2026 (CD-ST-07 section 2): 80 notifications, base hospital 13, Larkspur 22, Halden 22, Kestrel 11, Highfield 10 and reference laboratory 2.
5. For each notification and allowed setting, worked the unit's call had the result reached it at authorisation and that many hours later, and multiplied the booked hours in cc_room_bookings.csv the case would have spent at the centre between the two calls by the room's other attendees that day and the condition's rate, each feed's sum divided by three (CD-ST-07 section 2): 0.61, 0.69, 0.81, 0.74, 0.61 and 0.15 expected secondary cases a year at the chosen settings, and 1.33, 1.29, 3.54, 1.25 and 1.57 at the next longer ones.
6. Set each feed at the longest allowed setting whose expected secondary cases a year do not exceed 1.00 (CD-ST-07 section 2): base hospital 12 hours, Larkspur 2, Halden 12, Kestrel 4, Highfield 12 and reference laboratory 24.

## 4. Deliverable Answers

### elr_sla_thresholds_2026-27.csv

1. SLA lateness, with expected secondary cases a year at that setting and at the next longer one:
   - Coast and Ranges Base Hospital Laboratory (CRBH-MICRO): 12 hours, 0.61 at the setting, 1.33 at the next longer
   - Larkspur Pathology (LARKSPUR): 2 hours, 0.69 at the setting, 1.29 at the next longer
   - Halden Pathology (HALDEN): 12 hours, 0.81 at the setting, 3.54 at the next longer
   - Kestrel Pathology (Queensland) (KESTREL-QLD): 4 hours, 0.74 at the setting, 1.25 at the next longer
   - Highfield Pathology Services (LARKSPUR-HF): 12 hours, 0.61 at the setting, 1.57 at the next longer
   - State Enteric Reference Laboratory (SERL): 24 hours, 0.15 at the setting, no longer setting

### elr_sla_basis_2026-27.xlsx

1. Secondary cases per 1,000 child-hours of contact:
   - shigellosis: 7.94
   - STEC infection: 3.07
   - cryptosporidiosis: 6.98
2. Reports authorised from 1 October 2025 to 30 September 2026, and of them those that first reached the platform more than 24 hours after authorisation:
   - Coast and Ranges Base Hospital Laboratory: 2,377 reports, 12 more than 24 hours late
   - Larkspur Pathology: 3,884 reports, 22 more than 24 hours late
   - Halden Pathology: 2,473 reports, 19 more than 24 hours late
   - Kestrel Pathology (Queensland): 1,041 reports, 8 more than 24 hours late
   - Highfield Pathology Services: 1,167 reports, 11 more than 24 hours late
   - State Enteric Reference Laboratory: 256 reports, 4 more than 24 hours late
3. Shigellosis, STEC infection and cryptosporidiosis cases each feed was the first to notify from 1 October 2025 to 30 September 2026:
   - Coast and Ranges Base Hospital Laboratory: 34
   - Larkspur Pathology: 89
   - Halden Pathology: 47
   - Kestrel Pathology (Queensland): 24
   - Highfield Pathology Services: 29
   - State Enteric Reference Laboratory: 1

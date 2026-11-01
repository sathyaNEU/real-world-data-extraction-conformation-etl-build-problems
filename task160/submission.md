## Tags

**Domain:** Healthcare Delivery & Health Economics (utilization, access and demand forecasting: a remote pharmacy desk's override review volume when a hospital takes a medication alert package live on every adult ward).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Plan for about 300 more override reviews (to the nearest 100) from Quillfield's adult wards in the 13 weeks from Monday 4 January 2027 than the desk would get over those weeks without the go-live.** The QT combination alert adds about 500 reviews; the duplicate PRN opioid alert, answered by removing the new order 49 per cent of the time on the pilot units, takes about 200 of today's reviews off the desk. Not 500: the background log counts the package's own alerts, and a removed order carries no alerts of its own and has no severe interaction alert fire against it later in the stay.

## 2. Critical Components

1. The QT combination alert adds about **500** reviews over the 13 weeks (to the nearest 100): the background log's QT alerts on the wards going live, overridden at the pilot units' 58 per cent.
2. About **200** of today's reviews no longer reach the desk (to the nearest 100): overridden alerts on an order, or fired against an order, that the duplicate PRN opioid alert would have removed at the pilot units' 49 per cent.
3. Net change **+300** reviews (to the nearest 100), on the volume plan's admissions for the 13 weeks.

## 3. Step-by-Step Solution

1. Conformed QRMC_MedAlertHistory_20250101-20261025.csv: mapped the department names used before 9 November 2025 to the rule register's unit codes, dropped the boundary day each quarterly pull repeated, and moved the background log's UTC stamps to Eastern time.
2. On the pilot units (7W, 5E, 8N) over the whole history: 49 per cent of duplicate PRN opioid alerts answered by removing the order, 58 per cent of QT combination alerts overridden.
3. Base period 6 July to 25 October 2026 on the units going live: 1005 QT combination alerts in the background log on orders not removed, times 58 per cent, 578 reviews added.
4. For each of the 3410 overridden high-severity alerts on those units in the base period, the chance it no longer reaches the desk: its own order or its interacting order carries a background duplicate-opioid alert (each removed at 49 per cent), or its own order a QT alert (removed at 42 per cent); 230 reviews lost.
5. Scaled by the volume plan's admissions for the 13 weeks from 4 January 2027 over the census admissions in the base period (8,287 over 9,765): 491 added, 195 lost, net 296, about 300.
6. Desk hours: every queue session closing 1 July to 30 September 2026 Eastern, claim to close (returned sessions included), each given the department of the alert its alert_ref names in the alert history; the point of care follows the bed, and five pairs of wards exchanged wings between 20 July and 14 September.
7. Signed-off reviews: each signed-off task counted as the overridden high-severity alerts on its order at the same signing, by the month and shift of sign-off in Eastern time.
8. Recommended planning for about 300 more reviews in the 13 weeks.

## 4. Deliverable Answers

### msp26_review_forecast_q1_2027.xlsx

1. Net change in override reviews, 13 weeks from 4 January 2027: +300 (QT combination alert +500, current reviews lost -200), to the nearest 100.
2. Desk hours, July to September 2026, nearest whole hour:
   - 4N 4 North Medicine: 26
   - 4S 4 South Medicine: 20
   - 9E 9 East Medicine: 26
   - 9W 9 West Medicine: 14
   - 2N 2 North Medicine: 23
   - 12N 12 North Medicine: 16
   - 11N 11 North Geriatrics: 16
   - 11S 11 South Pulmonary: 17
   - 3E 3 East Neuroscience: 15
   - 3W 3 West Renal: 12
   - 6E 6 East Orthopaedics: 45
   - 6W 6 West General Surgery: 39
   - 10N 10 North Surgery: 35
   - 10S 10 South Surgery: 22
   - 5W 5 West Vascular Surgery: 25
3. Reviews signed off by shift:
   - July 2026: day 389, evening 363, night 370
   - August 2026: day 369, evening 372, night 308
   - September 2026: day 367, evening 374, night 332

### msp26_go_live_review_memo.docx

1. Net change: about 300 more override reviews in the 13 weeks from 4 January 2027.
2. Chart: reviews signed off by shift and month, July to September 2026, the values in item 3 above.

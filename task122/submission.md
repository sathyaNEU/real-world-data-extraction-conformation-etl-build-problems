## Tags

> **Domain:** Human Factors & Ergonomics (usability and task performance studies).
> **Analytical objective:** Experiment & Causal Analysis.

## 1. Final Recommendation

**Make PROBE-M mandatory at every en-route planner position from 1 April 2027.** Its use prevented about 30 per cent of the STCA activations the six sectors would have raised in the time it was running, against the 20 per cent the acceptance criteria require, read at the same sector, number of aircraft and number climbing or descending, minute by minute. Not the Safety Performance Report's rate per 1,000 flight hours (167.4 with the probe running, 77.2 without), which sets the probe's minutes against quieter ones; not a comparison at like occupancy alone, which leaves the probe's minutes with more climbing and descending traffic and shows no benefit.

## 2. Critical Components

1. Activations counted as the Safety Performance Report counts them over the trial: **4,742**, of which **1,865** in the probe's running time.
2. At the same sector, number of aircraft and number climbing or descending, the minutes without the probe put the activations the probe's running time would have raised at **2,596**.
3. The probe prevented **731**, about **30 per cent**, above the criterion's 20 per cent.

## 3. Step-by-Step Solution

1. Took each flight's latest plan revision from fdps_sector_crossings_2026-04_2026-09.csv (a revision re-issues the flight's whole crossing list) and counted, for each sector and minute, the aircraft in the sector and those whose entry and exit levels differ.
2. Marked the minutes with the probe running from probe_m_planner_workstation_log_2026-04_2026-09.csv, New Zealand time taken to UTC, a combined position's display covering both sectors (SRB 2026/04 section 3.3).
3. Counted the activations in stca_activations_2026-04_2026-09.csv as the Safety Performance Report counts them (live only, once per event in the sector where it began, a combined-sector activation in the sector of the first-named aircraft): 4,742.
4. Applied the activation rate of the minutes without the probe, at each sector, number of aircraft and number climbing or descending, to the probe's running minutes: 2,596 expected against 1,865 raised.
5. Took the share prevented, about 30 per cent, against section 3.1's one in five.
6. For the tables, split each flown crossing at New Zealand month ends, counted each month's activations per 1,000 flight hours in the sector where each began, and counted each flight once in each sector it entered.
7. Recommended making PROBE-M mandatory from 1 April 2027.

## 4. Deliverable Answers

### probe_decision_2027.docx

1. Recommendation: make PROBE-M mandatory at every en-route planner position from 1 April 2027.
2. The share its use prevented: about 30 per cent of the STCA activations the sectors would have raised in its running time (criterion 20 per cent).
3. Chart: the share of minutes with the probe running by the number of aircraft climbing or descending in the sector, beside the activations in the probe's running time as raised and as the same traffic raised without it.

### probe_trial_figures.xlsx

1. Flight hours by sector and month, New Zealand time, whole hours:
   - KPA: April 969, May 995, June 943, July 1,075, August 1,066, September 1,018
   - HKI: April 1,328, May 1,335, June 1,254, July 1,456, August 1,389, September 1,367
   - WKO: April 1,513, May 1,564, June 1,517, July 1,652, August 1,604, September 1,580
   - TKI: April 942, May 988, June 945, July 1,032, August 1,026, September 991
   - TPO: April 1,563, May 1,554, June 1,491, July 1,674, August 1,608, September 1,594
   - KPT: April 1,492, May 1,514, June 1,453, July 1,624, August 1,560, September 1,554
2. STCA activations per 1,000 flight hours by sector and month, one decimal:
   - KPA: April 125.9, May 125.7, June 130.4, July 121.8, August 141.6, September 135.5
   - HKI: April 96.4, May 118.3, June 75.8, July 81.0, August 92.9, September 100.9
   - WKO: April 74.7, May 85.0, June 71.9, July 76.9, August 81.0, September 81.0
   - TKI: April 135.9, May 119.4, June 116.4, July 149.2, August 136.5, September 152.4
   - TPO: April 83.8, May 83.7, June 87.2, July 110.5, August 86.5, September 106.7
   - KPT: April 77.1, May 89.2, June 73.0, July 85.0, August 82.1, September 88.8
3. Flights handled over the trial, whole flights:
   - KPA: 25,943
   - HKI: 35,991
   - WKO: 43,027
   - TKI: 25,401
   - TPO: 44,764
   - KPT: 43,552

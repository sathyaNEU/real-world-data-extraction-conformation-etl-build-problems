## Tags

> **Domain:** Human Factors & Ergonomics (usability and task performance studies).
> **Analytical objective:** Experiment & Causal Analysis.

## 1. Final Recommendation

**Make PROBE-M mandatory at every en-route planner position from 1 April 2027.** Its use prevented about 30 per cent of the STCA activations the six sectors would have raised in the time it was running, against the 20 per cent the acceptance criteria require, read at the same sector, number of aircraft and number climbing or descending, minute by minute. Not the Safety Performance Report's rate per 1,000 flight hours (136.5 with the probe running, 65.6 without), which sets the probe's minutes against quieter ones; not a comparison at like occupancy alone, which leaves the probe's minutes with more climbing and descending traffic and shows no benefit.

## 2. Critical Components

1. Activations counted as the Safety Performance Report counts them over the trial: **3,965**, of which **1,542** in the probe's running time, **1,520** of those at combinations of sector, number of aircraft and number climbing or descending that also occur without the probe.
2. At the same sector, number of aircraft and number climbing or descending, minute by minute, the probe prevented about **30 per cent** of the activations its running time would have raised, above the criterion's 20 per cent.

## 3. Step-by-Step Solution

1. Took each flight's latest plan revision from fdps_sector_crossings_2026-04_2026-09.csv (a revision re-issues the flight's whole crossing list) and counted, for each sector and minute, the aircraft in the sector and those whose entry and exit levels differ.
2. Marked the minutes with the probe running from probe_m_planner_workstation_log_2026-04_2026-09.csv, New Zealand time taken to UTC, a combined position's display covering both sectors (the acceptance criteria).
3. Counted the activations in stca_activations_2026-04_2026-09.csv as the Safety Performance Report counts them (live only, once per event in the sector where it began, a combined-sector activation in the sector of the first-named aircraft): 3,965.
4. Applied the activation rate of the minutes without the probe, at each sector, number of aircraft and number climbing or descending, to the probe's running minutes at combinations that also occur without it: 2,181 expected against 1,520 raised in them.
5. Took the share prevented, about 30 per cent, against the acceptance criteria's one in five.
6. For the tables, split each flown crossing at New Zealand month ends, counted each month's activations per 1,000 flight hours in the sector where each began, and counted each flight once in each sector it entered.
7. Recommended making PROBE-M mandatory from 1 April 2027.

## 4. Deliverable Answers

### probe_decision_2027.docx

1. Recommendation: make PROBE-M mandatory at every en-route planner position from 1 April 2027.
2. The share its use prevented: about 30 per cent of the STCA activations the sectors would have raised in its running time (criterion 20 per cent).
3. Chart: the share of minutes with the probe running by the number of aircraft climbing or descending in the sector, beside the activations in the probe's running time as raised and as the same traffic raised without it.

### probe_trial_figures.xlsx

1. Flight hours by sector and month, New Zealand time, whole hours:
   - KPA: April 968, May 995, June 944, July 1,075, August 1,065, September 1,018
   - HKI: April 1,329, May 1,336, June 1,253, July 1,457, August 1,389, September 1,368
   - WKO: April 1,513, May 1,564, June 1,517, July 1,652, August 1,604, September 1,579
   - TKI: April 942, May 988, June 945, July 1,032, August 1,027, September 991
   - TPO: April 1,563, May 1,553, June 1,490, July 1,674, August 1,607, September 1,593
   - KPT: April 1,492, May 1,514, June 1,453, July 1,624, August 1,560, September 1,554
2. STCA activations per 1,000 flight hours by sector and month, one decimal:
   - KPA: April 127.0, May 106.6, June 102.8, July 97.7, August 102.3, September 103.1
   - HKI: April 69.2, May 100.3, June 70.2, July 70.7, August 87.1, September 78.2
   - WKO: April 62.8, May 67.8, June 71.2, July 59.9, August 56.1, September 72.2
   - TKI: April 113.5, May 106.2, June 94.2, July 149.2, August 123.7, September 135.2
   - TPO: April 70.4, May 84.3, June 63.7, July 84.2, August 72.8, September 81.6
   - KPT: April 63.0, May 58.8, June 65.4, July 76.3, August 66.7, September 75.3
3. Flights handled over the trial, whole flights:
   - KPA: 25,864
   - HKI: 35,940
   - WKO: 42,990
   - TKI: 25,401
   - TPO: 44,721
   - KPT: 43,546

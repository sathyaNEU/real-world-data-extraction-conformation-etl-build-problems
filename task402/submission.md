## Tags

**Domain:** Energy Systems & Utilities, grid reliability and outage analysis (an electric membership cooperative's fiscal 2026 interruptions and the one fix in its 2027 reliability work plan).  
**Analytical objective:** Root-Cause Analysis (which of the changes in the fiscal 2026 reliability review raised members' sustained interruptions the most).

## 1. Final Recommendation

**Fund the 2027 fix for the SO-7 restoration switching revision.** It cost about 8,700 sustained customer interruptions in fiscal 2026, 7,200 more than the runner-up. Not the heat pumps connected without a load study (about 1,500), whose own harm is the service transformer trips a load study would have prevented; most of the overload category's rise is the revision's re-trips. Not the animal guards or the riser terminations (about 700 each), nor the transformer supplier (about 100).

## 2. Critical Components

1. The switching revision's cost, overload trips that began within minutes of the same section's restoration after an hour or more without supply on a frost day, from 1 December 2025: **8,700** customer interruptions.
2. The heat pump policy's cost, overload interruptions on the service transformers serving members connected under the waiver: **1,500**.
3. The gap between them: **7,200**.

## 3. Step-by-Step Solution

1. Read outage_events_fy2022-fy2026.csv (older section ids through the gis_crosswalk sheet of system_register_2026-09-30.xlsx), kept unplanned records and dropped major event days by IEEE 1366 2.5 beta on fiscal 2021 to 2025 daily SAIDI in daily_reliability_fy2021-fy2026.xlsx (the legacy sheet in hours), per the board policy's costing section: threshold 15.5 minutes.
2. Sorted section records by section and start and paired each with that section's previous restoration: from 1 December 2025 to 30 September 2026, overload records starting within 10 minutes of a restoration from an interruption of 60 minutes or more on a day averaging -3 C or colder (hq_substation_temperature_hourly.csv on local dates) total 8,700; October 2024 to November 2025 has no such pair, so nothing is netted.
3. Heat pump policy: overload records on transformers with load_study "waived" in heat_pump_rebates_fy2024-fy2026.xlsx, from each transformer's first waiver connection: 1,500.
4. Animal guards: ANML records at the 2026 list's structures in asset_programme_lists_2022-2026.xlsx from 1 January 2026: 700; risers: UGTERM records at the 2025 list's risers from 1 October 2025: 700; supplier: XFMR records on transformers after their Brekke Power Products unit was fitted (from 1 February 2026, transformer_units.parquet): 100.
5. Ask A: grouped each device's rows in scada_reclosing_operations_fy2026.csv (UTC to local) into five-minute sequences, dropped those ending in lockout (each matches a sustained record on the same device), gave breaker sequences to the sections on that feeder at the time (the register's feeders are as at 30 September 2026; the sections moved on 1 June 2026 carry an XFER record in the outage extract on their earlier feeder), counted one event per section per five minutes across all its devices, and divided member-weighted events by district members: the figures in block 4.
6. Ask B: in crew_time_overtime_fy2026.csv kept approved CALLOUT entries on OUTAGE orders at the latest entry per employee, order and start, dated each by its work order's outage in the outage extract (the foreman enters the week's time each Monday), chained each employee's rows under 15 minutes apart into one callout and paid it per labor_agreement_2024-2027_extract.pdf Article 14 (time and one-half, a 2 hour minimum per callout, double time on Article 18 holidays): the figures in block 4.
7. Ranked the five costs: the SO-7 revision at 8,700 against 1,500 for the heat pump policy takes the fix.

## 4. Deliverable Answers

### reliability_fix_2027.docx

1. Change to fix: the SO-7 restoration switching revision (1 December 2025).
2. Runner-up: heat pumps connected without a load study (1 November 2025).
3. Gap: 7,200 sustained customer interruptions.
4. Each change's fiscal 2026 cost, sustained customer interruptions to the nearest 100:
   - SO-7 restoration switching revision: 8,700
   - Heat pumps connected without a load study: 1,500
   - Animal guard programme ended: 700
   - Riser termination replacements suspended: 700
   - Transformer supplier change: 100

### fy2026_interruptions_by_change.png

1. Horizontal bar chart of the five costs, largest first, each bar labelled with its value and the SO-7 revision highlighted.

### interruption_costing_fy2026.xlsx

1. Momentary interruption events per member, two decimals (Q1 October to December 2025, Q2 January to March, Q3 April to June, Q4 July to September 2026):
   - North: Q1 2.12, Q2 1.42, Q3 2.61, Q4 3.51
   - Lakes: Q1 1.34, Q2 1.72, Q3 2.75, Q4 3.34
   - Prairie: Q1 1.68, Q2 1.22, Q3 2.17, Q4 3.24
   - River: Q1 1.58, Q2 1.18, Q3 2.27, Q4 2.80
2. Crew callout hours and callout pay for restoration work, nearest hour and nearest dollar:
   - Oct 2025: 517 hours, USD 51,564
   - Nov 2025: 600 hours, USD 56,839
   - Dec 2025: 254 hours, USD 26,726
   - Jan 2026: 513 hours, USD 53,587
   - Feb 2026: 410 hours, USD 43,840
   - Mar 2026: 357 hours, USD 39,302
   - Apr 2026: 463 hours, USD 46,314
   - May 2026: 727 hours, USD 67,235
   - Jun 2026: 429 hours, USD 43,364
   - Jul 2026: 233 hours, USD 25,066
   - Aug 2026: 243 hours, USD 26,666
   - Sep 2026: 234 hours, USD 26,163

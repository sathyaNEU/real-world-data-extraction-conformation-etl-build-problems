## Tags

**Domain:** Physical & Environmental Sciences (hydrology, flood frequency).  
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Carry Alternative C, the 38 MG tank, into design.**
It leaves Outfall 014 2.9 untreated overflow events in an average year against the decree's limit of 4. Not Alternative B (26 MG), which meets the limit only at its pump station's 31 MGD rating (2.8) and leaves 6.8 once its pump-back is held to the room the Southside plant has under its 140 MGD headworks capacity. Not Alternative D, which meets the limit too but costs USD 30.4 million more.

## 2. Critical Components

1. Alternative B, pumped back no faster than the Southside plant's room: **6.8 events a year**
2. Alternative C on the same replay: **2.9 events a year**

## 3. Step-by-Step Solution

1. Joined the two loggers in outfall_014_flow_monitoring_2014-2025.parquet onto UTC, FM-0142's cfs (Eastern Standard Time) times 0.646317 and AV-3315's MGD, the overlap week once.
2. Took the Southside WRP's hourly influent from wrp_influent_hourly_2014-2025.csv (both tag sets, local time with its repeated and missing hours, to UTC) and its room as 140 MGD less the influent.
3. Replayed the record through each TM-7 tank filling from the overflow and pumped back after the overflow stops (TM-7 3.2) at the lesser of the station's firm capacity and that hour's room.
4. Counted untreated overflow events under Appendix C 2.2 and 2.3: A 9.7, B 6.8, C 2.9, D 1.3 a year; C is the least-cost alternative at or under 4 (TM-7 4).
5. Rainfall 2025: dropped repeated tips, removed each calibration pour (a steady run of tips on a cal-check visit in rain_gauge_field_service_2014-2025.xlsx), read the TipLink C200 loggers (RG-3 and RG-4 from May 2024) as UTC and the HOBO loggers as Eastern Standard Time, and counted RG-4 at 0.2 mm a tip after its 12 August 2025 mechanism swap.
6. Northside returns: summed each fall in NT_LIT601_FT while a pump ran through O&M Table 4-1, the readings from the 23 August 2023 re-mount less the 0.45 ft the empty tank reads.
7. Recommended Alternative C at 2.9 events a year.

## 4. Deliverable Answers

### clay_street_storage_evaluation.xlsx

1. Events a year each alternative would leave, to one decimal:
   - Alternative A (19 MG): 9.7
   - Alternative B (26 MG): 6.8
   - Alternative C (38 MG): 2.9
   - Alternative D (50 MG): 1.3
2. Alternative to carry into design: Alternative C (38 MG)
3. Rainfall recorded in 2025, inches:
   - RG-1: Jan 3.94, Feb 1.79, Mar 7.54, Apr 6.31, May 6.85, Jun 2.81, Jul 3.31, Aug 2.13, Sep 3.51, Oct 10.14, Nov 1.27, Dec 2.24
   - RG-2: Jan 3.78, Feb 1.74, Mar 7.14, Apr 6.58, May 6.56, Jun 2.74, Jul 3.39, Aug 2.33, Sep 2.69, Oct 11.08, Nov 1.50, Dec 2.02
   - RG-3: Jan 3.57, Feb 1.95, Mar 7.02, Apr 6.83, May 5.93, Jun 2.79, Jul 4.01, Aug 2.12, Sep 3.81, Oct 11.87, Nov 1.36, Dec 2.01
   - RG-4: Jan 3.74, Feb 1.71, Mar 7.34, Apr 6.31, May 6.13, Jun 3.17, Jul 3.13, Aug 2.46, Sep 3.69, Oct 10.81, Nov 1.15, Dec 2.14
4. Volume the Northside tank returned to the Northside interceptor, million gallons:
   - 2021: 261
   - 2022: 161
   - 2023: 253
   - 2024: 244
   - 2025: 297

### clay_street_tank_selection_board.pptx

1. Selection: Alternative C (38 MG), on slide 2
2. Column chart of events a year by alternative (A 9.7, B 6.8, C 2.9, D 1.3) against the limit of 4, on slide 2, Alternative C highlighted

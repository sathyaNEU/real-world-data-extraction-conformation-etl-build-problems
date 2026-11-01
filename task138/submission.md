## Tags

**Domain:** Physical & Environmental Sciences (hydrology and flood frequency: the 1 per cent annual chance flood at a gauged river town and the levee crown raise it calls for).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Raise the Orrinsford levee crown by 2 ft before the 2027 flood season.** The design flood for the river as it now runs is 110,000 cfs at the Orrinsford gauge and the railroad closure is 1.50 ft short of it with freeboard; a 1 ft raise leaves a 1.1 per cent annual chance of exceeding what the levee holds, 2 ft brings it to 0.9 per cent. Not no raise: the fit to the published Orrinsford record (95,000 cfs) keeps floods the upstream floodplains cut before their levees were raised. Not 1 ft: the 18 water years since the last raise alone (105,000 cfs) set aside Coyle Bridge's 47 earlier years.

## 2. Critical Components

1. Every levee between Coyle Bridge and Orrinsford was raised by October 2008, so water year **2009** is the first of the river as it now runs.
2. The present river's 1 per cent annual chance discharge at Orrinsford is **110,000 cfs**.
3. Against it the railroad closure's crown is **1.50 ft** short of the design water surface plus freeboard.

## 3. Step-by-Step Solution

1. From the Segments and Gauges sheets of DNR_levee_inventory_Tamsen_2025.xlsx, took the six segments between river miles 41.0 and 12.6: their crown raises, the last in October 2008, were all in force from water year 2009.
2. Read each water year's annual peak at Orrinsford and Coyle Bridge from SWS_annual_peaks_Tamsen_basin_2026-10-28.csv (an October to December peak counts in the next water year) and fitted Orrinsford on Coyle Bridge through the origin over water years 2009 to 2026: 1.064; before 2009 the great floods sit well below it (1970: 93,200 against 132,000 cfs).
3. Took Orrinsford's peaks from 2009 and Coyle Bridge's times 1.064 before, and fitted LS-02's log-Pearson Type III by moments with the station skew weighted with the SW-16-03 region 2 skew (-0.08, mean square error 0.14): the 1 per cent discharge is 110,403 cfs, 110,000 to the nearest 5,000.
4. Read HWE-1907_hydraulic_update_2019_Table4.pdf linearly in discharge, added LS-02 freeboard (3.0 ft, 4.0 ft within 100 ft of a bridge, plus the upstream allowance) and set it against the 2024 crown in the inventory's Orrinsford crown sheet: the railroad closure is 1.50 ft short, so the smallest whole-foot raise is 2 ft.
5. For each uniform raise, found the discharge the levee then holds with freeboard at every cross-section (the railroad closure governs) and its annual chance on the present-river curve: 1.4, 1.1, 0.9, 0.7, 0.6 per cent for 0 to 4 ft.
6. Ask A: took 700 ft off each station of the 2016 survey (the four structures both surveys shot sit 700 ft apart), put its shots on NAVD 88 with OLDD_benchmark_list.csv (+0.27 ft) and averaged 2016 less 2024 by the 2024 survey's reach: R1 0.07, R2 0.12, R3 0.16, R4 0.21, R5 0.29, R6 0.24, R7 0.14, R8 0.09 ft.
7. Ask B: took OP-04's warning level, 661.00 ft NGVD 29, on the Coyle Bridge gauge datum in force at each flood (23.00 ft on the 638.00 ft datum the hourly export states, after the 2.00 ft step in stage against discharge on 22 October 2019), moved the old ORF2 logger's records 6 h to UTC (where they line up with the new logger's over the days both ran), put the Main Street sill at 16.95 ft on the ORF2 gauge and interpolated both crossings within the hour: 37, 29, 38, 38, 32, 35, 51 hours.
8. Raise the crown 2 ft before the 2027 flood season.

## 4. Deliverable Answers

### levee_raise_review.xlsx

1. Crown raise: 2 ft.
2. Design discharge at the Orrinsford gauge: 110,000 cfs.
3. Annual chance the river exceeds what the levee holds with its freeboard, by uniform raise:
   - 0 ft: 1.4%
   - 1 ft: 1.1%
   - 2 ft: 0.9%
   - 3 ft: 0.7%
   - 4 ft: 0.6%
4. Crown settlement between the 2016 and 2024 surveys, by reach:
   - R1: 0.07 ft
   - R2: 0.12 ft
   - R3: 0.16 ft
   - R4: 0.21 ft
   - R5: 0.29 ft
   - R6: 0.24 ft
   - R7: 0.14 ft
   - R8: 0.09 ft
5. Hours from the Coyle Bridge warning level to the Main Street sill at Orrinsford, floods since October 2016:
   - March 2020: 37 hours
   - May 2020: 29 hours
   - June 2020: 38 hours
   - February 2024: 38 hours
   - April 2024: 32 hours
   - June 2024: 35 hours
   - May 2025: 51 hours

### levee_raise_memo.pdf

1. One page recommending a 2 ft raise, with the chart of the present-river and published-record frequency curves at Orrinsford against the discharge each raise from 0 to 4 ft holds, the 1 per cent line marked, and the raise table.

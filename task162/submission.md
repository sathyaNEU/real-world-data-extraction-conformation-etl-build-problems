# task162 submission

## Tags

**Domain:** Energy Systems & Utilities, asset condition and maintenance (a water network's district leakage under a pressure management scheme).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Phase 3's valves will not deliver the contracted 0.48 Ml/d in 2027-28: the delivery plan adds 2 find-and-fix gang-years.**
Replayed hour by hour through the rev C settings, the 22 districts' assessed leakage falls from 3.22 to 2.81 Ml/d, a 0.41 Ml/d reduction, 0.07 Ml/d short. Not the night pressure ratio carried through the day (0.63 Ml/d, target met), which credits each valve with its setting in the weekday hours when the paper mill's draw on the trunk main has already taken its inlet below it.

## 2. Critical Components

1. The Phase 3 districts' 2025-26 assessed leakage is **3.22 Ml/d** (Lynmere's export of 14 May 2026).
2. Their forecast 2027-28 assessed leakage with the valves in service is **2.81 Ml/d**.
3. The reduction is **0.41 Ml/d**, **0.07 Ml/d** short of the 0.48 Ml/d target.

## 3. Step-by-Step Solution

1. Read Schedule 4 (target 0.48 Ml/d, 0.05 Ml/d a gang-year rounded up, both years by LW-LA-04 issue 6), the planning note (each 2027-28 month as recorded in the same month of 2025-26, valves at rev C all year) and the export's Year sheet: 2025-26 leakage 3.22 Ml/d.
2. Conformed the telemetry through logger_register.csv and district_code_history.csv (serials by their dates, bar at 10.197 m, re-sent rows once, NZ04A as NZ04) into hourly inflow, inlet pressure and average zone pressure per district and GMT day.
3. For each Phase 3 district and valid day, passed every hourly inlet pressure through its rev C setting from phase3_prv_schedule_rev_C.xlsx (the outlet the lower of the two) and lowered the zone pressure by what the valve takes off the inlet.
4. Scaled each day's net night flow by the replayed night zone pressure over the recorded one to the district's Table C2 N1, rebuilt the night-day factor from the replayed pressures and took LW-LA-04's months and year: 2027-28 leakage 2.81 Ml/d.
5. Reduction 0.41 Ml/d against 0.48: shortfall 0.07 Ml/d, 2 gang-years at 0.05 Ml/d each, rounded up.
6. Ran LW-LA-04 day by day on the zone's twelve other districts' own loggers (NZ04's two inlets summed; NZ09 and NZ10 without 12 to 20 January 2026, when NZ09's inlet was dry and BV-0910 open), allowing for each dwelling once from property_extract_2026-11-02.csv (a new build from its plot connection, its address record on the same supply point taking over; each flat on a shared supply): NZ01 0.153, NZ02 0.127, NZ03 0.164, NZ04 0.138, NZ05 0.126, NZ06 0.095, NZ07 0.209, NZ08 0.098, NZ09 0.146, NZ10 0.146, NZ11 0.101, NZ12 0.114 Ml/d.
7. Ran section 8 on thornholme_outlet_daily_2025_26.csv (readings before 12 November 2025 divided by 0.986, certificate FFS-25-1182) and billing_extract_north_2025_26.csv (the zone's properties and NZ-TM, bills apportioned by days, every identical assessed line kept as one flat's bill): system input 30.36, billed unmetered 5.61, real losses 5.97 Ml/d.
8. Phase 3 falls 0.07 Ml/d short of its target, so the 2027-28 delivery plan adds 2 find-and-fix gang-years.

## 4. Deliverable Answers

### phase3_leakage_forecast_2027_28.xlsx

1. Phase 3 in 2027-28: forecast leakage 2.81 Ml/d, reduction 0.41 Ml/d, shortfall 0.07 Ml/d against the contracted 0.48 Ml/d, 2 find-and-fix gang-years.
2. The zone's twelve other districts' 2025-26 assessed leakage, Ml/d to three decimals:
   - NZ01 Orlesby Village: 0.153
   - NZ02 Kessington Lane: 0.127
   - NZ03 Halverby Park: 0.164
   - NZ04 Wrenfold: 0.138
   - NZ05 Stainmoor Ings: 0.126
   - NZ06 Kestle Road: 0.095
   - NZ07 Sorrelby End: 0.209
   - NZ08 Cragthwaite Top: 0.098
   - NZ09 Linmere Green: 0.146
   - NZ10 Barrowside: 0.146
   - NZ11 Old Mill Fields: 0.101
   - NZ12 Ravens Clough: 0.114
3. The Northern zone's 2025-26 top-down balance: system input 30.36 Ml/d, billed unmetered consumption 5.61 Ml/d, real losses 5.97 Ml/d.

### phase3_leakage_by_district.svg

4. Dumbbell chart of the 22 Phase 3 districts, NZ13 to NZ34 in order along the trunk main, each district's 2025-26 assessed leakage beside its forecast 2027-28 leakage, the phase's 3.22 and 2.81 Ml/d in the subtitle.

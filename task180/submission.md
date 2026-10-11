# task180: the 2027/28 transformer inspection slate

## Tags

**Domain:** Energy Systems & Utilities (asset condition and maintenance, transformer dissolved gas analysis).
**Analytical objective:** Anomaly Detection & Diagnostics (fault diagnosis from dissolved gas analysis, each anomalous gas attributed to its source before ranking).
**Reasoning phases:** Explore/Discover, Hypothesize, Analyze/Validate, Synthesize, Recommend/Communicate.

## 1. Final Recommendation

**Take Southbridge T2, Rolleston T2 and Coalgate T1 for the three 2027/28 internal inspections, in that order.**

Southbridge T2 leads at a severity score of 8.07 on acetylene, then Rolleston T2 at 4.98 on acetylene and Coalgate T1 at 4.73 on ethylene, with Springston T2 at 4.43 the first left out. Not Dunsandel T1 or Leeston T2: both are code 3 as coded (9.64 and 8.07), but their main-tank acetylene rises with their in-oil tap changers' operations and is not generated in the main tank, so neither has a main-tank fault for an inspection to remedy. Not a slate that drops every transformer whose acetylene follows its tap changer's operations, or the acetylene at every in-oil tap changer: both lose Rolleston T2, whose acetylene tracks its operations but arrives with more hydrogen than acetylene, so it is made in the main tank.

## 2. Critical Components

1. Coded on the main-tank results, Dunsandel T1 is code 3 at **9.64** and Leeston T2 and Southbridge T2 are code 3 at **8.07** each
2. At Dunsandel T1, Leeston T2 and Rolleston T2 the main-tank acetylene rises with the tap operations; at Dunsandel T1 and Leeston T2 it arrives with almost no hydrogen (twelve-month C2H2/H2 **9.8** and **8.2**), at Rolleston T2 with more hydrogen than acetylene (**0.64**), as at Southbridge T2 (**0.51**), whose vacuum tap changer it does not follow
3. With their acetylene attributed to the tap changer, Dunsandel T1 and Leeston T2 stay code **3** but have **no main-tank fault**, so they take no inspection outage
4. Code 3 with a main-tank fault, by severity: Southbridge T2 **8.07**, Rolleston T2 **4.98**, Coalgate T1 **4.73**, Springston T2 **4.43**, Darfield T1 **3.45**

## 3. Step-by-Step Solution

1. Kept the latest issue of each laboratory report (ES-DGA-02 3.4), took below-detection results at half the limit (3.5) and coded all 44 transformers on the September 2026 round against annex A (section 4): seven code 3, led by Dunsandel T1 at 9.64 and Leeston T2 and Southbridge T2 at 8.07.
2. For each transformer with rising main-tank acetylene, set its increments between samples against the tap operations between the same dates in `scada_tap_counters_daily_2021-2026.csv`: at Dunsandel T1, Leeston T2 and Rolleston T2, all in-oil arcing tap changers in `asset_register_zone_transformers.xlsx`, they move together (r 0.998, 0.995 and 0.999); at Southbridge T2 (vacuum) they do not (r -0.07). Then read the gas the acetylene arrives with: twelve-month C2H2/H2 of 9.8 at Dunsandel T1 and 8.2 at Leeston T2 is the acetylene-rich, hydrogen-poor oil of a diverter compartment reaching the main tank; 0.64 at Rolleston T2 and 0.51 at Southbridge T2 is arc gas made in the main-tank oil, at Rolleston T2 at each tap change.
3. Set Dunsandel T1 and Leeston T2 aside: code 3, but the acetylene behind it is the tap changer's, so there is no fault in the main tank for an internal inspection to remedy (5.1).
4. Ranked the code 3 transformers with a main-tank fault by severity (5.2): Southbridge T2 8.07, Rolleston T2 4.98, Coalgate T1 4.73, Springston T2 4.43, Darfield T1 3.45.
5. Took each in-oil tap changer's last service from `maintenance_log_2019-2026.xlsx` (6.1) and summed the 00:00 counter increments to 16 October 2026, a drop being a rollover past 99,999 unless the log has the counter replaced that day: 7 of 27 past the annex B interval.
6. Computed relative saturation at each latest sample (annex C) from the label temperature or, where blank, the hourly top-oil temperature of `scada_top_oil_hourly_2021-2026.parquet`, whose timestamps are UTC, for the New Zealand clock hour of sampling: six above 30 per cent.
7. Recommendation: Southbridge T2, Rolleston T2 and Coalgate T1, in that order.

## 4. Deliverable Answers

### inspection_slate_2027-28.docx

1. The three, in the order they are taken, with substation, condition code, severity score and the gas behind it:
   - 1: SBG-T2, Southbridge, code 3, severity 8.07, acetylene
   - 2: RLS-T2, Rolleston, code 3, severity 4.98, acetylene
   - 3: CGT-T1, Coalgate, code 3, severity 4.73, ethylene
2. Every in-oil tap changer (27), operations since its last service and whether it is past its service interval:
   - DSL-T1, Dunsandel: 87,322 operations, past interval yes
   - DYL-T2, Doyleston: 87,029 operations, past interval yes
   - GLT-T1, Glentunnel: 75,013 operations, past interval yes
   - TPR-T2, Te Pirita: 64,224 operations, past interval yes
   - LST-T1, Leeston: 61,972 operations, past interval yes
   - GLT-T2, Glentunnel: 29,695 operations, past interval yes
   - SHF-T1, Sheffield: 23,553 operations, past interval yes
   - CGT-T2, Coalgate: 57,551 operations, past interval no
   - LST-T2, Leeston: 54,294 operations, past interval no
   - RLS-T2, Rolleston: 49,897 operations, past interval no
   - WDN-T1, Waddington: 38,209 operations, past interval no
   - DYL-T1, Doyleston: 32,511 operations, past interval no
   - SBG-T1, Southbridge: 32,019 operations, past interval no
   - WML-T1, West Melton: 31,680 operations, past interval no
   - CGT-T1, Coalgate: 27,923 operations, past interval no
   - DFD-T1, Darfield: 21,895 operations, past interval no
   - WDS-T1, Weedons: 21,319 operations, past interval no
   - DSL-T2, Dunsandel: 20,955 operations, past interval no
   - GDL-T1, Greendale: 20,915 operations, past interval no
   - LDB-T1, Ladbrooks: 20,592 operations, past interval no
   - LDB-T2, Ladbrooks: 16,890 operations, past interval no
   - LIN-T1, Lincoln: 16,064 operations, past interval no
   - SPF-T1, Springfield: 14,842 operations, past interval no
   - SPF-T2, Springfield: 11,034 operations, past interval no
   - LIN-T2, Lincoln: 10,079 operations, past interval no
   - KRW-T1, Kirwee: 6,837 operations, past interval no
   - HOR-T1, Hororata: 3,909 operations, past interval no
3. Transformers above 30 per cent relative saturation at their latest sample (6), to one decimal:
   - SHF-T1, Sheffield: 36.1 per cent
   - GDL-T1, Greendale: 34.9 per cent
   - WDN-T1, Waddington: 34.1 per cent
   - DYL-T1, Doyleston: 33.1 per cent
   - TPR-T2, Te Pirita: 31.7 per cent
   - SPF-T1, Springfield: 31.5 per cent

### dga_fleet_review.csv

1. One row per transformer (44): condition code, severity score, on the slate, tap operations since service where the tap changer is in-oil, relative saturation at the latest sample:
   - BNM-T1: code 1, severity 0.38, not on the slate, no in-oil tap changer, 8.8 per cent
   - BNM-T2: code 1, severity 0.21, not on the slate, no in-oil tap changer, 7.0 per cent
   - CGT-T1: code 3, severity 4.73, on the slate, 27,923 operations since service, 22.8 per cent
   - CGT-T2: code 1, severity 0.28, not on the slate, 57,551 operations since service, 28.2 per cent
   - DFD-T1: code 3, severity 3.45, not on the slate, 21,895 operations since service, 19.6 per cent
   - DFD-T2: code 1, severity 0.16, not on the slate, no in-oil tap changer, 11.7 per cent
   - DSL-T1: code 3, severity 9.64, not on the slate, 87,322 operations since service, 21.5 per cent
   - DSL-T2: code 1, severity 0.33, not on the slate, 20,955 operations since service, 17.0 per cent
   - DYL-T1: code 1, severity 0.29, not on the slate, 32,511 operations since service, 33.1 per cent
   - DYL-T2: code 1, severity 0.46, not on the slate, 87,029 operations since service, 23.9 per cent
   - GDL-T1: code 1, severity 0.34, not on the slate, 20,915 operations since service, 34.9 per cent
   - GDL-T2: code 1, severity 0.21, not on the slate, no in-oil tap changer, 20.9 per cent
   - GLT-T1: code 1, severity 0.19, not on the slate, 75,013 operations since service, 19.7 per cent
   - GLT-T2: code 2, severity 0.30, not on the slate, 29,695 operations since service, 18.2 per cent
   - HOR-T1: code 1, severity 0.49, not on the slate, 3,909 operations since service, 27.0 per cent
   - HOR-T2: code 1, severity 0.25, not on the slate, no in-oil tap changer, 15.6 per cent
   - KRW-T1: code 1, severity 0.49, not on the slate, 6,837 operations since service, 28.5 per cent
   - KRW-T2: code 1, severity 0.27, not on the slate, no in-oil tap changer, 11.0 per cent
   - LDB-T1: code 2, severity 0.33, not on the slate, 20,592 operations since service, 24.4 per cent
   - LDB-T2: code 1, severity 0.49, not on the slate, 16,890 operations since service, 21.1 per cent
   - LIN-T1: code 1, severity 0.14, not on the slate, 16,064 operations since service, 19.0 per cent
   - LIN-T2: code 1, severity 0.22, not on the slate, 10,079 operations since service, 27.3 per cent
   - LST-T1: code 1, severity 0.31, not on the slate, 61,972 operations since service, 22.2 per cent
   - LST-T2: code 3, severity 8.07, not on the slate, 54,294 operations since service, 18.2 per cent
   - PRB-T1: code 1, severity 0.42, not on the slate, no in-oil tap changer, 8.9 per cent
   - PRB-T2: code 1, severity 0.49, not on the slate, no in-oil tap changer, 10.0 per cent
   - RLS-T1: code 1, severity 0.45, not on the slate, no in-oil tap changer, 8.0 per cent
   - RLS-T2: code 3, severity 4.98, on the slate, 49,897 operations since service, 12.5 per cent
   - SBG-T1: code 1, severity 0.15, not on the slate, 32,019 operations since service, 26.7 per cent
   - SBG-T2: code 3, severity 8.07, on the slate, no in-oil tap changer, 13.9 per cent
   - SHF-T1: code 1, severity 0.21, not on the slate, 23,553 operations since service, 36.1 per cent
   - SHF-T2: code 1, severity 0.39, not on the slate, no in-oil tap changer, 16.9 per cent
   - SPF-T1: code 2, severity 0.24, not on the slate, 14,842 operations since service, 31.5 per cent
   - SPF-T2: code 1, severity 0.30, not on the slate, 11,034 operations since service, 22.4 per cent
   - SPN-T1: code 1, severity 0.11, not on the slate, no in-oil tap changer, 12.1 per cent
   - SPN-T2: code 3, severity 4.43, not on the slate, no in-oil tap changer, 11.0 per cent
   - TPR-T1: code 1, severity 0.49, not on the slate, no in-oil tap changer, 17.9 per cent
   - TPR-T2: code 1, severity 0.26, not on the slate, 64,224 operations since service, 31.7 per cent
   - WDN-T1: code 1, severity 0.28, not on the slate, 38,209 operations since service, 34.1 per cent
   - WDN-T2: code 1, severity 0.32, not on the slate, no in-oil tap changer, 14.5 per cent
   - WDS-T1: code 1, severity 0.23, not on the slate, 21,319 operations since service, 14.7 per cent
   - WDS-T2: code 1, severity 0.27, not on the slate, no in-oil tap changer, 10.7 per cent
   - WML-T1: code 2, severity 1.39, not on the slate, 31,680 operations since service, 16.1 per cent
   - WML-T2: code 1, severity 0.39, not on the slate, no in-oil tap changer, 19.0 per cent


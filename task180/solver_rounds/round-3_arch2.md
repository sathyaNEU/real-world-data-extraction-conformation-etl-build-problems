# solver round: round 3

**Proxy score 37.8 / 100** (recommendation 2.5 of 35, instruction 7.0 of 7, asks 28.3 of 58). Main call missed. 0 of 4 ask items cracked (80 per cent of tokens).

## Main call

golden: Take Southbridge T2, Rolleston T2 and Coalgate T1 for the three 2027/28 internal inspections, in that order.

solver: Give the three 2027-28 internal inspections to SBG-T2 Southbridge (code 3, severity 8.07, acetylene C2H2; window 1, 12 Apr-21 May 2027), then CGT-T1 Coalgate (code 3, severity 4.73, ethylene C2H4; window 2, 23 Aug-1 Oct 2027), then SPN-T2 Springston (code 3, severity 4.43, ethylene C2H4; window 3, 31 Jan-10 Mar 2028). The higher-scoring code 3 units DSL-T1 (9.64), LST-T2 (8.07) and RLS-T2 (4.98) are excluded because their acetylene tracks in-oil tap-changer operations (about 0.6, 0.6 and 0.36 ppm per 1,000 operations), which is compartment leakage and not a main-tank fault under ES-DGA-02 5.1-5.2. DFD-T1 Darfield (code 3, 3.45, C2H4) is fourth in line.

tokens matched 2 of 4 (28, Take Southbridge, Rolleston, Coalgate)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| inspection_slate_2027-28.docx | 1 | 5 | 7 | 71% |
| inspection_slate_2027-28.docx | 2 | 30 | 47 | 64% |
| inspection_slate_2027-28.docx | 3 | 9 | 15 | 60% |
| dga_fleet_review.csv | 1 | 0 | 116 | 0% |

## Solver's path

1. dga_main_tank_results_2021-2026.csv: 1,077 rows reduced to 1,072 samples by keeping the latest issue per sample_id (ES-DGA-02 3.4). The 5 reissues (LDB-T2, LIN-T1, KRW-T1, SPF-T1, GDL-T2) correct moisture or oil temperature. '<LOD' is taken as LOD/2 (3.5). The latest sample for every unit falls between 14 and 30 Sep 2026.
2. Base sample = the most recent sample at least 330 days before the latest (all intervals 366-378 days). Twelve-month increase = (latest - base) x 365 / days. Preservation class from latest O2/N2 (threshold 0.2). Age band from 2026 minus the manufacture or rewind year (DSL-T2 2003, CGT-T1 1998). Gases compared with tables A1, A2 and A3. Result: 7 code 3 units (DSL-T1 9.64, LST-T2 8.07, SBG-T2 8.07, RLS-T2 4.98, CGT-T1 4.73, SPN-T2 4.43, DFD-T1 3.45) and 5 code 2 units.
3. Rule 5.2 (main-tank fault only): built cumulative tap operations from scada_tap_counters_daily (adding 100,000 at each roll-over) and compared each sample-to-sample C2H2 change with operations in the same interval. DSL-T1 is about 0.6 ppm per 1,000 ops, LST-T2 about 0.6 and RLS-T2 about 0.36, steady across 12-15 intervals, and all three have In-oil arcing tap changers: leakage from the tap-changer compartment, so excluded. SBG-T2 (Vacuum) has erratic ratios and rising H2: main tank. CGT-T1, SPN-T2 and DFD-T1 ethylene shows no link to tap operations: main-tank thermal faults.
4. Slate = top 3 remaining by severity, matched in order to the Held windows MSU2-2702, 2705 and 2708 in mobile_substation_bookings_2027-28.xlsx: SBG-T2 8.07, CGT-T1 4.73, SPN-T2 4.43. DFD-T1 3.45 is fourth.
5. Tap changers: the 27 In-oil arcing units in asset_register. Last OLTC SERVICE taken from maintenance_log (6.1); 8 register dates are stale. The SCADA counter at 00:00 on the service day matches the log reading. Base = SCADA value the day after service (0 where the counter was replaced: SBG-T1, LIN-T1, LDB-T2, KRW-T1, HOR-T1, GDL-T1, WDN-T1). Roll-overs added (LST-T1, DYL-T2, GLT-T1, CGT-T2, TPR-T2, WDS-T1). For the pre-2021 services (GLT-T2 3,642; SHF-T1 17,728) the log reading is the base. Counts run to SCADA 16 Oct 2026. Past interval if more than 60,000 operations or more than 7 years (annex B): 7 units.
6. Water in oil (annex C): T = label oil_temp_c from the latest issue; otherwise the SCADA top_oil_c for the sample hour, converted from NZ time (Pacific/Auckland, NZDT from 27 Sep 2026) to the parquet's UTC timestamps. The conversion was validated on labelled samples (mean error 0.3 C, against 3.7 C unconverted). RS = moisture / 10^(7.42 - 1670/(T+273)) x 100. Six units exceed 30%; KRW-T1 drops to 28.5% after its corrected temperature, and SPF-T1 rises to 31.5% after its corrected moisture.

confidence: High on the codes, severities, tap counts and saturation figures, which are mechanical applications of ES-DGA-02. Medium-high on excluding DSL-T1, LST-T2 and RLS-T2: that rests on the acetylene-per-operation correlation together with their in-oil tap-changer type, since the standard does not spell out a test for tap-changer leakage.

notes: LST-T2 and SBG-T2 tie at 8.07; the tie does not matter because LST-T2 is excluded as a tap-changer leak. Past-interval status is assessed at the 16 Oct 2026 data date; CGT-T2 (57,551 operations) will pass 60,000 within about two months.

### inspection_slate_2027-28.docx (solver's answers)
- the three, in order, with substation, code, severity, gas: 1) SBG-T2, Southbridge, code 3, severity 8.07, acetylene C2H2 (4.7 to 12.9 ppm over 371 days = 8.07 ppm/yr against a free-breathing limit of 1.0; 12.9 ppm exceeds the 95th-percentile limit of 6); 2) CGT-T1, Coalgate, code 3, severity 4.73, ethylene C2H4 (106 to 140 ppm over 375 days = 33.1 ppm/yr against a limit of 7; 140 ppm exceeds the 95th-percentile limit of 120); 3) SPN-T2, Springston, code 3, severity 4.43, ethylene C2H4 (89 to 125 ppm over 371 days = 35.4 ppm/yr against a sealed limit of 8; 125 ppm exceeds the 95th-percentile limit of 95)
- in-oil tap changer table: ops since last service, past interval: 27 transformers, giving operations since last service and whether past interval (60,000 operations or 7 years): LST-T1 61972 Yes; LST-T2 54294 No; SBG-T1 32019 No; DYL-T1 32511 No; DYL-T2 87029 Yes; DSL-T1 87322 Yes; DSL-T2 20955 No; LIN-T1 16064 No; LIN-T2 10079 No; LDB-T1 20592 No; LDB-T2 16890 No; RLS-T2 49897 No; WDS-T1 21319 No; WML-T1 31680 No; KRW-T1 6837 No; DFD-T1 21895 No; TPR-T2 64224 Yes; HOR-T1 3909 No; CGT-T1 27923 No; CGT-T2 57551 No; GLT-T1 75013 Yes; GLT-T2 29695 Yes (7.5 yrs since service 9 Apr 2019); SHF-T1 23553 Yes (7.2 yrs since service 20 Aug 2019); SPF-T1 14842 No; SPF-
- oil wetter than 30% relative saturation at latest sample, 1 dp: SHF-T1 36.1%; GDL-T1 34.9%; WDN-T1 34.1%; DYL-T1 33.1%; TPR-T2 31.7%; SPF-T1 31.5% (6 transformers)

### dga_fleet_review.csv (solver's answers)
- one row per transformer: code, severity (2 dp), on slate, tap ops since service (in-oil only), relative saturation % (1 dp): LST-T1,1,0.31,No,61972,22.2; LST-T2,3,8.07,No,54294,18.2; SBG-T1,1,0.15,No,32019,26.7; SBG-T2,3,8.07,Yes,,13.9; DYL-T1,1,0.29,No,32511,33.1; DYL-T2,1,0.46,No,87029,23.9; DSL-T1,3,9.64,No,87322,21.5; DSL-T2,1,0.33,No,20955,17.0; LIN-T1,1,0.14,No,16064,19.0; LIN-T2,1,0.22,No,10079,27.3; SPN-T1,1,0.11,No,,12.1; SPN-T2,3,4.43,Yes,,11.0; LDB-T1,2,0.33,No,20592,24.4; LDB-T2,1,0.49,No,16890,21.1; PRB-T1,1,0.42,No,,8.9; PRB-T2,1,0.49,No,,10.0; RLS-T1,1,0.45,No,,8.0; RLS-T2,3,4.98,No,49897,12.5; BNM-T1,1,0.38,No,,8.8; BNM-T2,1,0.21,No,,7.0; WDS-T1,1,0.23,No,21319,14.7; WDS-T2,1,0.27,No,,10.7; WML-T1,2,

## Where the solver left the ladder (main thread's read, against the three rules)

Path steps 1, 2, 5 and 6 read every field and applied every stated rule correctly: the latest issue of each report,
below-detection at half the limit, preservation class from O2/N2, the rewind years, the 330-day base sample, all seven
code 3 units at the shipped severities, the stale register dates, the rollovers and counter replacements, the UTC
historian joined on the New Zealand hour. Every ask figure matches the golden (27 tap changers, 7 past the interval,
6 wet transformers; the CSV differs only in the on-slate column). The miss is at the decisive analytical step, path
step 3: "DSL-T1 is about 0.6 ppm per 1,000 ops, LST-T2 about 0.6 and RLS-T2 about 0.36, steady across 12-15 intervals,
and all three have In-oil arcing tap changers: leakage from the tap-changer compartment, so excluded." That is the easy
attribution the card's analyst_test names (rung 3b), and the slate it files (SBG-T2, CGT-T1, SPN-T2) is rung 3b's. The
solver noted SBG-T2's "rising H2" but never read the gas RLS-T2's acetylene arrives with (C2H2/H2 0.64 against 9.8 and
8.2 at the two leaks). A valid analytical miss: the round passes the worth-it gate.

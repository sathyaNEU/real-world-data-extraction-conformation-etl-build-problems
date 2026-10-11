# solver round: round 4

**Proxy score 74.8 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 32.8 of 58). Main call LANDED. 1 of 4 ask items cracked (80 per cent of tokens).

## Main call

golden: Take Southbridge T2, Rolleston T2 and Coalgate T1 for the three 2027/28 internal inspections, in that order.

solver: Give the three 2027-28 internal inspections, in this order, to SBG-T2 Southbridge (code 3, severity 8.07, acetylene 4.7 to 12.9 ppm, 8.07 ppm/yr against a 1.0 limit), RLS-T2 Rolleston (code 3, severity 4.98, acetylene 3.9 to 9.0 ppm) and CGT-T1 Coalgate (code 3, severity 4.73, ethylene 106 to 140 ppm, 33.09 ppm/yr against a 7 limit); code-3 DSL-T1 (9.64) and LST-T2 (8.07) are left out because their acetylene rise with flat hydrogen and in-oil arcing tap changers points to tap-changer contamination rather than the main-tank fault ES-DGA-02 s5.2 requires, and SPN-T2 (4.43) and DFD-T1 (3.45) rank below the three.

tokens matched 3 of 4 (28, Take Southbridge, Rolleston, Coalgate)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| inspection_slate_2027-28.docx | 1 | 7 | 7 | 100% |
| inspection_slate_2027-28.docx | 2 | 31 | 47 | 66% |
| inspection_slate_2027-28.docx | 3 | 9 | 15 | 60% |
| dga_fleet_review.csv | 1 | 0 | 116 | 0% |

## Solver's path

1. dga_main_tank_results_2021-2026.csv: kept the latest issue per sample_id (s3.4; 1,077 rows to 1,072 samples; corrections on LDB-T2, LIN-T1, KRW-T1, SPF-T1, GDL-T2); '<LOD' read as LOD/2 (s3.5); latest sample per transformer is the Sep 2026 round (14-30 Sep)
2. Preservation class from latest O2/N2 (<=0.2 sealed); age band from sample year minus year of manufacture, or rewind year for DSL-T2 (2003) and CGT-T1 (1998), from asset_register_zone_transformers.xlsx
3. Base sample = most recent sample >=330 days before the latest (all Sep 2025, 366-378 days); 12-month increase = diff*365/days; compared with tables A1/A2/A3 to give 7 code 3 (DSL-T1 9.64, LST-T2 8.07, SBG-T2 8.07, RLS-T2 4.98, CGT-T1 4.73, SPN-T2 4.43, DFD-T1 3.45), 5 code 2, 32 code 1
4. Main-tank fault screen (s5.1-5.2): DSL-T1 and LST-T2 (in-oil arcing tap changers) show C2H2 +9.8 and +8.2 ppm with H2 +1 ppm, read as tap-changer contamination and excluded; SBG-T2 (vacuum tap changer, H2 +16) and RLS-T2 (H2 +8) kept; ethylene/methane thermal units kept
5. Ranked the remaining code 3 units by severity and took the top three for MSU-2 Held windows MSU2-2702/2705/2708 (mobile_substation_bookings_2027-28.xlsx); peak loads in the SCADA parquet (SBG-T2 5.9, RLS-T2 11.0, CGT-T1 4.0 MVA) are within MSU-2's 15 MVA, so no reordering
6. Tap ops: last OLTC SERVICE/INSPECTION from maintenance_log_2019-2026.xlsx (log beats stale register dates for 9 units); ops = sum of daily SCADA counter increments from 00:00 on the service date to 00:00 on 16 Oct 2026, adding 100,000 at 5-digit rollovers and restarting from zero where the counter was replaced; checked against the log's counter readings; GLT-T2 and SHF-T1 (pre-2021 services) = current counter minus log reading; past interval if >60,000 ops or >7 yrs, giving 7 units
7. Relative saturation: Ws = 10^(7.42-1670/(T+273)); T = label temperature (issue of record), otherwise SCADA top oil for the sample hour with NZ local time converted to UTC (historian is UTC, checked against labelled temperatures); 6 units above 30%

confidence: Medium: the code, severity, tap and water figures are mechanical and checked (counter readings match the log, the UTC offset matches labelled temperatures), but the slate depends on excluding DSL-T1 and LST-T2 as tap-changer contamination, which rests on the gas pattern and tap-changer type rather than any explicit statement in the files.

notes: Nothing in the folder records a leak from DSL-T1's or LST-T2's tap changer; if the board treats every code 3 unit as eligible, the slate becomes DSL-T1 first and an exact tie at 8.07 between LST-T2 and SBG-T2 that the files cannot break. Thermal survey and relay events had no bearing on the call.

### inspection_slate_2027-28.docx (solver's answers)
- Slate pick 1: SBG-T2, Southbridge; condition code 3; severity 8.07; gas acetylene C2H2 12.9 ppm (14 Sep 2026) vs 4.7 ppm base (8 Sep 2025), increase 8.07 ppm/yr vs rate limit 1.0 (free-breathing), above 95th percentile 6 ppm (free-breathing, 10-30 yrs); H2 12 to 28 ppm; vacuum tap changer
- Slate pick 2: RLS-T2, Rolleston; condition code 3; severity 4.98; gas acetylene C2H2 9.0 ppm (21 Sep 2026) vs 3.9 ppm (12 Sep 2025), 374 days, 4.98 ppm/yr vs limit 1.0 (sealed), above 95th percentile 2 ppm (sealed, 10-30); H2 46 to 54 ppm
- Slate pick 3: CGT-T1, Coalgate; condition code 3; severity 4.73; gas ethylene C2H4 140 ppm (28 Sep 2026) vs 106 ppm (18 Sep 2025), 375 days, 33.09 ppm/yr vs limit 7 (free-breathing), above 95th percentile 120 ppm (free-breathing, 10-30 yrs, age counted from 1998 rewind); CH4 64 ppm also above its 95th (50) and rate (3.50x)
- In-oil tap changers: ops since last service, past interval (as of SCADA 00:00 16 Oct 2026; limit 60,000 ops or 7 yrs): CGT-T1 27,923 No; CGT-T2 57,551 No; DFD-T1 21,895 No; DSL-T1 87,322 Yes; DSL-T2 20,955 No; DYL-T1 32,511 No; DYL-T2 87,029 Yes; GDL-T1 20,915 No; GLT-T1 75,013 Yes; GLT-T2 29,695 Yes (7.52 yrs since 9 Apr 2019); HOR-T1 3,909 No; KRW-T1 6,837 No; LDB-T1 20,592 No; LDB-T2 16,890 No; LIN-T1 16,064 No; LIN-T2 10,079 No; LST-T1 61,972 Yes; LST-T2 54,294 No; RLS-T2 49,897 No; SBG-T1 32,019 No; SHF-T1 23,553 Yes (7.16 yrs since 20 Aug 2019); SPF-T1 14,842 No; SPF-T2 11,034 No; TPR-T2 64,224 Yes; WDN-T1 38,209 No; WDS-T1 21,319 No; WML-T1 31,680 No. 27 in-oil tap changers, 7 past interval
- Transformers above 30% relative saturation at latest sample (%, 1 dp): SHF-T1 36.1; GDL-T1 34.9; WDN-T1 34.1; DYL-T1 33.1; TPR-T2 31.7; SPF-T1 31.5 (6 transformers)

### dga_fleet_review.csv (solver's answers)
- Per transformer: code, severity (2 dp), on slate, in-oil tap ops since service, relative saturation % (1 dp): BNM-T1 1,0.38,N,-,8.8; BNM-T2 1,0.21,N,-,7.0; CGT-T1 3,4.73,Y,27923,22.8; CGT-T2 1,0.28,N,57551,28.2; DFD-T1 3,3.45,N,21895,19.6; DFD-T2 1,0.16,N,-,11.7; DSL-T1 3,9.64,N,87322,21.5; DSL-T2 1,0.33,N,20955,17.0; DYL-T1 1,0.29,N,32511,33.1; DYL-T2 1,0.46,N,87029,23.9; GDL-T1 1,0.34,N,20915,34.9; GDL-T2 1,0.21,N,-,20.9; GLT-T1 1,0.19,N,75013,19.7; GLT-T2 2,0.30,N,29695,18.2; HOR-T1 1,0.49,N,3909,27.0; HOR-T2 1,0.25,N,-,15.6; KRW-T1 1,0.49,N,6837,28.5; KRW-T2 1,0.27,N,-,11.0; LDB-T1 2,0.33,N,20592,24.4; LDB-T2 1,0.49,N,16890,21.1; LIN-T1 1,0.14,N,16064,19.0; LIN-T2 1,0.22,N,10079,27.3; LST-T1 1,0.3

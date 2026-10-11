# solver round: round 2

**Proxy score 74.6 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 32.6 of 58). Main call LANDED. 1 of 4 ask items cracked (80 per cent of tokens).

## Main call

golden: Take Southbridge T2, Rolleston T2 and Coalgate T1 for the three 2027/28 internal inspections, in that order.

solver: Take SBG-T2 (Southbridge, code 3, severity 8.07, acetylene), RLS-T2 (Rolleston, code 3, severity 4.98, acetylene) and CGT-T1 (Coalgate, code 3, severity 4.73, ethylene) in that order in MSU-2 windows 1-3; DSL-T1 (9.64) and LST-T2 (8.07) are code 3 but excluded because their acetylene tracks tap operations at about 0.6 ppm per 1,000 operations (in-oil tap-changer leak, not a main-tank fault), and SPN-T2 (4.43) and DFD-T1 (3.45) rank 4th and 5th.

tokens matched 2 of 4 (28, Take Southbridge, Rolleston, Coalgate)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| inspection_slate_2027-28.docx | 1 | 7 | 7 | 100% |
| inspection_slate_2027-28.docx | 2 | 30 | 47 | 64% |
| inspection_slate_2027-28.docx | 3 | 9 | 15 | 60% |
| dga_fleet_review.csv | 1 | 1 | 116 | 1% |

## Solver's path

1. dga_main_tank_results_2021-2026.csv: kept the latest issue per sample_id (5 corrected samples, ES-DGA-02 3.4); results below the limit of detection set to half the limit (3.5) -> 1,072 samples of record
2. Latest sample per transformer (all from the Sept 2026 round); preservation class from latest O2/N2 (<=0.2 sealed); age band = sample year minus rewind year if any (DSL-T2 2003, CGT-T1 1998), else year of manufacture, from asset_register Transformers sheet
3. Base sample = most recent sample >=330 days before the latest (Sept 2025 samples, 366-378 days); twelve-month increase = (latest-base)*365/days; compared with tables A1/A2/A3 -> code 3: DSL-T1 9.64, LST-T2 8.07, SBG-T2 8.07, RLS-T2 4.98, CGT-T1 4.73, SPN-T2 4.43, DFD-T1 3.45; code 2: WML-T1, LDB-T1, GLT-T2, SPF-T1; 33 at code 1
4. Main-tank test (5.2): joined monthly samples with tap ops from scada_tap_counters_daily (rollovers +100000; counters replaced -> reset). DSL-T1 and LST-T2 acetylene rises at a constant ~0.6 ppm per 1,000 ops in every interval (in-oil tap-changer leak) -> excluded; SBG-T2 (vacuum tap changer) and RLS-T2 acetylene rise in steps unrelated to ops; CGT-T1, DFD-T1, SPN-T2 ethylene trends are thermal, not tap-linked -> main-tank list SBG-T2 8.07, RLS-T2 4.98, CGT-T1 4.73, SPN-T2 4.43, DFD-T1 3.45
5. mobile_substation_bookings: 3 Ellesmere held windows (12 Apr-21 May 2027, 23 Aug-1 Oct 2027, 31 Jan-10 Mar 2028) -> top three by descending severity: SBG-T2, RLS-T2, CGT-T1
6. Tap changers: 27 'In-oil arcing' units in the asset register; last service = latest OLTC SERVICE in maintenance_log (overrides 8 stale register dates); ops = SCADA counter at 16 Oct 2026 minus counter on service date, allowing for 6 rollovers and 7 counter replacements; GLT-T2/SHF-T1 pre-2021 services use the logged counter readings 3,642/17,728; interval 60,000 ops or 7 years (annex B) -> 7 past
7. Relative saturation: latest-issue moisture; T = label temperature, else the SCADA top-oil reading for the sampling hour (NZ time converted to UTC, Pacific/Auckland, DST from 27 Sep 2026); Ws = 10^(7.42-1670/(T+273)); RS = water/Ws*100 -> 6 above 30%

confidence: Moderately high: the code and severity arithmetic and the tap and moisture figures follow ES-DGA-02 directly. The main judgement is reading DSL-T1 and LST-T2 as tap-changer leaks, based on acetylene rising in proportion to tap operations.

notes: ES-DGA-02 gives no explicit test for main-tank versus tap-changer acetylene, so the exclusion of DSL-T1 and LST-T2 rests on the tap-operation correlation. 'Past interval' is judged at the 16 Oct 2026 extract date. The protection relay events and the thermal survey were not needed.

### inspection_slate_2027-28.docx (solver's answers)
- slate #1: SBG-T2, Southbridge, code 3, severity 8.07 (2 dp); gas acetylene C2H2 4.7->12.9 ppm, twelve-month increase 8.07 ppm vs rate limit 1.0 (free-breathing), above 95th percentile of 6 ppm; vacuum tap changer
- slate #2: RLS-T2, Rolleston, code 3, severity 4.98 (2 dp); gas acetylene C2H2 3.1->8.2 ppm, twelve-month increase 4.98 ppm vs rate limit 1.0 (sealed), above 95th percentile of 2 ppm
- slate #3: CGT-T1, Coalgate, code 3, severity 4.73 (2 dp); gas ethylene C2H4 106->140 ppm, twelve-month increase 33.1 ppm vs rate limit 7 (free-breathing), above 95th percentile of 120 ppm; methane also code-3
- in-oil tap changer table: ops since last service, past interval: Past interval (7): DSL-T1 87,322; DYL-T2 87,029; GLT-T1 75,013; TPR-T2 64,224; LST-T1 61,972; GLT-T2 29,695 (7.5 yr); SHF-T1 23,553 (7.2 yr). Not past (20): CGT-T2 57,551; LST-T2 54,294; WDN-T1 38,209; DYL-T1 32,511; SBG-T1 32,019; WML-T1 31,680; CGT-T1 27,923; RLS-T2 27,534; DFD-T1 21,895; WDS-T1 21,319; DSL-T2 20,955; GDL-T1 20,915; LDB-T1 20,592; LDB-T2 16,890; LIN-T1 16,064; SPF-T1 14,842; SPF-T2 11,034; LIN-T2 10,079; KRW-T1 6,837; HOR-T1 3,909 (operations, whole numbers)
- transformers above 30% relative saturation at latest sample: SHF-T1 36.1%; GDL-T1 34.9%; WDN-T1 34.1%; DYL-T1 33.1%; TPR-T2 31.7%; SPF-T1 31.5% (1 dp)

### dga_fleet_review.csv (solver's answers)
- 44 rows: code, severity (2 dp), on slate, tap ops since service (in-oil only), RS % (1 dp): BNM-T1,1,0.38,N,,8.8; BNM-T2,1,0.21,N,,7.0; CGT-T1,3,4.73,Y,27923,22.8; CGT-T2,1,0.28,N,57551,28.2; DFD-T1,3,3.45,N,21895,19.6; DFD-T2,1,0.16,N,,11.7; DSL-T1,3,9.64,N,87322,21.5; DSL-T2,1,0.33,N,20955,17.0; DYL-T1,1,0.29,N,32511,33.1; DYL-T2,1,0.46,N,87029,23.9; GDL-T1,1,0.34,N,20915,34.9; GDL-T2,1,0.21,N,,20.9; GLT-T1,1,0.19,N,75013,19.7; GLT-T2,2,0.30,N,29695,18.2; HOR-T1,1,0.49,N,3909,27.0; HOR-T2,1,0.25,N,,15.6; KRW-T1,1,0.49,N,6837,28.5; KRW-T2,1,0.27,N,,11.0; LDB-T1,2,0.33,N,20592,24.4; LDB-T2,1,0.49,N,16890,21.1; LIN-T1,1,0.14,N,16064,19.0; LIN-T2,1,0.22,N,10079,27.3; LST-T1,1,0.31,N,61

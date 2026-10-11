# solver round: round 5

**Proxy score 47.3 / 100** (recommendation 1.2 of 35, instruction 7.0 of 7, asks 39.0 of 58). Main call missed. 0 of 4 ask items cracked (80 per cent of tokens).

## Main call

golden: Take Southbridge T2, Rolleston T2 and Coalgate T1 for the three 2027/28 internal inspections, in that order.

solver: Take SBG-T2 (Southbridge, code 3, severity 8.07, acetylene), then CGT-T1 (Coalgate, code 3, severity 4.73, ethylene), then SPN-T2 (Springston, code 3, severity 4.43, ethylene) in the three MSU-2 windows; DSL-T1 (9.64), LST-T2 (8.07) and RLS-T2 (4.98) are code 3 but left off because their acetylene tracks tap operations at a constant rate (about 0.60 and 0.37 ppm per 1,000 operations), pointing to diverter leakage, not a main-tank fault; DFD-T1 (3.45) is fourth.

tokens matched 1 of 4 (28, Take Southbridge, Rolleston, Coalgate)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| inspection_slate_2027-28.docx | 1 | 5 | 7 | 71% |
| inspection_slate_2027-28.docx | 2 | 29 | 47 | 62% |
| inspection_slate_2027-28.docx | 3 | 9 | 15 | 60% |
| dga_fleet_review.csv | 1 | 88 | 116 | 76% |

## Solver's path

1. dga_main_tank_results_2021-2026.csv: kept the highest issue per sample_id (5 reissues); results below the detection limit set to half the limit (ES-DGA-02 3.4, 3.5); 1,072 samples of record; latest sample for all 44 transformers is in Sep 2026.
2. Preservation class from latest O2/N2; age band from rewind or manufacture year; thresholds from Tables A1/A2.
3. Base sample = most recent sample >=330 days before latest; 12-month increase; severity = max over 7 gases; 7 code 3 (DSL-T1 9.64, LST-T2 8.07, SBG-T2 8.07, RLS-T2 4.98, CGT-T1 4.73, SPN-T2 4.43, DFD-T1 3.45) and 4 code 2.
4. Main-tank fault test (5.2): paired acetylene increments between successive monthly samples with tap operations from scada_tap_counters_daily. DSL-T1, LST-T2 and RLS-T2 (all in-oil arcing tap changers per the register) give correlation 1.0 at a constant ~0.60, ~0.60 and ~0.37 ppm C2H2 per 1,000 operations, meaning diverter oil getting into the main tank, so they were excluded. SBG-T2 (vacuum tap changer) gives correlation -0.07; the ethylene-driven CGT-T1, SPN-T2 and DFD-T1 are thermal. Remaining order: SBG-T2 8.07, CGT-T1 4.73, SPN-T2 4.43, then DFD-T1 3.45.
5. Tap changers: 27 register 'In-oil arcing' units; last service = latest OLTC SERVICE in maintenance_log; rollovers and replacements; 7 past interval.
6. Water: latest sample of record; label temperature else SCADA top oil for the sampling hour with NZ local time converted to UTC; six above 30%.

confidence: High for the tap changer and water tables and for the code/severity figures; medium-high for the slate, which depends on reading the constant acetylene-per-operation pattern as diverter leakage (the folder does not state this criterion directly).

notes: ES-DGA-02 does not say how to tell a main-tank fault from a diverter-compartment leak, so excluding DSL-T1, LST-T2 and RLS-T2 rests on the acetylene-tap-operation correlation.

### inspection_slate_2027-28.docx (solver's answers)
- Slate position 1: SBG-T2, Southbridge, condition code 3, severity 8.07 (2 dp), gas acetylene C2H2: 4.7 ppm on 2025-09-08 to 12.9 ppm on 2026-09-14, 371 days, 8.07 ppm/yr vs rate limit 1.0 (free-breathing, O2/N2 0.327, age band 10-30)
- Slate position 2: CGT-T1, Coalgate, condition code 3, severity 4.73 (2 dp), gas ethylene C2H4: 106 to 140 ppm (2025-09-18 to 2026-09-28, 375 days), 33.1 ppm/yr vs limit 7 (free-breathing, rewound 1998 so age 28, band 10-30; 140 > 95th percentile 120)
- Slate position 3: SPN-T2, Springston, condition code 3, severity 4.43 (2 dp), gas ethylene C2H4: 89 to 125 ppm (2025-09-10 to 2026-09-16, 371 days), 35.4 ppm/yr vs limit 8 (sealed, O2/N2 0.071, band 10-30; 125 > 95th percentile 95)
- In-oil tap changer table: operations since last service, past interval (60,000 ops or 7 years, as at 2026-10-16): LST-T1 61,972 YES (ops); LST-T2 54,294 no; SBG-T1 32,019 no; DYL-T1 32,511 no; DYL-T2 87,029 YES (ops); DSL-T1 87,322 YES (ops); DSL-T2 20,955 no; LIN-T1 16,064 no; LIN-T2 10,079 no; LDB-T1 20,592 no; LDB-T2 16,890 no; RLS-T2 49,897 no; WDS-T1 21,319 no; WML-T1 31,680 no; KRW-T1 6,837 no; DFD-T1 21,895 no; TPR-T2 64,224 YES (ops); HOR-T1 3,909 no; CGT-T1 27,923 no; CGT-T2 57,551 no; GLT-T1 75,013 YES (ops); GLT-T2 29,695 YES (time, 7.5 yr since 2019-04-09); SHF-T1 23,553 YES (time, 7.2 yr since 2019-08-20); SPF-T1 14,842 no; SPF-T2 11,034 no; WDN-T1 38,209 no; GDL-T1 20,915 no. 7 past interval
- Wet oil table: relative saturation above 30% at latest sample (1 dp): SHF-T1 36.1%; GDL-T1 34.9%; WDN-T1 34.1%; DYL-T1 33.1%; TPR-T2 31.7%; SPF-T1 31.5% (6 transformers)

### dga_fleet_review.csv (solver's answers)
- Severity (2 dp) and condition code per transformer: DSL-T1 9.64 c3; LST-T2 8.07 c3; SBG-T2 8.07 c3; RLS-T2 4.98 c3; CGT-T1 4.73 c3; SPN-T2 4.43 c3; DFD-T1 3.45 c3; WML-T1 1.39 c2; LDB-T1 0.33 c2; GLT-T2 0.30 c2; SPF-T1 0.24 c2; LDB-T2 0.49; PRB-T2 0.49; HOR-T1 0.49; TPR-T1 0.49; KRW-T1 0.49 (raw 0.4875); DYL-T2 0.46; RLS-T1 0.45; PRB-T1 0.42; WML-T2 0.39; SHF-T2 0.39; BNM-T1 0.38; GDL-T1 0.34; DSL-T2 0.33; WDN-T2 0.32; LST-T1 0.31; SPF-T2 0.30; DYL-T1 0.29; WDN-T1 0.28; CGT-T2 0.28; KRW-T2 0.27; WDS-T2 0.27; TPR-T2 0.26; HOR-T2 0.25; WDS-T1 0.23; LIN-T2 0.22; GDL-T2 0.21; SHF-T1 0.21; BNM-T2 0.21; GLT-T1 0.19; DFD-T2 0.16; SBG-T1 0.15; LIN-T1 0
- On slate flag: Yes for SBG-T2, CGT-T1, SPN-T2; No for the other 41
- Tap operations since service (in-oil only, blank for 17 vacuum): Same 27 figures as the docx tap changer table
- Relative saturation at latest sample, % (1 dp): SHF-T1 36.1; GDL-T1 34.9; WDN-T1 34.1; DYL-T1 33.1; TPR-T2 31.7; SPF-T1 31.5; KRW-T1 28.5; CGT-T2 28.2; LIN-T2 27.3; HOR-T1 27.0; SBG-T1 26.7; LDB-T1 24.4; DYL-T2 23.9; CGT-T1 22.8; SPF-T2 22.4; LST-T1 22.2; DSL-T1 21.5; LDB-T2 21.1; GDL-T2 20.9; GLT-T1 19.7; DFD-T1 19.6; LIN-T1 19.0; WML-T2 19.0; GLT-T2 18.2; LST-T2 18.2; TPR-T1 17.9; DSL-T2 17.0; SHF-T2 16.9; WML-T1 16.1; HOR-T2 15.6; WDS-T1 14.7; WDN-T2 14.5; SBG-T2 13.9; RLS-T2 12.5; SPN-T1 12.1; DFD-T2 11.7; KRW-T2 11.0; SPN-T2 11.0; WDS-T2 10.7; PRB-T2 10.0; PRB-T1 8.9; BNM-T1 8.8; RLS-T1 8.0; BNM-T2 7.0

## Where the solver left the ladder (main thread's read, against the three rules)

Every field read and every stated rule applied correctly (latest issue, half the detection limit, preservation class
from O2/N2, rewind years, the 330-day base, all seven code 3 units at the shipped severities, the stale register dates,
rollovers and replacements, the pre-2021 counter readings, the UTC historian), and every ask figure matches the golden.
The miss is at the decisive analytical step: "DSL-T1, LST-T2 and RLS-T2 (all in-oil arcing tap changers per the
register) give correlation 1.0 at a constant ~0.60, ~0.60 and ~0.37 ppm C2H2 per 1,000 operations, meaning diverter oil
getting into the main tank, so they were excluded." Tracking alone (rung 3b), with no reading of the hydrogen each
acetylene brings: SBG-T2, CGT-T1, SPN-T2. A valid analytical miss; the round passes.

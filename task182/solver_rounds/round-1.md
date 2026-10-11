# solver round: round 1

**Proxy score 35.0 / 100** (recommendation 3.0 of 35, instruction 7.0 of 7, asks 25.0 of 58). Main call missed. 0 of 5 ask items cracked (80 per cent of tokens).

## Main call

golden: Offer make-good agreements to four owners for five bores: Yarrowmere Pastoral Co Pty Ltd for KV-LB04 and KV-LB05 (one agreement), Tondara Grazing Pty Ltd for KV-LB07, Bluebush Downs Pty Ltd for KV-LB10 and Cypress Ridge Pastoral Trust for KV-LB12.

solver: Offer two make-good agreements: Yarrowmere Pastoral Co Pty Ltd (one agreement covering KV-LB04 house bore, mine-caused decline 5.1 m, and KV-LB05 Ten Mile bore, 5.5 m, both against the 5 m Permian trigger) and Cypress Ridge Pastoral Trust (KV-LB12 creek bore, 4.5 m against the 2 m alluvium trigger); 3 bores, 2 offers; none of the four complainants' bores (KV-LB01 Saltbush Flat 0.7 m, KV-LB02 Brolga Plains 0.7 m, KV-LB06 Ghost Gum 0.6 m, KV-LB18 Bottletree 0.7 m) passes, because their falls of 4.63, 5.23, 4.84 and 8.70 m since baseline are drought, matched by the state reference bores RF01/RF02 (about -4.0/-4.1 m) and RF03 (about -5.1 m).

tokens matched 3 of 5 (Offer, Yarrowmere Pastoral Co Pty Ltd, Tondara Grazing Pty Ltd, Bluebush Downs Pty Ltd, Cypress Ridge Pastoral Trust)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| bore_impact_assessment.xlsx | 1 | 41 | 71 | 58% |
| make_good_recommendation.docx | 1 | 6 | 10 | 60% |
| make_good_recommendation.docx | 2 | 0 | 1 | 0% |
| make_good_recommendation.docx | 3 | 9 | 14 | 64% |
| make_good_recommendation.docx | 4 | 1 | 3 | 33% |

## Solver's path

1. Read prompt, MG-02 rev 3 PDF (2.1 static only, 2.2 MP in force, 2.3/2.4 logger daily mean in Queensland time, assessment month September 2026, 3.1 triggers 2 m unconsolidated / 5 m consolidated, 6.1 one agreement per owner), monitoring notes, register (18 bores, measuring points, network bores), contact log (complaints: LB01 3 Aug, LB02 19 Aug, LB06 2 Sep, LB18 15 Sep)
2. water_level_dips: normalised 190+ site spellings (code, RN, bare RN, KVLB, LB, lowercase) to 27 bores; feet to metres for IVH 2012-14 rounds; dropped 18 exact duplicates; excluded pumped dips (remarks containing 'pump', except the baseline remark); level = MP in force on the date minus dtw (LB07 MP 236.492 from 14 Nov 2023, LB08 214.807 from 27 Aug 2025)
3. logger_pressure + barometric_logger + logger_installations: inner join on UTC hour, column = (P - Pbaro)/9.80665, level = MP - sensor depth (per serial, incl. 2190446 at 37.75 m and 2213378 at 30.65 m) + column, trimmed to installed periods, UTC+10 days; September 2026 mean of daily means for LB02/04/05/12/15/18; check dips agree to about ±0.005 m
4. Baseline levels from register baseline SWL against the MP in force on the baseline date (e.g. LB07 197.90, LB08 206.08, LB12 218.28, LB18 254.45) gave the change-since-baseline column
5. Monthly pre-take (before Jul 2022) regressions of each bore on same-aquifer references: alluvium on RF01 or RF02 by best fit (slopes about 0.9-1.2; LB13/14 about 0.34), basalt on RF03 (0.18-0.25; LB18 1.74), Permian on KV-LB16 (1.45-1.66, residual about 0.08-0.1 m, with lags of a few months)
6. Mine-caused decline = predicted natural September 2026 level minus observed; gave LB12 4.5 (>2), LB04 5.1 and LB05 5.5 (>5), LB07 4.9 and LB10 4.8 (<5), all others at or below 1.8
7. Applied 6.1: Yarrowmere owns LB04+LB05, so one agreement; plus Cypress Ridge, giving 2 offers for 3 bores; all four complainants miss

confidence: Medium: LB12 and LB05 are clear calls, but LB04 (4.9-5.2 m across correction variants) and LB07 (4.5-5.1 m) sit on the 5 m Permian trigger, and the Permian correction depends on treating KV-LB16 as an unaffected control.

notes: The folder gives no Permian state reference bore and no EIS predicted drawdown extent, so treating KV-LB16 as the Permian climate control is an inference; the rainfall file could not reproduce the hydrographs, so it was not used for the correction.

### bore_impact_assessment.xlsx (solver's answers)
- September 2026 level, m AHD, 2 dp: LB01 209.51; LB02 205.24; LB03 204.86; LB04 207.77; LB05 214.47; LB06 209.61; LB07 195.44; LB08 201.27; LB09 199.16; LB10 203.49; LB11 238.12; LB12 209.50; LB13 202.33; LB14 201.88; LB15 241.33; LB16 209.84; LB17 243.13; LB18 245.75
- Change since baseline assessment, m, 2 dp: LB01 -4.63; LB02 -5.23; LB03 -4.64; LB04 -2.44; LB05 -2.49; LB06 -4.84; LB07 -2.46; LB08 -4.81; LB09 -4.69; LB10 -2.21; LB11 -2.59; LB12 -8.78; LB13 -0.98; LB14 -0.87; LB15 -3.02; LB16 +1.74; LB17 -2.68; LB18 -8.70
- Decline caused by the mine, m, 1 dp: LB01 0.7; LB02 0.7; LB03 0.8; LB04 5.1; LB05 5.5; LB06 0.6; LB07 4.9; LB08 0.8; LB09 0.6; LB10 4.8; LB11 1.2; LB12 4.5; LB13 0.0; LB14 0.0; LB15 1.8; LB16 0.0 (Permian control); LB17 1.3; LB18 0.7
- Impaired capacity yes/no: Yes: KV-LB04, KV-LB05 (trigger 5 m), KV-LB12 (trigger 2 m). No: the other 15 (LB01, LB02, LB03, LB06, LB07, LB08, LB09, LB10, LB11, LB13, LB14, LB15, LB16, LB17, LB18)

### make_good_recommendation.docx (solver's answers)
- Bores and properties that get offers: Yarrowmere (Yarrowmere Pastoral Co Pty Ltd): KV-LB04 house bore and KV-LB05 Ten Mile bore; Cypress Ridge (Cypress Ridge Pastoral Trust): KV-LB12 creek bore
- Number of offers: 2 make-good agreements (one per owner under MG-02 6.1), covering 3 bores
- Complainants missing the test and what lowered their bore: KV-LB01 Saltbush Flat (Ernest Walker): down 4.63 m since June 2022, about 0.7 m from the mine, the rest from the dry years, the same fall as state reference bore RF02 (-4.1 m). KV-LB02 Brolga Plains: down 5.23 m, about 0.7 m from the mine; this bore swings about 1.2 times the reference RF01, which fell 4.0 m in the drought. KV-LB06 Ghost Gum (Clarence Lewis): down 4.84 m, about 0.6 m from the mine; the drought fall at RF02, scaled to this bore's response, accounts for the rest; the 2 Sep dip was taken with the stock pump running and was excluded. KV-LB18 Bottletree: down 8.70 m against a 5 m b

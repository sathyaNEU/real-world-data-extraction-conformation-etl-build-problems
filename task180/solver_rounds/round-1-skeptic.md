# solver round: round 1, skeptic

**Proxy score 85.6 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 43.6 of 58). Main call LANDED. 4 of 7 ask items cracked (80 per cent of tokens).

## Main call

golden: Place the field team in Caithness for January to March 2027; it starts the quarter with 54 referrals.

solver: Place the field team in Caithness (CAI) for January to March 2027. The screening run on Monday 7 December 2026 refers 54 supplies there (12 main meters and 42 heating-only meters). That is 19 more than the runner-up, Elgin and Lossiemouth (ELG, 35). Lochaber (LOC), the patch Judith asked for, has the best confirmation rate over the last three winters (68.2%, 15 confirmed out of 22 visits where the officer got in) but only 8 referrals, the fewest of the eight patches. Caithness can take at most 552 visits in the quarter.

tokens matched 5 of 5 (54, Place, Caithness, January, March)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| field_team_q1_2027.pptx | 1 | 4 | 4 | 100% |
| field_team_q1_2027.pptx | 2 | 2 | 2 | 100% |
| field_team_q1_2027.pptx | 3 | 4 | 4 | 100% |
| field_team_q1_2027.pptx | 4 | 2 | 2 | 100% |
| field_team_q1_2027.pptx | 5 | 9 | 19 | 47% |
| field_team_q1_2027.pptx | 6 | 38 | 48 | 79% |
| patch_screen_q1_2027.csv | 1 | 0 | 1 | 0% |

## Solver's path

1. RP-07 v4 sections 2-8: run 7 Dec 2026; assessment w/c 12 Oct to w/c 30 Nov 2026; history w/c 14 Oct 2024 to w/c 5 Oct 2026; supply = one MPAN and its meter; patch as held in CIS.
2. Supplies sheet 2,960 main MPANs plus Related metering points 699 heating-only MPANs = 3,659 supplies, matching the reads parquet; credit scope 3,235.
3. Weekly kWh per MPAN from Monday 00:00 reads; 107 exchanges stitched; 3,838 missing Monday reads interpolated (none in assessment weeks); alternatives give the same referrals.
4. Mart not used for screening: it equals main plus heating-only meters (within 0.19 kWh on 76,158 weeks); screening it would give CAI 12, ELG 35.
5. Weekly HDD Monday-Sunday sums of hdd_15_5c by station.
6. Per supply OLS over 104 history weeks; flagged if 8-week actual at most 70% of expected and below expected every week: 362 flagged.
7. Exclusions by UPRN 14 Oct 2024 to 6 Dec 2026: occupier changes removed 116 (72 INV); heat pumps removed 72 (57 SPY).
8. Referred supplies: CAI 54, ELG 35, INV 19, SKY 17, SPY 16, NRN 14, FRS 11, LOC 8; independent rebuild identical.
9. Visits: 199 FieldLink + 271 FieldOps minus 30 re-keyed = 440; UTC to local; patch from CIS by UPRN.
10. Winters: 379 visits; 75 appeals matched (4 via FieldLink numbers); 23 overturned recoded; access 328, confirmed 159.
11. Capacity: 61 Scottish field days; Matthew Gill 56, Aaron O'Connor 54, Chloe Lewis 28; 138 days; visits per day floor(450/(70+travel)).

confidence: High

notes: No published prior figures to reproduce; checked by reconciling mart, account history and vends.

### field_team_q1_2027.pptx (solver's answers)
- Slide 1 title (the decision): Field team goes to Caithness (CAI) for January to March 2027: 54 referrals, 19 more than Elgin and Lossiemouth
- Chosen patch and its referral count: Caithness (CAI): 54 referred supplies (whole number) from the 7 Dec 2026 screening run
- Runner-up and gap: Runner-up Elgin and Lossiemouth (ELG): 35 referred supplies. Gap: 19 referrals (54 minus 35)
- Bar chart: referrals for all 8 patches, largest first: CAI 54 (highlighted), ELG 35 (labelled runner-up), INV 19, SKY 17, SPY 16, NRN 14, FRS 11, LOC 8. Total 174
- Slide 2 per patch: INV 64 / 26 / 40.6% / 690; NRN 38 / 22 / 57.9% / 552; FRS 30 / 14 / 46.7% / 552; ELG 71 / 37 / 52.1% / 690; SPY 33 / 15 / 45.5% / 552; LOC 22 / 15 / 68.2% / 414; CAI 41 / 17 / 41.5% / 552; SKY 29 / 13 / 44.8% / 414. All patches together: 328 visits with access, 159 confirmed (48.5%)

### patch_screen_q1_2027.csv (solver's answers)
- One row per patch: CAI Caithness: 54, 41, 17, 41.5, 552 (chosen). ELG Elgin and Lossiemouth: 35, 71, 37, 52.1, 690 (runner-up). INV Inverness City: 19, 64, 26, 40.6, 690. SKY Skye and Lochalsh: 17, 29, 13, 44.8, 414. SPY Strathspey: 16, 33, 15, 45.5, 552. NRN Nairn and Ardersier: 14, 38, 22, 57.9, 552. FRS Forres: 11, 30, 14, 46.7, 552. LOC Lochaber: 8, 22, 15, 68.2, 414

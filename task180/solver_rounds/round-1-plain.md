# solver round: round 1, plain

**Proxy score 81.3 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 39.3 of 58). Main call LANDED. 3 of 7 ask items cracked (80 per cent of tokens).

## Main call

golden: Place the field team in Caithness for January to March 2027; it starts the quarter with 54 referrals.

solver: Send the field team to Caithness (CAI) for 1 January to 31 March 2027. The RP-07 screening run on Monday 7 December 2026 gives Caithness 54 referred credit-paying supplies (12 primary meters and 42 heating-only related meters). The runner-up is Elgin and Lossiemouth (ELG) with 35, so the gap is 19. The other patches are Inverness City 19, Skye and Lochalsh 17, Strathspey 16, Nairn and Ardersier 14, Forres 11 and Lochaber 8. RP-07 section 7 places the team in the patch with the most referred supplies, so Judith's request for Lochaber does not meet the rule: Lochaber has only 8 referrals, even though its confirmation rate over the last three winters is the highest at 68.2%. The team can make up to 552 visits in Caithness this quarter.

tokens matched 5 of 5 (54, Place, Caithness, January, March)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| field_team_q1_2027.pptx | 1 | 2 | 4 | 50% |
| field_team_q1_2027.pptx | 2 | 2 | 2 | 100% |
| field_team_q1_2027.pptx | 3 | 4 | 4 | 100% |
| field_team_q1_2027.pptx | 4 | 2 | 2 | 100% |
| field_team_q1_2027.pptx | 5 | 9 | 19 | 47% |
| field_team_q1_2027.pptx | 6 | 37 | 48 | 77% |
| patch_screen_q1_2027.csv | 1 | 0 | 1 | 0% |

## Solver's path

1. RP-07: run Mon 7 Dec 2026; assessment weeks w/c 12 Oct to 30 Nov 2026; history 104 weeks w/c 14 Oct 2024 to 5 Oct 2026; weeks Monday 00:00 to Monday 00:00 local.
2. supply_point_register: 2,960 primary supply numbers plus 699 heating-only related metering points = 3,659 supplies, per the RP-07 glossary; related points take the primary's patch, UPRN and payment method; credit scope 3,235 supplies.
3. smart_daily_reads: weekly kWh per supply from Monday 00:00 register reads; 107 meter exchanges bridged; missing Monday reads interpolated; rp_mart_weekly_import rejected for screening because it sums each related point into its primary's metering system (mart = primary + related reads to within 0.2 kWh).
4. station_degree_days with patch_weather_stations.json: weekly HDD Monday to Sunday sums of hdd_15_5c.
5. Per supply OLS of weekly kWh on weekly HDD over the 104 history weeks; referral test 8-week actual at most 70% of expected and below expected all 8 weeks: 362 flagged; ratios 0.40-0.64, next group from 0.80.
6. Change of occupier exclusion removes 116 supplies (72 in INV), leaving 246.
7. Heat pump exclusion removes 72 supplies (57 in SPY), leaving 174.
8. Count by CIS rp_patch: CAI 54 (12 primary + 42 related), ELG 35, INV 19, SKY 17, SPY 16, NRN 14, FRS 11, LOC 8; screening the mart instead gives ELG 35, INV 19, NRN 14, SKY 13, CAI 12.
9. Visit logs: 199 FieldLink + 271 FieldOps minus 30 re-created = 440 unique visits; UTC converted; outcomes mapped; patch by UPRN.
10. Appeals: 75 matched (4 via legacy_job_no); 23 overturned recoded to no fault.
11. Winters: 379 visits, 328 with access, 159 confirmed (48.5%).
12. FW-3 and rota: visits per officer-day floor(450/(70+travel)); 61 field days after Scottish holidays; Matthew Gill 56, Aaron O'Connor 54, Chloe Lewis 28; team 138 field days.

confidence: High on the placement; high on the visits table; medium-high on capacity (Monday to Friday assumed).

notes: Last three winters read as the complete Oct-Mar winters 2023-24 to 2025-26; FW-3 does not define the working week, so field days taken Monday to Friday.

### field_team_q1_2027.pptx (solver's answers)
- Chosen patch and its referral count: Caithness (CAI): 54 referred supplies (whole number) from the 7 Dec 2026 screening run
- Runner-up and the gap: Elgin and Lossiemouth (ELG): 35 referred supplies; gap 19 referrals (54 - 35)
- Bar chart of referrals for all eight patches, largest first: CAI 54 (highlighted), ELG 35 (labelled runner-up), INV 19, SKY 17, SPY 16, NRN 14, FRS 11, LOC 8; total 174 referred supplies
- Decision stated in the slide title: Field team to Caithness for Jan-Mar 2027: 54 referrals, 19 ahead of Elgin and Lossiemouth (35)
- Slide 2 (for Judith): per patch over winters Oct 2023-Mar 2024, Oct 2024-Mar 2025 and Oct 2025-Mar 2026, the access visits (officer got in), diversions confirmed after appeals, confirmation rate (% to 1 dp) and max visits 1 Jan-31 Mar 2027: CAI 41 access / 17 confirmed / 41.5% / 552 max visits; ELG 71 / 37 / 52.1% / 690; INV 64 / 26 / 40.6% / 690; SKY 29 / 13 / 44.8% / 414; SPY 33 / 15 / 45.5% / 552; NRN 38 / 22 / 57.9% / 552; FRS 30 / 14 / 46.7% / 552; LOC 22 / 15 / 68.2% / 414. All patches together: 328 access, 159 confirmed, 48.5%. Team field days 138.

### patch_screen_q1_2027.csv (solver's answers)
- One row per patch: code, name, referred supplies, access visits, diversions confirmed, confirmation rate % (1 dp), max visits Q1 2027: CAI,Caithness,54,41,17,41.5,552 | ELG,Elgin and Lossiemouth,35,71,37,52.1,690 | INV,Inverness City,19,64,26,40.6,690 | SKY,Skye and Lochalsh,17,29,13,44.8,414 | SPY,Strathspey,16,33,15,45.5,552 | NRN,Nairn and Ardersier,14,38,22,57.9,552 | FRS,Forres,11,30,14,46.7,552 | LOC,Lochaber,8,22,15,68.2,414 (counts are whole numbers; rate to 1 dp; CAI is the chosen patch)

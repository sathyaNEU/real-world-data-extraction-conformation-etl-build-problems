# task125 submission

## Tags

**Domain:** Survey Research & Official Statistics, anomaly detection in official statistics (a first-interview recruitment cap accumulating through a rotating-panel household labour survey, separated from the labour market).
**Analytical objective:** Anomaly Detection & Diagnostics (how much of a quarter's rise in the unemployment rate is a fieldwork artifact, how the artifact builds as the capped intakes spread through the panel, and how long it stays in the published rates).

## 1. Final Recommendation

**Most of the July to September 2026 rise in the unemployment rate is the three-visit cap, not the labour market: 0.18 of the 0.27-point rise is the cap and 0.09 point the labour market, and the published unemployment rate will sit 0.39, 0.53, 0.62, 0.47 and 0.28 point above the six-visit rate from July to September 2026 to July to September 2027, the employment rate 1.42, 1.97, 2.44, 1.88 and 1.19 point below it, with six visits back from 1 April 2027.**

The cap removes the households found only at a fourth to sixth visit, mostly adults in work, and the panel keeps an intake for five quarters, so an intake recruited under the cap is short of them in every quarter it stays in the sample. The cap has run since the April to June 2026 intake, so by July to September two of the five intakes in the sample were recruited under it and by January to March 2027 four will be: the gap builds to 0.62 point and only then fades, and the published rates are back on a six-visit basis from April to June 2028. Not "the rise is real", which treats the cap as a wave-1 effect, gives both quarters the same 0.21-point gap and so leaves the whole 0.27-point rise to the labour market. Not the wave-1 difference carried unchanged into the later waves, which overstates every quarter. Not the gap on the January to March 2026 weights kept, which overstates the employment gap in every quarter, because the estimator rakes every sample to the population controls.

## 2. Critical Components

1. The cap's gap on the unemployment rate: **0.21** point in April to June 2026 and **0.39** point in July to September 2026, so **0.18** point of the published rise is the cap
2. The cap's gap on the employment rate: **-0.79** point in April to June and **-1.42** point in July to September, so **-0.63** point of the published change is the cap
3. July to September 2026 on six visits throughout: unemployment rate **5.47** per cent (published **5.86**, April to June published **5.59**, April to June on six visits **5.38**), so the labour market's share of the rise is **0.09** point
4. Employment on six visits throughout: **59.67** per cent in April to June and **59.96** in July to September, a rise of **0.29** point against the published fall of **0.34** point to **58.54** per cent
5. Unemployment rate gap, July to September 2026 to July to September 2027: **0.39**, **0.53**, **0.62**, **0.47**, **0.28** point
6. Employment rate gap over the same quarters: **-1.42**, **-1.97**, **-2.44**, **-1.88**, **-1.19** point

## 3. Step-by-Step Solution

1. Took each address's interview visit from the visit number of its interview call (the interview outcome of `hls_data_dictionary.md`) in `hls_call_records_2025q1_2026q3.csv`, joined to `hls_person_quarter_2023q1_2026q3.parquet` on the serial's first nine characters (the check digit of `extract_notes_2026-10-20.md`): the households a three-visit cap (`field_instruction_FI-2026-04_first_interview_visits.pdf`) would not have recruited are those interviewed at visit 4, 5 or 6.
2. Placed the four capped intakes (April to June 2026 to January to March 2027) in each quarter's sample by the five-wave rotation of `hls_methods_note_2025.pdf` section 1: waves 1 and 2 in July to September 2026, 1 to 3 in October to December, 1 to 4 in January to March 2027, 2 to 5 in April to June and 3 to 5 in July to September 2027, and wave 1 alone in April to June 2026.
3. Rebuilt the counterfactual on January to March 2026, the one quarter with no capped intake at any wave whose five intakes all carry visit histories: for each quarter removed the visit 4 to 6 households from the waves that quarter's capped intakes hold, raked the rest to the January to March controls of `population_controls_2023q1_2027q4.xlsx` by region and by age group and sex as the methods note sets out, and took the change in each rate as it defines them: unemployment gaps 0.21, 0.39, 0.53, 0.62, 0.47 and 0.28 point from April to June 2026, employment gaps -0.79, -1.42, -1.97, -2.44, -1.88 and -1.19.
4. Computed the published rates with the file's final weights: unemployment 5.59 per cent in April to June and 5.86 in July to September, a rise of 0.27; employment 58.88 and 58.54, a fall of 0.34.
5. Took the change in the gap, not the gap, as the cap's share of the published change, because the cap was already in April to June: unemployment 0.39 less 0.21 is 0.18 point of the 0.27-point rise, leaving 0.09 to the labour market; employment -1.42 less -0.79 is -0.63 point, so on six visits throughout employment rose 0.29 point.
6. Recommendation: most of the rise is the cap, the gap goes on building to 0.62 point in January to March 2027, and it is still 0.28 point in July to September 2027 with six visits back from 1 April 2027.
7. Counted the July to September 2026 intake's calls once per serial and visit number, the regions from `hls_address_register_2025q1_2026q3.csv`.
8. Matched April to June and July to September respondents on serial, sex and date of birth for the flows, and converted telephone hours (recorded as hours and minutes) to decimal hours before summing the employed's weighted hours.

## 4. Deliverable Answers

### hls_visit_limit_note_2026q3.docx
1. The July to September rise in the unemployment rate: 0.27 point to 5.86 per cent, of which 0.18 point is the cap and 0.09 point the labour market; on six visits throughout, 5.38 per cent in April to June and 5.47 in July to September.
2. The employment rate: a fall of 0.34 point to 58.54 per cent, the cap having taken 0.63 point off the change; on six visits throughout it rose 0.29 point, from 59.67 to 59.96 per cent.
3. The unemployment rate above the six-visit rate by 0.39 point in July to September 2026, 0.53 in October to December, 0.62 in January to March 2027, 0.47 in April to June and 0.28 in July to September 2027; the employment rate below it by 1.42, 1.97, 2.44, 1.88 and 1.19 point in the same quarters, and by 0.79 point in April to June 2026. Back on a six-visit basis from April to June 2028.
4. Chart on page 1: the published unemployment rate from January to March 2023 to July to September 2026 with the six-visit rate for the two capped quarters already published (5.38 and 5.47 against 5.59 and 5.86), beside bars of the projected gap for the five quarters to July to September 2027, the return to six visits from April to June 2027 marked.
5. Table on page 2: the gap in each rate for each quarter, with the number of capped intakes in the sample and the waves they hold (2 of 5 at waves 1 and 2; 3 of 5 at waves 1, 2 and 3; 4 of 5 at waves 1, 2, 3 and 4; 4 of 5 at waves 2, 3, 4 and 5; 3 of 5 at waves 3, 4 and 5).

### hls_visit_limit_path_2027.xlsx
1. Gap path, percentage points (unemployment rate, employment rate):
   - Jul-Sep 2026: 0.39, -1.42
   - Oct-Dec 2026: 0.53, -1.97
   - Jan-Mar 2027: 0.62, -2.44
   - Apr-Jun 2027: 0.47, -1.88
   - Jul-Sep 2027: 0.28, -1.19
2. April to June to July to September 2026: unemployment rate 5.59 to 5.86 published, gaps 0.21 and 0.39, so 5.38 to 5.47 on six visits throughout, change 0.27 of which the cap 0.18 and the labour market 0.09; employment rate 58.88 to 58.54 published, gaps -0.79 and -1.42, so 59.67 to 59.96 on six visits throughout, change -0.34 of which the cap -0.63 and the labour market 0.29.
3. First-interview visits to the July to September 2026 intake:
   - Velmouth: 3,866
   - Carrowdene: 2,378
   - Pellard: 1,851
   - Haskvale: 1,629
   - Tirrin: 1,408
   - Dunmarrow: 1,282
4. Share of April to June 2026 unemployed respondents employed in July to September 2026, percent:
   - Velmouth: 31.65 (75 of 237)
   - Carrowdene: 25.19 (34 of 135)
   - Pellard: 37.96 (52 of 137)
   - Haskvale: 24.11 (27 of 112)
   - Tirrin: 30.12 (25 of 83)
   - Dunmarrow: 29.03 (27 of 93)
5. Total weekly hours actually worked by the employed, July to September 2026, thousands:
   - Velmouth: 26,679.5
   - Carrowdene: 16,124.7
   - Pellard: 12,659.1
   - Haskvale: 10,624.5
   - Tirrin: 9,734.0
   - Dunmarrow: 7,648.3

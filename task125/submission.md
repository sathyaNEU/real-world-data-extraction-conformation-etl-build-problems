# task125 submission

## Tags

**Domain:** Survey Research & Official Statistics, anomaly detection in official statistics (a first-interview fieldwork cap in a rotating-panel household labour survey separated from the labour market).
**Analytical objective:** Anomaly Detection & Diagnostics (how much of a quarter's rise in the unemployment rate is a fieldwork artifact, and how long the artifact stays in the published rates).

## 1. Final Recommendation

**With six visits back from January 2027 the published unemployment rate will still sit 0.22, 0.37, 0.25, 0.19 and 0.07 point above the six-visit rate from July to September 2026 to July to September 2027, and the employment rate 0.74, 1.37, 1.11, 0.93 and 0.63 point below it; almost none of the July to September 2026 rise is the labour market, 0.22 of the 0.27-point rise being the three-visit cap and 0.05 point the labour market.**

The households the cap fails to recruit are found only at a fourth to sixth visit, mostly adults in work, and the panel would have kept them for five quarters, so both capped intakes hold the rates off the six-visit basis at every wave they occupy. Not "clean from January 2027", which treats the cap as a wave-1 effect and drops it the quarter six visits return. Not the wave-1 gap carried unchanged into the later waves, which overstates every 2027 quarter because the missing households' rates move back towards the rest after their first interview. Not the gap on the April to June weights kept, which overstates the employment gap in every quarter because the estimator rakes every sample to the population controls.

## 2. Critical Components

1. The cap's gap in July to September 2026: **0.22** point on the unemployment rate and **-0.74** point on the employment rate
2. July to September 2026 without the cap: unemployment rate **5.04** per cent (published **5.27**, April to June **4.99**), so the labour market's share of the rise is **0.05** point
3. Unemployment rate gap, July to September 2026 to July to September 2027: **0.22**, **0.37**, **0.25**, **0.19**, **0.07** point
4. Employment rate gap over the same quarters: **-0.74**, **-1.37**, **-1.11**, **-0.93**, **-0.63** point

## 3. Step-by-Step Solution

1. Took each address's interview visit from the visit number of its outcome 110 call in `hls_call_records_2024q1_2026q3.csv`, joined to `hls_person_quarter_2023q1_2026q3.parquet` on the serial's first nine characters (the check digit of `extract_notes_2026-10-20.md`): the households a three-visit cap (`field_instruction_FI-2026-07_first_interview_visits.pdf`) would not have recruited are those interviewed at visit 4, 5 or 6.
2. Placed the two capped intakes in each quarter's sample by the rotation of `hls_methods_note_2025.pdf` section 1: July to September 2026 at wave 1 in that quarter, waves 2 and 1 in October to December, waves 3 and 2 in January to March 2027, 4 and 3, then 5 and 4.
3. Applied the cap to April to June 2026, the last full quarter before it (methods note section 5): for each quarter, removed the visit 4 to 6 households from the waves the capped intakes occupy, raked the rest to the April to June controls of `population_controls_2023q1_2027q4.xlsx` by region and by age group and sex as the methods note sets out, and took the change in each rate as it defines them: unemployment gaps 0.22, 0.37, 0.25, 0.19 and 0.07 point, employment gaps -0.74, -1.37, -1.11, -0.93 and -0.63.
4. Computed the published rates with the file's final weights: unemployment 4.99 per cent in April to June and 5.27 in July to September, a rise of 0.27; employment 60.01 and 59.36, a fall of 0.65.
5. Took the cap's July to September gap off the published July to September rates: unemployment 5.04 per cent without the cap, 0.05 point above April to June; employment 60.10, 0.09 point above.
6. Recommendation: the rise is the cap, and the gap path of step 3 stands in every quarter to September 2027 with six visits back from January.
7. Counted the July to September 2026 intake's calls once per serial and visit number, the regions from `hls_address_register_2024q1_2026q3.csv`.
8. Matched April to June and July to September respondents on serial, sex and date of birth for the flows, and converted telephone hours (recorded as hours and minutes) to decimal hours before summing the employed's weighted hours.

## 4. Deliverable Answers

### hls_visit_limit_note_2026q3.docx
1. The July to September rise in the unemployment rate: 0.27 point to 5.27 per cent, of which 0.22 point is the cap and 0.05 point the labour market; 5.04 per cent without the cap.
2. The employment rate: a fall of 0.65 point to 59.36 per cent, of which the cap is 0.74 point; 60.10 per cent without the cap, 0.09 point above April to June.
3. With six visits from January 2027, the published unemployment rate above the six-visit rate by 0.37 point in October to December 2026, 0.25 in January to March 2027, 0.19 in April to June and 0.07 in July to September 2027; the employment rate below it by 1.37, 1.11, 0.93 and 0.63 point (0.74 in July to September 2026).
4. Chart on page 1: the published unemployment rate from January to March 2023 to July to September 2026 with the July to September rate without the cap (5.04 against 5.27), beside bars of the projected gap for the five quarters to July to September 2027, the January 2027 return to six visits marked.
5. Table on page 2: the gap in each rate for each quarter, with the waves the capped intakes occupy.

### hls_visit_limit_path_2027.xlsx
1. Gap path, percentage points (unemployment rate, employment rate):
   - Jul-Sep 2026: 0.22, -0.74
   - Oct-Dec 2026: 0.37, -1.37
   - Jan-Mar 2027: 0.25, -1.11
   - Apr-Jun 2027: 0.19, -0.93
   - Jul-Sep 2027: 0.07, -0.63
2. July to September 2026 split: unemployment rate 4.99 to 5.27 published, 5.04 without the cap, change 0.27 of which the cap 0.22 and the labour market 0.05; employment rate 60.01 to 59.36 published, 60.10 without the cap, change -0.65 of which the cap -0.74 and the labour market 0.09.
3. First-interview visits to the July to September 2026 intake:
   - Velmouth: 3,945
   - Carrowdene: 2,360
   - Pellard: 1,856
   - Haskvale: 1,737
   - Tirrin: 1,469
   - Dunmarrow: 1,212
4. Share of April to June 2026 unemployed respondents employed in July to September 2026, percent:
   - Velmouth: 30.77 (72 of 234)
   - Carrowdene: 30.58 (37 of 121)
   - Pellard: 35.45 (39 of 110)
   - Haskvale: 39.22 (40 of 102)
   - Tirrin: 28.72 (27 of 94)
   - Dunmarrow: 27.14 (19 of 70)
5. Total weekly hours actually worked by the employed, July to September 2026, thousands:
   - Velmouth: 27,055.5
   - Carrowdene: 16,009.7
   - Pellard: 12,455.6
   - Haskvale: 11,070.1
   - Tirrin: 9,858.6
   - Dunmarrow: 8,103.1

# solver round: round 1

**Proxy score 44.5 / 100** (recommendation 3.3 of 35, instruction 7.0 of 7, asks 34.2 of 58). Main call missed. 1 of 6 ask items cracked (80 per cent of tokens). Ask share kept 59%. Gate: ASKS LEAK.

## Main call

golden: Commission 42 places for the 2027 Reading Partnership.

solver: Commission 28 Reading Partnership places for 2027: 28 of the 264 primary schools have an underlying Year 5 reading average below 480, using the REML random-effects model (fitted overall mean 496.48; school, year-group and student variances 271.39, 86.09 and 4,880.86) over the 2024-2026 sittings. The 28 places serve 5,531 Year 3-6 students in 2027 and need 5,776 km per fortnightly round across the Brinrigg, Carnbrae, Haskwick South, Kirkanby and Tullgate hubs.

tokens matched 2 of 3 (42, Commission, Reading Partnership)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| reading_partnership_2027.xlsx | 1 | 1 | 2 | 50% |
| reading_partnership_2027.xlsx | 2 | 7 | 13 | 54% |
| reading_partnership_2027.xlsx | 3 | 9 | 16 | 56% |
| reading_partnership_2027.xlsx | 4 | 5 | 16 | 31% |
| reading_partnership_2027_hubs.png | 1 | 5 | 8 | 62% |
| reading_partnership_2027_hubs.png | 2 | 1 | 1 | 100% |

## Solver's path

1. Read prompt.txt, the guidelines docx (one place per partner school; hub-to-school-and-back road travel each fortnight), LT-AS-04 (school random effect plus year-group-within-school random effect plus student residual, REML, every school included, Year 5 reading modelled alone, one scale across 2024-2026) and data_team_notes.txt.
2. Loaded Year 5 reading results for participating students only: 2024 legacy extract (YR_LVL 05, TEST_CD RD, PART_CD P) gave 10,232 rows; 2025 portal sheet 'Year 5' (header row 5, Reading, P) gave 10,400; 2026 export (Year 5, reading, participated) gave 10,324. Total 30,956 students, 264 schools, 792 school-year groups. No duplicates; all 264 codes match the register's primary schools.
3. Fitted the nested random-effects model by REML in numpy with Nelder-Mead, checked against a brute-force matrix likelihood. Results: overall mean 496.48, school variance 271.39, year-group variance 86.09, student variance 4,880.86.
4. Estimated each school's underlying average as overall mean plus its estimated school effect. 28 schools are below 480, against 56 by raw pooled mean.
5. Matched the 2027 hub servicing plan (5 sheets, 264 schools) to the register on normalised name plus locality, expanding Nth/Upr/Hts. All 264 matched uniquely. Joined region from the register.
6. Restored four-character codes in the census (zfill(4)) and summed 2026 Years 2-5 headcounts as the 2027 Year 3-6 cohort: 5,531 students across the 28 schools.
7. Joined hub_school_road_distances.csv on plan hub plus four-character school code. Fortnightly km = 2 x sum of one-way km per hub: Brinrigg 251 to 502, Carnbrae 1,106 to 2,212, Haskwick South 221 to 442, Kirkanby 631 to 1,262, Tullgate 679 to 1,358; total 5,776.
8. Region shares = region places / 28, per cent to one decimal; region and hub student counts are sums of the rolled-forward cohort.

confidence: High on 28 places and the regional split, since the REML fit converged and matches the brute-force check. Medium-high on students and km, which depend on rolling the census forward a year and on using the 2027 plan rather than the February 2026 Facilities directory for hubs.

notes: With current 2026 Years 3-6 instead of the rolled-forward cohort, students would total 5,408 (Coastal 163, Metropolitan North 854, Metropolitan South 3,205, Northern 213, Southern 323, Western 650). With the February 2026 Facilities hubs, km would be Brinrigg 612, Carnbrae 392, Kirkanby 3,500, Tullgate 1,358. The 2027 plan sends 1203 (Treardine) to Carnbrae at 854 km one way, and the files do not say why.

### reading_partnership_2027.xlsx (solver's answers)
- Total places: Places = 28 (whole number)
- Each region's share of places: Coastal 7.1% (2 places); Metropolitan North 14.3% (4); Metropolitan South 35.7% (10); Northern 10.7% (3); Southern 14.3% (4); Western 17.9% (5); per cent to one decimal
- Year 3-6 students served in 2027 by region: Coastal 153; Metropolitan North 893; Metropolitan South 3,359; Northern 204; Southern 305; Western 617; total 5,531 students (whole numbers)
- Students served per hub: Brinrigg 2,284; Carnbrae 2,051; Haskwick South 70; Kirkanby 570; Tullgate 556; total 5,531 students (whole numbers)
- Road km of one fortnightly round per hub: Brinrigg 502 km (8 schools); Carnbrae 2,212 km (7); Haskwick South 442 km (1); Kirkanby 1,262 km (5); Tullgate 1,358 km (7); total 5,776 km (whole numbers)

### reading_partnership_2027_hubs.png (solver's answers)
- Chart of each hub's fortnightly km: Brinrigg 502 km; Carnbrae 2,212 km; Haskwick South 442 km; Kirkanby 1,262 km; Tullgate 1,358 km (whole numbers)

## Main thread's reading

- **Main call: missed.** The golden commissions 42 places; the solver commits to 28. The first grade run's token match called it LANDED on "Commission" and "Reading Partnership" alone; re-graded with `--landed no`.
- **Where it left the ladder: the decisive analytical step, exactly the design's default path.** It read every file correctly, fitted the filed LT-AS-04 model by REML (variance components matching the golden fit), and then counted the schools whose model average (overall mean plus the predicted school effect) is below 480: 28, the default path's figure as built. It never formed the schools' probabilities of an underlying average below 480. It also rejected the raw three-year count (56). This is a miss at the analytical rung, not a misread field or a misapplied rule: the analyst test as written on the card.
- **Ask gate, adjudicated by figures.** The token share (59 per cent, one item "cracked") counts the region and hub names every answer lists. By figures the solver matches none of the 25 graded ask figures: its region shares (7.1, 14.3, 35.7, 10.7, 14.3, 17.9), students (5,531 in all) and kilometres (5,776 in all) are all off the golden (15.5, 25.6, 12.2, 16.7, 14.1, 15.9; 7,072; 8,327), because every ask is the golden's probability weighting on a segment; the png title item names Haskwick South in the golden and the solver's longest round is Carnbrae (the name was matched only because the solver lists every hub). Ask share kept by figures: 0 per cent, no item cracked. The ask gate holds.
- **Both ask devices were handled correctly by this solver** (the census rolled forward a year, hubs from the 2027 plan), so the devices are not what holds the asks for a response that misses the call; the coupling to the golden weighting is. The pair arithmetic in the design note already assumes a solver that lands the call keeps most of the asks (the cracker at about 65), with the pair held by the main ladder.
- **Decision: pass.** The round goes to the stage 6b repair of the deferred findings, then the determinism judge.

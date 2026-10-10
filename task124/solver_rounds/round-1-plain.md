# solver round: round 1, plain

**Proxy score 89.7 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 47.7 of 58). Main call LANDED. 5 of 8 ask items cracked (80 per cent of tokens).

## Main call

golden: Split the 400 MW summer block as Coast 120 MW, East 30, Far West 0, North 0, North Central 210, South Central 25, Southern 15 and West 0.

solver: File a 400 MW split of North Central 210 MW (42 lots), Coast 120 MW, East 30 MW, South Central 25 MW, Southern 15 MW, and 0 MW for Far West, North and West. Coast is not where the summer risk sits. Once the 31 Harlan Ridge cold-storage sites are counted at about 0.90 of their 186.0 MW enrolled demand, North Central carries the largest uncovered 1-in-10 exposure at 340 MW, against Coast's 251 MW. After the block, the largest uncovered exposure left on any book is Southern's 132 MW.

tokens matched 12 of 12 (400, 120, 15, Split, Coast, East, Far West, North, North Central, South Central, Southern, West)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| summer_block_committee.pptx | 1 | 10 | 10 | 100% |
| summer_block_committee.pptx | 2 | 10 | 17 | 59% |
| summer_block_committee.pptx | 3 | 7 | 7 | 100% |
| summer_block_committee.pptx | 4 | 3 | 3 | 100% |
| summer_block_committee.pptx | 5 | 7 | 7 | 100% |
| summer_block_split.xlsx | 1 | 10 | 22 | 45% |
| summer_block_split.xlsx | 2 | 24 | 45 | 53% |
| summer_block_split.xlsx | 3 | 17 | 17 | 100% |

## Solver's path

1. Coming book: open enrolment rows only (end_date blank) in enrollment_extract_20270409.csv, one row per ESI ID. In North Central there are 2,713 AMEND rows that duplicate open NEW rows; an amendment replaces the row it amends, so only one is kept. Counting both would add 275 MW to North Central (1,579.3 instead of 1,304.3 MW). All 3,845 starts since October have a matching switch confirm, and every book agrees with the load-profile zone in the premise register.
2. Rebuilt enrolled maximum demand at each summer's system peak date. It matches Table 1 of summer_2026_risk_report.pdf (for example Coast 1,464.8 MW). Settled true-up load at the published peak hour (HE17, or HE18 in 2024 and 2025) also matches (Coast 707.2 MW in 2026).
3. Each summer is restated at the coming book, the same replay the report uses: settled peak-hour load divided by enrolled maximum demand at that peak, times the coming book's enrolled maximum demand.
4. Harlan Ridge Cold Storage (account SC-4497203, from billing_accounts.csv) has 31 refrigerated-warehouse IDR sites (NAICS 493120) that moved in during February and March 2027, with 186.0 MW of enrolled demand in North Central. They are taken out of the book-ratio scaling, which runs at about 0.48. Instead they are loaded at the refrigerated peak-hour factor, measured from the Business Saver members' IDR reads.
5. The members were curtailed on every system peak day (bsaver_credits), so their peak-hour reads cannot be used directly; on those days they run at about 0.60 of maximum demand. Each site's baseline follows the program terms: the 10 most recent business days without a call, excluding Independence Day and Labor Day as observed. That gives a factor of about 0.900 of maximum demand in every summer (0.9002 to 0.9010). Harlan Ridge is not in the 2027 program, so its load is not curtailed.
6. 1-in-10 load is the 90th percentile of the 10 restated summers, inclusive linear method. Hedges are the summer MW from hedge_positions_20270409.xlsx, which also match the matched version of record in the blotter. Uncovered exposure before the block: North Central 340, Coast 251, East 159, South Central 153, Southern 147, Far West 114, West 106, North 96 MW.
7. Placed 80 lots of 5 MW one at a time, each to the book with the largest remaining uncovered exposure, ties going to the book listed first in the policy. Result: North Central 210, Coast 120, East 30, South Central 25, Southern 15 MW. The same split comes out whether exposures are rounded to whole MW first or not. Largest exposure left after the block: Southern 132 MW.
8. Premiums: Gulfline, Pecos (spreadsheet, sellers matched to counterparty codes by legal name) and Trinity quotes, joined to quote_decisions by reference and revision, keeping ACCEPTED only. Writers must have been approved on the day the quote was sent, which drops all seven Mesquite Flats (C0188) quotes because its approval ended 31 March 2027; C0231 in April is Saltgrass. Premiums convert to USD per MW-month at 5x16 hours for Gulfline and Pecos (352/336/352/336 for Jun/Jul/Aug/Sep, net of NERC holidays) and 7x16 hours for Trinity (480/496/496/480). The lowest is taken per load zone and month, with books mapped to zones by the 2027 book map (East is now LZ_HOUSTON).
9. Average fixed price: in confirm_match_log the latest status per amendment decides; the version of record is the latest amendment whose latest status is MATCHED. Kept Jun–Sep 2027 strips only, mapped portfolios to books through portfolio_books, and weighted by MWh using 1,376 hours for 5x16 and 1,952 hours for 7x16.

confidence: Medium-high. The premium and fixed-price figures follow written desk rules and come out the same however they are worked. The split depends on loading the Harlan Ridge sites at the measured refrigerated factor of about 0.90. Leaving them at the book ratio would give North Central 145, Coast 135, East 45, South Central 40, Southern 35 MW. Loading them at full enrolled demand would give North Central 225, Coast 115, East 25, South Central 20, Southern 15 MW.

notes: The files don't fully settle how far the Business Saver curtailment should be modelled. The members renewed for 2027, so history was not adjusted for their curtailment. The lenders' zone-share view and the report's replay at the 2026 book, which shows Coast as largest, were treated as context, not as the basis for the split.

### summer_block_committee.pptx (solver's answers)
- Slide 1 split (MW, adds to 400): Coast 120, East 30, Far West 0, North 0, North Central 210, South Central 25, Southern 15, West 0. Total 400 MW (80 lots of 5 MW).
- Chart bars: uncovered exposure before the block, largest first (whole MW): North Central 340, Coast 251, East 159, South Central 153, Southern 147, Far West 114, West 106, North 96
- Lots shaded on each bar (MW): North Central 210, Coast 120, East 30, South Central 25, Southern 15, Far West 0, West 0, North 0
- Line at the largest uncovered exposure any book still carries after the block: 132 MW (Southern)
- Title that reads as the split: 400 MW block: North Central 210, Coast 120, East 30, South Central 25, Southern 15 MW; no book is left above 132 MW uncovered

### summer_block_split.xlsx (solver's answers)
- Lots per book (MW): Coast 120, East 30, Far West 0, North 0, North Central 210, South Central 25, Southern 15, West 0 (total 400)
- Uncovered exposure before the block (whole MW): Coast 251, East 159, Far West 114, North 96, North Central 340, South Central 153, Southern 147, West 106
- Uncovered exposure after the block (whole MW): Coast 131, East 129, Far West 114, North 96, North Central 130, South Central 128, Southern 132, West 106
- Supporting working: 1-in-10 peak-hour load (P90 inclusive, MW) and summer hedges (MW): 1-in-10 load: Coast 725.91, East 304.17, Far West 208.91, North 176.12, North Central 705.00, South Central 433.19, Southern 267.09, West 241.14. Hedges: Coast 475, East 145, Far West 95, North 80, North Central 365, South Central 280, Southern 120, West 135
- Option premium in USD per MW-month, nearest dollar, by book and month (Jun / Jul / Aug / Sep): Coast (LZ_HOUSTON) 2348 / 5171 / 8082 / 3031; East (LZ_HOUSTON from 2027) 2348 / 5171 / 8082 / 3031; Far West (LZ_WEST) 2971 / 5920 / 9206 / 3753; North (LZ_WEST) 2971 / 5920 / 9206 / 3753; North Central (LZ_NORTH) 2237 / 4852 / 7550 / 2970; South Central (LZ_SOUTH) 2513 / 5369 / 8525 / 3211; Southern (LZ_SOUTH) 2513 / 5369 / 8525 / 3211; West (LZ_WEST) 2971 / 5920 / 9206 / 3753
- Average fixed price on existing summer hedges, USD/MWh to the cent: Coast 78.92, East 75.91, Far West 75.52, North 75.91, North Central 75.80, South Central 72.74, Southern 77.93, West 76.88
- Total block premium (derived, USD): About $7,277,445 (Coast $2,235,782; East $558,946; North Central $3,697,949; South Central $490,480; Southern $294,288)

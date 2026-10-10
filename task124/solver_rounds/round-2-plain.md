# solver round: round 2, plain

**Proxy score 96.6 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 54.6 of 58). Main call LANDED. 7 of 8 ask items cracked (80 per cent of tokens).

## Main call

golden: Split the 400 MW summer block as Coast 120 MW, East 30, Far West 0, North 0, North Central 210, South Central 25, Southern 15 and West 0.

solver: Split the 400 MW (80 lots of 5 MW) as follows: Coast 120, East 30, Far West 0, North 0, North Central 210, South Central 25, Southern 15, West 0. Gregory Sheppard's view is wrong because North Central, not Coast, now carries the largest uncovered summer exposure. Before the block, North Central is uncovered by 340 MW and Coast by 251 MW. The reason is 31 new refrigerated-warehousing (NAICS 493120) interval-metered sites in North Central, 186 MW of maximum demand starting February to March 2027. They are not in the Business Saver demand-response programme, so at the peak they will run near 98% of their maximum demand, not at the book's historical ratio of about 0.47. After the block, the largest uncovered exposure any book still carries is 132 MW (Southern). Total option premium is about $7.28M.

tokens matched 10 of 12 (400, 120, 15, Split, Coast, East, Far West, North, North Central, South Central, Southern, West)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| summer_block_committee.pptx | 1 | 10 | 10 | 100% |
| summer_block_committee.pptx | 2 | 17 | 17 | 100% |
| summer_block_committee.pptx | 3 | 7 | 7 | 100% |
| summer_block_committee.pptx | 4 | 3 | 3 | 100% |
| summer_block_committee.pptx | 5 | 7 | 7 | 100% |
| summer_block_split.xlsx | 1 | 22 | 22 | 100% |
| summer_block_split.xlsx | 2 | 24 | 45 | 53% |
| summer_block_split.xlsx | 3 | 17 | 17 | 100% |

## Solver's path

1. Policy (summer_risk_policy_2027.docx) and the 2026 close-out report define each book's exposure: for each of the 10 closed summers (2017-2026), take the book's true-up settled load in ERCOT's published system-peak hour (ercot_summer_system_peaks.csv, zone_settled_load_s17_s26.csv) and divide it by the book's enrolled maximum demand on the peak date. Apply that ratio to the coming book, take the 90th percentile with the inclusive linear method, and subtract the position-report hedges. Recomputing the report's Table 1 and Table 2 this way reproduces them exactly.
2. Coming book, from enrollment_extract_20270409.csv: of the open enrolments, 2,713 are AMEND rows (all North Central, broker B417). Each duplicates an open NEW row on the same ESI ID, so I deduplicated by ESI ID. That gives 54,248 premises, matching the 54,248 ACTIVE premises in the premise register. North Central maximum demand is 1,304.3 MW, not the 1,579.3 MW you get without deduplicating. Other books: Coast 1,503.5, East 648.3, Far West 431.7, North 382.5, South Central 898.1, Southern 569.4, West 503.8 MW.
3. Joining the premise register's NAICS codes found 31 new North Central interval-metered sites with NAICS 493120 (refrigerated warehousing), 186.0 MW of maximum demand, started February to March 2027. Business Saver members (the 2027 roster, mapped to ESI IDs through billing_accounts.csv) are 14 cold-storage and ice sites. They were called on every system-peak day and curtailed to about 0.60 of maximum demand. The new sites cannot join until they have a full summer of reads, so they will not curtail in 2027.
4. Uncurtailed cold-storage load at the peak, from idr_hourly_reads_summers_2017_2026.parquet: on each peak day, the 493120 member sites' average load in the uncalled hours (hours ending 11-14 and 19-20) divided by maximum demand is about 0.981-0.982 every year. North Central's load for each year = book ratio x (coming maximum demand minus 186.0) + that year's cold-storage ratio x 186.0. Its 90th percentile is 705.3 MW, against 609.7 MW from a plain book-ratio replay. Using a flat 0.98, or taking member sites out of the book ratio, changes it by less than 0.3 MW and leaves the split the same.
5. 1-in-10 loads minus hedges (position report, 5x16 plus 7x16 MW: 475/145/95/80/365/280/120/135) give uncovered exposures of 250.9/159.9/113.9/96.1/340.3/155.1/147.1/106.1 MW for Coast/East/Far West/North/North Central/South Central/Southern/West.
6. Placed the 5 MW lots one at a time to the largest remaining exposure, ties to the book listed first. Result: Coast 120, East 30, North Central 210, South Central 25, Southern 15, the rest 0. Running it on whole-MW-rounded exposures gives the same split. The largest exposure left after the block is 132.09 MW (Southern). The naive replay (no deduplication fix for the new sites' behaviour, book ratio only) would give Coast 140 / North Central 130, which is the Coast-led view.
7. Premiums: pooled option_quotes_s27.csv with the Pecos sheet (seller names mapped to counterparty codes through desk_counterparties.csv). Kept only quotes logged ACCEPTED in quote_decisions.csv whose writer was approved on the send date. That drops 7 Mesquite Flats (C0188) quotes, whose approval ended 2027-03-31, and keeps C0231 as Saltgrass. Converted to USD per MW-month using notional hours: 5x16 is 352/336/352/336 hours and 7x16 is 480/496/496/480 for June-September, from the NERC calendar (5 July and 6 September are holidays). Took the lowest per zone and month and mapped books to zones as of 2027, which puts East in LZ_HOUSTON.
8. Hedge prices: the version of record is the latest amendment whose final confirmation status is MATCHED (disputed or withdrawn amendments revert to the prior one). I kept the June-September 2027 strips, rolled portfolios up to books, and weighted fixed prices by MWh (MW x 1,376 hours for 5x16, x 1,952 for 7x16).

confidence: Medium-high. The split is the same under every variant tried for the cold-storage ratio and under exposures rounded to whole MW. Uncovered figures can move by about 0.3 MW depending on how the uncurtailed cold-storage ratio is estimated. Premium and hedge-price figures follow the desk procedures directly.

notes: I did not adjust for Business Saver curtailment by existing members, because all 12 member accounts renewed for 2027 and their curtailment is already inside the historical peak-hour loads. I treated the lenders' zone-share view, the day-ahead forecasts and the temperature file as not part of the policy's measure.

### summer_block_split.xlsx (solver's answers)
- Lots per book (MW): Coast 120; East 30; Far West 0; North 0; North Central 210; South Central 25; Southern 15; West 0; total 400 MW
- Uncovered exposure per book after the block (whole MW): Coast 131; East 130; Far West 114; North 96; North Central 130; South Central 130; Southern 132; West 106
- Uncovered exposure per book before the block (whole MW): Coast 251; East 160; Far West 114; North 96; North Central 340; South Central 155; Southern 147; West 106
- 1-in-10 load in the system peak hour (MW) and summer hedges (MW): Load: Coast 726, East 305, Far West 209, North 176, North Central 705, South Central 435, Southern 267, West 241. Hedges: Coast 475, East 145, Far West 95, North 80, North Central 365, South Central 280, Southern 120, West 135
- Option premium per book and month, USD per MW-month, nearest dollar (Jun/Jul/Aug/Sep 2027): Coast 2348/5171/8082/3031; East 2348/5171/8082/3031 (bought in LZ_HOUSTON from 2027); Far West 2971/5920/9206/3753; North 2971/5920/9206/3753; North Central 2237/4852/7550/2970; South Central 2513/5369/8525/3211; Southern 2513/5369/8525/3211; West 2971/5920/9206/3753
- Average fixed price on each book's existing summer 2027 hedges (USD/MWh, to the cent): Coast 78.92; East 75.91; Far West 75.52; North 75.91; North Central 75.80; South Central 72.74; Southern 77.93; West 76.88
- Block premium (USD): Total about $7,277,410 at the rounded per-MW prices ($7,277,445 unrounded). By book: Coast 2,235,840; East 558,960; North Central 3,697,890; South Central 490,450; Southern 294,270; Far West, North and West 0

### summer_block_committee.pptx (solver's answers)
- Slide 1 split (MW): Coast 120, East 30, Far West 0, North 0, North Central 210, South Central 25, Southern 15, West 0 = 400 MW
- Chart bars: uncovered exposure before the block, largest first (MW), with lots shaded: North Central 340 (210 lots), Coast 251 (120), East 160 (30), South Central 155 (25), Southern 147 (15), Far West 114 (0), West 106 (0), North 96 (0)
- Line at the largest uncovered exposure after the block: 132 MW (Southern)
- Chart title: 400 MW block: North Central 210, Coast 120, East 30, South Central 25, Southern 15; no book left above 132 MW uncovered

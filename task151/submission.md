## Tags

**Domain:** General Statistics & Data Science (resampling and simulation methods: the expected value of stepped plate-appearance bonuses priced from the distribution of comparable whole seasons, each season's starts read at the player's new lineup slot's plate appearances per start).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Accrue $4,250,000 at signing for the plate-appearance bonuses in the five free-agent hitters' 2027 contracts.**
Each bonus is priced at the share of the 1,440 seasons of the non-catcher regulars in the vendor's January 31 depth charts, 2021 to 2026, whose starts, read at the plate appearances per start of the player's 2027 lineup slot, reach its threshold: the basis with the lowest score in FIN-14 4.4's look-back over the 748 hitter-seasons of 2023 to 2026. Not the vendor's 2027 projections with a band from their past misses (30.3% worse in the look-back), which carry each player's full recent seasons at a higher slot for his old club; not the players' own seasons; and not the starting nines' seasons taken whole (26.1% worse), which keep the catchers in and ignore where each hitter bats.

## 2. Critical Components

1. Accrual by player: Sawyer Lusk **$500,000**; Andres Rivas **$1,000,000**; Drew Brock **$600,000**; Ángel Medina **$1,200,000**; Mike Meeks **$900,000**.
2. Plate appearances per start fall from **4.7** batting first to **3.8** batting ninth, and the depth chart bats the five Lusk fifth, Rivas sixth, Brock seventh, Medina eighth, Meeks ninth.
3. FIN-14 4.4's look-back over the **748** hitter-seasons of 2023 to 2026 ranks the regulars' seasons of starts at the slot ahead of the vendor's projection with a band and of the players' own seasons.

## 3. Step-by-Step Solution

1. Joined lsf_batting_2021_2024.txt (plate appearances AB + BB + HBP + SH + SF + CI, per lsf_feed_notes.txt) through lsf_player_id_crosswalk.csv to lsf_batting_2025_2026.csv: 276,378 batting lines, 2021 to 2026.
2. Took the lineup rows of hvbd_winter_depth_charts_2021_2026.xlsx other than catchers, 1,440 seasons, and counted each player's starts that season for every club (a start is a starter's line): 391 of the seasons had 155 starts or more and 178 had fewer than 100.
3. Plate appearances per start by lineup slot over all starters' lines, 2021 to 2026, fall from 4.72 batting first to 3.83 batting ninth; at the five's 2027 slots they are 4.25 batting fifth, 4.14 batting sixth, 4.04 batting seventh, 3.94 batting eighth, 3.83 batting ninth.
4. Ran the look-back of FIN-14 4.4 on the 748 hitter-seasons of 2023 to 2026 (a starting lineup of the January 31 depth charts and 100 plate appearances in each of the two seasons before), each basis built from what was published before the season: the regulars' seasons at the slot scored 0.1730; the vendor's projection with a band from its misses 0.2254; the players' own last three seasons 0.2698; the starting nines' plate appearances taken whole 0.2182.
5. For each bonus line in term_sheets_2027_free_agent_hitters.pdf, the probability under FIN-14 4.2 and 4.3 is the share of those seasons whose starts times the player's 2027 slot rate reach the threshold, and the expected amount is the bonus times that share.
6. Summed each player's expected amounts and rounded to the nearest $100,000: Sawyer Lusk $500,000; Andres Rivas $1,000,000; Drew Brock $600,000; Ángel Medina $1,200,000; Mike Meeks $900,000.
7. Summed the five players' unrounded amounts and rounded to the nearest $250,000 (FIN-14 6): $4,250,000; the rounded player figures add to $4,200,000.

## 4. Deliverable Answers

### pa_bonus_accrual_2027.xlsx

1. Accrual for each player and in total:
   - Sawyer Lusk: $500,000
   - Andres Rivas: $1,000,000
   - Drew Brock: $600,000
   - Ángel Medina: $1,200,000
   - Mike Meeks: $900,000
   - Total: $4,250,000
2. Injured-list stints since the start of the 2024 season, date each took effect and regular-season days covered:
   - Sawyer Lusk: took effect May 4, 2024, 68 days
   - Ángel Medina: took effect May 19, 2024, 10 days
   - Ángel Medina: took effect June 2, 2024, 14 days
   - Mike Meeks: took effect August 9, 2024, 8 days
   - Drew Brock: took effect August 14, 2024, 13 days
   - Mike Meeks: took effect March 25, 2025, 13 days
   - Drew Brock: took effect June 13, 2026, 76 days
   - Andres Rivas: took effect July 8, 2026, 14 days
   - Sawyer Lusk: took effect September 11, 2026, 17 days
3. Plate-appearance bonuses paid for each season, player by player and in total:
   - 2024 season, Edwin Cedeno: $200,000
   - 2024 season, Jonathan Vasquez: $125,000
   - 2024 season, total: $325,000
   - 2025 season, Jonathan Vasquez: $375,000
   - 2025 season, Gregorio Candelario: $300,000
   - 2025 season, Juan Nunez: $225,000
   - 2025 season, total: $900,000
   - 2026 season, Jacob Briggs: $262,500
   - 2026 season, Gregorio Candelario: $150,000
   - 2026 season, total: $412,500

### pa_bonus_accrual_memo_2027.docx

1. One-page note for the audit file stating the accrual of $4,250,000 and each player's amount: Sawyer Lusk $500,000; Andres Rivas $1,000,000; Drew Brock $600,000; Ángel Medina $1,200,000; Mike Meeks $900,000.

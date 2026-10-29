## Tags

**Domain:** General Statistics & Data Science (resampling and simulation methods: the expected value of stepped plate-appearance bonuses priced from the distribution of comparable whole seasons, each season's starts read at the player's new lineup slot's plate appearances per start).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Accrue $4,250,000 at signing for the plate-appearance bonuses in the five free-agent hitters' 2027 contracts.**
Each bonus is priced at the share of the 1,440 seasons of the non-catcher regulars in the vendor's January 31 depth charts, 2021 to 2026, whose starts, read at the plate appearances per start of the player's 2027 lineup slot, reach its threshold: the basis with the lowest score in FIN-14 4.4's look-back over the 748 hitter-seasons of 2023 to 2026. Not the vendor's 2027 projections with a band from their past misses, which carry each player's full recent seasons at a higher slot for his old club; not the players' own seasons; and not the starting nines' seasons taken whole, which keep the catchers in and ignore where each hitter bats; each scores higher in the look-back.

## 2. Critical Components

1. Accrual by player: Sawyer Lusk **$500,000**; Andres Rivas **$1,000,000**; Drew Brock **$600,000**; Ángel Medina **$1,200,000**; Mike Meeks **$900,000**.
2. Plate appearances per start fall from **4.7** batting first to **3.8** batting ninth, and the depth chart bats the five Lusk fifth, Rivas sixth, Brock seventh, Medina eighth, Meeks ninth.
3. FIN-14 4.4's look-back over the **748** hitter-seasons of 2023 to 2026 ranks the regulars' seasons of starts at the slot ahead of the vendor's projection with a band and of the players' own seasons.

## 3. Step-by-Step Solution

1. Joined lsf_batting_2021_2024.txt (plate appearances AB + BB + HBP + SH + SF + CI, per lsf_feed_notes.txt) through lsf_player_id_crosswalk.csv to lsf_batting_2025_2026.csv: 276,378 batting lines, 2021 to 2026.
2. Took the lineup rows of hvbd_winter_depth_charts_2021_2026.xlsx other than catchers, 1,440 seasons, and counted each player's starts that season for every club (a start is a starter's line): 391 of the seasons had 155 starts or more and 178 had fewer than 100.
3. Plate appearances per start by lineup slot over all starters' lines, 2021 to 2026, fall from 4.72 batting first to 3.83 batting ninth; at the five's 2027 slots they are 4.25 batting fifth, 4.14 batting sixth, 4.04 batting seventh, 3.94 batting eighth, 3.83 batting ninth.
4. Ran the look-back of FIN-14 4.4 (working paper CF-14.4) on the 748 hitter-seasons of 2023 to 2026 (a starting lineup of the January 31 depth charts and 100 plate appearances in each of the two seasons before), each basis built from what was published before the season: the regulars' seasons of starts at the slot, a tested catcher priced from the catcher regulars' seasons and every other hitter from the non-catcher regulars', scored 0.1730, the lowest; the vendor's projection with a band, the players' own seasons and the starting nines' seasons taken whole each scored higher.
5. For each bonus line in term_sheets_2027_free_agent_hitters.pdf, the probability under FIN-14 4.2 and 4.3 is the share of those seasons whose starts times the player's 2027 slot rate reach the threshold, and the expected amount is the bonus times that share.
6. Summed each player's expected amounts and rounded to the nearest $100,000: Sawyer Lusk $500,000; Andres Rivas $1,000,000; Drew Brock $600,000; Ángel Medina $1,200,000; Mike Meeks $900,000.
7. Summed the five players' unrounded amounts and rounded to the nearest $250,000 (FIN-14 6): $4,250,000; the rounded player figures add to $4,200,000.
8. For each player whose contract in ral_player_contract_register_2023_2026.xlsx carries other playing-time terms, took each season's payments in ral_payroll_player_earnings_2023_2026.csv on the schedule the register's header note files (a half in the October 15 run and a half in the January 15 run after it, the whole in the October run after a contract's last season), whatever the code (the legacy payroll paid the October halves on E45 OTHER BONUS), net of the October 2025 void and reissue, less the All-Star bonus a legacy October line carries and, after a contract's last season, the salary the contract deferred to its end (its register salary less the E01 salary lines paid, each season), each legacy line read by its name (number 01661 is Yordy Benítez in 2023 and Gilmar Pietersz in 2025), and counted the half no January run paid (Max White's for 2023, Joe Livingston's for 2024) to its season from his next October line, which exceeds the January half after it by exactly that half: 2023 $525,000; 2024 $1,005,000; 2025 $1,085,000.

## 4. Deliverable Answers

### pa_bonus_accrual_2027.xlsx

1. Accrual for each player and in total:
   - Sawyer Lusk: $500,000
   - Andres Rivas: $1,000,000
   - Drew Brock: $600,000
   - Ángel Medina: $1,200,000
   - Mike Meeks: $900,000
   - Total: $4,250,000
2. Playing-time bonuses other than plate-appearance bonuses paid for each season, player by player and in total:
   - 2023 season, Yordy Benítez: $55,000
   - 2023 season, Julio Casilla: $60,000
   - 2023 season, Carlos Lara: $140,000
   - 2023 season, Santiago Ruiz: $150,000
   - 2023 season, Max White: $120,000
   - 2023 season, total: $525,000
   - 2024 season, Carlos Lara: $300,000
   - 2024 season, Joe Livingston: $100,000
   - 2024 season, Tyler Reed: $170,000
   - 2024 season, Sam Robertson: $90,000
   - 2024 season, Santiago Ruiz: $225,000
   - 2024 season, Max White: $120,000
   - 2024 season, total: $1,005,000
   - 2025 season, Johnny Blair: $140,000
   - 2025 season, Carlos Lara: $200,000
   - 2025 season, Joe Livingston: $100,000
   - 2025 season, Gilmar Pietersz: $120,000
   - 2025 season, Tyler Reed: $255,000
   - 2025 season, Sam Robertson: $90,000
   - 2025 season, Max White: $180,000
   - 2025 season, total: $1,085,000

### pa_bonus_accrual_memo_2027.docx

1. One-page note for the audit file stating the accrual of $4,250,000 and each player's amount: Sawyer Lusk $500,000; Andres Rivas $1,000,000; Drew Brock $600,000; Ángel Medina $1,200,000; Mike Meeks $900,000.

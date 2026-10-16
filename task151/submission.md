## Tags

**Domain:** General Statistics & Data Science (resampling and simulation methods: the expected value of stepped plate-appearance bonuses priced from the distribution of comparable whole seasons, each season's starts read at the player's new lineup slot's plate appearances per start).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Accrue $3,500,000 at signing for the plate-appearance bonuses in the five free-agent hitters' 2027 contracts.**
Each bonus is priced at the share of the 1,440 seasons of the non-catcher regulars in the vendor's January 31 depth charts, 2021 to 2026, whose starts, read at the plate appearances per start of the player's 2027 lineup slot, reach its threshold. Not the vendor's 2027 projections with a band from their past misses, which carry each player's healthy recent seasons at his old club's higher slot and spread a season symmetrically when a regular's season is a near-full run of starts or one long injured-list loss. Not the players in the clubs' opening-day lineups, which drop the planned regulars hurt in spring training and keep the fill-ins who started for them.

## 2. Critical Components

1. Accrual by player: Jairo Calderón **$700,000**; Kevin Weeks **$800,000**; Ramon Figueroa **$800,000**; Eric Dobbs **$600,000**; Dylan Harlow **$600,000**.
2. Plate appearances per start fall from **4.7** batting first to **3.8** batting ninth, and the depth chart bats the five Calderón fourth, Weeks fifth, Figueroa sixth, Dobbs seventh, Harlow ninth.

## 3. Step-by-Step Solution

1. Joined lsf_batting_2021_2024.txt (plate appearances AB + BB + HBP + SH + SF + CI, per lsf_feed_notes.txt) through lsf_player_id_crosswalk.csv to lsf_batting_2025_2026.csv: 276,175 batting lines, 2021 to 2026.
2. Took the lineup rows of hvbd_winter_depth_charts_2021_2026.xlsx other than catchers, 1,440 seasons, and counted each player's starts that season for every club (a start is a starter's line): 379 of the seasons had 155 starts or more and 242 had fewer than 100.
3. Plate appearances per start by lineup slot over all starters' lines, 2021 to 2026, fall from 4.73 batting first to 3.84 batting ninth; at the five's 2027 slots they are 4.38 batting fourth, 4.26 batting fifth, 4.15 batting sixth, 4.05 batting seventh, 3.84 batting ninth.
4. For each bonus line in term_sheets_2027_free_agent_hitters.pdf, the probability under FIN-14 4.2 and 4.3 is the share of those seasons whose starts times the player's 2027 slot rate reach the threshold, and the expected amount is the bonus times that share.
5. Summed each player's expected amounts and rounded to the nearest $100,000: Jairo Calderón $700,000; Kevin Weeks $800,000; Ramon Figueroa $800,000; Eric Dobbs $600,000; Dylan Harlow $600,000.
6. Summed the five players' unrounded amounts and rounded to the nearest $250,000: $3,500,000.

## 4. Deliverable Answers

### pa_bonus_accrual_2027.xlsx

1. Accrual for each player and in total:
   - Jairo Calderón: $700,000
   - Kevin Weeks: $800,000
   - Ramon Figueroa: $800,000
   - Eric Dobbs: $600,000
   - Dylan Harlow: $600,000
   - Total: $3,500,000
2. Injured-list stints since the start of the 2024 season, date each took effect and regular-season days covered:
   - Jairo Calderón: took effect May 4, 2024, 66 days
   - Eric Dobbs: took effect May 18, 2024, 11 days
   - Eric Dobbs: took effect June 2, 2024, 14 days
   - Dylan Harlow: took effect August 9, 2024, 9 days
   - Ramon Figueroa: took effect August 15, 2024, 13 days
   - Dylan Harlow: took effect March 25, 2025, 15 days
   - Ramon Figueroa: took effect June 13, 2026, 76 days
   - Kevin Weeks: took effect July 8, 2026, 14 days
   - Jairo Calderón: took effect September 11, 2026, 17 days
3. Plate-appearance bonuses paid for each season, player by player and in total:
   - 2024 season, Carson Bickford: $420,000
   - 2024 season, Andrés Acevedo: $300,000
   - 2024 season, total: $720,000
   - 2025 season, Zach Strickland: $225,000
   - 2025 season, Shota Nakagawa: $100,000
   - 2025 season, total: $325,000
   - 2026 season, Elijah Mosley: $187,500
   - 2026 season, Shota Nakagawa: $150,000
   - 2026 season, Kody Bagwell: $87,500
   - 2026 season, total: $425,000

### pa_bonus_accrual_memo_2027.docx

1. One-page note for the audit file stating the accrual of $3,500,000 and each player's amount: Jairo Calderón $700,000; Kevin Weeks $800,000; Ramon Figueroa $800,000; Eric Dobbs $600,000; Dylan Harlow $600,000.

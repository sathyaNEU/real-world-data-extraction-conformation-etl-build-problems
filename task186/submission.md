## Tags

**Domain:** Survey Research & Official Statistics (anomaly detection in a mandatory price-reporting scheme); secondary Economics & Econometrics.
**Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**The pass-through inquiry before the 1 January 2027 levy rise should examine Tallis Petroleum.**
30 per cent of Tallis's examined stations passed on more than the 1 January 2026 rise with the false discovery rate held at 5 per cent, against the standard's bar of one in ten, and no station of the other six brands did. Not Harbourline Fuels, whose stations' margins rose most across the change but by no more than Brackwater's and Port Ostley's price cycles move a station's 28-day margin when the levy does not change.

## 2. Critical Components

1. Stations examined at the 1 January 2026 change: **369**.
2. Share of each brand's examined stations found at a 5 per cent false discovery rate: Tallis Petroleum **30 per cent**, every other brand **0 per cent**.

## 3. Step-by-Step Solution

1. Rebuilt each station's regular price from price_change_log_regular_2025-01-01_2026-11-15.csv (UTC to local time as extract_notes_2026-11-16.md gives it, old numbers joined to new through station_renumbering_2026-06-08.csv, a change received twice kept once) and took its time-weighted daily price from 06:00 to 22:00 local (PM-04 2.2).
2. Took the daily margin under PM-04 2.3: the daily price net of the 5 per cent sales tax, less the gasoline levy in carbon_levy_regulation_schedule_2.pdf (21.92 cents a litre in 2025, 25.38 in 2026), less the latest published regular rack price in terminal_rack_prices_2024-12_2026-11.csv.
3. Took each station's margin change across 1 January 2026 (PM-04 3.1) and kept the 369 stations carrying a monitored brand in station_register_2026-11-16.xlsx that day with a daily price on 20 or more days of each window (PM-04 3.2).
4. Judged each station's change against the 28-day changes its own margin made at every date in the log whose two windows hold no levy change (p is the share of those changes at least as large), since every area's margins cycle over five to nine weeks and a station's day-to-day variation does not show the cycle.
5. Applied Benjamini-Hochberg at 5 per cent across the 369 stations (PM-04 3.3): 28 found, all Tallis, a 30 per cent share against 0 for every other brand, so PM-04 4.1 names Tallis Petroleum.
6. Counted regular litres from fuel_sales_survey_returns_2026.csv: the latest revision of each return for the month it reports, on the station that filed it (the holder in fuel_sales_survey_frame_2026-11.csv, except 8 references given from August 2026 to stations newly added to the frame, whose January to March returns belong to the closed station at the site address the return carries in station_register_2026-11-16.xlsx), under the brand that station carried that month.
7. Counted the stations each brand prices itself from price_submissions_2026-11.csv: stations carrying the brand on 1 December 2026 whose November regular-price changes mostly came at the brand's push times, the minutes of the day at which three or more of its stations submitted through the API (Tallis 27).
8. Recommended Tallis Petroleum for the 2027 inquiry.

## 4. Deliverable Answers

### pass_through_inquiry_2027.docx

1. The inquiry should examine Tallis Petroleum.
2. Share of each brand's examined stations found, to the nearest ten per cent:
   - Garrow Fuels: 0 per cent
   - Harbourline Fuels: 0 per cent
   - Oxbury Fuels: 0 per cent
   - Pellow Gas: 0 per cent
   - Strathlowe Energy: 0 per cent
   - Tallis Petroleum: 30 per cent
   - Wexcombe Petroleum: 0 per cent
3. Chart on page 2: thousand litres of regular sold at the stations then carrying each brand, one bar for each of January, February and March 2026 for each of the seven brands, Tallis's bars labelled.

### inquiry_scope_2027.xlsx

1. Stations each brand prices itself on 1 December 2026:
   - Garrow Fuels: 5
   - Harbourline Fuels: 15
   - Oxbury Fuels: 8
   - Pellow Gas: 13
   - Strathlowe Energy: 9
   - Tallis Petroleum: 27
   - Wexcombe Petroleum: 10
2. Litres of regular sold at the stations then carrying each brand, thousands, January, February and March 2026:
   - Garrow Fuels: 12,461; 12,051; 13,829
   - Harbourline Fuels: 15,059; 14,690; 16,563
   - Oxbury Fuels: 11,386; 11,450; 13,127
   - Pellow Gas: 12,659; 11,802; 13,619
   - Strathlowe Energy: 12,721; 12,200; 13,855
   - Tallis Petroleum: 26,040; 25,076; 28,690
   - Wexcombe Petroleum: 11,593; 11,204; 12,851

## Tags

**Domain:** General Statistics & Data Science (data integration, record linkage and entity resolution: the authority's stand log linked to three operators' flight logs and its registers into turns, each turn's need left-censored by the time its 2026 schedule gave it).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Send back the minimum ground times filed for Norvale Connect flown by Pellmont Aviation, Embraer 175 (35 minutes), Tellura Express flown by Pellmont Aviation, Embraer 175 (40 minutes) and Tellura Express flown by Sable Coast Air, Dash 8-400 (30 minutes); accept the other three.**
An estimated 27, 26 and 31 per cent of those relationships' 2026 peak turns would need longer than the filed time, against the 20 per cent SFG-3 allows; the shortest ground times the authority would accept from them are 40, 45 and 35 minutes, and from the three it accepts 40 (filed 40), 30 (filed 30) and 30 (filed 35). Not accepting all six, which counts only the overruns the records show and divides by every turn (no relationship above 9 per cent), although most 2026 turns had more time than the new filings and finished inside it; not sending all six back, which reads each turn's time on the stand as its need (at least 74 per cent everywhere), although a turn ready early waited for its scheduled departure.

## 2. Critical Components

1. Turns at the E gates with on-block from 15 June to 15 September 2026: **2,731** (Norvale Connect flown by Pellmont Aviation, Embraer 175), **1,114** (Norvale Connect flown by Grayling Air, ATR 72-600), **2,398** (Norvale Connect flown by Sable Coast Air, Dash 8-400), **1,023** (Tellura Express flown by Pellmont Aviation, Embraer 175), **930** (Tellura Express flown by Sable Coast Air, Dash 8-400) and **1,016** (Grayling Air, ATR 72-600).
2. Estimated share of each relationship's peak turns needing longer than its filing: **27 per cent** (Norvale Connect flown by Pellmont Aviation, Embraer 175, filed 35), **6 per cent** (Norvale Connect flown by Grayling Air, ATR 72-600, filed 40), **7 per cent** (Norvale Connect flown by Sable Coast Air, Dash 8-400, filed 30), **26 per cent** (Tellura Express flown by Pellmont Aviation, Embraer 175, filed 40), **31 per cent** (Tellura Express flown by Sable Coast Air, Dash 8-400, filed 30) and **1 per cent** (Grayling Air, ATR 72-600, filed 35).
3. Shortest ground time each relationship's turns allow under the standard: **40 minutes** (Norvale Connect flown by Pellmont Aviation, Embraer 175; 8 per cent at 40, 27 per cent five minutes shorter), **40 minutes** (Norvale Connect flown by Grayling Air, ATR 72-600; 6 per cent at 40, 31 per cent five minutes shorter), **30 minutes** (Norvale Connect flown by Sable Coast Air, Dash 8-400; 7 per cent at 30, 29 per cent five minutes shorter), **45 minutes** (Tellura Express flown by Pellmont Aviation, Embraer 175; 6 per cent at 45, 26 per cent five minutes shorter), **35 minutes** (Tellura Express flown by Sable Coast Air, Dash 8-400; 5 per cent at 35, 31 per cent five minutes shorter) and **30 minutes** (Grayling Air, ATR 72-600; 8 per cent at 30, 30 per cent five minutes shorter).

## 3. Step-by-Step Solution

1. Built turns from kelderby_aodb_stand_events_jun_sep_2026.csv: registrations read without the hyphen, each on-block at an E stand paired with the same aircraft's next off-block on the same operating day, 03:00 to 02:59 (SFG-3 2.2, towed turns kept, night stops out), and kept the turns with on-block from 15 June to 15 September 2026.
2. Gave each turn the relationship of its departing flight: the callsign's number in the flight number blocks of kdy_affiliate_register.xlsx and the aircraft type of its registration in kdy_regional_aircraft_register.csv.
3. Joined each departure to its operator's log by flight number and date (pellmont_kdy_flight_log_s26.csv from UTC to Kelderby time, sable_coast_kdy_movements_s26.xlsx with the sub-code letter dropped, grayling_kdy_sectors_s26.csv with its delay field split) for the scheduled departure and the minutes coded aircraft not ready or held for another reason in kdy_delay_code_groups.csv.
4. Read each turn's need under SFG-3 2.4: the time it had (scheduled departure less on-block) plus its not-ready minutes where it held its departure, and no more than the time it had where it was ready in time.
5. Estimated, for each relationship, the share of turns needing longer than each ground time with the product-limit estimator for needs censored in this way; the share among turns that had less than the ground time, each of which shows whether it needed longer, gives the same decisions.
6. Applied SFG-3 3.1 and 3.3 to the filings in kdy_e_gates_ground_time_filings_s27.csv: Norvale Connect flown by Pellmont Aviation, Embraer 175, Tellura Express flown by Pellmont Aviation, Embraer 175 and Tellura Express flown by Sable Coast Air, Dash 8-400 sent back, the shortest acceptable ground time being the first five-minute step at or under 20 per cent.
7. Counted the turns of the week of 12 to 18 July 2027 in kdy_initial_submissions_s27.ssim: each brand's legs on a partner's flight (its DEI 050 record) left to the operating flight, UTC files on Kelderby time, an arrival paired with the same aircraft's next departure on the same operating day by its onward link or its next leg.
8. Recommended sending back the three filings and accepting the other three.

## 4. Deliverable Answers

### kelderby_summer2027_ground_time_review.xlsx

1. Norvale Connect flown by Pellmont Aviation, Embraer 175: filed 35 minutes, sent back, shortest ground time accepted 40 minutes.
2. Norvale Connect flown by Grayling Air, ATR 72-600: filed 40 minutes, accepted, shortest ground time accepted 40 minutes.
3. Norvale Connect flown by Sable Coast Air, Dash 8-400: filed 30 minutes, accepted, shortest ground time accepted 30 minutes.
4. Tellura Express flown by Pellmont Aviation, Embraer 175: filed 40 minutes, sent back, shortest ground time accepted 45 minutes.
5. Tellura Express flown by Sable Coast Air, Dash 8-400: filed 30 minutes, sent back, shortest ground time accepted 35 minutes.
6. Grayling Air, ATR 72-600: filed 35 minutes, accepted, shortest ground time accepted 30 minutes.
7. Line chart on the Need curves sheet of each relationship's share of 2026 peak turns needing longer than each ground time from 20 to 60 minutes, the 20 per cent standard dashed.
8. Turns the summer 2027 initial submissions schedule at Kelderby in the week of 12 to 18 July 2027, and of them shorter than the filed ground time:
   - Norvale Connect flown by Pellmont Aviation, Embraer 175: 213 turns, 42 shorter
   - Norvale Connect flown by Grayling Air, ATR 72-600: 84 turns, 21 shorter
   - Norvale Connect flown by Sable Coast Air, Dash 8-400: 189 turns, 42 shorter
   - Tellura Express flown by Pellmont Aviation, Embraer 175: 105 turns, 28 shorter
   - Tellura Express flown by Sable Coast Air, Dash 8-400: 91 turns, 28 shorter
   - Grayling Air, ATR 72-600: 77 turns, 21 shorter

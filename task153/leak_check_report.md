# leak check, task153

**Verdict: REVIEW.** 20 files read, 23 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: vehicle, visits, asserted, tankful, window, geofence, stretch, islands, telematics, decisive, prompt, overnight, quantity, forecasting, aboard, record, reserve, driver, carries, export, programme, midday, supply, channel, history

## 1 file names (REVIEW 2)
- **REVIEW** `smpm_card_activity_2024-09_2026-08.txt`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data
- **REVIEW** `yard_notes_2026-08.md`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `fms_island_transactions_2025.csv`: golden figure 37,170 appears: ...49,ULSD 32168,KNX-ISL1,2,K1122,4122,08/26/2025,16:37,170.1,694124,ULSD 32169,KNX-ISL1,1,K1106,4106,08/26/2...
- **REVIEW** `overton_offer_2026-08-26.pdf`: carries 12 of 15 distinctive words of the committed call: "Contract 23 of Overton's loads for 14 September to 8 November (Memphis 2, Jackson 5, Nashville 8, Cookeville 1, Knoxvill"

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `card_programmes_pricing_schedules.pdf`: 7 of 25 stump-paragraph terms appear (vehicle, record, carries, export, programme, supply); read whether the document names the move
- **REVIEW** `overton_jackson_tank_programme_2025-03-03.pdf`: 3 of 25 stump-paragraph terms appear (vehicle, carries, supply); read whether the document names the move
- **REVIEW** `yard_notes_2026-08.md`: 3 of 25 stump-paragraph terms appear (vehicle, islands, programme); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: "Put each yard's count, the total and the saving in overton_loads_sep-nov_2026.xlsx, with the diesel gallons each card account's vehicles bought in each of May, June and July and, for each month of last year's Jackson and"

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: question form 'how-many' at 30% of 196 prompts (cap 30%); second-sentence opener 'put' at 39% of 196 prompts (cap 20%); deliverable set 'png+xlsx' at 24% of 196 prompts (cap 20%); reword at the role level, not the verb

## 12 describing content (REVIEW 6)
- **REVIEW** `card_programmes_pricing_schedules.pdf`: names 4 column(s) of the data files verbatim (Diesel, Memphis, ULSD, Vehicle): confirm it is the organisation's own record and not a note written for the analyst
- **REVIEW** `overton_jackson_tank_programme_2025-03-03.pdf`: names 5 column(s) of the data files verbatim (Cookeville, Jackson, Memphis, Product, ULSD): confirm it is the organisation's own record and not a note written for the analyst
- **REVIEW** `overton_knoxville_tank_programme_2025-06-02.pdf`: names 4 column(s) of the data files verbatim (Cookeville, Jackson, Product, ULSD): confirm it is the organisation's own record and not a note written for the analyst
- **REVIEW** `overton_offer_2026-08-26.pdf`: names 5 column(s) of the data files verbatim (Cookeville, Jackson, Memphis, Product, ULSD): confirm it is the organisation's own record and not a note written for the analyst
- **REVIEW** `overton_tank_wagon_prices_2026-08-24.pdf`: names 4 column(s) of the data files verbatim (Cookeville, Jackson, Tank, ULSD): confirm it is the organisation's own record and not a note written for the analyst
- **REVIEW** `yard_notes_2026-08.md`: names 4 column(s) of the data files verbatim (Cookeville, Jackson, Memphis, Yard): confirm it is the organisation's own record and not a note written for the analyst

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)


## Solver's-eye read (11-01 re-check)

One isolated reader (sonnet, medium) on fresh copies of prompt.txt and the repaired target.zip (c2239b2d).

1. Decisive step: none quoted. The prompt names the quantity (the whole loads each island will hand out by 8 November if the vehicles run as in the eight weeks to 23 August), not the method.
2. Ranking file: none. The offer's "Up to 32 in all, for any of the six yards" is a cap.
3. Helper file: none as a dictionary or manifest; the yard notes are a signed internal memo with no column or method.
4. Answer-shaped figure: none.
5. Literal sentence: the prompt's estimand sentence with the offer's load and commitment terms; the reader notes the documents leave open how to estimate the draw from the card, telematics and geofence data (the method open, the WHAT filed).
6. What decides: an analytical choice (each yard's real island draw estimated from card buys, telematics and geofence presence, tanks, vehicle-to-yard attribution, floored to whole loads); the mess reads as source-system noise.

Sweep items: a SMPM batch file harmless (fixed-width H/D/C/T records, no prose); b yard notes harmless (signed memo); c island log harmless (ordinary transactions under the FMS's own headers); d offer harmless (terms only, argues no answer); e card schedules harmless (the programmes' own governing documents, Exhibit A a vendor record-layout spec, Layer 1 only); f programme letters and tank-wagon sheet harmless; g yard notes harmless. Realism: none serious; the yard notes' unit roster by type "a little complete" (minor).

Verdict: no leak.

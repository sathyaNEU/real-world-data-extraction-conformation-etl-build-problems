# leak check, task305

**Verdict: REVIEW.** 20 files read, 37 golden figures and 5 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: census, origin, grocery, households, wrentoft, pitches, guests, rating, measured, output, holiday, golden, asserted, region, estate, demand, readers, running, committee, method, carries, counts, shares, approves, resident

## 2 author vocabulary (REVIEW 1)
- **REVIEW** `spend_share_model_2025.pdf`: \bthe model\b x2: ...persedes the parameters of March 2022). Owner: Joshua Ingram. 1. What the model does The model shares grocery spend among the grocery stores that can...

## 3 answer figures in the pack (REVIEW 16)
- **REVIEW** `property_data_notes.md`: golden figure 107 appears: ...e by store from October 2025 (101 to 106 so far); 107 to 110 still book deliveries in on paper. - `wf...
- **REVIEW** `property_data_notes.md`: golden figure 110 appears: ...e from October 2025 (101 to 106 so far); 107 to 110 still book deliveries in on paper. - `wfm_paid_ho...
- **REVIEW** `property_data_notes.md`: golden figure 101 appears: ...ndhelds went in store by store from October 2025 (101 to 106 so far); 107 to 110 still book deliverie...
- **REVIEW** `property_data_notes.md`: golden figure 106 appears: ...went in store by store from October 2025 (101 to 106 so far); 107 to 110 still book deliveries in on...
- **REVIEW** `voa_list_entries_2026_lq.txt`: golden figure 822 appears: ...-APR-2026**27050**25132456**096G*****01-APR-2026* 822*3510**00470558034*CS*SHOP AND PREMISES*15534137*L...
- **REVIEW** `voa_list_entries_2026_lq.txt`: golden figure 103 appears: ...1-APR-2026**6900**15024161**249G*****01-APR-2026* 103*3510**00036110798*CO*OFFICES AND PREMISES*6735360...
- **REVIEW** `voa_list_entries_2026_lq.txt`: golden figure 764 appears: ...1-APR-2026**8400**24299974**249G*****01-APR-2026* 764*3510**00011499325*CO*OFFICES AND PREMISES*7728252...
- **REVIEW** `voa_list_entries_2026_lq.txt`: golden figure 107 appears: ...2*3510**00343886523*CA*ADVERTISING RIGHT*93953878*107, SCHOOL LANE, WRENTOFT, LQ8 1QX**107*SCHOOL LANE*...
- **REVIEW** `voa_list_entries_2026_lq.txt`: golden figure 105 appears: ...10**00543223294*CP*CAR PARK AND PREMISES*11077966*105, GREEN LANE, WITHYBECK, LQ6 1JG**105*GREEN LANE*W...
- **REVIEW** `voa_list_entries_2026_lq.txt`: golden figure 104 appears: ...1-APR-2026**6500**28647018**203G*****01-APR-2026* 104*3510**00467963099*CS*SHOP AND PREMISES*46814277*L...
- **REVIEW** `voa_list_entries_2026_lq.txt`: golden figure 108 appears: ...510**00087314822*CO*OFFICES AND PREMISES*21777401*108, WESTWAY, LODERWELL, LQ12 1ZX**108*WESTWAY*LODERW...
- **REVIEW** `voa_list_entries_2026_lq.txt`: golden figure 102 appears: ...6*3510**00481720636*CS*SHOP AND PREMISES*93802606*102, FORE STREET, BELLINGTOFT, LQ2 2RT**102*FORE STRE...
- **REVIEW** `voa_list_entries_2026_lq.txt`: golden figure 110 appears: ...1-APR-2026**2700**15735845**249G*****01-APR-2026* 110*3510**00524772763*LH*HOTEL AND PREMISES*72803743*...
- **REVIEW** `voa_list_entries_2026_lq.txt`: golden figure 109 appears: ...01*LS*LAND USED FOR STORAGE AND PREMISES*67672660*109, MOUNT PLEASANT, QUELLBY, LQ5 3LH**109*MOUNT PLEA...
- **REVIEW** `voa_list_entries_2026_lq.txt`: golden figure 101 appears: ...10*3510**00392513499*CS*SHOP AND PREMISES*2563406*101, STATION ROAD, RADDLEFORD, LQ9 2PY**101*STATION R...
- **REVIEW** `voa_list_entries_2026_lq.txt`: golden figure 106 appears: ...1-APR-2026**6200**25266231**096G*****01-APR-2026* 106*3510**00577051335*CO*OFFICES AND PREMISES*3277493...

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `property_data_notes.md`: 10 of 25 stump-paragraph terms appear (census, grocery, households, pitches, rating, measured); read whether the document names the move
- **REVIEW** `spend_share_model_2025.pdf`: 8 of 25 stump-paragraph terms appear (census, grocery, households, rating, output, region); read whether the document names the move

## 6 ranking artifacts (REVIEW 1)
- **REVIEW** `site_shortlist_2027.xlsx`: names 3 of 5 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 7 hidden content (REVIEW 2)
- **REVIEW** `gtfs_sallowmere_motor_services_20261002.zip`: nested_zip: true
- **REVIEW** `gtfs_wrentoft_district_coaches_20261002.zip`: nested_zip: true

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 5 announcements (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Round 4, two isolated readers (sonnet, medium) on target.zip 41415795, each holding only prompt.txt and the bundle; the
brief named neither the stump-vocabulary sweep's terms nor the answer-figure sweep's numbers (leak-check skill).

| Question | Reader G | Reader H |
|---|---|---|
| 1 decisive step stated | none | none |
| 2 file ranking the candidates | none | none |
| 3 file only for the analyst | property_data_notes.md (file descriptions) | property_data_notes.md, the model sheet's parameters |
| 4 figure reading as the answer | none | none |
| 5 sentence fixing the main figure | the model sheet's sections 2 to 4; literal result S1 at 0.496 | the model sheet's share sentence and section 4; literal result S1 at 0.496 |
| 6 what decides | the filed procedure (no analytical choice found) | the filed procedure, with the cannibalisation netting |
| Committed call | S1, 0.5 | S1, 0.5 |
| Ask figures kept | 10 of 26 (ask B) | 0 of 26 |

Both readers stopped at the resident route the model sheet files, which is the default path; neither read the
out-of-region card spend as guests. Question 6 answered "procedure" by readers who missed the decisive step is the
mirror's view of an analytical stump, not a rule-application finding (the judge's Gate H: decisive step analytical).

Rulings on the REVIEW lines:
- Author vocabulary, "the model" in the model sheet: harmless, the document's own title and subject (both readers).
- Answer figures: store numbers 101 to 110 in the notes, and house and list entry numbers in the rating list that
  coincide with ask figures: harmless, identifiers and addresses (ruled here; the numbers were not given to readers).
- Design-note vocabulary in the notes and the model sheet: harmless; the notes describe files and the model sheet
  states the residents-only method, and neither mentions guests, parks or the missing origin (ruled here).
- The shortlist names the sites beside their costs: harmless, it carries no ranking or score (both readers).
- The two GTFS zips: harmless, the operators' standard feeds (both readers).

Realism notes taken into the generator after round 4: the competitor entry at Brook Street with a September 2026
alteration (the grocery stores and parks now carry none), stops beside the sites named after nearby villages (now the
site's town), the count points' method columns disagreeing, cover at a neighbouring store spread over most
colleagues, and shift lengths from four fixed values.

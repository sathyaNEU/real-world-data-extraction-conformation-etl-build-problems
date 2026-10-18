# leak check, task470

**Verdict: REVIEW.** 18 files read, 7 golden figures and 30 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: counted, never-recorded, network, unrecorded, recorded, airplanes, register, airplane, method, decisive, operation, capture, n-number, silent, counts, quantity, activity, readable, towers, export, sentence, training, golden, closed, receiver

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `cvaqd_2027_unleaded_avgas_transition_grants.pdf`: golden figure 12.5 appears: ...mates it under method CVAQD-AQ-17, Revision 3, is 12.5 kg or more. 2.3 The round funds every qualifying...

## 4 design-note vocabulary (REVIEW 5)
- **REVIEW** `F37_2026_operations_count_report.pdf`: 6 of 25 stump-paragraph terms appear (counted, recorded, airplanes, airplane, operation, counts); read whether the document names the move
- **REVIEW** `G42_2026_activity_count.pdf`: 5 of 25 stump-paragraph terms appear (airplanes, airplane, method, operation, activity); read whether the document names the move
- **REVIEW** `cvaqd_adsb_receiver_network_notes.pdf`: 7 of 25 stump-paragraph terms appear (network, recorded, register, n-number, towers, export); read whether the document names the move
- **REVIEW** `cvaqd_aircraft_lead_inventory_method_rev3.pdf`: 8 of 25 stump-paragraph terms appear (network, recorded, register, method, operation, counts); read whether the document names the move
- **REVIEW** `cvaqd_faa_register_extract_notes.pdf`: 6 of 25 stump-paragraph terms appear (network, recorded, register, n-number, export, receiver); read whether the document names the move

## 6 ranking artifacts (REVIEW 4)
- **REVIEW** `airport_master_records_5010.xlsx`: names 30 of 30 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `cvaqd_aircraft_lead_inventory_method_rev3.pdf`: names 3 of 30 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `state_airport_directory_2026.xlsx`: names 30 of 30 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `state_based_aircraft_validation_2027.xlsx`: names 30 of 30 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Verdicts on the REVIEW lines (main thread): the guidelines' 12.5 kg is the round's threshold, harmless; the method, network and register notes and the two count reports use the inventory's own words and name no estimator, harmless; the 5010 records (declared wrong-basis distractor), the directory and the based list name the fields beside counts and identifiers and rank nothing on the call, harmless.

### Round 1 (isolated reader, sonnet, medium; the pack before the fix pass)

# Answers (leak read, task 470, r1)

## Part A

### A1. Main answer
Under my committed reading, 4 of the 24 non-towered fields qualify (2026 lead >= 12.5 kg): L08 Lanthorne Field 16 kg, F37 Fennick Airpark 14 kg, A71 Ambrell County Airport 21 kg, T13 Thornacre Regional 22 kg.

Confidence: the 4 counted fields and the 6 towered fields are exact. The 20 uncounted fields rest on an estimate the pack does not fully determine (see A3 and Part D). Five fields sit near the line and flip with the method: K58, P05, S27, T61 and N26.

2026 lead, whole kg, all 24 non-towered fields (kg unrounded in brackets):

| ID | Field | Basis | kg |
|---|---|---|---|
| A71 | Ambrell County | estimate (based list) | 21 (21.18) QUALIFIES |
| B48 | Brannoch Airstrip | estimate (median share) | 3 |
| C66 | Cobbett | estimate (based list) | 8 |
| D19 | Dunmarsh | count | 9 (9.04) |
| D73 | Dellow Strip | estimate | 2 |
| F37 | Fennick Airpark | count | 14 (14.10) QUALIFIES |
| G42 | Graylow Municipal | count | 10 (10.17) |
| H52 | Hollin Gap | estimate | 9 |
| K58 | Kestrel Ridge | estimate (based list) | 11 (11.15) |
| L08 | Lanthorne | count | 16 (16.09) QUALIFIES |
| L29 | Lissom | estimate | 6 |
| M09 | Marsh Hollow | estimate | 4 |
| N26 | Norwick | estimate | 11 (10.57; 13.5 under a 0.43 ratio) |
| O16 | Orrin Flats | estimate | 8 |
| P05 | Pellow Municipal | estimate (school field) | 11 (11.2) |
| R31 | Ravelle | estimate | 4 |
| S27 | Saltry | estimate (school field) | 11 (11.3) |
| T13 | Thornacre Regional | estimate | 22 (21.65) QUALIFIES |
| T61 | Tavish Aero Field | estimate (based list) | 11 (11.00) |
| U44 | Umber Creek | estimate | 9 |
| W33 | Wickrow | estimate | 9 |
| W85 | Wenmore | estimate (based list) | 8 |
| Y02 | Yarrow Bend | estimate | 4 |
| Z14 | Zellner | estimate | 6 |

Recorded-only lead (network-recorded piston operations, before any unrecorded add-on): A71 17.92, T13 18.42, L08 15.86, F37 10.66, K58 10.85, P05 11.00, S27 11.08, T61 10.78, N26 8.95. A71, T13 and L08 clear the line on recorded operations alone. F37 clears it only after the commissioned count is applied.

### A2. Six towered fields (2026 piston operations to nearest 100, lead in kg)
Operations = recorded piston operations + unrecorded, per method 4.2.

| ID | Field | Recorded piston ops | Unrecorded | Ops (nearest 100) | Lead kg |
|---|---|---|---|---|---|
| HWK | Halwick Municipal | 13,659 | 3,290 | 16,900 | 20 (20.17) |
| CRV | Corrisan Valley Regional | 5,346 | 2,544 | 7,900 | 12 (11.98) |
| OSY | Ostrey Field | 15,792 | 2,988 | 18,800 | 21 (21.34) |
| VNL | Varnell County | 8,739 | 2,768 | 11,500 | 14 (14.01) |
| KTY | Kesterly Field | 10,392 | 2,512 | 12,900 | 15 (14.88) |
| DMR | Dunmore Municipal | 4,930 | 2,368 | 7,300 | 11 (11.12) |

The unrecorded figure is tower civil operations less all network-recorded civil operations inside tower hours (any engine class). It is billed at 1.625 g each. It therefore contains some turbine and rotor operations (see Part D).

### A3. Path
1. Read the guidelines PDF. Eligibility is a non-towered public-use field with 2026 lead >= 12.5 kg under CVAQD-AQ-17 Rev 3. All 30 fields are public-use in the directory. 6 have an ATCT, which leaves 24.
2. Read the method PDF. An operation is a takeoff or a landing, and a touch-and-go is 2. The inventory year is the local calendar year. Lead per operation comes from Table 1 by engine count. Unrecorded operations get 1.625 g. Section 4 sets how the unrecorded operations are found: tower count minus recorded (4.2), commissioned count minus recorded (4.3), and "estimated from the fields with a count" at every other field (4.4).
3. ADS-B export (187,403 events). I converted event_time_utc to America/Los_Angeles, using the stated UTC-8 / UTC-7 rule and the 8 Mar 02:00 / 1 Nov 02:00 changeovers. This drops 469 events that fall in 2025 local and 440 that fall in 2027 local. 186,494 events remain in 2026.
4. Registry. I joined icao24 to MASTER (MODE S CODE HEX, lower-cased). 3,203 of the 3,228 addresses match. The other 25 are only in DEREG (cancelled during 2026, after their last event), so I took their aircraft and engine codes from DEREG. 198 addresses are in both files. DEREG holds an old cancellation of the same N-number and address, and MASTER holds the current re-registration to a different aircraft, so I used MASTER. Piston means ACFTREF TYPE-ENG = 1 (reciprocating). Engine count comes from ACFTREF NO-ENG (309 reciprocating multi-engine). Turboprop, turboshaft and turbofan types are excluded, and so are gliders (B1). A touch-and-go event = 2 operations, with Table 1's touch-and-go factor per operation.
5. Recorded piston lead per field: from 0.82 g per operation (S27) up to 1.48 g per operation (W85).
6. Towered fields. I took the daily tower counts and summed civil operations (itinerant air carrier + air taxi + GA + local civil, excluding military) per day. I took recorded events in tower hours, on the local clock, using the directory's hours: VNL 0700-2100, 0700-1900 for Nov-Feb; DMR 0700-2000, 0700-1800 for Nov-Feb; closed 25 Dec and 1 Jan. The difference is never negative on any day at any of the six, which confirms the hour and timezone handling. Unrecorded totals: HWK 3,290, CRV 2,544, OSY 2,988, VNL 2,768, KTY 2,512, DMR 2,368.
7. Counted fields. The count's piston operations less recorded piston operations:
   - F37: 10,504 - 8,384 = 2,120.
   - G42: 7,149 - 5,221 = 1,928.
   - D19: the daily piston column sums to 6,138, so 6,138 - 3,426 = 2,712.
   - L08: takeoffs + landings + 2 x circuits = 17,684, so 17,684 - 17,538 = 146. The tow plane is already in the piston counts.
   The unrecorded share of all operations is F37 20%, G42 27%, D19 44% and L08 0.8%. Pooling the four gives a ratio of 0.20 on recorded. Pooling the three non-school fields gives 0.40.
8. The 20 fields without a count (method 4.4: "estimates them from the fields with a count"). The 4 counts alone do not say how. I tested whether the unrecorded share is driven by the unequipped part of the based fleet.
   - state_based_aircraft_validation lists based aircraft for 8 public fields (CRV, KTY, F37, A71, C66, K58, T61, W85). I mapped N-numbers to addresses and checked which were ever seen in ADS-B. Unequipped share of based piston aircraft: F37 20% (30/149), CRV 21%, KTY 23%, A71 12%, C66 12.5%, W85 12%, K58 2.2%, T61 1.1%.
   - It matches the measured unrecorded share closely: F37 19.5% against 20.2% measured from the count. CRV and KTY tower unrecorded shares are 18% and 22% of civil operations.
   - Unrecorded operations per unequipped based aircraft are about 65-72 at F37, CRV and KTY. That is a stable rate.
   - So for the 5 list fields (A71, C66, K58, T61, W85) I set unrecorded = recorded x u/(1-u), with u the unequipped share.
   - For P05 and S27, both flight-school fields like L08 and T61, I used about a 1% ratio.
   - For the 13 others I used a median share of 0.14 of recorded, from the fields with a measured share.
   I rejected the plain pooled ratio from the four counts (0.20, or 0.40 on non-school fields) applied to every field. It would put K58, P05, S27 and T61 above 13.5 kg (and N26 at 13.5 under the 0.40 ratio). It ignores that the field's own unequipped fleet drives the gap. I also rejected the stale 5010 based counts: they are scrambled (see Part C) and predict D19 badly (1 - 60/72 = 17% against the measured 44%).
9. Lead = (recorded grams + unrecorded x 1.625 g) / 1000, rounded to whole kg.

## Part B

1. The decisive step is that operations the network never recorded must be added, and the added amount at the uncounted fields must be estimated. The method's Section 4 spells it out. Sentences quoted from the method: "2.2 A field's operations in the inventory year are every operation by a piston-engine aircraft at the field in that year, based or visiting, whether or not the District's receiver network recorded it." and "4.4 At every other field, the inventory estimates them from the fields with a count." The receiver notes add: "An aircraft without ADS-B Out, or with it switched off, is not recorded." Nothing says how to extrapolate. The estimate is left to the analyst.
2. No file ranks or scores the 24 fields on the question. Closest: the 5010 sheet and the directory list operations and facilities, and the lead-monitoring CSV is two monitors. None gives a lead score.
3. The files that exist only to help: the three notes PDFs (receiver network notes, FAA register extract notes, method rev 3), the code tables in the register notes, the ACFTREF/ENGINE reference files, and the directory "ATCT Hours (local)" column, which is needed for method 4.2.
4. No figure reads as the answer. The threshold, "12.5 kg or more", is the only number that decides eligibility. Recorded-only lead (for example T13 18.4, A71 17.9) is a trap that reads as an answer: leaving out the unrecorded add-on gives a plausible but wrong list.
5. Literal sentences with computable results:
   - "4.3 ... they are the count's piston-engine operations less those the network recorded." Result: F37 2,120, G42 1,928, D19 2,712, L08 146.
   - "4.2 ... the tower's count of civil operations in the tower's hours of operation less the civil operations the network recorded at the field in those hours." Results above.
   - "3.2 An operation the network did not record is assigned 1.625 g." The literal sentence for the 20 uncounted fields is 4.4, and it does not fix a figure.
6. A mix, and the weight is on the analytical choice. The figures for the 4 counted and 6 towered fields come from following stated rules (4.2, 4.3, Table 1) and reading the register correctly (hex join, deregistered aircraft, engine count, local year). What changes the set of qualifiers is the estimate at the uncounted fields. Quoted sentence: "4.4 At every other field, the inventory estimates them from the fields with a count." The share of the based fleet that is unequipped, found through the state based-aircraft list, is the key idea, and it is not stated anywhere. A flat ratio of unrecorded to recorded operations gives a different answer.

## Part C: realism

- airport_master_records_5010.xlsx: the date pairs look scrambled and contradict each other. HWK reports 12-month operations ending 2018-12-31 with based aircraft as of 2024-08. CRV reports operations ending 2024-12 with based as of 2016-11. S27 and others are similar. Based counts are far from the state list (F37: 178 piston against 149 listed). It reads as a deliberately stale distractor. The sheet name "5010 data" is also plain. Real 5010 records have one date per section, one inspection date and ops/based counts that are not round hundreds.
- 5010 operations figures are all round to 100 or 10 (840, 12,900) and not real-looking, and the Notes sheet says "Copied from the state's airport inspection files, 30 September 2026". The file modification time is 30 Sep, unlike the 2027 times on the others.
- D19_2026_daily_counts.xlsx: nearly all daily piston values are even, as if by pairs (2, 18, 12, 10, 14), with a few odd days (7, 11). Rarely a real count. No touch-and-go split.
- L08_2026_operations_count.xlsx: takeoffs and landings are almost equal each month, differing by only 0-2, and the Total row is =SUM formulas. The F37 PDF monthly table also looks too round (many numbers end in 0, 2, 4).
- adsb_field_events: 100% of events from 2025-12-30 to 2027-01-03 across 30 sites with no outages and no sub-second times. Real ADS-B exports have gaps and dropouts; the data has 87 zero-event days at B48 and 128 at D73 only because those fields are small. 100% commissioning recovery claimed in the notes. event_id strictly increases with time, which no real multi-receiver database would do. flight_id: 8,331 blanks, and addresses that broadcast a stale ID (a20602 broadcasts N409NW, an N-number cancelled in DEREG under a different address).
- Very few night-time events: hours 0-4 hold about 740 events in the year, but 8,602 between 8:00 and 9:00; the profile is smooth with no sharp daylight-saving shift.
- MASTER.txt: 4,562 rows, all STATUS V and all expiration dates 2026-01-01 or later, which a real register extract would not give. The 198 addresses in both MASTER and DEREG with the same N-number but a different aircraft are plausible but unusual. In ADS-B events from the "ACFTREF" the types are uniform. Owner fields are removed, as the notes say. Columns padded with trailing commas match the real FAA format.
- DEREG.txt: 223 rows, EXP-COUNTRY mostly blank. Cancellation dates for 25 aircraft that flew in 2026 are all after their last event, which is too neat.
- state_based_aircraft_validation_2027.xlsx: validation dates all fall between 2026-09-01 and 2026-12-28 and the sheet only covers 8 public fields plus two private strips (2C9, 7K5) that are not among the 30 fields. It looks cut for the task. A state list that covers only 8 fields is odd.
- state_airport_directory: 36 rows, with 6 private strips (6V2, 9H1, 3O8, 7K5, 2C9, 8W4) with no runways. Elevations, county names and the scheme "Corrisan Valley / Halwick / Ostrey / Varnell" are fictional. The register notes say "four counties", the directory has four, matching.
- Directory hours: two towers have a Nov-Feb hours rule and closure on Dec 25 and Jan 1 hidden in a text cell, which reads as a placed rule.
- atct_daily_operations_2026.csv: "Itinerant Air Carrier" is 0 for every field and every day, (military columns are small but non-zero). Format matches FAA OPSNET/TFMSC column names though.
- cvaqd_lead_monitoring_2026.csv: two sites, a monitor near HWK and one near CRV, both towered fields, so it cannot bear on the 24 fields. It is a distractor. Method_code 192 is a real Pb-TSP code. Fixed 6-day cadence.
- cvaqd_2027_unleaded_avgas_transition_grants.pdf: the threshold of exactly 12.5 kg and "kg or more" is a clean synthetic number, and the guidelines "issued 4 December 2026" cite a method adopted 18 March 2026 and a 2026 inventory not yet complete.
- Placed for the task: the F37/G42/L08/D19 count reports (four count styles, each in a different format and with different class names); the L08 note that tow planes' takeoffs are piston operations; the glider columns; "Gliders do not use the field" in G42; the receiver notes sentence "An aircraft without ADS-B Out ... is not recorded."
- Reports: the files are named by field id (F37, G42, L08, D19), which is realistic. The 5010 sheet's glider column for L08 is 2 while the count shows about 100 glider launches; consistent only with a stale record.

## Part D: ambiguities

1. Estimate at the 20 uncounted fields (method 4.4). Readings and results:
   - (a) Ratio of unrecorded to recorded pooled over the 4 counts (0.200): K58 13.6, P05 14.9, S27 15.5, T61 14.7 qualify; N26 11.3 does not. Qualifiers = L08, F37, A71, T13 + K58, P05, S27, T61 (8).
   - (b) Same pooled over the three non-school counts (0.397): the above plus N26 13.5 (9 qualifiers); H52 11.9 and others stay below.
   - (c) Based-fleet method (mine): 4 qualifiers (L08, F37, A71, T13). K58 11.15 and T61 11.00 stay below.
   - (d) Recorded-only, no add-on: qualifiers = L08, A71, T13 (3); F37 10.66 drops out.
2. Unrecorded operations at towered fields: the formula subtracts all recorded civil operations, but assigns every unrecorded operation 1.625 g even if it was a jet or helicopter. The alternative is to bill only piston operations. This moves lead by under 1 kg and CRV (11.98) stays below 12.5 either way. It changes the operations figure for the six towered fields by hundreds.
3. "Operations" for the memo's six towered fields: "piston-engine operations" could be recorded piston only (HWK 13,700) or recorded + unrecorded (16,900). I used the second.
4. Rounding: lead rounded to whole kg only at the end. CRV 11.98 rounds to 12, which is under the 12.5 line anyway. The qualification test uses unrounded kg.
5. D19: the daily workbook gives piston-engine airplanes 6,138; the column Total is 6,260 (includes turbine and helicopters). Using Total would be wrong.
6. Local year versus UTC year (469 events in 2025 local, 440 in 2027 local). Using UTC dates would shift the year edges (not computed; 909 events sit in the two edge years under local time).
7. Registry join: 198 addresses in both MASTER and DEREG. Using DEREG for those gives a different aircraft and engine for about 12,997 events and changes lead for several fields (size not computed).
8. The "24 fields" assumes all 30 are public-use: yes in the directory. The six private strips are not in scope.
9. Touch-and-go: one event = 2 operations, with the touch-and-go factor per operation (0.55/1.35 g each). Counting one event as one operation would lower recorded lead sharply and change the qualifiers (size not computed).


Main thread on round 1: stumped (four fields on a never-recorded-share route read from the first county sheet only); all twelve towered figures missed through today's register; question 6 analytical. Fixed in the generator: MASTER statuses and expiries, irregular event ids, more multi-day trips, method 4.2's pin on the towers' unrecorded operations, W33 cleared under the reader's route. No graded figure moved except W33's lead (14 kg either way).

### Round 2 (isolated reader, sonnet, medium; the fix-pass pack, before the ask's device was rebuilt)

Main-thread rulings: no leak (question 1 quotes method 2.2 and 4.4 and the network notes' statement that aircraft
without ADS-B Out are not recorded, which the determinism rule requires the network notes to carry; question 2 none;
question 3 the register and network notes are each system's own documentation; question 6 an analytical choice). The
reader landed the call and every towered figure by reading the moved addresses' DEREG rows by their cancel dates, so the
ask's device of the time was a mirror device: rebuilt in the generator (the Registry's move precedes each swap; the
honest cracker now misses all twelve). Its realism notes were fixed in the same pass (the register's model and engine
catalogue, the based list's make and model, a lapsed airplane's validation date, call signs, S27's fuel, the network
notes' commissioning counts, the guidelines' fuller text); the towers' full daily grid, one emitter category per
address, D19's daily spread and G42's even turbine months are the systems' own, harmless.

#### Answers (round 2)

## Part A

### A1. Main answer
**7 of the 24 fields qualify (2026 lead of 12.5 kg or more):**
Fennick Airpark (F37) 14 kg; Lanthorne Field (L08) 16 kg; Umber Creek Airport (U44) 15 kg; Orrin Flats Airport (O16) 14 kg; Wickrow Airfield (W33) 14 kg; Ambrell County Airport (A71) 21 kg; Thornacre Regional (T13) 22 kg.

2026 lead, whole kg, all 24 fields (unrounded kg in brackets):
F37 14 (14.10), L08 16 (16.10), G42 Graylow Municipal 10 (10.17), D19 Dunmarsh Airport 9 (9.04), T61 Tavish Aero Field 11 (10.89), P05 Pellow Municipal 11 (11.11), S27 Saltry Field 11 (11.08), U44 15 (14.79), O16 14 (14.09), W33 14 (14.13), Y02 Yarrow Bend Strip 6 (6.13), A71 21 (20.83), N26 Norwick Field 10 (9.96), T13 22 (22.12), K58 Kestrel Ridge Airpark 11 (11.07), Z14 Zellner Field 6 (5.81), H52 Hollin Gap Airport 9 (9.10), M09 Marsh Hollow Field 4 (4.19), C66 Cobbett Airport 8 (8.16), B48 Brannoch Airstrip 3 (3.12), D73 Dellow Strip 2 (1.83), R31 Ravelle Field 4 (3.85), W85 Wenmore Airport 9 (8.97), L29 Lissom Field 6 (5.78).

### A2. Six towered fields (piston ops nearest 100 / lead kg)
| Field | recorded piston ops | unrecorded (tower civil less network in tower hours) | piston ops | ops (nearest 100) | lead kg |
|---|---|---|---|---|---|
| HWK Halwick Municipal | 14,336 | 3,290 | 17,626 | 17,600 | 22 (22.12) |
| CRV Corrisan Valley Regional | 7,378 | 2,544 | 9,922 | 9,900 | 18 (17.95) |
| OSY Ostrey Field | 16,427 | 2,988 | 19,415 | 19,400 | 23 (23.19) |
| KTY Kesterly Field | 11,104 | 2,512 | 13,616 | 13,600 | 16 (16.04) |
| VNL Varnell County Airport | 9,424 | 2,768 | 12,192 | 12,200 | 16 (16.04) |
| DMR Dunmore Municipal | 5,559 | 2,368 | 7,927 | 7,900 | 13 (12.92) |

Towered total is about 80,700 piston operations.

### A3. Path
1. Read the grant guidelines (12.5 kg, method CVAQD-AQ-17 Rev 3, no tower, public use), the method (Table 1 factors; touch-and-go is 2 ops; unrecorded ops get 1.625 g; sections 4.2 to 4.4), the receiver notes (UTC; UTC-8 and UTC-7 from 8 Mar to 1 Nov) and the register notes. The state directory gives 24 public fields with ATCT = N and 6 with ATCT = Y (HWK, CRV, OSY, VNL, KTY, DMR) plus 6 private strips.
2. ADS-B export: 187,609 events. I converted to Pacific local time and kept calendar 2026 (186,717 events; the export also covers 30 Dec 2025 to 2 Jan 2027, so the edges are dropped). The UTC year or the full export moves any field by 0.1 kg at most and flips nothing.
3. Join icao24 to MASTER MODE S CODE HEX (case-insensitive, trimmed fixed-width padding). Engine type comes from ENGINE.txt through MASTER's ENG MFR MDL; engine count from ACFTREF NO-ENG. Piston means engine TYPE 1 (reciprocating); gliders, turboprops, turboshafts and fans are excluded. 25 addresses are only in DEREG.txt (cancelled in 2026), so I used their DEREG aircraft and engine codes.
4. Registration reuse. Eight addresses (N276SR, N3002F, N469HQ, N5172C, N51BY, N8144N, N9024A, N9305H; 570 to 900 events each) have a DEREG row cancelled in 2026 for a piston twin or single and a new MASTER row issued the same day for a turbine aircraft (PC-12, B200, Citation). I attributed events up to and including the cancel date (local) to the old piston aircraft and later events to the new turbine one. This only touches towered fields: using MASTER only drops HWK to 20.17 kg, CRV to 11.98, OSY to 21.34, KTY to 14.88, VNL to 14.01 and DMR to 11.12. None of the 24 fields moves (T13 by 2 ops).
5. Lead for recorded ops: takeoff, landing and 2 x the per-op touch-and-go factor, single or multi by NO-ENG (Table 1).
6. Unrecorded ops at the 4 counted fields (section 4.3), count piston ops less recorded piston ops:
   - F37: 10,504 (report) less 8,384 = 2,120.
   - G42: 7,150 less 5,222 = 1,928.
   - D19: daily sheet piston sum 6,138 less 3,426 = 2,712.
   - L08: takeoffs + landings + 2 x circuits = 17,685 (the sheet total is formulas) less 17,539 = 146.
7. Unrecorded ops at the 6 towered fields (section 4.2): tower civil ops (air carrier + air taxi + GA itinerant + local civil, military excluded) less all network ops (touch-and-go as 2) inside tower hours on open days. Hours: HWK 0700-2100, CRV 0600-2200, OSY 0700-2100, KTY 0700-2000, VNL 0700-2100 (Nov to Feb 0700-1900, closed 25 Dec and 1 Jan), DMR 0700-2000 (Nov to Feb 0700-1800, closed 25 Dec and 1 Jan). No day had more network than tower ops. Result: HWK 3,290, CRV 2,544, OSY 2,988, KTY 2,512, VNL 2,768, DMR 2,368, all valued at 1.625 g.
8. The 20 other fields (section 4.4: "estimates them from the fields with a count"). The method does not say how.
   - Alternatives I weighed: (a) a flat share of unrecorded to recorded piston ops (mean 0.31, pooled 0.237 over the 10 count fields); (b) ADS-B-silent based aircraft. For each field I took the based aircraft on the state validation list (N-numbers cleaned: case, spaces, missing N), matched them to the register and counted those whose address never appears in the export (zero events; a clean gap, since only 9 aircraft have 1 to 4 events). Two based aircraft (6574V at F37, 625EY at G42) are only in DEREG and do appear in the export, so they are not silent.
   - Across the 10 fields with a count, unrecorded ops per silent based aircraft are tight: CRV 65, F37 71, KTY 72, DMR 66, HWK 72, G42 67, OSY 71, D19 71, VNL 68, with L08 an outlier at 49 (3 silent aircraft). Unrecorded share of ops, by contrast, runs from 1 percent to 44 percent and is not stable. I chose (b): through-origin pooled slope 68.96 ops per silent based aircraft (69.14 without L08; the mean of ratios is 67.0; a regression with intercept gives 71.5/aircraft less 85). Estimated unrecorded ops = slope x silent based aircraft, then x 1.625 g, added to the recorded lead.
   - Why: the shares method sends the field with many silent aircraft (U44, O16, W33) below 12.5 and sends T61, P05, S27, K58 up above it, which is the opposite of what the based-aircraft evidence says. Rank is sensitive to this choice only through U44, O16, W33 (14.1 to 14.8 under (b), 9.2 to 10.7 under shares) and T61, P05, S27, K58 (about 11 under (b), 14 to 18 under shares).
9. Totals: recorded-only gives only L08, A71 and T13 (3 fields); the silent-aircraft estimate gives 7. Shares estimate gives 8 or 9 (different set). Method variants for the slope (all 10, ex-L08, mean of ratios, intercept) all give the same 7.

## Part B

1. The decisive step is not announced. The nearest sentences are method 2.2, "A field's operations in the inventory year are every operation by a piston-engine aircraft at the field in that year, based or visiting, whether or not the District's receiver network recorded it", and 4.4, "At every other field, the inventory estimates them from the fields with a count." The guidelines (2.2) say the 12.5 kg is the lead "as the District's aircraft lead inventory estimates it under method CVAQD-AQ-17, Revision 3". Nothing tells the solver what to estimate from. The receiver notes say "An aircraft without ADS-B Out, or with it switched off, is not recorded", which, with the based-aircraft list, is the hint.
2. No file ranks the 24 fields. The 5010 workbook (Ops: GA Local and GA Itinerant, as last filed, with out-of-date as-of dates) and the lead monitoring file (two towered sites only) are the nearest, and a solver using 5010 ops would get the wrong answer. Revision history row 1 ("operations from the airports' 5010 records") flags 5010 as the old method.
3. Files existing only to help: cvaqd_faa_register_extract_notes.pdf and cvaqd_adsb_receiver_network_notes.pdf (code tables, time zone); the Notes sheets of the L08/D19 workbooks. state_based_aircraft_validation_2027.xlsx is the key input for the estimate, not only a helper. Not used by the solution: airport_master_records_5010.xlsx, cvaqd_lead_monitoring_2026.csv, state_airport_directory columns other than ATCT (decoys).
4. Reads as the answer: "12.5 kg or more" (threshold, guidelines 2.2) and "$214,000"; the count totals "10,944 operations... 10,504 of them by piston-engine airplanes" are context. No candidate name stands out. The L08 sheet (very high touch-and-go circuits, flight school) hints that L08 is a big field, but nothing names a winner.
5. Literal sentences: method 4.3, "they are the count's piston-engine operations less those the network recorded" (F37 2,120; G42 1,928; D19 2,712; L08 146); 4.2, "the tower's count of civil operations in the tower's hours of operation less the civil operations the network recorded at the field in those hours; the inventory takes them as operations by piston-engine aircraft" (HWK 3,290 ... DMR 2,368). 4.4 read literally ("estimates them from the fields with a count") does not fix a figure, so the main figure for 20 fields is not fixed by any filed sentence: the population (based aircraft not on ADS-B) is not stated.
6. An analytical choice: how to estimate the operations the receivers missed at uncounted fields (what drives the missing ops). No single sentence decides it; 4.4 is the only pointer and the receiver notes sentence "An aircraft without ADS-B Out ... is not recorded" and the based list are the evidence. Data semantics (registration reuse by the 8 addresses) matters for towered figures only.

## Part C. Realism
- Register: every airframe model has exactly one engine model in MASTER (ACFTREF 38 rows, ENGINE 20 rows); 4,562 aircraft share 38 models, and the same mix of models appears at every field, including strips (e.g. Cirrus SR20/SR22, Mooney M20J, PA-32R-301 and an RV-7A at a grass strip). A real extract would show hundreds of models and many engine variants. Year of manufacture for a model spans a plausible range, but the PC-12/47E code carries 2008 and 2019 builds for the same registrations in DEREG vs MASTER.
- 142 of the 3,228 addresses seen have both a MASTER and a DEREG row; many DEREG rows are for the same N-number as a completely different aircraft (e.g. 1019V: PC-12 in DEREG, PA-28-181 in MASTER; 1255G; 2042T PA-28 vs PC-12). Eight in 2026 convert piston twins/singles to turbines on the same N-number and cancel date equal to the new CERT ISSUE DATE (276SR, 3002F, 469HQ, 5172C, 51BY, 8144N, 9024A, 9305H), and each flies 570 to 900 events in the year. A single-engine to turboprop change on one tail number does not happen in the real registry. They read as placed.
- 25 addresses are only in DEREG with 2026 cancel dates, and their events stop exactly before the cancel date (e.g. a16e6b last event 3 Jul, cancel 22 Jul); two of them (6574V, 625EY) are on the 2027 based list, with validation dates (15 Dec 2026, 8 Oct 2026) after or before cancel (17 Nov 2026, 27 Dec 2026), so validation "against the FAA register" of an aircraft cancelled 27 Dec is inconsistent.
- ADS-B: every address has exactly one emitter category; B200 (CLASS 2 in ACFTREF) and PC-12 broadcast A1, 7-passenger Bell 407 A7 (fine). Flight_id is the N-number for every row where non-blank (real avionics often carry callsigns), blank 4.2 percent. Events at night are thin but present; no event gaps; event_ids ascending with gaps (missing ids are the military exclusion or random). The 12-hour tower-hours pattern in network events looks smooth.
- The receiver notes say a four-week comparison found every ADS-B-equipped op recorded, a clean claim not found in real validation reports; "30 public-use airfields" and "six control towers" match the directory.
- State list: N-number formatting (lower case, leading N missing, trailing/leading spaces) is plausible mess; but Make/Model casing flips between rows ("CESSNA 172S" and "Cessna 172S") and 3,774 aircraft are all "validated" 1 Sep to 31 Dec 2026, for "1 January 2027" status, 11 of 36 sheets per county. The Make/Model strings are identical to ACFTREF's (no "Cessna 172 Skyhawk"). 'Aircraft Type' includes glider (2) but 5 other categories match the register.
- Based aircraft counts: the 5010 (e.g. HWK single 170, multi 15) is wildly different from the 2027 validation (HWK 243); 5010 "Ops" are round tens/hundreds (fine), but "Based aircraft as of" dates run 2016 to 2024 while "Operations for 12 months ending" runs 2018 to 2025 and are mismatched in the same row (CRV ops 2024, based 2016). Looks purposely stale. 5010 workbook says "Copied ... 30 September 2026" (file date 30 Sep) while the others have 2027 dates; fine.
- Directory: S27 Saltry Field has Fuel "None" and private ownership, yet has the third-highest ADS-B traffic (13,585 ops) and 5010 shows 100LL-like piston base; B48, D73, R31 are privately owned public-use with Fuel None. ADS-B ops at fuel-less fields are fine. The directory has a "Flight Training" column that, with L08 Y, hints at L08's circuits.
- Count reports: F37 PDF and G42 PDF are very clean one-page tables with round totals; F37 has a piston/turbine/helicopter/glider split that sums exactly (all totals tie). L08 workbook total row is formulas with no cached values. D19 daily sheet has days of 0 and 29 to 30 ops alongside 1 to 2 (very spiky: Jan 31 = 30, Jan 6 = 1), looks synthetic. The F37 report says "a takeoff or a landing is one operation and a touch-and-go two", all counts round to even numbers in turbine/helicopter columns (20, 16, 36...), which suggests generated rounding.
- ATCT file: 6 x 365 rows exactly, no missing/duplicate/zero days, internal totals tie, no revisions or blank days, including 25 Dec and 1 Jan zero rows at VNL/DMR (consistent with closure); a real FAA OPSNET export has Air Carrier/Taxi/GA/Military columns and tower-hour caveats; here the dates are mm/dd/yyyy text.
- Lead monitoring: only two sites (CV-0412 at HWK Runway 31 end, CV-0418 at CRV North), both at towered fields, each every 6 days for 61 samples, method 192; the AN qualifier on 6 rows with blank values. Nothing for the 24 fields, so it reads as a distractor.
- Method document: lead-per-operation table has round numbers, "1.625 g, the mean of a single-engine takeoff and landing" (exactly (2.30+0.95)/2) is neat; the grant text is unusually brief for a district program (no application criteria, no match).

## Part D. Ambiguities
- Estimation at uncounted fields (4.4): see A3 step 8. Silent-aircraft slope: 7 qualify (F37, L08, U44, O16, W33, A71, T13). Share of recorded (mean 0.312): 9 (F37, L08, T61, P05, S27, A71, N26, T13, K58). Pooled share 0.237: 8 (F37, L08, T61, P05, S27, A71, T13, K58). Recorded-only (no estimate): 3 (L08, A71, T13). Recorded-only is also how a solver reads 2.2 if 4.4 is ignored.
- Definition of "never recorded" based aircraft: any event at any field (my reading) vs events at this field. At a field, an aircraft based there but only seen elsewhere would count as silent under the second reading; the second gives different silent counts and slopes (not computed beyond noting that 2C9 style fields would be all silent).
- Touch-and-go: method 2.1 says 2 ops, Table 1 gives the factor "each operation of a touch-and-go". Read as one event at 0.55/1.35 g once, lead falls about 10 to 20 percent: L08 recorded 12.30 kg (12.5 for the two-op reading is 15.86); F37 9.71, A71 16.30, T13 16.78, T61 8.46; the qualification set with the estimate would shrink. Count reports and 4.3/4.2 also use the 2-op convention.
- Year: local Pacific 2026 (my reading) vs UTC 2026 vs the whole export: at most 0.1 kg per field, no flips.
- Registration in force: dated attribution (my reading) vs the current MASTER row. Towered only: HWK 22 vs 20, CRV 18 vs 12, OSY 23 vs 21, KTY 16 vs 15, VNL 16 vs 14, DMR 13 vs 11 kg (ops 17,600 vs 16,900; 9,900 vs 7,900; 19,400 vs 18,800; 13,600 vs 12,900; 12,200 vs 11,500; 7,900 vs 7,300). The boundary day (events on the cancel date itself) is ambiguous but appeared not to matter at the rounding level.
- Tower hours: end time inclusive vs exclusive changes unrecorded by at most 1 (HWK 3,289); seasonal windows ("Nov-Feb") applied by calendar month. Hours-of-operation edges relative to DST are not an issue since both are local.
- "Civil operations" at tower: whether Itinerant Military and Local Military are excluded (my reading). Including them adds HWK 62, CRV 96, KTY 18, OSY 30, VNL 8 ops (about +0.1 kg at CRV).
- Unrecorded ops "taken as piston": at towers all unrecorded ops (including turbine/helicopter) become piston, vs subtracting the tower's own non-piston share (not given, so no alternative figure).
- L08 total: the sheet's Total row is formulas (17,685 ops from takeoffs + landings + 2 x circuits). Reading each circuit as 1 operation would cut the count to about 11,400 (17,685 less the 6,283 circuits), below the 17,539 recorded, so count less recorded would be negative; the 2-op convention is forced.
- Rounding: lead "whole kilograms" from unrounded sums (my reading) vs from rounded per-field values: DMR 12.92 and CRV 17.95 round to 13 and 18 either way; no flip. The 12.5 test applied to unrounded kg: none of the 24 fields is within 0.3 kg of 12.5 under the silent-aircraft estimate (nearest: W33 14.13, K58 11.07, P05 11.11).

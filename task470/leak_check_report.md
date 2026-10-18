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

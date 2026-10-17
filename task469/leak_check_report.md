# leak check, task469

**Verdict: REVIEW.** 16 files read, 6 golden figures and 5 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: decisive, aircraft, filing, pellmont, norvale, grayling, estimator, operator, overruns, flight, departure, operators, on-block, censoring, tellura, filings, silent, censored, on-time, allowance, decision, arrival, brands, operating, reading

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `kda_schedule_facilitation_guideline_e_gates.pdf`: golden figure 175 appears: ...nect flights flown by Pellmont Aviation's Embraer 175s. A filing is made for each relationship. A turn...
- **REVIEW** `kda_schedule_facilitation_guideline_e_gates.pdf`: carries 21 of 28 distinctive words of the committed call: 'Send back the minimum ground times filed for Norvale Connect flown by Pellmont Aviation, Embraer 175 (35 minutes), Tellu'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `kda_schedule_facilitation_guideline_e_gates.pdf`: 12 of 25 stump-paragraph terms appear (aircraft, filing, pellmont, norvale, operator, flight); read whether the document names the move
- **REVIEW** `kdy_schedule_file_layout.pdf`: 4 of 25 stump-paragraph terms appear (aircraft, flight, departure, arrival); read whether the document names the move

## 6 ranking artifacts (REVIEW 4, INFO 1)
- **REVIEW** `kdy_affiliate_register.xlsx`: names 5 of 5 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `kdy_monthly_punctuality_by_carrier_2026.xlsx`: names 3 of 5 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `kdy_regional_aircraft_register.csv`: names 3 of 5 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `kdy_regional_fleet_plan_s27.csv`: names 3 of 5 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `kdy_e_gates_ground_time_filings_s27.csv`: names 5 of 5 answer-set candidates; confirm it does not rank them on the decision question

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

Each REVIEW line above, answered: the guideline's example relationship (Norvale Connect flown by Pellmont's Embraer
175s) is the definition's own example and names no share, estimator or decision; the stump-paragraph terms in the
guideline and the layout note (Pellmont, Norvale, aircraft, filing, operator, departure, flight, arrival) are the
documents' own subjects; the affiliate register, aircraft register, fleet plan and punctuality workbook name the
relationships beside counts, numbers and dates and rank nothing on the turns' needs. Harmless.

### Round 1 (isolated copy of prompt.txt and target.zip, first build)

Verdict: no sentence names the decisive step; no ranking or answer-shaped file; the reader's own answer sat on the
stand-time rung (all six sent back) and its question 6 described that rung's path; it filed all twelve schedule
figures through the DEI 050 records, so the schedule ask's device was rebuilt; its realism findings were fixed in the
generator.

1. Decisive step: no single sentence says "do X to decide which filings go back", but kda_schedule_facilitation_guideline_e_gates.pdf SFG-3 gives the pieces. 2.4: "Time a ready aircraft is held (by air traffic control, for the stand or the apron, for the weather or for connecting passengers) is not time the turn needs." with 3.1: "The authority accepts a filed minimum ground time for a carrier relationship when no more than 20 per cent of the relationship's turns would need longer than it." and 3.2 (peak window 15 Jun to 15 Sep). Nothing says how to build the turn list or join the three flight logs to the stand log.
2. None. The punctuality workbook ranks brands on on-time rates only (not ground times). No file scores relationships on the question.
3. kdy_delay_code_groups.csv (the "kda_group" column is the authority's own mapping and exists to make 2.4/2.5 executable; guideline 2.5 refers to it, so it is borderline natural). The staffing CSV, fleet plan, punctuality workbook and stations CSV look like context/distractors, not helpers.
4. Nothing reads as the answer. The filings CSV gives filed values only (35/40/30/40/30/35).
5. SFG-3 3.1 ("no more than 20 per cent of the relationship's turns would need longer than it"), 2.1 (relationship = brand + operator + aircraft type; "A turn belongs to the relationship of its departing flight"), 3.2 (turns with on-block 15 June to 15 September inclusive), 2.2 (turn = E-gate on-block to off-block, both on same operating day 03:00-02:59, tow time to a remote stand included), 2.4 (needed time runs to ready; held time not needed). Literal reading gives: Norvale Connect/Pellmont 55, Norvale Connect/Grayling 55, Norvale Connect/Sable 50, Tellura Express/Pellmont 60, Tellura Express/Sable 45, Grayling Air/Grayling 50 (all six sent back). Filed 5-minute multiples per 3.3.
6. Mostly following stated rules (2.2, 2.4, 2.5, 3.1-3.3) plus reading data correctly (UTC Pellmont log vs local others, Grayling "code-minutes" delay field, stand-log registration without hyphen, past-midnight date roll in Sable/Grayling logs, brand by flight-number block). The one analytic element is the "would need" estimand: removing held minutes (2.4) from gross on-block-to-off-block. Without it TQ/Pellmont is 65 not 60 and TQ/Sable 50 not 45; the other four are unchanged. Nothing looks planted.
7. Realism findings:
 - kelderby_aodb_stand_events: registration written "CGPUW" by VDGS rows and "C-GPGB" by RAMP rows (1297 hyphenated); callsign blank on tow rows. Plausible mess, but the ATC callsign is only on on-block/off-block.
 - Sable xlsx: date column is the scheduled date, so after-midnight actuals have no date (need roll-over); Grayling "delays" mixes "93-3 37-4" code-minutes in one text cell; Pellmont is UTC, others local. Plausible.
 - kdy_regional_aircraft_register.csv: home_base mixes IATA codes with names ("Brannoch", "Orlen Falls") and "spare" exactly on the rows without KDY line dates; Dash 8-400 and ATR serials of 17xxx (C-FSDR 17605, C-FSPG 17850, C-GGTM 17935) look like Embraer 175 serials. Fleet plan says 13 Pellmont E175 / 12 Sable / 7 Grayling; register lists 15 E175 etc. (some "spare"/non-KDY).
 - SSIM S27: TQ5108 and TQ5308 each appear twice as the same flight number/itinerary/dates on different routes (TRV and OLF origins); station block minutes in the stations CSV match the SSIM block times exactly (all 26,567 KDY departures, zero deviation), very clean. Schedule gaps are only 25/30/35/40/45 (hand-built feel). Stand times are suspiciously regular (many actual = scheduled to the minute).
 - NV3450-3499 reassigned to Sable from 2026-07-15 in the register, but no such flight appears in 2026 logs or in S27 files; a block with no content.
 - Filing file has non-sequential filed_on dates; fine. Punctuality workbook departures (e.g. Norvale June 2384) are not checked against logs.
8. Method: paired each ON-BLOCK (E stand) with the next OFF-BLOCK on the same registration (normalised hyphen), keeping towed turns (end at the R-stand off-block), only turns whose on and off fall on the same 03:00-02:59 operating day and whose on-block is 15 Jun to 15 Sep 2026 (selected 9,212 turns: Norvale/Pellmont 2731, Norvale/Grayling 1114, Norvale/Sable 2398, Tellura/Pellmont 1023, Tellura/Sable 930, Grayling own 1016). Departing callsign + registration + time matched to the operator log (Pellmont UTC minus 4h; Sable/Grayling local with day roll-over fix). Brand from flight prefix/number block. Needed time = off-block minus minutes of delay codes grouped "held for another reason", minus on-block. Smallest multiple of 5 with <=20% of turns needing longer:
 - Norvale Connect/Pellmont (filed 35): 55 (share >50 is 28.6%, >55 is 10.6%) -> sent back
 - Norvale Connect/Grayling (40): 55 (>50 36.4%, >55 12.5%) -> sent back
 - Norvale Connect/Sable (30): 50 (>45 23.7%, >50 3.1%) -> sent back
 - Tellura Express/Pellmont (40): 60 (>55 32.0%, >60 15.9%) -> sent back
 - Tellura Express/Sable (30): 45 (>40 55.4%, >45 19.6%, close to the edge) -> sent back
 - Grayling Air/Grayling (35): 50 (>45 33.8%, >50 12.0%) -> sent back
 Shares at 20..60 min are computed from the same needed-time distribution. All six sent back.
9. Method: parsed the S27 SSIM, dropped legs carrying DEI 050 (operating-carrier disclosure; marketing duplicates such as NV3200 = TQ5100, TQ5200 = NV3000, GY300 = NV3800), expanded legs by days of operation (L file local, U files UTC), checked block times equal the stations CSV, converted to Kelderby local (UTC-4), chained each KDY arrival to its onward flight (or next leg of same number) and kept chains where arrival and departure fall on the same 03:00 operating day (gaps 25-45 min; others 470+ overnight). Relationship from the departing operating flight number block. Week 12-18 Jul 2027, turns / scheduled shorter than filed:
 - Norvale Connect/Pellmont: 213 / 42 (filed 35, gaps 30 are short)
 - Norvale Connect/Grayling: 84 / 21 (filed 40)
 - Norvale Connect/Sable: 189 / 42 (filed 30, gaps 25)
 - Tellura Express/Pellmont: 105 / 28 (filed 40)
 - Tellura Express/Sable: 91 / 28 (filed 30)
 - Grayling Air/Grayling: 77 / 21 (filed 35)
 Total 759 turns, 182 short. Counting the DEI 050 duplicates would inflate turns.

### Round 2 (fresh copy of the fix-pass build)

Verdict: nothing quoted for question 1 beyond SFG-3 2.4, which defines need; no ranking, helping or answer-shaped file;
question 6 an analytical choice (the censoring); its own answer landed the call; it counted every leg of the 2027
submissions and missed all twelve schedule figures; its findings on the UTC files' station variations and the start-up
codes were fixed in the generator without moving a graded figure.

# Reader answers (task469 r2)

Shorthand: NV-PMV = Norvale Connect/Pellmont E175 (filed 35); NV-GYA = Norvale Connect/Grayling ATR (40); NV-SBC = Norvale Connect/Sable Dash 8 (30); TQ-PMV = Tellura Express/Pellmont (40); TQ-SBC = Tellura Express/Sable (30); GY-GYA = Grayling Air own flying (35).

1. No file or sentence names the decisive step. The closest, in kda_schedule_facilitation_guideline_e_gates.pdf s2.4, only define the quantity: "An aircraft that is ready before its scheduled departure waits for it. Time a ready aircraft is held (by air traffic control, for the stand or the apron, for the weather or for connecting passengers) is not time the turn needs." They do not say how to estimate the need when the aircraft was ready early and waited (the on-time turns).

2. None. kdy_monthly_punctuality_by_carrier_2026.xlsx gives on-time rates by brand but does not rank relationships on ground time. kdy_e_gates_ground_time_filings_s27.csv lists only the filed numbers.

3. Nothing is overtly analyst-only. kdy_delay_code_groups.csv (a "kda_group" column that tells you which codes are "aircraft not ready" or "held for another reason") reads slightly bespoke, since IATA codes carry no such grouping. kdy_regional_aircraft_register.csv and kdy_regional_fleet_plan_s27.csv are plausible distractors. The 12-day punctuality file, the staffing file and the fleet plan are not needed.

4. No figure reads as the answer. The filed minutes (30 to 40) are context. The 20 per cent in SFG-3 s3.1 and the 15 June to 15 September peak in s3.2 are the rule, not a result.

5. SFG-3 s3.1: "The authority accepts a filed minimum ground time for a carrier relationship when no more than 20 per cent of the relationship's turns would need longer than it." With s3.2 (turns with on-block 15 Jun to 15 Sep 2026 inclusive), s3.3 (multiples of 5) and s2.2/2.4 (turn and need), the literal reading depends on what "need" is. It does not give a method for turns that left on time, where the need is only known to be at most the time they stood. Read literally as "need = on-block to ready, ready where known": results below (my answer in 8). A cruder literal reading (need = off-block minus on-block minus held minutes, treating the on-time turns' stand time as the need) gives much longer times (shortest accepted: NV-PMV 55, NV-GYA 55, NV-SBC 50, TQ-PMV 60+, TQ-SBC 50, GY-GYA 50) and sends back all six filings. The sentence alone does not settle between these.

6. An analytical choice (censoring). Turns that left on time or with only held delays show when the aircraft was ready only as "no later than"; only turns with an aircraft-not-ready delay reveal the true need. Using raw stand time overstates need. No stated rule or single field decides it. Deciding text: s2.4 "An aircraft that is ready before its scheduled departure waits for it." Data semantics (delay-code grouping, sub-letters, UTC vs local, hyphenless registrations) is Layer 1 cleaning, needed but not decisive.

7. Realism findings:
- kelderby_aodb_stand_events: VDGS rows use registrations without hyphen (CFSBP), RAMP tow rows use hyphen (C-GPGB): plausible for a mixed-source log but inconsistent. Tow events have blank callsign. Very regular event_ids 700001 upward.
- Delay codes in Sable use sub-letters (89B), Grayling uses "89-2" with space-separated multiples ("93-3 37-4"), Pellmont separate columns: plausibly operator-specific, matches SFG note on sub-letters. grayling_kdy_sectors registration also hyphenless (CGGDM).
- Very uniform delay structure: a large share of departures carry code 89 with 1 to 3 minutes; 93 dominant. Looks formulaic (held minute 1 as a standing pushback delay).
- AODB off-block vs operator out time differ by exactly 0 or +/-1 minute for all matched departures (13,125 equal, 945 off by 1): too tidy.
- 14 aircraft appear with an OFF-BLOCK first event on 1 June (overnight carry-in) which is realistic.
- Pellmont log is in UTC with a fixed -4h offset needed (no DST problem in Jun to Sep). Sable xlsx has "Date" as datetime and times as text "06:05". Punctuality xlsx: departures/arrivals identical per month by brand, and brand counts (e.g. Norvale 2384) are round multiples of a daily pattern, so very regular.
- Sable movements row Reg uses hyphen; AODB does not.
- kdy_initial_submissions_s27.ssim: Tellura and Grayling files are in UTC with variation "+0000" for every station, even for stations with offsets (SLV, QRN) which a real SSIM would not do for a UTC file. Norvale file is local with proper offsets. TQ and GY blocks also run 29MAR27 to 31OCT27 for some legs (UTC date shift).
- kdy_regional_fleet_plan_s27 is a tidy monthly table with 0 or 1 in heavy check: plausible. Serial numbers for Dash 8 / ATR / E175 look plausible.
- Rotation layover for Norvale chains loops back to the first flight number (e.g. "NV 30001" layover 1 character merged), plausible.
- Season dates: s26 file created "02MAR26", s27 submissions created 01/06/08 OCT26, consistent with filings dates.
- AODB has stands R1 to R5 for 481 on-blocks (remote stand), these are not E gate turns.

8. My answer. Method: AODB ON-BLOCK to next OFF-BLOCK of the same aircraft (registration with hyphens stripped), tow pairs folded in (ending on R stand), kept only turns that began on an E stand with on-block and off-block on the same 03:00 to 02:59 operating day and on-block 15 Jun to 15 Sep 2026 inclusive (about 9,200 turns). Matched each to the departing operator flight log (callsign + off-block within 1 minute; Pellmont UTC minus 4h), took delay minutes by code and grouped them with the group file. Relationship from flight prefix and flight-number block (NV 3000-3499 Pellmont, 3500-3799 Sable, 3800-3899 Grayling; TQ 5100-5299 Pellmont, 5300-5399 Sable; GY Grayling). Need: where the turn left late with aircraft-not-ready minutes, need = scheduled departure + those minutes - on-block (exact); where there was no aircraft-not-ready delay the aircraft was ready by (off-block - held minutes), so need is only an upper bound (left-censored). I estimated the share needing longer than G with a Kaplan-Meier-style estimator on the flipped (censored) data, "longer" being strictly more than G. Accepted when share <= 20%.

Shares needing longer than G (G = 25, 30, 35, 40, 45):
GY-GYA .32 .08 .003 0 0 | NV-GYA .93 .60 .31 .06 .01 | NV-PMV .89 .61 .28 .08 .02 | NV-SBC .32 .08 .02 .01 .00 | TQ-PMV 1.00 .95 .64 .26 .08 | TQ-SBC .87 .30 .05 .00 .00.

Result: Send back NV-PMV (filed 35, share .28; shortest 40), TQ-PMV (filed 40, share .26; shortest 45), TQ-SBC (filed 30, share .30; shortest 35). Accept GY-GYA (35; shortest acceptable 30), NV-GYA (40; shortest acceptable 40), NV-SBC (30; shortest acceptable 30).
Shortest acceptable per relationship: NV-PMV 40, NV-GYA 40, NV-SBC 30, TQ-PMV 45, TQ-SBC 35, GY-GYA 30.
Alternative uncorrected readings (stand time minus held, ignoring that on-time aircraft waited) would instead send back all six; I judge that wrong because of s2.4.

9. Week 12 to 18 July 2027 (operating days, local). Method: parsed every type 3 leg in kdy_initial_submissions_s27.ssim, expanded over period and days of operation, honoured date variation, converted to UTC (Norvale file is mode L with the stated offsets; Tellura and Grayling files are mode U), then to Kelderby local (UTC-4 in July). A turn = a leg arriving at KDY paired with its onward KDY departure (onward airline/flight in positions 138-144 with layover 0, or the next leg sequence under the same number when the onward is blank), arrival and departure on the same 03:00 to 02:59 operating day; overnights (layover 1 or crossing 03:00) dropped. Relationship = departing flight's prefix and number block. Scheduled ground = departure minus arrival aircraft time; short when below the filed minutes. Eight chain breaks excluded.
Turns / scheduled shorter than filed:
NV-PMV 290 / 63; NV-GYA 133 / 56; NV-SBC 259 / 63; TQ-PMV 231 / 119; TQ-SBC 168 / 42; GY-GYA 154 / 42. (Total 1,235 turns.)

### Round 3 (fresh copy after the SFG-3 2.1 clause)

Verdict: no file states the decisive step (2.4 defines need; nothing says an undelayed turn only bounds it); question 6
an analytical choice; no ranking or answer-shaped file; its own answer landed the call by a reverse product-limit
estimate; it counted every leg and missed all twelve schedule figures (1,242 turns against 759). Its finding that the
2026 register's fourteen Pellmont aircraft disagreed with the fleet plan's thirteen was fixed (the plan now counts each
operator's whole fleet and, apart, the aircraft left for its Kelderby lines); the three delay formats, the registration
formats by recording source, Sable Coast's flight-date convention and the punctuality workbook's even months stand as
the systems' own.

# Reader answers (task 469, r3)

1. Decisive step: no sentence names it. The nearest text is SFG-3 2.4, "The time a turn needs runs from on-block until the aircraft is ready to push back: doors closed, ground equipment clear and the handler's release given. An aircraft that is ready before its scheduled departure waits for it. Time a ready aircraft is held (by air traffic control, for the stand or the apron, for the weather or for connecting passengers) is not time the turn needs." (kda_schedule_facilitation_guideline_e_gates.pdf). It defines need and says waiting/held time is excluded. It does not say that undelayed turns only bound the need from above, so no sentence tells you to treat those turns as censored.

2. No file ranks or scores the relationships on the main question. kdy_monthly_punctuality_by_carrier_2026.xlsx gives on-time rates by brand (not by relationship, and not ground time). The filings CSV only holds the filed minutes.

3. kdy_delay_code_groups.csv (the kda_group column) is the file closest to existing only to help: a delay-code to "aircraft not ready / held for another reason" grouping that sits on top of the standard IATA codes, and the guideline cites it. It could plausibly be an authority file, but it is the one that exists to feed the method. The staffing CSV, punctuality workbook, fleet plan and station list look like distractors, not helpers.

4. Nothing reads as the answer. The filed ground times (35/40/30/40/30/35) are context. The punctuality rates look like a lure toward ranking by punctuality.

5. SFG-3 3.1: "The authority accepts a filed minimum ground time for a carrier relationship when no more than 20 per cent of the relationship's turns would need longer than it." With 3.2 (turns at E gates, on-block 15 June to 15 September inclusive) and 3.3 (multiples of five, shortest acceptable). Read literally, "would need longer" is the share of turns whose need exceeds the ground time. The need is not observed for every turn, so the literal reading does not fix the computation: the naive reading (need = off-block minus on-block minus held minutes, for all turns) gives a different result from the censoring-aware reading. Naive results (peak, share needing > G): GY-GYA 30 min 86.7%, 45 min 33.2%, 50 min 11.9%; i.e. shortest acceptable GY 50, NV-GYA 55, NV-PMV 55, NV-SBC 50, TQ-PMV 60+ (15.6% at 60 -> 60), TQ-SBC 50. Censoring-aware results are in section 8.

6. An analytical choice (and some data work). The decisive step is treating the undelayed turns correctly: an aircraft that leaves on schedule was ready no later than its off-block, so its need is only bounded above (waiting for STD). Only turns with an "aircraft not ready" delay show the actual need. Using raw on-to-off durations overstates the need and moves every shortest acceptable time up by 15 to 20 minutes. Deciding this relies on SFG-3 2.4 (quoted above) plus the delay-code groups. The rest is cleaning: matching 3 operator logs (Pellmont in UTC, Sable/Grayling local, different delay formats), registrations with and without hyphen (RAMP rows), tows, overnight stays, relationship by departing flight number via the register's number blocks. A reader could argue part of it is rule application (2.4 plus the group file define the exclusions), but the censoring is not stated.

7. Realism findings:
 - kelderby_aodb_stand_events: registrations lose the hyphen in VDGS rows (CGPUW) but keep it in RAMP rows (C-GPGB); tow events have empty callsigns. Plausible mixed systems, but the clean split by recorded_by looks designed. 480 on-blocks at R stands.
 - pellmont log: times in UTC with a single minute offset between log out_utc and the AODB off-block on about 824 turns (log and AODB differ by exactly 1 minute); delay_min_1 is almost always 1 for codes 81/89 (suspiciously uniform).
 - grayling_kdy_sectors: reg without hyphens (CGGDM), delays as space separated "93-20 32-18" strings; sched_arr earlier than sched_dep for NV3810 KDY-QRN (time zone, local at destination) with no zone stated.
 - sable xlsx: Date as midnight datetimes, times as text, delay codes with sub-letters (89B, 81A) vs plain codes elsewhere; Date for after-midnight departures stays on the schedule date (e.g. STD 23:30, off-block 00:04 on the next calendar day recorded under the previous date).
 - Delay minutes do not always reconcile with actual minus scheduled (82 departures differ by more than 3 min, e.g. SBC3557 03 Aug 2026: 93-2 and 37-91 on a 102 min late flight is fine, others are not), and secondary delays are often logged as small sub-minute values.
 - Pellmont fleet in the aircraft register has 14 tails (4 without kdy_lines_from) but the fleet plan has 13 in fleet; the register's kdy_lines_from is 2026-03-29 for nearly all.
 - kdy_regional_aircraft_register / fleet plan / staffing / punctuality files are not needed for either question.
 - The initial submission has records with Tellura and Grayling in UTC (mode U) and Norvale in local, with period start 29MAR27 for early-UTC legs: realistic. Filed Norvale flights NV38xx for Grayling and the "12345 7" days pattern look generated but fine. The ssim has 201-char lines with CRLF (200 character records plus CR), fine.
 - Punctuality xlsx uses the "15 minutes" definition; departure counts for Norvale Connect are exactly equal to arrival counts each month, and several months show identical counts across brands (e.g. 713 for Tellura in July and August; 390/690/2384 repeat in June and September), which looks generated.

8. My answer to the main question. Method: turns from the stand log: pair each ON-BLOCK at an E stand with the next OFF-BLOCK of the same aircraft (hyphens stripped), ignoring tow events (a tow to R1 and back stays in the turn), requiring on-block and off-block on the same 03:00-02:59 operating day, on-block 15 Jun to 15 Sep 2026 (about 9,200 turns; arrivals straight onto R stands are not E gate turns). Relationship from the departing callsign number via the register blocks (NV3000-3499 Pellmont, NV3500-3799 Sable, NV3800-3899 Grayling, TQ5100-5299 Pellmont, TQ5300-5399 Sable, GY200-399 Grayling). Joined to the three operator logs (Pellmont converted from UTC by -4 h) on registration and callsign for the departure delay codes. Need = on-to-off minutes minus "held for another reason" minutes. Turns with a departure delay in an "aircraft not ready" code (and actual later than scheduled) give the exact need; the others (on-time or only held) are only known to need at most that figure. I estimated the share needing longer than each G with a reverse Kaplan-Meier (left-censored) estimate by relationship.
 Share needing longer than G (%), peak 2026:
 | G | GY-GYA | NV-GYA | NV-PMV | NV-SBC | TQ-PMV | TQ-SBC |
 | 25 | 32.0 | 92.7 | 88.7 | 31.7 | 100 | 87.3 |
 | 30 | 8.2 | 60.2 | 60.5 | 7.8 | 94.8 | 29.5 |
 | 35 | 0.3 | 30.7 | 27.7 | 2.0 | 63.6 | 4.9 |
 | 40 | 0.0 | 6.1 | 8.3 | 1.0 | 26.3 | 0.4 |
 | 45 | 0.0 | 1.2 | 2.3 | 0.4 | 7.5 | 0.2 |
 Shortest acceptable (first multiple of 5 at or under 20%): GY-GYA 30, NV-GYA 40, NV-PMV 40, NV-SBC 30, TQ-PMV 45, TQ-SBC 35.
 Filed: GY-GYA 35 (accept), NV-GYA 40 (accept), NV-PMV 35 (send back, 40), NV-SBC 30 (accept), TQ-PMV 40 (send back, 45), TQ-SBC 30 (send back, 35).
 Caveat: the censoring treatment is my judgement; the naive duration version gives 50/55/55/50/60/50 and sends all six back.

9. Second part. Method: parsed the type 3 records of kdy_initial_submissions_s27.ssim by the layout note; carrier times are in the carrier record's mode (Norvale L, Tellura and Grayling U, so converted to Kelderby local with the departure/arrival UTC variation fields; days of operation and periods apply to the date in the carrier's mode); aircraft times (positions 44-47 and 58-61), not passenger times. A turn is a leg arriving at KDY paired with the next KDY departure of the aircraft: the onward airline and flight (138-144), or, where blank, the next leg of the same flight number (through flights); kept only when arrival and departure fall on the same 03:00-02:59 local operating day (layover digit ignored, because U-mode date shifts make it unreliable, e.g. GY224 to GY225 is a 35 minute turn). Turns belong to the departing flight's relationship by number block. Counted by operating day 12 to 18 July 2027 (the "12345 7" flights do not operate Saturday 17 July). Scheduled ground = departure minus arrival.
 | Relationship | Filed | Turns | Scheduled shorter than filed |
 | NV-PMV (Norvale Connect/Pellmont) | 35 | 290 | 63 |
 | NV-GYA (Norvale Connect/Grayling) | 40 | 133 | 56 |
 | NV-SBC (Norvale Connect/Sable) | 30 | 259 | 63 |
 | TQ-PMV (Tellura Express/Pellmont) | 40 | 231 | 119 |
 | TQ-SBC (Tellura Express/Sable) | 30 | 168 | 42 |
 | GY-GYA (Grayling Air) | 35 | 161 | 42 |
 Total 1,242 turns. Strict "shorter than" used.

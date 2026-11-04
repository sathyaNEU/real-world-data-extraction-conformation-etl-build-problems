# leak check, task461

**Verdict: REVIEW.** 16 files read, 21 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: vapour, compartment, petrol, previous, diesel, dockets, delivery, equation, saturation, dispatch, sentence, exports, distillate, screen, system, golden, emissions-inventory, carries, measured, per-product, liquid, retail, decisive, leaves, loading-loss

## 3 answer figures in the pack (REVIEW 5)
- **REVIEW** `CAQA_return_protocol_petroleum_premises_2026.pdf`: golden figure 1.1 appears: ...2026. Replaces the 2021 edition. 1. Application 1.1 This protocol applies to every licensed premises...
- **REVIEW** `EPL_20514_licence_conditions.pdf`: golden figure 1.1 appears: ...anniversary date 1 July. 1. Scheduled activities 1.1 Petroleum products storage: bulk storage of unle...
- **REVIEW** `EPL_20514_licence_conditions.pdf`: golden figure 1.2 appears: ...th, and loading into road tankers at bays 1 to 5. 1.2 Scale: storage capacity above 20,000 kilolitres....
- **REVIEW** `vru1_stack_emission_survey_2026.pdf`: golden figure 1.1 appears: ...al. Test dates 18 and 19 August 2026. 1. Purpose 1.1 Annual compliance test of vapour recovery unit V...
- **REVIEW** `EPL_20514_licence_conditions.pdf`: carries 8 of 10 distinctive words of the committed call: "Report 38.4 tonnes of VOC from product loading for 2026: the Warrenby terminal exceeded its licence's limit by 18.4 tonn"

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `CAQA_return_protocol_petroleum_premises_2026.pdf`: 6 of 25 stump-paragraph terms appear (vapour, petrol, diesel, distillate, measured, liquid); read whether the document names the move
- **REVIEW** `EPL_20514_licence_conditions.pdf`: 6 of 25 stump-paragraph terms appear (vapour, petrol, diesel, distillate, system, measured); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 12 describing content (REVIEW 2)
- **REVIEW** `CAQA_return_protocol_petroleum_premises_2026.pdf`: names 7 column(s) of the data files verbatim (Diesel, Internal floating roof, Service, product, tank, time): confirm it is the organisation's own record and not a note written for the analyst
- **REVIEW** `EPL_20514_licence_conditions.pdf`: names 5 column(s) of the data files verbatim (Brennock Fuels, product, tank, time, unit): confirm it is the organisation's own record and not a note written for the analyst

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Isolated reader, 2026-11-04 (general-purpose, sonnet, medium), on a fresh copy of prompt.txt and target/ (target.zip sha256 ccb06130f80e87ba7423fed9056948c44ea7457e6ea8ebd8d4f800ac7d1f9f58). Sweep 4's lines and the answer-figure lines were kept out of the brief and ruled in the main thread.

# Leak reader answers (task461)

1. Decisive step: none states it outright. Closest: CAQA protocol 2.2 "Where bays send the vapour displaced during loading to a vapour recovery or vapour combustion unit, that unit's stack is the loading point for those bays" and licence O1 (petrol only at bays 1-3 via VRU-1). These are standing rules, not an announcement.
2. Ranking/scoring of candidates: none. No file ranks anything on the prompt's question.
3. Files existing only to help the analyst: none clearly. Mildest candidates: delivery_sites.csv, tanker_register_2027-01.xlsx (see d, e), both plausible business records.
4. Figure/name reading as the answer: none. The licence "20 tonnes in any calendar year" (L1) is the standing limit named in the prompt, context. Test report "mean outlet concentration was 6.5 g/m3 ... compliant" is a concentration test, not the annual mass.
5. Literal-fixing sentences: 
   - CAQA 2.1 "Reporting year: the calendar year, in the premises' local time"; fixes the window as local-time calendar year/quarters.
   - CAQA 3.1 "sum, over the 15-minute intervals that begin in the period, of the monitor's VOC mass rate times the interval" fixes measured release for the VRU-1 stack by interval start.
   - CAQA 3.2 "An interval without a valid reading ... takes the mean of the valid readings in the hour before it and the hour after it. An interval in which the unit was stopped ... releases nothing." fixes gap handling.
   - CAQA 4.1-4.4 fix the estimate inputs (Antoine-type vapour pressure, molecular weight by grade season of loading month, meter temperature and observed volume) for non-measured (distillate bays 4, 5).
   - CAQA 5.2 "A day takes the rate for the construction, seal and vents the tank had at the start of that day" and 5.3 "megalitres the tank received from ships in the period, as shore received at 15 degrees Celsius" fix tank standing/working loss populations.
   - Licence D2 "Product loading means the loading of petroleum product from the premises' storage into road tankers at the premises' loading bays", with L1: fixes the limit population as road-tanker loading only (excludes ship receipt/tank losses).
   This is a rule-application layer (the formula and population are fully filed); I find no sentence that fixes a choice between competing analytical methods.
6. What decides the main answer: mostly following stated rules/procedures (CAQA 3.1-3.2, 4.x, D2) plus reading fields/units correctly (local time vs AEST clocks, kg/h, L15). Deciding sentence candidates: CAQA 3.2 and licence D2 / L1 (which releases count toward the 20 t). Nothing reads as an analytical-choice stump (no comparison group, no estimation under uncertainty); nothing looks planted either, though the shift log and work orders carry the semantic keys (see notes).

## Flagged items
a. harmless, because EPL_20514 is a standing licence (conditions O1-O3, L1, M1, R1-R2, D1-D3) with no 2026 figures or conclusion; "20 tonnes in any calendar year" is the limit the prompt already names.
b. harmless, because CAQA protocol is written as the regulator's own publication (edition, publication date, enquiries line, "Industry Reporting, Coastal Air Quality Authority", footers); its column names (licence_no, point_id, period, etc.) are the return layout the prompt tells the analyst to use. It does fix the method literally (rule application), but it is not addressed to the analyst.
c. harmless, because EPL_20514 is issued "under the Protection of the Environment Act by a delegate of the Authority", Variation 4 with date and anniversary; R1 naming the return layout is normal licence text, not an analyst note.

d. tanker_register_2027-01.xlsx: reads as a terminal/fleet register (fleet unit, operator, TMS tanker ID, rego, compartment capacities, previous regos with changeover dates, contract-carrier notes). It reads as the terminal's own record, though the "TMS compartment numbers" and "Previous regos" columns are clearly there to bridge keys between systems; plausible for a real TMS/fleet list. Minor: slightly crosswalk-shaped, not an answer leak. Note the prompt-adjacent file "tank_register_2027-01.xlsx" is a genuine tank register (roof, rim seal, vents, diameter, "Register as at 08/01/2027") and shows end-of-year seal/vent state, not the date-of-change.
e. delivery_sites.csv: ordinary customer-site master (site_code, name, type, locality, postcode, customer_class); 150 rows, mixed Dealer/Commercial/Company site classes. Harmless, ordinary business record (a distractor).

## Mild notes (not leaks of the answer)
- control_room_shift_log_2026.csv 04/04/2026: "Daylight saving ended 03:00, TMS and VRU PLC back on AEST; tank gauging unchanged, it runs on AEST all year" and work order WO26004385 "system time AEST, no daylight saving" state the clock conventions in plain words; these are the kind of note an operator writes, but they do spell out the time-basis trap for the stock account.
- Shift log 12/05/2026 "VRU-1 outlet analyser replaced, new channel VOC_OUT2 on the CEMS" and work order WO26004136 explain the CEMS channel change; shift log and work orders give VRU-1 stop windows (24/02, 12/05 etc.) and TK seal/vent upgrade dates (WO26004104 etc.). These are real-looking operational records, and they are what the rules in CAQA 3.2/5.2 need; they do not state the result.
- vru1_stack_emission_survey_2026.pdf says CEMS agrees with the reference method within 10 per cent: a realistic third-party report, mildly reassuring about the monitor.

## Realism
none strong. Minor tells: shift log entries are heavily templated ("Fire pump weekly run, OK", "earth rig fault, reset"), and delivery site codes split cleanly R/S prefixes; both read plausibly as system logs. Shift log timestamps are occasionally out of chronological order within a date (e.g. 13/01 N 22:47, 23:13, then 02:04), consistent with night shifts spanning midnight.

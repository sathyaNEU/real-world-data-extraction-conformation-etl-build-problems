# leak check, task249

**Verdict: REVIEW.** 14 files read, 24 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: afternoon, reference, network, analysers, decisive, comparison, sensor, boundary, method, analyser, firmware, spreads, quality, records, all-hours, calibration, monitoring, surface, nothing, window, readable, architecture, decision, low-cost, comarca

## 3 answer figures in the pack (REVIEW 4)
- **REVIEW** `ozone_network_qa_plan_v3.pdf`: golden figure 0.85 appears: ...e eight weeks before the list is set lies outside 0.85 to 1.15. A node on the list is taken to the bench...
- **REVIEW** `ozone_network_qa_plan_v3.pdf`: golden figure 1.15 appears: ...weeks before the list is set lies outside 0.85 to 1.15. A node on the list is taken to the bench, measur...
- **REVIEW** `maintenance_log_2027-09_2028-05.pdf`: carries 4 of 6 distinctive words of the committed call: 'Take 8 nodes down for the bench at the June round: OZ06, OZ17, OZ21, OZ25, OZ29, OZ32, OZ33, OZ34.'
- **REVIEW** `ozone_network_qa_plan_v3.pdf`: carries 6 of 6 distinctive words of the committed call: 'Take 8 nodes down for the bench at the June round: OZ06, OZ17, OZ21, OZ25, OZ29, OZ32, OZ33, OZ34.'

## 4 design-note vocabulary (REVIEW 6)
- **REVIEW** `DATA_DICTIONARY.md`: 7 of 25 stump-paragraph terms appear (network, analysers, analyser, firmware, quality, records); read whether the document names the move
- **REVIEW** `indice_de_ficheros.md`: 6 of 25 stump-paragraph terms appear (network, analysers, analyser, firmware, quality, low-cost); read whether the document names the move
- **REVIEW** `maintenance_log_2027-09_2028-05.pdf`: 5 of 25 stump-paragraph terms appear (network, analyser, firmware, low-cost, comarca); read whether the document names the move
- **REVIEW** `ozn_firmware_4-2_release_note.pdf`: 3 of 25 stump-paragraph terms appear (network, firmware, records); read whether the document names the move
- **REVIEW** `ozone_network_qa_plan_v3.pdf`: 9 of 25 stump-paragraph terms appear (reference, network, analysers, sensor, analyser, quality); read whether the document names the move
- **REVIEW** `rrvca_ozone_station_sheet_2028-04.pdf`: 6 of 25 stump-paragraph terms appear (network, analysers, comparison, method, analyser, comarca); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

One isolated reader (Sonnet, medium, the prompt and a fresh unzip of b0efc2e9 only, about four minutes). It landed
the call: OZ06, OZ17, OZ21, OZ25 and OZ32 low, OZ29, OZ33 and OZ34 high, the golden list with every direction. Its
route: a regression of each node on the four analysers, the eight nodes at 900 m or more showing night-time intercepts
of 9 to 20 ppb ("the valley analysers at about 700 m decouple at night"), then the span on the midday hours (11:00 to
16:00 local), other midday windows agreeing. score_reader.py: the call hit, exit 1 (Gate F failed); the 36 capture
hours all missed (+18 to +24 each: it placed the records stamped in 2000 by their received times but read status 1
as accepted before each node's update). Q1 to Q4: no sentence names the step, nothing ranks the nodes, no figure reads
as the answer; Q5 the plan's span sentence; Q6 an analytical choice. Realism notes taken: OZN-B and OZ19B arrival lags
very uniform, the bench week eight days before installation for almost every node, the register's OZ19 row still
carrying the original unit's model and head serial, the visit sheet's alternating technicians and uniform remarks.


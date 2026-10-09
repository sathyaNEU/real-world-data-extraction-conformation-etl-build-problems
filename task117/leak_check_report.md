# leak check, task117

**Verdict: REVIEW.** 24 files read, 48 golden figures and 3 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: session, replay, closed, decisive, pedestal, decision, monthly, onboard, window, record, measured, rating, charging, forward, corpus, ladder, method, pattern, inside, library, regime, correct, design, binding, mechanism

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `civic_center_ev_service_agreement_draft.docx`: golden figure 11.5 appears: ...-port Level 2, 48 A continuous at 240 V 11.5 kW Civic Center South Deck, levels 2...
- **REVIEW** `civic_center_ev_service_agreement_draft.docx`: golden figure 6.6 appears: ...units replace thirty-two single-port units rated 6.6 kW, which the Customer will remove before energiz...
- **REVIEW** `civic_center_ev_service_agreement_draft.docx`: carries 6 of 7 distinctive words of the committed call: 'File 110 kW as the contracted demand for the first contract year, April 2027 to March 2028.'

## 4 design-note vocabulary (REVIEW 5)
- **REVIEW** `curbline_export_field_notes.txt`: 3 of 25 stump-paragraph terms appear (session, record, charging); read whether the document names the move
- **REVIEW** `fes-07_load_forecasting_standard_rev4.pdf`: 3 of 25 stump-paragraph terms appear (session, closed, record); read whether the document names the move
- **REVIEW** `nspl_schedule_26_ev_charging_service.pdf`: 3 of 25 stump-paragraph terms appear (monthly, measured, charging); read whether the document names the move
- **REVIEW** `parking_services_data_sources.txt`: 6 of 25 stump-paragraph terms appear (session, decision, monthly, record, rating, charging); read whether the document names the move
- **REVIEW** `prompt.md`: prompt sentence carries two or more stump terms: "And for each deck's panel meter and each of its 2026 readings, the kWh the meter recorded that the sessions charged through that panel don't account for."

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt form (clean)

## Solver's-eye read

One isolated reader, run on a fresh copy of `prompt.md` and `target/` only (no design note, generator, submission or report), 2026-10-09. Its four answers, as given:

1. **Which sentence or file tells you the decisive step?** No sentence names the decisive step outright. The closest is FES-07 Rev 4 §2: "Where the equipment the service will supply differs from the equipment in service during the base months, the forecast is prepared for the equipment the service will supply." Revision 3 is logged as "Base months set at the equipment the service will supply." This is a general rule written the way a real standard would write it. It says which equipment to forecast for, but not how: nothing tells you to re-run the sessions at 11.5 kW, capped by each vehicle's onboard charger. Two other lines point in the same direction. The first is in the prompt: "Ricardo Moore in facilities expects the new pedestals to have everyone charged before lunch." It hints that faster charging pulls load out of the noon-to-7:45 billing window. It is a single named opinion, so it could equally be a rung to refute. The second is in parking_services_data_sources.txt: "Each EV charging permit names one vehicle, and Parking Services checks the plate against the vehicle's registration at issue and at every January renewal." That steers toward joining permits to vehicles and then to onboard_charger_kw. A milder pointer is WO-26-0529: "County fleet attendant reports it on swaps between pool cars." I judge all of these acceptable context. None of them states the move.
2. **Which file already ranks or scores the candidates?** None. No file ranks or scores the candidate contract-demand figures. The sub-meter log's "Max demand (kW)" is an all-hours panel maximum and stops at 105.6 kW, which is 16 x 6.6 kW. The campus statements' billing_demand_kw covers the whole campus account. The NSPL guide §7.3 gives a sizing method ("connected nameplate rating ... multiplied by the diversity factor in Table 7-2, stated to the next 5 kW above"), and the prompt asks for that planner figure in its own right. These are inputs, not a ranking.
3. **Which file exists only to help the analyst?** parking_services_data_sources.txt: "Prepared January 19, 2027 by A. Warner for the City Energy Manager." This is the one file that exists to orient the reader. It is a folder index with glosses on how to read the export: "kept as delivered", "These sessions are not in the settlement export", the ACCEPTED/REJECTED replacement rule, and "Both Civic Center decks are permit-only. Each EV charging permit names one vehicle". A handover index like this is plausible in a real office, and it does not state the method or any figure, so it is borderline rather than a leak. Every other file reads as a record the organisation would keep anyway.
4. **Which figure or name reads as the answer?** None. 110 does not appear in any text document. Schedule 1 of the draft agreement is blank ("____________ kW"). The figures that look prominent are inputs or context: the 11.5 kW and 6.6 kW unit ratings in Exhibit A, 105.6 kW in the meter log, and the 0.60 diversity factor, which together with 32 units x 11.5 kW lets you derive the planner's figure, as the prompt asks.

The reader's verdict on each REVIEW line of the mechanical half:

- `civic_center_ev_service_agreement_draft.docx` 11.5: harmless. It is the Exhibit A unit rating (48 A at 240 V), a required input that the station register also states. It only matches a golden figure by coincidence and gives away no result.
- `civic_center_ev_service_agreement_draft.docx` 6.6: harmless. It is the rating of the units being retired, already given in station_register.csv and deck_panel_circuit_schedule.csv (6600 VA). Context only.
- `civic_center_ev_service_agreement_draft.docx` 6 of 7 call words: harmless. The shared words ('Contract Demand', 'first Contract Year', April 2027) are the agreement's own contract vocabulary. The Schedule 1 blank is empty and 110 appears nowhere, so the call's figure is not given away.
- `curbline_export_field_notes.txt` 3 terms: harmless. These are vendor field definitions (the version and auth_code semantics, the station_id reuse rule, the 4 x kWh demand convention). They are needed to read the export and say nothing about the forecasting move.
- `fes-07_load_forecasting_standard_rev4.pdf` 3 terms: harmless, with one caveat. The §2 sentence 'the forecast is prepared for the equipment the service will supply' is the nearest thing in the pack to naming the move. It is stated as a general rule in a standard's own voice and never says how (re-running sessions at the new rating under the vehicles' onboard charger caps). The 'closed month' and 'as they stood on the day' rules are backtest conventions the prompt's check relies on.
- `nspl_schedule_26_ev_charging_service.pdf` 3 terms: harmless. It is the tariff's definition of Billing Demand (weekday 12:00 to 19:45 window, holidays, 5 kW contract steps). The task cannot be done without it, and it does not describe the analysis.
- `parking_services_data_sources.txt` 6 terms: harmless but the most helper-like file in the pack. It indexes the files and glosses how to read them. 'Each EV charging permit names one vehicle' nudges toward the permit-to-vehicle-to-onboard-charger join, but it does not name the move or any figure.
- `prompt.md` meter-residual sentence: harmless. It defines the ask, which is panel kWh minus the kWh of sessions on that panel. It does not reveal the devices that decide it (the N-11 refeed from HP-N, the corrections sheet, the duplicate 2026-12-31 CP-S read, the meter clock with DST disabled).

**Main thread's decision:** no item is a leak, nothing fixed in the generator for the leak read; each item is answered in one line in DESIGN_NOTE.md under `## Leak review`. The reader answered question 1 "none"; the four sentences it quoted as nearest each pin or sit beside an earlier rung (or, for WO-26-0529, record the swaps without their timing), and none names the decisive rung (re-timing the pool-car hand-offs). Question 2 names no file. This mechanical report was re-run after the stage-6 judge's two in-house fixes (the memo's Schedule 26 Section 4 citation, submission step 6), which touched no file under `target/`: REVIEW, the same 8 lines, no LEAK.

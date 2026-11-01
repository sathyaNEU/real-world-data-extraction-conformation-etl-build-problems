# leak check, task152

**Verdict: REVIEW.** 22 files read, 29 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: decline, inverters, period, washes, decisive, carries, soiling, replacement, original, performance, report, measured, losses, restored, irradiation, policy, orders, boundary, schedule, nameplate, readable, decomposition, degradation, module, side-by-side

## 1 file names (REVIEW 1)
- **REVIEW** `vsipd_acct_7731-0459_daily_legacy_2015-2020.txt`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data

## 2 author vocabulary (REVIEW 1)
- **REVIEW** `vsipd_lgia_hadley_ranch_exhibit_c_metering.pdf`: \bdesign note\b|\bgenerator\b x1, a field term declared in metadata.json: ...LGIA Hadley Ranch Solar | Exhibit C (Amendment No. 2) Page 1 Large Generator Interconnection Agreement between Vado Seco Irrigation and Power Dist...

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `vsipd_acct_7731-0459_daily_legacy_2015-2020.txt`: golden figure 534 appears: ...310459 0418 12S0418C DEL 20160429 0000 534.1 A 77310459 0417 69R0417A REC 20160430 0000...
- **REVIEW** `marden-vail_energy_risk_policy_rev4.pdf`: carries 10 of 12 distinctive words of the committed call: "Sell 70,000 MWh of Hadley Ranch Solar's 2027 output forward: the one-year P90 of the plant with its new modules, rounded"

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `corvane_fa-2026-114_hadley_ranch_side_by_side.pdf`: 8 of 25 stump-paragraph terms appear (period, replacement, report, measured, irradiation, nameplate); read whether the document names the move
- **REVIEW** `hadley_ranch_module_replacement_scope_2026-07.docx`: 7 of 25 stump-paragraph terms appear (inverters, replacement, original, report, schedule, module); read whether the document names the move
- **REVIEW** `tresco_om_agreement_2021_schedules_2_and_4.pdf`: 6 of 25 stump-paragraph terms appear (inverters, washes, report, measured, schedule, module); read whether the document names the move
- **REVIEW** `tresco_repowering_program_2019-2026.pdf`: 3 of 25 stump-paragraph terms appear (inverters, original, module); read whether the document names the move

## 8 column names (REVIEW 3)
- **REVIEW** `hadley_scada_daily_2020-03-03_to_2026-09-30.csv`: columns a generator names and an organisation does not: device
- **REVIEW** `inverter_event_log_2025.csv`: columns a generator names and an organisation does not: device
- **REVIEW** `inverter_hourly_ac_2025.csv`: columns a generator names and an organisation does not: device

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: second-sentence opener 'put' at 39% of 196 prompts (cap 20%); reword at the role level, not the verb

## 12 describing content (REVIEW 1)
- **REVIEW** `westmark_confirmations_hadley_ranch_cy2016-cy2026.pdf`: names 5 column(s) of the data files verbatim (Date, Delivery, Product, Trade date, Westmark Power Trading LLC): confirm it is the organisation's own record and not a note written for the analyst

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 9 dates after the setting (clean)


## Solver's-eye read

Re-check of 2026-11-01, one isolated reader (Sonnet, medium) on the prompt and the 22-file pack without the README, before the C.3.1 wording fix.

- Q1 (decisive step named): none. Nearest, policy 4.2 and 4.4, the filed estimand and base period; neither says how the new modules are modelled.
- Q2 (ranking or answer file): none.
- Q3 (file existing only to help the analyst): none; the crosswalk, the service points and the Clearfield header read as the systems' own.
- Q4 (figure reading as the answer): none.
- Q5 (literal sentences): policy 3.1, 4.1 to 4.4, 5.2; O&M 4.1 to 4.3; LGIA C.1.1 and C.2.2. Executed, they give the estimand, the asks' definitions and the delivery point, not the volume.
- Q6 (what decides): an analytical choice (how the plant as it will stand in 2027 is built from its own record); nothing planted or announced.
- Realism: reads as real documents; the repowering table and the Corvane DC table slightly neat (kept: the distractor and the test's own table).
- Ask conventions: S-020 owner stops, F-217 against the district's report, the UTC and MST alignment, the legacy and meter data overlap and the versions are the asks' designed devices, each settled by its referee (ask sheet). One real finding: C.3.1's new sentence ("recorded against the end of that day") read literally would also shift the meter data system's day labels; fixed, C.3.1 now says the legacy billing system records a day's total at 0000 of the next date and the meter data system against the day itself.
- Sweep lines: (a) legacy .txt, harmless, the district's fixed-width record; (b) confirmations' fields, harmless, the counterparty's own record; (c) `device`, harmless, the systems' column; (d) "generator", harmless, the agreement's name.

Targeted re-read of the narrowed C.3.1 (Sonnet, medium, Exhibit C and the two district files only): no decisive-step sentence; C.3.1 states a fact and no method and reads as a metering clause; read literally, the legacy row stamped 20200101 0000 counts on December 31, 2019 and the meter data system's 2020-03-01 on March 1, with no second reading; minor tells only (C.2.1's "have been supplied" slightly narrative), kept.

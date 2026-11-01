# leak check, task161

**Verdict: LEAK.** 18 files read, 22 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: earlier, account, excess, rushes, shipments, forecast, accounts, december, policy, season, positions, seasonal, method, months, asserted, normal, decision, notices, decisive, domain, forecasting, balance, bought-ahead, bought, tracker

## 1 file names (LEAK 3, REVIEW 1)
- **LEAK** `avila_delivery_manifest_2024-03_2026-12.xlsx`: a file whose name says it describes the data (manifest): no dictionary, field notes, readme or manifest ships (dataset-generation section 3)
- **LEAK** `export_manifest.csv`: a file whose name says it describes the data (manifest): no dictionary, field notes, readme or manifest ships (dataset-generation section 3)
- **LEAK** `wms_export_dictionary_v3.pdf`: a file whose name says it describes the data (dictionary): no dictionary, field notes, readme or manifest ships (dataset-generation section 3)
- **REVIEW** `wms1_inv_daily_20190401-20220930.txt`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `ridley-ames_bldg-b_overflow_blocks_2026-11-19.pdf`: carries 10 of 11 distinctive words of the committed call: 'We should take 2 of the six 4,000-position overflow blocks at Tamarind Avenue Logistics Park for January to June 2027, $'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `ridley-ames_bldg-b_overflow_blocks_2026-11-19.pdf`: 3 of 25 stump-paragraph terms appear (account, accounts, positions); read whether the document names the move
- **REVIEW** `space_planning_policy_rev4.pdf`: 8 of 25 stump-paragraph terms appear (account, shipments, forecast, accounts, policy, positions); read whether the document names the move
- **REVIEW** `yv_client_advisories_2019-2026.pdf`: 3 of 25 stump-paragraph terms appear (earlier, shipments, months); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 11 prompt gate (REVIEW 2)
- **REVIEW** `prompt.txt`: no data count disclosed: each of the N: "How many of the six"; the N things: "our four buildings"; the N things: "the two ports"; the N things: "the two ports" (a count the data hold is the model's to find; drop it or keep only the decision parameter)
- **REVIEW** `prompt.txt`: shell quota: second-sentence opener 'put' at 36% of 196 prompts (cap 20%); rounding opener 'give' at 46% of 196 prompts (cap 20%); reword at the role level, not the verb

## 12 describing content (LEAK 1)
- **LEAK** `wms_export_dictionary_v3.pdf`: names 20 column(s) of the data files verbatim, 100% of wms_inbound_receipts_20220912_20261206.csv: a document that lists the data's columns describes the data whatever its name (dataset-generation section 3); the WHAT belongs in a governing document in the organisation's own genre, which names observables and never the files' fields

## 13 task metadata (REVIEW 2)
- **REVIEW** `metadata.json`: subdomain shares the design note's stump vocabulary (earlier, account, rushes, shipments, forecast): say what the task decides, not how
- **REVIEW** `metadata.json`: prompt_shape shares the design note's stump vocabulary (forecast, policy, positions, months): say what the task decides, not how

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

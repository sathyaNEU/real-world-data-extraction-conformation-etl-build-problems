# leak check, task130

**Verdict: REVIEW.** 17 files read, 15 golden figures and 8 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: window, rejected, golden, record, register, decisive, average, claims-made, asserted, severity, experience, carries, sentence, report, inside, exposure, construction, device, nothing, standard, holders, returns, household, restored, truncation

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `CPLT_funding_policy_adopted_2026-09-22.pdf`: carries 4 of 5 distinctive words of the committed call: 'Corvane Health should put $1,250,000 into its professional liability trust for 2027.'
- **REVIEW** `CPLT_trust_agreement_executed_2026-08-14.pdf`: carries 5 of 5 distinctive words of the committed call: 'Corvane Health should put $1,250,000 into its professional liability trust for 2027.'
- **REVIEW** `data_dictionary_rm_extracts.md`: carries 4 of 5 distinctive words of the committed call: 'Corvane Health should put $1,250,000 into its professional liability trust for 2027.'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `CPLT_funding_policy_adopted_2026-09-22.pdf`: 6 of 25 stump-paragraph terms appear (record, register, experience, carries, report, exposure); read whether the document names the move
- **REVIEW** `data_dictionary_rm_extracts.md`: 3 of 25 stump-paragraph terms appear (register, carries, report); read whether the document names the move

## 6 ranking artifacts (REVIEW 6, INFO 1)
- **REVIEW** `CPLT_trust_agreement_executed_2026-08-14.pdf`: names 6 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `QMPL_loss_run_Corvane_val_2026-06-30_rev1.xlsx`: names 4 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `QMPL_loss_run_Corvane_val_2026-09-30.xlsx`: names 4 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `clinician_staffing_plan_2027.xlsx`: names 5 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `cost_centre_directory_2026.csv`: names 4 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `insurance_premium_history_2016-2026.xlsx`: names 7 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `data_dictionary_rm_extracts.md`: names 7 of 8 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `insurance_premium_history_2016-2026.xlsx`: 4 ISO dates after 2026-10-12, e.g. 2027-01-01, 2027-04-01, 2027-07-01, 2027-10-01

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)
## Solver's-eye read (round 3a, hardened asks)

Read on the cut with target.zip sha256 410a3ff6b4593066 (17 files), the same pack leak.py swept above. Q1 to Q4: none;
no sentence or file names the decisive step, no file ranks the entities or states a 2027 contribution, a cost, a lag
table or a severity curve, no file is there only to help the analyst, and no figure or name reads as the answer. Q6: an
analytical choice (how the window's Claims are costed against the experience), not a field reading, a stated rule or a
plant. REVIEW lines: every one harmless (the agreement, the funding policy and the dictionary carry the call's words
because they name Corvane Health and the trust and state no contribution; the stump-paragraph nouns in the policy and
the dictionary are each document's own terms for the register, the exposure and the month a payout carries; the
schedules, loss runs, staffing plan, cost centre directory and premium history name the entities beside dates, policy
numbers, codes, amounts, FTE and premiums and rank none on the contribution; the 2027 dates in the premium history are
the 2026 policy terms' end dates). Funding policy 3.6 restating the prompt's rounding: harmless, a rounding convention
names no method. Ask readings it raised, each governed by the shipped files as the round 3a judge confirmed on the same
cut: the "latest" loss run is the latest valuation (the 30 September 2026 run, the 30 June rev1 a distractor); the
claim-key join (the insured reference through the notices and prior_claim_no, the no-reference suits by entity, date
and type); OPEN or REOPENED counted per Claim; paid FTE as hours/173.33 (the dictionary's hours paid on the line at
173.33 hours to 1.0 FTE).

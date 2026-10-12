# leak check, task130

**Verdict: REVIEW.** 16 files read, 31 golden figures and 10 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: window, rejected, decisive, exposure, experience, register, centre, golden, sentence, agreement, reader, asserted, system, report, incident, forecasting, claims-made, escalations, repeat, domain, inside, opening, pattern, family, payroll

## 3 answer figures in the pack (REVIEW 5)
- **REVIEW** `CPLT_trust_agreement_executed_2026-08-14.pdf`: golden figure 1.4 appears: ...ystem's Risk Management and Insurance department. 1.4 Medical Incident means an act or omission in th...
- **REVIEW** `CPLT_trust_agreement_executed_2026-08-14.pdf`: golden figure 2.3 appears: ...olicy. The Trust provides no prior acts coverage. 2.3 The Trust's limits are $2,000,000 each Claim an...
- **REVIEW** `CPLT_funding_policy_adopted_2026-09-22.pdf`: carries 4 of 5 distinctive words of the committed call: 'Corvane Health should put $784,000 into its professional liability trust for 2027.'
- **REVIEW** `CPLT_trust_agreement_executed_2026-08-14.pdf`: carries 5 of 5 distinctive words of the committed call: 'Corvane Health should put $784,000 into its professional liability trust for 2027.'
- **REVIEW** `data_dictionary_rm_extracts.md`: carries 4 of 5 distinctive words of the committed call: 'Corvane Health should put $784,000 into its professional liability trust for 2027.'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `CPLT_funding_policy_adopted_2026-09-22.pdf`: 8 of 25 stump-paragraph terms appear (exposure, experience, register, agreement, system, report); read whether the document names the move
- **REVIEW** `CPLT_trust_agreement_executed_2026-08-14.pdf`: 6 of 25 stump-paragraph terms appear (register, agreement, system, report, incident, family); read whether the document names the move
- **REVIEW** `data_dictionary_rm_extracts.md`: 6 of 25 stump-paragraph terms appear (register, centre, system, report, incident, payroll); read whether the document names the move

## 6 ranking artifacts (REVIEW 6, INFO 1)
- **REVIEW** `CPLT_trust_agreement_executed_2026-08-14.pdf`: names 8 of 10 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `QMPL_loss_run_Corvane_val_2026-06-30_rev1.xlsx`: names 3 of 10 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `QMPL_loss_run_Corvane_val_2026-09-30.xlsx`: names 3 of 10 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `clinician_staffing_plan_2027.xlsx`: names 9 of 10 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `cost_centre_directory_2026.csv`: names 5 of 10 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `insurance_premium_history_2017-2026.xlsx`: names 5 of 10 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `data_dictionary_rm_extracts.md`: names 5 of 10 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `insurance_premium_history_2017-2026.xlsx`: 4 ISO dates after 2026-10-12, e.g. 2027-01-01, 2027-04-01, 2027-07-01, 2027-10-01

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Q1 to Q4: none (funding policy 3.2 and 3.4 and trust agreement 1.3 read as the estimand's definition; the premium history may pull toward a premium basis but states no contribution). Q5, MAIN-CALL FINDING: the reader executed funding policy 3.1 to 3.4 literally (trended cost per covered FTE-year by class from the 2017 to 2024 experience, taken as a whole, times 2027 plan FTE-years from each Transition Date) and got about $4.85M, the default path's figure, not the golden $784,000. If the filed method's literal execution is the default, the policy is a filed basis giving the wrong answer: a Gate C/D fork and an official decoy under the three rules. Readings raised: chained claim numbers (prior_claim_no) summed or de-duplicated; what counts as covered; FTE pay codes (REG, PTO, CALL, ADMIN, LOA) and home_entity against the cost-centre mapping for ask B; "open" against OPEN plus REOPENED and which loss run is "latest" (the 06/30 rev1 has a later run date) for ask A. REVIEW lines: all harmless.

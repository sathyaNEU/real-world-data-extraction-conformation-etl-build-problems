# leak check, task264

**Verdict: REVIEW.** 14 files read, 11 golden figures and 10 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: dropped, change, window, architecture, operation, patient, decisive, case-mix, method, extract, answerers, spells, hospital, asserted, expected, admission, emergency, reader, golden, section, population, questionnaires, readmission, nothing, shared

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `spinal_contracting_policy_2027-28.pdf`: 9 of 25 stump-paragraph terms appear (change, operation, patient, case-mix, method, hospital); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: 'Send spinal_volume_2027-28.csv with a row for each provider giving its outcome under the policy and the operations placed with it, plus a row for any volume held back, and spinal_volume_board_paper.docx making the recomm'
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: 'Outcomes are in whole points, shares and participation in whole per cent, and patients and operations as whole numbers.'

## 6 ranking artifacts (REVIEW 1, INFO 2)
- **REVIEW** `spinal_capacity_returns_2027-28.xlsx`: names 10 of 10 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `cqc_locations_2026-09.json`: names 10 of 10 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `provider_reference_2026-09.csv`: names 10 of 10 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read (the isolated leak reader, two rounds)

Every REVIEW line above is ruled harmless by the reader in each round; neither round found a ranking file, a helper file or a figure that reads as the answer.

### Leak reader, round 1 (2026-11-01, isolated, Sonnet at medium effort, on target.zip d990a19c)

1. Decisive step: none stated; the nearest is policy 3's "over every eligible index operation the provider carried out from 1 April 2023 to 31 March 2025, whether or not the patient returned the 12-month questionnaire", the estimand's population, not a hint.
2. Nothing ranks or scores the providers (the capacity returns list offers; policy 4 gives the 14.5 line and the placing order, no outcomes).
3. Ordinary reference files only (OPCS code lookup, provider reference with predecessors).
4. Nothing reads as the answer (1,250 and 14.5 are policy parameters; capacity totals are offers).
5. Policy 3 (all-provider mean expected change plus the provider's mean of observed minus expected change over its eligible operations, Appendix B coefficients; every eligible operation counts whether or not the questionnaire came back) and 4 (descending order of outcome, each up to its offer, the rest held back).
6. The reader's answer: "mostly following stated rules and procedure ... The only analytical element is that the 3 population includes patients with no 12-month questionnaire, and 3 says so explicitly ... a rule-application risk (rule 3) more than an analytical-choice stump."
Sweep flags: all harmless (the policy files the WHAT; the prompt names deliverables only; the capacity returns rank nothing).
Realism: none strong; capacity totals all round multiples of 10 with smooth quarterly splits (plausible for a commissioner return, slightly tidy).

### Leak reader, round 2 (2026-11-01, isolated, Sonnet at medium effort, on target.zip 44c981bc)

1. Decisive step: policy 3's population ("over every eligible index operation ... whether or not the patient returned the 12-month questionnaire") and 4's placement rule; neither flagged as a trap.
2. Nothing ranks or scores the providers (the returns list offers only).
3. No helper file (plain code lookups, a provider code history).
4. Nothing reads as the answer (14.5 and 1,250 are policy inputs; no row says which providers qualify).
5. Policy 3 with Appendix B: every eligible operation stays in the population, including those with no 12-month questionnaire; the sentence does not say what value such an operation takes for its observed change.
6. A mix: handling the missing 12-month outcome is an analytical choice no sentence fixes; the case-mix formula and the placement rule are rule application; field readings (the NHS-number link, the provider code change, the triage clock) are needed but do not decide; nothing planted.
Sweep flags: the policy harmless on vocabulary (it names the population and formula, not the missing-outcome handling; borderline on question 6, not a clear leak); the capacity returns harmless (offers by quarter, no ranking).
Realism: none (system-export features throughout); the capacity quarters vary irregularly, acceptable.


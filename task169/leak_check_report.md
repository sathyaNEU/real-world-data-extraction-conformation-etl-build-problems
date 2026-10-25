# leak check, task169

**Verdict: REVIEW.** 16 files read, 28 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: arrests, courts, conversion, record, sentence, asserted, golden, revoked, return, methodology, decisive, cohort, admission, custody, family, window, records, prompt, default, discharged, nothing, method, extract, closed, parolees

## 3 answer figures in the pack (REVIEW 5)
- **REVIEW** `aoc_case_dispositions_2019-2026.csv`: golden figure 19,163 appears: ...way County,M2,2022-11-06,GP,2022-12-19,CJ,2022-12-19,163,2022-12-20 CR-COR-2022-00849,T40130985,Corliss Co...
- **REVIEW** `aoc_case_dispositions_2019-2026.csv`: golden figure 17,928 appears: ...ss County,FA,2025-01-26,GP,2025-04-17,DOC,2025-04-17,928,2025-04-17 CR-COR-2025-00277,T40204321,Corliss Co...
- **REVIEW** `aoc_case_dispositions_2019-2026.csv`: golden figure 21,409 appears: ...er County,FB,2023-09-07,GP,2023-12-21,DOC,2023-12-21,409,2023-12-24 CR-COR-2023-01030,T40252203,Corliss Co...
- **REVIEW** `aoc_case_dispositions_2019-2026.csv`: golden figure 10,241 appears: ...ner County,M2,2020-07-21,GP,2020-10-10,CJ,2020-10-10,241,2020-10-12 CR-COR-2020-00408,T40033303,Corliss Co...
- **REVIEW** `prison_population_projection_methodology_2026.pdf`: carries 7 of 10 distinctive words of the committed call: 'Carry a two-year return rate of 20 per cent for the 6,466 people the Department expects to release to parole in 2027.'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `act_26-114_enrolled.pdf`: 4 of 25 stump-paragraph terms appear (sentence, return, custody, parolees); read whether the document names the move
- **REVIEW** `prat_validation_study_2023.pdf`: 5 of 25 stump-paragraph terms appear (record, return, admission, custody, records); read whether the document names the move
- **REVIEW** `prison_population_projection_methodology_2026.pdf`: 12 of 25 stump-paragraph terms appear (courts, record, sentence, return, methodology, cohort); read whether the document names the move

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `doc_projected_releases_2027.csv`: 12932 ISO dates after 2026-10-14, e.g. 2027-01-01, 2027-01-02, 2027-01-03, 2027-01-04, 2027-01-05

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Determinism repair (2026-10-25), two scored readers on zip 73e3137b (`scratchpad/scored-task169e`, `scored-task169f`),
each with `score_reader.py --call-key call.rate_step`: reader E filed 10 against 20 and kept 23 of 26 ask figures
(tables 1 and 2 whole, three writ cells off); reader F filed 10 and kept 18 of 26 (tables 2 and 3 whole, table 1 off on
every cell). The call held in both.

Reader E's answers: 1. nothing named the decisive step; the Act and the methodology state the definition (a return
only on a new sentence of total confinement), which pointed it to the court sentences but not to the method. 2. the
validation study ranks release levels by return rate on all returns, not on the question, and was not used. 3. no file
exists only to help; the capacity report and the caseload file read as context. 4. nothing reads as the answer; the
study's 45 to 61 per cent all-returns figures read as a tempting wrong basis.

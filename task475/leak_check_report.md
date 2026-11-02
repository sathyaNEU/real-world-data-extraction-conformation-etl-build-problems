# leak check, task475

**Verdict: REVIEW.** 13 files read, 10 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: questions, difficulty, choice, average, answerers, member, standing, conformed, decisive, export, minutes, reader, architecture, conversion, record, comparison, examination, regulations, reviews, analyst, carries, examinee, closed, planted, shipped

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `cae_examination_regulations_2026.pdf`: carries 9 of 10 distinctive words of the committed call: 'Approve the November 2026 Paper 2 results with the optional questions moved Q1 -1, Q2 +1, Q3 0, Q4 +1, Q5 0, Q6 +3, Q7 -'
- **REVIEW** `examinations_committee_minutes_2026-06-18.docx`: carries 7 of 10 distinctive words of the committed call: 'Approve the November 2026 Paper 2 results with the optional questions moved Q1 -1, Q2 +1, Q3 0, Q4 +1, Q5 0, Q6 +3, Q7 -'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `cae_examination_regulations_2026.pdf`: 8 of 25 stump-paragraph terms appear (questions, choice, average, member, record, examination); read whether the document names the move
- **REVIEW** `cae_paper2_nov2026.pdf`: 5 of 25 stump-paragraph terms appear (questions, minutes, record, examination, carries); read whether the document names the move
- **REVIEW** `examinations_committee_minutes_2026-06-18.docx`: 8 of 25 stump-paragraph terms appear (questions, choice, member, minutes, examination, reviews); read whether the document names the move

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `corporate_accounts.csv`: 10 ISO dates after 2026-12-01, e.g. 2027-06-30

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 12 describing content (REVIEW 1)
- **REVIEW** `cae_examination_regulations_2026.pdf`: names 9 column(s) of the data files verbatim (Sydney, accredited, mark, paper, papers, questions): confirm it is the organisation's own record and not a note written for the analyst

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read (Leak reader, architecture 2 round 1 (2026-11-02, isolated, Sonnet at medium effort, on target.zip c316e563))

1. Decisive step: none stated; the nearest is regulation 14.1 (the move equals how much harder or easier the question proved than the average of the paper's optional questions, each counted once, for the candidates who sat the paper), which defines the estimand; 11.2 (the mark of record is the last mark entered) is rule context.
2. Nothing ranks November's questions; the minutes carry May's moves, a prior sitting's result.
3. Nothing exists only to help the analyst (the regulations, the paper and the minutes are governing context).
4. Nothing reads as the answer (May's moves and 433 of 698 are May values).
5. Regulations 14.1, 14.2 and 12 read literally: each optional question's difficulty against the average of the eight counted once, over the candidates who sat, rounded to a whole mark; the move applied to every answerer's mark of record, clamped to the question's range; the pass mark of 50 counted after the moves; how difficulty is measured is left to the analyst.
6. An analytical choice: how to measure how much harder a question proved when candidates chose five of eight, so each question's answerers are a self-selected group; Layer 1 reading (last mark of record, dash cells, sat against withdrawn or absent) is secondary.
Sweep flags: the regulations and minutes are harmless (no November move, pass count, step or difficulty measure; the minutes record that the Committee approved May's moves under regulation 14 with no method named or certified); the paper is question text and marks only; corporate_accounts.csv's 2027-06-30 is an ordinary two-year agreement end.
Realism: none generated; mildly tidy: the results history's rate column and the identical agreement terms in corporate_accounts.csv, both plausible.

## Solver's-eye read (Leak reader, architecture 2 round 2 (2026-11-02, isolated, Sonnet at medium effort, on target.zip 9a59084f))

1. Decisive step: none announced; the nearest is regulation 14.1, which fixes the estimand (each question's difficulty against the average optional question, compared on the same candidates whichever questions each chose) without saying that answerers self-select or naming any method.
2. Nothing ranks November's questions (the minutes carry May's moves; the history file carries accreditation rates).
3. Nothing exists only to help the analyst; distractors (invoices, corporate accounts, venue holds, centre directory, results history) read as office records.
4. Nothing reads as the answer (May's moves and 433 of 698 are May context).
5. Regulation 14.1 and 14.2 read literally: each optional question's move against the average optional question on the same candidates, rounded to a whole mark, applied to every answerer's mark of record within 0 to 20; no fit, model or formula named.
6. An analytical choice: the comparison design; mark of record, withdrawal and portal time zones are Layer 1.
Sweep flags: regulation 14.1 says only what is compared and names no executable method; the minutes certify no method and carry no November figure; corporate_accounts.csv's 2027-06-30 is a contract end date.
Realism: none generated (tidy billing amounts read as a real export).

# leak check, task464

**Verdict: REVIEW.** 14 files read, 14 golden figures and 8 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: marrick, window, patient, architecture, issues, record, decisive, repeats, cobbet, street, months, family, measured, forward, persistence, authorisation, re-authorisation, method, register, current, authorised, reading, carried, re-authorised, fennbridge

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `icb_cvd_repeat_return_2025_spec.pdf`: 5 of 25 stump-paragraph terms appear (patient, issues, months, register, carried); read whether the document names the move
- **REVIEW** `statin_continuity_sessions_brief.pdf`: 3 of 25 stump-paragraph terms appear (patient, record, register); read whether the document names the move

## 6 ranking artifacts (REVIEW 2)
- **REVIEW** `pcn_practice_profiles_2026.xlsx`: names 7 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `qof_cvd_achievement_2025-26.csv`: names 7 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question

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


## Solver's-eye read

Isolated reader (general-purpose, sonnet, medium), read 5 of 5, on the final prompt and pack (target.zip
b4b0fc88223e45b9a5097174052794cd). Reads 1 to 4 ran on earlier states of the same pack and returned the same
answers; their realism notes were acted on in the generator.

1. Decisive step stated: none. The brief's lines define the population and the outcome, not a method.
2. A file ranking the candidates on the question: none.
3. A file existing only to help: none; the product crosswalk is an ordinary join table.
4. A figure or name reading as the answer: none.
5. Literal reading: the brief's population (registered and issued a statin by the practice from 1 September to
   30 November 2026, still registered on 30 June 2027) with no statin issued from 1 March to 30 June 2027, an
   expected number rounded to 10 and compared before rounding; the specification's R1 and R2 definitions fix the
   return literally, R2 counting 90mg issues at any practice. This is the golden's reading.
6. What decides the main answer: an analytical choice, a forward expected count whose estimation method no file
   states; not a field reading, a filed procedure or a planted defect.

Prompt: names only the two deliverables, no input file and no method; presupposes nothing.

REVIEW lines: the practice profiles, harmless (list size and staffing, no statin or lapse figure); the QOF file,
harmless (a different measure and period, a declared distractor).

Realism: minor notes only (the brief's timetable and the specification's version line read a little tidy; file
names carry their date range).

### Read 6, the reshipped pack
Isolated reader (general-purpose, sonnet, medium), read 6, on the reshipped prompt and pack (target.zip
ab3f7d9afa77303ad3b4b8888f1eda6c), run because the determinism repair added a sentence to the board brief. Reads
1 to 5 ran on earlier packs.
1. Decisive step stated: none. The reader quoted the brief's selection rule ("The board will place the sessions at
   the practice with the largest expected number of patients who:"), the estimand the prompt points at, and said
   it states the rule, not a result or a method.
2. A file ranking the candidates on the question: none.
3. A file existing only to help: the reader named cvd_product_lookup.csv, a drug-name crosswalk between the two
   systems. Ruled harmless in the main thread: the network's own join table, used for every medicine on both
   systems, carries no patient or practice row and says nothing about stopping, repeats or reviews.
4. A figure or name reading as the answer: none.
5. Literal reading of the brief's new sentence: each practice's patients meeting both bullets, the figure the sum of
   each patient's own chance of no statin issued from March to June 2027, compared unrounded and reported to the
   nearest 10; it fixes the WHAT and leaves how each patient's chance is modelled open. This is the golden's
   reading.
6. What decides the main answer: an analytical choice, a forward probability per patient built from the record,
   with no field, code or stated procedure handing over the chance.
REVIEW lines: the practice profiles, harmless (list size, staffing, systems, sessions); the QOF file, harmless
(four unrelated indicators).
Realism notes, ruled in the main thread: the PDFs' dates read US Eastern to the reader, but the raw metadata is
D:20261203101500+00'00' and D:20260715143000+00'00', GMT, and the reader's tool printed them in its machine's
zone; system B's pseudonym equals the register's, which is the network's one pseudonym across systems by design
(and those files are byte-identical to the shipped pack); nothing else.

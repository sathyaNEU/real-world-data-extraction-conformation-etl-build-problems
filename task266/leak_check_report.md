# leak check, task266

**Verdict: REVIEW.** 14 files read, 19 golden figures and 8 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: student, admission, transfer, entering, sections, competing, admissions, withdrawal, extract, recorded, estimate, decisive, record, spring, college, degree, window, censored, second, asserted, endings, estimator, reason, register, survival

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `policy_3-12_program_review.pdf`: 14 of 25 stump-paragraph terms appear (student, admission, transfer, entering, sections, extract); read whether the document names the move
- **REVIEW** `registrar_extract_notes_2027-05.pdf`: 14 of 25 stump-paragraph terms appear (student, admission, transfer, sections, admissions, extract); read whether the document names the move

## 6 ranking artifacts (REVIEW 2)
- **REVIEW** `fall2026_section_schedule.xlsx`: names 4 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `program_register_2026-27.xlsx`: names 8 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `term_calendar_2018-2027.xlsx`: 4 ISO dates after 2027-05-28, e.g. 2027-05-31, 2027-06-08, 2027-08-06, 2027-08-10

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Two isolated reads (sonnet, medium), each on a fresh copy of prompt.txt and target/ only.

First read (pack before the fix pass):
1. Decisive step: none as a method; the policy gives the population and window, not the steps.
2. Ranking file: none; the register, schedule, success rates and outlook carry no completion figure.
3. Analyst-only file: the export manifest, the registrar's handoff index.
4. Answer-like figure or name: none.
5. Literal sentences: 3.3's first form ("those still enrolled included, from the student record as it stands") executed as degrees to date over all entrants, the open classes counted as non-completers.
6. What decides: read as a stated rule (the first form of 3.3), a main-call fork. Fixed: 3.3 now counts the students whose ninth term is still to come in full, their part of the share an estimate from the record of how many will have earned the degree by the end of their ninth term, the estimator unnamed; 3.2 says a degree under a readmission does not count for the class.
Realism tells fixed: the standing policy named the June 2027 review (now the second to fourth falls before any review); reason_changed_on labelled the recoded transfers (dropped); one conversion date on every map row (three load dates); the manifest's IR date and "1 pages". Ask forks fixed with filed sentences: the schedule's Cr Hrs (a linked section carries none), the registration program's vintage (when the file was extracted), linked sections as classes of their own (4.2), the video rooms' purpose; a linked BIO laboratory with no student is no longer offered.

Second read (pack after the fix pass):
1. Decisive step: none. 3.3 states the estimand (the open classes counted in full, their part an estimate made from the record) and names no method.
2. Ranking file: none.
3. Analyst-only file: the manifest; the success rates and the outlook read as files the request does not need (the declared distractors).
4. Answer-like figure or name: none.
5. Literal sentences: 3.1 the outcome (any associate degree from the college) and the nine-term window; 3.2 the IR file's entering students in their entry program, followed under the admission at entry, deaths removed; 3.3 the three classes pooled with the open students estimated; 3.4 below 30 enters review. Left open: the estimator for the students whose ninth term is still to come, and how the transfers and withdrawals enter it.
6. What decides: an analytical choice, the estimate for the students whose ninth term is still to come (censoring and survival-type estimation); nothing planted.
Realism: the outlook file read as tidy and generic (widened to 41 occupations in the final build); two exits recorded in 2023 are a death recorded 2023-09-14 and a quick second degree recorded 2023-12-27, both after the fall 2023 admissions opened, harmless. Ask notes: the lab rows' credit hours and the program of record at the census are filed in the notes (s.5 and the schedule's Cr Hrs); duplicate registrations do not occur (one row per student and section, asserted); sections meeting together beyond the video rooms do not occur (no stacked sections, asserted), so grouping by instructor, days and start time and grouping the video-room sections select the same classes; cancelled sections did not run (4.2 "ran in the fall term", the notes' "cancelled before the census").

REVIEW lines, final run (2027-05-28):
- Sweep 4, policy and notes: harmless. The shared words are the college's own vocabulary; neither document names censoring, a competing ending, a curve or an estimator.
- Sweep 6, schedule and register: harmless. Course titles and the program catalogue sit beside section numbers, CIP codes and credits; nothing ranks a program on completion.
- Sweep 9, term calendar: harmless. The four dates after the export are the published summer 2027 rows (first day, census, last day, conferral).

Third read (2026-10-18, the asks re-cut in the wave 3 audit, the call frozen; sonnet, medium, a fresh copy of prompt.txt and target/ only):
1. Decisive step: none named; the nearest is policy 3.3's "the share includes an estimate, made from that record, of how many of them will have earned the degree by the end of their ninth term", which says an estimate is needed and not how.
2. Ranking file: none; the admissions and conferral files are raw rows, the success rates score subjects, not programs.
3. Analyst-only file: none beyond the pack's own indexes (the export manifest, the notes as codebook, the term calendar, the conversion map, the IR file's About sheet, the register's Subjects sheet), each a file the college keeps.
4. Answer-like figure or name: none; the 30 per cent floor is context.
5. Literal sentences: 3.1 to 3.3 executed as the three classes pooled, the IR entrants less deaths over the degrees by the ninth term under the entry admission, the fall 2024 and 2025 classes' part an estimate of their future degrees; the estimate is the only open method.
6. What decides: an analytical choice, how to estimate eventual completion for the students still inside their ninth term; nothing planted. The reader called reporting the observed share against 3.3 a rule-application risk (that reading is R0, which 3.3 rules out) and named the conversion map, the admission at entry and the TO and WD reasons as secondary steps (Layer 1).
7. Asks: FTE, minor: the program at the census against the extract's program_code (the notes describe the file "as it stood when the file was extracted", and 4.1 asks for the program of record at the census, held in the history), and statuses dated after the census (4.3: in place on the census date). Classes: "meet together" inferred from days, times, room and instructor (no combination field); cancelled and online sections; the schedule's enrolment at export against the census registrations (the policy says census). The reader did not find the course record's credit hours on the extract or the eight-week sections' dates.
8. Realism: none.
Rulings: the policy (names the estimate requirement, not the method), the notes (field definitions; the WD to TO relabel stated as a definition), the schedule (no program mapping or ranking), the register (codes and the subject map) and the term calendar's summer 2027 rows (a forward calendar) are each harmless.

### Wave 3 audit, second pass (2026-10-18)

A data-only change (ten receiving video sections' start and end dates in the schedule), checked by leak.py alone. The
same two REVIEW lines, now with "sections" among the swept terms: policy 4.2's own definition of a class and the
notes' field list for the schedule. Neither says how sections meeting together are found or why any section's dates
differ. Harmless.

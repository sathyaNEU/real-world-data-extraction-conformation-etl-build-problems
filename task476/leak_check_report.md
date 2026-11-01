# leak check, task476

**Verdict: LEAK.** 13 files read, 27 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: surveyed, survey, guidelines, profile, december, decisive, previous, record, default, schedule, season, sentence, interval, starts, called, midpoint, elmwood, orders, convention, segment, fenwick, harlow, weighting, architecture, utility

## 1 file names (LEAK 1)
- **LEAK** `integrity_data_extract_notes.txt`: a file whose name says it describes the data (extract_notes): no dictionary, field notes, readme or manifest ships (dataset-generation section 3)

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `amr_program_guidelines_2027.pdf`: golden figure 3.30 appears: ...hane per mile of cast-iron and bare-steel main is 3.30 tonnes or more. 2.2 A district's 2026 leak methan...

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `amr_program_guidelines_2027.pdf`: 6 of 25 stump-paragraph terms appear (survey, guidelines, december, schedule, orders, segment); read whether the document names the move
- **REVIEW** `integrity_data_extract_notes.txt`: 4 of 25 stump-paragraph terms appear (survey, schedule, orders, segment); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 11 prompt gate (REVIEW 2)
- **REVIEW** `prompt.txt`: no data count disclosed: each of the N: "Which of our 12"; the N things: "our 12 districts" (a count the data hold is the model's to find; drop it or keep only the decision parameter)
- **REVIEW** `prompt.txt`: shell quota: question form 'how-many' at 30% of 196 prompts (cap 30%); rounding opener 'give' at 48% of 196 prompts (cap 20%); reword at the role level, not the verb

## 12 describing content (LEAK 1, REVIEW 1)
- **LEAK** `integrity_data_extract_notes.txt`: names 10 column(s) of the data files verbatim, 57% of leak_survey_finds_2016_2026.csv: a document that lists the data's columns describes the data whatever its name (dataset-generation section 3); the WHAT belongs in a governing document in the organisation's own genre, which names observables and never the files' fields
- **REVIEW** `amr_program_guidelines_2027.pdf`: names 4 column(s) of the data files verbatim (District, district, grade, posted): confirm it is the organisation's own record and not a note written for the analyst

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## Solver's-eye read

2026-11-01 re-check, one isolated reader (medium) on the repaired cut (extract notes out, 12 files): no sentence or
file names the decisive step; no file ranks the districts; no helper file ships; only the program line 3.30 reads as a
figure, and it is the filed rule. Question 5: guidelines 2.1 to 2.3 and 3.1 fix the comparison, population, window,
rate, local time, miles, cost and interruption units. Question 6: the reader named the surveyed leak's start as filed
nowhere, which the judge (pass 4) then ruled an open fork that is the stump. REVIEW lines (the 3.30 line, the domain
vocabulary, four column words in the guidelines, the how-many shell) ruled harmless. The sweeps above are the shipped
cut (5a46ee5a), restored after the architecture was found spent.

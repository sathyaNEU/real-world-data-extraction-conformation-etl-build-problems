# leak check, task189

**Verdict: REVIEW.** 14 files read, 11 golden figures and 7 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: method, sample, clause, asserted, average, standard, authority, decisive, programme, points, kilcrohane, laboratory, sentence, non-detects, limits, sensitive, comparison, dictionary, schedule, reading, window, estimate, estimator, censored, qualifier

## 4 design-note vocabulary (REVIEW 5)
- **REVIEW** `kilgarron_quarterly_report_2025q3.pdf`: 3 of 25 stump-paragraph terms appear (sample, authority, laboratory); read whether the document names the move
- **REVIEW** `laboratory_method_schedule.pdf`: 7 of 25 stump-paragraph terms appear (method, sample, authority, laboratory, dictionary, schedule); read whether the document names the move
- **REVIEW** `lims_field_dictionary.pdf`: 7 of 25 stump-paragraph terms appear (method, sample, authority, programme, laboratory, dictionary); read whether the document names the move
- **REVIEW** `surface_water_quality_regulations_2019.pdf`: 9 of 25 stump-paragraph terms appear (method, sample, average, standard, authority, programme); read whether the document names the move
- **REVIEW** `tirneevin_quarterly_report_2025q3.pdf`: 3 of 25 stump-paragraph terms appear (sample, authority, laboratory); read whether the document names the move

## 6 ranking artifacts (INFO 2)
- **INFO** `abstraction_point_register.csv`: names 6 of 7 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `monitoring_point_crosswalk.csv`: names 7 of 7 answer-set candidates; confirm it does not rank them on the decision question

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

Two isolated readers, each on the bundle as it then stood, seeing only `prompt.txt` and `target/`.

**Pass 1, the bundle as first cut.** Question 1: nothing quoted. "No sentence or file names the
decisive step." Question 2: no file ranks or assesses the water bodies. Question 3: nothing exists
only to help, but the method schedule's scope note was "unusually explanatory" because it said the
legacy limit "was developed for the drinking water parametric value", which "points straight at the
mismatch with the 0.05 standard" (**fixed**: the note now gives the accredited limit, the units and
the method's age). Question 4: nothing reads as the answer. Question 5: clause 7.2, and it showed that
a literal "average of results" could take the `result` field of a `<` row, which held a copy of the
limit, and reach 11 (**fixed**: a bounded row now carries an empty `result`, with the limit only in
`reporting_limit`, and the dictionary says so). Question 6: "an analytical choice: how to average MCPA
when 197 of the 225 KGL results and 77 of the 202 TAS results are censored, with the KGL limit above
the standard. The data shows this by itself, and no file states it."

**Pass 2, after those repairs.** Question 1: nothing quoted. "Nothing says how a result below the
reporting limit enters that average ... The substitution choice is left to the analyst." Question 2:
no file; the programme workbook "defines which samples count, but it does not assess anything".
Question 3: nothing, and it named both declared distractors unaided. Question 4: "the data hand over
no result." Question 5: clause 7.2 with 7.5, 4.2 and 4.4; it computed 3 at zero, 7 at half the limit
and 11 at the limit, the earlier literal-value route closed. Question 6: "a censored-data estimation
problem. It is not semantics or a stated rule. I do not see a planted defect." Asked directly about
the two laboratory documents: "Neither points the analyst at what to do with non-detects."

No third reader pass was run. The repairs after pass 2 re-rendered two PDF tables so that cells wrap
instead of clipping and added one phrase to an ask; no sentence was added to any document, and the
text the readers already saw by extraction is unchanged, so `leak.py` alone covers it.

**Mechanical sweeps.** `leak.py` returns REVIEW on six lines, each harmless. Sweep 4 flags the five
PDFs for sharing three to eight ordinary domain words with the stump paragraph (sample, method,
average, authority, standard, programme, laboratory); no document names the decisive step, which the
word sweep in `checks.py` asserts over every shipped file. Sweep 3 flags 0.005 and 0.10 in the method
schedule: those are the two accredited reporting limits, an input the pack must carry, both listed
under `stated_inputs` in `metadata.json`.

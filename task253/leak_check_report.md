# leak check, task253

**Verdict: REVIEW.** 13 files read, 26 golden figures and 4 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: standard, probabilities, averages, decisive, probability, golden, quantity, method, default, construction, points, architecture, counts, pooled, distribution, uncertainty, predicted, sentence, prediction, year-group, education, student, estimation, system, population

## 2 author vocabulary (REVIEW 1)
- **REVIEW** `LT-AS-04_analysing_school_results.pdf`: \bthe model\b x2: ...y restricted maximum likelihood. 3.3 Every school with results enters the model, whatever the size of its year groups. 3.4 Calculations for a school...

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `reading_partnership_2027_guidelines.docx`: carries 3 of 4 distinctive words of the committed call: 'Commission 42 places for the 2027 Reading Partnership.'

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `LT-AS-04_analysing_school_results.pdf`: 4 of 25 stump-paragraph terms appear (standard, counts, student, system); read whether the document names the move

## 6 ranking artifacts (REVIEW 1)
- **REVIEW** `school_register_2026.xlsx`: names 3 of 4 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Reader pass 1 on architecture 2 (one isolated Sonnet agent at medium effort, fresh copy of `prompt.txt` and `target/` from `target.zip`). Its answers, condensed, quotations kept:

1. Decisive step: "partly": `LT-AS-04_analysing_school_results.pdf` sections 3.1 to 3.5 file the random-effects model (school, year group within school, student residual), REML, every school entering whatever its size, calculations at the fitted values of the overall mean and the variance components, each test and year level modelled on its own; "nothing says shrink or empirical Bayes outright". `data_team_notes.txt` states the sitting structure and that no school opened, closed or merged.
2. Ranking or stated figure: none.
3. Help-only file: none strictly; nearest, `data_team_notes.txt` (a plausible cover note).
4. Answer-like figure: none.
5. Forks. Main call: the model variants are closed by sections 3.1 to 3.5; raw school means are a different quantity; the school count is closed by the register and the notes; one place per partner school is closed by the guidelines' section 3. Asks: 2027 Year 3 to 6 students from the August 2026 census (2026 Years 3 to 6 against Years 2 to 5 rolled forward); the hub assignment (the February 2026 directory against the 2027 visit plan, which the reader calls the natural answer); one-way distances doubled per visit, settled by the guidelines' section 4.
6. Realism tells: the notes' row counts and CC BY 4.0 line read as staged; the standard's truncated document-history row and a near-empty page 2; spelling variants in the visit plan uniform in frequency across sheets; synthetic-sounding localities and many repeated saint names; a full 264 x 5 distance matrix; one vehicle allowance for every role.

Step 2: the standard's "the model" lines called "leak, mild" (sections 3.3 and 3.4 read as pins); the guidelines' "3 of 4 distinctive words" harmless (no figure in `document.xml`; the reader asked that the other docx parts be checked); the register harmless.

### Main thread's dispositions

- Question 1 and the "mild" call on sections 3.3 and 3.4: harmless for the stump. They are the filed general method and two convention pins (every school enters; fitted values plugged in), which the default path and the golden path apply alike; no filed sentence says how to count the schools below the line, which is the decisive step, and the reader did not name it.
- The guidelines' REVIEW line: harmless, checked in every part of the docx (`document.xml`, `customXml/item1.xml`, `docProps`, the thumbnail), the standard and the notes: no 41 or 42 anywhere; the sweep line quotes the committed call itself.
- Questions 2 to 4: nothing to fix. Main-call forks: none live.
- Ask items: the census roll-forward and the hub source are the designed devices; deferred items, none beyond the realism tells.
- Realism tells: deferred to stage 6b (with the docx's python-docx template parts, `stylesWithEffects.xml`, `customXml` and a blank thumbnail).
- Stage 6b (`leak.py` re-run on the repaired pack, `--asof 2026-11-10`): the same three REVIEW lines as pass 1, each answered above; no LEAK. The docx now carries no `customXml`, `stylesWithEffects.xml` or thumbnail part. Documents under `target/` changed (the notes, the standard's history table, the docx container), so a second reader pass is owed.

### Reader pass 2 (after the stage 6b repair changed three documents)

One isolated Sonnet agent at medium effort on a fresh copy. Question 1: the standard's sections 3.1 to 3.4 again (read by the reader as "partial pooling rather than raw school means", the filed general method and a lower rung both paths apply); no sentence names how the schools below the line are counted. Questions 2 to 4: none (the guidelines carry no 42 or 41.95; the register ranks nothing). Main-call forks: none live (school set closed by the register, the notes and 3.3; the estimator by section 3; one place per partner school by the guidelines). Ask items: the census roll-forward (called a fork unless the files imply it), the hub source (the February 2026 directory against the November 2026 plan), Week A and B closed by "visits once a fortnight", the per-school round closed by guidelines section 4. Realism: the rates sheet's round amounts, a tidy notes file, compass-prefixed locality names. Disposition: nothing to fix before the judge; the census roll-forward is left to the judge's ruling at stage 7.
- Stage 7 FIX_NOW (`leak.py --asof 2026-11-10` on the repaired pack): the same three REVIEW lines, each answered above; no LEAK. The one document changed is the notes' census entry, which now files what a census year level means (the 2026 school-year level) and that students move up one level each school year: an ask-path fact with no figure, naming no main-call step.
- Resume 2, Ask A redesign (`leak.py --asof 2026-11-10` on the rebuilt pack): the same three REVIEW lines, each answered above; no LEAK. The one document changed is the notes' census entry, which now gives the run date (4 November 2026), says year level is as the student system held it on the day of the run, and keeps the move up one level each school year: ask-path facts with no figure, naming no main-call step and no school. A third reader pass is owed (stage 4).

### Reader pass 3 (resume 2, after the Ask A redesign changed the notes' census entry and the census file)

One isolated Sonnet agent at medium effort on a fresh copy of `prompt.txt` and `target.zip`. Question 1: none stated; nearest, the prompt's definition, guidelines section 2 and LT-AS-04 sections 3.1 and 3.4 ("nothing says to use shrunk estimates instead of raw means"). Questions 2 to 4: none (no file lists schools below 480 or gives a count; no 42 anywhere). Question 5: the guidelines' sections 2 and 3 and LT-AS-04 sections 2.1 to 3.5 fix the population, the threshold, one place per partner school and the model; "they leave open how the school's underlying value is read off the model", which is the decisive step, unnamed. Asks: the shares determinate; the 2027 students "mostly settled" by the notes' move up a level, with "Year level is as the student system held it on the day of the run" read as a question about whether the 4 November levels differ from 7 August (the reader did not open the census per school); the hub source settled by the plan's date and "takes effect" wording; the round settled by guidelines section 4. Realism: the notes read as a thorough hand-over note; the directory's "Opened July 2026" remark on the new hub reads as deliberate. REVIEW lines: the standard's "the model" lines "leak (mild)", the other three harmless.

Main thread's dispositions:
- Questions 1 to 4 and question 5 on the main call: nothing to fix; the standard's lines are the filed general method both paths apply, as in passes 1 and 2, and no sentence names how the schools below the line are counted.
- The census sentence: the designed fact that keeps the ask literal. Read alone it raises the question the reader raised; the census answers it at 64 primaries whose rows run Year 1 to Year 7 with no Foundation against the register's F-6, and nowhere else. No narration added; the judge rules on it.
- The hub source and the directory's remark: B1 as designed and as judged at stage 7; the remark is what makes a February directory carrying the July hub's six pilots consistent. Kept.
- The notes' thoroughness: a data team's hand-over note listing every file it sends; kept.
- No document or prompt change follows from this pass, so no fourth read is owed.

# leak check, task480

**Verdict: REVIEW.** 14 files read, 12 golden figures and 5 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: dwelling, census, persons, method, decisive, golden, groups, family, reader, population, average, reflex, register, station, sentence, household, housing, dwellings, estimator, default, profile, readable, pooled, counties, points

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `municipal_estimates_program_statement_2026.pdf`: 7 of 25 stump-paragraph terms appear (dwelling, census, persons, population, register, counties); read whether the document names the move

## 6 ranking artifacts (REVIEW 5, INFO 1)
- **REVIEW** `births_tamarack_residents_2025-2026.csv`: names 3 of 5 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `certificates_of_occupancy_2020-01_2026-06.csv`: names 3 of 5 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `decennial_census_tamarack_municipalities_2000-2020.xlsx`: names 3 of 5 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `demolition_permits_2000-2026.csv`: names 3 of 5 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `dot_certified_local_road_miles_2026.xlsx`: names 3 of 5 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `deaths_tamarack_residents_2025-2026.csv`: names 3 of 5 answer-set candidates; confirm it does not rank them on the decision question

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

Reader: one isolated general-purpose agent (sonnet, medium) on fresh copies of `prompt.txt` and `target/`, 2026-10-31.
It read both PDFs, every sheet of the three workbooks and the headers, samples and value counts of the nine CSVs, and
computed no figure.

1. Decisive step: none. The nearest sentence is the program statement's definition of an estimate (section 2) and the
   Act's s. 84.21 (4) and (6); they define the estimand and say nothing about the method.
2. Ranking file: none. The census workbook, the Census Bureau county file, the road miles and the group quarters
   survey give 2020 and earlier counts, county totals, beds or miles.
3. Helper-only file: none. Every file reads as a record an organisation keeps; the program statement and the Act are
   governing documents.
4. Answer-like figure: none. The nearest are the 2020 counts near the line (Maple Ford, Fallon), which are 2020 counts.
5. Sentence fixing the figure: the program statement, section 2 (usual residents of the municipality's dwellings on
   1 July inside the boundaries in force, plus the survey's group quarters residents); it names the components and the
   boundary basis, not a formula. Literal result: the golden's estimand, the method left open.
6. What decides it: an analytical choice, how to carry the 2020 census base forward to 1 July 2026; nothing states the
   method and no file picks the winner. Not a field reading, a rule or a plant.

REVIEW lines (sweep 6): births, certificates of occupancy, census history, demolitions and road miles: harmless, raw
records or 2020-and-earlier counts that rank nothing on the decision question.

Realism: plausible overall. Tells named: the placeholder state code ("ST") on the vital files and "State 57" in the
census names (removed: the vital files carry no state column and the census names end at the county); group quarters
facilities sharing one street address (each facility now on its own street, the group homes renamed); compound street
names of one pattern (subdivision names now mix single words, two-word names and compounds); the 1980 entry dates in
the workbook zips (harmless: Office writes the same DOS epoch).

Main-thread ruling on sweep 4 (stump vocabulary, not shown to the reader): `municipal_estimates_program_statement_2026.pdf`
carries the estimand's own words (dwelling, census, persons, population, register, counties); it names no persons per
dwelling, age, block group or method. Harmless.

Second read (after the prompt changed to ask for whole counts of births and deaths, 2026-10-31): questions 1 to 4
none, 6 an analytical choice (the estimation method); question 5 read twins as open, since no sentence said whether
twins are one birth or two (fixed: the program statement's section 3 now counts each live-born child one birth). Sweep
6 lines harmless. Realism: the census history and the survey both authored by the estimates manager (the history's
author is now the Office).

Third read (after the statement changed, 2026-10-31): questions 1 to 4 none; question 5 quotes section 2 for the
estimand with the method open and section 3 for births and deaths, twins two births; question 6 an analytical choice,
how to carry the 2020 base forward, with the ask-side readings (twins, boundaries, group quarters, the residence code)
on the asks only. Sweep 6 lines harmless. Realism notes, none a leak: PDF producer fields equal to their authors, the
road-miles certification dates spread across March, a tidy survey with every form returned.

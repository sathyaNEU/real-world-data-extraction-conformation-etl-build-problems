# leak check, task271

**Verdict: REVIEW.** 15 files read, 12 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: tested, relatives, relative, carriers, carrier, families, records, health, population, hospital, kin-cohort, points, decisive, selection, untested, probands, percent, likelihood, kaplan-meier, design, recorded, member, person, architecture, carries

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `contents.txt`: 4 of 25 stump-paragraph terms appear (carriers, carrier, health, hospital); read whether the document names the move
- **REVIEW** `family_outreach_program_criteria_2027.pdf`: 13 of 25 stump-paragraph terms appear (relatives, relative, carrier, families, records, health); read whether the document names the move
- **REVIEW** `icrs_registry_data_guide.pdf`: 9 of 25 stump-paragraph terms appear (relative, carriers, carrier, families, records, health); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Isolated readers (stage 4)

- Architecture 3 (target.zip from the PAUSED build 44e0b471): two scored readers, each on fresh copies of `prompt.txt` and `target/`. Reader 2 (r271f) took criteria 2.3's measuring population, every mother, sister and daughter of the probands living or dead, ran the kin-cohort (twice the relatives' Kaplan-Meier risk by 70 less the registry's 7.5 percent) and named PALB2-PTV and PALB2-MIS; reader 1 (r271e) ran the same estimator on a year-by-year life table with a bootstrap interval on CHEK2-PTV (24.1, about 20 to 28). Each took every ask figure, 20 of 20. `score_reader.py --call-key call.qualify` FAIL on both (the call): Gate F failed, the architecture is spent and the number retires.

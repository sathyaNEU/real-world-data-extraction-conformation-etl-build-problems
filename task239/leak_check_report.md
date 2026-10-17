# leak check, task239

**Verdict: REVIEW.** 15 files read, 49 golden figures and 6 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: covariance, factor, member, members, practice, reported, withdrawn, decisive, between-team, within-team, method, levels, decomposition, pooled, default, nothing, question, analyst, golden, carries, company, beside, estimator, september, sentence

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `lfp_wi_sv03_measurement_standard_2027.pdf`: golden figure 0.75 appears: ...se teams. 4.3 An item whose team-level loading is 0.75 or more stays in the index for the next survey. A...
- **REVIEW** `DATA_DICTIONARY.md`: carries 7 of 10 distinctive words of the committed call: 'Keep ten of the twelve items, TC01 to TC10, in the Team Climate Index for the 2028 Staff Voice survey, and withdraw TC11'
- **REVIEW** `lfp_wi_sv03_measurement_standard_2027.pdf`: carries 8 of 10 distinctive words of the committed call: 'Keep ten of the twelve items, TC01 to TC10, in the Team Climate Index for the 2028 Staff Voice survey, and withdraw TC11'

## 4 design-note vocabulary (REVIEW 5)
- **REVIEW** `DATA_DICTIONARY.md`: 4 of 25 stump-paragraph terms appear (member, question, company, september); read whether the document names the move
- **REVIEW** `README.md`: 4 of 25 stump-paragraph terms appear (method, question, analyst, september); read whether the document names the move
- **REVIEW** `lfp_staff_voice_2027_dashboard_methodology.docx`: 5 of 25 stump-paragraph terms appear (reported, method, analyst, company, september); read whether the document names the move
- **REVIEW** `lfp_staff_voice_2027_fieldwork_closeout.docx`: 4 of 25 stump-paragraph terms appear (member, question, company, september); read whether the document names the move
- **REVIEW** `lfp_wi_sv03_measurement_standard_2027.pdf`: 10 of 25 stump-paragraph terms appear (factor, member, reported, withdrawn, method, levels); read whether the document names the move

## 6 ranking artifacts (INFO 1)
- **INFO** `lfp_hr_team_register_2027-11-15.csv`: names 4 of 6 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Three isolated reads (Sonnet, medium), each on a fresh copy of `prompt.txt` and the pack only.

- Pass 1. Q1: none names the step; WI-SV-03 4.1 ("the score a member of the team is expected to give, which stays the
  same as staff come and go") read as defining the target, not the method. Q2 none (the 2026 item file gives percent
  favourable only). Q3 the README and dictionary as ordinary guides. Q4 none (0.75 is the filed line). Q5 4.2 with 4.4
  and 4.1: the population, the team as unit, standardisation across teams, the 0.75 line; how to estimate a team's
  expected score left open. Q6 an analytical choice. Every REVIEW line harmless. Realism: corporate team names such as
  "Legal Coastal 7", a stray "bureau" in the close-out, session numbers stepping in threes (all fixed in the generator).
- Pass 2 (after the judge's dictionary sentences). Q1 none; Q2 to Q4 none; Q6 an analytical choice. Every REVIEW line
  harmless. Realism: renamed and merged teams with unrelated July names, tablets set up "in the week before launch"
  against August installs, a personal link's structure left to inference (all fixed).
- Pass 3. Q1 none ("nothing says outright that a plain correlation of team means ... gives the wrong loadings"); Q2 to Q4
  none; Q5 as before; Q6 an analytical choice, section 3's rules the cleaning that feeds it. Each channel's team
  structure read off the dictionary and the tablets' log; a team that joined a division on 1 September placed in it.
  Every REVIEW line harmless. Realism (data only): most renamed teams kept their names, every tablet offline in the
  same minute, `invited` too regular (fixed with generators apart from the records'; no figure moved).

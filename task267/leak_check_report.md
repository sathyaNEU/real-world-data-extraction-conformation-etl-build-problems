# leak check, task267

**Verdict: REVIEW.** 14 files read, 46 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: program, random, sensitivity, tested, everyone, verification, protocol, reference, result, asserted, design, director, decisive, accuracy, verified, default, population, estimator, weighting, health, correction, partial, participants, signals, inverse

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `ogtt_results_2026.txt`: golden figure 120 appears: ...ION|PROGRAM_ID|COLLECTED|PSC|GLU_FASTING_MGDL|GLU_120MIN_MGDL|STATUS TL40213500|SF-0100002|03/10/2026|P...

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `screening_referral_protocol_2026-27.pdf`: 6 of 25 stump-paragraph terms appear (program, random, everyone, protocol, director, health); read whether the document names the move
- **REVIEW** `season_2026_extract_notes.pdf`: 4 of 25 stump-paragraph terms appear (program, random, result, health); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Reader (isolated, Sonnet at medium, a fresh copy of prompt.txt and target/ only), 2026-10-17:

1. Decisive step named: none. Protocol 6.2 ("counting every adult screened, whether or not they had the test") and 4.2 ("one in five of the adults it does not refer, drawn at random") state the population and the season's design as facts; the move (weighting the draw back to everyone screened) is not named.
2. A file ranking or scoring the rules: none (the candidate rules file lists logic only; the close-out counts by month and area).
3. A file existing only to help the analyst: none.
4. A figure reading as the answer: none (the close-out's new diabetes found counts the tested only, context).
5. Protocol 6.2: the population is every adult screened once (38,601), on the first screening's values, diabetes by 5.1; literal execution needs the untested adults' status estimated. No sentence fixes the computation to the easy answer.
6. An analytical choice: correcting the verification bias by weighting the draw; not planted. Lower steps (deduplication, first screening, the seven-digit match, complete tests) are cleaning.

Realism: none read as generated or planted; minor notes (the season totals, the re-sent rows the notes explain, the loaner on two tags, the notes reading as a tidy handoff, the protocol's neat decision rule) are the program's own records.

Asks: Ask A, the maker's reference gives the cartridge rule (controls take one, a run stopped at the check takes none) and the register the tags by date; the reader saw no other problem in the run database. Ask B, the reader asked which month a credit belongs to and whether "tests of adults we screened" could drop mistyped program IDs: the prompt's "the glucose tolerance tests done that month" puts each credit with the test it reverses (the credit line carries that test's service date), the invoice's service date is the OGTT's collection date for every program accession, and every OGTT row's program ID joins a screened adult once normalised (both asserted in checks.py).

REVIEW lines: `ogtt_results_2026.txt` 120, harmless (the column GLU_120MIN_MGDL, the two-hour sample). `screening_referral_protocol_2026-27.pdf`, harmless (the filed estimand and design, not the weighting). `season_2026_extract_notes.pdf`, harmless (file layouts and ID typing; no weighting named).

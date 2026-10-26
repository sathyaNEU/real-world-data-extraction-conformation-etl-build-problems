# leak check, task270

**Verdict: REVIEW.** 13 files read, 11 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: reader, readers, window, bookings, architecture, receiver, rotation, record, effect, landed, charges, golden, clinic, reading, correlation, register, recorded, sheets, patients, strong, correction, claims, primary, experiment, decisive

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `kelbray_service_specification_2024.pdf`: 5 of 25 stump-paragraph terms appear (receiver, record, charges, recorded, sheets); read whether the document names the move
- **REVIEW** `pack_contents.txt`: 3 of 25 stump-paragraph terms appear (receiver, register, sheets); read whether the document names the move
- **REVIEW** `refrigerant_strategy_2026.pdf`: 3 of 25 stump-paragraph terms appear (record, charges, register); read whether the document names the move

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


## Solver's-eye read

Architecture 7, stage 4 round 1 (2026-10-26, target.zip aec69c19d254e18c5490f12c66c33516): two isolated Sonnet readers at medium effort, each on its own fresh copy of prompt.txt and target/, briefed with the deliverable keys only (call, the four loss shares, the three asks) and scored with `score_reader.py --call-key call.name`. Both landed the call (Lancashire, shares 16, 13, 13, 11): each read Strategy 2.2's "refrigerant that escaped" as the charges netted against the change in receiver stock, fitted kilograms per level point per pack from the job sheets' arrival and departure readings and read the year's two ends from Tarnley's levels. Reader 1 kept 8 of 16 ask figures (Ask B whole, the cylinder log once per job; Ask A on the register's refrigerant), reader 2 all 16 (each pack's refrigerant from its latest job sheet). Both answered question 6 as an analytical choice. The REVIEW lines of sweep 4 were read by the main thread: the three documents describe what their rows and visits are and none names the move. Gate F failed and architecture 7 is spent.

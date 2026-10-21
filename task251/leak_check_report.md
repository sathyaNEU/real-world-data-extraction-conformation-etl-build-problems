# leak check, task251

**Verdict: REVIEW.** 11 files read, 2 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: validation, occupancy, section, reader, traffic, contractor, nothing, counted, bridges, points, queued, measured, carried, architecture, beyond, calibration, export, register, landed, pairing, queues, approaches, graded, states, approach

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `TDP-03_permanent_count_stations_rev4.pdf`: carries 6 of 8 distinctive words of the committed call: 'Flag 5 of the 30 stations in the 2027 report and send them to the spring 2028 recalibration: R03-02, R04-03, R05-01, R08'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `TDP-03_permanent_count_stations_rev4.pdf`: 8 of 25 stump-paragraph terms appear (validation, occupancy, section, traffic, contractor, counted); read whether the document names the move
- **REVIEW** `traffic_data_dictionary.md`: 9 of 25 stump-paragraph terms appear (validation, occupancy, traffic, contractor, counted, bridges); read whether the document names the move

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

Two isolated scored readers (Sonnet, medium), each on its own fresh copy of `prompt.txt` and `target/` (target.zip
555ce293), scored with `score_reader.py --call-key call.listed`.

**Reader A** (exit 1: the call landed, asks 0 of 24): R03-02, R04-03, R05-01, R08-05, R10-03. It saw that no filmed
hour exceeds about 9 per cent occupancy while the term-time peaks run 24 to 49, paired the bridge stations ("no junction
between them"), took the true flow from the far approach and fitted the counted over true factor against occupancy
(1.0 to about 24 per cent, 0.95 at 30, 0.82 at 40, 0.71 at 49). Visits from labour station-days (every cell two high),
failures from MAINS_FAIL with the repeats removed (TCX-2 failures missed).
1. None (TDP-03 section 5 gives the estimand, nothing on the congested-hour undercount). 2. None. 3. The mail is
context only; the network file lets an analyst check the pairs. 4. None. 5. TDP-03 section 5, executed with the passed
vehicles reconstructed: the five. 6. An analytical choice (the validation misses the congested hours; the undercount
calibrated against occupancy through the bridge pairs).

**Reader B** (exit 0: the call missed, asks 0 of 24): the validation list, R03-02, R14-01, R18-01; the same ask routes.
1. None. 2. None. 3. None (the dictionary at most). 4. None. 5. TDP-03 section 5 with the filmed day as the measure of
vehicles passed: the three. 6. An analytical choice (the validation day as the measure of passes), partly rule
application for the asks.

Generated-looking notes from both: the bias flat by direction and hour of day, the filmed loops identical to the hourly
export, uniform work order texts, exact repeats and 2000-01-01 stamps in the event log. Reader A also noted HLB-30
filmed before R19-01 became R19-03 though the register lists it under the new number (the register keys sites to
current numbers, as designed).

Sweep lines, both readers: harmless (the standard's own estimand vocabulary; neither document links occupancy to
counting error or bridges to station pairs).

Main thread: Gate F failed on reader A; architecture 4 is spent (design note, Tried and rejected).


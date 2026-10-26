# leak check, task137

**Verdict: REVIEW.** 13 files read, 23 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: patients, decisive, golden, architecture, window, run-out, record, turned, run-outs, deposit, practices, service, landed, default, special, january, maturity, activity, arrivals, deterrence, previous, generator, deposits, effect, in-house

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `icb_pathology_planning_assumptions_2026-27.pdf`: carries 3 of 5 distinctive words of the committed call: 'Plan for 45,000 GP-referred visits at the community phlebotomy hub in 2027-28.'
- **REVIEW** `phlebotomy_annual_report_2025-26.pdf`: carries 5 of 5 distinctive words of the committed call: 'Plan for 45,000 GP-referred visits at the community phlebotomy hub in 2027-28.'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `phlebotomy_annual_report_2025-26.pdf`: 6 of 25 stump-paragraph terms appear (patients, record, turned, practices, service, activity); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: "The files hold Hollinsfield General Hospital's walk-in clinic records from April 2023: two queue systems, reception's turned-away log, the e-roster, the kiosk's daily tickets, the practice and clinic registers and the 20"

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `bank_holidays_england.json`: 11 ISO dates after 2026-10-02, e.g. 2026-12-25, 2026-12-28, 2027-01-01, 2027-03-26, 2027-03-29

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read (stage 4, architecture 4)

Architecture 3's reads (the custody hub, on d1d38e72), which leak.py had carried across, are removed: they read another
world's pack. Each architecture 4 reader worked on its own fresh copy of `prompt.txt` and `target/`, scored by
`score_reader.py` on the emitted keys.

- Round 1, on 6611e937: the Sonnet reader filed 42,500 from seen plus turned away and kept 8 of 36 ask figures; the Opus
  reader filed 42,500 from the days the kiosk filled completed from the GP ticket-issue curve and kept 36 of 36. Both
  ask devices were re-sited (d3c6d25d).
- Round 2, on d3c6d25d: the Sonnet reader filed 42,500 and kept 0 of 36; the Opus reader landed 45,000 through ten daily
  lags of the days the kiosk filled, fitted on open days' GP-referred visits with weekday, financial year and month
  terms, and kept 8 of 36 (the sickness figures). The judge returned DETERMINISTIC with a wording FIX_NOW, applied.
- Hardened on c011ac53: the practices' in-housing now persists eight weeks after a run-out week, so ten daily lags see
  only its start (41,934 on this pack).
- Round 3, on c011ac53: the Sonnet reader filed 42,500 from seen plus turned away (39,218 grown) and kept 0 of 36; the
  Opus reader filed 42,500 from the days the kiosk filled before about 14:45 completed from the same weekday's arrival
  profile (39,441 grown), checked that turned-away patients did not come back, and kept 0 of 36. Neither found a
  sentence or file stating the move; both answered question 6 as an analytical choice on the capped seen count.

The mechanical REVIEW lines above are the ones the earlier rounds read: the call sentence's words in the board's letter
and the annual report, the report's ordinary service vocabulary, the prompt's file roll, and the bank holidays file
running past the setting into the planning year; none states a figure, a window or the move.

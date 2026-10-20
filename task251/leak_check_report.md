# leak check, task251

**Verdict: REVIEW.** 11 files read, 34 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: pairing, section, pairings, reading, calibration, confirmations, register, reader, architecture, export, factor, result, report, office, critical, service, decision, population, analyzer, monitoring, reference, neonatal, manager, confirmation, prompt

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `POCT-GLU-02_glucometri_rev3.pdf`: golden figure 400 appears: ...del glucometro inferiore a 50 mg/dL o superiore a 400 mg/dL, LO e HI compresi, è comunicato subito al m...

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: "Put the list in ritiro_glucometri_gennaio_2028.xlsx with each listed meter's ward, hospital and systematic error, together with the 2027 indicators our procedure reports: for each hospital and quarter, the share of patie"

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

Two isolated scored readers on fresh copies of target.zip dfd2d32a (stage 4, 2026-10-20).

- Reader A: landed the call (the eight meters, on the planned morning-round pairings only, the confirmations read as
  selected on the meter's own value); asks 25 of 25. score_reader exit 1. Question 1: no single sentence; it named section
  7's calibration and method clause, the laboratory note's factor and section 5's "almeno nei giorni del piano". Question 6:
  an analytical choice. Nothing quoted as the answer; no file ranks the meters.
- Reader B: missed the call (every pairing since the calibration: GX2-M707F in, GX2-K532W out, the default path); asks 25
  of 25. score_reader exit 1 on the asks. Question 6: following the stated procedure and reading the definition.
- REVIEW lines: both harmless (400 mg/dL is section 6's filed critical value; the prompt's ask sentence carries the
  deliverable's own column words). Neither reader quoted either.
- Outcome: Gate F failed on reader A's call and on both readers' asks; architecture 3 spent.


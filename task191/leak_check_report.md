# leak check, task191

**Verdict: REVIEW.** 10 files read, 11 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: undecided, decided, outcome, thread, decisive, business, investigation, conversion, export, default, prompt, decision, window, november, raised, nothing, xb-hrj, asserted, replacement, architecture, generator, financial, platform, triage, stamps

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `aml_alert_handling_procedure_2026.pdf`: 6 of 25 stump-paragraph terms appear (business, investigation, decision, raised, financial, triage); read whether the document names the move

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

## REVIEW lines, ruled in the build thread

- `aml_alert_handling_procedure_2026.pdf` carries six words of the stump paragraph (business, investigation, decision,
  raised, financial, triage): they are the procedure's own vocabulary for runs, triage, investigations and the SAR
  decision. It names no scenario, quotes no figure, and says nothing about how long an open alert has been open or
  what open alerts become. Harmless.

## Isolated leak reader

Pending: the reader is spawned from the main thread at stage 4 (a fork cannot spawn it), on the copy at
`scratchpad/leak-task191/` with the brief `scratchpad/task191_stage4_leak_brief.md`. Its verdict replaces this line.

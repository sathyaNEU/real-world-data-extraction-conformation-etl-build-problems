# leak check, task190

**Verdict: REVIEW.** 18 files read, 25 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: tested, sample, interval, decisive, projection, amount, carries, tainting, nothing, stratum, shipped, decision, stands, quantity, estimator, sentence, projects, sampled, inclusion, payment, stated, asserts, probability, arithmetic, follows

## 3 answer figures in the pack (REVIEW 4)
- **REVIEW** `audit_plan_2026.pdf`: golden figure 4.3 appears: ...ulation is tested to a confidence of 95 per cent. 4.3 Conclusion on a tested population A population is...
- **REVIEW** `audit_plan_2026.pdf`: carries 14 of 14 distinctive words of the committed call: 'The misstatement in the capital programme payments population for the year to 31 December 2026 is 850,000 euro, and the '
- **REVIEW** `internal_audit_testing_schedule_2026.pdf`: carries 10 of 14 distinctive words of the committed call: 'The misstatement in the capital programme payments population for the year to 31 December 2026 is 850,000 euro, and the '
- **REVIEW** `provenance.md`: carries 9 of 14 distinctive words of the committed call: 'The misstatement in the capital programme payments population for the year to 31 December 2026 is 850,000 euro, and the '

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `audit_manual_part9.pdf`: 9 of 25 stump-paragraph terms appear (tested, sample, interval, amount, carries, tainting); read whether the document names the move
- **REVIEW** `internal_audit_testing_schedule_2026.pdf`: 7 of 25 stump-paragraph terms appear (tested, interval, amount, nothing, quantity, payment); read whether the document names the move

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `capital_programme_register.csv`: 9 ISO dates after 2027-02-26, e.g. 2027-05-31, 2027-08-31, 2027-11-30, 2027-12-17, 2028-02-29

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read

The isolated reader saw `prompt.txt` and the bundle only, and never the design note, the generator or
the committed answer. Its substance is below with the author's verdict beside each finding.

**What it filed.** A projected misstatement of 1,700,000 and a refer, with the refer itself held at 88 per
cent confidence and the figure at about 70. It reached the figure by taking the selection interval as
tolerable misstatement over the reliability factor at nil overstatements, 1,160,000 over 3.0, which is
386,667, and it said in terms that it brought the factor and the formula from its own knowledge of the
field because no file gave them. It also said the data did not separate the candidate estimators and
called the figure under-determined without the interval. It read the selection pattern as a certainty
stratum beginning at about 100,000 rather than at the interval, because every line from 108,945 up was
tested while the rate fell to about a third between 60,000 and 100,000.

**The three findings that were the build's rather than the reader's, and what was done.**

1. **The interval was not in the bundle and the decision rested on it.** Fixed, and it is the largest
   change in this pass: the sampling design is now filed on the working paper as a fact about the sample,
   naming the interval, that it was common to every work programme, and which lines were certain of
   selection. The estimator is still nowhere filed, which is the decisive step.
2. **The reliability factor was not in the bundle and basic precision decides the call.** Fixed: the audit
   manual ships the factors at 95 per cent for nil to twenty overstatements, and `checks.py` asserts that
   the incremental allowance, the upper limit and basic precision all recompute from the shipped table
   exactly.
3. **The certainty lines were identifiable by their cents.** Fixed: every contractor certificate now
   carries cents like every other line, and about one sundry line in nine is invoiced at a round euro or
   half euro across every size band, so no surface feature of an amount marks the lines certain of
   selection.

**The realism list, file by file, with the verdict.**

| The reader's finding | Verdict |
|---|---|
| One finding phrase on all ten exceptions, no underpayments, no reviewer notes | Fixed: eight exception wordings and three clean wordings, assigned on the line's own reference, several of them something other than a rate error |
| `field_dictionary.csv` states the reversal, duplicate-delivery and superseded-row rules outright | Fixed: the column descriptions stay, the handling is cut. The dictionary now says what `reverses_line_ref`, `delivery_sequence` and `event_status` hold, not how to pair, which delivery to keep or which row supersedes which |
| The dictionary called the schedule's prefix the ledger's supplier number when it is the master's | Fixed: the description now says the supplier master's number, which is what the data carries |
| Programme line counts are round multiples of fifty | Fixed: 3,083 / 2,671 / 3,542 / 2,987 / 1,764 / 3,361 / 3,438 / 2,713 / 3,094 |
| Programme totals equal the register's thousands | Fixed: the register now carries the board's approved budget, a figure set when the programme was approved, which does not equal the year's spend and is not derivable from it |
| All nine programmes start 2024-04-01 and complete 2028-03-31 | Fixed: nine start dates across 2023-11 to 2025-04 and nine completions across 2027-05 to 2029-01 |
| Lines at or above 180,726 are all whole euro while the rest have cents | Fixed, and it was the most serious item in the report: see 3 above |
| The cents distribution is flat across a hundred endings | Fixed: a minority of lines are invoiced at a round euro, a half euro or a round five euro, as fee notes, retentions and standing charges are |
| `ledger_sequence` steps by exactly one in 26,645 of 26,647 steps | Open: a capital-only extract from a ledger that also posts revenue and payroll would carry gaps. Not yet done |
| Exactly 104 runs, 26 a quarter, 52 Tuesdays and 52 Fridays, lines per run 222 to 304 | Open: holidays, a missed run or two and a wider spread. Held deliberately until the runs-per-quarter and past-the-cut-off conventions are pinned in the asking sentence, because moving the calendar moves the figures those pins govern |
| Eleven superseded rows in tidy pairs, same effective date, load lag uniform at one to six days, label switch exactly on 1 October | Open: the asymmetry and the spread of the relabelling. This is the A2 ask's own data and moves with the ask rework |
| Crosswalk steps in near-constant strides and supplier names follow a town plus trade plus Limited pattern | Open |
| The grant claim and the revenue summary read as random draws inside a band | Open |
| The manual jumps 9.1, 9.2, 9.4, 9.7 | Harmless, and the reader said so itself: the pack ships an extract of the part, and a numbered extract with gaps is what an extract looks like. Now 9.1, 9.2, 9.3, 9.4, 9.5, 9.7 |
| `provenance.md`, `export_manifest.csv` and `field_dictionary.csv` exist only to help the analyst | Harmless: a one-off extract cut for an auditor ships a manifest and a data dictionary, and all three are descriptive. The handling that did help the analyst is cut, above |
| No file ranks or scores the programmes on the decision question | Confirmed, which is Gate G |

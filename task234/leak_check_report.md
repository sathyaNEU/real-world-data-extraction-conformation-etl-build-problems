# leak check, task234

**Verdict: REVIEW.** 11 files read, 36 golden figures and 12 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: positivity, laboratories, asserted, report, architecture, epidemic, golden, decisive, surveillance, county, testing, change, default, counts, message, monday, patients, brandmoor, linear, baseline, weekly, interface, period, messages, positives

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `DATA_DICTIONARY.md`: 9 of 25 stump-paragraph terms appear (laboratories, report, surveillance, county, change, message); read whether the document names the move
- **REVIEW** `FCP-2_feed_completeness_protocol.pdf`: 9 of 25 stump-paragraph terms appear (laboratories, report, surveillance, county, counts, monday); read whether the document names the move
- **REVIEW** `README.md`: 9 of 25 stump-paragraph terms appear (laboratories, report, surveillance, county, change, message); read whether the document names the move

## 6 ranking artifacts (INFO 1)
- **INFO** `respiratory_stream_register.xlsx`: names 10 of 12 answer-set candidates; confirm it does not rank them on the decision question

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

Architecture 2, one isolated reader (general-purpose, medium) on fresh copies of prompt.txt and target/, read before
the cancelled-order realism fix (a data-only change: the reports, documents and prompt are unchanged).

### Questions

1. None announces it. The nearest is FCP-2 s.5, "The next Monday's escalations are judged against the week's tests
   estimated in the way whose largest miss across the streams, as a share of the tests the reports counted, was
   smallest": a selection criterion that names no estimator; s.4's "The escalations are set that Monday, before the
   week's aggregate reports are due" makes the estimate necessary without naming it.
2. None. No file ranks or scores the streams on completeness.
3. None. The register, change log, result codes, README and dictionary read as the county's own records; the ED ILI,
   state positivity and admissions files read as plausible county files left unused.
4. None. The only call-adjacent number is the 80 per cent line, which is context.
5. FCP-2 s.3 (completeness) and s.4 (below 80 per cent, compared unrounded): for week 2 they execute to tests received
   by Monday 18 January 08:00 county time over the week-2 report of record; for week 3 they fix the numerator and leave
   the denominator, a report not yet due, to be estimated in the way s.5's check keeps; s.1, s.2 and s.6 fix the
   laboratory, the test and the specimen.
6. An analytical choice: estimating the missing week-3 denominators from the reports' history and choosing among the
   ways by s.5's check. The receipt clock (the broker migration, CHG-2027-0019), the facility merge, the influenza A and
   B rows and the corrections are Layer 1 mess on the numerators; the reader asked whether the clock could decide a
   stream near the line and did not run the analysis.

### REVIEW lines

- `DATA_DICTIONARY.md`: harmless; it defines the columns and the MMWR convention and names no move.
- `FCP-2_feed_completeness_protocol.pdf`: harmless; the governing document, s.5 the filed selection criterion naming no
  candidate estimator.
- `README.md`: harmless; a file list naming no move.

### Realism

- Receipt times about six hours before release from 10 to 18 January (county time before the broker migration): the
  Ask A device, with CHG-2027-0019 the migration's record.
- The distractors, the 142 resubmitted reports and the change log's unrelated IT entries read as plausible.
- Cancelled orders clustered at the start of the extract on Sunday 10 January: fixed in the generator (cancellations
  now held and lost with the results and numbered in sequence; no figure moved).
- Sheet names read as "Laboratories visible", "Streams visible": the reader's printout of the sheet state.

### Disposition (main thread)

- Q1 to Q4: nothing to fix. Q5 executes to the golden's week-2 figures and leaves week 3 to s.5, as designed. Q6
  analytical.
- The clock and week 3: no receipt in the extract is stored after 08:00 on 25 January, so under every reading of the
  receipt clock every week-3 result reached the platform before the cutoff (SF6, now asserted on all three readings);
  the call reads no receipt time.
- Cancelled orders: fixed; leak.py re-run on the rebuilt pack (REVIEW, no LEAK); goldens, figures.json and
  submission.md byte-identical.

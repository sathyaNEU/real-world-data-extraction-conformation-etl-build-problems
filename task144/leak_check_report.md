# leak check, task144

**Verdict: REVIEW.** 19 files read, 27 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: followers, readers, slidewell, tracewire, per-view, lottery, cascade, asserted, window, starrers, account, average, effect, decisive, follower, candidate, newsletter, population, measured, surface, decision, forecasting, seeded, events, snapshot

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `sluis_featuring_memo_2026-09.pdf`: carries 10 of 14 distinctive words of the committed call: 'Spotlight slidewell (pjvdlinden/slidewell) in the October 2026 issue of Sluis: it would have about 12,000 external stars'
- **REVIEW** `warehouse_extract_fields.md`: carries 10 of 14 distinctive words of the committed call: 'Spotlight slidewell (pjvdlinden/slidewell) in the October 2026 issue of Sluis: it would have about 12,000 external stars'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `sluis_featuring_memo_2026-09.pdf`: 4 of 25 stump-paragraph terms appear (lottery, account, surface, events); read whether the document names the move
- **REVIEW** `warehouse_extract_fields.md`: 7 of 25 stump-paragraph terms appear (followers, account, follower, newsletter, surface, events); read whether the document names the move

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `sluis_spotlight_lottery_2025-2026.xlsx`: 1 ISO dates after 2026-09-30, e.g. 2026-10-06

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

### Round 1: first cut, target.zip 224ba2c1

One isolated reader at medium effort read only prompt.txt and target/.
- **Q1, the decisive step:** none quoted. The memo's 2.1 to 2.4 fix the estimand and say that a forecast is needed,
  not how to make it.
- **Q2, a file ranking or scoring the candidates, or stating the asked figures:** none.
- **Q3, a file there only to help the analyst:** none. The extract contents and the field notes read as normal
  data-engineering hand-over notes.
- **Q4, a figure or name reading as the answer:** none.
- **Q5, filed sentences fixing the main figure:** the memo's 2.2, 2.3 and 2.4. They give the population and window of
  the count and leave the forecast open, so no literal figure follows. This is consistent with the golden.
- **Q6, what decides the answer:** an analytical choice, forecasting the days not yet observed and the spotlight's
  uplift from the lottery draws.

All six REVIEW lines of that cut were harmless.

Its realism tell was fixed in the generator: repository, owner and rename names had come from fixed pools. They now
come from names.py, as handles, organisations named after projects or companies, repositories named for what they do,
and renames with reasons.

The readings it raised are closed:
- A nominator seen by account and by email hash is device B1. Every signed-out nominator of the shortlist resolves to
  an account (asserted).
- Outside the organisation means membership when nominating, which equals membership now (asserted).
- The click-through's denominator is the prompt's "of them": the subscribers the issue was delivered to.
- The chart's stars by 27 September follow memo 2.2. The rollup and the events agree (asserted).
- The stars the spotlight adds are the prompt's "of those": the expected stars less the stars without the spotlight.

### Round 2: targeted re-read of the repaired cut

Q1, Q2 and Q4 were clean, Q6 analytical, and the names now read as real. Its small points were applied, and the cut
above is the result:
- Memo 5.1 now states the records kept, once, and section 4 is one line.
- Bots are named for their jobs, most without a -bot suffix; account_type is the key.
- Three readings are asserted, each giving the same call:
  - an owner of the organisation counts as a member (two such nominations);
  - no nomination of the shortlist came after the 20 September close;
  - a person nominating twice counts once.
- The ask readings are the devices, or are asserted single.

The five REVIEW lines above are answered in the design note.

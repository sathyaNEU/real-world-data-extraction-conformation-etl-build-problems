# leak check, task277

**Verdict: REVIEW.** 15 files read, 11 golden figures and 4 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: quantity, record, category, change, channel, forward, inners, article, schedule, reflex, decisive, configuration, method, silent, sentence, master, inside, inner-four, nothing, second, comparison, architecture, forecasting, probability, carried

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `venlo_siersma_closeout_2026-12.pdf`: golden figure 99.7 appears: ...31,133 99.87% 99.5% 99.68% 104 June 33,739 99.84% 99.7% 99.40% 97 July 35,226 99.84% 99.3% 99.33% 76 Aug...
- **REVIEW** `venlo_siersma_closeout_2026-12.pdf`: carries 13 of 19 distinctive words of the committed call: "No: the Venlo site will not hold Siersma's 99.80 per cent pick accuracy in February or March 2027; expect about 100 orde"

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `schedule_3_service_levels_v2.pdf`: 4 of 25 stump-paragraph terms appear (quantity, record, article, schedule); read whether the document names the move
- **REVIEW** `siersma_pcn_2026-11_daily_range.pdf`: 5 of 25 stump-paragraph terms appear (change, inners, article, configuration, master); read whether the document names the move

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `siersma_item_master_2027-01-04.xlsx`: 240 ISO dates after 2027-01-04, e.g. 2027-01-10, 2027-01-11

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

Two isolated reads (general-purpose, sonnet, medium) of fresh copies of `prompt.txt` and `target/` only; the second ran on the final cut after the realism fixes.

**Read 1 (first cut).**
1. Decisive step: none; Schedule 3.2 defines the metric, 3.6 says forecasts are built on the site's records, neither fixes a method.
2. Ranks or forecasts: none; the close-out is 2026 history, the plan is an input.
3. Helper-only file: none (no readme, dictionary or manifest); the plan's basis line ("Article mix and order sizes in each month as in the same month of 2026") is mild guidance on carrying the mix forward.
4. Reads as the answer: nothing; the close-out's history sits above target as context.
5. Filed sentences: Schedule 3.2's order line (as transmitted, however many picks, zero-confirmed lines not picked), its failure definition (short, over, wrong article; damage and labelling excluded), the Amsterdam pick date, both channels together; the prompt's claims scope. Literal results match the golden's readings.
6. What decides: mainly an analytical choice (forecasting through a structural change), with a semantic and cleaning layer around it.
Flagged items: the close-out harmless (history only, no forecast or method); the item master's 2027 dates harmless (future-effective configuration rows matching the notice).
Realism tells raised: the item master at exactly 500 rows with every Daily case contradicting the notice; flat monthly accuracy; December inventory accuracy at 100.00 per cent; old WMS users created after the cut-over. All four fixed in the generator (multinomial months, a 2.2 per cent count-difference rate, the old user list cut at the cut-over, earlier case rows and Daily cases at 24) and asserted in `checks.py`.

**Read 2 (final cut).**
1. Decisive step: none.
2. Ranks or forecasts: none.
3. Helper-only file: none.
4. Reads as the answer: nothing; the close-out's claims-received column counts all reasons and statuses, so it is not the claims answer.
5. Filed sentences: the same Schedule 3.2 readings and the plan's basis line; nothing filed on how to project February and March.
6. What decides: an analytical choice, a forecast through a structural change; the notice and item master make the change visible, which is context and not a stated method.
Flagged items: both harmless, as in read 1.
Realism tells: none requiring a fix (mixed export schemas read as a migration; the plan in tens fits an S&OP file).

**Read 3 (final cut, target.zip 2a534d35, after the judge's FIX_NOW pass and the prompt's rounding change).**
1. Decisive step: none; Schedule 3.2 and 3.6 define the metric and the record, the plan's basis line the forward volume, nothing says how to forecast failures.
2. Ranks or forecasts: none.
3. Helper-only file: none.
4. Reads as the answer: nothing; the close-out's history and the target are context.
5. Filed sentences: Schedule 3.2's population, unit, month and failure definition, and the prompt's claims scope; literal results match the golden's readings.
6. What decides: an analytical choice (turning the 2026 failure history into expected failing lines on the plan), with semantic and rule steps as supporting mess; nothing states which driver to use.
Flagged items: both harmless (the close-out is reported history; the item master's 2027 dates are future-effective configuration rows).
Realism tells: the office files' 1980 entry stamps are what Excel writes; the close-out's December note naming the agency pickers inducted is plausible narrative and points at no forecast; none requires a fix.

**Main-thread ruling.** No question-1 sentence, no helping file, every question-5 sentence executes to the golden's reading, no main-call fork. The stump-vocabulary lines are ruled in the design note's `## Leak rulings`.

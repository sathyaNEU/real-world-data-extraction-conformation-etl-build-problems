# leak check, task231

**Verdict: REVIEW.** 15 files read, 50 golden figures and 8 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: register, settled, rounds, closure, standard, non-returners, closures, decisive, trading, records, history, levels, islands, window, eligibility, earlier, extract, western, uplands, section, population, sentence, estimate, recorded, points

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `BCS_fieldwork_quality_standard_v3.pdf`: 8 of 25 stump-paragraph terms appear (register, rounds, closure, standard, trading, records); read whether the document names the move
- **REVIEW** `business_register_extract_notes.pdf`: 5 of 25 stump-paragraph terms appear (register, closure, trading, records, extract); read whether the document names the move

## 6 ranking artifacts (REVIEW 2, INFO 1)
- **REVIEW** `BCS_regional_balances_2026_06.xlsx`: names 7 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `bcs_invitations_2026_09.csv`: names 7 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `bcs_region_review_2023.csv`: names 7 of 8 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `BCS_round_calendar.xlsx`: 15 ISO dates after 2026-09-25, e.g. 2026-09-28, 2026-10-09, 2026-10-16, 2026-10-30, 2026-12-01

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read

One isolated reader (sonnet, medium) on a fresh copy of `prompt.txt` and `target/` only, 2026-10-13.

1. Decisive step: quotes standard section 4.2 ("A firm whose business ceased trading on or before the frame date is out of scope for the round, whether or not the Brevland Business Register yet records its closure.") with the register notes' "A company that has stopped trading but whose closure has not been registered does not appear."; says the denominator must be corrected beyond the register and that no method is given. Ruling: the estimand pin and the incomplete-source statement `determinism-check` section 1 requires (WHAT); the decisive step is how the unregistered closures are estimated (HOW), which no file states. Harmless.
2. Ranking file: none.
3. File only there to help: none; the register notes point at the gap "but a real register would plausibly write that note". Harmless.
4. Figure or name reading as the answer: none.
5. Literal reading of section 4.1: the population is the invited firms trading on 1 September; numerator the firms with a first return by 17:00 Brevland time on 25 September (15:00 UTC), each once; firms with no recorded status stay in the denominator unless shown ceased, while section 4.2 puts unrecorded closures out of scope, so the method for finding them is left open. Ruling: executes to the golden's estimand; the method stays open as designed.
6. What decides: an analytical choice (estimating the in-scope denominator when the register is incomplete); field readings and the time zone are Layer 1. Caution raised: a single clean signal (ceased call outcomes) could collapse it; ruling: the call records confirm a closure only when someone answers, the call-centre route is rung R2 and files four extension regions (asserted).

Review lines: the standard (harmless, the rate definition and scope rule, no method), the register notes (borderline, leaning harmless; a genuine extract limitation, no method), the June balances (harmless, opinions, no response data), the invitation list (harmless, row level), the calendar (harmless, real forward entries).

Realism tells and dispositions:
- Main closes on Christmas Day 2020 and 2026: fixed in the generator (the December close moves to 23 December when the Friday is the 24th or 25th; the post room keeps the holidays).
- Manifest entries with empty `extracted_at`, `rows` and `owner` for documents: fixed (documents carry their issue date and owner).
- A thin one-page questionnaire: fixed (the firm's details and how to return it).
- A tidy data dictionary, generic region names: harmless.

Ask readings raised: firms reached (BCB only or both teams and inbound) and calls placed (code 71 legs): closed by the outcome codes' notes (reached on either kind of call; code 71 continues the same call) and the dictionary's direction field. June late returns (time zone; denominator by the cut-off or by the close): standard section 2.4 and 4.3 fix 17:00 Brevland time and the reach time, and a share of the region's June returns counts every June return. Refreshment (Rev. 2 or Rev. 2.1 groups; which rounds count): the dictionary's crosswalk maps both to the survey's nine groups, and a recruit's returns can only be its own rounds from March 2026, the September round included. No change.

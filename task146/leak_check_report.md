# leak check, task146

**Verdict: REVIEW.** 16 files read, 29 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: quarter, refused, driver, refiling, effect, determinations, refusal, series, closing, period, regional, technical, advance, decisive, regions, checks, seasonal, statistics, asserted, official, forecasting, calendar, components, shares, months

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `ui_claims_statistics_technical_notes_2026-07.pdf`: golden figure 2.3 appears: ...already receiving benefit are not initial claims. 2.3 The monetary determination Every new claim is gi...
- **REVIEW** `ui_claims_statistics_technical_notes_2026-07.pdf`: carries 9 of 10 distinctive words of the committed call: 'The board will first report about 17,000 initial claims nationally for the claims week ended 10 October 2026.'
- **REVIEW** `ui_weekly_claims_release_2026-10-08.pdf`: carries 8 of 10 distinctive words of the committed call: 'The board will first report about 17,000 initial claims nationally for the claims week ended 10 October 2026.'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `ui_claims_statistics_technical_notes_2026-07.pdf`: 9 of 25 stump-paragraph terms appear (quarter, effect, determinations, period, technical, advance); read whether the document names the move
- **REVIEW** `ui_weekly_claims_release_2026-10-08.pdf`: 5 of 25 stump-paragraph terms appear (technical, advance, regions, seasonal, statistics); read whether the document names the move

## 9 dates after the setting (REVIEW 3)
- **REVIEW** `employer_portal_notices_export_2026-10-07.csv`: 332 ISO dates after 2026-10-08, e.g. 2026-10-09, 2026-10-10, 2026-10-11, 2026-10-12, 2026-10-13
- **REVIEW** `es_layoff_notice_register_2025-26.xlsx`: 35 ISO dates after 2026-10-08, e.g. 2026-10-12, 2026-10-14, 2026-10-15, 2026-10-28, 2026-11-01
- **REVIEW** `public_holidays_2014-2027.csv`: 13 ISO dates after 2026-10-08, e.g. 2026-10-26, 2026-12-25, 2026-12-28, 2027-01-01, 2027-01-04

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

Five isolated reads, each one agent at medium effort on fresh copies of `prompt.txt` and `target/` only. The last
leak.py run (2026-10-16, on the shipped cut) gives the eight REVIEW lines above and no LEAK; each is answered in the
design note's `## Leak review`.

**Round 1** (the stage 3 cut, commit f71f5a0, target.zip sha256 22f06ed9a9233bf7, before the rule 3 repair; the call
then 16,000):
1. Decisive-step sentence: none. Technical notes 2.1 (a claim's effective Sunday) and 2.3 (the base period) together
   point toward a quarter-start effect without naming it.
2. A file ranking or scoring the candidates, or stating the asked figures: none.
3. A file there only to help the analyst: none (the desk's data log a provenance log, harmless).
4. A figure or name reading as the answer: none.
5. Technical notes 3.1 makes the target the advance count; it prescribes no method and yields no figure.
6. An analytical choice. Every REVIEW line of that cut harmless. Its judgment call (the call well above any October
   step it saw) is the stump itself: the step is sized by the closing quarter's refusals, which the history shows. The
   rule 3 repair and the strengthening since changed the world and the notes, so that read applies to the earlier cut.

**Round 2** (the rule 3 repair's cut, commit 67e305d, target.zip sha256 a040f6c10bb1b148; the call then 16,000):
1. None. The nearest is technical notes 2.3, "A claimant found monetarily ineligible may file again in a later
   quarter, once the base period has moved.", a mechanism with no size, timing or region.
2. to 4. None.
5. Technical notes 2.1, 2.2, 3.1 and 5 fix the week, the population and the asks' bases; none gives a figure.
6. An analytical choice (modelling the refiling rather than extrapolating the trend), not field semantics, a stated
   rule or a plant. Every REVIEW line harmless (the stump-term overlap in the notes borderline, rated harmless). Its
   realism note (withdrawal phrases repeated in the case notes) was taken up in the strengthening; its reading of the
   open data's SIC version is Ask B's device.

**Round 3** (the strengthened cut the judge approved, commit 0f4de4d, target.zip sha256 f0b43f3f2b62ba5b; the call
17,000):
1. None. Technical notes 2.3 the nearest, "a hint toward the move but does not say it".
2. None.
3. The desk's data log "plausible as a desk file but reads as made for the analyst"; it became a plainer working log
   in the two later cuts.
4. None.
5. None computes a figure; the estimand is the prompt's.
6. An analytical choice (modelling the quarter-turn effect); the month of the refusal never surfaced. Every REVIEW
   line harmless. Its two-way readings are closed: the notice's region against the site's (technical notes 5, the
   site's), industry group against division (the divisions file's group column), the chart's latest week at its
   advance count (ungraded).

**Targeted re-read 1** (the case-note coherence fix's cut, commit 7137912, target.zip sha256 a502ea698f2d423a; the
case notes and the desk's data log read closely): no leak, nothing ranks or states a figure, Q6 an analytical choice.
Its realism tells in those two files (phrases recurring word for word, notes explaining the counting rules, too-clean
entries, an even workload, CN051234's scope, the data log's "experimental" tag and "after the release") were fixed in
the realism pass.

**Targeted re-read 2** (the shipped cut, commit 0a888d3, target.zip sha256
e5e9d268b7bd6c16d6a5cddd8940d004dbd9ac8645dd1ed80daf05e942720a54; the same two files read closely):
1. Decisive-step sentence: none; nothing says how to forecast the advance count.
2. None.
3. None labelled as a hint; the desk's data log a provenance log.
4. None (the 3 October advance count, 11,814, an anchor, not the answer).
5. Technical notes 3.1: the first report is the advance count of Thursday 15 October; section 5 fixes the layoff
   table's population and 2.1 the industry table's weeks; no sentence gives the number or the method.
6. An analytical choice; nothing reads as planted.

Rulings on the points it raised:
- The VR notes and the "amendment form emailed" notes do not change any count. Technical notes section 5 counts a
  change only through an amended notice, and the determinism judge reproduced all 24 Ask A cells on that reading.
- The chart's question for past weeks (revised or first reported) is ungraded and low risk.
- The technical notes' completeness is the board's own methodology document, so it is not steering.
- The remaining regularity in the case notes (a reason on most withdrawals, the whole-notice wording varied by officer,
  regular routine entries, the reference spellings) is accepted as a residual realism risk.
- Its other readings are the asks' bases, each closed by a filed sentence (the window from 11 October in the prompt;
  the site's region, amendments and withdrawals in section 5; the claims week's month in 2.1; transitional claims in
  2.2) or an ask's device. CN051251 and CN051272 record an employer emailing a copy of a notice already on the portal
  after the email register closed; it is filed as a duplicate and no count moves.

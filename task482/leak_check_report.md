# leak check, task482

**Verdict: REVIEW.** 12 files read, 44 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: regression, architecture, register, reader, dwelling, census, decisive, market, constant-quality, objective, designation, population, traded, effect, readable, commutes, readers, landed, beside, sample, location, status, default, lineage, pattern

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `bso_rppi_methodology_note_2026.pdf`: 4 of 25 stump-paragraph terms appear (register, dwelling, census, market); read whether the document names the move
- **REVIEW** `dhlgh_circular_rapid_price_growth_areas_2026.pdf`: 3 of 25 stump-paragraph terms appear (dwelling, market, designation); read whether the document names the move

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

## Solver's-eye read

Two isolated readers (general-purpose, sonnet, medium), each holding only fresh copies of prompt.txt and target/ (pack
of 2026-10-22), answered the six questions and committed their figures (scored with score_reader.py against
generator/figures.json).

Reader A: call missed (seven: AV, BM, CV, GS, KB, MR, RG, against the golden's AC, AV, CV, DM, GS, KB, MR), from
medians per area and dwelling type weighted by the census stock's type shares; changes 0 of 16, purchases 0 of 16,
paid 0 of 16 (every line of a sale counted).
1. methodology note section 1, "measures the change in the market value of the area's dwelling stock, the dwellings the
   2022 census counts there": "It points at stock weighting but does not say how."
2. none.
3. the data dictionary and the extract manifest (field descriptions).
4. none: the 8 per cent is the threshold.
5. circular section 1 and note section 1 (the window, the years taken whole, the census stock); "The main figure's
   method (stratified, stock-weighted) is not fixed to a statistic literally."
6. an analytical choice: a stock-weighted, type-mix-adjusted index rather than raw medians.
REVIEW lines: the circular harmless; the note "a mild leak of the approach; it does not give the method or a figure".

Reader B: call missed (the same seven), from a log-price regression per area with type-specific year effects, floor
area and age, the type effects weighted by the census stock's counts (no location term); changes 1 of 16 (KB 11.2),
purchases 0 of 16, paid 0 of 16 (every line of a sale counted).
1. the same sentence of the note; "no sentence states the step outright".
2. none.
3. "none really"; the dictionary and the manifest help with field reading.
4. none.
5. note section 1 with the full-market-price rule: "a stock-weighted (census type shares) price change on
   full-market-price sales, not the change in average sale price".
6. an analytical choice: a stock-weighted, mix-adjusted index against the naive average of what sold; the VAT, the
   overlap and the area mapping are cleaning.
REVIEW lines: the circular harmless; the note "leak (mild) ... it does not give a figure or the weighting method, so
borderline harmless-context".

Verdict on the REVIEW lines: harmless. The note's sentence is the filed estimand (the change in the market value of
the census stock), which determinism-check section 1 requires filed; it names no method, and both readers executing it
with their own methods landed on the same wrong seven, missing the location shift inside RG, BM, AC and DM. No
decisive-step sentence, no helping file, no main-call fork; question 6 analytical from both readers.

# leak check, task264

**Verdict: REVIEW.** 19 files read, 48 golden figures and 13 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: visits, survey, interview, weights, person, weight, contractor, people, population, sample, interviews, average, selection, design, decisive, dropped, visited, asserted, shared, probability, resident, counts, architecture, estimator, inverse

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `levy_papers_2027-28.pdf`: carries 28 of 30 distinctive words of the committed call: 'Charge the 2027-28 levy of £7,416,300 as follows: Keldmere District Council £1,252,070, Ravenwick Borough Council £1,540'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `fieldwork_and_weighting_note_2025-26.pdf`: 7 of 25 stump-paragraph terms appear (visits, survey, interview, weights, weight, interviews); read whether the document names the move
- **REVIEW** `levy_papers_2027-28.pdf`: 5 of 25 stump-paragraph terms appear (survey, weight, population, visited, resident); read whether the document names the move

## 6 ranking artifacts (REVIEW 7, INFO 3)
- **REVIEW** `car_park_asset_register.csv`: names 3 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `cash_book_receipts_2025-26.csv`: names 9 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `dvrpa_visitor_survey_2025-26_wave1.xlsx`: names 4 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `fieldwork_and_weighting_note_2025-26.pdf`: names 4 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `levy_papers_2027-28.pdf`: names 9 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `member_council_invoices_2025-26.csv`: names 9 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `population_estimates_mid-2025.xlsx`: names 9 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `car_park_tariffs_2025-26.xlsx`: names 3 of 13 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `dvrpa_settlement_gazetteer.csv`: names 9 of 13 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `survey_codebook_2025-26.xlsx`: names 13 of 13 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Three isolated readers (Sonnet, medium), each on a fresh copy of prompt.txt and target/ only.

**Reader 1 (first pack).** Q1 none: the resolution states the estimand (each resident counted once) and the field note the weights (adult visits); no file says how visits become people. Q2 none: Appendix B ranks the councils on the 2026-27 population basis the resolution replaces. Q3 export_manifest.csv reads as an index, plausible. Q4 none. Q5 the resolution's paragraphs 1, 2, 4 and 6; literal execution needs a visits-to-people conversion the text does not give. Q6 an analytical choice. Every REVIEW line harmless. Realism notes, all fixed in the generator: near-identical interview totals per park, one spelling pattern across the invented names, a remittance file with two senders, a table of weight ranges in the field note.

**Reader 2 (after the realism fixes).** Q1 none (the conversion is not announced), Q2 none, Q4 none, Q6 an analytical choice. Every REVIEW line harmless. Realism note fixed: the annual permits' single price (now three permit types). Kept as plausible: the manifest's tidy descriptions, the shared service's paired advices.

**Reader 3 (after the judge's fixes).** Q1 none, Q2 none, Q4 none, Q6 an analytical choice. Q7: the manifest says what each of the cash book's dates is (posting from the morning's statement, the bank's credit) and does not say which answers "paid by 31 March". Q8 none: no shipped sentence says a machine or counter moved or that a counter counts both ways; each is inferred from the data. Realism notes minor (tidy invoices and manifest), kept.

Third read (2026-10-18, the wave 3 audit: Q9 by park and Ask B re-cut; sonnet, medium, a fresh copy of prompt.txt and target/ only):
1. Decisive step: none named; the nearest is resolution 14/2026, paragraph 2 ("each resident counted once however many times they visited and however many of the parks they visited ... as estimated from the Authority's visitor survey"), which says what to count, not how; the note's weights are "the estimated number of adult visits".
2. Ranking file: none; Appendix B is the 2026-27 population basis and the invoices the 2025-26 instalments, references on the old basis.
3. Analyst-only file: none beyond the pack's own indexes (codebook, gazetteer, manifest, notes sheets, asset register).
4. Answer-like figure: none; the levy requirement, the 2026-27 levies and the 2,349,510 adult visits are context.
5. Literal sentences: paragraph 5 executed as the requirement times each council's distinct-resident estimate over the nine councils' total; the estimate is not fixed by any filed text, and summing the weights gives visits, not residents.
6. What decides: an analytical choice, turning weighted visits into distinct residents counted once across parks from an exit sample drawn in proportion to visit frequency, with Q9's per-park counts; nothing planted. The reader named the multi-park question itself, as an analyst would; no sentence states the method.
7. Asks: parking income, mild (UTC stamps against a local-time year, settled by the manifest's April to March parking; app income before commission); vehicles, the counter swaps and whether a counter counts in only or in and out (the devices, found in the counts); levy, which date counts as paid (the cash book's posting date or the bank's value date, each defined in the manifest) and that instalment 4's due date is the cutoff (its late part empty by construction).
8. Realism: none; the permits' valid-until dates run a year from issue.
Rulings: every REVIEW line harmless (the council names are the prompt's nouns; the note and the papers describe the data and the estimand, not the move; no file ranks the councils on the new basis; the permits' dates are twelve-month validity).

**Reader 4 (after Ask B's re-cut: the receipt's amount on each allocation line, the cash book's year by posting date).** Q1 the resolution's estimand (each resident counted once however many times and parks they visited), not the method; Q2 none; Q3 the field note, codebook, gazetteer, manifest and register as ordinary supporting files; Q4 Appendix B's population levy (the old basis, declared) and the population estimates (a distractor); Q5 the resolution and the note leave the method open; Q6 an analytical choice (weights expand visits, the resolution counts residents). Q7, the levy collection: a payment run's receipt is larger than its instalment (the cash book's second line and the invoices' amounts place the rest on a sundry invoice); the day paid (posting date or value date, each defined in the manifest; the judge reads the definitions as closing it); the fourth instalments of 31 March are in the bank's report only; non-levy bank lines are placed by the invoices' descriptions. Q8 nothing planted; the field note's detail is borderline but plausible. Every REVIEW line harmless.

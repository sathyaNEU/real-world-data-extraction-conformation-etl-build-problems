# leak check, task264

**Verdict: REVIEW.** 19 files read, 41 golden figures and 13 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: visits, survey, weights, interview, person, contractor, weight, people, population, sample, interviews, average, selection, design, decisive, dropped, visited, asserted, architecture, estimator, probability, resident, counts, inverse, weighted

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `levy_papers_2027-28.pdf`: carries 28 of 30 distinctive words of the committed call: 'Charge the 2027-28 levy of £7,416,300 as follows: Keldmere District Council £1,250,310, Ravenwick Borough Council £1,525'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `fieldwork_and_weighting_note_2025-26.pdf`: 7 of 25 stump-paragraph terms appear (visits, survey, weights, interview, weight, interviews); read whether the document names the move
- **REVIEW** `levy_papers_2027-28.pdf`: 5 of 25 stump-paragraph terms appear (survey, weight, population, visited, resident); read whether the document names the move

## 6 ranking artifacts (REVIEW 6, INFO 4)
- **REVIEW** `car_park_asset_register.csv`: names 3 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `dvrpa_visitor_survey_2025-26_wave1.xlsx`: names 4 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `fieldwork_and_weighting_note_2025-26.pdf`: names 4 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `levy_invoices_2025-26.csv`: names 9 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `levy_papers_2027-28.pdf`: names 9 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `population_estimates_mid-2025.xlsx`: names 9 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `car_park_tariffs_2025-26.xlsx`: names 3 of 13 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `dvrpa_settlement_gazetteer.csv`: names 9 of 13 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `remittance_advices_2025-26.csv`: names 4 of 13 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `survey_codebook_2025-26.xlsx`: names 13 of 13 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `annual_permits_2025-26.csv`: 39 ISO dates after 2027-01-08, e.g. 2027-01-09, 2027-01-10, 2027-01-11, 2027-01-17, 2027-01-18

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

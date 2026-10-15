# leak check, task260

**Verdict: REVIEW.** 18 files read, 10 golden figures and 11 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: examinations, random, asserted, delong, bootstrap, examination, shared, obuchowski-rockette, analysis, crossed, pooled, decisive, carries, factor, factors, export, rejected, method, populations, ratings, readings, paired, generator, two-way, condition

## 3 answer figures in the pack (REVIEW 4)
- **REVIEW** `ai_evaluation_protocol_v2.pdf`: carries 4 of 5 distinctive words of the committed call: 'License Halvic Breast for two years from 1 April 2027.'
- **REVIEW** `quote_halvic_breast_2027.pdf`: carries 4 of 5 distinctive words of the committed call: 'License Halvic Breast for two years from 1 April 2027.'
- **REVIEW** `quote_lumidra_detect_2027.pdf`: carries 3 of 5 distinctive words of the committed call: 'License Halvic Breast for two years from 1 April 2027.'
- **REVIEW** `quote_ondrix_mammo_2027.pdf`: carries 3 of 5 distinctive words of the committed call: 'License Halvic Breast for two years from 1 April 2027.'

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `ai_evaluation_protocol_v2.pdf`: 4 of 25 stump-paragraph terms appear (examinations, examination, ratings, condition); read whether the document names the move

## 6 ranking artifacts (REVIEW 4, INFO 3)
- **REVIEW** `film_reader_workforce_2026-10.xlsx`: names 4 of 11 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `mobile_unit_visits_2025-26.xlsx`: names 4 of 11 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `reader_study_case_sets_2026.xlsx`: names 3 of 11 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `screening_kpis_2023-24_to_2025-26.xlsx`: names 4 of 11 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `reader_study_panels_2026.xlsx`: names 3 of 11 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `screening_locations.json`: names 4 of 11 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `vendor_product_summaries_2026.pdf`: names 3 of 11 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `film_reader_workforce_2026-10.xlsx`: 3 ISO dates after 2026-10-15, e.g. 2027-02-01, 2027-03-31, 2027-04-01

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read (loop 0)

Isolated reader (general-purpose, Sonnet, medium) on a fresh copy of prompt.txt and target/, before the quote-layout
and workforce-registration fixes (the documents' text and every figure unchanged by them).

1. Decisive step: none named. Nearest: ai_evaluation_protocol_v2.pdf 4.1, "The gain and its interval are for the
   service's film readers reading the service's screening examinations", a population statement that "does not say
   how to build the interval".
2. Ranking on the question: none. vendor_product_summaries_2026.pdf carries the vendors' standalone AUCs (0.94, 0.92,
   0.91), "not results of the service's reader studies": a labelled lure (declared wrong-basis distractor).
3. Files only to help the analyst: none; the code table, location table and field guide are needed to read the
   records; the KPIs, self-assessment scores and product summaries read as context.
4. Answer-like figures or names: none.
5. Literal sentences: protocol 3.1, 3.2 and 4.1 fix the measure (each reader's empirical ROC area, the readers'
   average gain) and the populations; read literally they point to an interval allowing for both reader and case
   variation, the method not named; the reader did not compute a pick. The reader's added "gain for the service's
   reader mix" is closed as SF17 (protocol 3.2 files the readers' average; role weighting moves no verdict).
6. What decides: an analytical choice, how the gain's interval is built from reader and case variation; the mess
   (two export layouts, practice cases, resubmissions) is real and does not decide.

REVIEW lines: all harmless (the call's frame words in the protocol and quotes are generic procurement wording and all
three vendors quoted; the protocol states a population, not a method; the workforce, visit, case-set and KPI files
rank nothing on the decision question; the 2027 workforce dates are notified leaving and start dates).

Realism tells, disposition: the three quotes' shared template (fixed: three layouts); a GMC number on a radiographer's
row (fixed); the double contract readable as two rows (kept: the ask's device, now visible only by comparing the
registration numbers across formats); uniform visit lengths and polite venue names (kept, texture); the
self-assessment file unreferenced (kept, a declared distractor).

## Solver's-eye read (loop 1)

Isolated reader (general-purpose, Sonnet, medium) on a fresh copy of prompt.txt and target/ after the loop 0 fixes.

1. Decisive step: none announced. Nearest: ai_evaluation_protocol_v2.pdf 4.1, "The gain and its interval are for the
   service's film readers reading the service's screening examinations", read as a hint that the inference must
   reach beyond the panel and the 300 examinations; nothing says how to build the interval.
2. Ranking on the question: none. The product summaries' standalone areas (0.94, 0.92, 0.91) are labelled "not
   results of the service's reader studies"; the self-assessment file carries no tool.
3. Files only to help the analyst: none; the field guide, code table and location table are ordinary system
   artefacts needed to read the records.
4. Answer-like figures or names: none; no gain is stated anywhere.
5. Literal sentences: protocol 3.1, 3.2 and 4.1 fix the measure and the populations; the interval's method is left
   open (a paired t across readers or a case bootstrap as the easy routes, a reader-and-case method as 4.1's
   reading). The reader also raised reweighting the enriched set to the screening rate: closed as SF18 (the area
   compares cancers with normals, so a weight per class leaves it unchanged, asserted). The cost sentences are rule
   application on the asks.
6. What decides: an analytical choice, the interval built from reader and case variation; the cleaning is Layer 1.

REVIEW lines: all harmless (generic procurement wording naming no winner; the protocol names the estimand and no
method; the workforce, visit, case-set and KPI files rank nothing; the 2027 workforce dates are notified starts and
leaving dates).

Realism tells, disposition: the bank row of the double contract alone carried a blank FTE and a prefix-free
registration (fixed: every bank row now carries the bank system's conventions, and a mammographer holds a double
contract too); the three quotes shared their scope and terms sentences (fixed: each vendor's own); the
self-assessment file's uniform 60-case set (kept: a fixed self-assessment set is read by every reader); synthetic
venue names (kept, texture).

## Solver's-eye read (loop 2)

Isolated reader (general-purpose, Sonnet, medium) on a fresh copy of prompt.txt and target/ after the stage 4 fix pass
(Lumidra's episode basis and reader accounts, the location table's host at export, the bank rows, each vendor's own
scope and terms).

1. Decisive step: none announced. Nearest: ai_evaluation_protocol_v2.pdf 4.1, which "fixes the population (readers
   and examinations) but names no method"; nothing names MRMC, a bootstrap or DeLong.
2. Ranking on the question: none. The vendors' standalone areas are disclaimed ("not results of the service's
   reader studies"), the declared wrong-basis distractor.
3. Files only to help the analyst: none beyond ordinary supporting records (the export field guide, the code and
   location tables, the panel list).
4. Answer-like figures or names: none; no gain, verdict or cost is stated anywhere.
5. Literal sentences: protocol 3.1, 3.2 and 4.1 fix the measure and the populations; the interval's method is not
   named; the reader could not say which tool is picked or whether any qualifies. The quotes' cost and count
   sentences read as rule application on the asks.
6. What decides: an analytical choice, how the gain's uncertainty is estimated with readers and cases both sampled.

REVIEW lines: all harmless (the protocol's 1.2 decision frame and the quotes' contract terms name no tool; the
protocol's vocabulary states the measure, not the method; the workforce, visit, case-set, KPI and panel files rank
nothing; the 2027 workforce dates are notified starts and leaving dates under the extract's own header).

Realism tells, disposition: the location table's host at export beside the dated visit schedule read as layered
mess, and the workforce's double contracts and changed post as credible HR records (no change); the quotes as
plain one-page proposals, "slightly template-like" (kept: three layouts, voices and terms, one page each as a
summary proposal); clean, regularly timed ReadPoint exports (kept, the platform's own log).

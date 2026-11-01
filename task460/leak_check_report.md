# leak check, task460

**Verdict: REVIEW.** 11 files read, 33 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: margin, average, generators, charter, published, operating, change, project, decisive, generation, publication, checks, marginal, non-baseload, brackwell, generator, supplier, sentence, generates, balancing, tennaford, capital, register, emission, invoice

## 1 file names (REVIEW 2)
- **REVIEW** `edc_generation_emission_rates_2024.xlsx`: a sheet named 'Notes': confirm it is the organisation's own notes and does not describe the data's columns or files
- **REVIEW** `edc_generation_emission_rates_2025.xlsx`: a sheet named 'Notes': confirm it is the organisation's own notes and does not describe the data's columns or files

## 2 author vocabulary (REVIEW 1)
- **REVIEW** `ardley_power_content_label_2025.pdf`: \bdesign note\b|\bgenerator\b x1: ...urchases; unspecified sources are market purchases not traceable to a generator. Figures are rounded and may not sum to 100....

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `solar_pilot_siting_charter_2027.pdf`: carries 7 of 8 distinctive words of the committed call: 'Corvane should site its 2027 on-site solar pilot at its Gorsefield store (store 2291).'

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `solar_pilot_siting_charter_2027.pdf`: 13 of 25 stump-paragraph terms appear (generators, charter, published, operating, change, generation); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Reader, 2026-11-01 (general-purpose, sonnet, medium; isolated scratch copy of prompt.txt and target/ only, pack
8ad2aa13; the supplier's numbering realism fix that followed is data-only, so the read stands for b0a46e28).

1. none. The charter states the measure (3.1) and the premise "Each megawatt-hour the array generates is one
   megawatt-hour less that the area's generators produce" (3.3): the estimand and a physical premise, not a named
   decisive step.
2. none. No file ranks or scores the stores; the agency's workbooks give per-area annual rates, which are context.
3. none that is a helper. The code list and the utility map are reference tables; the Notes sheets are the agency's
   own notes.
4. none. Nothing is a store-level answer; the charter's "first candidate left out" is a request, not a result.
5. Charter 3.2 to 3.4, read literally: for each store, the carbon dioxide the area's generators avoid hour by hour from
   the array's hourly output, totalled and divided by the array's 2025 output, in metric tonnes; the sentences fix the
   population (the candidates, the store's own area, calendar 2025) and the unit and leave open which generators
   respond and which rate applies.
6. An analytical choice: charter 3.2 and 3.3 with the hourly operating data (generation by fuel and interchange) leave
   a real choice of which generation an extra megawatt-hour displaces; the agencies' annual average rates stand as
   the easy alternative; nothing planted; the clocks, the former area code and the units are Layer 1 around it.

REVIEW items: (a) the Notes sheets are the agency's methodology notes for its own table, harmless; (b) the label's
"generator" is retail-disclosure boilerplate, harmless; (c) the charter names the measure, the records and the memo's
contents, never ranks or points to a store, harmless.

Realism: the supplier's account and invoice numbers built from the store number read as too regular (fixed in the
generator: random account numbers and one running invoice sequence with gaps); the feasibility-study and model-run
identifiers keyed to the store number, a near-constant tilt and DC-to-AC ratio, modelled output clipping at the
inverter rating and an all-operating plant register read as tidy, all in the call's files, which stay byte-identical
to the 10-15 build that two earlier readers accepted. No file or sentence narrates how to clean or combine the data.

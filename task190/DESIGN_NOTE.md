# task190 design note

Pencarrow Mutual Bank, financial crime: which three business lines the two-week specialist review
team covers from 15 February 2027.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task190.json`, filed and committed with the wave |
| Domain, task type | Banking, Credit & Financial Risk, `fraud-aml-detection` |
| Objective | Anomaly Detection & Diagnostics (the caseload a line is carrying unseen, against the caseload it is finding) |
| Shape | 09, funnel of stages: each stage's volume, rate and cost |
| Decision | `designation_set`, the three business lines the review covers |
| Gate G | `method_or_model_selection`; decisive generator G3 record against operation, then G8, G7 |
| Strategy | `maturity_censoring`: the quantity is the part of the caseload that has not yet been detected |
| Layer 2 | `estimation_fit`, own pattern `stock-from-arrivals-and-time-unseen` |
| World | New Zealand, a retail and business bank; NZD |
| As-of date | 18 January 2027 (the extract date; the team is booked for 15 to 26 February 2027) |
| Guard | registered at WARN; differentiated against task450, task126 and task181 in the card |

**Data-native sentence.** In this bank's record a case is dated twice, by the month the activity began,
which the investigation establishes afterwards, and by the month someone first saw it, and the gap
between the two runs from under a month on the card and payment lines to a year and a half on trade
finance and correspondent banking, because the lines differ in how a case surfaces: a card case
surfaces when a customer disputes a transaction, a trade finance case only when a document review or
a counterparty enquiry reaches it.

**Sources read.** `analytical_tasks/02_anomaly_detection/AD13_hunt-placement-unmanaged-entry-yield.md`
(seed): the decision shape only, one scarce specialist team placed with one part of an organisation
for a fixed spell, scored on what it would find. Its own architecture ranks the parts by a filed
scorecard on confirmed movement per 1,000 accounts, a stated score deciding the call, and is not used:
no scorecard, league table or ranked artifact ships. `guard.py mechanisms --objective
anomaly-detection`: 22 spent drivers; the nearest, task181 v2 in lineage, completes a count whose
records have not all arrived, where here every record has arrived and the count is right, and the
decisive quantity is a different one.

## Default path

1. Read `alert_adjudication_extract.csv` and `confirmed_case_register.csv`, crosswalk the customer
   identifiers through `customer_id_crosswalk.csv`, and map each case to the business line in force in
   the review year from `line_structure_register.csv`.
2. Keep the cases the handbook counts as cases: one case per customer per typology, the confirmed
   disposition, the latest version of each record.
3. Count each line's confirmed cases over the last two quarters, the window the framework's review
   clause names.
4. Read the framework's placement clause, which sends the review where the most cases are expected to
   be found, and take the three lines with the most confirmed cases.
5. Write those three lines into the committee paper with their case counts.

**Ends on:** Cards, Deposits and Retail payments.
**Golden:** Trade finance, FX and remittance, and Business lending.

## Stump sentence

The default path ranks the lines on the cases they confirm in a quarter and files **Cards, Deposits
and Retail payments**, which is the three lines where cases are found fastest rather than the three
carrying the most cases unfound: those three confirm 108, 68 and 146 cases over the two quarters
clause 6.5 names and are expected to be carrying 18.2, 20.3 and 19.2, because a card or payment case
is seen within a month of beginning, while trade finance confirms 24 and is expected to be carrying
38.4, its cases going 9.0 months before anyone sees them.

## Three rules

- **Task type:** `fraud-aml-detection`, the task type in Banking, Credit & Financial Risk that serves
  Anomaly Detection: where in a book real activity is going undetected, and how much of it.
- **Domain test:** the deciding quantity is the undetected caseload each business line is carrying,
  which financial-crime analytics estimates as the rate at which cases arise multiplied by the time a
  case goes unseen, both read off the line's own closed cases, and never from the confirmation count
  alone, which is an arrival rate.
- **Swap:** "which three depots the audit team visits, ranked by the stock discrepancies they confirm
  each quarter" reads as a ranking of counted findings: a stocktake sees the whole shelf at a known
  moment, so there is no time a discrepancy spends unseen to multiply by, and the stock and the flow
  are the same number.
- **Layer 1:** the bank's own systems produce all of it. The alert system and the case system number
  customers differently and a crosswalk carries both; two business lines were merged and one renamed in
  the July 2026 reorganisation, with the register carrying the effective dates; a case is amended, so
  the register holds two versions; amounts sit in NZD and AUD with a currency column; the customer base
  arrives as a wide workbook with a header block; the contractor's ledger and the screening list
  versions are tables inside PDFs. None of it is placed to be caught and none of it decides the
  call.
- **Layer 2:** `estimation_fit`. The methodological choice is what quantity a scarce reviewer's yield
  is: the arrival rate the confirmations measure, or the stock those arrivals have built up at the rate
  they are being found.
- **Decisive step:** estimating each line's undetected caseload as its monthly arrival rate multiplied
  by the mean time a case goes unseen there, rather than ranking the lines by what they confirm.
- **Not semantics:** the handbook states what the onset month and the detection month of a case are and
  the dictionary gives both fields, so the reading is free. A solver who reads every field correctly
  still has to decide which quantity the placement turns on, and the confirmation count, the count per
  thousand customers, the unreviewed backlog and the time unseen each name a different three lines.
- **Not rule application:** the framework's clause 6.2 files what is wanted, the cases that have begun
  in a line and have not been detected by the review date, clause 6.4 the three-line capacity and
  clause 2.3 what a case is. No shipped sentence says how an undetected case is counted, and the
  framework, the handbook, the register and the dictionary are silent on it.
- **Analyst test:** a strong analyst who crosswalks every identifier, applies the reorganisation dates
  and the case definition correctly and reads the placement clause ranks the lines on confirmed cases a
  quarter and files Cards, Deposits and Retail payments (the `Ends on:` set), where the three carrying
  the most undetected cases are Trade finance, FX and remittance and Business lending.
- **Estimand:** clause 6.2 of `financial_crime_framework.pdf`: "The review is placed with the business
  lines expected to be carrying the most cases that have begun and have not been detected at the review
  date, counting one case per customer per typology as paragraph 2.3 defines it. A case that has begun
  and has not been detected is within this count whether or not the bank yet holds a record of it, and
  the expectation is taken over the cases the line's own closed record implies."
- **No decoy:** nothing is planted to be caught. No scorecard, league table, ranked artifact, draft
  paper, memo or stakeholder figure ships; no block is copied; the two lines whose stock and flow
  rankings agree agree because their cases surface quickly, which is the data's own consequence.
- **No certified replay:** no past placement, no published yield and no certified figure ships, so no
  method can be recovered by reproducing one. The method is forced by the data: the register's closed
  cohorts carry both dates for every case, and the cohort-survival sum and the arrivals-times-time
  product agree on all eight lines and on the three-line set.
- **Lesson:** what a scarce reviewer will find is a stock, and a stock is an arrival rate multiplied by
  how long an item stays in the state, so a unit that resolves its cases quickly can confirm the most
  and carry the least. No build on file teaches it: the 22 anomaly-detection drivers include a count
  read before its records have arrived (task181 v2, in lineage) and a yield carried onto a population
  with another base rate (task446 v2), but none has a correct, complete count that is the wrong
  quantity because the state it counts is one the items leave.

## Readability screen

| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 hygiene | 6 linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 confirmed cases a quarter | the placement clause names cases, not confirmations | the register's disposition column invites the count | yes, the first thing anyone computes | no corpus scores it | the battery counts the register, not the state | one group-by | readable |
| 1 confirmed per thousand customers | no | the customer base sits beside it | yes, the exposure reflex | no | no | one ratio | readable |
| 2 unreviewed alert backlog | no | the backlog file names it | yes, send the team where the work is piled up | no | the battery finds the backlog | one group-by | readable |
| 3 the months a case goes unseen, alone | no | both date columns are there | yes, the correction a careful solver makes after rung 0 | no | no | one subtraction and a mean | readable |
| 4 arrivals multiplied by the time unseen **(decisive)** | no sentence names a rate, a stock, a product or a duration; clause 6.2 names the cases begun and not detected and says nothing about how to count them, asserted by a word sweep over every shipped file | no column holds a stock or a rate; both dates are ordinary case fields the whole ladder reads | no reflex reaches it: the confirmation count, the exposure ratio, the backlog and the delay alone each name a different three lines, and the first three are the three reflexes | no control, corpus or published figure scores a line or a placement; the two quick-surfacing lines tie across rungs because their cases surface quickly | the battery finds the crosswalk, the versions and the reorganisation and leaves the quantity open | no: the stock is a product of two means, neither of which is reported anywhere | silent |

## Semantic fork table

| id | term or convention | golden reading | alternative | call under it | ruled out by |
|---|---|---|---|---|---|
| SF1 | case | one customer and one typology, paragraph 2.3 | one alert, or one customer | the set changes | paragraph 2.3, quoted; asserted on counts |
| SF2 | business line | the line in force at the review date | the line recorded on the case at the time | the set changes | clause 6.2 "the business lines" with the register's effective dates; asserted |
| SF3 | begun | the onset month the investigation establishes | the month the first alert fired | the set changes | the handbook's definition of the onset month; asserted |
| SF4 | detected | the month someone first saw the case | the month it was confirmed, or closed | `same call`, asserted: the three-line set and all eight ranks hold under the confirmation month too |
| SF5 | review date | 15 February 2027, the first day of the review | the extract date | `same call`, asserted at both dates |
| SF6 | the closed window | the onset cohorts the framework states are fully resolved | every cohort in the register | the set changes | clause 6.3, quoted; asserted |
| SF7 | record version | the latest amended version of a case | the first version | `same call`, asserted: no amendment moves an onset or detection month |
| SF8 | currency | the amount in NZD after converting the AUD rows | the amounts as recorded | `same call`, asserted: no amount enters the count |
| SF9 | capacity | three business lines | the lines a two-week spell could cover by volume | the set changes | clause 6.4 "three business lines", quoted |
| SF10 | the count's unit | cases | customers, or alerts | the set changes | clause 6.2 "counting one case per customer per typology" |
| SF11 | rounding | the three lines are named; no figure is rounded before the comparison | the stocks rounded to whole cases first | `same call`, asserted at whole cases and one decimal |
| SF12 | ties | none: the eight expectations are distinct | a tie at the cut | `same call`, asserted: the third line stands 26 per cent above the fourth |
| SF13 | the figure compared | the expected number carrying at the review date, clause 6.2 | the number a single realisation would carry | the third line changes | clause 6.2 "expected to be carrying" and "the expectation is taken over the cases the line's own closed record implies"; the two estimators the record admits agree and are asserted |

## Ladder

| Rung | The analysis | The three lines |
|---|---|---|
| 0 | the cases each line confirms in a quarter | **Cards, Deposits, Retail payments** |
| 1 | confirmed cases per thousand customers | Correspondent banking, Private wealth, Trade finance |
| 2 | the unreviewed alert backlog | Deposits, FX and remittance, Retail payments |
| 3 | the months a case goes unseen, alone | Correspondent banking, Private wealth, Trade finance |
| 4 | **answer:** the cases begun and not yet detected, the arrival rate multiplied by the time unseen | **Trade finance, FX and remittance, Business lending** |

**Worth on the graded quantity.** Rung 0's set is disjoint from the answer: all three names change.
Rung 1 and rung 3 share one name with it, rung 2 shares one. Four distinct answers across five rungs,
and no monotone correction reaches the answer: ranking on the arrival rate puts the quick lines first
and ranking on the delay puts the slow, small lines first, while the answer is the product, whose top
three are middling on both factors.

**Separation.** FX and remittance 46.2, Business lending 43.0, Trade finance 38.4, then Private wealth
26.1, so the third line stands 47 per cent above the fourth, asserted. The two estimators the data
admits agree on all eight lines and on the set: the product of the monthly arrival rate and the mean
months unseen, and the sum over onset cohorts of the arrivals still undetected at the review date.

**Dominance.** Trade finance is the line the ladder turns on: it is third on the expectation at 38.4
and seventh on confirmations at 24, and it is the only line the answer shares with rungs 1 and 3. FX
and remittance carries the largest unreviewed backlog, so rung 2 reaches it for the wrong reason, and
Cards confirms the second most cases and is expected to be carrying the least at 18.2.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | which cases are counted | clause 6.2 files it, including the cases the bank holds no record of yet, and files the figure as an expectation over the line's own closed record; SF1, SF6, SF10; C1 asserted on counts |
| 2 Unit of account | case, customer, alert | clause 6.2 "one case per customer per typology"; SF1, SF10 |
| 3 Attribution window | which cohort a case falls in | the onset month, SF3; the closed window, SF6; cohorts clear of the boundary, asserted |
| 4 As-of dating | the review date against the extract date | SF5; both give the same set, asserted |
| 5 Version basis | amended cases | SF7; asserted that no amendment moves either date |
| 6 Denominator | the arrival rate's period | months, from the onset months in the closed window; asserted at quarters too |
| 7 Weighting | each case weighted equally | clause 6.2 counts cases; no weight appears |
| 8 Window length | how far back the arrival rate is measured | C1 across the closed window's lengths, asserted over three lengths |
| 9 Boundary inclusivity | cases on the cutoff month | nothing on the boundary, asserted nine days clear |
| 10 Rounding path | before or after the comparison | SF11; the set is identical at whole cases and one decimal |
| 11 Tie-break | two lines at one stock | SF12; the eight stocks are distinct and the cut margin is 23 per cent |
| 12 Maturity and censoring | cases not yet detected | the decisive step; the estimand is filed and the estimator is forced by the closed cohorts |
| 13 Order of operations | crosswalk, reorganise, then count | every order gives the same figures, asserted |
| 14 Row order | the extract's order | C1, asserted over three permutations |
| 15 Duplicate resolution | one customer under two identifiers | the crosswalk resolves them; the main population holds no duplicate pair, asserted |
| 16 Identity normalisation | the alert system against the case system | `customer_id_crosswalk.csv`, every identifier matched, asserted |
| 17 Netting against gross | none; cases do not offset | asserted that no case count is negative |
| 18 Dimensional units | months against quarters | the arrival rate and the delay are both in months, asserted |
| 19 Code and status semantics | disposition and typology codes | the dictionary, SF1; never the decisive step |
| 20 Integerisation | three lines named | a set of three by construction |
| 21 Clause scope | per line, per review | clause 6.2's own scope |
| 22 Forward window contents | the review runs 15 to 26 February 2027 | the call is forward facing: the quantity is the caseload the review will meet, and the pack carries no record of that review |

## Literal reader

Executing the prompt, clause 2.3, 6.2, 6.3 and 6.4, the handbook's two date definitions and the
dictionary word for word selects the cases of the closed onset cohorts at the eight business lines in
force at the review date, and asks which three lines carry the most cases begun and not yet detected.
The text is silent on how an undetected case is counted, so every option was computed: the
confirmations a quarter name three lines, the confirmations per thousand customers another three, the
unreviewed backlog another three, the time unseen alone the same three as the ratio, and the two
estimators that count the state itself name Trade finance, FX and remittance and Business lending.
The easy ones are easy methods on the same literal estimand, not other readings of it, and every other
term and convention has an SF row ruled out by a quoted sentence or asserted to give the same call.

## Oracles

- The register's closed cohorts confirm that every case with an onset in the closed window carries a
  detection month; they tie under every rung, because they carry no rate, no stock and no placement.
- `extract_manifest.csv` confirms the extract's row count and date range; it ties under every rung.
- The contractor's hours ledger confirms what past reviews cost, never what they found.
- No control, published figure or corpus scores a line or a placement, and no past placement ships.
  There is no calibration organ.

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Files, columns | Stops, lazy delta | Realism |
|---|---|---|---|---|---|---|---|---|
| A1 the review contract's own spend | per quarter, the hours the contractor billed, the hours the contract allows, and the tickets billed outside the rate card (12 figures) | the audit trail of the instrument the call commits | the committee is asked for the spend beside the placement | D1, a credit note reissued under a second reference, so a plain sum counts it twice | the rate card revised mid-year; hours in two time bases | ledger, contract register, manifest, dictionary; 9 columns | 4 stops; the lazy sum double-counts 11 credit notes | the contract's quarterly reconciliation |
| A2 the screening list's own history | per list version, the customers who matched an entry that a later version removed, and how many were cleared (10 figures) | an input the call's own system consumes, read on rows the call never touches | the bank's own list-change review | D2 version, the entry in force at the screening date against the current list | a list version loaded twice; names transliterated two ways | screening versions, match log, dictionary; 8 columns | 4 stops; the lazy read applies the current list and files zero | the supervisor asks for it every year |
| A3 one line's alert funnel | per month for the card disputes queue, alerts raised, closed inside the five working day standard, and escalated (36 figures) | a measure every line carries that the call does not turn on | the operations report | D8 clocks, the standard counts working days and two runs fall after a public holiday | a queue renamed mid-year; a re-sent batch | alert extract, calendar, dictionary; 10 columns | 5 stops; the lazy read counts calendar days and files 14 months of breaches | the queue's monthly service report |

**Main population separation.** Zero device rows in the main call's population (the confirmed cases of
the closed onset cohorts at the eight lines, with the customer base): A1's credit notes are in the
contractor ledger, A2's list versions in the screening files, A3's device in the card disputes queue's
alert rows, which carry no case. Asserted by count in `checks.py`. The main path still carries its own
texture: the identifier crosswalk, the reorganisation dates, the amended case versions and the two
currencies.

**Hazard table.** The reorganisation moves A1 and A3; the identifier crosswalk moves A2 and A3; the
re-sent batch moves A3.

**Referee.** `extract_manifest.csv` arbitrates the extract's extent and nothing else; it ties under
every rung and settles no level.

**Cracker sheet.** The cracker placed the review correctly at rung 4, ran the hygiene battery,
executed clauses 2.3, 6.2, 6.3 and 6.4 and matched the manifest.

| Ask figure | Cracker's figure | Golden | Result |
|---|---|---|---|
| A1 hours billed, 2026 Q3 | sums the ledger, counting both references of each reissued credit note | 226.2 | miss |
| A1 tickets outside the rate card, 2026 Q1 | counts every ticket not at the review rate but keeps the duplicated credit notes | 4 | miss |
| A2 customers matched to an entry later removed, v2 | applies the current list to every screening date and files 0 | 14 | miss |
| A3 alerts closed inside the standard, 2026-01 | counts calendar days, not working days | 86 | miss |
| A3 alerts raised, 2026-06 | keeps the re-sent batch, so June is inflated | 139 | miss |

Pair ceiling: 34.0
Mirror leakage: 20.0 per cent of the ask weight

## Pre-ship check

- **The 10/10 rules re-read against the built pack.** The decisive step is still the quantity, not the
  method: `checks.py` runs the easy route on the generator's clean truth and it files Cards, Deposits
  and Retail payments, while the same clean truth under the decisive step files Business lending, FX
  and remittance and Trade finance. All four reflexes are executed there and none reaches the answer.
  The mess is Layer 1 only: the identifier crosswalk, the reorganisation codes, the amended versions
  and the two currencies all sit on the main path and removing every one of them leaves the call
  exactly as hard, because the decisive step is in the two months every case already carries.
- **Rule 3, each class.** Nothing is planted (no repeated case key, asserted; no scorecard, league
  table, past placement or ranked artifact ships, and the framework says in its own clause 9.2 that
  the bank maintains no ranking of its lines). Not semantics (the handbook defines all three months
  and the dictionary gives every field, and a word sweep over every shipped file asserts that none of
  them says arrival, per month, multiplied by, stock of, how long, mean time or Little's law). Not
  rule application (clause 6.2 files the population, the unit and the event that ends the count,
  clause 6.3 the closed record, clause 6.4 the capacity, and no shipped sentence says how a case that
  nobody has seen is counted).
- **Input gates.** 16 files, 4 formats (csv, xlsx, json, pdf), the alert extract at 25,825 rows, two
  distractors declared in `metadata.json` and named in neither a file name nor the prompt.
- **Gate G.** No shipped artifact ranks or scores the lines, asserted over every PDF. The difficulty
  survives deleting every number in the pack that is not a case record: the two months each case
  carries are the whole of it.
- **Free gates.** `precut.py` 49 checks 0 FAIL 0 WARN; `voice-check.py` PASS at 938 characters; 120
  generator assertions; 112 independent checks; two byte-identical rebuilds of `target/` and
  `golden/`; `figures_check.py` 64 of 64; `leak.py` REVIEW; `guard.py surface` clean and `heart` WARN
  only.
- **Forward facing.** The review runs 15 to 26 February 2027, after the 18 January extract and the 28
  January committee, so the quantity is the caseload the review will meet and the pack carries no
  record of that review (closure axis 22).

## Tried and rejected

- Ranking the lines by the share of alerts that prove real (the yield reading): `guard.py nearest`
  measured the driver at 0.15 against task446 v2, which already builds a yield carried onto a
  population with a different base rate. Dropped at the draw, before any data was cut.
- The seed's own architecture, a filed scorecard ranking the divisions on confirmed movement per 1,000
  accounts: a stated score deciding the call, which the 10/10 rules ban, and a ranked artifact Gate G
  forbids shipping. No scorecard ships.

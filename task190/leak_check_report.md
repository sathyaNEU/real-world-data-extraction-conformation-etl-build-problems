# leak check, task190

**Verdict: REVIEW.** 16 files read, 14 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: asserted, clause, quantity, arrival, unseen, record, customer, caseload, decisive, detected, ranking, register, carrying, scorecard, undetected, crosswalk, backlog, months, detection, ranked, different, sentence, multiplied, system, product

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `financial_crime_framework.pdf`: golden figure 6.2 appears: ...places it with, for the period the contract sets. 6.2 The review is placed with the business lines expe...

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `extract_dictionary.pdf`: 7 of 25 stump-paragraph terms appear (record, customer, register, crosswalk, backlog, months); read whether the document names the move
- **REVIEW** `financial_crime_framework.pdf`: 9 of 25 stump-paragraph terms appear (record, customer, detected, ranking, register, carrying); read whether the document names the move
- **REVIEW** `investigation_handbook.pdf`: 3 of 25 stump-paragraph terms appear (record, customer, months); read whether the document names the move

## 9 dates after the setting (REVIEW 2)
- **REVIEW** `alert_adjudication_extract.csv`: 883 ISO dates after 2027-01-18, e.g. 2027-01-19, 2027-01-20, 2027-01-21, 2027-01-22, 2027-01-23
- **REVIEW** `extract_manifest.csv`: 1 ISO dates after 2027-01-18, e.g. 2027-02-14

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

One isolated reader, pass 1, on the bundle as first cut (prompt and `target/` only, no design note,
generator or submission).

1. **Nothing quoted.** "No sentence names it", though it read clauses 6.2 and 6.3 as pointing at the
   quantity, which is the estimand being filed and is what determinism requires.
2. **No file.** It found clause 9.2 and named the per-line files (backlog, training, branches,
   customer base) as the ranking-shaped ones, adding that "none assesses the question directly" and
   that "the confirmed_case_register.csv counts by line are the tempting wrong ranking".
3. **Nothing.** "A bank would hold them, but nothing in the request uses them" of the four per-line
   files; it named the dictionary's two notes as guidance for the side asks, which is what a
   dictionary is for.
4. **Nothing.** "The tempting figure is the confirmed counts by line ... and the placement is the
   opposite of it."
5. Clauses 6.5 and 6.2 with 6.3 and 2.3, quoted. It then computed the whole table itself and
   reproduced every figure exactly: FX 46.2, BL 43.0, TF 38.4, PW 26.1, DP 20.3, RP 19.2, CD 18.2,
   CB 12.5, adding "mean lag times monthly onset rate gives the same numbers", which is the
   convergence `checks.py` asserts.
6. **An analytical choice.** "The decision is an analytical choice, the estimand ... The easy route
   counts confirmed cases by line. The right one is the expected count of begun-but-unseen cases ...
   The text states the quantity but not the arithmetic. Secondary mechanics ... are semantics or
   rules, not the decisive step."

**It landed the call**, naming FX and remittance, Business lending and Trade finance, and reported the
two bases as "completely disjoint sets". That is recorded as the honest Gate F signal on this build.
The reader is not a solver proxy: question 1 tells it to hunt for the decisive step, and it had read
clause 6.2 before answering. The stump stands on a solver who does not go looking, for whom the
default path, the exposure ratio, the backlog and the delay alone all land wrong, and the portal is
the only oracle for that. The judge's Gate F reads it independently.

**Realism, taken forward.** The reader called the pack "plausibly real but slightly too orderly":
every disposition `confirmed`, versions only 1 or 2, and sequential identifiers. It also read clause
9.2, the framework's statement that the bank maintains no ranking of its lines, as "placed on purpose
to reassure". Both are addressed in the fix pass: the clause is removed, the register carries the
withdrawn cases it would really hold, and the identifiers are no longer sequential.

**Mechanical sweeps.** `leak.py` returns REVIEW. The two LEAK lines of the first run were the
contract's allowed hours and rate card, which are inputs an ask reads and are now listed under
`stated_inputs` in `metadata.json`.

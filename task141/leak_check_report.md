# leak check, task141

**Verdict: REVIEW.** 13 files read, 27 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: petitions, decisive, window, record, petition, exposure, expiration, forecast, detention, family, clocks, forecasting, extracts, booking, nothing, architecture, revocations, center, extract, transition, analyst, scheduled, length, readable, release

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `jail_operations_plan_instructions_2027.pdf`: golden figure 220 appears: ...22 Okelan County pod of 64 beds one unit for each 220 felony probation revocation admissions projected...
- **REVIEW** `jail_operations_plan_instructions_2027.pdf`: golden figure 100 appears: ...extract. 4.3 State the projection to the nearest 100 admissions, with the parts it is built from. 5....
- **REVIEW** `jail_operations_plan_instructions_2027.pdf`: carries 11 of 13 distinctive words of the committed call: "Okelan County's 2027 Jail Operations Plan should carry 1,200 felony probation revocation admissions and staff 6 violator"

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `sb26_118_felony_probation_term_act.pdf`: 4 of 25 stump-paragraph terms appear (expiration, scheduled, length, release); read whether the document names the move

## 9 dates after the setting (REVIEW 2)
- **REVIEW** `circuit_court_term_orders_2016_2026.csv`: 2238 ISO dates after 2026-10-02, e.g. 2026-10-03, 2026-10-04, 2026-10-05, 2026-10-06, 2026-10-07
- **REVIEW** `cms2_supervision_cases_2023_2026.csv`: 11152 ISO dates after 2026-10-02, e.g. 2026-10-03, 2026-10-04, 2026-10-05, 2026-10-06, 2026-10-07

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read (architecture 3, stage 4 round 1, zip 7cd8129f)

Two isolated scored readers (general-purpose, sonnet, medium), each on its own fresh copy of `prompt.txt` and
`target/`, briefed with the prompt's own figures only (`call.admissions`, `call.pods`, the 16 ask figures).

**Reader A** (score_reader exit 1: the call landed, asks 14 of 16, estimated share 93.1). Simulated the 7,620 open
felony terms with petition rates by tenure and by days to the scheduled expiration in force ("filings spike 15 to 90
days before expiry, at about 90 per 1,000 term-months against about 16 otherwise, and this is stable every year"),
the Act's ends with the 31 March floor, section 6's pending proceedings and new starts; back-tested at September 2023,
2024 and 2025; about 1,146, calibrated about 1,165, 1,200 and six pods (it called the projection close to the 1,150
edge). Q1 to Q4: none. Q5: instructions 3.1 fixes the unit, the Annex the pods; no method filed. Q6: an analytical
choice, "a filing-rate model with a pre-expiry petition spike" ("the data, not a sentence, shows the spike"). Ask A:
linked each PV-FEL booking to the revoked term (203 relabelled), Q3 off by 14 felony and misdemeanor days on its
chaining; Ask B: term_months less the summed EXTENSION months, every figure.

**Reader B** (score_reader exit 1: the call landed, asks 16 of 16, estimated share 100.0). "A petition-filing model by
tenure and months to expiry, with the cap applied (31 March 2027 floor, 24 months), pending petitions continuing, and
new starts added": about 1,150 to 1,185, 1,200 and six pods. Q1 to Q4: none. Q5: the Annex fixes the pods; "No filed
sentence fixes how the projection is computed". Q6: an analytical choice ("Petition filings surge in the last 3
months before expiry"). Ask A: "About 196 misdemeanor-only commitments are booked PV-FEL because the person has an
active felony term", linked to the revoked term; Ask B: term_months less the summed extensions.

REVIEW lines (both readers): the instructions' 220 and 100 are the standard and the rounding, harmless; the call's
words in the instructions are the plan's own vocabulary, harmless; the dates after the setting are scheduled
expirations only (order, petition, closure and booking dates end on 30 September 2026), harmless. The stump-vocabulary
line (the Act's expiration, scheduled, length, release) ruled in the main thread: the statute's own subject, it names
no petition, clock or rate. Realism: both called the pack organic; reader A found the year-to-year stationarity tight
and the office codes tidy, reader B the term lengths all multiples of six months.

**Disposition: architecture 3 spent.** Both readers landed the call, so no ask repair reaches it (`leak-check`, the
pack that ships is read twice). The decisive alignment, petitions by days to the expiration in force, was the first
model both readers built once the Act was read: the statute points at the expiry clock, and the clock is one
subtraction and a histogram away. Both ask devices were also found by both readers.

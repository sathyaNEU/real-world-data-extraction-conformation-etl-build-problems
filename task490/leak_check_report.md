# leak check, task490

**Verdict: REVIEW.** 14 files read, 37 golden figures and 16 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: chamber, filling, register, harnock, camera, keepers, decisive, lockful, record, survey, objective, shared, sentence, cycles, conformed, decision, minutes, reading, chambers, kelsby, checks, movement, meeting, tilsey, repeat

## 3 answer figures in the pack (REVIEW 8)
- **REVIEW** `backpumping_programme_2027-28.pdf`: candidate 'Tilsey Top Lock' sits beside decision vocabulary: ...ck summit Harnock Top Lock (31) and Steward's Lock (32), Harnock Navigation Tilsey summit Tilsey Top Lock (8) and Engine Lock (9), Tilsey Canal 3.3 Water is reckoned in lockfuls, a lockful being...
- **REVIEW** `backpumping_programme_2027-28.pdf`: candidate 'Wharf Lock' sits beside decision vocabulary: ...hat rise to each summit pound: Summit Summit locks Kelsby summit Kelsby Top Lock (12) and Wharf Lock (13), Kelsby Canal Harnock summit Harnock Top Lock (31) and Steward's Lock (32), Harnock...
- **REVIEW** `backpumping_programme_2027-28.pdf`: candidate 'Kelsby Top Lock' sits beside decision vocabulary: ...locks are the two locks that rise to each summit pound: Summit Summit locks Kelsby summit Kelsby Top Lock (12) and Wharf Lock (13), Kelsby Canal Harnock summit Harnock Top Lock (31) and Steward's...
- **REVIEW** `backpumping_programme_2027-28.pdf`: candidate 'Harnock Top Lock' sits beside decision vocabulary: ...locks Kelsby summit Kelsby Top Lock (12) and Wharf Lock (13), Kelsby Canal Harnock summit Harnock Top Lock (31) and Steward's Lock (32), Harnock Navigation Tilsey summit Tilsey Top Lock (8) and En...
- **REVIEW** `backpumping_programme_2027-28.pdf`: candidate 'Engine Lock' sits beside decision vocabulary: ...ck (31) and Steward's Lock (32), Harnock Navigation Tilsey summit Tilsey Top Lock (8) and Engine Lock (9), Tilsey Canal 3.3 Water is reckoned in lockfuls, a lockful being the chamber volume t...
- **REVIEW** `reservoir_register_extract_2025.pdf`: candidate 'Lower Kelsby' sits beside decision vocabulary: ...Upper Kelsby 1,180 Valve tower, 300 mm outlet valve; daily return by the reservoir keeper Lower Kelsby Reservoir, by the Hollins Brook Lower Kelsby 2,410 Valve tower, 450 mm outlet valve, abou...
- **REVIEW** `reservoir_register_extract_2025.pdf`: candidate 'Lower Kelsby Reservoir' sits beside decision vocabulary: ...Upper Kelsby 1,180 Valve tower, 300 mm outlet valve; daily return by the reservoir keeper Lower Kelsby Reservoir, by the Hollins Brook Lower Kelsby 2,410 Valve tower, 450 mm outlet valve, about 16 Ml/d...
- **REVIEW** `backpumping_programme_2027-28.pdf`: carries 17 of 17 distinctive words of the committed call: 'Site the 2027/28 back-pumping scheme at Kelsby summit: its two summit locks drew 1,460.8 Ml from the summit pound by fil'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `backpumping_programme_2027-28.pdf`: 13 of 25 stump-paragraph terms appear (chamber, filling, harnock, keepers, lockful, record); read whether the document names the move
- **REVIEW** `reservoir_register_extract_2025.pdf`: 5 of 25 stump-paragraph terms appear (register, harnock, record, kelsby, tilsey); read whether the document names the move

## 6 ranking artifacts (REVIEW 8)
- **REVIEW** `abstraction_licences_2026.xlsx`: names 8 of 16 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `backpumping_programme_2027-28.pdf`: names 5 of 16 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `counter_sites_2026.json`: names 5 of 16 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `lock_register_2026.xlsx`: names 5 of 16 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `navigation_notices_2026.csv`: names 4 of 16 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `reservoir_register_extract_2025.pdf`: names 3 of 16 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `reservoir_returns_2026.xlsx`: names 3 of 16 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `reservoir_storage_weekly_2026.csv`: names 3 of 16 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 2)
- **REVIEW** `boat_licence_register_extract_2026-11.csv`: 1953 ISO dates after 2026-11-06, e.g. 2026-11-07, 2026-11-08, 2026-11-09, 2026-11-10, 2026-11-11
- **REVIEW** `navigation_notices_2026.csv`: 4 ISO dates after 2026-11-06, e.g. 2026-11-09, 2026-11-16, 2027-02-26, 2027-03-12

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read

The isolated leak reader (medium effort) read prompt.txt and the 14 files of target.zip (sha256 65c71f873a930e9dbe1fec3d3f54dff7b28f852a1f23cc528304e4b892099a9e) on 2026-11-07, quoting only, solving nothing. Verdict: no LEAK. Sweep 3's call vocabulary and sweep 4's design-note vocabulary in the programme paper were ruled by the orchestrator: section 3 states what is counted (the water the summit locks drew from the summit pound by filling their chambers, the season, the clock, the lockful) and nothing on how a filling is found from the movement records; the reservoir register names places beside its own figures.

1. Decisive step stated? backpumping_programme_2027-28.pdf 3.1: "The scheme will serve the summit whose summit locks drew the most water from the summit pound by filling their chambers over the 2026 boating season, 1 April to 31 October 2026, clock time at the lock." It fixes what is counted, not how to count it. Nothing else announces a step.
2. File that ranks/scores candidates on the prompt's question: none.
3. File that exists only to help the analyst: none. (lock_register_2026.xlsx "1951 schedule" sheet and abstraction_licences/reservoir_register extract read as ordinary context or distractors.)
4. Figure or name reading as the answer: none. No summit is flagged or totalled anywhere.
5. Literal fixing sentence: PDF 3.1 plus 3.2/3.3: "the two locks that rise to each summit pound" (Kelsby Top 12 and Wharf 13; Harnock Top 31 and Steward's 32; Tilsey Top 8 and Engine 9), "Water is reckoned in lockfuls, a lockful being the chamber volume the 2025 chamber survey gives for the lock, and reported in megalitres." Literal result: population = the six summit locks' chamber fillings, 1 April to 31 October 2026, clock (UK local) time, volume = survey lockful per filling, summed per summit. Also 3.4 names the counter export plus, on Tilsey keeper-duty days, the keepers' log, as the record. Unit/window/comparison fixed; counting rule for fillings is not.
6. What decides the main answer: from the folder it reads as an analytical reconstruction (turning boat movements, two firmware conventions, a second record at Tilsey and chamber state into fillings), not a stated rule; I find no sentence that executes it for the solver. Closest is in navigation_notices (see c).

a. harmless, because section 3 fixes only what is counted (water drawn from summit pound by filling chambers, season, clock time, lockful volume) and says nothing on boats sharing a chamber or the way a chamber is left.
b. harmless, because no file ranks or points at a summit on the siting basis.
c. Mild leak risk: lock_register has no boats-per-chamber or left-state column (only fill/empty minutes, gate years, 12 h fall), and counter_sites_2026.json says only camera at tail facing up the chamber, axis A tail pound / B lock chamber, and direction codes; neither decides the count. But navigation_notices_2026.csv (CCT-N-2026-0084/0085/0086 "All locks are left empty.", 0189 "The lock is left empty.") states a left-state fact for the reopening and one stoppage. That is realistic notice wording and applies at reopening only, not the daily convention, so I rate it harmless but the one place a left-state word appears. Nothing says how many boats a chamber takes.
d. harmless, because they carry per-reservoir, per-licence and per-week figures only; none totals or ranks summits by lockage.
e. harmless, because prompt.txt fixes the question, deliverables, and units/rounding ("megalitres to one decimal and abstraction in whole cubic metres") and describes no data or method. "on the siting basis in its programme paper" only points to the PDF.
f. harmless, because boat licence expiries run 2026-04-01 to 2027-03-31 (about 39 percent after 6 Nov 2026), exactly what a licence register holds; navigation notices after the setting (CCT-N-2026-0533/0537) are issued 21-22 Oct 2026 for winter stoppages from 9/16 Nov, ordinary planned-works notices. Every record of activity ends by 2 Nov 2026.

Realism: none that is clear. PDFs have letterhead, running header/footer, page numbers, version and document-control table, owner and dates consistent with PDF creation dates (21 Sep, 7 Jul 2026), no overflow. Minor tells only: the programme paper is brief and tidy, and works_orders_2026.csv is dominated by repeated "Lock cottage gutter repair / Complete." rows (filler-like uniformity); keepers' log notes are only "cruiser". Counter export, keepers' log (dd/mm/yy, watch time), reservoir returns (dd/mm/yyyy, 09:00 water day, keeper remarks), registers and the UTC outlet CSV carry distinct date formats and conventions, reading as separate systems. File names agree with contents.

Orchestrator's ruling on the reader's notes: the navigation notices' "All locks are left empty" is ordinary reopening wording after a stoppage and fixes no chamber's state between boats, so it stays. The repeated "Lock cottage gutter repair / Complete." rows in works_orders_2026.csv and the keepers' log notes that only ever say "cruiser" read as too uniform; both are varied in the generator.

# leak check, task255

**Verdict: REVIEW.** 12 files read, 42 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: million, likelihood, record, deductible, truncation, censoring, memorandum, closed, sentence, asserted, window, actuary, decisive, distribution, severity, fitted, recorded, archive, accident, ground-up, censored, thresholds, maximum, domain, truncated

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `risk_financing_policy_2026.pdf`: carries 10 of 13 distinctive words of the committed call: "Keep the first $4,000,000 of each 2027 liability occurrence: Fallowmere's 2027 retention is the $4.0 million quoted atta"

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `actuarial_study_2026_selected_exhibits.pdf`: 3 of 25 stump-paragraph terms appear (million, actuary, accident); read whether the document names the move
- **REVIEW** `extract_notes_2027_retention_review.md`: 4 of 25 stump-paragraph terms appear (deductible, closed, actuary, accident); read whether the document names the move
- **REVIEW** `liability_coverage_memorandum_2026.pdf`: 3 of 25 stump-paragraph terms appear (record, deductible, memorandum); read whether the document names the move
- **REVIEW** `risk_financing_policy_2026.pdf`: 10 of 25 stump-paragraph terms appear (likelihood, record, deductible, closed, actuary, distribution); read whether the document names the move

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `vehicle_schedule_log_2022-2026.csv`: 24 ISO dates after 2026-10-20, e.g. 2026-10-21, 2026-10-26, 2026-10-27, 2026-10-28, 2026-10-30

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

Two isolated reads (general-purpose, sonnet, medium) on fresh copies of prompt.txt and target/: once at stage 4, once
after the realism repairs.

1. Decisive step: none quoted. Memorandum 2.3 (tender when the member's payments reach the deductible) and 3.2 (the
   excess insurer's payments are not entered in the pool's claims system) make the record's structure discoverable;
   neither says how to estimate through it. Ruled harmless: they are the observation facts the estimand needs
   (determinism-check section 1), and the move (a truncated and censored likelihood at 2027 cost) is stated nowhere.
2. Ranking or answer files: none; the broker's letter lists the seven attachments with rates and no preference.
3. Analyst-only file: none; the extract notes read as the finance office's cover note.
4. Answer-like figure: none (228.7 and the payroll are inputs).
5. Literal sentences: policy 4.2, 4.3, 5.1 and 5.2. Reader 1 read 4.2 as leaving the likelihood open and computed the
   plain, censored and truncated-and-censored fits to the golden's own figures ($2.0 million, $2.5 million,
   $4.0 million). Ruled: the curve of 4.1 is over all the members' occurrences at their full cost, and the
   memorandum files how the record arises, so the record's likelihood is the truncated and censored one; the
   isolated judge read it the same way.
6. What decides: an analytical choice (estimating the severity curve through the deductible floor and the retention
   cap); no plant found.

Mechanical lines: all ruled harmless (the policy carries the call's own nouns; four documents use ordinary domain words
and none names a truncation or a censoring, asserted; schedule changes keyed before they take effect, allow-listed).

Realism rulings: fixed in the generator, no main-call figure moved: a 2024 member's schedule rows dated from 2022;
unit numbers in member blocks; one-formula revaluations; one-curve rate ladder; uniform closing pace in the triangles;
the log note's entry date. Kept as the record such a pool keeps: the pool's share stopping at the retention less the
deductible, a member's frequent deductible changes, the consortium's bulk load on one day. Did not hold on checking:
VINs with I, O or Q and model-year codes out of place (every cleaned VIN is valid).

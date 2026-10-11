# leak check, task133

**Verdict: REVIEW.** 15 files read, 25 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: sample, survival, asserted, nothing, months, performing, reporting, staging, arrangement, status, header, repayment, forward, development, reading, dividing, dictionary, decisive, conditioning, construction, device, register, cohort, analyst, reader

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `scorecard_v4_migration_note.pdf`: golden figure 560 appears: ...point. Selected scores on the two scales: v3 520 560 600 640 680 720 760 800 v4 564 609 654 699 744 78...
- **REVIEW** `scorecard_v4_migration_note.pdf`: golden figure 680 appears: ...ted scores on the two scales: v3 520 560 600 640 680 720 760 800 v4 564 609 654 699 744 788 833 878 Ap...
- **REVIEW** `CRM-ECL-04_expected_credit_loss_personal_loans.docx`: carries 8 of 9 distinctive words of the committed call: 'Book a collective expected credit loss allowance of AUD 13,160,000 on the PL36 and PL60 personal loans at 30 September 2'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `CRM-ECL-04_expected_credit_loss_personal_loans.docx`: 9 of 25 stump-paragraph terms appear (nothing, months, performing, reporting, staging, arrangement); read whether the document names the move
- **REVIEW** `ecl_extract_dictionary.txt`: 9 of 25 stump-paragraph terms appear (sample, nothing, months, reporting, arrangement, repayment); read whether the document names the move

## 9 dates after the setting (REVIEW 2)
- **REVIEW** `hardship_register_2026-09-30.xlsx`: 742 ISO dates after 2026-10-12, e.g. 2026-10-13, 2026-10-14, 2026-10-15, 2026-10-16, 2026-10-17
- **REVIEW** `personal_loan_book_2026-09-30.csv`: 864 ISO dates after 2026-10-12, e.g. 2026-10-13, 2026-10-14, 2026-10-15, 2026-10-16, 2026-10-17

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt form (clean)

## Solver's-eye read (hardening loop 1)

One isolated reader on Sonnet, on a fresh copy of the prompt (853 characters) and the 15 shipped files.

1. Decisive step: none. The nearest pointers are the two definitions: CRM-ECL-04 3.2 ("PD(k), the probability of default in the k-th month after the reporting date, comes from the model team's cumulative default curve for the loan's product") and the curve header ("cumulative_pd: share of the loans drawn in the development window that had defaulted by the end of that month on book"). Neither says to difference the curve, offset it by months on book or condition on loans still open.
2. Ranks or states the asked figures: none. The aggregate write-off file is the nearest and gives nothing by product, stage or default cohort.
3. Exists only to help: pd_model_development_sample.parquet. An allowance run has no use for a model's development sample, its loan_key joins to nothing, and its only function reads as supplying the prepaid and matured outcomes behind the curve. Weaker: the aggregate write-off file.
4. Reads as the answer: none. The 70 and 76 per cent, the 2.4 scalar, 3.85 cents and 60 points are stated inputs; the March 2026 recoveries spike in the write-off file is the debt sale, context for the LGD ask.

REVIEW lines: all harmless (the policy defines PD(k) and names the curve but never says how a cumulative curve becomes a loan's monthly PD; the dictionary defines fields and files; 560 and 680 are two of eight grid points in the conversion table; the dates after 12 October are first repayments of loans funded in September and arrangement end dates, and no event date passes 30 September).

Disposition, under "solver first, polish after":
- Fixed before the round (question 3): the development sample is given its in-world reason. PLPD-2026.06 was approved on 24 June 2026 and this is the first quarter-end run on it, so Credit Risk Modelling's release package (the curve and its development sample) is filed with the run for the external auditors' review of the model change.
- Fixed before the round (fork on the main call): whether a loan repaid in full during month on book a is still open at a. The sample's outcome month is pinned to the curve header's own convention, the month on book by whose end the loan had defaulted, been repaid in full or matured.
- The stump, for the determinism judge: dividing the increments by 1 minus the cumulative PD against dividing by the share of the cohort still open and performing.
- Low risk, left: 3.3's annual LGD review against the 70 and 76 per cent in force; 3.7's rounding (the stage amounts sum to the rounded total in this build).
- Deferred to the repair after a round the solver misses (stage 6b): the ask-level forks (the date a cured loan's full recovery is discounted from; contract rate over 12 against the annual rate per whole month in 3.3; whether "each stage" on the slide counts stage 3) and the realism tells (a policy that closes every ambiguity the data raises, with a v4.2 history line naming them and an effective date on the reporting date; 3.2 not citing PLPD-2026.06; a dictionary that reads as a guide to the pack; an unsmoothed empirical curve with a step in its last month; a hardship register whose statuses never go stale beyond the two pre-explained rows; reconciliations that tie almost to the loan; CHG-26-0418 and the run_date note reading as there so the 30 June score is recovered one way).

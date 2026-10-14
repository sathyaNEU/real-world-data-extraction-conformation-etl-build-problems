# leak check, task133

**Verdict: REVIEW.** 15 files read, 26 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: record, taken-over, repayment, decisive, drawdown, device, asserted, status, go-live, months, million, population, earlier, arrangement, sentence, points, dictionary, take-over, survival, sample, platform, silent, agency, truncation, reading

## 3 answer figures in the pack (REVIEW 4)
- **REVIEW** `CRM-ECL-04_expected_credit_loss_personal_loans.docx`: golden figure 7.1 appears: ...e modelled allowance. 7. Limitations 7.1 PD is set by product and month on book only. Risk...
- **REVIEW** `scorecard_v4_migration_note.pdf`: golden figure 560 appears: ...point. Selected scores on the two scales: v3 520 560 600 640 680 720 760 800 v4 564 609 654 699 744 78...
- **REVIEW** `scorecard_v4_migration_note.pdf`: golden figure 680 appears: ...ted scores on the two scales: v3 520 560 600 640 680 720 760 800 v4 564 609 654 699 744 788 833 878 Ap...
- **REVIEW** `CRM-ECL-04_expected_credit_loss_personal_loans.docx`: carries 9 of 10 distinctive words of the committed call: 'Book a collective expected credit loss allowance of AUD 13.2 million on the PL36 and PL60 personal loans at 30 September'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `CRM-ECL-04_expected_credit_loss_personal_loans.docx`: 6 of 25 stump-paragraph terms appear (record, repayment, status, months, arrangement, points); read whether the document names the move
- **REVIEW** `ecl_extract_dictionary.txt`: 10 of 25 stump-paragraph terms appear (record, repayment, drawdown, status, months, earlier); read whether the document names the move

## 9 dates after the setting (REVIEW 3)
- **REVIEW** `hardship_register_2026-09-30.xlsx`: 742 ISO dates after 2026-10-12, e.g. 2026-10-13, 2026-10-14, 2026-10-15, 2026-10-16, 2026-10-17
- **REVIEW** `loan_record_2026-09-30.parquet`: 865 ISO dates after 2026-10-12, e.g. 2026-10-13, 2026-10-14, 2026-10-15, 2026-10-16, 2026-10-17
- **REVIEW** `personal_loan_book_2026-09-30.csv`: 864 ISO dates after 2026-10-12, e.g. 2026-10-13, 2026-10-14, 2026-10-15, 2026-10-16, 2026-10-17

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read (round 2)

Q1 to Q4: none (CRM-ECL-04 3.3 says what the loss share measures, not how to assemble it; no allowance, stage amount, loss share or stage count is filed; the dictionary, the migration note and the scenarios workbook are named for their purposes; the March 2026 recoveries spike is the debt sale the dictionary records). Q5: CRM-ECL-04 1.1 to 4 executed word for word give the allowance; not computed. Q6: an analytical choice, the PD curve from the loan record as a hazard conditional on survival (3.2's sentence); the reader noted it leaves open how loans enter the at-risk set, without naming the take-over. REVIEW lines: all harmless (a section number, conversion-table points, shared ECL vocabulary, future repayment and arrangement-end dates inside the 30 September extracts). Realism: "the significant-increase scalar of 2.4" sits beside an unrelated section 2.4 (minor). Readings: the stage-movement slide (stage 3 and written-off loans among "the number in each stage" or "closed"; the 30 June book's score field); the loss share balance-weighted (3.3: a share of the balance at default); the allowance's LGD (the procedure's 70 and 76 per cent, the prompt's "will be set" being future).

The read above was made on the cut before the round 2 asks repair. The repair changed two documents under `target/`
(CRM-ECL-04 2.2, 3.3 and its version history; the dictionary's loan book paragraph, the receipts file's loan_no, the
placement report's Agency Ref and the job's change log), so the targeted re-read is owed on the current cut.

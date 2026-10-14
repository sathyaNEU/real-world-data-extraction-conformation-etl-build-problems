# leak check, task133

**Verdict: REVIEW.** 15 files read, 26 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: record, taken-over, device, repayment, asserted, decisive, drawdown, status, million, dictionary, population, earlier, go-live, months, extract, silent, arrangement, sentence, points, take-over, survival, sample, platform, counts, agency

## 3 answer figures in the pack (REVIEW 4)
- **REVIEW** `CRM-ECL-04_expected_credit_loss_personal_loans.docx`: golden figure 7.1 appears: ...modelled allowance. 7. Limitations 7.1 PD is set by product and month on book only. Risk...
- **REVIEW** `scorecard_v4_migration_note.pdf`: golden figure 560 appears: ...point. Selected scores on the two scales: v3 520 560 600 640 680 720 760 800 v4 564 609 654 699 744 78...
- **REVIEW** `scorecard_v4_migration_note.pdf`: golden figure 680 appears: ...ted scores on the two scales: v3 520 560 600 640 680 720 760 800 v4 564 609 654 699 744 788 833 878 Ap...
- **REVIEW** `CRM-ECL-04_expected_credit_loss_personal_loans.docx`: carries 9 of 10 distinctive words of the committed call: 'Book a collective expected credit loss allowance of AUD 13.2 million on the PL36 and PL60 personal loans at 30 September'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `CRM-ECL-04_expected_credit_loss_personal_loans.docx`: 6 of 25 stump-paragraph terms appear (record, repayment, status, months, arrangement, points); read whether the document names the move
- **REVIEW** `ecl_extract_dictionary.txt`: 11 of 25 stump-paragraph terms appear (record, repayment, drawdown, status, dictionary, earlier); read whether the document names the move

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

## Solver's-eye read (targeted, after the asks repair)

On CRM-ECL-04 and the extract dictionary. Q1 to Q4: none for the main allowance (3.2 and 2.4 are method rules naming no step; no file states an allowance, stage amount, loss share or count; the policy's 70 and 76 per cent are the rates in force). Q5: 3.7, 1.1, 3.1, 3.2 and 4 fix the per-loan sum over loans open and under 90 days at 30 September; not computed. Q6: analytical (estimating PD(k) from the loan record as a conditional hazard); the take-over not found. Realism: pre-emptive justifications in 2.4 and 3.6; 3.3 long and steering against the Collections file; the version history names the areas 3.3 and 2.2 changed; the dictionary's snapshot provenance line and pause explanation pointed. These bear on the asks' devices (A2, B3, the cure rule), not on the main call; the asks' residual pair risk is recorded in the design note. Readings: slide 2's stage 3 and closed (the dictionary: a closed loan is in no stage); the 2.4 scalar against section 2.4; the stacked scalar and multiplier capped at one; the long-tail month on book; September 2026 drawdowns' month on book; the financial-year 2023-24 and quarter of default; the sale proceeds per account; stage amounts as allowance by stage (section 5).

## After the round 2 re-judge (2026-10-14, leak.py only)

The prescribed fix and the realism softening changed two documents under `target/`: the dictionary's two loan book lines now
carry each extract's run clock (June's days_past_due counted to the run date, 1 July; September's to the reporting date)
and CHG-26-0418 reads as a plain change line; CRM-ECL-04 drops the justifications in 2.4 and 3.6 and the Collections
clause in 3.3, and its 4.2 history line reads "Annual review: 2.2 and 3.3 revised". leak.py --asof 2026-10-12 above:
REVIEW, no LEAK, the same REVIEW lines as before. The pause explanation in the hardship register's entry is kept: 3.2's
remaining term on the main call reads it.

## After round 2c (2026-10-14, leak.py only; the re-read and re-judge are owed)

Round 2c changed under `target/`: `behaviour_score_runs_2026-03_2026-08.parquet` (a `score_status` column and its
description; the June month end's partition carried forward in the run dated 1 July and rescored in a run dated 2
July), `CRM-ECL-04_expected_credit_loss_personal_loans.docx` (section 5 and the 4.1 history line report to the Audit and
Risk Committee) and `hardship_register_2026-09-30.xlsx` (the job account's last-modified-by persona). leak.py --asof
2026-10-12 above: REVIEW, no LEAK, the same lines as before (the dictionary's stump-term overlap now 11 of 25, the
subject's own words). Neither the dictionary nor the policy mentions the rerun (asserted in `checks.py`).

## Solver's-eye read (targeted, round 2c)

On the prompt, the scoring runs parquet, CRM-ECL-04 section 5 and its history, and the dictionary. Q1 to Q4: none. Q5: 3.7 with 1.1, 2.1 and 3.1 (the per-loan sum over stage 1 and 2 loans at 30 September); 3.2's PD estimand stated; not computed. Q6: the reader called the filed text mostly rule application and semantics because it found no step on the main figure beyond 3.2's PD construction; it did not find the October 2019 take-over (delayed entry), which no sentence names and which the judge has twice ruled the analytical decisive step (Gate H). Its rule-application points (2.2, 3.2's pause, the June clock, the carried-forward scores) all sit on the asks, which rule 3 does not bind. Realism: pre-emptive clauses (3.2's pause reason, 3.3's measure, 7.1's no-smoothing, 2.4's no probation); history rows pointing at revised sections, section 5 one line under "restated"; the dictionary's current_score_v4 added 21 July against a 2 July rerun (the book column, not the scoring file). Readings: slide 2's stage 3 and closed (the dictionary: a closed loan is in no stage); which June run governs (the device B4, resolvable from score_status); the June clock (filed); section 5's coverage ratios beyond the prompt.

# leak check, task133

**Verdict: REVIEW.** 20 files read, 21 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: borrower, record, register, division, industry, decisive, taken-over, credits, asserted, repayment, product, drawdown, sentence, allowance, take-over, system, sector, nothing, receipts, go-live, carries, trading, multiplier, textbook, cr-st-

## 3 answer figures in the pack (REVIEW 6)
- **REVIEW** `CR-ST-02_ICAAP_stress_testing_business_banking_v3.1.docx`: golden figure 2.1 appears: ...rd. 2. Scenario and stress year 2.1 The stress applies the severe scenario the Board...
- **REVIEW** `CR-ST-02_ICAAP_stress_testing_business_banking_v3.1.docx`: golden figure 1.3 appears: ...re stressed under CR-ST-03 and CR-ST-04. 1.3 A facility of a customer in default at the book d...
- **REVIEW** `CR-ST-02_ICAAP_stress_testing_business_banking_v3.1.docx`: golden figure 3.4 appears: ...No security held 75 3.4 A revolving facility (a business overdraft or a r...
- **REVIEW** `CR-ST-02_ICAAP_stress_testing_business_banking_v3.1.docx`: golden figure 2.4 appears: ...Date Change 2.4 July 2024 Stressed LGDs...
- **REVIEW** `CR-ST-02_ICAAP_stress_testing_business_banking_v3.1.docx`: carries 11 of 13 distinctive words of the committed call: 'The severe scenario puts NZD 11.5 million of stressed credit loss on the business banking book in the stress year to 30 '
- **REVIEW** `rural_book_stress_summary_ICAAP_2026.pdf`: carries 10 of 13 distinctive words of the committed call: 'The severe scenario puts NZD 11.5 million of stressed credit loss on the business banking book in the stress year to 30 '

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `CR-ST-02_ICAAP_stress_testing_business_banking_v3.1.docx`: 7 of 25 stump-paragraph terms appear (borrower, register, division, system, carries, multiplier); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read (the isolated leak reader, architecture 3)

### Leak reader, round 1 (2026-11-01, isolated, Sonnet at medium effort, on target.zip d613bac0)

1. Decisive step: none announced. CR-ST-02 states the procedure: stressed PD is the 12-month PD times the Table 2 multiplier "for the fall in the borrower's own sales over the stress year under the scenario"; "a borrower's segment follows its own division on the NZBN register"; the risk grade is the model grade or an override in force.
2. No file ranks or scores anything on the question (the rural PDF is another book; the scenario workbook gives divisional sales changes only).
3. No helper file outright (CR-ST-02 governs; the scenario workbook is a required input).
4. Nothing reads as the answer (the only totals are the rural book's, context).
5. CR-ST-02 3.1: a facility's stressed loss is stressed PD x stressed LGD x EAD, summed over the book; 4.2 and 4.3 fix the net credit loss per half and the default counts and shares per band.
6. The reader's answer: "following a stated rule or procedure (CR-ST-02 3.1 to 3.4, 4.1 to 4.3), plus reading fields and codes correctly (override validity dates, NZBN division against the book's industry_code, the customer merge log, the grade D exclusion). Nothing in the pack names an analytical choice as the stump. This is a Rule 2/3 concern for the author: the pack is largely semantics and rule execution."
Sweep flags: CR-ST-02's shared numbers and call words harmless (filed PD, multiplier and LGD tables; no loss figure); its shared vocabulary names the procedure, no pitfall (mild at most); the rural summary harmless (another book, excluded by 1.2, no business figure or method).
Realism: none clearly generated; one note: the override reasons in grade_overrides_2024-2026.xlsx look randomly assigned (reason text does not match the direction of the grade change).


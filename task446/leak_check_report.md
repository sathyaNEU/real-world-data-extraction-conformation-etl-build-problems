# leak check, task446

**Verdict: REVIEW.** 18 files read, 68 golden figures and 15 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: history, decisive, membership, quarter, relationship, semantics, domain, analyst, netting, lapsed, obligor, hierarchy, standard, formula, point-in-time, collateral, asserted, committed, window, reference, concentration, holdings, pairing, financial, quarter-ends

## 3 answer figures in the pack (REVIEW 6)
- **REVIEW** `credit_committee_agenda_20261104.docx`: golden figure 14.0 appears: ...Pellow Term loan GBP 14.0m 5 years chilled distribution...
- **REVIEW** `credit_committee_agenda_20261104.docx`: golden figure 25.0 appears: ...Revolving credit facility GBP 25.0m 3 years fleet replacement, 2...
- **REVIEW** `credit_committee_agenda_20261104.docx`: golden figure 20.0 appears: ...uneck (Germany) Term loan GBP 20.0m 3 years working capital for...
- **REVIEW** `credit_committee_agenda_20261104.docx`: golden figure 12.0 appears: ...Meridale Term loan GBP 12.0m 4 years new corrugator line,...
- **REVIEW** `credit_committee_agenda_20261104.docx`: carries 6 of 8 distinctive words of the committed call: "Credit committee should approve GBP 21.8m of Kelderby Facilities Ltd's GBP 30.0m term loan."
- **REVIEW** `limit_monitoring_standard_LMS-03.pdf`: carries 5 of 8 distinctive words of the committed call: "Credit committee should approve GBP 21.8m of Kelderby Facilities Ltd's GBP 30.0m term loan."

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `crdm_extract_log_20261009.txt`: 6 of 25 stump-paragraph terms appear (quarter, relationship, obligor, collateral, window, reference); read whether the document names the move
- **REVIEW** `crdm_field_reference.md`: 7 of 25 stump-paragraph terms appear (quarter, relationship, netting, obligor, collateral, committed); read whether the document names the move
- **REVIEW** `credit_concentration_policy.pdf`: 10 of 25 stump-paragraph terms appear (quarter, relationship, netting, lapsed, obligor, standard); read whether the document names the move
- **REVIEW** `limit_monitoring_standard_LMS-03.pdf`: 5 of 25 stump-paragraph terms appear (quarter, obligor, standard, concentration, quarter-ends); read whether the document names the move

## 6 ranking artifacts (REVIEW 3, INFO 1)
- **REVIEW** `gleif_lei_records_qe_archive.csv`: names 13 of 15 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `house_limit_register_20260930.xlsx`: names 6 of 15 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `loan_book_qe_extracts.csv`: names 10 of 15 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `credit_committee_agenda_20261104.docx`: names 6 of 15 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 2)
- **REVIEW** `loan_book_cwb_dub_20251231_late.csv`: 226 ISO dates after 2026-11-04, e.g. 2027-07-03, 2027-07-05, 2027-07-08, 2027-07-12, 2027-07-18
- **REVIEW** `loan_book_qe_extracts.csv`: 13800 ISO dates after 2026-11-04, e.g. 2027-07-01, 2027-07-02, 2027-07-03, 2027-07-04, 2027-07-05

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt form (clean)

## Solver's-eye read

One isolated reader (Sonnet), 2026-10-11, on a fresh scratch copy of prompt.md and target.zip.

- **Q1 (decisive step named):** none. Closest: `limit_monitoring_standard_LMS-03.pdf` s.2.2 and s.2.3 ("Projections are made for each Obligor Group as constituted at the projection date, from that group's exposure at each of the five quarter-ends"), read by the reader as the method's stated estimand rather than an announcement; it does not say how the past quarter-ends are to be rebuilt.
- **Q2 (file ranks the candidates):** none.
- **Q3 (file exists only to help):** none clearly; `crdm_extract_log_20261009.txt` and `crdm_field_reference.md` read as real data-mart release notes, with the late-delivery paragraph and the rerun/`migrated_from` notes the most helpful lines.
- **Q4 (figure reads as the answer):** none.
- **Realism tells (deferred to 6b):** house limit register name stems and uniform review-date cadence; round limits; case variation in customer names reads slightly planted.
- **Forks:** none on the main call that the pack leaves open; projecting past year-end is ruled out by the prompt's "projected year-end exposure"; Dublin, migrated facilities and the late file settled by the field reference and the log.
- **REVIEW lines:** agenda request amounts, word overlap, stump-term hits, LEI and facility rows, maturity dates after the setting: all harmless.

Main-thread disposition: no question 1 to 3 finding and no main-call fork, so nothing is fixed before the round. The reader's reading of LMS-03 s.2.3 as a stated rule is the Gate H question for the judge (the estimand is pinned as the standard requires; rebuilding the past quarter-ends on today's membership is the analyst's construction). Deferred to stage 6b: the register's review-date cadence and the customer-name case variation.

# Verdict: task133 round 2c (re-judge)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No repair is required and no rerun is needed. Three residual forks are listed under Evidence as optional pins. Pinning them would change what solvers see, so they are not FIX_NOW items.

**Why:** Every committed figure reproduces from the shipped files, and the literal reading of CRM-ECL-04 3.2 forces the allowance to 13.2 (10.6 + 2.6).
- Two independent PD estimators land on the same rounded answer. One chains pooled monthly hazards; the other takes the literal cohort share of loans open and not in default at the end of month a that first default in month a+k. Both give 10.59 / 2.60 / 13.19.
- The LGD shares and the slide-2 counts reproduce exactly.
- The decisive method step is left-truncation and competing risks in the PD read. The record starts at go-live and holds none of the earlier platform's loans that defaulted or closed before then. That is analytical. Residual forks exist but none flips a rounded committed figure on a reasonable reading (see Evidence).

## Evidence (recomputed from target/)

| Item | Golden | My recomputation | Source |
|---|---|---|---|
| Stage 2 loans, 30 Sep | 3,266 | 3,266 (stage 1 = 37,288; stage 3 = 343) | personal_loan_book_2026-09-30.csv, hardship_register (dates, cancel date ends force), v3 to v4 = round(1.12 v3 - 18) |
| PD multiplier | 1.06 | 0.55 + 0.30x1.28 + 0.15x0.81 = 1.0555 | ifrs9_scenarios_2026Q3.xlsx, sheet "Q1 FY27" |
| Stage 1 allowance | 10.6 | 10.584 (chain); 10.588 (cohort) | loan_record parquet, book, CRM 3.1 to 3.5 |
| Stage 2 allowance | 2.6 | 2.594 (chain); 2.599 (cohort) | same |
| Total | 13.2 | 13.178 / 13.187 | same |
| LGD shares (8 cells) | 67.9, 65.8, 70.7, 70.9, 70.2, 77.4, 73.2, 79.3 | 67.90, 65.81, 70.71, 70.92, 70.20, 77.39, 73.23, 79.33 | collections_defaults, receipts, placements, debt_sale schedule |
| Slide 2 (four groups x stage 1, 2, 3, closed) | e.g. PL36 S1: 14,470 / 680 / 42 / 1,586 | all 16 cells identical | 30 June book, score runs, 30 Sep book |

**PD sensitivity (allowance, AUD m)**

| Variant | Result | Status |
|---|---|---|
| Delayed entry at go-live plus competing-risk chain (golden) | 13.18 | forced |
| Delayed entry, literal cohort share | 13.19 | same answer |
| Counted from drawdown, ignoring truncation | 11.55 | easy wrong route |
| Repayment treated as censoring | 14.07 | contradicts the literal 3.2 probability |

**Other robustness checks**
- Multiplier 1.0555 versus 1.06 versus scenario-by-scenario weighting: stage 1 is 10.63 or 10.58, stage 2 is 2.61 or 2.59, so the rounded values do not move.
- The stage 1 lead over the 10.55 rounding edge is about 0.3 percent (10.584). That is thin but deterministic; both estimators clear it.
- The tail hazard cells with few loans (PL36 month 39 onwards, PL60 month 63 onwards) carry about AUD 3k, so they are not decisive.
- No repayment day is above 28, so the NSW holiday calendar, which is not shipped, cannot change the 30 Sep due count. A scheduled date of 28 Sep or earlier cannot be pushed past 30 Sep.
- No hardship start, end or cancellation falls on 30 Sep, so inclusive versus exclusive boundaries do not matter.

**LGD checks**
- Recoveries over all receipts to Sep 2026 reproduce the golden. A 24-month cap would give different figures (71.1 for PL36 Q3-23). The cap is ruled out by 3.3 "since" and by "including the proceeds of any sale of the debt", because the March 2026 sale is more than 24 months after default.
- Remittances map to loans by Agency Ref plus the placement window. The posted loan_no is wrong on 2,034 remittance lines, because refs are reused after a placement closes. 1,010 of those lines sit on 2023-24 defaulted loans. Using the posted loan_no gives different shares (66.0 for PL36 Q3-23).
- The window mapping is supported by the wirraway file ("reference ... while it is placed"). Every remittance falls inside exactly one placement window.
- Debt-sale proceeds are face x 3.85 cents. They sum to 1,800,666.58, matching the receipt of that amount, and are booked in March 2026.
- Cure rule: 59 loans that Collections calls "Cured" are written off in the loan record. 3.3 says to measure those on recoveries; following Collections instead gives 62.1 for PL36 Q3-23.
- Discounting is monthly at the contract rate, as 3.3 and 3.5 state.

**Slide-2 checks**
- The 30 June extract counts days past due to 1 July, so one day is subtracted. Without this, PL36 stage-2 loans still in stage 1 at 30 Sep change from 468 to 488.
- 7,731 loans are "Carried forward" in the 2026-07-01 score run and re-scored on 2026-07-02. Using the rerun gives the golden; ignoring it does not.
- The 1,353 loans with no run before first repayment use the application score on the v4 scale, which is stated in the dictionary.

**Literal-reading forks recorded (none flips a rounded committed figure on a reasonable reading)**
1. CRM 7.1 says "the record's experience is used as it stands". A reader could use it to resist the go-live correction and file 11.6. This is rebutted by the dictionary: the loan system took over the book at go-live. It is also rebutted by the data, where the earliest default_month is 2019-10 and no loan closed before Oct 2019.
2. Loans that defaulted and later cured (761 open, 462 repaid) are removed from the at-risk set at first default. The record has no cure date. Keeping them in the denominator from the default month onward is an upper-bound case, since it assumes instant cure. It gives 10.51 / 2.57 / 13.08, which would round to 10.5 and 13.1. The words "first defaults" support exit at first default. This is the single residual risk to Gate C and it is low.
3. The 2026-07-01 "Carried forward" rows and the 2026-07-02 rerun are not documented in the dictionary. This is a data-semantics step on slide 2 only. It is a mild fork, because a carried-forward value is evidently not a fresh score.

Cross-batch fingerprint: not performable. Reading other task folders is forbidden by the brief.

## Files/Hygiene
**PASS.**
- 15 files in 6 formats: docx, xlsx (4), parquet (2), csv (6), txt and pdf.
- Row counts: 103,566 in the loan record and 238,553 in the score runs, so a 25k-plus file is present.
- Distractors that are relevant but unused: the prior-quarter scenario sheet, arrears_roll_rates_fy26.xlsx, the scorecard grade bands, and the reused Wirraway refs.
- No authoring or benchmark language found in the files read.
- Dates are consistent. The dictionary was updated 2 Oct 2026, CRM-ECL-04 is effective 1 Sep 2026, and the scenarios were approved 18 Sep, before the reporting date.
- The fiction (Bellbird, Wirraway, Tarwin) is internally coherent and not public data. Nothing is exclusion-level.
- I did not verify file licence or source metadata, because metadata.json is forbidden to me.
- Dictionary and CRM-ECL-04 read like genuine operating documents. The CRM doc has an empty "8.2 Sign-off" heading above a populated table, a small tell that does not need fixing.

## Stump power (Gate F)
**Moderate to good.** The main call needs three things together:
- Delayed entry for the taken-over loans.
- A competing-risk chain with repayment as a rival exit, not censoring.
- Correct month-on-book and remaining-term mechanics.

The easy routes give 11.6 (counted from drawdown) or 14.1 (repayment as censoring). A strong analyst will probably see the go-live note, but must turn it into a left-truncation correction. The graded asks add several independent traps for the careful solver:
- reused Wirraway refs;
- the Collections "Cured" versus loan-record write-off conflict;
- debt-sale allocation by face value;
- the one-day days-past-due offset;
- the 2 July rerun of scores.

Together these should keep the top-two average down on the ask side. I did not see contrasting model responses, so the empirical bar is not assessed.

## Stumping type (Gate G)
`mechanism: statistical_rigor (survival / delayed entry with competing risks, plus method selection)`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.

No reported number or stakeholder conclusion is overturned. The task builds a number from honest, correctly stated data. The record's go-live coverage is documented in the dictionary and in the data, and the correct treatment is standard survival practice. Borderline note: the clean-data test could be argued either way. Without the predecessor-platform truncation, the chain estimate would be the naive one. But the stump is the analytical selection issue, not a corrupted value.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`

- **H1:** the deciding quantity is a lifetime ECL built on an empirical PD term structure and realised LGD, which a credit-risk team estimates. It fails the swap test for another field.
- **H2:**
  - Layer 1 is messy data: day-offset extracts, a rerun score file, reused agency refs, stale hardship statuses and conflicting cure records.
  - Layer 2 is survival-style PD estimation with delayed entry and competing risks.
- **H3:**
  - The easy route is to count every record loan from drawdown and chain hazards. A strong analyst who cleaned the data and read every field would file 11.6 (stage 1 9.2, stage 2 2.3). Repayment as censoring gives 14.1.
  - The answer is 13.2.
  - The decisive step is not data semantics or rule application. The stage 2 count, scenario weight and mechanics are rule application, but they are lower steps.

## Fix
**none.** Optional, with a rerun cost, only if the author wants fork 2 closed: one sentence in CRM 3.2 or the dictionary saying a loan that has defaulted leaves the at-risk set at its first default.

## Disposition (2026-10-14)

APPROVE accepted; the build reships with no change to the pack (`target/`, `target.zip` and `golden/` are the round 2c
cut, rebuilt byte-identical).

The optional pin on exit at first default (fork 2 above) is not taken, for two reasons: CRM-ECL-04 3.2's estimand already
says the probability that a loan open and not in default at a "first defaults in month on book a + k", so a loan leaves
the loans at risk at its first default; and the only variant that moves a figure keeps the defaulted loans at risk from
their default month, an instant cure the data do not support (the record carries no cure date, and 343 of the 761
defaulted loans still open are 90 or more days past due at 30 September). The fork is recorded as SF35 in the design
note and asserted in `generator/checks.py`: kept at risk, the 1,223 defaulted loans not written off or settled book
AUD 13.1 million (10.5, 2.6), the judge's 13.08.

Forks 1 and 3 stay as they are: 7.1's "as it stands" against the dictionary's go-live sentence is the stump's own ground
(the record holds what the loan system held), and the scoring file's status column and run dates resolve the 2 July
rerun (SF34, asserted). The empty-looking "8.2 Sign-off" heading above its table is left, as the judge advised.

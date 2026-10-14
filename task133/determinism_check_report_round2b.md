# Verdict: task133 round 2 (re-judge)

- **Verdict:** NOT_DETERMINISTIC (narrow: slide 2 only). The main allowance (13.2), the stage amounts (10.6 / 2.6) and the eight LGD shares are forced and reproduce. The 16 slide-2 counts reproduce only after an undocumented one-day correction to the 30 June extract's days_past_due.
- **Disposition:** FIX_NOW. Pin the June extract's dpd basis in `ecl_extract_dictionary.txt` (or restate the June `days_past_due` as at close of business 30 June). The main call, stage amounts, LGD and the Sept staging are untouched, so only the slide-2 asks would need regrading.
- **Why:** The literal reading of `personal_loan_book_2026-06-30.csv` (dpd as given, 30+ to stage 2, 90+ to stage 3) gives different slide-2 counts from the golden's, and no shipped sentence says the June dpd is struck at the run date (1 July) rather than at the 30 June close (CRM-ECL-04 1.3). The golden is right in principle (1.3 says close of business on the reporting date) but a literal solver and a reconciling solver get two different, both-defensible answers. Gate C/B on the slide-2 supplementary answers. Taxonomy: `underspecified_objective` (as-at basis of a field never pinned). Everything else is forced.

## Evidence (recomputed from the bundle)

| Item | Golden | My recompute | File / field |
|---|---|---|---|
| Stage 2 loans at 30 Sep | 3,266 | 3,266 (PL36 1,422, PL60 1,844); stage 3 = 343 | `personal_loan_book_2026-09-30.csv` days_past_due, origination_score (v3 to v4 = round(1.12 x v3 - 18), no ties), current_score_v4; `hardship_register` in force 30 Sep, cancelled_date respected (744 arrangements are cancelled before their start) |
| PD multiplier | 1.06 | 0.55 + 0.3 x 1.28 + 0.15 x 0.81 = 1.0555 | `ifrs9_scenarios_2026Q3.xlsx` sheet "Q1 FY27 scenarios" (not the prior sheet) |
| Stage 1 ECL | 10.6 | 10.629 (1.06) / 10.584 (1.0555) | PD from `loan_record` with delayed entry (see below); EAD annuity on current_balance over remaining term; DF at contract rate; 12 months or remaining term |
| Stage 2 ECL | 2.6 | 2.606 / 2.595 | same, with the 2.4 scalar; remaining term, pause dates counted as fallen due |
| Allowance | 13.2 | 13.235 / 13.18, both display 13.2 | the 13.235 sits 0.015m under the 13.25 rounding line, which is thin, but the exact multiplier moves it away from it |
| LGD (8 cells) | 67.9, 65.8, 70.7, 70.9 / 70.2, 77.4, 73.2, 79.3 | 67.90, 65.81, 70.71, 70.92 / 70.20, 77.39, 73.23, 79.33 | `collections_defaults_2023-24.csv` x `collections_receipts` x `wirraway_placements` x `debt_sale` x `loan_record`; all 8 reproduce |
| Slide 2 (16 counts) | PL36 s1: 14,470 / 680 / 42 / 1,586; PL36 s2: 468 / 658 / 115 / 123; PL60 s1: 17,724 / 831 / 46 / 1,180; PL60 s2: 560 / 942 / 140 / 112 | literal: PL36 s1 14,450 / 680 / 39 / 1,582; PL36 s2 488 / 658 / 118 / 124; PL60 s1 17,706 / 830 / 43 / 1,176; PL60 s2 578 / 943 / 143 / 113. With June dpd minus 1 day: exactly the golden, all 16 | `personal_loan_book_2026-06-30.csv`, score from the 2026-07-01 run of `behaviour_score_runs` (100% coverage of the 30 June book; the 1,353 loans before first repayment hold the application score, so no fall) |

**The PD method and its forks.** Hazards are by product and month on book from `loan_record`, with each taken-over (pre-October-2019) loan entering the at-risk set only from calendar month 2019-10. PD(k) = default share at a+k times the product of (1 - default share - closed share) over a+1 to a+k-1.

| Reading | Stage 1 / Stage 2 / Total (AUD m) |
|---|---|
| Golden: delayed entry, competing risks | 10.63 / 2.61 / 13.2 |
| Every loan counted from drawdown (left truncation ignored) | 9.27 / 2.33 / 11.6 |
| Repayment treated as censoring | 11.22 / 2.92 / 14.1 |
| Post-go-live cohorts only | 10.65 / 2.63 / 13.3 |
| Truncation start moved to Nov 2019 | 10.62 / 2.61 / 13.2 |

The first alternative is the intended trap. It is licensed against the filed text because the dictionary says the record holds only loans the system held from 1 Oct 2019 (loans closed or defaulted earlier never came across). Post-go-live-only breaks CRM 3.2's "every loan of its product in the loan record". The censoring route is excluded by 3.2's wording: it is a probability for a loan open at a, so a repaid loan cannot default. I find the first alternative the only fork that moves the answer by more than rounding, and it is a method choice the data's own structure settles.

**The slide-2 offset.** I rebuilt each loan's implied oldest due date as (report date - dpd) and compared it to the schedule day (first_repayment_date day of month, allowing for the next-business-day shift the dictionary states).
- Sept book: matches with dpd counted to 30 Sep (0 days of shift in the data, 70% exact, the rest the stated weekend shift).
- June book: matches only if dpd is counted to 1 July (64% exact against 19% for 30 June).
- Cross-check: 6 loans with June dpd = 90 have `default_month` = 2026-07 in the record (3 PL36, 3 PL60, exactly the golden's stage-3 shift); 20-odd loans per product at dpd 30 drop to 29.
- Nothing in the dictionary says the June dpd is struck at the run date; the Sept file, also run on the 1st of the next month, is not.

Competing answers surviving: literal June staging gives the counts in the table's literal row; reconciled staging gives the golden. Both are defensible from the shipped files, which is the fork.

**Other fork checks.** Cure by the loan record (not Collections' own "Cured" flag) per CRM 3.3: 62.1 / 57.0 / 66.2 / 68.1 / 68.3 / 70.7 / 68.8 / 75.6 if Collections' flag is used, so 3.3 is what pins it. Agency remittances must be re-posted to the Wirraway reference in the narrative, and the Agency Ref is reused across placements (676 repeats), resolved uniquely by placement dates for all 20,902 receipts; ignoring that gives 66.0 / 64.1 / 69.7 / 69.7 / 69.7 / 75.7 / 72.2 / 78.4. The debt-sale proceeds allocated by face value at 3.85c, undiscounted recoveries or omitted sale each move the shares by 1.4 to 5 points. Each is pinned by 3.3 and the shipped schedule, so the LGD asks are forced.

## Files/Hygiene
PASS. 15 files, formats: docx, xlsx (4), parquet (2), csv (5), txt, pdf. In-world artefacts with plausible authorship and metadata; no tracked changes, hidden sheets or comments in the docx or xlsx files; no authoring or synthetic disclosures; dates coherent (CRM v4.2 approved 25 Aug 2026, scenarios approved 18 Sep, dictionary 2 Oct; `current_score_v4` added 21 Jul 2026 so the June extract rightly has no score column). Distractors present (`arrears_roll_rates`, `write_offs`, the scorecard grade bands, the prior-quarter scenario sheet). Public-data contamination: none. Not exclusion-level. The cross-batch fingerprint could not be run from inside this isolation; no match is claimed or excluded.

## Stump power
High on the main call. A strong analyst who cleans the data and follows CRM 3.2 word for word can still count every record from drawdown (11.6 instead of 13.2) or treat repayment as censoring (14.1); the dictionary mentions the October 2019 take-over but nothing in a file names the consequence. The LGD asks add independent traps (reused agency references, lump-sum sale proceeds, record-based cure) and slide 2 adds the dpd-offset trap. No too-easy signals: no shipped document ranks the candidates or documents the defect.

## Stumping type
`mechanism: method_or_model_selection` (term-structure estimator with delayed entry and competing risks), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. No reported figure is shipped to be rejected; the difficulty is estimator choice on correctly kept records. (Borderline note: the stump would vanish if the earlier platform's closed loans were present, but that is the record's selection structure, not an error in it.)

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Swap test fails to transplant: the deciding quantity is a lifetime-PD term structure and realised discounted LGD under AASB 9, which only a credit-risk team would estimate. Layer 1: five extracts at different grains, v3 to v4 score conversion, hardship dates and cancellations, reused agency references, a lump-sum debt sale. Layer 2: delayed-entry, competing-risk hazards from a take-over book. Easy route: count each loan from drawdown (or censor repayments), giving 11.6 (or 14.1) against 13.2.

## Fix
- **Where:** input_files (one dictionary sentence), leaving the golden's slide-2 numbers as they are.
- **Change:** in `ecl_extract_dictionary.txt` section A, state that `days_past_due` in the 30 June extract is counted to the run date (1 July) while the 30 September extract's is counted to the reporting date, and that CRM 1.3's close-of-business basis governs staging. Alternatively regenerate the June `days_past_due` as at 30 June (each positive value minus 1), which reproduces the golden exactly. Do not re-key the golden to the literal counts while the file still carries the offset, since a reconciling solver would then fork the other way.
- **Not needed:** nothing else; the main call, stage amounts and LGD stand, with 13.2 holding under both the 1.06 and exact 1.0555 multiplier.

## Disposition (2026-10-14)

The prescribed fix applied, asserted. `ecl_extract_dictionary.txt` section A now records each loan book extract's run
clock on its own line: `personal_loan_book_2026-09-30.csv`, run 1 October 2026, every loan open at close of business on
30 September 2026, days_past_due counted to the reporting date, 30 September 2026; `personal_loan_book_2026-06-30.csv`,
run 1 July 2026, every loan open at close of business on 30 June 2026, days_past_due counted to the run date, 1 July
2026. CRM-ECL-04 1.3 (close of business on the reporting date) is unchanged, so the June values in arrears are put back
a day for staging at 30 June.

Asserted in `generator/checks.py` (SF25) and `generator/verify.py`: the verifier parses both clocks from the dictionary
(June one day after its close, September none); the literal reading with the June clock gives all sixteen golden counts
(PL36 stage 1 14,470 / 680 / 42 / 1,586, PL36 stage 2 468 / 658 / 115 / 123, PL60 stage 1 17,724 / 831 / 46 / 1,180,
PL60 stage 2 560 / 942 / 140 / 112); the column read unadjusted gives the judge's literal row and moves 14 of 16.

Also changed, no fork depending on them: CRM-ECL-04 2.4 and 3.6 lose their pre-emptive justifications, 3.3 loses
"whatever resolution Collections recorded" (the record clause still says a loan written off or settled for less did
not return to performing), the 4.2 history line reads "Annual review: 2.2 and 3.3 revised", and CHG-26-0418 reads
"current_score_v4 added; extract taken from the quarter-end end-of-day snapshot". The judge's three loss-share forks
(the cure by the record, the remittance attribution, the sale and discounting) stay closed and asserted.

Frozen and unchanged (`freeze.py check --mode determinism` PASS): the allowance AUD 13.2 million (stage 1 10.6, stage 2
2.6), 3,266 stage 2 loans, the multiplier 1.0555, the eight loss shares and the sixteen counts.

Consequence for the asks: the fix makes ask B's only device (the June clock) literal, so a careful reader keeps all 16
counts. Pair simulation: 65.2 with both top responses executing the clock (49.1 if only the cracker does; 33.1 if
neither); `precut.py` fails its three ask lines (pair ceiling, mirror leakage, the cracker keeping ask B).

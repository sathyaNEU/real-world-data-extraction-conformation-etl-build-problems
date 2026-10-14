# determinism-check report, task133, 2026-10-14, round 2

The judge ran at stage 4 of the round 2 build, isolated, at medium effort, on a fresh unzip of the committed
`target.zip` (3db99aa, sha256 `8b017e00...3927`; the judged folder is byte-identical to it). Its verdict is reproduced
verbatim below (`verdict.md`, sha256 `a9b659fc1e80bf30...`). The disposition after it was written by the build session,
which reads the design note, and is not part of the judge's thread.

## Verdict (verbatim)

# Verdict, task133 round 2 (adversarial, bundle only)

**Verdict:** NOT_DETERMINISTIC (main recommendation is forced and reproduces; two supplementary blocks do not: the LGD table and the slide-2 stage counts).

**Disposition:** SEND_BACK (light). Leave the allowance side untouched. Pin in the filed text how a loan that Collections labels Cured but the loan record later shows Written off is treated in the LGD, state pooled-by-balance, and re-derive the LGD table and the slide-2 table from one asserted generator path. Main-call runs stay valid; rerun only the asks.

**Why:** The AUD 13.2m / 10.6m / 2.6m allowance and the 3,266 stage-2 loans reproduce independently from `personal_loan_book_2026-09-30.csv`, `hardship_register_2026-09-30.xlsx`, `loan_record_2026-09-30.parquet` and `ifrs9_scenarios_2026Q3.xlsx` by CRM-ECL-04 read literally. The LGD table (supplementary answer 4) does not reproduce under any reading I tested, and the one reading that comes nearest depends on a fork the shipped text never closes (59 loans labelled Cured in `collections_defaults_2023-24.csv` that the loan record shows later Written off). Gate A fails for those committed answers, and Gate C fails for the LGD through that fork. Governing label: underspecified_objective (LGD), with solution_incorrect on the slide-2 counts.

## Evidence (recomputed; reproduced Y/N, source)

| Item | Golden | Mine | Source |
|---|---|---|---|
| Stage 2 loans at 30 Sep | 3,266 | 3,266 Y | book 09-30 dpd>=30, hardship in force (start<=30 Sep<=end, not cancelled), v4 drop>=60 with v3 converted 1.12x-18 |
| Stage 3 (excluded) | n/s | 343 | dpd>=90 |
| PD multiplier | 1.06 | 1.0555 Y (0.55+0.3x1.28+0.15x0.81) | scenarios sheet Q1 FY27 (the prior-quarter sheet is labelled prior) |
| Stage 1 / stage 2 / total ECL | 10.6 / 2.6 / 13.2 | 10.584 / 2.595 / 13.179 Y | hazard from loan record, delayed entry from Oct 2019, 2.4 scalar, 70/76 LGD, re-amortised EAD, contract-rate discount |

Method used: for each product and month on book m, at risk = open and not yet defaulted at the end of m-1, counted only for calendar months from Oct 2019; default share and closed-without-default share per month; PD(k) = default share at a+k times survival over a+1..a+k-1; remaining term from repayments fallen due (pauses counted, past maturity gives 1); stage 1 uses 12 months or the remaining term, stage 2 the remaining term.

Competing readings of the main call, all at one decimal:

| Reading | Stage 1 / stage 2 / total |
|---|---|
| Golden (delayed entry from go-live) | 10.6 / 2.6 / 13.2 |
| Same, but excluding takeover loans entirely | 10.6 / 2.6 / 13.2 |
| Same, using the rounded 1.06 multiplier | 10.6 / 2.6 / 13.2 |
| Count every loan from drawdown (the naive reading) | 9.2 / 2.3 / 11.6 |
| Closures treated as censoring (default share only) | 11.2 / 2.9 / 14.1 |

The margins to the rounding edges are 0.03 or more, so the main answer is forced at one decimal. The stump is real and separable: only the delayed-entry (or exclusion) estimator gives 13.2.

**Supplementary 4, LGD by product and quarter (does NOT reproduce).**
- My literal build: discount each receipt to the default month end at contract rate/12 by whole months. Sources: all non-"Debt sale" receipts, with negatives netted. The 3.85c sale proceeds are allocated by face value from `debt_sale_2026-03_schedule.xlsx` at 27 Mar 2026. Cured loans carry zero loss. Loss share is pooled by balance.
- That gives PL36 60.5, 55.6, 65.2, 66.8 and PL60 67.7, 69.1, 67.8, 74.7. The golden is 67.9, 65.8, 70.7, 70.9, 70.2, 77.4, 73.2, 79.3. The gap is 2.5 to 10 points per cell.
- Fork: 59 of the 194 "Cured" loans were later Written off per `loan_record`. Treating them as losses (balance less PV of receipts) is what moves my numbers toward the golden, to within about 1.5 points with the sale included and about 0.7 points with the sale excluded. Excluding the sale contradicts CRM 3.3 ("including the proceeds of any sale"). I tested about 1,000 toggle combinations (cured handling, sale on/off, post-sale receipts, 24/36-month windows, undiscounted, negative entries, flooring, pooled vs mean) and none reaches 0.1. The golden's exact path is not recoverable from the files.
- Two readings of "actually lost" survive. Collections label Cured gives zero loss for the 59 loans (60.5 to 74.7). Loan-record-aware gives about 66 to 80. Neither is filed. Pooled vs mean of loan ratios is also unpinned in the prompt (cell differences up to 6 points).

**Supplementary slide 2 (does NOT reproduce exactly).** Stage at 30 June uses `personal_loan_book_2026-06-30.csv` with the 30 June score taken from `behaviour_score_runs` run_date 2026-07-01 (run dates are the 1st after month end; the 2026-06-01 run is worse). Unscored loans (1,353) are given zero drop. My counts (PL36 stage 1 / PL36 stage 2 / PL60 stage 1 / PL60 stage 2, each as in stage 1, in stage 2, in stage 3, closed):

| Group | Golden | Mine |
|---|---|---|
| PL36 stage 1 | 14,470 / 680 / 42 / 1,586 | 14,450 / 680 / 39 / 1,582 |
| PL36 stage 2 | 468 / 658 / 115 / 123 | 488 / 658 / 118 / 124 |
| PL60 stage 1 | 17,724 / 831 / 46 / 1,180 | 17,706 / 830 / 43 / 1,176 |
| PL60 stage 2 | 560 / 942 / 140 / 112 | 578 / 943 / 143 / 113 |

Diffs are up to 20 loans per cell. Found data tension: 6 loans (3 PL36, 3 PL60) show dpd=90 in the June book (stage 3 literally under CRM 1.2) but `default_month`=2026-07 in the loan record, and the golden evidently counts them in stage 1 or 2 at June. I also found that 67 loans have a score drop of exactly 60, so the threshold sits on a populated boundary. A variant search over score rounding, threshold strictness, the dpd test and hardship cancellation did not reach the golden (best total absolute error 66 loans).

## Files/Hygiene
PASS (no exclusion-level finding). 15 files, formats docx, xlsx x4, parquet x2, csv x6, txt, pdf. Business-realistic noise present (DD/MM/YYYY agency file, dishonoured-debit reversals, change-log in the dictionary, superseded scenario sheet, v3/v4 scores). Distractors usable: `arrears_roll_rates_fy26.xlsx`, the Wirraway placements (agency refs reused across files, only 81 percent of remittances match a Client Ref), prior-quarter scenarios. Temporal coherence fine (scenarios approved 18 Sep, CRM effective 1 Sep, extracts 1 Oct). No authoring leakage seen. Cross-batch fingerprint: no prior package in the readable directory, so not run.

## Stump power
Likely strong. A capable analyst following CRM 3.2 literally counts every record loan from drawdown (PD slightly low, 11.6 total) or treats repayment as censoring (14.1); only delayed entry (or exclusion of takeover loans) gives 13.2. The dictionary and the CRM both state the record has no earlier-platform exits, so it is findable but needs the survival insight. The asks add many independent chances to miss, and as built they are not gradable against a reproducible golden.

## Stumping type
`mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no` (the left truncation is a structural feature of a migrated book, not a reported number that is wrong; borderline on the clean-data test because the trap vanishes if the earlier platform's exits were present). Passes Gate G.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Field's own analysis: IFRS 9 lifetime PD from a left-truncated loan record (delayed entry vs censoring vs naive from-drawdown). Easy route: count taken-over loans at risk from drawdown, giving 11.6 instead of 13.2. Swap test fails if the nouns change (PD by month on book, 2.4 SICR scalar, staging), so the domain is used.

## Fix
- solution: regenerate the LGD table and slide-2 counts from the asserted generator and recheck all 8 LGD cells and 16 slide cells against a clean-room recompute; fix or explain the 6 dpd=90 loans.
- input_files / prompt (minimal): add to CRM 3.3 one sentence closing the Cured-then-later-written-off treatment, and state pooled-by-balance in the prompt or 3.3; state the stage of a loan 90 dpd at the reporting date but with a later default_month.
- none for the main allowance, which is frozen and correct.

## Disposition

**FIX_NOW on the asks, done; the main recommendation side frozen.** `freeze.py check task133 --mode rubric` passes: the
allowance (AUD 13.2 million, 13,178,713), stage 1 (10.6) and stage 2 (2.6), the 3,266 stage 2 loans, the 1.06
multiplier, the stump sentence, the ladder, the default path, the call sentence and the card's stump and driver are
where the judge left them. No graded figure moved: the eight loss shares and the sixteen counts were correct and are
unchanged. What the judge could not do was reach them by executing the shipped text, so each step where its build
parted from the golden is now filed, by WHAT, where the lender would file it. Only two documents under `target/`
changed (`CRM-ECL-04_expected_credit_loss_personal_loans.docx`, `ecl_extract_dictionary.txt`); every data file is
byte-identical to the judged bundle.

**The loss-share table.** An independent build of the judge's method from the shipped files reproduces its figures to
the decimal (PL36 60.5, 55.6, 65.2, 66.8; PL60 67.7, 69.1, 67.8, 74.7). It agrees with the golden on the sale proceeds
(face value at the cut-off times 3.85 cents, received 27 March 2026), the discounting (whole months from the default
month end at the contract rate over 12), the window (every receipt to 30 September 2026), the netted dishonours (dropping
them moves no figure) and the pooling. It parts at two steps, and changing both, and only those, gives all eight golden
figures to 0.03 points:

1. The cure (the judge's open fork). 59 cases Collections closed as Cured were later written off. The judge measured
   them at zero. The golden measures them on what they recovered. That treatment rested on the register (arrangements
   withdrawn before they started) and on 3.3's "returns to performing", which the judge read as unfiled. 3.3 now says
   it in the policy's own words: "a loan the loan record shows written off or settled for less did not return to
   performing, whatever resolution Collections recorded, and is measured on what it recovered". The golden now
   executes that sentence on the record. The record and the register select the same 59 loans (C1, asserted), and
   every other cure is repaid in full or still open. The device A1 is dead as a device and survives as a filed rule. No
   replacement was drawn: the pair sheet already had the cracker resolving it.
2. The attribution (not found by the judge, who read the placement report as a distractor). 2,034 Wirraway
   remittances are posted to the account first placed under the reference they quote. For a reissued reference that is
   an earlier account. Each of the 2,034 arrives outside its posted account's own placement, and 719 of them after that
   account was sold. The golden gives each remittance to the account placed under its reference on the day received;
   all 20,902 fall inside exactly one such placement, none on a first or last day. The dictionary now says what the two
   fields hold, the way the ledger and the agency document them: the receipts file's loan number is the one "the
   receipt was posted to; an agency remittance is posted on the Wirraway reference its narrative quotes", and the
   Agency Ref is "Wirraway's reference for the account while it is placed". Nothing filed says the agency reissues
   references or how the posting picks a placement.

Pooled against mean of loan shares is closed in 3.3: "for each product and quarter of default, the balance at default
not recovered since, summed over the quarter's defaults, as a share of their total balance at default". The mean of
loan shares misses all eight, nearest 0.58 points.

**The allowance's LGD.** The old 3.3 stated 70 and 76 per cent without saying they hold while the review runs. Read
with the prompt's "will be set", one could put the 2023-24 losses into the allowance: PL36 68.9 and PL60 75.1 per cent
would book AUD 13.0 million. 3.3 now reads "LGD is 70 per cent for PL36 and 76 per cent for PL60, the rates in force
until the Audit and Risk Committee approves a change". The allowance does not move.

**Slide 2.** An independent build of the judge's method reproduces its sixteen counts (14,450 / 680 / 39 / 1,582 and so
on). It parts from the golden at one step only: the June extract's days past due. Put back a day for every loan in
arrears, all sixteen golden counts follow.

- The June extract was read from the live system at its 07:30 run on 1 July, so it counts days past due to 1 July. The
  dictionary's change log now records this, the way the job would: CHG-26-0418 (21 July 2026) added current_score_v4
  and moved the extract to the quarter-end day's end-of-day snapshot, "not the live system at the run".
- With that filed, the six loans are consistent. At close of business on 30 June they were 89 days past due, so they
  sit in stage 2 and inside the four groups, and the record dates each default to the July month end. The fifteen at
  180 days were at 179 when 1.4's June batch ran, so they had not been written off. A loan in stage 3 at 30 June (90 or
  more at close of business) stays outside the four groups, and the record dates every such default to June or before.
- The 82 June loans that fall exactly 60 points (67 of them in stage 2 on the score alone) stay where they are. Every
  score is a whole number, and the migration note converts v3 "rounded to the nearest whole point". No v3 score lands
  within 0.02 of a half point. So 2.1's "60 or more" is literal, and reading it as more than 60 moves 12 of the 16
  counts.
- "The number in each stage and the number closed" is filed in the dictionary: "a closed loan is in no stage", beside
  1.4's "a loan that has been written off is closed". Six loans of the four groups were written off by 30 September,
  and counting them in stage 3 would move 4 counts.
- 2.2 now says when a cancelled arrangement stops: "one that is cancelled stops being in force on the day it is
  cancelled". At 30 June, 57 arrangements cancelled later were in force. Dropping every cancelled arrangement moves 14
  counts, ignoring cancellation moves 8 and excluding the end date moves 6. No cancellation falls on 30 June or 30
  September, so the main call's staging is unchanged (asserted).

**Fork rows.** SF22, SF23 and SF25 were rewritten, and SF29 to SF33 added: the pooled share, the LGD in force, the
cancelled arrangement and the end date, the 60-point fall, and stage 3 against closed. Each is asserted in
`checks.py`, together with the judge's two builds reproduced to the figure. The literal execution of the repaired text
gives all eight loss shares and all sixteen counts on the verifier's own code path.

**Gates.**

- `checks.py` PASS 577; `verify.py` PASS.
- Two rebuilds are byte-identical to `target/`, `target.zip` and `golden/`.
- `figures_check.py` exit 0; `precut.py` 49 PASS; `voice-check.py` PASS.
- `leak.py --asof 2026-10-12` REVIEW, no LEAK.
- `guard.py` validate 169 cards valid, heart WARN with no BLOCK, surface 1 promoted (task180, unchanged and differentiated).
- `freeze.py check --mode rubric` exit 0.

**Pair arithmetic.** The pair is 33.1, unchanged. The cracker scores 49.6, missing all 8 loss shares and 14 of the 16
counts, and the mirror scores 16.6. The residual risks are now likelier, because the filed text that makes the asks
literal also names what A2 and B3 turn on:

| If | Pair |
|---|---|
| The cracker also resolves A2 | 42.3 |
| The cracker also resolves B3 | 49.1 |
| The cracker resolves both | 58.3 |
| Both top responses resolve A2 | 51.4 |
| Both top responses resolve B3 | 65.2 |

Ask B carries two-thirds of the ask weight. No second device that a literal reader could resolve was found for it.

**Owed.** A targeted re-read: both documents changed. Then one re-judge on the asks. The main-call runs stay valid.

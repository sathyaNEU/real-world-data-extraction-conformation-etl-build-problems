# Judge verdict, task 501 (standby facility 2027)

- **Verdict:** NOT_DETERMINISTIC (margin_or_boundary_fragility; borderline). Also SOLUTION_WRONG on one minor figure (the CHF 305.0 million of 2026 calls).
- **Disposition:** SEND_BACK. The filed basis for "expected capital calls" has to be closed in the directive or the margin widened. Both change what solvers see, so a model rerun is required.
- **Why:** The golden of CHF 225 million holds only while expected 2027 calls land between 318.2 and 340.9 million. The golden is 326.6, which is 8.4 million (2.6 per cent) above the 318.2 floor, and RL-PM-05 s.5 says only "prepares the plan from the programme's own records". No shipped file fixes how calls are estimated. The solution's own back-test error is 1.6 to 3.0 per cent, and it is not a filed criterion. Reasonable, differently chosen estimation windows land on both sides of the floor. The main recommendation is affected. The fee asks inherit it: they price 225 and the next amount down, 200, which would be the answer if the floor were crossed.
- **Evidence (recomputed from the bundle):**
  - **Ledger and FX.** The ledger has 11,062 rows, of which 23 are CANCELLED. Currency case is mixed and was normalised. Reference rates at 31 Dec 2026 are USD 0.7906 and EUR 0.9339.
  - **CC1.** The four funds' undrawn commitment is CHF 196.8m, reproduced. Their drawn shares are 57.6, 60.2, 63.3 and 47.8 per cent. Their investment periods end on 20 Sep, 22 Oct, 24 Nov and 18 Dec 2027.
  - **CC2.** I reproduced 27 funds with the investment period ended, 91.8 to 93.8 per cent drawn at the period-end date, mean 92.6. This is a real, data-pinned structure. The solution's step 2 wording ("by that day") is loose. At 31 Dec 2026 the figure is 92.2 to 96.7, mean 95.4.
  - **Forecast.** My reconstruction used pooled all-history 12-month age bands on unfunded commitment, plus a catch-up to 92.6 per cent for the funds whose periods end in 2027. It gives bands only: 234.5 total and 77.2 for the four (golden 235.6 and 77.2). With the catch-up it gives 325.2 total and 165.3 for the four (golden 326.6 and 165.5). Reproduced within about 0.5 per cent.
  - **Target sensitivity.** The catch-up target of 91.8 to 93.8 per cent gives 321.0 to 333.1, still 225.
  - **Estimation variants.** Total expected calls, and the facility amount each gives:

    | Variant | Calls (CHF m) | Facility (CHF m) |
    |---|---|---|
    | Bands from first close | 328.4 | 225 |
    | 6-month bands | 326.4 | 225 |
    | 24-month bands | 322.4 | 225 |
    | Rates fitted on 2022 onward | 320.8 | 225 |
    | Rates fitted on 2024 onward | **312.3** | **200** |

    The 2024-onward variant gives a requirement of 1.1 x 312.3 - 150 = 193.5, so 200.
  - **Competing answers.** 125 (band rates only, 235.6 calls) and 200 (2026 calls carried forward) are refuted by the data structure. The 200 answer also survives from a recency-fitted rate model, which is a legitimate pacing method. Whether the fit uses the whole record or a recent window is not filed.
  - **2026 calls.** The solution states 305.0. I get 298.3 at the plan-date rate that s.4 mandates, and 305.6 at value-date rates. The conclusion (200) is unchanged either way, so this is a solution-block wording defect only.
  - **Fees.** 0.30 per cent and 0.15 per cent of 225m give 675,000 + 337,500 = 1,012,500. At 200m they give 600,000 + 300,000 = 900,000. Reproduced, and forced by the term sheet.
  - **Distributions (xlsx ask and chart).** Reproduced exactly: every cell, every quarter total (104,639; 59,250; 69,198; 73,721) and the year total (306,808). I matched the 184 credits through Transaktionsreferenz or the notice number in Referenz and valued the cash on the credit's value date. Buyout is largest at 95,970.
  - **Residual fork on the distributions.** Quarter by Buchungsdatum rather than Valuta shifts infrastructure Q1 and Q4 and private credit Q1 to Q4. Three postings booked on 4 Jan 2027 carry value dates in 2026. The feldbeschrieb defines Valuta as the day credited, and "arrived" fits it. The winner is unchanged. I treat this as minor and not disqualifying.
- **Files/Hygiene:** PASS. 13 files in 7 formats (csv, xlsx, docx, pdf, json, txt, md). One file has 33,968 rows and another 27,507. Distractors are the NAV register, look-through holdings, audited capital accounts and the H1 2025 report. The documents are plausibly operational, dates are coherent with the 31 Dec 2026 extract, and there are no authoring leaks. The 2027 emails sit after the extract date by design and are coherent. No contamination.
- **Stump power:** Strong where it works. The default age-band pacing path gives 125, a clean wrong answer. The carry-forward gives 200. The investment-period-end clustering (all 27 completed funds draw about 92.6 per cent by period end) is the real pitfall, and a capable analyst could plausibly miss it. The risk is the opposite: the filed text does not force the golden over the 200 result (see Evidence).
- **Stumping type:** `mechanism: forecasting`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported figures are fine and the difficulty is a forward projection that the age-band history mispredicts for a supported structural reason. It would still stump on clean data, and there is no planted defect.
- **Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. Liquidity planning of capital calls (a pacing model with a reserve and facility sizing) is the field's own estimate. A swap of nouns breaks the task. Layer 1 is multi-currency, case-mixed and cancelled/reissued notices, custodian advice vs keyed notices, and register vs ledger. Layer 2 is the choice of forecasting structure: age-band rates versus investment-period-end catch-up. The easy route is the age-band rate model, which gives 235.6 and a facility of 125; the carry-forward gives 200.
- **Fix:** Fix location is input_files, with the prompt as an alternative.
  - Close the estimation basis in RL-PM-05 s.5. State that the plan estimates calls on all commitments from the full record, and say how funds nearing the end of their investment period are treated, for example by reference to the share completed funds had drawn at their period end.
  - Or widen the margin so that no valid fit window can put the total below 318.2. For example, lift the golden total to about 335 or more by changing the data, or shrink the 20m facility steps.
  - Separately, correct the solution's 305.0 and the step-2 wording to "by the end of the investment period".

## Disposition

SEND_BACK repaired in place in one generator pass and committed PAUSED for the main session's re-judge. The call
(CHF 225 million) and the decisive step (the four funds' drawdown to the closed funds' drawn share before their
investment periods end) are unchanged. The repair changed the world, so every figure the world produces moved and is
restated from `generator/figures.json`; the fees at CHF 225 and 200 million are unchanged.

1. **The main call (margin_or_boundary_fragility).** Both of the judge's fixes, without filing a method.
   - RL-PM-05 s.5.2 now files the estimation period: "Treasury & Liquidität prepares the plan from the programme's own
     records as they stand at the plan date, over the programme's whole history since its first commitment in 2015."
     It names no rate, band, model, target or treatment of funds near their deadline (the decisive-words sweep in
     `checks.py` still passes). A recent fit window is another reading of the record that this sentence rules out
     (fork row SF17). Measured for the record: fits from 2019, 2021, 2022, 2023 and 2025 give CHF 225 million
     (332.6, 337.0, 325.3, 320.0 and 324.8) and the fit from 2024 gives CHF 200 million (317.1).
   - The world was tightened in the generator. Each fund's spread around the managers' aim at a period end went from
     0.45 to 0.15 points of commitment, so the closed funds' drawn shares are 92.2 to 93.3 per cent with a mean of 92.6.
     The four funds' pace went from 0.38 to 0.36 (Tessin 0.35).
   - Expected 2027 calls are now CHF 329.3 million. The bin runs from 318.2 to 340.9 with its midpoint at 329.5, so the
     golden sits 3.5 per cent above the floor and 3.4 per cent below the ceiling. The requirement is CHF 212.2
     million: 12.2 above 200 and 12.8 below 225.
   - The judge's variants, each landing on CHF 225 million (expected calls in CHF million):

     | Variant | Calls | Distance to the nearer edge |
     |---|---|---|
     | 6-month bands | 329.3 | 3.39 per cent |
     | 24-month bands | 327.6 | 2.96 per cent |
     | Bands from the first close | 332.1 | 2.58 per cent |
     | Lowest catch-up target (92.2) | 326.5 | 2.62 per cent |
     | Highest catch-up target (93.3) | 333.3 | 2.23 per cent |
     | The judge's form (band rate to the deadline, top-up in the deadline month) | 329.4 | 3.39 per cent |

   - The other careful choices, also landing on CHF 225 million:

     | Variant | Calls | Distance to the nearer edge |
     |---|---|---|
     | Bands by strategy | 329.6 | 3.32 per cent |
     | Median target | 329.1 | 3.44 per cent |
     | Strategy-mean target | 329.2 | 3.42 per cent |
     | The balance for the four funds behind schedule only | 326.5 | 2.63 per cent |
     | Post-period rates after a deadline | 326.1 | 2.49 per cent |
     | First month left out of the rates | 328.2 | 3.15 per cent |

   - All 384 combinations of these choices land on CHF 225 million, at 320.1 to 336.8.
   - Two weaker estimators also land on it, with less room. The mean of fund-month rates gives 336.8, 1.20 per cent
     inside; it overstates the record's own calls by 6.3 per cent. Nothing called after a deadline gives 321.6, 1.07
     per cent inside; the record shows follow-on calls after a period ends.
   - With those two added, 52 of 1,152 combinations leave the bin. Each takes at least three departures from the
     canonical, one of them a weaker estimator.
   - Every one-at-a-time careful choice is asserted at 2 per cent or more inside the bin, the weaker estimators at 1
     per cent or more, and every combination inside it (`checks.py`). The five corridor cases are recomputed
     independently in `verify.py`.
   - The default path and every wrong rung stay outside, at least 7 million from the bin (asserted):

     | Rung | Calls (CHF million) | Facility (CHF million) |
     |---|---|---|
     | R1, the default | 236.1 | 125 |
     | R0, the 2026 calls carried forward | 310.0 | 200 |
     | R2 | 252.1 to 270.3 | 150 |
     | R1s | 253.5 | 150 |
     | R3own | 214.3 | 100 |
     | X2 | 291.1 | 175 |
     | X1 | 377.4 | 275 |

     R0 is the nearest: its requirement of 191.0 is 9.0 million below 200.
2. **The 2026 calls figure (SOLUTION_WRONG on CHF 305.0 million).**
   - The stated figure was right at the plan-date rate. The judge's CHF 298.3 million leaves out the calls of the
     franc commitments: the rate file carries no CHF row, so mapping currencies to the file's rates blanks them, and
     that was CHF 6.7 million in the judged build. With the franc commitments at par, the old build gives 305.0.
   - In the repaired build the figure is CHF 310.0 million, and the write-up now states its basis: "at the plan-date
     rates, the franc commitments at par". At value-date rates it is 310.6. All three bases land on CHF 200 million
     (asserted).
3. **Step 2's wording.** It now reads "divided each fund's calls value-dated by the end of its investment period by its
   commitment". Step 3 names the filed period, and step 6 says the amount sits within the term sheet's covenants.
4. **The leak reader's readings**, answered in the design note:
   - Dealing-rate francs are stop s4, every figure off by at least CHF 18.9 thousand.
   - The field notes define Valuta as the day credited. The booking-date reading moves 5 of the 186 credits of 2026
     across a quarter end, 3 of them into 2027. It changes 9 of the 24 figures and keeps the title.
   - The NAV covenant never binds. The programme NAV is CHF 1,231 to 1,418 million on every reading of the NAV
     register, so a quarter of it is above CHF 250 million (SF18, asserted). The NAV register stays a declared
     distractor.
5. **Found and fixed during the repair.**
   - The minutes of the 24 September sitting reported the facility's repayment on 2 October; item 6.1 now says it "is
     repaid from the October transfer".
   - The September 2026 draw is now triggered by an operating minimum of CHF 5 million on the account. The new world's
     calls had left the balance above zero. The facility was drawn CHF 6 million on 18 September.
   - The golden paper called the rate after a deadline "the post-period rate", where the computation uses the age-band
     rate. It now says the age-band rate.
   - The paper's strongest quarter is computed, not typed.
6. **Under `target/`.**
   - Two documents changed: RL-PM-05 (s.5.2) and the minutes (6.1). Every data file was regenerated from the new world,
     so the leak reader is due a re-read.
   - The ask moved with the world: all 20 figures and the 4 labels. The title still names Buyout and the cracker's path
     names Infrastructure.
   - The 2025-26 distribution arrivals are drawn on the timing stream. Stream 360 passed every assertion out of 2,000
     screened. Its smallest stop misses are s1 720.8, s2 97.6, s3 26.6 and s4 18.9 (CHF thousand).
7. **Free gates after the repair.**
   - `checks.py`: 250 assertions, 0 failed.
   - `verify.py`: 0 differences, the corridor included.
   - Two consecutive builds byte-identical (19 files).
   - `figures_check.py`: 99 figures, 0 absent.
   - `leak.py`: REVIEW, no LEAK.
   - `guard.py`: surface 0 pairs promoted; heart WARN, answered.
   - `precut.py`: 38 checks, 0 FAIL, 0 WARN. `voice-check.py`: PASS.
   - Container audit clean.

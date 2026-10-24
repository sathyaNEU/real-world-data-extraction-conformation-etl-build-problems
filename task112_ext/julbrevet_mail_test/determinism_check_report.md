# Verdict (task112ext-v2)

**Verdict:** NOT_DETERMINISTIC (Gate C, underspecified_objective, on the memo's range figures, supplementary ask 19, and on the card-offer purchases, asks 1-6, 8, 10, 12, 14, 16, 18, 21). The call itself (drop) is forced once the interval is clustered.

**Disposition:** FIX_NOW. Pin in guidance section 5 and the prompt the interval's WHAT (two-sided 90 percent interval on the contrast of the 24 mailed against the 3 held-back postcode areas, with the estimator and degrees of freedom stated), and state that "purchases paid" on offer receipts means the amount after the discount as in the BI table. No data file changes. If any model run already used the current text, a rerun is required.

**Why:** Every figure reproduces from the bundle, but under the filed text the 90 percent range, the lower-end margin, the miss and the needed lift are not unique. The guidance (section 5) says only "two-sided 90 percent interval". With 3 control clusters, equally standard estimators give different lower ends: Satterthwaite-Welch on household-weighted area means (golden) minus 56.99, Stata-style CR1 with 26 df minus 6.19. The golden's "weighted by households, about 4.5 df" is not in any shipped file. The card-offer sheet (asks 1-6) and the purchases by group (asks 8-18, 21) hold only if the POS receipt_total_sek is corrected at seven stores. The data dictionary states receipt_total_sek is "the amount paid after the discount", and no file mentions the till upgrade the golden cites, so a literal reader files different figures.

## Evidence (recomputed from target/)
| Item | Result |
|---|---|
| Eligible households (open 15 Nov 2027, Jan-Oct spend over all accounts >= 6,000) | 17,200, reproduced. The 14,108 Julbrevet households in the address file are a subset of them. Alternative eligibility on open accounts only gives 14,039 and does not match the address file. |
| Main card holder, post consent at the selection date | Reproduces the address file exactly (mailed set identical, 0 differences). The result is the same at 14 Nov 23:00 UTC, 15 Nov 23:00 UTC and 14 Nov 00:00 UTC. One tie on earliest joining date (HH4758279) is immaterial. |
| Control | Areas 803/805/852 hold 2,080 eligible households. 138 are objectors, leaving 1,942, reproduced. The 1,012 objectors in the mailed areas are not printed either. 1,150 objectors in total. |
| December purchases per household | Mailed 2,298.58, control 2,161.36, objectors 2,102.15, difference 137.21. All reproduced. |
| Interval, golden estimator | Weighted area means, cluster-robust Welch, df 4.54, se 94.21: minus 56.99 to 331.42. Margin minus 14.25, miss 25.65, needed 239.81. All reproduced. |
| Household-level Welch | 58.00 to 216.43. This is the easy route and gives KEEP. |
| Offer receipts 1-24 Dec | Raw POS: O1 394.7 / 641.1 / 30.4 and O2 869.2 / 1,537.1 / 62.3 (Stor / Mellan / Nära). |
| Offer receipts, corrected | At BV113/115/118/125/128/132/141 the POS total equals spend_sek plus the discount (for member-store-months where every receipt redeemed an offer: 643 of 643 in December, 117 of 137 in November, 5 of 151 in October). Every other store's POS total equals spend_sek. After subtracting the discount at those stores: O1 378.5 / 621.7 / 28.6 and O2 851.6 / 1,514.6 / 60.3. Reproduced. |
| Reach rules | 238 hard bounces in 2027 and 677 members whose last three pushes failed: both reproduced and documented (runbook 3.3 and 5.2). 252 consented-but-never-emailed members reproduced, but their suppression-list status is inferred from the absence of sends and stated in no file. |
| Reach counts | Gävleborg 3,913 / 1,798 / 1,545 and Västernorrland 3,719 / 1,678 / 1,455 (email / SMS or push only / none). Reproduced. |
| Purchases by group | Gävleborg 743.2 / 283.4 / 184.2 and Västernorrland 665.5 / 245.6 / 160.2. 3,000 households paid 344.4 in total (344.36). Reproduced with the corrected receipts. |

### Open forks (second readings)
- **Ask 19, variance estimator.**
  - CR1 with 26 df: minus 6.19 to 280.61, margin minus 1.55, miss 12.95, needed 189.00.
  - CR1 with 2 df: minus 108.28 to 382.71, miss 38.47, needed 291.10.
  - Unweighted Welch on area means: minus 56.34 to 336.49, needed 242.01.
  - Every clustered reading still gives DROP. Only the unclustered household-level reading flips the call.
- **Ask 19 and the control count.** Guidance section 4 says "the eligible households there", which can be read as 2,080. That gives control mean 2,155.85, incremental 142.72, range minus 79.49 to 364.93, control households 2,080, miss 31.27, needed 267.81. Section 3, "the same households", and the section 2 non-printing rule support 1,942.
- **Asks 1-6, 8-18 (purchases) and 21.** Literal use of POS receipt_total_sek ("after the discount") gives the raw figures above. Group purchases then change, for example the none-group total is 352.4 against 344.4.
- **Asks 7, 9, 11, 13, 15, 17, 20, 22 (household counts).** The 252-member suppression is inferred. Without it: Gävleborg 3,960 / 1,768 / 1,528 and Västernorrland 3,769 / 1,640 / 1,443. The none group then totals 2,971 rather than 3,000.

## Supplementary asks 1-22
1-6 (offer purchases by offer and format): reproduced only after the undocumented receipt correction. A literal reader files the raw POS figures.
7, 9, 11, 13, 15, 17 (household counts): reproduced. The 252 exclusion is an inference and is the only open reading.
8, 10, 12, 14, 16, 18 (group purchases): reproduced with the corrected receipts. The raw POS reading differs.
19 (memo figures): the control count 1,942, the means, 137.21 and the call reproduce. The range, margin, miss and needed lift are estimator-dependent.
20 (3,000 households): reproduced. It is 2,971 without the 252 exclusion.
21 (344.4): reproduced with the correction. It is 352.4 on raw POS totals.
22 (chart): reproduced, the same counts as asks 7 to 17 (odd numbers).

## Files/Hygiene
PASS. 22 files in csv, docx, xlsx, pdf and md, with several files above 25,000 rows. They read as system exports, with semicolon and decimal-comma POS, mixed clocks and a runbook with an incident log. Distractors: Meta ads, ESP and SMS logs. Dates are consistent with the January 2028 timeline. No authoring leakage found. The till-upgrade cause cited in the solution blocks appears in no shipped file.

## Stump power
Good. The easy routes file the wrong thing. A household-level interval gives 58.00 to 216.43 and wrongly clears the line (KEEP). The campaign report's 817.77 baseline, or the 3,092 eligible-but-not-mailed households (difference 159.23), is a poor control. The control is also unlisted and must be rebuilt from consent replay. The hard step is area-level inference with 3 control clusters.

## Stumping type
`mechanism: statistical_rigor` (cluster-level inference after ETL conformance), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. On clean data the 3-control-cluster inference still stumps.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Layer 1 is the mixed clocks, the POS and BI mismatch, the consent replay and the unlisted control. Layer 2 is the cluster-randomised incrementality test. The easy route (household-level interval or the report's baseline) gives KEEP or 159 SEK per piece. The domain passes the swap test: incrementality testing of direct mail and consented channel reach is marketing measurement.

## Fix
Where: prompt and the guidance docx (input_files text only).
1. Pin the interval's WHAT in guidance section 5 and the prompt: the contrast of the 24 mailed against the 3 held-back postcode areas, with the estimator and df named.
2. State that the control is the would-have-been-mailed households (non-objecting).
3. Define "purchases paid" on offer receipts as the amount after the discount, and either mark the receipt-total basis per store in the POS export or have the dictionary say to reconcile it to the BI table.
4. Optionally note that suppression carries over from before 2027 for the email platform.

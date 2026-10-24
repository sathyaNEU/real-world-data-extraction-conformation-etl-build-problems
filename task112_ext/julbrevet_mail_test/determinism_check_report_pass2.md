# Verdict, task112ext-v2b

- **Verdict:** NOT_DETERMINISTIC, narrowly. The keep-or-drop call and 21 of the 22 supplementary answers are forced and reproduce. The 90 percent range figures (main recommendation "minus 57 to plus 331", ask 19's -56.99 / 331.42 / 239.81 / 25.65-from-range) depend on an interval estimator the shipped text never files. Governing label: underspecified_objective (Gate C/E, ask 19 and the range in FINAL_RECOMMENDATION).
- **Disposition:** SEND_BACK (narrow). Any pin of the interval's estimand goes into the guidance docx or the prompt, which solvers see, so prior runs are invalid. The pack, the call and asks 1-18, 20-22 stay as they are.

## Why
Guidance s.5 requires "the lower end of the two-sided 90 percent interval on its incremental purchases per piece", but no shipped file says how to build the interval. The golden uses area means weighted by households, a variance of the weighted mean of the area means, and a Satterthwaite df of 4.54. Other cluster-aware estimators on the same 24 mailed and 3 control areas give different ranges (table below). The drop call is the same under all of them. The printed range, the needed lift (239.81) and the margin shortfall differ.

## Evidence (recomputed from target/)
| Item | Result |
|---|---|
| Eligible households (open account on 15 Nov 2027, Jan-Oct spend_sek summed over accounts >= 6,000) | 17,200 reproduced; all 14,108 D1 households eligible; 2,080 eligible in 803/805/852 (no D1 rows); 1,012 eligible, unmailed, outside the control areas are objectors |
| Main card holder (earliest joined open account on selection date) | equals addressee_member_id for 100% of D1 rows. One tie in HH4758279 (area 856, mailed area, no effect) |
| Post consent replay to 2027-11-14 23:00 UTC | 138 objectors in the control areas, control = 1,942. Same count at every cut from 14 Nov 22:00 to 15 Nov 23:59 UTC. 1,150 objectors overall |
| December purchases per household | mailed 2,298.58 (n 14,108), control 2,161.36, objected 2,102.15, difference 137.21 (all reproduce) |
| Interval, golden estimator (area means weighted by households, Satterthwaite df 4.54, SE 94.21) | -56.99 to 331.42; needed lift 45.60 + 2.0615 x 94.21 = 239.81. Reproduces exactly |
| Interval, other estimators | household-level Welch 58.00 to 216.43 (keeps the mailing: lower margin 14.50 > 11.40); unweighted area means, Welch df 3.97: -56.34 to 336.49; regression with cluster-robust SE, CR0, df 26: -3.50 to 277.93; CR1, df 26: -6.19 to 280.61 (needed lift about 189); CR1, df 4.5: -36.45 to 310.88; control = all 2,080 eligible: 142.72, -79.49 to 364.93 (needed lift 267.81) |
| Call across estimators | every cluster-aware version has a lower end below 45.60 (drop). Only the household-level interval, which ignores that the control was drawn by area, clears the line |
| Card offers (asks 1-6) | POS receipt_total is not the BI basis at BV113, 115, 118, 125, 128, 132, 141 (exceeds spend_sek by exactly discount_sek in 643 of 643 December all-offer member-store-months). Corrected O1 378.5 / 621.7 / 28.6, O2 851.6 / 1,514.6 / 60.3. Raw POS gives 394.7 / 641.1 / 30.4 / 869.2 / 1,537.1 / 62.3 |
| Reach (asks 7, 9, 11, 13, 15, 17) | Gävleborg 3,913 / 1,798 / 1,545; Västernorrland 3,719 / 1,678 / 1,455. Reproduced |
| Reach inputs | 238 hard bounces in 2027; 252 pre-2027 bounces inferred (consented at a newsletter release, never sent anything in 2027; every newsletter's unsent consented set is exactly the earlier 2027 bounces plus these); 11 end-consented members with no 2027 send stay in. 677 members with last three pushes failed. SMS and push consent imply contact data on file and an app sign-in |
| Group purchases (asks 8, 10, 12, 14, 16, 18, 21) | 743.16 / 283.39 / 184.19; 665.53 / 245.59 / 160.17; none-of-three 344.36 thousand SEK. Reproduced |
| Memo figures (ask 19 other than the range) | 2,298.58, 2,161.36, 137.21, 1,942, margin -14.25 (from -56.99), 11.40 piece cost |
| Asks 20, 22 | 3,000 and the chart values reproduce |

## Second readings the shipped text leaves open
- Ask 19 (and the range in FINAL_RECOMMENDATION): interval estimator. Second readings: unweighted area means, Welch, -56.34 to 336.49, needed lift about 241; CR1 regression with 26 df, -6.19 to 280.61, margin -1.55 per piece, shortfall about 12.95, needed lift about 189. The call holds; the figures do not.
- Ask 19: control population. Second reading: all 2,080 eligible households in the held-back areas, objectors included. It gives 2,080 control households, 142.72 incremental, -79.49 to 364.93. The "would have been printed" reading (1,942) is the better-licensed one, so the fork is moderate.
- Ask 20-21, 7-18: the 11 members with email consent but no 2027 send could be pre-2027 bounces, which no file can show. Treating them as suppressed moves counts by 1 to 4 households per group (for example Gävleborg email 3,911). The shipped text supports "stay in" but does not say it.
- Asks 1-6, 8-18, 21: using the POS receipt_total_sek as written ("amount paid after the discount") gives the raw figures above. The prompt's "on the BI warehouse's basis" pins the corrected figures, but only by inference from member_store_month. This is not an open fork.
- Push exclusion: "last three failed" and "any run of three failed" give the same 677. Members with one or two notifications, all failed (48), are not excluded under the literal reading.

## Files/Hygiene
PASS. 23 files, 22 data and document files plus the data dictionary. Formats: csv (16), xlsx (2), docx (2), pdf (2), md (1). The 25,000-row floor is met (esp_sends 589,974 rows). The documents read like operational artifacts, with realistic mess: time zones (UTC, local, offset), semicolon and decimal-comma POS, Apple proxy opens. No authoring or benchmark disclosure found. The dictionary's POS statement (receipt_total is the amount paid after the discount) is contradicted by the data at 7 stores, which is Layer 1 mess. No exclusion-level finding.

## Stump power
Good. The easy route, a household-level interval on the mailed-minus-control difference, gives 58.00 to 216.43 and keeps the mailing. The campaign report's basket sheet (2,298.58 vs 817.77 for the unmailed, or 2,139.34 for eligible but unmailed) is a seductive wrong comparison. A strong model that reads the guidance still has to find the control in no file, replay consent to the selection moment, and choose clustering by area. Several runs will plausibly use a household-level interval.

## Stumping type
`mechanism: statistical_rigor`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. Clean-data test: on defect-free data the unit-of-randomisation error (area, not household) still decides the call.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Domain: incremental-response measurement of a direct-mail test with a geographic control, taken from the campaign's own design (swap test: not interchangeable). Layer 1: UTC against local time, POS against BI basis, consent replay, suppression inferred from logs. Layer 2: cluster-aware inference at the assignment unit. The easy route (household-level interval, keep) is wrong.

## Fix
prompt or input_files (the guidance s.5 wording). File the interval's estimand and the control population so the range is forced: for example, state that the interval is a two-sided 90 percent t interval on the difference of household-weighted means of the postcode-area means, with the Welch-Satterthwaite degrees of freedom, and that the control is the would-have-been-printed households. Alternatively, drop the range endpoints and the needed lift from the graded figures and grade only the call, the incremental 137.21 and the 1,942. Add one sentence to the guidance (or accept as a convention) that members with email consent who were never sent a 2027 email and could not have bounced before 2027 stay on the list. Nothing in the pack, the call or the other asks needs to change.

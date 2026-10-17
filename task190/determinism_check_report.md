# Determinism verdict, task190 (judged cold, files in this directory only)

**Verdict: NOT_DETERMINISTIC. Disposition: SEND_BACK.**
**Gate G: no shipped artifact ranks the segments on the decision question** (not exhaustively proven; see G). **Gate H: analytical in kind, but the decisive estimator is not filed, so the call is not determinate (FAIL on determinism, not on the three rules).**

Scope note: my own specification family is 5 windows (half-width 5k,7.5k,10k,15k,20k around 10,000, floored at 0) x 5 bin widths (50,100,200,250,500) x 3 fits (Poisson, OLS, log-OLS) x polynomial order 1-3 = 225, of which 186 are complete (log fits fail on an empty bin in 39). The write-up's own family (225, 141 "standing") cannot be reproduced from the bundle: its refusal rule ("surplus below and deficit above fail to reconcile") is nowhere in the files. Scripts are in scratch/.

## 0. Reproduction table (shipped files, literal reading)

| Figure | Write-up | Mine | Note |
|---|---|---|---|
| Cash deposits paid in, bank | 46,772 | 46,772 | counter cash, less 2 reversed + 2 reversing rows, plus machine deduplicated on ref (82 re-sends); every machine row's UTC date equals its NZ date |
| Per segment paid in | 10,433 / 15,131 / 4,758 / 3,168 / 4,175 / 3,993 / 2,396 / 2,718 | identical | all 46,772 map through the crosswalk |
| 9,000-9,999.99 | 2,583 | 2,583 | |
| 10,000-10,999.99 | 1,428 | 1,428 | |
| "about 1,900" the profile puts in 10-11k | 1,900 | 1,635 to 2,286 over 186 specs (median 1,927; 72 of 186 round to 1,900) | NOT determinate |
| Quarterly sessions / over tolerance / net | 1145/117/17.00, 1126/119/100.28, 1081/223/-798.74, 1101/238/944.81 | identical | tolerance 25 to 2026-12-31, 15 from 2027-01-01; "at or under passes": 2 sessions at exactly 25 and 5 at exactly 15 are correctly not over; local vs raw stamp gives the same quarters |
| Risk bands raised in / lowered in / raised then out | B1 0/240/0, B2 392/241/153, B3 402/306/115, B4 320/391/3, B5 230/0/0 | identical (accepted rows only, letters mapped to 1-5) | including the 11 superseded rows would give 398/404 raised, 243/307 lowered, so the dictionary rule matters and is filed |
| Monthly out-of-service hours | 75.9 91.7 94.0 78.9 56.9 82.5 95.4 134.9 54.2 98.2 72.9 63.2 | identical when an incident is put in its REPORTED month | see fork F1 below |
| Machines with no service record | 3 (1455, 1509, 1562) | same | |
| Sites differing from vendor by over 2 h | AR15, AR19 | same (-21.1 h and -34.6 h on the year; every other site 0.00) | robust |
| Segment split table | 150/100/50/50/50/50/0/0, bank 450 | reproduced ONLY under one estimator, (surplus + deficit)/2, at 50 rounding (186 of 186 specs) | not filed anywhere; see section 1 |

## 1. Probe 1: estimand filed, method open?

Filed by 7.4: population (physical cash deposits of business-register customers at year end, by segment), outcome (count of deposits, one for one, "below the threshold when the amount would otherwise have been at or above it"), window (the reporting year, by paid-in date; 1.2 defines the year), unit (deposits, not value, customers or days), comparison (counterfactual "from the segment's trade outside the band"). Rounding: 7.4 says nearest ten and bank = sum of stated segment figures; the prompt says nearest 50 and bank = their sum. The prompt is the later and more specific instruction, so I take 50 (closed, but the handbook and prompt disagree and nothing says which governs; low risk because both give the same bank-is-sum rule).

No sentence gives a procedure, formula, fitting instruction, bin or profile. Good: the method is open. Executed literally, 7.4 names "deposits in the band (3.2: 9,000 to under 10,000) that would otherwise have been at or above 10,000". No column holds it (7.4 says so). What the literal text fixes is the surplus-in-band quantity S = observed(9-10k) minus counterfactual(9-10k) from "outside the band". It does NOT say that the 10-11k shortfall is part of the figure or that 10-11k is excluded from the profile. 3.2 defines the band as 9-10k, so "outside the band" literally includes 10-11k, which is visibly depleted (the 100-dollar histogram steps from about 240 per bin to about 145 per bin at exactly 10,000).

## 2. Probe 2: every defensible figure (bank, unrounded; segment rows in section 4)

All over my 186 complete specs; negative segment values clipped to 0 only where stated.

| Estimator | What it is | Unrounded bank range | Sum of 50-rounded segment figures (distinct values) |
|---|---|---|---|
| S, exclude 9-11k from the fit | surplus below | 71 to 786 (median 439) | 13 values, 150 to 800; modal 500 (73 of 186), 450 in 17 |
| S, exclude 9-10k only (literal 3.2 band) | surplus below, depleted 10-11k left in the fit | 171 to 799 on 120 specs (median 522) | 12 values, 250 to 850; modal 600 (25 of 120), 450 in 20 |
| D, deficit above | expected minus observed in 10-11k | 207 to 858 (median 499) | 13 values, 250 to 950; modal 450 (51), 400 (43) |
| min(S,D) | | 71 to 411 | 150 to 450 |
| (S+D)/2 | the write-up's "reconciled" figure | 402.3 to 510.3 (median 474.2) | **450 in all 186** |

Only the last row agrees across specs, and it agrees because of an identity, not because the data pick a candidate: (S+D)/2 = (obs_below - obs_above)/2 - (exp_below - exp_above)/2, so the profile enters only as a half-slope correction (range 2.7 to 58 deposits per segment, grocery the largest) and the huge level sensitivity of the extrapolation cancels. That is a legitimate discontinuity-style estimator, but the pack nowhere files it, and 7.4 reads as S. A literal solver running S gets 150 to 800 depending on window and polynomial order, and on the shipped record the specs do not agree (S minus D across specs: bank spread -786 to +579).

Easy-path figures named in the write-up (1,438 same-day, 500 band-alone, 1,633 prior-year) I did not reproduce: the same-day and prior-year definitions are not filed in the bundle, so I cannot confirm them. 2,583 (raw band) is exact.

## 3. Probe 3: forced by the data, or by data too smooth?

Neither extreme. The amounts are sampled, not drawn from a curve. Poisson cubic fit, 9-11k excluded, window 5,000-15,000 (where a cubic is adequate):

| segment / bank | w50 chi2/df (df, p) | w100 | w250 | w500 |
|---|---|---|---|---|
| bank | 1.11 (156, .16) | 1.12 (76, .23) | 1.44 (28, .06) | 1.28 (12, .22) |
| transport | 0.94 (156, .69) | 1.01 (76, .46) | 0.91 (28, .60) | 0.61 (12, .84) |
| grocery | 1.18 (156, .06) | 1.11 (76, .23) | 1.39 (28, .08) | 1.23 (12, .26) |
| hospitality | 0.95 (.67) | 0.91 (.69) | 0.81 (.75) | 0.37 (.97) |
| fuel | 1.05 (.31) | 1.23 (.09) | 1.27 (.16) | 1.34 (.19) |
| clubs / rural / trades / personal | 0.83-1.02 | 0.83-1.05 | 0.57-1.01 | 0.37-0.90 |

Chi2/df about 1 with mid-range p values: consistent with a count process at about Poisson noise; not overdispersed, and not suspiciously under-dispersed in aggregate (the small segments at w500 run 0.4-0.6, low but with 12 df inside tail range). Over the full 0-20,000 window the same cubic fails badly (bank chi2/df 6.5 at w50 to 57 at w500, p < 0.001) because the profile is not a cubic over that range, i.e. the specifications really do disagree there. Adjacent-100-bin statistic (should be 1 for Poisson counts on a smooth density): bank 1.41, segments 0.68 to 1.20. Variance over mean in 100-dollar bins after linear detrend: 5-9k bank 1.31, 11-15k bank 0.93; segments 0.57 to 1.51.

Which side: the mean-of-S-and-D figure sits on the "agree" side but for an algebraic reason (cancellation), and its agreement is NOT within a wide scatter: sampling SE of (obs_below - obs_above)/2 is sqrt(ob+oa)/2: transport 15.1, grocery 18.3, hospitality 10.0, personal 9.3, fuel 9.4, trades 8.1, clubs 7.2, rural 6.9, bank 31.7. The rounding half-width is 25, so each segment's cell is 1.4 to 3.6 SE wide and the bank figure's rounding cell (50 wide) is only 1.6 SE: the grid is at the edge of what the record's own scatter supports. S and D individually disagree between candidate fits by several SE; that is the candidates differing by far more than sampling error, so the method is not forced by the data for the filed quantity S.

## 4. Probe 4: distance to the rounding line (estimator (S+D)/2, 186 specs)

| Segment | Figure | Unrounded min / median / max | Nearest edge (min over specs) | Flip condition |
|---|---|---|---|---|
| Transport and courier | 150 | 142.8 / 157.3 / 163.9 | 11.1 to the 175 edge (163.9) and 17.8 to 125 | +11 deposits flips to 200 |
| Grocery and convenience | 100 | 80.4 / 105.3 / 116.7 | **5.4 to the 75 edge (80.4)**; 8.3 to 125 | -5.4 flips to 50 |
| Hospitality | 50 | 39.2 / 46.0 / 49.6 | 14.2 to the 25 edge (39.2) | -14 flips to 0 |
| Trades and construction | 50 | 48.4 / 52.1 / 53.7 | 21.3 | |
| Fuel and automotive | 50 | 49.0 / 54.8 / 58.7 | 16.3 | |
| Personal services | 50 | 50.6 / 56.7 / 61.0 | 14.0 | |
| Rural supply and horticulture | 0 | -4.9 / 0.4 / 2.8 | 20.1 to +25 | genuinely nil |
| Clubs and community | 0 | -3.1 / 2.2 / 4.6 | 20.4 to +25 | genuinely nil |
| Bank, path 1 (sum of rounded) | 450 | 450 in all 186 | binding segment margin is grocery 5.4 | |
| Bank, path 2 (round the unrounded sum) | | 402.3 / 474.2 / 510.3 | **median is 0.8 below the 475 edge** | |

The write-up states "closest segment 15.8 clear"; in my family grocery gets to 5.4. Under the (S+D)/2 estimator both nils are genuinely nil (|F| <= 5, 20 from the edge). Under S they range -40 to +12, so they are nil on any reading, but "nothing the record can distinguish" there cannot say whether a negative estimate means no splitting or a profile misfit. The grain: the write-up says 50 is "the granularity the record's own scatter supports"; with SEs of 7 to 18 per segment that is defensible, but the grain is the prompt's, not the record's, and it is the grain at which the (S+D)/2 table collapses to one value across all specs; at the handbook's nearest-ten the table is not stable (e.g. transport 142.8 to 163.9 spans ten-cells 140, 150, 160), so the agreement exists only at this coarse a grid.

## 5. The four requested answers

**A. Two paths to the headline.** Path 1 (sum of 50-rounded segment figures, which is what the prompt files): 450 in 186 of 186 specs (and in every one of the 186, identical segment tables, a single distinct table). Path 2 (round the unrounded sum to 50): 400 in 12, 450 in 93, 500 in 81. Unrounded range 402.3 to 510.3, median 474.2, 0.8 below the 475 edge. By parameter: window 5,000 gives 450 in 29/500 in 13; 7,500 gives 450 in 42; 10,000 gives 400 in 12/450 in 5/500 in 19; 15,000 gives 450 in 12/500 in 24; 20,000 gives 450 in 5/500 in 25. Polynomial order 1 gives 450 in 24/500 in 38; order 2 the same 24/38; order 3 gives 400 in 12/450 in 45/500 in 5. So "both paths agree" is false across the surviving set: they agree in 93 of 186 (50 percent). The headline the prompt asks for is path 1, so the answer text is internally OK, but the stated robustness of the bank figure is not a property of the unrounded estimate, and a solver who sums first (the handbook says sum of the stated segment figures, but a solver producing one figure may not) gets 500 in 44 percent of specs.

**B. Method forced or not.** Not forced for the filed quantity. S: 13 different 50-rounded bank values, 150 to 800. The record is not too smooth (chi2/df about 1, count-like, section 3) and the candidates differ by far more than sampling error on S and D, but they collapse to one table only under (S+D)/2, which the pack does not file and which a literal reading of 7.4 does not give. This sits on neither of the two failed sides cleanly: the data are properly noisy, and the candidates diverge by more than that noise unless one particular estimator is chosen; the agreement is manufactured by the estimator plus a 50-wide grid.

**C. Distance to rounding line** is in section 4. Smallest margins: grocery 5.4 deposits (flip to 50), transport 11.1 (flip to 200), personal services 14.0, hospitality 14.2. Bank path-2 median 0.8 from its edge. No figure is a rounding edge wearing a zero.

**D. Blind response on the per-segment table.** The split column takes 4 distinct values (150, 100, 50, 0): counts 1, 1, 4, 2 cells. A constant 50 in all eight cells scores 4 of 8 cells (50 percent of that column; the bank 400 is wrong, the largest segment is wrong). A constant 0 or nil scores 2 of 8 (25 percent; bank 0 wrong). A constant 100 scores 1 of 8. Worse, a flat rate on the paid-in column needs no look at amounts: at about 0.82 percent of paid in it matches 7 of 8 cells (bank 400); at 0.91 percent it matches 6 of 8 with the bank at exactly 450; only the top-two ordering (transport 150, grocery 100) is wrong. Proportional to the band count at 15 to 20 percent matches 7 of 8 (bank 400 to 500). So the only cells a no-analysis response misses are the two top segments and the largest-segment answer; roughly 6 to 7 of 8 of the split column plus the per-segment paid-in column (which is plain arithmetic, 8 cells) are obtainable blind. Rubric quality concern, not determinism: the grid is coarse enough that book size alone reproduces most of it.

## 6. Forks found (fork table, each with arithmetic consequence)

F0 (blocking). Estimator not filed: S vs D vs (S+D)/2, and whether 10-11k is in or out of the profile. Bank 71-786 (S), 207-858 (D), 402-510 (mean). The write-up's "reconciled" is a method, not an estimand; the handbook, field dictionary and prompt give no reconciling rule.
F1 (blocking, graded). Month attribution of the 4 incidents that cross a month end (SI000515, SI000583, SI000397, SI000216) is unfiled. Reported-month gives the write-up (Aug 91.7, Sep 94.0, Oct 78.9, Nov 56.9, Dec 82.5, Apr 98.2, May 72.9); restored-month gives Aug 85.3, Sep 94.2, Oct 85.0, Nov 49.5, Dec 89.8, Apr 92.4, May 78.7; pro-rating by minutes gives Aug 89.5, Sep 92.2, Oct 82.9, Nov 54.2, Dec 85.2, Apr 94.2, May 76.9. Eight of twelve monthly figures move by up to 7.4 hours.
F2. "About 1,900" in critical component 1 is 1,635 to 2,286 across specs; it is not a stable figure.
F3 (minor). Handbook says nearest ten, prompt says nearest 50. Closed by taking the prompt, not stated.
F4 (minor). Five service-log rows have minutes that differ from restored minus reported; the dictionary closes this ("minutes column is the figure of record"), which I applied.
F5 (minor). Per-band raised/lowered "counted once each however many times the rating moved" is read per band; a customer climbing two bands is counted in each band. Closed enough by the sentence, but the reading is not explicit.

## 7. Gates

- **H (three rules).** No decoy: the shipped files contain no memo or certified record arguing the wrong method (prescribed extracts hold only 10k-plus rows; branch cash summary and card settlements are context). Not semantics: pass; the segment recode, UTC/local and reversals are handled the same by every reading. Not rule application: the decisive step is estimating a counterfactual deposit profile, which is analytical. Could a strong analyst who cleaned every key and read every clause still file a wrong figure? Yes: reading 7.4 literally (surplus above a profile fitted outside 9-10k) gives bank 171-799, median 522, modal rounded sum 600; this is the easy route and it is also literal. The content of H is analytical, but H also requires that the right answer be reachable from the record; here it is reached only by an unfiled estimator, so I do not clear H as determinate.
- **G.** I found no shipped artifact that ranks segments on the split question. The prescribed extracts are 10k-plus only (so they hold none of the depleted-side or band information, only the above side), the branch cash summary is by branch, and the card file is a merchant-facility file. Not exhaustively tested against every column.
- **A (estimand filed).** FAIL in part: population, outcome, window, unit filed; comparison filed only as "outside the band", not whether 10-11k counts as outside.
- **B (no semantic fork on the main call).** FAIL at F0 and F2 above.
- **C (literal execution = golden).** FAIL: literal execution of 7.4 gives S, not the golden.
- **D (method open only where forced).** FAIL: S estimates are not separated by the data (13 candidate banks); only an unfiled estimator is stable.
- **E (graded figures off their edge).** Grocery 5.4 deposits and bank path 2 0.8 from its edge are fragile; segments otherwise 11 to 21 clear. Marginal.
- **F (stump power / the ladder holds on the record).** Not judged beyond the above; the analytical route does exist and the easy raw-band answer 2,583 is wrong, but the golden's own value is not unique.

## 8. What would fix it (without moving the call)

File the WHAT: state in the report brief that the figure is the surplus below the threshold and the shortfall above it measured together over the band 9,000 to 11,000 (so the estimate is each segment's half-difference in observed counts adjusted for the profile's slope), or equivalently state that deposits in 10,000 to 11,000 are part of what the figure reconciles. Fix the month attribution of an incident (reported month). Drop "about 1,900" or file its basis. Widen the grain, or state that the headline is the sum of the stated segment figures (the prompt already does).

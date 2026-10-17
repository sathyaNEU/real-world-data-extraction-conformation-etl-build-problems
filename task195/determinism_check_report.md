# Determinism verdict, task 195 re-judge (scoped)

**Verdict:** DETERMINISTIC
**Disposition:** APPROVE. Every graded figure reproduces from the shipped files. One residual (below, R1) is a method point the data structure settles but no shipped sentence states. It is an optional pin and needs no rerun.

## Reproduction table (own numbers, from target/ only)

| Block figure | Mine | Result |
|---|---|---|
| Comparison 5,839; 393 MIXED; 5,446 CONCORDANT | 5,839 / 393 / 5,446 | reproduces |
| Screen in service: 292 detected, 91 false calls, 1.67% | 292 / 91 / 1.671% | reproduces |
| Candidate detections 0.050/0.030/0.020/0.015/0.010 | 294/308/310/319/326 | reproduces |
| Increases (specimens) | 2/16/18/27/34 | reproduces |
| Increases (points) | 0.51/4.07/4.58/6.87/8.65 (0.5089/4.0712/4.5802/6.8702/8.6514) | reproduces |
| Candidate false calls | 61/74/80/85/104 = 1.12/1.36/1.47/1.56/1.91% | reproduces |
| Only 0.010 above the service's false-call rate | yes | reproduces |
| Interval test, paired estimators | 0.050 fails; 0.030, 0.020, 0.015, 0.010 clear | reproduces |
| Recommended cutoff | 0.030 | reproduces |
| Weekly W13..W21, vials and excess | 575/14, 596/12, 601/12, 628/13, 563/14, 541/13, 555/15, 519/23, 538/26 | reproduces |
| Flagged per thousand, 2026-03..2027-02 | 15.6, 15.3, 13.9, 14.9, 14.2, 15.1, 17.6, 19.6, 19.7, 18.8, 20.7, 16.1 | reproduces |
| Dilution L1/L2/L3 median share | 0.963, 0.865, 1.027 | reproduces |
| Dilution counts within a fifth | 7, 7, 6 | reproduces |

Nothing failed to reproduce. The png has no numeric figure in the blocks (the interval endpoints are not graded numbers).

How each was derived:
- **Comparison.** Accepted QC read, empty agreement_ref, one of the five cohort projects, received 1 Mar to 31 May. Joined on specimen_id to the accepted read set's mixture_fraction and to a MIXED or CONCORDANT register verdict reported on or before 21 June. Specimens with INCONCLUSIVE only are out. The five aliquot-conflict specimens (A1 CONCORDANT, A2 MIXED) are not in the comparison, so verdict collapsing (any MIXED, or A1 only) moves nothing.
- **Weekly.** Rows per report, joined on specimen_id to biobank_ref (the dictionary defines it as the vial). Rows equal the PDF counts for W13..W21.
- **Monthly.** RELEASED rows with the release_amendments log applied, one record per specimen, flagged = HETX FLAG for AUTO and review_outcome FLAGGED for REVIEWED, released month from released_date, denominator is distinct specimens released in the month. Unrounded values are far from any .x5 rounding edge (nearest 15.2996, 14.9078, 15.1046).

## 2. Dilution panel

Replicate rows all carry Stock NS-27-04, so the prepared levels are L1 0.0081, L2 0.0163, L3 0.0629. Level case is mixed (l1 and L1) and folds. The voided row (L3 replicate 10) has no value. Each level has n = 9 results.

| Level | Median (unrounded) | / prepared | Share | Band (0.8 to 1.2 of prepared) | In band |
|---|---|---|---|---|---|
| L1 | 0.0078 | 0.0078/0.0081 = 0.962963 | 0.963 | 0.00648 to 0.00972 | 7 |
| L2 | 0.0141 | 0.0141/0.0163 = 0.865031 | 0.865 | 0.01304 to 0.01956 | 7 |
| L3 | 0.0646 | 0.0646/0.0629 = 1.027027 | 1.027 | 0.05032 to 0.07548 | 6 |

Distance of each replicate to the nearest band edge, in units of 0.0001 (negative = outside):
- **L1:** 0.0038 is -26.8 from the lower edge; 0.0049 is -15.8; 0.0072 is +7.2; 0.0075 is +10.2; 0.0078 is +13.2; 0.0083 is +14.2 from the upper edge; 0.0085 is +12.2; 0.0087 is +10.2; 0.0093 is +4.2.
- **L2:** 0.0102 is -28.4; 0.0121 is -9.4; 0.0136 is +5.6; 0.0137 is +6.6; 0.0141 is +10.6; 0.0142 is +11.6; 0.0149 is +18.6; 0.0153 is +22.6; 0.0173 is +22.6 from the upper edge.
- **L3:** 0.0435 is -68.2; 0.0462 is -41.2; 0.0596 is +92.8; 0.0615 is +111.8; 0.0646 is +108.8 from the upper edge; 0.0675 is +79.8; 0.0697 is +57.8; 0.0708 is +46.8; 0.0771 is -16.2 from the upper edge.

No replicate is on an edge, so inclusive or exclusive "within" does not matter.

Smallest single-replicate move that changes a count (values stored to four places):
- **L1:** 0.0093 to 0.0098, +0.0005 (adds 1 outside; count 6).
- **L2:** 0.0136 to 0.0130, -0.0006 (count 6).
- **L3:** 0.0771 to 0.0754, -0.0017 (count 7).

Medians cannot move from one replicate unless that replicate crosses the middle value. The 5th of 9 is unambiguous, and the median of ratios equals the ratio of medians.

Is the stated prepared level the only one the records support? Yes for the join. The Replicate sheet's Stock column names NS-27-04, and Panel notes A3 says the prepared-level column is the gravimetric fraction and the labels (0.8, 1.6, 6.4 per cent) are nominal. The other stock's row (NS-27-07: 0.0078/0.0157/0.0606) has no replicates. If a reader took the other stock instead the shares would be 1.000/0.898/1.066, and with the nominal labels 0.975/0.881/1.009. Counts stay 7/7/6 under all three, so the counts are invariant and only the medians depend on the join. The join is closed by the Stock column plus A3, not by inference.

Other readings of "within a fifth":
- **Of the prepared level, ratio 0.8 to 1.2:** the reading above.
- **Of the recovered value (|r-p|/r <= 0.2):** gives 7/7/7, since 0.0771 is 18.4% from the prepared level relative to itself. It does not survive a quotable sentence, because "of it" has the prepared level as its antecedent.
- **Geometric band 1/1.2 to 1.2:** gives 7/7/6, same as the stated answer.

Side notes:
- The note "Replicates reported: 28" counts the voided row, so results with a value are 27.
- The model card's limit of detection (about 0.008) would put L1 replicates 0.0075, 0.0078, 0.0072, 0.0049 and 0.0038 below it, but no shipped sentence excludes them from "results reported". It is a hard-to-sustain reading; stated for completeness.

## 3. Screen in service calls

The run log (lims_run_log) carries control_threshold_het_pct = 36,60 on all 6,934 rows and in all 10 batches. It is the only validated threshold stated anywhere.

- **AUTO calls:** all 6,646 reproduce at "het_excess_pct >= 36.60". The highest AUTO CLEAR is 36.59 and the lowest AUTO FLAG is 36.61. No value is exactly 36.60, so >= or > gives the same calls.
- **REVIEWED calls:** 15 of the 177 disagree with the threshold (11 FLAG below it, 4 CLEAR above it). None of the 15 is in the comparison population (8 are contract agreement receipts; the other 7 lack an accepted re-run read or a register verdict). Inside the comparison, all 5,839 calls, AUTO and REVIEWED, agree with the threshold. The population flags 383 (292 events + 91 clean).
- **Counts either way (recorded call or threshold-derived, identical):** 292 detections and 91 false calls.

More than one threshold reading?
- The history extract (2026) constrains the threshold only to (36.44, 36.70] (highest AUTO CLEAR 36.44, lowest AUTO FLAG 36.70). It is a bound, not a stated threshold.
- If a reader re-derived the screen at another value in that range, the calls would change: 36.5 gives 304 / 457 (and 378 calls differ), 36.55 gives 297 / 272, 36.65 gives 275 / 88, 36.7 gives 259 / 81. The service's false-call rate would move from 1.67% to between 1.49% and 8.39%, and the comparison against 0.010 would change.
- No shipped sentence offers any of these as the threshold. The 36,60 in the run log and the 2027 export agree to the cent, so there is one reading.

## 4. Gates (H, G, A, B, C, D, E, F)

**Gate H**
- `domain: pass`, `layers: pass`, `decisive_step: analytical`.
- Swap test: a paired parallel-run comparison of two assays on one reference-standard set, with a false-call constraint and a limit-of-detection model card, does not survive a noun swap, so the domain is used.
- Layer 1: semicolon and decimal-comma exports from two instruments, voided reads, a depth top-up second read set, a re-issued register, request keys that map to two specimens, a stale warehouse extract with a later amendment log, UTC against local date.
- Layer 2: judging the increase in detection on the specimens that carry both calls.
- The easy route: judge each screen against its own interval (overlap), which files a hold, or an unpaired two-sample interval on the increase, which files 0.015. A strong analyst who read every field correctly can still file either.

**Gate G**
- `mechanism: statistical_rigor`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
- No reported number is wrong. The model card addendum (median 0.0022, 91.6 per cent below detection) is fine as printed and the task does not turn on rejecting it. It would stump on clean data.

**Gate A: pass.** See the reproduction table. The grains were honoured: register rows and aliquots, QC rows (73 void-plus-accepted pairs), re-run read sets, history rows (31,198 specimens in 32,647 rows).

**Gate B: pass.** The threshold is in the run log, the decision rule in KVAL-07 4.1, the cutoffs in Table 2, the vial key in the dictionary, the amendment values in the log. PDF tables were extracted with pdftotext and read in full.

**Gate C: pass, with the following forks named.**
- **R1 (method).** The shipped text puts the 95 per cent interval on "the increase" but does not say how. Paired estimators (Wald on discordant specimens, Newcombe, bootstrap, exact binomial, McNemar) all agree.

  | Cutoff | b/c discordant | Paired 95% lower bound | Exact one-sided p |
  |---|---|---|---|
  | 0.030 | 23/7 | +1.36 to +1.53 points | 0.0026 |
  | 0.050 | 14/12 | about -2.0 | 0.42 |

  Unpaired readings differ:
  - **Unpaired Wald on the increase:** 0.015 is the first to clear [1.07, 12.67]; 0.020 gives [-1.33, 10.49] and 0.030 gives [-1.86, 10.01]. Recommended cutoff 0.015.
  - **Each screen against its own Wilson interval:** only 0.010 separates (78.9 against 78.4), and it fails the false-call condition, so hold.

  I do not count this as an open fork. The two screens are scored on the same 393 events, with detection defined per specimen (3.4), so the unpaired estimators answer a different estimand and are not equally licensed. But no shipped sentence says "paired", and the write-up's step 5 narrates it. Optional pin, with no rerun: a clause in the prompt or in KVAL-07 4.1(a) naming the unit of the interval (the specimens the two screens call differently). It must not name the estimator.
- **R2 (amendments).** The prompt does not say to apply the amendment log. Applied (value_after) it gives the reported 15.6 .. 16.1. Unapplied it gives 19.7 .. 18.9, different in every month. Applied is the supported reading: the history extract was pulled 9 April, before the first amendment (12 April), the dictionary says value_after is what the record now carries, the log's reasons call the originals wrong, and 31 specimens booked twice have rows that disagree on month or flag before amendment (8 straddle months, 12 disagree on flag) and agree on all after it. So "each counted once" cannot be done without it.
- **R3 (denominator).** release_volumes_monthly counts results (rows), not specimens. The prompt says "specimens ... each counted once". On the volumes file the rates would be 14.9 .. 15.4. Closed by the prompt's own noun.
- **R4 (vial).** Via request_id the register maps to a different vial for 669 rows. Via specimen_id the excess per week is as reported. The dictionary defines biobank_ref as the vial, and the register carries specimen_id. Distinct specimens would give excesses of 4..7, which is not a vial count.

No margin problem: 0.030 clears every paired estimator by at least 1.36 points and 0.050 misses by about 2.

**Gate D: pass.** The split among good answers traces to the estimator for the interval (R1), not to what a word means.

**Gate E: pass.** One committed cutoff or hold; each ask has a unit and rounding inside the sentence (two decimals, one decimal for per-thousand, three for recovery, whole counts).

**Gate F: stump power adequate.** The paired interval is the lever. A solver who reads the protocol correctly but compares each screen's own interval, or uses an unpaired difference, files hold or 0.015. The documentation does not name the pairing, so the trap is not pre-disarmed. Not too easy.

## Hygiene

19 files, formats csv, tsv, pdf, xlsx, json (5). History file has 32,647 rows. Licence and source are recorded in export_manifest.csv. Distractors are present (extraction platform report, unit costs, plate map, volumes file, model card addendum). The PDF W06, W08 and W23 counts exceed the register by the re-typed results (78 against 75, 77 against 75, 453 against 449), which is explained on the page and does not touch W13..W21. No authoring leakage found. The cross-batch reference check could not be run in isolation and is not reported.

## Three answers, short

1. Figures: all reproduce, table above.
2. Dilution: medians 0.0078 / 0.0141 / 0.0646, shares 0.963 / 0.865 / 1.027, counts 7 / 7 / 6, smallest count-changing moves 0.0005 / 0.0006 / 0.0017. Prepared levels are those of the stock the replicates name; counts hold under every join. Only one reading of "within a fifth" survives.
3. Screen in service: 36,60 reproduces every call in the population (AUTO 6,646 of 6,646; the 15 reviewed disagreements are all outside the population). 292 detections, 91 false calls. One threshold is stated anywhere; the history only bounds it.

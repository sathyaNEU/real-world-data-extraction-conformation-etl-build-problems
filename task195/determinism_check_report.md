# Determinism verdict, task195

**Verdict:** DETERMINISTIC. No SOLUTION_WRONG: every figure in blocks 1 to 4 reproduced from target/.

**Disposition:** APPROVE. No model rerun. Two optional wording tightenings (ask 4 amendments, ask 5 "it") are listed under Fix; neither changes a committed number.

**Why:** The comparison is 5,839 specimens (393 MIXED, 5,446 CONCORDANT) under any handling of the pack's aliquots, resends, voids and second read sets. Every paired interval estimator (Wald, Newcombe, score/Tango-MN, exact conditional, Agresti-Min, bootstrap) clears zero at 0.030 and not at 0.050, and 0.010 fails 4.1(b), so the rule returns 0.030. The only route to a different cutoff is an interval that ignores that both screens are scored on the same 393 specimens (0.015), which the parallel-run design (KVAL-07 3.1, 3.2, 3.4) excludes.

## Evidence: reproduction table

| Item | Block value | Recomputed | Result |
|---|---|---|---|
| Comparison / events / clean | 5,839 / 393 / 5,446 | 5,839 / 393 / 5,446 | reproduced |
| In service detects / false calls | 292 / 91 (1.67) | 292 / 91 (91/5446 = 1.671) | reproduced |
| Candidate detections 0.050, 0.030, 0.020, 0.015, 0.010 | 294, 308, 310, 319, 326 | same | reproduced |
| Increase, points | 2/0.51, 16/4.07, 18/4.58, 27/6.87, 34/8.65 | same (n=393) | reproduced |
| Candidate false calls | 61, 74, 80, 85, 104 (1.12, 1.36, 1.47, 1.56, 1.91) | same | reproduced |
| Cutoff | 0.030 | 0.030 | reproduced |
| Ask 3, nine reports (vials, excess) | 575/14 ... 538/26 | all nine identical | reproduced |
| Ask 4, twelve monthly rates | 15.6 ... 16.1 | all twelve identical | reproduced only with the release-desk amendments applied (see below) |
| Ask 5 | L1 0.878/7, L2 0.865/7, L3 1.027/6 | identical | reproduced |

Population probe (probe 2). The literal 3.1 to 3.3 filter gives 5,839 / 393 / 5,446.
- Contract receipts (579 accepted QC reads, KT-ALPHA and KT-BORG): none has a re-run row, so they cannot enter.
- Voided reads: 111 rows (38 specimens have only voided reads). They have no accepted read and fail 3.2.
- INCONCLUSIVE: 35 specimens that fall outside 3.2.
- Cohort specimens with no verdict: 194.
- Second read sets: 139 non-accepted read sets. Using the max or mean of the two sets leaves every count identical (294/308/310/319/326; 61/74/80/85/104).
- Specimens with two register rows: 45 (resends, second aliquots). The five CONCORDANT/MIXED conflicts are not in the comparison. Verdict handling "any MIXED", "first", "drop conflicting" or "all MIXED" gives an identical 393/5,446.
- Excluding the 153 REVIEWED-source rows (not licensed by 3.4) gives 366 events and 5,320 clean, with detections 268 for the service and 269/283/285/294/301 for the cutoffs. That is a different table, but 0.030 still carries the largest clear increase of 15, and no sentence supports it.

Direction probe (probe 3). Cutoffs failing (a): 0.050 only. Cutoffs failing (b): 0.010 only (104 > 91). "Highest cutoff value" is numeric, 0.030. The only second reading, "most sensitive passing cutoff", gives 0.015, but 4.1 says "highest cutoff value" and Table 2 lists values, so that reading contradicts a quotable sentence.

## Probe 1 and answer 2: interval families on the increase (n = 393, discordant b = candidate only, c = service only)

| Cutoff | b / c / both | Paired Wald | Newcombe paired | Score (Tango/MN) | Exact conditional | Boot paired | Unpaired Wald | Unpaired Newcombe | McNemar chi2 (df 1) | Unpaired chi2 (df 1) |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.050 | 14/12/280 | -2.03, 3.05 | -2.06, 3.09 | -2.16, 3.23 | -2.20, 3.10 | -2.04, 3.05 | -5.58, 6.60 | -5.57, 6.59 | 0.154 | 0.027 |
| 0.030 | 23/7/285 | 1.37, 6.77 | 1.36, 6.84 | 1.43, 7.07 | 1.18, 6.12 | 1.53, 6.87 | -1.86, 10.01 | -1.88, 9.98 | 8.53 | 1.80 |
| 0.020 | 24/6/286 | 1.89, 7.27 | 1.88, 7.34 | 1.98, 7.59 | 1.75, 6.46 | 2.04, 7.38 | -1.33, 10.49 | -1.34, 10.47 | 10.80 | 2.30 |
| 0.015 | 32/5/287 | 3.91, 9.83 | 3.93, 9.91 | 4.09, 10.16 | 4.00, 8.56 | 4.07, 9.92 | 1.07, 12.67 | 1.05, 12.64 | 19.70 | 5.36 |
| 0.010 | 38/4/288 | 5.53, 11.77 | 5.56, 11.86 | 5.75, 12.10 | 5.85, 10.12 | 5.60, 11.96 | 2.95, 14.35 | 2.92, 14.32 | 27.52 | 8.75 |

(Interval endpoints in percentage points. Agresti-Min paired at 0.030: 1.32 to 6.78. Exact McNemar p at 0.030 is 0.0052, mid-p 0.0043. Exact McNemar p at 0.050 is 0.845. The McNemar chi2 with continuity correction is 7.50 at 0.030.)

What the table says:
- Paired families: lower bound 1.18 to 1.53 at 0.030, and -2.0 to -2.2 at 0.050. Every paired estimator returns 0.030.
- Unpaired families: lower bound -1.86 at 0.030, -1.33 at 0.020, +1.05 to +1.07 at 0.015. Unpaired returns 0.015 (false-call 85 <= 91, so (b) holds). A continuity-corrected unpaired Wald still clears at 0.015 (about +0.8).
- The gap between families at 0.030 is about 3.3 points of lower bound, from the correlation of the two calls (285 of 393 detected by both). It is structural, not sampling noise.
- Within the paired family, estimators differ by 0.0 to 0.35 points, far below the standard error of about 1.4 points. They agree on the decision because the 0.030 lower bound sits about one standard error above zero (McNemar p about 0.005) and 0.050 sits 1.4 standard errors below.
- Of your three failure sides: none applies. The data are not too smooth (paired and unpaired return different cutoffs), the candidates that matter are separated by a margin, and the agreement is not an insensitivity artefact, because unpaired disagrees. The one soft side is that paired-family differences sit inside sampling error, but none of them touches the decision.
- Chi-square per df measured on the record's counts: McNemar 8.53/1 at 0.030 (0.154/1 at 0.050, 10.8 at 0.020, 19.7 at 0.015, 27.5 at 0.010). Independent 2x2 chi2 per df at 0.030: 1.80/1.
- Which file and columns say how the two calls on a specimen came to exist: qc_screen_calls_gsqa/gsqb (hetx_call, read_accepted, specimen_id) and mixture_fraction_rerun_v34.csv (mixture_fraction, read_set_accepted, specimen_id). The model card says the estimate "is computed from the read set alone" and not from the HETX call. The calls are two per-specimen calls on the same specimen (KVAL-07 3.1, 3.4).

Is the pairing forced? No shipped sentence says "paired interval". It is forced by the parallel-run design and by the 5,839-specimen common comparison: an interval that treats the two detection rates as independent samples ignores a correlation that the record's own both-detected cell (285) displays. I count an unpaired interval as the easy route, not a defensible reading. This is the stump, and it is analytical (the estimand's unit of analysis).

## Answer 1: supplementary asks, ask by ask

Ask 1 (per cutoff table, interval test, recommendation).
- Detections, increases, points and false-call rates are forced by 3.4 and 3.5 counting.
- The wording "clears the interval test" is defined by 4.1(a).
- A second value exists only on the unpaired route: 0.030 "no" and 0.020 "no", and the cutoff becomes 0.015. That route is the stump, not a competing defensible answer.
- Forced.

Ask 3 (vials and excess).
- Vial = crosswalk biobank_ref, joined on specimen_id. Each register (request_id, specimen_id) pair exists in the crosswalk, so the join is unique.
- Results = register rows per report_ref, which equal the PDF "Results issued" for all nine reports (589, 608, 613, 641, 577, 554, 570, 542, 564).
- The PDF footer says "Where a report is re-sent, the week's count includes the results sent again", which closes whether the excess counts resends.
- Second handling: distinct (specimen, aliquot) as "results" gives 587 instead of 589 at W13 and so a different excess. That contradicts the PDF footer, so it is not licensed.
- Joining on request_id alone is not possible, because 312 requests map to 2 to 3 specimens and 105 map to 2 to 3 vials.
- Reports W13 to W21 are the nine issued April or May. The W19 "two working days late" note leaves it in May.
- Forced.

Ask 4 (monthly flagged rates). Reproduces exactly (all twelve months) when four rules hold:
- (i) only RELEASED rows, bucketed by released_date, with SUPERSEDED and WITHHELD excluded;
- (ii) flagged = AUTO with hetx_call FLAG, or REVIEWED with review_outcome FLAGGED, which is the asking sentence's "reviewed ones by their review outcome";
- (iii) the release-desk amendments applied (hetx_call 121, released_date 245, review_outcome 1);
- (iv) specimens counted once, which is the asking sentence's "each counted once", for numerator and denominator.
After the amendments there is no specimen in two months and no flag conflict between its released rows. First, last and any dedupe give identical rates, whether the amendment is applied to every row of the specimen or only to the row matching value_before.
Competing handlings:
- Denominator from release_volumes_monthly (2,342 for March, "as booked", rows with duplicates) gives 14.9 in March against 15.6. This is excluded by "each counted once".
- Counting the REVIEWED FLAG calls (hetx_call) instead of the review outcome contradicts "by their review outcome".
- Not applying amendments gives about 18.3, 20.8, 17.4, 16.9, 17.0, 18.2, 20.0, 22.6, 24.6, 24.0, 26.4, 21.6, so all twelve are wrong by 1 or more. The quotable sentence is the dictionary's value_after, "the value the record carries after the amendment", together with the manifest's "amendments to released records". No sentence says outright that the warehouse values are superseded. This is the weakest closure in the pack and it closes by the dictionary line plus the pack's purpose for the amendment file. It does not reach a second value with a sentence behind it, because the volume file's "as booked at month end" is for the row-count denominator it excludes.
- Forced, with that one residual.

Ask 5 (dilution).
- The Replicate results sheet carries Stock NS-27-04 only, and the prepared level is joined by Stock and Level (0.0041, 0.0163, 0.0629).
- Lower-case level labels (l1, l2, l3, six rows) are normalised, and the voided row is excluded.
- "A fifth of it" can only coherently mean the prepared level, since the results and the prepared level are both fractions around 0.004 to 0.06. A median recovery is a share near 1, and a result of 0.0045 can never be within 0.2 of it.
- The second reading is within 20 per cent of the median recovery: L1 8 and L3 7 (L2 stays 7). It does not survive the unit check, and it contradicts the quotable "recovery as a share of the prepared level".
- Alternative stock NS-27-07 (prepared 18 March): 0.923/0.898/1.066, contradicts the Stock column of the results sheet. Using the nominal label (0.4, 1.6, 6.4 per cent): L3 1.009, contradicts the sheet note that the prepared level column is the gravimetric fraction.
- Forced.

PNG. The block states no endpoints, only the form and the markings. Any paired estimator draws a bar that agrees with the description. The 0.010 mark (above the service's false-call rate) is true.

## Answer 3: is every figure in block 1 true of every estimator the records admit

- 16 more events, 4.07 points, 393, 5,839: estimator-free.
- "Clear of zero on every paired estimator" at 0.030: true for all seven I built (smallest lower bound 1.18, exact conditional).
- "0.050 ... established by no reading": true for every estimator including unpaired (all lower bounds negative; Fisher p 0.93, McNemar exact p 0.845).
- "0.020 or 0.015 ... clear both tests": true of paired estimators only. Unpaired 0.020 fails (lower -1.33). Inside block 1 the paired frame is stated just before, so it is not misleading, but it is true of one family only.
- 1.36, 1.67, 1.91 per cent: counts, estimator-free.
- "Not holding ... follows only if each screen's detection rate is judged against its own interval": the Wilson non-overlap rule does give a hold (0.010 clears the non-overlap at 78.9 vs 78.4 but fails (b); 0.015 overlaps, 77.0 vs 78.4). The unpaired difference interval does not give a hold (0.015). So the sentence is true of the overlap rule only.

## Answer 4: margins (would a replicate or specimen moving a hair change a graded count)

- Mixture-fraction hair. Values are stored to four decimals and the cutoff test is on the stored value, with no ties at any cutoff. Nearest stored values and what a one-unit (0.0001) move does:
  - 0.050: MIXED 0.0502 (294, 2, 0.51 move by one) and a CONCORDANT 0.0498 (61).
  - 0.015: MIXED at 0.0148 and 0.0147 (319, 27, 6.87 move by one to two).
  - 0.010: three CONCORDANT at 0.0099 and one MIXED at 0.0101 (104, 326, 34 move by up to three or one).
  - 0.030: nearest MIXED 0.0314 and CONCORDANT 0.0293, so two specimens within 0.0015 (0.0007 and 0.0014 away); a 0.0001 to 0.0005 move changes neither 308 nor 74, and even both crossing moves the increase by at most 1 net.
  - 0.020: nearest MIXED at 0.0193 and 0.0192.
  So the tightest graded counts are the 0.015 detection (319) and the 0.010 false-call count (104), each one 0.0001 unit from the cutoff. They are not decision-bearing: 0.010 stays far above 91 (needs 13 fewer) and 0.015 stays far above the interval threshold.
- Decision margin at 0.030: the interval stops clearing zero when the net increase drops from 16 to 10 (Wald lower -0.18; 11 gives +0.08, i.e. 5 specimens) with b+c held at 30; exact conditional also flips at about the same point. One specimen moves it by 0.26 points. False-call margins: 0.030 has 74 vs 91 (17), 0.015 has 85 (6), 0.010 has 104 (13). At 0.050 the increase would need about +10 net more detections (Wald) to clear.
- Ask 5: the tightest margin in the pack's block 4 is L1 (boundary 0.8 x 0.0041 = 0.00328): a replicate at 0.0034 (inside, 0.00012 above) and one at 0.0031 (outside, 0.00018 below). At the stored four decimals (half-unit 0.00005) neither crosses, but one replicate shifting by 0.0002 changes L1 from 7 to 6 (or 7 to 8). L2 margin 0.00066, L3 0.0016 (0.0771 vs 0.07548).
- Ask 4: each month's rate moves by about 0.4 per thousand if any single specimen's flag status changes. That is the count itself, not a hair, and the rates sit at 0.00 to 0.17 flagged-specimen distance from the rounding edge, so the decimal given is the rounding of an exact count.
- Ask 3: counts of rows and distinct keys; no hair.

## Gates, short

- A: reproduced (table). B: every decisive fact is in the pack (Table 2, 3.1 to 3.5, 4.1, PDF footer, dictionary). C, D: no objective or margin dispute. E: no competing defensible value found for asks 1, 3, 5 and, for ask 4, only the unamended series, which a shipped sentence excludes (weakly).
- Files/Hygiene: PASS. 19 files, formats csv, tsv, xlsx, pdf, json. One file at 32,647 rows (history) and QC exports at 3,590 and 3,344. Licences and sources are in export_manifest.csv, and the manifest row counts match every file (3,590; 3,344; 6,245; 7,838; 32,647; 367; 7,987; 6,934; 6,861). Distractors: assay_unit_costs, extraction_platform_validation, plate_layout_map (control_well), lims_run_log (control_threshold_het_pct), release_volumes_monthly, plus the contract receipts and the second read sets. One non-stump finding, not exclusion-level: the manifest says the history was pulled 2027-03-04, yet 823 rows carry a released_date after that (to 2027-04-02). The months asked (to 2027-02) are unaffected, but a careful reader would notice.
- Stump power (Gate F): the easy route (independent two-proportion interval) gives 0.015, a recommendable but wrong cutoff, and it is reached by a capable analyst who cleaned everything correctly. The difficulty survives deleting every wrong number from the pack.
- Stumping type (Gate G): `mechanism: method_selection (paired against independent interval on shared specimens)`, `stumping_family: statistical_method_choice`, `surface_read_dependency: no`, `sole_data_defect: no`. The pack ships no ranking of cutoffs on the decision question; the shipped pack and protocol give no wrong answer.
- Three rules (Gate H): `domain: pass`, `layers: pass`, `decisive_step: analytical`. Swap test: the quantity is the increase in sensitivity of a contamination screen on specimens that carry both screens' calls, with a paired interval, which is a diagnostic accuracy comparison that does not read the same with another field's nouns. Layer 1 is the decimal-comma exports, two instruments, voided and resent reads, aliquots, contract receipts, amendments and a late weekly report; Layer 2 is the paired comparison. The strong analyst who cleans everything and reads every rule correctly takes independent proportions and files 0.015.

## Fix

none required. Optional, no number moves:
1. Ask 5: replace "within a fifth of it" with "within a fifth of that level" (prompt is already 996 characters, so something else must lose at least 4 characters).
2. Ask 4: a clause such as "after the release desk's amendments" would close the one residual (weakest closure in the pack). The same length constraint applies.
3. Block 1's "which clear both tests" for 0.020 and 0.015 could read "on the paired interval".

# leak check, task195

**Verdict: REVIEW.** 19 files read, 34 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: paired, specimen, asserted, difference, estimate, nothing, decisive, comparison, sentence, estimator, uncertainty, window, laboratory, accepted, cutoffs, method, intervals, population, golden, corpus, parallel, closed, protocol, two-sample, checks

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `method_validation_protocol_kval07.pdf`: carries 8 of 10 distinctive words of the committed call: 'Replace the contamination screen in service with the re-run mixture-fraction screen at the 0.030 cutoff for the quarter '

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `extraction_platform_validation_2025.pdf`: 3 of 25 stump-paragraph terms appear (specimen, laboratory, method); read whether the document names the move
- **REVIEW** `method_validation_protocol_kval07.pdf`: 9 of 25 stump-paragraph terms appear (specimen, comparison, estimator, laboratory, accepted, cutoffs); read whether the document names the move
- **REVIEW** `mixture_estimator_model_card_v34.pdf`: 6 of 25 stump-paragraph terms appear (specimen, estimate, estimator, laboratory, accepted, cutoffs); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read (pass 2, after the ask re-cut)

# task195 reader answers

Headline: recommended is C2 (0.030) if the increase is tested as paired on the same 393 MIXED specimens; C4 (0.015) if tested as two independent proportions. Committed: C2, 0.030.

1. Decisive step. No sentence names it. KVAL-07 4.1(a) says only "the increase ... is established with a 95 per cent interval above zero". The method (paired vs independent) is not filed. 3.4 does supply the structure: both screens are applied to "that specimen" and "Detection is counted per specimen", so the same 393 confirmed events are scored by both screens. Nothing teaches the method by example.
2. No file ranks the candidates. model card v34 gives only the estimator's distribution ("states no verdict"). The release_volumes file and the 2025 extraction report are unrelated.
3. Help-only files: validation_extract_dictionary.csv (field glossary), export_manifest.csv, rerun_pipeline_config_v34.json. The weekly-reports PDF with its "results re-sent are included" footer and the dilution workbook's "Panel notes" are the same kind.
4. Nothing reads as the answer. The model-card line "Share below the limit of detection 91.6 per cent" and the 0.008 limit of detection read as a pull toward the LOD, but they are context.
5. Filed sentences that fix the figure.
 - 3.1 and 3.2 fix the population: cohort project codes, 1 Mar to 31 May, accepted QC read, v3.4 estimate on the accepted read set, MIXED or CONCORDANT verdict reported by 21 June. Literal result: 6,244 cohort accepted reads, 6,068 with an estimate, 5,839 with a verdict, of which 393 MIXED and 5,446 CONCORDANT.
 - 3.5 gives false-call rate = flagged / CONCORDANT. HETX flags 91/5,446 = 1.67%.
 - 4.1 "at the highest cutoff value listed in Table 2 at which both ... hold" gives C2 (0.030) when the interval is paired, because highest value means the highest numeric cutoff that passes, not the most sensitive one.
 - 3.4 gives candidate flagged = mixture_fraction at or above the cutoff.
6. What decides it: an analytical choice, the paired versus independent interval on the increase. Both screens score the same specimens, so the discordant pairs carry the information. Population and rule application get you to the table, but the call flips on the interval. 4.1 "highest cutoff value" is a rule to read, which C2/C3 vs C5 turns on. Nothing looks planted.

7. Work and result.
Detections among 393 MIXED (HETX detects 292 = 74.30%). False-call: HETX 1.67% (91/5,446).

| Cutoff | Detects | Increase (specimens) | pp | b/c (cand only / HETX only) | FCR | paired 95% CI pp (Wald) | unpaired Wald lower pp |
|---|---|---|---|---|---|---|---|
| C1 0.050 | 294 | 2 | 0.51 | 14/12 | 1.12% (61) | -2.03 to 3.05 | -5.58 |
| C2 0.030 | 308 | 16 | 4.07 | 23/7 | 1.36% (74) | 1.37 to 6.77 | -1.86 |
| C3 0.020 | 310 | 18 | 4.58 | 24/6 | 1.47% (80) | 1.89 to 7.27 | -1.33 |
| C4 0.015 | 319 | 27 | 6.87 | 32/5 | 1.56% (85) | 3.91 to 9.83 | 1.07 |
| C5 0.010 | 326 | 34 | 8.65 | 38/4 | 1.91% (104) | 5.53 to 11.77 | 2.95 |

Interval test: C1 fails. C2 to C5 pass paired (exact McNemar p 0.005, 0.0014, 7e-6, 6e-8). C5 fails false-call (1.91 > 1.67). So the highest passing value is C2, 0.030. Paired intervals by Newcombe or bootstrap give C2 lower bound 1.36 to 1.53, so the pass is safe. If the interval is built as two independent proportions, C2 and C3 fail and C4 (0.015) is recommended. Decision date 1 July 2027 is consistent with the June review and the autumn queue. Replacement from 1 July is a decision for the quality review, so the answer is "replace at C2".
Choices the documents left me: (i) paired vs unpaired interval and which paired method (the outcome is the same for all paired ones I tried); (ii) the interval's reported bounds (Wald vs Newcombe vs bootstrap differ by 0.0x to 0.2 pp, so the plot bounds and any bound asked in the workbook are not pinned); (iii) whether the 176 accepted specimens without an estimate (all CONCORDANT, below the depth floor) are excluded as 3.2 says (I did) or counted as not flagged (C5 still fails, 1.85 vs 1.71; nothing else moves); (iv) specimens with conflicting aliquot verdicts, where MIXED if any aliquot is MIXED vs excluded: all 3 are contract and drop out; (v) re-accessioned specimens (NFG27-16xxxx): they have register rows but no QC rows, so they never enter. Original NFG27 ids carry the verdict. A second analyst treating biobank_ref as the specimen could change a few verdicts (81 originals CONCORDANT while the re-accession is MIXED; 14 other pairs differ), I filed the original accession.

8. Realism. Mostly recorded-looking. Good: lims received times are weekday only with a working-hours hump (hour 7 to 17, peak 11), ragged daily counts (sd 13 vs Poisson 10.7), initials TK/JO; the QC history UTC hour hump (04 to 20); het_excess_pct unimodal with fuzzy HETX call boundary (CLEAR up to 37.24, FLAG down to 34.94, 15 conflicts at 36.6); dilution recoveries noisy with lower-case 'l1' labels and a voided row; panel_markers_typed 88 to 96 with a long INCONCLUSIVE tail. Tells of generation: (a) specimen ids step mostly by 4 (3,921 of 6,860 gaps) alternating GSQ-A/B in a fixed rota in the QC exports; (b) HETX flag rate is 5.75% on GSQ-A and 5.76% on GSQ-B, which is too equal; (c) qc_screen_history received_utc minutes are flat (about 570 each at 02, 12, 23 ...) and every second is "00Z", nothing clusters at :00/:30 as real hand-keyed times do; (d) extract_date is the constant 2027-06-21 in both QC exports (it is the pull date, not an extract date); (e) mixture_fraction is a clean lognormal plus a second mode at about 0.1 with four-decimal rounding and the register second_contributor_share is exactly never below 0.0058 though the threshold is 0.005; (f) the sum of release_volumes_monthly equals the history RELEASED row counts exactly per month (2,342 ...) even though the amendments table moves release months, so the volume file ignores the amendments but the history matches it to the unit; (g) the plate run_dates include weekends while receipts are weekdays only.

9. Supplementary asks, one by one.
- Per-cutoff detects, increase, pp, false-call, interval test: detects/increases/pp/FCR are forced (table above), pass/fail forced for each cutoff under a paired interval. Not forced: under independent proportions the C2 and C3 verdicts flip to fail, so the recommended cutoff is C4 instead of C2. Both pass/fail columns and the recommendation depend on that single unfiled choice. Interval bounds themselves are not forced (method).
- Recommended cutoff: not forced, C2 (paired) or C4 (independent). I file C2.
- Weekly reports issued in April and May: nine reports. By the register's report_date and the PDF "Issued" date these are W13 (2 Apr) to W21 (28 May). Distinct specimens with any verdict vs PDF total: W13 584 vs 588; W14 606 vs 612; W15 608 vs 613; W16 633 vs 636; W17 573 vs 580; W18 562 vs 566; W19 549 vs 555; W20 552 vs 557; W21 546 vs 551. Forced except: distinct specimens (584) vs distinct specimen-aliquots (586) is a second reading, and W19 issued two days late (note in the PDF) is still in May, and week-ending vs issued classification does not change the set.
- Screen in service flagged per thousand released by release month, twelve months to Feb 2027, reviewed by outcome: NOT forced. The release amendments table (245 released_date, 121 hetx_call, 1 review_outcome changes) was raised after the month closed. Applied: released 2,347 2,461 2,417 2,685 2,593 2,697 2,508 2,453 2,546 2,417 2,378 2,282; flagged per thousand 15.8 15.4 14.5 20.1 14.3 14.8 16.7 19.2 18.5 19.4 21.4 18.0. As filed (release_volumes_monthly denominators, no amendments): 18.4 21.1 18.2 22.0 17.0 17.8 19.1 22.4 23.6 24.4 26.5 23.2. Reviewed ones by outcome per thousand (applied): FLAGGED 4.3 1.6 2.5 2.2 2.3 2.2 2.4 4.5 3.1 4.1 6.3 1.3; CLEARED 30.7 27.6 30.2 33.9 27.4 30.4 34.3 26.1 23.6 27.7 31.5 25.4. Forks: amended or as reported; denominators from the volume file or recounted; amendments by specimen_id hit 1,449 specimens that appear on two RELEASED rows (30 amendments touch them), so which row; whether flagged means hetx_call FLAG, and how AUTO flagged vs REVIEWED (61 REVIEWED rows have hetx CLEAR but outcome FLAGGED) are split. Received timestamps being UTC does not matter since release month is the key.
- Dilution panel by level: forced given the prepared level of stock NS-27-04 (the only stock with replicates; NS-27-07 has prepared levels but no results). Recovery = recovered / prepared level, medians L1 0.878, L2 0.865, L3 1.027; within a fifth: L1 6 of 9, L2 7 of 9, L3 6 of 9 (the voided L3 replicate 10 excluded, 28 reported). Fork if the label (0.4, 1.6, 6.4 per cent) is used instead: medians 0.900, 0.881, 1.009 and counts 6, 7, 6, and if stock NS-27-07 prepared levels were wrongly used the medians would be 0.923, 0.898, 1.066.
- detection_gain_by_cutoff.png: forced for the points (0.51, 4.07, 4.58, 6.87, 8.65 pp or 2, 16, 18, 27, 34 specimens). Interval bounds are method dependent; chosen cutoff marking depends on the paired/unpaired choice.

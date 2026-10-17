# leak check, task195

**Verdict: REVIEW.** 19 files read, 32 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: paired, specimen, asserted, difference, estimate, verdict, nothing, decisive, comparison, sentence, estimator, uncertainty, window, laboratory, accepted, cutoffs, method, intervals, population, golden, corpus, parallel, closed, protocol, two-sample

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `method_validation_protocol_kval07.pdf`: carries 8 of 10 distinctive words of the committed call: 'Replace the contamination screen in service with the re-run mixture-fraction screen at the 0.030 cutoff for the quarter '

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `extraction_platform_validation_2025.pdf`: 3 of 25 stump-paragraph terms appear (specimen, laboratory, method); read whether the document names the move
- **REVIEW** `method_validation_protocol_kval07.pdf`: 10 of 25 stump-paragraph terms appear (specimen, verdict, comparison, estimator, laboratory, accepted); read whether the document names the move
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

## Solver's-eye read (pass 3)

# reader_answers, task195 (solver's-eye; read only prompt.txt, bundle/, brief)

## Committed answer
Replace the screen from 1 July 2027 at cutoff C2 (mixture fraction >= 0.030). Confidence about 75 percent. The 25 percent is the paired against unpaired interval fork (see 1, 6, 7). An unpaired two-proportion interval gives C4 (0.015).

Comparison population (KVAL-07 3.1 to 3.5): 393 MIXED and 5,446 CONCORDANT specimens (5,839).
- Received 1 Mar to 31 May 2027, agreement_ref empty (303 KT-ALPHA and 276 KT-BORG excluded).
- Accepted QC read, with a re-run row on the accepted read set (6,106 read sets; 176 cohort accepted specimens have no re-run row, 38 re-run specimens have a QC "N" read).
- Register verdict MIXED or CONCORDANT (35 INCONCLUSIVE dropped; 194 have no verdict).
- Verdict collapsed to the specimen. This has no effect, because the 5 specimens with an A1 CONCORDANT and A2 MIXED conflict were all received before March.

HETX (screen in service) detects 292/393 = 74.30 percent of events, with a false-call rate (FCR) of 91/5446 = 1.67 percent.

| Cutoff | Detects | Increase (specimens) | Increase (points) | FCR | Paired Wald 95% CI (points) | Unpaired 95% CI (points) | Clears? |
|---|---|---|---|---|---|---|---|
| C1 0.050 | 294 | +2 | 0.51 | 1.12% | -2.03 to 3.05 | -5.58 to 6.60 | no |
| C2 0.030 | 308 | +16 | 4.07 | 1.36% | 1.37 to 6.77 | -1.86 to 10.01 | paired yes, unpaired no |
| C3 0.020 | 310 | +18 | 4.58 | 1.47% | 1.89 to 7.27 | -1.33 to 10.49 | paired yes, unpaired no |
| C4 0.015 | 319 | +27 | 6.87 | 1.56% | 3.91 to 9.83 | 1.07 to 12.67 | yes under both |
| C5 0.010 | 326 | +34 | 8.65 | 1.91% (above 1.67, fails 4.1b) | 5.53 to 11.77 | 2.95 to 14.35 | fails FCR |

FCR counts are 61, 74, 80, 85 and 104 false calls of 5,446.

Discordant pairs, candidate only against HETX only: C1 14/12, C2 23/7, C3 24/6, C4 32/5, C5 38/4.

Other paired methods agree on C2 clearing: Newcombe paired (1.36, 6.84), bootstrap (1.27, 6.87), exact McNemar p = 0.005.

## 1. Which sentence or file tells the decisive step?
Nothing names it. I searched all PDFs, the dictionary and the manifest for "paired", "same specimens", "McNemar" and "interval" and found none. The closest text is:
- KVAL-07 4.1(a): "the increase in confirmed contamination events detected over the screen in service is established with a 95 per cent interval above zero". It names no interval method.
- KVAL-07 3.4: "Detection is counted per specimen. A screen detects ... when it flags that specimen." Together with 3.2 and 3.5 this makes both screens score the same specimens. That is the only structural hint that the data are paired.
- The model card says the estimator "does not use the specimen's heterozygosity", which is a mild independence hint.

No document teaches the paired method by example. No ordinary-looking column partitions candidates on the property. The reworked reference documents (protocol, model card, dictionary) do not point at the move.

The only wording that leans on the problem is the model card addendum: "91.6 per cent below the limit of detection", "limit of detection about 0.008", and "where a share falls relative to any screening cutoff is KVAL-07's matter". It pulls toward "the estimator is unreliable at low cutoffs, hold". It does not name the paired interval.

## 2. Which file ranks or scores the candidates?
None. The model card addendum gives percentiles and a LOD share, but no per-cutoff detection or ranking. The register gives the reference verdicts, not a ranking.

## 3. Which file exists only to help the analyst?
- export_manifest.csv and validation_extract_dictionary.csv are navigation aids.
- plate_layout_map_2027q2.csv and lims_run_log_2027-03_2027-05.csv largely duplicate fields already in the QC exports. The run log adds only the received time, the batch and a control threshold; the plate map adds control_well.
- assay_unit_costs_2027.csv and extraction_platform_validation_2025.pdf are plainly unused distractors.
- release_volumes_monthly is a trap denominator, because its counts equal RELEASED rows rather than distinct specimens.

## 4. Which figure or name reads as the answer?
None reads as the answer. "91.6 per cent below LOD" is the loaded statistic. The cutoff C5 = 0.010 sits just above the LOD of 0.008, and C5 has the largest raw gain, so it is the attractive wrong answer. It is blocked only by 4.1(b) (FCR 1.91 against 1.67).

## 5. Which filed sentence fixes the figure, and its literal result?
KVAL-07 4.1: "replaced ... at the highest cutoff value listed in Table 2 at which both of the following hold ... (a) ... 95 per cent interval above zero, and (b) ... false-call rate is not higher than the screen in service's". It fixes the cutoff ordering (highest value first: C1 0.050, C2 0.030, ...) and the FCR test. It does not file the interval method or the unit of the interval.
- Literal result with a paired interval (the same 393 events scored by both screens): C1 fails (a); C2 passes (a) (lower bound +1.37 points) and (b) (1.36 against 1.67), so the answer is C2.
- Literal result with an unpaired interval: C2 (-1.86), C3 (-1.33) and C1 fail (a); C4 passes both, so the answer is C4.

The population is filed by 3.1 to 3.5 and is unambiguous.

## 6. What decides the main answer?
An analytical choice: the interval for the increase. It must respect that both screens flag the same confirmed events (paired difference, McNemar-type), not two independent proportions.
- The easy route (two-proportion Wald or Newcombe on 308/393 against 292/393) files C4.
- The careful route (paired) files C2.
- Population construction is data cleaning and rule application. It does not flip the call: wrong populations such as including contract receipts, top-up read sets or an unfiltered register still give C2 or C4 depending on the interval.
- The decision is not semantics. Only the interval's pairing, which no sentence states, decides.

## 7. The work, and what the documents did not decide
Results are in the committed answer above. Choices the documents left to me:
1. Paired against unpaired interval, and which paired method. Wald, Newcombe paired, bootstrap and exact all agree for C2.
2. Whether HETX "flag" means hetx_call (which I used, per 3.4) or the reviewed outcome. In this comparison 3 REVIEWED rows are CLEAR with het at or above 36.5, and 10 are FLAG with het below 36.5, so the QC call is not a pure threshold. I followed 3.4 literally.
3. Collapsing aliquots to specimens, and treating any MIXED aliquot as a MIXED specimen. This does not matter here (see above).
4. "Points" taken as percentage points of the 393 events; counts are specimens.
5. Treating "highest cutoff value" as the highest numeric value (C1) and walking downward.
6. Multiplicity across five cutoffs: no adjustment is filed; I applied none.

Because C2 and C4 are two defensible calls from a single unfiled choice, that choice is the whole decision.

## 8. Realism, bluntly
Reads mostly as generated with good surface mess. The mess includes decimal commas, semicolons, the 111 voided reads, re-sent reports, case typos and the contract projects.

Specific tells:
- mixture_fraction_rerun_v34.csv: read_set_id steps by exactly +2 in 5,445 of 6,245 rows (+4 for a top-up, +0 for the rest) and never irregularly. That is an arithmetic stride.
- dilution_panel_2027q1.xlsx: read-set IDs step by exactly 3 (RS27-D04100, D04103, ...). Level 'l1', 'l3' lowercase typos look sprinkled. "Replicates planned 9" yet a 10th L3 row appears as "voided".
- qc_screen_calls (both): mean_depth, dna_ng_ul and het_excess_pct look uniformly drawn. dna_ng_ul has quartiles of about 54, 96 and 140 across 11.6 to 184, which is a uniform spread with no right tail, whereas real yields skew. Depth runs 26 to 71, flat.
- AUTO calls are an exact het_excess >= 36.5 for all 5,909 AUTO rows. Real HETX would have some instrument or plate drift, not zero exceptions.
- identity_panel_register_2027.csv: panel_markers_typed is 96 (54%), 88, 89, 90 and 91 in near-identical counts (952, 943, 999, 614), so a uniform draw. INCONCLUSIVE rows sit at 30 to 45 markers. The share is low-variance and monotone with the rerun estimate (Spearman 0.92 on the 393 MIXED).
- qc_screen_history: receipt UTC hours spread 4 to 20 as a smooth bell with uniform seconds, wider than the 7 to 17 local log window; duplicate-specimen rows carry identical received_utc to the second.
- The history extract is "pulled 2027-03-04" but carries 1,291 released_date values in March 2027 and two in April 2027. Amendments dated up to 2027-05-06 exist for rows whose before-values already show the corrected value in 8 percent of cases.
- Too-exact reconciliation:
  - release_volumes_monthly counts equal the history's RELEASED row counts for all 12 months.
  - The weekly PDF counts equal register row counts for all 20 weeks, with W05 at 44 and the rest at 75.
  - The model card addendum (6,106; median 0.0022; 91.6%) equals the file.
- Dates: the validation protocol, "approved 2027-02-19", names a 21 June 2027 cut and 31 May end that are the manifest's own pull date. The dictionary "issue 4, 2027-02-19" lists files that cover March to May 2027, which is anachronistic. Weekly PDFs are text-extractable although "scanned on receipt".
- Real-looking elements: only 2 reception points, received_by with two initials, the late-report footnote, vial reuse under a second accession (NFG27-16xxxx), the crosswalk's vials shared across two accessions.

Documents built for the analyst:
- extraction_platform_validation_2025.pdf is a pure distractor with no tie to the screen.
- assay_unit_costs_2027.csv carries no decision link.
- lims_run_log and plate_layout_map are redundancy that a real LIMS would not export alongside the QC export.

The three reworked documents (protocol, model card, dictionary) now carry owners, issue histories and licences, and read much more like the organisation's own. They still show several tells:
- The model card's revision table skips 3.3 and uses wrapped, misaligned cells.
- The dictionary's last_reviewed is 2026-06-15 for fields that did not exist then.
- The protocol's "Sections 1, 2, 6 and 7 ... not reproduced" is a conspicuous extract.
- The protocol's date anachronism above.
A real version would carry change-request numbers, signatures and document control IDs.

## 9. Asks, one by one

**(a) Per cutoff: detects, increase (specimens and points), FCR, interval test, recommendation.**
Figures are in the table above.
- Counts, FCR and the point gains are forced by the filed population.
- Not forced: "clears the interval test" for C2 and C3 (paired yes, unpaired no), and therefore the recommendation. The second defensible value is C4 with the unpaired Wald or Newcombe route (C4 lower bound +1.07 points). Nothing quotable forbids the unpaired reading.
- C1 (no) and C5 (fails FCR) are forced.

**(b) Per weekly report issued in April or May: distinct vials and the excess of results over them.**
Vials are distinct biobank_ref per report (via the crosswalk); results are the report's register rows. Reports W13 to W21 give:

| Report | Results | Vials | Excess |
|---|---|---|---|
| W13 | 589 | 575 | 14 |
| W14 | 608 | 596 | 12 |
| W15 | 613 | 601 | 12 |
| W16 | 641 | 628 | 13 |
| W17 | 577 | 563 | 14 |
| W18 | 554 | 541 | 13 |
| W19 | 570 | 555 | 15 |
| W20 | 542 | 519 | 23 |
| W21 | 564 | 538 | 26 |

- This is forced: the PDF counts equal the register rows, and "vial" is defined in the dictionary as biobank_ref.
- W19 "issued two working days late" is still in May, so there is no fork.

**(c) Screen-in-service flags per thousand released, by review outcome, twelve months to Feb 2027, each counted once.**
I applied the amendments, counted by distinct released specimen, and assigned each specimen to its release month (first or last row gives the same table).

Unreviewed AUTO flags per thousand:

| Month | Rate |
|---|---|
| 2026-03 | 11.6 |
| 2026-04 | 13.6 |
| 2026-05 | 11.3 |
| 2026-06 | 12.9 |
| 2026-07 | 11.8 |
| 2026-08 | 12.8 |
| 2026-09 | 15.1 |
| 2026-10 | 14.9 |
| 2026-11 | 16.4 |
| 2026-12 | 14.9 |
| 2027-01 | 15.0 |
| 2027-02 | 14.7 |

Reviewed outcome FLAGGED per thousand:

| Month | Rate |
|---|---|
| 2026-03 | 4.0 |
| 2026-04 | 1.7 |
| 2026-05 | 2.6 |
| 2026-06 | 2.0 |
| 2026-07 | 2.4 |
| 2026-08 | 2.3 |
| 2026-09 | 2.5 |
| 2026-10 | 4.7 |
| 2026-11 | 3.3 |
| 2026-12 | 3.9 |
| 2027-01 | 5.7 |
| 2027-02 | 1.4 |

Reviewed outcome CLEARED (hetx FLAG) per thousand:

| Month | Rate |
|---|---|
| 2026-03 | 2.2 |
| 2026-04 | 2.1 |
| 2026-05 | 2.2 |
| 2026-06 | 5.1 |
| 2026-07 | 1.6 |
| 2026-08 | 1.5 |
| 2026-09 | 1.7 |
| 2026-10 | 2.1 |
| 2026-11 | 1.2 |
| 2026-12 | 2.2 |
| 2027-01 | 3.1 |
| 2027-02 | 3.2 |

Distinct released specimens per month (the denominator): 2243, 2353, 2302, 2549, 2468, 2582, 2387, 2348, 2437, 2288, 2271, 2173.

Not forced. The forks are:
- Applying the release-desk amendments or not. Without them, the AUTO flag counts rise by 6 to 14 a month (for example March 2026 is 32 not 26, and the combined rate is 18.3 not 15.6), and the denominator changes slightly (2238 for March).
- Using the monthly pack row counts (2,342 and so on) as the denominator instead of distinct specimens.
- Whether "flagged" means hetx_call FLAG or the final disposition (reviewed ones by outcome).
- Which row's month a two-row specimen takes. This does not matter in aggregate, but an amendment to a row on a two-row specimen is ambiguous.

The wording "each counted once" and "reviewed ones by their review outcome" closes most of it, but the amendment application is a quotable-neither-way choice.

**(d) Dilution panel by level: median recovery (share of prepared) and count within a fifth.**
Prepared levels are the NS-27-04 gravimetric values, because the replicates name that stock. The 10th L3 row is voided and excluded.

| Level | Median recovery | Within a fifth (0.8 to 1.2) |
|---|---|---|
| L1 | 0.878 (n=9) | 7 |
| L2 | 0.865 (n=9) | 7 |
| L3 | 1.027 (n=9) | 6 |

- This is essentially forced. No value sits on a boundary.
- The second values come from using the other stock's prepared levels (NS-27-07: 0.923, 0.898, 1.066, same counts) or the nominal labels (0.900, 0.881, 1.009). Both contradict "prepared level" and the Stock column.
- Recovery to 3 decimals as filed.

**(e) detection_gain_by_cutoff.png.** Plot the increase with its interval per cutoff, a zero line and the marked cutoff. The chart changes with the interval method: paired C2 marked, unpaired C4 marked.

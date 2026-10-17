# Determinism verdict, task195

Isolation: read only prompt.txt, submission_blocks.md, judge_brief.md and target/ (19 files). Scratch scripts in scratch/. Nothing outside this directory was opened.

**Verdict:** NOT_DETERMINISTIC (main recommendation is forced and reproduces; supplementary answers 3 and 4 each admit a second licensed handling). Label: competing_defensible_answer. Blocks are not SOLUTION_WRONG: every block figure reproduces under the handling it chose.

**Disposition:** FIX_NOW. Pin the identity of "specimen" for the weekly ask and the numerator/denominator/amendment basis for the monthly ask in validation_extract_dictionary.csv (or the prompt, which is already at 998 of 1,000 characters, so the dictionary is the place). The main call, the ladder and every graded main-call figure stay byte-identical, so no rerun of the main-call side is needed; the two asks are re-keyed.

**Why:** Main call 0.030 reproduces exactly (5,839 / 393 / 5,446; 292 and 91; 294, 308, 310, 319, 326; 61, 74, 80, 85, 104) and holds under every paired interval estimator and every alternative population. Supplementary 4 (monthly rate) has a pack denominator reading (release_volumes_monthly, "results_released") that gives 14.9 for 2026-03 against the golden 15.6, and the two differ in all twelve months; supplementary 3 (weekly) has an accession-count reading that gives 4,6,5,3,7,4,6,5,5 against the golden 11,14,13,9,16,14,14,26,22. Each fork is closed only by the author's narration, not by a sentence in a shipped file.

## Evidence: reproduction table (all from target/ at stated grain)

| Block figure | Recomputed | Status |
|---|---|---|
| Comparison 5,839 (393 MIXED, 5,446 CONCORDANT) | 5,839 / 393 / 5,446 (cohort codes, accepted QC read, accepted read set mixture fraction, MIXED or CONCORDANT verdict) | reproduced |
| Screen in service 292 events, 91 false calls, 1.67% | 292, 91, 1.6710 | reproduced |
| Detected 294/308/310/319/326 | same | reproduced |
| Increase 2/16/18/27/34, pp 0.51/4.07/4.58/6.87/8.65 | same | reproduced |
| False-call 1.12/1.36/1.47/1.56/1.91 (61/74/80/85/104) | same | reproduced |
| Interval at 0.030, 1.37 to 6.77 | paired Wald on discordant specimens (b=23, c=7): 1.369 to 6.773 | reproduced, estimator specific |
| Cutoff flags (no, yes, yes, yes, yes) and (yes, yes, yes, yes, no) | same under paired estimators | reproduced |
| Recommended 0.030 | 0.030 | reproduced |
| Weekly 577,598,600,627,564,552,541,531,529 and diffs 11,14,13,9,16,14,14,26,22 | reproduce only as distinct biobank_ref (accession where no crosswalk row) among all register rows of the report; totals from PDF 588,612,613,636,580,566,555,557,551 | reproduced under one handling; second handling differs (finding) |
| Monthly 15.6,15.3,13.9,14.9,14.2,15.1,17.6,19.6,19.7,18.8,20.7,16.1 | reproduce only with amendments applied (dates, hetx_call, one review_outcome), RELEASED rows deduplicated to specimens, numerator and denominator both distinct specimens recomputed (pack discarded) | reproduced under one handling; others differ in every month (finding) |
| Dilution L1/L2/L3 medians 0.878/0.865/1.027; within-a-fifth 6/7/6 | 0.87805/0.86503/1.02703 on NS-27-04 prepared levels 0.0041/0.0163/0.0629 (labels upper-cased, voided row dropped); 6/7/6 | reproduced |

## Probe 1: the interval

File and columns telling how the calls on one specimen came to exist: qc_screen_calls_gsqa/gsqb (specimen_id, read_accepted, hetx_call) and mixture_fraction_rerun_v34.csv (specimen_id, read_set_accepted, mixture_fraction), joined on specimen_id; model card says the estimate is "computed from the read set alone", KVAL-07 3.1 "parallel run", 3.2 same specimens, 3.4 "Detection is counted per specimen". Both calls are therefore on one specimen's own read sets.

Increase and discordant cells (candidate-only b, service-only c), n=393 events:

| cutoff | b | c | increase | paired Wald | Newcombe paired | Tango score | paired bootstrap | McNemar exact p | unpaired Wald | unpaired Newcombe | unpaired bootstrap |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.050 | 14 | 12 | 0.51 | -2.03, 3.05 | -2.06, 3.09 | -2.13, 3.25 | -2.04, 3.05 | 0.845 | -5.58, 6.60 | -5.57, 6.59 | -5.60, 6.62 |
| 0.030 | 23 | 7 | 4.07 | 1.37, 6.77 | 1.36, 6.84 | 1.43, 7.08 | 1.53, 6.87 | 0.0052 | -1.87, 10.01 | -1.88, 9.98 | -2.04, 9.92 |
| 0.020 | 24 | 6 | 4.58 | 1.89, 7.27 | 1.88, 7.34 | 1.97, 7.60 | 2.04, 7.38 | 0.0014 | -1.33, 10.49 | -1.35, 10.47 | -1.27, 10.43 |
| 0.015 | 32 | 5 | 6.87 | 3.91, 9.83 | 3.93, 9.91 | 4.08, 10.16 | 4.07, 9.92 | 7e-6 | 1.07, 12.67 | 1.05, 12.64 | 1.02, 12.72 |
| 0.010 | 38 | 4 | 8.65 | 5.53, 11.77 | 5.56, 11.86 | 5.75, 12.11 | 5.60, 11.96 | 6e-8 | 2.95, 14.35 | 2.92, 14.32 | 2.80, 14.25 |

(Also checked at 0.030: Agresti-Min corrected lower 1.32, continuity-corrected Wald lower 1.24, Bonferroni 99% over five cutoffs lower 0.52. Zero is crossed only at z = 2.95; the lower bound reaches 0 if service-only events c rise from 7 to 12.)

Every paired estimator establishes 0.030, 0.020, 0.015, 0.010 and not 0.050 (z = 0.39), so the committed 0.030 stands. Every unpaired (independent-proportions) estimator establishes only 0.015 and 0.010, so it files 0.015 (false-call 1.56 < 1.67 passes), a different cutoff. A non-overlap of each screen's own Wilson interval gives hold (only 0.010 separates, and it fails 4.1(b)), the "Not holding" route in block 1. Whether the interval estimator moves the cutoff: yes, between paired and unpaired. The shipped files close it to paired by 3.1, 3.2, 3.4 (one set of specimens, per-specimen detection) and by the data: independence of the two calls on the 393 events is rejected at chi2(1) = 248 (phi 0.79) at 0.030, observed discordant 30 against 142 expected under independence. No shipped sentence names the estimator, so the closure is structural, not quoted. I accept it as forced because an unpaired interval contradicts the 3.2 matched comparison, but the quoted block 1 endpoints 1.37 and 6.77 are Wald specific (paired lower bounds run 1.36 to 1.53, upper 6.77 to 7.08); nothing in the asks grades those endpoints except the png.

## Probe 2: the population

Literal 3.1/3.2: 5,839 comparison specimens, 393 events, 5,446 clean. Alternatives and their effect (all keep 0.030 as highest meeting both rules):
- Contract receipts (579 KT-ALPHA/KT-BORG, with agreement_ref): none has a re-run mixture fraction (config: not in archive path), so cannot enter; excluded by 3.1 anyway.
- INCONCLUSIVE (35 in the register, none violate the comparison) as clean: n_clean 5,481, service false-call 1.66, 0.030 1.35.
- Specimens with no verdict (194 with accepted read and accepted set, no register row) as clean: 5,640, 1.67 vs 1.35.
- Both: 5,675, 1.66 vs 1.34.
- Voided reads (111 N rows, 73 later re-read as a Y row on another plate): carry no call, no effect; 3.2 needs an accepted read.
- Second (non-accepted) read sets (139): using the larger mixture fraction per specimen gives identical counts.
- Control wells (plate_layout_map control_well Y, 124 in the comparison): not mentioned by KVAL-07; excluding them gives 5,715 / 385 / 5,330, increase 16 (4.16 pp), lower 1.40, 0.030 still chosen; no file licenses the exclusion.
- Verdict date clause (reported on or before 21 June): inert, register max 2027-06-18.
- Six specimens carry A1 CONCORDANT and A2 MIXED, but none is in the comparison; four in-comparison specimens have two register rows, all CONCORDANT (resend or A2), so no conflict.

## Probe 3: the rule's direction

Failing: 0.050 fails 4.1(a) (interval -2.03 to 3.05); 0.010 fails 4.1(b) (1.91 > 1.67). Passing both: 0.030, 0.020, 0.015. "Highest cutoff value" is quoted from 4.1 and Table 2 lists values, so 0.030. A second reading ("highest" as the last row C5 or the most sensitive) gives 0.010, which fails (b) and so cannot be reached; the most-sensitive-that-passes reading gives 0.015, but violates "highest cutoff value". Not open. Note 4.1(b) is a point comparison, and the false-call differences are not themselves distinguishable from noise (paired exact p for candidate against service: 0.16 at 0.030, 0.33 at 0.010), but because the rule says "not higher" and 0.030 is above 0.010 whatever treatment of (b), the call does not move.

## Probe 4: the three non-recommendation answers

**Weekly (ask: "the specimens with any verdict against the total of each weekly report issued in April and May").** Identifier used: identity_panel_register_2027.csv report_ref grouped, specimen identity from specimen_request_crosswalk.tsv biobank_ref (fallback specimen_id where there is no crosswalk row: 354 rows in W13 to W17 have none). Totals from identity_panel_weekly_reports_2027.pdf; they equal the register row counts exactly (resends included). Nine reports W13 to W21 issued 2 April to 28 May (W19 "two working days late" stays in May).
Two handlings survive, each with a quotable sentence. Dictionary: "specimen_id ... The laboratory accession, one per specimen received" gives distinct accession counts 584,606,608,633,573,562,549,552,546 and differences 4,6,5,3,7,4,6,5,5. Dictionary: biobank_ref "A specimen re-accessioned for a repeat request carries one reference across its accessions" gives the golden 577,598,600,627,564,552,541,531,529 and 11,14,13,9,16,14,14,26,22. Accession plus aliquot gives 586,608,610,635,575,564,551,554,548. The sign of the difference is also not given by the asking sentence. FINDING (Gate C/E on supplementary 3). Where a re-accessioned specimen has no crosswalk row (the 354 rows) the golden silently treats it as one specimen.

**Monthly (ask: "the screen in service's flagged specimens, reviewed ones by their review outcome, per thousand released by release month for the twelve to February 2027").** Identifiers: qc_screen_history specimen_id, hetx_call, call_source, review_outcome, release_status, released_date; release_amendments (specimen_id, field, value_after); release_volumes_monthly results_released. Flagged = hetx_call FLAG for AUTO, review_outcome FLAGGED for REVIEWED (single reading, quoted from the ask). Forks, each licensed by a quotable sentence:
- Amendments (dictionary: value_after is "the value the record carries after the amendment"; manifest: raised after the month closed) applied or not.
- Duplicates: 1,449 specimens have two RELEASED rows (two plates). Counting rows or specimens.
- Denominator: the pack's results_released (matches the raw extract row counts by original release month exactly, 2,342 ... 2,281, so it is pre-amendment and counts duplicate rows) or specimens recomputed after amendments (2,243 ... 2,173).
2026-03 to 2027-02 under the main variants:
| variant | 2026-03 | 04 | 05 | 06 | 07 | 08 | 09 | 10 | 11 | 12 | 2027-01 | 02 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| golden: amended, specimens, recomputed specimens | 15.6 | 15.3 | 13.9 | 14.9 | 14.2 | 15.1 | 17.6 | 19.6 | 19.7 | 18.8 | 20.7 | 16.1 |
| amended, distinct flagged specimens, pack denominator | 14.9 | 14.6 | 13.2 | 14.2 | 13.5 | 14.5 | 16.7 | 18.8 | 18.8 | 17.8 | 19.8 | 15.3 |
| amended, rows, pack | 15.8 | 15.0 | 13.7 | 16.0 | 14.3 | 14.8 | 16.7 | 20.4 | 19.6 | 19.9 | 21.0 | 15.8 |
| raw extract, rows, pack | 18.4 | 20.7 | 17.4 | 17.9 | 17.0 | 17.8 | 19.1 | 23.7 | 24.7 | 24.8 | 26.5 | 21.0 |
| raw, distinct specimens, recomputed | 18.3 | 21.2 | 17.8 | 16.9 | 17.0 | 18.2 | 20.1 | 23.0 | 25.0 | 24.0 | 26.4 | 21.6 |
The ask says "flagged specimens" and "per thousand released"; the only shipped denominator is the pack's "results_released", whose literal use gives the second row. The golden requires discarding the pack because it is pre-amendment and counts duplicate results; no shipped sentence says so. FINDING (Gate C/E on supplementary 4): every month differs between the golden and the pack-literal handling by 0.6 to 0.9 per thousand, far outside the one-decimal rounding.

**Dilution (ask: median recovery as a share of the prepared level and how many results fall within a fifth).** Level = Level (case-normalised from l1/l2/l3), prepared value = "Prepared level (fraction)" joined on Stock+Level, value = "Recovered fraction". Replicates exist only for stock NS-27-04, so the prepared levels 0.0041/0.0163/0.0629 are forced by the Stock column (NS-27-07 has none). Voided row (L3 rep 10, no result) dropped. Medians 0.878, 0.865, 1.027; within 20% inclusive or strict: 6/7/6 (no tie; closest values are relative deviations 0.1951 in L1 and 0.2258 in L3). Alternatives not licensed: nominal label (0.4%) gives 0.900, average of the two stocks gives 0.900; the sheet's "Prepared level (fraction)" is the gravimetric value and the Stock key selects it. One determinate answer.

## Question 1: is the method forced, or forced only by data that cannot separate the candidates?

Neither failure side. (a) The paired family is not agreement through absence of noise: the data are real binomial counts (b+c = 30 discordant specimens at 0.030, SD of the increase 1.38 pp, z 2.95), and the estimators do disagree in the second decimal (paired lower bounds 1.36 to 1.53, uppers 6.77 to 7.08). But their differences (about 0.17 pp on the lower bound) are 0.12 of one standard error and cannot reach a decision line: the nearest line is the 0.030 lower bound at 1.4 pp (z 2.95 from zero) and the 0.050 lower bound at -2.0 pp (z 0.39 from zero). All defensible paired estimators therefore agree on every cutoff's pass or fail. (b) The paired and unpaired families do differ in outcome, by far more than their sampling error (lower bound 1.37 against -1.87 at 0.030, a 3.2 pp gap against a 1.38 pp SE), and the data separate them: independence of the two calls is rejected at chi2 = 248 (1 dof) at 0.030, 268 at 0.050, 198 at 0.010, so the unpaired variance (SE 3.03 pp) is 2.2 times the real SE. The method is forced by the matched structure, not by the data being unable to speak. (c) Sampling-noise plausibility, chi-square per degree of freedom measured: weekly MIXED rate by receipt ISO-week over the 14 weeks, 15.9 / 13 = 1.23 (p 0.25), plausible binomial; monthly MIXED rate, 0.32 / 2; dilution replicates, Bartlett over log recoveries 2.35 / 2 = 1.18 (p 0.31), CVs 23%, 14%, 18% (L1 SD 0.00079 against the model card's "within about 0.002" for repeats, implied sigma about 0.0007, chi2/dof about 1.2 on 8 dof); candidate detection against panel share, Hosmer-Lemeshow chi2/dof 0.0 to 0.7 for the five cutoffs (near step functions of the typed share, as a threshold on a monotone estimator should be: log ratio of mixture fraction to typed share has SD 0.29 and only events within that band of a cutoff can flip); HETX flag against typed share, chi2/dof 19.1 / 8 = 2.39 (p 0.014), overdispersed, as expected since HETX is driven by heterozygosity excess, not by share; weekly false-call (service flag among clean) 31.7 / 13 = 2.44 (p 0.003), mild overdispersion that does not touch the rule because 4.1(b) is a point comparison. So the record carries the noise a real validation would, not none, and the stated two-decimal rounding on counts-derived percentages is exact arithmetic on integers, not a precision claim. The one place two decimals claim more than the data carry is the interval endpoints in block 1 and the png (estimator-dependent to 0.2 pp, and the 0.030 uncertainty itself is 2.8 pp wide).

## Question 2: rounding edges

Distance of each figure from the nearest rounding flip, as a fraction of the half-unit (a value at the centre of its rounded cell scores 1, a figure on the edge scores 0), computed on 0.01 pp or 0.001 units.

- Increase (pp): 0.51 (0.5089), 4.07 (4.0712), 4.58 (4.5802), 6.87 (6.8702), 8.65 (8.6514). Distance to the nearest rounding edge 0.0039, 0.0038, 0.0048, 0.0048, 0.0036 against a half-unit of 0.005, so none is within 0.0036 of a flip, but one event moves the increase by 0.254 pp, so one more row moves each figure across about 25 rounding cells (it changes the figure, not just the rounding).
- False-call rates: 1.6710, 1.1199, 1.3589, 1.4688, 1.5607, 1.9096; edge distances 0.0040 to 0.0049 of 0.005. One more false call moves a rate by 0.018 pp (0.030 would read 1.38, the service 1.69), so 0.030 stays below the service until 17 more false calls (74 to 91) and 0.010 stays above until 13 fewer.
- Interval bounds (block 1 and png only): 1.369 is 0.0045 from an edge, 6.773 is 0.0020 from 6.775; elsewhere the paired Wald bounds at 0.010 (lower 5.5354, 0.0004 from 5.535), 0.020 (lower 1.886, 0.0014) and 0.015 (lower 3.914, 0.0013) sit closest to edges. Estimator choice moves these by 0.1 to 0.3 pp, so two-decimal endpoints are not graded-safe.
- Monthly per thousand (golden basis): 15.604, 15.300, 13.901, 14.908, 14.182, 15.105, 17.595, 19.591, 19.696, 18.794, 20.696, 16.107. Smallest distance to an edge is 2026-07 (14.1815, 0.0315 of 0.05); none is within 0.03 of a flip. One more flagged specimen adds 0.37 to 0.46 per thousand (it moves the one-decimal figure by 4 cells); one more clear specimen changes none of the twelve.
- Dilution medians: 0.87805, 0.86503, 1.02703; edge distances 0.00045, 0.00047, 0.00047 of 0.0005. Each is a single replicate (n=9). A tenth replicate would make the median the mean of two middle replicates and move it by about half the gap to its neighbour (L1 neighbours 0.0036 and 0.0037 or 0.0033, L2 0.0141 and 0.0142 or 0.0137, L3 0.0646 and 0.0675 or 0.0615): a change of 0.01 to 0.04 in the ratio, beyond rounding.
- Within-a-fifth counts: L1's 0.0033 replicate is 19.51% from the prepared level, 0.49 points inside the 20% line; four-decimal storage (half-unit 0.00005 = 1.2% of 0.0041) is larger than that margin, but the shipped number is the number, so 6 stands. L3's 0.0435 and 0.0771 sit at 30.8% and 22.6%; L2's 0.0102 at 37.4% and 0.0173 at 6.1%.

So no graded figure is within 0.0035 of its rounding edge on the shipped arithmetic; the nearest boundary of any graded answer is the L1 within-a-fifth count (0.1951 against 0.2000), and the nearest rounding edges are the unasked interval bounds (0.0004 to 0.0014).

## Gates

A: main call and critical components reproduce (table). Pass for the main side; supplementary answers 3 and 4 reproduce only under the author's handling (Gate A on the arithmetic passes, the fork is Gate C).
B: every decisive fact present in the shipped files. Pass. KVAL-07 gives population, definition and rule; Table 2 the cutoffs.
C: main call passes (paired estimators agree, population alternatives agree, direction closed by "highest cutoff value"). Fail on supplementary 3 (accession vs biobank_ref) and 4 (pack vs recomputed; amended vs raw; rows vs specimens). Label competing_defensible_answer.
D: the main difficulty (paired vs independent comparison) is analytical, not a word. Pass. The asks' forks are semantics, which asks may carry, but they must still close.
E: main ask unambiguous. Fail on supplementary 3 and 4 as above: key terms ("specimens", "released") have readings giving different numbers.
F (stump power): a strong model that sees both screens' calls per specimen will usually pair, and McNemar-type reasoning is common; the wrong routes are unpaired interval difference (files 0.015) or own-interval non-overlap (files hold); 0.050 and 0.010 each fail on the stated rules. Moderate stump power on the main call; most grading difficulty sits in the asks 3 and 4, where the forks above would stump careful solvers for a semantics reason, which is not stump power the build can claim.
G: see line. H: see line.

## Files/Hygiene

PASS with notes. 19 files; formats csv (12), tsv (1), json (1), xlsx (1), pdf (4, two carrying tables), so five formats; qc_screen_history has 32,647 rows (>= 25,000); distractors present (extraction_platform_validation_2025.pdf, assay_unit_costs_2027.csv, plate_layout_map, lims_run_log, release_volumes_monthly for the main call). export_manifest gives source and pull date for each file but no license column; licence and provenance cannot be judged from the bundle (metadata.json is out of bounds), so I do not call it a finding. No temporal leak found: latest pull 2027-06-21, setting 1 July 2027. Nothing reads as LLM generated in file names; the dictionary and the validation extract do not narrate the answer. Exclusion-level finding: none.

## Stumping type

`mechanism: statistical_rigor`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The difficulty is judging the increase with its uncertainty on the matched specimens (and rejecting 0.050 as not established), on honest data with no reported number being wrong; on clean data it would still stump the same way.

## Three rules

`domain: pass`, `layers: pass`, `decisive_step: analytical`. Domain: validating a replacement contamination screen against a reference standard (paired detection gain with a confidence interval, false-call rate) is the method-comparison work a genomics QC laboratory does; swapping the nouns would not leave it unchanged because the typed second-contributor share, the estimator's limit of detection and the paired calls are what decide. Layer 1: decimal-comma semicolon exports from two instruments, voided and re-read plates, contract receipts, resent reports, amendments, a stale pack. Layer 2: paired interval on the discordant specimens. The easy route (interval from each screen's own proportion, or independent two-sample difference) files hold or 0.015 on the same cleaned data.

## Fix

Fix location: input_files (dictionary pin). 1) Supplementary 3: add to validation_extract_dictionary.csv that a "specimen" for report counting is one biobank_ref where the crosswalk has one, otherwise one specimen_id, and the sign (total minus specimens), or rekey the golden to the accession count 584... and 4,6,5,3,7,4,6,5,5. 2) Supplementary 4: add a row stating the pack's results_released is as booked at 2027-03-06 (before amendments, one per result) and that the rate is flagged specimens per thousand specimens released, each counted once, on the amended record; or key the golden to the pack basis (14.9, 14.6, ...). 3) Optionally state in the protocol or the dictionary that detection and false-call are per-specimen indicators on the same specimens (the WHAT), so the paired closure is quotable; keep the method open. Main call, ladder and graded main figures stay frozen.

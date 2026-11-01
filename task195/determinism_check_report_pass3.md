# determinism-check report, task195, 2026-11-01 (pass 3, reship redesign)

The determinism-judge agent had no Agent tool, so it wrote the brief (/tmp/determinism-check-task195-p3/judge_brief.md) and the main session spawned the one isolated thread from it (general-purpose, Sonnet, medium) on target.zip 0925f9258f072b09. The thread's verdict follows verbatim.

# Determinism verdict, task195 pass 3

- **Verdict:** NOT_DETERMINISTIC. The main recommendation and ask 1 are forced and reproduce. Asks 3 and 4 (and the supplementary answers built on them) rest on specimen-identity keys the prompt and shipped text never pin.
- **Disposition:** SEND_BACK. Pin the unit of "distinct specimens" (ask 3) and "each specimen counted once" (ask 4) in the prompt, or ship a definition in a filed document. The graded figures and the main call can stay. Because the prompt changes, a rerun is required.
- **Why:** Ask 3 asks for "distinct specimens its results came from". The golden counts distinct `biobank_ref` in specimen_request_crosswalk.tsv. Counting distinct `specimen_id`, the register's own specimen key, gives different answers for all nine reports. For BA-2027-W13 that is 585 and an excess of 4, against the golden 575 and 14. Ask 4 counts a specimen once by `extraction_id`. Counting by `specimen_id` gives different rates in every month (2026-03 is 17.6 per thousand against the golden 15.6). No shipped sentence says that two accessions on one biobank reference, or two accessions on one extraction, are one specimen. The only support is a crosswalk header line ("the biobank's own reference for the vial") and a model-card sentence about depth top-ups. Gates C and E fail on asks 3 and 4; the governing label is underspecified_objective.

## Evidence (recomputed from target/)

| Item | Result | Source |
|---|---|---|
| Comparison population: 5,839 specimens, 393 MIXED, 5,446 CONCORDANT | Reproduced | Accepted rows of qc_screen_calls_gsqa and gsqb, cohort codes only (all 579 agreement_ref rows are KT-*), joined to accepted rows of mixture_fraction_rerun_v34.csv and to MIXED/CONCORDANT register verdicts |
| Screen in service: detects 292, flags 91 of 5,446 clean, false-call rate 1.67 | Reproduced | QC export `hetx_call` |
| Candidate screen, cutoffs 0.050 / 0.030 / 0.020 / 0.015 / 0.010 | Detects 294 / 308 / 310 / 319 / 326; increase 2 / 16 / 18 / 27 / 34; points 0.51 / 4.07 / 4.58 / 6.87 / 8.65; false-call rate 1.12 / 1.36 / 1.47 / 1.56 / 1.91. All reproduced. | Same join, mixture_fraction thresholds |
| Discordant specimens (candidate only / screen in service only) | 14/12, 23/7, 24/6, 32/5, 38/4 | Same join |
| Paired interval lower bounds | 0.050 fails on every paired estimator (Wald -0.020, Tango-type -0.017, exact McNemar p 0.85). 0.030 clears on every one (Wald +0.0137, continuity-corrected +0.011, Tango-type +0.011, exact p 0.005). | Computed from the discordant counts |
| Interval-method fork (main call) | Unpaired difference of two proportions gives lower bounds of -0.019 at 0.030 and -0.013 at 0.020, so it would recommend 0.015 (lower bound about +0.011, false-call rate 1.56 below 1.67). Judging each rate against its own interval gives hold. The paired reading gives 0.030. | Computed. Nothing in KVAL-07 says "paired". The parallel run is on the same specimens, so paired is the statistically correct reading and I treat it as forced, but this is the one point where the golden depends on method choice. |
| Control wells (plate_layout_map `control_well`=Y, 126 specimens in the comparison) | Excluding them leaves the same increases (2/16/18/27/34), the same discordants and the same call. | Computed |
| Mixed-verdict aliquots (5 specimens, A1 CONCORDANT and A2 MIXED) | Not in the comparison, so no effect. | Register |
| Ask 3 under the golden key | Reproduced: 575/14, 596/12, 601/12, 628/13, 563/14, 541/13, 555/15, 519/23, 538/26. Results issued per report (589 ... 564) agree between the PDF and the register. | Distinct `biobank_ref` per `report_ref`, via the crosswalk |
| Ask 3 under competing keys, W13 | Distinct `specimen_id` 585 (excess 4); specimen+aliquot 587; plate_barcode 583; `request_id` 566. Excess is 4, 6, 5, 3, 7, 4, 6, 5, 5 for W13 to W21 under `specimen_id`. | Same files. 214 biobank refs each carry two accessions; the second accession exists only in the register and crosswalk, and the pairs often carry different verdicts (87 are CONCORDANT with MIXED). |
| Ask 4 under the golden key | Reproduced: 15.6, 15.3, 13.9, 14.9, 14.2, 15.1, 17.6, 19.6, 19.7, 18.8, 20.7, 16.1. Built from release_amendments applied to the history, RELEASED rows only, month of the amended released_date, distinct `extraction_id`, flagged taken as AUTO `hetx_call` or REVIEWED `review_outcome`=FLAGGED, denominator the distinct released extractions. | qc_screen_history |
| Ask 4 under competing readings | Distinct `specimen_id`: 17.6, 17.2, 14.2, 16.0, 15.2, 16.9, 19.0, 20.3, 22.2, 20.8, 22.6, 17.7. Denominator from release_volumes_monthly (results released): 14.8 ... 15.2. No amendments: 19.7 ... 18.9. `hetx_call` only, ignoring review outcome: differs (for example 2026-06 is 19.6). | Computed |

The golden is correct under its own keys. The defect is that the keys are not literal in the text. A specimen is identified by `specimen_id` in every file. Collapsing top-up accessions by extraction, and double-booked accessions by biobank vial, is an unstated identity rule.

Low-severity points that do not move the call:
- The 17 June re-run batches are included. KVAL-07 3.2 sets no re-run completion cutoff, though the model card addendum used 16 June.
- The prompt does not say to apply the amendments file. The file describes itself as the replacement record.

## Files/Hygiene
**PASS.** 17 files in 5 formats: csv (many), tsv, xlsx, pdf (4), json. The QC history has 32,985 rows. Named distractors are plausible: assay_unit_costs, extraction_platform_validation_2025.pdf, dilution_panel_2027q1.xlsx, plate_layout_map, release_volumes_monthly. Headers, comments, decimal commas and semicolon exports, thousands spaces, and the late and re-sent weekly report notes read as system artifacts. I found no authoring or benchmark disclosure, and dates are coherent (KVAL-07 printed 2027-06-21, QC extract date 2027-06-21, register to 2027-06-18). Nothing is exclusion-level.

## Stump power
Moderate. The main call is carried by the interval method: an unpaired or own-interval reading files 0.015 or hold. A strong analyst who treats the parallel run as paired lands the golden, so the main call may be solved by some runs. The ask layer (crosswalk vial key, shared extraction, amendments, review outcome) is where most responses would diverge. As built, that divergence is largely unforced interpretation, not stump power.

## Stumping type
`mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The paired estimator for a same-specimen comparison is a FINE-numbers method choice and passes Gate G. The identity-key reconstruction in asks 3 and 4 is a hidden-key device, not a stump.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. The field's own analysis is a method-change validation on a parallel run: sensitivity gain with a paired interval, and a false-call rate against a reference standard. The easy route is to compare the two screens' detection rates with independent intervals. That files hold, or 0.015 under an unpaired difference interval, in place of 0.030. The domain would not read the same with other nouns. Layer 1 is the mixed exports, the re-run batches, the re-issued results and the amendments. Layer 2 is the paired interval and the highest cutoff under the filed rule.

## Fix
Fix location: prompt. Close the unit forks without filing the method.
- Ask 3: say that a specimen is the biobank's vial (one biobank reference), or file one sentence in a shipped document saying that two accessions on one biobank reference are one specimen.
- Ask 4: say that a specimen is one extraction (a depth top-up shares its specimen's extraction), and state that the denominator is the distinct specimens released in the month, not the reporting-pack results count.
- The packs, the goldens and the main call stay unchanged. Add a fork-table row for each in the design note.
- Optionally add one filed sentence that the interval on the increase is taken on the same specimens. That sentence would file the WHAT. It would make the main call fully literal, but it would also lower stump power on the main call.

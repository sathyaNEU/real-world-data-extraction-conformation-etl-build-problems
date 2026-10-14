# Verdict: task124 round 2

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No repair needed. Two wording risks are listed under Why and Fix as optional; neither needs a rerun to ship.

**Why:** The main call (every zone finished, RZ-06 Wexley in 2037, before 1 Nov 2037) reproduces from the shipped files. Plan s4.3 asks for "the share of lead or GRR expected among the district's Lead Status Unknown lines of its construction era" but does not name an estimator. The data forces the estimator. Lead rate among verified no-tap-card lines is 0.9286 (13/14) on mains where any tap card reads LEAD or GALV, and 0.0526 (1/19) elsewhere. That rate is identical across eras, zones, municipalities, decades, years, methods and crews. The verified sample sits 80% on lead or galvanized mains, against 19% of the Lead Status Unknown population. A rigorous analyst must therefore reweight by main kind, and the era-only verified share (2042) and the tap-card share (2039) are rejected on the data. The unpinned estimator is the main residual risk and is classed as method selection, not an open fork. Supplementary answers (zone lines and costs, 2026 payments, signed agreements) also reproduce, with the minor interpretive notes below.

## Evidence (recomputed from target/)

| Item | Result | Source |
|---|---|---|
| Verified lines with no tap card, built before 1989 | 3,409, reproduced. Each line at its first result; repeat visits never change lead status (142 lines, 0 flips). Premise padding and result codes map with 0 unmapped. | sl_field_verifications, cis_gis_crosswalk, sl_material_result_codes, inventory |
| Lead share by main kind | 2548/2744 = 13/14 and 35/665 = 1/19, reproduced. Within-cell values are exactly 13/14 and 1/19 in all three eras. | same |
| Lead Status Unknown lines on lead or galvanized mains | 3,822 of 9,939 (before 1930), 2,215 of 9,023 (1930-49), 359 of 14,569 (1950-88), reproduced | inventory |
| Era shares | 0.3895, 0.2677, 0.0742 (golden 0.389, 0.268, 0.074), reproduced | |
| Plan cost | $268.29M, 10.563 appropriation-years (golden $268.3M, 10.56), reproduced | unit_cost_schedule_2027.xlsx, plan s4 |
| Zone lines and costs | All 12 match the golden after rounding. Examples: RZ-07 1,250 / $20.7M / 2027; RZ-02 1,820 / $34.0M / 2029; RZ-06 890 / $18.1M / 2037. | |
| Finish years | 2027, 2029, 2030, 2031, 2032, 2033, 2034, 2034, 2035, 2036, 2036, 2037, reproduced. Every zone is at least $3.8M from a year boundary. The last zone has $11.1M of slack to the 2037 boundary (cap $279.4M = 11 x $25.4M). | CIP docx line 25.4; plan s5.3-5.4 |
| 2026 payments | All 12 contract-by-quarter values match (e.g. Brannigan Q1 $14,395, Kestrel Q3 $14,636). Basis: RECLOSED row replaces CLOSED, Eastern-time quarter, change order counted once. No change order spans two quarters, so allocating a change order to a quarter is not a fork. Quarter counts (97/226/434/96) match the progress report. | lsl_completions, change_orders |
| Signed agreements by zone | All 12 match (878, 1186, 633, 1020, 846, 607, 960, 685, 991, 386, 1077, 504). Basis: distinct lines with a SIGNED form, plus 430 E-SIGNED lines with no form at all, in the inventory zone. | access_agreements, crosswalk, tracker, inventory |

**Competing answers tested**

- **Era-only verified shares (0.852, 0.703, 0.225):** $386M, last zone 2042. Rejected: the verified sample is selected toward lead mains.
- **Tap-card lead or galvanized share (0.633, 0.523, 0.096):** last zone 2039. Rejected: the cards are a different population.
- **Main-kind shares applied line by line rather than at era level:** $268.4M and the same finish years, but zone lines and costs differ (RZ-02 1,910 / $35.2M against golden 1,820 / $34.0M). Plan s4.3 says "of its construction era", which favours era-level and the golden. This changes graded supplementary numbers, not the call.
- **Rounded shares:** 3-decimal shares reproduce the golden exactly. 2-decimal shares (0.39, 0.27, 0.07) move some zone lines and costs by one rounding step (e.g. RZ-04 1,170 / $22.9M against 1,180 / $23.0M). Mild rounding-edge risk.
- **Agreements, forms only (9,343 lines):** under-counts lines the tracker records as e-signed. The 69 lines whose form is WITHDRAWN but still show E-SIGNED have a portal status date equal to the original signing date, before the withdrawal, so excluding them is data-supported.

## Files/Hygiene

PASS. 17 files in csv, pdf, docx, xlsx and md. The largest is 87,410 rows. Dates are coherent (inventory, extract and progress report 6-8 Jan 2027, CIP board draft 14 Dec 2026, plan 20 Oct 2026). The distractors lcr_tap_samples (361 rows, all tap-card LEAD lines) and ami_meter_exchanges are relevant, not decisive, and not usable as a lead-share estimator. No benchmark or authoring disclosure was found. Minor: the field-notes phrases "for this extract" and "Other extracts in the folder" read slightly authored, a non-stump cosmetic item. Real-world rule date (1 Nov 2027 compliance, 1 Nov 2037 deadline) is stated in plan s1.2, so there is no external dependency. Nothing is exclusion-level.

## Stump power

Medium to high. The obvious route is the verified-sample lead rate by era, which gives 2042 ("not finished") or, by the tap-card share, 2039. Both flip the call to NO, so a capable but unreflective solver fails for an analytical reason: the verified lines are non-random and the correct estimator conditions on main kind. A solver who checks how the verified sample differs from the Lead Status Unknown population (main-kind mix) lands on the golden, so the stump rests on one non-trivial check. The structure is clean enough that those who find it all converge.

## Stumping type

mechanism: statistical_rigor (selection-adjusted share estimation, i.e. method_or_model_selection on honest data), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no.

No reported number is wrong and no defect is planted. The verified-lines share is the solver's own naive estimate, not a published figure. Clean-data test: on defect-free data the selection bias still decides the call. Borderline note only: a reader could call "the verified share is biased" a flip away from a surface read. I rate it as covariate-shift adjustment, not rejection of a stated number.

## Three rules

domain: pass, layers: pass, decisive_step: analytical.

- **Domain:** estimating the expected lead share of unknown service lines is the core LCR service-line inventory and predictive-model task. The swap test fails with another field's nouns.
- **Layer 1:** CIS and WMS result-code vocabularies, unpadded premise numbers and mixed date formats, UTC against Eastern quarters, RECLOSED rows, a vendor change under one contract, and form zones against plan zones.
- **Layer 2:** selection-adjusted lead share by main kind, then a cost and cumulative-appropriation schedule.
- **Easy route:** the era-only verified share gives 2042, or the tap-card share gives 2039, either answering NO.

## Fix

none. Optional hardening of wording, without moving figures:

- (solution) State the 430 E-SIGNED-no-form and 69 stale-E-SIGNED treatment in the agreement answer, and note that s4.3 is applied at era level.
- (prompt) Optionally pin 3-decimal share rounding or no rounding, since 2-decimal shares shift a few graded zone values by one rounding step.

## Disposition

Main session, 2026-10-14. APPROVE taken; the build ships. Nothing in the pack, the goldens or any graded figure moved
(`freeze.py check task124 --mode determinism` PASS; `target/`, `golden/`, `generator/figures.json`, `metadata.json`,
`prompt.txt` and `target.zip` byte-identical to the round-2 cut the judge read).

- Residual risk 1 (plan 4.3 names no estimator): no change. Method selection forced by the data, the design note's
  SF15: within each kind of main every route returns 13 in 14 and 1 in 19, and every era-wide rate runs past the
  deadline.
- Residual risk 2 (era shares rounded before they are applied): fork row SF19 added to the design note and asserted in
  `generator/checks.py`. The prompt's one closing rounding sentence ("Round lines to the nearest ten, zone costs to the
  nearest $100,000 and the 2026 payments to the nearest dollar.") names the reported figures and no share, so the
  literal reading carries the shares unrounded, and the golden is that path. Two-decimal shares keep the twelve finish
  years and the call and move zone lines in RZ-04, RZ-10 and RZ-06 and zone costs in RZ-04, RZ-12, RZ-08, RZ-10 and
  RZ-06 by one rounding step; three decimals move nothing (M26). Prompt unchanged.
- Residual risk 3 (the agreement count's rule): one clause added to step 6 of `submission.md` (an E-SIGNED line whose
  form was withdrawn is not added); the era-level application is one clause in step 4 (the unknown lines of each era
  carried at that era's share, unrounded). No new figure; `figures_check.py` exit 0.
- Hygiene note (field-notes phrasing): cosmetic, not a stump or determinism item; left as is.

Gates on the final rebuild: checks 135 assertions 0 failed, verify green, two builds byte-identical,
`figures_check.py` 0, `precut.py` 0 (19 fork rows), voice-check 0, `leak.py --asof 2027-01-11` REVIEW (no LEAK),
`guard.py surface` 0, `heart` WARN (no BLOCK), `validate` 169 cards 0 invalid, `freeze.py` PASS.

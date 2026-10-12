# determinism-check report, task134, 2026-10-12

One isolated judge thread (medium effort) on the stage 3 cut (`target.zip` sha256 23fbb025), the prompt and the submission's graded blocks. Its verdict follows verbatim; the Disposition after it is the build session's.

# Verdict, task134

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE. One optional in-prompt or notes pin (locality = the home's locality) would close the only live fork. It is a prompt/notes edit that would need a rerun, so it is not recommended unless the author wants zero risk on ask 2.
- **Why:** The main forecast is forced. Council-funded stock (745) + direct admissions (15.94 a month) + the open-award self-funder pipeline (599) all come from shipped files. The conversion hazard shows a clear structural feature: it is zero for about 15 months after admission, then rises. Every banded variant of the same method gives the same rounded answer (760/770/780/790). The naive alternatives land elsewhere (see Stump power). The ask-2 averages and the chart ordering reproduce exactly. One reading risk remains for ask 2 (placement `locality` column versus the home's postcode locality; see Evidence).
- **Evidence (recomputed from target/):**
  - 745 council-funded residents at 31 Dec 2026 reproduced. Method: PERM episodes stitched per person through `client_id_crosswalk_2023.csv` (legacy numbers and merged_into). Two EXACT deaths registered after 31 Dec but dated 16 and 29 Dec closed the open stays (`nrs_death_linkage_2027-01-15.tsv`). Counted once per person, including residents in homes outside Strathallan (definitions 2.4; 25 residents in 9 service numbers absent from the register).
  - 599 self-funders reproduced: open awards in `fpnc_payment_lines_2021-2026.csv`, all paid through 30 Dec 2026, none matched to a death. 505 of them were admitted from 1 Jan 2025. Self-funder admissions jump from about 245 a year to 368 in 2025 and 375 in 2026.
  - Direct admissions: 574 in 2024-26, so 15.94 a month. Reproduced.
  - Council-funded exit hazard is roughly flat at about 0.031 a month. Conversion hazard is 0 until about month 15, then about 0.03 to 0.07 a month.
  - My own piecewise-exponential model gave: existing 474.5, direct 184.0, conversions 131.8 at 31 Mar 2028. Quarter-end totals were 760.0, 771.0, 781.2 and 790.3 against the golden 759.1, 770.5, 780.1 and 789.0.
  - Sensitivity of the conversion component, all rounding to 760/770/780/790:
    - 1-month bands: 54.4 / 82.2 / 108.0 / 131.8
    - 3-month bands: 54.3 / 82.1 / 108.5 / 131.2
    - 6-month bands: 54.6 / 82.2 / 108.2 / 129.5
    - age counted from award start instead of admission: 54.2 / 82.0 / 107.6 / 131.0
  - The nearest rounding boundary is more than 4 residents away at every date (770.5 against 775).
  - Ask 2 (home locality via register postcode and `postcode_locality_lookup.csv`, contribution = latest assessment effective on or before 31 Dec 2026 over all the person's debtor refs, fee = episode `weekly_fee`, NIL = 0): all ten contribution and cost pairs reproduced to the pound.
    - Residential cost: Allanvale 673, Braeburn 709 (708.9), Carsefield 713, Dunmorrow 680, Kirkhallam 703.
    - Nursing cost: Allanvale 819, Braeburn 821, Carsefield 822, Dunmorrow 834, Kirkhallam 837.
    - Order of dearest nursing: Kirkhallam, Dunmorrow, Carsefield, Braeburn, Allanvale. Kirkhallam stays first under every variant I ran.
  - Variants run on ask 2:
    - completed on or before 31 Dec only: Kirkhallam nursing 843, still first
    - first debtor ref only: 839, still first
  - Surviving fork (ask 2 only): the placement file has a `locality` column ("partnership locality recorded on the placement") that differs from the home's postcode locality for 270 of 720 residents in registered homes. Used instead of the home's locality, the nursing ranking becomes Carsefield 862, Braeburn 844, Kirkhallam 841, Dunmorrow 809, Allanvale 795, so the title and order would change. The prompt says "the five localities' care homes", and the register plus lookup file exist to place homes, so the golden reading is the natural one. It is not stated outright, so it is a minor risk, not a failure.
  - Nothing in the main forecast depends on locality.
- **Files/Hygiene:** PASS. 14 files across csv, tsv, xlsx, docx, pdf and txt. One file has 50,773 rows. Distractors: `nchc_draft_offer_2027-28.pdf`, `nchc_rates_2021-22_to_2026-27.xlsx`, `care_at_home_hours_2024-2026.csv`, `care_inspectorate_grades_2026.csv`; none is needed for the answers. Dates are coherent (extract run 18 Jan 2027 is a Monday, definitions 12 Jan 2027, NRS match 15 Jan 2027, nothing after the cut). No README or authoring language, no synthetic disclosure. The extract notes are a plausible system document. Nothing LLM-looking beyond a slightly tidy definitions change log. Not exclusion-level. The cross-batch fingerprint check was not run because other task folders are off limits.
- **Stump power:** Good, for an analytical reason.
  - A flat or trend extrapolation of the council-funded stock (flat at about 745-770 for five years) gives about 750 at every date, against the golden 760 to 790.
  - A stock-flow of existing residents plus direct admissions that omits the self-funder pipeline gives about 658 at Mar 2028 (474 + 184).
  - A pipeline with a constant, non-age-dependent conversion rate gives about 93 conversions, roughly 750, against 131.
  - The data separates these: conversion is zero for the first 15 months, and the 2025-26 self-funder surge is exactly what the history cannot show. Closing the horizon works because admissions after 31 Dec 2026 cannot convert before Mar 2028. Strong models plausibly stop at one of the naive reads.
- **Stumping type:** `mechanism: forecasting` (with method_or_model_selection and etl_conformance layers), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported counts are fine. The difficulty is a forward projection that the correctly read past does not pin: an age-structured competing-risk pipeline from self-funders, validated by the data's own hazard shape. On clean data it would still stump.
- **Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`.
  - Domain: care-home commissioning demand forecasting by cohort and hazard modelling is the field's own estimate.
  - Layer 1: crosswalk merges, a case system migration, a lagged death register, interim and respite episodes, an out-of-area home, re-registered services.
  - Layer 2: the pipeline of self-funders converting on a time-since-admission hazard.
  - Easy route: extrapolate the flat stock or add admissions to survivors; this gives about 750 or about 660 against the golden 790.
  - Data semantics and rule application appear only in the supplemental asks and the census, not the main call.
- **Fix:** none required (fix location: none). Optional, in the extract notes or prompt: state that `locality` on a placement is not the home's locality, or that residents are placed by their home's postcode. This closes the ask-2 fork but changes what solvers see.

## Disposition

**APPROVE.** No FIX_NOW item, no re-judge.

- Gate G and Gate H: the thread's stumping type (forecasting, with method_or_model_selection and etl_conformance layers; analytical_non_defect; no surface-read dependency; no sole data defect) and its three-rules line (domain pass, layers pass, decisive_step analytical) match the card (`gate_g` method_or_model_selection, `stump_class` analytical) and the design note.
- The optional ask-2 pin (locality is the home's) is declined. The placement's `locality` column is the ask's designed primary device (the design note's ask sheet, D3), the prompt asks for "the five localities' care homes", and a pin would name the device.
- The contract-rate schedule the judge listed among the unused files is the ask's fee hazard (the schedule rate taken as the fee). `metadata.json` declares three distractors: the draft 2027-28 offer, the care at home hours and the inspection grades.
- After the verdict, the stage 4 fix pass reissued the placement and assessment numbers, labelled the one NIL row that carried a contribution (0.83) as ASSESSED, and removed the definitions' version table and the extract notes' row counts. No graded figure moved (`freeze.py check --mode determinism` PASS, `verify.py` 0 failed, `figures_check.py` 63 of 63, goldens and `figures.json` byte-identical), so the verdict stands; the two changed documents go back to the leak reader.

Next action: the reader's re-read of the definitions and the extract notes, then ship.

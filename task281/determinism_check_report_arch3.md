# task281 determinism check (architecture 3)

Two isolated judge passes at stage 4, each a Sonnet thread at medium effort that saw only a fresh unzip of target.zip, the
prompt and the judge's system prompt, and opened the graded blocks only after its own derivation was on disk.

| Round | Pack | Verdict | Disposition | Action |
|---|---|---|---|---|
| 1 | 11435654 | DETERMINISTIC (order kept; G PASS; H PASS) | APPROVE as labelled | the estimator finding (settled only by the plain reading) treated as a FIX_NOW and closed by construction: all fourteen estimators give the golden's point at every clinic, asserted in checks.py block F |
| 2 | 0837f761 | DETERMINISTIC (order kept; F strong; G PASS; H PASS) | APPROVE | three advisory notes closed by wording and document alignment (CAI-03 4.2 defines a clinic day lost; the protocol's amendment 1 matches the study file; the slide's basis line) |

After round 2, the guard's heart check blocked the deciding forum (committee_or_panel, held by task273 which shipped first in
the window), and the forum was redrawn for real to the network's executive leadership team (the standard's approval and
report clauses, the prompt's slide name, the golden slide, the card). None of these changes moves a graded figure:
generator/figures.json is byte-identical to round 2's, and submission.md's blocks 1 to 4 differ from round 2's in one heading
line only (the slide's file name). CAI-03 3.1's sentence, which the judge's literal reading turned on, is unchanged apart from
the recipient of the precision report. Shipped pack: target.zip 314f3a3b.


---

# Determinism check, round 1 (2026-11-01): DETERMINISTIC, APPROVE as labelled; order kept; Gate G PASS, Gate H PASS

Finding 1 (Gate C, the estimator) is settled by the thread only by the plain reading of 2.4 and protocol section 5, so under 'our judge is the floor' it is treated as a FIX_NOW and closed by construction in the generator, then re-judged once. Isolated thread, Sonnet at medium effort, on target.zip 11435654.

# Verdict: task281 (Kelvory RetinaCheck operating points 2027)

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE. No repair required; one optional one-line pin is listed under Fix (no rerun needed if skipped).
- **Order kept:** yes. derivation.md was written to disk before graded_blocks.md was opened; graded_blocks was then judged against it.

## Why
Every committed answer reproduced exactly from the bundle. The decisive step is a join the prompt never mentions: the AI export has no camera column, but Location History in biomed_asset_register_2026-09-30.xlsx puts a camera (NR-40 or NR-70) at each clinic on each date, loaners included. Placing the validation rows (site letters in the protocol, by capture_date) and the reference-year screenings on their camera shows that sensitivity differs sharply by model. Standard is 73.3% on NR-40 and 95.7% on NR-70, so the pooled 89.4% hides it. Under CAI-03 2.4 (sensitivity is the share of referable screenings the AI refers) and 3.1 (point estimate vs the 85 floor, "as it stands"), the camera-mix-weighted proportions force the golden: High at Brackenfield, Hollinmoor and Rookwood, Enhanced at Kestle Road and Veldane, Standard at the other seven. One residual estimator fork is reported under Evidence; it does not change the verdict.

## Evidence (all recomputed from target/)
| Item | Golden | Mine | File / field |
|---|---|---|---|
| NR-40 sens Std/Enh/High/Max | 73.3/82.2/90.1/96.0 | 74/101, 83/101, 91/101, 97/101 = same | local_validation_study (final_level, final_dme, dr_score, ai_result) x Location History |
| NR-70 sens | 95.7/97.3/98.8/98.8 | 247/258, 251, 255, 255 = same | same |
| NR-40 share of screenings | 100/100/100, 68, 58, 18, 8, 6, 6, 0, 0, 0 | 1340/1974, 1340/2320, etc. = same | AI export x Location History (Pacific local date) |
| Clinic estimates | NR-40-only: .733/.822/.901; Kestle .81/.873; Veldane .83/.889; 7 others >=.917 at Std | same | weighted by screenings or by expected referables, same call |
| Referrals by clinic | 754, 791, 518, 540, 410, 488, 686, 447, 451, 578, 496, 471 = 6,630 | identical | AI export (Ungradable or DR Score >= threshold) |
| Capacity | 7,200 | 7,200 (agreement 2.1); 6,630 is 570 under | pellam_reading_agreement_2027.pdf |
| High everywhere | 9,204 | 9,204 | AI export |
| Pellam read / share | e.g. 423/49%, 420/43%, 523/53%, 436/56%, 462/55% | identical for all 12 (total 5,205 read, 2,568 Referable, 49%) | overread log joined to the AI export by Accession; closing grade = the non-Insufficient case of the referral order |
| Days by quarter | 6.3, 6.2, 6.4, 6.3 | 6.266, 6.164, 6.363, 6.259 | Pacific local dates, quarter of the screening |
| Camera-fault no-screening days | Kestle 7, Orrin 3, Veldane 6, Sallow 4, Yarrowby 5, Pellsbury 7 | identical | AI export by local date; outage ends at loaner arrival (Location History) |

The fault-day counts agree with the 318 EHR orders cancelled "Equipment unavailable", which fall on exactly those days. Excluded as non-AI: 907 teleretinal read cases (IMG92250) and 408 retake cases filed under teleretinal accessions. 206 REF7734 orders were cancelled and never read.

**Competing answers tested**
- **Pooled, camera-blind:** all Standard, 5,411 referrals. Ruled out because it ignores a modifier the files expose; it is the intended easy route.
- **Smoothed score model by camera (logistic or binned calibration from validation):** NR-40 clinics come out at Enhanced (.86-.87). Kestle .847 and Veldane .850 are at the Standard line.
- **Hybrid using Pellam reference-year grades for true positives, validation calibration for misses:** same direction, NR-40 clinics Enhanced.
  - These give totals of 6,094 (Kestle and Veldane Enhanced) or 5,836 (both Standard).
  - Both are weaker than the golden. 2.4 defines sensitivity as a proportion, and the validation protocol (section 5) computes it that way at each point. The hybrid also uses Pellam's single-read closing grade, which is not "the reference standard of the network's local validation study" (2.3: two masked graders plus adjudication).
  - It remains a real fork for a solver who finds the camera effect but smooths. Report only; it is not a verdict-level hole because the filed definitions point to the direct proportion.
- **Margin:** the closest calls are NR-40 at Enhanced 82.2 vs 85 (2.8 points) and Kestle at Enhanced 87.3 vs 85. They are clean point estimates with no boundary rows. No validation row falls on a camera-swap day, and the weighting basis (screenings or expected referables) does not flip any clinic.
- **Clinic day:** CAI-03 4.2 says days with no screening "because its camera was out of service", which excludes weekends and the Memorial Day holiday. The outage windows end at loaner arrival, so the ticket Closed dates (Pellsbury 07-18) are not used.
- **Quarter and timezone:** CAI-03 4.1 closes quarter of the screening and local dates. Alternatives give different one-decimal values: quarter of grading 5.7/6.1/6.5/6.4, UTC dates 6.2/6.1/6.4/6.2.

## Files / Hygiene: PASS
- 16 files; formats csv, xlsx, pdf, json (4). Largest data files: registry 42,041 rows, AI export 26,997 rows, EHR orders 35,891 rows. Raw files are system-like, with mixed date formats, UTC against local time, three site-naming schemes and an HO- serial prefix that varies between sheets.
- Distractors: eye_screening_patient_survey, him_outside_eye_reports, diabetes_registry, retinacheck_site_dashboard_2026q3, the teleretinal read cases. None is used by the solution.
- No authoring or benchmark language or LLM tells found in the PDFs, json or CSV headers. Dates are coherent with the 2026-10-01 export and the 14 Oct 2026 agreement.
- Camera model never appears in an AI-export column or in a file name. Not exclusion-level.
- Cross-batch fingerprint: no earlier verdicts were available to me; not performed beyond the bundle.

## Stump power (Gate F)
The camera modifier is not stated in the prompt, a file name or any shipped note. It is reachable only by dating the validation and reference-year screenings against Location History, with ticket Location and Closed dates as the misleading shortcut. A solver who pools (89.4% at Standard everywhere) gets a clean-looking, wrong 5,411-referral answer; a solver who stratifies but smooths or uses Pellam grades lands on Enhanced at the NR-40 clinics. Plausibly stumps. Caution: that second solver found the intended mechanism and diverged on estimator, so such a divergence is not a clean analytical stump.

## Stumping type (Gate G)
`mechanism: statistical_rigor` (effect modification / transport of a validation estimate to each clinic's own equipment mix), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. No shipped number is wrong: the pooled sensitivity is nowhere reported, and on clean data the stratified problem still stumps. Passes Gate G.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
- **H1:** the deciding quantity is diagnostic sensitivity at vendor operating points, transported from a validation study to each clinic's reference-year screenings. This is the work of a clinical-AI evaluation. Swap test fails to preserve the task: "megawatt-hours" in place of "referable DR" breaks it.
- **Layer 1:** UTC against Pacific local capture dates, clinic names in four schemes, teleretinal cases and retakes mixed into the overread log, tickets with stale Location and Closed dates, loaners and serial-prefix drift.
- **Layer 2:** sensitivity by camera model, weighted to each clinic's camera mix.
- **Easy route:** a strong analyst who cleans everything and reads every rule correctly pools the validation (89.4% Standard) and files Standard everywhere (5,411 referrals). This is wrong at five clinics. H3 passes.

## Fix
none required. Optional, no rerun: if the author wants the estimator fork closed, add to the standard or prompt a filed WHAT such as "sensitivity is the observed share of the validation participants with referable disease whom the AI referred", stratified as the analysis requires. Do not file the camera stratification itself, which would turn the decisive step into rule application.


---

# Determinism check, round 2 (2026-11-01): DETERMINISTIC, APPROVE; order kept; Gate F strong; Gate G PASS; Gate H PASS

The re-judge after round 1's estimator finding was closed by construction. Its three advisory notes (the clinic-day definition behind ask 6, the heatmap cells' basis, the protocol's end date against the study file) were closed afterwards by wording and document alignment that move no graded figure, asserted by an unchanged figures.json and submission.md. Isolated thread, Sonnet at medium effort, on target.zip 0837f761.

# Verdict, task 281 r2

**Order kept:** yes. derivation.md was written to disk before graded_blocks.md was opened.

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No repair is required. Three low-severity wording risks are listed under Findings. They are advisory and do not move the main call.

**Why:** The shipped files force the main call. Sensitivity must be stratified by camera model. The model is recoverable from biomed_asset_register Location History (keyed on Asset Tag) joined to the study's site letter and capture date, and to each reference-year screening's clinic and Pacific local date. The result is Standard at 7 clinics and High at Brackenfield, Hollinmoor, Kestle Road, Rookwood and Veldane, with 7,076 referrals against 7,500. Every committed answer and the critical components reproduced exactly from the bundle. No Gate A to E failure.

## Evidence (all recomputed from target/)
| Item | My value | Golden | Source |
|---|---|---|---|
| Study referable (final_level >= moderate or final_dme Y), by camera | NR-40 90, NR-70 390 | same | local_validation_study, Location History |
| Referred at Std/Enh/High/Max, NR-40 | 58/70/80/89 of 90 | same | study dr_score, ai_result, thresholds from retinacheck_operating_points.pdf |
| Referred at Std/Enh/High/Max, NR-70 | 378/389/390/390 of 390 | same | same |
| NR-40 share of reference-year screenings | BF, HM, RW 100%; VD 90.7%; KN 90.0%; SC 11.3%; PB 7.9%; OF 6.1%; YB 6.0%; QH, TB, WM 0% | same (rounded) | AI results with Location History, local date |
| Weighted sensitivity at Std (5 NR-40 clinics) | 64.4, 64.4, 64.4, 67.7, 67.5 | not stated (heatmap) | camera-mix weighting |
| Weighted sensitivity at Enh (5 NR-40 clinics) | 77.8 to 80.0, below 85% | below 85% | same |
| Weighted sensitivity at High (5 NR-40 clinics) | 88.9, 88.9, 88.9, 90.0, 89.9 | at or above 85% | same |
| Weighted sensitivity at Std (other 7 clinics) | 93.3 to 96.9, all above 85% | above 85% | same |
| Operating points | as golden | as golden | |
| Referrals at chosen points (BF, HM, KN, OF, PB, QH, RW, SC, TB, VD, WM, YB) | 755, 793, 705, 549, 415, 498, 690, 452, 464, 763, 508, 484 | same | AI results, thresholds |
| Network referrals | 7,076 (headroom 424) | 7,076 | Pellam agreement 2.1 |
| Reads / share Referable | 391/43, 395/39, 355/41, 521/54, 395/48, 484/48, 336/44, 440/49, 442/56, 366/43, 486/49, 461/57 | same | Pellam log joined through EHR REF7734 order to AI accession |
| Days by quarter (local dates, original screening to last non-Insufficient case) | 6.339, 6.260, 6.822, 6.463 (6.3, 6.3, 6.8, 6.5) | same | |
| Fault days (KN, VD, OF, SC, YB, PB) | 4, 6, 3, 4, 5, 7 | same | tickets, Location History, AI daily counts |

Details behind the table:
- **Reads:** 5,072 referrals were read. All of them closed. 400 needed a second case after an Insufficient first case. 910 log rows are IMG92250 teleretinal and are excluded. 197 AI referrals had cancelled orders and were never read. Read count equals closed count, so there is no denominator fork.
- **Days:** the UTC-date variant gives 6.7, 6.6, 7.1, 6.7. Standard CAI-03 4.1 pins local dates, so the golden reading is the literal one.
- **Fault days:** the six non-holiday zero days per fault match the EHR "Equipment unavailable" cancellation dates exactly, apart from the open day, which had screenings before the failure.

**Competing answers tested**
- **Pooled study sensitivity, ignoring camera:** 90.8% at Standard, so Standard everywhere with 5,269 referrals. This ignores the effect modifier and does not estimate sensitivity "among that clinic's reference-year screenings" (3.1). It is the intended wrong easy route, not a defensible alternative.
- **Current register location for the camera:** Kestle Road and Veldane would be NR-70 and so Standard (6,353 referrals). 2.1 and 3.1 say reference-year screenings, so High is literal. This is a surviving contrarian argument but the text pins against it.
- **Confidence-interval floor:** the NR-40 High Wilson lower bound is about 80.5%, which gives Maximum. 3.1 states the estimate is compared "as it stands" and its precision is reported separately, so this is closed by the text.
- **Site-level study estimates:** Wendmere, Quarry Hill and Yarrowby are still Standard, so the decision is unchanged.
- **Protocol window (to 27 Jun 2025):** all NR-40 rows are inside it, so only NR-70 values move. NR-70 Standard goes from 96.9% to 96.4%, and no decision changes.

## Findings (low severity, none moves a graded count)
1. **Gate E/C, supplementary 6 (fault days).** "Clinic day" is undefined in the files, and no file lists holidays. The golden counts weekdays with no screening after the fault day, up to the loaner move. A solver who counts weekdays across the ticket Opened to Closed window including network-wide holidays gets Yarrowby 6, Pellsbury 9, Kestle Road 13 and Veldane 16. CAI-03 4.2 ("because its camera was out of service") and the exact match to the equipment-unavailable cancellations close it, but only by inference. Optional hardening is to state "clinic days on which the clinic screened" in the prompt, at the cost of a rerun.
2. **Gate C, slide heatmap cells.** The pptx cell values are not in the committed answers. The pilot clinics' cells depend on method. Pooled-by-camera gives Wendmere 97 at Standard. Site-by-camera strata give 99 (Wendmere), 96 (Quarry Hill), 96 (Yarrowby). Including or excluding the 1,110 study rows after 27 Jun 2025 moves NR-70 cells by about one point after rounding, for example 97 against 96. The outlined point is invariant. This is a graded-figure risk only if the rubric grades cell values.
3. **Hygiene and temporal, Gate B edge.** The study file runs to 22 Aug 2025 with about 1,500 participants per site. The protocol states enrolment to 27 Jun 2025 and about 1,100 per site. The local timezone is never stated and is inferred as Pacific from Pellam Image Date against UTC (the zip codes are consistent). The Pellam log and EHR orders run to 3 to 9 Nov 2026, past the 1 Oct 2026 config export, which is coherent only if the present is mid-November 2026.

## Files/Hygiene
**PASS.** There are 16 files in four formats: csv, pdf, xlsx and json. The AI results file is 27,034 rows, with the EHR orders at 35,744 and the registry at 42,041. Distractors that are weighed but not used: the registry, the patient survey, HIM outside eye reports, the Q3 dashboard (Standard only) and the site config (all Standard). Layer 1 mess is authentic: serial-prefix drift (HO-), UTC against Pacific, the mixed teleretinal and AI referral orders, a re-photo case under the same referral, and the register's current location against its movement history. Nothing reads as authoring leakage. File names do not name the trap. No exclusion-level finding. Finding 3 above is the only coherence note.

## Stump power (Gate F)
Strong. The trap is camera-model effect modification. The study pools two models, and a solver who stratifies nothing sees 90.8% at Standard and files Standard everywhere with 5,269 referrals. Reaching the camera requires reading the asset register's movement history rather than its current-location column, and it also requires keeping Kestle Road and Veldane on the reference-year mix. The camera is never named in the prompt or the standard, but it is reachable from the ticket and fault ask, the register and the study dates. The rule-discovery risk is low because nothing states the answer. I expect a capable model to miss it about half the time or more.

## Stumping type (Gate G)
mechanism: statistical_rigor (effect modification, transport of a validation estimate to each clinic's case mix); stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no.
No shipped artifact reports a wrong figure or blesses the wrong method. The numbers are fine and the work is a stratified transport. On clean data the heterogeneity would still stump. Gate G passes.

## Three rules (Gate H)
domain: pass | layers: pass (Layer 1 is local against UTC time, serial-prefix drift, teleretinal and re-photo case structure, and the current register location against its movement history; Layer 2 is camera-stratified sensitivity transport) | decisive_step: analytical
The field's own analysis is local validation of an AI diagnostic at each site: estimating sensitivity for the site's device mix, then applying a governance floor. The swap test fails to make it generic, because the decisive quantity is a device-stratified diagnostic sensitivity. The easy route is pooled study sensitivity (90.8% at Standard), which gives Standard everywhere and 5,269 referrals. The correct answer puts five clinics at High and gives 7,076 referrals.

## Fix
none. Optional (finding 1): state "clinic days on which the clinic screened" in the prompt, or define clinic days in a file. Optional (finding 2): fix the study window and the pooling method wherever heatmap cell values are graded. Neither is needed for the committed counts.


# Determinism check, task240, pass 3 (re-check 2026-11-01)

One isolated judge thread (Sonnet, medium), the shipped bundle and the graded blocks only; spawned by the main session from the determinism-judge brief because the judge agent had no Agent tool. Verdict DETERMINISTIC, disposition APPROVE. Its optional polish (writing out the with-replacement factor in QS-7 3.2) is not taken: SF16 asserts the warned set holds without it, and the with-replacement estimator QS-7 3.2 names carries it.

# Determinism verdict, task240 (Household Resources Survey 2027 quality report)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No rerun is needed. One optional one-line pin is noted under Fix.

**Why:** QS-7 2.1 and 3.2 define the estimate "as published", made with the final weights "as the contractor's weighting note describes". hrs27_weighting_note.docx says those weights were post-stratified in 96 region x age x sex cells. Executed literally, the published estimate is a post-stratified total, and its linearisation is z = w(y - p_cell). That warns exactly 9 of the 48 estimates, all the golden CVs reproduce, and the nearest values either side of the 20.0 line are 18.4 and 27.6, so the margin is wide. Every term used (PSU region, final outcome, e, call, duplicate record, late interview) is closed by a shipped file: QS-7 4.1 to 4.3, the households and call records, and the weighting note.

**Evidence (recomputed from target/, all reproduced):**
- Adults: 7,238 weighted adults in 3,764 households, 707 PSUs in 24 strata. The closeout memo's 708 PSUs is explained by P4083, which has no full interview.
- Post-stratified weights sum to the SSB population in all 96 cells (ratio 1.000000). This confirms the age-group, sex and household-region coding.
- CVs under post-stratified linearisation match the golden to 1 dp for all 48. Warned set (9): CARE R01 27.6, R02 48.7, R03 38.6, R04 34.3; ARR R01 30.1, R02 39.4, R03 30.0, R04 28.1; RENT R02 32.7. The highest unwarned CV is R01 RENT at 18.4.
- Public pension CVs in the four northern regions are 5.0, 7.5, 8.4 and 6.5. Fixed-weight linearisation gives 24.9, 37.8, 21.8 and 25.1, and warns 15 (the golden's six extras: R01 PEN, R01 RENT, R02 PEN, R03 PEN, R03 RENT, R04 PEN).
- Response rates reproduce (R01 to R12): 59.6, 49.9, 48.7, 52.7, 50.2, 53.6, 52.1, 51.3, 55.9, 54.8, 50.0, 54.4. The inputs are the same as the golden's:
  - e = 0.91697, from 7,058 addresses with established eligibility.
  - 3,764 full interviews, taken from households.csv. The extract's 3,657 plus 107 late interviews, all with an IC record received after 30 September.
  - 94 issued addresses absent from the extract, each with only an advance letter, counted as eligibility not established.
  - Region from households.csv. The 12 PSUs where the issued-sample region_code differs are all psu_frame 2023, which predates the review. P4083, with no households, is frame 2026 and R08 in region_code. Every 2026-frame PSU agrees with households.csv, so using region_code for P4083 is supported.
- Calls reproduce (R01 to R12): 96, 78, 120, 169, 1,660, 1,602, 1,238, 987, 873, 728, 454, 425.
  - Only VISIT and PHONE rows count. LETTER and CARD are excluded per QS-7 4.3.
  - All issues of full-interview addresses are included.
  - 769 duplicate pairs are removed. Each pair has the same address, issue, time, type, result and interviewer, but different record_id, event_no and later received_at, so they are tablet resyncs and cannot be two physical calls.

**Competing answers and forks:**
- Fixed-weight versus post-stratified variance gives 15 warned versus 9. This is the intended analytical fork. It is closed by QS-7 2.1/3.2 plus the weighting note, not left to taste.
- The n/(n-1) with-replacement factor is not written out in QS-7 3.2. Dropping it leaves the warned set at 9, but moves 1-dp CVs. Examples: R01 CARE 27.6 becomes 23.9, R02 CARE 48.7 becomes 41.5, R01 RENT 18.4 becomes 16.4. It is the textbook with-replacement estimator, so I treat it as forced by the standard's general method, with a small residual risk on the per-estimate CV asks (not on the warn flags).
- Using the extract's outcome codes alone, the issued-sample region_code, or counting duplicate rows each changes the rates or calls. Each of these is a reconstruction error the shipped files rule out, not a licensed alternative.
- No stated-objective, threshold, or window fork survives. The 20.0 line is a stated rule, and no estimate sits within 1.6 points of it.

**Files/Hygiene:** PASS. 12 files in 4 formats (7 CSV, 2 DOCX, 1 XLSX, 1 PDF).
- Distractors: hrs27_interviewers.csv, which is unused (hours_claimed and home_region); the closeout memo, which is partly used; the age-band structure of the population file.
- Timeline is coherent: letters from 30 March, fieldwork 7 April to 26 September, extract 30 September, late receipts to 14 October, weights 12 November.
- No authoring or provenance leakage, and no public-data contamination (a fictional survey and branch). Nothing exclusion-level.
- Minor realism note: the questionnaire cites Canadian pension names while the standard names a "Ministry of Finance". This is cosmetic.

**Stump power:** Strong. The tempting route is the default design-based linearisation with the final weights held fixed, which files 15 warned estimates and warns every northern pension estimate that is in fact almost pinned by the age and sex totals. The asks add independent silent reconstructions: region of lapsed-frame PSUs, 107 late interviews, 94 absent addresses and e, and 769 duplicate calls. A strong model that does not reconstruct these will miss several graded figures. It is plausible that both top responses miss the main call, though the warn set is only 9 versus 15 and a careful model may catch the post-stratification.

**Stumping type:** `mechanism: method_or_model_selection` (variance estimator for a post-stratified estimate, plus etl_conformance in the asks), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. All reported inputs are fine. The difficulty is choosing the correct estimator, not rejecting a misleading figure, and on clean data the fixed versus post-stratified fork would still stump. Gate G passes.

**Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`.
- The swap test fails to transplant: the deciding quantity is a sampling-error CV under the survey's actual weighting design. That is what a survey statistician estimates and tests.
- Layer 1 is mess from the organisation's own systems: a boundary review changing PSU regions, a 30 September extract that lags the analysis files, tablet-resynced duplicate calls, letters versus calls, and letters sent before assignment.
- Layer 2 is variance estimation that respects the post-stratification.
- The easy route is fixed-weight linearisation, which files 15 warned estimates, including six that are not warned.

**Fix:** none required (fix location: none). Optional, a rerun-free pin: QS-7 3.2 could state the with-replacement variance form (n_h/(n_h - 1) times the sum of squared PSU-total deviations). That would close the residual 1-dp CV fork.

# task259 determinism check (architecture 2)

Two isolated judge passes, each a Sonnet thread at medium effort that saw only a fresh unzip of target.zip, the prompt and the judge's system prompt, and opened the graded blocks only after its own derivation was on disk.

| Round | Pack | Verdict | Disposition | Action |
|---|---|---|---|---|
| 1 | 82205e8a | NOT_DETERMINISTIC on asks 4 and 5 only (order kept; main call forced; F high; G PASS; H PASS) | FIX_NOW | the technical note files which units are eligible for the response and noncontact rates and that a frame removal later reversed as made in error never happened; the proxy sensitivity stated with its computation; the person-file codebook shipped; the release's quarterly table made irregular |
| 2 | aae8a109 | DETERMINISTIC (order kept; F good; G PASS; H PASS) | APPROVE | critical component 2 restated without per-area decimals (each qualifier above 7.0 and each other area below it for every proxy sensitivity from 53 to 59 per cent, the panel's 95 per cent interval), asserted; target/ unchanged |

---

# Determinism check, round 1 (2026-11-01): NOT_DETERMINISTIC on supplementary asks 4 and 5 only, FIX_NOW; order kept; main call forced; Gate F high; Gate G PASS (statistical_rigor; surface_read_dependency borderline); Gate H PASS

Isolated thread, Sonnet at medium effort, on target.zip 82205e8a.

# Verdict, task259

- **Verdict:** NOT_DETERMINISTIC on the supplementary asks (response and noncontact rates, asks 4 and 5). The main call (areas, statewide 7%) is DETERMINISTIC and reproduces.
- **Disposition:** FIX_NOW. Pin the eligibility convention in HES_TECHNICAL_NOTE_2026-09.pdf (the WHAT: a unit the frame record shows deleted as vacant or demolished on or before the visit and not restored as DELETED IN ERROR is not eligible; say how a delete-then-restore interval is read). Main-call surface unchanged, no rerun for the main call; asks 4 and 5 need regrading.
- **Why:** The golden's 16 rate figures need the frame-maintenance file to remove 414 no-one-home units from the eligible base. No sentence links the two files. The technical note only says "occupied at the time of the interviewer's visit", and the codes file defines NC as an eligible disposition. The literal disposition-only reading gives different one-decimal values for every area. Gate C and E fail for asks 4 and 5. Taxonomy: underspecified_objective. Fix location: input_files (technical note).
- **Evidence (all recomputed from target/):**
  - Main call. Rev weights, employed = LFSTAT 1/2 (matches the preliminary release employed counts exactly), MJH=1 (matches the release multiple-jobholder percents). Four routes:

    | Route | Qualifying areas | State |
    |---|---|---|
    | As collected | 03 only (7.59) | 5.50 -> 5% |
    | Self-answered only | 03 only | 5.47 -> 5% |
    | Cell-imputed from self-answerers | 03 only | 5.5 |
    | Own answer carried from another quarter, no fallback | 03, 05 (8.49, 7.34) | 6.07 |
    | Proxy-sensitivity correction (area level, sens 0.535, false-positive rate 0.005) | 02, 03, 05, 07 (7.73, 9.31, 8.33, 7.96) | 6.88 -> 7% |
    | Panel substitution with sensitivity fallback | 02, 03, 05, 07 (7.62, 9.28, 8.40, 8.09) | 6.86 -> 7% |

    Not qualifying under the corrected routes: 01 5.7, 04 4.3, 06 5.4, 08 6.4-6.5. Margins to 7.0 are at least 0.38. The golden figures (7.8, 9.3, 8.3, 8.0 / 5.8, 4.4, 5.6, 6.5) reproduce within 0.15. The golden's 56% sensitivity gives me 53.5% unadjusted and 54.4% on adjacent quarters, so the exact value is method-dependent but the classification is invariant. Its claims about the rejected alternatives reproduce (imputation leaves Silver Creek alone; substitution adds Upper River only).
  - Why the correction is forced by the data: among persons with a self-report, proxy reports capture only 53% of second jobs (uniform by area, age, occupation and quarter). Multiple jobholders are proxied more often (corrected proxy-group rate about 9-10% vs 6-7% self), so self-answered-only is biased low. This is shown by the panel in the files and is not an assumption.
  - Rates. I get response / noncontact:

    | Area | Mine (disposition only) | Golden |
    |---|---|---|
    | 01 | 76.2 / 12.4 | 76.6 / 11.9 |
    | 02 | 67.2 / 19.9 | 67.5 / 19.5 |
    | 03 | 75.7 / 12.1 | 76.1 / 11.7 |
    | 04 | 73.9 / 13.6 | 74.3 / 13.2 |
    | 05 | 74.2 / 14.0 | 74.7 / 13.4 |
    | 06 | 69.4 / 17.0 | 69.7 / 16.6 |
    | 07 | 68.4 / 18.3 | 68.8 / 17.8 |
    | 08 | 83.4 / 6.2 | 83.8 / 5.8 |

    I reproduce the golden exactly only by also dropping units with a frame DELETE (VACANT or DEMOLISHED) on or before DISPO_DATE and no RESTORE ever. A second sub-fork is the delete-then-restore interval: "delete not yet restored at the visit" gives 76.7/11.7 for area 01 and moves most figures by 0.1-0.7. Interviews, refusals and other-eligible units are never affected. Only the NC count moves, because every deleted-and-unrestored unit is NC or NE. Dedupe to one disposition per frame unit per quarter (interview wins, old-system second record counted once) is correct and reproduces. Raw rows give different figures, which is intended Layer 1 mess.
- **Gate A:** main figures pass. Rate figures are not derivable without the unfiled frame step. **Gate B:** the decisive facts are in the files. LFSTAT, MJH and RESPLINE have no dictionary in the bundle. They are inferred from names and cross-validated against the release, which is low risk but a solver must infer that RESPLINE equals LINENO means self-report. **Gate C:** the main call passes; asks 4 and 5 fail on the unfiled eligibility convention and the restore-interval sub-fork. **Gate D:** the main stump is analytical. **Gate E:** the prompt is clear on the main call and the unit and rounding; the eligibility term is not pinned for asks 4 and 5.
- **Files/Hygiene:** PASS. 12 files in 4 formats (csv, xlsx, pdf, docx). The person file has 200,667 rows and the disposition file 156,160. Distractors present: the preliminary release (stale, first-issue weights and as-collected), LAUS, QCEW and the prelim Q3 weights sheet. Layer 1 mess is authentic (CAPI renumbering via crosswalk, dual-system records, refusal then converted, preliminary and reissued weights, the 59041 ZIP split). No authoring disclosures seen. No contamination. Not exclusion-level.
- **Stump power:** HIGH on the main call. The tempting routes (use MJH as collected, self-answered only, impute from self-answerers, carry own answers) all give 03 alone, or 03 plus 05, and the state at 5-6%. Only a validated sensitivity correction gives four areas and 7%. Rule 24.30.104(3) names the estimand but not the method, and the panel linkage through FRAMEID, LINENO and the crosswalk is needed to measure the bias.
- **Stumping type:** `mechanism: statistical_rigor` (measurement-error / misclassification correction validated on the panel), `stumping_family: analytical_non_defect`, `surface_read_dependency: no` (borderline: the as-collected share is a correct record of the proxy answers, and the filed rule sets the estimand, but a reader could call it a flip away from the published 5.3-5.7), `sole_data_defect: yes` (on clean self-reported data the main call is a weighted-share computation). Borderline, route to portal measurement.
- **Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. The field's own analysis is survey measurement-error correction (proxy underreporting of multiple jobholding, validated on the rotation panel) for an area-level estimate. Layer 1 is the CAPI 2026 renumbering, dual records, reissued weights and the ZIP-split county. The easy route that survives a clean read is the self-answered or imputed share, which gives Silver Creek alone and the state at 5%. Swap test: moving this to another field's nouns would lose proxy response, panel linkage and response rates, so the domain is used.
- **Findings by gate:**
  1. Gate C and E (asks 4 and 5): the frame-based eligibility rule is unfiled, so a disposition-only reading gives different rates. Underspecified_objective.
  2. Gate C and E (asks 4 and 5): the delete-then-restore interval is not pinned. Underspecified_objective.
  3. Gate A (critical component 1): the 56% sensitivity is method-dependent (53.5-57%). It is not load-bearing for the classification. Solution wording only.
  4. Gate B: no code dictionary for LFSTAT, MJH and RESPLINE (low risk).
- **Fix:** input_files. Add a sentence to the technical note's Response rates paragraph that fixes eligibility, so rates become determinate. Keep the main-call data unchanged. Optionally state the sensitivity as a range in the solution blocks.
- **Order kept:** yes. derivation.md was written before graded_blocks.md was opened.


---

# Determinism check, round 2 (2026-11-01): DETERMINISTIC, APPROVE; order kept; Gate F good; Gate G PASS; Gate H PASS

The re-judge after round 1's rate-ask repair, on target.zip aae8a109. Its note that the per-area shares are method-dependent at the first decimal is closed afterwards by restating critical component 2 without the decimals (each qualifier above 7.0 and each other area below it across the supported proxy sensitivities), a wording change in the write-up that moves no data. Isolated thread, Sonnet at medium effort.

# Verdict, task259 r2

Order kept: yes. derivation.md was written to disk before graded_blocks.md was opened. After comparing, my response/noncontact table differed from the golden; I traced it to my own keying error (CASEID instead of FRAMEID) and recorded it as a labelled addendum in derivation.md, not as a rewrite of the pre-read content. The main call, share table and statewide figure were in the pre-read derivation and matched.

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE. No repair needed; optional note-only items below need no rerun.
- **Why:** The filed rule (ARM 24.30.104(3), "counted as that resident would report it themselves") plus the person file's RESPLINE and the linked panel force the answer. Proxy-answered reports carry only about 54 to 56 percent of the second jobs the same adults report themselves, and the proxy-covered adults are more often multiple jobholders, so as-collected and self-respondent-only shares are both biased low. Corrected, 02, 03, 05, 07 qualify, 01, 04, 06, 08 do not, statewide 7 percent. The call is stable across every corrected variant I ran.
- **Evidence (recomputed from target/):**
  - Pooled 2025Q4 to 2026Q3, final weights, 2026Q3 rev sheet (the first issue differs by under 0.01 pt in shares; only WDA 06 weights move).
  - As collected: 5.50 statewide; only Silver Creek (7.59) is at 7.0 or more. Self respondents only: 5.47 statewide (5.20 reweighted on age, sex, relationship), Silver Creek alone.
  - Panel evidence (linked through the crosswalk): the same persons report MJ at 6.6 pct in self quarters and 4.0 pct in proxy quarters. MJ persistence is 0.97. Proxy detection of a self-reported MJ is 0.53 to 0.55 (adjacent-quarter version 0.549, divided by 0.97 persistence gives about 0.56, matching CRITICAL_COMPONENTS 1). Never-proxied persons self-report 5.2 pct against 6.4 pct for ever-proxied, so the self-only restriction is also selected.
  - Corrected shares, my variants (s .50 to .60, fp 0 to .5 pct): 01 5.5 to 6.0, 02 7.2 to 8.3, 03 8.9 to 9.6, 04 4.1 to 4.7, 05 7.9 to 8.7, 06 5.1 to 5.9, 07 7.5 to 8.5, 08 6.3 to 6.6, state 6.5 to 7.2. With the golden's s=0.56, fp=0.2 pct I reproduce 7.8, 9.3, 8.3, 8.0 | 5.8, 4.4, 5.6, 6.5 and 6.9 percent, all matching its critical components. Decisions never flip; WDA 08 tops out at 6.6 and WDA 02 and 07 bottom out at 7.2.
  - The golden's claim that carrying each resident's own answer from another quarter adds Upper River only reproduces: 05 7.29, 02 6.14, 07 6.51, state 6.04.
  - Response and noncontact, by housing unit (FRAMEID), interviewed if any record in the quarter is an interview, eligible = not coded vacant, demolished or not a housing unit, and on the master address file as finally corrected on the visit date (a DELETE followed by RESTORE "deleted in error" is void). I reproduce the golden exactly: RR 76.6, 67.5, 76.1, 74.3, 74.7, 69.7, 68.8, 83.8; NC 11.9, 19.5, 11.7, 13.2, 13.4, 16.6, 17.8, 5.8. Date choice (first, last, interview date) changes nothing.
  - Surviving alternative readings (forks), and what each gives:
    - Self-respondent-only or as-collected reading: Silver Creek only, statewide 5. Not defensible, because it drops the residents not at home from the population and is shown biased by the shipped panel, but this is the main route a competent solver will take (see Stump power).
    - Carry-own-answer-only: adds Upper River, statewide 6. Leaves about 47 pct of proxied adults unimputed and still proxy-reported, so it does not satisfy the literal rule; golden argues this explicitly.
    - Keying the housing unit by CASEID instead of FRAMEID, or taking the last disposition (362 interview-then-refusal sequences): shifts rates by 0.7 to 1.0 pt and changes rounding. The note's "each housing unit counted once" and the FRAMEID unit key close it; this is Layer 1 mess, not a fork the text leaves open.
    - Ignoring the "finally corrected" frame rule shifts rates 0.1 to 0.5 pt; the technical note states the rule literally.
- **Files/Hygiene:** PASS. 13 files, 4 formats (8 csv, 2 xlsx, 2 pdf, 1 docx); one 200,667-row person file and a 156,160-row dispositions file; distractors LAUS and QCEW unused by the answer; plausible survey-office artifacts with real irregularities (case number reissue, old and new disposition codes, rotation groups, preliminary and reissued weights, UTC start times). Temporal order coherent (rule effective 4 Sep 2026, release 2 Oct, weights reissued 16 Oct, certification by 1 Dec). No authoring or benchmark language found in the docx or pdfs. Nothing exclusion-level.
- **Findings (each with the gate it touches):**
  1. Gate C, low to moderate residual risk: rule (3) never says how to treat proxy answers, so a self-respondent-only (or carry-own-answer-only) reading is arguable at the margin. The shipped panel plus the release's "as collected in the survey interview" footnote separate the candidates, and the margins hold across s of .50 to .60, so I treat the call as forced, not as a fork. No change needed.
  2. Gate E, note only: the prompt pins only the statewide figure (whole percent). The chart's per-area shares are not graded to a stated rounding and are method-dependent at the first decimal (Silver Creek 9.3 to 9.6, Upper River 8.3 to 8.7). Do not add a decimal ask; if a grader reads area values, accept the decision side of the 7 percent line and the stated figures within the method range.
  3. Gate A, none: all CRITICAL_COMPONENTS and SOLUTION_STEPS figures reproduced; no block disagreements.
- **Stump power:** Good. The easy routes all land on Silver Creek only and statewide 5: as collected, self respondents only, and self respondents reweighted on age, sex, hours and occupation. The deciding step is calibrating proxy under-reporting from the same adults across quarters through the case-number crosswalk and noticing that at-home adults are a selected group. A strong model that sees RESPLINE very likely restricts to self respondents. Some risk of being too easy because the release footnote and rule (3) point at the issue.
- **Stumping type:** `mechanism: statistical_rigor` (measurement-error and selection correction on honest data, with a forecast-free survey-estimation core), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The as-collected 5.5 percent is not a planted defect; the filed rule defines the basis and the correction is an estimation task the field (survey methodology) performs. Borderline note: the published release figure is the surface read being corrected, but the work is estimating proxy sensitivity from the panel, not catching a wrong number.
- **Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. Swap test fails to read the same (proxy reporting, rotation-panel linkage, response rates and frame maintenance are survey-statistics work, not a backdrop). Layer 1: case-number reissue at the CAPI change, renumbered disposition codes, refusal-conversion duplicates, reissued weights, a county split across two areas by ZIP, frame deletes later restored. Layer 2: estimating the true multiple-jobholding share when proxy answers under-report and proxy-covered adults differ. Easy route: take the survey's collected or self-answered shares; gives Silver Creek only and 5 percent.
- **Fix:** none.


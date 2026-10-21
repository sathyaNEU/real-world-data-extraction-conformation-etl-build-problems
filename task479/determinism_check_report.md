# Verdict, task479 (round 4)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No repair is needed and no rerun is required. One residual risk is recorded under Why. An optional hardening is to file the estimand in the memo as the WHAT (expected cost for the employer given both its own and the trust's experience), without naming the method. That would change what solvers see and would need a rerun.

**Why:** The memo's test is "expected 2027 retained claims PMPM > elected claims component". Every input is in the files: claims lag reports, eligibility, Westerby reimbursements and policy schedule, elections xlsx, and the 7% trend. I rebuilt the whole path and got the golden set (CR113, 118, 131, 149, 167, 176). The result is the same under Buhlmann-Straub, limited-fluctuation full credibility at 1,000 and at 3,000 lives, and the kappa ratio scaled 0.5x to 2x. The smallest margin to the line is +17.2 (CR113). Residual risk: the memo never says "credibility-weight". A solver who reads "expected" as the plain average of the trended experience gets a different set (CR104, 109, 136, 167, 176). That route is the intended wrong easy path. The data separates the candidates: within-employer year-to-year variance (s2 about 1.44e7) is far larger than between-employer variance (a about 1,970), so own-experience-only is not a defensible expectation for 99 to 1,900 member-month groups. I judge "expected" to carry that, but it is the one place a literal reader could split.

**Evidence (recomputed, all reproduced):**
- Claims: incurred 2023-25, paid through March of the next year, taken from the legacy file. The May 2026 overlap between the two platforms is 144 vs 144 cells and identical to the cent, so it is irrelevant to the main call. The cents-to-dollars conversion is also not needed for it. Every 2023-25 cell is paid by the cutoff, so a later cutoff changes nothing (diff 0).
- Reimbursements: all 14 rows tie out as paid minus deductible equals reimbursed. The employer from the policy schedule equals the employer from the eligibility member_ref in all 14. Policy renumbering at CR113, 136, 154, 167 and 176 is harmless.
- Member months 2023-25 come from eligibility, with no duplicates before July 2026. The trust-wide level is 500.25 PMPM, with trend factors 1.07^4, 1.07^3 and 1.07^2.
- Credibility Z runs from 0.14 (CR104) to 0.81 (CR181). Expected PMPM minus elected claims component: CR113 +17.2, CR118 +21.5, CR131 +18.0, CR149 +20.4, CR167 +28.4, CR176 +80.1. Every other employer is negative; the closest is CR181 at -32.7. The elected components match the golden's list exactly.
- Raw trended PMPM, own experience only, for comparison: CR104 578, CR109 628, CR136 673 are over their components. CR113 460, CR118 446, CR131 453 and CR149 421 are under. The fork changes 7 of the 18 calls (CR104, 109, 136 added; CR113, 118, 131, 149 dropped).
- Minor forks, none of which change the call:
  - Dropping the reimbursements gives the same set.
  - A 2025-only or 2024-25 window gives the raw set, so it is not a credibility-style reading.
  - An ex-self trust mean as the complement gives the same set.
  - Using the Ridgeline broker survey median as the complement (561 or 549) flips the result. The survey is an unused distractor and the memo says "the trust's" experience. The golden itself weighs against the trust's level, so this is a low-probability reading.
- Ask A, July to September 2026 member months: counted once per person-month, matched on employer, birth date, sex and relationship. The 2,075 duplicate person-months are all in 2026-07 to 09 (H-ids reissued as N-ids). The deduplicated counts match the golden for all 18 employers (CR104 99 through CR181 2,642). Raw row counts, which a naive solver gets, are 111, 139, 185 and so on. No false merges: there are no key collisions before July. The match key is not stated in the files, but the person is the only sensible unit for "a member enrolled in the month".
- Ask B, high-cost claimant report: latest row per person with old and new ids merged (65 persons carry two ids). Members and paid-to-date match the golden for all 18 employers (CR104 2 / 86,105 ... CR181 21 / 1,022,799). Naive per-id counts give 3 / 128,365 for CR104 and 37 / 1,757,425 for CR176.

**Files/Hygiene:** PASS. There are 14 files in 3 formats (csv x10, pdf x2, xlsx x1, plus the manifest and data dictionary as csv). One file is 179,535 rows. Distractors: pharmacy rebates (excluded by the memo), the broker survey (the memo excludes rebates and fixes trend at 7%), and the plan summary. The two claims files differ in layout (MM/YYYY vs YYYY-MM, dollars vs cents, column names), which is realistic Layer 1 mess. There is no authoring language in the memo or the dictionary, and dates are coherent (extracts 2026-10-07, memo 6 October, meeting 12 November). No public-data contamination and nothing exclusion-level. The manifest and dictionary read slightly tidy but are plausible.

**Stump power:** Moderate to high. The memo supplies trended per-employer experience and the test line, so a strong model will likely compare each employer's own trended PMPM to its component and file CR104, 109, 136 (the large-claim employers) instead of CR113, 118, 131, 149. That is a provable analytical error: the three spike employers have Z of 0.14 to 0.33 and the four low-luck employers have claims components well under the trust level. Asks A and B add a second failure surface through the id reissue (naive counts), which is data-semantics but not the main call.

**Stumping type:** `mechanism: method_or_model_selection` (credibility / partial pooling, with statistical_rigor and etl_conformance as lower layers), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported claims and member months are correct. The difficulty is the estimator for a small group's expected cost, and it persists on perfectly clean data. Gate G passes.

**Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`.
- Domain: health-plan experience rating for a self-funded trust. The decision is a credibility-weighted expected PMPM against a rate component, which is core actuarial work.
- Layer 1: two claims platforms with different layouts and units, an overlapping month, member-id reissue, and policy renumbering.
- Layer 2: credibility-weighting small-group experience.
- Easy route: take each employer's own trended three-year PMPM at face value, which surcharges CR104, 109, 136, 167, 176 instead of the golden six.

**Fix:** none (solution and files are consistent). Optional prompt or memo hardening only, as noted under Disposition.

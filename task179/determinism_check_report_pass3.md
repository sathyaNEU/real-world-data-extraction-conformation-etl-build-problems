# determinism-check report, task179, 2026-10-25 (pass 3, portal round 5 repair)

## Verdict
DETERMINISTIC (SOLUTION_WRONG on one supporting figure, step 6, fixed in the write-up)
**Disposition:** FIX_NOW, applied: step 6 reworded to name the model (all 2019 to 2025 entrants, step 5's attributes, no
count) and the entrants it predicts for (the 11,640 meeting fewer than 10 others twice); the thread had fitted on those
11,640 and applied the model to 2026. The figure 4,166.2 is unchanged and asserted; nothing graded moved, so the verdict
stands without a further pass (a wording fix the judge asked for).
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Pack: target.zip 01124ef4, unchanged since portal round 5. Thread: scratchpad determinism-check-task179-r8, order kept
(blind_derivation.md on disk before graded_blocks.md was opened); its blind call 2,250.

## The thread's verdict, verbatim

- **Verdict:** DETERMINISTIC (SOLUTION_WRONG on one minor supporting figure, step 6)
- **Disposition:** FIX_NOW. Reword or correct SOLUTION_STEPS step 6 (the 4,166.2 check); no change to the prompt or the files, so no model rerun.
- **Order kept:** yes. blind_derivation.md was written to disk before graded_blocks.md was opened. My blind forecast was 2,250 (I missed the peer-sharing feature); I then reproduced the golden's mechanism from the files.

**Why:** Both asks are forced. The 20 group cells match the golden exactly, and the forecast reproduces at 3,250. The 2026 entrants were placed in classes in a different way from the 2019 to 2025 intakes. History: about 79% of entrants meet 10 or more other entrants in two or more classes. 2026: 10.7%, and 3,778 of 8,659 meet none (reproduced). Attrition runs 44% for entrants who meet nobody twice and about 20% for those who meet 15 or more. Adding the flag takes AIC from 57,453 to 56,377, and the prediction goes from 2,142 (so 2,250) to 3,244 (so 3,250). Every threshold from 3 to 15 gives 3,218 to 3,246 and an AIC within about 12, so 3,250 is robust. The 3,125 and 3,375 bin edges are 120 or more away.

**Evidence (recomputed):**
- Intakes: 8,659 first-time entrants enrolled in 2026. Continuation uses the crosswalk for the 2025 intake. Non-continuation by intake runs 25.6% down to 24.5%. The pooled rate gives 2,137 and the 2025 rate gives 2,119, which falls under the 2,125 line.
- Group counts (<=30 / >30), union of students per distinct class set, cancelled classes dropped, enrolled per census history:

| Faculty | 200 | 300+ |
|---|---|---|
| FASS | 14 / 40 | 20 / 45 |
| FBUS | 15 / 39 | 22 / 46 |
| FSCI | 15 / 39 | 22 / 38 |
| FENG | 18 / 33 | 25 / 34 |
| FHLT | 17 / 36 | 25 / 32 |

- 40 groups pair a 300 class with a 400 class, so level binning is unambiguous. No group mixes faculties or includes 100 level. The 34 duplicated timetable rows collapse under the set logic.
- Not reproduced: step 6's "predicts 4,166.2". I get 3,408 to 3,436 for the model fitted on entrants with fewer than 10 peers and applied to all 2026 entrants. Supporting check only; it does not move the call.
- Forks that survive:
  - (a) Census filter on class places. The extract header says "at the 2026 census" and every row is ENROLLED. Conventions s2 and s4 say a student on leave is not enrolled and size counts enrolled students. Excluded: 170 on-leave students and 242 students with no 2026 census row. Taking the extract as-is changes 14 or more of the 20 cells (FASS 200 would be 12/42). The filter is the literal reading of the conventions; the golden step 8 states it. Moderate fork, closed by text.
  - (b) The timetable "Enrolled at Census" column is inflated by 5 to 33 on 100 active 200+ classes (60 flip from <=30 to >30) and cannot give a union for a two-class group. The conventions call for students taught, so the student rows govern.
  - (c) Model set. The AIC rule is filed and the candidate set is not. Models without the peer feature give 2,070 to 2,300 (2,000 or 2,250); models with it give 3,218 to 3,246. The data separate the candidates by more than 1,000 AIC, so the AIC rule picks the feature. A solver who never builds it still follows the filed text literally, but is wrong on the data.

**Files/Hygiene:** PASS. 15 files, formats xlsx, pdf, csv and txt, with 25,000+ row files (the census file has 202,053 rows). Distractors: hall occupancy, school-leaver statistics, programme transfers. SIRIUS/ARC ID, date and code changes are realistic layer-1 mess. No authoring leakage seen. I did not inspect the PDFs for anything beyond their text. No exclusion-level finding.

**Stump power:** Strong. The easy route is an early-warning logistic model on admissions attributes and week-6 ratings, or the earlier intakes' rate. It gives about 2,140 to 2,200, so 2,250, which is about 1,000 too low. The 2026 entrants are largely outside the experience of the history: only 11% meet 10 or more others twice, against about 79%. The effect is visible inside the history (44% against 20%). Finding it needs the class-sharing network, which the prompt never mentions. The group-count ask carries its own device: the inflated timetable counts and the leave and withdrawn students.

**Stumping type:** `mechanism: forecasting`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The numbers are correct. The difficulty is a covariate-shift forecast on a structure the history pins, selected by AIC. It is not a flip away from a misleading reported read. On clean data it would still stump.

**Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`.
- Domain: retention forecasting with peer-integration (cohesion) effects and teaching-group planning is the field's own work. Swap test fails to hold: "megawatt-hours" does not fit a first-year class network.
- Layer 1 (mess): SIRIUS/ARC cutover (ID crosswalk, code and date formats), duplicated timetable rows, leave status.
- Layer 2 (analysis): a model whose predictor changes distribution in the forecast year, chosen by AIC.
- Easy route and wrong answer: the attribute-only retention model, 2,250. A strong analyst who cleaned everything and read every rule correctly still files that.
- Caveat: the peer feature is found by exploring the class-enrolment data, not stated. This is discovery of real structure, not a planted rule or a field reading.

**Fix:** solution only. Correct or drop step 6's 4,166.2 so it reproduces (about 3,408 to 3,436 under my specification). Nothing else needs to change; optionally add the ask 2 census filter to the data dictionary header, but the conventions already state it.


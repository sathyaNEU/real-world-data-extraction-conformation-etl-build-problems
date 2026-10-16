# Verdict (task150 re-judge, fresh)

**Cross-batch check:** only the shipped bundle was available to me (other tasks are forbidden); no duplicate could be checked from here. Nothing in the package suggests a public-data answer or an earlier delivered tasks's text.

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE. No repair required; no rerun. One residual fragility (method not filed in the prompt) is reported below and is optional to harden.
- **Why:** FEA-R2 (PDF) fixes the estimand (K-5 count-day enrollment, 2028-29 to 2032-33 mean, less permanent-room rated capacity in facilities_capacity_report_2026-09.xlsx, over 24 rounded up, ranked by excess, cap 8, remaining classrooms run out). Projecting by a component flow model (repeats, moves by destination, exits, arrivals, kindergartners per resident birth five years earlier) reproduces the golden need 7/6/5/4/3/1/0 and placement 7/6/5/4/2/0/0. The data pick that method over the textbook progression ratios by a back-test from 2019, and the placement does not move under any flow-model window or birth-assumption I tried. Main call and all three xlsx tables reproduce.

## Evidence (recomputed from the bundle)

| Item | Result | Source |
|---|---|---|
| Linked pupil rows | 76,597 over 14 count days, 0 duplicate pupil-year, reproduces | membership_oct2013-oct2018.txt (pipe, 241 blank SASID resolved through crosswalk, 34 more via STU_NBR to SASID) + october_membership_2019-2026.csv + student_number_crosswalk_2019.csv + school_codes.csv (105 = Kessler = state 6175) |
| Transitions 2013 to 2026 | 13; stay 54,152, repeat 484, move 2,098 (all +1 grade), exit 2,462, arrivals 14,662 | same |
| Ortega to Bluestem moves | 58 to 93 a year, 9.3 to 11.8 per 100 Ortega K-4 (reproduces); rate CV 6% vs count CV 11%, so a rate on the source school is what the data support | same |
| Fifth Street arrivals grades 1-5 | about 77 a year, range 66-89; Prairie Rose 61-81 (reproduces) | same |
| Excess over rated capacity, flow model, 2028-32 mean | Prairie Rose 152.7, Lincoln 131.5, Fifth Street 109.3, Bluestem 89.2, Kessler 61.7, North Fork 10.8, Ortega -91.8. Golden 152/131/109/89/60/10/-92. Reproduces within 2 pupils; needs 7/6/5/4/3/1/0 identical | facilities xlsx capacity 667/640/703/710/833/651/577 |
| Back-test from 2019, flow model | 2026 error: FS -0.4, Lin -0.4, Ort +4.9, Blu +2.7, PR -0.9, Kes +2.2, NF +0.8 (max 4.9, golden says 5.0 or less) | reproduces |
| Back-test, 5-year progression ratios from 2019 | FS -8.0, PR +8.5, Ort +5.6, Blu +3.9 (golden: 8.2 low, 8.3 high; window 3 gives -9.0 / +8.2). Flow model also wins from 2021, 2022, 2023 | reproduces |
| Ratio-method answer (the easy route) | window 5: PR 9 (cap 8), Bluestem 7, Lincoln 6, FS 5; placed PR 8, Bluestem 7, Lincoln 6, FS 3, Kessler 0 (golden's "not" line reproduces); window 3 gives PR 8, Bluestem 6, Lincoln 6, FS 4 | project |
| Robustness of the golden | flow model with windows all/8/5/3 transitions and births assumption 2025 / 2021-25 / 2023-25 average: placement 7/6/5/4/2/0/0 in all 12 runs. Margins to the ceiling lines: PR 6.36, Lin 5.48, FS 4.55, Blu 3.72, Kes 2.57 | var.py |
| Homeroom classes 10/1/2026 (K-2 / 3-5) | FS 17/17, Lin 19/15, Ort 19/13, Blu 15/20, PR 21/20, Kes 15/17, NF 13/13, all reproduce. Class = room + session, band by enrolled pupils' grade (sis_export_notes), active lines 5,401 equal the 2026 roll; end_date on or after 10/1 vs after 10/1 makes no difference | sections_fall2026.csv, section_enrollment_fall2026.csv, october_membership |
| Preschool 10/1/2026 | registrations active on the date, deduplicated by state_id (two true duplicates plus transfer pairs 00750 and 01278 each active once), plus ECSE-classroom and inclusive roster children by the room's school: FS 88, Ort 94, Kes 51, NF 35; rooms 4/4/3/3. Reproduces. Without the dedupe or the ECSE add the figures differ (78/81/34/30 and 77/79/32/29), but the ECSE notes pin the rule (itinerant not enrolled in a district class; classroom = where the class meets) | preschool_enrollments_2026-27.csv, ecse_roster_2026-10-01.xlsx |

## Gates A to E

- A: pass. Every critical component and supplementary figure reproduces. Grain honoured (snapshots are full October rolls, not change logs).
- B: pass. Rule, capacity, births, rolls, sections and rosters are all in the bundle; rooms and ECSE rules sit in the xlsx Notes sheet (table checked directly). Action vocabulary (classroom need, placed) is the PDF's own.
- C: pass with a stated residual. Competing answer: textbook five-year grade progression ratios give PR 8 / Bluestem 7 / Lincoln 6 / Fifth Street 3 / Kessler 0. It is rejected by the shipped data, not by taste: it misses Fifth Street by -8% and Prairie Rose by +8.5% in a 2019 hold-out, because it cannot see the steady arrival stream into those two schools or the Ortega-to-Bluestem stream. A second plausible flow variant (moves as fixed yearly counts rather than rates) gives Bluestem 6 and Kessler 0, but it fits the history worse on the volatile series (rate CV 6% vs count 11%) and misses Ortega by 9.4% against 4.9%; I count it as dominated, not defensible. Residual risk: neither the prompt nor FEA-R2 files a validation criterion, so the golden depends on the solver validating out of sample as an expert would.
- D: pass. The split among good answers traces to the analysis (flows vs ratios), not to a word.
- E: pass. Prompt asks one committed placement per school; tables and PNG pinned by policy and notes; "whole number" stated.

## Files/Hygiene

PASS. 16 files; formats pdf, txt, csv, xlsx (4); 76,597 membership rows (44,314 + 32,283) satisfies the 25,000-row gate. Legacy pipe/US-date file against current CSV/ISO-date file, blank SASIDs, a renamed school, code changes and a provisional births year are real-system mess. Distractors in play: meal_eligibility_2026-10.csv (its counts equal the 2026 roll, no placement use), facility_condition_assessment_2025.xlsx (FCI ranks Lincoln and Fifth Street worst, a wrong-basis ranking nobody needs), portables note. Neither ranks the candidates on the placement question. Dates are coherent with a 10/09/2026 pull and the 11/2026 Board meeting. No authoring or benchmark language seen in any file. Nothing exclusion-level. Tell worth a glance: births_file_notes and sis_export_notes are tidy, but they read as ordinary data-owner notes.

## Stump power

Good. The easy and standard route (five-year progression ratios plus births for K) gives a wrong placement at three of the top four schools and puts 3 classrooms at Fifth Street where the golden puts 5, and 8 at Prairie Rose where it puts 7; a strong model that stops there files it. Reaching the golden needs the 76,597-row pupil linking across two systems and the crosswalk, the realisation that arrivals and Ortega's transfers are structural, and a hold-out comparison. Still reachable by a careful solver, so the task is neither too easy nor a coin flip.

## Stumping type

`mechanism: method_or_model_selection` (with etl_conformance in Layer 1), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. No reported figure is wrong; difficulty is choosing the projection method that out-of-sample validation supports. On clean data the task would still stump (the ratio method fails the hold-out on clean data), so Gate G passes.

## Three rules

`domain: pass`, `layers: pass`, `decisive_step: analytical`. Domain: school enrollment projection for facilities planning (cohort survival vs component flow, births, hold-out accuracy), which a facilities planner or demographer does for real; swap test ("hospital" for "school") breaks it. Layer 1: two student systems, crosswalk, blank state IDs, renamed school, provisional births. Layer 2: component flow projection chosen by back-test. Easy route, taken by a strong analyst with clean data and every rule read right: five-year grade progression ratios, giving Prairie Rose 8, Bluestem 7, Lincoln 6, Fifth Street 3, Kessler 0 instead of 7/6/5/4/2.

## Fix

none. Optional hardening against the Gate C residual: one clause in the prompt filing the WHAT of validation (for example that the projection must reproduce the district's own 2026 counts when run from 2019), which would also make a solver act on the back-test. Not required to approve.

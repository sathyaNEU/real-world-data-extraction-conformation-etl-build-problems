# determinism-check report, task266, pass 6 (2026-11-01, the isolated thread's verdict on 78dca29c, kept as filed; not reconciled, because the build went to repair and then to a re-root)

# Determinism verdict, task266, pass 6

**Verdict:** NOT_DETERMINISTIC on the supplementary figures only (taxonomy: underspecified_objective). The main call (six programs: General Studies, Biological Sciences, Business Administration, Psychology, Medical Assisting, Early Childhood Education) reproduces and holds under every sensible estimator I tried, except one literal as-of-date reading (fork 3 below). Deliverable ask 2 (FTE, all nine) is not forced by the shipped files, and the nine one-decimal shares in ask 1 depend on an unfiled estimator.

**Disposition:** FIX_NOW. Close forks 1 to 3 below with one filed sentence each (policy 3.3 and 4.1, or the register). No data file changes, so no model rerun is needed if the graded figures stay as they are.

**Why:** Ask 2 is `deliverable ask 2` in program_completion_review_2027.xlsx. Policy 4.1 uses "program of record at the census". program_of_record_history.csv holds 229 students with two or three rows in effect at 202710 (226 with 2, 3 with 3). The golden resolves them with "the program the registrations carry" (regs program_code). No shipped file states that rule, and the export manifest that would have defined the column is gone. The other defensible rules (latest effective row, earliest row) give different one-decimal FTE for all nine programs, for example Nursing 533.1 (golden), 608.3 (latest row) and 533.8 (earliest row). Gate C/E fails for that ask. The main recommendation is not affected by this.

## Evidence (recomputed from target/)

Entering cohort: 1,691 + 1,752 + 1,849 = 5,292 students. Every fall-2023 legacy ID maps through the conversion file, 0 unmapped. Legacy programs map via the register. Every student matches exactly one admission row at (student, entry term), with no program mismatch. Admit types at entry are N (4,670) and T (622). The 5 deceased students (DC) are removed.

**Three-year completion share.** I used competing-risks cumulative incidence pooled over the three classes. Terms are counted from the entry fall with summer included, so the ninth term is summer 2026 for fall 2023, summer 2027 for fall 2024 and spring 2028 for fall 2025. TO and WD are competing endings, and open admissions are censored after 202720.

| Program | Golden | Recomputed |
|---|---|---|
| General Studies | 20.9 | 20.9 |
| Biological Sciences | 24.9 | 24.9 |
| Business Administration | 22.2 | 22.2 |
| Psychology | 25.9 | 25.9 |
| Medical Assisting | 26.2 | 26.2 |
| Early Childhood Education | 19.5 | 19.5 |
| Criminal Justice | 32.5 | 32.5 |
| HVAC-R Technology | 44.4 | 44.4 |
| Nursing | 36.7 | 36.7 |

- Reproduced, 9 of 9. Sources: ir_fall_entering_students sheets, sis_admissions_exits (exit_term, exit_reason), term_calendar.
- Policy 3.2 is what excludes a degree earned under a readmission. 21 entering students have a conferral on file after an entry admission that ended in WD. All 21 were readmitted (type R) and graduated under that readmission. A conferral-file-only approach would wrongly count them.
- For the 1,169 entry-admission GR exits, exit_term equals the conferral term in 100 percent of cases.

**Estimator sensitivity (not filed in 3.3, which says only "an estimate, made from that record").**

| Estimator | Programs under 30 |
|---|---|
| Pooled cumulative incidence (golden) | the same six |
| Conditional-landing from fully observed class, by program | the same six (CJ 31.5, NURS 37.1) |
| Conditional-landing, college-wide | the same six (NURS 33.2) |
| Ratio scaling from the fall-2023 class, by program | the same six (CJ 31.1, NURS 33.5) |
| Ratio scaling from the fall-2023 class, college-wide | the same six (NURS 30.7, thin) |
| Observed share only, no estimate (ignores 3.3) | eight (CJ 26.7, NURS 27.6 also fall below 30) |
| 1 minus Kaplan-Meier, leavers censored (contradicted by 3.2) | one (ECED only) |

- Under the sensible estimators the call is robust, but the one-decimal figures move by up to about 1 point. General Studies runs 20.7 to 21.4. Criminal Justice runs 31.1 to 32.5. Nursing runs 33.2 to 37.1.
- So the call is forced and the exact one-decimal shares are not (fork 1).

**FTE.** Registrations in place at the census are RE/RW dated on or before 2026-09-08, plus WC (all dated after the census). Credit hours come from the section schedule Cr Hrs, which differ from regs course_credit_hours on 6,690 rows (labs carry 0). Divided by 15.

- With the golden tie-break, all nine FTE reproduce exactly: 1,148.8, 352.5, 525.2, 399.4, 381.5, 341.0, 391.2, 272.3, 533.1.
- end_term is inclusive. Read as exclusive it leaves 437 registered students with no program, and the CHG rows show the next row starting one term later. The data closes this one.
- Regs program_code is not authoritative in general: it disagrees with the single in-effect history row for 241 of 7,127 single-row students. The history is the program of record, and the golden uses regs only as a tie-break. The tie-break is unfiled (fork 2).

**Small classes.** I counted active sections of each program's register subjects. Sections with the same instructor, days and begin time and overlapping dates are one class, with registrations added. LAB, SHP and CLN sections stay on their own. All nine counts reproduce exactly: 2, 15, 7, 7, 10, 5, 8, 21, 79.

- There are 20 same-instructor/days/time pairs. Ten overlap and merge. Ten are half-term sections with disjoint dates and do not merge.
- Ignoring date overlap changes the counts (for example General Studies 1, Nursing 78). The policy's "scheduled to meet together" supports the overlap reading, so I treat it as closed.
- The 200 online TBA-time sections are classes of their own.

## Forks (what the pack no longer defines)

1. **Estimator for the open-admission part of the share (ask 1, one decimal).** Policy 3.3 files only that "the share includes an estimate". The nine percentages vary by estimator as above. The main call is invariant across sensible estimators. Fix: file the WHAT in 3.3 (for example that admissions ended by TO or WD without the degree count as not completing, and that the estimate uses the three classes together), or state the grading tolerance.
2. **Tie-break between two program-of-record rows (ask 2, all nine FTE).** The pack gives no rule for 229 students with 2 or 3 history rows in effect. The golden rule exists only in the solution block. The history has no flag for a limited-enrolment application. Regs program_code is stale for other students. Fix: file the sentence in 4.1 or the register.
3. **"Record as it stands at the end of the spring term" (policy 3.3), literal date reading.** All 457 spring-2027 graduations carry exit_recorded_on from 2027-05-18 to 2027-05-25, after the term's last day (2027-05-14) and its conferral date (2027-05-17).
   - A strict as-of-5/14 cutoff drops them (373 are in the cohort) and gives 15.6, 18.4, 22.5, 16.5, 31.6, 18.9, 27.4, 18.1 and 16.1 for GS, PSYC, CJ, ECED, HVAC, MEDA, NURS, BIOL and BUSA. That is eight programs in review, with only HVAC-R above 30.
   - The sensible reading is that spring conferrals belong to the spring record. The conferral file and the calendar's conferral column support it, and the same 8-day lag appears in every earlier term. This is the only literal reading I found that flips the main call, so I recommend one clause in 3.3 (for example "including the term's conferrals").

Undefined-code check (no manifest or extract notes): reg_status (RE/RW/WC/DD/DW), admit_type, exit_reason and change_reason all carry in-row descriptions, and the dates separate them. Dropped rows are all dated before the census and WC rows all after, so no second figure opens from those codes. The only undefined item that opens a second figure is the tie-break (fork 2). The unit of the section Cr Hrs is stated in policy 4.1. The Link column is not needed.

## Files/Hygiene
PASS. 12 files in four formats (xlsx x5, csv x5, txt, pdf). The regs file has 28,117 rows, meeting the large-file gate. Distractors present: course_success_rates, the occupational outlook, and the conferrals file (relevant, but only the 21 readmit cases touch it). Authorship metadata is in-fiction (Registrar, Academic Affairs and the like), the PDF dates are 2025, and file dates are consistent with a late May 2027 extract and a June 2027 review. No benchmark language. Nothing exclusion-level. This is a synthetic-looking institution, but the files are heterogeneous and carry real noise (legacy and new keys, TBA sections, stale program codes).

## Stump power
Good. The easy routes file wrong answers a careful analyst can reach: the observed-only share gives eight programs, a Kaplan-Meier that censors leavers gives one, and a conferral-file degree count inflates shares through the readmitted graduates. The right estimand (competing-risks cumulative incidence under the entry admission) gives six. The 8 versus 6 versus 1 spread is analytical, not semantic.

## Stumping type
mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no. On clean data the censoring and competing-risk estimand still decides the call.

## Three rules (Gate H)
domain: pass, layers: pass, decisive_step: analytical. Layer 1 is the legacy-to-new ID and program-code conversion, term-code crosswalk, TBA sections and stale registration program codes. Layer 2 is the survival estimate of three-year degree completion with leavers as competing endings. The easy route is the observed share (eight programs, with CJ at 26.7 and NURS at 27.6) or Kaplan-Meier (one program).

## Fix
Fix location: input_files, not the golden.
- 4.1 (or the register): "where a student has two program-of-record rows in effect at the census, the program of record is the program the student's registrations carry."
- 3.3: a clause that the spring record includes the term's conferrals, plus the leaver treatment in fork 1.
- No data or prompt change. The golden figures stay as they are.
- A Gate G / Gate H change is not needed.

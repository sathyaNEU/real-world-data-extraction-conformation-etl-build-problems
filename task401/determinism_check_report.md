# determinism-check report, task401, 2026-11-04

Architecture 6 (Strathcorrie Council's S1 to S3 maths, the homework platform switch against the new framework).

## Pass 1 (target.zip e002e59b, judge thread run by the coordinator)

**Verdict:** NOT_DETERMINISTIC on one supplementary ask. **Disposition** as labelled by the thread: SEND_BACK. Read against
the gate table (determinism-check, a disposition is read against the gate table, not taken on its label): the main call
is forced (the switch leads by 2.5 times or more under every reading the thread ran), every headline, chart, reach and
lessons figure reproduced, Gate F strong (the thread's blind derivation, written before it opened the graded blocks,
filed the asymmetric week with the switch unidentified), Gate G decomposition_attribution and analytical_non_defect,
Gate H analytical. The one failure is Gate C on the classes ask: the golden counted both holders of a half-time
job-share post as teachers of its classes while the timetable carried one code for every period of those classes, and
two naming conventions (renames, summer changes of holder) were unstated. An ask-layer repair, no architecture spent.
Closed in one generator pass in the world: each job-share holder teaches the post's classes on their own days under
their own code; the establishment carries Previous_Surname; the three summer leavers stand on the establishment with
their last day in post (15/08/2025, before the first lesson on 18/08/2025) beside their successors. No graded figure
moved; the reader's realism list (post references, survey item nonresponse, sign-in reasons) was fixed in the same pass.
Before this pass the coordinator had moved the two June shares to whole per cents (at one decimal they sat 0.004 and
0.006 from a rounding edge); target.zip did not change.

### The thread's verdict, verbatim

- **Verdict:** NOT_DETERMINISTIC (the main call and the means/shares/lessons figures hold; supplementary answer 2, "classes with more than one teacher", does not).
- **Disposition:** SEND_BACK. The fix is local to the second column of support_and_staffing_by_school.csv: pin in the ask (or restrict the golden to) who counts as a teacher of a class, then rebuild the golden; the main call, the stump and the lessons column stay as they are. The ask text changes, so any prior reads are void.
- **Why:** The golden's teachers-per-class counts (6, 5, 9, 7, 3, 12, 3, 5) need a rule no shipped file states: the two holders of a 0.5 FTE job-share post in maths_staffing_establishment_2025-26.xlsx both teach the post's classes, although maths_timetable_2025-26.csv carries one code for every period of those classes (T3614, T5776, T9338, T8530, T6008) and the register (section 3, change E) describes only the split classes as shared. The literal timetable-plus-establishment reading gives 3, 5, 4, 7, 0, 9, 0, 5 (Ardcorrie, Balmorran, Glenwhinnie, Kilbraith, Lochbrannie, Muirlees, St Moluag's, Torranbrae). Both are defensible, and five schools differ. Gate C fails on supplementary 2: competing_defensible_answer. Two further conventions are also unstated: code-name changes (Pope to Turnbull, Matthews to Edwards, Brady to Holland, Cooper to Chadwick, McDonald to Willis, Thorpe to Morris) count as renames, while Roberts to Newton and Webster to Taylor count as hand-overs. The establishment supports both of those readings, so they are closable, but they are not filed.
- **Evidence:**

| Item | Golden | My recomputation from the bundle |
|---|---|---|
| Mean mark 2025 / 2026 | 32.3 / 30.3 | 32.31 / 30.31 (n 4,346 / 4,426) reproduced |
| Share at 36 or more | 42% / 36% | 42.15% / 35.86% reproduced |
| School means (8 schools, both years) | as listed | all 16 reproduced |
| Reached counts | 1,491 S3, 241 referred, 587 split | all three reproduced |
| Lessons missed per school | 24, 20, 22, 19, 15, 27, 24, 18 | reproduced exactly (169) only after rebuilding each pupil's autumn class |
| Classes with more than one teacher | 6, 5, 9, 7, 3, 12, 3, 5 | reproduced only with the job-share rule; the literal reading gives 3, 5, 4, 7, 0, 9, 0, 5 |

  - **Lessons missed:** reading the class off the June roll, the obvious route, gives 172 and 24, 22, 19, 20, 18, 28, 22, 19. About 353 pupils (7.6%) sat in another class before January. Their autumn class can be rebuilt only from identical autumn review sequences in mathsbridge_homework_export_2025-26.parquet, and the rebuild is unique and reproduces the golden. That is hard but forced. Nothing in the package says that classes were re-set in January.
  - **Main call:**
    - Order of the changes. The within-pupil weak-unit contrast widens from -0.123 to -0.187 in share (bottom 4 of 12 units by first-homework accuracy). That is about 5,600 marks, and 4,500 to 6,250 across bottom 2, 3, 4 and 6 units and random tie-breaks. Change A by the same contrast is about 1,500 marks. C, the S3 difference-in-differences, is about 1,600 to 2,400. D is under about 1,000 and E under about 600.
    - Mechanism. In corvella_homework_export_2024-25.csv, retrieval exposure is aimed at each pupil's weak units (correlation of unit accuracy with exposure -0.54). In the Mathsbridge export it is class-wide (+0.19). Homework completion is unchanged (79% to 82%), so the platform effect rides on the targeting.
    - Margin. The lead is 2.5 times or more under every reading I ran, so Gate C holds on the main call.
  - **Competing answer on the main call.** A group-level difference-in-differences that ignores the targeting gives C (the asymmetric week) as the largest. That is the intended easy-route error, not a defensible rival. The files evidence the mechanism, the weak-unit contrast is a recognised within-pupil design, and the register itself says no between-group comparison separates A from B.
  - **Gate B:** every decisive value is in a shipped file.
  - **Gate A:** the Critical Components agree with the files. A residual early-unit decline of about 0.12 per unit is not attributed to A to E in a group-level model. The weak-unit contrast absorbs it, which is the golden's logic.
- **Files/Hygiene:** PASS. Sixteen files; formats csv, xlsx, parquet, docx, pdf (five); the 2026 marks file has 163,476 rows and the Corvella export has 189,696. Distractors present: attendance, survey, Corvella retrieval history, the staffing sheets. Layer-1 mess is realistic: two SCN and Glow ID key systems, typed-name sign-ins, 20 exact duplicate sign-ins, staff codes that change between terms, S4 to S6 sign-ins to exclude, a base shared by two schools, a Friday short day. Dates are coherent (register 15 June 2026, roll 12 June 2026). I found no authoring leakage. Nothing is exclusion-level.
- **Stump power:** Strong. A capable analyst who cleans everything and runs the usual per-change difference-in-differences files C (the S3 week) at roughly -2,000 marks, or A, and never meets the targeted-versus-uniform review structure. A and B started the same day for everyone, so only the within-pupil contrast separates them. The supplementary asks add real difficulty: the January class re-set and the job-share, rename and hand-over conventions. These asks are determinate except as in the Why.
- **Stumping type:** `mechanism: decomposition_attribution` (within-pupil identification), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported means and shares are correct and nothing is planted. No shipped artifact ranks the five changes, so Gate G passes: the register states the remit and the cost definition, not a ranking.
- **Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`.
  - Layer 1: key mismatches, a January class re-set, a staff-code drift and a platform switch.
  - Layer 2: a within-pupil design that separates a change which hit every pupil on the same day.
  - Field analysis: education research on a multilevel, within-pupil estimand of what a homework platform's retrieval targeting is worth. The swap test fails if the nouns are changed, because the targeting channel is specific to homework retrieval.
  - Easy route: group difference-in-differences on S3 against S1 and S2, which names the asymmetric week.
- **Fix:** solution or prompt, supplementary 2 only.
  - Preferred: add to the ask the sentence that fixes the population, for example "counting both holders of a job-share post as teachers of its classes, and a code whose holder's name changed as one teacher". Then keep the golden as it is.
  - Alternative: restrict the golden to the timetable-coded teachers plus the two establishment hand-overs (3, 5, 4, 7, 0, 9, 0, 5), and drop the job-share inference. The zeros are weak for an ask.
  - Either way, regenerate the CSV and the submission block.
  - Optional: say in one clause that pupils may sit in a different class before January only if the ask must stay reachable. Otherwise it stays as a deliberate hard layer.

## Pass 2 (target.zip 1875a727, judge thread run by the coordinator, round1_findings.md opened with the graded blocks)

**Verdict:** DETERMINISTIC. **Disposition:** APPROVE, no fix, no rerun. Order kept; the thread's blind derivation again
could not name the switch (it found the asymmetric week first), and it reproduced every figure, the classes counts
included, once the filed records were applied.

### The thread's verdict, verbatim

# Determinism verdict, task 401 (Strathcorrie S1 to S3 maths changes)

Order kept: derivation.md was written before graded_blocks.md and round1_findings.md were opened. My blind pass could not name a change with confidence (it found C first, with B unidentified); I only found the within-pupil weak-unit mechanism after reading the graded blocks, and then verified it from the files (below). My blind pass also miscounted Ardcorrie classes (3 against 6) and the pre-January class for the lessons figure; both were reproduced to the golden once the filed rules were applied.

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE. No repair needed; no model rerun.
- **Why:** The register fixes the estimand (marks lost over reached S1-S3 pupils who sat June 2026), and the shipped data separate the candidates by a wide margin under every reasonable estimator that can see all five changes. Change B (Mathsbridge for Corvella) costs about 5.2k to 5.7k marks, against about 2.0k for C, about 1.3k for A, 0.4k to 1.0k for D and about 0.6k for E. All asks (means, shares, school means, lessons, classes) reproduce.

## Evidence (recomputed from target/)
| Item | Golden | Mine | Source |
|---|---|---|---|
| Mean 2025 / 2026 | 32.3 / 30.3 | 32.31 / 30.31 | june_common_paper_marks_2025/2026.csv, sat only (4,346 / 4,426) |
| Share >=36 | 42% / 36% | 42.15% / 35.86% | same |
| School means 2025 -> 2026 | all 16 | all 16 match (e.g. Ardcorrie 32.146, Kilbraith 2026 28.247, so 28.2 is not a rounding knife-edge) | roll joins |
| Reach: S3 / referred / split classes | 1,491 / 241 / 587 | identical | roll extract, register s.5 |
| Lessons missed (Ard, Bal, Glen, Kil, Loch, Muir, StM, Torr) | 24, 20, 22, 19, 15, 27, 24, 18 | identical | sign-ins, bell times, timetable, roll |
| Classes with >1 teacher | 6, 5, 9, 7, 3, 12, 3, 5 | identical | timetable, two code sheets, establishment |

- **Main call.** Corvella retrieval follows each pupil's errors: 75% of its slots fall on the pupil's weakest four units by first-attempt homework accuracy. Mathsbridge review is set per class: 37% (chance is 33%). Within pupil, the weak-unit mark shortfall (weak minus other units) widens from 2025 to 2026 by 5.2k to 5.7k marks over pupils who sat, whichever tie rule is used for "bottom third" (bottom 4 by unit order, reverse unit order, or a third of attempted). The widening is larger than the rewritten-unit contrast in all 24 school-by-stage cells. Alternatives:
  - C: S3 extra shortfall about 1.4 marks a pupil, 2.0k marks (2.0k to 2.5k by comparison group). Even attributing the whole S3 shortfall to C gives 4.25k, still below B.
  - A: 1.25k to 1.4k.
  - D: referral difference-in-differences about -3.0 a pupil, about 680 marks. Maths lessons missed carry no marks relationship once referral is in the model.
  - E: -1.05 a pupil, about 590 marks.
  - B is not visible to any between-group comparison, because it reached everyone (the golden says so in component 2). A model that stops at P7-adjusted group gaps or at the unit map's rewritten units lands on C or A.
- **Open forks I tested, none reaching the call.**
  - Lessons: distinct lessons give Ardcorrie 24 and Torranbrae 18, per-row sum gives 25 and 20. The PDF ("misses each lesson") and the golden's "each pupil and period once" settle it.
  - Pre-January class: Mathsbridge `class_code` is the June class on every row. The autumn review sets group the pupils into exactly 189 classes (spring sets equal the roll classes exactly; autumn sets match the roll for only 15% of classes). About 8% of pupils changed class at Christmas, in every school. Using the roll class gives different lessons for 6 of 8 schools. The reconstruction rests on the register's "a homework on each unit and a weekly review" set per class, and it reproduced the golden exactly. It is unsignposted but present in the files, so a careful solver is forced to it.
  - Classes: Ardcorrie rows run Valid_From 18/08/2025 to 26/06/2026 with one code T4286, which the two terms' code sheets name Roberts then Newton. Term-by-term resolution gives 6; reading the row as one code gives 3. Glenwhinnie's autumn sheet still names Cooper, who left on 15/08/2025, so the establishment decides. Maiden-name changes (Thorpe/Morris, McDonald/Willis, Pope/Turnbull) are closed by Previous_Surname. Counting job-share classes and replacements follows the literal "more than one teacher during the session".
- Round-1 findings (job-share codes, Previous_Surname, leavers' dates) are visibly fixed in the package: job-share holders have their own codes on their own days, and the establishment carries the leaving dates.

## Files/Hygiene
**PASS.** 16 files; formats csv, xlsx, parquet, docx, pdf (5). One 189,696-row csv (Corvella) and 193,162-row parquet. Distractors: attendance by month (unchanged year on year), pupil homework survey (positive on the website, which points away from B), bell and survey sheets. Roll, sign-in, code-sheet and establishment mess reads as system output (typed names with case errors, blank Time_Out, stale autumn code sheet, post-based codes). Dates are coherent: sign-ins to 29/05/2026, roll extract 12/06/2026, register updated 15/06/2026, budget set February 2027. No authoring or benchmark language seen. Not exclusion-level.

## Stump power
Good. The trap is analytical: the two all-pupil changes cannot be separated by group comparison, and the unit map hands the solver A (rewritten units) while C, D and E have clean reach flags. A strong model that runs P7-adjusted gaps will name C (S3 week, about 2k to 4k marks) or A. Only a within-pupil design that notices the Corvella error-following retrieval reaches B. Mild hints exist (register wording "a weekly review of earlier units"), but none gives the mechanism or the comparison.

## Stumping type
`mechanism: decomposition_attribution (causal attribution by a within-pupil design, with an ETL layer)`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. No shipped artifact ranks the candidates on the decision question, so Gate G passes. The data are honest; the register is correct; the difficulty is the estimand and design. On clean data it would still stump.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Domain: programme evaluation in education research (attributing an outcome change among concurrent interventions by counterfactual design). A swap to "hospital/visits" would not preserve the weak-unit design. Layer 1: code reformatting between terms, stale code sheet, typed names, class moves, overwritten class_code, SCN against MIS_Ref against Glow ID keys. Layer 2: separating universal changes by within-pupil, error-targeted exposure. Easy route a strong analyst takes after cleaning everything correctly: P7-adjusted reached-less-unreached gaps for C, D and E plus a rewritten-unit contrast for A, naming C (S3 asymmetric week, about 2.0k to 4.25k marks) or A. That is wrong; the golden is B.

## Fix
none. Optional, not needed: a sentence in no file is required, and nothing may be added to the inputs (it would change what solvers saw).

# determinism-check report, task281, 2026-10-24

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (judge thread). Main-session note: both stage 4 readers missed the call (each filed 63, title-average relief hours), so the stump landed; the ask layer is to be re-sited and the payroll rebuilt next pass.
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Judge thread (sonnet, one pass, run 1792874356, bundle md5 7563d715...) reproduced every committed answer from target/: 59 of 60 (9, 8, 7, 6, 6, 7, 10, 6), one to the reserve, via Standard 3.2 (fifth-heaviest week), 2.4, 2.3(b) and 3.4, with the relief holder's population fixed by the memo (July 2027 entry classes). The competing reading (title-average relief hour) gives 63 or 64; the memo's holder population closes it, and the data shows a clean tenure gradient in off-post share. The 59 is robust to any off-post share from 6% to 12% and to pooled/by-title, partial first week, and imputation variants.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Separation-vacant hours (roster) | 11,968 | 11,968 | yes |
| Vacant lines, first-shift weeks | 14, weeks 10 to 40 | same | yes |
| Fifth-heaviest week HRC/ACF/TWC/PCN/PCS/FFH/OXG/KPG | not filed in golden | 304/280/232/192/200/232/344/208 | n/a |
| July 2025 classes off-post share | 7.8% (units' holders 14.5%) | 7.83% (CO 8.05, PCO 7.38, FSA 8.25, HMW 7.76) | yes |
| Complements | 59 of 60 | 9,8,7,6,6,7,10,6 | yes |
| OT hours by unit (8) | 7,904 / 8,368 / 6,760 / 7,568 / 5,312 / 9,152 / 5,414 / 4,859 | identical | yes |
| Pay by title x quarter (16) | per submission | all 16 to the dollar | yes |
| People over 600 h | 10 / 5 / 6 / 4 | 10 / 5 / 6 / 4 (nearest 584 and 612) | yes |

## Competing answers that survived
- Title-average relief hour: 63 (new-line holders at zero off-post, or imputed vacancies) or 64 (new-line holders at title rate). Closed by the memo's holder population and 3.3 "its holder". Judge calls it a stump, not a fork; residual risk noted because "Hours are reckoned by title" alone licenses it. The design note itself says nothing files HOW the holders' share is estimated, so the closure rests on the memo sentence plus the HR join.
- Payroll file holds 682 exact-duplicate rows. Deduping moves unit hours (HRC 7,564, ACF 7,828, ...) and over-600 counts (9/4/3/3). Golden keeps them (dictionary: one row is one line; OTR hours reconcile only if repeats are real). Diverges on asks 2 to 4, not the main call. Residual fork on the asks.
- Over-600 unjoined: 9/4/5/4; paid-OT-only: 7/5/4/4. Both ruled out by MOU 14.2 and Art. 16.1.
- Fiscal and calendar quarters coincide for FY2026: no fork.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 15 | yes |
| Formats | 3+ | 4 (CSV, PDF, TXT, XLSX) | yes |
| Large file | 25,000+ rows | roster 44,115 rows (43,800 deduped) | yes |
| Distractors in metadata.json | 2+, none labelled by file name | 4 (DOC ADP, MSP call volume, SHA winter log, Comptroller overtime xlsx); names carry no label | yes |
| Distractors unused yet weighable | yes | unused by solution; scale/basis differ and tie to nothing. Weak on "answers a graded quantity arithmetically" (design note: ties to nothing) | yes, thin |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both present in golden/ | yes |
| Asks multi-dimensional with unit and rounding | yes | per-unit, per-title-quarter, per-title counts; prompt states nearest hour/dollar; the count ask has no stated rounding but is an integer | yes |
| Prompt shape, 25+ criteria | yes | prompt 867 chars; 8+8+16+4+ chart/reserve items clears 25 by count | yes |
| Not LLM generated, goldens real | yes | payroll has employee-days up to 40 OT hours (88 days over 16 h): reads generated | no, note |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, family analytical_non_defect, surface_read no, sole_data_defect no. Card/design note: stump_class analytical, estimand_identification (entry-cohort comparison group for the relief holder). Match. The declared distractors are not the surface read carrying the task. No mismatch. Design note default path numbers are stale against the rebuilt bundle (design note: 8,968 vacant hours and TWC 244.2 / PCS 201.5 / FFH 240.0 fifth-heaviest; judge recomputed 11,968, 232, 200, 232). Main thread should reconcile the note, since the golden's 59 agrees with both.

## Gate H
domain: pass, layers: pass, decisive_step: analytical (matched-cohort capacity estimate, fifth-heaviest week as sizing quantile). Matches design note's Three rules. Judge flags the 5th-week and vacancy rules as rule application but not the stump. The note concedes the estimation HOW is unfiled; the judge accepted the memo's population as the closure.

## Stump power (Gate F)
Judge: moderate trap; a strong model that joins academy_class to the rosters passes, many use the title average. Scored readers' result (from the main session): both filed 63, so the call stumped both; the asks were landed 28 of 28, so the ask layer carries no stump power and is to be re-sited. The method is textbook (matched cohort) but both strong readers missed it.

## Findings, ranked
1. Payroll: 682 exact-duplicate rows and implausible employee-days (up to 40 OT hours) read as generated and open a residual fork on asks 2 to 4. Fix in the planned payroll rebuild.
2. Asks carry no stump power (28 of 28 landed): re-site, per main session.
3. Design note default-path figures stale against the rebuilt bundle (11,968 vs 8,968 vacant hours; TWC/PCS/FFH fifth-heaviest weeks).
4. Step 4 and Critical Component 3 say "7.8 per cent overall" where the workings use title rates (CO 8.0, PCO 7.4, FSA 8.3, HMW 7.8); word as by-title rates. Moves no figure.
5. Title-average reading is licensed by "Hours are reckoned by title" unless the memo's holder population is applied; closure is one memo sentence.

## Next action for the author
Rebuild the payroll file without exact-duplicate or 40-hour employee-days and re-site the ask layer, keeping the 59 call, its goldens and the memo's holder sentence frozen; then re-run this check once.

## Round 2 re-judge (target.zip 50a788c5)

- **Verdict:** DETERMINISTIC (main call and all 8 + 16 + 4 supplementary figures reproduce from the bundle), with two residual literal-reader forks named below.
- **Disposition:** FIX_NOW. File two things in the prompt or data dictionary, with no change to data: (a) the unit of "worked at" is the unit that posted the work (offer log first, else work_location); (b) the relief holder's off-post rate is that of a first-year entry-class hire. No analytic surface changes; no rerun needed if the filing only restates the golden's estimand.
- **Why:** 59 of 60, 1 returned, is the only result under the memo's population ("filled from the July 2027 entry classes") with Budget Instruction 2024-07 read literally (2.4 drops FY2026 vacant lines, 2.3(b) carries the 14 FY2028 vacant lines in full, 3.2 fifth-heaviest week, 52 fiscal weeks). The weakest links are the relief-hours rate (3.3 says "reckoned by title", which a literal reader can take as the title average, 63) and the unit attribution of overtime hours (work_location vs offer log).
- **Evidence (recomputed):**
  - Rosters: 315 duplicate exports are identical in status, so latest-export dedupe is neutral. Vacant-line hours = 11,968 (matches). Week 53 (1 day) excluded.
  - Fifth-heaviest weekly need with the 14 vacant lines (days_off excluded, 8h per scheduled day before first_shift_on_post): ACF 280, FFH 232, HRC 304, KPG 208, OXG 344, PCN 192, PCS 200, TWC 232. Vacant-line weeks run 10 to 40 as stated.
  - July 2025 class off-post share by title: CO 8.08%, PCO 7.40%, FSA 8.27%, HMW 7.79% (overall about 7.8%); title averages CO 14.8%, PCO 11.9%, FSA 18.9%, HMW 14.6% (overall 14.5%). Relief hours/week about 36.8 to 37.0.
  - Complements: HRC 9 (8.27), ACF 8 (7.61), TWC 7 (6.31), PCN 6 (5.18), PCS 6 (5.40), FFH 7 (6.32), OXG 10 (9.33), KPG 6 (5.64) = 59, matches. Robust to the analog chosen: all FY2026 first-year hires (CO 10.0%, PCO 8.4%, FSA 9.4%, HMW 7.8%) and CO 2025-2/FSA 2025-2 only still give 59; robust to adding or not adding off-post for the new lines after their first shift. Title-average reading gives 63 (64 with new-line off-post), not 59.
  - OT hours (offer-log unit first, else work_location, SL-0410 = TWC; second payments counted once; CTE over 1.5, FSA CTE 1.0): ACF 8144, FFH 9216, HRC 7984, KPG 5019, OXG 5502, PCN 7616, PCS 5320, TWC 6824, all match. Using payroll work_location alone gives ACF 7932, HRC 8088, KPG 5079, OXG 5442, PCN 7592, PCS 5344, TWC 6932 (7 of 8 differ). In every one of the 747 mismatches work_location equals the employee's home_unit, supporting the offer-log reading, but the dictionary calls work_location "the timekeeping location of the line", so a literal reader can take it.
  - FSA 1:1 credit is not in the MOU (excerpts exclude FSA); it is derivable only from the offer log (CTE hours = post hours for all 96 matched FSA lines, 1.5 for all other titles).
  - Pay, 16 cells: all reproduce to the dollar (e.g. CO Q1 285,497; HMW Q1 159,711; FSA Q2 117,886). OTR hours equal the OT hours in the service period including second payments in all 2,164 lines, which forces the spread by OT work_date. Second payments are included in pay by "pay on the lines" and counted once in hours.
  - People over 600: CO 13, PCO 6, FSA 7, HMW 2 reproduce (28 persons). Entity resolution of 4 rehires via seniority_date plus separated record with same title is unique. Nearest non-qualifiers 588 and 564, nearest qualifiers 632 and 636. Counting second payments adds one person (E183564), so the once-only rule matters; FSA CTE at 1.5 would not change the count.
  - Open point: "July 2027 entry classes" does not map to academy_start dates in entry_class_calendar (CO 2027-2 enters 28 June and goes on post 18 October). The golden reads it as classes on post 1 July 2027 (the "2027-1" classes), analogous to the "2025-1" classes. Result is unchanged under other analogs.
- **Files/Hygiene:** PASS. 16 files; formats csv, pdf, xlsx, txt. Distractors present and relevant but unused (DOC ADP, MSP call volume, SHA winter log, Comptroller Table 7). Dates coherent (memo 9 Oct 2026, HR extract 1 Oct 2026, dictionary 23 Oct 2026). No authoring or benchmark disclosure found. The data dictionary is in-fiction. Nothing exclusion-level.
- **Stump power:** Moderate to good. A strong model that reads the standard literally and uses the title's average FY2026 off-post (the reconstruction the standard's "by title" invites) files 63 and a 3-position shortfall; one that keeps the FY2026 vacant lines in the need files 62. Rated medium rather than high because the cohort adjustment is a visible step once the memo's "July 2027 entry classes" is read.
- **Stumping type:** `mechanism: method_or_model_selection` (choosing the estimand, the new-hire cohort's off-post rate, over the title average), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. No reported figure is wrong; difficulty lives in which population's off-post rate the standard's "holder will be" calls for, with the standard's own figures correct.
- **Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. Domain: relief-factor workforce sizing (shift-relief complement sized at a tail week from leave and vacancy data) is the field's own analysis; swap test fails to reduce it to a backdrop. Layer 1: duplicate nightly exports, two timekeeping systems with different codes, a mid-year system migration, biweekly checks with a retro line, rehires under new IDs, cross-unit overtime. Layer 2: the relief holder's off-post rate as a first-year cohort. Easy route: title-average off-post, giving 63 (3 short). Caveat for the author: the "by title" wording lets a literal reader reach the easy route as a reading, not only as an analytical error.
- **Fix:** prompt (or data dictionary). (1) State the unit attribution for hours worked ("at the unit that posted the work"). (2) State that a relief position's holder is read as a first-year entry-class hire, or tie "by title" to the entry class explicitly; clarify "July 2027 entry classes" as the classes on post from 1 July 2027. (3) Optionally note that FSA overtime comp time is credited hour for hour (not in the MOU excerpts). The data and the golden figures stay unchanged.

Disposition taken: 3.3's "Hours are reckoned by title" removed (the grain is a same-call row, SF14); payroll's work_location renamed timekeeping_location and filed as the timekeeper that keyed the line. The suggested filing of the first-year rate was not taken: it would file the decisive step and make the call rule application. The FSA credit was left to the data (CTE hours equal the post hours on every matched aide line).

## Round 3 re-judge (target.zip 7c914942)

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE. Every committed answer reproduced from the bundle; no repair needed, no rerun.

**Why:** The standard (Budget Instruction 2024-07, 2.1 to 3.4), the Director's memo (positions filled from the July 2027 entry classes) and the position control pin the estimand. Read literally, they give 59 of 60 placed and 1 returned. The result does not move under the forks I tested, and each supplementary figure falls out of a single identity or placement rule the files support.

**Evidence (all recomputed with pandas from target/):**
- Rosters: kept the latest export of each shift_date, unit and line, mapped codes through timekeeping_status_codes.csv, and cut at fiscal weeks 1 to 52. Vacant-line hours total 11,968 (matches the claim). Off-post = leave, injury on duty and training.
- The 14 vacant FY2028 lines, using days_off and 8 hours a scheduled day before first_shift_on_post, add 0 to 3,568 hours per unit (KPG has none).
- Fifth-heaviest week per unit: HRC 304, ACF 280, TWC 232, PCN 192, PCS 200, FFH 232, OXG 344, KPG 208.
- Relief hours, from the July 2025-1 classes' FY2026 off-post share: CO 8.08%, PCO 7.40%, FSA 8.27%, HMW 7.79%. Pooled 7.86%. The units' holders run 14.51%.
- Complements: 9, 8, 7, 6, 6, 7, 10, 6 = 59 (matches).
- Forks tested, none moves the total:
  - by-title against pooled share: 59 in both;
  - all FY2026 entry classes: 59;
  - calendar against position-control first-shift date: 59;
  - adding the new holder's off-post share on the vacant lines: 59.
- What does move it: the title-average holder gives 63, the all-holder average 62, dropping the vacant lines 50, ignoring days_off 62, and a different cut rank 64 (4th), 56 (6th), 51 (7th). All of these depart from a stated rule (3.2, 1.1, 2.3(b)) or from the memo, so none is a defensible rival. Excluding training gives 56, but 2.3(a) names training as off post.
- FY2026 overtime hours, with exact duplicate-payment removal (employee, work date, start time, hours, earn code), FY2026 work dates, CTE divided by 1.5 (1.0 for FSA, whose own offer-log ratio is 1.0) and unit taken from the accepted offer-log post, else timekeeping_location (SL-0410 = TWC): HRC 7,984; ACF 8,144; TWC 6,824; PCN 7,616; PCS 5,320; FFH 9,216; OXG 5,502; KPG 5,019. All reproduce. Keying on timekeeping_location alone gives different numbers (ACF 7,932). The offer log is the only evidence of where the work was done; 747 accepted offers differ from the keyed location, and 99% of those are keyed to the worker's home unit.
- People: the four rehired records (seniority_date earlier than hire_date) each match exactly one separated record on seniority_date and title. Counting persons gives 66, 66, 62, 44, 44, 23, 38, 39 (reproduces). Counting employee_ids would give 66, 67, 63, 45, 45, 24, 39, 40.
- Over 600 hours by person and title: CO 13, PCO 6, FSA 7, HMW 2 (reproduces). Counting without the rehire join gives CO 12, PCO 5, FSA 6, HMW 1.

**Residual points, none disqualifying:**
- The CTE credit rule (1.5 under MOU 14.2, hour for hour for FSA outside the MOU) and the placement rule are inferences from files, not stated in the data dictionary.
- The July-2025-class off-post share rests on only 16 people. It is robust, since every cohort variant gives 59.

**Files/Hygiene:** PASS. There are 16 files, in csv, pdf, xlsx and txt. Rosters have 44,115 rows. Distractors are the ADP, MSP call-volume, SHA winter-log and expenditure files. Dates are coherent (extracts 1 Oct 2026, memo 9 Oct, dictionary 23 Oct). Roster duplicates, two timekeeping systems, a retro-pay lag, duplicate payments and rehire ids read as real system mess. I found no authoring or benchmark disclosure and nothing exclusion-level.

**Stump power (Gate F):** Moderate to good. The memo hands over the entry-class sentence, but the solver must turn it into a cohort-specific off-post rate; the easy route uses the title or all-holder average and files 63 or 62, short by 3 or 2. The vacant lines, the fifth-heaviest cut and the many supplementary devices (offer-log placement, rehire join, CTE credit, duplicate payments) add further failure surface. Lever if it proves too easy: none needed.

**Stumping type (Gate G):** mechanism: method_or_model_selection (estimand and cohort choice), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no. No reported figure is wrong, and the task still stumps on clean data via the cohort estimand. This passes Gate G.

**Three rules (Gate H):** domain: pass, layers: pass, decisive_step: analytical. The domain's own analysis (workforce relief-factor sizing from fifth-heaviest-week demand and a cohort-specific availability rate) decides the call. Layer 1 is the two timekeeping systems, duplicate exports and payments, and rehire ids. Layer 2 is estimating the relief holder's availability from the entry-class cohort. The easy route is the title-average holder at 14.5% off post, which gives 63 and a shortfall of 3. Borderline note: the memo does disclose the entry-class staffing, but turning that into the right rate is analysis, not a rule lookup.

**Fix:** none.

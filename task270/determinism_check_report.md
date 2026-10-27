# determinism-check report, task270, 2026-10-27

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: other (measurement-interval correction of a successive-difference statistic), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Process note: the runtime had no Agent tool, so the brief (/tmp/determinism-check-task270-164411/judge_brief.md) was spawned by the main session as one sonnet/medium thread. Its verdict is /tmp/determinism-check-task270-164411/verdict.md. One pass, no retry.

## Why
The funded set (Dunnerby, Marrowcombe, Drystow, Haddersley, Cressbeck) is forced by the committee paper's 30 per cent rule read with "as the collaborative's app will measure it", and the standard's 3-hourly schedule (2.1). The trust app's prompts sit about 90 minutes apart; the literal adjacent-prompt reading gives only two teams (the intended wrong route). The judge found the five teams stable under every three-hour emulation tried (pair windows 2 to 4, 2.75 to 3.25, 2.9 to 3.1, 1.5 to 4.5 h, skip-one, nearest-to-slot, root-2 scaling; Cressbeck lowest at .327, all other six at or below .21). All ask-2 figures reproduced.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Cohort | 578 | 578 (enrolments, register, episodes, v3/v4; 630 resent v4 rows dropped, UTC to London, v3 /10) | yes |
| Share at 2.0+, 2.5 to 3.5 h pairs | five teams at 30%+ | .492 .473 .472 .449 .446; others .04 to .12 | yes |
| Adjacent-prompt reading | wrong route, two teams | Dunnerby .492, Marrowcombe .436; Drystow .208, Haddersley .143, Cressbeck .102 | yes |
| Clinicians / WTE, 11 teams | 1/0.60 ... 6/4.92 ... | all 11 match | yes |
| Mean weeks, 11 teams | 31.4 ... 43.2 ... 30.0 | all 11 match; 87 on list, ack letter found for all 87 | yes |
| PTD-114 / EXT-0412 / PTD-301 mapping | DBT facilitation codes | derivable from annual report counts (6/10/11; 1/2/2) and learning records | yes |
| Chart (ask 3) | shares vs 30% line, five blue | determined by main call | yes |

## Competing answers that survived
No fork on the main call. Mild supplementary forks, each closed by a shipped rule and judged defensible:
- Referral date: module date_received (migrated referrals keyed later) gives 15.5 to 25.2 weeks; standard 2.2 makes the acknowledgement letter the receipt day. Closed by the standard and the prompt's "since the service received their referral".
- Latest acknowledgement for 13 patients with an earlier prior-referral letter: latest on or before the module date.
- Two removals effective 26 and 28 Dec but recorded 5 and 6 Jan: excluded under standard 3.1 (a record-as-of-31-Dec reading would include them).
- Estimator window (2.5 to 3.5 h) is not in a shipped file; the funded set does not move with it, so it is a method pin only.
- The v3 0 to 100 scale is inferred from "_vas" columns and the maximum of 100, not stated (soft, not a finding).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10+ / 3+ / 25,000+ rows | 17 / 4 (csv, xlsx, pdf, docx) / v4 export 45,318 rows | yes |
| Distractors | 2+ named in metadata.json, none labelled by file name | phq9_gad7_at_assessment_2026.csv, sallowdene_mood_app_pilot_evaluation_2025.pdf; names carry no label | yes |
| Distractor unused yet weighable; wrong-answer reproduction ruled out by a shipped fact | yes | judge: unused by the answer (pilot response rate and 6-minute lag do not feed it); I did not separately test whether PHQ-9/GAD-7 reproduces a graded quantity | yes (PHQ-9/GAD-7 arithmetic not independently tested) |
| Deliverables | 1 to 3, all in golden, no format family required | 2 (xlsx, png), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | ask 2 is 11 teams x 4 fields, one decimal and two decimals stated in the prompt | yes |
| Prompt shape, rubric 25+ criteria | shape identifiable, 25+ | shape 14 (cuts of a distribution per segment); 11 teams x 4 fields plus the set and chart comfortably support 25+; the rubric itself is generated downstream and was not inspected | yes (inferred) |
| Not LLM-looking; goldens read as work products | yes | judge found no authoring language or temporal contradictions; golden realism not re-read by me | yes (judge hygiene) |

## Gate G reconciliation
Judge: mechanism other, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: strategy `other` (interval dependence of a successive-difference index), Gate G `method_or_model_selection`, stump_class analytical, default path ends on Dunnerby and Marrowcombe, golden five. Match. No shipped artifact ranks the teams wrongly (no decoy memo); the declared distractors are not named by the judge as the surface read carrying the task. Gate G classification: method_or_model_selection / analytical_non_defect, no mismatch. The judge flags it as borderline against single_conceptual_flip (a lens change); it leaned pass because the adjustment comes from the data's structure.

Gate H: domain: pass, layers: pass, decisive_step: analytical. Matches the card's analyst_test and domain_test and the note's Three rules (Layer 1: version change, UTC, resent rows, previous employee numbers, course recode, team merger; Layer 2: reading instability at the collaborative's three-hour interval).

## Stump power (Gate F)
The easy route (apply 3.2 to the trust's adjacent prompts) gives two teams; cleaning everything correctly does not rescue it. Reaching the five requires noticing the schedule gap and that the successive-difference RMS grows with interval, then emulating three hours. Main-thread weighing points: (1) the "as the collaborative's app will measure it" wording in the paper is the only shipped pointer, so a strong solver who reads that line closely may land the call; (2) the estimator family is wide but all members agree, so the call is not a method lottery (design note ladder R3/R4); (3) supplementary asks add cost (PTD-114 recode, ack-letter dating, preceding employee numbers, late-recorded removals). Not a textbook route with no judgment: the data must settle the interval dependence.

## Findings, ranked
1. None blocking.
2. Optional pin: the 2.5 to 3.5 h pairing window or "ratings about three hours apart" is stated nowhere; the call is invariant to it. Note the repo rule files WHAT not HOW, so pinning the window would turn the decisive step toward rule application; recommend leaving it.
3. Borderline classification against single_conceptual_flip (see Gate G); the main thread weighs it against the note's ladder.
4. Mild supplementary forks above (late-recorded removals, latest-acknowledgement choice) are defensible and closed by the standard.

## Next action for the author
None required to pass this gate: proceed to the pre-ship check once the leak reader returns. Fixed nothing.

# AD50 — Which alerts feed next year's tutor call lists, when a third of withdrawals come from students no alert can flag

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Policy & Education · distance higher education |
| Mirrors | Customer-health and churn early warning where churn spreads through small groups that no per-account metric expresses (SaaS seats leaving with a departing champion, friend-group churn on Meta and Instagram, multiplayer game clans quitting together) |
| Decision shape | A structure the body adopts: the set of alert rules feeding tutors' weekly call lists, scored on the share of last year's withdrawals flagged at least two weeks ahead, never exceeding the 8% weekly call capacity |
| Committed call | The adopted alert rules and their settings, and the share of 2024 withdrawals the structure would have flagged in time, adopted by the student-success board in June |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · every screen is right and the answer is what nothing flags (students whose peer-review circle has just lost a member, a group grain built from the review graph), with a suppressed cell recovered exactly from a published total and bounded by worst-case allocation below it |
| Gate G mechanism | method_or_model_selection, with binding_constraint support |
| Measured traps engaged | #24 treats an unpublished figure as unknown · #7 uses the ready-made measure · #4 never tests its reading against the control |
| Calibration form | Change-log natural experiments: the course-design change log's 14 assessment-calendar changes (2019–2023), each with weekly activity before and after |
| Driving force | Every alert in use is right about the students it flags: low activity against the cohort, missed submissions, long absences. A third of 2024's withdrawals came from students none of them flags, because those students worked normally until they left, within three weeks of a member of their peer-review circle leaving. The circle is a group no file names (four students who review each other), recoverable only as components of the review-assignment graph, and once it is built the hazard is plain: 19% of remaining members leave within three weeks of a circle-mate, against 2% otherwise. |

## 1. Situation

A distance-learning university's student-success team calls students at risk of withdrawing. Tutors can call at most 8% of active
students in any week. Next year's call lists will be fed by a new set of alert rules, and the student-success policy scores any proposed set
on the share of the last full year's withdrawals (2024) it would have flagged at least two weeks before the withdrawal, without breaching
capacity in any week. The policy's equity rule bars any rule that flags students with a declared disability at more than 1.25 times their
share of active students. The team holds daily activity, assessment submissions, registrations and withdrawal dates, the peer-review tool's
assignment log, the course-design change log and the university's equality report; its extract suppresses the disability field in
module-presentations with fewer than five declarations. The head of tutoring trusts missed assessments above everything.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: clicks, ranks, submissions, withdrawal dates, the review assignments and the equality report. Each
  existing alert flags real disengagement, and the head of tutoring is right that missed assessments predict failure. Nothing is overturned;
  the difficulty is a population whose risk lives in a group no alert observes.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the current alert. A cohort-relative alert with missed assessments, equity checked by bounding,
  is still the natural build and still misses the circle withdrawals.
* **Instrument repair.** Record every click and submission perfectly: the students who leave after a circle-mate look the same as students
  who stay until they go. No better instrument of individual activity shows a group's loss.
* **Lens swap.** The naive population is students whose own behaviour flags them; the answer adds students flagged by what happened to their
  circle, a different set of students and a different structure.

## 3. The driving force

A strong solver drops absolute click counts (the change log shows calendar shifts swinging them across whole cohorts), ranks each student
within module, presentation and week, bounds the suppressed disability cells to clear the missed-assessment rule on equity, and tunes the
cohort-relative cut so the two rules fill capacity: 46% of withdrawals flagged in time. Every step is correct, and every rule looks at one
student's own record. The withdrawal file, read against the review-assignment log, shows the rest. The peer-review tool puts each student in a
circle of four who review each other's drafts all term; the log records only reviewer–reviewee pairs per assignment, so circles are
components of that graph. When a circle-mate withdraws, each remaining member's chance of leaving in the next three weeks rises from 2% to
19% and falls back after, and those students' activity never dips beforehand. A circle-loss rule flagging remaining members for three weeks
costs little capacity and catches what no individual rule can.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The current absolute alert (under 20 clicks in a week) | Structure: {absolute} | It is what tutors work from today | The change log: calendar changes pushed absolute flags to 31% of a cohort in assessment weeks, far over capacity, while cohort ranks stayed flat |
| 1 | Cohort-relative rank alone at the cut that fills capacity (rank below 14th percentile two weeks running); the missed-assessment rule left out because its equity cannot be checked where disability is suppressed | Structure: {cohort-relative 14}, 38% caught | The change log certifies cohort ranks, and only verifiable rules can be adopted | The equality report: each module has one suppressed presentation, so its declared total less the visible presentations gives that presentation's declared count exactly, and even with every declared student there flagged the missed-assessment rule's ratio is at most 1.12 |
| 2 | Cohort-relative and missed-assessment rules, cut retuned to fill capacity together | Structure: {cohort-relative 9, missed assessment}, 46% caught | Both strongest individual signals, equity-cleared, within capacity | The withdrawal file against the review log: 31% of withdrawals fell within three weeks of a circle-mate's, with no flag from any rule beforehand |
| 3 | **Decisive:** circles built as components of the review-assignment graph; remaining members flagged for three weeks after a circle-mate withdraws; the cohort cut retuned to fill what capacity remains | **Structure: {cohort-relative 7, circle loss}, 61% caught** | — | — |

* **Structure table.** Four different rule sets, and the circle-loss rule appears on no lower rung. Scores run 38%, 46% and 61%; the
  absolute rule is infeasible on capacity.
* **Separation.** The best structure without the circle-loss rule catches 46%; adding the rule while keeping missed assessments forces the
  cohort cut to 5 and catches 52%; the answer's two-rule set catches 61%, 1.17× the nearest alternative, because missed assessments mostly
  re-flag students the cohort rank already holds.
* **Partial correction priced (L3).** A solver who looks for group effects in tutor groups (a column) instead of review circles finds a weak
  clustering, adds a tutor-group-loss rule that flags twenty students per withdrawal, and adopts {cohort-relative 10, tutor-group loss} at
  41% caught: below rung 2, and 20 points under the answer. A solver who builds circles but keeps the missed-assessment rule adopts three
  rules at cut 5 and catches 52%, the answer's 61% being 1.17× that.
* **Grid.** Rule set (each subset of cohort-relative, missed assessment, circle loss, tutor-group loss) × equity handling (suppressed cells
  unknown or bounded) = 30 cells. Every set without circle loss scores 46% or less; with it, only the two-rule set at cut 7 reaches 61%.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The peer-review tool is documented as a teaching tool; no document mentions circles in connection with retention, and
   the assignment log has no circle field.
2. **Corpus blind for a computable reason.** *Every module in the change log ran without peer-review circles, because circles were introduced
   only in modules redesigned after the last logged calendar change.* The log certifies cohort-relative ranks against absolute counts (rung 1)
   and cannot show a group effect.
3. **No arithmetic symptom.** Every rule's weekly flags stay under 8%, the scores reconcile to the withdrawal file, and the circle withdrawals
   carry no missing data or odd activity.
4. **Not a row predicate.** Circles are components of a reviewer–reviewee graph per term; flags need each circle's withdrawal dates and a
   three-week window per remaining member, recomputed week by week against capacity.
5. **The enumeration is arithmetic.** Which students the circle rule flags in each week is computed; no column names a circle or a loss.
6. **No cutover date.** Circles reached modules gradually as each was redesigned; the 2024 contagion is a standing pattern within the year.
7. **Survives deletion.** Remove both voices and the absolute alert, and the two individual rules are still the natural build.

## 6. The calibration corpus

* **Form.** The course-design change log: 14 assessment-calendar changes in 2019–2023 presentations, with each module's weekly activity
  before and after.
* **What it certifies.** Calendar shifts move whole cohorts' clicks by up to 40% while within-cohort ranks barely move, so cohort-relative
  ranks are the right individual signal; a back-tester is confirmed at rungs 1 and 2.
* **What it is blind to.** Circles (above). The pin for the decisive rung is the policy's scoring clause on 2024 withdrawals, which the
  constructed rule meets exactly, with the hazard's three-week end visible as an empty fourth week.
* **Twin pair.** Tutor groups T-114 and T-207 in one module are identical on every alert's flag counts, activity distributions and
  submissions. T-114 lost 14 students and T-207 seven, 2.0× apart, because two of T-114's circles unravelled one member after another; only the
  circle construction separates them.
* **Resemblance points at the decoy.** 2024's activity profile resembles 2022's, the year the cohort and missed-assessment pair would have
  caught the most.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The student-success policy: a rule set is scored on the share of the last full year's withdrawals it flags at least two
  weeks ahead, never exceeding 8% of active students in any week; no rule may flag students with a declared disability at more than 1.25
  times their share. The equality report's suppression rule. One sentence each.
* **Empirical pins.** Cohort ranks, from the change log; the circle hazard and its three-week window, from the 2024 withdrawals.
* **Voices.** The head of tutoring: "Missed assessments are the best predictor we have; every tutor knows it." The data team lead:
  "Engagement against the cohort catches everyone who is drifting."
* **Licensed wrong basis.** The policy records that the academic board evaluates alerts by their precision against end-of-module failure and
  will review the structure on that basis.

## 8. Determinism by construction

* **Circles.** Every term's review graph splits into disjoint groups of four in which each member reviews the other three, so components and
  cliques give the same circles.
* **Window.** The hazard after a circle-mate's withdrawal is 19% in weeks one to three and back to 2% in week four, so two- to four-week windows
  pick the same structure and the scoring uses three.
* **Capacity.** The cohort cut is the largest whole percentile keeping every week under 8%, which is unique for each rule set.
* **Equity.** Every bounded suppressed cell leaves each adopted rule under 1.25 at the bound's upper end.

## 9. Prompt sketch and deliverables

> The board adopts next year's alert rules in June, and tutors can only call so many students a week. Our head of tutoring thinks missed
> assessments are all we really need. Tell me which rules we adopt and with what settings, and what share of last year's withdrawals that set
> would have caught at least two weeks ahead, to the nearest per cent, in a paragraph for the board. Send `alert_structure.xlsx`, a chart
> `caught_in_time.png`, and a one-page `board_note.pdf`.

* `alert_structure.xlsx` — each rung's rule set with its weekly flag shares and score (ask C), the call-log sheet (ask A) and the forum sheet
  (ask B).
* `caught_in_time.png` — weekly flags as a share of active students for each rung's rule set, the 8% capacity line drawn and labelled, the
  share of withdrawals caught in time annotated for each set, and the circle-loss flags shaded in the adopted set.
* `board_note.pdf` — the committed structure and score, and why each other structure falls short.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of six faculties, tutor calls attempted and connected per week last year and the mean
  connected-call length. *Device:* softphone calls record durations in seconds and the legacy desk phones in minutes, as the contact guide
  says; averaging raw values misstates four faculties. The structure never uses the call log.
* **Ask B (device-carried).** For each of the 22 module-presentations, forum posts per active student per week. *Device:* an edited post is
  logged again with an edit flag, and the forum guide counts the original only; counting rows inflates nine modules. The circle construction
  uses the review-assignment log, never the forum.
* **Ask C (validity).** Each rung's rule set: its score and its highest weekly flag share.
* **Decoupling.** Clearing the circle construction and the equity bound changes no figure in asks A or B.

## 11. Rubric arithmetic

6 faculties × 2 (ask A) + 22 module-presentations (ask B) + 4 rule sets × 2 (ask C) + the committed rules, the cohort cut, the circle window
and the score + 5 named chart parts + 3 files ≈ 54 criteria.

## 12. World-building constraints

* Scores 38% / 46% / 61%; the three-rule set at cut 5 scores 52%; the tutor-group variant 41%. Absolute flags reach 31% in assessment weeks.
* 31% of 2024 withdrawals fall within three weeks of a circle-mate's, with no prior flag; circle hazard 19% for three weeks, 2% otherwise.
* Each module has exactly one suppressed presentation, recovered exactly from the module's declared total; with every declared student there
  flagged, the missed-assessment rule's ratio is at most 1.12.
* T-114 and T-207 are identical on every alert, activity and submission column.
* Call logs and forum posts never touch activity, submissions, withdrawals or the review log.

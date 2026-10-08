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
on the share of the last full year's withdrawals (2024) whose student it would have had on a call list two weeks before the withdrawal,
without breaching capacity in any week. The policy's equity rule bars any rule that flags students with a declared disability at more than
1.25 times their share of active students. The team holds daily activity, assessment submissions, registrations and withdrawal dates, the
peer-review tool's assignment log, the course-design change log and the university's equality report; its extract suppresses the
disability field in module-presentations with fewer than five declarations. The head of tutoring trusts missed assessments above everything.

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
cohort-relative cut so the two rules fill capacity: 40% of withdrawals flagged in time. Every step is correct, and every rule looks at one
student's own record. The withdrawal file, read against the review-assignment log, shows the rest. The peer-review tool puts each student in a
circle of four who review each other's drafts all term; the log records only reviewer–reviewee pairs per assignment, so circles are
components of that graph. When a circle-mate withdraws, each remaining member's chance of leaving in the next three weeks rises from 2% to
19% and falls back after, and those students' activity never dips beforehand. A circle-loss rule flagging remaining members for the two weeks
after a circle-mate leaves catches what no individual rule can. It needs the room missed assessments take in the weeks after each
deadline, so the structure trades that rule for this one and retunes the cohort cut to what is left.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The current absolute alert (under 20 clicks in a week) | Structure: {absolute} | It is what tutors work from today | The change log: calendar changes pushed absolute flags to 31% of a cohort in assessment weeks, far over capacity, while cohort ranks stayed flat |
| 1 | Cohort-relative rank alone at the cut that fills capacity (rank below 14th percentile two weeks running); the missed-assessment rule left out because its equity cannot be checked where disability is suppressed | Structure: {cohort-relative 14}, 36% caught | The change log certifies cohort ranks, and only verifiable rules can be adopted | The equality report: each module has one suppressed presentation, so its declared total less the visible presentations gives that presentation's declared count exactly, and even with every declared student there flagged the missed-assessment rule's ratio is at most 1.12 |
| 2 | Cohort-relative and missed-assessment rules, cut retuned to fill capacity together | Structure: {cohort-relative 9, missed assessment}, 40% caught | Both strongest individual signals, equity-cleared, within capacity | The withdrawal file against the review log: 36% of withdrawals fell within three weeks of a circle-mate's, 31 points of them two weeks or more after it, with no flag from any rule beforehand |
| 3 | **Decisive:** circles built as components of the review-assignment graph; remaining members flagged for the two weeks after a circle-mate withdraws; the cohort cut retuned to fill what capacity remains | **Structure: {cohort-relative 7, circle loss}, 61% caught** | — | — |

* **Structure table.** Four different rule sets, and the circle-loss rule appears on no lower rung. Scores run 36%, 40% and 61%; the
  absolute rule is infeasible on capacity.
* **Separation.** The best structure without the circle-loss rule is rung 2's, at 40%. Circle loss cannot join missed assessments: in the two
  weeks after each deadline they flag 3.2% and 5.1% of active students, so any set holding both breaches 8% before a single cohort flag.
  Circle loss alone catches 31%; with the cohort cut at 7 it catches 61%, 1.53× the best feasible alternative and 21 points clear of it.
* **Partial correction priced (L3).** A solver who looks for group effects in tutor groups (a column) instead of review circles sees a
  group's three-week risk rise from 2% to 4.7% after a withdrawal, but flagging whole groups is far over capacity, so the affordable rule
  flags each group's three lowest-ranked remaining members for two weeks. Those are students the cohort rank already holds, and
  {cohort-relative 4, tutor-group loss} catches 22%, 39 points under the answer. A solver who builds circles but keeps missed assessments as
  the head of tutoring's fixed rule finds no feasible set holding both and stays on rung 2's {cohort-relative 9, missed assessment} at 40%;
  the answer's 61% is 1.53× that.
* **Grid.** Rule set (each non-empty subset of cohort-relative, missed assessment, circle loss and tutor-group loss) × equity handling
  (suppressed cells unknown or bounded) = 30 cells. Every set holding two of missed assessment, circle loss and tutor-group loss breaches 8%
  in the weeks after a deadline. Feasible sets without circle loss score at most 40% (rung 2's pair, and only with the equity bound; 36%
  without it); circle loss alone scores 31%; only {cohort-relative 7, circle loss} reaches 61%, 1.53× the best feasible alternative.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The peer-review tool is documented as a teaching tool; no document mentions circles in connection with retention, and
   the assignment log has no circle field.
2. **Corpus blind for a computable reason.** *Every module in the change log ran without peer-review circles, because circles were introduced
   only in modules redesigned after the last logged calendar change.* The log certifies cohort-relative ranks against absolute counts (rung 1)
   and cannot show a group effect.
3. **No arithmetic symptom.** Every rule's weekly flags stay under 8%, the scores reconcile to the withdrawal file, and the circle withdrawals
   carry no missing data or odd activity.
4. **Not a row predicate.** Circles are components of a reviewer–reviewee graph per term; flags need each circle's withdrawal dates and a
   two-week flag per remaining member, recomputed week by week against capacity.
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

* **Filed pins.** The student-success policy: a rule set is scored on the share of the last full year's withdrawals whose student was on a
  call list two weeks before the withdrawal, never exceeding 8% of active students in any week; no rule may flag students with a declared
  disability at more than 1.25 times their share. The equality report's suppression rule. One sentence each.
* **Empirical pins.** Cohort ranks, from the change log; the circle hazard and its three-week span, from the 2024 withdrawals.
* **Voices.** The head of tutoring: "Missed assessments are the best predictor we have; every tutor knows it." The data team lead:
  "Engagement against the cohort catches everyone who is drifting."
* **Licensed wrong basis.** The policy records that the academic board evaluates alerts by their precision against end-of-module failure and
  will review the structure on that basis.

## 8. Determinism by construction

* **Circles.** Every term's review graph splits into disjoint groups of four in which each member reviews the other three, so components and
  cliques give the same circles.
* **Window.** The hazard after a circle-mate's withdrawal is 19% over weeks one to three and back to 2% in week four, and 31 of the 36
  points of circle withdrawals fall in weeks two and three. A flag raised at the circle-mate's withdrawal and held two weeks is on the list
  two weeks before every one of them; a one-week flag misses the third-week leavers and a longer flag spends capacity that catches nothing
  more, so the score peaks at two weeks and the first-week leavers are out of every structure's reach.
* **Capacity.** The cohort cut is the largest whole percentile keeping every week under 8%, which is unique for each rule set.
* **Equity.** Every bounded suppressed cell leaves each adopted rule under 1.25 at the bound's upper end. Only the missed-assessment rule's
  flags gather in the small, suppressed presentations; the cohort and circle rules clear 1.25 on visible presentations alone.

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

* Scores 36% / 40% / 61%, the answer 1.53× rung 2; circle loss alone 31%; the tutor-group variant 22%. Absolute flags reach 31% in assessment
  weeks.
* Cohort-relative catches: cut 4 19%, cut 7 30%, cut 9 32%, cut 14 36%; missed assessments add 8 points at cut 9; circle loss adds 31 points
  with no overlap; tutor-group loss adds 3.
* Peak weekly flags in the two weeks after each deadline: missed assessments 5.1%, tutor-group loss 5.4%, circle loss 3.2% of active students.
  The binding cohort cuts are 14 alone, 9 with missed assessments, 7 with circle loss and 4 with tutor-group loss; any two of the three
  other rules together exceed 8%.
* 36% of 2024 withdrawals fall within three weeks of a circle-mate's with no prior flag, 31 points of them in weeks two and three; circle
  hazard 19% for three weeks, 2% otherwise; the circle flag runs two weeks; a tutor group's three-week risk after a withdrawal 4.7%.
* Each module has exactly one suppressed presentation, recovered exactly from the module's declared total; with every declared student there
  flagged, the missed-assessment rule's ratio is at most 1.12.
* T-114 and T-207 are identical on every alert, activity and submission column.
* Call logs and forum posts never touch activity, submissions, withdrawals or the review log.

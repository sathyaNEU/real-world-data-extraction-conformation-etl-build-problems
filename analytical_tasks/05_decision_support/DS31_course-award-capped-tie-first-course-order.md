# DS31 — Which finalist takes the year's homepage slot, when three of them sit tied at the award's ceiling

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Product Analytics · ratings calibration and featured placement |
| Mirrors | Featured placement decided among items whose capped scores tie at the top (app-store and course-marketplace editors' picks, Uber and Airbnb rating inflation at 4.9–5.0, performance-review calibration where several reports reach the top box), where a borrowed sort order quietly makes the call |
| Decision shape | Which of N gets one scarce thing: the homepage Course of the Year slot for twelve months, among eight finalists |
| Committed call | The winning course, and the score that orders the tie: its calibrated rating among the learners for whom it was their first course, as a lead over the catalogue median in stars to two decimals |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · Pattern B behind a saturated tie (E21: the award score is capped at 5.00, and calibration stacks three finalists there), with the quiet second trap (E15) at rung 1 |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #19 breaks a big tie instead of questioning it · #1 reports a failed back-test, ships anyway · #11 beats the headline trap, misses the quiet one |
| Calibration form | Published control set with a reproduction clause: last year's award table, 60 courses with calibrated scores and published places, nine of them tied at the cap, which the award rules make the test of any method |
| Driving force | The award caps scores at 5.00, so once leniency is calibrated three finalists tie at the ceiling and the catalogue's sort order (completions) hands the slot to the biggest course. Last year's table had nine courses at the cap, and their published places follow no column. They follow one construction: each tied course's calibrated rating among learners for whom it was their first course on the platform, a group-and-rank over the whole enrolment history. |

## 1. Situation

An online learning platform gives one homepage slot for a year to its Course of the Year, chosen from eight finalists (A–H) on calibrated
learner ratings. Every learner rates the same five onboarding modules at sign-up, and the ratings handbook measures each learner's leniency
against them and shrinks course scores toward the catalogue. The award rules cap the score at 5.00 and make last year's published table,
scores and places, the test of any method. The head of content believes completions are the truest vote.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the ratings export, the anchors, completions, the enrolment history and last year's table. No
  stakeholder read is overturned. The biggest course really does have the most completions and a perfect capped score. The difficulty is
  what orders a tie the cap creates.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the head of content's view and the partner council's raw table. Calibration still stacks three finalists at
  the cap, and the catalogue's own sort order still names C.
* **Instrument repair.** Give every learner a perfect, unbiased rating instrument. The cap is the award's, not the scale's, so C, D and E
  still score 5.00, and the tie still has to be ordered the way the published table orders ties. No better measurement supplies the order.
* **Lens swap.** The tie-break and the answer differ in population: every completer of the course against the learners for whom it was
  their first course on the platform, a group that exists only through the enrolment history.

## 3. The driving force

A strong solver discards raw averages, removes the duplicates the quiet trap plants, calibrates each learner against the anchors as the
handbook says, shrinks, and applies the award's cap. C, D and E then all score 5.00. The handbook is silent on ties, so the solver borrows
the catalogue's sort order, which breaks equal scores by completions, and names C. Every step is defensible. But the award rules make last
year's table the test, and that table holds nine courses at the cap in published places that completions get right for two of the nine.
Raw means, rating counts and the uncapped calibrated score do no better than six. One construction places all nine: rank each learner's
enrolments by start date, keep the learners for whom the tied course came first, and order the tied courses by their calibrated rating
among those learners. Applied this year, it puts E first by a wide margin. C's ceiling was reached by learners who arrived from its
enterprise programme having taken other courses first.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Raw mean rating, shrunk toward the catalogue, as a lead over the catalogue median | A, a data-engineering course (0.61 against B's 0.50) | The storefront's own figure, stabilised for size | The ratings handbook: scores are calibrated for each learner's leniency against the five anchor modules |
| 1 | Handbook calibration on the ratings export, shrunk, capped at 5.00 | B, a cloud-certification course (0.88 against C's 0.72) | The loud trap is beaten: raters' generosity is removed by the platform's own method | The ratings guide: the legacy app and the sync service both log each legacy-app rating, de-duplicated on learner, course and day. B's fives are 31% duplicates |
| 2 | Duplicates removed, then calibration; C, D and E tie at the cap, ordered by the catalogue's sort rule (more completions) | C, the platform's largest course (41,000 completions against D's 26,000) | Clean data, the documented method, and the platform's own rule for equal scores | Last year's table: ordering its nine capped courses by completions puts two of the nine in their published places |
| 3 | **Decisive:** order the tied courses by calibrated rating among learners for whom the course was their first on the platform, the construction that places all nine | **E, a UX-research course, first-course lead 0.78** (5th of eight on rung 0) | — | — |

* **Position table.** E is 5th on rung 0 (0.38), 4th on rung 1 (0.60), and on rung 2 tied at the cap and third on completions (12,000).
  It is never second and leads only rung 3. Rung margins: A over B 1.22×, B over C 1.22×, C over D on completions 1.58×, E over D on the
  first-course score 1.53× (0.78 against 0.51).
* **Discriminator dominance.** C carries a 1.58× completions advantage into rung 3. On the first-course score E stands at 3.5× C (0.78
  against 0.22), more than 1.2 × 1.58 = 1.90.
* **Partial correction priced (L3).** A solver who distrusts the sort order and breaks the tie on the uncapped calibrated score over all
  raters places six of last year's nine and names D (5.21 against E's 5.12 uncapped). One who keeps first-course learners but leaves them
  uncalibrated places five and names C. Half the construction lands on a wrong course.
* **Grid.** Duplicates (kept, removed) × tie order (completions, uncapped all-rater score, first-course score) × calibration of the
  tie-break population (raw, calibrated) = 12 cells; duplicates kept name B in every cell. With duplicates removed the cells name C or D,
  except the one cell with the calibrated first-course score, which names E. The nearest wrong cell is D, one choice of population away.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The handbook defines leniency, shrinkage and nothing about ties; the award rules set the cap and the test. Only
   the catalogue's product notes mention an order for equal scores, and it is the wrong one.
2. **The control pins it, as a construction.** The first-course score places 9 of 9 capped courses and reproduces all 51 uncapped scores.
   The best rival, the uncapped all-rater score, places 6; completions place 2. A first-course population exists in no column: it needs
   every learner's enrolments ranked by start date, so no menu of course attributes contains it.
3. **No arithmetic symptom.** Counts reconcile to the storefront once duplicates go, shrinkage weights sum, and a capped 5.00 is a legal
   score. The rung-2 order fails only when the table's places are checked one by one.
4. **Not a row predicate.** First-course status is a rank inside a learner's enrolment history; the score then pools calibrated ratings
   across those learners, each calibrated against that learner's own anchors.
5. **The enumeration is arithmetic.** Which learners are first-course learners, and which tied course leads among them, is computed.
6. **No cutover date.** The ratings and enrolments span one award year, and no series steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, the catalogue's sort order still decides the tie.

## 6. The calibration corpus

* **Form.** Last year's award table: 60 courses with calibrated scores to two decimals and published places, the catalogue median, and the
  ratings, anchors and enrolment records behind them. The award rules: a method may be used only if it reproduces every published score and
  place.
* **What it pins.** The handbook's calibration with duplicates removed (51 of 51 uncapped scores) and the first-course order for the nine
  capped courses (9 of 9).
* **Twin pair.** Two courses tied at the cap last year are identical on every course-level column: completions within 1%, 3,100 ratings, the
  same category, raw mean 4.74 and the same anchor mean among their raters. They were published 2nd and 8th; their first-course leads are
  0.81 and 0.40 (2.0×). Most of the second course's learners came to it after other courses.
* **Resemblance points at the decoy.** By size, category and completions, C most resembles last year's winner.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The award rules: one homepage slot for twelve months to the highest-scoring finalist; scores capped at 5.00; a method may
  be used only if it reproduces every score and place in last year's published table. The handbook: leniency is a learner's anchor mean
  less the mean over all learners, and course scores shrink toward the catalogue mean with weight 25. The ratings guide: duplicates are
  removed on learner, course and day. One sentence each.
* **Empirical pins.** The tie order, from the published places.
* **Voices.** The head of content: "Completions are the truest vote, and the biggest course has earned it." The data-science lead: "Once
  leniency is out, the scores speak for themselves." The catalogue product manager: "Equal scores have always sorted by completions on our
  pages."
* **Licensed wrong basis.** The award rules record that the instructor-partner council publishes its own table on raw average rating and
  will set it beside the announcement.

## 8. Determinism by construction

* **First course.** A learner's first course is their earliest enrolment start. No learner has two starts on the same day, and bundle
  purchases create enrolments only when each course is started.
* **Sample.** Every finalist has at least 800 first-course learners with ratings, and every capped course last year at least 600.
* **Calibration of the tie score.** First-course learners are calibrated against their own anchors exactly as all learners are, and the tie
  score is uncapped; the published places pin both, since raw and capped variants misplace at least four of the nine.
* **Rounding.** E's first-course lead is 0.783 and D's 0.512; no finalist sits within 0.005 of a rounding edge.

## 9. Prompt sketch and deliverables

> Our Course of the Year takes the homepage for twelve months, and the eight finalists are in. The head of content thinks the course with
> the most completions has earned it. Name the winner, with the score that settles it in stars to two decimals, as the line for the
> announcement. Send `award_scores.csv`, a chart `ceiling_tie.svg`, and a short `award_decision.md`.

* `award_scores.csv` — the eight finalists under each of the four rung constructions with last year's hit counts (ask C), plus the refund
  rows (ask A) and the monthly learner rows (ask B).
* `ceiling_tie.svg` — the eight finalists' capped scores as bars with the 5.00 cap drawn, and for the three at the cap a second panel of
  their completions and first-course leads side by side, with last year's nine capped courses in published order as a reference strip and
  the winner marked.
* `award_decision.md` — the committed course and score, and why completions do not order the tie.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the eight finalists, refunds requested in the first 30 days and the refund rate.
  *Device:* bundle purchases post one payment, and a bundle refund posts one negative line that the bundle allocation table spreads over
  its courses, as the payments guide documents. Charging each refund line to the first course in the bundle misplaces refunds in five
  finalists.
* **Ask B (device-carried).** For each month of last year, the number of learners on a paid plan. *Device:* a family plan has one payer
  row in the subscription table and up to four learner profiles in the profile table. Counting payers undercounts learners every month, by
  a share that grows after the family plan's spring launch.
* **Ask C (validity).** For each of the four rung constructions, the places it gives last year's nine capped courses (hits out of 9) and
  its ordering of this year's eight finalists.
* **Decoupling.** Clearing the first-course construction changes no figure in asks A or B. Payments and subscriptions touch no rating,
  anchor or enrolment-start record.

## 11. Rubric arithmetic

8 finalists × 2 (ask A) + 12 months (ask B) + 4 hit counts + 8 finalists × 4 constructions (ask C) + the committed course, its tie score,
the runner-up and the margin + 5 named chart parts + 3 files ≈ 76 criteria.

## 12. World-building constraints

* Rung 0 leads: A 0.61, B 0.50, F 0.47, C 0.44, E 0.38, D 0.35, G 0.30, H 0.22. Rung 1: B 0.88, C 0.72, D 0.66, E 0.60. Rung 2: C, D and E
  capped at 5.00 (lead 0.90); completions C 41,000, D 26,000, E 12,000; B 0.70. Rung 3 first-course leads: E 0.78, D 0.51, C 0.22.
  Uncapped all-rater scores: D 5.21, E 5.12, C 5.08.
* B's legacy-app fives are 31% duplicates; no duplicate falls on C, D or E. C's learners mostly arrive through its enterprise programme after
  other courses.
* Last year's table: 60 courses, nine at the cap; places reproduced 9 / 6 / 5 / 2 by the first-course, uncapped all-rater, raw first-course
  and completions orders. The twin courses match on every course-level column.
* Rung leaders A, B, C, E. Bundle refunds and family profiles touch no rating or enrolment record.

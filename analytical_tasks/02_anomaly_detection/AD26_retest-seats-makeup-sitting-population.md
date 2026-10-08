# AD26 — How many supervised retest seats to book for June, when the irregular sittings are the ones no classroom owns

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Policy & Education · assessment integrity |
| Mirrors | Integrity screens whose unit is the occasion rather than the account a result is filed under (online-proctored certification exams at Google, Microsoft and Amazon, where an irregular session is filed under each candidate's own profile; payment-fraud teams screening a terminal-day instead of the merchant account) |
| Decision shape | One figure committed at a date: the number of supervised retest seats booked for the June window |
| Committed call | The number of students the department books into the June supervised retest, filed with the testing contractor by 20 May |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · the population a field suggests (the October classroom stands in for the sitting), with Pattern B for the referral standard recovered from the audited sittings and Pattern D (school-grade means against matched-student gains) below it |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #5 takes the population a flag or filter suggests · #4 never tests its reading against the control · #2 counts file rows instead of the real unit |
| Calibration form | Gold-standard verification subsample: 520 sittings drawn at random from the 2025 administration and audited on site, each with a determination |
| Driving force | Every result carries the student's October classroom, and every screen groups on it. A result is produced in a sitting: one administrator, one room, one day. For 92% of students the two coincide. The 8% absent on the main day test later in make-up sittings that one coordinator runs per school, drawn from many classrooms in ones and twos, so an irregular make-up sitting moves no classroom statistic. It appears only when results are regrouped into sittings through each answer document's scan date and envelope number. |

## 1. Situation

The state department of education's assessment office ran the spring 2026 grade 3–8 paper maths test: 412,000 results from 1,420
schools and 17,800 classrooms. The integrity regulation withholds every result produced under an administration that meets the
department's referral standard, and each affected student is offered one supervised retest in June. The testing contractor needs a firm
seat count by 20 May. A seat costs $38 booked and $210 if added in June, and a student turned away becomes an appeal. The vendor's gain-flag
file marks 640 classrooms, and the director of assessment wants to book on it.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct: the vendor's flags measure what they say (school-grade year-over-year gains), the
  rosters are the October rosters, and the audited determinations are right. No stakeholder read is overturned. The difficulty is which
  students sat a referred administration, a population no file is keyed on.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the director's preference and the vendor's flag file. A competent screen built from the score file still groups
  on classroom, still reproduces every audit, and still books the wrong number.
* **Instrument repair.** Suspect files: the audited sittings, filtered to main-window sittings because audit teams leave before any make-up
  is held, and the October rosters, stale by May. Audit make-up sittings too and roster every result to its May classroom: rung 0 still
  books 15,400, rung 1 9,900 and rung 2 7,200, each within 1%, because each counts classrooms; the audited make-ups now break rung 2's 520
  of 520 instead of certifying it, and the regroup into sittings is still needed to find the 84 referred make-ups among 2,600. The score
  file's classroom is a correct record of a different thing, the roster group, and no file records the sitting a result came from.
* **Lens swap.** The naive figure counts students on the rosters of referred classrooms; the answer counts students who sat referred
  sittings. The two populations differ in both directions (absentees leave, make-up testers arrive), not only in lens.

## 3. The driving force

A strong solver replaces the vendor's school-grade gain with each student's gain on their own 2025 score, recovers the department's
two-part standard (implausible matched gains and heavy wrong-to-right erasure) from the audited sittings, and gets 520 of 520. Every step
is correct, and every step groups results by classroom, because the score file, the vendor file and the dashboards all key on it. But the
regulation acts on administrations, and an administration is a sitting. Students absent on the main day sit a make-up days later, run by
the school's test coordinator, alongside absentees from every other classroom in the grade. Make-up sittings are where the department's
audit teams have never been. In 84 of them the standard fires at sitting grain, and at classroom grain each contributes one to three
students to a classroom of 24 and moves nothing. Seeing them means joining each answer document's scan date and envelope number to the
sitting register and screening the sittings that result.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Students on the rosters of the 640 classrooms the vendor flags (school-grade year-over-year mean gain beyond its 2.0 SD line) | 15,400 seats, +86% | The vendor's list is the department's long-standing referral list, and roster counts tie to enrolment | The audited sittings: the vendor flag reproduces 361 of 520 determinations, its misses concentrated in high-mobility schools |
| 1 | Pattern D: rescreen classrooms on matched-student gains (each student against their own 2025 score) at the vendor's line: 410 classrooms | 9,900, +19% | The textbook cohort correction; both grains are flawless and this one compares the same children | The audited sittings: 447 of 520; every miss is a classroom with high gains and ordinary erasure |
| 2 | Department standard recovered from the audited sittings (matched residual at or above 2.1 SD and wrong-to-right erasure index at or above 3.0), at classroom grain: 300 classrooms | 7,200, −13% | Reproduces 520 of 520 audited determinations | Scan dates and envelope numbers place 8% of results in make-up sittings that no classroom statistic can see |
| 3 | **Decisive:** regroup results into sittings (scan date and envelope to the sitting register), apply the recovered standard to every sitting, and count the students who sat a referred one | **8,300** | — | — |

* **Figure shape.** Rungs 0 to 2 walk the figure down (−36%, then −27%), and the decisive move turns it back up by 15%. A solver stopping
  anywhere short is wrong by a stated amount in a known direction.
* **Partial correction priced (L3).** A solver who notices that some roster students tested on a later date and drops them from their
  referred classrooms, without screening the make-up sittings, books 6,620: 20% below the answer and further from it than rung 2. Adding
  referred make-up sittings while keeping full classroom rosters counts 40 students twice, so that route breaks a distinct-student check
  and discloses itself.
* **Grid.** Gain grain (school-grade or matched) × rule (vendor line or recovered standard) × population (roster or sitting) = 8 cells:
  15,400 / 9,900 / 10,600 / 7,200 on rosters and 16,900 / 11,200 / 11,900 / 8,300 on sittings. The nearest wrong cell is rung 2, 13% away,
  and every other cell is at least 19% away.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The security manual's glossary defines an administration as the giving of the test to a group of students by one
   test administrator on one day. No document mentions make-up sittings in connection with referral, and the sitting register is filed
   as a materials-accountability log.
2. **Corpus blind for a computable reason.** *In every audited sitting the classroom statistic and the sitting statistic differ by at most
   0.11 SD, inside the empty gap, because the 2025 audit teams observe main-window classroom sittings on the day and leave before any
   make-up sitting is held.* Both groupings reproduce 520 of 520, so the back-test certifies rung 2 and cannot see rung 3.
3. **No arithmetic symptom.** Every result has one classroom, one scan record and one envelope; rosters tie to enrolment, envelopes tie to
   the sitting register, and every count reconciles under both groupings.
4. **Not a row predicate.** It needs a two-hop join (scan record to envelope to sitting), a regroup of 412,000 results into 20,400
   sittings, a sitting-level residual and erasure index, and the recovered two-key standard applied to each group.
5. **The enumeration is arithmetic.** Which make-up sittings are referred is computed; no column marks a sitting as a make-up, let alone as
   irregular.
6. **No cutover date.** Make-up sittings happen every year in every school; no series steps.
7. **Survives deletion.** Remove every voice and the vendor file: the roster-grain screen remains the natural build and remains wrong.

## 6. The calibration corpus

* **Form.** 520 sittings drawn at random from the 2025 administration and audited on site (seat charts, envelope seals, administrator
  interviews), each with a determination: 64 confirmed irregular, 456 cleared.
* **What it pins (Pattern B).** The recovered standard reproduces 520 of 520. The vendor's year-over-year flag reproduces 361 (159 cleared
  sittings referred) and matched gains alone reproduce 447 (73 cleared sittings referred). Both rivals miss in one direction, referring
  223 and 137 sittings against 64, so neither reconciles on the total either.
* **The absolute split (O2).** Every confirmed sitting has a matched residual of at least 2.1 SD and an erasure index of at least 3.0; every
  cleared sitting falls below 1.5 on at least one of them; no audited sitting lies between, so any cut-offs inside the gaps refer the same
  sittings.
* **Every rule exercised.** 41 cleared sittings have high residuals and ordinary erasure (a new teacher's genuine gains) and 23 have heavy
  erasure and ordinary residuals (a class told to check its work), so each key of the standard is tested.
* **What it is blind to.** Make-up sittings (above).
* **Twin pair.** Corrie Lane and Hatherley elementary schools are identical on enrolment, classrooms, vendor flags, classroom-grain
  referrals (one grade-5 classroom each, 24 on the roster, two absent) and make-up share. Corrie Lane books 22 seats and Hatherley 44,
  because Hatherley's grades 3–5 make-up sitting, 22 absentees from eleven classrooms, meets the standard. Only the sitting regroup
  separates them.
* **Resemblance points at the decoy.** The 2026 referral profile at classroom grain closely matches 2025's, the year the classroom-grain
  standard reproduced every audit.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The integrity regulation: a result produced under an administration that meets the referral standard is withheld and
  the student offered one supervised retest in June. The security manual: the referral standard in words (gains implausible against each
  student's own prior attainment, with heavy wrong-to-right erasure), the glossary definition of an administration, and the audited
  sittings as the department's record of determinations. One sentence each.
* **Empirical pins.** The two cut-offs, from the absolute split in the audited sittings.
* **Voices.** The director of assessment: "The vendor's flags have caught every case we have ever confirmed." A regional superintendent:
  "Erasures are the only evidence that has ever held up at a hearing."
* **Licensed wrong basis.** The security manual records that the testing contractor refers on the classroom year-over-year gain flag as
  its national standard and will present its list at the results meeting.

## 8. Determinism by construction

* **Cut-offs.** The audited gaps (1.5 to 2.1 SD on the residual, 1.5 to 3.0 on the erasure index) are empty in 2026 too, at both classroom
  and sitting grain, so no cut-off choice inside them moves a referral.
* **Make-up identification.** Every make-up sitting has its own envelope and its own register row dated after the school's main window,
  and scan date and envelope agree for every result, so either route assigns the same sitting.
* **Seats.** Maths is one sitting per student and no student sat two make-ups, so students and seats are the same count. The regulation
  offers a seat to every affected student, so enrolment in June is not a fork.
* **Rounding.** The committed figure is booked to the nearest ten and the answer sits mid-bin.

## 9. Prompt sketch and deliverables

> I have to give the contractor a firm number of June retest seats by 20 May, and I would rather not pay for empty chairs or turn a family
> away. Our director is confident the vendor's flags have always caught what matters. Tell me how many students we book, to the nearest
> ten, in one sentence I can put in the order. Send `retest_booking.xlsx` with the sheets below, a chart `sitting_screen.png`, and a
> one-page `booking_note.pdf`.

* `retest_booking.xlsx` — the booking build, the participation sheet (ask A), the booklet sheet (ask B) and the construction table (ask C).
* `sitting_screen.png` — every 2026 sitting as a point, matched residual against erasure index, with classroom sittings and make-up
  sittings in two marker shapes, the two cut-offs as labelled lines, the empty gap shaded, and the booked figure in the title.
* `booking_note.pdf` — the committed seat count and the alternatives a reviewer will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each grade 3 to 8, the federal participation rate and the number of non-participants.
  *Device:* the federal denominator is enrolment on the first day of the testing window, read from the effective-dated enrolment register,
  and the reporting guide removes medical-emergency exemptions from numerator and denominator alike. Dividing tested students by the October
  census misstates four grades. The retest count never uses the enrolment register.
* **Ask B (device-carried).** For the nine districts with the most booklets, booklets shipped, returned used, returned unused and
  unaccounted for. *Device:* the shipping manifest records grade 3–5 booklets in sealed packs of 25 and grade 6–8 booklets singly, as its
  notes page says. Reading every quantity as booklets invents thousands of missing booklets in six districts.
* **Ask C (validity).** The seat count under each of the four rung constructions, with each construction's hits on the 520 audited
  sittings.
* **Decoupling.** Clearing the sitting regroup and the recovered standard changes no figure in asks A or B.

## 11. Rubric arithmetic

6 grades × 2 (ask A) + 9 districts × 4 (ask B) + 4 constructions × 2 (ask C) + the committed seats, the referred make-up sittings and the
classroom-grain figure they replace + 5 named chart parts + 3 files ≈ 65 criteria.

## 12. World-building constraints

* 412,000 results, 17,800 classroom sittings and 2,600 make-up sittings. Make-up testers are 8.0% of results, at most three per classroom in
  94% of classrooms.
* Referred at classroom grain: 300 classrooms, 7,200 on the rosters, 580 of them absent on the main day. Referred make-up sittings: 84,
  with 1,680 students (40 of them absentees from referred classrooms). Answer 8,300.
* Rung figures are 15,400 / 9,900 / 7,200 / 8,300, the partial route 6,620, and every other grid cell sits at least 13% from the answer.
* The audited sample holds 64 confirmed and 456 cleared sittings with empty gaps on both keys; classroom and sitting statistics differ by
  at most 0.11 SD in every audited sitting.
* Corrie Lane and Hatherley are identical on every classroom-level column. The enrolment register and the shipping manifest never touch
  scan records or the sitting register.
* May rosters differ from October's for under 1% of students in every referred classroom.

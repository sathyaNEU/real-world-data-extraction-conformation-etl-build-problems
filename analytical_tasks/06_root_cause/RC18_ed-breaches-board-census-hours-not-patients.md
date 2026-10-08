# RC18 — Which cause of the major emergency department's four-hour breaches the winter fund fixes, when the board census counts hours, not patients

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Policy & Education · health-system administration |
| Mirrors | Capacity investments read off hourly occupancy snapshots (queue-depth boards in support operations, dock-door and picker boards at Amazon fulfilment centres, incident boards at cloud platforms), where an item stuck for ten hours fills ten snapshots and one stuck for an hour fills one, so snapshot shares over-weight long waits and the unit the investment is judged on has to be rebuilt from another record |
| Decision shape | Which of N root causes gets the fix: the winter fund buys one scheme for the major emergency department |
| Committed call | The cause the fund fixes, and the type 1 four-hour breaches its fix would avoid across this winter's nights |
| Gap · Pattern | Gap 2 (population) · Pattern D, E07 (two grains, both flawless: the hourly board census counts patient-hours by waiting reason, the fund counts breaching attendances, and only each attendance's timestamped moves between spaces link the two), with E18 (the segment coarsened: all department types for type 1) at rung 1 |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #14 coarsens the segment it was asked about · #2 counts file rows instead of the real unit · #1 reports a failed back-test, ships anyway |
| Calibration form | Settled-transaction ledger: the commissioner's settlements of nine past winter schemes, each paid on the breaches it avoided |
| Driving force | The department's board census records every occupied space each hour with its waiting reason and a red flag once the patient passes four hours, and the site team's breach report counts flagged rows. A patient waiting ten hours past four for a bed fills ten rows; one whose senior decision came an hour late fills one, then often reappears as a bed wait. The fund counts breaching attendances, each attributed to the reason in force when its four hours elapsed. The census carries no patient number or arrival time, so only each attendance's timestamped moves between spaces place its four-hour point on one census row. Counted that way, the late senior decision, not the bed, is the biggest cause. |

## 1. Situation

A hospital's all-types four-hour performance rose from 71% to 77% after it opened a co-located urgent treatment centre, and the board credited its
flow programme. The major emergency department's own (type 1) performance fell from 68% to 61%. The integrated care board has one winter fund for
one scheme: an escalation ward against exit block (A), a resident night consultant (B), an overnight CT radiographer (C), an ambulance handover
cohort area (D) or psychiatric liaison for mental-health waits (E). The fund rule says how schemes are judged. The commissioner pays past winter
schemes on the breaches they avoided, and its settlements sit in a ledger. The site team reports breaches by waiting reason from the board census.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: attendances and breaches by department type, the validated breach codes, every board-census row, each
  attendance's moves between spaces and the ledger. The board's all-types figure is correct, and the site team's breach hours are correct breach
  hours. Nothing is overturned; the census measures patient-hours and the fund is judged on attendances, and the two differ in shape.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the board's credit, every voice and the licensed basis. The census still shows the department full of flagged
  patients waiting for beds, and nothing in the pack says how many patients those rows are.
* **Instrument repair.** Give the census perfect reasons, a patient number and a timestamp on every row: a ten-hour bed wait still fills ten
  rows, as an hourly census is designed to, and the fund still counts the attendance once, at its four-hour point. The better instrument
  shortens the bridge; the grain difference stays.
* **Lens swap.** The naive build counts hours of flagged occupancy; the answer counts attendances at one moment each, their four-hour point:
  a different population (attendances, not hours) at a different moment.

## 3. The driving force

A strong solver sets aside the board's all-types table, because the urgent treatment centre's breaches (mostly evening waits for its closed
x-ray room) inflate "awaiting diagnostics" there, and works on type 1 alone. It distrusts the validated codes, which record the earliest delay
on a pathway, and turns to the department's own record of what every patient over four hours was waiting for: the hourly board census, filed
by the nurse in charge, with the site team's breach report built on it. Apportioned by flagged rows, exit block takes 3,120 of the winter's
5,400 night breaches and the senior gap 360. But the census is hourly. A frail patient admitted at three hours waits a mean nine hours past
four for a bed and fills nine flagged rows; a patient whose senior decision is an hour late fills one, and if admitted then fills six more as a
bed wait. The fund counts each breaching attendance once, under the reason in force when its four hours elapsed. Counting runs of rows does
not recover patients, because bed waits move from cubicle to corridor to the holding area and each move starts a new run. The census carries
no patient number, so each breaching attendance's four-hour point has to be placed in the space it then occupied, from its timestamped moves,
and read off that hour's census row. Counted that way, the senior gap holds 1,750 breaches and exit block 1,100.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Breaches by validated cause code, from the board's all-types table | C, overnight CT (2,100) | The board's own report, every breach coded by the validation team | The fund rule names the type 1 department; 1,300 of the "awaiting diagnostics" codes belong to the urgent treatment centre |
| 1 | The same codes, type 1 only | D, ambulance handover (1,650) | The right department, its own validated codes | The coding guide records the earliest delay on each pathway, so handover is coded for most ambulance arrivals whatever held them later |
| 2 | The night breaches apportioned by the board census's flagged rows by waiting reason, the site team's breach report | A, exit block (3,120) | The department's own hour-by-hour record of what every patient over four hours was waiting for | The census guide: one row per occupied space per hour, so a patient waiting ten hours past four fills ten flagged rows |
| 3 | **Decisive:** each breaching attendance placed, through its timestamped moves, in the space it occupied when its four hours elapsed, and its reason read from that hour's census row | **B, night senior gap (1,750)** (4th of 5 on rung 0) | — | — |

* **Position table.** B ranks 4th on rungs 0 and 1 and 3rd on rung 2 (360, behind A and E), and leads only rung 3. Rung leaders beat their
  runners-up by 1.27×, 1.38×, 2.33× and 1.59×.
* **Discriminator dominance.** Exit block carries an 8.66× lead into rung 3 (3,120 against 360). Linking multiplies the senior gap's figure by
  4.86 and exit block's by 0.35, an edge of 13.8×, 1.33 times the required 1.2 × 8.66 = 10.4; the net margin is 1.59×.
* **Partial correction priced (L3).** Every half-built grain fix leaves exit block in front. Counting runs of flagged rows in one space under
  one reason as patients, or counting the hours a space turns from unflagged to flagged, splits every bed wait at each of its moves: A 4,940
  runs against B's 1,930 (2.56×). Linking the census to attendances but taking each breach's reason at departure, or the reason it held
  longest, against the commissioner's four-hour-point rule, hands exit block every late senior decision that ended in a bed wait: A 2,275
  against B's 875 (2.60×), or A 1,975 against C's 900 (2.19×).
* **Grid.** Segment (all types, type 1) × source (codes, census rows, census runs, linked attendances) × reason (at the four-hour point, at
  departure, longest held; linked builds only) gives seven feasible builds, because the census and the moves cover only type 1. They name C,
  D, A, A, A, A and B. The nearest wrong cell is the linked build with the longest-held reason, one rule away from the answer.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The census guide says one row per occupied space per hour, with the waiting reason and the four-hour flag; the
   commissioner's contract says which reason a breach takes. No document says the site team's report counts hours, or that census rows reach
   attendances through the move history.
2. **The ledger pins a construction, not a menu.** The linked count reproduces 9 of 9 settled schemes to the breach; apportionment by
   flagged rows reproduces 2 (the two night-consultant schemes, whose reason clears within the hour past four), runs of rows 3 and reasons at
   departure 4. Every rival over-credits the long-wait reasons and under-credits the short ones, so none reconciles on the nine-scheme total.
   The link is a join on space and time with no parameter to scan.
3. **No arithmetic symptom.** Census rows, attendances, moves and breaches reconcile on every rung; every flagged row is a real patient-hour
   over four hours.
4. **Not a row predicate.** A breach's reason comes from the census row of the space its patient occupied in the hour its four hours
   elapsed, found by joining the attendance's move history to another table on space and time.
5. **The enumeration is arithmetic.** No column carries a breach's reason or a census row's patient; 5,400 breaches are placed from two tables.
6. **No cutover date.** Bed waits and late senior decisions run all winter; the dated event (the treatment centre's opening) moves the
   all-types figure and is the decoy.
7. **Survives deletion.** With every voice removed, the flagged rows still name exit block.

## 6. The calibration corpus

* **Form.** The commissioner's ledger: nine past winter schemes, each with the nights it ran, its settlement in breaches avoided, and the
  board census, attendance and move records for those winters.
* **What it pins.** The link (above), and that a settlement counts attendances at their four-hour point, never patient-hours.
* **Twin pair.** Schemes S-21 and S-24, two escalation wards, ran 26 nights each with identical census profiles (flagged rows by reason, 900
  bed-wait rows each), attendances and triage mixes. They settled at 180 and 90 breaches avoided (2.0×): S-21's winter had more bed waits at
  five hours past four, S-24's half as many at ten. Only the linked count reproduces both.
* **Every rule exercised.** One settled night-consultant scheme's breaches cleared within the hour past four (census and link agree), one
  mental-health scheme's patients moved to the safe room after four hours (testing the link through moves), and one ward reopened a space
  within the hour (testing a space held by two patients in one night).
* **Resemblance points at the decoy.** This winter's census profile matches S-22, the escalation ward that settled highest of the nine, on
  flagged rows, alert levels and night count.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The fund rule: the fund buys the scheme that would avoid the most type 1 (major emergency department) four-hour breaches
  across this winter's nights. The commissioner's contract: a scheme is settled on the breaches whose reason, in force when their four hours
  elapsed, it addresses. The census guide: one row per occupied space per hour, with the waiting reason and the four-hour flag.
* **Empirical pins.** The link through the move history, from the ledger; the mapping of census reasons to schemes.
* **Voices.** The site manager: "Look at the board on any night; it's wall-to-wall patients waiting for beds." The director of operations:
  "Ambulances queue outside every evening. Handover is the bottleneck."
* **Licensed wrong basis.** The fund rule records that the integrated care board's performance team reviews schemes on validated breach codes
  across all department types and will present that table.

## 8. Determinism by construction

* **Breach.** A type 1 attendance lasting over four hours from arrival to departure; the treatment centre's attendances are outside the fund
  rule. A breach belongs to the winter's nights when its four-hour point falls between 20:00 and 08:00.
* **Reason.** The census row for the attendance's space at the first hourly snapshot at or after its four-hour point; no attendance moves
  between its four-hour point and that snapshot, and every census reason maps to one scheme or to "other".
* **Census.** Rows carry the hour, the space, the waiting reason and the flag, and no patient number or arrival time; moves are timestamped to
  the minute and no space holds two patients at one snapshot.
* **Rounding.** Breaches to the nearest fifty; the committed figure sits mid-bin.

## 9. Prompt sketch and deliverables

> Our all-types four-hour number looks better, but the major department is getting worse, and the winter fund buys one scheme for it. The chair
> is sure overnight scanning is what breaks it. Tell me which cause we fix and how many type 1 breaches the fix would avoid across this winter's
> nights, to the nearest fifty, as one sentence for the fund panel. Send `winter_fund_case.xlsx` and a chart `breach_reasons.png`.

* `winter_fund_case.xlsx` — the five causes under each construction, the treatment-centre sheet (ask A), the staffing sheet (ask B) and the
  ledger reproduction (ask C).
* `breach_reasons.png` — paired bars per cause of flagged census rows and linked breaches, an inset histogram of hours past four by reason, the
  ledger's nine settlements as a strip of reproduced and missed points under each construction, and the funded cause labelled.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each winter week, treatment-centre attendances and its four-hour performance. *Device:* patients
  streamed to the major department after triage appear in both department types with a streaming flag, as the data definitions document;
  counting both rows overstates the centre's attendances and its performance.
* **Ask B (device-carried).** For each winter week, nursing and medical sickness absence in the department as a share of rostered hours.
  *Device:* the rostering system records a shift swap as a cancelled shift plus a new shift carrying a swap reference, as its guide documents;
  counting cancelled shifts as absence overstates the rate in the four weeks around Christmas.
* **Ask C (validity).** For each of the nine settled schemes, the settled figure and what flagged rows, runs, departure reasons and the link
  return; and each cause under each rung construction.
* **Decoupling.** Clearing the link changes no figure in asks A or B; neither touches a census row, a move or a settlement.

## 11. Rubric arithmetic

13 weeks × 2 figures (ask A) + 13 weeks × 2 groups (ask B) + 9 schemes × 5 figures + 5 causes × 4 constructions (ask C) + the funded cause,
its figure and the runner-up's + 4 named chart parts + 2 files ≈ 125 criteria.

## 12. World-building constraints

* Type 1 night breaches 5,400, by reason at the four-hour point: B 1,750, A 1,100, C 900, E 650, D 600, other 400.
* Codes (A / B / C / D / E): all types 1,200 / 750 / 2,100 / 1,650 / 600, with 1,300 of C's at the treatment centre; type 1 1,200 / 750 /
  800 / 1,650 / 600.
* Flagged census rows: A 15,150 (bed waits a mean nine hours past four, plus 875 late senior decisions that went on to wait six hours for a
  bed), E 6,500, B 1,750, C 1,350, other 1,000, D 480. Apportioned to the 5,400 breaches: A 3,120, E 1,340, B 360, C 280, D 100.
* Moves after the four-hour point: bed waits 2.5 a patient, mental-health waits 1.5, imaging 1.2, senior waits 1.1, handover 1.0. Runs of
  flagged rows: A 4,940, B 1,930, C 1,080, E 980, D 600. Reasons at departure: A 2,275, B 875, E 650, C 600, D 600.
* Ledger: link 9/9; flagged rows 2; runs 3; departure reasons 4. S-21 and S-24 identical on every census and scheme column.
* Streaming flags and rostering swap rows touch no census row, move or settlement.

# RC18 — Which scheme the winter fund buys against the major emergency department's four-hour breaches, when the wait a breach carries is often not the one a scheme would remove

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Policy & Education · health-system administration |
| Mirrors | Capacity investments judged on the failures they would prevent (support queues where a ticket escalated late still waits on engineering, fulfilment-centre bottlenecks at Amazon where faster picking still meets a full dock, incident queues at cloud platforms), where the stage a failed item was waiting at when its deadline passed is often not the stage whose fix would have saved it, and a fix with fixed capacity caps what it can save |
| Decision shape | Which of N root causes gets the fix: the winter fund buys one scheme for the major emergency department |
| Committed call | The cause the fund fixes, and the type 1 four-hour breaches its fix would avoid across this winter's nights |
| Gap · Pattern | Gap 3 (objective) over Gap 2 (population) · E22 (the deciding comparison is a set of isolated counterfactuals: every breaching stay recomputed without each scheme's waits, the escalation ward's beds a binding nightly limit), pinned by the settled ledger, with E07 (census hours and attendances linked through timestamped moves) at rung 3 and E18 (the segment coarsened) at rung 1 |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #14 coarsens the segment it was asked about · #2 counts file rows instead of the real unit · #20 leaves the deciding comparison unstated |
| Calibration form | Settled-transaction ledger: the commissioner's settlements of nine past winter schemes, each paid on the breaches it avoided |
| Driving force | Linked to attendances, the board census puts the late senior decision first among the reasons in force when patients' four hours ran out. A breach is avoided only if the patient would have left within four hours: most patients whose decision came late were then admitted and waited hours for a bed, so a night consultant gets few of them out in time, and the escalation ward's seven beds cap what it can take each night. Mental-health patients wait hours for assessment, often before their four hours are up and under another reason at the four-hour point, and most leave once seen. Every breaching stay recomputed without each scheme's waits, at its response standard and the ward's nightly beds, makes psychiatric liaison the scheme that avoids the most. |

## 1. Situation

A hospital's all-types four-hour performance rose from 71% to 77% after it opened a co-located urgent treatment centre, and the board credited its
flow programme. The major emergency department's own (type 1) performance fell from 68% to 61%. The integrated care board has one winter fund for
one scheme: an escalation ward against exit block (A), a resident night consultant (B), an overnight CT radiographer (C), an ambulance handover
cohort area (D) or psychiatric liaison for mental-health waits (E). The fund rule says how schemes are judged. The commissioner pays past winter
schemes on the breaches they avoided, and its settlements sit in a ledger. The site team reports breaches by waiting reason from the board census.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: attendances and breaches by department type, the validated breach codes, every board-census row, each
  attendance's moves between spaces, the scheme catalogue and the ledger. The board's all-types figure is correct, and the site team's breach
  hours are correct breach hours. Nothing is overturned; every table counts breaches by what they carried, and the fund buys the breaches a
  scheme would remove.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the board's credit, every voice and the licensed basis. The census still shows the department full of patients
  waiting for beds, and the linked count still puts the late senior decision first.
* **Instrument repair.** Suspect files: the validated breach code, which records the earliest delay on a pathway, and the board census, which
  carries no patient number. Repaired so that every breach carries the reason in force at its four-hour point and every census row its patient,
  rung 0 returns C (2,200, the treatment centre's imaging waits included), rungs 1 and 3 return B (1,750), and rung 2, which counts rows, still
  returns A; none returns E. The answer still needs every stay recomputed without each scheme's waits: no record, however complete, says which
  breaches a scheme would have removed, or how many the ward's seven beds can take in a night.
* **Lens swap.** The naive build counts breaches by the reason they carry; the answer counts the breaches each scheme would have removed, a
  different set of attendances for each scheme, overlapping and including breaches that carry another reason.

## 3. The driving force

A strong solver sets aside the board's all-types table, because the urgent treatment centre's breaches (mostly evening waits for its closed
x-ray room) inflate "awaiting diagnostics" there, and works on type 1 alone. It distrusts the validated codes, which record the earliest delay
on a pathway, and turns to the hourly board census of what every patient over four hours was waiting for. Apportioned by flagged rows, exit
block takes 3,120 of the winter's 5,400 night breaches, but the census is hourly and a patient waiting nine hours past four for a bed fills nine
rows. Placing each breaching attendance, through its timestamped moves, in the space it occupied when its four hours elapsed counts patients,
and the late senior decision leads with 1,750. That is still not what the fund buys. A breach is avoided only if the patient would have left
within four hours. 1,190 of those 1,750 patients were admitted after the decision and waited a mean six hours for a bed, so a resident
consultant would have got 540 of the 1,750 out in time. The escalation ward's seven beds each take one patient a night, which caps it at about
600 breaches however many patients wait for beds. Mental-health patients wait hours for an assessment, often before their four hours are up and
under another reason at the four-hour point, and most leave once seen. Recomputing every breaching stay without each scheme's waits, at the
scheme's response standard and the ward's nightly beds, psychiatric liaison avoids 900 breaches, the escalation ward 600 and the night
consultant 540.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Breaches by validated cause code, from the board's all-types table | C, overnight CT (2,100) | The board's own report, every breach coded by the validation team | The fund rule names the type 1 department; 1,300 of the "awaiting diagnostics" codes belong to the urgent treatment centre |
| 1 | The same codes, type 1 only | D, ambulance handover (1,650) | The right department, its own validated codes | The coding guide records the earliest delay on each pathway, so handover is coded for most ambulance arrivals whatever held them later |
| 2 | The night breaches apportioned by the board census's flagged rows by waiting reason, the site team's breach report | A, exit block (3,120) | The department's own hour-by-hour record of what every patient over four hours was waiting for | The census guide: one row per occupied space per hour, so a patient waiting ten hours past four fills ten flagged rows |
| 3 | Each breaching attendance placed, through its timestamped moves, in the space it occupied when its four hours elapsed, its reason read from that hour's census row | B, night senior gap (1,750) | Every breach counted once, under the reason in force when its four hours ran out: patients, not hours | The move history: 1,190 of those 1,750 patients were admitted after the decision and waited a mean six hours for a bed |
| 4 | **Decisive:** every breaching stay recomputed without each scheme's waits, at the scheme's response standard, with the escalation ward's seven beds as a nightly limit, and the breaches each scheme avoids compared | **E, psychiatric liaison (900)** (5th of 5 on rung 0) | — | — |

* **Position table.** E ranks 5th on rungs 0 and 1, 2nd on rung 2 (2.33× behind exit block) and 4th on rung 3, and leads only rung 4. Rung
  leaders beat their runners-up by 1.27×, 1.38×, 2.33×, 1.59× and 1.50× (900 against the ward's 600).
* **Discriminator dominance.** The senior gap carries a 2.69× lead into rung 4 (1,750 against 650). Recomputing stays multiplies liaison's
  figure by 1.38 and the senior gap's by 0.31, an edge of 4.49×, 1.39 times the required 1.2 × 2.69 = 3.23; the net margin is 1.67×.
* **Partial correction priced (L3).** Each half-built counterfactual names a wrong scheme. Recomputing stays without the ward's nightly bed
  limit credits the escalation ward with every bed wait that was a breach's last obstacle: A 2,300 against E's 900 (2.56×). Crediting each
  scheme with every breach whose stay included its wait, whatever followed, hands the senior gap nearly every admitted patient: B 3,900 against
  A's 3,000 (1.30×).
* **Grid.** Segment (all types, type 1) × source (codes, census rows, linked attendances) × measure on linked attendances (reason at the
  four-hour point, any wait in the stay, avoided without the bed limit, avoided with it) gives seven feasible builds, because the census and
  the moves cover only type 1. They name C, D, A, B, B, A and E. The nearest wrong cell is the counterfactual without the bed limit, one
  constraint away from the answer.
* **The deciding comparison (#20).** 900 breaches avoided by psychiatric liaison against 600 by the escalation ward is the sentence the fund
  panel needs; no table of breach reasons contains it.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The census guide says one row per occupied space per hour; the commissioner's contract says a scheme is settled on the
   breaches it avoided. No document says how an avoided breach is counted, that a patient's later waits keep it a breach, or that the ward's
   beds cap it.
2. **The ledger pins a construction, not a menu.** The recomputed stays reproduce 9 of 9 settled schemes to the breach; without the bed limit
   4 (the five wards over-credited), reasons at the four-hour point 3, flagged rows 2, any wait in the stay 1. Every rival over-credits wards
   and senior cover and under-credits liaison, so none reconciles on the nine-scheme total. The recomputation has no parameter: response
   standards and bed counts are the schemes' own specifications.
3. **No arithmetic symptom.** Census rows, attendances, moves and breaches reconcile on every rung; every flagged row is a real patient-hour
   over four hours.
4. **Not a row predicate.** Whether a breach is avoided depends on the attendance's whole sequence of waits and, for the ward, on how many
   patients reached an admission decision ahead of it that night.
5. **The enumeration is arithmetic.** No column carries an avoided breach; 900 are counted from 5,400 stays recomputed for each scheme.
6. **No cutover date.** Bed waits, late decisions and mental-health waits run all winter; the dated event (the treatment centre's opening)
   moves the all-types figure and is the decoy.
7. **Survives deletion.** With every voice removed, the four-hour-point reasons still name the senior gap and the flagged rows exit block.

## 6. The calibration corpus

* **Form.** The commissioner's ledger: nine past winter schemes, each with the nights it ran, its settlement in breaches avoided, and the
  board census, attendance and move records for those winters.
* **What it pins.** The recomputation (above): the scheme's waits shortened to its response standard, a ward's beds as a nightly limit, and a
  breach counted as avoided only when the whole stay falls within four hours.
* **Twin pair.** Schemes S-21 and S-24, two psychiatric liaison pilots, ran 26 nights each with identical census profiles, four-hour-point
  reasons (190 mental-health breaches each), attendances and triage mixes. They settled at 180 and 90 breaches avoided (2.0×): in S-21's winter
  most patients left once assessed, while in S-24's half went on to wait for an inpatient psychiatric bed. Only the recomputed stays reproduce
  both.
* **Every rule exercised.** One settled ward scheme filled its beds every night (testing the limit), one night-consultant scheme ran in a
  winter with few bed waits (testing the whole stay), and one liaison scheme's patients waited for assessment before their four hours under
  another reason (testing breaches carried by another reason).
* **Resemblance points at the decoy.** This winter's census profile matches S-22, the escalation ward that settled highest of the nine, on
  flagged rows, alert levels and night count.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The fund rule: the fund buys the scheme that would avoid the most type 1 (major emergency department) four-hour breaches
  across this winter's nights. The commissioner's contract: a scheme is settled on the type 1 breaches it avoided. The scheme catalogue: each
  scheme's response standard (a decision within 30 minutes, an assessment within an hour, a scan within an hour, handover within 15 minutes)
  and the escalation ward's seven beds. The census guide: one row per occupied space per hour, with the waiting reason and the four-hour flag.
* **Empirical pins.** The recomputation and the ward's allocation in order of admission decision, from the ledger; the mapping of census
  reasons to schemes.
* **Voices.** The site manager: "Look at the board on any night; it's wall-to-wall patients waiting for beds." The director of operations:
  "Ambulances queue outside every evening. Handover is the bottleneck."
* **Licensed wrong basis.** The fund rule records that the integrated care board's performance team reviews schemes on validated breach codes
  across all department types and will present that table.

## 8. Determinism by construction

* **Breach.** A type 1 attendance lasting over four hours from arrival to departure; the treatment centre's attendances are outside the fund
  rule. A breach belongs to the winter's nights when its four-hour point falls between 20:00 and 08:00.
* **Waits.** Each attendance's waits by reason are read hour by hour from the census rows of the spaces its moves place it in; reasons change
  only on the hour, and no space holds two patients at one snapshot.
* **Avoided.** A breach is avoided by a scheme when the stay, with every wait of the scheme's reason shortened to its response standard, is
  four hours or less. The ward takes up to seven patients a night in order of admission decision, each leaving the department fifteen minutes
  after the decision.
* **Census.** Rows carry the hour, the space, the waiting reason and the flag, and no patient number or arrival time; moves are timestamped to
  the minute.
* **Rounding.** Breaches to the nearest fifty; the committed figure sits mid-bin.

## 9. Prompt sketch and deliverables

> Our all-types four-hour number looks better, but the major department is getting worse, and the winter fund buys one scheme for it. The chair
> is sure overnight scanning is what breaks it. Tell me which cause we fix and how many type 1 breaches the fix would avoid across this winter's
> nights, to the nearest fifty, as one sentence for the fund panel. Send `winter_fund_case.xlsx` and a chart `breach_reasons.png`.

* `winter_fund_case.xlsx` — the five causes under each construction, the treatment-centre sheet (ask A), the staffing sheet (ask B) and the
  ledger reproduction (ask C).
* `breach_reasons.png` — paired bars per cause of breaches by four-hour-point reason and breaches avoided, an inset of the ward's beds filled
  by hour of night, the ledger's nine settlements as a strip of reproduced and missed points under each construction, and the funded cause
  labelled.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each winter week, treatment-centre attendances and its four-hour performance. *Device:* patients
  streamed to the major department after triage appear in both department types with a streaming flag, as the data definitions document;
  counting both rows overstates the centre's attendances and its performance.
* **Ask B (device-carried).** For each winter week, nursing and medical sickness absence in the department as a share of rostered hours.
  *Device:* the rostering system records a shift swap as a cancelled shift plus a new shift carrying a swap reference, as its guide documents;
  counting cancelled shifts as absence overstates the rate in the four weeks around Christmas.
* **Ask C (validity).** For each of the nine settled schemes, the settled figure and what flagged rows, four-hour-point reasons, any wait in
  the stay, the unlimited counterfactual and the recomputation return; and each cause under each rung construction.
* **Decoupling.** Clearing the recomputation changes no figure in asks A or B; neither touches a census row, a move or a settlement.

## 11. Rubric arithmetic

13 weeks × 2 figures (ask A) + 13 weeks × 2 groups (ask B) + 9 schemes × 6 figures + 5 causes × 5 constructions (ask C) + the funded cause,
its figure and the runner-up's + 4 named chart parts + 2 files ≈ 140 criteria.

## 12. World-building constraints

* Type 1 night breaches 5,400, by reason at the four-hour point: B 1,750, A 1,100, C 900, E 650, D 600, other 400.
* Codes (A / B / C / D / E): all types 1,200 / 750 / 2,100 / 1,650 / 600, with 1,300 of C's at the treatment centre; type 1 1,200 / 750 /
  800 / 1,650 / 600.
* Flagged census rows: A 15,150 (bed waits a mean nine hours past four, plus late senior decisions that went on to wait six hours for a bed),
  E 6,500, B 1,750, C 1,350, other 1,000, D 480. Apportioned to the 5,400 breaches: A 3,120, E 1,340, B 360, C 280, D 100.
* Breaches avoided: E 900 (560 of its own 650, the rest waiting for inpatient psychiatric beds, plus 340 whose assessment wait ended before
  their four hours under another reason), A 600 (seven beds over 90 nights, nearly every night full), B 540 (1,190 of its 1,750 went on to
  wait for a bed), C 380, D 250. Without the bed limit A 2,300; any wait in the stay B 3,900, A 3,000, C 1,500, E 1,100, D 900.
* Ledger: recomputation 9/9; without the bed limit 4; four-hour-point reasons 3; flagged rows 2; any wait 1. S-21 and S-24 identical on every
  census, reason and scheme column.
* Streaming flags and rostering swap rows touch no census row, move or settlement.

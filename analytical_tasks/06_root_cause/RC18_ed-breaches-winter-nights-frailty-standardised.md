# RC18 — Which cause of the major emergency department's four-hour breaches the winter fund fixes, when the two biggest causes strike on the same nights

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Policy & Education · health-system administration |
| Mirrors | Capacity investments where two bottlenecks bind on the same nights (support queues when both tier-2 staffing and a backend tool degrade, fulfilment nights at Amazon when dock doors and pickers are both short, on-call at cloud platforms when a database and its responder rota are both thin), so the only clean reads come from nights that had one and not the other |
| Decision shape | Which of N root causes gets the fix: the winter fund buys one scheme for the major emergency department |
| Committed call | The cause the fund fixes, and the type 1 four-hour breaches its fix would avoid across this winter's nights |
| Gap · Pattern | Gap 2 (population) · Pattern D (two grains, both flawless: partial-exposure nights standardised to the winter base through the frailty register), with E18 (the segment coarsened: all department types for type 1) at rung 1 |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #14 coarsens the segment it was asked about · #13 validates on one population, applies to another · #1 reports a failed back-test, ships anyway |
| Calibration form | Settled-transaction ledger: the commissioner's settlements of nine past winter schemes, each paid on the breaches it avoided |
| Driving force | Exit block and missing senior cover bind on the same winter nights, so their effects separate only on nights with an escalation ward open (beds, no senior) or a resident consultant on (senior, no beds). Both effects fall mostly on frail patients. Escalation wards open on frailty-surge nights and the consultant rota covers quieter weekends, so read straight the senior gap looks bigger. Frailty lives in the community frailty register, reached by patient number. Standardised to the winter's nights, exit block is the bigger cause. |

## 1. Situation

A hospital's all-types four-hour performance rose from 71% to 77% after it opened a co-located urgent treatment centre, and the board credited its
flow programme. The major emergency department's own (type 1) performance fell from 68% to 61%. The integrated care board has one winter fund for
one scheme: an escalation ward against exit block (A), a resident night consultant (B), an overnight CT radiographer (C), an ambulance handover
cohort area (D) or psychiatric liaison for mental-health waits (E). The fund rule says how schemes are judged. The commissioner pays past winter
schemes on the breaches they avoided, and its settlements sit in a ledger.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: attendances and breaches by department type, the validated breach codes, the nightly site reports, the
  frailty register and the ledger. The board's all-types figure is correct, and the emergency medicine lead's escalation-night read is a true
  measurement. Nothing is overturned; the two reads that separate the collinear causes describe nights that are not miniatures of the winter.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the board's credit, every voice and the licensed basis. Escalation-ward nights still show the senior gap as the
  larger effect, and nothing in the pack says those nights are frailer.
* **Instrument repair.** Record every patient's timeline perfectly: on nights with both exit block and no senior, the two still act on the same
  patients, so the counterfactual without one of them is identified only through partial-exposure nights, whose frailty a better clock does
  not change.
* **Lens swap.** The raw reads describe escalation nights and consultant nights; the answer describes the whole winter's nights, a different
  population with a different frailty mix.

## 3. The driving force

A strong solver sets aside the board's all-types table, because the urgent treatment centre's breaches (mostly evening waits for its closed
x-ray room) inflate "awaiting diagnostics" there, and works on type 1 alone. It distrusts the validated codes, which record the earliest delay
on a pathway, and models breaches avoided night by night. Exit block and the senior gap cannot be separated on ordinary winter nights, because they
coincide. Two kinds of night break the tie: nights with the escalation ward open, which relieve exit block, and nights with a resident consultant.
Read inside those nights, the senior gap accounts for 2,300 breaches over the winter and exit block for 1,500, and the two sum exactly to their
joint effect. Both effects fall overwhelmingly on frail patients, who need a bed and a senior decision. The escalation ward opens when a frailty
surge pushes the hospital to its highest alert level (55% of attendances frail), while the consultant rota covers weekends (12% frail); the winter
base is 30%. Frailty is in the community frailty register, matched by patient number, not in the attendance record. Standardised to the winter
base, exit block accounts for 2,350 and the senior gap for 1,450, and they still sum to the same 3,800.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Breaches by validated cause code, from the board's all-types table | C, overnight CT (2,100) | The board's own report, every breach coded by the validation team | The fund rule names the type 1 department; 1,300 of the "awaiting diagnostics" codes belong to the urgent treatment centre |
| 1 | The same codes, type 1 only | D, ambulance handover (1,650) | The right department, its own validated codes | The coding guide records the earliest delay on each pathway, so handover is coded for most ambulance arrivals whatever held them later |
| 2 | Night-level counterfactual: breaches each cause's fix would avoid, the collinear pair read on escalation-ward and consultant nights | B, night senior gap (2,300) | Two clean natural experiments, and their effects sum exactly to the joint effect | The frailty register: escalation nights are 55% frail and consultant nights 12%, against the winter base's 30% |
| 3 | **Decisive:** each partial-exposure effect estimated by frailty and standardised to the winter base | **A, exit block (2,350)** (4th of 5 on rung 0) | — | — |

* **Position table.** A ranks 4th on rungs 0 and 1 and 2nd on rung 2, 1.53× behind B, and leads only rung 3. Rung leaders beat their runners-up
  by 1.27×, 1.57×, 1.53× and 1.62×.
* **Discriminator dominance.** The senior gap carries a 1.53× lead into rung 3 (2,300 against 1,500). Standardisation multiplies exit block's
  read by 1.57 and the senior gap's by 0.63, an edge of 2.49×, above the required 1.2 × 1.53 = 1.84; the net margin is 1.62×.
* **Partial correction priced (L3).** A solver who suspects the two kinds of night differ and standardises on the attendance record's own
  columns (triage category, age band, arrival mode), which are decorrelated from frailty inside each night type by construction, changes nothing
  and still names B.
* **Grid.** Segment (all types, type 1) × method (codes, raw reads, standardised on record columns, standardised on frailty) gives six feasible
  builds naming C, D, B, B and A; the nearest wrong cell is the record-column standardisation, one join away from the answer.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The escalation policy says the ward opens at the highest alert level; the consultant rota is a staffing table. No
   document says either kind of night differs in frailty or that the effects depend on it.
2. **The ledger pins a construction, not a menu.** Frailty-standardised reads reproduce 9 of 9 settled schemes to the breach; triage-standardised
   reads 5, raw reads 4 (the four schemes that ran on randomised rotas, whose nights were miniatures of their winters). The rivals' misses run one
   way for each scheme type, so neither reconciles on the nine-scheme total. Standardisation needs the register join and a base built from a
   third set of nights; there is no parameter to scan.
3. **No arithmetic symptom.** Raw and standardised splits sum to the same joint effect (3,800); attendances, breaches and nights reconcile on
   every rung.
4. **Not a row predicate.** Each effect is estimated by frailty class inside a set of nights defined by the site report, then reweighted to a
   composition taken from all winter nights.
5. **The enumeration is arithmetic.** No column carries frailty or "breach avoidable by a bed"; both are built.
6. **No cutover date.** Exit block and the senior gap run all winter; the dated event (the treatment centre's opening) moves the all-types
   figure and is the decoy.
7. **Survives deletion.** With every voice removed, the raw reads still name the senior gap.

## 6. The calibration corpus

* **Form.** The commissioner's ledger: nine past winter schemes, each with the nights it ran, its settlement in breaches avoided, and the
  attendance and site data for those winters.
* **What it pins.** Frailty standardisation (above); the four randomised-rota schemes certify that a raw read is right when the nights are a
  miniature of the base.
* **Twin pair.** Schemes S-21 (an escalation ward) and S-24 (a second escalation ward) ran 26 nights each with identical attendances, breaches
  during the scheme and triage mixes. They settled at 180 and 88 breaches avoided (2.05×): S-21's nights were 31% frail and S-24's 14%. Only the
  frailty standardisation reproduces both.
* **Resemblance points at the decoy.** This winter's consultant and escalation nights match S-22, the night-consultant scheme that settled
  highest of the nine, on night count, alert levels and staffing.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The fund rule: the fund buys the scheme that would avoid the most type 1 (major emergency department) four-hour breaches across
  this winter's nights. The commissioner's contract: a scheme is settled on the breaches it avoided.
* **Empirical pins.** Frailty-specific effects inside each kind of night; the winter base's frailty mix from the register.
* **Voices.** The emergency medicine lead: "Nights without a consultant are where it falls apart; the escalation-ward nights prove it." The
  director of operations: "Ambulances queue outside every evening. Handover is the bottleneck."
* **Licensed wrong basis.** The fund rule records that the integrated care board's performance team reviews schemes on validated breach codes
  across all department types and will present that table.

## 8. Determinism by construction

* **Breach.** A type 1 attendance lasting over four hours from arrival to departure; the treatment centre's attendances are outside the fund
  rule.
* **Frailty.** Two classes from the register's score (frail at 5 or above); every type 1 attendance matches the register, and no score changes
  within the winter.
* **Nights.** The site report marks escalation-ward and consultant nights; no night has both, and the base is every winter night.
* **Additivity.** The collinear pair's effects are additive by construction (no interaction), so both splits sum to the joint effect.
* **Rounding.** Breaches to the nearest fifty; the committed figure sits mid-bin.

## 9. Prompt sketch and deliverables

> Our all-types four-hour number looks better, but the major department is getting worse, and the winter fund buys one scheme for it. The chair
> is sure overnight scanning is what breaks it. Tell me which cause we fix and how many type 1 breaches the fix would avoid across this winter's
> nights, to the nearest fifty, as one sentence for the fund panel. Send `winter_fund_case.xlsx` and a chart `night_effects.png`.

* `winter_fund_case.xlsx` — the five causes under each construction, the treatment-centre sheet (ask A), the delayed-transfers sheet (ask B)
  and the ledger reproduction (ask C).
* `night_effects.png` — dot pairs for exit block and the senior gap showing the raw and standardised reads, an inset of the frail share on
  escalation nights, consultant nights and the winter base, the joint effect as a reference band, and the funded cause labelled.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each winter week, treatment-centre attendances and its four-hour performance. *Device:* patients
  streamed to the major department after triage appear in both department types with a streaming flag, as the data definitions document;
  counting both rows overstates the centre's attendances and its performance.
* **Ask B (device-carried).** For each winter week, delayed-transfer patient-days on the wards. *Device:* the midnight census lists a delayed
  patient on every night they stay, and the weekly measure is patient-days, not patients, as the census guidance documents; counting distinct
  patients understates the measure about sixfold.
* **Ask C (validity).** For each of the nine settled schemes, the settled figure and what raw, triage-standardised and frailty-standardised
  reads return; and each cause under each rung construction.
* **Decoupling.** Clearing the frailty standardisation changes no figure in asks A or B.

## 11. Rubric arithmetic

13 weeks × 2 figures (ask A) + 13 weeks (ask B) + 9 schemes × 4 figures + 5 causes × 4 constructions (ask C) + the funded cause, its figure and
the runner-up's + 5 named chart parts + 2 files ≈ 105 criteria.

## 12. World-building constraints

* Breaches by rung (A / B / C / D / E): 700 / 1,300 / 2,100 / 1,650 / 600 all types; 700 / 1,050 / 800 / 1,650 / 600 type 1; 1,500 / 2,300 /
  700 / 1,100 / 650 raw; 2,350 / 1,450 / 700 / 1,100 / 650 standardised.
* Frail shares: escalation nights 55%, consultant nights 12%, winter base 30%. Frail patients carry about six times the non-frail exit-block
  effect and nine times the senior-gap effect.
* Triage, age band and arrival mode decorrelated from frailty within each night type.
* S-21 and S-24 identical on every scheme column except frailty.
* Streaming flags and census days touch no type 1 night, register match or settlement.

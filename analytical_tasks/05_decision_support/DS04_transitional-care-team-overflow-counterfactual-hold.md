# DS04 — Which hospital gets the extra transitional-care nurse team, when the only fair comparison says none of them clears break-even

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Policy & Education · health-system administration |
| Mirrors | Funding an outreach programme on outcomes of contacted versus uncontacted users, where contact depends on who answers (Google and Meta customer-success outreach, Amazon seller-support callbacks, onboarding calls at cloud platforms), with capacity overflow supplying the natural experiment |
| Decision shape | Hold, forced by a blocking quantity: one team for one of five hospitals, or the money back to the reserve |
| Committed call | The hospital that gets the team, or that none does; and the readmissions prevented per 100 patients called that the call rests on, to one decimal |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · S10, the governing verb is causal so the baseline is constructed from capacity overflow, with the population a flag suggests (#5) at rung 1 |
| Gate G mechanism | signal_vs_noise_or_hold, with decomposition_attribution |
| Measured traps engaged | #5 takes the population a flag or filter suggests · #15 follows the requester's hunch over the rule · #7 uses the ready-made measure · #13 validates on one population, applies to another |
| Calibration form | Gold-standard verification subsample: the quality office's chart review of a random 10% of eligible discharges, verifying eligibility, contact and 30-day unplanned readmission |
| Driving force | The board funds a team only where calls prevent at least 3.4 readmissions per 100 patients called. Called patients do come back far less often, but a nurse reaches the patients who answer, and those patients were going to do better anyway. On days the list outruns the team, the patients below the day's last attempted call are never attempted, and list order is set by discharge time alone. That overflow, built from list positions and the capacity log, is the only comparison in which a call is as good as random. On it the best hospital prevents 1.9 per 100, with a 90% upper bound of 3.0. |

## 1. Situation

A regional health system runs a transitional-care programme in which nurses call eligible patients on the first day after discharge. Next
year it can fund one more nurse team at one of five member hospitals, or return the money to the reserve. The board's expansion policy funds
a team only where the programme prevents at least 34 readmissions per team-year, which is 3.4 per 100 patients called. The discharge
register carries a high-risk flag from the readmission model. The programme protocol defines who goes on the call list, and each team's
capacity log records how many calls it attempted each day. The chief medical officer is convinced the calls work.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct and no stakeholder read is overturned. That covers the register's flag (correctly computed by
  the model), the call log, the claims readmissions, the capacity log and the chart-verified subsample. Called patients really do readmit
  less. The difficulty is that the policy's verb is "prevents", and the comparison that measures prevention has to be constructed from an
  operational file nobody reads as evidence.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the CMO's belief and the subsample. Called against uncalled, risk-adjusted, still clears break-even at Elmhurst,
  and every number reconciles.
* **Instrument repair.** No file the ladder uses is suspect: the flag is a correct model score (a different attribute from eligibility),
  the call and capacity logs are complete, and the chart-verified subsample confirms the claims capture every readmission. The deepest
  repair on offer, a recorded reason for every uncalled patient, leaves rungs 0 to 2 at Northgate, Riverside and Elmhurst, because each
  compares called with uncalled patients, and no record of the past observes a called patient's uncalled outcome. The overflow split is
  still needed for the hold.
* **Lens swap.** The naive comparison sets all called patients against all uncalled ones. The answer compares patients on over-capacity days
  split at the day's attempt count: a different population, compared at a cut the naive read never forms.

## 3. The driving force

A strong solver compares called with uncalled patients and finds a 5.7 to 8.1 point gap. It restricts to the patients the protocol
actually lists and adjusts for risk, age and prior admissions. Each step is competent, and Elmhurst still clears break-even at 3.9. But who
gets a call is not random. Nurses reach the patients who pick up, and those patients have lower readmission risk on dimensions no
covariate in the register carries. One file breaks the selection. Each team works its list from the top, the list is ordered by discharge
time, and the capacity log says how many patients the team attempted that day. On over-capacity days every patient below that count was
never attempted, for no reason connected to their health. Comparing attempted with never-attempted patients on those days, within each
hospital, gives the effect of a call. It is 0.5 to 1.9 per 100, and no hospital's upper bound reaches 3.4.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Readmission rate of uncalled minus called among flagged discharges, per hospital | A, Northgate (8.1 per 100) | The programme's own outcomes; every hospital clears break-even | The protocol: the list holds patients discharged home with an attributed practice on the discharge date, and 11% of flagged discharges never qualify |
| 1 | The protocol's eligible population (#5), unadjusted | B, Riverside (5.6) | The right population, and Northgate's facility discharges no longer inflate its uncalled group | The register: called patients carry lower risk scores, fewer prior admissions and younger ages than uncalled ones at every hospital |
| 2 | Eligible population, risk-adjusted called-versus-uncalled gap | C, Elmhurst (3.9, the only hospital above 3.4) | Population and confounders handled; Elmhurst clears the policy bar | The capacity log with list positions: on over-capacity days the never-attempted patients readmit within 1.9 points of the attempted ones at Elmhurst |
| 3 | **Decisive:** within each hospital, on days the list exceeded attempts, compare attempted with never-attempted patients split at the day's attempt count | **Hold: none of the five clears 3.4 (Elmhurst 1.9, 90% interval 0.8–3.0)** | — | — |

* **Position table.** Rung leaders are Northgate, Riverside, Elmhurst and then hold. Margins are 1.23 (Northgate over Riverside), 1.22
  (Riverside over Elmhurst) and 1.26 (Elmhurst over Riverside). On rung 3 Elmhurst still ranks first (1.9 against Westbrook's 1.4), so the
  hold is a refusal of the leader, not a tie.
* **Blocking quantity.** The best overflow effect is Elmhurst's 1.9 per 100 called, 56% of break-even. Its 90% upper bound is 3.0 and its
  95% bound 3.2, both under 3.4. The other four hospitals' upper bounds are 1.9 to 2.6.
* **Falsifiability.** Elmhurst would have been the pick at an overflow effect of 3.4 per 100, 1.79× its measured effect. Any hospital whose
  upper bound and point estimate cleared 3.4 would have been funded.
* **Partial correction priced (L3).** Using the over-capacity days but comparing called patients with every uncalled patient on those days,
  refusals and unreachable patients included, puts Elmhurst at 3.6 and funds it. The half-insight lands on a pick, further from the answer
  than rung 2's own figure. Pooling the overflow across hospitals mixes their baselines: the hospitals with the most over-capacity days
  also readmit most, so the pooled cut puts the effect at 3.6 per 100 everywhere, and the team goes where most patients are called,
  Northgate. No half-insight holds.
* **Grid.** Population (flag, protocol) × adjustment (none, risk) × comparison (all uncalled, overflow cut) gives 8 cells. Under the cut
  the population and adjustment toggles are idle (only listed patients have list positions, and the cut is as-good-as-random), so the four
  cut cells are one construction, and it holds. The four without it name Northgate,
  Riverside or Elmhurst. The nearest pick to the answer is the partial above (Elmhurst at 3.6), and it costs one error: an uncalled group the
  list cut never formed.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The protocol says the list is worked from the top. No document calls the never-attempted patients a comparison
   group, or says that nurses reach the healthier patients.
2. **No sweepable corpus nominates it.** *The verification protocol records whether a patient was reached and never why an unreached patient
   was not called.* So the subsample's called-versus-uncalled gap reproduces rung 2's adjusted gap within 0.2 points at every hospital, and
   it cannot see the overflow cut.
3. **No arithmetic symptom.** List lengths, attempts and calls reconcile with the capacity log, and readmissions tie to claims under every
   comparison.
4. **Not a row predicate.** Overflow status is a rank inside a team-day group, cut at that day's attempt count from a second file, and the
   effect is then a within-hospital difference on those days only.
5. **The enumeration is arithmetic.** No column marks a patient as never attempted for capacity; it follows from position against the
   day's count.
6. **No cutover date.** Overflow days are scattered through the year, on 38–46% of days at every hospital, and no series steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The quality office's chart-verified subsample: 2,140 eligible discharges drawn at random last year, each with verified
  eligibility, verified contact (from call recordings) and verified 30-day unplanned readmission.
* **What it certifies.** The measures every rung uses. The claims readmission flag agrees with chart review on 97.8% of records and the call
  log's contact field on 99.1%. The register flag disagrees with verified eligibility on 11%, every case a facility discharge or an expired
  attribution, which confirms rung 1.
* **What it is blind to.** The reason a patient went uncalled (above). A back-tester is confirmed at rung 2.
* **Twin pair.** Riverside's second quarter and Westbrook's third are identical on every visible column: 612 eligible discharges, 410
  calls, mean risk score 0.24, unadjusted gap 5.0 and adjusted gap 2.9. Their overflow effects are 2.2 and 1.0 per 100 (2.2×). Only the
  overflow cut separates them, so no gap transferred by resemblance reproduces both.
* **Every rule exercised.** Thirty team-days had a list exactly as long as the attempts (no overflow), which tests the day-level cut. Two
  teams split a hospital's list by ward, so the cut is per team, not per hospital.
* **Resemblance points at the decoy.** Elmhurst's profile matches the flagship site of the published programme evaluation the CMO cites.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The board's expansion policy: a team is funded only where the programme prevents at least 34 readmissions per team-year,
  otherwise the funds return to the reserve. The protocol: the list holds patients discharged home with an attributed practice on the
  discharge date, and calls happen on the first post-discharge day. The list specification: lists are built in discharge-time order. One
  sentence each, in three documents.
* **Empirical pins.** The call effect, from the overflow cut. Covariate balance between attempted and never-attempted patients, from the same
  days.
* **Voices.** The CMO: "Our called patients come back half as often; the calls work." Elmhurst's director: "We run the tightest programme in
  the system." The finance lead: "If it clears break-even, fund it."
* **Licensed wrong basis.** The policy records that the regional commissioner judges care programmes on risk-adjusted outcomes of contacted
  against uncontacted patients and will see that comparison.

## 8. Determinism by construction

* **The cut.** The capacity log counts attempts per team-day, and attempts run strictly down the list, so the never-attempted set has one
  reading. No patient is carried to a later day, because the call window is the first post-discharge day.
* **Balance.** On overflow days attempted and never-attempted patients match on risk score (0.31 against 0.31), age and prior admissions
  to within 0.5%, so adjusted and unadjusted overflow effects agree to 0.1.
* **Intervals.** Every hospital's 90% and 95% upper bounds sit below 3.4, so the interval convention cannot turn the hold into a pick.
* **Maturity.** The extract is 60 days after the last discharge, so every 30-day outcome has matured.

## 9. Prompt sketch and deliverables

> Next year I can fund one more transitional-care nurse team at one of our five hospitals, or put the money back in the reserve. Our CMO is
> convinced the calls are working. Tell me where the team goes, or that it should not be funded, in one sentence for the board, with the
> readmissions per hundred patients called you are relying on, to one decimal. Send `team_case.xlsx`, a chart `effect_by_hospital.png`,
> and a one-page `board_note.docx`.

* `team_case.xlsx` — the five hospitals' effects under each construction, the length-of-stay sheet (ask A), the discharge-summary sheet (ask
  B) and the balance sheet (ask C).
* `effect_by_hospital.png` — five hospitals with the overflow effect as points and 90% intervals, the risk-adjusted gap as hollow markers,
  break-even as a labelled reference line at 3.4, and the leader's distance to it annotated.
* `board_note.docx` — the committed call, the blocking quantity, and what would have made it a pick.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each hospital and quarter, the median length of stay of eligible discharges. *Device:* a
  transfer between member hospitals produces two encounters, joined in the encounter-linkage table. Counting each leg as a stay shortens
  Northgate's median by about a day in every quarter.
* **Ask B (device-carried).** For each hospital, the share of discharge summaries reaching the attributed practice within 48 hours.
  *Device:* an amended summary is re-sent with a new transmission ID and the same document ID, as the interface specification documents.
  Timing each transmission instead of each document's first send overstates timeliness at three hospitals.
* **Ask C (validity).** Each hospital's effect under the four constructions, and the attempted-versus-never-attempted balance on risk
  score, age and prior admissions.
* **Decoupling.** Clearing the overflow cut changes no figure in asks A or B. Encounter legs and summary transmissions never enter the call
  list, the capacity log or the readmission outcome.

## 11. Rubric arithmetic

5 hospitals × 4 quarters (ask A) + 5 timeliness shares (ask B) + 5 × 4 effects + 5 × 3 balance checks (ask C) + the hold, the blocking
quantity, break-even and the falsifying effect + 5 named chart parts + 3 files ≈ 72 criteria.

## 12. World-building constraints

* Effects per 100 called. Rung 0: 8.1 / 6.6 / 5.7 / 4.9 / 4.2. Rung 1: 4.1 / 5.6 / 4.6 / 2.9 / 3.6. Rung 2: 2.8 / 3.1 / 3.9 / 2.0 / 2.7.
  Overflow: 0.8 / 1.2 / 1.9 / 0.5 / 1.4 (Northgate, Riverside, Elmhurst, Castlefield, Westbrook). Break-even 3.4.
* Elmhurst's overflow standard error is 0.67 over three years of overflow days. Every hospital's list overflowed on 38–46% of days, and
  discharge time is unrelated to every register covariate.
* Called-versus-uncalled with every uncalled patient on overflow days gives Elmhurst 3.6.
* Northgate's flagged population holds most of the facility discharges. The twin quarters are identical on every visible column.
* Transfers and summary re-sends never touch the list, attempts, calls or readmissions.

# AD18 — Whether the end-of-line test switches to a multivariate screen in July, when the winning parallel run was a statement about winter

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Supply Chain & Logistics · manufacturing end-of-line quality |
| Mirrors | Switching a production screen on a parallel run held under conditions the next period will not share (end-of-line test changes at contract manufacturers for Apple-class devices, burn-in screens for data-centre hardware, vehicle end-of-line test changes before a seasonal ramp) |
| Decision shape | Hold, forced by a blocking quantity: the quality board's 30 June decision to switch to one of three multivariate screens for July–September, or hold the switch |
| Committed call | The screen the line switches to, or a hold of the switch for the quarter, with the quantity that decides it |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · past exceedance against forward yield (E08): the stand's oil temperature is how a period treats a unit, so winter detection does not carry; a quiet retest contamination behind the loud multiple-testing story at the lower rung (E15) |
| Gate G mechanism | signal_vs_noise_or_hold, with forecasting support |
| Measured traps engaged | #13 validates on one population, applies to another · #11 beats the headline trap, misses the quiet one · #9 picks from the offered options when none passes |
| Calibration form | Parallel-run overlap: ten winter weeks in which all four screens scored every unit, with teardown of every flagged unit, a 5% audit of the rest and 90-day field returns |
| Driving force | In the winter overlap the full multivariate screen beat the per-sensor limits by 18 points, and that is correct. But the stand's hydraulic oil runs 12 °C hotter from July, which shifts the healthy units' correlation structure and brings a different fault mix, seal extrusion. Re-baselined on last summer's healthy units and scored against last summer's field returns, every candidate's advantage over the incumbent has a 95% interval spanning zero; the largest, the residual screen's +9 points, would need about 138 summer faults to clear, and the record holds 42. |

## 1. Situation

A hydraulic-unit maker tests every unit on a 60-second cycle with 17 sensor channels, and the end-of-line screen today is a set of
per-sensor 3σ limits. The quality board decides on 30 June 2027 whether to switch for July to September to one of three multivariate
screens: the full Hotelling T² on all 17 features, a hybrid (T² on the hydraulic channels, per-sensor limits on the rest), or a PCA
residual (Q) screen. The quality manual says a screen replaces the incumbent when, on evidence about the faults the line will produce next
quarter, it catches more of them at no higher unit false-reject rate, with the detection difference's 95% interval above zero, and that
otherwise the switch is held and the parallel run extended. The pack carries the winter overlap, the station's test log, the MES unit
dispositions, the stand historian, and last summer's units with their 90-day field returns.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the overlap's scores and teardown results, the test log, the dispositions, the historian and last
  summer's returns. The overlap's report states what it found in winter. Nothing reported is overturned and no stakeholder read is
  corrected; the difficulty is that the quarter the switch buys is not the quarter the overlap measured.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices. The overlap still shows every multivariate screen ahead, and a careful solver who fixes the
  retest count still switches.
* **Instrument repair.** Suspect file: the station test log, which records a reject per test, so a unit retested twice under one serial
  counts three times. Repaired to one disposition per unit, rung 0 lands on rung 1 and switches to the hybrid (82% against 61%); rung 1
  still switches to the hybrid and rung 2 to the Q screen. The overlap, the MES dispositions, the historian and last summer's records are
  complete: every summer unit's channels are logged, every reject was torn down, and every shipped unit has its full return window, with no
  screenable fault returned after day 90. No record of a past season is a record of July to September, so the summer re-baseline scored
  against last summer's 42 faults is still needed for the hold.
* **Lens swap.** The naive read is winter units on winter baselines; the answer is summer units on summer baselines against summer
  faults: a different population at a different moment.

## 3. The driving force

A strong solver knows why seventeen separate limits over-reject, computes each screen's detection at a matched false-reject rate on the
overlap, notices that the station log records tests and that a failed unit is retested up to twice under one serial, rebuilds the rates
per unit from the MES dispositions, and finds the hybrid best at 82% against the incumbent's 61%. It switches. Each step is competent,
and the loud trap has been beaten and the quiet one too. But the overlap ran with the stand's oil between 38 and 41 °C, and the historian
shows it at 50 to 53 °C from July to September. Warm oil changes the healthy units' pressure-flow-power relationships, so a winter
covariance mis-scores healthy summer units, and summer brings seal extrusion, a fault class the overlap saw three times. The forward
question can be asked of last summer: re-baseline each screen on last summer's healthy units, match the incumbent's unit false-reject
rate, and score all four against last summer's 42 field-return faults. Every advantage is real in sign and none clears zero, and the
manual holds the switch.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The overlap's headline: detection at the station's 1.2% false-reject rate | Switch to the full T² (88% against 61%) | The parallel run the board commissioned, every unit scored by every screen | The test-log guide: rejects are logged per test, and a failed unit is retested up to twice under one serial; per unit the incumbent rejects 0.5% |
| 1 | Hygiene: rates rebuilt per unit from the MES dispositions, limits matched at 0.5% | Switch to the hybrid (82% against 61%; full T² 79%) | Both traps beaten: multiple testing by the multivariate screens, retests by the unit-level rebuild | The stand historian: from July the oil runs 12 °C hotter, and every screen's baseline is winter's |
| 2 | Each screen re-baselined on last summer's healthy units, the overlap's winter detection carried into summer | Switch to the Q screen (77% winter detection, the most stable under re-baselining) | The covariance shift is handled, and the overlap remains the only detection evidence with full teardown | Last summer's field returns: summer faults are 55% seal extrusion, a class the overlap saw three times |
| 3 | **Decisive:** every screen re-baselined on last summer's healthy units at a matched 0.5% and scored against last summer's 42 field-return faults | **Hold: no candidate's summer advantage has a 95% interval above zero** | — | — |

* **Blocking quantity.** Summer detection differences against the incumbent's 64%: full T² +7 points [−9, +23], hybrid +5 [−11, +21], Q
  screen +9 [−7, +25]. The largest would need about 138 summer faults to exclude zero; the record holds 42.
* **Why each candidate fails.** Each multivariate screen's interval spans zero, so none meets the manual's condition; the incumbent is not a
  candidate for adoption, only what runs while the switch is held.
* **Partial correction priced (L3).** A solver who re-baselines on summer healthy units but keeps winter detection (rung 2) switches to Q. A
  solver who scores last summer but forgets the retest correction sets limits at the 1.2% test-level rate and finds T² +14 [+1, +27], a
  switch the manual would allow and the unit-level evidence does not.
* **Grid.** Rate grain (test or unit) × baseline (winter or summer) × evidence (overlap or last summer) gives eight cells: every overlap
  cell switches (T², hybrid or Q); summer-evidence cells at test-level rates switch to T²; only unit-level, summer-baselined, summer-scored
  evidence holds.
* **Falsifiable.** The hold becomes a switch to the Q screen if a summer overlap adds about 96 more seal-era faults at the same advantage,
  or if the advantage proves above 16 points on the 42.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The overlap's report records temperatures as test conditions; no document links oil temperature to screen
   performance, and the manual's "next quarter" names no season.
2. **Corpus blind for a computable reason.** *In every overlap week the stand's oil sat between 38 and 41 °C, because the overlap ran from
   January to March,* so the overlap is arithmetically incapable of scoring a summer covariance or a summer fault mix.
3. **No arithmetic symptom.** The overlap's figures recompute exactly, unit rates tie to the MES, and last summer's data is complete.
4. **Not a row predicate.** It needs a covariance re-estimated on a season's healthy units, limits re-matched to a false-reject rate, and a
   paired comparison with an interval over a season's faults.
5. **The enumeration is arithmetic.** The verdict is three computed intervals against zero; no field marks a season as different.
6. **No cutover date.** Oil temperature follows the season gradually, and the screens' behaviour drifts with it; no series steps.
7. **Survives deletion.** With every voice removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The winter overlap: 10 weeks, 18,400 units, all four screens' scores per unit, teardown of every unit any screen flagged, a 5%
  random teardown audit of the rest, and 90-day field returns.
* **What it certifies.** Winter detection and false-reject rates per screen at unit level: incumbent 61% at 0.5%, full T² 79%, hybrid 82%,
  Q 77% at matched 0.5%, all intervals above zero in winter.
* **What it is blind to.** Summer (above): three seal-extrusion faults in ten weeks.
* **Twin pair.** Last July's and last September's units are identical on per-sensor flags, field-return faults (14 each) and fault classes.
  Re-baselined T² caught 12 in September and 6 in July (2×), because July ran 5 °C above the summer baseline's mean; no winter-based
  construction separates them.
* **Resemblance points at the decoy.** By fault mix and volume, the coming quarter most resembles the overlap's busiest weeks, the ones in
  which the hybrid's lead was largest.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The quality manual: a screen replaces the incumbent when, on evidence about the faults the line will produce next quarter,
  it catches more at no higher unit false-reject rate with the difference's 95% interval above zero; otherwise the switch is held and the
  parallel run extended. False-reject rates are per unit. The MES disposition is the unit's record of truth.
* **Empirical pins.** The summer baseline (last summer's units without a 90-day return) and the summer fault set (last summer's returns).
* **Voices.** The quality manager: "Seventeen separate limits is how you fill a line with false rejects." The test engineer: "The hybrid
  keeps the noisy temperature channels out of the covariance; that's the robust choice."
* **Licensed wrong basis.** The manual records that the customer's supplier-quality engineer judges screens on the parallel run's detection
  at a matched false-reject rate and will review the decision on that basis.

## 8. Determinism by construction

* **Healthy set.** Last summer's healthy units are those without a 90-day return; every one has a complete return window, and the
  twelve-month return file adds no screenable fault after day 90.
* **Intervals.** Paired Wald, exact McNemar and bootstrap intervals all span zero for every candidate (half-widths 15–17 points).
* **Limits.** Each screen's limit is the unit false-reject rate's quantile on the summer healthy set; 0.4% and 0.6% leave every interval
  across zero.
* **Season.** July to September matches last summer's historian within 1 °C each month.

## 9. Prompt sketch and deliverables

> On 30 June the quality board decides whether end-of-line test switches to one of the multivariate screens for July to September. Our
> quality manager is certain seventeen separate limits are the problem. Tell me in one sentence for the board which screen we switch to, or
> that we hold the switch this quarter, and send `screen_decision.xlsx` holding the sheets below, the chart `summer_detection.png`, and a
> one-page `board_decision.pdf`.

* `screen_decision.xlsx` — winter and summer evaluations for all four screens, the calibration sheet (ask A), the scrap sheet (ask B) and
  the evidence table (ask C).
* `summer_detection.png` — each candidate's detection advantage over the incumbent with its 95% interval, winter overlap against last summer
  side by side, the zero line drawn, oil temperature by month as an inset, and the July–September band shaded.
* `board_decision.pdf` — the committed verdict, the blocking quantity, and what would turn it into a switch.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the line's six test stands, calibration checks in the last twelve months and the share
  found out of tolerance. *Device:* a check that fails and is redone after adjustment is logged as two rows marked "as found" and "as left",
  per the calibration procedure. Counting rows overstates checks and understates the out-of-tolerance share on the three stands adjusted
  most. The screens never read the calibration log.
* **Ask B (device-carried).** For each of the last twelve months, scrap cost at end of line. *Device:* scrapping a finished unit also logs
  its scrapped sub-assemblies with a parent link, as the MES scrap guide documents. Summing every row double-counts sub-assembly cost in
  every month with finished-unit scrap.
* **Ask C (validity).** For each of the four screens, winter detection at matched unit rates and summer detection on last summer's faults,
  each with its interval.
* **Decoupling.** Clearing the summer re-baseline changes no figure in asks A or B.

## 11. Rubric arithmetic

6 stands × 2 (ask A) + 12 months (ask B) + 4 screens × 2 (ask C) + the hold verdict, the largest advantage's interval and the faults needed +
5 named chart parts + 3 files ≈ 43 criteria.

## 12. World-building constraints

* Winter overlap at unit level and 0.5%: incumbent 61%, T² 79%, hybrid 82%, Q 77%; at test level (1.2%) T² reads 88%.
* Last summer: 42 field-return faults, 55% seal extrusion; incumbent 64%; T² 71%, hybrid 69%, Q 73% after summer re-baselining.
* Oil: 38–41 °C in the overlap, 50–53 °C from July to September; the overlap saw three seal-extrusion faults.
* Last July and September are identical on per-sensor flags and returns; re-baselined T² caught 6 and 12.
* Calibration re-checks and sub-assembly scrap rows never touch the station log, the MES dispositions or the returns.

# DS40 — The cycle length a city files for its school-run corridor, when no retiming it can find would survive the authority's evaluation

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Supply Chain & Logistics · urban traffic signal operations |
| Mirrors | Shipping a tuned configuration only when its predicted gain clears the verification noise (ranking and pricing changes held because the experiment's noise floor exceeds the expected lift, cloud autoscaler retunes, fulfilment-centre slotting changes judged against control sites across seasons) |
| Decision shape | One figure committed at a date: the AM-peak cycle length filed in the corridor timing plan by 1 August, which may be the current 90 s (a hold forced by a blocking quantity) |
| Committed call | The cycle length filed in whole seconds, with the deciding figure: the change the authority's evaluation can detect, against the best plan's predicted saving |
| Gap · Pattern | Gap 1 (time) over Gap 4 (rule) · signal against noise (E28: the best predicted saving is smaller than the change a before-and-after evaluation across the summer break can detect, a floor the revision log's control corridors pin), with the coarsened design period (E18) at rung 1 |
| Gate G mechanism | signal_vs_noise_or_hold, with method_or_model_selection |
| Measured traps engaged | #26 picks a window across a documented confounder · #1 reports a failed back-test, ships anyway · #14 coarsens the segment it was asked about |
| Calibration form | Retry or revision log: six rounds of the regional authority's retiming evaluations, 14 corridor retimings with predicted savings, before-and-after daily travel times, control corridors, and whether each plan stood or was reverted |
| Driving force | The best retiming the delay model finds saves 6.0% of corridor travel time. The authority's evaluations compare 20 school days either side of the summer break, and term-to-term shifts move every corridor, retimed or not. In the revision log, a plan stood only when its saving beat twice the spread of the untouched control corridors, 5.2%. Nothing under 10.4% can be confirmed, and an unconfirmed plan is reverted. |

## 1. Situation

A city is retiming an eight-signal corridor before the new school year, after complaints about queues in the fifteen minutes before school
starts. The AM-peak cycle length goes into the corridor timing plan filed with the regional authority by 1 August; the current plan runs
90 s. The authority funds and confirms retimings through a before-and-after evaluation over 20 school days either side of the change, and
reverts plans it cannot confirm. The city's timing standard files a new cycle only where its predicted saving exceeds the change that
evaluation can detect. The consultant has sized the cycle on hourly volumes.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the hourly and 15-minute counts, the recounts, the delay model, the probe travel times and the
  revision log. No stakeholder read is overturned: the queues are real, and the model's best plan does save 6.0%. The difficulty is whether
  that saving can ever be shown.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the consultant's table and every voice. The delay model on the design flows still finds a better cycle, and
  within-term probe noise still says its saving is detectable.
* **Instrument repair.** Suspect file: the counts at two intersections, superseded by recounts after camera faults. Repaired, rung 0 still
  files 100 s, rung 1 a cycle at or near the controller's 120 s maximum and rung 2 112 s. Perfect travel-time measurement leaves the
  term-to-term shifts, which are real changes in school traffic, so the control-spread floor is still needed and the plan stays at 90 s.
* **Lens swap.** The naive read and the answer differ in moment: day-to-day variation within one term, against the change between June and
  September that every evaluation straddles.

## 3. The driving force

A strong solver sizes the cycle on the timing standard's design period (the peak 15 minutes of the school-start surge, not the hour),
uses the recounted volumes, finds the delay model's best cycle (112 s, saving 6.0%), and applies the standard's test. Measured as
within-term day-to-day variation in the probe archive, the evaluation's noise is small: 20 days either side gives a detectable change of
3.6%, and the plan passes. But the evaluation does not compare days within a term. It compares June with September, across the summer
break, and between terms school traffic shifts on every corridor: new intakes, changed bell times, moved bus routes. The authority
evaluates control corridors alongside every retiming, and their before-and-after changes, which nothing caused, spread with a standard
deviation of 5.2%. Across the six rounds in the revision log, a retiming stood exactly when its realised saving exceeded twice its round's
control spread: 14 of 14. Twice 5.2% is 10.4%, and no cycle the controller can run saves that much.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Webster's cycle on the consultant's hourly volumes | 100 s (+11.1%) | The textbook method on the table the consultant supplied | The timing standard: the design period is the peak 15 minutes of the school-start surge |
| 1 | Webster on peak 15-minute flows, at the controller's 120 s maximum | 120 s (+33.3%) | The standard's own design period, sized for the surge | The count revision log: two intersections were recounted after camera faults, and the recount supersedes the first count |
| 2 | Hygiene: recounted flows, the delay model's best cycle, and the standard's test with noise from within-term daily travel times | 112 s (+24.4%), saving 6.0% against a detectable 3.6% | Correct flows, the model's optimum, and the filing test passed | The revision log: the within-term noise rule reproduces 9 of 14 past outcomes, and every miss is a plan it would have confirmed that the authority reverted |
| 3 | **Decisive:** the detectable change is twice the control corridors' spread in the authority's evaluations, the rule that reproduces all 14 outcomes | **90 s, kept: 6.0% against a detectable 10.4%** | — | — |

* **Figure shape.** The answer is the minimum cell: every construction that files a new plan lands at least 11.1% above 90 s.
* **Blocking quantity.** The detectable change is 10.4%, 1.73× the best predicted saving of 6.0%. The hold is falsifiable: a predicted
  saving above 10.4%, or a pooled control spread under 3.0%, would have filed 112 s.
* **Discriminator dominance.** Rung 2's plan clears its test by 1.67× (6.0 against 3.6). The control spread multiplies the detectable
  change by 2.9× (10.4 against 3.6), against the required 1.2 × 1.67 = 2.0 and past the 2.6 that headroom asks, so the plan lands at 0.58
  of the line.
* **Partial correction priced (L3).** No half-applied test keeps 90 s; each files 112 s (+24.4%). A solver who requires the plan to beat
  the control spread once, not twice, finds 5.2% and files, 1.15× clear; the log refutes that rule on three retimings that beat one spread
  and were reverted. One who uses the control corridors but tests against their pooled day-to-day variation, not their corridor-to-corridor
  change across the break, finds 3.4% and files. One who scales within-term noise for 20 days without the cross-term shift stays at 3.6%
  and files.
* **Grid.** Design period (hour, peak 15) × counts (first, recount) × noise (within-term, the control spread once, twice the control
  spread) = 12 cells. The eight cells without the doubled spread file a new cycle at 100, 118, 120 or 112 s. The four with it hold at
  10.4%, and only the peak-15, recount cell among them states the best saving correctly as 6.0% (the hourly cells put it at 5.5% and
  5.7%, the peak-15, first-count cell at 7.2%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard says a plan must beat the change the evaluation can detect. The authority's protocol says what is
   compared. No document says how big that change is, or that the summer break sets it.
2. **The log pins it, as a construction.** Twice each round's control-corridor spread reproduces 14 of 14 past outcomes; the spread taken
   once reproduces 11, and within-term noise 9, every miss running the same way (plans the rule would confirm that were reverted). The
   spread is built from before-and-after differences on corridors nobody retimed, school days only, round by round, so no setting of the
   day-to-day model reaches it.
3. **No arithmetic symptom.** Counts, recounts, probe times and the delay model reconcile, and every rung's plan improves the model's
   delay.
4. **Not a row predicate.** The floor is a standard deviation across control corridors of differences between two windows' means, per
   round.
5. **The enumeration is arithmetic.** No column holds a detectable change or a noise figure.
6. **No cutover date.** The break is the same in every round and steps no series the decision reads; what matters is the spread it leaves.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, the model's best plan still passes the within-term test.

## 6. The calibration corpus

* **Form.** The revision log: six evaluation rounds, 14 retimings with their predicted saving, 20 school days of corridor travel times
  either side, the round's three control corridors over the same days, and the outcome (the plan stood, or was revised back).
* **What it pins.** The detectable change (above). The rounds' control spreads run from 5.0% to 5.4%; pooled, latest and averaged they
  all give 5.2%.
* **Twin pair.** Two control corridors in the 2019 round are identical on every within-term column the archive shows: eight signals, the
  same AM volume and the same day-to-day standard deviation of travel time, 2.1%. Their June-to-September changes were 3.8% and 7.6%
  (2.0×): the second carries a school whose intake grew across the break. Within-term noise cannot separate them; only the cross-term
  difference does.
* **Resemblance points at the decoy.** The corridor most resembles the 2019 retiming of the parallel avenue, which stood.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The timing standard: the design period is the peak 15 minutes of the school-start surge; a new cycle is filed only where
  its predicted saving exceeds the change the authority's evaluation can detect; otherwise the current plan stays. The authority's
  protocol: mean AM corridor travel time over 20 school days before and 20 after, with control corridors evaluated alongside; unconfirmed
  plans are reverted. The controller range: 60 to 120 s.
* **Empirical pins.** The detectable change, from the log's outcomes.
* **Voices.** The traffic engineer: "Webster's cycle is the textbook answer." The consultant: "Size for the surge and the queues go away."
  The schools liaison: "Parents will not accept another term of these queues."
* **Licensed wrong basis.** The standard records that the council's transport committee will see the consultant's hourly-volume timing
  table.

## 8. Determinism by construction

* **Delay model.** The standard's delay formula on the recounted peak-15 flows; its best cycle is 112 s, and no cycle from 60 to 120 s
  saves more than 6.0%.
* **School days.** The authority's calendar defines school days; every evaluation window holds exactly 20.
* **Spread.** Sample standard deviation across each round's three control corridors of the percentage change in mean travel time; the
  six rounds sit within 0.2 points of 5.2%, so pooling conventions converge.
* **Rounding.** The filed figure is a whole second, and the hold leaves it at 90.

## 9. Prompt sketch and deliverables

> The corridor's new timing plan goes to the regional authority by 1 August, and the consultant has sized the cycle on hourly volumes.
> Give me the AM-peak cycle length we file, in whole seconds, or tell me we keep 90, with the figure that decides it, as the line for the
> filing. Send `cycle_decision.xlsx`, a chart `saving_vs_detectable.png`, and a one-page `timing_filing_note.pdf`.

* `cycle_decision.xlsx` — each rung's cycle and predicted saving with the noise measures and the log's reproduction counts (ask C), the
  pedestrian sheet (ask A) and the camera sheet (ask B).
* `saving_vs_detectable.png` — predicted saving against cycle length from 60 to 120 s as a curve, with the within-term detectable change
  and the control-spread detectable change as two labelled horizontal lines, the 112 s optimum marked and the 14 past retimings as points,
  stood or reverted.
* `timing_filing_note.pdf` — the filed figure, the blocking quantity, and what would have justified a change.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the eight signals, pedestrian calls per school-day AM peak last term. *Device:*
  every button press is logged, and repeat presses within a cycle carry no "call registered" flag, as the controller log guide documents.
  Counting presses overstates calls at the school crossings by up to 4×.
* **Ask B (device-carried).** For each month of last year, red-light violations at the two camera signals. *Device:* two cameras cover
  each stop line, and the vendor's export flags a second image of the same plate within two seconds as a duplicate. Counting images
  overstates violations every month.
* **Ask C (validity).** Each rung's cycle and predicted saving, the detectable change under within-term noise and under the control
  spread, and each of the three noise rules' reproduction counts out of 14.
* **Decoupling.** Clearing the control-spread floor changes no figure in asks A or B. Pedestrian minimums are met by every candidate cycle,
  and button and camera logs touch no count, probe or evaluation record.

## 11. Rubric arithmetic

8 signals (ask A) + 12 months (ask B) + 4 rung cycles and savings + 2 detectable changes + 3 reproduction counts (ask C) + the filed
figure, the blocking quantity, the best predicted saving and the falsifier + 5 named chart parts + 3 files ≈ 47 criteria.

## 12. World-building constraints

* Rung figures 100 / 120 / 112 / 90 s; best predicted saving 6.0% at 112 s (5.5% and 5.7% on hourly flows, 7.2% on the peak-15 first
  count); within-term detectable change 3.6%, pooled daily controls 3.4%; control spreads 5.0–5.4% (5.2% pooled); detectable change 10.4%.
* Revision log: 14 retimings across six rounds; outcomes reproduced 14 of 14 by twice the round's control spread, 11 by the spread once,
  9 by within-term noise. The 2019 twin control corridors match on every within-term column.
* Two recounts supersede first counts. Pedestrian minimums never bind. Button and camera logs are independent of every main-call record.

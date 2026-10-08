# RC04 — Which of five delay causes on the commuter line gets this winter's one fix, when the cause that loses the most time is mostly a consequence

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Supply Chain & Logistics · commuter rail timetable performance |
| Mirrors | Latency attribution along multi-hop paths (a slow service hop that makes a downstream call miss its batch window, a late linehaul leg that makes a sort miss its wave at a parcel hub), where per-hop latency points at the hop where waiting happens and only a replay of the path shows which hop caused it |
| Decision shape | Which of N root causes gets the fix: one intervention budget this winter |
| Committed call | The cause fixed, the late peak arrivals at the terminal its fix would have avoided this autumn, and the same figure for the runner-up |
| Gap · Pattern | Gap 4 (rule) over Gap 3 (objective) · Pattern B (the published controls pin a path replay) carrying E22 (the deciding comparison is a set of isolated counterfactuals), with E21 (a saturated tie) at rung 1 |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #20 leaves the deciding comparison unstated · #1 reports a failed back-test, ships anyway · #19 breaks a big tie instead of questioning it |
| Calibration form | Published control set with a reproduction clause: twelve certified fault-free punctuality figures for closed disruptions on the line |
| Driving force | Read segment by segment, the single-track loop loses the most time, because inbound trains that arrive late at the meet wait four minutes for the opposing train. Most of those late arrivals were made late upstream, by dwell overruns at the interchange, which also hold the following train outside the platform. Only replaying each train's path in timetable order, with the preceding train's departure and the opposing train's clearance as inputs, sets the overruns' combined effect against the loop's own, and that comparison reverses the ranking. |

## 1. Situation

A regional commuter line's morning-peak inbound punctuality at the capital terminal (arrival within three minutes) fell from 94.0% last autumn to
86.0% this autumn: 151 late arrivals out of 1,080 trains. Five causes are on the table: conflicts in the terminal throat (A), a bridge speed
restriction imposed in June (B), meets at the single-track loop, re-timed in the autumn timetable (C), dwell overruns at the interchange station,
growing with a new housing district's ridership (D), and conflicts with long-distance trains at the junction (E). There is money for one fix this
winter. The infrastructure manager's performance standard governs how an investment case attributes punctuality.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the train-running records, the delay codes, the working timetable and the twelve published fault-free
  figures. Each cause's gained delay is measured correctly, and no stakeholder's reading of their own numbers is overturned. The difficulty is
  that the decision turns on combined effects that no segment-level figure contains.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the director's belief, both voices and the licensed basis. The running records still put the largest gained delay at
  the loop, and the delay codes still put it at the terminal.
* **Instrument repair.** Record every train's position to the second and every cause perfectly. The loop's waits are still real waits, and
  whether they would vanish with the interchange fixed is still a counterfactual that only a path replay answers.
* **Lens swap.** The gained-delay ranking describes where this autumn's trains lost time. The answer is a set of counterfactual autumns, one
  per fix: different trains are late in each, so it is not one population under another lens.

## 3. The driving force

A strong solver knows delay is noticed at the terminal and gained upstream, so it computes delay gained per segment and per dwell, and the loop
wins clearly. That reading takes each segment one at a time. A train that leaves the interchange 75 seconds late reaches the loop after the
opposing train has claimed the single line, waits four minutes, and arrives at the terminal late although its own segment times were normal.
The following train, held outside the interchange platform, inherits part of the overrun as well. The interchange's own gained delay is small,
but the comparison that decides the fix is between whole autumns: each train's path replayed in timetable order with one cause removed, with
the working timetable's allowances absorbing what they can, the preceding train setting the platform release and the opposing train setting the
meet. Replayed that way, removing the overruns avoids 96 late arrivals and removing the loop's waits 61.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Minutes on late trains by the delay-cause code recorded at the terminal | A, terminal throat (610 min) | The codes are the operator's own attribution, and they are complete | The coding guide records a cause where a train's lateness crosses three minutes, at the point of observation; the published controls reproduce 0 of 12 under coded minutes |
| 1 | Incidence: share of late trains that lost at least 30 s at each location; A and B tie at 100%, and the standard's filed two-level tie-break (first the location further upstream, then the larger mean loss per affected train) settles it at level one and names B | B, bridge restriction | It is the standard's own incidence measure, settled by the standard's own filed tie-break | The working timetable under-times both locations against recovery allowances, so every train loses time there by design; incidence reproduces 2 of 12 controls |
| 2 | Gross delay gained per segment and per dwell, summed over the peak | C, single-track loop (1,320 min) | Delay is attributed where it is gained, the textbook correction | The controls: gross subtraction reproduces 7 of 12, missing every disruption whose trains were followed within the platform headway or met at the loop |
| 3 | **Decisive:** for each cause, every peak train's path replayed in timetable order without that cause, and the late arrivals avoided compared across causes | **D, interchange dwell overruns (96 avoided)** (5th of 5 on rung 0) | — | — |

* **Position table.** D ranks 5th on rung 0, 4th on rung 1 and 3rd on rung 2, and leads only rung 3. Rung 0's leader beats its runner-up by
  1.61×, rung 2's by 1.47× and rung 3's by 1.57× (96 against the loop's 61). Rung 1 is a designed exact tie (1.00×): A and B sit at 100% under
  every cut-off from 15 to 60 s. The standard's filed two-level tie-break decides it at level one, the location further upstream, and names B,
  the bridge restriction, 14 km upstream of the throat; level two (mean loss per affected train) is never reached. The third candidate trails
  at 73% (1.37×) and D at 55% (1.82×).
* **Discriminator dominance.** The loop carries a 1.78× gross-gain advantage into rung 3 (1,320 against 742 minutes). Late arrivals avoided
  per gained minute are 0.129 for D and 0.046 for C, an edge of 2.80×, 1.31 times the required 1.2 × 1.78 = 2.14; the net margin is 1.57×.
* **Partial correction priced (L3).** A solver who replays paths with the allowances but treats trains independently (no platform headway)
  credits D with only the meets it causes, 58 avoided against the loop's 61, and names C, rung 2's answer. One who replays with first-come
  meets moves the waits onto outbound trains outside the measure and names A.
* **Grid.** Attribution (coded, incidence, gross, replay) × headway knock-on (off, on) × meet order (first-come, timetabled) gives six
  distinct builds. Coded, incidence and gross name A, B and C; the three incomplete replays name C or A; only the full replay names D, and it
  alone reproduces all twelve controls.
* **The deciding comparison (#20).** 96 late arrivals avoided by fixing the overruns against 61 by fixing the loop is the sentence the board
  note has to carry; no segment-level table contains it.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard requires reproduction of the published figures and does not say how they were produced. No document
   describes meet order, headway knock-on or a replay.
2. **The controls pin a construction, not a menu.** The full replay reproduces 12 of 12 published figures to 0.1 point; the best rival (replay
   without headway) reproduces 9, first-come meets 8, gross subtraction 7, incidence 2. Every rival's misses understate the punctuality the line
   would have had, so none reconciles on the twelve-control total either. The replay has no parameter: its inputs are the working timetable's
   running times, allowances, minimum dwells and headways, and the observed positions of the trains around each train.
3. **No arithmetic symptom.** Gained delay sums to each train's terminal lateness on every rung; train counts, codes and segments reconcile.
4. **Not a row predicate.** Each train's counterfactual depends on the train ahead of it at the interchange and the opposing train at the loop,
   so it needs trains ordered within the peak and events replayed in sequence.
5. **The enumeration is arithmetic.** Which late arrivals each fix avoids is the output of 1,080 replays per cause; no column marks them.
6. **No cutover date.** The overruns grew with ridership over the year; the dated events (the June restriction, the autumn timetable) step the
   series for B, C and E and are the decoys.
7. **Survives deletion.** With every voice and code removed, the gained-delay table still names the loop.

## 6. The calibration corpus

* **Form.** The performance board's published control set: twelve closed disruptions on the line over three years, each with its dates,
  location, trains affected and the certified fault-free punctuality (what the line would have recorded without it), plus the standard's
  clause that an investment case may use an attribution method only if it reproduces every published figure to one decimal.
* **What it pins.** The full replay (12 of 12) against the rivals above. The running records for each control period ship, so every rival
  can be scored.
* **Twin pair.** Controls CP-03 and CP-09 are dwell overruns at the interchange, identical in overrun minutes, trains affected (24), time band,
  weekday mix and period length. Their published fault-free gains are 1.9 and 4.1 points (2.16×): in CP-09 the overrun trains were followed
  within the platform headway and reached the loop inside the meet window. Only the replay reproduces both.
* **Every rule exercised.** One control is a loop disruption with no upstream lateness, one an overrun with no following train inside the
  headway, and one a terminal-throat disruption with no downstream allowance, so each element of the replay is tested on its own.
* **Resemblance points at the decoy.** This autumn's loss pattern, long waits at the loop, most resembles CP-05, a loop disruption whose
  published gain is the largest in the set.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The board's investment rule: an intervention is judged on the late arrivals at the terminal it would have avoided over the
  autumn peak. The standard's reproduction clause, one sentence. The standard's two-level tie-break for its incidence measure: tied locations
  are ordered first by distance upstream of the terminal, then by mean seconds lost per affected train. The working timetable (running times,
  allowances, minimum dwells, the interchange headway, the planned meets).
* **Empirical pins.** Meet order (timetabled order held) and the headway knock-on, both recovered from the controls.
* **Voices.** The operations manager: "Everything bunches in the throat; that's where we lose the trains." The infrastructure planner: "The loop
  is the bottleneck. Since the timetable change trains have stood there every morning."
* **Licensed wrong basis.** The standard records that the operator's performance team attributes punctuality loss by the cause codes
  recorded at the terminal and will present that attribution at the board.

## 8. Determinism by construction

* **Lateness.** Late means arrival at the terminal more than 180 s after schedule; the peak is origin departures from 06:30 to 09:00; cancelled
  trains are outside the measure under the standard.
* **Counterfactual.** Removing a cause sets its excess over the working timetable to zero at its own location only; every later event is
  replayed in timetable order with observed running wherever no constraint binds.
* **Thresholds.** The incidence cut-off is immaterial: the A–B tie holds from 15 to 60 s, and under every cut-off the filed two-level
  tie-break settles it at level one (the bridge lies upstream of the throat) and names B.
* **Interactions.** Each fix is replayed alone, so the ranking needs no joint convention; the 96 and 61 do not sum with each other.
* **Rounding.** Late arrivals are whole trains; the committed figures are exact counts.

## 9. Prompt sketch and deliverables

> There's money for one fix on the commuter line this winter, and the director is sure the bridge restriction is what broke the morning peak.
> Name the cause we fix, how many of this autumn's late peak arrivals at the terminal it would have saved, and what the next-best fix would
> have saved, as two sentences for the board. Send `peak_fix_case.xlsx`, a chart `fix_comparison.svg` and a one-page `board_note.docx`.

* `peak_fix_case.xlsx` — the five causes under each construction, the passenger-count sheet (ask A), the cancellation sheet (ask B) and the
  control reproduction (ask C).
* `fix_comparison.svg` — a slope chart from each cause's gross gained minutes to its late arrivals avoided, with the punctuality the line would
  have recorded under each fix as point labels, last autumn's 94.0% as a reference line, and the chosen cause highlighted.
* `board_note.docx` — the committed cause, its figure and the runner-up's.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 14 stations, mean weekday boardings and alightings in the autumn peak. *Device:*
  coupled trains report counts once per unit under one train number, each row carrying its unit id, as the counting system's guide documents;
  de-duplicating on train number drops the second unit and understates nine stations by about a third.
* **Ask B (device-carried).** Cancelled peak trips by cause group for each of the twelve autumn weeks. *Device:* a trip that terminates
  short is marked cancelled only on the stops it skipped, and the standard counts a trip as cancelled when it does not reach the terminal;
  counting any trip with a cancelled stop over-counts, and counting only fully cancelled trips under-counts.
* **Ask C (validity).** For each of the twelve controls, the published figure and the figure each of the five constructions reproduces.
* **Decoupling.** Clearing the replay changes no figure in asks A or B; ask B's trips are outside the punctuality measure.

## 11. Rubric arithmetic

14 stations × 2 figures (ask A) + 12 weeks × 4 cause groups (ask B) + 12 controls × 5 constructions (ask C) + the committed cause, its figure
and the runner-up's + 5 named chart parts + 3 files ≈ 145 criteria.

## 12. World-building constraints

* 1,080 peak inbound trains, 151 late. Coded minutes A 610, E 380, C 250, B 120, D 60; incidence A and B 100%, C 73%, D 55%, E 41%; gross gains
  C 1,320, B 900, D 742, A 700, E 520; replay avoidances D 96, C 61, A 40, E 30, B 18.
* Overruns average 75 s on 55% of trains; a train more than 60 s late at the loop waits for the opposing train; the interchange headway is
  three minutes.
* The twelve controls: replay 12/12, no-headway 9/12, first-come meets 8/12, gross 7/12, incidence 2/12, all misses one way.
* CP-03 and CP-09 are identical on every published column.
* Passenger-count unit rows and short-terminated trips touch no train in the punctuality measure's replay.
